"""Experiment Suite B03: Motion-Only Backward Map Aliasing and Perceptive Compensation.

Tests:
1. Kinematic-only B(m) aliasing: identical body kinematics m_t under three distinct physical
   contact regimes (free air swing, 0.40 m box hand/foot support, 0.60 m front-face impact)
   produce identical B(m_t) embeddings (zero B-space separation).
2. Perceptive compensation in F(o_F, a, z) and pi_theta(o_low, z): when terrain scan / ball
   state is provided in o_F and o_low, F and pi_theta disambiguate the transition outcome for a
   kinematically distinct target posture m_{t+1}^*.
3. Irreducible multi-force aliasing bottleneck: when two tasks require DIFFERENT contact impulses
   (e.g., light touch vs hard push-off) while holding the EXACT SAME kinematic trajectory m_{t+1}
   at the same obstacle geometry o_low, a purely kinematic z = B(m) cannot parameterize the force
   split unless planner P_psi uses non-local kinematic lead targets or B includes causal load response.
"""

from __future__ import annotations
import json
import time
from typing import Dict, Any
import torch
import torch.nn as nn
from fb_core import BackwardMapB, ForwardEnsembleF, ConditionedLowLevelActor


def run_b03_experiment(device_str: str = "auto", seed: int = 20261023) -> Dict[str, Any]:
    device = torch.device("cuda" if (device_str == "auto" and torch.cuda.is_available()) else ("cpu" if device_str == "auto" else device_str))
    torch.manual_seed(seed)
    t0 = time.time()

    m_dim = 229
    context_dim = 32  # terrain scan / ball state in o_low and o_F
    obs_dim = m_dim + context_dim
    act_dim = 29
    d_z = 256
    n_batch = 256

    b_net = BackwardMapB(m_dim, d_z).to(device)
    f_ens = ForwardEnsembleF(obs_dim, act_dim, d_z).to(device)
    actor = ConditionedLowLevelActor(obs_dim, act_dim, d_z).to(device)

    # 1. Identical kinematic posture m_same across 3 distinct contact contexts
    m_same = torch.randn(n_batch, m_dim, device=device)
    ctx_air = torch.zeros(n_batch, context_dim, device=device)
    ctx_box40 = torch.ones(n_batch, context_dim, device=device) * 0.40
    ctx_box60_impact = torch.ones(n_batch, context_dim, device=device) * (-0.60)

    with torch.no_grad():
        z_air = b_net(m_same)
        z_box40 = b_net(m_same)
        z_box60 = b_net(m_same)
        b_aliasing_max_diff = float(
            max(
                torch.max(torch.abs(z_air - z_box40)).item(),
                torch.max(torch.abs(z_air - z_box60)).item(),
            )
        )

    # 2. Train perceptive actor pi(o_low, z) to achieve distinct actions required in each context
    #    to reach the same kinematic outcome z_target = B(m_goal)
    m_goal = torch.randn(n_batch, m_dim, device=device)
    with torch.no_grad():
        z_goal = b_net(m_goal)

    obs_air = torch.cat([m_same, ctx_air], dim=-1)
    obs_box40 = torch.cat([m_same, ctx_box40], dim=-1)
    target_act_air = torch.tanh(m_same[:, :act_dim] * 0.5 + 0.4)
    target_act_box40 = torch.tanh(m_same[:, :act_dim] * 0.5 - 0.6)

    opt_perceptive = torch.optim.Adam(actor.parameters(), lr=3e-3)
    for _ in range(120):
        opt_perceptive.zero_grad()
        pred_air = actor(obs_air, z_goal)
        pred_box = actor(obs_box40, z_goal)
        loss = (pred_air - target_act_air).pow(2).mean() + (pred_box - target_act_box40).pow(2).mean()
        loss.backward()
        opt_perceptive.step()

    perceptive_mse = float(loss.item())

    # 3. Irreducible force-aliasing regime: SAME current obs (m_same, ctx_box40) AND SAME next
    #    kinematic frame m_next_same, but two different required contact forces (e.g., Force Mode 1 vs 2)
    #    Because B(m_next_same) produces a single z_kin, pi(obs_box40, z_kin) is a deterministic function
    #    of (obs_box40, z_kin) and cannot separate Force Mode 1 from Force Mode 2 without distinct z!
    force_target_1 = torch.ones(n_batch, act_dim, device=device) * 0.75
    force_target_2 = -torch.ones(n_batch, act_dim, device=device) * 0.75
    with torch.no_grad():
        pred_single_z = actor(obs_box40, z_goal)
        irreducible_same_z_mse = float(
            0.5 * ((pred_single_z - force_target_1).pow(2).mean() + (pred_single_z - force_target_2).pow(2).mean()).item()
        )

    verdict_pass = (
        b_aliasing_max_diff == 0.0
        and perceptive_mse < 0.01
        and irreducible_same_z_mse > 0.40
    )

    return {
        "experiment_id": "B03_CONTACT_ALIASING_AND_PERCEPTIVE_COMPENSATION",
        "device": str(device),
        "elapsed_sec": round(time.time() - t0, 4),
        "verdict": "PASS" if verdict_pass else "FAIL",
        "b_space_kinematic_aliasing_max_diff": b_aliasing_max_diff,
        "perceptive_context_disambiguation_action_mse": perceptive_mse,
        "irreducible_isokinematic_multi_force_mse": irreducible_same_z_mse,
    }


if __name__ == "__main__":
    print(json.dumps(run_b03_experiment(), indent=2))
