"""Monte Carlo preference queries over exactly replay-induced next-result rho.

These preferences are used only for querying/evaluation, never learner.update.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import torch
from .replay import fingerprint, plain, RHO_VERSION

from .schema import G_SCALES
SCALES=G_SCALES
FIELDS={'q':2,'dq':3,'tau':4,'tip_vx':7,'tip_vz':8,'ddq':9,'tip_ax':10,'tip_az':11}

@dataclass(frozen=True)
class Query:
    kind: str
    target: float=0.
    width: float=.1
    q_ref: float=0.
    stiffness: float=0.
    damping: float=0.
    bias: float=0.
    def score(self,g):
        a=np.asarray(g)*SCALES
        if self.width<=0: raise ValueError('query width must be positive')
        if self.kind=='compliance': error=a[:,4]-(self.bias+self.stiffness*(self.q_ref-a[:,2])-self.damping*a[:,3])
        elif self.kind in FIELDS: error=a[:,FIELDS[self.kind]]-self.target
        else: raise ValueError('query must be a declared g13 physical preference')
        r=np.exp(-.5*(error/self.width)**2)
        if self.kind in ('ddq','tip_ax','tip_az'): r=np.where(a[:,12]>.5,r,0.)
        return r

class QueryPool:
    def __init__(self,g,rho,ids=None):
        self.g=np.asarray(g,dtype=np.float32); self.rho=plain(rho); self.ids=ids
        if self.g.ndim!=2 or self.g.shape[1]!=13 or not np.isfinite(self.g).all(): raise ValueError('g13 reference')
        if self.rho['version']!=RHO_VERSION: raise ValueError('query rho version')
        self.version=fingerprint({'rho':self.rho,'g':self.g,'ids':ids})
    @classmethod
    def from_replay(cls,replay,n=65536):
        data=replay.reference(n); return cls(data['g'],data['rho'],data['ids'])
    def assert_current(self,replay):
        if fingerprint(self.rho)!=fingerprint(replay.distribution()): raise ValueError('stale query rho; regenerate pool')
    def integrate(self,b,query,samples=4096,seed=0):
        if samples<2: raise ValueError('at least two MC samples')
        rng=np.random.default_rng(seed); ids=rng.integers(len(self.g),size=samples); g=self.g[ids]
        device=next(b.parameters()).device
        with torch.no_grad(): encoded=b(torch.as_tensor(g,device=device)).detach().cpu().numpy()
        products=query.score(g)[:,None]*encoded
        estimate=products.mean(axis=0); se=products.std(axis=0,ddof=1)/np.sqrt(samples)
        norm=float(np.linalg.norm(estimate))
        if norm<=1e-12: raise ValueError('zero preference mass/direction under frozen rho')
        z=estimate/norm*4
        return z.astype(np.float32),{'pool_version':self.version,'rho':self.rho,'samples':samples,
                'seed':seed,'mean':estimate.tolist(),'standard_error':se.tolist(),'preference_mass':float(query.score(g).mean())}
    def save(self,path):
        import json
        np.savez_compressed(path,g=self.g,manifest=np.asarray(json.dumps({'rho':self.rho,'ids':self.ids,'version':self.version})))
    @classmethod
    def load(cls,path):
        import json
        with np.load(path,allow_pickle=False) as d:
            m=json.loads(str(d['manifest'])); pool=cls(d['g'],m['rho'],m['ids'])
        if pool.version!=m['version']: raise ValueError('query pool modified')
        return pool
