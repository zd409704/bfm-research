"""Complete-episode collection with raw interval integrals and paired F memory."""
from __future__ import annotations
import copy
import numpy as np
import torch
from .replay import Episode, fingerprint, plain
from .programs import RuleProgram, CallScheduler


def independent_seed(run_seed,geometry_id,limit_id,scene,episode_id,purpose):
    digest=fingerprint([run_seed,geometry_id,limit_id,scene,episode_id,purpose])
    return int(digest[:16],16)%(2**32)

def oracle_static_feedforward(env):
    """CPU behavior-only bias torque in canonical coordinates; never a feature."""
    if callable(getattr(env,'static_bias_torque',None)): return env.static_bias_torque
    if not all(hasattr(env,k) for k in ('model','data','vadr','tree_sign')): return None
    import mujoco
    probe=mujoco.MjData(env.model)
    def bias(boundary):
        probe.qpos[:]=env.data.qpos; probe.qvel[:]=0
        mujoco.mj_forward(env.model,probe)
        return float(env.tree_sign*probe.qfrc_bias[env.vadr])
    return bias

class PolicyBehaviour:
    def __init__(self,learner,seed=0,goal_provider=None,noise=.2,noise_clip=.3):
        # Snapshot both networks once per rollout. Calls re-encode current-snapshot B.
        self.actor=copy.deepcopy(learner.net.actor).eval().requires_grad_(False)
        self.b=copy.deepcopy(learner.net.b).eval().requires_grad_(False)
        self.device=next(self.actor.parameters()).device
        self.rng=np.random.default_rng(seed); self.calls=CallScheduler(seed)
        self.goal_provider=goal_provider; self.noise=noise; self.noise_clip=noise_clip; self.z=None
        self.goal_fallback=0
    def prepare_z(self,known):
        if self.calls.remaining<=0:
            self.calls.begin(); goal=None
            if self.rng.random()<.5 and self.goal_provider is not None: goal=self.goal_provider(known,self.rng)
            with torch.no_grad():
                if goal is None:
                    z=self.rng.normal(size=16); z=z/max(np.linalg.norm(z),1e-12)*4
                    self.z=torch.tensor(z,dtype=torch.float32,device=self.device)[None]; self.goal_fallback+=1
                else: self.z=self.b(torch.as_tensor(goal,dtype=torch.float32,device=self.device)[None]).detach()

    def action(self,features,known):
        self.prepare_z(known)
        with torch.no_grad():
            x=torch.as_tensor(features['x'],dtype=torch.float32,device=self.device)[None]
            u=float(self.actor(x,self.z).reshape(-1)[0].cpu())
        u=float(np.clip(u+np.clip(self.rng.normal(0,self.noise),-self.noise_clip,self.noise_clip),-1,1))
        info={'call_kind':self.calls.kind,'call_remaining':self.calls.remaining,'z':self.z.cpu().numpy().tolist()}
        self.calls.step(); return u,'policy',info


