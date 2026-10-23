# Blind review B on proposal A — Prin-8

Reviewer: B. Scope: proposal A only. Read the run and packet brief/roster, all supplied `source/` files, `proposals/A.md`, and `drafts/A/summary.md`. No competing proposal or competing draft was inspected. References below are to the supplied packet materials. This is a proposal review, not a claim adjudication.

**Disposition: revise before adoption.** A provides a useful planning template, especially its independent task requirements, force-accounting safeguards, uncertainty outcomes, and separation of target matching from claim promotion. However, its current MATCH rules can certify assumptions that the inherited claims explicitly exclude, and its evidence/status machinery has contradictions. Recommend retaining the structure only with the mandatory repairs below. This assessment makes no comparative ranking.

## Gates before ranking

| Gate | Finding |
|---|---|
| Packet scope | Pass: templates only; no execution, target measurements, or spike is claimed. |
| Candidate authority | Pass: no veto, lock, grade change, research-order necessity, or Eng-2 gate change is asserted. Preserve D-P1-001, D-Prin-3-001, D-Eng-2-001 and D-Prin-4-001 by ID. |
| Exact premise mapping | Not ready: T-010 substitutes unproved tolerances for explicit exclusions; T-002 does not fully register the initially hidden condition or the robust feasibility quantifiers. |
| Verification and governance | Conditional: correct independent adjudication/signature routing, but the pre-freeze B.9.6 exemption is too broad and Part-B applicability has an unsupported override. |
| Adoption eligibility | Eligible as a revision source; not eligible for unamended operational use. No locked-claim conflict is established by the supplied materials. |

## Mandatory revisions

### R1 — A tolerance is not a theorem-premise match

Sections 4.2 and 7 explicitly permit small coupling, extra delay, and quantization under thresholds accepted at freeze. P10-A3 additionally permits nonlinear-friction residuals within a fitted tolerance without labeling that an interpretive choice. C-P1-010 premises 1–3 and Scope instead specify a single-degree-of-freedom class, no extra delay, and linear viscous damping, with explicit exclusions. Predeclaring a tolerance prevents result-dependent tuning; it does not establish that the original bound survives the deviation. Claim-adjudicator acceptance alone is not the missing derivation.

Separate exact model-class membership, target-to-model adequacy, and any approximation extension. A known excluded effect yields SCOPE-EXIT for application of the present claim; insufficient evidence yields UNESTABLISHED. An approximation may support planning, but cannot yield the same MATCH without an independently checked reduction or robustness result showing the conclusion remains valid over the stated uncertainty. Any changed bound or additional scope belongs in a separately governed claim or amendment, outside this template-only packet. Apply this rule to A1a, A2b, A2c, and A3, not just the three labeled choices.

Remove §4.1's permission to evaluate the Part-B applicability verdict without its Part-A dependencies merely because an adjudicator accepts a documented reason. Arithmetic can be computed provisionally; an application verdict requires every necessary dependency or a separately verified extension.

### R2 — Restore T-002's full quantified premise checks

P2-3 records an admissible pair and matched initial condition but omits the claim's **initially hidden** requirement as an explicit check. Add the initial observation histories, information available through each permitted channel, and the argument that the worlds are initially indistinguishable at that boundary. Physical disturbance differences alone do not establish this premise.

P2-2 permits a demonstrated realization to establish feasibility under **all** declared disturbances. A finite successful probe set does not discharge that universal statement. Register the horizon, initial-state set, disturbance set, uncertainty set, and coverage argument explicitly. A demonstration qualifies only with a justified exhaustive or generalizing coverage argument; otherwise it supports tested-instance feasibility only.

Also distinguish a single allowed causal mechanism that succeeds across the declared class from separate force histories that could succeed in each world if the world were known in advance. The latter does not establish robust feasibility under the registered observation channels. P2-3's disjointness argument must quantify over the fixed plant/resources and their registered uncertainties, rather than only a nominal trajectory. An unresolved argument remains UNESTABLISHED, never FAIL by lack of proof.

### R3 — Make provenance, validation, and verdicts separate fields

Section 2.1 says every field has exactly one status, makes DERIVED inherit the weakest input status, and permits MATCH only from MEASURED fields or declarations. Yet P2-2/P2-3 properly require analytical arguments, and P10-B-cmp is DERIVED. A derived proof cannot literally become a measured fact. Likewise, a control-law specification can be established by an implementation audit rather than physical measurement alone. The forward-only vocabulary does not define how measured evidence can later become contested or inapplicable.

Use distinct fields for provenance (declaration, specification/audit, observation, derivation), validation state (pending, accepted, contested, superseded), and row verdict. For each derivation, record dependency versions, uncertainty propagation, method, and independent check. Allow analytical rows to match through a checked argument whose dependencies are adequate for that row. Preserve old versions when later evidence changes validation.

