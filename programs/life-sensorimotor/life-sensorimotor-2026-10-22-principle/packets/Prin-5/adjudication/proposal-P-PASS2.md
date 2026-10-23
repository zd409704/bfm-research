# Prin-5 proposal B — Certify an information boundary, not a sensor list

**LABEL=B.** Competing-author proposal; document review only. C-P1-011 remains **Candidate**, with its recorded grade unchanged. No claim-state ruling, lock, spike, or Eng-2 gate amendment is made here.

## Thesis and decision requested

Adopt a **time-bounded information-access certificate** as the organizing object for C-P1-011. A list of cameras, commands, and memories cannot establish the export-only premise: an omitted path can enter through timing, initial state, a shared random variable, or feedback. The useful deliverable is a traceable argument that every input to a specified recipient by a specified decision time is either represented in the declared channel, derived from it, or demonstrably irrelevant under the stated probability model.

The certificate has three possible application outcomes: **export-only justified**, **joint-channel justified**, or **unresolved**. These describe the evidence for one application, not claim lifecycle states or permission to execute engineering work. Its value is preventing an unjustified export ceiling from vetoing a route while making an adequately supported ceiling precise.

Recommend this certificate plus the inventory and checklist below. Reject an inventory whose unchecked rows default to “absent,” or whose completion alone is treated as proof of necessity, export sufficiency, or research order. Inherit D-Prin-4-001 as planning authority only. D-Prin-3-001 and D-Eng-2-001 remain unchanged; this proposal adds no Eng-2 preconditions.

## 1. Exact object to be audited

For each application, fill one record before making an information-ceiling assertion:

| Field | Required declaration |
|---|---|
| Target | Contact variable `Z`, physical meaning, target interval, units, resolution, and treatment of no-contact cases |
| Recipient and cutoff | Named functional recipient, decision time `t`, online or retrospective mode, and clock alignment |
| Export `X_t` | Exact body-loop transcript available by `t`: fields, precision, rates, timestamps, packet availability, and history included |
| Additional access `W_t` | Joint tuple of all other accessible inputs and initial state, with provenance and availability times |
| Upper-layer object `Y_t` | Actual accessible state or declared output by `t`; specify which is being bounded |
| Model | One joint law over `(Z, X_t, W_t, Y_t)`, including policy, environment distribution, reset/selection rules, and fixed configuration |
| Evidence version | Interface/code/configuration references, data lineage, reviewer, open objections, and invalidation conditions |

The distinction between the target interval and the information cutoff matters. Earlier export history can inform a present contact; future measurements can inform a retrospective estimate. Neither may be silently treated as processing of the current-window payload alone. A “same-window” restriction is an application choice to justify, not a property of the theorem.

Proposed exact core for independent review:

> If `Y_t` is conditionally independent of `Z` given `(X_t, W_t)`, then `I(Z;Y_t) <= I(Z;X_t,W_t)`. The export-only form additionally requires `Z -> X_t -> Y_t`. Additional access need not be statistically independent of the export. The bound concerns a fixed joint law and the declared information cutoff.

An explicit sufficient construction is `Y_t = f(X_t,W_t,U)` with `U` conditionally independent of `Z` given `(X_t,W_t)`. Include all inputs needed to justify this construction. Exogenous randomness at episode start does not automatically satisfy that conditional independence after feedback.

For finite information quantities, the chain rule gives

`I(Z;X_t,W_t) = I(Z;X_t) + I(Z;W_t | X_t)`.

Thus the relevant extra information is **conditional and joint**, not each channel's marginal correlation with `Z`. Under the same joint Markov premise, the useful incremental statement is `I(Z;Y_t | W_t) <= I(Z;X_t | W_t)`. It compares information beyond the same declared side information, not performance across different policies or datasets. No numerical value of either ceiling is established by an architecture inventory.

These identities explain the proposal; they are not an independent B.9.2 verification. The source record's broader prose must be reviewed along with its formula.

## 2. Inventory organized by how a path crosses the boundary

Every row below is an **audit candidate**, not an observed target-stack feature. The supplied claim and decisions contain no implementation manifest sufficient to establish presence, absence, or closure. Every target-specific disposition starts **unresolved**.

