"""Compile geometry, ballast, anchor positions and nominal inertia together."""
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np
import mujoco


@dataclass
class Structure:
    role: int
    index: int
    lp: float = .25
    ld: float = .35
    mp: float = 1.
    md: float = .25
    bp: float = 0.
    bd: float = 0.
    fp: float = .5
    fd: float = .5
    tilt: float = 0.
    narrow: bool = False

    @property
    def key(self):
        return f'R{self.role}_{self.index:03d}'

    def xml(self, timestep=.001):
        r = self.role
        def geom(name, length, mass, ballast, fraction, color):
            # Multiple real geoms are compiled into one consistent rigid inertia.
            return (f'<geom name="{name}_box" type="box" size=".02 .02 {length/2}" '
                    f'pos="0 0 {-length/2}" mass="{mass}" rgba="{color}"/>'
                    + (f'<geom name="{name}_ballast" type="sphere" size=".012" '
                       f'pos=".01 0 {-length*fraction}" mass="{mass*ballast}" contype="0" conaffinity="0"/>' if ballast else '')
                    + f'<site name="{name}_end" pos="0 0 {-length}"/>')
        pg = geom('P',self.lp,self.mp,self.bp,self.fp,'.25 .55 .9 1')
        dg = geom('D',self.ld,self.md,self.bd,self.fd,'.9 .5 .2 1')
        tail = (f'<body name="T" pos="0 0 {-self.ld}"><joint name="q3"/>'
                + geom('T',.22,.2,0,.5,'.3 .8 .4 1') + '</body>') if r == 3 else ''
        distal = f'<body name="D" pos="0 0 {-self.lp}"><joint name="motor"/>{dg}{tail}</body>'
        root_dofs = ('<joint name="root_x" type="slide" axis="1 0 0" limited="false" damping="0" frictionloss="0" armature="0"/>'
                     '<joint name="root_z" type="slide" axis="0 0 1" limited="false" damping="0" frictionloss="0" armature="0"/>'
                     '<joint name="root_pitch" limited="false" damping="0" frictionloss="0" armature="0"/>') if r in (1,2) else ''
        if r == 3:
            body = ('<body name="A" pos="0 0 1.4">' + geom('A',.2,.6,0,.5,'.6 .6 .6 1')
                    + f'<body name="P" pos="0 0 -.2"><joint name="q1"/>{pg}{distal}</body></body>')
        else:
            # R1 root reference at z=1; root slides are world axes (no rotated body).
            tilt = self.tilt if r == 0 else 0.
            body = f'<body name="P" pos="0 0 1" euler="0 {tilt} 0">{root_dofs}{pg}{distal}</body>'
        floor = '<geom name="floor" type="plane" size="5 5 .1" rgba=".35 .38 .4 1"/>' if r == 2 else ''
        contacts = '1' if r == 2 else '0'
        return f'''<mujoco model="{self.key}">
<compiler angle="radian" autolimits="true"/>
<option timestep="{timestep}" integrator="implicitfast" solver="Newton" iterations="20" gravity="0 0 -9.81"/>
<default><joint type="hinge" axis="0 1 0" range="-1.2 1.2" damping=".03" frictionloss=".02" armature=".003" solreflimit=".002 1" solimplimit=".99 .999 .001" margin=".03"/>
<geom friction=".8 .005 .0001" condim="3" contype="{contacts}" conaffinity="{contacts}" solref=".01 1"/>
<site size=".008"/></default>
<visual><global offwidth="640" offheight="480"/><headlight ambient=".4 .4 .4"/></visual>
<worldbody><light pos="1 -2 3"/>{floor}{body}</worldbody>
</mujoco>'''

    def compile(self, timestep=.001):
        return mujoco.MjModel.from_xml_string(self.xml(timestep))

    def nominal(self, model=None):
        model = model or self.compile()
        p,d = (model.body(name).id for name in ('P','D'))
        # Inertia yy is invariant under the principal-axis rotation of planar ballast.
        inertia=[]
        for b in (p,d):
            mat=np.empty(9); mujoco.mju_quat2Mat(mat,model.body_iquat[b])
            rot=mat.reshape(3,3)
            inertia.append((rot@np.diag(model.body_inertia[b])@rot.T)[1,1])
        com_p=model.body_ipos[p]-np.array([0,0,-self.lp])
        com_d=model.body_ipos[d]
        values=np.array([self.lp,self.ld,model.body_mass[p],model.body_mass[d],*inertia,
                         com_p[0],com_p[2],com_d[0],com_d[2],-1.2,1.2,6.,.01],np.float32)
        scale=np.array([.4,.4,2.,1.,.1,.1,.4,.4,.4,.4,1.2,1.2,6.,.02],np.float32)
        return np.r_[values/scale,np.ones(14,np.float32)].astype(np.float32)


def library(seed=31001, count=32, training=True):
    rng=np.random.default_rng(seed)
    result=[]
    for role in range(4):
        for i in range(count):
            narrow=training and i < 8
            lp=rng.uniform(.225,.275) if narrow else rng.uniform(.15,.4)
            ld=rng.uniform(.315,.385) if narrow else rng.uniform(.25,.45)
            mp=np.exp(rng.uniform(np.log(.85 if narrow else .4),np.log(1.15 if narrow else 2.)))
            md=np.exp(rng.uniform(np.log(.2125 if narrow else .15),np.log(.2875 if narrow else .6)))
            bp,bd=(0.,0.) if narrow else tuple(rng.uniform(0,.2,2))
            result.append(Structure(role,i,lp,ld,mp,md,bp,bd,*rng.uniform(.2,.8,2),
                                    0. if narrow else rng.uniform(-.5,.5),narrow))
    return result


def save_library(path, structures):
    path=Path(path); path.mkdir(parents=True,exist_ok=True)
    (path/'structures.json').write_text(json.dumps([asdict(s) for s in structures],indent=2))
    for s in structures:
        model=s.compile()
        if not np.isfinite(model.body_inertia).all() or (model.body_inertia[1:]<=0).any():
            raise ValueError(f'Invalid inertia {s.key}')
        (path/f'{s.key}.xml').write_text(s.xml())
