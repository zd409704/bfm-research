import copy
import unittest
import numpy as np
import torch
from torch import nn
from unit_bfm.v3.fb_loss import fb_loss, actor_loss
from unit_bfm.v3.networks import Networks, orthogonal_init
from unit_bfm.v3.learner import Learner, frozen_forward
from unit_bfm.v3.schema import VERSION, MEMORY_DIM

torch.set_num_threads(1)


def batch(n=8,p_dim=MEMORY_DIM+3):
    r=torch.Generator().manual_seed(87)
    b={k:torch.randn(n,d,generator=r) for k,d in
       [('x',137),('p',p_dim),('u',1),('x_next',137),('p_next',p_dim),('g_next',13),('goal_g',13)]}
    b['u']=b['u'].tanh()
    b['discount']=torch.full((n,1),.99); b['discount'][0]=0
    b['goal_valid']=torch.ones(n,dtype=torch.bool)
    b['goal_g'][:,[0,1,5,6]]=b['x'][:,[0,1,5,6]]
    return b


class LossTests(unittest.TestCase):
    def test_independent_scalar_formula_and_gradients(self):
        torch.manual_seed(12)
        f=torch.randn(2,4,3,dtype=torch.float64,requires_grad=True)
        b=torch.randn(4,3,dtype=torch.float64,requires_grad=True)
        target=torch.randn(4,4,dtype=torch.float64,requires_grad=True)
        d=torch.tensor([[0.],[.99],[.3],[.99]],dtype=torch.float64,requires_grad=True)
        got=fb_loss(f,b,target,d)
        off=0.; pos=0.; orth=0.
        for i in range(4):
            for j in range(4):
                for k in range(2):
                    delta=sum(f[k,i,l]*b[j,l] for l in range(3))-d[i,0].detach()*target[i,j].detach()
                    if i!=j: off=off+delta**2/(2*4*3)
                    else: pos=pos-delta/4
                gram=sum(b[i,l]*b[j,l] for l in range(3))
                if i!=j: orth=orth+gram**2/(2*4*3)
                else: orth=orth-gram/4
        expected=(off+pos+orth,off,pos,orth)
        for v,w in zip(got,expected): torch.testing.assert_close(v,w)
        for v,w in zip(torch.autograd.grad(got[0],(f,b),retain_graph=True),torch.autograd.grad(expected[0],(f,b))):
            torch.testing.assert_close(v,w)
        got[0].backward()
        self.assertIsNone(target.grad); self.assertIsNone(d.grad)
        with self.assertRaises(ValueError): fb_loss(f,b,target,d[:,0])
        # Row zero is terminal; changing that target row has no effect, unlike a reference-column mask.
        changed=target.detach().clone(); changed[0]+=1000
        torch.testing.assert_close(fb_loss(f,b,changed,d)[0],got[0])

    def test_actor_min_after_dot_not_vector_min(self):
        f=torch.tensor([[[10.,0.]],[[0.,10.]]]); z=torch.tensor([[1.,1.]])
        self.assertEqual(float(actor_loss(f,z)),-10.)


class NetworkTests(unittest.TestCase):
    def test_counts_sphere_gain_and_input_isolation(self):
        net=Networks(7); net.apply(orthogonal_init)
        c=net.counts()
        self.assertEqual(c['actor'],207617); self.assertEqual(c['b'],74000)
        self.assertEqual(c['f1'],211728+512*7); self.assertEqual(c['online'],705073+1024*7)
        self.assertEqual(c['execution'],281617)
        x=torch.randn(3,137); p=torch.randn(3,7); u=torch.randn(3,1); z=torch.randn(3,16); g=torch.randn(3,13)
        a=net.actor(x,z); b=net.b(g)
        torch.testing.assert_close(b.norm(dim=-1),torch.full((3,),4.))
        f=net.f1(torch.cat((x,p),-1),u,z)
        p+=2
        torch.testing.assert_close(a,net.actor(x,z),rtol=0,atol=0)
        torch.testing.assert_close(b,net.b(g),rtol=0,atol=0)
        self.assertFalse(torch.allclose(f,net.f1(torch.cat((x,p),-1),u,z)))
        for m in net.modules():
            if isinstance(m,nn.Linear):
                w=m.weight.detach(); gram=w.T@w if w.shape[0]>=w.shape[1] else w@w.T
                torch.testing.assert_close(gram,torch.eye(len(gram)),atol=2e-6,rtol=2e-6)
                torch.testing.assert_close(m.bias,torch.zeros_like(m.bias))

    def test_frozen_f_preserves_action_gradient_and_restores_flags(self):
        net=Networks(2)
        x=torch.randn(4,137); p=torch.randn(4,2); z=torch.randn(4,16)
        y=torch.cat((x,p),-1)
        with frozen_forward(net):
            u=net.actor(x,z); u.retain_grad()
            loss=actor_loss(torch.stack((net.f1(y,u,z),net.f2(y,u,z))),z)
            loss.backward()
            self.assertGreater(float(u.grad.abs().sum()),0)
            self.assertTrue(all(q.grad is None for q in net.f1.parameters()))
            self.assertTrue(all(q.grad is None for q in net.f2.parameters()))
            self.assertGreater(float(sum(q.grad.abs().sum() for q in net.actor.parameters())),0)
        self.assertTrue(all(q.requires_grad for q in net.f1.parameters()))
        with self.assertRaises(RuntimeError):
            with frozen_forward(net): raise RuntimeError('test restoration')
        self.assertTrue(all(q.requires_grad for q in net.f2.parameters()))


