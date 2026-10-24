"""CPU/GPU assertions are runnable on a CUDA-enabled worker, never fake data."""
import unittest
import numpy as np
import torch
from unit_bfm.v3.physics import UnitEnv,make_scene
from unit_bfm.v3.warp_backend import WarpBatchEnv,MjlabBatchEnv


class BackendContract(unittest.TestCase):
    def test_unavailable_cuda_rejected_not_cpu_fallback(self):
        if torch.cuda.is_available():self.skipTest('CUDA accessible; paired tests exercise backend')
        with self.assertRaisesRegex(RuntimeError,'no CPU substitution'):
            WarpBatchEnv([make_scene()])

    def test_explicit_warp_cpu_batch_reference_path(self):
        # Executes the actual Warp kernels on CPU; this is NOT CUDA validation.
        c=make_scene(scene='E4',fixed_side='D',tilt=0.,load_start=0.,load_end=.12,
                     initial_q=.1,load_force=0.,load_couple=0.,support_preload=.5)
        cpu=[UnitEnv(c),UnitEnv(c)]; batch=WarpBatchEnv([c,c],device='cpu')
        for k in range(25):
            actions=[.1,-.1];x=[e.step(u) for e,u in zip(cpu,actions)];y=batch.step(actions)
            for a,b in zip(x,y):
                self.assertTrue(b['valid'])
                np.testing.assert_allclose([a['q'],a['dq'],a['tau_integral']],
                    [b['q'],b['dq'],b['tau_integral']],rtol=2e-3,atol=5e-4)
                self.assertAlmostEqual(a['diagnostics']['contact_force'],b['diagnostics']['contact_force'],delta=.08)
                # Contact slot ordering is backend dependent; compare aggregate wrench.
                from unit_bfm.v3.privileged import INDEX
                keys=[name for name in INDEX if not name.startswith('contact.')]
                indices=[INDEX[name] for name in keys]
                np.testing.assert_allclose(a['p'][indices],b['p'][indices],rtol=5e-3,atol=3e-3)
        self.assertNotEqual(y[0]['q'],y[1]['q'])
        batch.close()
        c=make_scene(tilt=0.)
        cpu=UnitEnv(c);mjlab=MjlabBatchEnv([c],device='cpu')
        a=cpu.step(.1);b=mjlab.step([.1])[0]
        np.testing.assert_allclose(a['p'],b['p'],atol=2e-4,rtol=1e-3)
        mjlab.close()

    @unittest.skipUnless(torch.cuda.is_available(),'CUDA inaccessible; CPU/GPU parity NOT validated')
    def test_cpu_gpu_all_scenes_paired(self):
        for backend in (WarpBatchEnv,MjlabBatchEnv):
            for scene in ('E0','E1','E2','E3','E4'):
                for side in ('P','D'):
                    c=make_scene(scene=scene,fixed_side=side,tilt=0.,load_start=.02,load_end=.06)
                    cpu=[UnitEnv(c),UnitEnv(c)];gpu=backend([c,c])
                    for k in range(10):
                        u=[.2*np.sin(k*.2),-.15];a=[e.step(x) for e,x in zip(cpu,u)];b=gpu.step(u)
                        for x,y in zip(a,b):
                            self.assertTrue(y['valid'])
                            np.testing.assert_allclose([x['q'],x['dq'],x['tau_integral']],[y['q'],y['dq'],y['tau_integral']],rtol=2e-3,atol=3e-4)
                            np.testing.assert_allclose(x['p'],y['p'],rtol=1e-2,atol=2e-3)
                    gpu.close()

if __name__=='__main__':unittest.main()
