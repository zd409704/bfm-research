"""Real homogeneous-bucket mujoco-warp/mjlab batch backend.

The solver/integrator are batched on the requested CUDA device. Drives, loading,
and export are host-orchestrated at 1 kHz for correctness, so this is deliberately
not advertised as a high-throughput all-device rollout. There is no CPU fallback
when CUDA is requested. Different compiled physical parameters require buckets.
"""
import numpy as np
import os
import tempfile
from .physics import UnitEnv, PhysicallyInvalidTransition
from .privileged import MAX_CONTACTS
from .kernels import assign_batch,check_capacity


class WarpBatchEnv:
    def __init__(self,configs,seed=0,device='cuda:0',backend='mujoco-warp'):
        import warp as wp
        import mujoco_warp as mw
        # Respect a caller cache override; otherwise keep compilation in writable temp.
        wp.config.kernel_cache_dir=os.environ.get('WARP_CACHE_PATH',os.path.join(tempfile.gettempdir(),'unit_bfm_v3_warp'))
        if not configs: raise ValueError('nonempty homogeneous config bucket required')
        if backend not in ('mujoco-warp','mjlab'): raise ValueError('unknown solver backend')
        if str(device).startswith('cuda'):
            import torch
            if not torch.cuda.is_available():
                raise RuntimeError('CUDA inaccessible in this process; GPU physics not validated; no CPU substitution')
        self.wp,self.mw,self.device=wp,mw,device
        self.envs=[UnitEnv(c,seed+i) for i,c in enumerate(configs)]
        if len({e.metadata['xml_sha256'] for e in self.envs})!=1:
            raise ValueError('different compiled constants/shapes must use separate buckets; no implicit broadcast')
        self.nworld=len(self.envs);self.model=self.envs[0].model
        self.p_dim=self.envs[0].p_dim;self.physics_schema=self.envs[0].physics_schema
        self.backend=backend;self.sim=None
        with wp.ScopedDevice(device):
            if backend=='mjlab':
                from mjlab.sim.sim import Simulation,SimulationCfg,MujocoCfg
                cfg=SimulationCfg(nconmax=MAX_CONTACTS,njmax=1024,mujoco=MujocoCfg(timestep=.001,integrator='euler',iterations=80,tolerance=1e-10,disableflags=('filterparent',)))
                self.sim=Simulation(self.nworld,cfg,model=self.model,device=device)
                self.wp_model,self.wp_data=self.sim.wp_model,self.sim.wp_data
            else:
                self.wp_model=mw.put_model(self.model)
                self.wp_data=mw.put_data(self.model,self.envs[0].data,nworld=self.nworld,nconmax=MAX_CONTACTS,njmax=1024)
        self.metadata={'backend':backend,'device':device,'nworld':self.nworld,
                       'host_drive_and_export':True,'optimized_postintegration_pull':'batched kinematics only; same-solve force pull retained','gpu_pair_validation':'required; see test_physics_backend',
                       'bucket_hash':self.envs[0].metadata['xml_sha256']}
        self.reset()

    @property
    def known(self):return [e.known for e in self.envs]

    def _push_state(self):
        for name in ('qpos','qvel','qacc_warmstart','qfrc_applied','xfrc_applied'):
            assign_batch(getattr(self.wp_data,name),np.stack([getattr(e.data,name) for e in self.envs]))
        assign_batch(self.wp_data.time,np.array([e.process_time for e in self.envs]))

    def _pull(self):
        for w,e in enumerate(self.envs):
            self.mw.get_data_into(e.data,e.model,self.wp_data,w)
            e.data.time=e.process_time

    def _pull_kinematics(self):
        # Only arrays needed by next millisecond force evaluation/current boundary.
        # Each field transfers once per batch, rather than get_data_into per world.
        names=('qpos','qvel','qacc_warmstart','xpos','xmat','xipos','ximat','xanchor',
               'xaxis','subtree_com','cvel','geom_xpos','geom_xmat')
        host={name:getattr(self.wp_data,name).numpy() for name in names}
        for w,e in enumerate(self.envs):
            e.data.time=e.process_time
            for name,values in host.items():
                target=getattr(e.data,name);target[:]=values[w].reshape(target.shape)

    def snapshot(self):return [e.snapshot() for e in self.envs]

    def restore(self,snapshots,episode_id=0):
        if len(snapshots)!=self.nworld:raise ValueError('one compatible snapshot per world required')
        result=[e.restore(s,episode_id if not isinstance(episode_id,(tuple,list)) else episode_id[w]) for w,(e,s) in enumerate(zip(self.envs,snapshots))]
        self._push_state()
        return result

    def reset(self,episode_id=0):
        for w,e in enumerate(self.envs):e.reset(episode_id if not isinstance(episode_id,(tuple,list)) else episode_id[w])
        self._push_state()
        with self.wp.ScopedDevice(self.device):self.mw.forward(self.wp_model,self.wp_data)
        self._pull()
        return [e._boundary(False) for e in self.envs]

    def step(self,u_c):
        u=np.asarray(u_c,dtype=float).reshape(-1)
        if u.shape!=(self.nworld,) or not np.isfinite(u).all() or np.any(abs(u)>1):raise ValueError('one finite canonical [-1,1] action per world')
        if any(e._ended for e in self.envs):raise RuntimeError('explicit whole-bucket reset required after end')
        integrals=np.zeros(self.nworld)
        for e in self.envs:e._interval_checks=[]
        for _ in range(10):
            # Device float time is a projection, never the event clock.
            assign_batch(self.wp_data.time,np.array([e.process_time for e in self.envs]))
            loads=[e._forces(float(a)) for e,a in zip(self.envs,u)]
            for name in ('qfrc_applied','xfrc_applied'):
                assign_batch(getattr(self.wp_data,name),np.stack([getattr(e.data,name) for e in self.envs]))
            with self.wp.ScopedDevice(self.device):
                self.mw.forward(self.wp_model,self.wp_data)
                self.mw.rne_postconstraint(self.wp_model,self.wp_data)
                n=check_capacity(self.wp_data,MAX_CONTACTS)
                ids=self.wp.array(np.arange(n,dtype=np.int32),dtype=self.wp.int32,device=self.device)
                force=self.wp.zeros(n,dtype=self.wp.spatial_vector,device=self.device)
                if n:self.mw.contact_force(self.wp_model,self.wp_data,ids,False,force)
                raw=force.numpy();worlds=self.wp_data.contact.worldid.numpy()[:n]
                self._pull()
                for w,e in enumerate(self.envs):
                    e._device_contact_forces=raw[worlds==w]
                    e._solve=e._snapshot_solve(*loads[w]);integrals[w]+=e.drives[0].tau*.001
                    check=e._validate_solve();e._interval_checks.append(check)
                    if not check['solver_valid']:
                        check['world_id']=w
                        for other in self.envs:other._ended=True
                        e._fail(check)
                    del e._device_contact_forces
                self.mw.euler(self.wp_model,self.wp_data)
                for e in self.envs:e._advance_tick()
                self.mw.kinematics(self.wp_model,self.wp_data);self.mw.com_pos(self.wp_model,self.wp_data);self.mw.com_vel(self.wp_model,self.wp_data)
                self._pull_kinematics()
        boundaries=[]
        for w,e in enumerate(self.envs):
            e._tau_integral=float(integrals[w]);e._u_integral=float(u[w]*.01);e._last_u=float(u[w]);e.step_count+=1
            b=e._boundary(True)
            if not b['valid']:e._fail(b['diagnostics'])
            e._ended=b['terminated'] or b['truncated'];boundaries.append(b)
        return boundaries

    def close(self):
        for e in self.envs:e.close()


class MjlabBatchEnv(WarpBatchEnv):
    def __init__(self,configs,seed=0,device='cuda:0'):
        super().__init__(configs,seed,device,backend='mjlab')
