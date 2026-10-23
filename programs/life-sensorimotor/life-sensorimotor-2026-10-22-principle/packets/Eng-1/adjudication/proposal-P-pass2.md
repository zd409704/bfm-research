# Eng-1 — Proposal B: envelope certificates for coupled modes

Author B. **Recommend one primary scope: richer-plant S0a finite-horizon envelope certification.** Proposed/provisional; sealed deferred-runnable PLAN, no experiment results. No new necessity claim.

## Thesis

Extend the provisional S0a acceptance contract to a coupled plant with delayed sensing, actuator memory/limits and explicit mode transitions. Produce a checkable reachable tube and a versioned refusal interface: a verified model certificate, a concrete failure witness, or an explicit unresolved result. The next scientific question is whether the scalar acceptance concept remains useful when these assumptions interact.

This is the richer-plant S0a option, distinct in scope from an S2a contact-observability floor or a merged S0a/S2a export package. No contact detector, new impedance tier, locomotion policy or scene planner is included. Isolation prevents checking the other author's scope; no claim about unseen proposal contents is made.

Relative to S2a, this choice costs more model work and yields less immediate contact-channel evidence, but addresses actuator authority, envelope ownership/versioning and transition semantics. Relative to a merged packet, it has one acceptance object and a small controller. S2a remains an admissible alternative and may proceed independently. Engineering order is a reversible planning choice.

Inherit by ID: D-P1-001; X-P1-001, X-P1-002, X-P1-003, X-P1-004. **D-P1-001 remains Provisional S0a acceptance-gate, NOT necessity order.** No prior conclusion is rewritten.

## Necessity vs sufficiency

Apply B.9.5 before ranking: no Locked Grade-1 or Locked Grade-2 claim is present, and **NO Prin-2 ladder edge is an Eng-1 necessity gate**. No Candidate supplies a veto or an incomplete-role ruling. The requirements below are chosen engineering acceptance specifications.

| Design input | Authoritative grade/state | Permitted use and limitation |
|---|---|---|
| C-P1-001 | Grade 1 narrow scalar Candidate; conditional recommendation-for-lock | Motivate separating response latency from feasibility. Its scalar limit does not certify this coupled fixture; independent verification/target match remain open. |
| C-P1-002 | Grade 2 Candidate, tighten-premises | Inventory total corrective forces and actuator authority. No incompatible-history proof for the richer fixture or mandatory active module is asserted. |
| C-P1-003 | Grade 3 Candidate, quarantined | No gate or necessity-order argument. |
| C-P1-010 | Grade 1 formal/conditional Candidate, tighten-premises | Scope warning: single-joint passivity relation does not certify coupled delayed dynamics. We seek envelope containment, not passivity. |
| C-P1-011 | Grade 1 narrow DPI Candidate | Audit all controller inputs and provenance; no mandatory contact export or research order follows. |
| C-P1-012 | **Grade 2 Candidate, downgraded from Grade 1** | Rate/effort confound warning only. Not a Grade-1 necessity for export. Logging applied effort for envelope auditing does not assert that a contact detector requires it. |
| C-Prin2-E03 / E07 | Conditional Grade 1 availability kernels; E03 also Grade 2 companion; acquisition readings Grade 3; all Candidate | Expose missing timing/task/disturbance matches. No scalar-to-coupled transfer and no gate. |
| C-Prin2-E13 / E15 | Provisional narrow Grade 1 hypotheses; general/acquisition Grade 3; Candidate | No S0b or passivity prerequisite. |
| C-Prin2-E17 | Conditional Grade 1 KL core, tighten-premises; acquisition Grade 3; Candidate | No contact-information floor is imposed; do not inherit its uncorrected zero-FPR assertion. |

A verified certificate establishes finite-horizon sufficiency for one controller and its exact model/sets. A violation defeats that implementation/contract combination, not all implementations. Failure to certify may be numerical conservatism, not impossibility. No universal rate floor, obligatory active correction, stage order or hardware transfer follows. Removing biological citations leaves the rationale unchanged; none is load-bearing.

## Interface contracts

