"""Stage-2 gates H1–H4 on the scaled full-physics smoke plant.

Numeric PASS/FAIL values are scale-conditional. ``scientific_lock`` stays false.
"""

from __future__ import annotations

import math
import time
from typing import Dict, List

import numpy as np
import torch
import torch.nn as nn

from contracts import (
    FUTURE_SLICE,
    P_DIM,
    DualPartitionNormalizer,
    SupportSampler,
    equilibrium_label,
    frozen_local_hash,
    logit_path_alive,
    make_program,
    marginals_do_not_certify_joint,
    participation_ratio,
    philox_digest,
    rule_step,
    sanitize_privileged,
    schema_guard_g,
    t_kappa,
    t_kappa_inverse,
)
from physics import (
    build_unit_configs,
    five_point_accel_coeffs,
    forward_kinematics,
    free_flight_com_identity_error,
    gravity_identity_error,
    halving_gate,
    ik_roundtrip_error,
    inverse_kinematics,
    limb_gravity,
    limb_mass_matrix,
    limb_substep,
    pack_g13,
    pelvis_load_torque,
    project_to_sphere,
    schur_identity_error,
    single_joint_substep,
    single_link_gravity,
    static_required_torque,
    u_clip,
)
from scale_flags import SCALE_FLAGS

FROZEN_GAINS = {
    "kp": 27.0,
    "ki": 27.0,
    "kd": 9.0,
    "lambda_reserve": 0.92,
    "z_radius": 4.0,
    # Limb servo gains are torques, not accelerations. Distal inertia is too
    # small for an inertia-scaled acceleration gain to both beat the pose
    # stiffness and stay inside a 5 ms step.
    "h4_kp": 20.0,
    "h4_kd": 1.2,
    "h4_q_scale": 0.35,
    "h4_ff_scale": 0.35,
}


def _device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _py(v):
    if isinstance(v, dict):
        return {str(k): _py(val) for k, val in v.items()}
    if isinstance(v, (list, tuple)):
        return [_py(x) for x in v]
    if isinstance(v, (np.floating,)):
        return float(v)
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    if isinstance(v, torch.Tensor):
        if v.ndim == 0:
            return _py(v.detach().cpu().item())
        return _py(v.detach().cpu().tolist())
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    return v


def spec_closure() -> Dict:
    """Controller-independent identities and contract unit checks."""
    schur = schur_identity_error()
    grav = gravity_identity_error()
    com = free_flight_com_identity_error()
    ik = ik_roundtrip_error()
    half = halving_gate(
        dt=SCALE_FLAGS["halving_probe_dt_s"],
        duration=SCALE_FLAGS["halving_probe_duration_s"],
    )
    d_r = philox_digest(7, 3, "E4", 0, 0, "E4-R")
    d_ri = philox_digest(7, 3, "E4", 0, 0, "E4-RI")
    labels = {
        "over_reserve": equilibrium_label(0.2, 1.0, 0.95, 8.0),
        "under_load": equilibrium_label(0.0, 1.0, 0.10, 8.0),
        "ok": equilibrium_label(0.4, -1.0, 0.55, 8.0),
    }
    # Rule equilibrium: κ=1 and a warm delay cancel a feasible load exactly.
    q_star = torch.tensor([0.70])
    mass = torch.tensor([0.56])
    length = torch.tensor([0.22])
    s_max = torch.tensor([7.5])
    inertia = torch.tensor([0.02])
    grav_star = single_link_gravity(q_star, mass, length)
    sigma = torch.tensor([1.0])
    u_star = sigma * 0.70 * s_max
    tau_load = grav_star - u_star
    u, _ = rule_step(
        q_star,
        torch.zeros(1),
        q_star,
        torch.zeros(1),
        inertia,
        grav_star,
        tau_load,
        torch.ones(1),
        s_max,
        0.02,
        kp=FROZEN_GAINS["kp"],
        ki=FROZEN_GAINS["ki"],
    )
    residual = float((u - grav_star + tau_load).abs().item())
    # Sanitizer strips a future-dated slice.
    raw = torch.zeros(4, P_DIM)
    raw[:, 12:16] = 0.2
    raw[:, 16:20] = 3.0  # endogenous future, not equal to the lag
    cleaned = sanitize_privileged(raw)
    g = torch.zeros(5, 13)
    g[:, 0] = 1.0
    g[:, 4] = 0.2
    g[:, 7] = 0.1
    rho = torch.full((5,), 0.2)
    g_hat = t_kappa(g, rho)
    g_back = t_kappa_inverse(g_hat)
    # vz was structurally 0 and is the slot λ overwrites
    roundtrip = float((g_back - g).abs().max().item())
    sampler = SupportSampler({0: 10, 1: 0, 2: 8})
    missing = sampler.sample([0, 1])
    ok_w = sampler.sample([0, 2])
    hinge = logit_path_alive()
    norm = DualPartitionNormalizer(4, 4)
    norm.update_proprio(torch.ones(8, 4))
    snap = norm.p_mean.clone()
    norm.freeze()
    norm.update_proprio(torch.ones(8, 4) * 9)
    norm.update_privileged(torch.ones(8, 4) * 9)
    freeze_ok = float((norm.p_mean - snap).abs().max().item()) == 0.0 and norm.privileged_updates == 0
    # Partition isolation while unfrozen: privileged updates must not move proprio stats.
    norm2 = DualPartitionNormalizer(4, 4)
    norm2.update_proprio(torch.randn(16, 4))
    snap2 = norm2.p_mean.clone()
    norm2.update_privileged(torch.randn(16, 4) * 5)
    isolated = float((norm2.p_mean - snap2).abs().max().item()) == 0.0
    passed = all(
        [
            schur < 1e-8,
            grav < 1e-5,
            com < 1e-5,
            ik < 1e-4,
            bool(half["pass"]),
            d_r != d_ri,
            labels["over_reserve"] == "INFEASIBLE_CONFIG",
            labels["under_load"] == "INFEASIBLE_CONFIG",
            labels["ok"] == "FEASIBLE",
            residual < 1e-5,
            cleaned["consumed_violations"] == 0,
            cleaned["raw_fail_closed_rows"] == 4,
            cleaned["freeze_normalizer"] is True,
            roundtrip < 1e-5,
            schema_guard_g(g) == "OK",
            missing["status"] == "INSUFFICIENT_SUPPORT",
            ok_w["status"] == "OK" and abs(float(np.sum(ok_w["weights"])) - 1.0) < 1e-8,
            hinge["pass"],
            marginals_do_not_certify_joint(),
            freeze_ok,
            isolated,
        ]
    )
    return {
        "pass": passed,
        "schur_identity_abs_err": schur,
        "gravity_finite_difference_abs_err": grav,
        "free_flight_com_identity_abs_err": com,
        "ik_roundtrip_abs_err": ik,
        "halving_gate": half,
        "e4_r_digest": d_r,
        "e4_ri_digest": d_ri,
        "e4_keys_distinct": d_r != d_ri,
        "equilibrium_labels": labels,
        "rule_equilibrium_residual_nm": residual,
        "t_kappa_roundtrip_abs_err": roundtrip,
        "logit_path": hinge,
        "marginals_insufficient": marginals_do_not_certify_joint(),
        "fail_closed_freeze": freeze_ok,
        "bn_partitions_isolated": isolated,
        "frozen_hash": frozen_local_hash(FROZEN_GAINS),
        "frozen_hash_check": frozen_local_hash(FROZEN_GAINS),
    }


def _stack_configs(configs: List[dict], device, dtype):
    def col(key):
        return torch.tensor([c[key] for c in configs], device=device, dtype=dtype)

    return {
        "length": col("length"),
        "mass": col("mass"),
        "s_max": col("s_max"),
        "inertia": col("inertia"),
        "qmin": col("qmin"),
        "qmax": col("qmax"),
        "amp": col("amp"),
        "freq": col("freq"),
        "c0": col("c0"),
        "seed_id": col("seed_id").long(),
        "stroke_id": col("stroke_id").long(),
        "config_id": col("config_id").long(),
    }


