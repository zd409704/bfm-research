# Packet B02 — Independent Cross-Family Adjudication (order2: Candidates P, Q)

**Adjudicator:** Sonnet 5.5 (cross-family). **Method:** v1.0 (§4 Step 4, App. B.9). **Tie margin:** 5.0.
**Inputs:** Charter, `brief.md`, `anonymized/order2_P.md`, `anonymized/order2_Q.md`, `reviews/review-A-on-B.md` (critique of P), `reviews/review-B-on-A.md` (critique of Q).
**Scope notes:** No deanonymization was attempted. The critiques use proposal labels and claim IDs from before anonymization, so I refer to P and Q only. I did not have the Methodology v1.0 text or the baseline files. Where a judgment depends on them, I say so. I re-derived the arithmetic that mattered for scoring (below). The critiques were treated as evidence to check, not as authority.

---

## 1. Eligibility Gate Check

| Gate | P | Q |
|---|---|---|
| Charter B1: deployment purity (only `x137`, `g13`) | PASS. The actor sees `x137, z*`. Rule access to privileged data is training-only. | PASS. Same split. Q adds an export test for symbol reachability. This is weaker evidence than data provenance, as the critique notes, but it is not a violation. |
| Charter B2: causal privileged inputs | PASS, conditional on `D-B01-001` being admissible context. The collector ordering is explicit. Exogenous and endogenous parts are separated. | PASS, same condition. The time-triggered release is exogenous. |
| Charter B3: real physics, 144×E0–E4, no fabricated metrics | PASS. INFEASIBLE_CONFIG fails closed. Labels alone never count. | PASS. Counts come from simulator readback. `infeasible` forces `coverage_ready=false`. |
| Charter B4: no convergence claim from the 101-update smoke run | PASS | PASS |
| Brief: 98,304 transitions (32,768 + 65,536) | PASS. Per-cell quotas sum exactly. I re-derived the largest-remainder numbers (rule 6554/4915/6554/4915/9830; policy 13107/9831/13107/9830/19661). | PASS. 144×226+224 = 32,768 and 144×455+16 = 65,536. |
| Brief: all 144 groups, all 3 `C0` tiers | PASS | PASS |
| Brief deliverables 1–3 present | PASS | PASS. The deliverable 3 target is hedged between two g13 layouts (see §2). |
| No experiment results claimed | PASS | PASS. Q explicitly labels its arithmetic checks. |

**Verdict:** P and Q are both eligible, and neither is disqualified. Open conditionals:
- **Shared:** the admissibility of `D-B01-001` as frozen context is an orchestrator question. The brief's snapshot lists only `X-BASE-001..005`, and both candidates rely on D-B01-001.
- **P:** the memory layout depends on an unverified 512-slot factoring. It carries an explicit MEMORY_LAYOUT_BLOCKED path.
- **Q:** the tensor budget is checked only for replay plus sidecar. It does not budget model or optimizer state.

---

## 2. Rubric Scores (brief weights: 35 / 25 / 20 / 20)

### Row 1 — Resolution of Audit Issues #1, #2, #3, #5, #6, #8 (35)

I scored each issue out of 35/6 ≈ 5.83 and rounded to 0.5.

