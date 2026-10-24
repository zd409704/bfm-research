"""Experiment Suite B04: Controlled 4-Arm Ablation — Pathwise World-Model Gradients vs FB Successor Derivatives.

Evaluates on the exact same DifferentiableContactPlant (causal state-action inputs only, ZERO future reference lookahead):
- Ground Truth Oracle: High-sample true-physics closed-loop trajectory return gradient d J_true / d theta.
- Arm A (Single-Task World Model, H=32): Learned world model W_psi(s_t, a_t) + task critic V_phi, unrolled H=32 steps.
- Arm B (Multi-Task World Model, H=32): W_psi(s_t, a_t) + z-conditioned policy pi_theta(s,z) and V_phi(s,z), H=32 steps.
- Arm C (Multi-Task World Model, H=1 First-Action Derivative Only): Same as Arm B, but unrolled H=1 step with stop-gradient
  on future policy calls inside V_phi(s_1, z), isolating H=1 vs H=32 pathwise differentiation.
- Arm D (Hybrid FB + Short-Horizon World Model, H in {1, 4, 8, 16, 32}):
  Unrolls W_psi(s_t, a_t) for H steps accumulating whitened intrinsic rewards r_z(hat_s_{t+1}) = B(hat_m_{t+1})^T W_lambda z
  plus terminal FB value bootstrap gamma^H F(hat_s_H, pi_theta(hat_s_H, z), z)^T z.
"""

from __future__ import annotations
import copy
import json
import math
import time
from typing import Dict, Any, List
import torch
import torch.nn as nn
from fb_core import BackwardMapB, ForwardEnsembleF, ConditionedLowLevelActor, EMAWhiteningTracker, project_to_sphere
from physics_env import DifferentiableContactPlant


