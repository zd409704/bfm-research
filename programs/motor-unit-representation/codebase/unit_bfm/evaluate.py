"""Paired held-out unit task panel; analytic controller is a reference, not a teacher."""
import argparse,json,gc,os
from pathlib import Path
import numpy as np
import torch
import warp as wp
from .mechanics import library,Structure
from .environment import UnitEnv
from .tasks import rewards,project
from .bootstrap import rule_action


def panel(per_family=4):
    alpha=[]
    for q in np.linspace(-.7,.7,per_family): alpha.append([0,q,0,0,0])
    vs=[-.5,.5,-2,2,-1,1,-4,4][:per_family]
    for v in vs: alpha.append([1,v,0,0,0])
    for a in np.linspace(.5,2,per_family): alpha.append([2,0,a,.1,0])
    for i,K in enumerate(np.geomspace(.3,12,per_family)): alpha.append([3,(-1)**i*.3,K,.15,0])
    return np.asarray(alpha,np.float32)


@torch.no_grad()
def evaluate(learner,out,full=False,analytic=False,save_trajectories=False,nominal_only=False):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    learner.refresh()
    structures=library(41001,count=8,training=False)
    tasks=panel(8 if full else 4)
    # Each task repeated under four initial states; each role is a separate condition.
    alpha=np.repeat(tasks,4,axis=0)
    models=[s for s in structures if s.index < (2 if full else 1)]
    if nominal_only: models=[Structure(0,100)]
    records=[]
    for structure in models:
        env=UnitEnv(structure,nworld=len(alpha),seed=84001)
        env.reset(np.arange(len(alpha)),level=0 if nominal_only else 1,snapshots=False)
        z=learner.encode(alpha)
        x=env.history.input(env.m)
        ys=[]; works=[]; qp=[]
        for step in range(500):
            if analytic:
                u=torch.as_tensor(rule_action(env.tensors['obs'].cpu().numpy(),alpha,np.zeros(len(alpha))),
                                  device=env.device,dtype=torch.float32)[:,None]
            else: u=learner.net.actor(x,z)
            x,y=env.step(u)
            if not torch.isfinite(y).all(): raise FloatingPointError('Invalid evaluation physics')
            ys.append(y.cpu()); works.append(env.tensors['work'].cpu().clone())
            if save_trajectories: qp.append(env.sim.data.qpos.cpu().clone())
        yy=torch.stack(ys,1); work=torch.stack(works,1)
        a=torch.as_tensor(alpha)
        rr=rewards(yy.flatten(0,1),a,include_command=False).reshape(len(alpha),500,len(alpha))
        returns=rr[torch.arange(len(alpha)),:,torch.arange(len(alpha))].mean(1)
        for i in range(len(alpha)):
            q=yy[i,:,0]*1.2; v=yy[i,:,1]*6; tau=yy[i,:,12]*6
            kind,ref,K,D,bias=alpha[i]
            if kind==0: error=float(((q[-100:]-ref)**2).mean().sqrt())
            elif kind==1:
                feasible=((1.2-q) if ref>=0 else (1.2+q))>.15
                error=float(((v[feasible]-ref)**2).mean().sqrt()) if feasible.any() else None
            elif kind==2: error=float(v[-100:].square().mean().sqrt())
            else: error=float((tau-(bias+K*(ref-q)-D*v)).square().mean().sqrt())
            records.append(dict(model=structure.key,task=int(kind),alpha=alpha[i].tolist(),initial=i%4,
                reward=float(returns[i]),physical_error=error,positive_work=float(work[i,:,0].sum()),
                negative_work=float(work[i,:,1].sum()),saturation=float((yy[i,:,13].abs()>.98).float().mean()),
                q_min=float(q.min()),q_max=float(q.max()),dq_max=float(v.abs().max())))
        if save_trajectories:
            np.savez_compressed(out/f'{structure.key}.npz',y=yy.numpy(),qpos=torch.stack(qp,1).numpy(),
                                work=work.numpy(),alpha=alpha,z=z.cpu().numpy())
            (out/f'{structure.key}.xml').write_text(structure.xml())
        del env; gc.collect()
    summary={}
    for kind,name in enumerate(('hold','velocity','brake','compliance')):
        subset=[r for r in records if r['task']==kind]
        summary[name]=dict(mean_reward=float(np.mean([r['reward'] for r in subset])),
            mean_physical_error=float(np.mean([r['physical_error'] for r in subset if r['physical_error'] is not None])),
            mean_saturation=float(np.mean([r['saturation'] for r in subset])))
    result=dict(profile='SIM_PRIVILEGED',controller='analytic' if analytic else 'FB_actor',
                summary=summary,representation=learner.diagnostics(),records=records)
    (out/'metrics.json').write_text(json.dumps(result,indent=2)); return result


@torch.no_grad()
def random_atlas(learner,out,nz=256):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    generator=torch.Generator(device=learner.device).manual_seed(94001)
    directions=project(torch.randn(nz,16,device=learner.device,generator=generator)).repeat_interleave(2,0)
    report=[]
    for structure in [s for s in library(51001,8,False) if s.index<2]:
        env=UnitEnv(structure,nworld=2*nz,seed=85001)
        x=env.reset(np.arange(2*nz),level=1,snapshots=False)
        ys=[]; qp=[]
        for t in range(500):
            x,y=env.step(learner.net.actor(x,directions))
            ys.append(y.cpu()); qp.append(env.sim.data.qpos.cpu().clone())
        y=torch.stack(ys,1)
        if not torch.isfinite(y).all(): raise FloatingPointError('Nonfinite atlas rollout')
        np.savez_compressed(out/f'{structure.key}.npz',y=y.numpy(),qpos=torch.stack(qp,1).numpy(),
                            z=directions.cpu().numpy())
        (out/f'{structure.key}.xml').write_text(structure.xml())
        report.append(dict(model=structure.key,mean_q_range=float((y[:,:,0].amax(1)-y[:,:,0].amin(1)).mean()*1.2),
                           saturation=float((y[:,:,13].abs()>.98).float().mean())))
        del env; gc.collect()
    (out/'index.json').write_text(json.dumps(report,indent=2)); return report


def main():
    from .learner import Learner
    p=argparse.ArgumentParser(); p.add_argument('--checkpoint',required=True); p.add_argument('--bootstrap',required=True)
    p.add_argument('--out',required=True); p.add_argument('--full',action='store_true'); p.add_argument('--analytic',action='store_true')
    p.add_argument('--atlas',action='store_true'); p.add_argument('--nominal',action='store_true')
    a=p.parse_args(); torch.set_num_threads(1); wp.config.quiet=True
    l=Learner(torch.load(a.bootstrap,weights_only=False)['reference'])
    state=torch.load(a.checkpoint,weights_only=False,map_location=l.device); l.load_state_dict(state['learner'])
    result=evaluate(l,a.out,a.full,a.analytic,True,a.nominal); print(json.dumps(result['summary']))
    if a.atlas: random_atlas(l,Path(a.out)/'random_z')

if __name__=='__main__': main()