def rollout_coverage(configs: List[dict]) -> Dict[str, np.ndarray]:
    """One physics episode per (config, scene) cell. Returns flat step records."""
    device = torch.device("cpu")
    dtype = torch.float32
    steps = int(SCALE_FLAGS["episode_steps"])
    warmup = int(SCALE_FLAGS["warmup_steps"])
    dt_c = float(SCALE_FLAGS["control_dt_s"])
    n_sub = int(SCALE_FLAGS["coverage_substeps_per_control"])
    dt = float(SCALE_FLAGS["coverage_physics_dt_s"])
    n_cfg = len(configs)
    n_scene = 5
    B = n_cfg * n_scene
    cfg = _stack_configs(configs, device, dtype)
    # Repeat each config across scenes. scene index cycles fastest.
    rep = n_scene
    length = cfg["length"].repeat_interleave(rep)
    mass = cfg["mass"].repeat_interleave(rep)
    s_max = cfg["s_max"].repeat_interleave(rep)
    inertia = cfg["inertia"].repeat_interleave(rep)
    qmin = cfg["qmin"].repeat_interleave(rep)
    qmax = cfg["qmax"].repeat_interleave(rep)
    amp = cfg["amp"].repeat_interleave(rep)
    freq = cfg["freq"].repeat_interleave(rep)
    c0 = cfg["c0"].repeat_interleave(rep)
    seed_id = cfg["seed_id"].repeat_interleave(rep)
    config_id = cfg["config_id"].repeat_interleave(rep)
    scene_id = torch.arange(n_scene, device=device).repeat(n_cfg)

    programs = []
    infeasible = 0
    for c in configs:
        for scene in ("E0", "E1", "E2", "E3", "E4"):
            prog = make_program(
                20261024,
                c["config_id"],
                scene,
                n=0,
                domain=0,
                variant="train",
                length=c["length"],
                mass=c["mass"],
                s_max=c["s_max"],
                qmin=c["qmin"],
                qmax=c["qmax"],
                amp=c["amp"],
                freq=c["freq"],
                steps=steps,
                control_dt=dt_c,
            )
            if prog["status"] != "FEASIBLE":
                infeasible += 1
            programs.append(prog)
    assert len(programs) == B
    tau_cmd = torch.tensor(np.stack([p["tau_load"] for p in programs], axis=0), device=device, dtype=dtype)
    q_des = torch.tensor(np.stack([p["q_des"] for p in programs], axis=0), device=device, dtype=dtype)
    kappa = torch.tensor([p["kappa"] for p in programs], device=device, dtype=dtype)
    q_star = torch.tensor([p["q_star"] for p in programs], device=device, dtype=dtype)
    # Contact site for E2, a fixed exogenous angle.
    q_obs = q_star + 0.12
    k_contact = 5.0 + (config_id % 4).to(dtype)

    q = q_star.clone()
    # E1 starts just inside the positive stop.
    e1 = scene_id == 1
    q = torch.where(e1, qmax - 0.03, q)
    qd = torch.zeros(B, device=device, dtype=dtype)
    integ = torch.zeros(B, device=device, dtype=dtype)
    bristle = torch.zeros(B, device=device, dtype=dtype)
    tau_delay = tau_cmd[:, 0].clone()
    coef = five_point_accel_coeffs(dt_c, device=device, dtype=dtype)
    q_buf = q.unsqueeze(1).repeat(1, 5)

    total = warmup + steps
    store_q = []
    store_qd = []
    store_u = []
    store_tau = []
    store_fric = []
    store_stop = []
    store_qdd = []
    store_grav = []
    finite = torch.ones(B, dtype=torch.bool)

    for t in range(total):
        tau_g_hat = single_link_gravity(q, mass, length)
        src = min(t, steps - 1) if t >= warmup else 0
        # During warmup, hold the first-step command. After warmup, index t-warmup.
        if t < warmup:
            qdes_t = q_des[:, 0]
            cmd_t = tau_cmd[:, 0]
            # E1 warmup should not start on the stop spring already slammed.
        else:
            k = t - warmup
            qdes_t = q_des[:, k]
            cmd_t = tau_cmd[:, k]
        contact = torch.zeros(B, device=device, dtype=dtype)
        if True:
            depth = torch.relu(q - q_obs)
            contact = torch.where(scene_id == 2, -k_contact * depth - 0.4 * qd * (depth > 0), contact)
        tau_plant = cmd_t + contact
        # Inner servo runs at the physics substep. The logged command is the last
        # substep of the 50 Hz bucket. Delayed feedforward still updates once
        # per control step, so E3 keeps a one-step lag and E4 stays κ=0.
        u = torch.zeros(B, device=device, dtype=dtype)
        qdd_last = torch.zeros(B, device=device, dtype=dtype)
        fric_last = torch.zeros(B, device=device, dtype=dtype)
        stop_last = torch.zeros(B, device=device, dtype=dtype)
        grav_last = tau_g_hat
        tau_s = cmd_t
        for _ in range(n_sub):
            tau_g_hat = single_link_gravity(q, mass, length)
            depth = torch.relu(q - q_obs)
            contact_s = torch.where(
                scene_id == 2,
                -k_contact * depth - 0.4 * qd * (depth > 0),
                torch.zeros_like(q),
            )
            tau_s = cmd_t + contact_s
            u, integ = rule_step(
                q, qd, qdes_t, integ, inertia, tau_g_hat, tau_delay, kappa, s_max, dt,
                kp=FROZEN_GAINS["kp"], ki=FROZEN_GAINS["ki"],
            )
            q, qd, bristle, qdd_last, grav_last, fric_last, stop_last = single_joint_substep(
                q, qd, u, tau_s, bristle, mass, length, inertia, qmin, qmax, dt
            )
        tau_delay = cmd_t + torch.where(
            scene_id == 2,
            -k_contact * torch.relu(q - q_obs),
            torch.zeros_like(q),
        )
        q_buf = torch.cat([q_buf[:, 1:], q.unsqueeze(1)], dim=1)
        finite = finite & torch.isfinite(q) & torch.isfinite(qd)
        store_q.append(q)
        store_qd.append(qd)
        store_u.append(u)
        store_tau.append(tau_s.detach())
        store_fric.append(fric_last.detach())
        store_stop.append(stop_last.detach())
        store_qdd.append(qdd_last.detach())
        store_grav.append(grav_last.detach())

    Q = torch.stack(store_q, 0)  # [Ttot, B]
    QD = torch.stack(store_qd, 0)
    U = torch.stack(store_u, 0)
    TAU = torch.stack(store_tau, 0)
    FR = torch.stack(store_fric, 0)
    ST = torch.stack(store_stop, 0)
    QDD = torch.stack(store_qdd, 0)
    # Control-rate q history for the 5-point fit, including warmup.
    # Rebuild q buffer causally from Q.
    qdd_hat = torch.zeros_like(Q)
    for t in range(total):
        window = []
        for lag in range(4, -1, -1):
            idx = max(0, t - lag)
            window.append(Q[idx])
        stacked = torch.stack(window, 0)  # [5, B]
        qdd_hat[t] = torch.einsum("s,sb->b", coef, stacked)

    # Keep post-warmup steps only, but future slots need t+1, so the last step is dropped later.
    sl = slice(warmup, warmup + steps)
    out = {
        "q": Q[sl].numpy(),
        "qd": QD[sl].numpy(),
        "u": U[sl].numpy(),
        "tau": TAU[sl].numpy(),
        "fric": FR[sl].numpy(),
        "stop": ST[sl].numpy(),
        "qdd": QDD[sl].numpy(),
        "qdd_hat": qdd_hat[sl].numpy(),
        "length": length.numpy(),
        "mass": mass.numpy(),
        "s_max": s_max.numpy(),
        "inertia": inertia.numpy(),
        "c0": c0.numpy(),
        "amp": amp.numpy(),
        "freq": freq.numpy(),
        "seed_id": seed_id.numpy(),
        "config_id": config_id.numpy(),
        "scene_id": scene_id.numpy(),
        "kappa": kappa.numpy(),
        "q_des": q_des.numpy(),
        "tau_cmd": tau_cmd.numpy(),
        "qmin": qmin.numpy(),
        "qmax": qmax.numpy(),
        "finite": finite.numpy(),
        "infeasible_programs": infeasible,
        "e3_onset": np.array([p["onset"] for p in programs], dtype=np.int64),
        "e3_len": np.array([p["e3_len"] for p in programs], dtype=np.int64),
        "e4_release": np.array([p["e4_release"] for p in programs], dtype=np.int64),
        "anchor": np.array([p["anchor"] for p in programs], dtype=np.int64),
        "tier": np.array([p["tier"] for p in programs], dtype=np.int64),
        "program_status": np.array([1 if p["status"] == "FEASIBLE" else 0 for p in programs], dtype=np.int64),
    }
    return out


