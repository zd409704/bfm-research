"""Integer process clock regressions for GPU debug E0/P k5, tested on CPU."""
import copy
import unittest
import numpy as np
from unit_bfm.v3.physics import UnitEnv,make_scene,event_tick
from unit_bfm.v3.privileged import INDEX
from unit_bfm.v3.warp_backend import WarpBatchEnv,MjlabBatchEnv


class PhysicsClock(unittest.TestCase):
    def test_float32_counterexample_and_integer_event_edges(self):
        accumulated=np.float32(0.)
        for _ in range(60):accumulated+=np.float32(.001)
        self.assertLess(float(accumulated),.06)  # Exact coordinator failure mechanism.
        e=UnitEnv(make_scene(load_start=.02,load_end=.06,load_mode='repeated',load_period=.4,load_repeats=3))
        for tick,expected in ((19,False),(20,True),(59,True),(60,False),(419,False),(420,True),(459,True),(460,False),(820,True),(860,False),(1220,False)):
            e._physics_tick=tick
            for floating_time in (float(np.nextafter(np.float32(tick/1000),np.float32(-np.inf))),float(np.nextafter(np.float32(tick/1000),np.float32(np.inf)))):
                e.data.time=floating_time
                self.assertEqual(e._load_state()[0],expected)
                self.assertEqual(e._boundary(False)['p'][INDEX['controller.load.active']],float(expected))
        self.assertEqual(event_tick(.06),60)
        self.assertEqual(event_tick(.060001),61)
        self.assertEqual(event_tick(1.000001),1001)
        with self.assertRaises(TypeError):e._load_state(.06)

    def test_all_generator_outputs_ignore_float_clock_drift(self):
        for side in ('P','D'):
            e=UnitEnv(make_scene(scene='E4',fixed_side=side,load_start=.02,load_end=.06,load_mode='repeated',load_period=.4,load_repeats=3))
            for tick in (19,20,59,60,61,299,300,359,360,419,420,459,460,461):
                e._physics_tick=tick
                e.data.time=float(np.nextafter(np.float32(tick/1000),np.float32(-np.inf)))
                p0=e._boundary(False)['p'];object0=e._obstacle_reference();support0=e._support_reference(side,e.process_time)
                e.data.time=float(np.nextafter(np.float32(tick/1000),np.float32(np.inf)))
                np.testing.assert_array_equal(p0,e._boundary(False)['p'])
                for a,b in zip(object0,e._obstacle_reference()):np.testing.assert_array_equal(a,b)
                for a,b in zip(support0,e._support_reference(side,e.process_time)):np.testing.assert_array_equal(a,b)

    def test_snapshot_tick_and_restore_at_release(self):
        c=make_scene(scene='E0',load_start=.02,load_end=.06,duration=.1,load_mode='single')
        a,b=UnitEnv(c),UnitEnv(c)
        for _ in range(6):out=a.step(0.)
        self.assertEqual(out['time'],.06);self.assertEqual(a.physics_tick,60)
        self.assertEqual(out['p'][INDEX['controller.load.active']],0.)
        self.assertEqual(a._solve['tick'],59);self.assertEqual(a._solve['time'],.059)
        snapshot=a.snapshot();self.assertEqual(snapshot['physics_tick'],60)
        # The saved float integration clock can be low precision: integer tick wins.
        low_precision=copy.deepcopy(snapshot)
        low_precision['integration_state']=snapshot['integration_state'].copy()
        low_precision['integration_state'][0]=float(np.float32(.06))
        restored=b.restore(low_precision)
        self.assertEqual(restored['time'],.06);self.assertFalse(restored['interval_valid'])
        for _ in range(4):
            x,y=a.step(.1),b.step(.1)
            np.testing.assert_array_equal(x['p'],y['p'])
            self.assertEqual(x['q'],y['q'])
        self.assertTrue(x['truncated']);self.assertFalse(y['truncated'])
        old=copy.deepcopy(snapshot);old['version']=1
        with self.assertRaises(ValueError):b.restore(old)

    def test_real_warp_cpu_clock_pair_and_restore(self):
        # No CUDA used. Warp CPU has the same FP32 Data.time representation.
        for backend in (WarpBatchEnv,MjlabBatchEnv):
            c=make_scene(scene='E0',load_start=.02,load_end=.06,load_mode='single',duration=.2)
            cpu=UnitEnv(c);batch=backend([c],device='cpu')
            for k in range(8):
                a=cpu.step(.1);b=batch.step([.1])[0]
                self.assertEqual(a['time'],b['time'])
                self.assertEqual(cpu.physics_tick,batch.envs[0].physics_tick)
                self.assertEqual(a['p'][INDEX['controller.load.active']],b['p'][INDEX['controller.load.active']])
                self.assertEqual(a['diagnostics']['load_active'],b['diagnostics']['load_active'])
                np.testing.assert_allclose(a['p'],b['p'],rtol=1e-2,atol=2e-3)
            cpu.restore(cpu.snapshot());batch.restore(batch.snapshot())
            a=cpu.step(.1);b=batch.step([.1])[0]
            self.assertEqual(a['time'],b['time']);self.assertEqual(b['diagnostics']['episode_start_tick'],80)
            np.testing.assert_allclose(a['p'],b['p'],rtol=1e-2,atol=2e-3)
            batch.close()

if __name__=='__main__':unittest.main()
