"""Author-A dry run of the proposed B02-SPIKE protocol (NOT the registered spike run).

Checks the closed forms in proposal.md §1 and the pass/fail mechanics of §5 on CPU.
The official B02-SPIKE run is executed by the experiment runner (method §12.2).
"""
import json
import math
import sys
import time

import torch
import torch.nn as nn

SEED = 20261023
D_M, D_Z, D_A, K = 229, 256, 29, 10
R_Z = math.sqrt(D_Z)
torch.manual_seed(SEED)
results = {}


def proj(x):
    return R_Z * x / (x.norm(dim=-1, keepdim=True) + 1e-8)


# ---------------------------------------------------------------- (a) normalizer contract
class RunningNorm(nn.Module):
    """Count-weighted running mean/var. Updates only via explicit .update() in train mode."""

    def __init__(self, d, auto_update=False):
        super().__init__()
        self.register_buffer("mean", torch.zeros(d, dtype=torch.float64))
        self.register_buffer("var", torch.ones(d, dtype=torch.float64))
        self.register_buffer("count", torch.zeros((), dtype=torch.float64))
        self.auto_update = auto_update  # buggy variant: forward() mutates stats in train mode
        self.update_calls = 0

    @torch.no_grad()
    def update(self, x):
        if not self.training:
            raise RuntimeError("normalizer update while frozen")
        x = x.double()
        n = x.shape[0]
        bm, bv = x.mean(0), x.var(0, unbiased=False)
        tot = self.count + n
        delta = bm - self.mean
        self.mean += delta * n / tot
        self.var = (self.var * self.count + bv * n + delta**2 * self.count * n / tot) / tot
        self.count = tot
        self.update_calls += 1

    def forward(self, x):
        if self.auto_update and self.training:
            self.update(x)
        return ((x.double() - self.mean) / (self.var.sqrt() + 1e-6)).float()


class Backward(nn.Module):
    def __init__(self, auto_update=False):
        super().__init__()
        self.norm = RunningNorm(D_M, auto_update)
        self.net = nn.Sequential(nn.Linear(D_M, 256), nn.LayerNorm(256), nn.SiLU(), nn.Linear(256, D_Z))

    def forward(self, m):
        return proj(self.net(self.norm(m)))


def norm_state(b):
    return torch.cat([b.norm.mean, b.norm.var, b.norm.count.view(1)]).clone()


def ufo_update(b, m_cur, m_next, demo, correct=True):
    """One FBAgent.update prefix: two normalizer passes, freeze, z_update, expert query."""
    b.train()
    b.norm.update(m_cur)
    b.norm.update(m_next)
    if correct:
        b.eval()
    frozen = norm_state(b)
    with torch.no_grad():
        n = m_next.shape[0]
        z_rand = proj(torch.randn(n, D_Z))
        z_goal = b(m_next[torch.randperm(n)])
        mask = torch.rand(n, 1) < 0.5
        z_upd = torch.where(mask, z_goal, z_rand)
        _ = b(demo[torch.randint(len(demo), (8,))])  # expert/near prompt encoding
    drift = (norm_state(b) - frozen).abs().max().item()
    return z_upd, drift


demo = torch.randn(859, D_M) * 0.5 + 1.0
mu_c, mu_n = torch.zeros(D_M), torch.full((D_M,), 0.3)
U, n = 400, 256

for name, auto, correct in [("correct", False, True), ("double_update_bug", True, False)]:
    b = Backward(auto_update=auto)
    drifts, calls = [], []
    for _ in range(U):
        c0 = b.norm.update_calls
        _, d = ufo_update(b, mu_c + torch.randn(n, D_M), mu_n + torch.randn(n, D_M), demo, correct)
        drifts.append(d)
        calls.append(b.norm.update_calls - c0)
    results[f"a_{name}"] = {
        "max_frozen_drift": max(drifts),
        "update_calls_per_update": sorted(set(calls)),
        "final_mean_avg": b.norm.mean.mean().item(),
    }
# Count-weighted prediction: correct -> (mu_c+mu_n)/2 = 0.15; bug ([c,n,n,demo]) -> weights over
# (n, n, n, 8): (0*n + 0.3*2n + 1.0*8)/(3n+8)
pred_bug = (0.3 * 2 * n + 1.0 * 8) / (3 * n + 8)
results["a_pred"] = {"correct_mean": 0.15, "bug_mean": pred_bug, "bug_bias_vs_correct": pred_bug - 0.15}

