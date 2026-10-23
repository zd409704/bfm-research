#!/usr/bin/env python3
"""S0a spike per spikes/PLAN.md: latency sweep (fixture A) + LIP L* (fixture B)."""
import json, math, os
import numpy as np

A, B_ENV, D, UMAX = 10.0, 0.01, 1.0, 3.0
K = 200.0                       # Proposal B candidate gain
TAUS_MS = [2, 5, 8, 9.5, 10, 12, 15, 20]
SEEDS = [0, 1, 2]
SIGMA, LAG = 1e-4, 2e-3         # sensor noise, actuator lag (s)
DT, T_END, TS = 5e-5, 0.25, 1e-3  # integration step, episode, controller sample period


def run(tau, seed, sign, closed=True):
    rng = np.random.default_rng(seed * 10 + (sign > 0))
    onset = rng.uniform(0.0, 4e-3)           # off-grid onset (continuous)
    n = int(round(T_END / DT))
    k_tau = int(round(max(tau * 1e-3 - LAG - TS / 2, 0.0) / DT))  # tau = total effective latency: pure delay + actuator lag + mean ZOH hold
    xs = np.zeros(n + 1)
    x = ua = 0.0
    cmd = 0.0
    next_sample = 0.0
    for i in range(n):
        t = i * DT
        if closed and t >= next_sample - 1e-12:
            # sensor value delayed by effective latency tau, plus noise; ZOH hold
            xd = xs[max(i - k_tau, 0)] + rng.normal(0, SIGMA)
            cmd = float(np.clip(-K * xd, -UMAX, UMAX))
            next_sample += TS
        ua += DT * (cmd - ua) / LAG          # first-order actuator lag
        d = sign * D if t >= onset else 0.0
        x += DT * (A * x + ua + d)
        xs[i + 1] = x
    return float(np.max(np.abs(xs)))


def main():
    peaks = {}
    for tau in TAUS_MS:
        peaks[str(tau)] = {str(s): float(np.mean([run(tau, s, sg) for sg in (+1, -1)]))
                           for s in SEEDS}
    ol = [run(0, s, sg, closed=False) for s in SEEDS for sg in (+1, -1)]
    invalid = not all(p > B_ENV for p in ol)
    lo = all(peaks[str(t)][str(s)] <= B_ENV for t in TAUS_MS if t <= 5 for s in SEEDS)
    hi = all(peaks[str(t)][str(s)] > B_ENV for t in TAUS_MS if t >= 15 for s in SEEDS)
    verdict = "INVALID" if invalid else ("PASS" if lo and hi else "FAIL")
    lstar = math.log(1 + A * B_ENV / D) / A * 1e3
    # Fixture B: same construction L* = ln(1 + a b/D)/a with a = sqrt(g/zc), same b, D
    a_lip = math.sqrt(9.81 / 0.9)
    lstar_lip = math.log(1 + a_lip * B_ENV / D) / a_lip * 1e3
    flag = "POLICY_50HZ_MAY_SUFFICE" if lstar_lip > 20 else "NONE"
    out = {"metric": "discriminating_latency_sweep",
           "threshold": "tau<=5ms peak<=0.01 AND tau>=15ms peak>0.01",
           "fixture_A_peaks": peaks, "open_loop_peaks_min": min(ol),
           "L_star_ms": round(lstar, 3), "L_star_lip_ms": round(lstar_lip, 3),
           "a_lip": round(a_lip, 3),
           "lip_formula": "L*=ln(1+a*b/D)/a, b=0.01, D=1",
           "flag": flag, "verdict": verdict}
    line = json.dumps(out)
    print(line)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs.log"), "a") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    main()
