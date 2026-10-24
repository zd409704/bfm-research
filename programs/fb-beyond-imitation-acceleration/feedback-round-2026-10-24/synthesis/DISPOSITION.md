# Disposition — feedback-round-2026-10-24 (orchestrator synthesis)

**Program**: `fb-beyond-imitation-acceleration`
**Date**: 2026-10-24
**Inputs reconciled**: `adjudication-agy-order1.md` (Order 1, P = draft A, Q = draft B) and `adjudication-sonnet-order2.md` (Order 2, P = draft B, Q = draft A). Cited mandatory fixes were cross-checked against `../reviews/review-B-on-A.md` (fixes F1–F10) and `../reviews/review-A-on-B.md` (fixes F1, M1–M6, m1–m5).
**Method**: this file reconciles the two adjudications. It does not re-adjudicate the drafts. Wherever this document says "draft A" or "draft B", it has already translated the Order-1 and Order-2 labels into those names. CRITICAL items are taken from the intersection of both adjudications. Where only one adjudication raised an item, the item is labelled with its source.
**Evidence rule**: B01–B05 script and accelerator PASS records are local algebra, contract or state-machine checks on artificial inputs or toy plants. None of them validates the framework. Every empirical cell of the owner's causal chain remains empty.

---

## 1. Owner call

**Call: REVISE-THEN-CONTINUE**, at bounded, staged scale.

| Source | Final call | Agreement |
|---|---|---|
| Order 1 (agy) | `revise-then-continue` | — |
| Order 2 (Sonnet) | `revise-then-continue` | — |
| Both blind reviews | "revise-then-adjudicate"; both agree with revise-then-continue as the investment posture | Unanimous |

The two adjudications agree, so the call is not overridden. The call can be checked on three points:
1. No empirical (E) cell of the chain *body experience → conditional behaviors → z-organized exploration → expanded body skill → planner uses skill → later goals* has been filled. B01–B05 cannot fill one.
2. The design is theoretically coherent enough to test. It has a reward-free, off-policy, relabeled body layer and a macro-z task layer. The absence of a full neural convergence proof is not grounds to reject it (owner rule, accepted by both).
3. The validation plans in both drafts had blocking defects:
   - censoring;
   - invalid-run auto-restart and arm exclusion;
   - an under-powered budget in one draft and an unbounded one in the other;
   - weak stop authority for a pose-proximity metric.

   The implementation as audited also lacks executed planner-z exploration, and its source schedule is time-based. Repairs, then a staged spend, come before any efficacy claim.

**What would change the call** (taken from Sonnet §4 and agy §4 and merged):
- Escalate to **substantive architectural revision** if either of these holds:
  - controllability (D1) fails after the capped exploration-repair diagnostic (Z2);
  - an adequate simpler baseline reaches the absolute-competence gate while the framework misses the efficiency gate (A outcome `BASELINE-WINS`).
- **Stop this configuration** if both of those conditions persist after that one capped diagnostic. This stops the tested configuration only. It is not a claim that every FB architecture is impossible.
- Become **small-scale-only** if Stage 2 of A ends `NO-ADVANTAGE` or `INCONCLUSIVE` while D1 passes. C may still run, because reuse is a separate claim. No scale-up follows.

---

## 2. Hybrid base choice

Both adjudications recommend a **Tie/Hybrid**. Their dimension scores rank the drafts **in the same direction on every dimension**:

| Dimension | agy (A vs B) | Sonnet (A vs B) | Better base (both agree) |
|---|---|---|---|
| Framework-theory soundness | 88 vs 89 | 74 vs 78 | B, narrowly. A's causal T/I/E table, cold-start analysis and mechanism list are merged in. |
| Implementation-gap honesty | 85 vs 91 | 76 vs 80 | B (provenance labels, three data paths). A's priority column and rows are merged in. |
| B01–B05 re-scoping | 94 vs 86 | 84 vs 76 | A (per-number ledger) |
| Minimal-experiment design | 78 vs 83 | 55 vs 70 | B (entry gate, AUC, seed rules, fault protocol, causal C). A's controls (DA-C, E0, Z2) are merged in. |
| Investment-judgment clarity | 90 vs 82 | 80 vs 62 | A (single category, D1–D3, alternatives table) |

**Adopted hybrid, by file:**

