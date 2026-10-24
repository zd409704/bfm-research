import tempfile
import unittest
from pathlib import Path
import torch
from unit_bfm import VERSION
from unit_bfm.networks import Networks,physical_result
from unit_bfm.interface import FrozenUnit


class Interface(unittest.TestCase):
    def test_frozen_live_feedback_and_reset(self):
        torch.manual_seed(7); network=Networks()
        state=dict(version=VERSION,actor=network.actor.state_dict(),b=network.b.state_dict(),reward_cross=torch.eye(16))
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'unit.pt'; torch.save(state,path)
            unit=FrozenUnit(path,nworld=2)
            o=torch.randn(2,24); m=torch.randn(2,28); z=torch.zeros(2,16); z[:,0]=4
            unit.reset(o,m)
            self.assertTrue((unit.feedback()[:,-1]==0).all())
            next_o=torch.randn(2,24)
            unit.observe(next_o)
            self.assertEqual(unit.feedback().shape,(2,197))
            self.assertTrue((unit.feedback()[:,-1]==1).all())
            torch.testing.assert_close(unit.result,network.b(physical_result(next_o)))
            torch.testing.assert_close(unit.act(z),network.actor(unit.x,z))
            unit.reset(next_o,m)
            self.assertTrue((unit.result==0).all())
            self.assertTrue((unit.history.n==0).all())


if __name__=='__main__': unittest.main()