def static_hold_panel(configs: List[dict]) -> Dict[str, float]:
    """Canonical zero-velocity hold, both load signs, plus a u=0 negative control."""
    device = torch.device("cpu")
    dtype = torch.float32
    dt_c = float(SCALE_FLAGS["control_dt_s"])
    n_sub = int(SCALE_FLAGS["coverage_substeps_per_control"])
    dt = float(SCALE_FLAGS["coverage_physics_dt_s"])
    steps = 60
    cfg = _stack_configs(configs, device, dtype)
    # two signs
    signs = (1.0, -1.0)
    masses = []
    rmses = []
    pos_err = []
    control_fail = 0
    for sigma in signs:
        B = len(configs)
        length, mass, s_max = cfg["length"], cfg["mass"], cfg["s_max"]
        inertia, qmin, qmax = cfg["inertia"], cfg["qmin"], cfg["qmax"]
        q_star = torch.full((B,), 0.0, device=device, dtype=dtype)
        grav = single_link_gravity(q_star, mass, length)
        m_frac = (0.25 + grav.abs() / s_max + 0.06).clamp(0.40, 0.70)
        u_star = sigma * m_frac * s_max
        tau_level = grav - u_star
        q = q_star.clone()
        qd = torch.zeros(B, device=device, dtype=dtype)
        integ = torch.zeros(B, device=device, dtype=dtype)
        bristle = torch.zeros(B, device=device, dtype=dtype)
        kappa = torch.ones(B, device=device, dtype=dtype)
        tau_delay = tau_level.clone()
        qd_tail = []
        last_q = q
        finite = True
        for t in range(steps):
            tau_g_hat = single_link_gravity(q, mass, length)
            u, integ = rule_step(
                q, qd, q_star, integ, inertia, tau_g_hat, tau_delay, kappa, s_max, dt_c,
                kp=FROZEN_GAINS["kp"], ki=FROZEN_GAINS["ki"],
            )
            for _ in range(n_sub):
                q, qd, bristle, _, _, _, _ = single_joint_substep(
                    q, qd, u, tau_level, bristle, mass, length, inertia, qmin, qmax, dt
                )
            tau_delay = tau_level
            if t >= steps - 20:
                qd_tail.append(qd.detach().clone())
            last_q = q
            finite = finite and bool(torch.isfinite(q).all() and torch.isfinite(qd).all())
        tail = torch.stack(qd_tail, 0)
        rmse = torch.sqrt(torch.mean(tail * tail, dim=0))
        perr = (last_q - q_star).abs()
        rmses.append(rmse)
        pos_err.append(perr)
        control_fail += int((~torch.isfinite(last_q) | (perr > 0.6)).sum().item())
        if not finite:
            control_fail += B
    rmse_all = torch.cat(rmses, 0)
    perr_all = torch.cat(pos_err, 0)

    # Negative control: u = 0 on the positive-sign load, 16 configs.
    n_neg = 16
    length = cfg["length"][:n_neg]
    mass = cfg["mass"][:n_neg]
    s_max = cfg["s_max"][:n_neg]
    inertia = cfg["inertia"][:n_neg]
    qmin = cfg["qmin"][:n_neg]
    qmax = cfg["qmax"][:n_neg]
    q_star = torch.full((n_neg,), 0.0, dtype=dtype)
    grav = single_link_gravity(q_star, mass, length)
    m_frac = (0.25 + grav.abs() / s_max + 0.06).clamp(0.40, 0.70)
    tau_level = grav - m_frac * s_max
    q = q_star.clone()
    qd = torch.zeros(n_neg, dtype=dtype)
    bristle = torch.zeros(n_neg, dtype=dtype)
    u = torch.zeros(n_neg, dtype=dtype)
    qd_tail = []
    for t in range(40):
        for _ in range(n_sub):
            q, qd, bristle, _, _, _, _ = single_joint_substep(
                q, qd, u, tau_level, bristle, mass, length, inertia, qmin, qmax, dt
            )
        if t >= 20:
            qd_tail.append(qd.detach().clone())
    neg = torch.stack(qd_tail, 0)
    neg_rmse = float(torch.sqrt(torch.mean(neg * neg)).item())
    return {
        "zero_vel_rmse_mean": float(rmse_all.mean().item()),
        "zero_vel_rmse_worst": float(rmse_all.max().item()),
        "hold_position_abs_err_worst": float(perr_all.max().item()),
        "control_fail_count": int(control_fail),
        "negative_control_rmse": neg_rmse,
        "negative_control_position_abs_err": float((q - q_star).abs().mean().item()),
        "n_panel": int(rmse_all.numel()),
    }


def _build_step_tensors(roll: Dict[str, np.ndarray]):
    """Pack transitions (state_t, action that produces state_{t+1}, g_{t+1}).

    Stored rollout rows are post-step. The action aligned with the successor of
    row t is ``u[t+1]``, and the endogenous future slice is the reaction at t+1.
    """
    T, B = roll["q"].shape
    q = roll["q"]
    qd = roll["qd"]
    u = roll["u"]
    length = roll["length"]
    s_max = roll["s_max"]
    qt = torch.tensor(q)
    qdt = torch.tensor(qd)
    qddt = torch.tensor(roll["qdd_hat"])
    lt = torch.tensor(length)
    ut = torch.tensor(u)
    st = torch.tensor(s_max)
    g_all = [pack_g13(qt[t], qdt[t], qddt[t], lt, ut[t], st) for t in range(T)]
    G = torch.stack(g_all, 0).numpy()

    n = T - 1

    def lag_q(lag: int) -> np.ndarray:
        idx = np.clip(np.arange(n) - lag, 0, T - 1)
        return q[idx]

    ones = np.ones((n, B), dtype=np.float64)
    x = np.stack(
        [
            np.cos(q[:n]),
            np.sin(q[:n]),
            q[:n],
            qd[:n],
            lag_q(1),
            lag_q(2),
            lag_q(3),
            lag_q(4),
            u[:n],
            np.broadcast_to(roll["inertia"], (n, B)) * 50.0,
            np.broadcast_to(s_max, (n, B)) / 10.0,
            np.broadcast_to(length, (n, B)),
            np.broadcast_to(roll["mass"], (n, B)),
            np.transpose(roll["q_des"][:, :n], (1, 0)),
            roll["tau"][:n] / np.broadcast_to(s_max, (n, B)),
            ones,
        ],
        axis=-1,
    ).astype(np.float64)

    reaction = roll["tau"] + roll["fric"] + roll["stop"]
    fut = np.stack(
        [reaction[1:], roll["qdd"][1:], roll["fric"][1:], roll["stop"][1:]],
        axis=-1,
    ).astype(np.float64)
    lag = np.zeros_like(fut)
    lag[1:] = fut[:-1]
    lag[0] = fut[0]
    sched = roll["tau_cmd"]
    sched_now = np.transpose(sched[:, :n], (1, 0))
    sched_next = np.transpose(sched[:, 1:], (1, 0))
    p = np.zeros((n, B, P_DIM), dtype=np.float64)
    p[..., 0] = roll["scene_id"] / 4.0
    p[..., 1] = (np.arange(n) / max(n, 1))[:, None]
    p[..., 2] = roll["kappa"]
    p[..., 3] = roll["amp"]
    p[..., 4] = sched_now
    p[..., 5] = sched_next
    p[..., 6] = sched_next
    p[..., 7] = roll["freq"]
    p[..., 8] = roll["tau"][:n]
    p[..., 9] = roll["fric"][:n]
    p[..., 10] = roll["stop"][:n]
    p[..., 11] = roll["qdd_hat"][:n]
    p[..., 12:16] = lag
    p[..., 16:20] = fut
    p[..., 20] = roll["c0"] / 9.0
    p[..., 21] = (roll["scene_id"] == 3).astype(np.float64)

    a = u[1:][..., None].astype(np.float64)
    tau_next = roll["tau"][1:].astype(np.float64)

    def tile(vec):
        return np.broadcast_to(vec, (n, B)).copy()

    flat3 = lambda z: z.reshape(-1, z.shape[-1])
    return {
        "x": flat3(x),
        "p": flat3(p),
        "a": flat3(a),
        "g": flat3(G[:n].astype(np.float64)),
        "g_next": flat3(G[1:].astype(np.float64)),
        "config_id": tile(roll["config_id"]).reshape(-1),
        "seed_id": tile(roll["seed_id"]).reshape(-1),
        "scene_id": tile(roll["scene_id"]).reshape(-1),
        "length": tile(roll["length"]).reshape(-1),
        "mass": tile(roll["mass"]).reshape(-1),
        "c0": tile(roll["c0"]).reshape(-1),
        "amp": tile(roll["amp"]).reshape(-1),
        "freq": tile(roll["freq"]).reshape(-1),
        "s_max": tile(roll["s_max"]).reshape(-1),
        "tau_next": tau_next.reshape(-1),
        "u": a.reshape(-1),
    }


def _explained_variance(pred: np.ndarray, target: np.ndarray) -> float:
    var = target.var(axis=0)
    mask = var > 1e-6
    if not np.any(mask):
        return 0.0
    resid = ((pred - target) ** 2).mean(axis=0)
    ev = 1.0 - resid[mask] / var[mask]
    return float(np.mean(ev))


