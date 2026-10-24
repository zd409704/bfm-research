"""Fork, bearing clearance, reversible tree, and independent distance gate."""
import itertools
import numpy as np
import mujoco


def _capsule(name,a,b,r,m):
    return f'<geom name="{name}" type="capsule" fromto="{a} {b}" size="{r}" mass="{m}"/>'


def link_geometry(side,L,m,ballast=0.,fraction=.5):
    payload=m*ballast; m-=payload
    extra=''
    if payload>0:
        if side=='P':
            extra=''.join(f'<geom name="P_ballast{i}" type="sphere" pos="0 {y} {L*fraction}" size=".014" mass="{payload/2}"/>' for i,y in enumerate((-.04,.04)))
        else: extra=f'<geom name="D_ballast" type="sphere" pos="0 0 {-L*fraction}" size=".014" mass="{payload}"/>'
    if side=='P':
        # Two physical fork tines joined by a pin through the output bearing bore.
        return (_capsule('P_left',f'0 -.04 0',f'0 -.04 {L}',.01,m*.45)+
                _capsule('P_right','0 .04 0',f'0 .04 {L}',.01,m*.45)+
                _capsule('P_pin','0 -.04 0','0 .04 0',.008,m*.1)+extra)
    s=_capsule('D_rod','0 0 -.022',f'0 0 {-L}',.01,m*.8)
    # Explicit hollow output bearing: no solid overlapping hub or disabled pairs.
    for i in range(16):
        a,b=2*np.pi*np.array([i,i+1])/16
        s+=_capsule(f'D_ring{i}',f'{.022*np.sin(a)} 0 {.022*np.cos(a)}',
                    f'{.022*np.sin(b)} 0 {.022*np.cos(b)}',.003,m*.2/16)
    return s+extra


def build_xml(c, limits=(-3.09,3.09)):
    neighbour=c.scene in ('E3','E4')
    floating=c.scene in ('E1','E2','E4')
    base,child=c.fixed_side,('D' if c.fixed_side=='P' else 'P')
    sign=1 if base=='P' else -1
    mass=np.array(c.masses)*(c.density_multiplier if c.mass_error else 1.)
    geo={s:link_geometry(s,c.lengths[i],mass[i],c.ballast_ratios[i],c.ballast_fractions[i]) for i,s in enumerate(('P','D'))}
    lo,hi=sorted([sign*limits[0],sign*limits[1]])
    rootj='<joint name="root_x" type="slide" axis="1 0 0"/><joint name="root_z" type="slide" axis="0 0 1"/><joint name="root_y" type="hinge" axis="0 1 0"/>' if floating else ''
    motor=f'<joint name="motor" axis="0 1 0" limited="true" margin=".08" solreflimit=".002 1" solimplimit=".999 .999 .001" range="{lo} {hi}" damping="{c.damping}" frictionloss="{c.friction}" armature="{c.armature}"/>'
    distal=''
    if neighbour and c.neighbour_sides in (child,'both'):
        l=c.neighbour_lengths[1]; direction=-1 if child=='D' else 1
        distal=f'<body name="N1" pos="0 0 {direction*c.lengths[("P","D").index(child)]}"><joint name="neighbour1" axis="0 1 0" damping=".05" armature=".003" limited="true" range="-1 1"/>'+_capsule('N1_rod',f'0 -.12 0',f'0 -.12 {direction*l}',.012,c.neighbour_masses[1])+'</body>'
    unit=f'<body name="{base}">{geo[base]}<site name="tip_{base}" pos="0 0 {(1 if base=="P" else -1)*c.lengths[("P","D").index(base)]}"/><body name="{child}">{motor}{geo[child]}<site name="tip_{child}" pos="0 0 {(1 if child=="P" else -1)*c.lengths[("P","D").index(child)]}"/>{distal}</body></body>'
    if neighbour and c.neighbour_sides in (base,'both'):
        l=c.neighbour_lengths[0]
        unit=f'<body name="N0">'+_capsule('N0_rod','0 .12 .06',f'0 .12 {l+.06}',.012,c.neighbour_masses[0])+f'<body name="mount" pos="0 0 -.06"><joint name="neighbour0" axis="0 1 0" damping=".05" armature=".003" limited="true" range="-1 1"/>{unit}</body></body>'
    root=f'<body name="root" pos="0 0 1.2" euler="0 {c.tilt} 0">{rootj}<inertial pos="0 0 0" mass=".05" diaginertia=".001 .001 .001"/>{unit}</body>'
    objects=''
    if c.scene in ('E2','E4'):
        objects=f'<geom name="floor" type="plane" size="3 3 .1"/><body name="object0" pos=".25 0 .9"><joint name="object_x" type="slide" axis="1 0 0" damping=".1"/><joint name="object_z" type="slide" axis="0 0 1" damping=".1"/><geom name="obstacle" type="sphere" size="{c.object_radius}" mass="{c.object_mass}"/></body>'
    return f'<mujoco><compiler angle="radian"/><option timestep=".001" integrator="Euler" iterations="80" tolerance="1e-10"><flag filterparent="disable"/></option><size nconmax="128" njmax="1024"/><default><geom friction="{c.contact_friction} .005 .0001" solref=".003 1"/></default><worldbody>{root}{objects}</worldbody></mujoco>'


def independent_gate(model, limits=(-3.09,3.09), step=np.pi/360):
    """All P/D pairs, including parent-child; signed distances independent of contacts.

    Fork sides occupy distinct y slabs; exhaustive angular scan is conservatively
    inset using a Lipschitz bound L*dtheta for moving geometry.
    """
    d=mujoco.MjData(model); j=model.joint('motor').id; adr=model.jnt_qposadr[j]
    ids={s:[i for i in range(model.ngeom) if (mujoco.mj_id2name(model,mujoco.mjtObj.mjOBJ_GEOM,i) or '').startswith(s+'_')] for s in ('P','D')}
    pairs=list(itertools.product(ids['P'],ids['D']))
    qs=np.linspace(*limits,int(np.ceil((limits[1]-limits[0])/step))+1)
    distances=[]; fromto=np.zeros(6)
    for q in qs:
        d.qpos[adr]=q; mujoco.mj_kinematics(model,d)
        distances.append(min(mujoco.mj_geomDistance(model,d,a,b,10,fromto) for a,b in pairs))
    # Global bound includes bounding radii and offsets, valid between grid points.
    reach=max(np.linalg.norm(model.geom_pos[i])+model.geom_rbound[i] for i in ids['P']+ids['D'])
    margin=reach*(qs[1]-qs[0])/2+1e-5
    safe=np.asarray(distances)>margin
    center=int(np.argmin(abs(qs)))
    if not safe[center]: raise ValueError('assembly fails independent distance gate at straight zero')
    a=b=center
    while a>0 and safe[a-1]: a-=1
    while b<len(qs)-1 and safe[b+1]: b+=1
    if b-a<2: raise ValueError('no safe connected travel')
    return {'limits':(float(qs[a]+step),float(qs[b]-step)), 'min_distance':float(min(distances[a:b+1])),
            'tolerance_m':1e-5,'grid_rad':float(qs[1]-qs[0]),'continuous_bound_m':float(margin),
            'pairs':[(int(x),int(y)) for x,y in pairs],'collision_filter':'filterparent disabled; no exclusions',
            'scope':'unit P/D only; per-state scene gate required', 'samples':len(qs)}
