"""Raw episode storage, uniform episode then transition within each role."""
import numpy as np
import torch
from .history import assemble


class SequenceReplay:
    def __init__(self,capacity=1_000_000,horizon=500,device='cuda:0',seed=91001):
        self.horizon=horizon; self.device=device
        self.slots=(max(4,capacity//horizon)//4)*4
        self.per_role=self.slots//4
        self.raw=torch.zeros(self.slots,horizon+1,24,device=device)
        self.m=torch.zeros(self.slots,28,device=device)
        self.length=np.zeros(self.slots,np.int32)
        self.role=np.full(self.slots,-1,np.int8)
        self.eid=np.full(self.slots,-1,np.int64)
        self.cursor=np.zeros(4,np.int64); self.next_id=0; self.active=None
        self.rng=np.random.default_rng(seed)

    def begin(self,o,m,role):
        n=len(o)
        if n>self.per_role: raise ValueError('Per-role Replay smaller than active environment batch')
        ids=role*self.per_role+(self.cursor[role]+np.arange(n))%self.per_role
        self.cursor[role]=(self.cursor[role]+n)%self.per_role
        self.active=ids; self.time=0
        self.length[ids]=0; self.role[ids]=role
        self.eid[ids]=self.next_id+np.arange(n); self.next_id+=n
        self.raw[ids,0]=o; self.m[ids]=m

    def append(self,o):
        self.time+=1
        if self.time>self.horizon: raise ValueError('Episode exceeds declared horizon')
        self.raw[self.active,self.time]=o
        self.length[self.active]=self.time

    def _indices(self,n,role_weights,rng=None):
        rng=self.rng if rng is None else rng
        available=np.array([np.any((self.role==r)&(self.length>0)) for r in range(4)])
        weights=np.asarray(role_weights,float)*available
        if weights.sum()==0: raise ValueError('No valid source episodes')
        selected_roles=rng.choice(4,n,p=weights/weights.sum())
        slots=np.zeros(n,np.int64)
        for r in range(4):
            mask=selected_roles==r
            if mask.any():
                candidates=np.flatnonzero((self.role==r)&(self.length>0))
                slots[mask]=rng.choice(candidates,mask.sum())
        times=(rng.random(n)*self.length[slots]).astype(np.int64)
        si=torch.as_tensor(slots,device=self.device)
        t=torch.as_tensor(times,device=self.device)
        return si,t

    def sample_results(self,n,role_weights,rng=None):
        si,t=self._indices(n,role_weights,rng)
        now=self.raw[si,t]; nxt=self.raw[si,t+1]
        return torch.cat((nxt,nxt[:,13:14]-now[:,13:14]),-1)

    def sample(self,n,role_weights):
        si,t=self._indices(n,role_weights)
        def window(end):
            indices=end[:,None]+torch.arange(-21,1,device=self.device)
            raw=self.raw[si[:,None],indices.clamp_min(0)]
            return raw*(indices>=0)[...,None]
        now=window(t); nxt=window(t+1)
        m=self.m[si]
        x=assemble(now,t,m); xp=assemble(nxt,t+1,m)
        action=nxt[:,-1,13:14]
        y=torch.cat((nxt[:,-1],action-now[:,-1,13:14]),-1)
        return x,action,xp,y

    def state_dict(self):
        return dict(raw=self.raw.cpu(),m=self.m.cpu(),length=self.length,role=self.role,eid=self.eid,
                    cursor=self.cursor,next_id=self.next_id,rng=self.rng.bit_generator.state)

    def load_state_dict(self,state):
        for name in ('raw','m'): getattr(self,name).copy_(state[name])
        for name in ('length','role','eid','cursor','next_id'): setattr(self,name,state[name])
        self.rng.bit_generator.state=state['rng']