def collect_episode(env,episode_id,source='rule',seed=0,gamma=.99,learner=None,
                    goal_provider=None,max_steps=1000,metadata=None,behaviour_time=None,reset_snapshot=None):
    from .features import FeatureHistory
    if source not in ('rule','policy'): raise ValueError('source')
    if source=='policy' and learner is None: raise ValueError('policy requires learner')
    b=copy.deepcopy(restore_snapshot(env,reset_snapshot,episode_id) if reset_snapshot else env.reset(episode_id=episode_id)); known=copy.deepcopy(env.known)
    history=FeatureHistory(); history.reset(b,known)
    raw=[b]; knowns=[known]; fs=[history.features()]; actions=[]; phases=[]; discounts=[]; behaviour=[]
    controller=RuleProgram(known,seed,feedforward=oracle_static_feedforward(env),fixed_side=getattr(env.config,'fixed_side','P'),load_schedule=env.config) if source=='rule' else PolicyBehaviour(learner,seed,goal_provider)
    if behaviour_time is not None:
        (controller.schedule if source=='rule' else controller.calls.time).load_state_dict(behaviour_time)
    saved_snapshot=None
    for t in range(max_steps):
        if t==max(1,max_steps//4) and callable(getattr(env,'snapshot',None)) and b['valid']:saved_snapshot=capture_snapshot(env)
        if source=='rule': u,phase,info=controller.action(b,known)
        else: u,phase,info=controller.action(fs[-1],known)
        try:nxt=copy.deepcopy(env.step(u))
        except Exception as exc:
            if not hasattr(exc,'boundary'):raise
            if not actions:raise
            raw[-1]['truncated']=True;raw[-1]['diagnostics']['failed_next_interval']=plain(exc.diagnostics);break
        known=copy.deepcopy(env.known)
        required=('time','q','dq','tau_endpoint','u_previous','tau_integral','u_integral','interval_dt','interval_valid','p','terminated','truncated','valid','diagnostics')
        missing=[k for k in required if k not in nxt]
        if missing: raise ValueError(f'physics boundary missing {missing}')
        if float(nxt['time'])<=float(b['time']): raise ValueError('noncausal physics time')
        if not np.isclose(float(nxt['u_previous']),u,atol=1e-6): raise ValueError('physics action is not canonical requested u')
        history.append(nxt,known); fs.append(history.features()); raw.append(nxt); knowns.append(known)
        actions.append([u]); phases.append(phase); discounts.append([gamma*(1-bool(nxt['terminated']))]); behaviour.append(info)
        b=nxt
        if b['terminated'] or b['truncated']: break
    if not b['terminated'] and not b['truncated']:
        # Collector's explicit time limit is also a truncation, with the real final state.
        raw[-1]['truncated']=True; raw[-1]['diagnostics']['collector_time_limit']=True
    meta=copy.deepcopy(getattr(env,'metadata',{})); meta.update(metadata or {})
    meta.update({'reset_snapshot_used':reset_snapshot is not None,'snapshot':saved_snapshot,'behaviour':behaviour,'collection_seed':seed,'gamma':gamma,'max_steps':max_steps,
                 'behaviour_time':(controller.schedule if source=='rule' else controller.calls.time).state_dict(),
                 'physics_schema':plain(env.physics_schema),'program_version':RuleProgram.VERSION if source=='rule' else 'actor-b-snapshot-1'})
    scene=meta.get('scene',getattr(getattr(env,'config',None),'scene','E0'))
    config_id=str(meta.get('config_id',fingerprint({'lengths':knowns[0]['lengths'],'limits':knowns[0]['limits']})[:20]))
    p=np.asarray([np.concatenate([np.asarray(r['p']),f['memory']]) for r,f in zip(raw,fs)],dtype=np.float32)
    ep=Episode(str(episode_id),source,scene,config_id,np.asarray([f['x'] for f in fs],dtype=np.float32),
               np.asarray([f['g'] for f in fs],dtype=np.float32),p,np.asarray(actions,dtype=np.float32),
               np.asarray(discounts,dtype=np.float32),np.asarray(phases,dtype=str),raw,knowns,meta)
    ep.validate()
    return ep


def matching_goal_provider(replay,geometry_family='straight_planar'):
    def sample(known,rng):
        return replay.matching_goal(known,rng,geometry_family)
    return sample


class SingleWorldBackend:
    """Adapt the physics batch API to complete-episode collection, without fallback.

    One homogeneous world is intentional. This path enables backend correctness
    integration; it does not claim high-throughput asynchronous GPU collection.
    """
    def __init__(self,config,seed=0,backend='mujoco-warp',device='cuda:0'):
        from .warp_backend import WarpBatchEnv
        self.batch=WarpBatchEnv([config],seed=seed,device=device,backend=backend)
        self.config=config; self.physics_schema=self.batch.physics_schema; self.p_dim=self.batch.p_dim
    @property
    def metadata(self): return {**self.batch.envs[0].metadata,**self.batch.metadata}
    @property
    def known(self): return self.batch.known[0]
    def reset(self,episode_id=0): return self.batch.reset(episode_id=episode_id)[0]
    def step(self,u_c): return self.batch.step([u_c])[0]
    def close(self): self.batch.close()
    def static_bias_torque(self,boundary):
        if not hasattr(self,'_bias'): self._bias=oracle_static_feedforward(self.batch.envs[0])
        return self._bias(boundary)


def make_environment(config,seed=0,backend='cpu',device='cuda:0'):
    if backend=='cpu':
        from .physics import UnitEnv
        return UnitEnv(config,seed=seed)
    if backend in ('mujoco-warp','mjlab'): return SingleWorldBackend(config,seed,backend,device)
    raise ValueError('unknown physics backend; no automatic CPU fallback')

class CpuBatch:
    """Explicit CPU diagnostic batch; never substituted for requested GPU."""
    def __init__(self,configs,seed=0):
        from .physics import UnitEnv
        self.envs=[UnitEnv(c,seed+i) for i,c in enumerate(configs)]
        self.physics_schema=self.envs[0].physics_schema;self.p_dim=self.envs[0].p_dim
        self.metadata={'backend':'cpu','nworld':len(configs),'host_orchestration':True}
    @property
    def known(self):return [e.known for e in self.envs]
    def reset(self,episode_id=0):
        ids=episode_id if isinstance(episode_id,list) else [episode_id]*len(self.envs)
        return [e.reset(i) for e,i in zip(self.envs,ids)]
    def step(self,actions):
        from .physics import PhysicallyInvalidTransition
        out=[]
        for e,a in zip(self.envs,actions):
            try:out.append(e.step(float(a)))
            except PhysicallyInvalidTransition as exc:out.append(exc.boundary)
        return out
    def restore(self,snapshots,episode_id=0):return [e.restore(s,episode_id=i) for e,s,i in zip(self.envs,snapshots,episode_id)]
    def close(self):
        for e in self.envs:e.close()

def make_batch(configs,seed=0,backend='cpu',device='cuda:0'):
    if backend=='cpu':return CpuBatch(configs,seed)
    if backend not in ('mujoco-warp','mjlab'):raise ValueError('unknown physics backend')
    from .warp_backend import WarpBatchEnv
    return WarpBatchEnv(configs,seed=seed,device=device,backend=backend)


class CollectionResult(list):
    """List-compatible episode result with bounded, public interval-failure audit."""
    def __init__(self,episodes,diagnostics):
        super().__init__(episodes);self.collection_diagnostics=diagnostics


def collect_batch(batch,episode_ids,sources,seeds,gamma=.99,learner=None,goal_provider=None,
                  max_steps=1000,metadata=None,behaviour_times=None,reset_snapshots=None):
    """One vector physics step and one Actor forward for all policy worlds per tick.

    Homogeneous compiled-model bucket; independent history, RNG, z, calls, rules.
    Every world is retained on an invalid/early-ending peer; no silent world reset.
    """
    from .features import FeatureHistory
    n=len(episode_ids)
    if len(sources)!=n or len(seeds)!=n:raise ValueError('one source/seed/id per world')
    boundaries=batch.restore(reset_snapshots,episode_id=episode_ids) if reset_snapshots is not None else batch.reset(episode_id=episode_ids);known=batch.known
    histories=[FeatureHistory() for _ in range(n)];fs=[];controllers=[]
    actor=copy.deepcopy(learner.net.actor).eval().requires_grad_(False) if 'policy' in sources else None
    backward=copy.deepcopy(learner.net.b).eval().requires_grad_(False) if actor is not None else None
    device=next(actor.parameters()).device if actor is not None else 'cpu'
    for i in range(n):
        histories[i].reset(boundaries[i],known[i]);fs.append([histories[i].features()])
        if sources[i]=='rule':
            c=RuleProgram(known[i],seeds[i],feedforward=oracle_static_feedforward(batch.envs[i]),
                          fixed_side=batch.envs[i].config.fixed_side,load_schedule=batch.envs[i].config)
            if metadata and metadata[i].get('target_xi') is not None:c.target_xi=metadata[i]['target_xi']
        else:c=PolicyBehaviour(learner,seeds[i],goal_provider);c.actor=actor;c.b=backward
        if behaviour_times and behaviour_times[i] is not None:(c.schedule if sources[i]=='rule' else c.calls.time).load_state_dict(behaviour_times[i])
        controllers.append(c)
    raw=[[copy.deepcopy(b)] for b in boundaries];knowns=[[copy.deepcopy(k)] for k in known]
    actions=[[] for _ in range(n)];phases=[[] for _ in range(n)];infos=[[] for _ in range(n)]
    snapshots=[None]*n
    collection_diagnostics={'attempted_world_intervals':0,'failed_worlds':[],'aborted_valid_worlds':[],
                            'failed_world_count':0,'aborted_valid_world_count':0,'unattributed_failures':0,'failure_examples':[]}
    for step in range(max_steps):
        if step==max(1,max_steps//4):
            for i,e in enumerate(batch.envs):
                if callable(getattr(e,'snapshot',None)) and boundaries[i]['valid']:snapshots[i]=e.snapshot()
        u=np.zeros(n);tick_info=[None]*n;phase=['policy']*n;policy=[]
        for i,c in enumerate(controllers):
            if sources[i]=='rule':u[i],phase[i],tick_info[i]=c.action(boundaries[i],known[i])
            else:
                c.prepare_z(known[i]);policy.append(i)
        if policy:
            with torch.no_grad():
                x=torch.as_tensor(np.asarray([fs[i][-1]['x'] for i in policy]),dtype=torch.float32,device=device)
                z=torch.cat([controllers[i].z for i in policy]);means=actor(x,z).cpu().numpy().reshape(-1)
            for i,mean in zip(policy,means):
                c=controllers[i];u[i]=np.clip(mean+np.clip(c.rng.normal(0,c.noise),-c.noise_clip,c.noise_clip),-1,1)
                tick_info[i]={'z':c.z.cpu().numpy().tolist(),'call_kind':c.calls.kind,'call_remaining':c.calls.remaining}
                c.calls.step()
        collection_diagnostics['attempted_world_intervals']+=n
        failure=None
        try:boundaries=batch.step(u)
        except Exception as exc:
            if not hasattr(exc,'boundary'):raise
            failure=exc
        if failure is not None or any(not b['valid'] for b in boundaries):
            if failure is not None:
                wid=getattr(failure,'world_id',None)
                if wid is None:wid=failure.diagnostics.get('world_id')
                if wid is None and n==1:wid=0
                failed=[int(wid)] if wid is not None and 0<=int(wid)<n else []
                details={i:plain(failure.diagnostics) for i in failed}
                if not failed:collection_diagnostics['unattributed_failures']=1
            else:
                failed=[i for i,b in enumerate(boundaries) if not b['valid']]
                details={i:plain(boundaries[i]['diagnostics']) for i in failed}
            aborted=[i for i in range(n) if i not in failed]
            collection_diagnostics.update(failed_worlds=failed,aborted_valid_worlds=aborted,
                failed_world_count=len(failed),aborted_valid_world_count=len(aborted))
            collection_diagnostics['failure_examples']=[{'world_id':i,'control_step':step,'diagnostics':details[i]} for i in failed[:8]]
            if failure is not None and not failed:
                collection_diagnostics['failure_examples']=[{'world_id':None,'control_step':step,'diagnostics':plain(failure.diagnostics)}]
            for i in range(n):
                raw[i][-1]['truncated']=True
                if i in failed:raw[i][-1]['diagnostics']['failed_next_interval']=details[i]
                else:raw[i][-1]['diagnostics']['aborted_next_interval']=True
            break
        known=batch.known
        for i,b in enumerate(boundaries):
            histories[i].append(b,known[i]);fs[i].append(histories[i].features());raw[i].append(copy.deepcopy(b));knowns[i].append(copy.deepcopy(known[i]))
            actions[i].append([u[i]]);phases[i].append(phase[i]);infos[i].append(tick_info[i])
        if any(b['terminated'] or b['truncated'] or not b['valid'] for b in boundaries):break
    episodes=[]
    for i in range(n):
        if not raw[i][-1]['terminated']:raw[i][-1]['truncated']=True
        meta={**batch.envs[i].metadata,**(metadata[i] if metadata else {}),'backend':batch.metadata,
              'snapshot':snapshots[i],'reset_snapshot_used':reset_snapshots is not None,'behaviour':infos[i],'physics_schema':plain(batch.physics_schema),'collection_seed':seeds[i],
              'behaviour_time':(controllers[i].schedule if sources[i]=='rule' else controllers[i].calls.time).state_dict()}
        meta.setdefault('scene',batch.envs[i].config.scene);meta.setdefault('fixed_side',batch.envs[i].config.fixed_side)
        meta.setdefault('config_id',fingerprint({'lengths':knowns[i][0]['lengths'],'limits':knowns[i][0]['limits']})[:20])
        p=np.asarray([np.r_[b['p'],f['memory']] for b,f in zip(raw[i],fs[i])],dtype=np.float32)
        if not actions[i]:continue
        ep=Episode(str(episode_ids[i]),sources[i],meta['scene'],meta['config_id'],np.asarray([f['x'] for f in fs[i]]),
                   np.asarray([f['g'] for f in fs[i]]),p,np.asarray(actions[i]),
                   np.asarray([[gamma*(1-b['terminated'])] for b in raw[i][1:]]),np.asarray(phases[i]),raw[i],knowns[i],meta)
        episodes.append(ep.validate())
    return CollectionResult(episodes,collection_diagnostics)


def main(argv=None):
    import argparse,json
    from pathlib import Path
    from .train import load_config,safe_run_directory,_scene,schema_manifest
    from .learner import Learner
    from .replay import storage_report
    p=argparse.ArgumentParser(description='Complete compressed V3 episode batch collection')
    p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--episodes',type=int,default=2);p.add_argument('--backend',choices=['cpu','mujoco-warp','mjlab'],default='cpu');p.add_argument('--physics-device',default='cuda:0')
    a=p.parse_args(argv);cfg=load_config(a.config);root=safe_run_directory(a.output)
    c=_scene(cfg,cfg['collection']['structures'][0],next(iter(cfg['collection']['scene_weights'])),0)
    batch=make_batch([c]*a.episodes,seed=cfg['seed'],backend=a.backend,device=a.physics_device)
    try:
        learner=Learner(batch.p_dim+len(__import__('unit_bfm.v3.schema',fromlist=['MEMORY_SCHEMA']).MEMORY_SCHEMA))
        episodes=collect_batch(batch,[f'collect_{i}' for i in range(a.episodes)],['rule' if i%2==0 else 'policy' for i in range(a.episodes)],list(range(a.episodes)),learner=learner,max_steps=round(c.duration/.01))
        from .replay import Replay
        replay=Replay(rule_capacity=cfg['replay']['rule_capacity'],policy_capacity=cfg['replay']['policy_capacity'],scene_weights=cfg['collection']['scene_weights'])
        for ep in episodes:replay.add(ep)
        torch.save(replay.state_dict(),root/'replay.pt')
        result={**replay.memory_report(),'collected_W':sum(map(len,episodes)),'collection_diagnostics':episodes.collection_diagnostics,'backend':batch.metadata}
        (root/'manifest.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
    finally:batch.close()

if __name__=='__main__':main()


def capture_snapshot(env):
    if not callable(getattr(env,'snapshot',None)):raise ValueError('physics public snapshot API unavailable')
    return env.snapshot()


def restore_snapshot(env,snapshot,episode_id):
    if not callable(getattr(env,'restore',None)):raise ValueError('physics public restore API unavailable')
    return env.restore(snapshot,episode_id=episode_id)
