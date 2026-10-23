# Spike PLAN — Eng-1 / Proposal A — XC-0 floor certificate + C-P1-012 factorial

**Status:** SEALED by Author A (sha256 in `spike-PLAN.sha256`). Deferred-runnable by the experiment runner (Sonnet). It must not be edited after sealing. Any change needs a new version with a new hash and a logged reason.
**Rules:** CPU-only, numpy only, no network, no hardware. PASS = harness only. The runner files data and does not change claim state (B.9.8). Thresholds below are fixed before the run.

## 1. Purpose

1. Produce `floor-cert.json` certificates (C-Eng1-A-01) for the XC-0 export cells on a fixture.
2. Run C-P1-012's registered factorial counterexample search and its B.9.3 effort-substitution test, with the H2 and H3 repairs.
3. Check XC-0 non-interference (C-Eng1-A-03).

## 2. Fixture (ground truth)

- Planar 2-link arm in the horizontal plane (no gravity). Link lengths 0.3 m and 0.25 m, masses 1.5 kg and 1.0 kg, uniform rods. Simulated with semi-implicit Euler at `dt = 1 ms`.
- Controller at 1 kHz: joint PD tracking a band-limited reference (sum of 3 sinusoids per joint, 0.2–1.5 Hz, amplitude 0.3 rad, random phases per episode). Gains `Kp = [60, 40]`, `Kd = [4, 3]`. Saturation at ±8 N·m.
- Actuator: `τ_motor = sat(τ_cmd) + ripple + bias`. Ripple is 0.15 N·m at 2×–6× the joint rotation frequency. Bias is uniform ±0.1 N·m per episode (unmodeled).
- Friction at the joint output: Coulomb 0.2 N·m (tanh smoothing at 0.01 rad/s) and viscous 0.05 N·m·s/rad.
- Sensor noise: `q` σ = 1e-4 rad, `q̇` σ = 1e-3 rad/s, effort σ = 0.02 N·m.
- Contact: a non-support force on link 2 at a location uniform in [0.4, 1.0]·L2, direction uniform in the plane. Rectangular pulse with 2 ms raised-cosine edges, magnitude `M` and duration `d`. Onset uniform in [30, 60] ms within a 100 ms decision window.

## 3. Factorial cells (export as seen by the detector)

| Axis | Levels |
|---|---|
| Rate | R2 = 50 Hz (T = 20 ms), R1 = 200 Hz (T = 5 ms). Decimation is by sample-and-hold of the 1 kHz truth (no anti-alias filter, declared) |
| Effort source | CMD_RECON = `sat(τ_cmd)` (nominal law; no ripple, bias or friction knowledge). REALIZED = the measured sensor value under the placement below |
| Placement | DOWNSTREAM: the sensor reads `τ_motor` (current-derived; friction is not in the measurement). UPSTREAM: the sensor reads `τ_motor − τ_friction` (output torque sensor) |

That gives 8 cells, plus controls:

- **ORACLE (positive):** at R1, the true external joint torque `J_cᵀF` plus effort noise (σ = 0.02 N·m) is exported directly. The detector thresholds ‖·‖ of this channel through the same CUSUM.
- **NULL (negative):** every cell rerun with `M = 0` in the positive episodes.

`W` declaration: CMD_RECON cells use the command (efference), so they are reported as the joint channel `(X, W = τ_cmd)`. REALIZED cells also receive `τ_cmd` for the nominal model. All cells declare `W = {τ_cmd, reference}`.

## 4. Detector (identical family in every cell)

- Generalized-momentum observer at the export period `T`, with the nominal model (true inertia, no friction model), **gain·T = 0.25 fixed** (gain 50 s⁻¹ at R1, 12.5 s⁻¹ at R2). Residual `r_k`, statistic = ‖r_k‖, followed by a one-sided CUSUM with drift equal to the median residual on the calibration split.
- Threshold calibration: on a contact-free calibration split (seed-disjoint, 4000 windows), set the threshold to the empirical (1 − r) quantile of the per-window max CUSUM, for each `r ∈ {0.01, 0.05}`. Then freeze it.
- Decision: `Ẑ = 1` if the CUSUM crosses the threshold inside the window. Latency = crossing time − onset.
- Separately reported sensitivity (not used for verdicts): the fixed-gain 50 s⁻¹ variant from P1, to show the H2 effect.

