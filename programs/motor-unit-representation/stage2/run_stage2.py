"""Write stage2_results.json from the scaled plant and a V3 learner probe.

The numeric gates are scale-conditional. ``scientific_lock`` stays false.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

_CODEBASE = Path(__file__).resolve().parents[1] / "codebase"
if str(_CODEBASE) not in sys.path:
    sys.path.insert(0, str(_CODEBASE))

from suite import run_all  # noqa: E402


def _v3_learner_probe() -> dict:
    """A few FB updates on the vendored V3 modules. This is not an H1–H4 lock."""
    import torch

    from unit_bfm.v3.learner import Learner

    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(20261024)
    learner = Learner(32, device=device, seed=20261024, config={"action_std": 0.05, "lr": 1e-4})
    n = 8
    g = torch.Generator(device="cpu").manual_seed(11)

    def rows():
        batch = {
            "x": torch.randn(n, 137, generator=g),
            "p": torch.randn(n, 32, generator=g),
            "u": torch.randn(n, 1, generator=g).tanh(),
            "x_next": torch.randn(n, 137, generator=g),
            "p_next": torch.randn(n, 32, generator=g),
            "g_next": torch.randn(n, 13, generator=g),
            "goal_g": torch.randn(n, 13, generator=g),
            "discount": torch.full((n, 1), 0.99),
            "goal_valid": torch.ones(n),
            "future_slice": (28, 32),
            "lag_slice": (24, 28),
            "config_id": torch.tensor([0, 0, 1, 1, 2, 2, 3, 3]),
        }
        batch["goal_g"][:, [0, 1, 5, 6]] = batch["x"][:, [0, 1, 5, 6]]
        batch["p"][:, 28:32] = 3.0
        batch["p"][:, 24:28] = 0.25
        batch["p_next"][:, 28:32] = 4.0
        batch["p_next"][:, 24:28] = -0.5
        return batch

    curve = []
    t0 = time.time()
    for step in range(6):
        metrics = learner.update(rows())
        curve.append({"update": step + 1, "fb": metrics["fb"], "actor": metrics["actor"]})
    return {
        "status": "executed",
        "scientific_lock": False,
        "device": device,
        "cuda_available": bool(torch.cuda.is_available()),
        "updates": learner.updates,
        "sanitize_calls": learner.sanitize_calls,
        "last_sanitize": learner.last_sanitize,
        "b_norm": float(learner.net.b(torch.randn(4, 13, device=device)).norm(dim=-1).mean().detach().cpu()),
        "curve": curve,
        "elapsed_sec": round(time.time() - t0, 4),
        "note": (
            "V3 learner path with B01 sanitizer, B02 logit hinge, and B03 "
            "matched pairs. Not a charter-scale physics run."
        ),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Stage-2 gate suite")
    parser.add_argument("--output", type=Path, default=Path("stage2_results.json"))
    args = parser.parse_args(argv)
    report = run_all()
    try:
        report["v3_learner_probe"] = _v3_learner_probe()
    except Exception as exc:  # noqa: BLE001 — recorded, not swallowed silently
        report["v3_learner_probe"] = {
            "status": "FAILED_TO_RUN",
            "scientific_lock": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    verdicts = report.get("metric_verdicts", {})
    print(json.dumps({"metric_verdicts": verdicts, "scientific_lock": report.get("scientific_lock"),
                      "v3_learner_probe": report["v3_learner_probe"].get("status"),
                      "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
