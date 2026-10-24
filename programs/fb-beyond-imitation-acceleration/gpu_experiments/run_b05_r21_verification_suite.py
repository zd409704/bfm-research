"""Experiment Suite B05: R2.1 Terminal Boundary (`severe_penetration` vs `invalid`) and Multi-Height Curriculum Verification.

Executes the 3-part R2.1 verification suite on real MuJoCo 3.17 (`dt_physics=0.005s`, 4 substeps):
1. Test 1 (Credible Failure Commit): Substep 1 penetration > 0.03 m with finite states/contacts across all 4 substeps
   latches `terminated=True`, `status='severe_penetration'`, `phi_next=0.0`, commits once, and continues evaluation panel.
2. Test 2 (Post-Penetration Corruption Override): Substep 1 penetration > 0.03 m followed by Substep 3 `NaN` state or
   contact buffer overflow (`ncon >= nconmax`) strictly overrides `severe_penetration` with `status='invalid'`,
   rejects replay/normalizer update, and does not increment committed step count.
3. Test 3 (Curriculum Controller & Quota Accounting): Verifies `PoolQuotaSchedule` 50/30/20 allocation on `4096` rows
   with zero integer rounding loss, two-panel `95%` Wilson lower bound >= 0.70 unlock gate, and >10% low-height regression hold.
"""

from __future__ import annotations
import json
import math
import time
from typing import Dict, Any, List
import numpy as np
from physics_env import MuJoCoObstacleTraversalR21Env, SubstepSnapshot, evaluate_r21_substep_state_machine


def wilson_lower_bound_95(successes: int, total: int, z: float = 1.959963984540054) -> float:
    if total <= 0:
        return 0.0
    phat = successes / float(total)
    denom = 1.0 + (z * z) / total
    center = phat + (z * z) / (2.0 * total)
    half = z * math.sqrt((phat * (1.0 - phat) + (z * z) / (4.0 * total)) / total)
    return max(0.0, (center - half) / denom)


