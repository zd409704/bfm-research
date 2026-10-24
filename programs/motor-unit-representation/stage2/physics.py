"""Generic single-actuator plant and LIMB2-v1 two-joint smoke plant.

Angle convention for the single rotary unit: housing frame M, rotation about
z_M, q = 0 along +x_M. Gravity in M is (0, -g, 0).

Angle convention for the two-joint limb: q = 0 is upright, positive q1 swings
the hip in the sagittal plane. Link gravity uses analytic dV/dq. A pelvis
payload is a vertical force at the hip, mapped through the foot-contact
Jacobian. It is not a mass on the grounded foot.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple

import torch

G = 9.81


def five_point_accel_coeffs(dt: float, device=None, dtype=None) -> torch.Tensor:
    """Causal quadratic fit over five control samples; returns qdd = 2 c2."""
    t = torch.arange(5, device=device, dtype=torch.float64) * float(dt)
    design = torch.stack([torch.ones(5, dtype=torch.float64), t, t * t], dim=1)
    coef = 2.0 * torch.linalg.pinv(design)[2]
    return coef.to(device=device, dtype=dtype or torch.float32)


def project_to_sphere(x: torch.Tensor, radius: float = 4.0, eps: float = 1e-8) -> torch.Tensor:
    norm = torch.linalg.vector_norm(x, ord=2, dim=-1, keepdim=True).clamp_min(eps)
    return radius * x / norm


def single_link_gravity(q: torch.Tensor, m: torch.Tensor, length: torch.Tensor) -> torch.Tensor:
    """Generalized gravity torque, consistent with V = -m g lc sin(q), lc = L/2.

    With gravity along -y_M and the tip at (L cos q, L sin q, 0):
    V = m * (0, -g, 0) · (lc cos q, lc sin q, 0) = -m g lc sin(q),
    G = dV/dq = -m g lc cos(q).
    Plant uses M qdd = u - G + tau_load, so the cancelling feedforward is +G? 
    Wait: standard manipulator form is M qdd + G = u + tau_load with G = dV/dq.
    Then u_ff = G - tau_load. G = -m g lc cos(q).
    """
    lc = 0.5 * length
    return -m * G * lc * torch.cos(q)


def single_joint_substep(
    q: torch.Tensor,
    qd: torch.Tensor,
    u: torch.Tensor,
    tau_load: torch.Tensor,
    bristle: torch.Tensor,
    m: torch.Tensor,
    length: torch.Tensor,
    inertia: torch.Tensor,
    qmin: torch.Tensor,
    qmax: torch.Tensor,
    dt: float,
    k_stop: float = 40.0,
    d_stop: float = 2.0,
    k_bristle: float = 0.35,
    bristle_max: float = 0.04,
    viscous: float = 0.12,
) -> Tuple[torch.Tensor, ...]:
    """One semi-implicit Euler substep with joint-stop spring, viscous drag, and bristle friction."""
    grav = single_link_gravity(q, m, length)
    pen_hi = torch.relu(q - qmax)
    pen_lo = torch.relu(qmin - q)
    active = (pen_hi + pen_lo) > 0
    tau_stop = -k_stop * pen_hi + k_stop * pen_lo - d_stop * qd * active.to(q.dtype)
    bristle = torch.clamp(bristle + qd * dt, -bristle_max, bristle_max)
    tau_fric = -k_bristle * bristle - viscous * qd
    # M qdd + G = u + tau_load + tau_stop + tau_fric, G = grav
    qdd = (u - grav + tau_load + tau_stop + tau_fric) / inertia.clamp_min(1e-6)
    qd = torch.clamp(qd + dt * qdd, -8.0, 8.0)
    q = q + dt * qd
    return q, qd, bristle, qdd, grav, tau_fric, tau_stop


def tip_kinematics(
    q: torch.Tensor,
    qd: torch.Tensor,
    qdd: torch.Tensor,
    length: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Tip pose/velocity/acceleration in housing frame M. z components are structural zeros."""
    c = torch.cos(q)
    s = torch.sin(q)
    px = length * c
    py = length * s
    pz = torch.zeros_like(px)
    vx = -length * s * qd
    vy = length * c * qd
    vz = torch.zeros_like(vx)
    ax = -length * c * qd * qd - length * s * qdd
    ay = -length * s * qd * qd + length * c * qdd
    az = torch.zeros_like(ax)
    pos = torch.stack([px, py, pz], dim=-1)
    vel = torch.stack([vx, vy, vz], dim=-1)
    acc = torch.stack([ax, ay, az], dim=-1)
    return pos, vel, acc