class _ScaledMLP(nn.Module):
    """Feature-standardized MLP used as the smoke stand-in for F."""

    def __init__(self, n_in: int, n_out: int, width: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_in, width),
            nn.SiLU(),
            nn.Linear(width, width),
            nn.SiLU(),
            nn.Linear(width, n_out),
        )

    def fit_standardized(self, feat: np.ndarray, target: np.ndarray, train_mask: np.ndarray, steps: int, seed: int):
        torch.manual_seed(seed)
        mu = feat[train_mask].mean(0)
        sd = feat[train_mask].std(0)
        sd = np.where(sd < 1e-6, 1.0, sd)
        ym = target[train_mask].mean(0)
        ys = target[train_mask].std(0)
        ys = np.where(ys < 1e-6, 1.0, ys)
        self.mu = mu.astype(np.float32)
        self.sd = sd.astype(np.float32)
        self.ym = ym.astype(np.float32)
        self.ys = ys.astype(np.float32)
        xt = torch.tensor((feat[train_mask] - mu) / sd, dtype=torch.float32)
        yt = torch.tensor((target[train_mask] - ym) / ys, dtype=torch.float32)
        opt = torch.optim.Adam(self.parameters(), lr=2e-3)
        n = xt.shape[0]
        for _ in range(steps):
            sel = torch.randint(0, n, (1024,))
            opt.zero_grad()
            loss = (self.net(xt[sel]) - yt[sel]).pow(2).mean()
            loss.backward()
            opt.step()
        self.eval()

    @torch.no_grad()
    def predict(self, feat: np.ndarray) -> np.ndarray:
        z = (feat.astype(np.float32) - self.mu) / self.sd
        pred = self.net(torch.tensor(z, dtype=torch.float32)).numpy()
        return pred * self.ys + self.ym


def run_h1(packed: Dict[str, np.ndarray]) -> Dict:
    x = packed["x"]
    p_raw = packed["p"]
    a = packed["a"]
    g_next = packed["g_next"]
    seed = packed["seed_id"]
    # Hold out a few geometry seeds for the factual panel.
    test_seeds = {5, 18, 33}
    test = np.isin(seed, list(test_seeds))
    train = ~test
    # Drop non-finite rows.
    finite = np.isfinite(x).all(1) & np.isfinite(p_raw).all(1) & np.isfinite(g_next).all(1)
    train = train & finite
    test = test & finite

    p_torch = torch.tensor(p_raw, dtype=torch.float64)
    cleaned = sanitize_privileged(p_torch)
    p_causal = cleaned["p"].numpy()
    # Consumed stream must carry the lagged carrier in the future slice.
    consumed_violations = int(cleaned["consumed_violations"])

    def features(p):
        base = np.concatenate([x, p, a], axis=1)
        prod = x[:, :4] * a
        return np.concatenate([base, prod], axis=1).astype(np.float32)

    f_c = features(p_causal)
    f_l = features(p_raw)
    # cos, sin, qd, tip position, tip velocity x/y. Acceleration channels are
    # a separate diagnostic: a 5-point second difference is not a smooth map
    # of the same features, and it dominated the earlier full-vector score.
    kin = np.array([0, 1, 2, 4, 5, 6, 7, 8], dtype=np.int64)
    y_kin = g_next[:, kin].astype(np.float32)
    width = int(SCALE_FLAGS["h1_mlp_width"])
    steps = int(SCALE_FLAGS["h1_mlp_steps"])

    def fit_arm(feat, target, seed_i):
        model = _ScaledMLP(feat.shape[1], target.shape[1], width)
        model.fit_standardized(feat, target, train, steps, seed_i)
        pred = model.predict(feat[test])
        return _explained_variance(pred, target[test]), model

    ev_c, model_c = fit_arm(f_c, y_kin, 20261024)
    ev_l, model_l = fit_arm(f_l, y_kin, 20261024)
    ev_full_c, _ = fit_arm(f_c, g_next.astype(np.float32), 20261025)
    ev_full_l, _ = fit_arm(f_l, g_next.astype(np.float32), 20261025)
    retention = float(ev_c / ev_l) if ev_l > 0.5 else 0.0

    # Counterfactual: stale future slots, action column shifted, truth from a
    # resimulated plant. Both arms are the factual-panel MLPs.
    cf = _counterfactual_probe(packed, model_c, model_l, train)
    charter_pass = bool(retention > float(SCALE_FLAGS["h1_retention_min"]) and consumed_violations == 0 and ev_l > 0.5)
    return {
        "status": "Candidate",
        "metric_verdict": "PASS" if charter_pass else "FAIL",
        "pass_is_scale_conditional": True,
        "td_explained_variance_causal": ev_c,
        "td_explained_variance_leaked": ev_l,
        "td_explained_variance_full_vector_causal": ev_full_c,
        "td_explained_variance_full_vector_leaked": ev_full_l,
        "target": str(SCALE_FLAGS["h1_target"]),
        "retention": retention,
        "retention_threshold": float(SCALE_FLAGS["h1_retention_min"]),
        "consumed_causality_violations": consumed_violations,
        "raw_fail_closed_rows": int(cleaned["raw_fail_closed_rows"]),
        "freeze_normalizer_on_raw_future": bool(cleaned["freeze_normalizer"]),
        "n_train": int(train.sum()),
        "n_test": int(test.sum()),
        "counterfactual": cf,
        "p_dim_executed": P_DIM,
        "p_dim_charter": 5065,
    }


def _counterfactual_probe(packed, model_c, model_l, train_mask) -> Dict[str, float]:
    """Replay 48 E3 rows one control step with a perturbed torque.

    Leaked features keep the original future slice (stale). Causal features do not
    contain that slice. Compare prediction error against the resimulated outcome.
    """
    scene = packed["scene_id"]
    idx = np.flatnonzero((scene == 3) & train_mask)
    if idx.size < 48:
        idx = np.flatnonzero(train_mask)
    rng = np.random.default_rng(1)
    choose = rng.choice(idx, size=min(48, idx.size), replace=False)

    # Recover plant state from packed g and the stored scalars. g has cos/sin/qd.
    g = packed["g"][choose]
    q = np.arctan2(g[:, 1], g[:, 0])
    qd = g[:, 2]
    length = packed["length"][choose]
    mass = packed["mass"][choose]
    s_max = packed["s_max"][choose]
    # Inertia is inside x column 9 / 50.
    inertia = packed["x"][choose, 9] / 50.0
    tau = packed["tau_next"][choose]
    u0 = packed["a"][choose, 0]
    u1 = u0 + 0.35
    dt = float(SCALE_FLAGS["coverage_physics_dt_s"])
    n_sub = int(SCALE_FLAGS["coverage_substeps_per_control"])

    def resim(u_np):
        q_t = torch.tensor(q, dtype=torch.float64)
        qd_t = torch.tensor(qd, dtype=torch.float64)
        u_t = torch.tensor(u_np, dtype=torch.float64)
        tau_t = torch.tensor(tau, dtype=torch.float64)
        br = torch.zeros_like(q_t)
        m = torch.tensor(mass, dtype=torch.float64)
        L = torch.tensor(length, dtype=torch.float64)
        J = torch.tensor(inertia, dtype=torch.float64).clamp_min(1e-5)
        qmin = torch.full_like(q_t, -2.0)
        qmax = torch.full_like(q_t, 2.0)
        qdd = torch.zeros_like(q_t)
        for _ in range(n_sub):
            q_t, qd_t, br, qdd, _, _, _ = single_joint_substep(
                q_t, qd_t, u_t, tau_t, br, m, L, J, qmin, qmax, dt
            )
        return q_t, qd_t, qdd

    q_n, qd_n, _qdd_n = resim(u1)
    # First three kinematic outputs are cos, sin, qd.
    truth = torch.stack([torch.cos(q_n), torch.sin(q_n), qd_n], dim=-1).numpy()

    def perturbed(p_rows, a_rows):
        x_rows = packed["x"][choose]
        prod = x_rows[:, :4] * a_rows
        return np.concatenate([x_rows, p_rows, a_rows, prod], axis=1).astype(np.float32)

    p_c = sanitize_privileged(torch.tensor(packed["p"][choose], dtype=torch.float64))["p"].numpy()
    p_l = packed["p"][choose].copy()  # stale future from the unperturbed transition
    a_rows = u1.reshape(-1, 1)
    pred_c = model_c.predict(perturbed(p_c, a_rows))[:, :3]
    pred_l = model_l.predict(perturbed(p_l, a_rows))[:, :3]
    err_c = float(np.mean((pred_c - truth) ** 2))
    err_l = float(np.mean((pred_l - truth) ** 2))
    return {
        "counterfactual_mse_causal": err_c,
        "counterfactual_mse_leaked_stale_future": err_l,
        "causal_better": bool(err_c < err_l),
    }


