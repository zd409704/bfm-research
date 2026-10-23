# Spike PLAN v2 — Eng-1 / Proposal A — XC-0 floor certificate + C-P1-012 factorial

**Version:** v2 (supersedes `PLAN-v1-author.md`, sha in `PLAN-v1-author.sha256`). Sealed by `PLAN.sha256` before `run.py` is executed.
**Path:** `packets/Eng-1/spikes/S2a-XC/` (decision.md amendment 2; replaces the `drafts/A/` location in v1).
**Rules:** CPU-only, numpy only, no network, no hardware. PASS = harness only. The runner files data and does not change any claim grade or state (B.9.8). Thresholds below are fixed before the run. Any change needs a new version and hash plus a log entry in `deviations.md`.
**Reason for v2:** mandatory amendments in `decision.md` (1–6) and `score-pass1.md` / `score-pass2.md` (P-amendments 1–6, M1–M6).

## 0. Epistemic status (M1)

- C-Eng1-A-01 (the floor certificate) is a **Candidate**, not a gate. The certificate's soundness is conditional on that lemma (a corollary of the data-processing inequality). If the lemma fails, certificates are not valid evidence. Certificates cite it as a *design lemma* only.
- "Meets the floor" is a chosen engineering specification. It never vetoes anything and never imposes a necessity gate.
- Domain: `0 < r < q ≤ 1`. All logs are base 2: `d_cert` is in **bits** and `d(a‖b) = a·log2(a/b) + (1−a)·log2((1−a)/(1−b))`.
- A certificate says information is **present** in the declared channel. It is never evidence of absence.
- C-P1-012 stays Candidate. The runner states which criteria were met and does not state a grade or state change.
- Bypassed Grade-3 edges (logged in `run.log` and `VERDICT.json`): **E05/E06** (S0a→S2a), **E08/E09** (S1→S2a), **E14** (S0b→S2a). **E10/E11** (S2a→S1) are *listed but not bypassed* (XC-0 claims no gate on S1). E17 Reading P is not invoked. None is a gate (D-Prin-2-001).

## 1. Purpose

1. Produce per-detector floor certificates for the XC-0 export cells on a fixture.
2. Run C-P1-012's factorial counterexample search and its B.9.3 substitution test, with the registered units (§5) and the H2/H3 repairs.
3. Check XC-0 non-interference (C-Eng1-A-03).

## 2. Fixture (ground truth)

- Planar 2-link arm in the horizontal plane (no gravity). Link lengths `l1 = 0.3`, `l2 = 0.25` m, masses `m1 = 1.5`, `m2 = 1.0` kg, uniform rods (COM at l/2, inertia `ml²/12` about COM). Semi-implicit Euler at `dt = 1 ms`. Standard 2-link `M(q)`, `C(q,q̇)q̇`.
- Controller at 1 kHz, on the true state: joint PD tracking a band-limited reference. Per joint, 3 sinusoids with frequency uniform in 0.2–1.5 Hz, amplitude 0.1 rad each (sum ≤ 0.3 rad) and random phases per episode, about the posture `q0 = [0.5, 1.0]` rad. The episode starts at the reference position and velocity. `Kp = [60, 40]`, `Kd = [4, 3]`. `τ_cmd = sat(PD, ±8 N·m)`.
- Actuator: `τ_motor = τ_cmd + ripple + bias`. Ripple is `0.15 · sin(n·K_g·(q_j − q0_j) + φ_j)`, with `n` uniform in {2..6} per joint and episode, `K_g = 10` and `φ` random. This gives a ripple frequency of `n·K_g·|q̇|/2π`. Bias is uniform ±0.1 N·m per joint and episode (unmodeled).
- Friction at the joint output: `τ_f = 0.2·tanh(q̇/0.01) + 0.05·q̇`. It acts on the joint: `τ_joint = τ_motor − τ_f + τ_ext`.
- Sensor noise (independent Gaussian per 1 kHz step, own RNG stream): `q` σ = 1e-4 rad, `q̇` σ = 1e-3 rad/s, effort σ = 0.02 N·m per joint.
- Contact: force on link 2 at `s·l2`, `s` uniform [0.4, 1.0], direction uniform in the plane, magnitude `M`. `τ_ext = J_cᵀ(q) F`. Pulse profile: total width `d` including 2 ms raised-cosine rise and fall edges (plateau `d − 4` ms, so d = 5 gives a 1 ms plateau). Onset is an integer ms, uniform in {30..60} after the start of the decision window.
- **Episode layout:** 401 export-time steps (i = 0..400). Steps 0..299 are a contact-free pre-roll (observer warm-up, 300 ms). The decision window is steps 300..400 (100 ms, observer sample times 300+jT for j = 1..100/T). The CUSUM resets to 0 at step 300. The observer is never reset. A pulse is truncated by the window end (censoring) if `onset + d > 100 ms`.