def pack_g13(
    q: torch.Tensor,
    qd: torch.Tensor,
    qdd_hat: torch.Tensor,
    length: torch.Tensor,
    u_nm: torch.Tensor,
    s_max: torch.Tensor,
) -> torch.Tensor:
    """13-field outcome: cos, sin, qd, qdd_hat, tip p/v/a, with tip z structural 0.

    Torque effort is not a 14th field. The schema note allows a variant to swap
    one tip channel; this smoke keeps the kinematic 13 and reports u_clip beside it.
    """
    pos, vel, acc = tip_kinematics(q, qd, qdd_hat, length)
    g = torch.cat(
        [
            torch.cos(q).unsqueeze(-1),
            torch.sin(q).unsqueeze(-1),
            qd.unsqueeze(-1),
            qdd_hat.unsqueeze(-1),
            pos,
            vel,
            acc,
        ],
        dim=-1,
    )
    assert g.shape[-1] == 13
    return g


def u_clip(u_nm: torch.Tensor, s_max: torch.Tensor) -> torch.Tensor:
    return torch.clamp(u_nm / s_max.clamp_min(1e-6), -1.0, 1.0)


# ---------------------------------------------------------------------------
# LIMB2-v1 two-joint dynamics
# ---------------------------------------------------------------------------


def _as_batch(value, ref: torch.Tensor) -> torch.Tensor:
    if not torch.is_tensor(value):
        value = torch.tensor(value, device=ref.device, dtype=ref.dtype)
    else:
        value = value.to(device=ref.device, dtype=ref.dtype)
    if value.ndim == 0:
        value = value.expand(ref.shape[0])
    return value


def limb_inertial_params(m1, m2, l1, l2):
    lc1 = l1 * 0.5
    lc2 = l2 * 0.5
    i1 = m1 * l1 * l1 / 12.0
    i2 = m2 * l2 * l2 / 12.0
    return lc1, lc2, i1, i2


def limb_mass_matrix(q2, m1, m2, l1, l2):
    """Planar RR inertia. Returns M11, M12, M22, a2 (coupling coefficient)."""
    lc1, lc2, i1, i2 = limb_inertial_params(m1, m2, l1, l2)
    a1 = i1 + i2 + m1 * lc1 * lc1 + m2 * (l1 * l1 + lc2 * lc2)
    a2 = m2 * l1 * lc2
    a3 = i2 + m2 * lc2 * lc2
    c2 = torch.cos(q2)
    m11 = a1 + 2.0 * a2 * c2
    m12 = a3 + a2 * c2
    if not torch.is_tensor(a3):
        m22 = torch.ones_like(m11) * float(a3)
    elif a3.ndim == 0:
        m22 = torch.ones_like(m11) * a3
    else:
        m22 = a3
    return m11, m12, m22, a2


def limb_coriolis(q2, qd1, qd2, a2):
    h = -a2 * torch.sin(q2)
    c1 = h * (2.0 * qd1 * qd2 + qd2 * qd2)
    c2 = -h * qd1 * qd1
    return c1, c2


def limb_gravity(q1, q2, m1, m2, l1, l2):
    """G = dV/dq with z up and q = 0 upright."""
    lc1 = 0.5 * l1
    lc2 = 0.5 * l2
    s1 = torch.sin(q1)
    s12 = torch.sin(q1 + q2)
    g1 = -G * ((m1 * lc1 + m2 * l1) * s1 + m2 * lc2 * s12)
    g2 = -G * (m2 * lc2 * s12)
    return g1, g2