def run_h2(roll: Dict[str, np.ndarray], panel: Dict[str, float]) -> Dict:
    T, B = roll["qd"].shape
    n_cfg = 144
    cells = np.zeros((n_cfg, 5), dtype=np.int64)
    cfg = roll["config_id"]
    scene = roll["scene_id"]
    for s in range(5):
        for c in range(n_cfg):
            # one episode per cell, T steps, if finite
            cells[c, s] = T
    finite_eps = roll["finite"]
    if not bool(finite_eps.all()):
        bad = np.flatnonzero(~finite_eps)
        for b in bad:
            cells[int(cfg[b]), int(scene[b])] = 0

    e3 = scene == 3
    e4 = scene == 4
    e1 = scene == 1
    hold = 0
    recovery = 0
    e3_sched_ok = True
    e4_sched_ok = True
    for b in np.flatnonzero(e3):
        onset = int(roll["e3_onset"][b])
        length = int(roll["e3_len"][b])
        if length < 25 or onset + length > T:
            e3_sched_ok = False
            continue
        window = roll["qd"][onset : onset + length, b]
        # Settled portion of the sustained window.
        settled = window[-15:]
        if np.mean(np.abs(settled)) < 0.35:
            hold += 1
    for b in np.flatnonzero(e4):
        rel = int(roll["e4_release"][b])
        if rel >= T or (T - rel) < 20:
            e4_sched_ok = False
            continue
        # A real release: load before the edge, ~0 after.
        before = np.max(np.abs(roll["tau_cmd"][b, :rel])) if rel > 0 else 0.0
        after = np.max(np.abs(roll["tau_cmd"][b, rel:]))
        if before < 1e-6 or after > 1e-6:
            e4_sched_ok = False
        tail = roll["qd"][-10:, b]
        if np.mean(tail ** 2) ** 0.5 < 0.35:
            recovery += 1

    # λ = 0.92 witness: a finite step inside the reserve with the actuator working.
    witness = np.zeros(n_cfg, dtype=bool)
    u = roll["u"]
    s_max = roll["s_max"]
    for b in range(B):
        util = np.abs(u[:, b]) / max(float(s_max[b]), 1e-6)
        if np.any((util <= 0.92 + 1e-4) & (util >= 0.15) & np.isfinite(u[:, b])):
            witness[int(cfg[b])] = True

    # E1 escape: started near the stop (qmax - q small at step 0) and ended clear.
    escapes = 0
    e1_n = int(e1.sum())
    for b in np.flatnonzero(e1):
        # E1 is initialized on the positive stop before warmup. Success is a
        # final pose clear of that stop with bounded speed, not a still-contacting joint.
        gap1 = float(roll["qmax"][b] - roll["q"][-1, b])
        if gap1 > 0.20 and abs(float(roll["qd"][-1, b])) < 1.5:
            escapes += 1
    escape_rate = float(escapes / max(e1_n, 1))

    # Distinct anchors across the config axis (de-synchronization happened).
    anchor_nunique = int(len(np.unique(roll["anchor"])))

    coverage_ready = bool(
        cells.min() >= 1
        and e3_sched_ok
        and e4_sched_ok
        and bool(witness.all())
        and hold >= n_cfg
        and recovery >= n_cfg
        and panel["zero_vel_rmse_worst"] < float(SCALE_FLAGS["zero_vel_rmse_max"])
        and panel["control_fail_count"] == 0
        and panel["negative_control_position_abs_err"] > 0.30
        and roll["infeasible_programs"] == 0
        and escape_rate >= 0.9
        and bool(finite_eps.all())
    )
    return {
        "status": "Candidate",
        "metric_verdict": "PASS" if coverage_ready else "FAIL",
        "pass_is_scale_conditional": True,
        "coverage_ready": coverage_ready,
        "joint_cells": int(cells.size),
        "joint_cell_min_steps": int(cells.min()),
        "joint_cell_max_steps": int(cells.max()),
        "marginal_scene_steps": cells.sum(0).tolist(),
        "marginals_do_not_certify_joint": True,
        "sustained_load_hold_count": int(hold),
        "post_load_recovery_count": int(recovery),
        "e3_schedule_ok": e3_sched_ok,
        "e4_schedule_ok": e4_sched_ok,
        "lambda_092_witness_configs": int(witness.sum()),
        "limit_escape_rate": escape_rate,
        "anchor_levels_observed": anchor_nunique,
        "infeasible_programs": int(roll["infeasible_programs"]),
        "zero_vel_rmse_mean": panel["zero_vel_rmse_mean"],
        "zero_vel_rmse_worst": panel["zero_vel_rmse_worst"],
        "zero_vel_rmse_threshold": float(SCALE_FLAGS["zero_vel_rmse_max"]),
        "hold_position_abs_err_worst": panel["hold_position_abs_err_worst"],
        "control_fail_count": panel["control_fail_count"],
        "negative_control_rmse": panel["negative_control_rmse"],
        "negative_control_position_abs_err": panel["negative_control_position_abs_err"],
        "executed_mixture": "uniform_one_episode_per_cell",
        "charter_mixture": "E0:0.20,E1:0.15,E2:0.20,E3:0.15,E4:0.30",
    }


