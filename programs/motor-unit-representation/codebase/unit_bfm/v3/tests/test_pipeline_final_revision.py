"""Final coordinator rework: independent scene queues, active checkpoint, failures."""
import copy
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
import torch
from unit_bfm.v3.train import (collection_schedulers, choose_collection_group,
                              record_collection_group, CheckpointRetention, load_config, V3_ROOT)
from unit_bfm.v3.replay import Replay
from unit_bfm.v3.collect import collect_batch
from unit_bfm.v3.tests.test_pipeline_contract import synthetic

class FakeBatch:
    def __init__(self,fail_at=1,exception=False):
        ep=synthetic('fixture',4);self.records=ep.raw;self.calls=0;self.fail_at=fail_at;self.exception=exception
        cfg=SimpleNamespace(scene='E0',fixed_side='P',load_start=.1,load_end=.3)
        self.envs=[SimpleNamespace(config=cfg,metadata={}) for _ in range(2)]
        self.known=[ep.known[0],ep.known[0]];self.physics_schema=[];self.metadata={'backend':'fake-contract'}
    def reset(self,episode_id=0):return [copy.deepcopy(self.records[0]) for _ in range(2)]
    def step(self,u):
        self.calls+=1
        out=[copy.deepcopy(self.records[self.calls]) for _ in range(2)]
        for i,b in enumerate(out):b['u_previous']=u[i];b['u_integral']=u[i]*.01
        if self.calls==self.fail_at:
            out[0]['valid']=False;out[0]['diagnostics']={'reason':'injected_invalid'}
            if self.exception:
                exc=RuntimeError('batch failure');exc.boundary=out[0];exc.diagnostics={'world_id':0,'reason':'injected_invalid'};raise exc
        return out

