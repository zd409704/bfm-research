"""Physics gates, recorded as JSON; a failure exits before training."""
import argparse,json,time
from pathlib import Path
import numpy as np
import torch
import warp as wp
from .environment import UnitEnv
from .mechanics import Structure
from .cpu import CPUUnit


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',default='unit_bfm/artifacts/physics.json')
    args=ap.parse_args(); torch.set_num_threads(1); wp.config.quiet=True
    results={}
    for role in range(4):
        env=UnitEnv(Structure(role,0),nworld=2)
        env.reset([910,911],level=1,snapshots=False)
        # Force an in-window off-COM pulse, exercise moment and duration clearing.
        env.tensors['pulses'][:,0]=torch.tensor([.02,.12,1.,2.,.1,.7,1.],device=env.device)
        cpu=CPUUnit.from_gpu(env)
        diffs=[]; obs=[]
        for i in range(30):
            u=.15*np.sin(i*.2)
            yc=cpu.step(u)
            _,yg=env.step(torch.full((2,1),u,device=env.device))
            diff=np.abs(yc-yg[0].cpu().numpy()); diffs.append(diff); obs.append(yg.cpu().numpy())
        diffs=np.asarray(diffs)
        # Contact trajectories may branch, but short trajectories must agree closely.
        q_error=float(diffs[:,:2].max()); wrench_error=float(diffs[:,18:24].max())
        threshold=.03 if role==2 else .003
        if q_error>threshold or wrench_error>(.5 if role==2 else .01):
            raise AssertionError(f'CPU/GPU mismatch R{role}: q={q_error}, wrench={wrench_error}')
        # Same reset is bitwise repeatable and uses immutable nominal parameters.
        env.reset([910,911],level=1,snapshots=False)
        mass=env.sim.model.body_mass.clone(); before=env.history.input(env.m).clone()
        env.reset([910,911],level=1,snapshots=False)
        torch.testing.assert_close(mass,env.sim.model.body_mass.clone(),rtol=0,atol=0)
        torch.testing.assert_close(before,env.history.input(env.m),rtol=0,atol=0)
        assert not torch.equal(mass[0,1:],mass[1,1:])
        results[f'R{role}']=dict(max_q_dq_normalized_error=q_error,max_wrench_normalized_error=wrench_error,
                               finite=bool(np.isfinite(obs).all()),reset_repeatable=True)
        del env
    # Exact latency+one-pole response independent of mechanical motion.
    env=UnitEnv(Structure(0,1),nworld=2)
    env.tensors['delay'].fill_(10); env.tensors['tm'].fill_(.01)
    _,y1=env.step(torch.ones(2,1,device=env.device)); _,y2=env.step(torch.ones(2,1,device=env.device))
    torch.testing.assert_close(y1[:,12],torch.zeros(2,device=env.device),atol=1e-6,rtol=0)
    torch.testing.assert_close(y2[:,12],torch.full((2,),1-np.exp(-1),device=env.device),atol=1e-5,rtol=0)
    results['delay_one_pole']='pass'
    p=Path(args.out); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