## 3. Factorial cells (export as seen by the detector)

| Axis | Levels |
|---|---|
| Rate | R2 = 50 Hz (T = 20 ms), R1 = 200 Hz (T = 5 ms). Decimation is by sample-and-hold of the 1 kHz truth, with no anti-alias filter (declared). Window length: 5 samples at R2, 20 at R1 |
| Effort source | CMD_RECON, REALIZED |
| Placement | DOWNSTREAM, UPSTREAM |

- **W declaration (M6):** the history available to the detector at export sample `k` is `{q̃_j, q̃̇_j, ref_j, refd_j, effort_j : j ≤ k}` at the export rate. There are no future samples. The reference and its derivative are exported with each sample (zero publication age in this harness). Publication age, jitter and queue policy are **not modeled** (a hardware-integration prerequisite, out of scope).
- CMD_RECON effort `u_k = sat(Kp(ref_k − q̃_k) + Kd(refd_k − q̃̇_k))`. This is the nominal law reconstructed from the exported samples. It has no ripple, bias or friction knowledge.
- REALIZED, DOWNSTREAM: the sensor reads `τ_motor + noise` (current-derived; friction is not in the measurement).
- REALIZED, UPSTREAM: the sensor reads `τ_motor − τ_f + noise` (an output torque sensor). **Scope (M4):** C-P1-012 excludes plants with dedicated torque sensing (premise 5). UPSTREAM cells are filed separately and flagged `outside_C-P1-012_premise5_scope`. DOWNSTREAM is the primary placement.
- CMD_RECON is identical across placements. It is a **shared baseline**: it is computed once per rate and cited by both placements.
- Unique cells: 2 CMD + 4 REALIZED = 6, plus controls.
- **ORACLE (positive control):** at R1, exports `τ_ext + effort noise (σ = 0.02)` directly. The same CUSUM is applied to `‖·‖`.
- **NULL (negative control):** every detector is run on episodes with `M = 0` (the classes keep their nominal `d`, which is irrelevant) and the same onset draw.
- **Sensitivity (not used in verdicts, §9):** observer gain 50 s⁻¹ at R2 (gain·T = 1.0, the P1 H2 handicap), and gain 12.5 s⁻¹ at R1 (matched bandwidth, gain·T = 0.0625), for CMD / REAL_DOWN / REAL_UP.

## 4. Detector (identical family in every cell)

- Generalized-momentum observer at the export period `T`. It uses the nominal model (true inertia, no friction model). **gain·T = 0.25 fixed** (gain 50 s⁻¹ at R1, 12.5 s⁻¹ at R2).
  - Inputs at sample `k`: `p_k = M(q̃_k) q̃̇_k`; `f_k = u_k + Cᵀ(q̃_k, q̃̇_k) q̃̇_k`, where `u_k` is the effort channel (CMD_RECON or REALIZED); initialisation `p̂_0 = p_0`, `r_0 = 0`.
  - Update: `p̂_k = p̂_{k−1} + T (f_{k−1} + r_{k−1})`; `r_k = K (p_k − p̂_k)`.
  - Statistic `s_k = ‖r_k‖`.
- CUSUM: `c_k = max(0, c_{k−1} + s_k − δ)`, with `c = 0` at window start and drift `δ` = median of `s` over all window samples of the calibration split (per channel).
- **Bandwidth confound (M4):** the two rates differ in observer bandwidth (50 vs 12.5 s⁻¹) because gain·T is held fixed. The inference is therefore narrowed to "these two rate-specific implementations". The matched-bandwidth sensitivity is reported alongside.
- **Alarm event:** the first `k` in the window with `c_k > thr`.
- **Calibration (separate data, conservative).** The calibration split is 40000 contact-free windows (seed domain `cal`, disjoint from all certification data). For each channel `ch` and `r_w ∈ {0.001, 0.005}`, take the window maxima `m = max_k c_k`. Let `k*` be the largest integer `k` such that the one-sided 97.5% Clopper–Pearson upper bound on `k/40000` is ≤ `0.25·r_w`. Set `thr` to the `(k*+1)`-th largest `m`, so at most `k*` calibration windows exceed it. The threshold is then frozen. It is recalibrated per cell and per `r_w`, never re-fitted afterwards.
- **Detector ID:** `<channel>@r<r_w>` (e.g. `R1_REAL_DOWN@r0.001`). Each has its own certificate.

