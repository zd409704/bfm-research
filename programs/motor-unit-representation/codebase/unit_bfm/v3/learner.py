"""Asymmetric, reward-free FB training; independent matched goals supplied by replay."""
import copy
from contextlib import contextmanager
from dataclasses import asdict, dataclass
import torch
from torch import nn
from .schema import VERSION, SCHEMA_VERSION, SCHEMA_HASH, ESTIMATOR_VERSION, G_DIM, X_DIM, Z_DIM
from .networks import Networks, orthogonal_init
from .fb_loss import fb_loss, actor_loss, sample_action
from .stage2_norms import matched_pair_mask, sanitize_privileged_tensor


@dataclass(frozen=True)
class LearnerConfig:
    lr: float = 1e-4
    polyak: float = .01
    action_std: float = .2
    action_clip: float = .3

    def __post_init__(self):
        if not (0 < self.lr and 0 <= self.polyak <= 1 and self.action_std >= 0 and self.action_clip >= 0):
            raise ValueError('Invalid learner configuration')
        if not all(torch.isfinite(torch.tensor(v)) for v in asdict(self).values()):
            raise ValueError('Nonfinite learner configuration')


@contextmanager
def frozen_forward(net):
    """Freeze F weights while preserving dF/du for the Actor."""
    params = list(net.f1.parameters())+list(net.f2.parameters())
    flags = [p.requires_grad for p in params]
    try:
        for p in params:
            p.requires_grad_(False)
        yield
    finally:
        for p,flag in zip(params,flags):
            p.requires_grad_(flag)


