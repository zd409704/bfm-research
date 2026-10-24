"""Master Runner for B01-B05 GPU/CPU Simulation & Verification Suite.

Executes all five experiment suites (B01 through B05), records hardware/GPU telemetry,
and writes `colab_gpu_results.json`.
"""

from __future__ import annotations
import json
import platform
import time
import torch

from run_b01_gram_spike import run_b01_experiment
from run_b02_nonstationarity_spike import run_b02_experiment
from run_b03_contact_aliasing_spike import run_b03_experiment
from run_b04_four_arm_ablation import run_b04_experiment
from run_b05_r21_verification_suite import run_b05_experiment


def main(output_path: str = "colab_gpu_results.json") -> dict:
    t0 = time.time()
    device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    suites = [
        run_b01_experiment(),
        run_b02_experiment(),
        run_b03_experiment(),
        run_b04_experiment(),
        run_b05_experiment(),
    ]
    summary = {
        "program": "fb-beyond-imitation-acceleration",
        "timestamp_utc": int(time.time()),
        "platform": platform.platform(),
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "device_name": device_name,
        "total_elapsed_sec": round(time.time() - t0, 4),
        "all_passed": all(s["verdict"] == "PASS" for s in suites),
        "suites": {s["experiment_id"]: s for s in suites},
    }
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved complete results to {output_path} | all_passed={summary['all_passed']}")
    return summary


if __name__ == "__main__":
    main()
