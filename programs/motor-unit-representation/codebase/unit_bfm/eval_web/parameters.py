"""Editable evaluation physics. Training distributions and code stay immutable."""
import math
import xml.etree.ElementTree as ET
import numpy as np

GROUPS = [
    ('geometry', 'Side structure (nominal description provided to network)'),
    ('limits', 'Physical joint limit (training always <unk>1.2 rad)'),
    ('dynamics', 'Real power (no extra random amount available to the network)'),
    ('drive', 'Electricly driven'),
    ('boundary', 'Boundary and initial whole movement'),
    ('support', 'R1 Resilient Support'),
    ('neighbours', 'R3 Adjacent joints'),
]
FIELDS = []
def field(key, label, group, default, lower, upper, training, step=.01, roles=None, log=False):
    FIELDS.append(dict(key=key,label=label,group=group,default=default,min=lower,max=upper,
        training=list(training),step=step,roles=roles,log=log))

for side,length,mass,lr,mr in [('p',.25,1.,(.15,.4),(.4,2)),('d',.35,.25,(.25,.45),(.15,.6))]:
    title=side.upper()
    field('l'+side,title+'Length / m','geometry',length,.08,.8,lr)
    field('m'+side,title+'Basic quality / kg','geometry',mass,.05,5,mr,log=True)
    field('b'+side,title+'Heavy/basic quality','geometry',0,0,.5,(0,.2))
    field('f'+side,title+'Heavy position/bar length','geometry',.5,.05,.95,(.2,.8))
field('lower','Bottom limit for joints / Rad','limits',-1.2,-math.pi,math.pi,(-1.2,-1.2))
field('upper','Collapse / Rad','limits',1.2,-math.pi,math.pi,(1.2,1.2))
for side,roles in [('p',None),('d',None),('a',[3]),('t',[3])]:
    field('density_'+side,side.upper()+'Real/nominal density','dynamics',1,.5,1.5,(.8,1.2),roles=roles)
field('damping','Electrical barriers / N.m.s/rad','dynamics',.03,0,.3,(.01,.08),.001)
field('friction','Dry frictions / N.m.','dynamics',.02,0,.3,(0,.08),.001)
field('armature','Electrical Equivalent Rotation Logic / kg.m2','dynamics',.003,.0001,.03,(.001,.006),.0001,log=True)
field('ground_mu','Exposure smoothing factor','dynamics',.8,.05,2,(.4,1),roles=[2])
field('gravity','Simulation of gravity acceleration / m/s2','dynamics',9.81,0,20,(9.81,9.81))
field('cap','Real power rectangular capacity / N.m.','drive',6,1,12,(4.8,7.2),.1)
field('tm','Driver Response Time / s','drive',.01,.001,.05,(.005,.02),.001)
field('delay','Command Delay / ms','drive',0,0,10,(0,10),1)
field('tilt','Fixed Parent Pitch/ Rad','boundary',0,-math.pi,math.pi,(-.5,.5),roles=[0])
field('root_pitch','Initial Parent & / Rad','boundary',0,-math.pi*2,math.pi*2,(-.35,.35),roles=[1,2])
field('root_x','Initial root x offset / m','boundary',0,-.2,.2,(-.05,.05),roles=[1])
field('root_z','Initial root z offset / m','boundary',0,-.2,.2,(-.05,.05),roles=[1])
field('root_vx','Initial root vx / m/s','boundary',0,-2,2,(-.5,.5),roles=[1,2])
field('root_vz','Initial root vz / m/s','boundary',0,-2,2,(-.5,.5),roles=[1,2])
field('root_omega','Initial root <unk>y / Rad/s','boundary',0,-4,4,(-1.5,1.5),roles=[1,2])
field('clearance','R2 Minimum pole above / m','boundary',.001,.001,.5,(.001,.1),.001,roles=[2])
for key,label,default,tr in [('kx','x Rigid / N/ m',110,(20,200)),('kz','z Rigid / N/ m',300,(100,500)),('kt','Pitch Rigid / N.m/rad',2.55,(.1,5))]:
    field(key,label,'support',default,tr[0]/2,tr[1]*2,tr,roles=[1])
