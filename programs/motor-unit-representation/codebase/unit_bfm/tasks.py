"""All rewards are functions of the declared y25, including command cost."""
import numpy as np
import torch

# alpha: [family (H=0,V=1,D=2,C=3), qref/vtarget, a/K, b/D, bias]
def sample_tasks(rng, n, family=None):
    a = np.zeros((n, 5), dtype=np.float32)
    a[:, 0] = rng.integers(0, 4, n)
    if family is not None: a[:,0] = family
    a[:, 1] = rng.uniform(-.8, .8, n)
    v = a[:, 0] == 1
    a[v, 1] = rng.choice([-4., -2., -1., -.5, .5, 1., 2., 4.], v.sum())
    a[:, 2] = rng.uniform(.5, 2, n)
    a[:, 3] = rng.uniform(.05, .2, n)
    c = a[:, 0] == 3
    a[c, 1] = rng.uniform(-.6, .6, c.sum())
    a[c, 2] = np.exp(rng.uniform(np.log(.3), np.log(12), c.sum()))
    a[c, 3] = np.exp(rng.uniform(np.log(.02), np.log(.5), c.sum()))
    a[c, 4] = rng.uniform(-1, 1, c.sum())
    return a


def rewards(y, alpha, include_command=True):
    """Pair all results N with all tasks A -> N,A. Inputs are normalized."""
    q, v, tau, u, du = (y[:, i:i+1] * s for i, s in ((0, 1.2), (1, 6.), (12, 6.), (13, 1.), (24, 1.)))
    kind, ref, a, b, bias = (alpha[:, i][None] for i in range(5))
    cost = (.005 * u.square() + .02 * du.square()) if include_command else 0.
    h = -((q-ref)/.5).square() - .1*(v/3).square()
    distance = torch.where(ref >= 0, 1.2-q, 1.2+q)
    ramp = (distance/.15).clamp(0, 1)
    ramp = ramp.square() * (3-2*ramp)
    vr = -((v-ref*ramp)/3).square()
    dr = -a*(v/3).square() - b*(tau*v).clamp_min(0)/36
    desired = bias + a*(ref-q) - b*v
    cr = -((tau-desired)/3).square()
    return torch.where(kind == 0, h, torch.where(kind == 1, vr, torch.where(kind == 2, dr, cr))) - cost


def durations(rng, n):
    short = rng.random(n) < .5
    return np.where(short, rng.choice([4, 8], n), rng.integers(10, 101, n))


def project(z):
    norm = z.norm(dim=-1, keepdim=True)
    if bool((norm < 1e-8).any()):
        raise ValueError('Undefined near-zero task encoding')
    return 4*z/norm


def reward_features(y):
    """Exact 16-term algebraic basis for the documented rewards, not a network input."""
    q,v,tau,u,du=(y[:,i]*s for i,s in ((0,1.2),(1,6.),(12,6.),(13,1.),(24,1.)))
    rp=((1.2-q)/.15).clamp(0,1); rp=rp.square()*(3-2*rp)
    rn=((1.2+q)/.15).clamp(0,1); rn=rn.square()*(3-2*rn)
    return torch.stack((torch.ones_like(q),q,v,tau,q*q,v*v,tau*tau,q*v,q*tau,v*tau,
                        .005*u*u+.02*du*du,(tau*v).clamp_min(0),v*rp,v*rn,rp*rp,rn*rn),-1)


def reward_weights(alpha):
    kind,ref,a,b,bias=alpha.unbind(-1)
    h=(kind==0).float(); v=(kind==1).float(); d=(kind==2).float(); c=(kind==3).float()
    cp=bias+a*ref
    vp=v*(ref>=0); vn=v*(ref<0)
    return torch.stack((-4*h*ref.square()-c*cp.square()/9,
        8*h*ref+c*2*a*cp/9,c*2*b*cp/9,c*2*cp/9,-4*h-c*a.square()/9,
        -.1*h/9-v/9-d*a/9-c*b.square()/9,-c/9,-2*c*a*b/9,-2*c*a/9,-2*c*b/9,
        -torch.ones_like(ref),-d*b/36,2*vp*ref/9,2*vn*ref/9,-vp*ref.square()/9,-vn*ref.square()/9),-1)
