"""Coordinator regressions for audited retention and failed evaluation paths."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from unit_bfm.v3.replay import Replay
from unit_bfm.v3.tests.test_pipeline_contract import synthetic


class FinalEdges(unittest.TestCase):
    def test_p0_remainder_slots_used(self):
        r=Replay(rule_capacity=10,policy_capacity=10,scene_weights={'E0':1.},expected_configs={'E0':['a','b','c']})
        for cid in ('a','b','c'):
            ep=synthetic(cid,16);ep.config_id=cid;r.add(ep,p0=True)
        r.add(synthetic('rolling',10));r.add(synthetic('policy',10,source='policy'))
        self.assertEqual(r.memory_report()['p0_retained'],5)
        self.assertEqual(len(r),20)
        s=r.state_dict()
        for k,v in s['arrays'].items():self.assertEqual(v.data_ptr(),r.arrays[k].ctypes.data)
        clone=Replay();clone.load_state_dict(copy.deepcopy(s))
        self.assertEqual(r.sample(64)['audit']['ids'],clone.sample(64)['audit']['ids'])

    def test_substep_failure_evaluation_saved_without_history_append(self):
        from unit_bfm.v3.evaluate import evaluate
        from unit_bfm.v3.physics import UnitEnv
        from unit_bfm.v3.interface import Interface
        root=Path(__file__).resolve().parents[1]/'runs'/'coordinator_mixed_01'
        if not (root/'export').exists():self.skipTest('coordinator frozen export unavailable')
        spec=json.loads((root/'evaluation_spec.json').read_text())
        original=UnitEnv.step;observe=Interface.observe;calls=[0]
        def fail(env,u):
            calls[0]+=1
            if calls[0]==2:
                env._physics_tick+=3;env.data.time=env.process_time
                env._fail({'invalid_reasons':['injected_substep_failure']})
            return original(env,u)
        def track(runtime,b,known=None):
            self.assertTrue(b['valid'],'invalid substep boundary fed to history')
            return observe(runtime,b,known)
        parent=Path(tempfile.mkdtemp(prefix='eval_failure_',dir=root.parent))
        with patch.object(UnitEnv,'step',fail),patch.object(Interface,'observe',track):
            result=evaluate(root/'export',root/'query_pool.npz',spec,parent/'evaluation')
        case=result['results'][0]
        self.assertEqual(case['classification'],'numerical_failure')
        self.assertFalse(case['metrics'][0]['success'])
        self.assertTrue((parent/'evaluation'/'report.json').exists())


if __name__=='__main__':unittest.main()
