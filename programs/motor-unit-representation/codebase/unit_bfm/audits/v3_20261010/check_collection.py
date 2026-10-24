"""CPU checks for V2 migration risks, not a V3 implementation."""
import json,sys
from pathlib import Path
import numpy as np
import mujoco
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from unit_bfm.mechanics import Structure
from unit_bfm.cpu import CPUUnit
from unit_bfm.replay import SequenceReplay
torch.set_num_threads(1)
s=Structure(0,0,ld=.45,md=2.);m=s.compile();d=mujoco.MjData(m);mujoco.mj_forward(m,d)
e=CPUUnit(m,d,s,dict(u=0.,tau=0.,cap=6.,tm=.01,delay=0,clock=0,ring=np.zeros(11),support=np.zeros(7),pulses=np.zeros((0,7)),peripheral=np.zeros((2,3))))
for _ in range(200):e.step(np.clip((6*(1.-d.qpos[0])-.6*d.qvel[0])/6,-1,1))
hold=dict(q_ref=1.,q_final=float(d.qpos[0]),dq_final=float(d.qvel[0]),required_gravity_torque=2*9.81*.45/2*np.sin(1.),capacity=6.,max_PD_torque_in_acceptance_region=6*.05+.6*.05)
r=SequenceReplay(capacity=80,horizon=10,device='cpu',seed=91001);r.role[:2]=0;r.length[:2]=[1,9]
ids,_=r._indices(100000,[1,0,0,0]);counts=np.bincount(ids.numpy(),minlength=2)
assert abs(hold['q_final']-1.)>.3 and abs(counts[0]/sum(counts)-.5)<.02
print(json.dumps(dict(hold=hold,replay_episode_counts=counts.tolist(),uniform_transition_expected_short_probability=.1,scope='Old PD and Replay tested as migration risks; not evidence of V3 training outcomes'),indent=2))
