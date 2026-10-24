"""No-gradient paired goal-result and reward queries on the nominal R0 unit."""
import argparse,json,gc
from pathlib import Path
import numpy as np
import torch
import mujoco
import warp as wp
from .environment import UnitEnv
from .mechanics import Structure
from .networks import physical_result
from .tasks import project
from .learner import Learner


def static_goals(structure,targets):
    m=structure.compile(); d=mujoco.MjData(m)
    j=int(m.joint('motor').dofadr[0])
    results=[]
    for target in targets:
        d.qpos[:]=0; d.qvel[:]=0; d.qpos[j]=target
        mujoco.mj_forward(m,d)
        o=np.zeros(25,np.float32); o[0]=target/1.2
        for side,name in enumerate(('P','D')):
            rot=d.xmat[m.body(name).id].reshape(3,3)
            o[2+side*5]=rot[0,2]; o[3+side*5]=rot[0,0]
        o[12]=d.qfrc_bias[j]/6; o[13]=o[12]
        o[16:18]=[(target+1.2)/2.4,(1.2-target)/2.4]
        results.append(o)
    return np.asarray(results)


@torch.no_grad()
def run(learner,out):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    structure=Structure(0,100)
    targets=np.repeat(np.array([-.7,-.5,-.35,-.15,.15,.35,.5,.7],np.float32),4)
    goal=torch.as_tensor(static_goals(structure,targets),device=learner.device)
    alpha=np.zeros((len(targets),5),np.float32); alpha[:,1]=targets
    generator=torch.Generator(device=learner.device).manual_seed(120001)
    commands={'goal_result':project(learner.net.b(physical_result(goal))),
              'reward_query':learner.encode(alpha),
              'random_z':project(torch.randn(len(targets),16,device=learner.device,generator=generator))}
    summary={}
    for mode,z in commands.items():
        env=UnitEnv(structure,len(targets),seed=84001)
        x=env.reset(np.arange(len(targets)),level=0,snapshots=False)
        ys=[]; qps=[]
        for t in range(500):
            x,y=env.step(learner.net.actor(x,z))
            ys.append(y.cpu()); qps.append(env.sim.data.qpos.cpu().clone())
        y=torch.stack(ys,1).numpy(); q=y[:,:,0]*1.2; v=y[:,:,1]*6
        final=q[:,-100:].mean(1)
        errors=np.sqrt(((q[:,-100:]-targets[:,None])**2).mean(1))
        summary[mode]=dict(mean_hold_rmse=float(errors.mean()),
            mean_terminal_speed_rms=float(np.sqrt((v[:,-100:]**2).mean(1)).mean()),
            targets=targets.tolist(),terminal_q=final.tolist(),errors=errors.tolist(),
            terminal_q_spread=float(final.std()),mean_motion_range=float((q.max(1)-q.min(1)).mean()),
            saturation=float((np.abs(y[:,:,13])>.98).mean()))
        np.savez_compressed(out/f'{mode}.npz',y=y,qpos=torch.stack(qps,1).numpy(),z=z.cpu().numpy(),targets=targets)
        (out/f'{mode}.xml').write_text(structure.xml())
        del env; gc.collect()
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps({k:{name:value for name,value in v.items() if not isinstance(value,list)}
                      for k,v in summary.items()}),flush=True)
    return summary


def main():
    p=argparse.ArgumentParser(); p.add_argument('--checkpoint',required=True); p.add_argument('--out',required=True)
    a=p.parse_args(); wp.config.quiet=True; torch.set_num_threads(1)
    state=torch.load(a.checkpoint,weights_only=False,map_location='cuda:0')
    l=Learner(state['learner']['reference']); l.load_state_dict(state['learner'])
    run(l,a.out)

if __name__=='__main__': main()