def limb_potential(q1, q2, m1, m2, l1, l2):
    lc1 = 0.5 * l1
    lc2 = 0.5 * l2
    z1 = lc1 * torch.cos(q1)
    z2 = l1 * torch.cos(q1) + lc2 * torch.cos(q1 + q2)
    return G * (m1 * z1 + m2 * z2)


def pelvis_load_torque(q1, q2, l1, l2, m_payload: float):
    """Generalized torque of a vertical pelvis force through the foot Jacobian.

    Foot is the contact origin. Hip (pelvis) position is the forward map of the
    two links. F = (0, -m_payload * g) is applied at the pelvis, never as an
    added foot mass.
    """
    s1 = torch.sin(q1)
    c1 = torch.cos(q1)
    s12 = torch.sin(q1 + q2)
    c12 = torch.cos(q1 + q2)
    dx1 = l1 * c1 + l2 * c12
    dx2 = l2 * c12
    dz1 = -l1 * s1 - l2 * s12
    dz2 = -l2 * s12
    fz = -float(m_payload) * G
    # Fx = 0
    return dz1 * fz, dz2 * fz


def limb_qdd(q1, q2, qd1, qd2, u1, u2, m1, m2, l1, l2, m_payload: float, damp: float = 0.08):
    m11, m12, m22, a2 = limb_mass_matrix(q2, m1, m2, l1, l2)
    c1, c2 = limb_coriolis(q2, qd1, qd2, a2)
    g1, g2 = limb_gravity(q1, q2, m1, m2, l1, l2)
    p1, p2 = pelvis_load_torque(q1, q2, l1, l2, m_payload)
    rhs1 = u1 + p1 - c1 - g1 - damp * qd1
    rhs2 = u2 + p2 - c2 - g2 - damp * qd2
    det = (m11 * m22 - m12 * m12).clamp_min(1e-8)
    qdd1 = (m22 * rhs1 - m12 * rhs2) / det
    qdd2 = (-m12 * rhs1 + m11 * rhs2) / det
    return qdd1, qdd2


def limb_substep(q, qd, u, m1, m2, l1, l2, m_payload: float, dt: float, damp: float = 0.08):
    """Semi-implicit Euler. q, qd, u are [B, 2]. l2 may be [B] or scalar."""
    q1, q2 = q[:, 0], q[:, 1]
    qd1, qd2 = qd[:, 0], qd[:, 1]
    u1, u2 = u[:, 0], u[:, 1]
    l2b = _as_batch(l2, q1)
    qdd1, qdd2 = limb_qdd(q1, q2, qd1, qd2, u1, u2, m1, m2, l1, l2b, m_payload, damp=damp)
    qd_next = torch.stack(
        [
            torch.clamp(qd1 + dt * qdd1, -8.0, 8.0),
            torch.clamp(qd2 + dt * qdd2, -8.0, 8.0),
        ],
        dim=-1,
    )
    q_next = q + dt * qd_next
    return q_next, qd_next


def static_required_torque(q1, q2, m1, m2, l1, l2, m_payload: float):
    """Inverse-dynamics torque at rest: u = G - tau_pelvis (C = 0, no damping)."""
    g1, g2 = limb_gravity(q1, q2, m1, m2, l1, l2)
    p1, p2 = pelvis_load_torque(q1, q2, l1, l2, m_payload)
    # At rest rhs without u is p - g, and M qdd = u + p - g, so u = g - p
    return g1 - p1, g2 - p2


def forward_kinematics(q1, q2, l1, l2):
    x = l1 * torch.sin(q1) + l2 * torch.sin(q1 + q2)
    z = l1 * torch.cos(q1) + l2 * torch.cos(q1 + q2)
    return x, z


