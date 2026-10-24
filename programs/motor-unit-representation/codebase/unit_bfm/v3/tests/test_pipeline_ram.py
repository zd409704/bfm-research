import copy
import tempfile
import time
import unittest
from unittest.mock import patch
import numpy as np
import torch
from unit_bfm.v3.replay import Replay,EmptyReplayGroup
from unit_bfm.v3.tests.test_pipeline_contract import synthetic
from unit_bfm.v3.queries import QueryPool

class RamReplayTests(unittest.TestCase):
    def test_capacity_eviction_no_disk_and_resume(self):
        r=Replay(rule_capacity=32,policy_capacity=64,scene_weights={'E0':1.})
        for i in range(120):
            e=synthetic(f'e{i}',12,source='rule' if i%2 else 'policy')
            with patch.object(e,'save',side_effect=AssertionError('disk write')):r.add(e,p0=i<4)
        self.assertEqual(len(r),96);self.assertEqual(r.counts,{'rule':32,'policy':64})
        self.assertFalse(hasattr(r,'episodes'));self.assertLessEqual(len(r.tags.occupied),96)
        with patch('builtins.open',side_effect=AssertionError('disk sample')),patch('numpy.load',side_effect=AssertionError('disk load')):
            b=r.sample(512)
        self.assertTrue(all(int(eid[1:])>=108 or int(eid[1:])<4 for eid,t in b['audit']['ids']))
        s=copy.deepcopy(r.state_dict());other=Replay();other.load_state_dict(s)
        a=r.sample(50);b=other.sample(50)
        self.assertEqual(a['audit']['ids'],b['audit']['ids'])
        for k in ('x','p','p_next','goal_g','goal_valid'):torch.testing.assert_close(a[k],b[k],rtol=0,atol=0)
        self.assertEqual(r.memory_report()['raw_resident'],0)
    def test_exact_marginal_probability(self):
        r=Replay(rule_capacity=32,policy_capacity=32,scene_weights={'E0':1.})
        r.add(synthetic('short',1,q=-1.9));r.add(synthetic('long',9,q=0))
        slots,prob,_,_=r._draw(1000)
        for slot,p in zip(slots,prob):
            self.assertAlmostEqual(p,.4*.5+.6*.1 if r.tags[int(slot)][4]=='short' else .4*.5/9+.6*.1)
    def test_resume_preserves_group_and_bin_order(self):
        r=Replay(rule_capacity=24,policy_capacity=24,scene_weights={'E0':1.})
        for i in range(20):
            e=synthetic(str(i),8,source='rule' if i%2 else 'policy',q=(-1.7 if i%3 else .8));e.config_id='a' if i%4 else 'b';r.add(e,p0=i<2)
        other=Replay();other.load_state_dict(copy.deepcopy(r.state_dict()))
        self.assertEqual(r.sample(128)['audit']['ids'],other.sample(128)['audit']['ids'])

    def test_strict_partial_and_rho_identity(self):
        a=Replay(rule_capacity=32,policy_capacity=32,scene_weights={'E0':1.},expected_configs={'E0':['same','missing']},strict=True)
        a.add(synthetic('rule',12));a.add(synthetic('policy',12,source='policy'))
        with self.assertRaises(EmptyReplayGroup):a.sample(8)
        a.strict=False;self.assertEqual(a.distribution()['distribution_status'],'partial')
        pool=QueryPool.from_replay(a,16)
        b=Replay(rule_capacity=32,policy_capacity=32,scene_weights={'E0':1.},expected_configs={'E0':['same','missing']})
        b.add(synthetic('rule',12));b.add(synthetic('policy',12,source='policy'))
        with self.assertRaises(ValueError):pool.assert_current(b)
    def test_p0_all_groups_reservoir_protected(self):
        configs=[f'c{i}' for i in range(8)]
        r=Replay(rule_capacity=32,policy_capacity=32,scene_weights={'E0':1.},expected_configs={'E0':configs})
        for i,cid in enumerate(configs):
            e=synthetic(f'p0_{i}',20);e.config_id=cid;r.add(e,p0=True)
        for i in range(30):r.add(synthetic(f'rolling_{i}',12))
        retained=[r.tags[int(s)][0][2] for s in np.flatnonzero(r.active&r.p0_mask)]
        self.assertEqual(set(retained),set(configs));self.assertEqual(len(retained),16)

    def test_memory_limit_actual_p(self):
        with self.assertRaises(MemoryError):Replay(rule_capacity=32768,policy_capacity=65536,p_dim=6000)
    def test_invalid_and_matched_goals(self):
        r=Replay(rule_capacity=32,policy_capacity=32,scene_weights={'E0':1.})
        e=synthetic('r',12);e.raw[3]['valid']=False;e.valid=None;r.add(e)
        r.add(synthetic('p',12,source='policy',length=.4))
        b=r.sample(200)
        self.assertNotIn(('r',2),b['audit']['ids']);self.assertNotIn(('r',3),b['audit']['ids'])
        np.testing.assert_allclose(b['goal_g'][:,[0,1,5,6]],b['x'][:,[0,1,5,6]])
if __name__=='__main__':unittest.main()