| Merged file | Primary base | Merged from the other draft |
|---|---|---|
| Framework judgment (this file, §1 and §4) | Draft A §0, §8–§10 | Draft B: objective-sufficiency objection, extreme-point caveat, measure-density vs moment-consistency premises |
| `MERGED_GAP_TABLE.md` | Draft B provenance taxonomy and three-path audit | Draft A GAP-01…21 rows and P0–P2 priorities; new rows required by the reviews |
| `MERGED_CORRECTED_CONCLUSIONS.md` | Draft A per-number ledger | Draft B premise wording, the B03 `p^2 + 0.5625` derivation, append-only framing |
| `MERGED_MINIMAL_EXPERIMENTS.md` | Draft B protocol (entry gate, AUC, seeds, fault rules, causal C) | Draft A: DA-C, E0 controllability probe (repaired), Z2 planner-z diagnostic, alternatives |

**Residual disagreement R1 (fallback base):** if the owner insists on one unmerged package, agy names **draft A** and Sonnet names **draft B**. This synthesis resolves the question per file (table above), so no single-package fallback is needed. If one is still required, use draft B for experiments and draft A for judgment and ledger. Neither draft is acceptable unrepaired: draft A's E1 rules and fault handling need rewriting, and draft B's A budget is uninformative.

---

## 3. Unified mandatory merge/fix list (deduplicated)

Severity follows the intersection rule. An item is **CRITICAL** only if both adjudications treat it as blocking: agy labels it CRITICAL, and Sonnet either labels it blocking or lists it in a way that requires a protocol rewrite before spend. All other items are **MAJOR** or **MINOR**. "Where fixed" points to the merged file that carries the fix.

