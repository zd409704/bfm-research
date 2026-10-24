"""V3 1 kHz CPU oracle. No automatic reset and no V2 imports.

A solve is performed and its wrench/coordinates copied BEFORE Euler integration.
The next boundary keeps that solve snapshot separate from refreshed geometry.
"""
from dataclasses import asdict
import copy
import hashlib
from decimal import Decimal, ROUND_CEILING
import numpy as np
import mujoco
from .randomization import SceneConfig, make_scene, stream
from .mechanics import build_xml, independent_gate
from .privileged import PHYSICS_SCHEMA, P_DIM, pack, empty_masked_values, MAX_CONTACTS, SCHEMA_VERSION

_BLOCK_NAMES={}
for _field in PHYSICS_SCHEMA:
    _BLOCK_NAMES.setdefault(_field["name"].rsplit(".",1)[0],[]).append(_field["name"])


PHYSICS_HZ=1000


def event_tick(seconds):
    """First 1 ms boundary at/after a configured SI time, computed once in decimal."""
    return int((Decimal(str(seconds))*PHYSICS_HZ).to_integral_value(rounding=ROUND_CEILING))


class PhysicallyInvalidTransition(RuntimeError):
    """A failed numerical/physical solve; never a normal terminal transition."""
    def __init__(self, diagnostics, boundary=None):
        self.diagnostics=copy.deepcopy(diagnostics);self.boundary=boundary
        super().__init__('invalid physics: '+str(diagnostics.get('invalid_reasons',diagnostics)))


class Drive:
    def __init__(self,S,capacity,T,delay_ms):
        self.S,self.capacity,self.T,self.delay_ms=map(float,(S,capacity,T,delay_ms))
        self.delay_ms=int(delay_ms); self.queue=np.zeros(11); self.tau=0.; self.target=0.
    def advance(self,u,dt=.001):
        self.queue[:-1]=self.queue[1:]; self.queue[-1]=self.S*u
        self.target=float(np.clip(self.queue[-1-self.delay_ms],-self.capacity,self.capacity))
        self.tau+=(self.target-self.tau)*(-np.expm1(-dt/self.T))
        return self.tau


def _freeze(value):
    if isinstance(value,np.ndarray):
        value=value.copy(); value.setflags(write=False); return value
    if isinstance(value,dict): return {k:_freeze(v) for k,v in value.items()}
    if isinstance(value,list): return [_freeze(v) for v in value]
    return copy.deepcopy(value)


