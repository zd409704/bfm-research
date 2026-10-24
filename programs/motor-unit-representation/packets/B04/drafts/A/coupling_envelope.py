"""Proposal A (B04) worked coupling calculation.

Planar 2-DoF serial limb on a passive vertical rail (base height y), hip q1
(absolute thigh angle from downward vertical), knee q2 (relative).  Geared
rotors (ratio n, inertia Jr): hip rotor on base, knee rotor on thigh.
Generalised coordinates Q = (y, q1, q2).  All torques are reported as
fractions of the joint's S_max = 1.25 C0.

Outputs: (1) numerical check of the reduction identity, (2) coupling
amplitude ratios for tracking / squat / landing cells, (3) PI closed-chain
null-mode demonstration.
"""
import json
import sys

import numpy as np

G = 9.81


def leg(l1=0.25, l2=0.25, m1=0.60, m2=0.25, mb=1.5, mp=0.0, C1=9.0, C2=6.0,
        n=9.0, Jr=5e-5):
    return dict(l1=l1, l2=l2, lc1=0.6 * l1, lc2=0.5 * l2, m1=m1, m2=m2,
                I1=m1 * l1 ** 2 / 12, I2=m2 * l2 ** 2 / 12, mb=mb + mp,
                S1=1.25 * C1, S2=1.25 * C2, n=n, Jr=Jr)


def mass_matrix(p, q1, q2):
    l1, lc1, lc2, m1, m2 = p["l1"], p["lc1"], p["lc2"], p["m1"], p["m2"]
    I1, I2, n, Jr = p["I1"], p["I2"], p["n"], p["Jr"]
    s1, s12 = np.sin(q1), np.sin(q1 + q2)
    M = np.zeros((3, 3))
    M[0, 0] = p["mb"] + m1 + m2
    M[0, 1] = M[1, 0] = (m1 * lc1 + m2 * l1) * s1 + m2 * lc2 * s12
    M[0, 2] = M[2, 0] = m2 * lc2 * s12
    M[1, 1] = (I1 + m1 * lc1 ** 2 + I2 + m2 * (l1 ** 2 + lc2 ** 2 + 2 * l1 * lc2 * np.cos(q2))
               + n ** 2 * Jr + Jr)
    M[1, 2] = M[2, 1] = I2 + m2 * (lc2 ** 2 + l1 * lc2 * np.cos(q2)) + n * Jr
    M[2, 2] = I2 + m2 * lc2 ** 2 + n ** 2 * Jr
    return M


def bias(p, q1, q2, dq1, dq2):
    """Coriolis/centrifugal + gravity vector h(Q, dQ) with M ddQ + h = B tau + Jc^T lam."""
    l1, lc1, lc2, m1, m2 = p["l1"], p["lc1"], p["lc2"], p["m1"], p["m2"]
    a = m1 * lc1 + m2 * l1
    c1, c12 = np.cos(q1), np.cos(q1 + q2)
    s1, s12 = np.sin(q1), np.sin(q1 + q2)
    hh = m2 * l1 * lc2 * np.sin(q2)
    cor = np.array([
        a * c1 * dq1 ** 2 + m2 * lc2 * c12 * (dq1 + dq2) ** 2,
        -hh * (2 * dq1 * dq2 + dq2 ** 2),
        hh * dq1 ** 2,
    ])
    grav = np.array([
        (p["mb"] + m1 + m2) * G,
        G * (a * s1 + m2 * lc2 * s12),
        G * m2 * lc2 * s12,
    ])
    return cor, grav


def foot(p, y, q1, q2):
    l1, l2 = p["l1"], p["l2"]
    x = l1 * np.sin(q1) + l2 * np.sin(q1 + q2)
    z = y - l1 * np.cos(q1) - l2 * np.cos(q1 + q2)
    J = np.array([[0.0, l1 * np.cos(q1) + l2 * np.cos(q1 + q2), l2 * np.cos(q1 + q2)],
                  [1.0, l1 * np.sin(q1) + l2 * np.sin(q1 + q2), l2 * np.sin(q1 + q2)]])
    return x, z, J


def decompose(p, Q, dQ, ddQ, lam, Jtrain, gtrain):
    """Effective external torque on unit j split into the brief's four classes.

    Local unit EOM: Jtrain_j ddq_j + tau_grav_train_j(q_j) - tau_ext_eff_j = S_j u_j
    (friction/damping identical in both and omitted).  Returns per-joint dict.
    """
    y, q1, q2 = Q
    M = mass_matrix(p, q1, q2)
    cor, grav = bias(p, q1, q2, dQ[1], dQ[2])
    _, _, J = foot(p, y, q1, q2)
    tc = J.T @ lam
    out = {}
    for j in (1, 2):
        others = [k for k in range(3) if k != j]
        t_inert = -sum(M[j, k] * ddQ[k] for k in others)          # from other coords
        t_self = -(M[j, j] - Jtrain[j]) * ddQ[j]                  # inertia mismatch
        t_cor = -cor[j]
        t_grav = -(grav[j] - gtrain[j])
        t_con = tc[j]
        out[j] = dict(inertial=t_inert, self_inertia=t_self, coriolis=t_cor,
                      grav=t_grav, contact=t_con)
    return out, M, cor, grav, tc