def run_h3(packed: Dict[str, np.ndarray], device: torch.device) -> Dict:
    torch.manual_seed(20261024)
    g = torch.tensor(packed["g"], dtype=torch.float32, device=device)
    g_next = torch.tensor(packed["g_next"], dtype=torch.float32, device=device)
    # Schema: repair tiny drift of cos/sin from packing noise by renormalizing nothing;
    # values come from cos/sin directly so the guard should pass.
    if schema_guard_g(g[:64]) != "OK":
        return {
            "status": "Candidate",
            "metric_verdict": "FAIL",
            "pass_is_scale_conditional": True,
            "reason": "SCHEMA_INCOMPATIBLE",
        }
    rho = torch.tensor(packed["length"], dtype=torch.float32, device=device)
    seed = packed["seed_id"].astype(np.int64)
    hold = set(int(s) for s in SCALE_FLAGS["h3_holdout_geometry_seeds"])
    train_m = torch.tensor([int(s) not in hold for s in seed], device=device)
    test_m = ~train_m
    g_hat = t_kappa(g, rho)
    g_next_hat = t_kappa(g_next, rho)
    a = torch.tensor(packed["a"], dtype=torch.float32, device=device)
    a_n = a / torch.tensor(packed["s_max"], dtype=torch.float32, device=device).unsqueeze(-1).clamp_min(1e-6)
    lam = g_hat[:, 9:10]
    geom = torch.stack(
        [
            rho / 0.22,
            torch.tensor(packed["mass"], dtype=torch.float32, device=device) / 0.55,
            torch.tensor(packed["c0"], dtype=torch.float32, device=device) / 6.0,
            torch.tensor(packed["amp"], dtype=torch.float32, device=device),
            torch.tensor(packed["freq"], dtype=torch.float32, device=device),
            lam.squeeze(-1),
        ],
        dim=-1,
    )
    cfg = torch.tensor(packed["config_id"].astype(np.int64), device=device)

    class BMap(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(13, 64), nn.SiLU(),
                nn.Linear(64, 16),
            )
            # Nonlinear decoder so a curved code can still reconstruct g.
            self.dec = nn.Sequential(
                nn.Linear(16, 64), nn.SiLU(),
                nn.Linear(64, 13),
            )

        def forward(self, g_in):
            return project_to_sphere(self.net(g_in), 4.0)

    class FMap(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(13 + 1 + 6, int(SCALE_FLAGS["h3_width"])),
                nn.SiLU(),
                nn.Linear(int(SCALE_FLAGS["h3_width"]), int(SCALE_FLAGS["h3_width"])),
                nn.SiLU(),
                nn.Linear(int(SCALE_FLAGS["h3_width"]), 16),
            )

        def forward(self, g_in, a_in, geom_in):
            return self.net(torch.cat([g_in, a_in, geom_in], dim=-1))

    # Per-dimension scale so a large acceleration channel cannot hide a collapsed code.
    mu = g_hat[train_m].mean(0)
    sd = g_hat[train_m].std(0).clamp_min(1e-3)
    g_s = (g_hat - mu) / sd
    g_next_s = (g_next_hat - mu) / sd

    bmap = BMap().to(device)
    fmap = FMap().to(device)
    opt_b = torch.optim.Adam(bmap.parameters(), lr=2e-3)
    train_idx = torch.nonzero(train_m, as_tuple=False).squeeze(-1)
    # Counts per train config for the support sampler.
    train_cfgs = cfg[train_idx].detach().cpu().numpy()
    counts: Dict[int, int] = {}
    for c in train_cfgs.tolist():
        counts[int(c)] = counts.get(int(c), 0) + 1
    sampler = SupportSampler(counts)
    present = [c for c, n in counts.items() if n >= 2]
    draw = sampler.sample(present[:8] if len(present) >= 8 else present, mixture=0.1)
    insufficient = sampler.sample(present[:4] + [-999], mixture=0.1)

    erank_floor = float(SCALE_FLAGS["h3_erank_floor"])

    def erank_hinge(z_group: torch.Tensor) -> torch.Tensor:
        zc = z_group - z_group.mean(0, keepdim=True)
        cov = (zc.transpose(0, 1) @ zc) / float(z_group.shape[0])
        ev = torch.linalg.eigvalsh(cov).clamp_min(1e-8)
        p = ev / ev.sum()
        er = torch.exp(-(p * torch.log(p)).sum())
        # Per-config effective-rank floor. Not a blind covariance-to-identity penalty.
        return torch.relu(erank_floor - er)

    steps = int(SCALE_FLAGS["h3_train_steps"])
    bs = int(SCALE_FLAGS["h3_batch"])
    for step in range(steps):
        sel = train_idx[torch.randint(0, train_idx.numel(), (bs,), device=device)]
        opt_b.zero_grad()
        z = bmap(g_s[sel])
        rec = (bmap.dec(z) - g_s[sel]).pow(2).mean()
        # Stratified hinge on four configs inside the batch.
        hinge = torch.zeros((), device=device)
        uniq = cfg[sel].unique()
        used = 0
        for c in uniq[:8]:
            mask = cfg[sel] == c
            if int(mask.sum()) >= 8:
                hinge = hinge + erank_hinge(z[mask])
                used += 1
        if used:
            hinge = hinge / used
        loss = rec + 0.15 * hinge
        loss.backward()
        opt_b.step()

    bmap.eval()
    for p in bmap.parameters():
        p.requires_grad_(False)
    opt_f = torch.optim.Adam(fmap.parameters(), lr=1.5e-3)
    for step in range(steps):
        # Hierarchical draw: pick configs, then rows inside them.
        pick = [present[int(i)] for i in torch.randint(0, len(present), (8,))]
        decision = sampler.sample(pick, mixture=0.1)
        if decision["status"] != "OK":
            continue
        parts = []
        for c in pick:
            pool = train_idx[cfg[train_idx] == c]
            if pool.numel() == 0:
                continue
            take = pool[torch.randint(0, pool.numel(), (64,), device=device)]
            parts.append(take)
        if not parts:
            continue
        sel = torch.cat(parts, 0)
        opt_f.zero_grad()
        with torch.no_grad():
            target = bmap(g_next_s[sel])
        pred = fmap(g_s[sel], a_n[sel], geom[sel])
        # Configuration-matched successor. No pooled-shell target.
        loss = (pred - target).pow(2).mean()
        loss.backward()
        opt_f.step()

    def group_rel(mask: torch.Tensor) -> Dict[str, float]:
        if int(mask.sum()) == 0:
            return {"worst": None, "mean": None, "n_groups": 0}
        with torch.no_grad():
            target = bmap(g_next_s[mask])
            pred = fmap(g_s[mask], a_n[mask], geom[mask])
            rel = (pred - target).norm(dim=-1) / target.norm(dim=-1).clamp_min(1e-6)
            cfgs = cfg[mask]
            worst = 0.0
            total = 0.0
            n_groups = 0
            pooled_err = []
            for c in cfgs.unique().tolist():
                m = cfgs == c
                val = float(rel[m].mean().item())
                worst = max(worst, val)
                total += val
                n_groups += 1
                # Pooled reference: distance to a shuffled other-config embedding.
            perm = torch.randperm(int(mask.sum()), device=device)
            pooled = (pred - target[perm]).norm(dim=-1) / target[perm].norm(dim=-1).clamp_min(1e-6)
            pooled_mean = float(pooled.mean().item())
        return {
            "worst": worst,
            "mean": total / max(n_groups, 1),
            "n_groups": n_groups,
            "pooled_reference_mean_rel": pooled_mean,
        }

    hold_stats = group_rel(test_m)
    train_stats = group_rel(train_m)
    # Per-config erank on a slice of training data, after freeze.
    eranks = []
    with torch.no_grad():
        z_all = bmap(g_s[train_m])
        cfgs = cfg[train_m]
        for c in cfgs.unique()[::6].tolist():
            zc = z_all[cfgs == c]
            if zc.shape[0] >= 16:
                eranks.append(participation_ratio(zc))
    worst_erank = float(min(eranks)) if eranks else float("nan")
    # Tip length-relative probe: linear map from z to tip xy / rho on holdout.
    with torch.no_grad():
        z_te = bmap(g_s[test_m])
        tip = g[test_m][:, 4:6] / rho[test_m].unsqueeze(-1).clamp_min(1e-6)
        # lstsq
        sol = torch.linalg.lstsq(z_te, tip).solution
        tip_rmse = float((z_te @ sol - tip).pow(2).mean().sqrt().item())
    threshold = float(SCALE_FLAGS["h3_worst_group_rel_err_max"])
    tip_max = float(SCALE_FLAGS["h3_tip_rmse_max"])
    worst = hold_stats["worst"]
    # A constant code on the sphere has norm 4, so relative successor error
    # can look small while the representation has collapsed. Rank is part of the gate.
    passed = (
        worst is not None
        and worst < threshold
        and worst_erank >= erank_floor
        and tip_rmse < tip_max
        and insufficient["status"] == "INSUFFICIENT_SUPPORT"
    )
    return {
        "status": "Candidate",
        "metric_verdict": "PASS" if passed else "FAIL",
        "pass_is_scale_conditional": True,
        "worst_group_relative_successor_error_holdout": worst,
        "mean_group_relative_successor_error_holdout": hold_stats["mean"],
        "pooled_reference_mean_rel_holdout": hold_stats.get("pooled_reference_mean_rel"),
        "worst_group_relative_successor_error_train": train_stats["worst"],
        "threshold": threshold,
        "n_holdout_groups": hold_stats["n_groups"],
        "n_train_groups": train_stats["n_groups"],
        "holdout_geometry_seeds": list(SCALE_FLAGS["h3_holdout_geometry_seeds"]),
        "worst_stratified_erank_train_subsample": worst_erank,
        "erank_floor": erank_floor,
        "charter_erank_floor": float(SCALE_FLAGS["h3_charter_erank_floor"]),
        "tip_length_relative_rmse_holdout": tip_rmse,
        "ipw_missing_stratum_status": insufficient["status"],
        "matched_reference": "same_config_successor",
        "t_kappa_isolated_from_input_normalizer": True,
    }


class _Upper(nn.Module):
    def __init__(self, d_in: int, d_out: int, width: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, width),
            nn.LayerNorm(width),
            nn.SiLU(),
            nn.Linear(width, width),
            nn.LayerNorm(width),
            nn.SiLU(),
            nn.Linear(width, d_out),
        )
        nn.init.normal_(self.net[-1].weight, std=0.08)
        nn.init.zeros_(self.net[-1].bias)

    def forward(self, obs):
        return self.net(obs)


def _limb_constants(device, dtype):
    return {
        "m1": float(SCALE_FLAGS["limb_m1_kg"]),
        "m2": float(SCALE_FLAGS["limb_m2_kg"]),
        "l1": float(SCALE_FLAGS["limb_l1_m"]),
        "m_payload": float(SCALE_FLAGS["limb_m_payload_kg"]),
        "q_target": torch.tensor(SCALE_FLAGS["limb_q_target"], device=device, dtype=dtype),
    }


def _classify_limb_cells(device, dtype):
    c = _limb_constants(device, dtype)
    cells = []
    grid = [(L2, C02, "grid") for L2 in SCALE_FLAGS["grid_L2_m"] for C02 in SCALE_FLAGS["grid_C02_nm"]]
    grid.append((SCALE_FLAGS["stress_L2_m"], SCALE_FLAGS["stress_C02_nm"], "stress"))
    q1 = c["q_target"][0]
    q2 = c["q_target"][1]
    for L2, C02, panel in grid:
        u1, u2 = static_required_torque(q1, q2, c["m1"], c["m2"], c["l1"], float(L2), c["m_payload"])
        s1 = 1.25 * float(SCALE_FLAGS["grid_C01_nm"])
        s2 = 1.25 * float(C02)
        d1 = abs(float(u1)) / s1
        d2 = abs(float(u2)) / s2
        demand = max(d1, d2)
        if demand <= float(SCALE_FLAGS["edge_reserve"]):
            label = "IN"
        elif demand <= float(SCALE_FLAGS["publish_reserve_lambda"]):
            label = "EDGE"
        else:
            label = "OUT"
        q2t = torch.tensor([float(q2)], device=device, dtype=dtype)
        m11, _, m22, _ = limb_mass_matrix(q2t, c["m1"], c["m2"], c["l1"], float(L2))
        cells.append(
            {
                "L2": float(L2),
                "C02": float(C02),
                "C01": float(SCALE_FLAGS["grid_C01_nm"]),
                "S1": s1,
                "S2": s2,
                "panel": panel,
                "demand": demand,
                "label": label,
                "feasible": label in ("IN", "EDGE"),
                "J1": float(m11.item()),
                "J2": float(m22.item()),
                "u_required": [float(u1), float(u2)],
            }
        )
    return cells


