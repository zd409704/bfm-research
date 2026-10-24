"""Online FB over transition results with a fixed, independent reference pool."""
import copy
import numpy as np
import torch
from .networks import Networks
from .tasks import sample_tasks,reward_features,reward_weights,project


class Learner:
    def __init__(self,reference,device='cuda:0',seed=61001):
        self.device=device
        self.rng=np.random.default_rng(seed)
        self.net=Networks().to(device)
        self.target=copy.deepcopy(self.net).requires_grad_(False)
        self.critic_params=list(self.net.f1.parameters())+list(self.net.f2.parameters())+list(self.net.b.parameters())
        self.critic_opt=torch.optim.Adam([
            {'params':list(self.net.f1.parameters())+list(self.net.f2.parameters()),'lr':3e-4},
            {'params':self.net.b.parameters(),'lr':1e-4}])
        self.actor_opt=torch.optim.Adam(self.net.actor.parameters(),lr=3e-4)
        self.reference=reference.to(device)
        self.reference_features=reward_features(self.reference)
        self.cache_ids=torch.as_tensor(self.rng.choice(len(reference),4096,replace=False),device=device)
        self.updates=0
        self.refresh()

    @torch.no_grad()
    def refresh(self):
        self.cached_b=self.net.b(self.reference[self.cache_ids])
        self.cov=self.cached_b.T@self.cached_b/len(self.cached_b)
        self.cross=self.cached_b.T@self.reference_features[self.cache_ids]/len(self.cached_b)
        eps=1e-3*self.cov.trace()/16+1e-6
        self.inverse=torch.linalg.inv(self.cov+eps*torch.eye(16,device=self.device))

    @torch.no_grad()
    def encode(self,alpha):
        a=torch.as_tensor(alpha,device=self.device,dtype=torch.float32)
        return project(reward_weights(a)@self.cross.T)

    def sample_z(self,n):
        alpha=torch.as_tensor(sample_tasks(self.rng,n),device=self.device)
        z=self.encode(alpha)
        random_mask=torch.as_tensor(self.rng.random(n)<.2,device=self.device)
        random_z=project(torch.randn_like(z))
        return torch.where(random_mask[:,None],random_z,z)

    @torch.no_grad()
    def polyak(self,source,target):
        for p,q in zip(source.parameters(),target.parameters()): q.lerp_(p,.005)

    def update(self,batch):
        x,u,xp,y=batch
        if self.updates%100==0: self.refresh()
        z=self.sample_z(len(x)).detach()
        ids=torch.as_tensor(self.rng.integers(len(self.reference),size=len(x)),device=self.device)
        yr=self.reference[ids]
        with torch.no_grad():
            noise=(.1*torch.randn_like(u)).clamp(-.2,.2)
            up=(self.target.actor(xp,z)+noise).clamp(-1,1)
            future=.5*(self.target.f1(xp,up,z)+self.target.f2(xp,up,z))
            target_density=.99*future@self.target.b(yr).T
        f1=self.net.f1(x,u,z); f2=self.net.f2(x,u,z)
        br=self.net.b(yr); by=self.net.b(y)
        # Independent rho integral: no diagonal mask (unlike same-batch UFO goals).
        integral=.5*((f1@br.T-target_density).square().mean()+(f2@br.T-target_density).square().mean())
        positive=-((f1*by).sum(-1).mean()+(f2*by).sum(-1).mean())
        fb=integral+positive
        cov=br.T@br/len(br)
        orth=(cov-torch.eye(16,device=self.device)).square().sum()/16
        alpha=torch.as_tensor(sample_tasks(self.rng,64),device=self.device)
        weights=reward_weights(alpha)
        with torch.no_grad():
            beta=(self.inverse@self.cross@weights.T).detach()
        # New independent rho draw, not the covariance/encoding sample set.
        tid=torch.as_tensor(self.rng.integers(len(self.reference),size=1024),device=self.device)
        prediction=self.net.b(self.reference[tid])@beta
        expected=self.reference_features[tid]@weights.T
        task=(prediction-expected).square().mean()
        loss=fb+orth+task
        if not torch.isfinite(loss): raise FloatingPointError('Nonfinite FB loss')
        self.critic_opt.zero_grad(set_to_none=True)
        loss.backward()
        grad=torch.nn.utils.clip_grad_norm_(self.critic_params,10.)
        self.critic_opt.step()
        for name in ('f1','f2','b'): self.polyak(getattr(self.net,name),getattr(self.target,name))
        actor_loss=torch.zeros((),device=self.device); actor_grad=torch.zeros_like(actor_loss)
        if self.updates%2==0:
            self.net.f1.requires_grad_(False); self.net.f2.requires_grad_(False)
            action=self.net.actor(x,z)
            q1=(self.net.f1(x,action,z)*z).sum(-1)
            q2=(self.net.f2(x,action,z)*z).sum(-1)
            actor_loss=-torch.minimum(q1,q2).mean()
            self.actor_opt.zero_grad(set_to_none=True)
            actor_loss.backward()
            actor_grad=torch.nn.utils.clip_grad_norm_(self.net.actor.parameters(),10.)
            self.actor_opt.step()
            self.net.f1.requires_grad_(True); self.net.f2.requires_grad_(True)
            self.polyak(self.net.actor,self.target.actor)
        self.updates+=1
        return torch.stack([fb.detach(),orth.detach(),task.detach(),actor_loss.detach(),grad.detach(),actor_grad.detach()])

    @torch.no_grad()
    def diagnostics(self):
        self.refresh()
        indices=torch.as_tensor(self.rng.choice(len(self.reference),1024,replace=False),device=self.device)
        alpha=torch.as_tensor(sample_tasks(self.rng,128),device=self.device)
        weights=reward_weights(alpha)
        target=self.reference_features[indices]@weights.T
        pred=self.net.b(self.reference[indices])@self.inverse@self.cross@weights.T
        rmse=(pred-target).square().mean(0).sqrt()
        nrmse=rmse/(target.square().mean(0).sqrt()+1e-6)
        eig=torch.linalg.eigvalsh(self.cov)
        return dict(projection_nrmse=float(nrmse.mean()),projection_nrmse_max=float(nrmse.max()),
                    covariance_eigenvalues=eig.cpu().tolist(),effective_rank=int((eig>1e-3).sum()))

    def state_dict(self):
        return dict(net=self.net.state_dict(),target=self.target.state_dict(),
                    actor_opt=self.actor_opt.state_dict(),critic_opt=self.critic_opt.state_dict(),
                    updates=self.updates,rng=self.rng.bit_generator.state,cache_ids=self.cache_ids.cpu())

    def load_state_dict(self,state):
        self.net.load_state_dict(state['net']); self.target.load_state_dict(state['target'])
        self.actor_opt.load_state_dict(state['actor_opt']); self.critic_opt.load_state_dict(state['critic_opt'])
        self.updates=state['updates']; self.rng.bit_generator.state=state['rng']
        self.cache_ids=state['cache_ids'].to(self.device); self.refresh()
