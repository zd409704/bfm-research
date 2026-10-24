"""Coordinator-owned tests spanning physical boundaries, replay, and learning."""
import copy
import tempfile
import unittest
import numpy as np
import torch


class IntegratedContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)

    def test_physics_feature_history_and_privacy_all_templates(self):
        from unit_bfm.v3.physics import UnitEnv, make_scene
        from unit_bfm.v3.features import FeatureHistory
        from unit_bfm.v3.schema import MEMORY_DIM
        schemas=[]
        for scene in ('E0','E1','E2','E3','E4'):
            for side in ('P','D'):
                with self.subTest(scene=scene,side=side):
                    env=UnitEnv(make_scene(seed=113,scene=scene,fixed_side=side),seed=31)
                    try:
                        b=env.reset(episode_id=0); h=FeatureHistory(); h.reset(b,env.known)
                        schemas.append(env.physics_schema)
                        for t in range(26):
                            previous=copy.deepcopy(b)
                            u=.12*np.sin(t*.21)
                            b=env.step(float(u)); h.append(b,env.known)
                            f=h.features()
                            self.assertTrue(b['valid'],b['diagnostics'])
                            self.assertAlmostEqual(b['time']-previous['time'],.01,places=7)
                            self.assertEqual(f['g'].shape,(13,))
                            self.assertEqual(f['x'].shape,(137,))
                            self.assertEqual(f['memory'].shape,(MEMORY_DIM,))
                            self.assertTrue(all(np.isfinite(a).all() for a in f.values()))
                            self.assertAlmostEqual(b['u_integral'],u*.01,places=7)
                            # Reconstruct causal state, then check its next update against the real history.
                            if t==23:
                                restored=FeatureHistory.from_memory(f['memory'],env.known,b['time'])
                            if t==24:
                                restored.append(b,env.known)
                                for name in f:
                                    np.testing.assert_allclose(restored.features()[name],f[name],atol=2e-5,rtol=2e-5)
                        state=h.state_dict(); altered=copy.deepcopy(b)
                        altered['p']=np.full_like(b['p'],1e6)
                        altered['diagnostics']={'unknown_contact_force':1e6}
                        h1=FeatureHistory(); h1.reset(dict(altered,interval_valid=False),env.known)
                        h2=FeatureHistory(); h2.reset(dict(b,interval_valid=False),env.known)
                        for name in ('g','x'):
                            np.testing.assert_array_equal(h1.features()[name],h2.features()[name])
                    finally:
                        env.close()
        self.assertTrue(all(s==schemas[0] for s in schemas),'physics schema must be common to all templates')

    def test_real_episode_replay_fb_and_exact_update_resume(self):
        from unit_bfm.v3.physics import UnitEnv, make_scene
        from unit_bfm.v3.collect import collect_episode
        from unit_bfm.v3.replay import Replay
        from unit_bfm.v3.learner import Learner
        with tempfile.TemporaryDirectory() as tmp:
            env=UnitEnv(make_scene(seed=81,scene='E0',duration=.3),seed=61)
            try:
                ep=collect_episode(env,'integration_rule',source='rule',max_steps=30)
                for name,value in ep.reconstruct().items():
                    np.testing.assert_allclose(value,getattr(ep,name),atol=1e-6,rtol=1e-6)
                replay=Replay(tmp,seed=3,scene_weights={'E0':1.},max_episode_steps=30,strict=False)
                replay.add(ep,p0=True)
                learner=Learner(ep.p.shape[1],seed=17)
                pol=collect_episode(env,'integration_policy',source='policy',learner=learner,max_steps=30)
                replay.add(pol)
                batch=replay.sample(16)
                before={k:v.detach().clone() for k,v in learner.net.actor.state_dict().items()}
                metrics=learner.update(batch)
                self.assertTrue(all(np.isfinite(v) for v in metrics.values()))
                self.assertTrue(any(not torch.equal(before[k],v) for k,v in learner.net.actor.state_dict().items()))
                clone=Learner(ep.p.shape[1],seed=333); clone.load_state_dict(learner.state_dict())
                a=learner.update(batch); b=clone.update(batch)
                self.assertEqual(a,b)
                for k,v in learner.net.state_dict().items():
                    torch.testing.assert_close(v,clone.net.state_dict()[k],atol=0,rtol=0)
                self.assertGreater(metrics['actor_grad'],0)
            finally:
                env.close()


if __name__=='__main__': unittest.main()
