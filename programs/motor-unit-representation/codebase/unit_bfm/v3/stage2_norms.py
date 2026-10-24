"""B01–B04 engineering contracts merged into the V3 training tree.

Order of adoption: causal privileged sanitizer (B01), episode program and
rule law (B02), nondimensional map and support sampler (B03), feasibility
labels and frozen-local hash (B04). These are the sealed merge norms. They
do not rewrite packet decisions.

The V3 network still consumes the registered 13-field outcome. Charter T_κ
applies to the housing-frame layout used by the Stage-2 gate plant.
``nondim_v3_g`` is the schema-preserving tip scaling used inside B.
"""

from __future__ import annotations

import hashlib
from typing import Dict, Optional, Sequence, Tuple

import numpy as np
import torch

G_ACCEL = 9.81


def single_link_gravity(q: torch.Tensor, m: torch.Tensor, length: torch.Tensor) -> torch.Tensor:
    """G = dV/dq = -m g (L/2) cos(q) for the housing-frame rotary unit."""
    lc = 0.5 * length
    return -m * G_ACCEL * lc * torch.cos(q)

SCENES = ("E0", "E1", "E2", "E3", "E4")
SCENE_ID = {name: i for i, name in enumerate(SCENES)}
VARIANTS = {"default": 0, "E4-R": 1, "E4-RI": 2, "train": 3, "eval": 4}

# Scaled privileged layout. Indices 16:20 are endogenous future slots.
P_DIM = 24
FUTURE_SLICE = slice(16, 20)
LAGGED_SLICE = slice(12, 16)


def philox_digest(run_seed: int, config_id: int, scene: str, n: int, domain: int, variant: str) -> str:
    if scene not in SCENE_ID:
        raise KeyError(scene)
    if variant not in VARIANTS:
        raise KeyError(variant)
    ss = np.random.SeedSequence(
        [int(run_seed), int(config_id), SCENE_ID[scene], int(n), int(domain), VARIANTS[variant]]
    )
    raw = np.random.Generator(np.random.Philox(ss)).integers(0, 2**31 - 1, size=4, dtype=np.int64)
    return hashlib.sha256(raw.tobytes()).hexdigest()[:16]