| Issue | P | Q | Justification |
|---|---:|---:|---|
| #1 scene/load sync | 5.5 | 5.0 | **P** gives an explicit 80-step table with integer half-open boundaries. E3 has 65 constant intervals and E4 has 30 loaded + 40 recovery intervals. It has a certificate with a failed-attempt rule. Weakness: the training load sign is fixed by the `|A|` maximization, so only one sign is trained (critique P R1-a). I confirmed this: the argmax always selects the same σ for a given `G`. **Q**'s single `make_program` source of truth is the better design idea. Its defects: (a) the sign-flip argument does not guarantee `|τ_ext|≥0.25S` (the critique's counterexample, m=0.20, τ_g=−0.02S, gives 0.18S, is arithmetically valid, though it still clears the 0.15S sustained predicate); (b) the step-on first sample violates the ≤0.02S increment predicate on the declared window; (c) E4-R and E4-RI share ordinal 0 and `n mod 3=0`, so they have identical keys (I confirmed this; `make_program` takes no variant argument). |
| #2 rule wiring | 4.5 | 4.0 | **P** has an enum dispatch that raises with no fallback, explicit gains, and anti-windup tied to the pre-clip torque. Weakness: instantaneous feedforward of the scheduled `τ_ext` makes the E4 "recovery" nearly tautological (P R1-b), and `J_nom` provenance is loose. **Q** has a gain derivation, a stability check, and a κ=1/0 split that is thoughtful about E4. Weaknesses: the claim that the pre-roll integral "absorbs" model error is wrong when `e=0` under a lock (Q critique B02-B-02), and E4 integral authority of 0.6S is not shown to cover loads up to 0.85. |
| #3 720-cell tracking | 5.0 | 4.5 | **P** gives an explicit 144×5 array with source split, a checksum identity, and a fail-closed predicate. **Q** gives a richer JSON ledger with per-cell event bits and gates GC-1..6. Q's GC-5 requires policy-dependent contact events, and its thresholds are inconsistent between §2.2, GC and S1 (all vs. 95%). |
| #5 static-hold panel | 5.0 | 4.0 | **P** commits to a single canonical 13-field `g_hold` with zero velocity and acceleration. It runs both load signs, with position and contact guards and a separate E1/E2 panel. **Q** is not exact: it hedges between L13-A and L13-U, depends on a calibration convention outside its read set, and sets the L13-U effort slot to a value it admits is "deliberately wrong" under load. Its panel design is otherwise sound (disjoint keys, rule positive control). |
| #6 normalizer drift | 4.5 | 4.5 | **P**: one sealed balanced transform for both sources and all networks. This is simple and removes normalization-induced shift. Weakness: the policy half of the statistics comes from an untrained actor (P R1-g). **Q**: the function-preserving first-layer refresh is the stronger idea and keeps ρ-weighted statistics current. Weakness: the Adam-state rescaling is wrong. Under `W'=W·diag(σ'/σ)`, gradients scale inversely, so `m` should scale by σ/σ' and `v` by (σ/σ')², not the reverse (Q critique B02-B-05; I agree). The sampler's 171/341 split also is not exactly 1/3 : 2/3. |
| #8 tanh saturation | 4.5 | 4.0 | **P** has a direct logit penalty plus a rule-imitation logit term that bypasses `sech²`. Weakness: the imitation target includes the E4 release edge, which is not inferable from `x137` (P R1-c), and the two terms conflict when `|u|≥0.95`. **Q** has a hinge plus TD target smoothing, which is a legitimate secondary mechanism. Weakness: the claimed bound `|y|≤2` is not enforced by a finite penalty (Q critique B02-B-03; I agree). Its S2-9 saturation probe is a good test. |
| **Row 1 total** | **29.0** | **26.0** | |

### Row 2 — 720-Cell Cross-Coverage Guarantee (25)

- **P: 20.0.** It has 720 independent fixed-capacity cells in each source partition, with exact quotas and joint resident, lifetime and source arrays. Protected E3 `[40,65)` and E4 `[15,65)` windows fit inside the smallest quotas. Commit is atomic through an 80-row scratch area, so no fragmented window is valid. `resident_ok` demands equality with the quota in every cell. Deductions:
  - Phase-locking: sub-case (anchor, λ) depends only on `j`, so resident cells are synchronized across configurations (P R2-a). Accepted.
  - Witness counters can be satisfied by the easiest tier (P R2-b).
  - Initialization can deadlock if any required initial window fails and there is no retry rule (P R2-c).
- **Q: 17.0.** It also has per-cell slot addressing and a rich per-cell ledger. Deductions:
  - GC-2's "always resident" claim is false during writes. The ring evicts the old episode's first transition at write 5, as the critique's counterexample shows (B02-B-04). It holds only at commit boundaries.
  - GC-5 needs policy-side contact events that an open-loop schedule cannot force. Q's statement that no count depends on policy competence is therefore false for E2 (B02-B-08).
  - The E4-R/RI key collision breaks the "6 rule episodes" accounting.
  - The 224 reserve slots and the 16 non-sampled policy slots are not reconciled with the per-cell quotas ("exactly 144" in S1-2 vs. extra reserve episodes).
  - Re-collection and top-up make the ledger path-dependent. Q claims it is a function of the scheduler pointer alone.

### Row 3 — Memory & Compute Compliance (20)

- **P: 15.0.** Replay is held at exactly 98,304 transitions. The dense row size (10,419 FP32) gives 4,096,917,504 B, which I confirmed. P says openly that this leaves almost no room under 4.10 GB. It proposes lossless factoring of 512 static privileged slots (3,694,559,232 B, confirmed arithmetic) and budgets 350 MB for everything else. It sets out RSS ≤ 4.694 GB, microbatching, and BLOCKED semantics. Deductions:
  - The 512-slot number has no provenance.
  - The 350 MB budget for F heads, targets and Adam state was not computed from the architecture (critique P R3-b is plausible).
  - Evaluation of 7,776 cases × 4 checkpoints × 12 arm-seeds is heavy for CPU.
  - P reports honestly that INCOMPLETE is a possible outcome.
