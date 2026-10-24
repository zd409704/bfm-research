"""CPU audit probes only. Does not implement or train V3."""
import json, math, sys
from pathlib import Path
import numpy as np
import torch
from torch import nn
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from unit_bfm.networks import Actor, ForwardMap, BackwardMap, embedding
from unit_bfm.fb_loss import fb_loss

def count(m): return sum(p.numel() for p in m.parameters())
a=Actor();a.embed_s=embedding(137);a.embed_z=embedding(153)
f=ForwardMap();f.embed_sa=embedding(138+512);f.embed_z=embedding(153+512)
b=BackwardMap(13)
counts=dict(actor=count(a),b=count(b),each_F_Dp512=count(f))
assert counts==dict(actor=207617,b=74000,each_F_Dp512=473872)
# Relative tip derivatives agree with central difference of local geometry.
L=.37;q=.83;v=-1.4;acc=2.1;dt=1e-4
pos=lambda t: np.array([-L*np.sin(q+v*t+.5*acc*t*t),-L*np.cos(q+v*t+.5*acc*t*t)])
v_exp=np.array([-L*np.cos(q)*v,L*np.sin(q)*v])
a_exp=np.array([L*np.sin(q)*v*v-L*np.cos(q)*acc,L*np.cos(q)*v*v+L*np.sin(q)*acc])
kin=dict(velocity_error=float(np.max(np.abs((pos(dt)-pos(-dt))/(2*dt)-v_exp))),acceleration_error=float(np.max(np.abs((pos(dt)-2*pos(0)+pos(-dt))/dt**2-a_exp))))
assert kin['velocity_error']<1e-7 and kin['acceleration_error']<1e-7
# Canonical five-point causal slope has 20 ms effective delay for linearly varying acceleration.
t=np.arange(-4,1)*.01
slope=lambda x:float(np.dot(t-t.mean(),x)/np.sum((t-t.mean())**2))
j=100.;vel=.5*j*t*t
accel=dict(current_true_acceleration=0.,estimated=slope(vel),effective_delay_s=.02)
# Selected history summaries do not generally determine the next summary.
# This algebraic example is not a pair of fully matched, physically realized x/p trajectories.
v1=np.zeros(5);v2=np.array([0.,.1,0.,.1,0.])
assert np.allclose(v1[::2],v2[::2]) and abs(slope(v1)-slope(v2))<1e-12
memory=dict(current_slopes=[slope(v1),slope(v2)],next_slopes_if_same_next_velocity=[slope(np.r_[v1[1:],0.]),slope(np.r_[v2[1:],0.])])
# Loss formula equals V2 for scalar gamma. Row-wise discounts need shape [N,1].
torch.manual_seed(8);N=7;F=torch.randn(2,N,16,dtype=torch.float64);B=torch.randn(N,16,dtype=torch.float64);T=torch.randn(N,N,dtype=torch.float64)
base=fb_loss(F,B,T)[0];D=F@B.T-.99*T;G=B@B.T;mask=~torch.eye(N,dtype=torch.bool)
manual=sum(.5*d[mask].square().mean()-d.diag().mean() for d in D)+.5*G[mask].square().mean()-G.diag().mean()
assert torch.allclose(base,manual)
gamma=torch.linspace(0,.99,N,dtype=torch.float64)
row=(F@B.T)-gamma[:,None]*T
col=F@B.T-gamma*T
loss=dict(scalar_formula_abs_error=float(abs(base-manual)),row_vs_column_discount_max_error=float((row-col).abs().max()))
# Coarse immutable-context occupancy: C disconnected contexts requires rank >= C for exact global density.
C,d=144,16
rank=dict(contexts=C,z_dim=d,coarse_occupancy_rank=C,best_rank16_relative_frobenius_error=math.sqrt((C-d)/C),scope='Exact global discounted occupancy of immutable context indicators at a fixed z, not a measured control-error bound')
print(json.dumps(dict(counts=counts,kinematics=kin,acceleration=accel,compressed_history=memory,loss=loss,global_context_rank=rank),ensure_ascii=False,indent=2))