| Owner / interface | Contract | Operational check |
|---|---|---|
| Target-plant/envelope owner | Version state/units, initial set, horizon, disturbance/model-error sets, observations, modes/resets and effort/timing limits. Synthetic values are author choices; target use needs owner ratification and measurements. | Changed or missing premises invalidate applicability; hash every version. |
| Body-loop owner | Fixed feedback in the spike sees delayed noisy state only. Command and applied effort are distinct. Actuator and delayed-state memory persist across resets. | Trace timing and force provenance; no evaluator mode/reset/disturbance truth in feedback. |
| Certificate producer and separate checker paths | Bind reachable tube to plant/controller/contract hashes, arithmetic method, schedule, delay and finite horizon. Preserve uncertainty correlations. | Independently reconstruct bounds; mutation tests reject incompatible certificates. Unresolved is not unsafe. |
| Scene publisher | Read-only certificate ID, version, scope, expiry, observation age and status. No contact label is exported by this packet. | Stale/missing status becomes unknown, never accepted; publisher cannot widen bounds. |
| Decision core | Request a scenario and consume scoped validity. Unknown requests are refused by this acceptance interface. | Unsupported schedule/disturbance request returns OUT_OF_SCOPE. Refusal is not a physically certified stopping maneuver. |

The fixture's 1 ms clock defines a synthetic model, not a recommended target frequency. Scene publication and the decision core are asynchronous readers outside feedback. Certificates cover 0.2 s; concatenation requires a checked handoff-state inclusion including actuator/history memory. Evaluator-known schedules are scenario assumptions, not contact-mode inference. No physical trial is authorized or required.

## Claims table

New IDs below are **engineering Candidate hypotheses**, not necessity claims. Grade N/A means sufficiency/contract, not Grade 1/2/3. They have no lock or veto authority. No new necessity claim directories are needed; inherited claims are reused as design inputs.

| ID | Engineering hypothesis and scope | Evidence / failure | State and grade |
|---|---|---|---|
| C-Eng1-B-01 | The PLAN's fixed delayed-feedback controller admits a checked envelope certificate for at least one fixed-mode and one transition cell at the same delay. | No qualifying pair means unsupported. A verified in-set replay outside a claimed certified envelope falsifies that certificate implementation. | Candidate, untested; sufficiency, N/A |
| C-Eng1-B-02 | Version/scope checks prevent certificate reuse for incompatible delay, reset, disturbance or schedule. | Mutation tests must reject; acceptance of an incompatible certificate fails the contract. | Candidate, untested; contract, N/A |
| C-Eng1-B-03 | Separate observation age, commands, applied effort and evaluator truth make timing/authority assumptions auditable without S2a. | Missing provenance or a truth leak fails the audit. This is not a contact-observability result. | Candidate, untested; contract, N/A |

Any future necessity claim needs its own claim.md, upgrade-log.md and violations.md, explicit grade/premises/falsifier and separate cross-family adjudication. No state transition, independent proof verification or signature is implied here.

## Minimal spike PLAN

Complete preregistration: **packets/Eng-1/drafts/B/PLAN.md**, sealed by **PLAN.sha256** before execution. Deferred-runnable, no implementation or experiment executed. PLAN-only leaves the proposal provisional.

CPU-only, 15 minutes / 1 GiB. A two-state discrete coupled surrogate has two modes, bounded disturbances/noise, four observation delays, a first-order actuator, effort caps and a declared reset. Sixteen cells cover four schedules. Correlation-preserving affine reachability certifies only when saturation is proven inactive; exact/outward-rounded arithmetic checks bounds. Otherwise report unresolved or a verified clipped-system violation.

Analytic positive/negative controls and deliberate delay/reset/channel/scope mutations test the harness. Engineering support additionally requires a verified fixed-mode/transition pair at one delay. **Harness PASS may coexist with engineering NOT_SUPPORTED. PASS = harness only; never hardware transfer.** Equations, step ordering, limits, verdict schema and amendment rules are fixed in the sealed PLAN.

A supported result recommends the certificate interface as a model-scoped acceptance artifact. An unsupported result favors the S2a alternative or an explicitly amended narrower contract; never silently reduce disturbance, remove transitions, increase effort or change the envelope. Measured target-premise matching remains separate work.