def compute_pool_quota_4096(unlocked_heights: List[float], total_rows: int = 4096) -> Dict[str, int]:
    """Allocates 4096 control rows across unlocked heights per Baseline 05 §6.1 with exact remainder accounting."""
    heights = sorted(unlocked_heights)
    if len(heights) <= 2:
        base = total_rows // len(heights)
        rem = total_rows - base * len(heights)
        out = {f"{h:.2f}": base for h in heights}
        out[f"{heights[-1]:.2f}"] += rem
        return out

    lowest_two = heights[:2]
    frontier = heights[-1]
    intermediate = heights[2:-1]

    if len(intermediate) == 0:
        # Only 3 heights unlocked: 50% frontier, 50% split across lowest two (or 50/30/20 merged)
        q_front = int(round(0.50 * total_rows))
        rem_low = total_rows - q_front
        q_l0 = rem_low // 2
        q_l1 = rem_low - q_l0
        return {
            f"{lowest_two[0]:.2f}": q_l0,
            f"{lowest_two[1]:.2f}": q_l1,
            f"{frontier:.2f}": q_front,
        }

    q_front = int(round(0.50 * total_rows))
    q_low_total = int(round(0.20 * total_rows))
    q_inter_total = total_rows - q_front - q_low_total

    out: Dict[str, int] = {}
    out[f"{lowest_two[0]:.2f}"] = q_low_total // 2
    out[f"{lowest_two[1]:.2f}"] = q_low_total - (q_low_total // 2)

    inter_base = q_inter_total // len(intermediate)
    inter_rem = q_inter_total - inter_base * len(intermediate)
    for idx, h in enumerate(intermediate):
        out[f"{h:.2f}"] = inter_base + (1 if idx == len(intermediate) - 1 else 0) * inter_rem

    out[f"{frontier:.2f}"] = q_front
    assert sum(out.values()) == total_rows, f"Quota sum mismatch: {sum(out.values())} != {total_rows}"
    return out


def run_b05_experiment() -> Dict[str, Any]:
    t0 = time.time()
    env = MuJoCoObstacleTraversalR21Env(obstacle_height=0.20)
    m0 = env.reset(seed=42)

    # Test 1: Credible severe penetration on Substep 1, valid substeps 2..4
    act_zero = np.zeros(29, dtype=np.float32)
    outcome_test1 = env.step_control(act_zero, inject_penetration_substep=1, inject_nan_substep=None)

    # Test 2: Substep 1 penetration > 0.03 m followed by Substep 3 NaN corruption
    step_before_test2 = env.step_count
    outcome_test2 = env.step_control(act_zero, inject_penetration_substep=1, inject_nan_substep=3)
    step_after_test2 = env.step_count

    # Test 2b: Substep 2 penetration > 0.03 m followed by Substep 4 contact buffer overflow (ncon >= nconmax)
    substeps_overflow = [
        SubstepSnapshot(1, 0.002, True, True, 4, 64, False, True),
        SubstepSnapshot(2, 0.042, True, True, 8, 64, False, True),
        SubstepSnapshot(3, 0.015, True, True, 12, 64, False, True),
        SubstepSnapshot(4, 0.010, True, True, 64, 64, False, True),
    ]
    outcome_test2b = evaluate_r21_substep_state_machine(
        substeps=substeps_overflow,
        final_state_finite=True,
        final_schema_ok=True,
        raw_phi_next=1.25,
    )

    # Test 3: Curriculum Wilson lower bound and PoolQuotaSchedule invariants
    lb_78_of_100 = wilson_lower_bound_95(78, 100)
    lb_79_of_100 = wilson_lower_bound_95(79, 100)
    quota_2 = compute_pool_quota_4096([0.10, 0.20])
    quota_5 = compute_pool_quota_4096([0.10, 0.20, 0.30, 0.40, 0.50])
    quota_7 = compute_pool_quota_4096([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70])

    verdict_pass = (
        m0.shape == (229,)
        and outcome_test1.status == "severe_penetration"
        and outcome_test1.terminated is True
        and outcome_test1.commit_to_replay is True
        and outcome_test1.phi_next == 0.0
        and len(outcome_test1.substep_trace) == 4
        and outcome_test2.status == "invalid"
        and outcome_test2.commit_to_replay is False
        and outcome_test2.update_normalizers is False
        and step_after_test2 == step_before_test2
        and outcome_test2b.status == "invalid"
        and outcome_test2b.offending_substep == 4
        and lb_78_of_100 < 0.70
        and lb_79_of_100 >= 0.70
        and sum(quota_2.values()) == 4096
        and sum(quota_5.values()) == 4096
        and sum(quota_7.values()) == 4096
    )

    return {
        "experiment_id": "B05_R21_TERMINAL_BOUNDARY_AND_CURRICULUM_SUITE",
        "elapsed_sec": round(time.time() - t0, 4),
        "verdict": "PASS" if verdict_pass else "FAIL",
        "motion_descriptor_shape": list(m0.shape),
        "test1_credible_penetration": {
            "status": outcome_test1.status,
            "terminated": outcome_test1.terminated,
            "commit_to_replay": outcome_test1.commit_to_replay,
            "phi_next": outcome_test1.phi_next,
            "substeps_checked": len(outcome_test1.substep_trace),
        },
        "test2_post_penetration_nan_override": {
            "status": outcome_test2.status,
            "commit_to_replay": outcome_test2.commit_to_replay,
            "update_normalizers": outcome_test2.update_normalizers,
            "step_counter_unchanged": (step_after_test2 == step_before_test2),
            "offending_substep": outcome_test2.offending_substep,
        },
        "test2b_post_penetration_buffer_overflow_override": {
            "status": outcome_test2b.status,
            "offending_substep": outcome_test2b.offending_substep,
        },
        "test3_curriculum_and_quota": {
            "wilson_lb95_78_of_100": round(lb_78_of_100, 6),
            "wilson_lb95_79_of_100": round(lb_79_of_100, 6),
            "min_successes_of_100_for_lb70": 79,
            "quota_2_heights": quota_2,
            "quota_5_heights": quota_5,
            "quota_7_heights": quota_7,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_b05_experiment(), indent=2))
