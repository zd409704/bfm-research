"""CPU counterexample: equality multipliers are not generally physical moments."""
import json
import mujoco as mj
import numpy as np
rows=[]
for scale in [1,2]:
 m=mj.MjModel.from_xml_string(f'''<mujoco><option gravity="0 0 0" jacobian="dense"/><worldbody><body name="b"><freejoint/><geom type="sphere" size=".1" mass="1"/></body></worldbody><equality><weld body1="b" torquescale="{scale}"/></equality></mujoco>''')
 d=mj.MjData(m);d.xfrc_applied[1,5]=2.;mj.mj_forward(m,d);mj.mj_rnePostConstraint(m,d)
 generalized=d.efc_J.reshape(d.nefc,m.nv).T@d.efc_force
 angular_balance=float(m.body_inertia[1,2]*d.qacc[5]-2.)
 reported=float(d.cfrc_ext[1,2]-2.)
 assert abs(generalized[5]-angular_balance)<1e-10
 rows.append(dict(torquescale=scale,physical_weld_moment=angular_balance,J_transpose_lambda=float(generalized[5]),postconstraint_reported_weld_moment=reported,mismatch=reported-angular_balance))
assert abs(rows[0]['mismatch'])>1.
print(json.dumps(dict(mujoco=mj.__version__,scope='Single CPU free body/world weld at identity orientation. Reproduces API discrepancy, not a general replacement extractor.',rows=rows),indent=2))
