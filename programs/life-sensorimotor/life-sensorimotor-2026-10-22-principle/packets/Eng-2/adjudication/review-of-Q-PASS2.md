# Eng-2 blind review — B on A

**Reviewer:** Blind Reviewer B (Codex Astra). **Reviewed rival:** A only.

**Disposition:** Retain A as a **provisional contract plus deferred-PLAN candidate, requiring amendments**. It follows the Prin-3 planning sequence and supplies a potentially informative channel ceiling. Its current outcome labels and routing do not yet support trusting the engineering recommendation. No execution authorization, claim adjudication, grade change, or lock is issued by this review.

Read: `proposals/A.md`, `source/packet-brief.md`, `source/Prin-3-decision.md`, and the root `brief.md` rubric. Also inspected A's referenced `drafts/A/PLAN.md`, its seal, and `claims/C-Eng2-A-01/claim.md`; checked existence of that claim's companion records. The PLAN checksum matches. Did not read `proposals/B.md`, change claims, or run spikes. This is an assessment of A, not a comparison with B.

## Gates before ranking

| Gate | Assessment |
|---|---|
| Deferred spike; human `(q,r)`/placeholder-policy ratification **and** measurement-point declaration | **Satisfied as a stated restriction; clearance not evidenced.** Both proposal and PLAN explicitly block execution. A carried `PLACEHOLDER` value is not itself the human's explicit exploratory policy. Keep execution blocked until both declarations are recorded. |
| Human branch choice; override of Eng-1 automatic Alternate-B routing | **Substantively satisfied, operational linkage incomplete.** A labels the override and states the delay cost. Prin-3 also reserves branch choice to the human after the common gate; record that choice alongside the ratification and resealed PLAN before execution. The common gate alone does not choose A. |
| Symmetric eligibility | **Largely satisfied.** Placeholder fixture work is allowed for either branch only after the common gate. Task acceptance requires ratification. Amended B still needs an independently specified envelope question and filled contract; the skeleton does not make B executable. |
| Channel-level upper reference for amended A | **Present, conditionally eligible.** An exact joint-law NP reference can upper-bound every detector on the exported channel. Exactness and the proposed empirical threshold procedure remain insufficiently specified; H2/H4 sanity checks cannot establish an upper bound by themselves. |
| Principle constraints | **Good separation, incomplete artifacts.** No Candidate veto, Grade-3 necessity order, UP scope expansion, FAIL-driven downgrade, or Locked Grade-1 is asserted. The new necessity claim lacks the checked companion records described below. |
| Complete deferred PLAN / provisional status | **Provisional only.** The PLAN is sealed and explicitly deferred, but sealing does not resolve its statistical and routing ambiguities. Amend and reseal before treating it as execution-ready. |

Ratified `(q_c,r_c)` can be class-specific in XC-1, while PLAN §1 speaks of applying changed values to “all cells.” Freeze an explicit per-cell table, the exploratory/acceptance interpretation, measurement-point declaration, branch choice, and their identifiers with the next seal. No task-acceptance or transfer conclusion follows merely from human ratification or a harness PASS.

## Principle integrity

A correctly preserves C-P1-012 as Grade-2 Candidate, treats Eng-1 FAIL as sufficiency data, leaves B.9.6 accounting to the claim adjudicator, and lists bypassed Grade-3 edges. Its formal argument survives citation ablation. The exact information-inclusion inequality in C-Eng2-A-01 is a defensible candidate argument: adding observations cannot reduce optimal achievable power. A low enough **valid upper bound** can therefore exclude all detectors on the smaller channel. This is distinct from a deployable detector's failure.

The statistical version needs a sharper premise: fixing a threshold **family** before evaluation is not equivalent to fixing the tested threshold independently of evaluation. The claim's own challenge section excludes thresholds fitted on evaluation data, but PLAN §3 says to choose `t*` by its CP lower FPR bound without assigning that choice to a split. An independently selected threshold evaluated once would support the stated pointwise CP reasoning. A sweep on evaluation windows needs a separately justified simultaneous or selection-valid argument. This review requests clarification; it does not declare the exact NP inequality false or change the claim's grade.