for axis in ('x','z','t'):
    field('zeta_'+axis,axis+'Stop Nieby.','support',.65,.1,2,(.3,1),roles=[1])
for side,phase in [('p',0),('d',math.pi)]:
    field('amp_'+side,side.upper()+'Neighbourhood target range / Rad','neighbours',.3,0,1,(.1,.7),roles=[3])
    field('hz_'+side,side.upper()+'Neighbourhood / Hz','neighbours',1,.05,4,(.3,2),roles=[3])
    field('phase_'+side,side.upper()+'/ RAd','neighbours',phase,0,2*math.pi,(0,2*math.pi),roles=[3])
    field('q_'+side,side.upper()+'q / Rad','neighbours',0,-1.1,1.1,(-.6,.6),roles=[3])
    field('dq_'+side,side.upper()+'_Other Organiserdq /rad/s','neighbours',0,-4,4,(-1.5,1.5),roles=[3])


def defaults():
    return {f['key']:f['default'] for f in FIELDS}


def validate(values):
    if not isinstance(values,dict):
        raise ValueError('Physical parameters must be objects')
    unknown=set(values)-set(defaults())
    if unknown:raise ValueError('Unknown physical parameters:'+','.join(sorted(unknown)))
    result={}
    for f in FIELDS:
        try:v=float(values.get(f['key'],f['default']))
        except (ValueError,TypeError):raise ValueError(f"{f['label']}must be a value")
        if not math.isfinite(v) or not f['min']<=v<=f['max']:
            raise ValueError(f"{f['label']}It must be.{f['min']:g}to{f['max']:g}")
        result[f['key']]=v
    if result['lower']+.1>result['upper']:
        raise ValueError('The upper limit of the joint must be at least 0.1 Rad')
    if result['delay']!=int(result['delay']):raise ValueError('The delay must be in the milliseconds.')
    return result


def sample(seed,role):
    """Broad structure marginals + full-course dynamics; not a saved training world."""
    rng=np.random.default_rng(seed)
    p=defaults()
    for f in FIELDS:
        if f['roles'] and role not in f['roles']:continue
        lo,hi=f['training']
        p[f['key']]=float(np.exp(rng.uniform(np.log(lo),np.log(hi))) if f['log'] else rng.uniform(lo,hi))
    p['delay']=int(rng.integers(0,11))
    if role==2:
        p['root_pitch']=float(rng.choice([0.,np.pi])+rng.uniform(-.35,.35))
        p['root_vz']=float(rng.uniform(-.3,.3))
        p['clearance']=float(rng.uniform(.02,.1)) if rng.random()<.2 else .001
    return p


def outside_training(p,role):
    labels=[]
    for f in FIELDS:
        if f['roles'] and role not in f['roles']:continue
        v=p[f['key']];lo,hi=f['training']
        if f['key']=='root_pitch' and role==2:
            inside=min(abs(v),abs(v-np.pi))<=.35+1e-8
        elif f['key']=='root_vz' and role==2:inside=abs(v)<=.3+1e-8
        elif f['key']=='clearance':inside=abs(v-.001)<1e-8 or .02<=v<=.1
        else:inside=lo-1e-8<=v<=hi+1e-8
        if not inside:labels.append(f['label'])
    return labels


def model_xml(structure,p,actual=False):
    """Recompile real geometries so mass, COM and inertia remain consistent."""
    root=ET.fromstring(structure.xml())
    motor=root.find(".//joint[@name='motor']")
    motor.set('range',f"{p['lower']} {p['upper']}")
    if actual:
        motor.set('damping',str(p['damping']))
        motor.set('frictionloss',str(p['friction']))
        motor.set('armature',str(p['armature']))
        root.find('option').set('gravity',f"0 0 {-p['gravity']}")
        root.find('default/geom').set('friction',f"{p['ground_mu']} .005 .0001")
        for side in ('P','D','A','T'):
            body=root.find(f".//body[@name='{side}']")
            if body is not None:
                for geom in body.findall('geom'):
                    if 'mass' in geom.attrib:
                        geom.set('mass',str(float(geom.get('mass'))*p['density_'+side.lower()]))
    return ET.tostring(root,encoding='unicode')
