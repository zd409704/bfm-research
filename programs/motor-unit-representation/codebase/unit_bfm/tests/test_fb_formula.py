"""An independent scalar-loop oracle checks both losses and gradients."""
import unittest
import torch
from unit_bfm.fb_loss import fb_loss,actor_loss
from unit_bfm.networks import physical_result


class Formula(unittest.TestCase):
    def test_density_and_orthogonal_value_and_gradients(self):
        torch.manual_seed(10)
        n,d=5,3
        f=torch.randn(2,n,d,dtype=torch.double,requires_grad=True)
        b=torch.randn(n,d,dtype=torch.double,requires_grad=True)
        target=torch.randn(n,n,dtype=torch.double,requires_grad=True)
        actual=fb_loss(f,b,target)[0]
        expected=torch.zeros((),dtype=torch.double)
        for head in range(2):
            for i in range(n):
                for j in range(n):
                    error=(f[head,i]*b[j]).sum()-.99*target[i,j].detach()
                    expected=expected+(.5*error.square()/(n*(n-1)) if i!=j else -error/n)
        for i in range(n):
            expected=expected-(b[i]*b[i]).sum()/n
            for j in range(n):
                if i!=j: expected=expected+.5*(b[i]*b[j]).sum().square()/(n*(n-1))
        torch.testing.assert_close(actual,expected,atol=1e-12,rtol=1e-12)
        a=torch.autograd.grad(actual,(f,b,target),allow_unused=True)
        e=torch.autograd.grad(expected,(f,b,target),allow_unused=True)
        for av,ev in zip(a[:2],e[:2]): torch.testing.assert_close(av,ev,atol=1e-12,rtol=1e-12)
        self.assertIsNone(a[2])

    def test_actor_min_is_after_dot_product(self):
        f=torch.tensor([[[1.,-3.]], [[-2.,4.]]],requires_grad=True)
        z=torch.tensor([[1.,1.]])
        value=actor_loss(f,z)
        self.assertEqual(float(value),2.)
        value.backward()
        torch.testing.assert_close(f.grad,torch.tensor([[[-1.,-1.]],[[0.,0.]]]))

    def test_result_excludes_command_fields(self):
        y=torch.randn(8,25); altered=y.clone()
        altered[:,13]=100; altered[:,24]=-100
        torch.testing.assert_close(physical_result(y),physical_result(altered),atol=0,rtol=0)
        self.assertEqual(physical_result(y).shape,(8,23))

if __name__=='__main__': unittest.main()