# EMA (torch BatchNorm1d, momentum beta) fixed point at read time
beta = 0.1
for pattern, name in [(["c", "n"], "two_pass"), (["c", "n", "n"], "double_next")]:
    bn = nn.BatchNorm1d(1, momentum=beta)
    bn.train()
    for _ in range(3000):
        for p in pattern:
            bn(torch.full((64, 1), 0.0 if p == "c" else 1.0) + 1e-3 * torch.randn(64, 1))
    results[f"a_ema_{name}_weight_on_next"] = bn.running_mean.item()
results["a_ema_pred"] = {"two_pass": 1 / (2 - beta), "double_next": (2 - beta) / (3 - 3 * beta + beta**2)}

# Telescoping identity mu_next - mu_cur = sum_ep(m_final - m_init) / N_transitions
eps = [torch.randn(int(L), 4).cumsum(0) for L in torch.randint(20, 200, (50,))]
cur = torch.cat([e[:-1] for e in eps])
nxt = torch.cat([e[1:] for e in eps])
tele = sum(e[-1] - e[0] for e in eps) / cur.shape[0]
results["a_telescoping_err"] = (nxt.mean(0) - cur.mean(0) - tele).abs().max().item()

# ---------------------------------------------------------------- (b) behavior_z immutability
N_rep = 4096
behavior_z = proj(torch.randn(N_rep, D_Z))
before = behavior_z.clone()
b = Backward()
m_store = torch.randn(N_rep, D_M)
for bug in [False, True]:
    behavior_z.copy_(before)
    for _ in range(20):
        idx = torch.randint(N_rep, (256,))
        z_upd, _ = ufo_update(b, m_store[idx], m_store[idx], demo)
        assert z_upd.data_ptr() != behavior_z.data_ptr()
        if bug:
            behavior_z[idx] = z_upd
    diff = (behavior_z - before).abs().max().item()
    cos = (behavior_z * before).sum(-1) / D_Z
    results[f"b_{'overwrite_bug' if bug else 'correct'}"] = {
        "max_abs_diff": diff,
        "frac_rows_corrupted": (cos < 1 - 1e-6).float().mean().item(),
        "mean_cos_corrupted_rows": cos[cos < 1 - 1e-6].mean().item() if bug else None,
    }

# ---------------------------------------------------------------- (c) drift metrics and bias bound
D_O, SIG, GAM = 32, 0.2, 0.99
A = torch.randn(D_O, D_O) * (0.9 / math.sqrt(D_O))
Bu = torch.randn(D_O, D_A) * (0.5 / math.sqrt(D_A))
cvec = torch.randn(D_O) / math.sqrt(D_O)


class Actor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(D_O + D_Z, 256), nn.ELU(), nn.Linear(256, D_A))

    def forward(self, o, z):
        return torch.tanh(self.net(torch.cat([o, z / R_Z], -1)))


def rollout(pi, s0, z, noise):
    """noise: [S, K, D_A] common random numbers. Returns g, per-step obs and means."""
    s, g, obs, mus = s0, 0.0, [], []
    for j in range(K):
        mu = pi(s, z)
        obs.append(s)
        mus.append(mu)
        a = (mu + SIG * noise[:, j]).clamp(-1, 1)
        s = torch.tanh(s @ A.T + a @ Bu.T)
        g = g + GAM**j * torch.tanh(s @ cvec)
    return g, torch.stack(obs, 1), torch.stack(mus, 1)


