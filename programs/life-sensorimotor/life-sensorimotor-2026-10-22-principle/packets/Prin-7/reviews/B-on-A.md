# Blind review B on proposal A — Prin-7

**Disposition:** useful design input, but revision required before adoption as an executable PLAN. No comparative ranking is made. C-P1-012 remains Grade 2, Candidate; this review changes no claim, counter, decision, or engineering gate.

**Read boundary:** root and packet brief/roster; every supplied file in `source/`; `proposals/A.md`; and `drafts/A/summary.md` (the only file in that draft directory). The other current proposal and draft tree were not read. References to earlier competing proposals within the supplied source records were treated as inherited context, not independently inspected. No external search, proof attempt, refuter run, or spike was performed.

## Strengths

1. **The main scientific risk is correctly identified.** Sections 1–3 recognize that unrestricted nuisance inputs can make impossibility true by construction. AD-1 and AD-3 demand independently motivated mechanisms and realizable hidden-state witnesses, rather than treating membership in a broad amplitude envelope as physical realizability.
2. **Placement is substantive.** The mandatory downstream-friction variants expose the inherited H3 confound. Requiring a constructive positive result with the additional measurement is a useful stronger research target: it tests whether that measurement actually resolves the ambiguity.
3. **The detector quantifier is appropriately broad.** AD-5 includes adaptive and learning detectors and declared command history. RF-1 through RF-4 identify concrete structural routes by which a naive overlap argument could fail.
4. **Several inherited governance safeguards survive.** Full registered contact-class coverage, explicit subclass reporting, separate factor accounting, the existing narrowing count, independent proof verification, human signature for a lock, and preservation of the factorial falsifier are all visible. No score or spike is offered as Grade-1 evidence.
5. **Failure can produce useful information.** Placement failure, a separating detector, inadmissible nuisance assumptions, and budget exhaustion have distinct proposed outcomes. The plan explicitly avoids turning unresolved work into support for the claim.

## Defects and required repairs

### D1 — The deliverable is a PLAN schema, not a ready PLAN (major)

Sections 2 and 5 explicitly defer the nuisance-family choice and numerical budget. The family names do not specify generator equations, parameter domains, initial hidden states, or physically justified envelopes. Plant geometry is referenced rather than supplied. Contact onset/location classes, sampling/noise settings, allowed prehistory and commands, and the task contract remain open. K-nD contains only “general families.” No selected proof-check route is self-contained: the proposed published-result route identifies no result or premise match.

Symbolic parameters are legitimate; their domains and quantifiers must nevertheless be fixed. An executor must currently make substantive scientific choices before knowing what a counterexample is. Provide at least one fully specified minimal variant and its downstream companion, exact observation and event definitions, a bounded proof/refutation schedule, artifact destinations, and an explicit checking route. State which extensions are optional. The absence of a current seal is not itself a violation in this PLAN-only packet; the missing content prevents meaningful sealing for execution.

### D2 — L0 overextends the sampled linear model (major)

Section 4.1 first states a claim for the nonlinear rigid-body plant and then says sampled observations factor through per-interval linear functionals of residual effort. The two displayed moments are appropriate to the specified double-integrator simplification. They are not an exact sampled observation map for a general configuration-dependent inertia and nonlinear drift. Equal total residuals give the continuous-time indistinguishability route only with matching initial conditions and an appropriate well-posedness assumption; equal unweighted interval moments do not automatically extend that route to the nonlinear plant.

Separate the exact continuous-time statement, an explicitly restricted linear statement, and any approximate local statement with its error bounds. T-R must use the appropriate observation map. A future checker cannot repair a theorem target whose intended scope is ambiguous.

### D3 — Confusion is not yet linked to the declared detection contract (major)

