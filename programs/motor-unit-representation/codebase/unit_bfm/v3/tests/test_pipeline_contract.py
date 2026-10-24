"""Pipeline contract tests, including exact row probabilities and honest coverage."""
import copy
import tempfile
import unittest
from pathlib import Path
import numpy as np
import torch
from unit_bfm.v3.replay import Episode,Replay,EmptyReplayGroup
from unit_bfm.v3.programs import CallScheduler,RuleProgram
from unit_bfm.v3.coverage import Coverage
from unit_bfm.v3.queries import Query,QueryPool
from unit_bfm.v3.train import safe_run_directory,load_config,V3_ROOT


def synthetic(episode_id,n,source='rule',scene='E0',q=0.,length=.3):
    from unit_bfm.v3.features import FeatureHistory
    known={'lengths':np.array([length,.3]),'limits':np.array([-2.,2.]),'rigid':np.array([.6,0,.15,.01,.6,0,-.15,.01]),
           'rigid_valid':np.ones(8),'drive':np.array([7.5,-6,6,.01,.005,.03,.02,.003]),'drive_valid':np.ones(8)}
    raw=[];fs=[];h=FeatureHistory()
    for t in range(n+1):
        b={'time':t*.01,'q':q,'dq':0.,'tau_endpoint':0.,'u_previous':0.,'tau_integral':0.,'u_integral':0.,
           'interval_dt':.01 if t else 0.,'interval_valid':bool(t),'p':np.array([float(t)]),
           'terminated':False,'truncated':t==n,'valid':True,'diagnostics':{}}
        raw.append(b)
        if t:h.append(b,known)
        else:h.reset(b,known)
        fs.append(h.features())
    return Episode(episode_id,source,scene,'same',np.array([f['x'] for f in fs]),np.array([f['g'] for f in fs]),
        np.array([np.r_[r['p'],f['memory']] for r,f in zip(raw,fs)]),np.zeros((n,1)),np.full((n,1),.99),
        np.full(n,'main'),raw,[copy.deepcopy(known) for _ in raw]).validate()

class PipelineContract(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def test_reconstruct_disk_complete_truncation(self):
        e=synthetic('a',12);e.save(self.root);restored=Episode.load(e.path)
        for k,v in restored.reconstruct().items():np.testing.assert_allclose(v,getattr(e,k),atol=1e-6)
        self.assertEqual(restored.discount[-1,0],.99)
        e.raw[-1]['truncated']=False
        with self.assertRaises(ValueError):e.validate()
    def test_transition_uniform_not_episode_uniform(self):
        r=Replay(self.root,seed=1,scene_weights={'E0':1.},strict=False)
        r.add(synthetic('short',1));r.add(synthetic('long',9))
        rows,prob,_,_=r._draw(12000)
        self.assertLess(abs(np.mean([r.tags[int(i)][4]=='short' for i in rows])-.1),.015)
        np.testing.assert_allclose(prob,.1)
    def test_probability_sums_all_family_paths(self):
        r=Replay(self.root,scene_weights={'E0':1.},strict=False)
        r.add(synthetic('a',1,q=-1.9));r.add(synthetic('b',9,q=0))
        rows,prob,_,_=r._draw(1000)
        for i,p in zip(rows,prob):
            self.assertAlmostEqual(p,.4*.5+.6*.1 if r.tags[int(i)][4]=='a' else .4*.5/9+.6*.1)
    def test_goals_independent_matching_and_p_pair(self):
        r=Replay(self.root,seed=15,scene_weights={'E0':1.},strict=True)
        r.add(synthetic('r',12));r.add(synthetic('p',12,source='policy'));r.add(synthetic('other',12,source='policy',length=.4))
        b=r.sample(100)
        self.assertTrue(torch.all(b['p_next'][:,0]-b['p'][:,0]==1))
        self.assertTrue(torch.all(b['goal_valid']))
        np.testing.assert_allclose(b['goal_g'][:,[0,1,5,6]],b['x'][:,[0,1,5,6]])
        self.assertGreater(r.audit['gradient_rule_E0'],0);self.assertGreater(r.audit['gradient_policy_E0'],0)
    def test_empty_group_formal_raises_diagnostic_records(self):
        r=Replay(self.root,strict=True);r.add(synthetic('r',5))
        with self.assertRaises(EmptyReplayGroup):r.sample(8)
        r.strict=False;d=r.distribution();self.assertTrue(d['empty_groups']);self.assertTrue(d['empty_bins']);self.assertTrue(d['fallback'])
    def test_resume_sampler_exact(self):
        r=Replay(self.root,seed=3,scene_weights={'E0':1.},strict=False);r.add(synthetic('r',12));state=r.state_dict()
        before=r.sample(30);other=Replay(self.root/'other');other.load_state_dict(state);after=other.sample(30)
        for key in ('x','u','p','goal_g','goal_valid'):torch.testing.assert_close(before[key],after[key])
        self.assertEqual(before['audit']['ids'],after['audit']['ids'])
    def test_invalid_raw_cannot_be_reenabled(self):
        e=synthetic('invalid',12);e.raw[3]['valid']=False;e.valid=np.ones(12,dtype=bool)
        with self.assertRaisesRegex(ValueError,'invalid raw'):e.validate()
        e.valid=None;e.validate();self.assertFalse(e.valid[2]);self.assertFalse(e.valid[3])

    def test_call_time_80_20(self):
        s=CallScheduler(123)
        for _ in range(20000):
            if s.remaining==0:s.begin()
            s.step()
        ratio=s.time.steps['short']/sum(s.time.steps.values());self.assertLess(abs(ratio-.2),.01)
    def test_real_tau_scale(self):
        e=synthetic('r',12);p=RuleProgram(e.known[0]);p.category='transient';p.mode='torque';p.tau_ref=3.;p.remaining=4
        u,_,info=p.action(e.raw[0]);self.assertAlmostEqual(u,3/7.5);self.assertEqual(info['tau_ref'],3.)
    def test_no_false_coverage(self):
        c=Coverage({'groups':[{'scene':'E0','config_id':'same','feasible_xi':[5]}]});c.add(synthetic('r',30))
        self.assertFalse(c.report(formal=True)['coverage_ready']);self.assertTrue(c.report()['deficits'])
    def test_query_rho_and_mask(self):
        r=Replay(self.root,scene_weights={'E0':1.},strict=False);r.add(synthetic('r',12));pool=QueryPool.from_replay(r,20)
        pool.assert_current(r);r.add(synthetic('s',12))
        with self.assertRaises(ValueError):pool.assert_current(r)
        g=np.zeros((2,13));g[1,12]=1
        np.testing.assert_array_equal(Query('ddq',0,1).score(g),[0,1])
    def test_safe_output_and_configs(self):
        with self.assertRaises(ValueError):safe_run_directory(self.root/'V2')
        for mode in ['full','smoke']:self.assertEqual(load_config(V3_ROOT/'configs'/f'{mode}.json')['mode'],mode)

if __name__=='__main__':unittest.main()