`claims/C-Eng2-A-01/claim.md` exists, but `upgrade-log.md` and `violations.md` were absent when checked. A itself requires these companions for necessity claims. Supply them through the authorized claim workflow before declaring the new claim artifact complete. The reviewer's cross-family identity is not a substitute for a separate claim-adjudication record or human lock signature.

## Concrete objections and required amendments

1. **`DET_GAP_OPEN` confuses extra-information success with exported-channel headroom.** G-marg sees the true contact template; D1 does not. G-marg meeting the floor while D1 fails is compatible with the template itself supplying the decisive information and **no** detector on `(X,W)` meeting the target. PLAN §§4/7 nevertheless call this headroom and make a new detector family eligible. Rename the outcome as genie-only success / unresolved exported-channel headroom. Require a successful witness using only `(X,W)`, or an additional justified argument on that channel, before interpreting it as a detector opportunity. A valid genie ceiling can exclude success on the smaller channel; genie success cannot establish it.

2. **`NUISANCE_LIMIT` overstates what “not ceiling-limited” proves.** G-full's upper bound failing to fall below q can simply mean uncertainty. Combined with a G-marg ceiling, it does not establish that revealing nuisance restores feasibility. For a demonstrated nuisance-information gap require G-full to **meet a valid floor** and G-marg to fall below a valid ceiling, holding the template and model fixed. Otherwise report the marginal ceiling with unresolved attribution. G-marg can still bound the smaller channel under its declared prior if its LR is exact, but that is not the claimed causal diagnosis. Do not route away from detector work on the strength of the stronger unsupported label.

3. **The reference likelihood is described, not fully specified.** PLAN §2 does not define the genie template under null windows, the joint nuisance/template laws under both hypotheses, or why the conditional matched-filter statistic equals the joint LR. If genie laws differ by hypothesis, their likelihood contribution matters. Gaussian measurement noise alone does not establish that the full observation process has the stated Gaussian-innovation likelihood. Require equations, nuisance dimensions, null-template generation, and an explicit conditioning/marginalization rule for power at the common FPR. If the analytic formula is unavailable or mismatched, use `UNRESOLVED` for the ceiling; agreement at three MC thresholds and failure of practical detectors to beat it are necessary diagnostics, not proof of optimality.

4. **Threshold selection and numerical error leave the rare-event ceiling vulnerable.** Assign `t*` to calibration and keep evaluation untouched, or provide a justified alternative as discussed above. Specify the D1 selection objective, tie-break, and threshold calibration rule as well. H5's AUC agreement within 0.005 does not control errors at `r=0.001`: substantial tail disagreement can coexist with nearly identical AUC. Check convergence of the actual tail probabilities, threshold, and ceiling/floor decision, with numerical uncertainty handled conservatively. An approximate marginal LR without an error bound cannot certify the optimum over all channel detectors.

5. **The sealed verdict and routing rules have conflicts and uncovered cases.** Section 5 says PASS iff all H criteria hold, but H5 says its failure is not a harness failure. Section 7 allows both a limit route and `E-INFO=false` to apply, for example one limit cell plus two unresolved cells. It also leaves patterns such as both short classes `MET`, or one family gap and one unresolved class, without an explicit route. Declare precedence and defaults. The q/r-dependent H3 requirement and its assertion that a correct harness “cannot fail spuriously” also need correction: finite replicate criteria can fail by chance. State which statistical false-alarm risk is accepted. Do not give the aggregated E-INFO/routing decision the per-cell 95% guarantee; no simultaneous guarantee is currently established.

6. **Reproduction needs an apples-to-apples specification.** PLAN §1 freezes the Eng-1 window definition, while §3 mandates fresh episodes and detector resets to address the independence audit. State whether these exactly reproduce Eng-1 state initialization and window sampling. If they change it, log the change and separate historical reproduction from the new independent-window estimator. Comparing a new lower confidence bound with the old estimate's interval is not by itself a sound drift test. H1 also needs to distinguish the unchanged Eng-1 operating point from newly ratified thresholds. PLAN §4 says D0 `MET` requires changed targets or drift, but stochastic reruns can change a confidence-bound decision without either; d50 is not one of the two stated miss classes.