| ID | Sev. | Fix | agy | Sonnet | Review origin | Where fixed |
|---|---|---|---|---|---|---|
| **MX-1** | CRITICAL | **Informative two-tier budget and censor-proof endpoint.**<br>• Primary endpoint: normalized trapezoidal success AUC in [0,1].<br>• T70 is secondary and censor-aware (attainment counts plus per-arm survival curves). Non-attainment never produces a fabricated time. Both-fail is `INCONCLUSIVE`, never ratio 1.<br>• Relative-efficiency gate (A1) is separate from the absolute 0.70 Wilson gate (A2).<br>• Comparator frozen from setup seeds before test seeds.<br>• Critical effect and MDE stated at 5 paired seeds; one pre-declared seed extension.<br>• Stage 1 = 15M transitions per run; Stage 2 = 100M per run, only if Stage 1 shows learning or controllability. | MF-1 | Fixes 2, 3 | A-on-B F1; B-on-A F1 | Experiments §2, §4 |
| **MX-2** | CRITICAL | **Entry integrity gate and Charter §2.4 fault protocol.**<br>• At most 10k transitions plus fixtures.<br>• Fixtures verify: three-path provenance; snapshot-level `behavior_z` and normalizer immutability; 1e-6 macro-return parity; 1e-5 recurrent-prefix parity; R2.1 terminal-priority latch.<br>• Delete auto-restart and the ">2 halts → exclude arm" rule. A verified invalid fault means halt, inspect, then record a documented disposition.<br>• Retain every scheduled seed. Charge rolled-back and restart work to cost. | MF-2 | Fix 4, gate table | B-on-A F2; A-on-B (draft B entry gate) | Experiments §1, §3 |
| **MX-3** | CRITICAL | **E0 controllability probe limited to a validated construct.**<br>• Frozen feature metric including velocity.<br>• Both goal pools (demo, replay) and both horizons (k = 10, 50).<br>• Terminated branches stay in denominators.<br>• Seed-level bootstrap.<br>• Explicit `INCONCLUSIVE` outcome.<br>• PASS = CR ≤ 0.80 *or* repeatable non-fall branching.<br>• E0 is a diagnostic and a launch gate for Stage 2 / C / Z2. A poor demo-pose CR alone never rejects the framework. | MF-3 | Fix 6 | B-on-A F3 | Experiments §5 |
| MX-4 | MAJOR | **Temporal-abstraction and exploration-fidelity controls inside A.**<br>• Add DA-C (held/OU noise over K = 10 at matched marginal action variance).<br>• Add a correlated-noise direct-action probe to the branch panels.<br>• Frozen definitions for A-I (imitation comparator; its reference phase and recovery rules are fixed).<br>• Declare up front that an A-F failure with poor executed-z coverage is routed to a capped Z2 diagnostic. It is not counted as architectural refutation. | MF-4 | Fix 5 | B-on-A F5, F6; A-on-B M2 | Experiments §4.2, §6 |
| MX-5 | MAJOR | **Causal C protocol.**<br>• Common frozen donor pool; C-use vs C-omit, plus a size-matched random-enrichment control (C-rand) and a V-relevant positive control (C-pos).<br>• Fresh V planner on frozen bodies.<br>• Three retention senses measured separately.<br>• C is gated on integrity, controllability and minimal competence, not on A superiority. | MF-5 | Fix 6 | A-on-B M3; B-on-A F9 | Experiments §7 |
| MX-6 | MAJOR | **One verdict category with enumerated decisive assumptions.** D1–D3 from draft A, plus objective sufficiency and planner coverage (D4, D5) from draft B. "Investment hurdle", "no benefit on this task" and "mechanism falsified" are kept distinct. | MF-6 | Fix 1 | A-on-B M1; B-on-A §2.5 | This file §4 |
| MX-7 | MAJOR | **Theory premise repairs.**<br>• "All z" claims become sampled-update eligibility claims.<br>• Ideal FB is kept distinct from the learned controller.<br>• Equal-occupancy and indistinguishable-full-input (U_t) premises are restored for B03 contact impossibility.<br>• Planner-z confinement is restated as a measurable coverage risk.<br>• Off-support planner z, negative-transfer mechanisms and an early cold-start discriminator are added. | MF-6 | Fix 8 | B-on-A F4; A-on-B m4 | This file §4.2; Gap table G30–G31 |
| MX-8 | MAJOR | **Per-number re-scoping ledger.**<br>• B03 `> 0.40` check is unfalsifiable.<br>• B02 Gaussian-KL drift gate is linked to deterministic `.loc` execution.<br>• Wilson rule is a formula check only.<br>• H1 is untested and deprioritized.<br>• Exact source pointers. | MF-6 | Fix 9 | A-on-B M5, m1; B-on-A F10 | Corrected conclusions |
| MX-9 | MAJOR | **Gap-table provenance and new rows.**<br>• Labels: Observed / Reported / Specified / Pending.<br>• New rows: three data paths; executed stochasticity by source; evaluation/collection protocol; demonstration coverage.<br>• Production identity is recorded as "unresolved", not "absent".<br>• BN-order check is P0. | MF-6 | Fix 10 | B-on-A F8; A-on-B M6, m5 | Gap table |
| MX-10 | MAJOR | **Explicit cost ceilings.**<br>• Accelerator-hour, wall-clock and memory ranges with stated throughput assumptions.<br>• Vector-step vs aggregate-transition units defined.<br>• Evaluation transitions capped well below training transitions.<br>• Caps may only shrink after the measured-throughput freeze. | MF-7 | Fix 7 | B-on-A F7; A-on-B M4 | Experiments §8; this file §6 |
| MX-11 | MAJOR | **Q-calibration target and drift metric.**<br>• Full-return Monte-Carlo target with bootstrap only at truncation.<br>• Slope, intercept and RMSE per replay-age bin.<br>• Deterministic-execution drift metric (action-space RMS on a probe set, not Gaussian KL).<br>• Explicitly non-gating. | (in MF-5) | Fix 11 | B-on-A §4 end, F9 | Experiments §4.5 |
| MX-12 | MINOR | **Cross-file consistency.**<br>• A single deadlock Boolean.<br>• T70 Wilson rule consistent with n = 20 intermediate panels (two pooled panels, ≥34/40).<br>• Pre-registered symmetric futility stop.<br>• V is labelled the most favourable transfer target, and the C claim is scoped to failure-to-recovery. | (confounds §3) | Fix 2 (n=20) | B-on-A F10; A-on-B m2, m3 | Experiments §2, §5.4, §7 |

**Out of scope, unchanged by both adjudications:** no whitening, no same-height relabel, no world-model losses, and no B-input expansion. Sealed B01 semantics are kept: standard expert/near encoding, UFO `z_update` 50/50, and the standard `F·z` actor readout.

---

## 4. Decisive assumptions

### 4.1 Assumption table