## 5. Classes and sample sizes

- `d ∈ {5, 10, 20, 50} ms` × `M ∈ {2, 5, 10} N` gives 12 classes.
- Per cell, class and seed: `n_pos = 2000` and `n_neg = 2000` held-out episodes, one window each, independent initial phases. Seeds {0, 1, 2}. Certificates use the pooled seeds (n = 6000 each). Per-seed values are reported for spread.

## 6. Certificate computation (C-Eng1-A-01)

- `TPR_L` is the one-sided Clopper–Pearson lower bound at level `α/2`. `FPR_U` is the one-sided upper bound at `α/2`. α = 0.05 per (cell, class).
- `d_cert = d(TPR_L ‖ FPR_U)` in bits if `TPR_L > FPR_U`, else 0.
- `meets(q, r) = (TPR_L ≥ q) ∧ (FPR_U ≤ r)`, using the threshold calibrated for that `r`, on the placeholder grid `q ∈ {0.90, 0.95}`, `r ∈ {0.01, 0.05}`. Marked `placeholder_qr: true`.

## 7. Contrasts filed for C-P1-012 (registered criteria, verbatim thresholds)

- Reference cell: REALIZED @ R1, separately for each placement.
- **Factor-E counterexample:** CMD_RECON @ R1 matches the reference within ΔTPR ≤ 0.05 and Δp95 latency ≤ 10 ms on **every** class with `d ≥ 10 ms`, at FPR target 0.01.
- **Factor-R counterexample:** REALIZED @ R2 matches the reference on the same criterion.
- **B.9.3 substitution test:** replacing REALIZED with CMD_RECON at R1 must lower TPR by more than 0.10 at FPR 0.01 on the identifiable classes (those where the reference has TPR_hat ≥ 0.5). If it does not, file "role not realized by that channel on this fixture".
- These are filed as data. The runner states which criteria were met and does not state a grade or state change.

## 8. Non-interference (C-Eng1-A-03)

Run 50 episodes with the XC-0 publisher enabled and disabled. Joint trajectories `q(t)` at 1 kHz must be bitwise identical (`np.array_equal`).

## 9. Harness PASS (all required) — harness validity only

- **H1 determinism:** rerunning with the same seeds gives a byte-identical `verdict.json`.
- **H2 negative control:** NULL gives `d_cert = 0` and `meets = false` for every cell, class and `(q, r)`.
- **H3 positive control:** ORACLE meets `(0.95, 0.01)` for all classes with `d ≥ 10 ms` and `M = 10 N`.
- **H4 non-interference:** §8 holds.

FAIL on any of these means the harness is invalid. File it and do not interpret the science outputs.

## 10. Outputs

`spikes/<id>/{verdict.json, floor-cert/*.json, contrasts.json, sensitivity_fixedgain.json, run.log}`. `verdict.json` has the fields `harness_pass`, `H1..H4`, `factorE_counterexample_{DOWN,UP}`, `factorR_counterexample_{DOWN,UP}`, `substitution_drop_{DOWN,UP}`, `placeholder_qr: true`, `plan_sha256`.

## 11. Interpretation limits (fixed now)

- A PASS validates the harness only. There is no hardware transfer and no grade change.
- A met certificate is sufficiency evidence for this fixture, detector and export.
- A failed certificate is not evidence that information is absent.
- Results about the counterexample criteria go to the C-P1-012 claim adjudicator (cross-family) for any ruling.

## 12. Budget

About 8 cells × 12 classes × 2 rates of calibration × 3 seeds × 4000 episodes × 100 steps, plus controls, comes to about 10⁸ vectorized step-evaluations. The target is under 30 min on one CPU core.
