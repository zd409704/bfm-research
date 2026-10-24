"""P1–P3 training with persistent manifests, raw Replay, and periodic held-out checks."""
import argparse,gc,hashlib,importlib.metadata,json,os,platform,random,signal,sys,time,shutil
from pathlib import Path
from dataclasses import asdict
import numpy as np
import torch
import warp as wp
from . import VERSION
from .environment import UnitEnv,stream
from .mechanics import library,save_library,Structure
from .tasks import durations,project
from .networks import physical_result
from .learner import Learner
from .replay import SequenceReplay


def stage_at(W,p0,cfg):
    if cfg.get('diagnostic_role') is not None:
        weights=np.zeros(4); weights[cfg['diagnostic_role']]=1.
        return 'R0_DIAGNOSTIC',0.,weights,weights
    if W<p0+cfg['P1_W']: return 'P1',0.,np.array([.7,.3,0,0]),np.array([.7,.3,0,0])
    if W<p0+cfg['P1_W']+cfg['P2_W']:
        a=(W-p0-cfg['P1_W'])/cfg['P2_W']
        return 'P2',a,(1-a)*np.array([.7,.3,0,0])+a*np.array([.25,.3,.2,.25]),(1-a)*np.array([.7,.3,0,0])+a*.25
    return 'P3',1.,np.array([.25,.3,.2,.25]),np.full(4,.25)


def manifest(cfg):
    sources={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('unit_bfm').glob('*.py')}
    return dict(version=VERSION,config=cfg,python=sys.executable,platform=platform.platform(),
        packages={p:importlib.metadata.version(p) for p in ('torch','numpy','mujoco','mujoco-warp','warp-lang','mjlab')},
        cuda_device=torch.cuda.get_device_name(),source_sha256=sources,
        schema=dict(o=24,m=28,raw_result=25,b_input=23,x=336,z=16,control_hz=100,physics_hz=1000,
                    slow=dict(hz=50,length=10,phase='episode even n>=2',age_scale_s=.2),
                    fast=dict(hz=100,length=8,fields=['u_previous','tau_endpoint','padding'])),
        permissions='SIM_PRIVILEGED; actual dynamics parameters and future plans hidden')