def inverse_kinematics(x, z, l1, l2):
    """Elbow-bent (q2 <= 0) analytic IK. Targets are clamped into the reachable annulus."""
    l2b = _as_batch(l2, x) if not torch.is_tensor(l2) or l2.ndim == 0 else l2
    if not torch.is_tensor(l1):
        l1t = torch.ones_like(x) * float(l1)
    else:
        l1t = l1.to(dtype=x.dtype, device=x.device)
        if l1t.ndim == 0:
            l1t = l1t.expand_as(x)
    r_max = (l1t + l2b) - 1e-6
    r_min = (l1t - l2b).abs() + 1e-6
    r = torch.sqrt(x * x + z * z).clamp(min=1e-8)
    r_clamped = torch.minimum(torch.maximum(r, r_min), r_max)
    # keep direction
    x = x / r * r_clamped
    z = z / r * r_clamped
    r2 = x * x + z * z
    c2 = (r2 - l1t * l1t - l2b * l2b) / (2.0 * l1t * l2b)
    c2 = c2.clamp(-1.0 + 1e-6, 1.0 - 1e-6)
    q2 = -torch.acos(c2)
    alpha = torch.atan2(l2b * torch.sin(q2), l1t + l2b * torch.cos(q2))
    q1 = torch.atan2(x, z) - alpha
    return q1, q2


def schur_identity_error(q2: float = 0.4, m1: float = 1.0, m2: float = 0.8, l1: float = 0.25, l2: float = 0.25) -> float:
    """Compare full inertia solve at tau=(1, 0) with the Schur complement of joint 2."""
    q2t = torch.tensor([q2], dtype=torch.float64)
    m11, m12, m22, _ = limb_mass_matrix(q2t, m1, m2, l1, l2)
    det = m11 * m22 - m12 * m12
    # inv(M) @ [1, 0]
    qdd1 = m22 / det
    m_schur = m11 - (m12 * m12) / m22
    qdd1_s = 1.0 / m_schur
    return float((qdd1 - qdd1_s).abs().item())


def gravity_identity_error(q1: float = 0.4, q2: float = -0.7) -> float:
    """Finite-difference dV/dq versus analytic gravity."""
    m1, m2, l1, l2 = 1.0, 0.8, 0.25, 0.22
    eps = 1e-6
    q1t = torch.tensor(q1, dtype=torch.float64)
    q2t = torch.tensor(q2, dtype=torch.float64)
    g1, g2 = limb_gravity(q1t, q2t, m1, m2, l1, l2)

    def V(a, b):
        return limb_potential(a, b, m1, m2, l1, l2)

    g1_n = (V(q1t + eps, q2t) - V(q1t - eps, q2t)) / (2 * eps)
    g2_n = (V(q1t, q2t + eps) - V(q1t, q2t - eps)) / (2 * eps)
    return float(torch.max(torch.stack([(g1 - g1_n).abs(), (g2 - g2_n).abs()])).item())


def free_flight_com_identity_error(q1: float = 0.3, q2: float = -0.5) -> float:
    """Internal-torque-free check: G matches the COM Jacobian transpose times total weight.

    For this fixed-base model the identity is G(q) = J_com(q)^T (m_tot * g_vec)
    with g_vec the upward coordinate derivative convention used in V.
    """
    m1, m2, l1, l2 = 1.1, 0.7, 0.25, 0.25
    q1t = torch.tensor(q1, dtype=torch.float64, requires_grad=True)
    q2t = torch.tensor(q2, dtype=torch.float64, requires_grad=True)
    # COM height
    lc1 = 0.5 * l1
    lc2 = 0.5 * l2
    z1 = lc1 * torch.cos(q1t)
    z2 = l1 * torch.cos(q1t) + lc2 * torch.cos(q1t + q2t)
    z_com = (m1 * z1 + m2 * z2) / (m1 + m2)
    # d z_com / dq * (m_tot * g) should equal G
    dz1, dz2 = torch.autograd.grad(z_com, [q1t, q2t])
    g1, g2 = limb_gravity(q1t.detach(), q2t.detach(), m1, m2, l1, l2)
    pred1 = dz1 * (m1 + m2) * G
    pred2 = dz2 * (m1 + m2) * G
    return float(torch.max((pred1 - g1).abs(), (pred2 - g2).abs()).item())


