"""Core Forward-Backward (FB) + Low-Level Actor + Task-Q + Planner modules.

Implements the exact mathematical and engineering contracts from Baselines 01-05:
- Spherical backward map B(m) with radius sqrt(d_z)
- Forward successor ensemble F_{1,2}(o_F, a, z) with scalar inner-product order
- Causal EMA Gram matrix tracker Sigma_B and damped Cholesky whitening W_lambda
- Strict UFO update contract: single-pass BN update on (obs, m_current) and
  (next_obs, m_next), BN freeze, 50/50 sample_mixed_z relabeling without
  mutating behavior_z
- Full-prefix zero-hidden RNN burn-in for recurrent planner P and task critic Q
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


def project_to_sphere(x: torch.Tensor, d_z: Optional[int] = None, eps: float = 1e-8) -> torch.Tensor:
    """Projects last-dimension vectors onto the sphere of radius sqrt(d_z)."""
    dim = x.shape[-1] if d_z is None else d_z
    radius = math.sqrt(float(dim))
    norm = torch.linalg.vector_norm(x, ord=2, dim=-1, keepdim=True)
    return radius * x / (norm + eps)


class RunningMeanStdNormalizer(nn.Module):
    """Causal running mean/std normalizer with explicit update freeze control."""

    def __init__(self, shape: Tuple[int, ...], eps: float = 1e-5, clip: float = 5.0):
        super().__init__()
        self.eps = eps
        self.clip = clip
        self.register_buffer("mean", torch.zeros(shape, dtype=torch.float32))
        self.register_buffer("var", torch.ones(shape, dtype=torch.float32))
        self.register_buffer("count", torch.tensor(1e-4, dtype=torch.float64))
        self. register_buffer("update_calls", torch.tensor(0, dtype=torch.long))

    @torch.no_grad()
    def update_stats(self, x: torch.Tensor) -> None:
        if not self.training:
            raise RuntimeError("Attempted to update RunningMeanStdNormalizer while frozen (eval mode).")
        if not torch.isfinite(x).all():
            raise ValueError("Cannot update normalizer with non-finite tensor (invalid physics).")
        flat = x.reshape(-1, x.shape[-1]).to(dtype=torch.float64)
        batch_mean = flat.mean(dim=0)
        batch_var = flat.var(dim=0, unbiased=False)
        batch_count = float(flat.shape[0])

        delta = batch_mean - self.mean.to(torch.float64)
        tot_count = self.count + batch_count
        new_mean = self.mean.to(torch.float64) + delta * (batch_count / tot_count)
        m_a = self.var.to(torch.float64) * self.count
        m_b = batch_var * batch_count
        m2 = m_a + m_b + delta.pow(2) * self.count * batch_count / tot_count
        new_var = m2 / tot_count

        self.mean.copy_(new_mean.to(torch.float32))
        self.var.copy_(new_var.to(torch.float32))
        self.count.copy_(tot_count)
        self.update_calls.add_(1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        std = torch.sqrt(self.var + self.eps)
        normed = (x - self.mean) / std
        return torch.clamp(normed, -self.clip, self.clip)


class EMAWhiteningTracker(nn.Module):
    """Tracks EMA second-moment matrix Sigma_B = E[B(x)B(x)^T] and damped inverse."""

    def __init__(self, d_z: int, beta: float = 0.05, lambda_reg: float = 1e-2):
        super().__init__()
        self.d_z = d_z
        self.beta = beta
        self.lambda_reg = lambda_reg
        self.register_buffer("sigma_b", torch.eye(d_z, dtype=torch.float32))
        self.register_buffer("num_updates", torch.tensor(0, dtype=torch.long))

    @torch.no_grad()
    def update(self, b_batch: torch.Tensor) -> None:
        # b_batch: [N, d_z] on sphere of radius sqrt(d_z)
        n = b_batch.shape[0]
        gram = (b_batch.transpose(0, 1) @ b_batch) / float(max(n, 1))
        gram = 0.5 * (gram + gram.transpose(0, 1))
        if int(self.num_updates.item()) == 0:
            self.sigma_b.copy_(gram)
        else:
            self.sigma_b.lerp_(gram, self.beta)
        self.num_updates.add_(1)

    @torch.no_grad()
    def spectral_diagnostics(self, mat: Optional[torch.Tensor] = None) -> Dict[str, float]:
        target = self.sigma_b if mat is None else mat
        sym = 0.5 * (target + target.transpose(0, 1))
        evals = torch.linalg.eigvalsh(sym).clamp(min=1e-12)
        l_max = float(evals[-1].item())
        l_min = float(evals[0].item())
        cond = l_max / max(l_min, 1e-12)
        probs = evals / evals.sum()
        entropy = -torch.sum(probs * torch.log(probs + 1e-12))
        erank = float(torch.exp(entropy).item())
        off_diag_frob = float(torch.linalg.matrix_norm(sym - torch.diag(torch.diag(sym)), ord="fro").item())
        return {
            "lambda_max": l_max,
            "lambda_min": l_min,
            "condition_number": cond,
            "effective_rank": erank,
            "trace": float(evals.sum().item()),
            "off_diag_frobenius": off_diag_frob,
        }

    def whiten_vector(self, v: torch.Tensor, lambda_reg: Optional[float] = None) -> torch.Tensor:
        """Computes (Sigma_B + lambda_reg * I)^{-1} v via Cholesky decomposition."""
        reg = self.lambda_reg if lambda_reg is None else lambda_reg
        eye = torch.eye(self.d_z, device=v.device, dtype=v.dtype)
        damped = 0.5 * (self.sigma_b + self.sigma_b.transpose(0, 1)) + reg * eye
        chol = torch.linalg.cholesky(damped)
        # Solve damped @ x = v^T
        sol = torch.cholesky_solve(v.transpose(-2, -1), chol)
        return sol.transpose(-2, -1)

    def intrinsic_reward(self, b_next: torch.Tensor, z: torch.Tensor, whitened: bool = True) -> torch.Tensor:
        """Computes one-step intrinsic reward r_z(y) = B(y)^T Sigma_B^{-1} z or raw B(y)^T z."""
        if whitened:
            phi_next = self.whiten_vector(b_next)
            return (phi_next * z).sum(dim=-1)
        return (b_next * z).sum(dim=-1)


class BackwardMapB(nn.Module):
    """Single-frame motion encoder B_omega(m) -> S^{d_z - 1}(sqrt(d_z))."""

    def __init__(self, motion_dim: int, d_z: int = 256, hidden_dim: int = 256):
        super().__init__()
        self.motion_dim = motion_dim
        self.d_z = d_z
        self.net = nn.Sequential(
            nn.Linear(motion_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, d_z),
        )

    def forward(self, m_normed: torch.Tensor) -> torch.Tensor:
        raw = self.net(m_normed)
        return project_to_sphere(raw, self.d_z)


class ForwardHeadF(nn.Module):
    """Two-branch forward successor network F(o_F, a, z) -> R^{d_z}."""

    def __init__(self, obs_f_dim: int, action_dim: int, d_z: int = 256, hidden_dim: int = 256):
        super().__init__()
        self.sa_branch = nn.Sequential(
            nn.Linear(obs_f_dim + action_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
        )
        self.sz_branch = nn.Sequential(
            nn.Linear(obs_f_dim + d_z, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
        )
        self.trunk = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, d_z),
        )

    def forward(self, obs_f: torch.Tensor, action: torch.Tensor, z: torch.Tensor) -> torch.Tensor:
        h_sa = self.sa_branch(torch.cat([obs_f, action], dim=-1))
        h_sz = self.sz_branch(torch.cat([obs_f, z], dim=-1))
        return self.trunk(torch.cat([h_sa, h_sz], dim=-1))


class ForwardEnsembleF(nn.Module):
    """Twin forward successor heads F_1, F_2 enforcing scalar inner-product order."""

    def __init__(self, obs_f_dim: int, action_dim: int, d_z: int = 256, hidden_dim: int = 256):
        super().__init__()
        self.f1 = ForwardHeadF(obs_f_dim, action_dim, d_z, hidden_dim)
        self.f2 = ForwardHeadF(obs_f_dim, action_dim, d_z, hidden_dim)

    def forward(self, obs_f: torch.Tensor, action: torch.Tensor, z: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.f1(obs_f, action, z), self.f2(obs_f, action, z)

    def conservative_scalar_value(self, obs_f: torch.Tensor, action: torch.Tensor, w: torch.Tensor, z: Optional[torch.Tensor] = None) -> torch.Tensor:
        """Computes min_{k=1,2} (F_k(obs_f, action, z)^T w) AFTER scalar inner products."""
        z_cond = w if z is None else z
        f1_out, f2_out = self.forward(obs_f, action, z_cond)
        q1 = (f1_out * w).sum(dim=-1)
        q2 = (f2_out * w).sum(dim=-1)
        return torch.minimum(q1, q2)


class ConditionedLowLevelActor(nn.Module):
    """Low-level conditioned actor pi_theta(o_low, z) -> [-1, 1]^{action_dim}."""

    def __init__(self, obs_low_dim: int, action_dim: int, d_z: int = 256, hidden_dim: int = 256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_low_dim + d_z, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, action_dim),
        )

    def forward(self, obs_low: torch.Tensor, z: torch.Tensor) -> torch.Tensor:
        return torch.tanh(self.net(torch.cat([obs_low, z], dim=-1)))


class RecurrentLatentPlanner(nn.Module):
    """High-level recurrent planner P_psi(H_plan) -> S^{d_z - 1}(sqrt(d_z)) with zero-hidden burn-in."""

    def __init__(self, obs_plan_dim: int, d_z: int = 256, hidden_dim: int = 128):
        super().__init__()
        self.d_z = d_z
        self.hidden_dim = hidden_dim
        self.rnn = nn.LSTM(obs_plan_dim, hidden_dim, num_layers=2, batch_first=True)
        self.head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ELU(),
            nn.Linear(hidden_dim, d_z),
        )

    def forward_sequence(
        self,
        obs_seq: torch.Tensor,
        burn_in_len: int = 0,
    ) -> torch.Tensor:
        """Runs full-prefix zero-hidden burn-in on [:, :burn_in_len] under no_grad, then BPTT."""
        bsz = obs_seq.shape[0]
        device = obs_seq.device
        h0 = torch.zeros(2, bsz, self.hidden_dim, device=device, dtype=obs_seq.dtype)
        c0 = torch.zeros(2, bsz, self.hidden_dim, device=device, dtype=obs_seq.dtype)

        if burn_in_len > 0:
            with torch.no_grad():
                _, (h_burn, c_burn) = self.rnn(obs_seq[:, :burn_in_len, :], (h0, c0))
            h_init = h_burn.detach()
            c_init = c_burn.detach()
            active_seq = obs_seq[:, burn_in_len:, :]
        else:
            h_init, c_init = h0, c0
            active_seq = obs_seq

        rnn_out, _ = self.rnn(active_seq, (h_init, c_init))
        raw_z = self.head(rnn_out)
        return project_to_sphere(raw_z, self.d_z)


class RecurrentTaskTwinCritic(nn.Module):
    """Recurrent Twin Task Critic Q_{1,2}(H_Q, cmd) supporting either macro-z or step-action cmd."""

    def __init__(self, obs_q_dim: int, cmd_dim: int, hidden_dim: int = 128):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.rnn1 = nn.LSTM(obs_q_dim, hidden_dim, num_layers=2, batch_first=True)
        self.rnn2 = nn.LSTM(obs_q_dim, hidden_dim, num_layers=2, batch_first=True)
        self.q1_head = nn.Sequential(
            nn.Linear(hidden_dim + cmd_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.q2_head = nn.Sequential(
            nn.Linear(hidden_dim + cmd_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward_sequence(
        self,
        obs_q_seq: torch.Tensor,
        cmd_seq: torch.Tensor,
        burn_in_len: int = 0,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        bsz = obs_q_seq.shape[0]
        device = obs_q_seq.device
        h0 = torch.zeros(2, bsz, self.hidden_dim, device=device, dtype=obs_q_seq.dtype)
        c0 = torch.zeros(2, bsz, self.hidden_dim, device=device, dtype=obs_q_seq.dtype)

        if burn_in_len > 0:
            with torch.no_grad():
                _, (h1_b, c1_b) = self.rnn1(obs_q_seq[:, :burn_in_len, :], (h0, c0))
                _, (h2_b, c2_b) = self.rnn2(obs_q_seq[:, :burn_in_len, :], (h0, c0))
            s1 = (h1_b.detach(), c1_b.detach())
            s2 = (h2_b.detach(), c2_b.detach())
            active_obs = obs_q_seq[:, burn_in_len:, :]
            active_cmd = cmd_seq[:, burn_in_len:, :]
        else:
            s1 = (h0, c0)
            s2 = (h0, c0)
            active_obs = obs_q_seq
            active_cmd = cmd_seq

        out1, _ = self.rnn1(active_obs, s1)
        out2, _ = self.rnn2(active_obs, s2)
        q1 = self.q1_head(torch.cat([out1, active_cmd], dim=-1)).squeeze(-1)
        q2 = self.q2_head(torch.cat([out2, active_cmd], dim=-1)).squeeze(-1)
        return q1, q2


def compute_orthonormalization_loss(b_batch: torch.Tensor) -> torch.Tensor:
    """Computes standard FB orthonormalization regularizer on B(x)."""
    n = b_batch.shape[0]
    gram = b_batch @ b_batch.transpose(0, 1)
    diag = torch.diag(gram)
    off_diag_sq = (gram.pow(2).sum() - diag.pow(2).sum()) / float(max(n * (n - 1), 1))
    pull = diag.mean()
    return 0.5 * off_diag_sq - pull


@torch.no_grad()
def sample_ufo_mixed_z(
    b_net: BackwardMapB,
    m_next_normed: torch.Tensor,
    goal_ratio: float = 0.5,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Samples 50% online-B permuted m_next goals and 50% random sphere latents under frozen BN."""
    n = m_next_normed.shape[0]
    d_z = b_net.d_z
    device = m_next_normed.device
    z_rand = project_to_sphere(torch.randn(n, d_z, device=device, dtype=m_next_normed.dtype), d_z)
    perm = torch.randperm(n, device=device)
    z_goal = b_net(m_next_normed[perm])
    mask = (torch.rand(n, 1, device=device) < goal_ratio)
    z_update = torch.where(mask, z_goal, z_rand)
    return z_update, perm