def run(cfg,out,resume=None):
    out=Path(out)
    if (out/'manifest.json').exists() and not resume:
        raise FileExistsError('Existing run: use --resume or choose a new output directory')
    out.mkdir(parents=True,exist_ok=True)
    torch.set_num_threads(1); wp.config.quiet=True
    torch.manual_seed(cfg['seed']); np.random.seed(cfg['seed']); random.seed(cfg['seed'])
    torch.backends.cuda.matmul.allow_tf32=True
    if cfg['version'] != VERSION:
        raise ValueError('Configuration version does not match source')
    bootstrap=torch.load(cfg['bootstrap'],weights_only=False)
    learner=Learner(bootstrap['reference'],cfg['device'],cfg['seed']+10)
    cfg['replay_capacity']=max(cfg['replay_capacity'],4*cfg['num_envs']*cfg['horizon'])
    replay=SequenceReplay(cfg['replay_capacity'],cfg['horizon'],cfg['device'],cfg['seed']+20)
    scheduler=np.random.default_rng(cfg['seed']+30)
    goal_rng=np.random.default_rng(cfg['seed']+70)
    diagnostic_rng=np.random.default_rng(cfg['seed']+80)
    p0=int(bootstrap['W']); W=p0; visit=0; credit=0.; episode=100000
    structures=library(); save_library(out/'models',structures)
    queues={}; snapshots={}; role_counts=np.zeros(4,np.int64); visits={}; role_debt=np.zeros(4)
    stop=False
    def handle_stop(sig,frame):
        nonlocal stop
        stop=True
    signal.signal(signal.SIGTERM,handle_stop); signal.signal(signal.SIGINT,handle_stop)
    if resume:
        state=torch.load(resume,weights_only=False,map_location=cfg['device'])
        learner.load_state_dict(state['learner']); replay.load_state_dict(state['replay'])
        W=state['W']; visit=state['visit']; credit=state['credit']; episode=state['episode']
        scheduler.bit_generator.state=state['scheduler']; queues=state['queues']; snapshots=state['snapshots']
        role_counts=state['role_counts']; visits=state['visits']
        role_debt=state['role_debt']
        goal_rng.bit_generator.state=state['goal_rng']
        diagnostic_rng.bit_generator.state=state['diagnostic_rng']
        torch.set_rng_state(state['torch_rng'].cpu()); torch.cuda.set_rng_state(state['cuda_rng'].cpu())
    info=manifest(cfg); info['counts']=learner.net.counts(); info['bootstrap_W']=p0
    (out/'manifest.json').write_text(json.dumps(info,indent=2))
    (out/'config.json').write_text(json.dumps(cfg,indent=2))
    code_dir=out/'source'; code_dir.mkdir(exist_ok=True)
    for source in Path('unit_bfm').glob('*.py'): shutil.copy2(source,code_dir/source.name)
    log=(out/'metrics.jsonl').open('a'); start=time.monotonic(); start_W=W
    next_save=(W//cfg['save_every_W']+1)*cfg['save_every_W']
    next_eval=(W//cfg['eval_every_W']+1)*cfg['eval_every_W']
    if cfg.get('evaluate_initial') and not resume:
        from .evaluate import evaluate
        initial=evaluate(learner,out/'initial_validation',nominal_only=cfg.get('fixed_structure',False))
        print(json.dumps(dict(W=W,initial_validation=initial['summary'])),flush=True)

    def save(final=False):
        state=dict(version=VERSION,W=W,learner=learner.state_dict(),replay=replay.state_dict(),
            visit=visit,credit=credit,episode=episode,scheduler=scheduler.bit_generator.state,
            queues=queues,snapshots=snapshots,role_counts=role_counts,visits=visits,role_debt=role_debt,
            torch_rng=torch.get_rng_state(),cuda_rng=torch.cuda.get_rng_state(),
            goal_rng=goal_rng.bit_generator.state,diagnostic_rng=diagnostic_rng.bit_generator.state)
        tmp=out/'checkpoint.tmp'; torch.save(state,tmp); os.replace(tmp,out/'checkpoint.pt')
        torch.save({k:v for k,v in state.items() if k not in ('replay','snapshots')},out/f'model_{W:09d}.pt')
        (out/'status.json').write_text(json.dumps(dict(W=W,target_W=cfg['total_W'],stage=stage_at(W,p0,cfg)[0],
            updates=learner.updates,elapsed_s=time.monotonic()-start,
            state=('stopped' if stop else 'budget_completed') if final else 'training',
            validated=False),indent=2))

    while W<cfg['total_W'] and not stop:
        stage,level,collect_weights,source_weights=stage_at(W,p0,cfg)
        role_debt+=collect_weights
        role=int(np.argmax(role_debt+scheduler.uniform(0,1e-8,4)))
        role_debt[role]-=1
        key=(role,stage=='P1')
        if not queues.get(key):
            queues[key]=scheduler.permutation(8 if stage=='P1' else 32).tolist()
        model_index=queues[key].pop()
        structure=structures[role*32+model_index]
        if cfg.get('fixed_structure'):
            structure=Structure(role,0)
        env=UnitEnv(structure,cfg['num_envs'],cfg['device'],seed=cfg['seed']+40)
        env.bank=snapshots.get(structure.key,[])
        ids=np.arange(episode,episode+cfg['num_envs']); episode+=cfg['num_envs']
        x=env.reset(ids,level=level)
        replay.begin(env.tensors['obs'],env.m,role)
        crng=[stream(cfg['seed'],structure.key,int(i),'command') for i in ids]
        erng=[stream(cfg['seed'],structure.key,int(i),'exploration') for i in ids]
        left=np.zeros(cfg['num_envs'],int); z=torch.zeros(cfg['num_envs'],16,device=cfg['device'])
        events=np.zeros((2,2),int); loss_sum=torch.zeros(len(learner.metric_names),device=cfg['device']); update_n=0
        ystats=[]; time_before=time.monotonic()
        for step in range(cfg['horizon']):
            change=np.flatnonzero(left<=0)
            if len(change):
                if replay.length.sum()>0:
                    goals=replay.sample_results(len(change),source_weights,goal_rng)
                else:
                    gi=goal_rng.integers(len(bootstrap['reference']),size=len(change))
                    goals=bootstrap['reference'][gi].to(cfg['device'])
                with torch.no_grad():
                    commands=project(learner.net.b(physical_result(goals)))
                    for j,w in enumerate(change):
                        r=crng[w]; is_random=r.random()<.5
                        left[w]=durations(r,1)[0]
                        events[int(is_random),int(left[w]>8)]+=1
                        if is_random:
                            direction=r.normal(size=16)
                            commands[j]=torch.as_tensor(4*direction/np.linalg.norm(direction),device=cfg['device'],dtype=torch.float32)
                z[change]=commands
            with torch.no_grad():
                noise=torch.as_tensor([r.normal(0,.2) for r in erng],device=cfg['device'],dtype=torch.float32)[:,None]
                u=(learner.net.actor(x,z)+noise).clamp(-1,1)
                x,y=env.step(u)
            if not bool(torch.isfinite(y).all()) or float(y[:,1].abs().max())>100:
                torch.save(dict(model=asdict(structure),y=y.cpu(),W=W),out/'invalid_sample.pt')
                raise FloatingPointError('Invalid physics; trajectory quarantined, training stopped')
            replay.append(y[:,:24]); left-=1
            W+=cfg['num_envs']; role_counts[role]+=cfg['num_envs']
            if W-p0>=cfg.get('warmup_W',8192): credit+=cfg['num_envs']/256
            while credit>=1:
                metrics=learner.update(replay.sample(cfg['batch_size'],source_weights))
                loss_sum+=metrics; update_n+=1; credit-=1
            if step in (124,249,374): env.capture_snapshots(range(min(8,cfg['num_envs'])))
            if step%50==0: ystats.append(y[:,:].detach().cpu())
        snapshots[structure.key]=env.bank
        visits[structure.key]=visits.get(structure.key,0)+1
        visit+=1
        learner.set_reference(replay.sample_results(65536,source_weights,diagnostic_rng),
                              source=f'Replay_at_W{W}_weights{source_weights.tolist()}')
        diag=learner.diagnostics()
        data=torch.cat(ystats)
        record=dict(W=W,stage=stage,model=structure.key,level=level,updates=learner.updates,
                    bucket_seconds=time.monotonic()-time_before,wall_seconds=time.monotonic()-start,
                    W_per_second=(W-start_W)/(time.monotonic()-start),
                    learning=dict(zip(learner.metric_names,(loss_sum/max(update_n,1)).cpu().tolist())),
                    role_W=role_counts.tolist(),command_events=events.tolist(),reset=env.reset_stats,
                    dq_rms=float((data[:,1]*6).square().mean().sqrt()),saturation=float((data[:,13].abs()>.98).float().mean()),
                    **diag)
        log.write(json.dumps(record)+'\n'); log.flush(); print(json.dumps(record),flush=True)
        del env; gc.collect()
        if W>=next_save or stop or W>=cfg['total_W']:
            save(); next_save=(W//cfg['save_every_W']+1)*cfg['save_every_W']
        if W>=next_eval:
            from .evaluate import evaluate
            result=evaluate(learner,out/'validation'/f'W{W:09d}',nominal_only=cfg.get('fixed_structure',False))
            print(json.dumps(dict(W=W,validation=result['summary'])),flush=True)
            next_eval=(W//cfg['eval_every_W']+1)*cfg['eval_every_W']
    save(final=True); learner.refresh()
    torch.save(dict(version=VERSION,W=W,actor=learner.net.actor.state_dict(),b=learner.net.b.state_dict(),
                    covariance=learner.cov.cpu(),reward_cross=learner.cross.cpu(),reference=learner.reference.cpu(),
                    manifest=info,validated=False,candidate=True),out/'candidate_unit.pt')
    log.close()
    print(json.dumps(dict(finished_W=W,updates=learner.updates,out=str(out))),flush=True)


def main():
    p=argparse.ArgumentParser(); p.add_argument('--config',default='unit_bfm/configs/train.json')
    p.add_argument('--out',required=True); p.add_argument('--resume'); p.add_argument('--total-W',type=int)
    p.add_argument('--num-envs',type=int); p.add_argument('--eval-every-W',type=int)
    a=p.parse_args(); cfg=json.loads(Path(a.config).read_text())
    for arg,key in ((a.total_W,'total_W'),(a.num_envs,'num_envs'),(a.eval_every_W,'eval_every_W')):
        if arg is not None: cfg[key]=arg
    run(cfg,a.out,a.resume)

if __name__=='__main__': main()