7. **The contract's own falsifier is outside the proposed checks.** C-Eng2-A-03 claims the typed interface prevents placeholder results from becoming task acceptance and names a mutation test. H1–H7 never run that test. Specify a deferred contract check that submits a placeholder certificate, stale certificate, and out-of-scope request to the decision-core boundary, with explicit expected rejection/UNKNOWN behavior and ownership. Include gate/contract version identifiers in the certificate. Until tested, typed fields and scope text are a design proposal, not demonstrated prevention.

## Falsifiability, cost, and integration

The deferred PLAN is more than an aspiration: it fixes primary cells, sample counts, detector family, split intent, resource limits, forbidden rescues, outputs, and an informativeness criterion. E-INFO can fail even when the harness passes, which is a useful distinction. A narrow fixture-level negative result could inform contract revision without asserting hardware transfer or necessity order.

The main weakness is **interpretability of failure**, not the absence of a possible failing run. Unsupported genie-success interpretations, threshold ambiguity, and incomplete routing could produce a decisive-looking label without answering “detector or channel.” These are document-level amendments that should precede execution, not post-result explanations.

The budget is modest in stated resources, but 64/128 nodes **per nuisance dimension** can grow rapidly, particularly when the full genie includes a nuisance trajectory. State the actual quadrature dimension, computation strategy, and timeout outcome; the claim of CPU-minutes is not demonstrated. Do not resolve a timeout by changing the prior or grid after observing results.

Ownership is otherwise clear: fast body-loop exports, evaluator-only genies, read-only scene publication, and scoped decision-core consumption. No expensive reference is proposed in the reflex loop. A detector-family success still requires a later deployment timing check; the present PLAN supplies no end-to-end latency bound. Contract versioning and reversible fixture work make abandonment cheap and leave later stages uncommitted.

## Fixed-rubric scores

Scores assess A on its own; gates precede any ranking. Higher Evidence demand scores mean a more economical evidence burden.

| Dimension | Score / 5 | Reason |
|---|---:|---|
| Constraint fit | 4 | Explicit deferred gate and provisional scope; branch-choice evidence and execution-ready amendments remain outstanding. |
| Principle integrity | 3 | Strong grade/scope discipline, but missing claim companion records and overinterpretation of genie outcomes weaken the formal-to-engineering bridge. |
| Falsifiability | 3 | Concrete finite experiment and E-INFO failure; threshold, reference, and routing ambiguities prevent unambiguous read-back. |
| Evidence demand | 4 | Reuses a local fixture with no hardware/GPU demand; quadrature feasibility within the budget is unsubstantiated. |
| Failure modes | 3 | Names mismatch, leakage, drift, and noninformativeness; current checks miss genie-success inference and rare-tail numerical failure. |
| Integrability | 4 | Clear body-loop/scene/core ownership; the claimed placeholder rejection lacks a specified check. |
| Latency / criticality | 4 | Correctly keeps genie computation offline and logging non-interfering; detector deployment latency remains unmeasured. |
| Complexity cost | 3 | Upper reference addresses a real ambiguity, but two genie models, numerical integration, and outcome classes need tighter justification. |
| Reversibility | 5 | Contract and fixture work are cheap to abandon; no hardware commitment or claim promotion is asserted. |
| Stackability | 4 | No premature ladder prerequisite; useful scoped interfaces, but unresolved classes need safer downstream routing. |
| **Total** | **37 / 50** | **Conditional deferred candidate; total does not waive gates.** |

**Recommendation to adjudication:** Preserve the contract-first proposal and bounded ceiling idea. Require the likelihood/statistical specifications, conservative genie interpretations, exhaustive verdict/routing rules, and complete claim artifacts before accepting the PLAN as ready for later execution. Keep the packet provisional and execution deferred pending the recorded human gate and branch choice. No comparison with the unread rival or claim-state change is implied.