T-E.i uses “large enough” without defining the probability space or contact aggregation. Its “power ≤ size” comparison concerns event probabilities, while Spec expresses alpha as false events per second. These quantities cannot be identified without a decision window, event-counting/refractory rule, and an explicit conversion. Worst-case performance over trajectories, stochastic measurement noise, randomized detectors, and a Bayesian prior also require different quantifier statements. Latency percentiles require a declared treatment of misses.

AD-3 requires equal state trajectories only over the decision window. Detectors may use earlier declared history, including calibration. A valid witness must match the entire permitted observation history available at the decision, or specify a common initialization and history boundary. Otherwise RF-2/RF-4 can distinguish histories excluded from the witness construction. Fix these definitions before proof or search.

### D4 — The measurement-conditioned ambiguity is oversimplified (major)

T-E.ii and section 8 replace the ambiguity with `Conf(U↓)`. In the augmented experiment the paired worlds must also have identical observed measurement histories. Upstream and downstream generators may share parameters, hidden state, loading, and control dependence; sampling and measurement noise further affect equality of observations. A Minkowski-sum notation alone does not specify the joint admissible world set or justify eliminating the upstream component.

Define confusion using pairs of complete admissible worlds and equality, or a declared distance, between their observation laws under each signal set. A strict shrinkage of a contact confusion set is also insufficient for the section 8 “iff”: it may leave the same worst-case task failure, or remove contacts irrelevant to Spec. Use a task-qualified separation criterion rather than treating any shrinkage as sufficient realization.

### D5 — Necessary information is conflated with sufficient measurement (moderate)

The inherited Grade-1 target states non-identifiability without a measurement. It does not logically promise that the measurement alone suffices. AD-4 is a useful additional requirement for demonstrating a practical separation, but failure of T-E.ii does not by itself disprove the weaker necessity proposition. O-2's statement that “Factor E's Grade-1 form fails” must distinguish failure of this stronger research target from refutation of the inherited statement.

Similarly, a single chosen effort measurement demonstrating separation does not establish that its physical implementation is uniquely necessary. State precisely which information distinction is necessary and which measurement is a sufficient witness. Keep any proposed change to the inherited claim separate and subject to adjudication.

### D6 — The formal outcome table can exclude adverse evidence (major)

Section 6 initially allows refuter success only through a separating detector or an admissibility failure. RF-5 instead challenges the positive half, and RF-7 may challenge a rate theorem. An incorrect lemma or proof also need not imply either of the two opening success categories. Add explicit theorem/derivation failures and distinguish an invalid proof from a false theorem.

More importantly, O-6 says an omitted rule routes to “AN only.” The supplied ruling's P-5 expressly preserves independent review of a concrete competent witness despite an unresolved registered comparison; P-7 also preserves review of unlisted evidence and premise failures. Include those overrides explicitly. O-5 may void a planned variant but must not erase an independently admissible witness against the original claim. The inherited claim and adjudicator's ruling control over the table.

### D7 — Independence and freeze order are not operationally bound (moderate)

Section 9 allows either family to prove, fixes the refuter to the review-side family, and requires prover/refuter families to differ. These conditions force the prover to the author-side family unless the table changes. The same review-side family is proposed for refutation and claim adjudication without binding separate agents. That is not automatically prohibited by B.9.1, but agent separation and the residual family affinity must be explicit, particularly for adjudicating a refuter-authored result. The proposed alternate rule is not a completed binding.

Section 5 seals before the added-premise ruling, yet allows premises to be dropped after that ruling. Require a new final seal after any such edits and before any proof or refuter work. An added assumption in an exploratory theorem is not automatically an accepted modification of the inherited claim; the adjudicator must specify whether a particular event actually changes claim scope or adds a survival premise under B.9.6.

## Appendix B gates before scores