class Learner:
    def __init__(self,p_dim,device='cpu',seed=61001,config=None):
        self.device = torch.device(device)
        self.config = config if isinstance(config,LearnerConfig) else LearnerConfig(**(config or {}))
        self.p_dim = p_dim
        # Initialization does not consume a caller's independent global CPU stream.
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed)
            self.net = Networks(p_dim)
            self.net.apply(orthogonal_init)
        self.net.to(self.device)
        self.generator = torch.Generator(device=self.device).manual_seed(seed+1)
        self.target = nn.ModuleDict({k:copy.deepcopy(getattr(self.net,k)) for k in ('f1','f2','b')})
        self.target.requires_grad_(False)
        self.f_params = list(self.net.f1.parameters())+list(self.net.f2.parameters())
        self.forward_opt = torch.optim.Adam(self.f_params,lr=self.config.lr)
        self.backward_opt = torch.optim.Adam(self.net.b.parameters(),lr=self.config.lr)
        self.actor_opt = torch.optim.Adam(self.net.actor.parameters(),lr=self.config.lr)
        self.updates = 0
        self.last_goal_fraction = 0.
        self.sanitize_calls = 0
        self.last_sanitize = {'applied': False, 'consumed_violations': 0, 'freeze_normalizer': False}

    @torch.no_grad()
    def sample_z(self,n,goal_g=None,goal_valid=None):
        if n < 1:
            raise ValueError('n must be positive')
        z = Z_DIM**.5*torch.nn.functional.normalize(
            torch.randn(n,Z_DIM,device=self.device,generator=self.generator),dim=-1)
        if (goal_g is None) != (goal_valid is None):
            raise ValueError('Provide both goal_g and goal_valid')
        if goal_g is None:
            self.last_goal_fraction = 0.
            return z.detach()
        goal_g = torch.as_tensor(goal_g,dtype=torch.float32,device=self.device).detach()
        valid = torch.as_tensor(goal_valid,device=self.device)
        if goal_g.shape != (n,G_DIM) or valid.shape != (n,):
            raise ValueError('Expected independent goal_g [N,13], goal_valid [N]')
        if not torch.all((valid==0)|(valid==1)) or not torch.isfinite(goal_g).all():
            raise ValueError('Invalid goal input')
        choose = (torch.rand(n,device=self.device,generator=self.generator)<.5)&valid.bool()
        # No permutation: each complete goal remains matched to its transition configuration.
        if choose.any():
            z[choose] = self.net.b(goal_g[choose])
        self.last_goal_fraction = float(choose.float().mean())
        return z.detach()

    def _batch(self,batch):
        dims = {'x':X_DIM,'p':self.p_dim,'u':1,'x_next':X_DIM,'p_next':self.p_dim,
                'g_next':G_DIM,'discount':1,'goal_g':G_DIM}
        out = {k:torch.as_tensor(batch[k],dtype=torch.float32,device=self.device).detach() for k in dims}
        n = len(out['x'])
        if n < 2:
            raise ValueError('FB batch requires at least two rows')
        for k,d in dims.items():
            if out[k].shape != (n,d) or not torch.isfinite(out[k]).all():
                raise ValueError(f'Invalid batch {k}: expected finite [{n},{d}]')
        out['goal_valid'] = torch.as_tensor(batch['goal_valid'],device=self.device).detach()
        if out['goal_valid'].shape != (n,) or not torch.all((out['goal_valid']==0)|(out['goal_valid']==1)):
            raise ValueError('goal_valid must be binary [N]')
        if torch.any((out['discount']<0)|(out['discount']>1)):
            raise ValueError('Discount outside [0,1]')
        if torch.any(out['u'].abs()>1+1e-6):
            raise ValueError('Canonical action outside [-1,1]')
        # Lengths and limits define the goal group; capacity/mass/beta are not goal keys.
        valid = out['goal_valid'].bool()
        idx = [0,1,5,6]
        if not torch.allclose(out['goal_g'][valid][:,idx],out['x'][valid][:,idx],atol=1e-6,rtol=1e-6):
            raise ValueError('goal_g must match each transition geometry and limits')
        return out

    def _action(self,mean):
        return sample_action(mean,self.config.action_std,self.config.action_clip,self.generator)

    @torch.no_grad()
    def target_density(self,x_next,p_next,g_next,z):
        u_next = self._action(self.net.actor(x_next,z))
        y_next = torch.cat((x_next,p_next),-1)
        future = .5*(self.target['f1'](y_next,u_next,z)+self.target['f2'](y_next,u_next,z))
        return future @ self.target['b'](g_next).T

    @staticmethod
    def grad_norm(parameters):
        norms = [p.grad.detach().square().sum() for p in parameters if p.grad is not None]
        return torch.stack(norms).sum().sqrt() if norms else torch.tensor(0.)

    @torch.no_grad()
    def polyak(self):
        for name in ('f1','f2','b'):
            for online,target in zip(getattr(self.net,name).parameters(),self.target[name].parameters()):
                target.lerp_(online,self.config.polyak)

    def update(self,batch):
        future = batch.get('future_slice') if isinstance(batch, dict) else None
        lag = batch.get('lag_slice') if isinstance(batch, dict) else None
        config_id = batch.get('config_id') if isinstance(batch, dict) else None
        batch = self._batch(batch)
        # B01: every forward call consumes a sanitized privileged tensor.
        batch['p'], rep_p = sanitize_privileged_tensor(batch['p'], future, lag)
        batch['p_next'], rep_n = sanitize_privileged_tensor(batch['p_next'], future, lag)
        self.sanitize_calls += 1
        self.last_sanitize = {
            'applied': bool(rep_p['applied'] or rep_n['applied']),
            'consumed_violations': int(rep_p['consumed_violations'] + rep_n['consumed_violations']),
            'freeze_normalizer': bool(rep_p['freeze_normalizer'] or rep_n['freeze_normalizer']),
        }
        x,p,u = (batch[k] for k in ('x','p','u'))
        z = self.sample_z(len(x),batch['goal_g'],batch['goal_valid'])
        target = self.target_density(batch['x_next'],batch['p_next'],batch['g_next'],z)
        y = torch.cat((x,p),-1)
        forwards = torch.stack((self.net.f1(y,u,z),self.net.f2(y,u,z)))
        backward = self.net.b(batch['g_next'])
        pair_mask = None
        if config_id is not None:
            pair_mask = matched_pair_mask(torch.as_tensor(config_id, device=self.device)).to(dtype=backward.dtype)
        total,offdiag,positive,orth = fb_loss(forwards,backward,target,batch['discount'],pair_mask)
        if not torch.isfinite(total):
            raise FloatingPointError('Nonfinite FB loss')
        self.forward_opt.zero_grad(set_to_none=True)
        self.backward_opt.zero_grad(set_to_none=True)
        total.backward()
        f_grad = self.grad_norm(self.f_params)
        b_grad = self.grad_norm(self.net.b.parameters())
        if not torch.isfinite(f_grad+b_grad):
            raise FloatingPointError('Nonfinite F/B gradients')
        self.forward_opt.step(); self.backward_opt.step()
        self.forward_opt.zero_grad(set_to_none=True)
        self.backward_opt.zero_grad(set_to_none=True)
        self.actor_opt.zero_grad(set_to_none=True)
        with frozen_forward(self.net):
            action = self._action(self.net.actor(x,z))
            # B02: keep a direct logit path so saturation does not erase the actor gradient.
            logit = self.net.actor.logits(x,z)
            hinge = torch.relu(logit.abs() - 3.0).mean()
            af = torch.stack((self.net.f1(y,action,z),self.net.f2(y,action,z)))
            policy = actor_loss(af,z) + 1e-3 * hinge
            if not torch.isfinite(policy):
                raise FloatingPointError('Nonfinite Actor loss')
            policy.backward()
            actor_grad = self.grad_norm(self.net.actor.parameters())
            if not torch.isfinite(actor_grad):
                raise FloatingPointError('Nonfinite Actor gradients')
            self.actor_opt.step()
        self.polyak(); self.updates += 1
        return {k:float(v) for k,v in dict(fb=total.detach(),fb_offdiag=offdiag.detach(),
            fb_positive=positive.detach(),orth=orth.detach(),actor=policy.detach(),f_grad=f_grad,
            b_grad=b_grad,actor_grad=actor_grad,f_rms=forwards.detach().square().mean().sqrt(),
            b_norm=backward.detach().norm(dim=-1).mean(),target_density_rms=target.square().mean().sqrt(),
            goal_fraction=self.last_goal_fraction,updates=self.updates).items()}

    def state_dict(self):
        return copy.deepcopy(dict(version=VERSION,schema_version=SCHEMA_VERSION,schema_hash=SCHEMA_HASH,
            estimator_version=ESTIMATOR_VERSION,p_dim=self.p_dim,config=asdict(self.config),
            net=self.net.state_dict(),target=self.target.state_dict(),forward_opt=self.forward_opt.state_dict(),
            backward_opt=self.backward_opt.state_dict(),actor_opt=self.actor_opt.state_dict(),
            generator=self.generator.get_state(),updates=self.updates))

    def load_state_dict(self,state):
        required = dict(version=VERSION,schema_version=SCHEMA_VERSION,schema_hash=SCHEMA_HASH,
                        estimator_version=ESTIMATOR_VERSION,p_dim=self.p_dim,config=asdict(self.config))
        for key,value in required.items():
            if state.get(key) != value:
                raise ValueError(f'Refuse incompatible V2/foreign checkpoint: {key}')
        self.net.load_state_dict(state['net'],strict=True)
        self.target.load_state_dict(state['target'],strict=True)
        self.target.requires_grad_(False)
        for name in ('forward_opt','backward_opt','actor_opt'):
            getattr(self,name).load_state_dict(state[name])
        self.generator.set_state(state['generator'].cpu())
        self.updates = int(state['updates'])
