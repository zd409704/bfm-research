"""Coordinator: real batched GPU physics -> RAM replay -> CUDA FB -> export."""
import argparse
import hashlib
import json
import time
from pathlib import Path
import numpy as np
import torch
from unit_bfm.v3.physics import make_scene
from unit_bfm.v3.collect import make_batch,collect_batch,matching_goal_provider
from unit_bfm.v3.learner import Learner
from unit_bfm.v3.replay import Replay
from unit_bfm.v3.schema import MEMORY_DIM
from unit_bfm.v3.train import schema_manifest
from unit_bfm.v3.interface import export_actor_b


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    out=Path(a.output);out.mkdir(exist_ok=False)
    root=Path(__file__).resolve().parents[1]
    def hashes():return {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in root.glob('*.py')}
    before=hashes();torch.set_num_threads(1)
    replay=Replay(rule_capacity=512,policy_capacity=512)
    learner=None;rows=0;metrics=[];start=time.monotonic();scenes=[]
    for j,scene in enumerate(('E0','E1','E2','E3','E4')):
        c=make_scene(seed=0,scene=scene,fixed_side='D' if j%2 else 'P',tilt=0.,duration=.2,load_start=.02,load_end=.12)
        batch=make_batch([c,c],backend='mujoco-warp',device='cuda:0')
        try:
            if learner is None:
                learner=Learner(batch.p_dim+MEMORY_DIM,device='cuda:0',seed=71)
                schema=schema_manifest(batch.envs[0])
            episodes=collect_batch(batch,[scene+'_r',scene+'_p'],['rule','policy'],[7,8],learner=learner,
                                   max_steps=20,goal_provider=matching_goal_provider(replay))
            assert len(episodes)==2
            for ep in episodes:
                assert ep.valid.all()
                replay.add(ep);rows+=len(ep)
            for _ in range(8):
                m=learner.update(replay.sample(32,device='cuda:0'))
                assert all(np.isfinite(v) for v in m.values());metrics.append(m)
            scenes.append({'scene':scene,'rows':sum(map(len,episodes))})
        finally:batch.close()
    torch.cuda.synchronize()
    export_actor_b(learner,out/'export',schema,{'probe':True})
    torch.save(learner.state_dict(),out/'learner.pt')
    after=hashes()
    result={'device':torch.cuda.get_device_name(),'backend':'mujoco-warp','worlds':2,'rows':rows,
            'updates':learner.updates,'seconds':time.monotonic()-start,'scenes':scenes,
            'gradient_usage':dict(replay.audit),'last_metrics':metrics[-1],'counts':learner.net.counts(),
            'before':before,'after':after,'changed':[k for k in before if before[k]!=after[k]],'validated':False}
    (out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('before','after')},indent=2))


if __name__=='__main__':main()
