# Blind Review B on Proposal A (Packet B05)

## 1. Gate & Hard-Constraint Audit

**Recommendation: do not pass B05; require revision and executable production-path evidence.**
Scope: Charter, B05 brief, Proposal A, and the permitted spike VERDICT only.
The referenced baselines and Appendix B were not supplied in the authorized context; their full requirements cannot be independently certified.
The verdict reports selected logic outcomes, not implementation inspection or real-backend conformance.

- **Charter §2.1 — conditional pass:** no BC or tracking loss is proposed for the selected method.
  The actor objective is not specified, so exclusive conservative-FB optimization remains unverified.
- **Charter §2.2 — [CRITICAL], unfulfilled:** fresh 50/50 UFO relabel sampling and frozen-BN encoding are absent.
  Preserving `behavior_z` and using `z_actual` in the macro tuple are correct but insufficient.
- **Charter §2.3 — incomplete:** the 229-dimensional frame is named; motion-only inputs to B are not explicitly enforced.
  A dimension check cannot exclude terrain, phase, or frame-index substitution.
- **Charter §2.4 — [CRITICAL], potential violation:** finite jumps/speeds are declared corruption without proving solver divergence.
  A finite, schema-valid penetration with such a speed can therefore halt instead of being committed as credible failure.
  The selected method otherwise preserves termination, absorption potential, rejection, and pre-reset observations.
- **Charter §2.5 — pass:** A expressly limits its evidence and makes no learned-competence claim.
- **Brief §2 — mostly satisfied in the classifier:** 0.03 m is retained, later substeps continue after penetration,
  subsequent invalidity dominates, zero-filled terminal states are forbidden, and invalid batches do not increment S.
  Same-seed panel reruns preserve stated denominators, but the required continuation test is missing.
- **Brief §1/§3 — [MAJOR], unfulfilled:** hold-on-regression is delayed by a second bad panel;
  required runner integration, quota-credit transitions, and six-optimizer update smoke are not specified adequately.

## 2. Rubric-Keyed Technical Objections

### Substep Priority & Replay Isolation Rigor — 35%

- **[CRITICAL] Corruption predicates exceed their justification (A §1.1).**
  J and V are heuristic thresholds, not certificates of numerical corruption under the supplied charter.
  Supply an independent divergence criterion, or treat finite threshold exceedances as diagnostics pending classification.
- **[MAJOR] The final-check domain is incomplete (A §1.1–1.2).**
  P is accumulated only over substeps 1–4; final penetration is absent from the terminal rule.
  Prove the final contact state is identical to substep 4, or include P_F explicitly.
  Also define final displacement indexing and finite checks on every derived observation/motion tensor before commit.
- **[MINOR] The priority proof establishes a latch invariant, not physical order independence.**
  Swapping substep physics changes the trajectory; only aggregation of a fixed predicate trace is order independent.
  The formula also omits the other terminal failures mentioned immediately above it.
- **[MAJOR] Atomicity does not cover every relevant mutation (A §1.3).**
  Replay, input normalizers, and Gram state are listed, but network BN buffers, RNG advances,
  pending macro accumulators, and reset/curriculum bookkeeping need explicit prepare/commit ownership.
  Rejecting the whole batch is conservative, but necessity of discarding valid sibling environments is not proved.
- **[MAJOR] The stated FB target is not a complete gradient contract.**
  Give target dimensions and stop-gradient boundaries, including the target-policy call and online B relabel encoding.
  The terminal mask and true pre-reset state are sound; they do not establish the rest of the update.

### UFO Relabel & BN Order Fidelity — 25%

- **[CRITICAL] The central 25% rubric requirement has no algorithm (A §1.3, §5).**
  Specify fresh per-update 50/50 sphere samples of radius sqrt(d_z) and current-online-B encodings
  of permuted replay m_next, with BN frozen during relabel construction and subsequent relevant forwards.
  Show exactly one current (obs, m_current) BN pass followed by one next (next_obs, m_next) pass.
- **[MAJOR] Input normalization is conflated with network BN fidelity.**
  Collection-time normalizer updates do not implement replay-update BN ordering.
  Test 1's count increment of one is also unexplained against the two updates stated in §1.3.
  Add instrumented forward-call assertions and immutable replay behavior-latent checks.
- **[MAJOR] CandidateProvider and production wiring are absent.**
  Assert unfiltered [T,229] candidate access and exercise train.py -> runner.run -> Trainer;
  a separate classifier harness cannot certify the required training path.

### Curriculum & Quota State Completeness — 20%

