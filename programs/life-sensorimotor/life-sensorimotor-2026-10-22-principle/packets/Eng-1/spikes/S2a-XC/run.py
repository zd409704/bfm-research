#!/usr/bin/env python3
"""S2a-XC spike harness, per PLAN.md v2. numpy only. Usage: python3 -I run.py [--smoke]"""
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from xcstats import cp_lower, cp_upper, dbits  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUT = os.path.join(HERE, "smoke_out") if SMOKE else HERE
os.makedirs(os.path.join(OUT, "floor-cert"), exist_ok=True)
LOG = open(os.path.join(OUT, "run.log"), "w")


def log(*a):
    s = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    LOG.write(s + "\n")
    LOG.flush()
    print(s, flush=True)


# ---------------- fixture constants (PLAN §2) ----------------
L1, L2, M1, M2 = 0.3, 0.25, 1.5, 1.0
LC1, LC2 = L1 / 2, L2 / 2
I1, I2 = M1 * L1**2 / 12, M2 * L2**2 / 12
KP = np.array([60.0, 40.0])
KD = np.array([4.0, 3.0])
SAT = 8.0
Q0 = np.array([0.5, 1.0])
NSTEP, WIN0 = 400, 300  # export steps 0..400, window starts at 300
SIG_Q, SIG_QD, SIG_E = 1e-4, 1e-3, 0.02
KG = 10.0
DS = [5, 10, 20, 50]
MS = [2, 5, 10]
CLASSES = [(d, m) for d in DS for m in MS]
RW = [0.001, 0.005]
Q_GRID = [0.90, 0.95]
ALPHA = 0.05
N_CAL = 4000 if SMOKE else 40000
N_NEG = 400 if SMOKE else 4000
N_POS = 200 if SMOKE else 2000
N_NULL = 50 if SMOKE else 500
N_SUB = 100 if SMOKE else 1000
SEEDS = [0, 1, 2]
SUB_SEED = 100
CHUNK = 2000

# channel: (Tsteps, source, gain)
CHANNELS = {
    "R1_CMD": (5, "cmd", 50.0), "R2_CMD": (20, "cmd", 12.5),
    "R1_REAL_DOWN": (5, "down", 50.0), "R1_REAL_UP": (5, "up", 50.0),
    "R2_REAL_DOWN": (20, "down", 12.5), "R2_REAL_UP": (20, "up", 12.5),
    "ORACLE_R1": (5, "oracle", 0.0),
    "R2_CMD_g50": (20, "cmd", 50.0), "R2_REAL_DOWN_g50": (20, "down", 50.0),
    "R2_REAL_UP_g50": (20, "up", 50.0),
    "R1_CMD_g12.5": (5, "cmd", 12.5), "R1_REAL_DOWN_g12.5": (5, "down", 12.5),
    "R1_REAL_UP_g12.5": (5, "up", 12.5),
}
MAIN = ["R1_CMD", "R2_CMD", "R1_REAL_DOWN", "R1_REAL_UP", "R2_REAL_DOWN",
        "R2_REAL_UP", "ORACLE_R1"]
SENS = [c for c in CHANNELS if c not in MAIN]


def nwin(ch):
    return 100 // CHANNELS[ch][0]


def tms(ch):
    return CHANNELS[ch][0]


def massmat(q1, q2):
    c2 = np.cos(q2)
    m11 = M1 * LC1**2 + I1 + M2 * (L1**2 + LC2**2 + 2 * L1 * LC2 * c2) + I2
    m12 = M2 * (LC2**2 + L1 * LC2 * c2) + I2
    m22 = M2 * LC2**2 + I2 + 0 * c2
    h = M2 * L1 * LC2 * np.sin(q2)
    return m11, m12, m22, h