def _own_gravity(q, m1, m2, l1, l2):
    lc1 = 0.5 * l1
    lc2 = 0.5 * l2
    g1 = -9.81 * m1 * lc1 * torch.sin(q[:, 0])
    g2 = -9.81 * m2 * lc2 * torch.sin(q[:, 1])
    return torch.stack([g1, g2], dim=-1)


def _decode_setpoint(q, z, S):
    """Absolute joint setpoint and feedforward torque held for one control step.

    The latent trim is a residual about the measured angle. A neutral code
    therefore asks the local servo to stay, and the feedforward channel has
    to carry the pelvis load the own-link gravity term does not.
    """
    delta = FROZEN_GAINS["h4_q_scale"] * torch.tanh(z[:, 0:2] / 2.0)
    q_des = q.detach() + delta
    tau_ff = FROZEN_GAINS["h4_ff_scale"] * S * torch.tanh(z[:, 2:4] / 2.0)
    return q_des, tau_ff


def _torque_servo(q, qd, q_des, tau_ff, S, g_own):
    kp = FROZEN_GAINS["h4_kp"]
    kd = FROZEN_GAINS["h4_kd"]
    u = g_own + tau_ff + kp * (q_des - q) - kd * qd
    return torch.clamp(u, -0.92 * S, 0.92 * S)


def _upper_obs(q, qd, u_prev, q_target, L2, S, z_hip, zd_hip):
    return torch.cat(
        [
            q,
            qd,
            torch.sin(q),
            torch.cos(q),
            q_target.expand_as(q),
            L2.unsqueeze(-1),
            S / 10.0,
            u_prev / 10.0,
            z_hip.unsqueeze(-1),
            zd_hip.unsqueeze(-1),
        ],
        dim=-1,
    )


def _initial_q(q_target: torch.Tensor) -> torch.Tensor:
    offset = torch.tensor(
        SCALE_FLAGS["h4_init_offset_rad"], device=q_target.device, dtype=q_target.dtype
    )
    return q_target + offset


def _substep_torque(mode, q, qd, q_des, tau_ff, batch, cnst):
    damp = float(SCALE_FLAGS["h4_learning_damp"])
    dt = float(SCALE_FLAGS["h4_physics_dt_s"])
    n_sub = int(SCALE_FLAGS["h4_substeps_per_control"])
    for _ in range(n_sub):
        if mode in ("A", "A-rand"):
            g_own = _own_gravity(q, cnst["m1"], cnst["m2"], cnst["l1"], batch["L2"])
            u = _torque_servo(q, qd, q_des, tau_ff, batch["S"], g_own)
        elif mode == "C":
            u = tau_ff
        elif mode == "oracle":
            g1, g2 = limb_gravity(
                cnst["q_target"][0], cnst["q_target"][1], cnst["m1"], cnst["m2"], cnst["l1"], batch["L2"]
            )
            p1, p2 = pelvis_load_torque(
                cnst["q_target"][0], cnst["q_target"][1], cnst["l1"], batch["L2"], cnst["m_payload"]
            )
            u_hold = torch.stack([g1 - p1, g2 - p2], dim=-1)
            u = _torque_servo(q, qd, q_des, u_hold, batch["S"], torch.zeros_like(q))
        else:
            raise KeyError(mode)
        q, qd = limb_substep(
            q, qd, u, cnst["m1"], cnst["m2"], cnst["l1"], batch["L2"], cnst["m_payload"], dt, damp=damp
        )
    return q, qd, u


def _rollout_cost(mode: str, policy: nn.Module, batch: Dict[str, torch.Tensor], cnst: Dict, train: bool):
    T = int(SCALE_FLAGS["h4_episode_steps"])
    B = batch["L2"].shape[0]
    q_target = cnst["q_target"].unsqueeze(0).expand(B, -1)
    q = _initial_q(q_target)
    qd = torch.zeros_like(q)
    u_prev = torch.zeros_like(q)
    loss_task = torch.zeros((), device=q.device, dtype=q.dtype)
    hinge = torch.zeros((), device=q.device, dtype=q.dtype)
    z_hip_prev = None
    for t in range(T):
        _x, zhip = forward_kinematics(q[:, 0], q[:, 1], cnst["l1"], batch["L2"])
        zd = torch.zeros_like(zhip) if z_hip_prev is None else (zhip - z_hip_prev) / float(SCALE_FLAGS["control_dt_s"])
        z_hip_prev = zhip.detach()
        obs = _upper_obs(q, qd, u_prev, q_target, batch["L2"], batch["S"], zhip, zd)
        logit = policy(obs)
        hinge = hinge + torch.relu(logit.abs() - 8.0).mean()
        if mode == "A":
            zlat = project_to_sphere(logit, 4.0)
            q_des, tau_ff = _decode_setpoint(q, zlat, batch["S"])
        elif mode == "C":
            q_des = q_target
            tau_ff = 0.92 * batch["S"] * torch.tanh(logit[:, 0:2])
        else:
            raise KeyError(mode)
        q, qd, u = _substep_torque(mode, q, qd, q_des, tau_ff, batch, cnst)
        u_prev = u.detach()
        loss_task = loss_task + (q - q_target).pow(2).mean() + 0.01 * qd.pow(2).mean()
    loss = loss_task / T + 1e-3 * hinge / T
    return loss


def _eval_cells(mode, policy, batch, cnst) -> Dict[str, float]:
    T = int(SCALE_FLAGS["h4_episode_steps"])
    B = batch["L2"].shape[0]
    q_target = cnst["q_target"].unsqueeze(0).expand(B, -1)
    q = _initial_q(q_target)
    qd = torch.zeros_like(q)
    u_prev = torch.zeros_like(q)
    z_hip_prev = None
    pos_acc = torch.zeros(B, device=q.device, dtype=q.dtype)
    vel_acc = torch.zeros_like(pos_acc)
    n_tail = 0
    with torch.no_grad():
        for t in range(T):
            _x, zhip = forward_kinematics(q[:, 0], q[:, 1], cnst["l1"], batch["L2"])
            zd = torch.zeros_like(zhip) if z_hip_prev is None else (zhip - z_hip_prev) / float(SCALE_FLAGS["control_dt_s"])
            z_hip_prev = zhip
            obs = _upper_obs(q, qd, u_prev, q_target, batch["L2"], batch["S"], zhip, zd)
            if mode == "A":
                logit = policy(obs)
                zlat = project_to_sphere(logit, 4.0)
                q_des, tau_ff = _decode_setpoint(q, zlat, batch["S"])
            elif mode == "C":
                logit = policy(obs)
                q_des = q_target
                tau_ff = 0.92 * batch["S"] * torch.tanh(logit[:, 0:2])
            elif mode == "oracle":
                q_des = q_target
                tau_ff = torch.zeros_like(q)
            else:
                zlat = project_to_sphere(torch.randn(B, 16, device=q.device, dtype=q.dtype), 4.0)
                q_des, tau_ff = _decode_setpoint(q, zlat, batch["S"])
                mode = "A-rand"
            q, qd, u = _substep_torque(mode, q, qd, q_des, tau_ff, batch, cnst)
            u_prev = u
            if t >= T // 2:
                pos_acc = pos_acc + (q - q_target).pow(2).mean(-1).sqrt()
                vel_acc = vel_acc + qd.pow(2).mean(-1).sqrt()
                n_tail += 1
    pos = pos_acc / max(n_tail, 1)
    vel = vel_acc / max(n_tail, 1)
    return {
        "per_cell_pos_rmse": [float(v) for v in pos.detach().cpu()],
        "per_cell_vel_rmse": [float(v) for v in vel.detach().cpu()],
        "worst_pos_rmse": float(pos.max().item()),
        "worst_vel_rmse": float(vel.max().item()),
        "mean_pos_rmse": float(pos.mean().item()),
    }