class UnitEnv:
    physics_schema=list(PHYSICS_SCHEMA)
    p_dim=P_DIM
    def __init__(self,config,seed=0):
        self.config=config if isinstance(config,SceneConfig) else SceneConfig(**config)
        c=self.config
        if c.weld: raise ValueError('weld templates disabled pending independent angular momentum calibration')
        self.seed=seed; self.tree_sign=1 if c.fixed_side=='P' else -1
        candidate=mujoco.MjModel.from_xml_string(build_xml(c))
        gate=independent_gate(candidate)
        a,b=gate['limits']; fractions=(1.,.65,.65,.65)
        f=fractions[c.limit_id%4]; width=f*(b-a)
        center=(a+b)/2 if c.limit_id%4<2 else (a+width/2 if c.limit_id%4==2 else b-width/2)
        self.limits=(center-width/2,center+width/2)
        self.xml=build_xml(c,self.limits); self.model=mujoco.MjModel.from_xml_string(self.xml)
        self.data=mujoco.MjData(self.model)
        self.motor=self.model.joint('motor').id
        self.qadr=int(self.model.jnt_qposadr[self.motor]); self.vadr=int(self.model.jnt_dofadr[self.motor])
        self.body_ids={s:self.model.body(s).id for s in ('P','D')}
        for s in ('N0','N1','object0','root','mount'):
            i=mujoco.mj_name2id(self.model,mujoco.mjtObj.mjOBJ_BODY,s)
            if i>=0:self.body_ids[s]=i
        self.neighbours=[]
        for n in range(2):
            i=mujoco.mj_name2id(self.model,mujoco.mjtObj.mjOBJ_JOINT,f'neighbour{n}')
            if i>=0:self.neighbours.append(i)
        self.metadata=dict(config=asdict(c),geometry_gate=gate,xml_sha256=hashlib.sha256(self.xml.encode()).hexdigest(),
            coordinate_map=dict(tree_sign=self.tree_sign,beta_model=0.,qpos_ref=0.,encoder_sign=c.encoder_sign,
                canonical_angle_at_encoder_zero_rad=c.beta_encoder,calibration_valid=True,source='synthetic exact output-side calibration',
                version='v3-1',angle_side='output',torque_side='output',P='housing_link',D='output_link'),
            weld_enabled=False,closed_chain_covered=False,backend='mujoco-cpu',schema_version=SCHEMA_VERSION,
            force_time_contract='forward/rnePostConstraint -> copy solve -> Euler -> kinematics/comPos',
            unimplemented_randomization=['full conditional coverage manifest'],
            shape_family='fork_pin_hollow_bearing_ballast_v1')
        self.fixture_sides=tuple(('P','D') if c.fixture_mode=='both' else
            ((c.fixed_side,) if c.fixture_mode=='auto' and c.scene=='E1' else
             (('P','D') if c.fixture_mode=='auto' and c.scene=='E4' else
              ((c.fixture_mode,) if c.fixture_mode in ('P','D') else ()))))
        self.metadata.update(scene=c.scene,config_id=f'g{c.geometry_seed}:{c.geometry_id}:l{c.limit_id}',
            geometry_seed=c.geometry_seed,variant_id=c.variant_id,neighbour_sides=c.neighbour_sides,
            fixture_sides=list(self.fixture_sides),actual_tags={'neighbour_count':len(self.neighbours),
            'fixture_count':len(self.fixture_sides),'load_mode':c.load_mode,'load_side':c.load_side,
            'load_frame':c.load_frame,'point_bin':c.load_point_bin,'direction_bin':c.load_direction_bin},
            reset_api={'modes':['configured','xi','velocity'],'snapshot':'same model hash + external config hash',
                       'mixture_owner':'pipeline 50% xi / 30% velocity / 20% snapshot'},
            validity_thresholds={'contact_penetration_m':.01,'unit_self_penetration_m':1e-5,
                                 'limit_overshoot_rad':.05,'solver_gradient':1e-3,'soft_limit_activation_margin_rad':.08})
        self._load_start_tick=event_tick(c.load_start)
        self._load_end_tick=event_tick(c.load_end)
        self._load_period_tick=max(1,event_tick(c.load_period))
        self._duration_ticks=event_tick(c.duration)
        self.metadata['clock_contract']={'version':'integer-ms-v1','physics_hz':PHYSICS_HZ,
            'event_quantization':'ceil(decimal_seconds * 1000); start inclusive/end exclusive',
            'load_start_tick':self._load_start_tick,'load_end_tick':self._load_end_tick,
            'load_period_tick':self._load_period_tick,'duration_ticks':self._duration_ticks}
        self.reset()

    @property
    def physics_tick(self):
        return self._physics_tick

    @property
    def process_time(self):
        return self._physics_tick / PHYSICS_HZ

    def _advance_tick(self):
        self._physics_tick+=1
        self.data.time=self.process_time

    def _frame(self):
        return self.data.xanchor[self.motor].copy(),self.data.xmat[self.body_ids['P']].reshape(3,3).copy()

    def _velocity(self,b,point=None):
        v=np.zeros(6);mujoco.mj_objectVelocity(self.model,self.data,mujoco.mjtObj.mjOBJ_BODY,b,v,0)
        if point is not None: v[3:]+=np.cross(v[:3],point-self.data.xipos[b])
        return v

    def _tip(self,side,fraction=1.):
        b=self.body_ids[side]; direction=1 if side=='P' else -1
        return self.data.xpos[b]+self.data.xmat[b].reshape(3,3)@np.array([0.,0.,direction*self.config.lengths[('P','D').index(side)]*fraction])

    def reset(self,episode_id=0):
        c=self.config; mujoco.mj_resetData(self.model,self.data)
        initial_q=c.initial_q if c.initial_fraction is None else self.limits[0]+c.initial_fraction*(self.limits[1]-self.limits[0])
        if not self.limits[0]<=initial_q<=self.limits[1]: raise ValueError('initial_q outside independently gated limits')
        initial_dq=c.initial_dq
        if c.reset_mode in ('stratified','xi','velocity'):
            rng=stream(self.seed,c.geometry_id,c.limit_id,episode_id,'reset')
            xi=(int(rng.integers(10))+rng.uniform(.05,.95))/10
            initial_q=self.limits[0]+xi*(self.limits[1]-self.limits[0])
            initial_dq=0. if c.reset_mode=='xi' else float(rng.choice([-.5,.5,-1.,1.,-2.,2.,-4.,4.]))
        self.data.qpos[self.qadr]=self.tree_sign*initial_q
        self.data.qvel[self.vadr]=self.tree_sign*initial_dq
        root_velocity=c.root_velocity
        if c.reset_mode=='velocity':root_velocity=(float(rng.uniform(-.5,.5)),float(rng.uniform(-.5,.5)),float(rng.uniform(-1.5,1.5)))
        for axis,velocity in zip(('x','z','y'),root_velocity):
            j=mujoco.mj_name2id(self.model,mujoco.mjtObj.mjOBJ_JOINT,'root_'+axis)
            if j>=0:self.data.qvel[self.model.jnt_dofadr[j]]=velocity
        self.drives=[Drive(1.25*c.capacity_nominal,c.capacity_nominal*c.capacity_multiplier,c.response_s,c.delay_ms)]
        self.drives += [Drive(1.25*c.neighbour_capacity,c.neighbour_capacity,c.response_s,c.delay_ms) for _ in self.neighbours]
        self.step_count=0; self.episode_id=episode_id; self._ended=False
        self._solve=None; self._last_u=0.;self._tau_integral=0.;self._u_integral=0.
        self._physics_tick=0;self._episode_start_tick=0;self._episode_start_time=0.;self._interval_checks=[];self._invalid_reasons=[]
        mujoco.mj_forward(self.model,self.data)
        self._anchors={side:self._tip(side).copy() for side in ('P','D')}
        self._angles={side:float(np.arctan2(self.data.xmat[b].reshape(3,3)[0,2],self.data.xmat[b].reshape(3,3)[2,2])) for side,b in self.body_ids.items()}
        self._initialization_attempts=[]
        if 'object0' in self.body_ids:self._place_obstacle()
        if 'object0' in self.body_ids:
            for axis,k in (('x',0),('z',2)):
                self.data.qvel[self.model.jnt_dofadr[self.model.joint('object_'+axis).id]]=c.object_speed*self._object_normal[k]
        self._reset_scene_distance=self._scene_distance()
        self.metadata['initialization']={'attempts':copy.deepcopy(self._initialization_attempts),
            'min_distance_m':self._reset_scene_distance,'requested_q':initial_q,'accepted_q':initial_q,
            'rejected_attempts':sum(not a['accepted'] for a in self._initialization_attempts)}
        if self._reset_scene_distance < -1e-5: raise ValueError(f'illegal initial assembly: distance {self._reset_scene_distance}')
        mujoco.mj_forward(self.model,self.data)
        return self._boundary(False)

    def _place_obstacle(self):
        """Use actual closest surface point/normal, then independently check every pair.

        The dynamic sphere stays planar. Both local link normals are considered;
        outward offsets are resampled without changing installation or joint q.
        """
        m,d,c=self.model,self.data,self.config
        point=self._tip(c.load_side,c.load_fraction)
        R=d.xmat[self.body_ids[c.load_side]].reshape(3,3)
        obstacle=m.geom('obstacle').id
        unit_geoms=[i for i in range(m.ngeom) if m.geom_bodyid[i]==self.body_ids[c.load_side]]
        def position(x):
            for axis,k,offset in (('x',0,.25),('z',2,.9)):
                d.qpos[m.jnt_qposadr[m.joint('object_'+axis).id]]=x[k]-offset
            mujoco.mj_kinematics(m,d);mujoco.mj_comPos(m,d)
        initial_sign=1 if c.variant_id%2==0 else -1
        for sign in (initial_sign,-initial_sign):
            direction=R@np.array([float(sign),0.,0.]);direction[1]=0;direction/=np.linalg.norm(direction)
            for clearance in (.008,.025,.06,.12,.24):
                candidate=point+direction*(c.object_radius+.055+clearance)
                position(candidate)
                # Project from actual closest capsule/sphere surface, not a nominal radius.
                pairs=[]
                for g in unit_geoms:
                    segment=np.zeros(6);distance=mujoco.mj_geomDistance(m,d,g,obstacle,10.,segment)
                    pairs.append((distance,segment.copy(),g))
                distance,segment,g=min(pairs,key=lambda item:item[0])
                normal=segment[3:]-segment[:3]
                if np.linalg.norm(normal)>1e-9:normal/=np.linalg.norm(normal)
                else:normal=direction.copy()
                normal[1]=0
                if np.linalg.norm(normal)<1e-6:normal=direction.copy()
                normal/=np.linalg.norm(normal)
                # Preserve y=0. Refine along planar surface normal using signed distances.
                candidate=point+direction*(c.object_radius+.055+clearance)
                for _ in range(12):
                    position(candidate)
                    closest=min(mujoco.mj_geomDistance(m,d,j,obstacle,10.,np.zeros(6)) for j in unit_geoms)
                    if closest>=clearance-1e-6:break
                    candidate+=normal*(clearance-closest+.0001)
                position(candidate);minimum=self._scene_distance()
                accepted=minimum>=-1e-5
                self._initialization_attempts.append({'normal_world':normal.tolist(),'clearance_m':clearance,
                    'point_world':candidate.tolist(),'source_geom':int(g),'min_distance_m':minimum,'accepted':accepted})
                if accepted:
                    self._object_base=candidate.copy();self._object_normal=normal.copy();self._object_track_origin=point.copy()
                    closest=min(mujoco.mj_geomDistance(m,d,j,obstacle,10.,np.zeros(6)) for j in unit_geoms)
                    self._object_travel=float(closest+.025)
                    return
        raise ValueError('obstacle placement exhausted actual-surface candidates: '+str(self._initialization_attempts))

    def snapshot(self):
        """Full integration state; same-model and same-process compatibility only."""
        if self._ended or self._invalid_reasons:raise ValueError('cannot snapshot ended/invalid physics')
        spec=mujoco.mjtState.mjSTATE_INTEGRATION
        state=np.empty(mujoco.mj_stateSize(self.model,spec))
        self.data.time=self.process_time
        mujoco.mj_getState(self.model,self.data,state,spec)
        return _freeze({'version':2,'model_hash':self.metadata['xml_sha256'],
            'process_hash':hashlib.sha256(repr(asdict(self.config)).encode()).hexdigest(),
            'snapshot_time':self.process_time,'physics_tick':self._physics_tick,'clock_version':'integer-ms-v1','integration_state':state,
            'drives':[copy.deepcopy(x.__dict__) for x in self.drives],
            'anchors':self._anchors,'angles':self._angles,
            'object_base':getattr(self,'_object_base',None),'object_normal':getattr(self,'_object_normal',None),
            'object_travel':getattr(self,'_object_travel',None),'object_track_origin':getattr(self,'_object_track_origin',None),
            'initialization':self.metadata.get('initialization',{})})

    def restore(self,snapshot,episode_id=0):
        expected=hashlib.sha256(repr(asdict(self.config)).encode()).hexdigest()
        if snapshot.get('version')!=2 or snapshot.get('clock_version')!='integer-ms-v1' or snapshot['model_hash']!=self.metadata['xml_sha256'] or snapshot['process_hash']!=expected:
            raise ValueError('incompatible snapshot model/process hash')
        tick=snapshot.get('physics_tick')
        if type(tick) is not int or tick<0 or snapshot['snapshot_time']!=tick/PHYSICS_HZ:
            raise ValueError('incompatible snapshot integer clock')
        mujoco.mj_resetData(self.model,self.data)
        mujoco.mj_setState(self.model,self.data,np.asarray(snapshot['integration_state']),mujoco.mjtState.mjSTATE_INTEGRATION)
        for drive,saved in zip(self.drives,snapshot['drives']):drive.__dict__.update(copy.deepcopy(saved));drive.queue=np.array(drive.queue,copy=True)
        self._anchors={k:np.array(v,copy=True) for k,v in snapshot['anchors'].items()};self._angles=copy.deepcopy(snapshot['angles'])
        for name in ('object_base','object_normal','object_travel','object_track_origin'):
            if snapshot[name] is not None:setattr(self,'_'+name,copy.deepcopy(snapshot[name]))
        self._physics_tick=tick;self._episode_start_tick=tick;self.data.time=self.process_time
        self._episode_start_time=self.process_time;self.episode_id=episode_id;self.step_count=0;self._ended=False
        self._solve=None;self._last_u=0.;self._tau_integral=0.;self._u_integral=0.;self._interval_checks=[];self._invalid_reasons=[]
        # Forward must not replace the saved warmstart used by the next solve.
        warm=self.data.qacc_warmstart.copy();mujoco.mj_forward(self.model,self.data);self.data.qacc_warmstart[:]=warm
        self.metadata['restore']={'snapshot_time':snapshot['snapshot_time'],'episode_start_time':self._episode_start_time,
                                  'history_padding':True,'truncation_after_s':self.config.duration}
        boundary=self._boundary(False)
        if not boundary['valid']:self._fail(boundary['diagnostics'])
        return boundary

    def _load_state(self,tick=None):
        tick=self._physics_tick if tick is None else tick
        if not isinstance(tick,(int,np.integer)):raise TypeError('process clock requires integer physics ticks')
        c=self.config;elapsed=tick-self._load_start_tick
        cycle=max(0,elapsed//self._load_period_tick) if c.load_mode=='repeated' else 0
        phase_ticks=elapsed-cycle*self._load_period_tick
        active=elapsed>=0 and cycle<c.load_repeats and phase_ticks<self._load_end_tick-self._load_start_tick
        return bool(active),int(cycle),phase_ticks/PHYSICS_HZ,0 if elapsed<0 else (1 if active else 2)

    def _support_reference(self,side,t):
        c=self.config;omega=2*np.pi*c.support_frequency
        target=self._anchors[side]+np.array([c.support_motion*np.sin(omega*t),0.,0.])
        velocity=np.array([c.support_motion*omega*np.cos(omega*t),0.,0.])
        angle=self._angles[side]+c.support_angle_motion*np.sin(omega*t)
        angular=c.support_angle_motion*omega*np.cos(omega*t)
        return target,velocity,angle,angular

    def _obstacle_reference(self,tick=None):
        tick=self._physics_tick if tick is None else tick
        c=self.config;_,cycle,phase,_=self._load_state(tick)
        local=tick-min(cycle,c.load_repeats-1)*self._load_period_tick if c.load_mode=='repeated' else tick
        ramp_ticks=300;approach_start=max(0,self._load_start_tick-ramp_ticks)
        approach=np.clip((local-approach_start)/ramp_ticks,0,1)
        release=np.clip((local-self._load_end_tick)/ramp_ticks,0,1)
        adot=PHYSICS_HZ/ramp_ticks if approach_start<local<approach_start+ramp_ticks else 0.
        rdot=PHYSICS_HZ/ramp_ticks if self._load_end_tick<local<self._load_end_tick+ramp_ticks else 0.
        # Return to base before next cycle, so repeated withdrawal is continuous.
        travel=self._object_travel
        tracking=self._tip(c.load_side,c.load_fraction)-self._object_track_origin
        tracking_velocity=self._velocity(self.body_ids[c.load_side],self._tip(c.load_side,c.load_fraction))[3:]
        target=self._object_base+tracking+self._object_normal*travel*(-approach+release)
        velocity=tracking_velocity+self._object_normal*travel*(-adot+rdot)
        return target,velocity

    @property
    def known(self):
        c=self.config;O,R=self._frame();rigid=[]
        multiplier=c.density_multiplier if c.mass_error else 1.
        for s in ('P','D'):
            b=self.body_ids[s]; com=R.T@(self.data.xipos[b]-O)
            I=self.model.body_inertia[b];rot=R.T@self.data.ximat[b].reshape(3,3)
            rigid.extend([self.model.body_mass[b]/multiplier,com[0],com[2],(rot@np.diag(I)@rot.T)[1,1]/multiplier])
        C=c.capacity_nominal if c.drive_error else self.drives[0].capacity
        drive=[self.drives[0].S,-C,C,.01,.005,.03,.02,.003] if c.drive_error else [self.drives[0].S,-C,C,c.response_s,c.delay_ms*.001,c.damping,c.friction,c.armature]
        return _freeze(dict(lengths=np.array(c.lengths),limits=np.array(self.limits),rigid=np.array(rigid),rigid_valid=np.ones(8),drive=np.array(drive),drive_valid=np.ones(8)))

    def _scene_distance(self):
        m,d=self.model,self.data;minimum=1e6;fromto=np.zeros(6)
        # Independently inspect every distinct-body pair, even parent/child.
        for a in range(m.ngeom):
            for b in range(a+1,m.ngeom):
                if m.geom_bodyid[a]==m.geom_bodyid[b]:continue
                minimum=min(minimum,mujoco.mj_geomDistance(m,d,a,b,10,fromto))
        return float(minimum)

    def _apply_point(self,b,point,force,couple):
        self.data.xfrc_applied[b,:3]+=force
        self.data.xfrc_applied[b,3:]+=couple+np.cross(point-self.data.xipos[b],force)

    def _forces(self,u):
        c=self.config;m,d=self.model,self.data;t=self.process_time;O,R=self._frame()
        d.qfrc_applied[:]=0;d.xfrc_applied[:]=0
        tau=self.drives[0].advance(u);d.qfrc_applied[self.vadr]=self.tree_sign*tau
        references=[]
        for n,j in enumerate(self.neighbours):
            qa,va=int(m.jnt_qposadr[j]),int(m.jnt_dofadr[j])
            ref=c.neighbour_amplitude*np.sin(2*np.pi*c.neighbour_frequency*t+c.neighbour_phase+n*np.pi)
            request=(c.neighbour_kp*(ref-d.qpos[qa])-c.neighbour_kd*d.qvel[va])/self.drives[n+1].S
            d.qfrc_applied[va]=self.drives[n+1].advance(np.clip(request,-1,1));references.append(float(ref))
        loads=[];active,cycle,load_phase,phase_id=self._load_state()
        side=c.load_side; b=self.body_ids[side];point=self._tip(side,c.load_fraction)
        force=np.array([np.cos(c.load_angle),0,np.sin(c.load_angle)])*c.load_force*active
        if c.load_frame=='body':force=d.xmat[b].reshape(3,3)@force
        couple=np.array([0.,c.load_couple*active,0.]);self._apply_point(b,point,force,couple)
        loads.append([1.,float(active),float(side=='D'),*(R.T@(point-O)),*(R.T@force),*(R.T@(couple+np.cross(point-O,force))),float(phase_id)])
        supports=[]
        sides=self.fixture_sides
        for side in sides:
            b=self.body_ids[side];p=self._tip(side);v=self._velocity(b,p)
            k=np.array(c.support_k);mass=sum(m.body_mass);damp=2*c.support_damping_ratio*np.sqrt(k*np.array([mass,mass,.05]))
            target,target_v,target_angle,target_angular=self._support_reference(side,t)
            angle=np.arctan2(d.xmat[b].reshape(3,3)[0,2],d.xmat[b].reshape(3,3)[2,2]);err=np.arctan2(np.sin(target_angle-angle),np.cos(target_angle-angle))
            f=np.array([k[0]*(target[0]-p[0])-damp[0]*(v[3]-target_v[0])+c.support_horizontal_preload*mass*9.81/len(sides),0,k[1]*(target[2]-p[2])-damp[1]*v[5]+c.support_preload*mass*9.81/len(sides)])
            torque=np.array([0,k[2]*err-damp[2]*(v[1]-target_angular)+c.support_torque_preload,0]);self._apply_point(b,p,f,torque)
            fm=R.T@f;tm=R.T@(torque+np.cross(p-O,f));tar=R.T@(target-O)
            supports.append([1.,*k,*damp,tar[0],tar[2],np.arctan2(np.sin(target_angle-np.arctan2(R[0,2],R[2,2])),np.cos(target_angle-np.arctan2(R[0,2],R[2,2]))),fm[0],fm[2],tm[1]])
        if 'object0' in self.body_ids:
            b=self.body_ids['object0'];p=d.xpos[b];v=self._velocity(b)
            target,target_velocity=self._obstacle_reference()
            f=150*(target-p)-10*(v[3:]-target_velocity)+np.array([0,0,c.object_mass*9.81])
            self._apply_point(b,p,f,np.zeros(3))
            loads.append([1.,1.,2.,*(R.T@(p-O)),*(R.T@f),*(R.T@np.cross(p-O,f)),float(phase_id)])
        return loads,supports,references

    def _snapshot_solve(self,loads,supports,references):
        m,d=self.model,self.data;O,R=self._frame()
        if d.ncon>MAX_CONTACTS: raise OverflowError('contact schema overflow; expand and recollect')
        connections={}
        for name,b in self.body_ids.items():
            if name not in ('P','D','N0','N1'):continue
            C=d.subtree_com[m.body_rootid[b]];T,F=d.cfrc_int[b,:3],d.cfrc_int[b,3:]
            connections[name]=[1.,*(R.T@F),*(R.T@(T+np.cross(C-O,F)))]
        contacts=[]
        for k in range(d.ncon):
            con=d.contact[k]
            if con.efc_address<0:continue
            raw=np.zeros(6)
            if hasattr(self,'_device_contact_forces'):raw[:]=self._device_contact_forces[k]
            else:mujoco.mj_contactForce(m,d,k,raw)
            A=con.frame.reshape(3,3).T;F=A@raw[:3];T=A@raw[3:]
            b0,b1=m.geom_bodyid[con.geom[0]],m.geom_bodyid[con.geom[1]]
            v0=self._velocity(b0,con.pos)[3:];v1=self._velocity(b1,con.pos)[3:]
            normal=A[:,0];slip=v1-v0;slip-=normal*(slip@normal)
            contacts.append([1.,*con.geom,con.dist,*(R.T@(con.pos-O)),*(R.T@normal),*(R.T@F),*(R.T@(T+np.cross(con.pos-O,F))),*(R.T@slip),con.friction[0],*con.solref])
        contacts.sort(key=lambda row:(int(row[1]),int(row[2]),*np.round(row[4:7],8)))
        return dict(time=self.process_time,tick=self._physics_tick,origin=O,rotation=R,connections=connections,contacts=contacts,loads=loads,supports=supports,references=references,
                    qacc=d.qacc.copy(),q=d.qpos.copy(),dq=d.qvel.copy(),constraint=d.qfrc_constraint.copy())

    def _validate_solve(self):
        m,d=self.model,self.data;reasons=[]
        arrays={'qpos':d.qpos,'qvel':d.qvel,'qacc':d.qacc,'constraint':d.qfrc_constraint,
                'tree_force':d.cfrc_int,'explicit_force':d.xfrc_applied}
        if self._solve:
            arrays.update({'saved_'+k:np.asarray(self._solve[k]) for k in ('q','dq','qacc','constraint')})
            for key in ('contacts','loads','supports'):
                arrays['saved_'+key]=np.asarray(self._solve[key])
        for name,value in arrays.items():
            if not np.isfinite(value).all():reasons.append('nonfinite_'+name)
        warnings=[int(w.number) for w in d.warning]
        if any(warnings):reasons.append('mujoco_warning')
        if d.ncon>MAX_CONTACTS or d.nefc>1024:reasons.append('solver_capacity')
        penetration=max((max(0.,-con.dist) for con in d.contact),default=0.)
        if penetration>.01:reasons.append('scene_penetration')
        unit=set(self.body_ids[x] for x in ('P','D'))
        self_pen=max((max(0.,-con.dist) for con in d.contact if set(m.geom_bodyid[con.geom]).issubset(unit)),default=0.)
        if self_pen>1e-5:reasons.append('unit_self_collision')
        q=self.tree_sign*d.qpos[self.qadr]
        if q<self.limits[0]-.05 or q>self.limits[1]+.05:reasons.append('joint_limit_overshoot')
        iterations=int(d.solver_niter[0]);gradient=0.
        if iterations:
            gradient=float(d.solver[iterations-1].gradient)
            if not np.isfinite(gradient) or (iterations>=m.opt.iterations and gradient>1e-3):reasons.append('solver_not_converged')
        return {'solver_valid':not reasons,'invalid_reasons':reasons,'solver_iterations':iterations,
                'solver_gradient':gradient,'max_penetration_m':penetration,'unit_self_penetration_m':self_pen,
                'numerical_warning_counts':warnings}

    def _fail(self,diagnostics):
        self._invalid_reasons=list(diagnostics['invalid_reasons']);self._ended=True
        try:boundary=self._boundary(False)
        except (FloatingPointError,ValueError):
            boundary={'time':self.process_time,'valid':False,'terminated':False,'truncated':False,
                      'interval_valid':False,'p':None,'diagnostics':copy.deepcopy(diagnostics)}
        raise PhysicallyInvalidTransition(diagnostics,boundary)

    def _substep(self,u):
        self.data.time=self.process_time
        loads,supports,refs=self._forces(u)
        mujoco.mj_forward(self.model,self.data)
        mujoco.mj_rnePostConstraint(self.model,self.data)
        self._solve=self._snapshot_solve(loads,supports,refs)
        check=self._validate_solve();self._interval_checks.append(check)
        if not check['solver_valid']:
            check['substep_in_interval']=len(self._interval_checks)-1;self._fail(check)
        mujoco.mj_Euler(self.model,self.data)
        self._advance_tick()
        mujoco.mj_kinematics(self.model,self.data);mujoco.mj_comPos(self.model,self.data);mujoco.mj_comVel(self.model,self.data)
        return self.drives[0].tau*.001

    def step(self,u_c):
        if self._ended:raise RuntimeError('episode ended; explicit reset required')
        u=float(u_c)
        if not np.isfinite(u) or abs(u)>1+1e-9:raise ValueError('u_c must be finite in [-1,1]')
        self._interval_checks=[]
        self._tau_integral=sum(self._substep(u) for _ in range(10));self._u_integral=u*.01
        self._last_u=u;self.step_count+=1
        boundary=self._boundary(True)
        if not boundary['valid']:self._fail(boundary['diagnostics'])
        self._ended=boundary['terminated'] or boundary['truncated']
        return boundary

    def _privileged(self):
        m,d=self.model,self.data;c=self.config;O,R=self._frame();v=empty_masked_values()
        v.update({'clock.time':self.process_time,'clock.solve_time':self._solve['time'] if self._solve else 0.,'clock.solve_valid':float(self._solve is not None and not self._invalid_reasons and self._validate_solve()['solver_valid'])})
        common=self._velocity(self.body_ids['P'],O);grav=R.T@m.opt.gravity;lin=R.T@common[3:];ang=R.T@common[:3]
        v.update(dict(zip(['common.gravity_x','common.gravity_z','common.linear_x','common.linear_z','common.angular_y'],[grav[0],grav[2],lin[0],lin[2],ang[1]])))
        def block(prefix,values):
            names=_BLOCK_NAMES[prefix]
            if len(names)!=len(values):raise ValueError((prefix,len(names),len(values)))
            v.update(zip(names,values))
        block('topology',[float(c.fixed_side=='D'),self.tree_sign,m.nv,m.nbody,m.neq,float('P' in self.fixture_sides),float('D' in self.fixture_sides)])
        floor=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_GEOM,'floor')
        if floor>=0:
            normal=d.geom_xmat[floor].reshape(3,3)[:,2]
            block('floor',[1.,*(R.T@normal),float(normal@(O-d.geom_xpos[floor]))])
        if m.nbody>16:raise OverflowError('tree schema overflow')
        for b in range(m.nbody):
            block(f'tree.{b}',[1.,m.body_parentid[b],b,m.body_weldid[b],m.body_dofnum[b],*m.body_pos[b],*m.body_quat[b]])
        active,cycle,phase,phase_id=self._load_state()
        if True:  # The deterministic generator is configured and active from reset.
            direction=np.array([np.cos(c.load_angle),0.,np.sin(c.load_angle)])
            if c.load_frame=='body':direction=d.xmat[self.body_ids[c.load_side]].reshape(3,3)@direction
            block('controller.load',[1.,float(active),float(c.load_side=='D'),float(c.load_frame=='body'),c.load_fraction,*(R.T@direction),c.load_force,c.load_couple,phase,(self._load_end_tick-self._load_start_tick)/PHYSICS_HZ,self._load_period_tick/PHYSICS_HZ,cycle,max(0,c.load_repeats-cycle),self._load_start_tick/PHYSICS_HZ])
        if 'object0' in self.body_ids:
            target,velocity=self._obstacle_reference()
            block('controller.object_program',[*(R.T@(self._object_track_origin-O)),float(c.load_side=='D'),c.load_fraction,self._load_start_tick/PHYSICS_HZ,self._load_end_tick/PHYSICS_HZ,self._load_period_tick/PHYSICS_HZ,c.load_repeats,float(c.load_mode=='repeated')])
            block('controller.object',[1.,150.,10.,*(R.T@(self._object_base-O)),*(R.T@self._object_normal),self._object_travel,*(R.T@(target-O)),*(R.T@velocity)])
        for side in self.fixture_sides:
            k=np.array(c.support_k);mass=sum(m.body_mass);damp=2*c.support_damping_ratio*np.sqrt(k*np.array([mass,mass,.05]))
            target,velocity,angle,angular=self._support_reference(side,self.process_time)
            mangle=np.arctan2(R[0,2],R[2,2]);relative_angle=np.arctan2(np.sin(angle-mangle),np.cos(angle-mangle))
            block('controller.fixture'+side,[1.,*k,*damp,*(R.T@(target-O)),*(R.T@velocity),relative_angle,angular,c.support_horizontal_preload,c.support_torque_preload,c.support_angle_motion,*(R.T@np.array([1.,0.,0.]))])
        for name,b in self.body_ids.items():
            com=R.T@(d.xipos[b]-O);rot=R.T@d.ximat[b].reshape(3,3);I=rot@np.diag(m.body_inertia[b])@rot.T
            idx=('P','D','N0','N1','object0','root','mount').index(name)
            length=(tuple(c.lengths)+tuple(c.neighbour_lengths)+(0.,0.,0.))[idx];radius=max((m.geom_size[g,0] for g in range(m.ngeom) if m.geom_bodyid[g]==b),default=0.)
            block('body.'+name,[1.,m.body_mass[b],*com,*np.diag(I),I[0,1],I[0,2],I[1,2],length,radius])
            vel=self._velocity(b);pos=R.T@(d.xpos[b]-O);relative=R.T@d.xmat[b].reshape(3,3)
            block('state.'+name,[*pos,*relative.ravel(),*(R.T@(vel[3:]-common[3:])),*(R.T@(vel[:3]-common[:3]))])
        block('process.neighbour',[c.neighbour_amplitude,c.neighbour_frequency,c.neighbour_phase])
        block('process.support',[c.support_motion,c.support_frequency,c.support_preload])
        mangle=np.arctan2(R[0,2],R[2,2])
        for side in ('P','D'):
            block('process.anchor'+side,[*(R.T@(self._anchors[side]-O)),np.arctan2(np.sin(self._angles[side]-mangle),np.cos(self._angles[side]-mangle))])
        if m.njnt>16:raise OverflowError('joint schema overflow')
        for j in range(m.njnt):
            va=m.jnt_dofadr[j]
            block(f'joint.{j}',[1.,m.jnt_bodyid[j],m.jnt_type[j],m.jnt_limited[j],*m.jnt_range[j],*m.jnt_pos[j],*m.jnt_axis[j],m.dof_damping[va],m.dof_frictionloss[va],m.dof_armature[va]])
        if m.ngeom>64:raise OverflowError('geometry schema overflow')
        for i in range(m.ngeom):
            block(f'geometry.{i}',[1.,m.geom_bodyid[i],m.geom_type[i],*m.geom_size[i],*m.geom_pos[i],*m.geom_quat[i],*m.geom_friction[i]])
        for n,drive in enumerate(self.drives):
            j=self.motor if n==0 else self.neighbours[n-1];qa=m.jnt_qposadr[j];va=m.jnt_dofadr[j];sgn=self.tree_sign if n==0 else 1
            reference=self._solve['references'][n-1] if n and self._solve else 0.
            block(f'drive.{n}',[1.,drive.S,-drive.capacity,drive.capacity,drive.T,drive.delay_ms*.001,m.dof_damping[va],m.dof_frictionloss[va],m.dof_armature[va],drive.tau,sgn*d.qpos[qa],sgn*d.qvel[va],reference,c.neighbour_kp if n else 0.,c.neighbour_kd if n else 0.,*drive.queue])
        if self._solve and self._validate_solve()['solver_valid'] and not self._invalid_reasons:
            for name,values in self._solve['connections'].items():block('connection.'+name,values)
            for prefix in ('load','support','contact'):
                for i,values in enumerate(self._solve[prefix+'s']):block(f'{prefix}.{i}',values)
        return pack(v)

    def _boundary(self,valid_interval):
        d=self.data;c=self.config;solve=self._solve
        check=self._validate_solve();valid=check['solver_valid'] and not self._invalid_reasons
        contacts=solve['contacts'] if solve else []
        contact_force=sum(np.linalg.norm(row[10:13]) for row in contacts if
            not {int(self.model.geom_bodyid[int(row[1])]),int(self.model.geom_bodyid[int(row[2])])}.issubset(set(self.body_ids[s] for s in ('P','D'))))
        supports=solve['supports'] if solve else []
        support_force=[float(np.linalg.norm(row[10:12])) for row in supports]
        neighbour_dq=[abs(float(d.qvel[self.model.jnt_dofadr[j]])) for j in self.neighbours]
        neighbour_tau=[abs(x.tau) for x in self.drives[1:]]
        diagnostics=dict(solve_valid=bool(solve),solve_time=solve['time'] if solve else None,
            contact_count=len(contacts),contact_force=contact_force,contact_active=contact_force>.1,
            neighbour_active=any(x>.02 for x in neighbour_dq),neighbour_dq=neighbour_dq,neighbour_tau=neighbour_tau,
            neighbour_stall=any(t>.1 and q<=.02 for t,q in zip(neighbour_tau,neighbour_dq)),
            support_force=support_force,bilateral_active=len(support_force)==2 and min(support_force)>.1,
            load_active=bool(solve and solve['loads'][0][1]),released=bool(solve and solve['loads'][0][-1]==2),
            saturated=abs(self.drives[0].target)>=self.drives[0].capacity-1e-8,
            reset_min_distance=self._reset_scene_distance if hasattr(self,'_reset_scene_distance') else None,
            max_penetration=max([max(0.,-x[3]) for x in contacts],default=0.),contact_overflow=False,
            raw_qpos=float(d.qpos[self.qadr]),raw_encoder_q=(self.tree_sign*d.qpos[self.qadr]-c.beta_encoder)*c.encoder_sign)
        if diagnostics['max_penetration']>.02:valid=False
        diagnostics['numerical_warning_counts']=[int(w.number) for w in d.warning]
        if any(diagnostics['numerical_warning_counts'][i] for i in (0,4,5,6)):valid=False
        diagnostics.update(check)
        diagnostics['solver_valid']=bool(valid and solve is not None)
        diagnostics['solve_valid']=diagnostics['solver_valid']
        unit=set(self.body_ids[x] for x in ('P','D'))
        relevant=[row for row in contacts if len(unit.intersection({int(self.model.geom_bodyid[int(row[1])]),int(self.model.geom_bodyid[int(row[2])])}))==1]
        diagnostics['contact_normal_force_N']=float(sum(abs(np.dot(row[7:10],row[10:13])) for row in relevant))
        diagnostics['adjacent_max_abs_dq']=max(neighbour_dq,default=0.)
        diagnostics['adjacent_max_abs_tau_Nm']=max(neighbour_tau,default=0.)
        diagnostics['adjacent_declared_capacity_Nm']=c.neighbour_capacity if self.neighbours else 0.
        diagnostics['adjacent_axes']=[{'abs_dq':q,'abs_tau_Nm':tau,'declared_capacity_Nm':c.neighbour_capacity} for q,tau in zip(neighbour_dq,neighbour_tau)]
        for side in ('P','D'):
            row=supports[self.fixture_sides.index(side)] if side in self.fixture_sides and supports else None
            diagnostics['fixture_'+side+'_force_N']=float(np.linalg.norm(row[10:12])) if row else 0.
            diagnostics['fixture_'+side+'_torque_Nm']=abs(float(row[12])) if row else 0.
        diagnostics['applied_load_norm_N']=float(np.linalg.norm(solve['loads'][0][6:9])) if solve else 0.
        diagnostics['applied_load_couple_Nm']=abs(c.load_couple) if solve and solve['loads'][0][1] else 0.
        diagnostics['interval_solve_count']=len(self._interval_checks)
        diagnostics['interval_all_solver_valid']=bool(self._interval_checks and all(x['solver_valid'] for x in self._interval_checks))
        diagnostics['physics_tick']=self._physics_tick
        diagnostics['episode_start_tick']=self._episode_start_tick
        diagnostics['episode_elapsed_s']=(self._physics_tick-self._episode_start_tick)/PHYSICS_HZ
        diagnostics['invalid_reasons']=list(dict.fromkeys(check['invalid_reasons']+self._invalid_reasons))
        diagnostics['e4_simultaneous']=c.scene=='E4' and diagnostics['neighbour_active'] and (diagnostics['contact_active'] or diagnostics['bilateral_active'])
        return _freeze(dict(time=self.process_time,q=float(self.tree_sign*d.qpos[self.qadr]),dq=float(self.tree_sign*d.qvel[self.vadr]),
            tau_endpoint=self.drives[0].tau,u_previous=self._last_u,tau_integral=self._tau_integral,u_integral=self._u_integral,
            interval_dt=.01 if valid_interval else 0.,interval_valid=valid_interval and valid,p=self._privileged(),valid=valid,
            terminated=False,truncated=bool(self._physics_tick-self._episode_start_tick>=self._duration_ticks and valid),diagnostics=diagnostics))

    def static_bias_torque(self,boundary=None):
        """Privileged rule-only gravity bias, zero-velocity fixed configuration."""
        scratch=mujoco.MjData(self.model);scratch.qpos[:]=self.data.qpos
        mujoco.mj_forward(self.model,scratch)
        return float(self.tree_sign*scratch.qfrc_bias[self.vadr])

    def close(self):
        pass