# ---------------- publisher (XC-0 export): read-only wrt plant ----------------
class Publisher:
    def __init__(self, n, rng):
        self.n = n
        self.noise = rng.standard_normal((NSTEP + 1, 4, n, 2))  # q, qd, effort, oracle-effort
        self.out = {c: np.zeros((n, nwin(c))) for c in CHANNELS}
        self.st = {}

    def publish(self, i, q, qd, tau_motor, tau_f, tau_ext, ref, refd):
        for a in (q, qd, tau_motor, tau_f, tau_ext, ref, refd):
            a.setflags(write=False)  # read-only views: a write would raise
        nz = self.noise[i]
        qs = q + SIG_Q * nz[0]
        qds = qd + SIG_QD * nz[1]
        ne = SIG_E * nz[2]
        m11, m12, m22, h = massmat(qs[:, 0], qs[:, 1])
        p = np.stack([m11 * qds[:, 0] + m12 * qds[:, 1],
                      m12 * qds[:, 0] + m22 * qds[:, 1]], 1)
        ctq = np.stack([0 * h, -h * qds[:, 0] * (qds[:, 0] + qds[:, 1])], 1)
        ucmd = np.clip(KP * (ref - qs) + KD * (refd - qds), -SAT, SAT)
        eff = {"cmd": ucmd, "down": tau_motor + ne, "up": tau_motor - tau_f + ne}
        for ch, (T, src, K) in CHANNELS.items():
            if i % T:
                continue
            if src == "oracle":
                s = np.linalg.norm(tau_ext + SIG_E * nz[3], axis=1)
            else:
                f = eff[src] + ctq
                Ts = T * 1e-3
                if i == 0:
                    self.st[ch] = [p.copy(), np.zeros_like(p), f.copy()]
                    continue
                phat, r, fprev = self.st[ch]
                phat = phat + Ts * (fprev + r)
                r = K * (p - phat)
                self.st[ch] = [phat, r, f.copy()]
                s = np.linalg.norm(r, axis=1)
            if i > WIN0 and (i - WIN0) % T == 0:
                self.out[ch][:, (i - WIN0) // T - 1] = s


def simulate(n, plant_rng, Mmag, dms, publisher=None, sens_rng=None, record=False):
    """Vectorised batch of n episodes. Plant RNG only drawn here (up front)."""
    # --- plant/episode parameters (plant stream only) ---
    fr = plant_rng.uniform(0.2, 1.5, (n, 2, 3))
    ph = plant_rng.uniform(0, 2 * np.pi, (n, 2, 3))
    bias = plant_rng.uniform(-0.1, 0.1, (n, 2))
    rn = plant_rng.integers(2, 7, (n, 2))
    rph = plant_rng.uniform(0, 2 * np.pi, (n, 2))
    sloc = plant_rng.uniform(0.4, 1.0, n)
    ang = plant_rng.uniform(0, 2 * np.pi, n)
    onset = plant_rng.integers(30, 61, n)
    onset_step = WIN0 + onset
    Fx, Fy = np.cos(ang), np.sin(ang)

    def refs(t):
        a = 0.1
        w = 2 * np.pi * fr
        ref = Q0 + (a * np.sin(w * t + ph)).sum(2)
        refd = (a * w * np.cos(w * t + ph)).sum(2)
        return ref, refd

    ref0, refd0 = refs(0.0)
    q, qd = ref0.copy(), refd0.copy()
    dt = 1e-3
    traj = [] if record else None
    for i in range(NSTEP + 1):
        t = i * dt
        ref, refd = refs(t)
        tau_cmd = np.clip(KP * (ref - q) + KD * (refd - qd), -SAT, SAT)
        ripple = 0.15 * np.sin(rn * KG * (q - Q0) + rph)
        tau_motor = tau_cmd + ripple + bias
        tau_f = 0.2 * np.tanh(qd / 0.01) + 0.05 * qd
        # contact
        trel = (i - onset_step) * dt * 1e3  # ms since onset
        d = dms
        rise = np.where((trel >= 0) & (trel < 2), 0.5 * (1 - np.cos(np.pi * trel / 2)), 0.0)
        plat = np.where((trel >= 2) & (trel <= d - 2), 1.0, 0.0)
        fall = np.where((trel > d - 2) & (trel <= d), 0.5 * (1 + np.cos(np.pi * (trel - (d - 2)) / 2)), 0.0)
        mag = Mmag * (rise + plat + fall)
        s1, c1 = np.sin(q[:, 0]), np.cos(q[:, 0])
        s12, c12 = np.sin(q[:, 0] + q[:, 1]), np.cos(q[:, 0] + q[:, 1])
        fx, fy = mag * Fx, mag * Fy
        tau_ext = np.stack([
            -(L1 * s1 + sloc * L2 * s12) * fx + (L1 * c1 + sloc * L2 * c12) * fy,
            -sloc * L2 * s12 * fx + sloc * L2 * c12 * fy], 1)
        if publisher is not None:
            publisher.publish(i, q, qd, tau_motor, tau_f, tau_ext, ref, refd)
        if record:
            traj.append(np.concatenate([q, qd, tau_cmd], 1))
        if i == NSTEP:
            break
        m11, m12, m22, h = massmat(q[:, 0], q[:, 1])
        cqd = np.stack([-h * qd[:, 1] * (2 * qd[:, 0] + qd[:, 1]), h * qd[:, 0] ** 2], 1)
        rhs = tau_motor - tau_f + tau_ext - cqd
        det = m11 * m22 - m12**2
        qdd = np.stack([(m22 * rhs[:, 0] - m12 * rhs[:, 1]) / det,
                        (-m12 * rhs[:, 0] + m11 * rhs[:, 1]) / det], 1)
        qd = qd + dt * qdd
        q = q + dt * qd
    return onset, (np.array(traj) if record else None)


def run_set(domain, seed, key, n, Mmag, dms):
    """Chunked generation; returns {ch: (n,nw)} and onsets."""
    outs = {c: [] for c in CHANNELS}
    ons = []
    for ci, a in enumerate(range(0, n, CHUNK)):
        b = min(n, a + CHUNK)
        ss = np.random.SeedSequence([domain, seed, key, ci])
        pr, sr = [np.random.default_rng(s) for s in ss.spawn(2)]
        m = np.broadcast_to(np.asarray(Mmag, float), (n,))[a:b]
        d = np.broadcast_to(np.asarray(dms, float), (n,))[a:b]
        pub = Publisher(b - a, sr)
        on, _ = simulate(b - a, pr, m, d, publisher=pub)
        for c in CHANNELS:
            outs[c].append(pub.out[c])
        ons.append(on)
    return {c: np.concatenate(v) for c, v in outs.items()}, np.concatenate(ons)


# ---------------- detector ----------------
def cusum(s, drift):
    c = np.zeros_like(s)
    prev = np.zeros(s.shape[0])
    for k in range(s.shape[1]):
        prev = np.maximum(0.0, prev + s[:, k] - drift)
        c[:, k] = prev
    return c


def first_cross(s, drift, thr):
    c = cusum(s, drift)
    hit = c > thr
    idx = np.where(hit.any(1), hit.argmax(1), -1)
    return idx


def calibrate(cal):
    det = {}
    for ch in CHANNELS:
        s = cal[ch]
        drift = float(np.median(s))
        m = np.sort(cusum(s, drift).max(1))[::-1]
        det[ch] = {"drift": drift}
        for r in RW:
            ks = 0
            # largest k with CP upper(k, N, .975) <= 0.25 r
            while cp_upper(ks + 1, len(m), ALPHA / 2) <= 0.25 * r:
                ks += 1
            if cp_upper(0, len(m), ALPHA / 2) > 0.25 * r:
                ks = -1  # even k=0 not conservative enough
            kk = max(ks, 0)
            det[ch][r] = {"thr": float(m[kk]), "kstar": ks,
                          "cal_exceed": int((m > m[kk]).sum())}
    return det


def fl(x):
    if isinstance(x, float) and math.isinf(x):
        return "inf"
    if isinstance(x, (np.floating, float)):
        return round(float(x), 10)
    return x


def pipeline():
    t0 = time.time()
    R = {"config": {"N_CAL": N_CAL, "N_NEG": N_NEG, "N_POS": N_POS, "N_NULL": N_NULL,
                    "N_SUB": N_SUB, "smoke": SMOKE}}
    # --- calibration ---
    cal, _ = run_set(1, 0, 0, N_CAL, 0.0, 10.0)
    det = calibrate(cal)
    del cal
    R["calibration"] = {ch: {"drift": fl(v["drift"]),
                             **{f"r{r}": {k: fl(x) for k, x in v[r].items()} for r in RW}}
                        for ch, v in det.items()}
    log("calibrated", round(time.time() - t0, 1), "s")

    def alarms(stats, onsets):
        """-> {(ch,r): (idx array)}"""
        return {(ch, r): first_cross(stats[ch], det[ch]["drift"], det[ch][r]["thr"])
                for ch in CHANNELS for r in RW}

    # --- negatives and null (pooled counts) ---
    neg_cnt = {(c, r): 0 for c in CHANNELS for r in RW}
    null_cnt = {(c, r): 0 for c in CHANNELS for r in RW}
    n_neg = n_null = 0
    for sd in SEEDS:
        st, on = run_set(2, sd, 0, N_NEG, 0.0, 10.0)
        al = alarms(st, on)
        for k, v in al.items():
            neg_cnt[k] += int((v >= 0).sum())
        n_neg += N_NEG
        for ci, (d, m) in enumerate(CLASSES):
            st, on = run_set(4, sd, ci, N_NULL, 0.0, float(d))
            al = alarms(st, on)
            for k, v in al.items():
                null_cnt[k] += int((v >= 0).sum())
            n_null += N_NULL
        log("neg/null seed", sd, round(time.time() - t0, 1), "s")
    # --- positives ---
    pos = {}  # (ch,r,class_idx) -> lists per seed of (detect_flag, lat_ms, pre_flag)
    for sd in SEEDS:
        for ci, (d, m) in enumerate(CLASSES):
            st, on = run_set(3, sd, ci, N_POS, float(m), float(d))
            al = alarms(st, on)
            for (ch, r), idx in al.items():
                cross = np.where(idx >= 0, (idx + 1) * tms(ch), -1)
                pre = (idx >= 0) & (cross < on)
                dete = (idx >= 0) & (cross >= on)
                lat = np.where(dete, cross - on, np.inf)
                pos.setdefault((ch, r, ci), []).append((dete, lat, pre))
        log("pos seed", sd, round(time.time() - t0, 1), "s")
    # --- subset-definition split ---
    sub = {}
    for ci, (d, m) in enumerate(CLASSES):
        st, on = run_set(5, SUB_SEED, ci, N_SUB, float(m), float(d))
        al = alarms(st, on)
        for (ch, r), idx in al.items():
            cross = np.where(idx >= 0, (idx + 1) * tms(ch), -1)
            sub[(ch, r, ci)] = float(((idx >= 0) & (cross >= on)).mean())
    log("subset", round(time.time() - t0, 1), "s")

    # --- certificates / metrics ---
    NB = len(MAIN) * len(CLASSES) * len(RW)
    ab = ALPHA / NB
    metrics = {}
    certs = {}
    for ch in CHANNELS:
        for r in RW:
            did = f"{ch}@r{r}"
            nfp = neg_cnt[(ch, r)]
            fpr_hat = nfp / n_neg
            fpr_u = cp_upper(nfp, n_neg, ALPHA / 2)
            fpr_ub = cp_upper(nfp, n_neg, ab / 2)
            cl = []
            for ci, (d, m) in enumerate(CLASSES):
                dete = np.concatenate([x[0] for x in pos[(ch, r, ci)]])
                lat = np.concatenate([x[1] for x in pos[(ch, r, ci)]])
                pre = np.concatenate([x[2] for x in pos[(ch, r, ci)]])
                n = len(dete)
                k = int(dete.sum())
                tpr_l = cp_lower(k, n, ALPHA / 2)
                tpr_lb = cp_lower(k, n, ab / 2)
                ls = np.sort(lat)
                p95 = float(ls[int(math.ceil(0.95 * (n - 1)))])
                seeds_tpr = [float(x[0].mean()) for x in pos[(ch, r, ci)]]
                e = {
                    "d_ms": d, "M_N": m, "n_pos": n, "tpr_hat": k / n, "tpr_L": tpr_l,
                    "fpr_hat": fpr_hat, "fpr_U": fpr_u,
                    "d_cert_bits": dbits(tpr_l, fpr_u),
                    "d_cert_bits_bonferroni": dbits(tpr_lb, fpr_ub),
                    "p95_latency_ms": p95, "pre_onset_alarm_rate": float(pre.mean()),
                    "tpr_per_seed": seeds_tpr,
                    "meets": {f"q{q}": bool(tpr_l >= q and fpr_u <= r) for q in Q_GRID},
                    "meets_bonferroni": {f"q{q}": bool(tpr_lb >= q and fpr_ub <= r) for q in Q_GRID},
                    "subset_split_tpr": sub[(ch, r, ci)],
                }
                cl.append(e)
            metrics[did] = cl
            nn = null_cnt[(ch, r)]
            certs[did] = {
                "detector_id": did, "channel": ch, "r_w": r,
                "r_per_s_registered_equiv": r / 0.1,
                "placeholder_qr": True, "alpha": ALPHA, "coverage": "pointwise",
                "bonferroni_alpha": ab, "plan": "PLAN.md v2",
                "lemma_status": "C-Eng1-A-01 Candidate; design lemma only; certificate invalid if lemma fails",
                "log_base": 2, "n_neg": n_neg, "neg_alarms": nfp,
                "null_alarms": nn, "n_null": n_null,
                "null_alarm_rate": nn / n_null,
                "scope_flags": (["outside_C-P1-012_premise5_scope"] if channel_up(ch) else []),
                "classes": [{k2: (fl(v) if not isinstance(v, (dict, list)) else
                                  ([fl(z) for z in v] if isinstance(v, list) else v))
                             for k2, v in e.items()} for e in cl],
            }

    # --- H2 (coverage) ---
    DET_MAIN = [(c, r) for c in MAIN for r in RW]
    lvl = ALPHA / len(DET_MAIN)
    h2 = {}
    h2ok = True
    for (c, r) in DET_MAIN:
        lo = cp_lower(null_cnt[(c, r)], n_null, lvl)
        ok = lo <= r
        h2ok &= ok
        h2[f"{c}@r{r}"] = {"null_alarms": null_cnt[(c, r)], "n": n_null,
                           "cp_lower": lo, "r_w": r, "ok": bool(ok)}
    # --- H3 ---
    h3 = {}
    h3ok = True
    for ci, (d, m) in enumerate(CLASSES):
        if d >= 10 and m == 10:
            e = metrics["ORACLE_R1@r0.001"][ci]
            ok = bool(e["meets"]["q0.95"])
            h3ok &= ok
            h3[f"d{d}_M{m}"] = {"tpr_L": e["tpr_L"], "fpr_U": e["fpr_U"], "ok": ok}
    # --- contrasts ---
    def cm(ch, ci):
        return metrics[f"{ch}@r0.001"][ci]

    def match(ref, alt, ci):
        a, b = cm(ref, ci), cm(alt, ci)
        dt = abs(a["tpr_hat"] - b["tpr_hat"])
        pa, pb = a["p95_latency_ms"], b["p95_latency_ms"]
        if math.isinf(pa) and math.isinf(pb):
            lm, lni = True, True
        elif math.isinf(pa) or math.isinf(pb):
            lm, lni = False, (math.isinf(pa))
        else:
            lm, lni = abs(pa - pb) <= 10, pb <= pa + 10
        return {"d_ms": a["d_ms"], "M_N": a["M_N"], "ref_tpr": a["tpr_hat"], "alt_tpr": b["tpr_hat"],
                "abs_dTPR": dt, "ref_p95": pa, "alt_p95": pb,
                "match": bool(dt <= 0.05 and lm),
                "noninferior": bool(b["tpr_hat"] >= a["tpr_hat"] - 0.05 and lni)}

    def contrast(ref, alt):
        rows = [match(ref, alt, ci) for ci in range(len(CLASSES))]
        idc = [ci for ci in range(len(CLASSES)) if sub[(ref, 0.001, ci)] >= 0.5]
        big = [ci for ci, (d, m) in enumerate(CLASSES) if d >= 10]
        return {
            "ref": ref, "alt": alt, "classes": [{k: fl(v) for k, v in x.items()} for x in rows],
            "counterexample_all_d_ge_10": bool(all(rows[ci]["match"] for ci in big)),
            "counterexample_noninferior_all_d_ge_10": bool(all(rows[ci]["noninferior"] for ci in big)),
            "identifiable_classes": [f"d{CLASSES[ci][0]}_M{CLASSES[ci][1]}" for ci in idc],
            "counterexample_identifiable_only": (bool(all(rows[ci]["match"] for ci in idc)) if idc else None),
            "n_classes_matching_d_ge_10": int(sum(rows[ci]["match"] for ci in big)),
        }

    con = {}
    for pl in ("DOWN", "UP"):
        ref = f"R1_REAL_{pl}"
        e = contrast(ref, "R1_CMD")
        rr = contrast(ref, f"R2_REAL_{pl}")
        idc = [ci for ci in range(len(CLASSES)) if sub[(ref, 0.001, ci)] >= 0.5]
        drops = [cm(ref, ci)["tpr_hat"] - cm("R1_CMD", ci)["tpr_hat"] for ci in idc]
        subst = {
            "identifiable_classes": e["identifiable_classes"],
            "drops": {f"d{CLASSES[ci][0]}_M{CLASSES[ci][1]}": fl(x) for ci, x in zip(idc, drops)},
            "min_drop": (fl(min(drops)) if drops else None),
            "mean_drop": (fl(float(np.mean(drops))) if drops else None),
            "substitution_drop_met": (bool(all(x > 0.10 for x in drops)) if drops else None),
            "policy": "recalibrate threshold on substituted channel, same r_w",
            "message_if_not_met": "role not realized by that channel on this fixture, detector and calibration; NOT proof that effort information is absent",
        }
        con[pl] = {"reference": ref, "factorE": e, "factorR": rr, "substitution": subst,
                   "scope_flags": (["outside_C-P1-012_premise5_scope"] if pl == "UP" else []),
                   "cmd_recon_shared_baseline": True}
    sens = {}
    for pl in ("DOWN", "UP"):
        sens[f"R2_g50_vs_R1_REAL_{pl}(FactorR,gain.T=1.0)"] = contrast(f"R1_REAL_{pl}", f"R2_REAL_{pl}_g50")
        sens[f"R2_REAL_{pl}(g12.5)_vs_R1_REAL_{pl}_g12.5(FactorR,matched-bw)"] = contrast(
            f"R1_REAL_{pl}_g12.5", f"R2_REAL_{pl}")
        sens[f"R1_CMD_g12.5_vs_R1_REAL_{pl}_g12.5(FactorE,matched-bw)"] = contrast(
            f"R1_REAL_{pl}_g12.5", "R1_CMD_g12.5")
    # A02
    prim = metrics["R1_REAL_DOWN@r0.001"]
    a02_rows = {f"d{d}_M{m}": bool(prim[ci]["meets"]["q0.9"]) for ci, (d, m) in enumerate(CLASSES)
                if d >= 10 and m == 10}
    R["A02"] = {"cell": "R1_REAL_DOWN@r0.001", "per_class_meets_q0.9": a02_rows,
                "met": bool(all(a02_rows.values()))}
    R["H2"] = {"ok": bool(h2ok), "detectors": h2,
               "null_dcert_info": {k: max(e["d_cert_bits"] for e in v) for k, v in
                                   ((f"{c}@r{r}", metrics[f"{c}@r{r}"]) for c, r in DET_MAIN)}}
    R["H3"] = {"ok": bool(h3ok), "classes": h3}
    R["contrasts"] = con
    R["sensitivity"] = sens
    R["certs"] = certs
    R["neg_counts"] = {f"{c}@r{r}": v for (c, r), v in neg_cnt.items()}
    R["runtime_s_note"] = "see run.log"
    log("pipeline done", round(time.time() - t0, 1), "s")
    return R


def channel_up(ch):
    return "_UP" in ch


def h4_noninterference():
    ok = True
    details = []
    for rep in range(1):
        n = 50
        ss = np.random.SeedSequence([9, 0, rep])
        rngs = ss.spawn(4)
        cls = np.random.default_rng(rngs[0]).integers(0, len(CLASSES), n)
        Mv = np.array([CLASSES[c][1] for c in cls], float)
        Mv[::5] = 0.0
        dv = np.array([CLASSES[c][0] for c in cls], float)
        on_a, tr_a = simulate(n, np.random.default_rng(rngs[1]), Mv, dv,
                              publisher=Publisher(n, np.random.default_rng(rngs[2])), record=True)
        on_b, tr_b = simulate(n, np.random.default_rng(rngs[1]), Mv, dv, publisher=None, record=True)
        same = bool(np.array_equal(tr_a, tr_b) and np.array_equal(on_a, on_b))
        ok &= same
        details.append({"episodes": n, "trajectories_bitwise_identical": same,
                        "compared": "q, qd, tau_cmd at 1 kHz, 401 steps"})
    return {"ok": bool(ok), "details": details}


def main():
    plan_sha = hashlib.sha256(open(os.path.join(HERE, "PLAN.md"), "rb").read()).hexdigest()
    sealed = open(os.path.join(HERE, "PLAN.sha256")).read().split()[0]
    log("plan sha256", plan_sha, "sealed ok" if plan_sha == sealed else "MISMATCH")
    if plan_sha != sealed and not SMOKE:
        raise SystemExit("PLAN hash mismatch")
    log("Bypassed Grade-3 edges: E05/E06 (S0a->S2a), E08/E09 (S1->S2a), E14 (S0b->S2a); "
        "E10/E11 (S2a->S1) listed, not bypassed; E17 Reading P not invoked. None used as gate.")
    h4 = h4_noninterference()
    log("H4", h4["ok"])
    R1 = pipeline()
    R1["H4"] = h4
    R1["plan_sha256"] = plan_sha
    b1 = json.dumps(R1, sort_keys=True, indent=1).encode()
    with open(os.path.join(OUT, "results.json"), "wb") as f:
        f.write(b1)
    log("running pipeline a second time for H1")
    R2 = pipeline()
    R2["H4"] = h4
    R2["plan_sha256"] = plan_sha
    b2 = json.dumps(R2, sort_keys=True, indent=1).encode()
    h1 = hashlib.sha256(b1).hexdigest() == hashlib.sha256(b2).hexdigest()
    log("H1 determinism", h1, hashlib.sha256(b1).hexdigest())
    R = R1
    for did, c in R["certs"].items():
        with open(os.path.join(OUT, "floor-cert", did.replace("@", "_") + ".json"), "w") as f:
            json.dump(c, f, indent=1, sort_keys=True)
    with open(os.path.join(OUT, "contrasts.json"), "w") as f:
        json.dump(R["contrasts"], f, indent=1, sort_keys=True)
    with open(os.path.join(OUT, "sensitivity_fixedgain.json"), "w") as f:
        json.dump(R["sensitivity"], f, indent=1, sort_keys=True)

    H = {"H1": h1, "H2": R["H2"]["ok"], "H3": R["H3"]["ok"], "H4": R["H4"]["ok"]}
    harness = all(H.values())
    a02 = R["A02"]["met"]
    fired = [k for k, v in H.items() if not v]
    if harness and not a02:
        fired.append("A02")
    for pl in ("DOWN", "UP"):
        c = R["contrasts"][pl]
        if c["factorE"]["counterexample_all_d_ge_10"]:
            fired.append(f"FE_{pl}")
        if c["factorR"]["counterexample_all_d_ge_10"]:
            fired.append(f"FR_{pl}")
        if c["substitution"]["substitution_drop_met"] is False:
            fired.append(f"SUB_{pl}_NOT_MET")
    verdict = "INVALID" if not harness else ("PASS" if a02 else "FAIL")
    V = {
        "verdict": verdict, "harness_pass": harness, **H, "A02": a02,
        "criteria_fired": fired,
        "criteria_fired_note": "H*/A02 decide the verdict; FE_*/FR_*/SUB_* are informational C-P1-012 data flags",
        "factorE_counterexample_DOWN": R["contrasts"]["DOWN"]["factorE"]["counterexample_all_d_ge_10"],
        "factorE_counterexample_UP": R["contrasts"]["UP"]["factorE"]["counterexample_all_d_ge_10"],
        "factorR_counterexample_DOWN": R["contrasts"]["DOWN"]["factorR"]["counterexample_all_d_ge_10"],
        "factorR_counterexample_UP": R["contrasts"]["UP"]["factorR"]["counterexample_all_d_ge_10"],
        "substitution_drop_DOWN": R["contrasts"]["DOWN"]["substitution"],
        "substitution_drop_UP": R["contrasts"]["UP"]["substitution"],
        "placeholder_qr": True, "plan_sha256": plan_sha, "results_sha256": hashlib.sha256(b1).hexdigest(),
        "claim_grade_changes": "none (runner files data only)",
        "scope": "harness validity only; no hardware transfer",
        "bypassed_edges": {"bypassed": ["E05", "E06", "E08", "E09", "E14"],
                           "listed_not_bypassed": ["E10", "E11"], "not_invoked": ["E17-ReadingP"]},
        "smoke": SMOKE,
    }
    with open(os.path.join(OUT, "VERDICT.json"), "w") as f:
        json.dump(V, f, indent=1, sort_keys=True)
    write_metrics(R, V)
    log("VERDICT", verdict, fired)


def write_metrics(R, V):
    L = ["# METRICS — S2a-XC spike (PLAN v2)", "",
         f"Verdict: **{V['verdict']}** (harness_pass={V['harness_pass']}; A02={V['A02']}). "
         f"Fired: {', '.join(V['criteria_fired']) or 'none'}. Harness validity only; no claim grade changes. `(q, r)` is PLACEHOLDER.", "",
         "Units: `r_w = 0.001` per 100 ms window = registered 0.01 /s; `r_w = 0.005` = 0.05 /s. d_cert in bits. Coverage pointwise; Bonferroni fields in floor-cert/.", "",
         "## Harness", "", f"- H1 determinism: {V['H1']}", f"- H2 null coverage: {V['H2']}",
         f"- H3 oracle: {V['H3']}", f"- H4 non-interference: {V['H4']}", "",
         "## Calibration (thresholds/exceed counts)", ""]
    for ch in MAIN:
        c = R["calibration"][ch]
        L.append(f"- {ch}: drift={c['drift']}; r0.001: thr={c['r0.001']['thr']} k*={c['r0.001']['kstar']}; r0.005: thr={c['r0.005']['thr']} k*={c['r0.005']['kstar']}")
    L += ["", "## TPR_hat / TPR_L / p95 latency by class at r_w=0.001 (0.01/s), pooled 3 seeds", "",
          "| detector | " + " | ".join(f"d{d}M{m}" for d, m in CLASSES) + " |",
          "|---|" + "---|" * len(CLASSES)]
    for ch in MAIN:
        mt = R["certs"][f"{ch}@r0.001"]["classes"]
        L.append(f"| {ch} TPR | " + " | ".join(f"{e['tpr_hat']:.3f}" for e in mt) + " |")
        L.append(f"| {ch} d_cert bits | " + " | ".join(f"{e['d_cert_bits']:.2f}" for e in mt) + " |")
        L.append(f"| {ch} p95 ms | " + " | ".join(str(e['p95_latency_ms']) if isinstance(e['p95_latency_ms'], str) else f"{e['p95_latency_ms']:.0f}" for e in mt) + " |")
    L += ["", "FPR_U (r_w=0.001): " + ", ".join(
        f"{ch}={R['certs'][f'{ch}@r0.001']['classes'][0]['fpr_U']:.2e}" for ch in MAIN), ""]
    L += ["## Meets (pointwise), q=0.90/0.95 at own r_w=0.001 — count of 12 classes", ""]
    for ch in MAIN:
        cl = R["certs"][f"{ch}@r0.001"]["classes"]
        L.append(f"- {ch}: q0.90 {sum(e['meets']['q0.9'] for e in cl)}/12, q0.95 {sum(e['meets']['q0.95'] for e in cl)}/12; "
                 f"Bonferroni q0.90 {sum(e['meets_bonferroni']['q0.9'] for e in cl)}/12")
    L += ["", "## C-P1-012 contrasts (data only; no grade statement)", ""]
    for pl in ("DOWN", "UP"):
        c = R["contrasts"][pl]
        L.append(f"### Placement {pl} {'(outside C-P1-012 premise-5 scope)' if pl == 'UP' else '(primary)'}")
        L.append(f"- Factor-E counterexample (CMD_RECON@R1 matches REAL@R1 on all d>=10): **{c['factorE']['counterexample_all_d_ge_10']}** "
                 f"({c['factorE']['n_classes_matching_d_ge_10']}/9 classes match); identifiable-only: {c['factorE']['counterexample_identifiable_only']}")
        L.append(f"- Factor-R counterexample (REAL@R2 matches REAL@R1 on all d>=10): **{c['factorR']['counterexample_all_d_ge_10']}** "
                 f"({c['factorR']['n_classes_matching_d_ge_10']}/9 classes match); identifiable-only: {c['factorR']['counterexample_identifiable_only']}")
        s = c["substitution"]
        L.append(f"- B.9.3 substitution (identifiable={s['identifiable_classes']}): met={s['substitution_drop_met']}, min drop={s['min_drop']}, mean drop={s['mean_drop']}")
        L.append("")
    L += ["Caveats: rate contrast is confounded with observer bandwidth (gain.T fixed); sensitivity variants in sensitivity_fixedgain.json. "
          "CMD_RECON cells are shared baselines across placements. A small substitution drop is not proof that effort information is absent.", ""]
    with open(os.path.join(OUT, "METRICS.md"), "w") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    main()