def ik_roundtrip_error() -> float:
    q1 = torch.tensor([0.45, -0.2], dtype=torch.float64)
    q2 = torch.tensor([-0.8, -0.4], dtype=torch.float64)
    l1, l2 = 0.25, 0.25
    x, z = forward_kinematics(q1, q2, l1, l2)
    q1b, q2b = inverse_kinematics(x, z, l1, l2)
    return float(torch.max(torch.stack([(q1 - q1b).abs(), (q2 - q2b).abs()])).item())


def halving_gate(dt: float = 2.5e-4, duration: float = 0.04) -> Dict[str, float]:
    """Float64 semi-implicit Euler at dt and dt/2. Relative final-state drift."""
    m1, m2, l1, l2 = 1.0, 0.8, 0.25, 0.25
    m_payload = 1.5

    def roll(step):
        q = torch.tensor([[0.2, -0.5]], dtype=torch.float64)
        qd = torch.tensor([[0.0, 0.0]], dtype=torch.float64)
        n = int(round(duration / step))
        impulse = 0.0
        for i in range(n):
            phase = i * step
            u = torch.tensor(
                [[1.5 * math.sin(8 * phase), -0.8 * math.cos(5 * phase)]],
                dtype=torch.float64,
            )
            q, qd = limb_substep(q, qd, u, m1, m2, l1, l2, m_payload, step, damp=0.05)
            impulse += float(u.abs().sum().item()) * step
        return q, qd, impulse

    q_a, qd_a, imp_a = roll(dt)
    q_b, qd_b, imp_b = roll(dt * 0.5)
    dq = float((q_a - q_b).abs().max().item())
    dqv = float((qd_a - qd_b).abs().max().item())
    # impulses of the open-loop command match by construction; compare state drift
    # relative to the coarser trajectory magnitude
    mag = float(q_a.abs().max().item()) + float(qd_a.abs().max().item()) + 1e-8
    rel = max(dq, dqv) / mag
    return {
        "dt_s": dt,
        "half_dt_s": dt * 0.5,
        "max_abs_q_drift": dq,
        "max_abs_qd_drift": dqv,
        "relative_drift": rel,
        "command_impulse_coarse": imp_a,
        "command_impulse_fine": imp_b,
        "pass": rel < 0.05,
    }


def build_unit_configs(dtype=torch.float64):
    """36 geometry seeds x 4 stroke profiles. All-feasible under the smoke load law."""
    n_seeds = 36
    lengths = torch.linspace(0.12, 0.32, n_seeds, dtype=dtype)
    masses = 0.55 + 0.004 * torch.arange(n_seeds, dtype=dtype)
    c0_cycle = torch.tensor([3.0, 6.0, 9.0], dtype=dtype)
    strokes = [
        {"qmin": -1.6, "qmax": 1.6, "amp": 0.0, "freq": 0.0},
        {"qmin": -1.8, "qmax": 1.5, "amp": 0.25, "freq": 0.4},
        {"qmin": -2.0, "qmax": 1.8, "amp": 0.40, "freq": 0.7},
        {"qmin": -2.2, "qmax": 2.0, "amp": 0.55, "freq": 1.0},
    ]
    rows = []
    for s in range(n_seeds):
        for k, stroke in enumerate(strokes):
            c0 = c0_cycle[s % 3]
            length = lengths[s]
            mass = masses[s]
            j_link = mass * length * length / 3.0
            gear = 8.0
            j_rotor = 3.0e-4
            s_max = float(1.25 * c0)
            # Scale reflected inertia with actuator capacity so a feasible load
            # (a fixed fraction of S_max) produces a comparable angular acceleration.
            inertia = max(float(j_link + (gear ** 2) * j_rotor), 0.045 * s_max)
            rows.append(
                {
                    "config_id": s * 4 + k,
                    "seed_id": s,
                    "stroke_id": k,
                    "length": float(length),
                    "mass": float(mass),
                    "c0": float(c0),
                    "s_max": s_max,
                    "inertia": float(inertia),
                    "gear": gear,
                    "qmin": stroke["qmin"],
                    "qmax": stroke["qmax"],
                    "amp": stroke["amp"],
                    "freq": stroke["freq"],
                }
            )
    assert len(rows) == 144
    return rows
