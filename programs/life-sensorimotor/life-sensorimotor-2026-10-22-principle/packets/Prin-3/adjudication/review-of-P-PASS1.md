# Prin-3 blind review — B on rival P (proposal A)

Reviewer: B. Reviewed only rival P, filed as `proposals/A.md`; did not read `proposals/B.md`. This is a proposal review, not claim adjudication. No claim grades, states, or proposal files are changed.

Basis: `brief.md` rubric; Prin-3 packet brief and Appendix B; proposal A; source Eng-1 decision, METRICS and VERDICT; C-P1-012 claim record. Numerical statements below refer to these filed artifacts; missing sensitivity/contrast details are not independently verified here.

## Disposition and gates before ranking

**Eligible for Principle review; incomplete as an actionable Eng-2 gate specification. Recommend amendment before adoption.** The preference for amended S0a is defensible under the Eng-1 Alternate rule, but P has not established that it is the only eligible engineering route. This review does not rank P against the unseen rival proposal.

| Gate | Review finding |
|---|---|
| Locked Grade-1 conflict → reject | None identified in the supplied argument. P asserts no new lock, human signature, or grade change. There is no demonstrated Principle basis to reject P outright. |
| Missing Locked Grade-2 role → incomplete | No applicable locked role is identified as missing. The incompleteness here concerns experimental and decision specifications, not a newly imposed Grade-2 veto. |
| Candidate claims cannot veto; Grade-3 edges cannot bind | P explicitly preserves both rules and D-P1-001's provisional status. However, G-4 imports C-P1-012 H5 into a categorical engineering exclusion without establishing an independent binding requirement. This must be repaired. |
| Engineering readiness | S0a remains conditional on substantive amendments that P does not specify. Amended S2a can remain a scoped, provisional engineering candidate with declared simulated placements and placeholder thresholds. Task ratification is needed for task-level acceptance, not demonstrated here as a prerequisite to every fixture experiment. |
| Counterexample-search readiness | Eligible to develop a PLAN, but not ready to execute from P alone: A-1 leaves `q_id` and the reference cutoff open; A-2 leaves the latency statistic undecided; A-3 leaves tuning protocol and budget unspecified. G-4 is not simply “n/a”: A-1 itself uses an absolute identifiability threshold. |
| Reject risks | Reject an inference of necessary S0a-first order, a Candidate-based veto, retroactive rewriting of the filed FAIL, or universal necessity from the substitution contrast. These are prohibited conclusions, not reasons to reject all of P's useful amendments. |

## Principle integrity and reading the FAIL

P correctly distinguishes A02 engineering insufficiency from claim falsification, preserves Candidate status, treats UP as outside the current scope, and declines to infer hardware transfer. Its attention to Factor R's bandwidth confound and the pooled-window independence premise is valuable. It also correctly leaves detection data from this spike out of C-P1-002's response claim.

Three statements nevertheless overreach:

1. **“The operational test has power” needs a narrower interpretation.** UP meets the registered substitution criterion and DOWN does not, but a positive-control separation does not establish calibrated power to recognize every realization of an implementation-independent role. The VERDICT explicitly limits non-realization to “this fixture, detector and calibration.” Carry all three qualifiers into the thesis and I-2/I-3. P's later caveats do not fully repair its broad claim that measurement placement is *the* operative variable.
2. **A false counterexample flag is not a conclusive failed search for a competent role-free system.** The recorded Factor E/R flags are false; retain that historical fact. P also identifies undefined latency comparisons and a confounded rate comparison. Log those limits with the result and label Factor R unresolved pending sensitivity analysis. Do not count an inconclusive comparison as satisfying the serious failed-search component of B.9.2. A-1's reference TPR of 0.5 alone does not establish the competence class that a necessity counterexample must attain.
3. **Oracle success is a fixture control, not an ordinary-channel feasibility proof.** ORACLE success on nine classes supports harness identifiability under oracle access. It cannot establish that proprioception or an admissible export can reach the same operating point. Similarly, UP's reported Bonferroni 0/12 warns about the acceptance calculation; it does not prove thresholds infeasible or establish that human ratification would resolve the statistical problem. A02 remains the filed FAIL, independently of these interpretations.

## Concrete objections and required repairs

**1. G-4/G-5 create asymmetric eligibility rules (major).** P permits S0a thresholds to be declared placeholders *or* ratified, but requires ratification before any S2a engineering retry. The Eng-1 decision explicitly allowed a placeholder task table in a sealed engineering spike. C-P1-012 H5 constrains a necessity claim's premises; it does not itself prohibit exploratory engineering with placeholders. Likewise, simulated placement variants can be declared without claiming target-plant transfer. Apply the same rule to both routes: fixture work may proceed provisionally with declared assumptions; claims of task acceptance or transfer require matched requirements and plant evidence. Any stricter scheduling preference should be stated as a proposed planning choice, not an existing Principle veto.

**2. A-4 is a substantive change, not an established physical equivalence (major).** “Downstream of the command” and “downstream of the dominant unmodeled effect” are different requirements. Declaring sensor placement in premise 2 does not require a particular placement. Nor does non-reconstructibility from commands prove that physical downstream sensing is the only way to obtain relevant information: the claim itself admits an observer-exported residual. P's parenthetical equivalence between downstream placement and observability needs an argument. A universal spatial condition also risks requiring sensing that A-5 simultaneously keeps outside the covered plant class. Keep the functional role implementation-independent; describe placement as a tested realization condition. If A-4 is retained, supply a premise/scope redline and leave its B.9.6 treatment explicitly to the adjudicator.