## 5. Units: registered false-event rate (decision.md amendment 1; M4, P-3)

- C-P1-012 registers a fixed false-event rate of **0.01 /s** (the spike line in its record). The unit here is one decision per 100 ms window. Mapping: CUSUM resets at each window start, at most one alarm event is counted per window (alarms are merged within the window, no re-arm), windows are independent contact-free draws after a 300 ms warm-up. The event rate is then `FPR_window / 0.1 s`.
- Therefore **registered operating point `r_s = 0.01 /s` ⇔ `r_w = 0.001` per window**; the second placeholder level `0.05 /s` ⇔ `r_w = 0.005`.
- The v1 PLAN's per-window `r ∈ {0.01, 0.05}` equalled 0.1 /s and 0.5 /s, which is 10× looser than the registered criteria. v2 replaces them.
- All contrast criteria (§8) use `r_w = 0.001` (0.01 /s). The results are described as the C-P1-012 registered counterexample search **only** under this mapping; the mapping is stated here and in the output files.

## 6. Classes and sample sizes (recomputed for r_w = 0.001)

- `d ∈ {5, 10, 20, 50} ms` × `M ∈ {2, 5, 10} N` = 12 classes.
- Certification data (seeds {0, 1, 2}, disjoint from calibration and subset splits):
  - negatives: 4000 per seed (pooled n = 12000);
  - positives: 2000 per class per seed (pooled n = 6000 per class);
  - null (`M = 0`): 500 per class per seed (pooled n = 18000).
- Subset-definition split (seed 100): 1000 positives per class. It determines the "identifiable" classes (§8) on data separate from certification.
- Why these n: with calibration `FPR ≤ 0.25 r_w = 0.00025`, an expected ≤ 3 false events in 12000 gives `FPR_U ≈ 7e-4 < 1e-3`, so a correct oracle can meet `r_w = 0.001`.

## 7. Certificate computation (C-Eng1-A-01)

- Per detector and class, `TPR_L` is the one-sided Clopper–Pearson lower bound at level `α/2` and `FPR_U` the one-sided upper bound, `α = 0.05`. Coverage is **pointwise** (per detector and class). `FPR_U` uses the pooled certification negatives.
- `d_cert = d(TPR_L ‖ FPR_U)` bits if `TPR_L > FPR_U`, else 0.
- `meets(q, r_w) = (TPR_L ≥ q) ∧ (FPR_U ≤ r_w)`, for `q ∈ {0.90, 0.95}`, `r_w` being that detector's own `r_w`. Marked `placeholder_qr: true`. `(q, r)` stay PLACEHOLDER until the human lead ratifies the task table.
- **Multiplicity:** per-detector-class claims are pointwise only. For any packet-wide or selected-cell claim, a Bonferroni field `meets_bonferroni` is also filed, with `α_b = 0.05 / 168` (7 channels × 12 classes × 2 `r_w`). Packet-wide statements in METRICS.md cite the Bonferroni version. Independent confirmation on a fresh set is required after the human lead ratifies the table.

## 8. Event and latency semantics (M5), and contrasts for C-P1-012

- **Detection** of a positive episode: first alarm at a sample time `≥ onset`. A first alarm before onset is a **pre-onset alarm**: the episode is scored as a *miss* (conservative) and counted in `pre_onset_alarm_rate`. There is no re-arm. A pulse censored by the window still counts as positive. A miss has latency `+∞`.
- **Latency** = alarm time − onset (ms). `p95` is over all positive episodes (a miss counts as `+∞`; if TPR < 0.95, `p95 = ∞`).
- **Match** to the reference on a class: `|ΔTPR| ≤ 0.05` (absolute difference, at `r_w = 0.001`, point estimates) **and** latency match: both p95 finite → `|Δp95| ≤ 10 ms`; both infinite → match; one infinite → no match. A one-sided noninferiority variant (`TPR_alt ≥ TPR_ref − 0.05`, `p95_alt ≤ p95_ref + 10`) is filed as a secondary field.
- Reference cell: REALIZED @ R1, separately for each placement.
- **Factor-E counterexample** (per placement): CMD_RECON @ R1 matches the reference on **every** class with `d ≥ 10 ms` (9 classes). Also filed: the same restricted to the identifiable classes.
- **Factor-R counterexample** (per placement): REALIZED @ R2 matches the reference on the same criterion.
- **B.9.3 substitution test:** the identifiable classes are those where the reference has `TPR_hat ≥ 0.5` on the **subset-definition split** (seed 100). Replacement = the CMD_RECON @ R1 detector with its **own recalibrated threshold** (policy: recalibrate on the substituted channel, same `r_w`; the frozen-threshold variant is not run). The drop is `TPR_ref − TPR_cmd` on the certification data. `substitution_drop_met` = drop > 0.10 on **every** identifiable class (min drop is also filed; mean also filed). If it is not met, file: "role not realized by that channel *on this fixture, detector and calibration*". **This message must not be read as proof that effort information is absent**, and a small drop is not proof of equivalence.
- Sensitivity variants (§3) are put through the same Factor-R and Factor-E match tests and filed in `sensitivity_fixedgain.json`. They are not used in any verdict.
- The results are data. The claim adjudicator (cross-family) rules; the runner states no grade.

