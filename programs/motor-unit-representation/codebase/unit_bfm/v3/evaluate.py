"""Locked, reward-free-training evaluation of a paired frozen Actor/B export."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import time
import numpy as np
from . import VERSION
from .queries import Query, QueryPool
from .interface import Interface
from .replay import plain, fingerprint
from .coverage import longest_duration

def metrics(records,query,spec):
    total_records=len(records)
    failed=any(not r.get('valid',False) for r in records)
    # A failed substep has no complete 100 Hz response or valid estimator output.
    records=[r for r in records if r.get('valid',False)]
    if not records:
        return {'rmse':None,'max_abs_error':None,'visited':False,'first_arrival_s':None,
                'longest_hold_s':0.,'success':False,'valid_fraction':0.,'overshoot':None,
                'numerical_failure':failed}
    q=np.asarray([r['q'] for r in records]); dq=np.asarray([r['dq'] for r in records]); tau=np.asarray([r['tau_endpoint'] for r in records]); dt=np.asarray([r['interval_dt'] for r in records])
    kind=query.kind; limits=spec['thresholds']
    value={'q':q,'dq':dq,'tau':tau}.get(kind)
    if value is None:
        if kind=='compliance': value=tau-(query.bias+query.stiffness*(query.q_ref-q)-query.damping*dq)
        else: value=np.asarray([r['feedback']['physical'][{'ddq':'ddq_hat','tip_ax':'tip_ax','tip_az':'tip_az','tip_vx':'tip_vx','tip_vz':'tip_vz'}[kind]] for r in records])
    target=0. if kind=='compliance' else query.target; error=value-target
    tolerance=limits[kind]; valid=np.asarray([r.get('valid',False) for r in records])
    if kind in ('ddq','tip_ax','tip_az'): valid &= np.asarray([r['feedback']['acc_valid'] for r in records])
    ok=(np.abs(error)<=tolerance)&valid
    if kind=='q': ok &= np.abs(dq)<=limits['hold_dq']
    indices=np.flatnonzero(ok); hold=longest_duration(ok,dt)
    return {'rmse':float(np.sqrt(np.mean(error**2))),'max_abs_error':float(np.abs(error).max()),
            'visited':bool(len(indices)),'first_arrival_s':float(np.sum(dt[:indices[0]+1])) if len(indices) else None,
            'longest_hold_s':hold,'success':bool(not failed and hold>=limits['hold_duration_s']),
            'numerical_failure':failed,
            'valid_fraction':float(valid.sum()/max(1,total_records)),'overshoot':float(max(0,np.max(value)-target))}

def finite_json(value):
    """Keep failed diagnostics serializable; JSON null explicitly means nonfinite."""
    value=plain(value)
    if isinstance(value,dict):return {k:finite_json(v) for k,v in value.items()}
    if isinstance(value,list):return [finite_json(v) for v in value]
    if isinstance(value,float) and not np.isfinite(value):return None
    return value

def evaluate(export_path,pool_path,spec,output,seed=8001):
    from .physics import UnitEnv,make_scene
    from .train import safe_run_directory
    output=safe_run_directory(output)
    runtime=Interface(export_path); pool=QueryPool.load(pool_path)
    locked=runtime.manifest.get('query_manifest') or {}
    if locked.get('evaluation_hash')!=fingerprint(spec): raise ValueError('evaluation thresholds/distribution not frozen with model')
    if locked.get('pool_version')!=pool.version: raise ValueError('reference pool is not the frozen model rho')
    (output/'spec.json').write_text(json.dumps(spec,indent=2),encoding='utf8')
    results=[]; rng=np.random.default_rng(seed)
    for case_index,case in enumerate(spec['cases']):
        for repeat in range(spec['repeats']):
            scene_seed=seed+case_index*1000+repeat
            overrides=copy.deepcopy(case.get('overrides',{}))
            for key in ('lengths','masses','support_k','neighbour_lengths','neighbour_masses'):
                if key in overrides: overrides[key]=tuple(overrides[key])
            cfg=make_scene(seed=scene_seed,scene=case['scene'],geometry_id=case['geometry_id'],limit_id=case['limit_id'],
                           fixed_side=case['fixed_side'],capacity_nominal=case['capacity_nominal'],duration=spec['episode_s'],
                           **overrides)
            env=UnitEnv(cfg,seed=scene_seed); records=[]; query_log=[]
            try:
                boundary=env.reset(episode_id=repeat); runtime.reset(env.known,boundary,env.metadata['coordinate_map'])
                stages=case.get('stages',[{'start_s':0.,'query':case.get('query',{'kind':'random'})}]); active=-1; z=None; query=None
                for step in range(int(round(spec['episode_s']/.01))):
                    stage=max(i for i,s in enumerate(stages) if float(boundary['time'])+1e-8>=s['start_s'])
                    if stage!=active:
                        active=stage; query_spec=stages[stage]['query']
                        if query_spec['kind']=='random':
                            z=rng.normal(size=16); z=(z/np.linalg.norm(z)*4).astype(np.float32); query=None; info={'random_z':z.tolist()}
                        else:
                            query=Query(**query_spec); z,info=pool.integrate(runtime.b,query,spec['integration_samples'],scene_seed+stage)
                        query_log.append({'z':np.asarray(z).tolist(),'target_physical':query_spec,'stage':stage,'time':boundary['time'],'query':query_spec,'integration':info})
                    before=time.perf_counter(); u=runtime.act(z); latency=time.perf_counter()-before
                    try:boundary=copy.deepcopy(env.step(u))
                    except Exception as exc:
                        if not hasattr(exc,'boundary'):raise
                        boundary=copy.deepcopy(exc.boundary);boundary['diagnostics']['failure_reason']=str(exc)
                    if boundary['valid']:
                        feedback=runtime.observe(boundary,env.known)
                    else:
                        # Preserve diagnostic state without feeding a partial/nonfinite
                        # solver step to the public 100 Hz history interface.
                        feedback=copy.deepcopy(runtime.feedback())
                        feedback.update(stale=True,acc_valid=False)
                    records.append({**boundary,'feedback':feedback,'u':u,'latency_s':latency,'stage':stage,'known':env.known})
                    if boundary['terminated'] or boundary['truncated'] or not boundary['valid']: break
                per_stage=[]
                for entry in query_log:
                    subset=[r for r in records if r['stage']==entry['stage']]
                    if entry['query']['kind']!='random': per_stage.append({'stage':entry['stage'],**metrics(subset,Query(**entry['query']),spec)})
                result={'case':case,'repeat':repeat,'seed':scene_seed,'metrics':per_stage,'query_log':query_log,
                        'classification':'numerical_failure' if not all(r['valid'] for r in records) else 'observed_response',
                        'feasibility':'unverified' if case.get('feasibility_evidence') is None else case['feasibility_evidence'],
                        'latency_ms_p99':float(np.quantile([r['latency_s'] for r in records],.99)*1000),
                        'failure_preserved':True,'privileged_diagnostics':True}
                import gzip
                with gzip.open(output/f'case_{case_index:04d}_{repeat:03d}.json.gz','wt',encoding='utf8') as f:
                    json.dump(finite_json({'result':result,'records':records,'metadata':env.metadata}),f,allow_nan=False)
                results.append(result)
            finally: env.close()
    report={'version':VERSION,'evaluation_hash':fingerprint(spec),'rho':pool.rho,'pool_version':pool.version,
            'results':results,'validated':False,'note':'Per-case success is measured; feasibility and generalization require separate evidence.'}
    (output/'report.json').write_text(json.dumps(plain(report),indent=2),encoding='utf8')
    return report

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-dir',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--seed',type=int,default=8001)
    a=p.parse_args(argv); spec=json.loads((a.run_dir/'evaluation_spec.json').read_text())
    report=evaluate(a.run_dir/'export',a.run_dir/'query_pool.npz',spec,a.output,a.seed)
    print(json.dumps({'cases':len(report['results']),'validated':False,'output':str(a.output)}))
if __name__=='__main__': main()
