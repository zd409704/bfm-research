"""P0: full structure library, causal rule controllers, fixed role-balanced rho."""
import argparse,json,time,gc
from pathlib import Path
import numpy as np
import torch
import warp as wp
from .environment import UnitEnv,stream
from .mechanics import library,save_library
from .tasks import sample_tasks,durations


def rule_action(o,alpha,colored):
    q=o[:,0]*1.2; v=o[:,1]*6
    kind,ref,a,b,bias=alpha.T
    hold=6*(ref-q)-.6*v
    ramp=np.clip(np.where(ref>=0,1.2-q,1.2+q)/.15,0,1)
    ramp=ramp*ramp*(3-2*ramp)
    velocity=1.5*(ref*ramp-v)
    brake=-a*v
    compliant=bias+a*(ref-q)-b*v
    tau=np.where(kind==0,hold,np.where(kind==1,velocity,np.where(kind==2,brake,compliant)))
    return np.clip(np.where(kind==4,colored,tau/6),-1,1)


def run(out,seed=31001,count=32,nworld=4):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    wp.config.quiet=True; torch.set_num_threads(1)
    structures=library(seed,count,training=True)
    for s in structures:
        existing=out/'models'/f'{s.key}.xml'
        if existing.exists() and existing.read_text()!=s.xml():
            raise ValueError(f'Physics changed for existing P0 {s.key}; choose a new reference version')
    save_library(out/'models',structures)
    start=time.monotonic()
    refs=[[] for _ in range(4)]; rollouts=[]; nominal=[]; roles=[]; keys=[]
    for ix,s in enumerate(structures):
        path=out/f'{s.key}.pt'
        if path.exists():
            saved=torch.load(path,weights_only=False)
        else:
            env=UnitEnv(s,nworld=nworld,seed=73001)
            env.reset(np.arange(nworld),level=1,snapshots=False)
            rngs=[stream(73001,s.key,w,'bootstrap_command') for w in range(nworld)]
            erg=[stream(73001,s.key,w,'bootstrap_exploration') for w in range(nworld)]
            remain=np.zeros(nworld,int); alpha=np.zeros((nworld,5),np.float32)
            color=np.zeros(nworld); raw=[env.tensors['obs'].cpu().clone()]; ys=[]
            work=np.zeros((nworld,2)); events=np.zeros((5,2),int)
            for step in range(500):
                for w,rng in enumerate(rngs):
                    if remain[w]<=0:
                        alpha[w]=sample_tasks(rng,1)[0]
                        if rng.random()<.2: alpha[w,0]=4
                        remain[w]=durations(rng,1)[0]
                        events[int(alpha[w,0]),int(remain[w]>8)]+=1
                    color[w]=.95*color[w]+.2*erg[w].normal()
                o=raw[-1].numpy(); u=rule_action(o,alpha,color)
                _,y=env.step(torch.as_tensor(u[:,None],device=env.device,dtype=torch.float32))
                remain-=1
                if not bool(torch.isfinite(y).all()) or float(y[:,1].abs().max())>100:
                    raise FloatingPointError(f'Invalid bootstrap trajectory {s.key} step {step}')
                raw.append(y[:,:24].cpu().clone()); ys.append(y.cpu().clone())
                work+=env.tensors['work'].cpu().numpy()
                if step in (124,249,374): env.capture_snapshots(range(nworld))
            saved=dict(raw=torch.stack(raw,1),y=torch.stack(ys,1),m=env.m.cpu(),role=s.role,
                       key=s.key,work=work,events=events,snapshots=env.bank)
            torch.save(saved,path)
            del env; gc.collect()
        rollouts.append(saved['raw']); nominal.append(saved['m']); roles += [s.role]*nworld; keys += [s.key]*nworld
        refs[s.role].append(saved['y'].flatten(0,1))
        print(json.dumps(dict(stage='P0',model=s.key,completed=ix+1,total=len(structures),
                              W=(ix+1)*nworld*500,elapsed=time.monotonic()-start)),flush=True)
    rng=np.random.default_rng(83001)
    balanced=[]
    for values in refs:
        values=torch.cat(values)
        ids=rng.choice(len(values),16384,replace=len(values)<16384)
        balanced.append(values[ids])
    pool=torch.cat(balanced)
    torch.save(dict(reference=pool,raw=torch.cat(rollouts),m=torch.cat(nominal),roles=np.asarray(roles),
                    keys=keys,W=len(rollouts)*nworld*500,seed=seed),out/'bootstrap.pt')
    report=dict(W=len(rollouts)*nworld*500,reference_size=len(pool),roles=[16384]*4,
                elapsed_s=time.monotonic()-start,q_dq_tau_quantiles=torch.quantile(pool[:,[0,1,12]],
                torch.tensor([0.,.01,.5,.99,1.]),dim=0).tolist(),finite=bool(torch.isfinite(pool).all()))
    (out/'report.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report),flush=True)


def main():
    p=argparse.ArgumentParser(); p.add_argument('--out',required=True)
    p.add_argument('--count',type=int,default=32); p.add_argument('--nworld',type=int,default=4)
    a=p.parse_args(); run(a.out,count=a.count,nworld=a.nworld)

if __name__=='__main__': main()
