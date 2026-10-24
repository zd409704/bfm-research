import unittest
import numpy as np
import torch
from unit_bfm.history import History,assemble
from unit_bfm.networks import Networks
from unit_bfm.replay import SequenceReplay
from unit_bfm.tasks import rewards,reward_features,reward_weights,sample_tasks


class Contracts(unittest.TestCase):
    def test_network_counts_and_feedback_independence(self):
        n=Networks()
        self.assertEqual(n.counts(),dict(actor=309505,f1=313616,f2=313616,b=76560,online=1013297,execution=386065))
        self.assertEqual(len({id(p) for p in n.parameters()}),len(list(n.parameters())))
        x=torch.randn(3,336)
        self.assertEqual(n.actor(x,torch.randn(3,16)).shape,(3,1))
        self.assertEqual(n.actor.context(x).shape,(3,128))
        torch.testing.assert_close(n.b(torch.randn(3,23)).norm(dim=-1),torch.full((3,),4.))

    def test_live_replay_equivalence_including_odd_phase(self):
        h=History(2,'cpu'); m=torch.randn(2,28); o=torch.randn(2,24)
        h.reset(o)
        replay=SequenceReplay(1000,50,'cpu'); replay.begin(o,m,0)
        for n in range(1,42):
            o=torch.randn(2,24); o[:,14:16]=(torch.rand(2,2)>.5).float()
            h.append(o); replay.append(o)
            t=torch.full((2,),n)
            indices=(t[:,None]+torch.arange(-21,1)).clamp_min(0)
            raw=replay.raw[torch.arange(2)[:,None],indices]
            raw*=((t[:,None]+torch.arange(-21,1))>=0)[...,None]
            torch.testing.assert_close(h.input(m),assemble(raw,t,m))
            x=h.input(m)
            slow=x[:,52:312].reshape(2,10,26)
            if n>=2:
                self.assertAlmostEqual(float(slow[0,-1,-1]),.05 if n%2 else 0.)
        x,u,xp,y=replay.sample(30,[1,0,0,0])
        torch.testing.assert_close(xp[:,:24],y[:,:24])
        torch.testing.assert_close(u,y[:,13:14])
        torch.testing.assert_close(y[:,24:25],u-x[:,13:14])
        h.reset(o)
        self.assertTrue((h.input(m)[:,52:312].reshape(2,10,26)[:,:,24]==1).all())

    def test_interval_summary_not_subsample(self):
        h=History(1,'cpu'); m=torch.zeros(1,28); h.reset(torch.zeros(1,24))
        a=torch.zeros(1,24); a[:,14]=1; a[:,18]=2; a[:,13]=1
        b=torch.zeros(1,24); b[:,18]=4; b[:,13]=-1; b[:,0]=.7
        h.append(a); h.append(b)
        slow=h.input(m)[:,52:312].reshape(1,10,26)[0,-1]
        self.assertEqual(float(slow[14]),1); self.assertEqual(float(slow[18]),3)
        self.assertEqual(float(slow[13]),0); self.assertAlmostEqual(float(slow[0]),.7)

    def test_reward_basis_exact(self):
        y=torch.randn(500,25); a=torch.tensor(sample_tasks(np.random.default_rng(5),100))
        direct=rewards(y,a); fast=reward_features(y)@reward_weights(a).T
        torch.testing.assert_close(direct,fast,atol=2e-4,rtol=2e-5)

if __name__=='__main__': unittest.main()
