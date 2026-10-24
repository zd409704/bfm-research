"""Output-side zero/sign contract; CPU fixture only, not a V3 collector."""
import json
import numpy as np
import mujoco

def state(beta,sign,qc=None,raw=None,ref=0.):
 lo,hi=sorted(sign*(np.array([-.9,1.1])-beta)+ref)
 xml=f'''<mujoco><compiler angle="radian"/><option timestep=".001" gravity="0 0 -9.81"/>
 <worldbody><body name="P" pos="0 0 1"><geom type="sphere" size=".01" contype="0" conaffinity="0"/>
 <body name="D" euler="0 {beta} 0"><joint name="j" axis="0 {sign} 0" ref="{ref}" limited="true" range="{lo} {hi}" armature=".003"/>
 <geom type="capsule" fromto="0 0 0 0 0 -.35" size=".01" mass=".5" contype="0" conaffinity="0"/><site name="tip" pos="0 0 -.35"/>
 </body></body></worldbody></mujoco>'''
 m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m)
 d.qpos[0]=sign*(qc-beta)+ref if qc is not None else raw
 qcanon=sign*(d.qpos[0]-ref)+beta
 d.qvel[0]=sign*.4;d.qfrc_applied[0]=sign*.7;mujoco.mj_forward(m,d)
 tip=d.site_xpos[0]-d.xanchor[0]
 assert np.allclose(tip,[-.35*np.sin(qcanon),0,-.35*np.cos(qcanon)],atol=1e-12)
 assert np.allclose(sorted(sign*(np.array([lo,hi])-ref)+beta),[-.9,1.1])
 return dict(beta=beta,sign=sign,raw=float(d.qpos[0]),canonical=float(qcanon),tip=tip.tolist(),bias=float(sign*d.qfrc_bias[0]),qacc=float(sign*d.qacc[0]),power=float(d.qfrc_applied[0]*d.qvel[0]))
zero=[state(b,1,raw=0.) for b in [0.,.6]]
assert np.linalg.norm(np.array(zero[0]['tip'])-zero[1]['tip'])>.1
same=[state(b,s,qc=.3) for b,s in [(0.,1),(.6,1),(-.5,-1)]]
for r in same[1:]:
 for key in ['tip','bias','qacc','power']:assert np.allclose(r[key],same[0][key],atol=1e-10)
ref=state(.6,1,raw=0.,ref=.2);assert abs(ref['canonical']-.4)<1e-12
families=[]
for c0 in [3.,6.,9.]:
 scale=1.25*c0
 for ratio in [.8,1.,1.2]:
  cap=c0*ratio;assert scale>cap
  families.append(dict(C0=c0,request_scale=scale,actual_cap=cap,max_request_saturates=True))
print(json.dumps(dict(scope='CPU coordinate, limit, power and scalar saturation proof; no actual V3 geometry/collection/network training',raw_zero=zero,same_physical_state=same,nonzero_ref=ref,drive_families=families),indent=2))
