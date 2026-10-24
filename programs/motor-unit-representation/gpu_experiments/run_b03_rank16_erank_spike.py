#!/usr/bin/env python3
"""B03 spike: rank-16 erank across morphology groups (CPU)."""
from __future__ import annotations
import json, time
from pathlib import Path
import torch
import torch.nn as nn

OUT = Path("/srv/claude/research/motor-unit-representation/packets/B03/spikes/B03-SPIKE")
DEVICE = torch.device("cpu")
torch.manual_seed(0)
DZ, N_CFG = 16, 144


class BEnc(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(13, 64), nn.SiLU(), nn.Linear(64, DZ))

    def forward(self, g):
        z = self.net(g)
        return z / (z.norm(dim=-1, keepdim=True) + 1e-8) * (DZ ** 0.5)


def make_g(n, L, nondim=False):
    # g: cos,sin,qdot,acc, tip_p(3), tip_v(3), tip_a(3) — tip scales with L
    ang = torch.rand(n, 1) * 6.28
    cos, sin = torch.cos(ang), torch.sin(ang)
    qdot = torch.randn(n, 1) * 0.5
    acc = torch.randn(n, 1) * 0.2
    tip_p = torch.randn(n, 3) * L
    tip_v = torch.randn(n, 3) * L
    tip_a = torch.randn(n, 3) * L
    g = torch.cat([cos, sin, qdot, acc, tip_p, tip_v, tip_a], dim=-1)
    if nondim:
        scale = torch.tensor([1, 1, 1, 1] + [1 / L] * 9)
        g = g * scale
    return g


def erank(Sigma):
    ev = torch.linalg.eigvalsh(Sigma).clamp_min(1e-12)
    p = ev / ev.sum()
    H = -(p * p.log()).sum()
    return float(torch.exp(H))


def gram(B, g):
    with torch.no_grad():
        z = B(g)
        return (z.T @ z) / z.shape[0]


def main():
    t0 = time.time()
    lengths = torch.linspace(0.08, 0.45, N_CFG)
    B_raw = BEnc()
    B_nd = BEnc()
    # train lightly on mixture
    opt = torch.optim.Adam(list(B_raw.parameters()) + list(B_nd.parameters()), lr=1e-2)
    for _ in range(40):
        loss = 0
        for L in [0.08, 0.2, 0.45]:
            g = make_g(128, L, False)
            z = B_raw(g)
            Sig = (z.T @ z) / z.shape[0]
            loss = loss + ((Sig - torch.eye(DZ)) ** 2).mean()
            g2 = make_g(128, L, True)
            z2 = B_nd(g2)
            Sig2 = (z2.T @ z2) / z2.shape[0]
            # stratified: equal weight per L
            loss = loss + ((Sig2 - torch.eye(DZ)) ** 2).mean()
        opt.zero_grad(); loss.backward(); opt.step()

    er_raw, er_nd = [], []
    for L in lengths.tolist():
        er_raw.append(erank(gram(B_raw, make_g(256, L, False))))
        er_nd.append(erank(gram(B_nd, make_g(256, L, True))))
    worst_raw, worst_nd = min(er_raw), min(er_nd)
    g1 = worst_nd >= 12.0
    g2 = worst_raw < 10.0 or (sum(e < 12 for e in er_raw) >= 10)
    # tip decode: linear probe tip_v from z
    g = make_g(512, 0.25, True)
    z = B_nd(g).detach()
    tip_v = g[:, 7:10]
    W, *_ = torch.linalg.lstsq(z, tip_v)
    pred = z @ W
    tip_rmse = float(((pred - tip_v) ** 2).mean().sqrt())
    # angular-only ablation
    g_ang = g.clone(); g_ang[:, 4:] = 0
    z_ang = B_nd(g_ang).detach()
    W2, *_ = torch.linalg.lstsq(z_ang, tip_v)
    tip_rmse_ang = float(((z_ang @ W2 - tip_v) ** 2).mean().sqrt())
    g3 = tip_rmse < tip_rmse_ang * 0.85
    verdict = "PASS" if g1 and g2 and g3 else "FAIL"
    payload = {
        "experiment_id": "B03_RANK16_144_MORPHOLOGY_ERANK",
        "device": str(DEVICE),
        "elapsed_sec": round(time.time() - t0, 4),
        "verdict": verdict,
        "gates": {
            "G1_worst_nondim_erank_ge_12": {"worst": worst_nd, "pass": g1},
            "G2_global_raw_collapse": {"worst_raw": worst_raw, "pass": g2},
            "G3_tip_decode_retains_lever_arm": {"tip_rmse": tip_rmse, "tip_rmse_ang_only": tip_rmse_ang, "pass": g3},
        },
        "summary": {"mean_erank_raw": float(sum(er_raw)/len(er_raw)), "mean_erank_nd": float(sum(er_nd)/len(er_nd))},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "VERDICT.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
