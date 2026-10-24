"""Batched single-structure Simulation bucket with explicit millisecond hooks."""
import hashlib
import numpy as np
import torch
import mujoco
import mujoco_warp as mjw
import warp as wp
from mjlab.sim.sim import Simulation, SimulationCfg, MujocoCfg
from mjlab.managers.event_manager import requires_model_fields, RecomputeLevel
from .mechanics import Structure
from .history import History
from . import kernels as k


@requires_model_fields('body_mass','body_inertia','dof_damping','dof_frictionloss',
                       'dof_armature','geom_friction',recompute=RecomputeLevel.set_const)
def randomization_fields():
    pass


def stream(seed, structure, episode, name):
    # Separate per-episode streams: world resets and parallel count do not couple draws.
    text=f'{seed}:{structure}:{episode}:{name}'.encode()
    return np.random.default_rng(int.from_bytes(hashlib.sha256(text).digest()[:8],'little'))


class UnitEnv:
    def __init__(self, structure: Structure, nworld=128, device='cuda:0', seed=73001):
        self.structure,self.nworld,self.device,self.seed=structure,nworld,device,seed
        self.model=structure.compile()
        cfg=SimulationCfg(nconmax=64,njmax=256,mujoco=MujocoCfg(timestep=.001,
                            iterations=20,integrator='implicitfast'))
        with wp.ScopedDevice(device):
            self.sim=Simulation(nworld,cfg,model=self.model,device=device)
            self.sim.expand_model_fields(randomization_fields.model_fields)
        self.p,self.d=(self.model.body(x).id for x in ('P','D'))
        self.motor=int(self.model.joint('motor').dofadr[0])
        self.q1=int(self.model.joint('q1').dofadr[0]) if structure.role==3 else 0
        self.q3=int(self.model.joint('q3').dofadr[0]) if structure.role==3 else 0
        self.defaults={f:self.sim.get_default_field(f).clone() for f in randomization_fields.model_fields}
        self.s=k.State()
        data=self.sim.wp_data; mod=self.sim.wp_model
        mapping={'qpos':'qpos','qvel':'qvel','qfrc':'qfrc_applied','xfrc':'xfrc_applied',
                 'xpos':'xpos','xipos':'xipos','xmat':'xmat','cvel':'cvel','subtree_com':'subtree_com',
                 'nacon':'nacon'}
        for dst,src in mapping.items(): setattr(self.s,dst,getattr(data,src))
        self.s.efc_force=data.efc.force
        for dst,src in {'rootid':'body_rootid','body_mass':'body_mass','geom_body':'geom_bodyid'}.items():
            setattr(self.s,dst,getattr(mod,src))
        for dst,src in {'contact_geom':'geom','contact_pos':'pos','contact_frame':'frame',
                        'contact_friction':'friction','contact_dim':'dim','contact_adr':'efc_address',
                        'contact_world':'worldid'}.items(): setattr(self.s,dst,getattr(data.contact,src))
        self.tensors={}
        shapes={'u':(nworld,),'tau':(nworld,),'cap':(nworld,),'tm':(nworld,),
                'delay':(nworld,),'clock':(nworld,),'ring':(nworld,11),'support':(nworld,7),
                'pulses':(nworld,16,7),'peripheral':(nworld,2,3),'wrench':(nworld,2,3),
                'contact':(nworld,2),'work':(nworld,2),'obs':(nworld,24)}
        for name,shape in shapes.items():
            dtype=torch.int32 if name in ('delay','clock') else torch.float32
            tensor=torch.zeros(shape,dtype=dtype,device=device)
            self.tensors[name]=tensor; setattr(self.s,name,wp.from_torch(tensor))
        self.tensors['tm'].fill_(.01); self.tensors['cap'].fill_(6.)
        self.m=torch.from_numpy(structure.nominal(self.model)).to(device).repeat(nworld,1)
        self.history=History(nworld,device)
        self.steps=0
        self.bank=[]
        self.reset_stats={'ordinary':0,'wide':0,'snapshot':0,'snapshot_fallback':0}
        self.episode_ids=np.arange(nworld)
        self.reset(self.episode_ids,level=0,snapshots=False)
        self.reset_stats={name:0 for name in self.reset_stats}
        with wp.ScopedDevice(device):
            self._physics()  # Warm up kernels before capture; then reset real state.
            with wp.ScopedCapture() as capture: self._physics()
            self.graph=capture.graph
        self.reset(self.episode_ids,level=0,snapshots=False)

    def _launch(self,kernel,args,dim=None):
        wp.launch(kernel,dim=self.nworld if dim is None else dim,inputs=args,device=self.device)

    def _physics(self):
        self._launch(k.clear_interval,[self.s])
        for _ in range(10):
            mjw.forward(self.sim.wp_model,self.sim.wp_data)
            self._launch(k.drive,[self.s,self.structure.role,self.p,self.d,self.motor,
                                  self.structure.lp,self.structure.ld,self.q1,self.q3,.001])
            mjw.step(self.sim.wp_model,self.sim.wp_data)
            self._launch(k.accumulate_explicit,[self.s,self.p,self.d])
            if self.structure.role==2:
                self._launch(k.accumulate_contacts,[self.s,self.p,self.d,int(self.model.opt.cone),
                                                   self.sim.wp_data.njmax],
                             self.sim.wp_data.contact.pos.shape[0])
        mjw.forward(self.sim.wp_model,self.sim.wp_data)
        self._launch(k.observe,[self.s,self.p,self.d,self.motor])

    def step(self,u):
        before=self.tensors['u'].clone()
        self.tensors['u'].copy_(u.detach().flatten().clamp(-1,1))
        with wp.ScopedDevice(self.device): wp.capture_launch(self.graph)
        o=self.tensors['obs'].clone()
        self.history.append(o)
        self.steps+=1
        y=torch.cat((o,(self.tensors['u']-before)[:,None]),-1)
        return self.history.input(self.m),y

    def _initial(self,rng,wide):
        q=np.zeros(self.model.nq,dtype=np.float32)
        v=np.zeros(self.model.nv,dtype=np.float32)
        q[self.motor]=rng.uniform(-1.1 if wide else -.6,1.1 if wide else .6)
        v[self.motor]=rng.uniform(-4 if wide else -2,4 if wide else 2)
        if self.structure.role==1:
            q[:3]=[rng.uniform(-.05,.05),rng.uniform(-.05,.05),rng.uniform(-.35,.35)]
            v[:3]=[rng.uniform(-.5,.5),rng.uniform(-.5,.5),rng.uniform(-1.5,1.5)]
        elif self.structure.role==2:
            # Choose distal or proximal as low side; derive legal height from box corners.
            q[2]=rng.choice([0.,np.pi])+rng.uniform(-.35,.35)
            v[:3]=[rng.uniform(-.5,.5),rng.uniform(-.3,.3),rng.uniform(-1.5,1.5)]
            data=mujoco.MjData(self.model); data.qpos[:]=q; mujoco.mj_forward(self.model,data)
            bottoms=[]
            for name in ('P_box','D_box'):
                g=self.model.geom(name).id
                extent=np.abs(data.geom_xmat[g].reshape(3,3)[2])@self.model.geom_size[g]
                bottoms.append(data.geom_xpos[g,2]-extent)
            clearance=rng.uniform(.02,.10) if rng.random()<.2 else .001
            q[1]+=clearance-min(bottoms)
        elif self.structure.role==3:
            q[[self.q1,self.q3]]=rng.uniform(-.6,.6,2)
            v[[self.q1,self.q3]]=rng.uniform(-1.5,1.5,2)
        return q,v

    def reset(self,episode_ids=None,level=1.,snapshots=True):
        self.steps=0
        self.reset_stats={name:0 for name in self.reset_stats}
        if episode_ids is not None: self.episode_ids=np.asarray(episode_ids)
        self.level=float(level)
        self.sim.reset()
        arrays={name:np.zeros(tuple(t.shape),np.float32) for name,t in self.tensors.items()}
        qpos=np.zeros((self.nworld,self.model.nq),np.float32)
        qvel=np.zeros((self.nworld,self.model.nv),np.float32)
        fields={f:self.defaults[f].cpu().numpy()[None].repeat(self.nworld,0)
                for f in ('body_mass','body_inertia','dof_damping','dof_frictionloss','dof_armature','geom_friction')}
        for w,ep in enumerate(self.episode_ids):
            rr=stream(self.seed,self.structure.key,int(ep),'reset')
            dr=stream(self.seed,self.structure.key,int(ep),'dynamics')
            er=stream(self.seed,self.structure.key,int(ep),'excitation')
            branch=rr.random()
            eligible=[s for s in self.bank if s['level']<=level]
            if snapshots and branch>=.8 and eligible:
                snap=eligible[int(rr.integers(len(eligible)))]
                qpos[w],qvel[w]=snap['qpos'],snap['qvel']
                for name in fields: fields[name][w]=snap['fields'][name]
                for name in ('u','tau','cap','tm','delay','clock','ring','support','pulses','peripheral'):
                    arrays[name][w]=snap['state'][name]
                # Preserve active/planned pulses; refill expired slots beyond the last
                # retained event so repeated snapshot resets never exhaust excitation.
                now=float(arrays['clock'][w])*.001
                remaining=[p.copy() for p in arrays['pulses'][w] if p[0]+p[1]>now]
                time=max(now,max((p[0]+p[1] for p in remaining),default=now))+er.uniform(.5,2.)
                mass=fields['body_mass'][w,1:].sum()
                while len(remaining)<16:
                    duration=er.uniform(.1,.5); angle=er.uniform(0,2*np.pi)
                    magnitude=level*er.uniform(0,.5*mass*9.81)
                    remaining.append(np.array([time,duration,magnitude*np.cos(angle),magnitude*np.sin(angle),
                        level*er.uniform(-1.8,1.8),er.uniform(.2,.8),er.integers(2)],np.float32))
                    time+=duration+er.uniform(.5,2.)
                arrays['pulses'][w]=np.asarray(remaining)
                self.reset_stats['snapshot']+=1
                continue
            if snapshots and branch>=.8: self.reset_stats['snapshot_fallback']+=1
            wide=rr.random()<3/8 if branch>=.8 else branch>=.5
            self.reset_stats['wide' if wide else 'ordinary']+=1
            qpos[w],qvel[w]=self._initial(rr,wide)
            factors=1+level*dr.uniform(-.2,.2,self.model.nbody)
            factors[0]=1
            fields['body_mass'][w]*=factors
            fields['body_inertia'][w]*=factors[:,None]
            for name,lo,hi,nom in (('dof_damping',.01,.08,.03),('dof_frictionloss',0.,.08,.02),
                                   ('dof_armature',.001,.006,.003)):
                val=np.exp(dr.uniform(np.log(lo),np.log(hi))) if name=='dof_armature' else dr.uniform(lo,hi)
                fields[name][w,self.motor]=nom+level*(val-nom)
            mu=.8+level*(dr.uniform(.4,1)-.8)
            fields['geom_friction'][w,:,0]=mu
            arrays['cap'][w]=6*(1+level*dr.uniform(-.2,.2))
            arrays['tm'][w]=.01+level*(dr.uniform(.005,.020)-.01)
            arrays['delay'][w]=int(dr.integers(0,11)) if level else 0
            mass=fields['body_mass'][w,1:].sum()
            stiffness=np.array([dr.uniform(20,200),dr.uniform(100,500),dr.uniform(.1,5)])
            stiffness=np.array([110.,300.,2.55])+level*(stiffness-[110.,300.,2.55])
            inertia=sum(fields['body_inertia'][w,1:,1])+mass*(self.structure.lp+self.structure.ld)**2/3
            damping=2*dr.uniform(.3,1.,3)*np.sqrt(stiffness*np.array([mass,mass,inertia]))
            arrays['support'][w]=np.r_[stiffness,damping,mass*9.81]
            time=er.uniform(.5,2.)
            for event in range(16):
                duration=er.uniform(.1,.5)
                angle=er.uniform(0,2*np.pi)
                magnitude=level*er.uniform(0,.5*mass*9.81)
                arrays['pulses'][w,event]=[time,duration,magnitude*np.cos(angle),magnitude*np.sin(angle),
                    level*er.uniform(-1.8,1.8),er.uniform(.2,.8),er.integers(2)]
                time+=duration+er.uniform(.5,2.)
            for side in range(2):
                arrays['peripheral'][w,side]=[er.uniform(.1,.7),er.uniform(.3,2.)*2*np.pi,er.uniform(0,2*np.pi)]
        for name,array in fields.items():
            getattr(self.sim.model,name).copy_(torch.as_tensor(array,device=self.device))
        self.sim.recompute_constants(RecomputeLevel.set_const)
        self.sim.data.qpos.copy_(torch.as_tensor(qpos,device=self.device))
        self.sim.data.qvel.copy_(torch.as_tensor(qvel,device=self.device))
        for name,array in arrays.items():
            self.tensors[name].copy_(torch.as_tensor(array,device=self.device,dtype=self.tensors[name].dtype))
        self.sim.forward()
        self._launch(k.observe,[self.s,self.p,self.d,self.motor])
        self.history.reset(self.tensors['obs'])
        return self.history.input(self.m)

    def capture_snapshots(self,ids=range(4),max_size=128):
        fields={f:getattr(self.sim.model,f).cpu().numpy() for f in
                ('body_mass','body_inertia','dof_damping','dof_frictionloss','dof_armature','geom_friction')}
        state={f:self.tensors[f].cpu().numpy() for f in
               ('u','tau','cap','tm','delay','clock','ring','support','pulses','peripheral')}
        qp=self.sim.data.qpos.cpu().numpy(); qv=self.sim.data.qvel.cpu().numpy()
        for i in ids:
            self.bank.append(dict(level=self.level,qpos=qp[i].copy(),qvel=qv[i].copy(),
                fields={f:a[i].copy() for f,a in fields.items()},state={f:a[i].copy() for f,a in state.items()}))
        self.bank=self.bank[-max_size:]

    def cpu_copy(self,world=0):
        model=self.structure.compile()
        for name in ('body_mass','body_inertia','dof_damping','dof_frictionloss','dof_armature','geom_friction'):
            getattr(model,name)[:]=getattr(self.sim.model,name)[world].cpu().numpy()
        data=mujoco.MjData(model); mujoco.mj_setConst(model,data)
        data.qpos[:]=self.sim.data.qpos[world].cpu().numpy()
        data.qvel[:]=self.sim.data.qvel[world].cpu().numpy()
        mujoco.mj_forward(model,data)
        return model,data
