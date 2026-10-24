# Minimal Decisive Experiments — Author A

**Choice after review:** run **A (E1)**, with a built-in controllability gate **E0** on the same runs. Run **B (E2)** only if E0 passes and E1 is not refuted. **C** is pre-registered but deferred.

**Why A first.** Under the corrected mainline the framework's claim is sample/learning efficiency. If it does not beat direct-action task RL with matched temporal coherence, the B and C questions are about a system with no efficiency case. E0 is nearly free (probes on E1 checkpoints) and tests the load-bearing assumption D1 (`FRAMEWORK_REVIEW.md` §9).

**All training runs are PLANNED EXTERNAL STEPS** on the production humanoid climb/traversal chain outside `/srv/claude`. Nothing here was run. Only summaries come back into this tree (§5).

---

## 0. Common protocol (frozen before the first non-pilot run)

| Item | Value |
|---|---|
| Plant / task | Production 29-DoF home-humanoid obstacle traversal, R2.1 terminal semantics (baseline/05) |
| Curriculum | Heights {0.10, 0.20, 0.30, 0.40} m with the same `PoolQuotaSchedule` + two-panel Wilson gate for **all arms** (the gate is policy-agnostic) |
| Demo | The single 859-frame 0.70 m file (hash in baseline/05 §1.1); used only as specified per arm |
| Budget | S_max = 150M committed control steps per run (owner may rescale **once** before launch; frozen afterwards) |
| Seeds | 5 per arm; env/eval seeds paired across arms |
| Eval | Every 2M committed steps: 100 episodes per active height, deterministic policy (framework: 100% planner), frozen weights/normalizers, zero replay writes |
| Primary endpoint | **T70(0.30)**: first committed step at which two consecutive panels on h=0.30 m have Wilson LB95 ≥ 0.70. Runs that never reach it are censored at S_max. |
| Tuning fairness | Each arm gets the same sweep budget (≤ 6 configs × 1 seed pilot at 30M steps); choose by pilot AUC, then freeze |
| Invalid handling | Any `invalid` halt is logged and the run is restarted from the last checkpoint. More than 2 halts in an arm → the arm is flagged and excluded from claims |
| Costs | GPU-hours, wall-clock, and env-steps/s logged per run. The efficiency claim is on env steps; the GPU-hour ratio is reported alongside |

---

## E0 — Controllability and branching gate (on framework checkpoints; precondition)

**Question (D1):** does z index controllable, distinct closed-loop behaviors in real physics?

**Procedure.** At checkpoints 10% / 25% / 50% of S_max of each framework seed:
- Draw N=1024 start states from recent FB replay (upright, valid).
- For each start, pick a goal frame m_g from (a) demo frames and (b) held-out replay next-frames.
- Execute π_z with z = B(m_g) for K=10 and for 50 steps.
- Execute the same with a **mismatched** z = B(m_other), with m_other drawn from the same pool (permuted).

**Metrics**
- **Controllability ratio:** CR = E[d(m_{t+k}, m_g) | matched] / E[d(m_{t+k}, m_g) | mismatched], where d is the normalized Euclidean distance on a fixed hand-chosen kinematic subset (joint positions + root height proxy + gravity vector). B is deliberately not used, to avoid self-reference.
- **Branching diversity:** BD = mean pairwise outcome distance after 10 steps across 128 z (64 near-planner tangent, 32 demo, 32 sphere; B03 Merge 2 design) ÷ the same across 128 action-noise samples at matched per-step action variance.
- **Deadlock signature:**
  - upright fraction of FB replay over the first 25%
  - planner-source macro return minus uniform-random-z macro return

**Pre-registered thresholds**

| Outcome | Rule |
|---|---|
| **PASS D1** | CR(k=10) ≤ 0.80 for demo goals at the 50% checkpoint in ≥ 4/5 seeds, with bootstrap 95% CI upper bound ≤ 0.90 |
| **FAIL D1 → stop / redesign body objective** | CR ≥ 0.95 at 50% in ≥ 3/5 seeds |
| **Deadlock flag** | CR ≥ 0.95 at 25% **and** (upright fraction decreasing monotonically over the first 25% **or** planner-minus-random-z return ≤ 0) |
| BD | Reported, not gating. BD ≤ 1.0 is recorded as "z branching no richer than action noise" and feeds E2 |

Cost: inference-only rollouts, under 5% of one run.

---

## E1 — A: framework vs direct-action task RL vs imitation baseline (sample efficiency)

| Arm | Description |
|---|---|
| **FW** | Framework **as implemented** (expert/near/planner time schedule, planner deterministic, unfiltered FB replay, K=10). Planner-z noise knob present but **off**. |
| **DA** | Direct-action off-policy task RL (twin-critic, deterministic-policy family). Same obs as π plus a recurrent history encoder like the planner, same task reward / terminal semantics / curriculum, per-step independent Gaussian exploration. |
| **DA-C** | DA + temporally correlated action noise (held/OU over K=10 steps, matched marginal action variance). This is the null for "temporal coherence" (§5 mechanism 1). |
| **TR** | Imitation baseline: reference-tracking reward on the demo + task reward, on-policy family, same curriculum. |
| *(PP, optional reference)* | On-policy direct-action task RL, massively parallel. Reported for wall-clock context; not part of the decision. |