| Gate | Assessment |
|---|---|
| B.3 explicit premises, scope, implementation independence, falsifier | **Incomplete for execution.** Broad detector coverage is strong; D1–D5 leave the actual experiment and theorem contract underdefined. |
| B.4–B.5 grade/state discipline | **Pass for this PLAN-only proposal.** No promotion, veto, or benchmark-based necessity is requested. |
| B.8 ladder/citation discipline | **Pass.** No evolutionary ordering argument or ladder mandate is introduced; citation ablation is inapplicable. |
| B.9.1–B.9.2 independent adjudication and verification | **Prospective only.** Correct verification/signature requirements are acknowledged; role bindings and a concrete check route remain outstanding. |
| B.9.4 and inherited witness-admission routing | **Repair required.** D6 must preserve independent witness and premise-failure review. The present claim is Candidate, so this does not pause or resume a lock. |
| B.9.6 scope accounting | **Provisionally sound intent.** Counts are adjudicator decisions; resolve D7 and retain explicit subclass accounting. No event is accepted by this review. |
| B.9.7 researcher agreement | **Pass.** Agreement is expressly excluded as grade evidence. |
| B.9.8 PLAN before search | **Current restraint passes; execution readiness fails.** No search was run; D1 must be repaired before the future experiment. |

Appendix B supplies gates, not a separate numerical scale. The following scores use the frozen brief's ten dimensions (1–5, higher is better); they cannot override the gates.

| Dimension | Score | Reason |
|---|---:|---|
| Constraint fit | 4 | PLAN-only scope and engineering boundary respected; delivers incomplete execution content. |
| Principle integrity | 3 | Strong anti-vacuity safeguards; D2–D6 affect the claimed logical and routing guarantees. |
| Falsifiability | 2 | Concrete attack themes, but no frozen instance, complete success contract, or finite budget. |
| Evidence demand | 4 | Paper-first approach avoids hardware demand; sourcing and proof work remain substantial. |
| Failure modes | 4 | Good placement, history, onset, and adaptation coverage; theorem and routing failures need explicit handling. |
| Integrability | 4 | Clear engineering non-gating boundary; the information-access contract is still deferred. |
| Latency / criticality | 2 | T-R and latency semantics depend on unresolved sampling and event definitions. |
| Complexity cost | 3 | Five variants and two theorem tracks exceed the concrete specification supplied; start with the minimal paired variants. |
| Reversibility | 5 | No execution, claim mutation, or irreversible commitment is proposed. |
| Stackability | 4 | Useful placement and admissibility scaffolding for later work once the contract is repaired. |
| **Total** | **35/50** | **Design value only; not execution authorization.** |

## Is the PLAN executable without search?

**No, as submitted.** A runner can follow the administrative sequence, but cannot begin a reproducible proof/refutation experiment without first designing the model instance, contract, and budget. The missing definitions cannot be recovered solely from the provided packet. This is not a demand to run a search now: the required next artifact is a complete, bounded PLAN assembled before any search. A minimal symbolic instance could satisfy that requirement without empirical measurements if its physical scope and added assumptions are explicit.

## Confounds and review limits

- This is a blind review of A only; neither relative superiority nor parity of the competing proposal can be assessed.
- The reviewer is cross-family to the proposal and inherited claim author. The supplied prior ruling discloses same-family claim adjudication, and its description of prior score-pass authorship differs from the roster/decision description. This review cannot verify execution provenance and does not treat those records as independent theorem checks.
- Identical residuals, finite-rate sampled observations, and probabilistic task performance are different objects. D2–D4 prevent silently moving between them.
- Worst-case nuisance selection may have limited target relevance even if a conditional theorem is valid. Independent envelope sourcing and premise-match evidence remain necessary; no target transfer is established here.
- Changing measurement placement, access history, sampling, or contact coverage between the negative and positive halves would confound Factor E with another change. Hold those elements fixed except for the declared added signal.
- Author-declared isolation and future seals were not independently authenticated. The present assessment is a document review, not B.9.2 verification, a proof, or a counterexample search.

**Recommendation to the packet adjudicator:** retain A's physical admissibility checks, downstream variants, and adversarial battery as design inputs; require D1–D7 repairs before accepting a runnable PLAN. No claim-state or engineering-gate action follows from this review.