- **Q: 13.0.** Replay is held at 98,304 rows. Q's row size of 41,677 B gives 4,097,015,808 B, which is 98 KB above P's figure. With sidecar, normalizer sums and ledger, Q totals about 4.0981e9 B. That is about 1.9 MB under the cap and counts only replay, sidecar, normalizer sums and ledger. Deductions:
  - Models, targets, optimizer state, batches and evaluation tensors are outside the table.
  - The "rollback in place" design has no old-data storage. A 64-row staging copy (about 2.7 MB) would exceed the headroom (critique B02-B-09; arithmetic confirmed).
  - The RSS ceiling gets only a "must be measured" statement.

### Row 4 — Spike Falsifiability (20)

- **P: 16.0.** It pre-registers exact conjunctive `coverage_ready` (resident_ok, exposure_ok, anchors_ok, physical_ok, integrity_ok, actor_hold_ok). It pre-registers counts of 144/144, 288/288 and 144 E2 cells in both material variants, and per-case RMSE < 0.35 for all 7,776 cases at checkpoint 20,000 on 3 seeds. Stage A has fault injections. Deductions:
  - The ablation arms have no directional predictions (P S1).
  - Train and eval schedules are identical, so timing memorization is untested (P S2).
  - "Strictly every case" gating is demanding, and the aggregate gates are redundant (P S4).
  - A 24 h CPU cap likely yields INCOMPLETE.