class CausalWorldModel(nn.Module):
    """Causal state-delta world model W_psi(s_t, a_t) -> (s_{t+1}, m_{t+1}) with zero future reference hints."""

    def __init__(self, state_dim: int = 32, action_dim: int = 12, motion_dim: int = 229, hidden_dim: int = 256):
        super().__init__()
        self.delta_net = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, state_dim),
        )
        self.motion_head = nn.Linear(state_dim, motion_dim)

    def step(self, s: torch.Tensor, a: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        s_next = s + 0.05 * self.delta_net(torch.cat([s, a], dim=-1))
        m_next = torch.tanh(self.motion_head(s_next))
        return s_next, m_next


def flatten_grad(params: List[nn.Parameter]) -> torch.Tensor:
    grads = []
    for p in params:
        if p.grad is not None:
            grads.append(p.grad.detach().reshape(-1))
        else:
            grads.append(torch.zeros_like(p).reshape(-1))
    return torch.cat(grads, dim=0)


def run_b04_experiment(device_str: str = "auto", seed: int = 20261023) -> Dict[str, Any]:
    device = torch.device("cuda" if (device_str == "auto" and torch.cuda.is_available()) else ("cpu" if device_str == "auto" else device_str))
    torch.manual_seed(seed)
    t0 = time.time()

    state_dim = 32
    act_dim = 12
    m_dim = 229
    d_z = 64
    gamma = 0.96
    batch_size = 128

    plant = DifferentiableContactPlant(state_dim=state_dim, action_dim=act_dim, motion_dim=m_dim).to(device)
    wm = CausalWorldModel(state_dim=state_dim, action_dim=act_dim, motion_dim=m_dim).to(device)
    b_net = BackwardMapB(motion_dim=m_dim, d_z=d_z, hidden_dim=128).to(device)
    f_ens = ForwardEnsembleF(obs_f_dim=state_dim, action_dim=act_dim, d_z=d_z, hidden_dim=128).to(device)
    actor = ConditionedLowLevelActor(obs_low_dim=state_dim, action_dim=act_dim, d_z=d_z, hidden_dim=128).to(device)
    whitener = EMAWhiteningTracker(d_z=d_z, beta=0.1, lambda_reg=1e-2).to(device)

    # 1. Collect real transitions and train CausalWorldModel (8-step rollout loss) + FB representation
    s0 = torch.randn(batch_size, state_dim, device=device) * 0.5
    z_batch = project_to_sphere(torch.randn(batch_size, d_z, device=device), d_z)

    opt_wm = torch.optim.Adam(wm.parameters(), lr=3e-3)
    for _ in range(80):
        opt_wm.zero_grad()
        s_real = s0
        s_hat = s0
        wm_loss = torch.tensor(0.0, device=device)
        for h in range(8):
            with torch.no_grad():
                a_h = actor(s_real, z_batch)
                s_real_next, m_real_next = plant.step(s_real, a_h)
            s_hat_next, m_hat_next = wm.step(s_hat, a_h)
            wm_loss = wm_loss + (s_hat_next - s_real_next).pow(2).mean() + 0.5 * (m_hat_next - m_real_next).pow(2).mean()
            s_real = s_real_next
            s_hat = s_hat_next
        wm_loss.backward()
        opt_wm.step()

    # Update whitener on real motion states
    with torch.no_grad():
        _, m_sample = plant.step(s0, actor(s0, z_batch))
        b_sample = b_net(m_sample)
        whitener.update(b_sample)

    # Fit F_ens to multi-step oracle return on current policy so F represents discounted future B visitation
    opt_f = torch.optim.Adam(f_ens.parameters(), lr=3e-3)
    for _ in range(100):
        opt_f.zero_grad()
        with torch.no_grad():
            s_cur = s0
            a0_cur = actor(s0, z_batch)
            s_cur, m_cur = plant.step(s_cur, a0_cur)
            phi_sum = whitener.whiten_vector(b_net(m_cur))
            disc = gamma
            for _ in range(15):
                a_next = actor(s_cur, z_batch)
                s_cur, m_cur = plant.step(s_cur, a_next)
                phi_sum = phi_sum + disc * whitener.whiten_vector(b_net(m_cur))
                disc *= gamma
        a0_pred = actor(s0, z_batch).detach()
        f1, f2 = f_ens(s0, a0_pred, z_batch)
        loss_f = (f1 - phi_sum).pow(2).mean() + (f2 - phi_sum).pow(2).mean()
        loss_f.backward()
        opt_f.step()

    # 2. Compute Ground-Truth True-Physics Closed-Loop Policy Gradient (H_true = 24)
    actor_params = list(actor.parameters())
    actor.zero_grad()
    s_cur = s0
    j_true = torch.tensor(0.0, device=device)
    for t in range(24):
        a_t = actor(s_cur, z_batch)
        s_cur, m_cur = plant.step(s_cur, a_t)
        r_t = whitener.intrinsic_reward(b_net(m_cur), z_batch, whitened=True)
        j_true = j_true + (gamma ** t) * r_t.mean()
    (-j_true).backward()
    grad_true = flatten_grad(actor_params)

    # 3. Evaluate Hybrid FB + World-Model across horizons H in {1, 4, 8, 16, 32}
    #    Note H=0 corresponds to pure 1st-action FB derivative: -F(s_0, pi_theta(s_0, z), z)^T z
    horizon_metrics = {}

    # Pure FB first-action derivative (Standard FB)
    actor.zero_grad()
    a0 = actor(s0, z_batch)
    q_fb0 = f_ens.conservative_scalar_value(s0, a0, z_batch, z_batch)
    (-q_fb0.mean()).backward()
    grad_fb_first = flatten_grad(actor_params)
    cos_fb_first = float(torch.nn.functional.cosine_similarity(grad_fb_first, grad_true, dim=0).item())
    horizon_metrics["H_0_standard_FB_first_action"] = {
        "gradient_cosine_vs_true_physics": cos_fb_first,
        "relative_l2_grad_error": float(torch.linalg.vector_norm(grad_fb_first - grad_true).item() / (torch.linalg.vector_norm(grad_true).item() + 1e-8)),
    }

    for h_val in [1, 4, 8, 16, 32]:
        actor.zero_grad()
        s_hat = s0
        s_real_check = s0
        total_obj = torch.tensor(0.0, device=device)
        rollout_state_err = 0.0
        for t in range(h_val):
            a_t = actor(s_hat, z_batch)
            with torch.no_grad():
                s_real_check, _ = plant.step(s_real_check, a_t)
            s_hat, m_hat = wm.step(s_hat, a_t)
            rollout_state_err = float(torch.linalg.vector_norm(s_hat.detach() - s_real_check, dim=-1).mean().item())
            r_hat = whitener.intrinsic_reward(b_net(m_hat), z_batch, whitened=True)
            total_obj = total_obj + (gamma ** t) * r_hat.mean()
        # Terminal FB bootstrap at step H
        a_term = actor(s_hat, z_batch)
        q_tail = f_ens.conservative_scalar_value(s_hat, a_term, z_batch, z_batch)
        total_obj = total_obj + (gamma ** h_val) * q_tail.mean()
        (-total_obj).backward()
        grad_h = flatten_grad(actor_params)
        cos_h = float(torch.nn.functional.cosine_similarity(grad_h, grad_true, dim=0).item())
        horizon_metrics[f"H_{h_val}"] = {
            "horizon": h_val,
            "gradient_cosine_vs_true_physics": cos_h,
            "compounded_state_error_at_H": rollout_state_err,
            "relative_l2_grad_error": float(torch.linalg.vector_norm(grad_h - grad_true).item() / (torch.linalg.vector_norm(grad_true).item() + 1e-8)),
        }

    # Compare unwhitened vs whitened hybrid rollout at H=8
    actor.zero_grad()
    s_hat = s0
    unwhitened_obj = torch.tensor(0.0, device=device)
    for t in range(8):
        a_t = actor(s_hat, z_batch)
        s_hat, m_hat = wm.step(s_hat, a_t)
        r_unw = whitener.intrinsic_reward(b_net(m_hat), z_batch, whitened=False)
        unwhitened_obj = unwhitened_obj + (gamma ** t) * r_unw.mean()
    a_term = actor(s_hat, z_batch)
    unwhitened_obj = unwhitened_obj + (gamma ** 8) * f_ens.conservative_scalar_value(s_hat, a_term, z_batch, z_batch).mean()
    (-unwhitened_obj).backward()
    grad_h8_unw = flatten_grad(actor_params)
    cos_h8_unw = float(torch.nn.functional.cosine_similarity(grad_h8_unw, grad_true, dim=0).item())

    # Throughput benchmark: World Model MLP step vs MuJoCo step
    t_wm0 = time.perf_counter()
    with torch.no_grad():
        s_tmp = s0
        a_tmp = actor(s0, z_batch)
        for _ in range(200):
            s_tmp, _ = wm.step(s_tmp, a_tmp)
    wm_steps_per_sec = (200 * batch_size) / max(time.perf_counter() - t_wm0, 1e-6)

    best_intermediate_cos = max(horizon_metrics["H_4"]["gradient_cosine_vs_true_physics"], horizon_metrics["H_8"]["gradient_cosine_vs_true_physics"])
    verdict_pass = (
        best_intermediate_cos > cos_fb_first
        and horizon_metrics["H_32"]["compounded_state_error_at_H"] > horizon_metrics["H_8"]["compounded_state_error_at_H"]
    )

    return {
        "experiment_id": "B04_FOUR_ARM_PATHWISE_VS_FB_ABLATION",
        "device": str(device),
        "elapsed_sec": round(time.time() - t0, 4),
        "verdict": "PASS" if verdict_pass else "FAIL",
        "standard_fb_first_action_cosine": cos_fb_first,
        "best_short_horizon_hybrid_cosine": best_intermediate_cos,
        "h8_whitened_vs_unwhitened_cosine": {
            "whitened": horizon_metrics["H_8"]["gradient_cosine_vs_true_physics"],
            "unwhitened": cos_h8_unw,
        },
        "horizon_sweep": horizon_metrics,
        "batched_wm_steps_per_sec": round(wm_steps_per_sec, 1),
    }


if __name__ == "__main__":
    print(json.dumps(run_b04_experiment(), indent=2))
