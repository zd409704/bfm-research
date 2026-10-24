"""Millisecond physics hooks captured together with MuJoCo-Warp stepping."""
import warp as wp
from mujoco_warp._src.support import contact_force_fn
from mujoco_warp._src.types import vec5


@wp.struct
class State:
    qpos: wp.array2d(dtype=float)
    qvel: wp.array2d(dtype=float)
    qfrc: wp.array2d(dtype=float)
    xfrc: wp.array2d(dtype=wp.spatial_vector)
    xpos: wp.array2d(dtype=wp.vec3)
    xipos: wp.array2d(dtype=wp.vec3)
    xmat: wp.array2d(dtype=wp.mat33)
    cvel: wp.array2d(dtype=wp.spatial_vector)
    subtree_com: wp.array2d(dtype=wp.vec3)
    rootid: wp.array(dtype=int)
    body_mass: wp.array2d(dtype=float)
    u: wp.array(dtype=float)
    tau: wp.array(dtype=float)
    cap: wp.array(dtype=float)
    tm: wp.array(dtype=float)
    delay: wp.array(dtype=int)
    clock: wp.array(dtype=int)
    ring: wp.array2d(dtype=float)
    support: wp.array2d(dtype=float)
    pulses: wp.array3d(dtype=float)
    peripheral: wp.array3d(dtype=float)
    wrench: wp.array3d(dtype=float)
    contact: wp.array2d(dtype=float)
    work: wp.array2d(dtype=float)
    obs: wp.array2d(dtype=float)
    contact_geom: wp.array(dtype=wp.vec2i)
    contact_pos: wp.array(dtype=wp.vec3)
    contact_frame: wp.array(dtype=wp.mat33)
    contact_friction: wp.array(dtype=vec5)
    contact_dim: wp.array(dtype=int)
    contact_adr: wp.array2d(dtype=int)
    contact_world: wp.array(dtype=int)
    nacon: wp.array(dtype=int)
    efc_force: wp.array2d(dtype=float)
    geom_body: wp.array(dtype=int)


@wp.func
def velocity(s: State, w: int, b: int):
    cv = s.cvel[w,b]
    return wp.spatial_bottom(cv) + wp.cross(wp.spatial_top(cv), s.xipos[w,b]-s.subtree_com[w,s.rootid[b]])


@wp.kernel
def clear_interval(s: State):
    w=wp.tid()
    for b in range(2):
        s.contact[w,b]=0.0
        for k in range(3): s.wrench[w,b,k]=0.0
    s.work[w,0]=0.0
    s.work[w,1]=0.0


@wp.kernel
def drive(s: State, role: int, p: int, d: int, motor: int, lp: float, ld: float,
          q1: int, q3: int, dt: float):
    w=wp.tid()
    tick=s.clock[w]
    t=float(tick)*dt
    for b in range(s.xfrc.shape[1]): s.xfrc[w,b]=wp.spatial_vector()
    for j in range(s.qfrc.shape[1]): s.qfrc[w,j]=0.0
    s.ring[w,tick%11]=6.0*s.u[w]
    delayed=s.ring[w,(tick-s.delay[w]+22)%11]
    target=wp.clamp(delayed,-s.cap[w],s.cap[w])
    tau=s.tau[w]+(1.0-wp.exp(-dt/s.tm[w]))*(target-s.tau[w])
    s.tau[w]=tau
    s.qfrc[w,motor]=tau
    power=tau*s.qvel[w,motor]
    s.work[w,0]+=wp.max(power,0.0)*dt
    s.work[w,1]+=wp.min(power,0.0)*dt
    if role == 1:
        # Root joint coordinates are world-x, world-z and pitch about root origin.
        fx=-s.support[w,0]*s.qpos[w,0]-s.support[w,3]*s.qvel[w,0]
        fz=-s.support[w,1]*s.qpos[w,1]-s.support[w,4]*s.qvel[w,1]+s.support[w,6]
        my=-s.support[w,2]*s.qpos[w,2]-s.support[w,5]*s.qvel[w,2]
        force=wp.vec3(fx,0.0,fz)
        moment=wp.vec3(0.0,my,0.0)+wp.cross(s.xpos[w,p]-s.xipos[w,p],force)
        s.xfrc[w,p]=wp.spatial_vector(force,moment)
    for event in range(s.pulses.shape[1]):
        start=s.pulses[w,event,0]
        duration=s.pulses[w,event,1]
        phase=t-start
        if phase >= 0.0 and phase < duration:
            envelope=wp.min(wp.min(phase/.05,(duration-phase)/.05),1.0)
            envelope=.5-.5*wp.cos(3.141592653589793*envelope)
            force=envelope*wp.vec3(s.pulses[w,event,2],0.0,s.pulses[w,event,3])
            b=p
            length=lp
            if s.pulses[w,event,6] > .5:
                b=d
                length=ld
            point=s.xpos[w,b]+s.xmat[w,b]*wp.vec3(0.0,0.0,-length*s.pulses[w,event,5])
            moment=wp.cross(point-s.xipos[w,b],force)+wp.vec3(0.0,envelope*s.pulses[w,event,4],0.0)
            s.xfrc[w,b]=s.xfrc[w,b]+wp.spatial_vector(force,moment)
    if role == 3:
        for side in range(2):
            j=q1
            if side == 1: j=q3
            amp=s.peripheral[w,side,0]
            freq=s.peripheral[w,side,1]
            phase=s.peripheral[w,side,2]
            target_q=amp*wp.sin(freq*t+phase)
            target_v=amp*freq*wp.cos(freq*t+phase)
            s.qfrc[w,j]=wp.clamp(8.0*(target_q-s.qpos[w,j])+.5*(target_v-s.qvel[w,j]),-3.6,3.6)
    s.clock[w]=tick+1


