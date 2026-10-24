"""Proposal A (B04): effective-inertia ratios seen by each unit and the
50 Hz sampled-loop stability band of a servo tuned for J_train."""
import json, sys
import numpy as np
sys.path.insert(0, ".")
from coupling_envelope import leg, mass_matrix

p = leg()
out = {}
q2s = np.linspace(0.1, 2.0, 50)
M11 = np.array([mass_matrix(p, 0.0, q)[1, 1] for q in q2s])
out["hip_M11_range"] = [float(M11.min()), float(M11.max()), float(M11.max() / M11.min())]
out["knee_M22_free"] = float(mass_matrix(p, 0.0, 1.0)[2, 2])
# stance manifold: foot pinned under hip, coordinate s = q2, q1 = -q2/2, y = 2 l cos(q2/2)
res = []
for mp in (0.0, 2.0):
    pp = leg(mp=mp)
    for q2 in (0.4, 1.2, 2.0):
        phi = np.array([-pp["l1"] * np.sin(q2 / 2), -0.5, 1.0])  # dQ/ds (l1 = l2)
        Js = phi @ mass_matrix(pp, -q2 / 2, q2) @ phi
        res.append({"payload": mp, "q2": q2, "J_stance": round(float(Js), 4),
                    "ratio_vs_M22": round(float(Js / mass_matrix(pp, 0, q2)[2, 2]), 1)})
out["knee_stance_reflected"] = res

def stable(rho, wn=2 * np.pi * 2, zeta=0.7, dt=0.02, delay=1):
    """Discrete double integrator J ddq = tau, ZOH at dt, PD tuned for J_train=1 with
    one-step actuation delay; plant inertia rho * J_train.  Returns spectral radius."""
    kp, kd = wn ** 2, 2 * zeta * wn
    A = np.array([[1, dt], [0, 1]]); Bv = np.array([dt ** 2 / 2, dt]) / rho
    n = 2 + delay
    Acl = np.zeros((n, n)); Acl[:2, :2] = A; Acl[:2, 2] = Bv
    for d in range(delay - 1):
        Acl[2 + d, 3 + d] = 1
    Acl[n - 1, :2] = [-kp, -kd]
    if delay > 1:
        Acl[n - 1, 2:n - 1] = 0
    return float(max(abs(np.linalg.eigvals(Acl))))
rhos = np.geomspace(0.05, 100, 400)
sr = np.array([stable(r) for r in rhos])
ok = rhos[sr < 1]
out["pd_50Hz_delay1_stable_rho"] = [float(ok.min()), float(ok.max())]
out["pd_spectral_radius"] = {str(r): round(stable(r), 3) for r in (0.25, 0.4, 0.5, 1, 4, 10, 20, 50)}
json.dump(out, sys.stdout, indent=1)