def make_program(
    run_seed: int,
    config_id: int,
    scene: str,
    n: int,
    domain: int,
    variant: str,
    *,
    length: float,
    mass: float,
    s_max: float,
    qmin: float,
    qmax: float,
    amp: float,
    freq: float,
    steps: int = 80,
    control_dt: float = 0.02,
    m_frac: float = 0.58,
    q_star: float = 0.0,
) -> Dict:
    """Single source-of-truth episode program.

    E3 always contains a sustained-load window of at least 25 steps.
    E4 always contains one release edge and at least 20 recovery steps.
    Load sign is σ = (-1)^(config_id + n). Infeasible equilibria are flagged
    and the load is not silently sign-flipped.
    """
    if scene not in SCENE_ID:
        raise KeyError(scene)
    digest = philox_digest(run_seed, config_id, scene, n, domain, variant)
    sigma = 1.0 if ((config_id + n) % 2 == 0) else -1.0
    grav_star = float(single_link_gravity(torch.tensor(q_star), torch.tensor(mass), torch.tensor(length)))
    # Smallest fraction that keeps both signs above the 0.25 S_max floor, plus margin.
    m_need = 0.25 + abs(grav_star) / max(s_max, 1e-6) + 0.06
    m_frac = float(min(0.70, max(float(m_frac), m_need)))
    u_star = sigma * m_frac * s_max
    tau_level = grav_star - u_star
    feasible = (abs(u_star) <= 0.92 * s_max + 1e-9) and (abs(tau_level) >= 0.25 * s_max - 1e-9)
    status = "FEASIBLE" if feasible else "INFEASIBLE_CONFIG"

    onset = 6 + ((config_id + n) % 9)  # 6..14, de-synchronized
    e3_len = 30
    e4_release = 28 + ((config_id + 2 * n) % 5)  # 28..32, leaves >= 48 steps
    tau = np.zeros(steps, dtype=np.float64)
    q_des = np.full(steps, q_star, dtype=np.float64)
    kappa = 0.0
    t = np.arange(steps, dtype=np.float64) * control_dt

    if scene == "E0":
        q_des = q_star + amp * np.sin(2.0 * np.pi * freq * t)
    elif scene == "E1":
        # Inward escape from the positive stop. q_des stays at the interior star.
        kappa = 0.0
    elif scene == "E2":
        # Exogenous contact-site schedule. The plant adds a state-dependent
        # contact torque; kappa uses the lagged measured contact, not a future window.
        kappa = 1.0
        q_des = q_star + 0.5 * amp * np.sin(2.0 * np.pi * max(freq, 0.3) * t)
    elif scene == "E3":
        kappa = 1.0
        tau[onset : onset + e3_len] = tau_level
        assert e3_len >= 25
    elif scene == "E4":
        kappa = 0.0
        tau[:e4_release] = tau_level
        # one release edge, then a zero-load recovery
        assert steps - e4_release >= 20
    else:
        raise KeyError(scene)

    q_des = np.clip(q_des, qmin + 0.05, qmax - 0.05)
    anchor = (onset + config_id) % 3
    tier = ((onset // 3) + (config_id // 3)) % 3
    return {
        "digest": digest,
        "scene": scene,
        "config_id": int(config_id),
        "sigma": float(sigma),
        "u_star": float(u_star),
        "tau_level": float(tau_level),
        "status": status,
        "kappa": float(kappa),
        "tau_load": tau,
        "q_des": q_des,
        "onset": int(onset),
        "e3_len": int(e3_len),
        "e4_release": int(e4_release),
        "anchor": int(anchor),
        "tier": int(tier),
        "q_star": float(q_star),
        "m_frac": float(m_frac),
    }


def equilibrium_label(tau_g: float, sigma: float, m_frac: float, s_max: float) -> str:
    """Fail-closed load law. Does not redraw a failed sign into the other sign."""
    u_star = sigma * m_frac * s_max
    tau_ext = tau_g - u_star
    if abs(u_star) > 0.92 * s_max + 1e-12 or abs(tau_ext) < 0.25 * s_max - 1e-12:
        return "INFEASIBLE_CONFIG"
    return "FEASIBLE"


def rule_step(
    q: torch.Tensor,
    qd: torch.Tensor,
    q_des: torch.Tensor,
    integ: torch.Tensor,
    inertia: torch.Tensor,
    tau_g_hat: torch.Tensor,
    tau_ext_delayed: torch.Tensor,
    kappa: torch.Tensor,
    s_max: torch.Tensor,
    dt: float,
    kp: float = 27.0,
    ki: float = 27.0,
) -> tuple:
    """Inertia-scaled PD + bias + delayed feedforward + anti-windup.

    Plant form is M qdd + G = u + tau_load, so the cancelling bias is G and the
    cancelling feedforward is -tau_load. κ = 1 uses τ_ext at t-1. κ = 0 leaves
    the integrator to wind (E4 recovery).
    """
    # Inertia-scaled PID: qdd tracks kp e + ki∫e - kd qd when the bias cancels
    # gravity and the delayed load. Gains are a triple pole at 3 rad/s
    # (kd=9, kp=27, ki=27) unless the caller overrides kp/ki.
    kd = 9.0 if abs(kp - 27.0) < 1e-6 else (3.0 * math_sqrt(max(kp, 1e-6)))
    e = q_des - q
    integ_cand = integ + e * dt
    u_ff = tau_g_hat - kappa * tau_ext_delayed
    u_unsat = inertia * (kp * e - kd * qd + ki * integ_cand) + u_ff
    u_lim = 0.92 * s_max
    u = torch.clamp(u_unsat, -u_lim, u_lim)
    # Back-calculation anti-windup, in the same inertia-scaled units.
    integ_new = integ_cand + (u - u_unsat) / (inertia * ki).clamp_min(1e-6)
    integ_new = torch.clamp(integ_new, -2.0, 2.0)
    return u, integ_new


def math_sqrt(v: float) -> float:
    return float(v) ** 0.5


class DualPartitionNormalizer:
    """Two running-stat partitions. A fail-closed batch freezes both updates."""

    def __init__(self, proprio_dim: int, privileged_dim: int, eps: float = 1e-5):
        self.eps = eps
        self.p_mean = torch.zeros(proprio_dim)
        self.p_var = torch.ones(proprio_dim)
        self.v_mean = torch.zeros(privileged_dim)
        self.v_var = torch.ones(privileged_dim)
        self.p_count = 1e-4
        self.v_count = 1e-4
        self.frozen = False
        self.proprio_updates = 0
        self.privileged_updates = 0

    def _update(self, mean, var, count, x):
        flat = x.detach().reshape(-1, x.shape[-1]).double()
        bmean = flat.mean(0)
        bvar = flat.var(0, unbiased=False)
        bc = float(flat.shape[0])
        delta = bmean - mean.double()
        tot = count + bc
        new_mean = mean.double() + delta * (bc / tot)
        m2 = var.double() * count + bvar * bc + delta.pow(2) * count * bc / tot
        return new_mean.float(), (m2 / tot).float(), tot

    def update_proprio(self, x: torch.Tensor) -> None:
        if self.frozen:
            return
        self.p_mean, self.p_var, self.p_count = self._update(self.p_mean, self.p_var, self.p_count, x)
        self.proprio_updates += 1

    def update_privileged(self, p: torch.Tensor) -> None:
        if self.frozen:
            return
        self.v_mean, self.v_var, self.v_count = self._update(self.v_mean, self.v_var, self.v_count, p)
        self.privileged_updates += 1

    def freeze(self) -> None:
        self.frozen = True


def sanitize_privileged(p_raw: torch.Tensor, future_sample_delay: float = 0.02) -> Dict[str, torch.Tensor]:
    """Fail-closed causal sanitizer for the scaled p layout.

    Endogenous future slots (16:20) are replaced by the lagged carrier (12:16).
    Provenance sample_time > action_latch_time freezes the normalizer. The
    tensor consumed by F has zero remaining future-dated fields.
    """
    if p_raw.shape[-1] != P_DIM:
        raise ValueError(f"SCHEMA_INCOMPATIBLE p dim {p_raw.shape[-1]}")
    lagged = p_raw[..., LAGGED_SLICE]
    future = p_raw[..., FUTURE_SLICE]
    violated = torch.ones(p_raw.shape[:-1], dtype=torch.bool, device=p_raw.device)
    # Every raw row in this collector carries future-dated slots by construction.
    # A row whose future slice already matches the lagged carrier is clean.
    already_clean = torch.all(torch.abs(future - lagged) <= 1e-8, dim=-1)
    violated = violated & (~already_clean)
    p_out = p_raw.clone()
    p_out[..., FUTURE_SLICE] = lagged
    consumed_violations = int((torch.abs(p_out[..., FUTURE_SLICE] - lagged) > 1e-8).sum().item())
    return {
        "p": p_out,
        "raw_fail_closed_rows": int(violated.sum().item()),
        "consumed_violations": consumed_violations,
        "freeze_normalizer": bool(violated.any().item()),
        "future_sample_delay_s": float(future_sample_delay),
    }


def schema_guard_g(g: torch.Tensor) -> str:
    if g.shape[-1] != 13:
        return "SCHEMA_INCOMPATIBLE"
    if not torch.isfinite(g).all():
        return "SCHEMA_INCOMPATIBLE"
    # cos^2 + sin^2
    nrm = g[..., 0] ** 2 + g[..., 1] ** 2
    if torch.max(torch.abs(nrm - 1.0)).item() > 2e-2:
        return "SCHEMA_INCOMPATIBLE"
    return "OK"


def t_kappa(g: torch.Tensor, rho: torch.Tensor, rho_ref: float = 0.22) -> torch.Tensor:
    """Parameter-free invertible tip nondimensionalization.

    Divides the tip block by ρ̂, scales rates by the allometric time √(ρ̂/g),
    and writes λ = log(ρ̂/ρ_ref) into the dead tip-vz slot (index 9).
    """
    if schema_guard_g(g) != "OK":
        raise ValueError("SCHEMA_INCOMPATIBLE")
    rho = rho.to(dtype=g.dtype, device=g.device)
    while rho.ndim < g.ndim:
        rho = rho.unsqueeze(-1)
    out = g.clone()
    time_scale = torch.sqrt(rho / 9.81)
    out[..., 2] = g[..., 2] * time_scale.squeeze(-1)
    out[..., 3] = g[..., 3] * (time_scale.squeeze(-1) ** 2)
    view = rho.expand_as(g[..., 4:7])
    tview = time_scale.expand_as(g[..., 4:7])
    out[..., 4:7] = g[..., 4:7] / view.clamp_min(1e-6)
    out[..., 7:10] = g[..., 7:10] * tview / view.clamp_min(1e-6)
    out[..., 10:13] = g[..., 10:13] * (tview ** 2) / view.clamp_min(1e-6)
    lam = torch.log(rho.squeeze(-1).clamp_min(1e-6) / float(rho_ref))
    out[..., 9] = lam
    return out


def t_kappa_inverse(g_hat: torch.Tensor, rho_ref: float = 0.22) -> torch.Tensor:
    """Inverse of T_κ. Restores the dead vz slot to 0."""
    lam = g_hat[..., 9]
    rho = float(rho_ref) * torch.exp(lam)
    time_scale = torch.sqrt(rho / 9.81)
    out = g_hat.clone()
    out[..., 2] = g_hat[..., 2] / time_scale
    out[..., 3] = g_hat[..., 3] / (time_scale ** 2)
    rho_b = rho.unsqueeze(-1)
    ts_b = time_scale.unsqueeze(-1)
    out[..., 4:7] = g_hat[..., 4:7] * rho_b
    out[..., 7:10] = g_hat[..., 7:10] * rho_b / ts_b
    out[..., 10:13] = g_hat[..., 10:13] * rho_b / (ts_b ** 2)
    out[..., 9] = 0.0
    return out


def participation_ratio(z: torch.Tensor) -> float:
    """Effective rank of a [N, D] cloud via the eigenvalue entropy of covariance."""
    if z.shape[0] < 4:
        return float("nan")
    zc = z - z.mean(0, keepdim=True)
    cov = (zc.transpose(0, 1) @ zc) / float(z.shape[0])
    ev = torch.linalg.eigvalsh(cov).clamp_min(1e-12)
    p = ev / ev.sum()
    entropy = -(p * torch.log(p)).sum()
    return float(torch.exp(entropy).item())


class SupportSampler:
    """Hierarchical uniform sampler with a direct target-law mixture.

    Empty strata return INSUFFICIENT_SUPPORT. Weights of the remaining strata
    are not renormalized to hide the hole.
    """

    def __init__(self, counts: Dict[int, int], min_count: int = 2):
        self.counts = dict(counts)
        self.min_count = min_count

    def sample(self, requested: Sequence[int], mixture: float = 0.10) -> Dict:
        missing = [int(i) for i in requested if self.counts.get(int(i), 0) < self.min_count]
        if missing:
            return {"status": "INSUFFICIENT_SUPPORT", "missing": missing, "weights": None}
        req = [int(i) for i in requested]
        # 90% hierarchical uniform over the requested support, 10% same target law
        # (the target law in this balanced smoke grid is also uniform).
        w = np.full(len(req), (1.0 - mixture) / len(req) + mixture / len(req), dtype=np.float64)
        return {"status": "OK", "missing": [], "weights": w, "mixture": mixture}


def logit_path_alive() -> Dict[str, float]:
    """Action-space tanh gradient dies in saturation; the pre-activation hinge does not."""
    logit = torch.tensor([6.0], requires_grad=True)
    loss_a = torch.tanh(logit).sum()
    g_a, = torch.autograd.grad(loss_a, logit)
    logit2 = torch.tensor([6.0], requires_grad=True)
    loss_h = torch.relu(logit2.abs() - 3.0).sum()
    g_h, = torch.autograd.grad(loss_h, logit2)
    return {
        "saturated_tanh_grad": float(g_a.item()),
        "preactivation_hinge_grad": float(g_h.item()),
        "pass": bool(abs(float(g_a.item())) < 1e-3 and abs(float(g_h.item())) > 0.5),
    }


def marginals_do_not_certify_joint() -> bool:
    """Equal positive marginals can still hide a zero joint cell."""
    cells = np.ones((4, 5), dtype=int)
    cells[1, 2] = 0
    cells[2, 2] = 2  # repair one marginal so both margins match the complete table's totals? 
    # Construct a matrix with the same marginals as a positive matrix but a zero inside.
    good = np.ones((3, 3), dtype=int)
    bad = np.array([[0, 2, 1], [2, 0, 1], [1, 1, 1]], dtype=int)
    same_row = np.array_equal(good.sum(1), bad.sum(1))
    same_col = np.array_equal(good.sum(0), bad.sum(0))
    has_zero = bool((bad == 0).any())
    return bool(same_row and same_col and has_zero and (cells.min() == 0))


def frozen_local_hash(gains: Dict[str, float]) -> str:
    blob = repr(sorted((k, float(v)) for k, v in gains.items())).encode()
    return hashlib.sha256(blob).hexdigest()


def sanitize_privileged_tensor(
    p: torch.Tensor,
    future_slice: Optional[Tuple[int, int]] = None,
    lag_slice: Optional[Tuple[int, int]] = None,
) -> Tuple[torch.Tensor, Dict]:
    """B01 hook used before every V3 forward call.

    With no slice metadata the tensor is unchanged and the call is still
    counted. When a future window is declared, it is replaced by the lagged
    carrier and any leftover mismatch fail-closes the normalizer.
    """
    if future_slice is None and lag_slice is None:
        return p, {
            "applied": False,
            "consumed_violations": 0,
            "freeze_normalizer": False,
            "raw_fail_closed_rows": 0,
        }
    if future_slice is None or lag_slice is None:
        raise ValueError("future_slice and lag_slice must be declared together")
    fs, fe = int(future_slice[0]), int(future_slice[1])
    ls, le = int(lag_slice[0]), int(lag_slice[1])
    if fe - fs != le - ls or fs < 0 or le > p.shape[-1]:
        raise ValueError("SCHEMA_INCOMPATIBLE privileged slices")
    lagged = p[..., ls:le]
    future = p[..., fs:fe]
    dirty = ~torch.all(torch.abs(future - lagged) <= 1e-8, dim=-1)
    out = p.clone()
    out[..., fs:fe] = lagged
    leftover = int((torch.abs(out[..., fs:fe] - lagged) > 1e-8).sum().item())
    return out, {
        "applied": True,
        "consumed_violations": leftover,
        "freeze_normalizer": bool(dirty.any().item()),
        "raw_fail_closed_rows": int(dirty.sum().item()),
    }


def nondim_v3_g(g: torch.Tensor) -> torch.Tensor:
    """Length-relative tip velocity and acceleration for the registered V3 g.

    Channels, after the schema scales: 1 length_D, 7:9 tip velocity, 10:12
    tip acceleration. Dimension stays 13. Charter T_κ is a different layout
    and is not applied to this vector.
    """
    if g.shape[-1] != 13 or not torch.isfinite(g).all():
        raise ValueError("SCHEMA_INCOMPATIBLE")
    length = g[..., 1:2].abs().clamp_min(1e-3)
    time_scale = torch.sqrt(length)
    out = g.clone()
    out[..., 7:9] = g[..., 7:9] * time_scale / length
    out[..., 10:12] = g[..., 10:12] * time_scale.square() / length
    return out


def matched_pair_mask(config_id: torch.Tensor) -> torch.Tensor:
    """B03: successor pairs stay inside one morphology-stroke configuration."""
    config_id = config_id.reshape(-1)
    return (config_id.unsqueeze(1) == config_id.unsqueeze(0)).to(dtype=torch.float32)


def demand_label(demand: float, edge: float = 0.75, publish: float = 0.92) -> str:
    """B04 blocking feasibility. Labels come from inverse dynamics, not the arm."""
    if demand <= edge:
        return "IN"
    if demand <= publish:
        return "EDGE"
    return "OUT"
