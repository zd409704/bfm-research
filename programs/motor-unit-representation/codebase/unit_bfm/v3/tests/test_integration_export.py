"""Roundtrip runtime checks: Actor/B deployment has no additional F input."""
import tempfile
import unittest
from pathlib import Path
import numpy as np
import torch

class ExportRoundtripTests(unittest.TestCase):
    def test_export_matches_online_without_physics_privileged_vector(self):
        from unit_bfm.v3.physics import UnitEnv,make_scene
        from unit_bfm.v3.learner import Learner
        from unit_bfm.v3.features import FeatureHistory
        from unit_bfm.v3.schema import MEMORY_DIM
        from unit_bfm.v3.train import schema_manifest
        from unit_bfm.v3.interface import export_actor_b,Interface
        torch.set_num_threads(1)
        env=UnitEnv(make_scene(seed=127,scene='E0'))
        try:
            learner=Learner(env.p_dim+MEMORY_DIM)
            with tempfile.TemporaryDirectory() as tmp:
                destination=Path(tmp)/'export'
                export_actor_b(learner,destination,schema_manifest(env))
                self.assertEqual({x.name for x in destination.iterdir()},{'actor.pt','b.pt','manifest.json'})
                runtime=Interface(destination); b=env.reset(); known=env.known
                h=FeatureHistory();h.reset(b,known)
                telemetry={k:v for k,v in b.items() if k not in ('p','diagnostics')}
                runtime.reset(known,telemetry,env.metadata['coordinate_map'])
                z=learner.sample_z(1)
                for t in range(24):
                    f=h.features()
                    with torch.no_grad():
                        expected=float(learner.net.actor(torch.tensor(f['x'])[None],z)[0,0])
                        expected_b=learner.net.b(torch.tensor(f['g'])[None]).numpy()[0]
                    self.assertAlmostEqual(runtime.act(z.numpy()[0]),expected,places=7)
                    np.testing.assert_allclose(runtime.feedback()['B16'],expected_b,atol=1e-7)
                    b=env.step(expected);known=env.known;h.append(b,known)
                    runtime.observe({k:v for k,v in b.items() if k not in ('p','diagnostics')},known)
        finally: env.close()

if __name__=='__main__':unittest.main()