| ID | Decisive assumption | Origin | If false → | Decisive check | Kind of conclusion if false |
|---|---|---|---|---|---|
| **D1** | **Controllability.** In real physics, holding z = B(m_g) moves the body toward m_g measurably better than a mismatched z, or produces repeatable, distinct, non-fall branches. | A §9 (both adj.) | The body layer is not a usable skill library and the chain breaks at its first links. Run the capped Z2 diagnostic. If Z2 also fails → substantive architectural revision (body objective / exploration). | E0 (`MERGED_MINIMAL_EXPERIMENTS.md` §5) | Mechanism failure *for the tested configuration* |
| **D2** | **Framework efficiency.** At matched interaction budgets, A-F success AUC exceeds the frozen best direct-action arm and the imitation comparator. | A §9 (A1 gate replaces A's 0.67 ratio) | No sample-efficiency case on this task at this budget → small-scale-only. If a baseline wins and reaches A2 → substantive revision. | A, Stage 1 → Stage 2 | "No benefit on this task/budget", not a falsification of the mechanism |
| **D3** | **z-exploration specificity.** Gains from held-z exploration exceed matched temporally correlated action noise. | A §9 | Drop the FB-specific exploration claim. Keep the framework only via relabeled reuse (D2, C). | DA-C inside A (partial); full E2 deferred | Claim narrowing |
| **D4** | **Objective sufficiency.** The reward-free body objective acquires the behaviors the task needs; a planner cannot select what the actor cannot execute. | B (Sonnet fix 1) | Planner improvements cannot help. Revise the body objective or add task-directed body data. Do not tune the planner further. | Branch-panel bounded command search: does any probed command make task progress where the planner does not? | Architectural revision (division of labour) |
| **D5** | **Planner coverage / findability.** The planner finds and uses executable, useful z, with executed-z dispersion not collapsed onto the cue set and no off-support outputs. | B (Sonnet fix 1); A §0 | Exploration repair (Z2) or planner revision. The body layer may still be fine. | Executed-z telemetry (Gap G05–G06, G30); command-search vs planner gap | Implementation gap, not mechanism failure |

Monitored, non-decisive: task-Q calibration under actor drift (MX-11). It is reported but does not gate.

### 4.2 Most promising benefit vs strongest objection (merged)

- **Most promising benefit (both drafts agree):** every *valid* real transition, including failures and low-return episodes, is eligible to train a reusable conditional controller through reward-free relabeling. Separately, macro-K shortens task credit assignment by about 10×. The benefit is **sampled-update eligibility**, not "every z is trained". Whether eligibility becomes executable capability is exactly what D1 and C test.
- **Strongest objection (merged A + B):**
  - **Objective sufficiency.** Linear preference optimization over motion occupancy favours exposed extreme points of the achievable occupancy set (draft B). A reward-free repertoire may therefore lack the task-needed contact behaviors.
  - **Exploration starvation.** With deterministic `.loc` execution and a time-based ramp to 0.70 planner share, executed exploration can shrink before competence arrives (draft A cold-start hazard).
  - **Drift.** Joint training moves the planner's effective dynamics.

### 4.3 Simpler alternatives and fair-comparison costs (draft A §10, reconciled with draft B)

| Alternative | Status this round | Fairness requirements |
|---|---|---|
| Direct-action off-policy task RL (A-D) | **Mandatory in A** | Same observations/history, reward, terminal semantics, heights, interaction cap, setup budget, evaluation panels |
| Same with held/OU correlated action noise (A-DC) | **Mandatory in A** (temporal-coherence null) | Matched marginal action variance; K = 10 hold |
| Imitation-assisted task learner (A-I) | **Mandatory in A** | Same motion material, used as a prior and not as action labels; task adaptation allowed. The no-imitation rule applies to A-F only. |
| Massively parallel on-policy direct-action RL | Deferred (wall-clock reference only) | Report environment steps and accelerator-hours |
| Hindsight goal-conditioned RL plus planner | Deferred (second wave if D2 holds) | Same interaction and tuning budget |
| Frozen pretrained body plus new planner | Deferred (if drift dominates) | Pretraining interactions counted |

**Confounds named by both adjudications (carried into the plan):**
- Demonstration-information asymmetry. A-F and A-I see the demo; A-D and A-DC do not. Gains over A-D therefore measure demo cues + hierarchy + relabeling jointly.
- Temporal correlation vs learned manifold.
- Compute vs sample efficiency. Six networks against two, so both ratios are reported.
- Failure-to-recovery alignment in C.

---

## 5. Residual disagreements (explicit)

| # | Topic | agy (Order 1) | Sonnet (Order 2) | Resolution in this synthesis |
|---|---|---|---|---|
| R1 | Single-package fallback | Draft A | Draft B | Per-file hybrid (§2). No single fallback is needed. |
| R2 | Budget numbers | Concrete anchors: Stage 1 = 15M, Stage 2 ≤ 100M aggregate transitions. The text leaves "per run" implicit; it is read as per run because it replaces draft B's 1M per-run cap. | No numbers; derive from measured throughput or learning curves | 15M / 100M per run become **ceilings**. Final caps = min(anchor, measured-throughput allocation within the approved hours) and are frozen at Stage 0. They may only shrink, and must go back to the owner if the shrink exceeds 2×. |
| R3 | Severity of draft A's fault defect | "Conditional pass, fix required" | "Plan-level blocking defect" | Same remedy (MX-2). Treated as CRITICAL. |
| R4 | A-F′ minimal-exploration arm vs routing | Either | Either | **Routing chosen**: a conditional, capped Z2 diagnostic, not a standing arm. This keeps the confirmatory family at two comparisons. The Z2 trigger is pre-declared (Experiments §6). |
| R5 | Verification of script-level claims | Accepted A's B03/B04 details | Marked them unverified | **Verified this round** by direct source read (Corrected conclusions §0): B03 lines 84–95, B04 lines 63–66, 106, 125, B01 line 33. |
| R6 | Positive case for z-exploration | Credits A's mechanism list | Calls B's positive case thin and A's richer | Merged (§4.2). D3 stays open and is not argued from inner-product smoothness or dimension. |

No residual disagreement concerns the owner call, the eligibility of either draft, or the CRITICAL list.

---

## 6. Staged spend gate

Units:
- **transition** = one control step of one environment instance, aggregated across all parallel environments.
- **vector step** = one synchronous step of all N environments = N transitions.

Every cap below is in transitions. The production source-ramp unit ("100k control steps") must be resolved at Stage 0 (Gap G17).

Throughput assumption, to be replaced by Stage-0 measurement: end-to-end training throughput of **2k–20k transitions/s per accelerator** for off-policy arms with recurrent planner/critic updates. Inference-only evaluation runs at **20k–200k transitions/s**. Hours = transitions ÷ throughput ÷ 3600, × 1.5 for evaluation, I/O and checkpoint overhead.

| Stage | Content | Interaction ceiling | Accelerator-hours (order of magnitude, from the assumption) | Gate to enter | Gate to exit / next |
|---|---|---|---|---|---|
| **S0 Entry integrity** | Production identity resolution, fixtures, ≤10k audit transitions, throughput benchmark ≤100k transitions per arm type, telemetry patches (executed-z source tags, planner-z knob present but off) | ≤ 0.41M | ≤ 8 | Owner approves this disposition | All fixtures pass; caps and hour ceilings frozen in the manifest. Any failure → repair, bump the protocol version, rerun S0. **No efficacy spend before S0 passes.** |
| **S1 A Stage 1** | Setup: ≤2 configs × 4 arms × 1 seed × ≤1.5M. Test: 4 arms × 5 seeds × 15M. E0 probes at 25 / 50 / 100%. | Training ≤ 312M; evaluation ≤ 34M; probes ≤ 1.4M | ~6–70 | S0 PASS | Interim report. Stage-2 learning gate (L-gate): ≥1 arm with ≥3/5 seeds ≥16/100 at 0.10 m in the final pooled panel (Wilson LB ≥ 0.10), **or** E0 PASS on A-F. If neither: stop and return to the owner as "task/budget adequacy unresolved". No framework conclusion. |
| **S1-Z2 (conditional)** | Planner-z tangent-noise diagnostic, 5 seeds × 15M | ≤ 75M + 8M evaluation | ~2–17 | Z2 trigger (Experiments §6) | Z2 E0 PASS → revised framework enters S2 on fresh seeds. Z2 fails → D1 escalation (§1). |
| **S2 A Stage 2** | Extend all arms to 100M per run, or restart on fresh seeds if the framework was revised. Seeds 5 or 10, fixed from Stage-1 paired SD before any Stage-2 outcome. | +1.70B (5 seeds: 20 runs × 85M) to +3.70B (10 seeds: the same plus 20 new runs × 100M); evaluation ≤ 1.6M per run | ~35–770 | L-gate PASS **and** owner spend approval against measured S0 cost | Confirmatory A verdict (Experiments §4.4) |
| **S3 C** | Donor 2.5M; offline updates 200k; V training 5M; evaluation ≤ 8.3M | ≤ 16M plus 200k offline updates | ~1–5 | S0 PASS + E0 PASS (A-F or Z2-revised) + A-F ≥3/5 seeds ≥39/100 at 0.10 m (Wilson LB ≥ 0.30). **Not** gated on A superiority. | C verdict (Experiments §7.5) |
| Deferred | Full E2 sweep (near ablation Z1, Z3/Z4 nulls), K sweep, second C target task | — | — | A SUPPORTED/PARTIAL and D1 PASS | Separate pre-registration |

**Hard rules for every stage:**
- No training runs in this sandbox. All runs are planned external steps.
- Caps may be lowered and never raised after the S0 freeze without a new owner approval and a protocol version bump.
- Every attempted, rolled-back, evaluation and probe transition is counted.
- No stage can promote B01–B05 PASS to framework evidence.