Define a complete aggregation table: P2-1a/P2-1d FAIL, CONTESTED rows, and NOT-APPLICABLE interruption/passivity rows currently lack consistent instance routing. A conditional interruption row can be satisfied when its condition is false without pretending interruption was measured; an inapplicable passivity requirement cannot produce a Part-A application MATCH. Standardize CIRCULARITY-FLAG across both phase vocabularies.

### R4 — Remove the blanket pre-freeze narrowing exemption

Section 2.5 says pre-freeze edits cannot be narrowing events because no value has been seen. Phase 0 expressly allows specification values and prior design knowledge. More fundamentally, B.9.6 requires logging every narrowing of a claim's scope; the local freeze date is not its governing criterion.

Distinguish selecting an instance within unchanged claim scope, revising a local measurement plan, correcting an erroneously mapped existing exclusion, and changing the claim's scope or premises. Log each with its reason and available evidence. Refer possible claim narrowings to the bound adjudicator regardless of phase; do not automatically count every plan edit or scope exit. Leave accepted counts unknown pending the relevant records/ruling: the supplied packet does not establish either claim's cumulative count.

### R5 — Make Part-B comparison and physical-compliance outcomes precise

P10-B-cmp promises propagated uncertainty but specifies only above/below/overlapping an interval. Register the uncertainty sets for required stiffness, damping, and period; the period must have a positive lower bound, and the damping must satisfy the applicable class assumptions. A sufficient rule is: applicability only if the lowest admissible required stiffness exceeds the highest admissible ceiling; antecedent absent only if the highest admissible required stiffness is at most the lowest admissible ceiling; otherwise unresolved. Respect dependencies if the uncertainties are correlated. The equality case belongs with the claim's non-strict retirement trigger when it is established, not automatically with overlap.

Name the low-side outcome **Part-B antecedent not established for this joint/configuration**, with the source claim's per-joint retirement request routed separately. It establishes neither passivity of the actual controller nor falsity of the general conditional; the comparison omits the actual virtual-damping penalty and tests only the stated Part-B trigger.

P10-B8 must account for how physical and virtual contributions supply the task requirement. Mere presence of a spring does not show the physical route supplies the needed stiffness, while partial contribution does not by itself settle the remaining virtual requirement. Keep an unresolved allocation open, and route confirmed failure of premise 8 without making a broader architecture claim.

### R6 — Separate bookkeeping units from physical applicability

Section 4.1 creates one instance per rendering loop. That is useful inventory, but multiple loops acting on one joint share the physical port and damping. Individual in-class records cannot independently allocate the full measured damping or imply a passivity guarantee for their combination. Record the aggregate port law and all simultaneous contributions. Evaluate an isolated loop only under an explicit isolation condition; if the aggregate is outside the inherited class, return SCOPE-EXIT or UNESTABLISHED as appropriate.

## Strengths to retain

- G-1/G-2/G-3 and G-6 prevent controller failure, achieved performance, or existing gains from silently defining the purported necessity premises.
- Passive and embedded response mechanisms receive explicit consideration; unavailable force instrumentation yields UNESTABLISHED rather than role absence.
- Claim hashes, independent review, append-only evidence, and separate Part-A/Part-B outcomes are useful safeguards.
- No target match is substituted for independent proof verification, a serious Grade-2 counterexample search, or the human signature required by B.9.2.
- Phase 0 remains planning, and prior harness results cannot establish target transfer or research ordering.

## Rubric assessment of A as submitted

Scores are diagnostic only; they do not override the adoption gate above. Higher is better, including lower evidence and complexity burden.

| Dimension | Score / 5 | Basis |
|---|---:|---|
| Constraint fit | 5 | Clear template-only scope and unchanged execution/claim gates. |
| Principle integrity | 2 | Approximate MATCH rules and the applicability override exceed the inherited premises; R1 is blocking. |
| Falsifiability | 3 | Concrete absence tests and uncertainty outcomes, but feasibility coverage and initial hiddenness remain incomplete. |
| Evidence demand | 3 | Honest instrumentation requirements; full safe-history analysis and force inventory may be costly. |
| Failure modes | 4 | Strong circularity and instrumentation safeguards; aggregate-loop and approximation failures need repairs. |
| Integrability | 4 | Clear owner/runner/adjudicator separation and no premature module requirements. |
| Latency / criticality | 4 | Explicit deadlines, total-force timing, and loop periods; initial channel information needs a registered check. |
| Complexity cost | 3 | Detailed templates are useful, but inconsistent statuses and multiplicative instances add avoidable burden. |
| Reversibility | 5 | Planning artifacts can be revised without hardware execution or claim-state changes. |
| Stackability | 4 | Supports later evidence collection without importing ladder ordering or new Eng-2 gates. |
| **Total** | **37 / 50** | **Revision source; not unamended adoption.** |

R1–R6 are template repairs, not instructions to execute measurements or edit claim records. After revision, a later authorized packet must seal its own complete execution PLAN; freezing this schema alone does not establish that an experiment is ready. No claim state, grade, decision, narrowing count, or Eng-2 permission is changed by this review.