## Failure modes

| Risk | Handling |
|---|---|
| Synthetic model presented as target physics | Label normalized parameters synthetic; no target certification without measured dynamics/error sets, actuator/timing characterization and ratified envelope. |
| Sampled containment presented as continuous safety | Cover discrete states/reset only; intersample and infinite-horizon claims require separate evidence. |
| Ignoring saturation or delayed-state correlations | Validate pre-clip commands; preserve generator identities, actuator memory and shared initial history; unresolved cases remain explicit. |
| Composing per-mode or successive-horizon certificates | Verify reset and whole incoming augmented state. No arbitrary switching or repeated-horizon guarantee. |
| Loose bounds presented as impossibility | Require a verified concrete in-set violation witness; otherwise unresolved. |
| Truth leakage or stale status | Audit input provenance and expiry; unsupported acceptance requests are refused without claiming safe physical stopping. |
| Scope growth into a merged architecture | No contact detector, impedance design, S1 training or S2 benchmark. Keep interfaces reversible. |

## Non-claims

No lock, transferable necessity, stage-order law, unique controller, mandatory rate or effort export. No passivity guarantee, arbitrary-switching guarantee, continuous/infinite-horizon safety, complete locomotion/manipulation competence or hardware transfer. No experiment result or certificate is asserted before running the plan. Passive, embedded, direct-policy and joint-design alternatives remain admissible under explicit contracts.

## Bypassed Grade-3 edges list

B.8.5 inventory distinguishes waived prerequisite readings from experimentally demonstrated bypasses. This S0a-only extension does not instantiate S1/S2a/S2 destinations; the set of forward ladder edges actually traversed/skipped in the spike is empty. The mandatory Prin-2 edge inventory is explicit below; no listed edge gates research.

| IDs / edge | Grade-3 reading | Bypass disposition |
|---|---|---|
| C-Prin2-E01 / E02: S0a → S0b | Both broad edges Grade 3 | No separate S0b package prerequisite imposed; destination deferred, no refutation claimed. |
| C-Prin2-E05 / E06: S0a → S2a | Grade 3 | Waived as ordering prerequisites for independent S2a; destination unexercised here. |
| C-Prin2-E08 / E09: S1 → S2a | Grade 3 | Prior S1 not required for future S2a; destination unexercised. |
| C-Prin2-E14: S0b → S2a | Grade 3 | No reflex/impedance prerequisite on independent observation; destination unexercised. |
| C-Prin2-E10 / E11: S2a → S1 | Grade 3 | S1 is not pursued. Adding S1 without S2a would be an actual bypass to record, not a reason to import a gate. |
| C-Prin2-E03 / E04: S0a → S1 | Acquisition Grade 3; E04 broad edge Grade 3 | S1 deferred; E03 conditional Candidate availability kernel is not a gate. |
| C-Prin2-E07: S0a → S2 | Acquisition Grade 3 | S2 deferred; conditional Candidate availability kernel is not a gate. |
| C-Prin2-E12 / E13: S0b → S1 | E12 broad edge; E13 general/acquisition Grade 3 | S1 deferred, no impedance prerequisite. |
| C-Prin2-E15: S0b → S2 | General/acquisition Grade 3 | S2 deferred; narrow Candidate passivity hypothesis is not a gate. |
| C-Prin2-E17: S2a → S2 | Acquisition Grade 3 | S2 deferred; Candidate information kernel is not a gate. |
| C-Prin2-E19: S1 → S2 | Grade 3 | Destinations outside this packet; no planning sequence imposed. |

Unknown mode inference is not hidden S2a: feedback receives no mode label. The finite scenario language is an evaluator premise, not a perception result. No Grade-3 edge is refuted by a paper construction or by harness PASS.

Provenance: brief.md; roster.md; packets/Eng-1/source/*; cited claims/C-P1-*/claim.md and claims/C-Prin2-E*/claim.md. Sealed decisions/adjudication summaries govern over older author nominations. No other author's drafts or proposals were consulted.