- **Q: 15.0.** Staged S0–S3 gates with explicit constants. It pre-registers `coverage_ready=true` at update 4,096 on 3 seeds. It adds an evaluator negative control and a rule positive control (<0.10 rad/s). A saturation-recovery probe has a 3× criterion, and the budget-exhausted outcome is separated from falsification. Deductions:
  - The scene-pooled RMSE can hide a single bad configuration (critique's 3/√144 example is valid). Position error is only reported, not gated.
  - The negative-control injection is underspecified.
  - Several thresholds are inconsistent.
  - The falsification list omits S1-4, S1-7 and S2-9.
  - The positive-control failure is called "infeasible" instead of "unvalidated".

### Totals

| | Row 1 (35) | Row 2 (25) | Row 3 (20) | Row 4 (20) | **Total /100** |
|---|---:|---:|---:|---:|---:|
| **P** | 29.0 | 20.0 | 15.0 | 16.0 | **80.0** |
| **Q** | 26.0 | 17.0 | 13.0 | 15.0 | **71.0** |

Margin = 9.0 > tie margin 5.0.

---

## 3. Principle Claim Adjudication (Appendix B.9)

I did not have the Methodology text. This is my assessment on the technical merits. Promotion state changes need independent proof verification and human-lead signature, as the candidates themselves say. I recommend no promotion to Locked.

| Claim | Assessment | Recommended state |
|---|---|---|
| **P-01** Marginal counts cannot certify joint coverage | **Valid.** The paired 2×2 counterexample has equal marginals and different coverage, and the embedding argument is sound. It is a standard fact, and the premises are stated. Weakness: it supports a joint-array verifier, not deterministic scheduling (critique P §3.2). The text partly concedes this. | Candidate, Grade 1. It is suitable for quick independent verification. Restrict the stated use to "the gate must use the joint array". |
| **P-02** Bounded action derivative cannot prevent squash decay | **Valid but near-trivial.** `|dQ/dh| ≤ M·sech²h` is correct. It is true only through the stated single gradient path, and the claim says so. It does not show the specific penalty is necessary. | Candidate, Grade 1, with scope as stated. |
| **Q-01** Window-residency feasibility bound | **Valid as a counting lemma** (720×64 = 46,080 > 32,768). Needs three corrections: (a) the mean length bound is 32,768/720 = 45.51, not ⌊·⌋ = 45; the floor applies only to uniform allocation; (b) distinct, non-overlapping witnesses must be an explicit premise; (c) part (c) holds for i.i.d. insertion only. A deterministic spacing schedule can satisfy a FIFO, so it does not exclude "global FIFO with a hard gate" in general (Q critique §3). | Candidate, Grade 1, conditional. Retain (a)–(b) with corrections. Narrow (c) to i.i.d. insertion. |
| **Q-02** Bounded saturation attenuation | **Overstated.** Conclusion (i) holds only given `|y|≤y_max`. A finite hinge does not enforce that condition, because stationary points with `Q_a·sech²(y) = 2λ(y−2)` can exist above 2. Conclusion (iii), non-binding at holding optima, is correct. | Candidate, Grade 1, narrowed to "head-Jacobian lower bound inside the region plus non-binding of the penalty at |u|≤0.92". |
| **Q-03** Internal-model role for load holding | **Reasonable but heuristic.** The Francis–Wonham principle is rigorous for LTI plants only, and Q labels Grade 2. The operational test (ablate `u_prev` history) also breaks feedback and observability, so the 3×/R² signature is exploratory. The warning that zero velocity can occur at a wrong angle is correct and useful, and P gates position while Q only reports it. | Candidate, Grade 2. Use the test as exploratory only. Make no necessity inference from a single-seed ablation. |

Neither candidate offers a claim strong enough to change the disposition. The claims are supporting rationale and were not decisive in scoring.

---

## 4. Disposition

**Recommend: P**

**Alternate: Q.** This is for the specific mechanisms listed in the merge items below, not as an equal alternative.

### Mandatory Merge Items

*Required changes to P (each is an accepted, checkable defect):*
1. **Load sign in training.** Alternate σ deterministically in E3/E4 training (for example `σ=(−1)^(c+j+⌊j/9⌋)`), with the panel's 0.15S floor and 0.95S feasibility rule. Otherwise mark the opposite-sign panel cases as a held-out generalization set with their own criterion (P R1-a).
2. **De-synchronize sub-cases across configurations.** Use anchor `(j+c) mod 3` and tier `(⌊j/3⌋+⌊c/3⌋) mod 3`. Add a resident (scene, anchor, λ, σ) marginal gate alongside the 720-cell array (P R2-a).
3. **Tier-qualified witnesses.** Require at least one resident rule witness at λ=0.92 per configuration, or gate on tier-qualified counts (P R2-b).
4. **Initialization retry and safety-termination definition.** Pre-register bounded retries and a dedicated reason code. Stop contact alone must not abort an episode (P R2-c, S8).
5. **Release-edge realism.** Either lag the rule's `τ_ext` knowledge by a pre-registered `d` intervals or add a source-qualified policy recovery counter to the readiness conjunction. Exclude the k intervals after a load edge from the logit-imitation term (P R1-b, R1-c).
6. **Memory evidence before sealing.** Produce the 512-slot provenance audit and compute model, target and optimizer bytes from the frozen architecture, instead of asserting 350 MB. Add a lossless fallback that needs no slot assumption, as the critique suggests (P R3-a, R3-b).
7. **Ablation predictions.** Pre-register one directional, thresholded, paired-seed prediction per ablation, and state what each outcome implies for the corresponding Issue fix (P S1).

*Adopt from Q:*
8. **Evaluator negative control** (S2-3) with its injection semantics fully specified, and a **rule positive control** on the frozen panel. A failure is reported as CONTROL_FAIL, not as proof of physical infeasibility.
9. **Physics-readback event predicates** with `scene_sync_violation_count` (at most one count per episode per event type). Keep P's full-rollout certificate.
10. **Pre-roll to fill history** before `t=0` (Q §1.2), so the early-window validity masks do not cost rows.
11. **Function-preserving normalizer refresh** as the registered alternative arm. If it is adopted, fix the Adam-state transformation. This is optional for B02 and required before any later adaptive-normalizer packet.
12. **Saturation-recovery probe** (S2-9) as a P arm, with identical smoothing in both arms.
13. **Held-out evaluation panel** with release timing shifted and an intermediate λ. It is common to both candidates' gaps.
14. Q's defects (E4 variant key collision, rollback storage, GC-5 policy dependence, threshold inconsistency, onset-edge predicate, hinge claim) need no merge, because P does not contain them.

### Confounds

The 9.0-point margin comes mostly from three differences:
- P commits to a single exact g13 target, per-case position and contact guards, and atomic windows.
- Q carries several internal inconsistencies that the critique identified and I independently confirmed: the E4 key collision, the rollback storage, and the false "always resident" claim.
- P's memory design is the more cautious one, but it rests on an unverified assumption.

Several confounds limit this judgment:
- I scored from text only. No candidate has been run, so physical feasibility of P's λ=0.92 loads and Q's κ-split E4 recovery is untested.
- The critiques differ in depth, and the order2 critique of P probes P's phase-locking more deeply than the critique of Q probes Q's schedule diversity. Q uses randomized draws via Philox, so it may have the diversity P lacks. I gave Q only partial credit for this because its own draws are not shown to cover load tiers.
- Baseline files and `D-B01-001` text were not available, so the g13 layout, network widths and model memory are unverified for both candidates. If the baseline confirms Q's L13-A layout, Q's #5 deduction (about 1 point) would shrink. If the baseline architecture is large, P's 350 MB budget and Q's tensor total both fail.
- P and Q differ in length and polish. I attempted to score on specified mechanism rather than prose.
- Both critiques use rubric headings as categories, so row-level scores may carry some correlation with critique emphasis.
- The tie margin is 5. A plausible shift of a few points on the unverifiable memory row (P 15 vs. Q 13) or on #5 would not close a 9-point gap. A swing of 9 or more would need both of those uncertainties to resolve in Q's favor together.
