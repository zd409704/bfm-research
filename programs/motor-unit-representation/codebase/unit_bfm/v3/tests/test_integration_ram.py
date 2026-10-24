"""Coordinator-owned bounded replay regressions, independent of implementation handoff."""
import copy
import unittest
from unittest.mock import patch
import numpy as np
import torch
from unit_bfm.v3.replay import Replay
from unit_bfm.v3.queries import QueryPool
from unit_bfm.v3.tests.test_pipeline_contract import synthetic


class BoundedReplayIntegration(unittest.TestCase):
    def test_many_overwrites_frozen_anchor_no_io_exact_resume(self):
        r=Replay(rule_capacity=40,policy_capacity=60,scene_weights={'E0':1.},seed=90)
        r.add(synthetic('anchor',20),p0=True)
        anchor={i:tuple(r.tags[i][-2:]) for i in r.tags.occupied if r.p0_mask[i]}
        sizes={k:v.nbytes for k,v in r.arrays.items()}
        for i in range(100):
            ep=synthetic('r'+str(i),8,source='rule' if i%2 else 'policy')
            with patch.object(ep,'save',side_effect=AssertionError('training archives episode')):
                r.add(ep)
        self.assertEqual(len(r),100)
        self.assertEqual(sizes,{k:v.nbytes for k,v in r.arrays.items()})
        self.assertEqual(anchor,{i:tuple(r.tags[i][-2:]) for i in r.tags.occupied if r.p0_mask[i]})
        with patch('builtins.open',side_effect=AssertionError('sampling needs files')):
            batch=r.sample(1000)
        self.assertTrue(all(e=='anchor' or int(e[1:])>=84 for e,t in batch['audit']['ids']))
        saved=copy.deepcopy(r.state_dict()); clone=Replay();clone.load_state_dict(saved)
        a=r.sample(64);b=clone.sample(64)
        self.assertEqual(a['audit']['ids'],b['audit']['ids'])
        for k in ('x','p','u','x_next','p_next','g_next','goal_g','discount'):
            torch.testing.assert_close(a[k],b[k],atol=0,rtol=0)

    def test_checkpoint_contains_only_active_tensor_rows(self):
        r=Replay(rule_capacity=40,policy_capacity=60,scene_weights={'E0':1.})
        r.add(synthetic('a',6),p0=True);r.add(synthetic('b',7,source='policy'))
        state=r.state_dict()
        for k,values in state['arrays'].items():
            self.assertEqual(values.shape[0],len(r),f'{k}: unused capacity serialized')

    def test_p0_retention_not_just_last_episodes(self):
        r=Replay(rule_capacity=80,policy_capacity=40,scene_weights={'E0':1.},seed=90)
        for i in range(50):
            ep=synthetic('anchor'+str(i),8);ep.config_id='c'+str(i%5)
            r.add(ep,p0=True)
        tags=[r.tags[i] for i in r.tags.occupied if r.p0_mask[i]]
        # A reservoir or stratified retention can retain early samples. A FIFO cannot.
        self.assertTrue(any(int(t[4][6:])<40 for t in tags),'P0 is still a last-episodes FIFO')
        self.assertEqual(len(tags),40)

    def test_query_identity_includes_actual_replay(self):
        a=Replay(rule_capacity=20,policy_capacity=20,scene_weights={'E0':1.})
        b=Replay(rule_capacity=20,policy_capacity=20,scene_weights={'E0':1.})
        a.add(synthetic('same',8,q=.1));b.add(synthetic('same',8,q=.9))
        pool=QueryPool.from_replay(a,20)
        with self.assertRaises(ValueError):pool.assert_current(b)


if __name__=='__main__':unittest.main()
