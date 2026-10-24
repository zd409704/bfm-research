# Adjudication — Sonnet, Presentation Order 2 (P and Q reversed)

Round: feedback-round-2026-10-24. Program: fb-beyond-imitation-acceleration. Date: 2026-10-24.
Inputs read: charter, brief, owner feedback, the P and Q indexes, all ten inventory files, and both blind critiques (critique on P, critique on Q). I did not read `adjudication-agy-order1.md`. I ran no code or training and pushed nothing. I did not re-open B01–B05 source scripts, so I treat script-level claims (B03 0.5625 bound, B04 setup) as the authors' and critics' assertions.
B01–B05 script/GPU PASS is treated as local-check evidence only, never as framework validation.

## 1. Eligibility and hard-constraint gate

| Check | P (Order 2) | Q (Order 2) |
|---|---|---|
| All five deliverables present | Pass | Pass |
| English only; no commercial robot, product or company names | Pass (critique ran a token grep) | Pass (read-through; only generic algorithm-family wording) |
| Under `/srv/claude`; no invented production paths | Pass; production entrypoints are listed "to resolve" | Pass; production work marked planned-external |
| B01–B05 PASS not claimed as framework validation | Pass, stated up front | Pass, stated up front |
| No BC/tracking fallback in the framework (charter §2.1) | Pass; imitation arm is an explicitly exempt comparator | Pass in substance; the exemption for the TR comparator is not stated (critique flags ambiguity) |
| Failure vs invalid semantics (charter §2.4) | Pass; invalid runs retained, repaired reruns separately identified | **Plan-level defect.** E1 auto-restarts after `invalid` halts and excludes an arm after more than 2 halts. This conflicts with "halt for inspection" and can bias the comparison |
| No bundled whitening, same-height relabel, world-model loss or B-input expansion | Pass | Pass |
| Owner deliverable 5 (configs, identities, curves, costs) | Partial: identities and curves are detailed, but there are no cost figures | Partial: identities and curves are present, GPU-hour ratios are reported only as estimates, and steps are not defined across vector environments |
| Sibling isolation | No violation observed | No violation observed |

Gate verdict: both packages are **eligible**. No disqualifying violation. Q carries a blocking protocol defect (invalid-run handling) that must be fixed. P carries a missing-cost gap that must be filled.

## 2. Comparative scores (0–100)

| Dimension | P | Q | Justification |
|---|---:|---:|---|
| Framework-theory soundness | 78 | 74 | P keeps premises tight: the readout is linear in w_r only for a fixed policy, the extreme-point caveat on linear preferences, contact aliasing needs full-input and occupancy premises, and the F·z and 50/50 semantics are preserved. Its weakness is a thin positive case for z-space exploration. It never separates temporal correlation from learned structure, and it under-weights the consequence of deterministic planner execution. Q is richer: it has a cold-start deadlock mechanism, a time-based rather than competence-based schedule hazard, and an explicit list of why z might help with a skeptic's null. But it overstates in places: "every transition trains all z", ideal-FB optimality attributed to the learned controller, contact impossibility stated without the B03 premises, and a "thin demo tube" claim that is a risk, not a proof. |
| Implementation-gap honesty | 80 | 76 | P's Observed / Reported / Specified / Pending labels are applied consistently, and each row has a minimal closing evidence. Gaps: no row for executed stochasticity by source, and it blurs "no class in this tree" with "no production class". Q's table is more informative (priorities, planner-z gap, time-based schedule, run identity). But its "Exists" column mixes owner audit with baseline contracts, the priority of the BN-order test is inconsistent (P1 in the table, planned in §5), and it does not audit the three data paths explicitly. |
| B01–B05 claim re-scoping | 76 | 84 | Both reflect every owner correction. Both catch the B03 point that 0.9105 is predictor error above a 0.5625 bound for that setup. Q goes further with per-number slots: B01 spectrum imposed by the script, B03 aliasing 0.0 tautological, B04 toy dimensions and favored whitened reference, withdrawal of the H=0 orthogonality reading. P's critique correctly notes that neither draft says the B03 `> 0.40` assertion can never fail. P lacks a per-number list and does not link the B02 Gaussian-KL gate to deterministic execution. Q's extra details are not independently verified (the critique on Q says so). |
| Minimal-experiment design quality | 70 | 55 | P has an entry integrity gate, seed-level inference, paired seeds, full cost counters, and a causally designed C (common donor pool, C-use vs C-omit, three retention senses measured separately). Its main flaw is that A is probably too small to be informative: 1M aggregate transitions with an absolute gate of 79/100 at both heights in 4 of 5 seeds, with C gated on A. It also lacks a temporal-correlation control, tests the framework with planner exploration off against a baseline with its normal noise, and has no power statement (the 97.5% t-interval at 5 seeds needs a large mean effect). Q correctly adds a correlated-noise arm and a controllability probe. But its decision rules have a blocking statistical defect: a median ratio with S_max substitution means both-fail gives ratio 1 and triggers REFUTE. E0's CR metric is not a validated construct, yet it has stop authority; it omits velocity and leaves its feature set unspecified. The budget is up to about 8.2B steps, which is not small scale. C is an outline, not a preregistration, and its return filter confounds turnover with usefulness. |
| Investment-judgment clarity | 62 | 80 | Q gives one category, three decisive assumptions (D1–D3) with if-false consequences, kill criteria, and a most-promising-benefit vs strongest-objection pair. Its 0.67 ratio conflates an investment hurdle with scientific falsification. P gives a compound verdict ("substantive revision … revise-then-continue at small scale only") that spans owner categories, and has no enumerated decisive assumptions. Its benefit/objection pair is good. |
| **Sum (unweighted)** | **366** | **369** | Statistically a tie. P leads where evidence can be trusted (protocol, integrity). Q leads where the owner asked for judgment (assumptions, cold start, exploration mechanism, per-number corrections). |

