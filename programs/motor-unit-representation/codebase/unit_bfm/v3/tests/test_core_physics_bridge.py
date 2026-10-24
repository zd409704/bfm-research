"""Short CPU integration of core APIs against the concurrently supplied modules.

This checks feature/learning wiring, not scene coverage or physical correctness.
No replay files, models or weights are written.
"""
import unittest
import numpy as np
import torch
from unit_bfm.v3.schema import MEMORY_DIM, concatenate_privileged
from unit_bfm.v3.features import FeatureHistory
from unit_bfm.v3.learner import Learner


class CorePhysicsBridgeTests(unittest.TestCase):
    def test_cpu_e0_both_sides_features_and_actual_p(self):
        from unit_bfm.v3.physics import UnitEnv, make_scene
        for side in ('P','D'):
            env=UnitEnv(make_scene(seed=81,scene='E0',fixed_side=side,duration=.3))
            try:
                b=env.reset(); h=FeatureHistory(); h.reset(b,env.known)
                for i in range(25):
                    b=env.step(float(.1*np.sin(i*.3))); h.append(b,env.known)
                    f=h.features()
                    self.assertTrue(b['valid'])
                    p=concatenate_privileged(b['p'],f['memory'])
                    self.assertEqual(len(p),env.p_dim+MEMORY_DIM)
                    self.assertEqual(len(env.physics_schema),env.p_dim)
                    self.assertTrue(np.isfinite(p).all())
                    if i==22: clone=FeatureHistory.from_memory(f['memory'],env.known,b['time'])
                    if i==23:
                        clone.append(b,env.known)
                        for key in f: np.testing.assert_allclose(clone.features()[key],f[key],atol=2e-5)
            finally: env.close()

    def test_collector_episode_reconstruct_and_replay_update_without_disk(self):
        from unit_bfm.v3.physics import UnitEnv, make_scene
        from unit_bfm.v3.collect import collect_episode
        from unit_bfm.v3.replay import Replay
        torch.set_num_threads(1)
        env=UnitEnv(make_scene(seed=81,scene='E0',duration=.3))
        try:
            ep=collect_episode(env,'core_e0',max_steps=30)
            for key,value in ep.reconstruct().items():
                np.testing.assert_allclose(value,getattr(ep,key),atol=1e-6)
            # Replay.add now retains bounded RAM transitions, without episode files.
            from pathlib import Path
            replay=Replay(Path(__file__).parent,strict=False,scene_weights={'E0':1.})
            replay.add(ep)
            batch=replay.sample(8)
            learner=Learner(env.p_dim+MEMORY_DIM,seed=45)
            metrics=learner.update(batch)
            self.assertTrue(all(np.isfinite(v) for v in metrics.values()))
            self.assertGreater(metrics['actor_grad'],0)
            self.assertGreater(metrics['f_grad'],0)
            self.assertGreater(metrics['b_grad'],0)
            self.assertEqual(learner.updates,1)
        finally: env.close()

if __name__=='__main__': unittest.main()
