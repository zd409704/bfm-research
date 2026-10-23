# Eng-1 — Blind Reviewer B on Proposal A (S2a-XC)

Reviewer: B (Astra). Scope: Proposal A only. Read `proposals/A.md`, `drafts/A/summary.md`, `drafts/A/spike-PLAN.md`, `claims/C-Eng1-A-01/claim.md`, the brief/rubric, and all seven `Eng-1/source/*` files. Additionally checked canonical `claims/C-P1-012/claim.md` to verify the claimed registered-search match, the new claim's artifact filenames, and the PLAN hash. Proposal B and drafts/B were not read. This review changes no claim state and provides no B.9.2 lock verification.

## Summary

S2a-XC is a useful, reversible engineering candidate: a versioned body-loop export, explicit side-channel register, and held-out detector test. Its strongest feature is the distinction between positive evidence that a declared joint channel carries contact information and the absence of any inference from detector failure. It preserves D-P1-001, acknowledges that all relevant claims remain Candidate, and lists bypassed Grade-3 edges.

The narrow C-Eng1-A-01 argument is mathematically coherent under its premises. The sealed experiment does not yet warrant the stronger presentation of a repaired factorial or reliable floor-certification harness. Calibration, multiple testing, event timing, and false-event units need repair. Placeholder requirements permit a provisional fixture study, not task acceptance. Lean: **Alternate / revise before Recommend as the next mainline**. This is an absolute assessment of A, not a comparison with an unseen proposal.

## Gate notes — before scores

- **Locked-principle gates: pass / none applicable.** The source decisions establish no Eng-1 ladder-edge gates. A neither violates a Locked Grade-1 claim nor omits an applicable Locked Grade-2 role. Candidate C-P1-012 cannot veto it. The bypass list satisfies the relevant B.8.5 obligation.
- **Claim governance: pass for exploration.** C-Eng1-A-01 states premises, scope, falsifier, author/adjudicator separation, and Candidate status. The three B.7 artifact filenames exist. Its derivation is not an authorized lock check; no signature or state promotion follows from this review or a harness PASS.
- **Engineering readiness: incomplete.** The PLAN exists and its SHA-256 matches the filed hash, but no runnable harness or result was supplied. The brief therefore permits only a provisional decision. Fixes below require a newly versioned, sealed PLAN, not silent runner discretion.
- **Task acceptance: pending.** The human lead has not ratified contact classes, q/r, or latency requirements. The explicit placeholder flag is good discipline, but does not establish an operational S2a acceptance floor.
- **Planning rationale needs correction.** Proposal §1.3 says richer S0a certification would let planning order pose as necessity. Such certification can be a legitimate engineering choice under D-P1-001. Likewise, merging fixtures does not itself recreate a rate/source confound (§1.4); experimental controls determine that. Retain the concrete evidence-demand argument and remove these unsupported methodological objections.

## Concrete objections and required repairs

### 1. C-Eng1-A-01 is sound pointwise; the reporting protocol exceeds that scope

For a fixed detector and conditional probability model, KL data processing gives `D(P1 || P0) >= d(TPR || FPR)`. On the joint coverage event, `TPR >= L > U >= FPR`; binary KL increases in its first argument and decreases in its second over this region. Thus the claimed lower bound follows. Independent calibration is compatible with this argument by conditioning on the calibrated detector. This supports Candidate-stay, not a lock.

The PLAN, however, evaluates two r-specific detectors in each of 96 cell/class combinations, with pooled-seed and additional control outputs. Alpha/2 covers the two binomial endpoints for **one fixed detector**, not both thresholds, every class, or a selected winning cell. The current certificate format also does not clearly identify which r-specific detector produced each bound. State explicitly whether coverage is pointwise or simultaneous; give each detector its own ID and certificate; and predefine multiplicity control or independent confirmation for any selected export or packet-wide claim. The two q values can reuse the same detector bounds; the two r values cannot silently share a single 95% claim.

State `0 < r < q <= 1` in the interface contract, not merely `r > 0`. Require consistent log units for channel KL and `d_cert_bits`. For finite samples, a zero observed FPR still yields a positive upper bound. Keep that distinction explicit. Certificates concern `(X,W)` and the declared episode distribution, not XC-0 alone or every duration/location instance inside a class.

### 2. H2/H3 confuse statistical outcomes with harness correctness

H2 requires every NULL certificate to equal zero. The claim record correctly allows a nonzero false-certification probability under the null. Across many tests, a valid harness can produce a positive bound somewhere; that is not automatically a software defect. Replace the universal-zero rule with a predeclared coverage check with a statistical tolerance, and separately test deterministic invariants.

H3 requires an ORACLE FPR upper confidence bound at or below 0.01, but thresholds are calibrated to the empirical 0.99 quantile. If the true FPR is exactly 0.01, a 97.5% one-sided upper bound falls below that boundary only at approximately its lower-tail error rate. Good detection sensitivity cannot fix this. Calibrate conservatively below r, using a predeclared tolerance/order-statistic procedure and enough calibration data; reserve independent data for certification. Distinguish an informative certification failure from an invalid implementation. This issue also affects every non-oracle `meets` result.

### 3. The factorial repairs the original comparison only partially

Crossing rate and effort source removes their original bundling. Declaring both motor-side and output-side measurements improves physical honesty. Fixed `gain*T=0.25` also implements the mitigation explicitly suggested by C-P1-012 H2; credit is due for following it.