| ID / access class | Potential path and why it matters | Evidence to collect; disposition rule |
|---|---|---|
| B01 — Export content and delivery | Raw fields, residuals, quantization, batching, message size, timestamps, missing packets, delivery latency. Contact can affect when a packet arrives even with identical payloads. | Trace publisher-to-reader contracts and transport behavior. Include observable delivery metadata in `X_t` if that is the declared export; otherwise inventory it in `W_t`. A payload-only ceiling needs a separate metadata argument. |
| B02 — Independent ingress | Other sensory streams, raw actuator diagnostics, safety-controller events, external annotations, or human input reaching the recipient. A nominal body-loop export may coexist with direct reads. | Enumerate subscriptions, shared-memory reads, callbacks, files, and service responses, including fallback/debug routes. Put accessible non-export inputs in `W_t`; record evidence for disabled or unreachable paths. |
| B03 — Commands and feedback | Command history, efference copies, action selection, exploration seeds, and policy mode. These can help determine contact rather than merely observe it. | Trace action generation and plant response with time order. Include commands and relevant initial random state unless their derivation from declared access is established. Distinguish commanded from realized actuation. |
| B04 — Retained history | Recurrent state, cached scenes, previous exports, prior episodes, reset failures, maps, and delayed messages. State can contain information absent from the current export window. | Trace initialization, update, persistence, and reset paths. Extend `X_t` history where explicitly declared, or include the initial/history state in `W_t`. “Computed from exports” is insufficient if those exports fall outside `X_t`. |
| B05 — Learned or calibrated state | Parameters, priors, calibration tables, task-specific adaptation, and parameter updates. A frozen parameter can be fixed in the model; a run-specific learned state can carry episode information. | Record training/adaptation provenance and what is held fixed. Condition the model on genuinely fixed configuration; put varying accessible state in `W_t`. Do not label all pretrained parameters leakage or all frozen parameters irrelevant without specifying the sampling model. |
| B06 — Shared context and selection | Task identifier, episode seed, object/fixture label, reset condition, scheduler state, and inclusion/exclusion flags. Joint interpretation with `X_t` may reveal contact even when individual signals do not. | Trace context injection and dataset selection. Audit the entire tuple jointly; declare selection in the law and include accessible context in `W_t`. A zero marginal association does not justify exclusion. |
| B07 — Evaluator and future access | Ground truth, simulator internals, post-contact labels, future sensor samples, offline smoothing, replay indices, and reward available only after the decision. | Separate recipient-visible inputs from evaluator-only data and record access times. Exclude from an online tuple only with an access argument; include in a declared retrospective tuple. Verify the evaluator does not feed the recipient through adaptation or selection. |
| B08 — Derived features and hidden dependencies | Residuals, certificates, latents, and filtered fields can be deterministic functions of the declared input, or can silently use calibration, history, clocks, or additional measurements. | Obtain the dependency graph and parameter/history versions. Classify as derived only when every parent is accounted for. C-P1-011 H4's I2 redundancy holds when I2 is a function of the actual declared I1 transcript and fixed configuration. |

Each instantiated row needs: **producer → transport/store → recipient; physical sample time; availability time; retention/reset behavior; dependency references; disposition; evidence reference; owner; unresolved objection**. Allowed dispositions are `in X_t`, `in W_t`, `derived from declared tuple`, `excluded with evidence`, and `unresolved`. Duplicate sources may appear in several paths; deduplicate information by provenance, not by dropping a visible route.

## 3. Two analytic stress cases that a laundry-list audit misses

**Joint information without marginal information.** Let contact indicator `Z` and context bit `K` be independent fair bits. Set `X = Z XOR K` and `W = K`; an upper layer can output `Y = X XOR W = Z`. Then `I(Z;X)=0` and `I(Z;W)=0`, but `I(Z;X,W)=1` bit. Discarding `W` because it has no marginal contact correlation makes the export-only application false. The joint bound holds. These are stipulated finite variables, not measured target-stack behavior.

**Feedback makes a “noise” seed informative.** Let a fair bit `R` select a probing action and stipulate a toy plant where `Z=R`; let the export be constant and the recipient retain `R`. Then `I(Z;X)=0` but `I(Z;Y)=1` for `Y=R`. Although the seed was independent of the plant's initial state, it is not independent of the resulting contact. It belongs in the access account. An action can also acquire fresh measurements or change the distribution of later contact. Comparing the old and new regimes is not a violation of DPI under a fixed law.

These examples are paper checks of proposed premises, not counterexample-search experiments, hardware evidence, or theorem refutations. No spike is run or proposed as necessary for this packet.

## 4. Tighten-premises checklist for C-P1-011

The following are proposed edits or checks for later adjudication, not changes to the canonical claim.

