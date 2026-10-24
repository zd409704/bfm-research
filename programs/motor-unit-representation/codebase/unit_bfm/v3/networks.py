"""V3 input dimensions with the unchanged V2/UFO hidden skeleton."""
import torch
from torch import nn
from .schema import G_DIM, X_DIM, Z_DIM
from .stage2_norms import nondim_v3_g


def embedding(n):
    return nn.Sequential(nn.Linear(n,256),nn.LayerNorm(256),nn.Tanh(),
                         nn.Linear(256,128),nn.ReLU())


class Actor(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed_s = embedding(X_DIM)
        self.embed_z = embedding(X_DIM+Z_DIM)
        # Tanh is applied in forward so a pre-activation hinge can see the logit.
        self.head = nn.Sequential(nn.Linear(256,256),nn.ReLU(),nn.Linear(256,1))

    def context(self,x):
        return self.embed_s(x)

    def logits(self,x,z):
        # Pre-activation path. The published action is tanh(logits).
        return self.head(torch.cat((self.embed_s(x),self.embed_z(torch.cat((x,z),-1))),-1))

    def forward(self,x,z):
        return torch.tanh(self.logits(x,z))


class ForwardMap(nn.Module):
    def __init__(self,p_dim):
        super().__init__()
        self.embed_sa = embedding(X_DIM+p_dim+1)
        self.embed_z = embedding(X_DIM+p_dim+Z_DIM)
        self.head = nn.Sequential(nn.Linear(256,256),nn.ReLU(),nn.Linear(256,Z_DIM))

    def forward(self,y,u,z):
        return self.head(torch.cat((self.embed_sa(torch.cat((y,u),-1)),
                                    self.embed_z(torch.cat((y,z),-1))),-1))


class SphereNorm(nn.Module):
    def forward(self,x):
        return Z_DIM**.5 * torch.nn.functional.normalize(x,dim=-1)


class BackwardMap(nn.Sequential):
    def __init__(self):
        super().__init__(nn.Linear(G_DIM,256),nn.LayerNorm(256),nn.Tanh(),
                         nn.Linear(256,256),nn.ReLU(),nn.Linear(256,Z_DIM),SphereNorm())

    def forward(self, g):
        # B03: tip channels are length-relative before the linear map.
        return super().forward(nondim_v3_g(g))


class Networks(nn.Module):
    def __init__(self,p_dim:int):
        super().__init__()
        if isinstance(p_dim,bool) or not isinstance(p_dim,int) or p_dim < 0:
            raise ValueError('p_dim must be a nonnegative integer including feature memory')
        self.p_dim = p_dim
        self.actor = Actor()
        self.f1,self.f2 = ForwardMap(p_dim),ForwardMap(p_dim)
        self.b = BackwardMap()

    def counts(self):
        counts = {k:sum(p.numel() for p in m.parameters()) for k,m in self.named_children()}
        counts['online'] = sum(counts.values())
        counts['execution'] = counts['actor']+counts['b']
        return counts


def orthogonal_init(module):
    if isinstance(module,nn.Linear):
        nn.init.orthogonal_(module.weight,gain=1.)
        nn.init.zeros_(module.bias)
    elif isinstance(module,nn.LayerNorm):
        module.reset_parameters()