## 9. Non-interference (C-Eng1-A-03) — H4

Run 50 episodes (a mix of contact, `M = 0` and varied classes) with the XC-0 publisher enabled and disabled. The publisher is read-only with respect to the plant: it receives read-only array views, uses its own RNG stream, and the control law has no access to any export. `q(t)` and `q̇(t)` at 1 kHz must be bitwise identical (`np.array_equal`), and the control torque as well.

## 10. Harness checks (all required) — harness validity only

- **H1 determinism:** the full pipeline is run twice with identical seeds. `results.json` must be byte-identical (compared by sha256).
- **H2 negative-control coverage (replaces v1's "all NULL certificates are zero"):** for each detector `D` (7 channels × 2 `r_w` for the main grid), the NULL alarm count `k` out of `n = 18000` must satisfy `CP_lower(k, n; level 0.05/14) ≤ r_w(D)`, i.e. the null alarm rate is not significantly above the nominal rate (Bonferroni over 14 detectors). `d_cert` on NULL is filed for information. Deterministic invariants stay separate: H1 and H4.
- **H3 positive control:** ORACLE @ R1 detector `r_w = 0.001` meets `(q = 0.95, r_w = 0.001)` for all classes with `d ≥ 10 ms` and `M = 10 N`. (Calibration is conservative at 0.25·`r_w` on separate data with n_neg = 12000, so a correct harness meets this.)
- **H4 non-interference:** §9 holds.

If any of H1–H4 fails, the harness is **INVALID**. File it and do not interpret the science outputs.

## 11. Outcome definitions (machine-readable in `VERDICT.json`)

- **INVALID:** any of H1–H4 fails, or the run did not complete.
- **FAIL:** the harness is valid (H1–H4 pass) but the preregistered engineering sufficiency criterion **A02** is not met. A02 (C-Eng1-A-02, preregistered here): in the primary cell REALIZED @ R1 DOWNSTREAM, the detector `r_w = 0.001` meets `(q = 0.90, r_w = 0.001)` (`meets`, pointwise) for **every** class with `d ≥ 10 ms` and `M = 10 N`. FAIL routes to Alternate B per `decision.md`. "Fires" lists the criteria that failed.
- **PASS:** H1–H4 pass and A02 met. Harness validity only. No hardware transfer, no grade change.
- `criteria_fired` lists: failed `H*`, `A02` if unmet, and, as informational data flags, `FE_DOWN`/`FE_UP` (Factor-E counterexample = CMD matches), `FR_DOWN`/`FR_UP` (Factor-R counterexample), `SUB_DOWN_NOT_MET`/`SUB_UP_NOT_MET`. Informational flags never change PASS/FAIL/INVALID.

## 12. Outputs

`results.json` (deterministic science output, the v1 "verdict.json"), `floor-cert/<detector-id>.json`, `contrasts.json`, `sensitivity_fixedgain.json`, `run.log`, `METRICS.md`, `VERDICT.json`, `deviations.md`. `VERDICT.json` fields include `verdict`, `harness_pass`, `H1..H4`, `A02`, `criteria_fired`, `factorE_counterexample_{DOWN,UP}`, `factorR_counterexample_{DOWN,UP}`, `substitution_drop_{DOWN,UP}`, `placeholder_qr: true`, `plan_sha256`, `bypassed_edges`.

## 13. Interpretation limits (fixed now)

- A PASS validates the harness only. There is no hardware transfer and no grade change.
- A met certificate is sufficiency evidence for this fixture, detector and export. A failed certificate is not evidence that information is absent.
- The rate contrast is confounded with observer bandwidth by construction (§4). Inference is limited to these two rate-specific implementations.
- Results go to the C-P1-012 claim adjudicator for any ruling.

## 14. Budget

About 154k episodes × 401 steps, one pass, vectorized in chunks, run twice for H1. Target: under ~20 minutes CPU total on one core. If it would exceed that, the grid is reduced and the reduction is logged in `deviations.md`.