- [ ] **P1 — Define the target and two time boundaries.** State `Z` and its resolution, target interval, recipient cutoff, and online/retrospective mode. Resolve whether past history is inside `X_t` or `W_t`. Keep the general theorem separate from a finite-resolution application.
- [ ] **P2 — State both Markov premises explicitly.** Attach `Z -> (X_t,W_t) -> Y_t` to the joint-channel form; the existence of a symbol `W_t` does not establish completeness. For export-only wording, independently justify `Z -> X_t -> Y_t`.
- [ ] **P2 — Replace “independent channel” with “additional accessible information.”** Statistical independence from `X_t` is neither required nor generally true. Additional conditional information can occur in correlated or jointly informative channels. Replace the conclusion's absolute recovery wording with the mutual-information bound under its stated premises.
- [ ] **P2/P3 — Audit joint access, not individual correlation.** Include the command/context/memory tuple before considering exclusions. Establish a conditional-independence or deterministic-derivation argument; marginal screening alone does not establish one.
- [ ] **P3 — Account for feedback and internal random state.** Declare the policy and action history. Check whether alleged independent processing noise helps generate `Z`. Include relevant state or narrow the application to an explicitly justified observation-only setting; log any narrowing.
- [ ] **P4 — Name one probability model per assertion.** Include the entire joint tuple, configuration, selection rules, and policy. Both sides of a comparison must use that law. Distribution shift calls for a new application audit; DPI itself does not require deployment and evaluation to share one universal distribution forever.
- [ ] **P5 — Use “cannot increase,” not necessarily “lowers.”** Filtering, quantization, and compression obey the bound when they are processing of the declared inputs. Equality is possible. Adaptive filter parameters, timestamps, retained samples, and auxiliary inputs must be accounted for before invoking P5 or H4.
- [ ] **Scope — Preserve the exclusions.** No estimator error, latency guarantee, sufficient export, mandatory signal such as realized actuation, ladder edge, or research order follows from the inequality alone. Improved estimation can reflect a better decoder of existing information.
- [ ] **Evidence — Separate structural argument from observations.** A manifest plus data-flow derivation supports an access premise; a trace can expose an omitted path but cannot alone prove no other path exists. Finite mutual-information estimates or successful prediction cannot certify conditional independence.
- [ ] **Governance — Review the exact proposed version independently.** Resolve the source record's conditional recommended-for-lock wording against the ledger's Candidate/tighten-premises disposition without treating this author proposal as reconciliation. An independent checker must verify the whole statement and premise match; any Grade-1 lock still requires the human lead's signature and an authorized non-author state transition.
- [ ] **Governance — Account for amendments and objections.** Have the authorized adjudicator inspect upgrade/violation records and classify any scope narrowing or added survival premise under B.9.6. Those logs were not supplied for this proposal, so no narrowing count or retirement clearance is asserted. The author of these amendments must not adjudicate their own amendments; bind a separate reviewer under the roster's role-separation rule.

## 5. Audit procedure, outcomes, and limits

1. **Architecture owner** freezes one recipient/configuration/cutoff record and populates B01–B08 with evidence. Walk backward from actual readers and persistent state, not just forward from the nominal exporter. Inspect paths through transport, initialization, control, and evaluation.
2. **Independent reviewer** attempts to route information into `Y_t` without traversing the declared tuple. Review the two analytic stress cases, access timing, fallback paths, and all unresolved dependencies. A concrete bypass is a premise objection to the application, not a numerical refutation of the theorem.
3. **Reviewer** records one of the outcomes below, a versioned rationale, and precisely which assertions the evidence supports. If an empirical counterexample search is later commissioned, seal a PLAN under B.9.8 before execution; that is separate work.
4. **Claim adjudicator** later handles proposed text, objections, any B.9.6 accounting, independent verification, and state recommendations. This packet author does not perform those transitions.

| Application outcome | Evidence needed | Permitted inference |
|---|---|---|
| Export-only justified | Every relevant access path accounted for and an argument establishing the export-only Markov premise. A sufficient route is that all additional access is derived from `X_t`, or is jointly conditionally independent of `Z` given `X_t`. | Use `I(Z;Y_t) <= I(Z;X_t)` for this declared law and cutoff. No numerical tightness or task sufficiency is implied. |
| Joint-channel justified | Declared `W_t` accounts for the additional paths and the joint Markov premise is supported. | Use `I(Z;Y_t) <= I(Z;X_t,W_t)`; identify which export-only premise lacked support. Do not advertise an export-only ceiling. |
| Unresolved | An access path, time boundary, dependency, or model assumption lacks evidence. | Treat the theorem as conditional and withhold the target-specific ceiling assertion. This outcome does not block Eng-2 or other engineering work. |

Avoid a vacuous certificate that defines `W_t=Y_t` and declares success. Inventory primitive inputs and their lineage independently of the output being bounded. Even a complete access account only licenses the inequality; a useful impossibility conclusion additionally needs an information bound on that tuple and a justified task requirement. Neither is established here.

Invalidate the application certificate when inputs, persistent state, training/adaptation provenance, policy, timing, selection, or configuration changes in a relevant way. Recheck the affected premises rather than asserting automatic theorem transfer. A late packet newly admitted after the cutoff changes the application, not the old-time bound.

For C-Eng1-A-01 and C-Eng2-A-01, offer only a later cross-reference: map any certificate's declared inputs to B01/B04/B05/B08 and check reader/evaluator separation through B07. Their detailed premises are not in this source bundle, so this proposal supplies no ruling on either claim and no additional Eng-2 execution condition. D-Prin-3-001's existing human `(q,r)`, measurement point, and branch-choice requirements remain exactly as inherited through D-Prin-4-001.

## 6. Evidence boundary and delivery

Read: root `brief.md` and `roster.md`; all five files in `packets/Prin-5/source/`; canonical `claims/C-P1-011/claim.md`. The source claim copy and canonical claim agree on the narrow theorem and its unresolved application audit. The architecture inventory is proposed, not completed against a target implementation. No competing draft was consulted.

This satisfies the Prin-5 minimum with a bounded document-review task: populate one application record, resolve the eight access classes, and attach the checklist disposition. It requires no compute allocation or hardware run and is cheap to revise. Its principal risk is incomplete architecture evidence; the explicit unresolved outcome prevents missing evidence from turning into a necessity assertion. No named product, company, new ladder constraint, claim-grade change, or Eng-2 gate change is introduced.
