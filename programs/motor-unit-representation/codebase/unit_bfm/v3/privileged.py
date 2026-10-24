"""Frozen, scalar, versioned physics fields. Values returned in fixed scaled SI."""
import numpy as np

SCHEMA_VERSION='v3-physics-4-tick1'
MAX_CONTACTS=128


def _schema():
    fields=[]
    def add(prefix,names,scales,units,source,time='boundary',reference='M at boundary',mask=None):
        if not len(names)==len(scales)==len(units):raise ValueError('schema field metadata length mismatch: '+prefix)
        for name,scale,unit in zip(names,scales,units):
            fields.append(dict(name=f'{prefix}.{name}',scale=float(scale),units=unit,source=source,time=time,reference=reference,mask=mask,invariants=['finite when present','p = SI value / fixed scale','absent slot is zero only with present mask false']))
    add('clock',['time','solve_time','solve_valid'],[10,10,1],['s','s','bool'],'control clock',reference='episode')
    add('topology',['fixed_D','tree_sign','nv','nbody','neq','fixture_P','fixture_D'],[1]*7,['bool','sign','count','count','count','bool','bool'],'compiled mechanical topology',reference='P housing, D output')
    add('floor',['present','nx','ny','nz','offset'],[1,1,1,1,.4],['bool','1','1','1','m'],'world plane transformed into M; n dot x + offset = 0',mask='floor.present')
    add('controller.load',['present','active','side','body_frame','point_fraction','direction_x','direction_y','direction_z','force','couple','phase_elapsed','active_duration','period','cycle','remaining_cycles','start_time'],[1]*4+[1]*4+[20,6,3,3,5,3,3,10],['bool','bool','id','bool','1','1','1','1','N','Nm','s','s','s','count','count','s'],'currently configured deterministic loader state; no future independent random events',mask='controller.load.present')
    add('controller.object',['present','kp','kd','base_x','base_y','base_z','normal_x','normal_y','normal_z','travel','target_x','target_y','target_z','velocity_x','velocity_y','velocity_z'],[1,200,20]+[.4]*3+[1]*3+[.4]*4+[3]*3,['bool','N/m','Ns/m']+['m']*3+['1']*3+['m']*4+['m/s']*3,'current obstacle servo; inertial target velocity expressed in M',mask='controller.object.present')
    add('controller.object_program',['track_x','track_y','track_z','load_side','fraction','start','end','period','repeats','repeated'],[.4,.4,.4,1,1,3,3,5,3,1],['m','m','m','id','1','s','s','s','count','bool'],'current deterministic obstacle program compiled and active from reset; no future random draws',mask='controller.object.present')
    for side in ('P','D'):
        add('controller.fixture'+side,['present','kx','kz','ktheta','dx','dz','dtheta','target_x','target_y','target_z','velocity_x','velocity_y','velocity_z','angle','angular_velocity','horizontal_preload','torque_preload','angle_amplitude','world_x_x','world_x_y','world_x_z'],[1,200,500,5,50,50,5]+[.4]*3+[3]*3+[np.pi,6,1,6,1]+[1]*3,['bool','N/m','N/m','Nm/rad','Ns/m','Ns/m','Nms/rad']+['m']*3+['m/s']*3+['rad','rad/s','1','Nm','rad']+['1']*3,'actual compliant attachment parameters and boundary reference; force validity separate',mask='controller.fixture'+side+'.present')
    for i in range(16):
        add(f'tree.{i}',['present','parent','body_id','weld_id','dof_count','position_x','position_y','position_z','qw','qx','qy','qz'],[1]*5+[.4]*3+[1]*4,['bool','id','id','id','count']+['m']*3+['1']*4,'compiled parent relation, attachment and unconstrained degrees of freedom',time='model constant',reference='parent body frame',mask=f'tree.{i}.present')
    add('common' ,['gravity_x','gravity_z','linear_x','linear_z','angular_y'],[9.81,9.81,3,3,6],['m/s2']*2+['m/s']*2+['rad/s'],'mj_objectVelocity and gravity')
    for body in ['P','D','N0','N1','object0','object1','root','mount']:
        mask=f'body.{body}.present'
        add(f'body.{body}',['present','mass','com_x','com_y','com_z','Ixx','Iyy','Izz','Ixy','Ixz','Iyz','length','max_geom_radius'],[1,2,.4,.4,.4,.1,.1,.1,.1,.1,.1,.4,.1],['bool','kg']+['m']*3+['kg m2']*6+['m']*2,'effective mjModel/body geometry',mask=mask)
        add(f'state.{body}',['x','y','z','r00','r01','r02','r10','r11','r12','r20','r21','r22','vx','vy','vz','wx','wy','wz'],[.4]*3+[1]*9+[3]*3+[6]*3,['m']*3+['1']*9+['m/s']*3+['rad/s']*3,'body transform and world velocity difference',mask=mask)
    add('process.neighbour',['amplitude','frequency','phase'],[1,2,np.pi],['rad','Hz','rad'],'current active reference generator; no future event plan',reference='neighbour joint')
    add('process.support',['motion','frequency','preload'],[.05,1,1],['m','Hz','1'],'current compliant reference generator',reference='world x motion, nominal weight preload')
    for side in ('P','D'):
        add('process.anchor'+side,['x','y','z','angle'],[.4,.4,.4,np.pi],['m','m','m','rad'],'reset attachment anchor, transformed to current M',reference='M at boundary')
    for i in range(16):
        mask=f'joint.{i}.present'
        add(f'joint.{i}',['present','body_id','type','limited','lower','upper','anchor_x','anchor_y','anchor_z','axis_x','axis_y','axis_z','damping','friction','armature'],[1]*4+[np.pi]*2+[.4]*3+[1]*3+[.1,.1,.01],['bool','id','id','bool','rad or m','rad or m']+['m']*3+['1']*3+['SI','SI','SI'],'effective mjModel joint, fixed topology',time='model constant',reference='joint owning body local frame',mask=mask)
    for i in range(64):
        mask=f'geometry.{i}.present'
        add(f'geometry.{i}',['present','body_id','type','size0','size1','size2','x','y','z','qw','qx','qy','qz','friction0','friction1','friction2'],[1,1,1]+[.4]*6+[1]*4+[1]*3,['bool','id','id']+['m']*6+['1']*7,'effective mjModel geom shape and attachment',time='model constant',reference='owning body local frame',mask=mask)
    for i in range(3):
        mask=f'drive.{i}.present'
        add(f'drive.{i}',['present','S','lower','upper','T','delay','damping','friction','armature','tau','q','dq','reference','kp','kd'],[1,6,6,6,.02,.01,.08,.08,.006,6,np.pi,6,np.pi,12,1],['bool','Nm','Nm','Nm','s','s','Nms/rad','Nm','kg m2','Nm','rad','rad/s','rad','Nm/rad','Nms/rad'],'actual millisecond drive/model',mask=mask)
        add(f'drive.{i}',[f'queue{j}' for j in range(11)],[6]*11,['Nm']*11,'drive queue oldest to newest; zero initialized physical requests',mask=mask)
    for i in range(4):
        mask=f'load.{i}.present'
        add(f'load.{i}',['present','active','side','point_x','point_y','point_z','force_x','force_y','force_z','torque_x','torque_y','torque_z','phase'],[1,1,1]+[.4]*3+[20]*3+[6]*3+[1],['bool','bool','id']+['m']*3+['N']*3+['Nm']*3+['id'],'explicit loader before summation',time='last completed solve',reference='M at solve; torque about M origin',mask=mask)
    for i in range(2):
        mask=f'support.{i}.present'
        add(f'support.{i}',['present','kx','kz','ktheta','dx','dz','dtheta','target_x','target_z','target_angle','force_x','force_z','torque_y'],[1,200,500,5,50,50,5,.4,.4,np.pi,20,20,6],['bool','N/m','N/m','Nm/rad','Ns/m','Ns/m','Nms/rad','m','m','rad','N','N','Nm'],'explicit compliant attachment',time='last completed solve',reference='M at solve; torque at M origin',mask=mask)
    for body in ['P','D','N0','N1']:
        mask=f'connection.{body}.present'
        add(f'connection.{body}',['present','Fx','Fy','Fz','Tx','Ty','Tz'],[1]+[20]*3+[6]*3,['bool']+['N']*3+['Nm']*3,'mj_rnePostConstraint cfrc_int; parent on child',time='last completed solve',reference='M at solve; shifted from root subtree COM to M origin',mask=mask)
    for i in range(MAX_CONTACTS):
        mask=f'contact.{i}.present'
        add(f'contact.{i}',['present','geom0','geom1','distance','point_x','point_y','point_z','normal_x','normal_y','normal_z','Fx','Fy','Fz','Tx','Ty','Tz','slip_x','slip_y','slip_z','friction','solref_time','solref_damping'],[1,1,1,.01]+[.4]*3+[1]*3+[20]*3+[6]*3+[3]*3+[1,.02,1],['bool','id','id','m']+['m']*3+['1']*3+['N']*3+['Nm']*3+['m/s']*3+['1','s','1'],'mj_contactForce positive on geom1 and same-solve point velocities',time='last completed solve',reference='M at solve; torque at M origin',mask=mask)
    return tuple(fields)

PHYSICS_SCHEMA=_schema()
P_DIM=len(PHYSICS_SCHEMA)
INDEX={f['name']:i for i,f in enumerate(PHYSICS_SCHEMA)}
SCALES=np.array([f['scale'] for f in PHYSICS_SCHEMA])


def pack(values):
    # Missing registered fields are a coding error. Absent slots must be explicit,
    # with a present=0 mask; callers cannot silently emit unimplemented zeros.
    missing=set(INDEX)-values.keys()
    if missing: raise KeyError(f'missing physics fields: {sorted(missing)[:5]}')
    p=np.array([values[f['name']] for f in PHYSICS_SCHEMA],dtype=np.float64)/SCALES
    if not np.all(np.isfinite(p)): raise FloatingPointError('nonfinite privileged state')
    p.setflags(write=False)
    return p


def empty_masked_values():
    return {f['name']:0. for f in PHYSICS_SCHEMA if f['mask'] is not None}