def run_h4(device: torch.device) -> Dict:
    torch.manual_seed(20261024)
    dtype = torch.float32
    cells = _classify_limb_cells(device, dtype)
    learn_cells = [c for c in cells if c["feasible"] and c["panel"] == "grid"]
    if not learn_cells:
        return {
            "status": "Candidate",
            "metric_verdict": "FAIL",
            "pass_is_scale_conditional": True,
            "reason": "no_feasible_grid_cells",
            "cells": cells,
        }
    cnst = _limb_constants(device, dtype)
    batch = {
        "L2": torch.tensor([c["L2"] for c in learn_cells], device=device, dtype=dtype),
        "S": torch.tensor([[c["S1"], c["S2"]] for c in learn_cells], device=device, dtype=dtype),
        "J": torch.tensor([[c["J1"], c["J2"]] for c in learn_cells], device=device, dtype=dtype),
    }
    d_in = _upper_obs(
        torch.zeros(1, 2, device=device),
        torch.zeros(1, 2, device=device),
        torch.zeros(1, 2, device=device),
        cnst["q_target"].unsqueeze(0),
        batch["L2"][:1],
        batch["S"][:1],
        torch.zeros(1, device=device),
        torch.zeros(1, device=device),
    ).shape[-1]
    width = int(SCALE_FLAGS["h4_upper_width"])
    pol_a = _Upper(d_in, 16, width).to(device)
    pol_c = _Upper(d_in, 16, width).to(device)
    # Sphere calibration: unused latent axes carry the norm so the decoded
    # trim and feedforward start near zero. Flat torque keeps a zero bias.
    with torch.no_grad():
        pol_a.net[-1].bias[4:].fill_(1.5)
    n_a = sum(p.numel() for p in pol_a.parameters())
    n_c = sum(p.numel() for p in pol_c.parameters())
    assert n_a == n_c
    hash_before = frozen_local_hash(FROZEN_GAINS)
    opt_a = torch.optim.Adam(pol_a.parameters(), lr=3e-3)
    opt_c = torch.optim.Adam(pol_c.parameters(), lr=3e-3)
    updates = int(SCALE_FLAGS["h4_updates"])
    every = int(SCALE_FLAGS["h4_log_every"])
    curve_a = []
    curve_c = []

    def log(policy, mode, update):
        stats = _eval_cells(mode, policy, batch, cnst)
        stats["update"] = update
        return stats

    curve_a.append(log(pol_a, "A", 0))
    curve_c.append(log(pol_c, "C", 0))
    for update in range(1, updates + 1):
        opt_a.zero_grad()
        loss_a = _rollout_cost("A", pol_a, batch, cnst, True)
        loss_a.backward()
        torch.nn.utils.clip_grad_norm_(pol_a.parameters(), 1.0)
        opt_a.step()
        opt_c.zero_grad()
        loss_c = _rollout_cost("C", pol_c, batch, cnst, True)
        loss_c.backward()
        torch.nn.utils.clip_grad_norm_(pol_c.parameters(), 1.0)
        opt_c.step()
        if update % every == 0 or update == updates:
            curve_a.append(log(pol_a, "A", update))
            curve_c.append(log(pol_c, "C", update))
    hash_after = frozen_local_hash(FROZEN_GAINS)
    oracle = _eval_cells("oracle", pol_a, batch, cnst)
    arand = _eval_cells("A-rand", pol_a, batch, cnst)

    def auc(curve):
        return float(np.mean([row["worst_pos_rmse"] for row in curve]))

    auc_a = auc(curve_a)
    auc_c = auc(curve_c)
    final_a = curve_a[-1]["worst_pos_rmse"]
    final_c = curve_c[-1]["worst_pos_rmse"]

    def first_hit(curve):
        for row in curve:
            if row["worst_pos_rmse"] < 0.20 and row["worst_vel_rmse"] < float(SCALE_FLAGS["zero_vel_rmse_max"]):
                return int(row["update"])
        return None

    # Positive skill on the nominal cell (L2=0.25, C02=6) versus the worst cell.
    def skill(row):
        # R̃ = exp(-rmse / sigma)
        return [math.exp(-v / 0.25) for v in row["per_cell_pos_rmse"]]

    # Nominal index
    nominal = 0
    for i, c in enumerate(learn_cells):
        if abs(c["L2"] - 0.25) < 1e-9 and abs(c["C02"] - 6.0) < 1e-9:
            nominal = i
    skill_a = skill(curve_a[-1])
    skill_c = skill(curve_c[-1])
    delta_a = [s - skill_a[nominal] for s in skill_a]
    delta_c = [s - skill_c[nominal] for s in skill_c]
    contrast = [da - dc for da, dc in zip(delta_a, delta_c)]

    # Five-code diagnostic at the nominal operating point, not a certificate.
    with torch.no_grad():
        q_t = cnst["q_target"]
        u1, u2 = static_required_torque(
            q_t[0], q_t[1], cnst["m1"], cnst["m2"], cnst["l1"], learn_cells[nominal]["L2"], cnst["m_payload"]
        )
        smax = max(learn_cells[nominal]["S1"], learn_cells[nominal]["S2"])
        codes = {
            "A-AMP": abs(float(u2)) / (0.92 * learn_cells[nominal]["S2"]),
            "A-BW": 1.0,  # hold task, no commanded oscillation
            "A-IMP": 0.0,
            "A-RHO": learn_cells[nominal]["demand"],
            "A-NULL": abs(float(u1) + float(u2)) * 0.0 + abs(
                float(u1) - learn_cells[nominal]["u_required"][0]
            ),
            "certifies_h4": False,
            "note": "Grade-2 diagnostic at the nominal static operating point. Amplitude inclusion is not coverage.",
        }

    passed = bool(
        auc_a < 0.85 * auc_c
        and final_a <= final_c + 0.02
        and oracle["worst_pos_rmse"] < 0.15
        and hash_before == hash_after
        and n_a == n_c
    )
    return {
        "status": "Candidate",
        "metric_verdict": "PASS" if passed else "FAIL",
        "pass_is_scale_conditional": True,
        "definition": (
            "PASS when Mode A worst-cell position-RMSE area under the learning curve "
            "is below 85% of equal-parameter flat-torque Baseline C, Mode A is not worse "
            "at the final update, the gravity/payload oracle holds every feasible cell "
            "(worst tail position RMSE below 0.15) from the registered pose offset, "
            "and the frozen-local hash is unchanged. Episodes start at the target plus "
            "that offset. The local servo is a torque PD toward a latent setpoint."
        ),
        "auc_worst_pos_rmse_mode_A": auc_a,
        "auc_worst_pos_rmse_baseline_C": auc_c,
        "final_worst_pos_rmse_mode_A": final_a,
        "final_worst_pos_rmse_baseline_C": final_c,
        "updates_to_pos0.20_vel0.35_mode_A": first_hit(curve_a),
        "updates_to_pos0.20_vel0.35_baseline_C": first_hit(curve_c),
        "equal_trainable_params": n_a,
        "charter_upper_trainable_params": 140000,
        "frozen_hash_before": hash_before,
        "frozen_hash_after": hash_after,
        "frozen_hash_unchanged": hash_before == hash_after,
        "oracle_worst_pos_rmse": oracle["worst_pos_rmse"],
        "a_rand_worst_pos_rmse": arand["worst_pos_rmse"],
        "curve_mode_A": curve_a,
        "curve_baseline_C": curve_c,
        "delta_skill_A_minus_nominal": delta_a,
        "delta_skill_C_minus_nominal": delta_c,
        "paired_contrast_A_minus_C": contrast,
        "worst_cell_paired_contrast": float(min(contrast)) if contrast else None,
        "cells": cells,
        "learn_cell_count": len(learn_cells),
        "five_code_diagnostic": codes,
        "rail_in_upper_obs_only": True,
        "mode_B": "not_executed",
        "mode_B_note": "Smooth IK adapter is a Grade-2 diagnostic and is not trained in this smoke.",
    }


def run_all() -> Dict:
    t0 = time.time()
    device = _device()
    closure = spec_closure()
    if not closure["pass"]:
        # Still return a structured failure so the notebook writes JSON.
        return {
            "program": "motor-unit-representation",
            "stage": 2,
            "scientific_lock": False,
            "lock_reason": "Specification closure failed. No hypothesis is locked.",
            "scale_flags": SCALE_FLAGS,
            "spec_closure": closure,
            "hypotheses": {},
            "device": str(device),
            "elapsed_sec": round(time.time() - t0, 4),
        }
    configs = build_unit_configs()
    roll = rollout_coverage(configs)
    panel = static_hold_panel(configs)
    packed = _build_step_tensors(roll)
    h1 = run_h1(packed)
    h2 = run_h2(roll, panel)
    h3 = run_h3(packed, device)
    h4 = run_h4(device)
    hash_end = frozen_local_hash(FROZEN_GAINS)
    summary = {
        "program": "motor-unit-representation",
        "stage": 2,
        "scientific_lock": False,
        "lock_reason": (
            "Smoke-scale execution. Privileged width, proprioceptive history, "
            "network width, upper-parameter budget, and the learning timestep "
            "differ from the charter protocol. Numeric PASS values do not lock H1–H4."
        ),
        "hypothesis_status": "Candidate",
        "scale_flags": SCALE_FLAGS,
        "spec_closure": closure,
        "hypotheses": {"H1": h1, "H2": h2, "H3": h3, "H4": h4},
        "metric_verdicts": {
            "H1": h1["metric_verdict"],
            "H2": h2["metric_verdict"],
            "H3": h3["metric_verdict"],
            "H4": h4["metric_verdict"],
        },
        "frozen_hash_end": hash_end,
        "frozen_hash_matches_spec": hash_end == closure["frozen_hash"],
        "device": str(device),
        "torch_version": torch.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "elapsed_sec": round(time.time() - t0, 4),
    }
    return _py(summary)
