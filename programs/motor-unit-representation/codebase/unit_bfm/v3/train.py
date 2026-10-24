"""V3 executable CPU smoke / formal training, isolated runs and resumable episodes.

python -m unit_bfm.v3.train --mode smoke --run-dir unit_bfm/v3/runs/my-smoke
Checkpoints are taken at episode boundaries; no half environment state is omitted.
"""
from __future__ import annotations
import argparse
import copy
from dataclasses import asdict, replace
import json
import os
from pathlib import Path
import random
import time
import numpy as np
import torch
from . import VERSION
from .replay import Replay, SCENES, fingerprint, plain
from .programs import TimeDeficitScheduler
from .coverage import Coverage
from .collect import collect_episode, independent_seed, matching_goal_provider, make_environment

V3_ROOT=Path(__file__).resolve().parent

def load_config(path):
    c=json.loads(Path(path).read_text(encoding='utf8'))
    if c.get('version')!=VERSION or c.get('config_version')!='v3-pipeline-1': raise ValueError('V3 config version required')
    for key in ('physics','collection','learning','replay','coverage','evaluation','budget','seed','mode','run_root'):
        if key not in c: raise ValueError(f'missing config {key}')
    if c['physics']['dt']!=.001 or c['physics']['control_dt']!=.01: raise ValueError('requires 1kHz/100Hz')
    if c['learning']['batch_size']<2 or c['learning']['updates_per_W']<=0: raise ValueError('learning schedule')
    if c['collection']['source_weights']!={'rule':.5,'policy':.5}: raise ValueError('rule/policy time mixture is 50/50')
    return c

def safe_run_directory(path,root=None):
    # Runs are constrained under this isolated V3 tree, with no symlink escape.
    root=(V3_ROOT/'runs') if root is None else Path(root).resolve()
    if not root.is_relative_to(V3_ROOT) or root==V3_ROOT: raise ValueError('run root must be isolated under v3')
    path=Path(path).resolve()
    if not path.is_relative_to(root) or path==root: raise ValueError('run directory must be beneath configured V3 runs root')
    if any(x.lower() in ('v2','artifacts','weights','configs','tests') for x in path.relative_to(root).parts): raise ValueError('reserved/legacy output path')
    path.mkdir(parents=True,exist_ok=False)
    return path

def schema_manifest(env):
    from .schema import registry, SCHEMA_HASH, ESTIMATOR_VERSION, MEMORY_DIM
    return {'version':VERSION,'core_hash':SCHEMA_HASH,'estimator':ESTIMATOR_VERSION,
            'core':registry(),'physics':plain(env.physics_schema),'physics_dim':env.p_dim,
            'memory_dim':MEMORY_DIM,'p_dim':env.p_dim+MEMORY_DIM}


def capture_rng():
    return {'python':random.getstate(),'numpy':np.random.get_state(),'torch_cpu':torch.get_rng_state(),
            'torch_cuda':torch.cuda.get_rng_state_all() if torch.cuda.is_initialized() else []}

def restore_rng(s):
    random.setstate(s['python']); np.random.set_state(s['numpy']); torch.set_rng_state(s['torch_cpu'])
    if s['torch_cuda']:
        if not torch.cuda.is_available(): raise ValueError('CUDA RNG checkpoint requires matching CUDA runtime')
        torch.cuda.set_rng_state_all(s['torch_cuda'])


def save_checkpoint(path,learner,replay,coverage,schedulers,state,config,schema):
    path=Path(path)
    if path.exists(): raise FileExistsError(path)
    checkpoint={'version':VERSION,'checkpoint_version':'v3-complete-2-active-scene-config','config':config,'config_hash':fingerprint(config),
        'schema':schema,'schema_hash':fingerprint(schema),'learner':learner.state_dict(),'replay':replay.state_dict(),
        'coverage':coverage.state_dict(),'schedulers':{k:v.state_dict() for k,v in schedulers.items()},
        'state':copy.deepcopy(state),'rng':capture_rng(),'boundary_checkpoint':True,
        'lr_scheduler':{'kind':'constant','learning_rate':config['learning']['lr']}}
    tmp=path.with_suffix(path.suffix+'.tmp'); torch.save(checkpoint,tmp); os.replace(tmp,path)
    return path