**3. A-1/A-2 are useful repair directions, but not complete falsifiers (major).** Specify `q_id`, confidence treatment, the reference cutoff, minimum class count rationale, and how the identifiable set is selected without using the final evaluation outcomes to favor a comparison. Separate oracle identifiability, reference competence, and candidate competence. Report excluded classes and preserve the original result alongside the revised protocol. Equal membership on this one dataset does not prove a rule is semantically only a clarification.

For latency, select one statistic and one tolerance before running. Restricted mean and Kaplan–Meier median are not interchangeable; the median can also be unestimable when fewer than half the events are detected. Censoring at contact duration `d` changes the observation horizon: the filed UP d20M10 p95 is 23 ms, already beyond `d`. Define the task's allowable detection horizon and handling of misses. Do not drop latency and adjudicate on TPR alone merely because two latency estimands disagree after the run.

**4. A-3 needs a fair tuning experiment, not just a second setting (moderate).** Optimizing each rate can help, but specify equal tuning budgets, permitted parameter ranges, stability checks, separate tuning/evaluation data, and matched false-event calibration. Matched continuous bandwidth may be infeasible at the slower sample rate; that limitation must be reported rather than silently changing the comparison. Retrieve and assess the already-filed sensitivity artifact before requiring a new run. Disagreement between tuning regimes is evidence of sensitivity, not automatically an uninterpretable result: a valid competent low-rate counterexample must still receive adjudicator review.

**5. The model-compensation cell needs a premise audit (major).** CMD plus a model identified on disjoint data is a useful stress test. If it removes the very unmodeled nuisance required by the claim, a match is a premise-failure result, not an in-premise refutation. If relevant nuisance remains and the command-only system meets the stated competence, it could challenge Factor E. Specify which of these cases is being tested and compare under matched plant conditions. “Any competent design already does” actuator modeling is not a reason to retire a functional role; distinguish a ubiquitous role from an unnecessary one.

**6. B.9.6 accounting cannot be decided by amendment labels (moderate).** A-1 through A-3 need not all be narrowing events, but “falsifier repair” does not automatically exempt a semantic change to what evidence can refute the claim. Ask the adjudicator to assess each change's effect on scope and premises, reconcile the previous counter, and record rationale. P does defer the A-4 decision appropriately; extend that discipline to the full amendment set. A third qualifying event triggers retirement *review*, not automatic retirement. P's assertion that retirement “needs falsification or ... count 3” also overstates B.9.6: it mandates review at three; it does not make those the exclusive reasons to consider retirement.

**7. S0a is recommended before its missing amendments are concrete (major).** The predecessor says its frozen spike is low-information and must be amended. P mostly repeats that obligation. Require the Eng-2 proposal to specify the richer plant/mode set, discriminating failure case, horizon and disturbance assumptions, pass/fail rule, and observable output contract. Identify body-loop enforcement ownership, scene-publication interface if used, and decision-core consumption, including timing assumptions. Until then S0a is a provisional direction, not the “remaining eligible” executable candidate. Absence of a locked veto also does not logically reject “neither”; deferral may have engineering or resource reasons, although P may reasonably prefer continued work.

## Fixed-rubric scores

Scores assess P as written; higher is better. They do not override gates or change any claim grade.

| Dimension | Score (1–5) | One-line reason |
|---|---:|---|
| Constraint fit | 4 | Preserves scope, grades, generic plant framing and the no-rerun constraint, but invents a stricter engineering eligibility requirement. |
| Principle integrity | 3 | Strong necessity/sufficiency separation is weakened by A-4's spatial requirement and premature amendment-count exemptions. |
| Falsifiability | 3 | Concrete contrasts can fail quickly, but competence, class selection, latency and tuning rules remain underdefined. |
| Evidence demand | 4 | Reuses a cheap local fixture and disjoint-data controls; inspect existing sensitivity results before adding runs. |
| Failure modes | 4 | Identifies floor matches, censoring, placement, bandwidth and independence risks, but underchecks premise escape in the compensation test. |
| Integrability | 2 | Recommends S0a without a concrete amended interface or ownership contract across body loop, scene publication and decision core. |
| Latency / criticality | 3 | Notices unusable p95 values and rate confounding, but the replacement horizon and S0a timing assumptions are unresolved. |
| Complexity cost | 3 | Most added controls are motivated, but optional estimands and multiple tuning regimes need one bounded protocol. |
| Reversibility | 4 | Local simulation and unchanged claim states are easy to abandon; categorical retry exclusions would unnecessarily restrict options. |
| Stackability | 3 | Preserves non-necessary ladder ordering, but future integration depends on an unspecified S0a contract. |

## Adjudicator follow-up

- **C-P1-012:** assess A-1–A-5 individually, including scope/premise changes, the operational-test qualifiers, model-compensation premise match, and reconciliation of the existing B.9.6 counter. Preserve grades and filed verdicts pending authorized adjudication.
- **C-Eng1-A-01:** audit the independence/calibration assumptions behind pooled-window certificates; failed assumptions limit certificate applicability without refuting the conditional lemma.
- **C-P1-002 / C-P1-011:** no new action justified by this review.

**Recommended disposition:** retain P's provisional preference for an amended S0a packet and its proposed Principle search; require the repairs above before adopting its Eng-2 eligibility table or revised falsifier. Preserve the sealed Eng-1 FAIL and every existing claim grade.
