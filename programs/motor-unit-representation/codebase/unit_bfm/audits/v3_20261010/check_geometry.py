"""Reproduce collision filtering of existing V2 bars, not a V3 model test."""
import json,sys
from pathlib import Path
import numpy as np
import mujoco
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from unit_bfm.mechanics import Structure
rows=[]
for explicit in [False,True]:
 xml=Structure(2,0).xml().replace('range="-1.2 1.2"','range="-3.09159265359 3.09159265359"')
 if explicit:xml=xml.replace('</mujoco>','<contact><pair geom1="P_box" geom2="D_box"/></contact></mujoco>')
 m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m)
 p,dd=m.geom('P_box').id,m.geom('D_box').id
 for q in [0.,.6,1.2,2.4]:
  mujoco.mj_resetData(m,d);d.qpos[int(m.joint('motor').qposadr[0])]=q;mujoco.mj_forward(m,d)
  dist=mujoco.mj_geomDistance(m,d,p,dd,10.,None)
  contacts=sum(set(c.geom)=={p,dd} for c in d.contact[:d.ncon])
  rows.append(dict(explicit_pair=explicit,q=q,distance_m=float(dist),pair_contacts=contacts))
assert any(r['distance_m']<-.01 and r['pair_contacts']==0 for r in rows if not r['explicit_pair'])
assert any(r['pair_contacts']>0 for r in rows if r['explicit_pair'])
print(json.dumps(dict(scope='Existing V2 geometry; V3 hinge-clearance models have not been implemented',rows=rows),indent=2))