pi_then = Actor()
S = 20000
span = 2 * sum(GAM**j for j in range(K))
rows = []
with torch.no_grad():
    for scale in [0.001, 0.003, 0.01]:  # synthetic actor drift levels
        pi_now = Actor()
        pi_now.load_state_dict(pi_then.state_dict())
        for p in pi_now.parameters():
            p.add_(scale * torch.randn_like(p))
        for r in range(3):
            s0 = torch.randn(1, D_O).expand(S, D_O) * 0.5
            z = proj(torch.randn(1, D_Z)).expand(S, D_Z)
            noise = torch.randn(S, K, D_A)
            g_then, obs, mu_then = rollout(pi_then, s0, z, noise)
            zz = z.repeat_interleave(K, 0)
            mu_now_on_then = pi_now(obs.reshape(-1, D_O), zz).view(S, K, D_A)
            mu_snap = pi_then(obs.reshape(-1, D_O), zz).view(S, K, D_A)  # stored column vs recompute
            col_err = (mu_snap - mu_then).abs().max().item()
            kl = ((mu_now_on_then - mu_then) ** 2).sum((1, 2)) / (2 * SIG**2)  # pre-clip Gaussian KL
            g_now, _, _ = rollout(pi_now, s0, z, torch.randn(S, K, D_A))
            bias = (g_then.mean() - g_now.mean()).item()
            se = math.sqrt((g_then.var() / S + g_now.var() / S).item())
            bound = span * math.sqrt(kl.mean().item() / 2)
            dmu = mu_now_on_then - mu_then
            logrho = ((noise * dmu).sum((1, 2)) / SIG - (dmu**2).sum((1, 2)) / (2 * SIG**2))
            rho = logrho.exp()  # exact per-row likelihood ratio from stored behavior_mu and a_raw
            chi2 = (rho.pow(2).mean() - 1).clamp_min(0).item()
            bound_chi2 = math.sqrt(g_then.var().item() * chi2)
            is_err = ((rho * g_then).mean() - g_now.mean()).item()
            rows.append({"chi2": chi2, "bound_chi2": bound_chi2, "is_corrected_err": is_err,
                         "ok_chi2": abs(bias) <= bound_chi2 + 3 * se, "scale": scale, "bias": bias, "se": se, "bound": bound, "kl": kl.mean().item(),
                         "delta_pi_rms": (mu_now_on_then - mu_then).norm(dim=-1).pow(2).mean().sqrt().item(),
                         "stored_column_err": col_err, "ok": abs(bias) <= bound + 3 * se})
results["c_actor_drift_rows"] = rows

# B drift with pi frozen: keep z_actual (exactly unbiased) vs re-encode z' = B_now(m_demo)
b_then = Backward()
b_then.norm.train(); b_then.norm.update(demo); b_then.eval()
b_now = Backward(); b_now.load_state_dict(b_then.state_dict()); b_now.eval()
with torch.no_grad():
    for p in b_now.net.parameters():
        p.add_(0.005 * torch.randn_like(p))
    zt, zn = b_then(demo), b_now(demo)
    dB = 1 - (zt * zn).sum(-1) / D_Z
    results["c_deltaB_identity_err"] = ((zt - zn).pow(2).sum(-1) - 2 * D_Z * dB).abs().max().item()
    results["c_deltaB_mean"] = dB.mean().item()
    s0 = (torch.randn(1, D_O) * 0.5).expand(S, D_O)
    noise = torch.randn(S, K, D_A)
    g_exec, _, _ = rollout(pi_then, s0, zt[:1].expand(S, D_Z), noise)
    g_keep, _, _ = rollout(pi_then, s0, zt[:1].expand(S, D_Z), noise)  # target semantics, same CRN
    g_reenc, _, _ = rollout(pi_then, s0, zn[:1].expand(S, D_Z), torch.randn(S, K, D_A))
    results["c_keep_bias_crn"] = (g_exec - g_keep).abs().max().item()
    results["c_reencode_bias"] = (g_exec.mean() - g_reenc.mean()).item()
    results["c_reencode_se"] = math.sqrt((g_exec.var() / S + g_reenc.var() / S).item())

# Procrustes gauge decomposition: synthetic pure rotation must give zero deformation drift
with torch.no_grad():
    Q_, _ = torch.linalg.qr(torch.randn(D_Z, D_Z, dtype=torch.float64))
    zt64 = zt.double()
    zr = zt64 @ Q_.T  # B_now = R B_then
    U_, _, Vh_ = torch.linalg.svd(zr.T @ zt64)
    R_hat = U_ @ Vh_
    tot = 1 - (zr * zt64).sum(-1).mean().item() / D_Z
    dfm = 1 - (zr * (zt64 @ R_hat.T)).sum(-1).mean().item() / D_Z
    results["c_procrustes"] = {"total": tot, "deformation": dfm, "gauge": tot - dfm}

