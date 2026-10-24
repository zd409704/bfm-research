"""Reward-free FB baseline. Rewards appear only in no-grad post-training queries."""
import copy
import numpy as np
import torch
from torch import nn
from . import VERSION
from .networks import Networks, orthogonal_init, physical_result
from .tasks import project
from .fb_loss import fb_loss, actor_loss, sample_action


class Learner:
    metric_names = ('fb_offdiag', 'fb_positive', 'orth', 'actor', 'f_grad', 'b_grad',
                    'actor_grad', 'f_rms', 'b_norm', 'target_density_rms')

    def __init__(self, reference, device='cuda:0', seed=61001):
        self.device = device
        self.rng = np.random.default_rng(seed)
        self.net = Networks().to(device)
        self.net.apply(orthogonal_init)
        self.target = nn.ModuleDict({name: copy.deepcopy(getattr(self.net, name))
                                    for name in ('f1', 'f2', 'b')}).requires_grad_(False)
        self.f_params = list(self.net.f1.parameters()) + list(self.net.f2.parameters())
        self.forward_opt = torch.optim.Adam(self.f_params, lr=1e-4)
        self.backward_opt = torch.optim.Adam(self.net.b.parameters(), lr=1e-4)
        self.actor_opt = torch.optim.Adam(self.net.actor.parameters(), lr=1e-4)
        self.updates = 0
        self.set_reference(reference, source='P0_initial_query_only')

    @torch.no_grad()
    def set_reference(self, reference, source='current_replay'):
        self.reference = reference.to(self.device)
        self.reference_source = source
        ids = self.rng.choice(len(reference), min(4096, len(reference)), replace=False)
        self.cache_ids = torch.as_tensor(ids, device=self.device)
        self.refresh()

    @torch.no_grad()
    def refresh(self):
        from .tasks import reward_features
        self.reference_features = reward_features(self.reference)
        b = self.net.b(physical_result(self.reference[self.cache_ids]))
        self.cov = b.T @ b / len(b)
        self.cross = b.T @ self.reference_features[self.cache_ids] / len(b)
        eps = 1e-3 * self.cov.trace() / 16 + 1e-6
        self.inverse = torch.linalg.inv(self.cov + eps * torch.eye(16, device=self.device))

    @torch.no_grad()
    def encode(self, alpha):
        from .tasks import reward_weights
        weights = reward_weights(torch.as_tensor(alpha, device=self.device, dtype=torch.float32))
        weights[:, 10] = 0  # V2 query has no command magnitude/change penalty.
        return project(weights @ self.cross.T)

    @torch.no_grad()
    def sample_z(self, n, goals=None):
        random_z = project(torch.randn(n, 16, device=self.device))
        if goals is None:
            ids = torch.as_tensor(self.rng.integers(len(self.reference), size=n), device=self.device)
            goals = self.reference[ids]
        perm = torch.randperm(n, device=self.device)
        goal_z = project(self.net.b(physical_result(goals[perm])))
        return torch.where(torch.rand(n, 1, device=self.device) < .5, goal_z, random_z)

    @torch.no_grad()
    def polyak(self):
        for name in ('f1', 'f2', 'b'):
            for online, target in zip(getattr(self.net, name).parameters(), self.target[name].parameters()):
                target.lerp_(online, .01)

    @staticmethod
    def grad_norm(parameters):
        return torch.stack([p.grad.detach().square().sum() for p in parameters if p.grad is not None]).sum().sqrt()

    def update(self, batch):
        x, u, xp, y = batch
        goal = physical_result(y)
        z = self.sample_z(len(x), y).detach()
        with torch.no_grad():
            up = sample_action(self.net.actor(xp, z))
            future = .5 * (self.target['f1'](xp, up, z) + self.target['f2'](xp, up, z))
            target_density = future @ self.target['b'](goal).T
        forwards = torch.stack((self.net.f1(x, u, z), self.net.f2(x, u, z)))
        backward = self.net.b(goal)
        total, offdiag, positive, orth = fb_loss(forwards, backward, target_density)
        if not torch.isfinite(total):
            raise FloatingPointError('Nonfinite FB loss')
        self.forward_opt.zero_grad(set_to_none=True)
        self.backward_opt.zero_grad(set_to_none=True)
        total.backward()
        f_grad = self.grad_norm(self.f_params)
        b_grad = self.grad_norm(self.net.b.parameters())
        if not torch.isfinite(f_grad + b_grad):
            raise FloatingPointError('Nonfinite F/B gradient')
        self.forward_opt.step()
        self.backward_opt.step()
        self.net.f1.requires_grad_(False)
        self.net.f2.requires_grad_(False)
        action = sample_action(self.net.actor(x, z))
        actor_forwards = torch.stack((self.net.f1(x, action, z), self.net.f2(x, action, z)))
        policy_loss = actor_loss(actor_forwards, z)
        self.actor_opt.zero_grad(set_to_none=True)
        policy_loss.backward()
        actor_grad = self.grad_norm(self.net.actor.parameters())
        if not torch.isfinite(actor_grad):
            raise FloatingPointError('Nonfinite Actor gradient')
        self.actor_opt.step()
        self.net.f1.requires_grad_(True)
        self.net.f2.requires_grad_(True)
        self.polyak()
        self.updates += 1
        return torch.stack([offdiag.detach(), positive.detach(), orth.detach(), policy_loss.detach(),
                            f_grad, b_grad, actor_grad, forwards.detach().square().mean().sqrt(),
                            backward.detach().norm(dim=-1).mean(), target_density.square().mean().sqrt()])

    @torch.no_grad()
    def diagnostics(self):
        from .tasks import sample_tasks, reward_weights
        self.refresh()
        ids = torch.as_tensor(self.rng.choice(len(self.reference), min(1024, len(self.reference)), replace=False),
                              device=self.device)
        alpha = torch.as_tensor(sample_tasks(self.rng, 128), device=self.device)
        weights = reward_weights(alpha)
        weights[:, 10] = 0
        target = self.reference_features[ids] @ weights.T
        pred = self.net.b(physical_result(self.reference[ids])) @ self.inverse @ self.cross @ weights.T
        nrmse = (pred-target).square().mean(0).sqrt() / (target.square().mean(0).sqrt()+1e-6)
        eig = torch.linalg.eigvalsh(self.cov)
        return dict(projection_nrmse=float(nrmse.mean()), projection_nrmse_max=float(nrmse.max()),
                    covariance_eigenvalues=eig.cpu().tolist(), effective_rank=int((eig > 1e-3).sum()),
                    reference_source=self.reference_source)

    def state_dict(self):
        return dict(version=VERSION, net=self.net.state_dict(), target=self.target.state_dict(),
                    actor_opt=self.actor_opt.state_dict(), forward_opt=self.forward_opt.state_dict(),
                    backward_opt=self.backward_opt.state_dict(), updates=self.updates,
                    rng=self.rng.bit_generator.state, reference=self.reference.cpu(),
                    reference_source=self.reference_source, cache_ids=self.cache_ids.cpu())

    def load_state_dict(self, state):
        if state.get('version') != VERSION:
            raise ValueError('Refuse to resume another algorithm/schema version')
        self.net.load_state_dict(state['net'])
        self.target.load_state_dict(state['target'])
        self.actor_opt.load_state_dict(state['actor_opt'])
        self.forward_opt.load_state_dict(state['forward_opt'])
        self.backward_opt.load_state_dict(state['backward_opt'])
        self.updates = state['updates']
        self.rng.bit_generator.state = state['rng']
        self.reference = state['reference'].to(self.device)
        self.reference_source = state['reference_source']
        self.cache_ids = state['cache_ids'].to(self.device)
        self.refresh()
