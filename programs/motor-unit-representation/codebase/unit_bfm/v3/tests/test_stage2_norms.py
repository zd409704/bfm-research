"""Stage-2 norms on the V3 learner path. No physics backend required."""
import unittest

import torch

from unit_bfm.v3.learner import Learner
from unit_bfm.v3.stage2_norms import (
    demand_label,
    nondim_v3_g,
    philox_digest,
    sanitize_privileged_tensor,
)


def _batch(n=4, p_dim=8):
    g = torch.Generator().manual_seed(3)
    b = {k: torch.randn(n, d, generator=g) for k, d in
         [("x", 137), ("p", p_dim), ("u", 1), ("x_next", 137), ("p_next", p_dim),
          ("g_next", 13), ("goal_g", 13)]}
    b["u"] = b["u"].tanh()
    b["discount"] = torch.full((n, 1), 0.99)
    b["goal_valid"] = torch.ones(n)
    b["goal_g"][:, [0, 1, 5, 6]] = b["x"][:, [0, 1, 5, 6]]
    return b


class Stage2NormTests(unittest.TestCase):
    def test_distinct_release_keys_and_demand_labels(self):
        self.assertNotEqual(
            philox_digest(1, 3, "E4", 0, 0, "E4-R"),
            philox_digest(1, 3, "E4", 0, 0, "E4-RI"),
        )
        self.assertEqual(demand_label(0.5), "IN")
        self.assertEqual(demand_label(0.8), "EDGE")
        self.assertEqual(demand_label(0.95), "OUT")

    def test_sanitizer_replaces_future_slice_before_forward(self):
        learner = Learner(8, seed=4, config={"action_std": 0.0})
        b = _batch()
        b["p"][:, 4:6] = 9.0
        b["p"][:, 2:4] = 1.0
        b["p_next"][:, 4:6] = 8.0
        b["p_next"][:, 2:4] = 0.5
        b["future_slice"] = (4, 6)
        b["lag_slice"] = (2, 4)
        seen = {}

        def hook(_module, args):
            y = args[0]
            seen["p"] = y[:, 137:145].detach().clone()

        handle = learner.net.f1.register_forward_pre_hook(hook)
        try:
            metrics = learner.update(b)
        finally:
            handle.remove()
        self.assertEqual(learner.sanitize_calls, 1)
        self.assertTrue(learner.last_sanitize["applied"])
        self.assertEqual(learner.last_sanitize["consumed_violations"], 0)
        self.assertTrue(torch.allclose(seen["p"][:, 4:6], seen["p"][:, 2:4]))
        self.assertTrue(metrics["fb"] == metrics["fb"])
        self.assertGreater(metrics["actor_grad"], 0.0)

    def test_v3_tip_nondim_keeps_rank16_sphere(self):
        g = torch.randn(6, 13)
        g[:, 1] = 0.4
        out = nondim_v3_g(g)
        self.assertEqual(tuple(out.shape), (6, 13))
        learner = Learner(4, seed=9)
        z = learner.net.b(g)
        self.assertTrue(torch.allclose(z.norm(dim=-1), torch.full((6,), 4.0), atol=1e-5))


if __name__ == "__main__":
    unittest.main()
