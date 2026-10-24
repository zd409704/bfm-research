import unittest
import torch
from unit_bfm.learner import Learner


class LearningContracts(unittest.TestCase):
    def test_fixed_z_target_and_optimizer_ownership(self):
        torch.set_num_threads(1); torch.manual_seed(2)
        reference=torch.randn(8192,25)*.2
        learner=Learner(reference,device='cpu')
        seen=[]
        hooks=[learner.net.actor.register_forward_pre_hook(lambda _,args:seen.append(args[1].clone())),
               learner.target['f1'].register_forward_pre_hook(lambda _,args:seen.append(args[2].clone())),
               learner.target['f2'].register_forward_pre_hook(lambda _,args:seen.append(args[2].clone()))]
        batch=(torch.randn(16,336),torch.rand(16,1),torch.randn(16,336),torch.randn(16,25)*.2)
        actor_before=[p.detach().clone() for p in learner.net.actor.parameters()]
        metrics=learner.update(batch)
        self.assertTrue(torch.isfinite(metrics).all())
        self.assertEqual(len(seen),4)
        torch.testing.assert_close(seen[0],seen[1],rtol=0,atol=0)
        torch.testing.assert_close(seen[0],seen[2],rtol=0,atol=0)
        self.assertTrue(any(not torch.equal(a,b) for a,b in zip(actor_before,learner.net.actor.parameters())))
        self.assertTrue(all(p.grad is None and not p.requires_grad for p in learner.target.parameters()))
        actor_ids={id(p) for group in learner.actor_opt.param_groups for p in group['params']}
        critic_ids={id(p) for opt in (learner.forward_opt,learner.backward_opt) for group in opt.param_groups for p in group['params']}
        self.assertFalse(actor_ids&critic_ids)
        self.assertEqual(actor_ids|critic_ids,{id(p) for p in learner.net.parameters()})
        for h in hooks: h.remove()


if __name__=='__main__': unittest.main()
