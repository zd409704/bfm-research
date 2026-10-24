"""MuJoCo CPU reaction/sign/reference-point check, no V3 production implementation."""
import json
import mujoco
import numpy as np
xml='''<mujoco><option gravity="0 0 -9.81" timestep="0.001"/>
<worldbody><body name="rod"><joint name="j" type="hinge" axis="0 1 0"/>
<geom type="capsule" fromto="0 0 0 0 0 -0.4" size="0.02" mass="1"/>
<site name="joint" pos="0 0 0"/></body></worldbody>
<sensor><force site="joint"/><torque site="joint"/></sensor></mujoco>'''
m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m)
d.qpos[0]=.3;d.qfrc_applied[0]=1.
mujoco.mj_forward(m,d);mujoco.mj_rnePostConstraint(m,d)
b=m.body('rod').id;root=m.body_rootid[b]
f=d.cfrc_int[b,3:].copy();reference=d.subtree_com[root].copy();joint=d.site_xpos[0].copy()
moment=d.cfrc_int[b,:3]+np.cross(reference-joint,f)
R=d.site_xmat[0].reshape(3,3)
calculated=np.r_[R.T@f,R.T@moment]
error=float(np.max(np.abs(calculated-d.sensordata)))
assert error<1e-10 and abs(moment[1]-1.)<1e-10
no_sensor=xml.replace('<sensor><force site="joint"/><torque site="joint"/></sensor>','')
m2=mujoco.MjModel.from_xml_string(no_sensor);d2=mujoco.MjData(m2)
d2.qfrc_applied[0]=1.;mujoco.mj_forward(m2,d2)
before=d2.cfrc_int[b].copy();mujoco.mj_rnePostConstraint(m2,d2);after=d2.cfrc_int[b].copy()
assert np.linalg.norm(after-before)>1
print(json.dumps(dict(mujoco=mujoco.__version__,sensor_crosscheck_error=error,
 spatial_order='cfrc_int torque then force; xfrc_applied force then torque',
 reference='subtree_com[body_rootid[body]]',
 joint_axis_total_reaction_Nm=float(moment[1]),
 caveat='Total tree interaction includes actuator transfer; not an independently identified external contact wrench',
 without_sensor_after_forward=before.tolist(),after_explicit_postconstraint=after.tolist(),
 scope='CPU one-link hinge API proof only; no GPU, closed-loop, fixed-D, contact or randomized-batch acceptance'),indent=2))
