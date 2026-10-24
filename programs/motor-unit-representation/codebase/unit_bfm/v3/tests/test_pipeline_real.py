"""Short real CPU contracts, never a learning-quality or coverage certificate."""
import copy
import tempfile
import unittest
from pathlib import Path
import numpy as np
import torch
from unit_bfm.v3.physics import UnitEnv,make_scene
from unit_bfm.v3.collect import collect_episode
from unit_bfm.v3.replay import Replay
from unit_bfm.v3.coverage import inspect_episode,DEFAULT_THRESHOLDS
from unit_bfm.v3.learner import Learner
from unit_bfm.v3.train import schema_manifest,load_config,run,V3_ROOT
from unit_bfm.v3.interface import Interface,export_actor_b

class PipelineReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):torch.set_num_threads(1)
    def test_e0_e4_real_replay_update_export(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);replay=Replay(root/'replay',strict=True,rule_capacity=128,policy_capacity=128)
            schema=None;learner=None;first=None
            for i,scene in enumerate(['E0','E1','E2','E3','E4']):
                env=UnitEnv(make_scene(seed=12,scene=scene,duration=.08,initial_q=0.,initial_dq=0.,load_force=0.),seed=12)
                try:
                    current=schema_manifest(env)
                    if schema is None:schema=current;learner=Learner(current['p_dim']);first=(copy.deepcopy(env.known),copy.deepcopy(env.reset()),copy.deepcopy(env.metadata['coordinate_map']))
                    self.assertEqual(schema,current)
                    for source in ['rule','policy']:
                        e=collect_episode(env,f'{scene}_{source}',source,seed=i,learner=learner,max_steps=8,metadata={'scene':scene,'fixed_side':env.config.fixed_side})
                        self.assertTrue(e.valid.all())
                        for name,arr in e.reconstruct().items():np.testing.assert_allclose(arr,getattr(e,name),atol=1e-5)
                        replay.add(e,p0=source=='rule')
                        diagnostics=inspect_episode(e,DEFAULT_THRESHOLDS)
                        self.assertEqual(diagnostics['missing_diagnostics'],[])
                finally:env.close()
            batch=replay.sample(16);metrics=learner.update(batch);self.assertTrue(np.isfinite(metrics['fb']))
            export_actor_b(learner,root/'export',schema)
            runtime=Interface(root/'export');feedback=runtime.reset(first[0],first[1],first[2]);u=runtime.act(np.ones(16,dtype=np.float32))
            self.assertLessEqual(abs(u),1);self.assertEqual(feedback['B16'].shape,(16,));self.assertNotIn('p',feedback)
    def test_exact_checkpoint_resume(self):
        # Persistent outputs are under v3/runs; each temporary run parent is unique.
        parent=Path(tempfile.mkdtemp(prefix='pipeline_resume_',dir=V3_ROOT/'runs'))
        c=load_config(V3_ROOT/'configs/smoke.json')
        a=run(c,parent/'original');b=run(c,parent/'resumed',resume=parent/'original'/'p0.pt')
        sa=torch.load(parent/'original'/'final.pt',weights_only=False);sb=torch.load(parent/'resumed'/'final.pt',weights_only=False)
        self.assertEqual(a['updates'],b['updates']);self.assertEqual(a['W'],b['W'])
        for name in ('net','target'):
            for k,v in sa['learner'][name].items():torch.testing.assert_close(v,sb['learner'][name][k],rtol=0,atol=0)
        self.assertEqual(sa['schedulers'],sb['schedulers']);self.assertEqual(sa['replay']['rng'],sb['replay']['rng'])
        self.assertEqual(sa['state']['last_metrics'],sb['state']['last_metrics'])
        with self.assertRaises(FileExistsError):run(c,parent/'original')
        # Checkpoint schema/version mismatch rejection occurs before learner restoration.
        bad=copy.deepcopy(c);bad['version']='V2'
        from unit_bfm.v3.train import read_checkpoint
        with self.assertRaises(ValueError):read_checkpoint(parent/'original'/'p0.pt',bad)

if __name__=='__main__':unittest.main()