@wp.kernel
def accumulate_explicit(s: State, p: int, d: int):
    w=wp.tid()
    for j in range(2):
        b=p
        if j == 1: b=d
        f=s.xfrc[w,b]
        s.wrench[w,j,0]+=f[0]*.1
        s.wrench[w,j,1]+=f[2]*.1
        s.wrench[w,j,2]+=f[4]*.1


@wp.kernel
def accumulate_contacts(s: State, p: int, d: int, cone: int, njmax: int):
    c=wp.tid()
    if c >= s.nacon[0]: return
    w=s.contact_world[c]
    geoms=s.contact_geom[c]
    b0=s.geom_body[geoms[0]]
    b1=s.geom_body[geoms[1]]
    if (b0 == p and b1 == d) or (b0 == d and b1 == p): return
    force=contact_force_fn(cone,s.contact_frame,s.contact_friction,s.contact_dim,
                           s.contact_adr,s.efc_force,njmax,s.nacon,w,c,True)
    for side in range(2):
        b=p
        if side == 1: b=d
        sign=0.0
        if b0 == b: sign=-1.0
        if b1 == b: sign=1.0
        if sign != 0.0:
            f=sign*wp.spatial_top(force)
            moment=sign*wp.spatial_bottom(force)+wp.cross(s.contact_pos[c]-s.xipos[w,b],f)
            wp.atomic_add(s.wrench,w,side,0,.1*f[0])
            wp.atomic_add(s.wrench,w,side,1,.1*f[2])
            wp.atomic_add(s.wrench,w,side,2,.1*moment[1])
            wp.atomic_max(s.contact,w,side,1.0)


@wp.kernel
def observe(s: State, p: int, d: int, motor: int):
    w=wp.tid()
    q=s.qpos[w,motor]
    s.obs[w,0]=q/1.2
    s.obs[w,1]=s.qvel[w,motor]/6.0
    for side in range(2):
        b=p
        if side == 1: b=d
        v=velocity(s,w,b)
        rot=s.xmat[w,b]
        s.obs[w,2+5*side]=rot[0,2]
        s.obs[w,3+5*side]=rot[0,0]
        s.obs[w,4+5*side]=v[0]/2.0
        s.obs[w,5+5*side]=v[2]/2.0
        s.obs[w,6+5*side]=s.cvel[w,b][1]/6.0
        s.obs[w,14+side]=s.contact[w,side]
        s.obs[w,18+3*side]=s.wrench[w,side,0]/20.0
        s.obs[w,19+3*side]=s.wrench[w,side,1]/20.0
        s.obs[w,20+3*side]=s.wrench[w,side,2]/6.0
    s.obs[w,12]=s.tau[w]/6.0
    s.obs[w,13]=s.u[w]
    s.obs[w,16]=(q+1.2)/2.4
    s.obs[w,17]=(1.2-q)/2.4