class FinalRevisionTests(unittest.TestCase):
    def test_all_720_scene_config_groups(self):
        c=load_config(V3_ROOT/'configs/full.json');ids=[x['config_id'] for x in c['collection']['structures']]
        sched=collection_schedulers(c['collection']['scene_weights'],ids);seen=set()
        for _ in range(7200):
            scene,cid,_=choose_collection_group(sched);seen.add((scene,cid));record_collection_group(sched,scene,cid,2000)
        self.assertEqual(len(seen),720)
        self.assertEqual({s:sum(sc==s for sc,_ in seen) for s in c['collection']['scene_weights']},{s:144 for s in c['collection']['scene_weights']})
    def test_snapshot_selects_available_group_and_accounts_actual(self):
        sched=collection_schedulers({'E0':.5,'E1':.5},['a','b','c'])
        preferred=choose_collection_group(sched)[:2]
        pool=[{'scene':'E1','config_id':'c','snapshot':{'model_hash':'X'},'config':'exact-compatible-config'}]
        scene,cid,entry=choose_collection_group(sched,pool,True)
        self.assertNotEqual((scene,cid),preferred);self.assertIs(entry,pool[0])
        record_collection_group(sched,scene,cid,40)
        self.assertEqual(sched['scene'].steps['E1'],40);self.assertEqual(sched['config_E1'].steps['c'],40)
        self.assertEqual(sum(sched['config_E0'].steps.values()),0)
    def test_selected_snapshot_really_restores_with_padding(self):
        from unit_bfm.v3.physics import UnitEnv,make_scene
        from unit_bfm.v3.collect import make_batch
        c=make_scene(seed=12,scene='E0',duration=.04,initial_q=0.,initial_dq=0.,load_force=0.)
        env=UnitEnv(c,seed=12)
        try:
            env.reset();env.step(0.);snapshot=env.snapshot()
        finally:env.close()
        sched=collection_schedulers({'E0':1.},['a','b'])
        scene,cid,entry=choose_collection_group(sched,[{'scene':'E0','config_id':'b','config':c,'snapshot':snapshot}],True)
        batch=make_batch([entry['config']]*2,seed=12,backend='cpu')
        try:
            with patch.object(batch,'restore',wraps=batch.restore) as restore:
                eps=collect_batch(batch,['a','b'],['rule','rule'],[12,13],max_steps=2,
                    reset_snapshots=[entry['snapshot']]*2,metadata=[{'scene':scene,'config_id':cid}]*2)
                restore.assert_called_once()
            for ep in eps:
                self.assertTrue(ep.metadata['reset_snapshot_used']);self.assertTrue(ep.metadata['restore']['history_padding'])
                self.assertEqual(ep.raw[0]['time'],snapshot['snapshot_time']);self.assertFalse(ep.raw[0]['interval_valid'])
                self.assertTrue(ep.valid.all());self.assertEqual(ep.config_id,'b')
            record_collection_group(sched,scene,cid,sum(map(len,eps)))
            self.assertEqual(sched['config_E0'].steps['b'],4);self.assertEqual(sched['config_E0'].steps['a'],0)
        finally:batch.close()
    def test_first_invalid_public_diagnostics(self):
        for exception in (False,True):
            with self.subTest(exception=exception):
                result=collect_batch(FakeBatch(exception=exception),['a','b'],['rule','rule'],[1,2],max_steps=3)
                self.assertEqual(result,[])
                d=result.collection_diagnostics
                self.assertEqual(d['failed_worlds'],[0]);self.assertEqual(d['aborted_valid_worlds'],[1])
                self.assertEqual(d['failed_world_count'],1);self.assertEqual(d['attempted_world_intervals'],2)
                self.assertEqual(len(d['failure_examples']),1)
    def test_legal_prefix_retained_peer_not_failed(self):
        result=collect_batch(FakeBatch(fail_at=3),['a','b'],['rule','rule'],[1,2],max_steps=4)
        self.assertEqual([len(e) for e in result],[2,2]);self.assertTrue(all(e.valid.all() for e in result))
        self.assertIn('failed_next_interval',result[0].raw[-1]['diagnostics'])
        self.assertNotIn('failed_next_interval',result[1].raw[-1]['diagnostics'])
        self.assertTrue(result[1].raw[-1]['diagnostics']['aborted_next_interval'])
    def test_undersized_groups_and_no_groups_use_reservoir(self):
        for expected in ({},{'E0':[f'c{i}' for i in range(20)]}):
            r=Replay(rule_capacity=16,policy_capacity=16,scene_weights={'E0':1.},expected_configs=expected,seed=90)
            for i in range(50):
                e=synthetic(f'anchor{i}',8);e.config_id='c'+str(i%5);r.add(e,p0=True)
            self.assertEqual(r.memory_report()['p0_retention_mode'],'global_reservoir')
            self.assertEqual(len(r),8);self.assertTrue(any(int(r.tags[i][4][6:])<40 for i in r.tags.occupied))
            clone=Replay();clone.load_state_dict(copy.deepcopy(r.state_dict()))
            self.assertEqual(r.sample(32)['audit']['ids'],clone.sample(32)['audit']['ids'])
    def test_active_rows_zero_copy_full_partial_compact(self):
        r=Replay(rule_capacity=8,policy_capacity=8,scene_weights={'E0':1.})
        r.add(synthetic('a',2),p0=True);r.add(synthetic('b',3,source='policy'))
        s=r.state_dict();self.assertTrue(all(a.shape[0]==5 for a in s['arrays'].values()))
        self.assertEqual(s['arrays']['p'].untyped_storage().nbytes(),5*r.p_dim*4)
        clone=Replay();clone.load_state_dict(copy.deepcopy(s))
        self.assertEqual(r.sample(10)['audit']['ids'],clone.sample(10)['audit']['ids'])
        r.add(synthetic('a2',8),p0=True);r.add(synthetic('c',8));r.add(synthetic('b2',8,source='policy'))
        s=r.state_dict();self.assertEqual(len(r),16)
        self.assertEqual(s['arrays']['p'].data_ptr(),r.arrays['p'].ctypes.data)
    def test_retention_only_manages_new_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);old=root/'old.pt';old.touch()
            for keep in (False,True):
                folder=root/str(keep);folder.mkdir();manager=CheckpointRetention(keep)
                for name in ('p0','checkpoint_1','checkpoint_2','final'):
                    p=folder/(name+'.pt');p.touch();manager.record(p,'p0' if name=='p0' else 'rolling')
                self.assertEqual({p.name for p in folder.iterdir()},{'checkpoint_2.pt','final.pt'}|({'p0.pt'} if keep else set()))
                self.assertTrue(old.exists())
    def test_train_counts_first_invalid_without_prefix(self):
        # Real train control flow; deterministic fake physics, no optimization or long rollout.
        from unit_bfm.v3.train import run
        cfg=load_config(V3_ROOT/'configs/smoke.json')
        root=Path(tempfile.mkdtemp(prefix='pipeline_first_invalid_',dir=V3_ROOT/'runs'))/'run'
        with patch('unit_bfm.v3.collect.make_batch',side_effect=lambda *a,**k:FakeBatch()),patch.object(FakeBatch,'close',lambda self:None,create=True):
            with self.assertRaisesRegex(RuntimeError,'8 consecutive'):run(cfg,root)
        s=torch.load(root/'no_valid_boundary.pt',weights_only=False)
        self.assertEqual(s['state']['invalid_W'],8);self.assertEqual(s['state']['aborted_valid_W'],8)
        self.assertEqual(s['state']['physical_steps'],16);self.assertEqual(len(s['state']['failure_examples']),8)

if __name__=='__main__':unittest.main()
