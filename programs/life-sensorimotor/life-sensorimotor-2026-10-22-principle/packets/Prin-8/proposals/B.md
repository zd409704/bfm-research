# Prin-8 — Proposal B: Separate applicability from realization

**LABEL=B. Design only.** C-P1-002 remains Grade-2 Candidate. C-P1-010 Part A remains Grade-1 Candidate and Part B Grade-1 conditional Candidate. No measurements, searches, spikes, theorem verification, claim transitions, or engineering acceptance are reported here.

Recommend a pair of premise-match forms that produce two separate records: **what target setting the claim applies to**, and **what evidence supports a proposed realization or conditional bound in that setting**. Each record preserves uncertainty and adverse evidence. A successful behavior trace cannot fill an applicability row; an applicability match cannot fill a realization row.

This implements D-Prin-4-001 priority 5. Inherit D-P1-001, D-Prin-2-001, D-Prin-3-001, D-Eng-2-001, and D-Prin-7-001 by ID. These forms add no Eng-2 preconditions and clear none. The existing human `(q,r)`, measurement-point, and branch requirements remain unchanged. A future declared measurement point supplies context, not automatic authorization for a new experiment.

## 1. Common cover sheet and evidence rules

Copy this cover separately for each claim and each target case. No measured values are supplied by this proposal.

| Field | Entry to complete later | Current entry |
|---|---|---|
| Identity | Claim ID, exact claim version, form version, target-case ID | Claim ID only; other fields UNSET |
| Target scope | Plant/model version, joint or port, support/contact mode, initial-state set, task, horizon, resources | UNSET |
| Measurement context | Declared measurement point and reference frame; declaration reference; separate future experiment authorization | UNSET; no execution authorized here |
| Requirements | Envelope or task specification, requirement owner, approval/version reference | UNSET |
| Evidence custody | Artifact reference, version/hash, author, date, method, raw-to-derived transformation | UNSET |
| Uncertainty | Units, deterministic bounds or stated statistical coverage, calibration, model discrepancy, timing bounds | UNSET |
| Review | Evidence owner, independent checker, bound claim adjudicator; conflicts of authorship/affinity | UNSET; this author supplies no ruling |
| Revision history | Old/new scope, reason, adverse observation, potential B.9.6 event, adjudicator disposition | No claim amendment proposed; historical count not assessed |

Each premise row has these repeatable fields:

`premise ID | exact target proposition | evidence required | artifact reference | uncertainty/domain | status | objection | reviewer`

Statuses are **UNSET**, **SUPPORTED-IN-SCOPE**, **CONTRADICTED**, and **UNRESOLVED**. They describe evidence, not claim state. Missing artifacts stay UNSET; conflicting evidence or insufficient resolution is UNRESOLVED. A contradicted premise stops that target application and is preserved as an adverse record. It does not retire the general claim automatically.

Evidence must distinguish a task requirement, a model assumption, an analytic certificate, and a measurement. Statistical coverage is not a universal disturbance guarantee. Pooling modes, temperatures, loads, or parameter ranges needs an explicit argument; otherwise use separate cases. Changing plant mechanics, controller class, or task tolerance creates a new case/version and retains the original disposition. If a change is proposed to rescue the claim, route it for B.9.6 assessment; do not reset or guess its cumulative count.

## 2. C-P1-002 template: paired-world certificate and force accounting

### A. Applicability rows

| Row / source premise | Required content and future evidence | Failure or ambiguity route |
|---|---|---|
| R1 / P1 | Fixed dynamics and parameter domain; initial-state set; envelope; disturbance set; actuator authority; all observation and actuation channels; support-mode scope | An unmodeled channel or mode change makes the case unresolved pending an explicit model revision |
| R2 / P2 | Robust competence quantified over the declared horizon and disturbances; independent feasibility argument for at least one allowed mechanism | Inadequate authority or an empty feasible task cannot support a timing-role inference |
| R3 / P3 | Two admissible initially hidden disturbances; initial-state matching tolerance; who cannot distinguish them and until when; independent safe-history incompatibility certificate | One controller failing, two recorded forces differing, or an assumed delay does not establish incompatibility |
| R4 / P4 | Complete accounting of active, embedded, passive restoring and dissipative generalized forces in the same coordinates; exogenous disturbance separately identified | Missing passive force or hidden actuator feedback leaves applicability and realization unresolved |
| R5 / P5 | Inventory of every permitted timely response source and its availability; upper-layer interruption only if already in the declared resource/disturbance envelope | Do not add a universal stall condition or require a dedicated module |

The R3 certificate attachment is a blank mathematical specification:

```text
worlds: w0 = UNSET; w1 = UNSET
fixed plant/resources/initial-state domain: UNSET
horizon H: UNSET; incompatible-history deadline D: UNSET
safe-history sets: S_i(D) = all admissible total corrective generalized-force
  histories on [0,D] that preserve the specified envelope in world w_i
quantification over uncertain parameters and matched initial states: UNSET
nonemptiness/feasibility evidence for both worlds: UNSET
independent certificate that S_0(D) intersects S_1(D) nowhere: UNSET
force-history metric, units/scales, and separation lower bound delta: UNSET
source and independent check of deadline/certificate: UNSET
```

