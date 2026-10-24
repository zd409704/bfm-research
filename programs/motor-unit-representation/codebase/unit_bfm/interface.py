"""Frozen callable module: observe first, send feedback, then accept upper z."""
import torch
from . import VERSION
from .networks import Actor,BackwardMap,physical_result
from .history import History
from .tasks import project


class FrozenUnit:
    def __init__(self,bundle,nworld=1,device='cpu'):
        state=torch.load(bundle,map_location=device,weights_only=False)
        if state['version']!=VERSION: raise ValueError('Incompatible unit schema')
        self.device=device
        self.actor=Actor().to(device).eval().requires_grad_(False)
        self.b=BackwardMap().to(device).eval().requires_grad_(False)
        self.actor.load_state_dict(state['actor']); self.b.load_state_dict(state['b'])
        self.cross=state['reward_cross'].to(device)
        self.history=History(nworld,device)
        self.valid=torch.zeros(nworld,1,device=device)
        self.result=torch.zeros(nworld,16,device=device)

    @torch.no_grad()
    def reset(self,o,m):
        self.o=o.to(self.device); self.m=m.to(self.device)
        self.history.reset(self.o); self.valid.zero_(); self.result.zero_()
        self.x=self.history.input(self.m)
        self.context=self.actor.context(self.x)

    @torch.no_grad()
    def observe(self,o):
        """Exactly one call per completed 10 ms interval, using normalized o24."""
        o=o.to(self.device)
        y=torch.cat((o,o[:,13:14]-self.o[:,13:14]),-1)
        self.result=self.b(physical_result(y)); self.valid.fill_(1)
        self.o=o; self.history.append(o); self.x=self.history.input(self.m)
        self.context=self.actor.context(self.x)

    def feedback(self):
        return torch.cat((self.o,self.m,self.result,self.context,self.valid),-1)

    @torch.no_grad()
    def act(self,z):
        z=project(z.to(self.device))
        return self.actor.head(torch.cat((self.context,self.actor.embed_z(torch.cat((self.x,z),-1))),-1))

    @torch.no_grad()
    def encode_task(self,alpha):
        from .tasks import reward_weights
        weights=reward_weights(torch.as_tensor(alpha,device=self.device,dtype=torch.float32))
        weights[:,10]=0
        return project(weights@self.cross.T)