**Decision rule (primary, T70(0.30); best direct-action = min median of DA, DA-C)**

| Verdict | Rule |
|---|---|
| **SUPPORT (D2 holds)** | median T70(FW) / median T70(best-DA) ≤ **0.67**, FW reaches the threshold in ≥ 4/5 seeds, **and** paired bootstrap 95% CI of log-ratio has upper bound < 0 |
| **REFUTE** | ratio ≥ **1.0**, **or** FW reaches the threshold in ≤ 2/5 seeds while best-DA reaches it in ≥ 4/5 |
| **INCONCLUSIVE** | Otherwise. Add 5 seeds to FW and best-DA **once** and apply the same rule. Still inconclusive → verdict "small-scale-only" |

**Secondary (reported, non-gating)**
- AUC of mean ID success over {0.10..0.40}.
- Beyond-demo outcome: interpolation heights {0.15, 0.25, 0.35} and the frequency of contact modes absent from the demo (hand-on-box, multi-step takeoff, stumble recovery), FW vs TR.
- Q_task calibration slope (realized vs predicted macro return on fresh rollouts) by replay-age bin. Target [0.7, 1.3] in the second half.
- Actor KL drift on a frozen probe set.
- Production FB replay Gram κ and effective rank (information only).
- GPU-hours ratio FW / best-DA. If > 3×, the efficiency claim is stated as "env-step efficient, compute-expensive".

Cost: 4 arms × 5 seeds = 20 runs (+ ≤ 24 short pilot runs). Units: R = one FW run. Expect DA/DA-C ≈ 0.3–0.6 R and TR ≈ 0.3–0.6 R (estimate, to be replaced by measured cost).

---

## E2 — B: z-space exploration incl. near ablation (staged; run only if E0 PASS and E1 not REFUTE)

All arms are FW variants; everything except the exploration source stays fixed.

| Arm | Change |
|---|---|
| Z0 | FW as implemented |
| Z1 | **Near ablation**: p_near reallocated to expert at every schedule point |
| Z2 | **Planner-z exploration**: tangent noise θ ~ U[5°, 15°] on the planner mean, held for the macro (planner source only) |
| Z3 | Planner deterministic + per-step independent Gaussian action noise, variance matched to Z2's measured per-step action perturbation (pilot calibration) |
| Z4 | As Z3, but noise held/OU over the macro (temporal-coherence null) |

**Thresholds**

| Claim | Rule |
|---|---|
| z-exploration is specific (D3) | median T70(Z2) ≤ 0.80 × min(median T70(Z3), median T70(Z4)), with ≥ 4/5 seed-paired wins against each |
| Planner-z exploration helps | median T70(Z2) ≤ 0.80 × median T70(Z0), ≥ 4/5 paired wins |
| Near is effective / harmful | median ratio Z0/Z1 ≤ 0.80 / ≥ 1.25. Otherwise "near neutral" → prefer the simpler schedule |
| Coverage (secondary) | k-NN entropy of replay outcomes in the fixed kinematic subset; count of novel contact modes |

Cost: 5 arms × 5 seeds (Z0 reuses the E1 FW runs) = 20 new runs.

---

## C (pre-registered, deferred): low-task-return experience serves later tasks

**Design.**
- Phase 1: train on {0.10, 0.20} m until the two-panel gate passes.
- Phase 2: unlock {0.30, 0.40}.
- Arms:
  - C0: unfiltered FB replay (as implemented)
  - C1: FB replay admits only transitions from episodes with task return ≥ the running median
  - C2: as C0, but the FB replay capacity is halved (retention stress)

**Metrics**
- Phase-2 T70(0.30).
- Retention, three senses, at the end of phase 2:
  - (i) readable: fraction of phase-1 transitions still in the FB buffer
  - (ii) executable: CR for phase-1 goal frames
  - (iii) findable: planner success on {0.10, 0.20} (baseline/05 low-height regression panel)

**Thresholds**
- C supported if median phase-2 T70(C0) ≤ 0.80 × T70(C1), with ≥ 4/5 paired wins, **and** low-height regression ≤ 10 pp.
- Negative transfer is indicated if T70(C0) ≥ 1.25 × T70(C1).

---

## 5. Real code / evidence plan for the production climb chain (PLANNED EXTERNAL)

1. **Code identity:** production repository revision, a diff of the planner-z noise knob and the logging patches, and unit tests for:
   - BN two-pass order
   - `behavior_z` immutability
   - executed-z source tagging
   - `invalid`/`severe_penetration` routing on forced-fault fixtures
2. **Config identity:** one frozen config file per arm with a content hash; demo file hash; simulator version; seed list.
3. **Per-seed curves:** per eval panel, a CSV row with (step, height, successes/100, Wilson LB, invalid count, return mean), plus E0 probe outputs and Q-calibration bins.
4. **Costs:** GPU-hours, wall-clock, and env-steps/s per run; pilot sweep costs listed separately.
5. **Return path into this tree:** summaries only, under `feedback-round-2026-10-24/evidence/<E0|E1|E2|C>/<arm>/<seed>/` with a `manifest.json` containing (code revision, config hash, demo hash, seed, S_max, status, cost fields), plus a `VERDICT.md` per experiment that applies the rules above verbatim.
6. **Stop conditions:**
   - E0 FAIL → halt E1 framework extensions and report.
   - E1 REFUTE → no E2/C at production scale.