It does not isolate information loss due to rate. The physical observer gain changes from 50/s to 12.5/s, with nominal time constants of 20 ms and 80 ms. The slower detector therefore has a different response bandwidth within the same 100 ms window. A fixed-gain sensitivity trace excluded from verdicts is insufficient to call this fully repaired. Predeclare equal tuning budgets on independent data, a numerically appropriate matched-bandwidth comparison, or narrow the inference to these two rate-specific observer implementations. A successful low-rate counterexample remains useful; a low-rate failure does not establish a rate floor.

Placement is also nested within REALIZED: CMD_RECON's specified signal does not change with placement while the true plant remains the same. Treat duplicate commanded conditions as paired/shared baselines, not independent placement evidence. State sensor-relative friction placement unambiguously, use common plant episodes for contrasts, and report rate-by-source interactions. An output-torque-sensor result also needs scope qualification because canonical C-P1-012 excludes plants with dedicated torque sensing; it cannot silently adjudicate the same target scope as current-derived effort.

### 4. The claimed registered-search match changes false-event units

Canonical C-P1-012's registered PLAN specifies a false-event rate of **0.01/s**. A uses FPR **0.01 per 100 ms window** while calling its contrasts the registered criteria. With ten nonoverlapping windows per second, that is nominally 0.1 flagged windows/s; alarm-reset and event-merging rules still need definition. The numerical TPR/latency margins match, but the operating point does not.

Reconcile this through an explicit registered amendment or preserve the original false-event requirement and define its mapping to window decisions. Recalculate calibration and evaluation sample sizes accordingly. Do not describe these results as the original counterexample search until the units and event semantics agree.

### 5. Contact timing and latency are underspecified

An onset as late as 60 ms with duration 50 ms extends to 110 ms, beyond the 100 ms window. Some nominal 50 ms contacts are therefore censored. Also, a CUSUM crossing before onset counts as a positive window under the stated decision rule and yields negative latency. Misses have no specified latency treatment, so p95 could look favorable by excluding difficult contacts.

Seal a rule for complete versus censored pulses, pre-onset alarms, detector initialization/reset, and missed detections. Report detection probability alongside latency with a declared censoring policy. Define whether the contrast margins are one-sided noninferiority or absolute differences, and attach uncertainty to the matching decision. A weak reference and equally weak substitutes can satisfy relative margins without reaching any contact-detection competence.

### 6. Placeholder q/r and the substitution test do not establish the proposed role

The placeholder labels are necessary and correctly present. They do not resolve C-P1-012 H5: task requirements remain unavailable. Ratify the class distribution, missed-contact cost, false-event units, and latency limit before calling an export task-acceptable. If ratification follows exploration, use a fresh confirmation set. Until then, describe results as provisional operating-point estimates and fixture certificates.

The substitution test selects “identifiable” classes using held-out `TPR_hat >= 0.5`, which introduces an evaluation-dependent subset. Predefine the subset or select it on separate data, and specify whether substitution freezes the detector or permits retraining/recalibration. A greater-than-0.10 drop establishes reliance by this detector under that intervention. A smaller drop does not prove that effort information or a functional role is absent: q/qdot or W may provide redundant information. Scope the proposed “role not realized” message accordingly.

### 7. The export contract needs enough detail to preserve the causal comparison

W lists command and reference but lacks their actual rates, history lengths, resampling, and availability times. A 1 kHz command history supplied to a 50 Hz cell can defeat the intended rate intervention. Declare the complete detector input history and prohibit future samples. Add observer equations/discretization, initial conditions/warm-up, CUSUM reset/tie rules, and a numeric method for exact bounds under the numpy-only constraint; these choices materially affect the planned conclusions.

Bitwise-identical simulated trajectories are a useful non-interference check, but do not establish publisher scheduling cost or real-time isolation. Add publication age/jitter and queue policy to the contract before hardware integration. Retain the current no-transfer scope.

## Scores — fixed brief rubric, 1–5 (higher is better)

| Dimension | Score | Reason |
|---|---:|---|
| Constraint fit | 4 | CPU-only, generic plant, reversible scope and no locks; provisional readiness and registered-search mismatch remain. |
| Principle integrity | 4 | Correct one-sided reasoning and quarantine; packet-wide confidence and role language need narrowing. |
| Falsifiability | 3 | Concrete controls and contrasts, but current H2/H3 can reject a correct harness and timing rules are incomplete. |
| Evidence demand | 4 | Local simulation is practical; conservative rare-event certification may need materially larger samples. |
| Failure modes | 3 | Many risks named, but calibration-boundary failure, multiplicity and latency censoring are unresolved. |
| Integrability | 4 | Clear ownership and versioning; W timing/history and publication semantics remain open. |
| Latency / criticality | 3 | Appropriate body-loop ownership, but observer bandwidth varies and latency statistics are not defined sufficiently. |
| Complexity cost | 3 | Certificate metadata is justified; duplicated factorial cells and statistical machinery need a tighter protocol. |
| Reversibility | 5 | Read-only export and local fixture are inexpensive to abandon or revise. |
| Stackability | 4 | Useful later-stage interface without forced ladder ordering; actual task requirements remain pending. |
| **Total** | **37/50** | Scores follow gates and do not grant claim authority. |

## Lean

**Alternate; eligible for a provisional Recommend after protocol repair.** Keep XC-0 and the narrow Candidate lemma. Before running the experiment, version and reseal the PLAN to fix calibration/control logic, confidence scope, false-event units, detector comparisons, and event/latency semantics. Task q/r ratification is required for task acceptance, not for authorized exploratory work. No current evidence supports a lock, a necessity claim for realized effort or R1, or a comparative ranking against another proposal.