# Train-mode BatchNorm expert encoding: per-coordinate relative input error ~ 3/(2 n_e)
bn_err = {}
for n_e in [8, 64]:
    errs = []
    for _ in range(400):
        x = torch.randn(n_e, D_M)  # population mean 0, var 1 = running stats
        xb = (x - x.mean(0)) / x.var(0, unbiased=False).add(1e-5).sqrt()
        errs.append(((xb - x) ** 2).mean().item())
    bn_err[n_e] = {"measured": sum(errs) / len(errs), "pred": 3 / (2 * n_e)}
results["a_bn_trainmode_rel_err"] = bn_err

# ---------------------------------------------------------------- (d) RNN burn-in exactness
D_Q, H, T, L_TR, NB = 135, 128, 600, 32, 16
lstm = nn.LSTM(D_Q, H, num_layers=2, batch_first=True)
head = nn.Linear(H, 1)
x = torch.randn(NB, T, D_Q)
t0s = torch.randint(100, T - L_TR, (NB,))
with torch.no_grad():
    stale_cache = []
    for i in range(NB):  # hidden states cached at collection time under old weights
        _, hc = lstm(x[i:i + 1, : t0s[i]])
        stale_cache.append(hc)
opt = torch.optim.Adam(list(lstm.parameters()) + list(head.parameters()), lr=3e-4)
tgt = torch.randn(NB, T, 1)
for _ in range(200):  # pre-registered synthetic critic drift
    opt.zero_grad()
    out, _ = lstm(x[:, :64])
    loss = (head(out) - tgt[:, :64]).pow(2).mean()
    loss.backward()
    opt.step()
err_burn, err_stale = 0.0, 0.0
t_start = time.time()
with torch.no_grad():
    for i in range(NB):
        t0 = int(t0s[i])
        full, _ = lstm(x[i:i + 1, : t0 + L_TR])
        q_exact = head(full[:, t0:])
        _, hc = lstm(x[i:i + 1, :t0])  # zero-hidden full-prefix burn-in, current weights
        tail, _ = lstm(x[i:i + 1, t0:t0 + L_TR], hc)
        stale_tail, _ = lstm(x[i:i + 1, t0:t0 + L_TR], stale_cache[i])
        err_burn = max(err_burn, (head(tail) - q_exact).abs().max().item())
        err_stale = max(err_stale, (head(stale_tail) - q_exact).abs().max().item())
results["d_burnin_max_abs_diff"] = err_burn
results["d_stale_max_abs_diff"] = err_stale
results["d_seconds"] = time.time() - t_start

# ---------------------------------------------------------------- verdict
checks = {
    "a_freeze_zero_drift": results["a_correct"]["max_frozen_drift"] == 0.0,
    "a_update_calls_eq_2": results["a_correct"]["update_calls_per_update"] == [2],
    "a_bug_detected": results["a_double_update_bug"]["max_frozen_drift"] > 0.0,
    "a_bug_mean_matches_pred": abs(results["a_double_update_bug"]["final_mean_avg"] - pred_bug) < 5e-3,
    "a_ema_matches_pred": all(abs(results[f"a_ema_{k}_weight_on_next"] - v) < 5e-3
                              for k, v in results["a_ema_pred"].items()),
    "a_telescoping": results["a_telescoping_err"] < 1e-4,
    "b_immutable": results["b_correct"]["max_abs_diff"] == 0.0,
    "b_bug_detected": results["b_overwrite_bug"]["max_abs_diff"] > 0.0,
    "c_bound_holds": all(r["ok"] for r in rows),
    "c_chi2_bound_holds": all(r["ok_chi2"] for r in rows),
    "c_stored_column_exact": all(r["stored_column_err"] < 1e-6 for r in rows),
    "c_deltaB_identity": results["c_deltaB_identity_err"] < 1e-3,
    "c_keep_exact": results["c_keep_bias_crn"] == 0.0,
    "c_procrustes_pure_rotation": abs(results["c_procrustes"]["deformation"]) < 1e-6,
    "a_bn_trainmode_matches_pred": all(abs(v["measured"] / v["pred"] - 1) < 0.25 for v in bn_err.values()),
    "d_burnin_exact": err_burn < 1e-5,
    "d_stale_detected": err_stale > 1e-2,
}
results["checks"] = checks
results["verdict"] = "PASS" if all(checks.values()) else "FAIL"
json.dump(results, sys.stdout, indent=1, default=float)
print()
