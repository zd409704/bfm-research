"""Report measured deployment/learning latency and storage without pass fabrication."""
import argparse,json,time,tempfile
from pathlib import Path
import numpy as np
import torch
from unit_bfm.v3.physics import UnitEnv,make_scene
from unit_bfm.v3.features import FeatureHistory
from unit_bfm.v3.schema import MEMORY_DIM
from unit_bfm.v3.learner import Learner
from unit_bfm.v3.collect import collect_episode
from unit_bfm.v3.replay import Replay

def measure(device='cpu'):
    torch.set_num_threads(1)
    env=UnitEnv(make_scene(seed=228,scene='E0',duration=.5))
    try:
        start=time.perf_counter();ep=collect_episode(env,'benchmark',max_steps=50)
        collect_s=time.perf_counter()-start
        net=Learner(env.p_dim+MEMORY_DIM,device=device,seed=42)
        x=torch.tensor(ep.x[-1].copy(),device=device)[None]
        g=torch.tensor(ep.g[-1].copy(),device=device)[None];z=net.sample_z(1)
        def sync():
            if device.startswith('cuda'):torch.cuda.synchronize()
        times=[]
        with torch.no_grad():
            for i in range(220):
                sync();start=time.perf_counter();net.net.actor(x,z);net.net.b(g);sync()
                if i>=20:times.append((time.perf_counter()-start)*1000)
        with tempfile.TemporaryDirectory() as tmp:
            replay=Replay(tmp,scene_weights={'E0':1.},max_episode_steps=50,strict=False)
            replay.add(ep,p0=True)
            disk=sum(p.stat().st_size for p in Path(tmp).rglob('*') if p.is_file())
            bt=[];ut=[]
            for i in range(12):
                start=time.perf_counter();b=replay.sample(512,device=device);sync();bt.append(time.perf_counter()-start)
                start=time.perf_counter();net.update(b);sync();ut.append(time.perf_counter()-start)
        return dict(device=device,physics_p=env.p_dim,memory_dim=MEMORY_DIM,counts=net.net.counts(),
                    actor_plus_B_ms_p50=float(np.median(times)),actor_plus_B_ms_p99=float(np.quantile(times,.99)),
                    CPU_collection_W_per_s=50/collect_s,episode_bytes=disk,bytes_per_transition=disk/50,
                    sample512_s=float(np.median(bt[2:])),update512_s=float(np.median(ut[2:])),
                    note='CPU episode collection; network device separately specified; latency excludes external sensors/bus.')
    finally:env.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cpu');args=p.parse_args();print(json.dumps(measure(args.device),indent=2))