def check_identity(p, rng):
    """tau_j from full EOM must equal local-unit EOM with tau_ext_eff."""
    worst = 0.0
    for _ in range(2000):
        Q = np.array([0.4, rng.uniform(-1, 1), rng.uniform(0.1, 2.0)])
        dQ, ddQ, lam = rng.normal(0, 3, 3), rng.normal(0, 30, 3), rng.normal(0, 20, 2)
        Jtrain = {1: rng.uniform(0.01, 0.05), 2: rng.uniform(0.003, 0.01)}
        gtrain = {1: rng.normal(), 2: rng.normal()}
        comp, M, cor, grav, tc = decompose(p, Q, dQ, ddQ, lam, Jtrain, gtrain)
        tau_full = M @ ddQ + cor + grav - tc
        for j in (1, 2):
            tau_local = Jtrain[j] * ddQ[j] + gtrain[j] - sum(comp[j].values())
            worst = max(worst, abs(tau_full[j] - tau_local))
    return worst


def tracking_cell(p, f, A1=0.6, A2=0.5, q20=1.0):
    """Fixed base (ddy = 0), sinusoidal hip/knee, phase 90 deg.  Units trained on own
    rigid link with fixed housing: Jtrain = M_jj at q2 = q20, gravity at nominal housing."""
    t = np.linspace(0, 2 / f, 2001)
    w = 2 * np.pi * f
    q1, dq1, ddq1 = A1 * np.sin(w * t), A1 * w * np.cos(w * t), -A1 * w ** 2 * np.sin(w * t)
    q2 = q20 + A2 * np.sin(w * t + np.pi / 2)
    dq2 = A2 * w * np.cos(w * t + np.pi / 2)
    ddq2 = -A2 * w ** 2 * np.sin(w * t + np.pi / 2)
    M0 = mass_matrix(p, 0.0, q20)
    Jtrain = {1: M0[1, 1], 2: M0[2, 2]}
    res = {1: {}, 2: {}}
    for i in range(len(t)):
        _, grav = bias(p, q1[i], q2[i], 0, 0)
        # unit 1 trained as rigid link with frozen knee at q20 (gravity phase fixed);
        # unit 2 trained with housing fixed at q1 = 0.
        gtr = {1: G * ((p["m1"] * p["lc1"] + p["m2"] * p["l1"]) * np.sin(q1[i])
                       + p["m2"] * p["lc2"] * np.sin(q1[i] + q20)),
               2: G * p["m2"] * p["lc2"] * np.sin(q2[i])}
        comp, *_ = decompose(p, np.array([0.5, q1[i], q2[i]]), np.array([0, dq1[i], dq2[i]]),
                             np.array([0, ddq1[i], ddq2[i]]), np.zeros(2), Jtrain, gtr)
        for j in (1, 2):
            for k, v in comp[j].items():
                res[j][k] = max(res[j].get(k, 0.0), abs(v))
        # total required motor torque fraction
        M = mass_matrix(p, q1[i], q2[i])
        cor, grv = bias(p, q1[i], q2[i], dq1[i], dq2[i])
        tau = M[1:, 1:] @ np.array([ddq1[i], ddq2[i]]) + cor[1:] + grv[1:]
        for j in (1, 2):
            res[j]["u_req"] = max(res[j].get("u_req", 0.0), abs(tau[j - 1]))
    S = {1: p["S1"], 2: p["S2"]}
    return {j: {k: round(v / S[j], 3) for k, v in res[j].items()} for j in (1, 2)}


def squat_static(p, q2):
    """Foot pinned under hip (x_foot = 0), zero horizontal foot force (lam_x = 0),
    static.  Returns joint torques / S_max and the 1-D internal-force null direction."""
    # choose q1 s.t. foot directly below hip
    l1, l2 = p["l1"], p["l2"]
    q1 = -np.arctan2(l2 * np.sin(q2), l1 + l2 * np.cos(q2))
    _, grav = bias(p, q1, q2, 0, 0)
    _, _, J = foot(p, 0.5, q1, q2)
    # y-row: grav_y = lam_z  (J[1,0] = 1, J[0,0] = 0)
    lam = np.array([0.0, grav[0]])
    tau = grav[1:] - (J.T @ lam)[1:]
    null = -J[0, 1:]  # torque change per unit lam_x
    return q1, tau / np.array([p["S1"], p["S2"]]), null / np.array([p["S1"], p["S2"]])