## 3. Disposition

**Recommend: Hybrid, with P as the experimental and protocol base and Q as the theory, gap and decision-framing base.** If a single package must be chosen, choose P: its plan can be repaired by adding items, while Q's E1 rules and fault handling need rewriting before they could govern spending.

**Alternate: Q.** Prefer it only if the owner values the early controllability probe and a richer exploration story above statistical safety, and accepts that its rules be rewritten before launch.

### Mandatory merge/fix items

1. **One owner category plus decisive assumptions.** Use Q's D1 (controllability), D2 (efficiency), D3 (z-exploration specificity), and add P's objective-sufficiency and planner-coverage conditions (a planner cannot select what the actor cannot execute). State what each failure implies and keep "investment hurdle", "no benefit on this task", and "mechanism falsified" distinct.
2. **Make A informative (applies to P).**
   - Justify the transition budget from measured throughput or learning curves, and state units across vector environments.
   - Split the efficiency endpoint (AUC) from the absolute-competence gate so efficiency can be shown or refuted without 0.70 by the cap.
   - State assumed seed SD and minimum detectable effect at five seeds, or raise seeds.
   - Fix the n=20 intermediate-panel Wilson inconsistency.
3. **Censor-aware decision rule (applies to Q).** Predeclare an estimand for non-attainment. Both-fail is INCONCLUSIVE, never ratio 1. Freeze the comparator before test seeds. Define the one allowed seed-extension procedure and seed-level resampling.
4. **Auditable fault protocol (applies to Q).** Replace auto-restart and exclusion with inspect-then-recover. Keep every scheduled seed, keep valid physical failures as committed experience, and charge rollback and restart work to cost.
5. **Temporal-coherence and exploration controls inside A.** Take Q's DA-C (correlated action noise at matched variance) plus an action-repeat or macro-decision null. Either add a minimal-exploration framework variant or declare up front that an A-F failure with exploration off cannot be attributed to the architecture. Keep a capped diagnostic path for exploration failure rather than closing it after one refutation.
6. **Controllability evidence without stop authority from a weak metric.** Keep E0-style branching but freeze the feature metric and goal pools, include velocity, report both horizons, preserve terminated branches, provide an INCONCLUSIVE outcome, and bootstrap over seeds. Poor demo-pose CR alone must not reject the framework. Use controllability (not A superiority) as the C launch gate, with P's C design plus size-matched random-omission and positive-control branches.
7. **Cost realism and launch gate.** Give order-of-magnitude accelerator-hours, wall-clock and memory ranges with assumptions, pilot and extension caps, and a staged launch order that does not commit baseline spend before the controllability check.
8. **Theory premise repairs.** Reword "all-z" claims as sampled-update claims, distinguish ideal FB from the learned controller, restore B03 premises on contact impossibility, and state planner-z confinement as a measurable coverage risk. Add negative-transfer mechanisms, a discriminating early cold-start signal, and the planner-output off-support risk.
9. **Corrections ledger.** Merge Q's per-number re-scoping with P's cautious wording. Add that the B03 `> 0.40` assertion is unfalsifiable. Give exact source/result pointers for the 0.5625 convention and B04 setup. Note the Wilson rule was checked as a formula only. Link the B02 Gaussian-KL drift gate to deterministic `.loc` execution. Mark H1 untested and deprioritized.
10. **GAP table.** Take Q's priority column and planner-z row. Add P's provenance labels. Add rows for executed stochasticity by source, the three data paths, evaluation/collection protocol, and demonstration coverage. Mark the production class identity as unresolved, not absent.
11. **Define the Q-calibration target and drift metric** (full-return or compatible bootstrap; a non-Gaussian drift measure for deterministic execution), and choose gating versus non-gating consistently.

### Confounds in this adjudication

- **Reviewer asymmetry.** The critique on P ran an arithmetic check and spot-checked source, and listed many minor items. The critique on Q did not verify script-level claims and listed three criticals. Severity labels are not calibrated across the two, so I weighted content over label counts.
- **Different scale choices.** P's 1M-transition budget and Q's 150M budget are not comparable. Neither is grounded in measured throughput, so "too small" and "too large" are both unverified.
- **Length and verbosity.** P's weight is in the experiments file, Q's in the review file. I scored on content, not size.
- **Unverified source claims.** B03's 0.5625 bound and B04's toy setup were asserted by both authors or critics and not independently re-run by me.
- **Presentation order and independence.** This is the Order-2 labeling, and the two adjudications should be reconciled by the orchestrator, not by me. I avoided reading the other order's output.
- **Gate-sensitive scoring.** Moving a mandatory-fix item between "eligibility" and "design quality" (notably Q's fault protocol) could flip the narrow score gap, so I report the disposition as Hybrid, not as a margin win.

## 4. Final investment call

**revise-then-continue**

Reason, checkable: no empirical cell of the causal chain is filled, and neither package makes B01–B05 PASS count as validation. The architecture is coherent enough to test, and the absence of a convergence proof is not grounds for rejection. But the validation plan needs the revisions above before spend, and the as-implemented collector lacks planner-z exploration and has a time-based source schedule. Continue only at bounded small scale after the integrity gate and the revised A and controllability checks, with C launched on demonstrated controllability. Escalate to substantive architectural revision if controllability fails or an adequate simpler baseline wins while the framework misses its gate. Stop this configuration if both persist after one capped exploration-repair diagnostic.