The certificate must concern all allowed histories, not sampled controller outputs. A conservative reachable-set enclosure may support disjointness if the enclosures themselves are disjoint; overlapping enclosures mean unresolved, not a demonstrated common safe history. Any certificate must explain how its treatment of plant uncertainty preserves its quantifiers.

Disjointness alone need not provide a positive measurable distance. Record a certified `delta > 0` in the declared metric if a finite-resolution absence test requires it; otherwise label that test unresolvable. Do not invent a numerical separation or an earlier response deadline from the symbolic condition. Measured total delay and the interval of common corrective history are distinct fields.

### B. Realization and absence rows

| Attachment | Fields to fill before any future authorized probe |
|---|---|
| Force inventory | For each active actuator, embedded controller, structural spring, damping element, and other state-dependent mechanism: contribution, coordinates, observation channel, uncertainty, bandwidth, and whether directly measured or bounded by a validated model |
| Paired traces | Disturbance, state/envelope margin, total corrective force, common-clock timestamps, onset phase, saturation, sensor error, timing jitter, filtering, actuator lag, and missing samples |
| Resolution contract | History metric shared with R3; per-world reconstruction errors; relative clock-error bound; total pairwise error budget `E`; relation of `E` to `delta` and deadline `D` |
| Alternative realizations | Passive-only, existing embedded feedback, and proposed active feedback; feasibility and instrumentation for each; no default preference for a new controller |
| Intervention validity | Proposed replay/channel suppression; all changed dynamics, resources, forces, and observations; whether R1–R5 remain true; same-setting comparison justification |

Use the predeclared error budget to bound true history distance by an interval around the observed distance. If its lower bound is positive, differentiation is resolved. If its upper bound is below certified `delta`, the traces cannot jointly be members of both certified safe-history sets. The latter is an inconsistency to investigate, not proof of exact equality of continuous histories. If a deadline-resolved differentiation requirement is independently certified, record whether it was met; timing uncertainty overlapping the deadline is unresolved.

Prospective dispositions:

| Evidence pattern | Permitted output |
|---|---|
| R1–R5 supported; timely force differentiation resolved; tested envelope maintained | Tested realization supported for the registered probes only; universal robustness and necessity remain unestablished |
| Force accounting or timing resolution insufficient | Realization unestablished; role absence not demonstrated |
| Valid probe shows no required timely differentiation and envelope failure | Evidence of role absence/failure in that probe; not a proof of necessity |
| Verified envelope success in both matched worlds with history-distance upper bound below `delta`, or other demonstrably absent required response | Counterexample candidate / certificate inconsistency; independently inspect force accounting, premises, and derivation before any claim action |
| Passive forces supply timely differentiation | Passive realization candidate; not evidence that active feedback is mandatory |
| A common safe total-force history is independently established | R3 contradicted for this case; withdraw this target application |
| Intervention changes the declared plant/resources | New case; no same-premise absence inference |

A finite success record does not establish the robust task over the full declared set. A local contradiction to a purported universal certificate can still identify a certificate or premise error. The future form must preserve that distinction.

## 3. C-P1-010 template: theorem mapping before parameter comparison

Maintain separate Part A and Part B records. The supplied claim contains the candidate expression `K < 2(b - |B|)/T`; this proposal does not independently verify its theorem, strict boundary, or stability wording.

### A. Formal mapping and target applicability

| Row / source premise | Required future attachment | Non-match route |
|---|---|---|
| V0 / formal statement | Exact independently checked theorem, source/version or proof, force/velocity port and sign convention, storage definition, necessary versus sufficient direction, strictness/equality boundary, and conditions for the claimed coupled-stability conclusion | Until checked, all numeric interpretations are provisional candidate calculations; never promote an `iff` by repetition |
| V1 / P1 | Single-DoF reduction and validity domain; linear time-invariant virtual spring/damper; exact backward-difference velocity definition | Multi-DoF coupling or nonlinear direct-torque control is outside the stated class unless independently justified |
| V2 / P2 | Position sample and command-hold alignment; actual period; zero-order hold; absence of extra compute/transport/filter delay; quantization assumption and its target justification | Do not replace `T` with total latency or silently absorb jitter/delay into this formula; unresolved deviations need a separate extension |
| V3 / P3 | Continuous parallel linear viscous damping; identification method; actuator/gear contribution; load and temperature domain | Nonlinear friction, varying damping, or a digital damping term cannot simply be called physical `b` |
| V4 / P4 | Explicit passive-environment class and basis for that restriction | Arbitrary unknown or active environments are not covered |
| V5 / P5 | Independent requirement for device-port passivity against that class | Stability in a selected environment does not establish this property or make passivity necessary |
| V6 / P6, Part B | Joint-reflected `b_j`, units, interval, uncertainty source, and domain matched to V3 | Unmeasured or mismatched damping leaves the threshold unresolved |
| V7 / P7, Part B | Task-derived `K_req,j`, units, uncertainty/requirement range, owner, and derivation independent of installed gains | Copying controller gains into the requirement is circular |
| V8 / P8, Part B | Physical and virtual stiffness contributions separately specified; intrinsic compliance mechanism; coupled-model justification for any decomposition | Do not subtract physical stiffness from task stiffness without a valid model; physical provision may defeat the virtual-only premise |