def read_checkpoint(path,config):
    s=torch.load(path,map_location='cpu',weights_only=False)
    if s.get('version')!=VERSION or s.get('checkpoint_version')!='v3-complete-2-active-scene-config' or s.get('boundary_checkpoint') is not True: raise ValueError('complete V3 checkpoint required')
    if fingerprint(config)!=s['config_hash'] or fingerprint(s['config'])!=s['config_hash']: raise ValueError('resume config changed')
    if fingerprint(s['schema'])!=s['schema_hash']: raise ValueError('checkpoint schema corrupted')
    return s


def _scene(config,structure,scene,episode_index):
    from .physics import make_scene
    base_seed=config['seed']; geometry=structure['geometry_id']; limit=structure['limit_id']
    # Stable geometry/limits across episodes; dynamics use independently keyed streams.
    seed=independent_seed(base_seed,geometry,limit,scene,episode_index,'dynamics')
    assignment=np.random.default_rng(independent_seed(base_seed,geometry,limit,scene,episode_index,'assignment'))
    fixed=str(assignment.choice(['P','D']))
    nominal=float(assignment.choice(config['collection']['capacity_nominal']))
    canonical=make_scene(seed=base_seed,scene=scene,geometry_id=geometry,limit_id=limit)
    c=make_scene(seed=seed,scene=scene,fixed_side=fixed,geometry_id=geometry,limit_id=limit,capacity_nominal=nominal,geometry_seed=base_seed,episode_id=episode_index,
                 duration=config['physics']['episode_s'],lengths=canonical.lengths)
    overrides=copy.deepcopy(config['physics'].get('overrides',{}))
    for k in ('lengths','masses','support_k','neighbour_lengths','neighbour_masses'):
        if k in overrides: overrides[k]=tuple(overrides[k])
    assignment_overrides={'tilt':float(assignment.integers(8)*np.pi/4),'encoder_sign':int(assignment.choice([-1,1])),
                         'load_side':str(assignment.choice(['P','D'])),'load_frame':str(assignment.choice(['world','body'])),
                         'load_start':float(assignment.uniform(.2,2.))}
    assignment_overrides['load_end']=assignment_overrides['load_start']+float(assignment.uniform(1.,3.))
    if config['mode']=='full': overrides={**assignment_overrides,**overrides}
    return replace(c,**overrides)


def collection_schedulers(scene_weights,config_ids):
    result={'source':TimeDeficitScheduler({'rule':.5,'policy':.5}),
            'reset':TimeDeficitScheduler({'xi':.5,'velocity':.3,'snapshot':.2}),
            'scene':TimeDeficitScheduler(scene_weights)}
    for scene in scene_weights:result['config_'+scene]=TimeDeficitScheduler({cid:1/len(config_ids) for cid in config_ids})
    return result


def choose_collection_group(schedulers,snapshot_pool=(),use_snapshot=False):
    """Choose a new group normally, or the most owed compatible cached group.

    Snapshot entries carry their exact model/process configuration; callers create
    that config and restore through the physics hash-checking public API.
    """
    scene=schedulers['scene'].choose();cid=schedulers['config_'+scene].choose()
    if use_snapshot:
        available=[e for e in snapshot_pool if e['scene'] in schedulers['scene'].weights
                   and e['config_id'] in schedulers['config_'+e['scene']].weights]
        def debt(entry):
            sc=entry['scene'];key=entry['config_id'];ss=schedulers['scene'];cs=schedulers['config_'+sc]
            return (ss.weights[sc]*(sum(ss.steps.values())+1)-ss.steps[sc],
                    cs.weights[key]*(sum(cs.steps.values())+1)-cs.steps[key])
        if available:
            chosen=max(available,key=debt)
            return chosen['scene'],chosen['config_id'],chosen
    return scene,cid,None


def record_collection_group(schedulers,scene,cid,steps):
    schedulers['scene'].record(scene,steps);schedulers['config_'+scene].record(cid,steps)


class CheckpointRetention:
    """Only manages paths created by this run; never scans/deletes historical runs."""
    def __init__(self,keep_p0=False):self.keep_p0=keep_p0;self.managed=[];self.extra_p0=None
    def record(self,path,kind='rolling'):
        path=Path(path)
        if kind=='p0' and self.keep_p0:self.extra_p0=path;return
        self.managed.append(path)
        while len(self.managed)>2:self.managed.pop(0).unlink()
    def manifest(self):
        return {'managed_limit':2,'p0_retained_extra':self.keep_p0,'final_counts_toward_limit':True,
                'files':[str(p) for p in self.managed]+([str(self.extra_p0)] if self.extra_p0 else [])}


