"""Physical snapshot reset keeps dynamics/process, resets only feature history."""
import unittest
import numpy as np
from unit_bfm.v3.physics import UnitEnv,make_scene
from unit_bfm.v3.features import FeatureHistory

class SnapshotIntegration(unittest.TestCase):
    def test_snapshot_preserves_next_response_but_pads_history(self):
        for side in ('P','D'):
            c=make_scene(seed=92,scene='E1',fixed_side=side,load_start=.01,load_end=.15,
                         initial_q=.1,initial_dq=.1,duration=.5)
            e=UnitEnv(c)
            try:
                for _ in range(8):e.step(.04)
                snapshot=e.snapshot();a=e.step(-.07)
                restored=e.restore(snapshot,episode_id=99)
                self.assertAlmostEqual(restored['time'],.08,places=8)
                self.assertFalse(restored['interval_valid'])
                self.assertEqual(restored['tau_integral'],0.)
                h=FeatureHistory();h.reset(restored,e.known)
                self.assertEqual(h.features()['g'][12],0.)
                b=e.step(-.07);h.append(b,e.known)
                for k in ('q','dq','tau_endpoint','tau_integral'):
                    self.assertAlmostEqual(a[k],b[k],places=8,msg=k)
                np.testing.assert_allclose(a['p'],b['p'],atol=2e-6,rtol=2e-6)
                self.assertFalse(b['truncated'])
            finally:e.close()

if __name__=='__main__':unittest.main()
