"""Experiment Suite B01: FB Density Factorization, Gram Conditioning, and Intrinsic Reward Identifiability.

Tests:
1. Spectral conditioning of Sigma_B = E[B(x)B(x)^T] under anisotropic replay distributions
   for d_z in {100, 256} and motion_dim in {229, 277} despite exact spherical norm ||B(x)||_2 = sqrt(d_z).
2. Exact cancellation of Sigma_B in zero-shot linear reward readout z_r = E[B(x)r(x)] = Sigma_B lambda
   vs non-cancellation in single-state goal encoding z_g = B(g) and one-step intrinsic reward r_z(y).
3. Reduction of intrinsic reward MSE and improvement of policy-gradient cosine alignment via
   causal EMA damped Cholesky whitening W_lambda = (Sigma_B_hat + lambda_reg I)^{-1}.
"""

from __future__ import annotations
import json
import math
import time
from typing import Dict, Any
import torch
from fb_core import BackwardMapB, EMAWhiteningTracker, project_to_sphere


def run_b01_experiment(device_str: str = "auto", seed: int = 20261023) -> Dict[str, Any]:
    device = torch.device("cuda" if (device_str == "auto" and torch.cuda.is_available()) else ("cpu" if device_str == "auto" else device_str))
    torch.manual_seed(seed)
    t0 = time.time()
    results_by_dim = {}

    for d_z, m_dim in [(100, 277), (256, 229)]:
        # Construct an anisotropic latent replay distribution on S^{d_z-1}(sqrt(d_z))
        # simulating early online training where standing/falling transitions dominate
        n_samples = 4096
        raw_coords = torch.randn(n_samples, d_z, device=device)
        # Induce realistic spectral decay across dimensions
        decay = torch.exp(-torch.linspace(0.0, 2.8, d_z, device=device))
        b_samples = project_to_sphere(raw_coords * decay.unsqueeze(0), d_z)

        # True population Gram matrix on the batch
        sigma_true = (b_samples.transpose(0, 1) @ b_samples) / float(n_samples)
        tracker = EMAWhiteningTracker(d_z=d_z, beta=0.10, lambda_reg=1e-2).to(device)
        for chunk in torch.chunk(b_samples, 16, dim=0):
            tracker.update(chunk)

        spec = tracker.spectral_diagnostics(sigma_true)

        # Ground-truth successor expectation E[sum_t gamma^t B(s_{t+1})] = Sigma_B F(s,a,z)
        # Let Q_B(s,a,z) = Sigma_true @ F_true(s,a,z). Suppose the true target direction is z.
        # Under exact FB convergence, Sigma_true F(s,a,z) = z  <=>  F(s,a,z) = Sigma_true^{-1} z.
        n_queries = 512
        z_queries = project_to_sphere(torch.randn(n_queries, d_z, device=device), d_z)
        eye = torch.eye(d_z, device=device)
        sigma_inv_true = torch.linalg.inv(sigma_true + 1e-5 * eye)

        # 1. Linear task reward r(x) = B(x)^T lambda_true:
        #    True task Q_r = lambda_true^T Q_B. Zero-shot z_r = E[B(x)r(x)] = Sigma_true lambda_true.
        #    Since F = Sigma_true^{-1} Q_B, F^T z_r = Q_B^T Sigma_true^{-1} Sigma_true lambda_true = Q_r!
        lambda_true = torch.randn(d_z, 1, device=device)
        q_b = torch.randn(n_queries, d_z, device=device)
        f_converged = torch.linalg.solve(sigma_true.to(torch.float64), q_b.transpose(0, 1).to(torch.float64)).transpose(0, 1).to(torch.float32)
        q_r_exact = (q_b @ lambda_true).squeeze(-1)
        z_r = sigma_true @ lambda_true
        q_r_readout = (f_converged @ z_r).squeeze(-1)
        linear_readout_max_err = float(torch.max(torch.abs(q_r_exact - q_r_readout)).item())

        # 2. Intrinsic state-matching reward r_z(y):
        #    Exact one-step reward whose discounted sum equals F(s,a,z)^T z is r_z*(y) = B(y)^T Sigma_B^{-1} z.
        y_states = b_samples[:n_queries]
        r_exact = ((sigma_inv_true @ y_states.transpose(0, 1)).transpose(0, 1) * z_queries).sum(dim=-1)
        r_unwhitened = tracker.intrinsic_reward(y_states, z_queries, whitened=False)
        r_whitened = tracker.intrinsic_reward(y_states, z_queries, whitened=True)

        mse_unwhitened = float(torch.mean((r_unwhitened - r_exact).pow(2)).item())
        mse_whitened = float(torch.mean((r_whitened - r_exact).pow(2)).item())

        cos_unwhitened = float(torch.nn.functional.cosine_similarity(r_unwhitened, r_exact, dim=0).item())
        cos_whitened = float(torch.nn.functional.cosine_similarity(r_whitened, r_exact, dim=0).item())

        # 3. Single-state goal direction cosine alignment:
        #    Suppose we want policy gradient in action space where Jacobian d Q_B / d a = J_a.
        #    True state-matching direction in B-space is Sigma_B^{-1} B(g), whereas raw prompt uses B(g).
        g_states = b_samples[n_queries : 2 * n_queries]
        exact_goal_dir = (sigma_inv_true @ g_states.transpose(0, 1)).transpose(0, 1)
        whitened_goal_dir = tracker.whiten_vector(g_states)
        pg_cos_unwhitened = float(torch.nn.functional.cosine_similarity(g_states, exact_goal_dir, dim=-1).mean().item())
        pg_cos_whitened = float(torch.nn.functional.cosine_similarity(whitened_goal_dir, exact_goal_dir, dim=-1).mean().item())

        results_by_dim[f"dz_{d_z}_m_{m_dim}"] = {
            "d_z": d_z,
            "motion_dim": m_dim,
            "sphere_norm_mean": float(torch.linalg.vector_norm(b_samples, dim=-1).mean().item()),
            "spectral": spec,
            "linear_reward_readout_cancellation_max_error": linear_readout_max_err,
            "intrinsic_reward_mse_unwhitened": mse_unwhitened,
            "intrinsic_reward_mse_whitened": mse_whitened,
            "intrinsic_reward_mse_reduction_ratio": mse_unwhitened / max(mse_whitened, 1e-12),
            "intrinsic_reward_cosine_unwhitened": cos_unwhitened,
            "intrinsic_reward_cosine_whitened": cos_whitened,
            "goal_gradient_cosine_unwhitened": pg_cos_unwhitened,
            "goal_gradient_cosine_whitened": pg_cos_whitened,
        }

    r256 = results_by_dim["dz_256_m_229"]
    verdict_pass = (
        abs(r256["spectral"]["trace"] - 256.0) < 1e-2
        and r256["spectral"]["condition_number"] > 10.0
        and r256["linear_reward_readout_cancellation_max_error"] < 1e-3
        and r256["intrinsic_reward_mse_whitened"] < 0.15 * r256["intrinsic_reward_mse_unwhitened"]
        and r256["goal_gradient_cosine_whitened"] > 0.95
    )

    return {
        "experiment_id": "B01_GRAM_CONDITIONING_AND_WHITENING",
        "device": str(device),
        "elapsed_sec": round(time.time() - t0, 4),
        "verdict": "PASS" if verdict_pass else "FAIL",
        "results": results_by_dim,
    }


if __name__ == "__main__":
    out = run_b01_experiment()
    print(json.dumps(out, indent=2))