def run(config,run_dir,device='cpu',resume=None):
    from .learner import Learner
    from .collect import make_batch,collect_batch
    from .replay import EmptyReplayGroup
    torch.set_num_threads(config.get('cpu_threads',1))
    run_dir=safe_run_directory(run_dir,V3_ROOT/config['run_root'])
    (run_dir/'config.json').write_text(json.dumps(config,indent=2))
    (run_dir/'evaluation_spec.json').write_text(json.dumps(config['evaluation'],indent=2))
    structures=config['collection']['structures'];scenes=config['collection']['scene_weights'];nworld=config['collection'].get('num_worlds',2)
    backend=config['physics'].get('backend','cpu');physics_device=config['physics'].get('device','cuda:0')
    first=make_environment(_scene(config,structures[0],next(iter(scenes)),0),seed=config['seed'])
    try:schema=schema_manifest(first)
    finally:first.close()
    replay=Replay(seed=config['seed']+17,scene_weights=scenes,expected_configs={s:[a['config_id'] for a in structures] for s in scenes},
                  rule_capacity=config['replay'].get('rule_capacity',32768),policy_capacity=config['replay'].get('policy_capacity',65536),
                  p_dim=schema['p_dim'] if not resume else None,strict=False,p0_fraction=config['replay'].get('p0_fraction',.5))
    rollout_upper=nworld*(round(config['physics']['episode_s']/.01)+1)*(24*schema['p_dim']+8192)
    if rollout_upper>config['collection'].get('rollout_memory_limit_bytes',512*1024**2):raise MemoryError('multiworld episode temporary budget exceeded; reduce num_worlds/horizon')
    learner=Learner(schema['p_dim'],device=device,seed=config['seed'],config={k:config['learning'][k] for k in ('lr','polyak','action_std','action_clip')})
    coverage=Coverage(config['coverage']);schedulers=collection_schedulers(scenes,[a['config_id'] for a in structures])
    state={'W':0,'physical_steps':0,'invalid_W':0,'online_W':0,'p0_W':0,'credit':0.,'episodes':0,'p0_done':False,
           'stage':'p0','last_checkpoint_W':0,'last_coverage_W':0,'last_metrics':None,'elapsed_s':0.,'failure_examples':[],
           'config_visits':{},'snapshot_pool':[],'reset_requested':{},'snapshot_fallbacks':0,'reset_counts':{},'behaviour_time':{'rule':None,'policy':None},'batch_count':0,'reset_rejections':[]}
    if resume:
        old=read_checkpoint(resume,config)
        if old['schema_hash']!=fingerprint(schema):raise ValueError('physics schema changed')
        learner.load_state_dict(old['learner']);replay.load_state_dict(old['replay']);coverage.load_state_dict(old['coverage']);state=old['state']
        for k,v in schedulers.items():v.load_state_dict(old['schedulers'][k])
        restore_rng(old['rng'])
    else:random.seed(config['seed']);np.random.seed(config['seed']);torch.manual_seed(config['seed'])
    (run_dir/'schema.json').write_text(json.dumps(schema,indent=2))
    (run_dir/'storage_manifest.json').write_text(json.dumps({**replay.memory_report(),'rollout_upper_bytes':rollout_upper},indent=2))
    start=time.monotonic();retention=CheckpointRetention(config['budget'].get('keep_p0_checkpoint',config['mode']!='full'))
    def checkpoint(name):
        path=save_checkpoint(run_dir/(name+'.pt'),learner,replay,coverage,schedulers,state,config,schema)
        retention.record(path,'p0' if name=='p0' else 'rolling')
        (run_dir/'checkpoint_retention.json').write_text(json.dumps(retention.manifest(),indent=2))
        return path
    while state['W']<config['budget']['total_W']:
        reset_mode=schedulers['reset'].choose()
        snapshot_supported=backend=='cpu' or callable(getattr(__import__('unit_bfm.v3.warp_backend',fromlist=['WarpBatchEnv']).WarpBatchEnv,'restore',None))
        scene,cid,restore_entry=choose_collection_group(schedulers,state['snapshot_pool'],reset_mode=='snapshot' and snapshot_supported)
        structure=next(a for a in structures if a['config_id']==cid)
        batch=None
        state['reset_requested'][reset_mode]=state['reset_requested'].get(reset_mode,0)+1
        if reset_mode=='snapshot' and restore_entry is None:state['snapshot_fallbacks']+=1
        actual_reset=reset_mode if reset_mode!='snapshot' or restore_entry else 'xi'
        for attempt in range(config['collection'].get('max_reset_attempts',8)):
            c=restore_entry['config'] if restore_entry else _scene(config,structure,scene,state['batch_count']*31+attempt)
            if not restore_entry:
                from .physics import make_scene
                visit=state['config_visits'].get(scene+':'+cid,0)
                # Explicit balanced variant blocks are local to each structural group.
                stable=make_scene(seed=c.seed,scene=scene,fixed_side=c.fixed_side,geometry_id=c.geometry_id,limit_id=c.limit_id,geometry_seed=config['seed'],
                                  episode_id=state['batch_count']*31+attempt,variant_id=visit,capacity_nominal=c.capacity_nominal,duration=c.duration,
                                  **config['physics'].get('overrides',{}))
                c=stable
            if not restore_entry:c=replace(c,reset_mode=actual_reset if config['mode']!='smoke' else 'configured')
            try:
                batch=make_batch([c]*nworld,seed=config['seed']+state['batch_count'],backend=backend,device=physics_device)
                break
            except ValueError as exc:
                if 'initial' not in str(exc) and 'assembly' not in str(exc):raise
                state['reset_rejections'].append({'batch':state['batch_count'],'attempt':attempt,'seed':c.seed,'error':str(exc)})
                state['reset_rejections']=state['reset_rejections'][-32:]
        if batch is None:
            checkpoint('failed_reset_boundary');raise RuntimeError('bounded legal assembly resampling exhausted')
        p0=state['p0_W']<config['budget']['p0_min_W'];sources=[];projected=dict(schedulers['source'].steps)
        for i in range(nworld):
            source='rule' if p0 else min(projected,key=projected.get)
            sources.append(source);projected[source]+=round(c.duration/.01)
        observed=[r for r in coverage.records if r['scene']==scene and r['config_id']==cid]
        visits={b:sum(r['xi_steps'][str(b)] for r in observed) for b in range(10)}
        target_xi=(min(visits,key=visits.get)+.5)/10
        was_warm=state['online_W']>=config['learning']['online_warmup_W']
        try:
            episodes=collect_batch(batch,[f'{sources[i]}_{state["episodes"]+i:09d}' for i in range(nworld)],sources,
                [independent_seed(config['seed'],c.geometry_id,c.limit_id,scene,state['episodes']+i,'behaviour') for i in range(nworld)],
                learner=learner,goal_provider=matching_goal_provider(replay),gamma=config['learning']['gamma'],max_steps=round(c.duration/.01),
                metadata=[{'scene':scene,'config_id':cid,'fixed_side':c.fixed_side,'geometry_family':structure.get('geometry_family','straight_planar'),
                           'target_xi':target_xi if config['collection'].get('directed_coverage',False) else None,
                           'cross_tags':{'fixed_side':c.fixed_side,'capacity':c.capacity_nominal,'encoder_sign':c.encoder_sign,
                                         'installation_sector':int(round(c.tilt/(np.pi/4)))%8,'load_side':c.load_side}} for _ in sources],
                behaviour_times=[state['behaviour_time'][s] for s in sources],
                reset_snapshots=[restore_entry['snapshot']]*nworld if restore_entry else None)
        finally:batch.close()
        diagnostics=episodes.collection_diagnostics
        state['invalid_W']+=diagnostics['failed_world_count']+diagnostics['unattributed_failures']
        state['aborted_valid_W']=state.get('aborted_valid_W',0)+diagnostics['aborted_valid_world_count']
        state['physical_steps']+=diagnostics['attempted_world_intervals']
        state['episodes']+=nworld
        examples=state.setdefault('failure_examples',[])
        examples.extend(diagnostics['failure_examples'][:max(0,8-len(examples))])
        added=0
        time_before=copy.deepcopy(state['behaviour_time'])
        for ep in episodes:
            replay.add(ep,p0=p0);coverage.add(ep)
            if ep.metadata.get('snapshot') is not None:
                state['snapshot_pool'].append({'scene':scene,'config_id':cid,'config':c,'snapshot':ep.metadata['snapshot']})
                state['snapshot_pool']=state['snapshot_pool'][-8:]
            count=int(ep.valid.sum());added+=count;state['W']+=count;state['invalid_W']+=len(ep)-count
            after=ep.metadata['behaviour_time'];before=time_before[ep.source]
            if state['behaviour_time'][ep.source] is None:state['behaviour_time'][ep.source]={'weights':after['weights'],'steps':{k:0 for k in after['steps']}}
            for key,value in after['steps'].items():state['behaviour_time'][ep.source]['steps'][key]+=value-(before['steps'][key] if before else 0)
            if p0:state['p0_W']+=count
            elif ep.source=='policy':state['online_W']+=count
            if not p0:schedulers['source'].record(ep.source,count)
        state['config_visits'][scene+':'+cid]=state['config_visits'].get(scene+':'+cid,0)+1
        schedulers['reset'].record(actual_reset,1);state['reset_counts'][actual_reset]=state['reset_counts'].get(actual_reset,0)+1
        record_collection_group(schedulers,scene,cid,added);state['batch_count']+=1
        if not state['p0_done'] and state['p0_W']>=config['budget']['p0_min_W']:
            state['p0_done']=True;state['stage']='online_warmup';checkpoint('p0')
        if was_warm and not p0:state['credit']+=added*config['learning']['updates_per_W']
        if replay.counts['rule'] and replay.counts['policy'] and state['credit']>=1:
            state['stage']='training'
            while state['credit']>=1:
                metrics=learner.update(replay.sample(config['learning']['batch_size'],device=device))
                if not all(np.isfinite(v) for v in metrics.values()):raise FloatingPointError('nonfinite learner diagnostics')
                state['last_metrics']=metrics;state['credit']-=1
                with (run_dir/'metrics.jsonl').open('a') as f:f.write(json.dumps({'W':state['W'],**metrics})+'\n')
        if added==0:
            state['empty_buckets']=state.get('empty_buckets',0)+1
            if state['empty_buckets']>=8:
                checkpoint('no_valid_boundary');raise RuntimeError('8 consecutive buckets without valid transitions')
        else:state['empty_buckets']=0
        if state['W']-state['last_coverage_W']>=config['budget']['coverage_interval_W']:
            coverage.write(run_dir/f'coverage_{state["W"]}.json',dict(replay.audit),formal=False);state['last_coverage_W']=state['W']
        if state['W']-state['last_checkpoint_W']>=config['budget']['checkpoint_interval_W']:
            state['last_checkpoint_W']=state['W'];checkpoint(f'checkpoint_{state["W"]}')
    state['elapsed_s']+=time.monotonic()-start
    report=coverage.write(run_dir/'coverage.json',dict(replay.audit),formal=False);final=checkpoint('final')
    from .queries import QueryPool
    from .interface import export_actor_b
    pool=QueryPool.from_replay(replay,config['evaluation']['reference_samples']);pool.save(run_dir/'query_pool.npz')
    export_actor_b(learner,run_dir/'export',schema,{'pool_version':pool.version,'rho':pool.rho,'evaluation_hash':fingerprint(config['evaluation'])})
    result={'version':VERSION,'mode':config['mode'],'W':state['W'],'p0_W':state['p0_W'],'online_W':state['online_W'],
            'invalid_W':state['invalid_W'],'aborted_valid_W':state.get('aborted_valid_W',0),'physical_steps':state['physical_steps'],'updates':learner.updates,'elapsed_s':state['elapsed_s'],'checkpoint':str(final),
            'coverage_ready':report['coverage_ready'],'validated':False,'status':'training_budget_complete',
            'gradient_usage':dict(replay.audit),'replay':replay.memory_report(),'distribution':replay.distribution(),
            'reset_counts':state['reset_counts'],'reset_requested':state['reset_requested'],'snapshot_fallbacks':state['snapshot_fallbacks'],'backend':backend,'num_worlds':nworld,'last_metrics':state['last_metrics']}
    (run_dir/'result.json').write_text(json.dumps(plain(result),indent=2));return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('smoke','dev','full'),default='smoke'); parser.add_argument('--config',type=Path)
    parser.add_argument('--run-dir',type=Path,required=True); parser.add_argument('--device',default='cpu'); parser.add_argument('--resume',type=Path)
    args=parser.parse_args(argv)
    config=load_config(args.config or V3_ROOT/'configs'/(args.mode+'.json'))
    if config['mode']!=args.mode: parser.error('mode/config mismatch')
    print(json.dumps(run(config,args.run_dir,args.device,args.resume),indent=2))

if __name__=='__main__': main()