- **[CRITICAL] Removing “paused” does not prove quota-credit correctness (A §2.2).**
  D <- D + q - r conserves only the total deficit; it supplies neither a deficit bound nor service guarantee.
  Several simultaneous resets can all choose the same argmax because no reservation/debit occurs between choices.
  Specify reset ordering, immediate reservations, epoch replenishment, and bounded starvation tests.
- **[MAJOR] Allocation and time units conflict.**
  Fixed prefix env mapping in §2.1 and deficit-based reset allocation in §2.2 need a stated precedence.
  One 4096-env commit adds 4096 control rows but increments S by one; define separate row and vector-step counters.
  Derive evaluation timing and training budgets from those units before claiming the 100,000-step contract.
- **[MAJOR] Anti-forgetting admits a forbidden unlock.**
  After one clean pass, a frontier pass with a first low-height drop >10 pp is still a pass under “confirmed forgetting.”
  It can complete pass_streak=2 and unlock despite regression.
  Any such drop must block that panel's unlock eligibility; define streak reset, hold release, and initial reference state.
- **[MAJOR] Stage changes and resume state are incomplete.**
  Define new-height deficit initialization, treatment of old episodes, streak reset after unlock, and reference updates.
  The hash omits per-env heights, episode state, pending macros, epoch position, and outstanding credit reservations.

### Verification Suite Executability — 20%

- **[CRITICAL] The mandatory panel-continuation denominator test is replaced by quota/Wilson tests.**
  Run a fixed full panel with an early credible failure; assert later episodes execute and the failed seed remains counted.
  Test invalid-panel halting separately, including same-seed replay and no partial success publication.
- **[MAJOR] Save/load hash equality is weaker than six-optimizer update and resume parity.**
  Execute actual updates, checkpoint mid-episode/macro, then compare uninterrupted and resumed next actions,
  minibatches, targets, parameter updates, counters, BN, scheduler state, and RNG-driven choices.
- **[MAJOR] The physical fixtures are not reproducible specifications.**
  Provide an exact model, initial state, solver configuration, action sequence, injection hooks, and bounded step count.
  A capsule fallback tests classifier plumbing but cannot certify the 229-dimensional production runner.

## 3. Audit of Rejected Alternative & Necessity Claim

- **[MAJOR] A1 has a concrete operational motivation but is contract-inadmissible by construction.**
  A2 also violates rejection requirements; neither challenges the selected architecture within the feasible design space.
  Compare against immediate online terminal updates with separate failure storage, or per-env transactional rejection.
  A3's use as an evaluation metric alone does not violate the charter's prohibition on tracking training rewards.
- **[CRITICAL] C-B05-A-01 does not follow from P1–P3 as stated.**
  The bias identity holds for conditional target means under a fixed policy/target law and uncorrected survivor-only regression.
  P1–P3 do not require those conditions, realizable regression, convergence, or absence of an independent failure estimator.
  Recursive Bellman fixed points and a changing planner need a separate derivation.
  Committing to both buffers is a charter requirement; necessity for unbiased task Q does not follow from FB support.
- **[MAJOR] The proposed falsifiers are not logical negations of the analytic claim.**
  A CI containing zero can reflect low power; P3 supplies no minimum detectable effect.
  Equal penetration rates do not contradict critic bias because the planner need not change its selected action.
  Use a fixed-policy finite MDP with known hazard/returns, then separately test planner consequences.
- **Appendix B:** necessity grading cannot be certified without its text.
  On the stated premises alone, “Grade 1” is unsupported; restrict the quantifiers and make the statistical test precise.

## 4. Spike Protocol Critique

- **[MAJOR] Mechanism controls:** add no-penetration valid steps, equality at 0.03 m, empty contacts,
  final-only corruption/schema/timing failures, success-plus-penetration, timeout bootstrap, and one-invalid-env batches.
  Exhaustive Boolean patterns test the latch, not extraction of those predicates from actual simulator state.
- **[MAJOR] Execution evidence:** elapsed time is not a backend detector.
  Log backend/model versions, actual substep calls, production entry point, and fixture identities.
  The supplied VERDICT lacks panel continuation, BN traces, optimizer updates, and resume evidence.
- **[MAJOR] Statistical confounds:** equal committed-step budgets give commit/drop arms unequal attempted interactions.
  Match attempted steps and compute, report retained rows, and measure bias against independent fixed-policy MC returns.
  Define pairing/seed clustering for success CIs; pooled episodes do not provide independent training-seed evidence.
- **[MAJOR] Threshold scope:** 79/100 correctly implements the stated Wilson gate for n=100 only.
  Repeated unlock looks and multiple heights/arms require an explicit inferential scope or multiplicity treatment.
  Define the E+M ratio direction and censored-run comparisons; neither is presently an executable acceleration rule.