def landing_cell(p, h, k=2.0e4, c=150.0, kp=None, dt=1e-4, T=0.5):
    """Drop from foot clearance h with joint PD hold (stand-in for frozen units),
    compliant ground (vertical spring-damper, horizontal viscous pin).  Peak
    contact torque per joint (5 ms substep peak and 20 ms control-interval mean)."""
    q1s, q2s = -0.5, 1.0
    _, _, _ = foot(p, 0, q1s, q2s)
    y0 = p["l1"] * np.cos(q1s) + p["l2"] * np.cos(q1s + q2s) + h
    Q = np.array([y0, q1s, q2s])
    dQ = np.zeros(3)
    xf0 = None
    S = np.array([p["S1"], p["S2"]])
    Kp = np.array([60.0, 40.0]) if kp is None else kp
    Kd = 0.08 * Kp
    tcon = []
    for i in range(int(T / dt)):
        M = mass_matrix(p, Q[1], Q[2])
        cor, grav = bias(p, Q[1], Q[2], dQ[1], dQ[2])
        xf, zf, J = foot(p, *Q)
        vf = J @ dQ
        lam = np.zeros(2)
        if zf < 0:
            if xf0 is None:
                xf0 = xf
            lam[1] = max(0.0, -k * zf - c * vf[1])
            lam[0] = np.clip(-3000.0 * vf[0] - 2e4 * (xf - xf0), -0.8 * lam[1], 0.8 * lam[1])
        else:
            xf0 = None
        u = np.clip(Kp * (np.array([q1s, q2s]) - Q[1:]) - Kd * dQ[1:] + grav[1:] * 0.0, -S, S)
        tau = np.concatenate([[0.0], u])
        tc = J.T @ lam
        ddQ = np.linalg.solve(M, tau + tc - cor - grav)
        dQ = dQ + dt * ddQ
        Q = Q + dt * dQ
        tcon.append(tc[1:].copy())
    tcon = np.abs(np.array(tcon))
    n5, n20 = int(5e-3 / dt), int(20e-3 / dt)
    pk5 = np.max(np.array([tcon[i:i + n5].mean(0) for i in range(0, len(tcon) - n5, n5)]), 0)
    pk20 = np.max(np.array([tcon[i:i + n20].mean(0) for i in range(0, len(tcon) - n20, n20)]), 0)
    return {"peak_5ms": np.round(pk5 / S, 2).tolist(), "peak_20ms": np.round(pk20 / S, 2).tolist()}


def null_mode_demo(inconsistent=0.0, leak_T=None, T=4.0, dt=1e-3):
    """Two PI joint servos on a 1-DoF closed chain (linearised, unit inertia on the
    manifold coordinate s, Jacobian phi = (1, -0.5)).  Returns internal-force proxy
    w = phi2*I1 - phi1*I2 at t = T."""
    phi = np.array([1.0, -0.5])
    kp, kd, ki = 50.0, 5.0, 40.0
    s, ds, I = 0.0, 0.0, np.zeros(2)
    qstar = phi * 0.2 + np.array([0.0, inconsistent])
    hist = []
    for _ in range(int(T / dt)):
        e = qstar - phi * s
        de = -phi * ds
        tau = kp * e + kd * de + ki * I
        dds = phi @ tau
        ds += dt * dds
        s += dt * ds
        I += dt * (e - (I / leak_T if leak_T else 0.0))
        hist.append(ki * (phi[1] * I[0] - phi[0] * I[1]))
    return float(hist[len(hist) // 2]), float(hist[-1])


def main():
    rng = np.random.default_rng(20261023)
    p = leg()
    out = {"identity_residual_max": check_identity(p, rng)}
    out["tracking"] = {f"f={f}Hz": tracking_cell(p, f) for f in (0.5, 1.0, 2.0, 3.0)}
    sq = {}
    for mp in (0.0, 1.0, 2.0, 3.0):
        pp = leg(mp=mp)
        q1, tau, null = squat_static(pp, 1.2)
        sq[f"payload={mp}kg"] = {"q1": round(float(q1), 3), "u_hip_knee": np.round(tau, 3).tolist(),
                                 "null_dir_per_N": np.round(null, 4).tolist()}
    out["squat_q2=1.2"] = sq
    out["landing"] = {f"h={h}m": landing_cell(p, h) for h in (0.05, 0.10, 0.15)}
    out["null_mode"] = {
        "consistent_pure_I": null_mode_demo(0.0),
        "inconsistent_0.02rad_pure_I": null_mode_demo(0.02),
        "inconsistent_0.02rad_leak_0.48s": null_mode_demo(0.02, leak_T=0.48),
    }
    json.dump(out, sys.stdout, indent=1, default=float)


if __name__ == "__main__":
    main()