class LearnerTests(unittest.TestCase):
    def test_target_mean_detached_and_p_next_used(self):
        learner=Learner(3,config={'action_std':0.})
        x=torch.randn(4,137,requires_grad=True); p=torch.randn(4,3,requires_grad=True)
        g=torch.randn(4,13,requires_grad=True); z=torch.randn(4,16,requires_grad=True)
        actual=learner.target_density(x,p,g,z)
        with torch.no_grad():
            u=learner.net.actor(x,z).clamp(-1+1e-6,1-1e-6); y=torch.cat((x,p),-1)
            b=learner.target['b'](g)
            expected=(learner.target['f1'](y,u,z)@b.T+learner.target['f2'](y,u,z)@b.T)/2
        torch.testing.assert_close(actual,expected)
        self.assertFalse(actual.requires_grad)
        self.assertFalse(torch.allclose(actual,learner.target_density(x,p+10,g,z)))
        self.assertTrue(all(not q.requires_grad for q in learner.target.parameters()))

    def test_independent_z_matching_no_shuffle_and_invalid_fallback(self):
        learner=Learner(2,seed=13)
        goals=torch.randn(512,13,requires_grad=True)
        encoded=learner.net.b(goals).detach()
        z=learner.sample_z(512,goals,torch.ones(512))
        equal=torch.isclose(z,encoded,atol=1e-6).all(-1)
        self.assertGreater(int(equal.sum()),190); self.assertLess(int(equal.sum()),320)
        self.assertFalse(z.requires_grad)
        torch.testing.assert_close(z.norm(dim=-1),torch.full((512,),4.))
        # Zero valid rows must not touch B (not even an empty batch).
        hook=learner.net.b.register_forward_pre_hook(lambda *args: (_ for _ in ()).throw(AssertionError('B called for invalid goals')))
        try: learner.sample_z(8,torch.zeros(8,13),torch.zeros(8))
        finally: hook.remove()
        self.assertEqual(learner.last_goal_fraction,0)
        b=batch(p_dim=2); b['goal_g'][0,0]+=1
        with self.assertRaisesRegex(ValueError,'geometry'): learner.update(b)
        del b['goal_g']
        with self.assertRaises(KeyError): learner.update(b)

    def test_update_inputs_detached_actor_privileged_isolation_and_resume(self):
        pd=MEMORY_DIM+3
        learner=Learner(pd,seed=31)
        b=batch(p_dim=pd)
        for k in b:
            if b[k].dtype.is_floating_point: b[k].requires_grad_()
        actor_inputs=[]
        hook=learner.net.actor.register_forward_pre_hook(lambda module,args: actor_inputs.append(args[0].detach().clone()))
        before={k:v.clone() for k,v in learner.net.state_dict().items()}
        metrics=learner.update(b); hook.remove()
        self.assertTrue(all(np.isfinite(v) for v in metrics.values()))
        self.assertGreater(metrics['actor_grad'],0); self.assertGreater(metrics['f_grad'],0); self.assertGreater(metrics['b_grad'],0)
        self.assertEqual(len(actor_inputs),2)
        torch.testing.assert_close(actor_inputs[0],b['x_next']); torch.testing.assert_close(actor_inputs[1],b['x'])
        self.assertTrue(all(v.grad is None for v in b.values()))
        self.assertTrue(all(q.grad is None for q in learner.target.parameters()))
        self.assertTrue(all(q.grad is None for q in learner.f_params))
        for prefix in ('actor','b','f1','f2'):
            self.assertTrue(any(not torch.equal(v,before[k]) for k,v in learner.net.state_dict().items() if k.startswith(prefix+'.')))
        checkpoint=learner.state_dict()
        restored=Learner(pd,seed=999); restored.load_state_dict(checkpoint)
        # Full optimizer and generator restoration must reproduce the next update.
        left=learner.update(b); right=restored.update(b)
        self.assertEqual(left,right)
        for k,v in learner.net.state_dict().items(): torch.testing.assert_close(v,restored.net.state_dict()[k],rtol=0,atol=0)
        bad=copy.deepcopy(checkpoint); bad['version']='V2'
        with self.assertRaisesRegex(ValueError,'version'): restored.load_state_dict(bad)
        bad=copy.deepcopy(checkpoint); bad['schema_hash']='old'
        with self.assertRaisesRegex(ValueError,'schema_hash'): restored.load_state_dict(bad)
        with self.assertRaisesRegex(ValueError,'p_dim'): Learner(pd+1).load_state_dict(checkpoint)
        self.assertEqual(checkpoint['version'],VERSION)

if __name__=='__main__': unittest.main()