V0 must explicitly reconcile the source record's strict inequality, its use of “largest,” and its equality-case falsifier before using equality as a verdict. It must also distinguish device-port passivity from stability of one coupled environment. No external theorem is asserted verified in this packet.

### B. Conservative parameter worksheet

Blank entries: `b in [b_L,b_U]`, `|B| in [beta_L,beta_U]`, `T in [T_L,T_U]`, `K_req in [K_L,K_U]`, all with units, domain, and uncertainty interpretation. Require positive periods and nonnegative stiffness. The interval for `T` bounds an unknown fixed period across admissible cases; it does not authorize within-run variable sampling under a fixed-period theorem.

After V0–V8 are supported, the following are prospective interpretations of the candidate bound, not target results:

| Comparison | Permitted inference |
|---|---|
| `K_L > 2*b_U/T_L` | Part B trigger holds throughout the bounded parameter domain, even under the optimistic zero-virtual-damping ceiling |
| `K_U <= 2*b_L/T_U` | Part B's strict trigger is not established anywhere in this bounded domain; this does not certify passivity, particularly with nonzero virtual damping |
| Neither comparison resolves the trigger | Uncertainty-straddling; no rate conclusion |
| Known virtual damping and `b_L > beta_U` | Candidate ceiling enclosure: `[2*(b_L-beta_U)/T_U, 2*(b_U-beta_L)/T_L]`; compare only under the independently checked boundary convention |
| `b-beta` may be nonpositive | Separate parameter cases; no positive-stiffness guarantee follows for those cases from the strict candidate inequality |

These interval comparisons are conservative; correlations can make them inconclusive. A narrower joint uncertainty set requires documented justification, not a convenient choice of endpoints. Statistical confidence intervals produce conclusions at that coverage only.

When the Part B trigger is supported, the permitted conclusion is restricted: the stated sampled virtual-impedance class at that period cannot supply the required passive guarantee under the matched candidate premises. A faster loop or physical provision is an option to assess, not a validated solution or an exhaustive necessity across all architectures. Changed damping, task requirements, environment guarantees, or controller class change the case. A faster period alone does not establish target passivity or competence.

Part A remains independently reviewable even if Part B is unresolved. Conversely, a measured task success or a threshold comparison cannot verify Part A. A proposed in-premise violation must include device-port passivity evidence and a complete mapping; stability against one environment is insufficient. Formal-bound objections and target-premise failures remain distinct entries.

## 4. Joint use, governance, and selection

Shared physical evidence may be referenced by both forms only with an explicit coordinate and scope mapping. A damping estimate does not prove incompatible safe histories; a force-response deadline does not prove a sampled-data passivity bound. Passive mechanics may realize C-P1-002 while placing a target outside C-P1-010's virtual-only application. This is a coherent outcome, not a reason to modify the target after observing results.

Select this design for its explicit treatment of inconclusive evidence, passive mechanisms, and uncertainty at the decision boundary. Its cost is two evidence records rather than one checkbox sheet. Start with one declared mode/joint and reuse provenance references to limit paperwork. Dominant failure modes are incomplete force accounting, circular task requirements, overbroad theorem transfer, and post-result scope changes; the corresponding rows make each visible without imposing an engineering gate.

The proposal supplies reusable fields and prospective routing only. Every target evidence row starts UNSET. No claim is recommended for promotion by this packet. Candidate claims cannot veto a route. No architecture, controller rate, ladder order, or processor location becomes mandatory.

Future experiments require a separate sealed PLAN and authorization; no counterexample search is performed here. Future Grade-2 locking requires the B.9.2 implementation-independent argument, operational test, logged serious failed counterexample search, and human signature. Future Grade-1 locking requires independent verification and human signature. A non-author bound adjudicator handles any state change. This template's author does not adjudicate its own amendments, including amendments affecting a claim for which the roster otherwise assigns that author's family.

Read-only provenance: run-root `brief.md` and `roster.md`; packet `brief.md` and `roster.md`; all seven supplied files in `packets/Prin-8/source/`: the two claim records, `method-Appendix-B.md`, `packet-brief.md`, `Prin-4-decision.md`, `Prin-7-decision.md`, and `program-ledger-current.md`. No competing draft was consulted. No upgrade/violation logs beyond these supplied sources were inspected; no historical narrowing count or retirement finding is asserted.
