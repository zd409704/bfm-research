# Prin-3 Author A (Opus): one-page summary

Full text: `packets/Prin-3/proposals/A.md`. Generic home humanoid / target plant only.

## Thesis
The S2a-XC FAIL shows that **one realization** fails engineering sufficiency: a motor-side "realized" effort export under XC-0, on a planar fixture, scored against **placeholder** `(q, r)`. It is not a Principle result. **No grade changes** (B.9.8).

## What the data say about C-P1-012 (Grade 2 Candidate)
- **No falsifier fired.** This holds for Factor E and Factor R, at both DOWN and UP placements. It counts as one weak, single-fixture failed counterexample search, logged only.
- **The falsifier is degenerate.** All three Factor E "matches" at DOWN (d10M2, d10M5, d20M2) are cells where both detectors fail (TPR < 0.05). p95 is `inf` in most cells, so the latency term is undefined.
- **The B.9.3 substitution test has power.** UP drop is met (mean 0.56). DOWN drop is not met (min 0.06, mean 0.11). Motor-side effort does not realize the role when the dominant nuisance is downstream of sensing. Calibrated drift is about the same for CMD (0.35) and REAL_DOWN (0.33), against REAL_UP (0.02). This is the outcome H3 predicted.
- **Factor R is unadjudicated.** The fixed-gain·T design confounds rate with observer bandwidth. The sensitivity artifact is needed.
- **The harness can identify contacts.** ORACLE meets 9/12. Even UP meets 0/12 under Bonferroni q0.90, so the placeholder `(q, r)` may itself be binding.

## Proposed B.9.6 amendments (adjudicator: Astra)
| ID | Amendment | Counts toward B.9.6? |
|---|---|---|
| A-1 | Match only on a pre-registered identifiable set (ORACLE meets, and the reference TPR ≥ 0.5). If fewer than 3 classes qualify, the search is inconclusive. | No (falsifier repair) |
| A-2 | Replace p95 with restricted-mean or KM latency, censored at d | No |
| A-3 | Factor R is admissible only with a bandwidth-decoupled (optimized-tuning) cell | No |
| A-4 | Restate Factor E by **measurement point relative to the dominant nuisance**. Add a **CMD + identified friction-model** cell. If that cell matches, it signals retire-nominate for Factor E. | Arguably no. If yes, the counter goes to 2 and the next event triggers retirement review. |
| A-5 | Keep UP / dedicated sensing **out of scope** (premise 5). UP serves as a positive control only. | No |

Each amendment carries its own falsifier (see A.md §3). The upgrade-log counter (0) needs reconciling with the Prin-1 ruling (event #1 accepted).

## Eng-2: gates before ranking
- **B (S0a envelope, amended): ELIGIBLE (conditional).** The conditions are amendments before the spike, placeholder thresholds declared, and bypassed edges listed.
- **Amended-A as an engineering retry: INELIGIBLE now.** It fails G-4 (`(q, r)` not ratified) and G-5 (target-plant sensing placement not declared).
- **Amended-A as a C-P1-012 counterexample search: ELIGIBLE.**

**Recommend B** as the Eng-2 mainline. B wins by the Alternate rule and elimination, not by necessity, and D-P1-001 stays Provisional. **Alternate (Principle track, parallel, cheap):** run the C-P1-012 v3 search with A-1 to A-4 under a sealed PLAN. **Reject:** relaxed-threshold retry, widening scope to include UP, citing the FAIL as necessity or ordering evidence, and "neither".

## Human lead
Ratify the `(q_c, r_c)` task table. Declare the target plant's effort measurement point(s) relative to the dominant actuator nuisances. No locks.

## Over-reading risks
Each of these misreads the FAIL: "floor unachievable", "downgrade C-P1-012", "C-P1-012 now supported", "add torque sensors and S2a is solved", "S0a first by necessity", "XC-0 insufficient for home tasks" (the `(q, r)` are placeholders), and "loosen thresholds and retry".

## Adjudicator follow-up
- **C-P1-012:** rule on A-1 to A-5 and reconcile the counter.
- **C-Eng1-A-01:** run the i.i.d. audit of pooled-seed windows. No state change.
- **C-P1-011, C-P1-002:** none.
