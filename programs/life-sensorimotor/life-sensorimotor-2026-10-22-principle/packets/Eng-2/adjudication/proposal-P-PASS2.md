# Eng-2 — Proposal B: contract-first, then one channel-ceiling discriminator

Author B (Astra). **Recommend a conditional sequence: ratified task/channel contract → one bounded amended-A discriminator → stop and choose again.** This is a proposed planning override of D-Eng-1-001's Alternate-B routing, requiring the human lead's branch choice under D-Prin-3-001. It is neither an authorized retry nor an assertion that S2a precedes S0a by necessity. Proposal and deferred PLAN only; no spike has run.

## Thesis

The next useful distinction is between a detector missing an attainable operating point and a specified channel failing to support that operating point under a specified probability model. Re-running a detector without a channel-level upper reference cannot resolve that distinction. Extend the engineering question with a small, exactly specified Gaussian channel surrogate whose likelihood-ratio reference yields both a ceiling and an attainable reference performance. Compare a frozen residual detector with that reference at identical false-positive units and deadlines. The result can be REF_DETECTOR_GAP, MODEL_CHANNEL_SHORTFALL, SUPPORTED, or UNRESOLVED; it cannot restore Eng-1 A02 or diagnose the historical detector without a matched model and implementation.

This choice inherits D-Prin-3-001's conditional sequence. **D-Eng-1-001 remains Closed — Recommend A spike FAIL: harness valid, A02 unmet.** X-Eng-1-001 is sufficiency data. SUB_DOWN_NOT_MET does not establish absent effort information; the UP result is outside C-P1-012's retained scope. No grade changes follow.

Why this branch: an exact reference can turn another failed engineering detector into an interpretable model-scoped result, while preserving the full class grid. The cost is delaying the coupled-mode envelope investigation by one implementation/run cycle, capped at one attempt and 15 CPU minutes for the run. It also introduces a deliberately simplified probability model. That cost is justified only if the human lead accepts this diagnostic question. If the priority is an independent envelope question, choose the amended-B alternative below. If neither question has an eligible contract, choose neither; do not manufacture a passing task.

## Necessity vs sufficiency

D-P1-001 remains a **Provisional acceptance-gate recommendation**, not a necessity order. D-Prin-2-001 supplies **no ladder-edge gates**. All listed claims remain Candidate, with no veto authority. Decisions govern over older author recommendations in claim records.

| Claim ID | Grade/state inherited | Use here; limit |
|---|---|---|
| C-P1-001 | Grade 1 narrow scalar Candidate; conditionally recommended-for-lock per ledger | Separates delay from feasibility. Its scalar bound does not certify this channel model or the coupled envelope alternative. |
| C-P1-002 | Grade 2 Candidate, tighten-premises | Audit all corrective-force sources if choosing the envelope branch. Does not require a new active module. |
| C-P1-003 | Grade 3 Candidate, quarantined | No load-bearing role. Evolutionary order supplies neither branch eligibility nor ranking. |
| C-P1-010 | Grade 1 narrow/conditional Candidate, tighten-premises | No extension of single-joint passivity to delayed coupled control, and no passivity requirement imposed here. |
| C-P1-011 | Grade 1 narrow DPI Candidate, tighten-premises | Declare the joint channel, command history and task metadata. Does not supply a detection ceiling numerically or mandate research order. |
| C-P1-012 | Grade 2 Candidate, retained by Prin-3 | Keep downstream nuisance and effort measurement point explicit. This simplified discriminator is not its registered factorial falsifier and does not amend its premises or event accounting. |
| C-Eng1-A-01 | Grade 1 narrow formal Candidate, unverified; no lock | Optional design rationale for one-sided achieved-performance reporting only. Independence must hold per window; this PLAN does not use it to certify absence or as an eligibility gate. |

The exact Gaussian reference is an engineering calculation under chosen simple hypotheses, not a new transferable necessity claim. A model-scoped upper bound can rule out the operating point for detectors restricted to that exact channel/model; it says nothing about an unmodeled target plant. Successful detectors demonstrate sufficiency only. No independent verification, Grade-1 lock, or human signature is asserted. Citation ablation leaves the engineering argument unchanged.

## Interface contracts

| Owner / boundary | Required contract |
|---|---|
| Human task/plant owner → experiment | Ratify every `(q_c,r_c)`, the 60 ms decision deadline and reset-window units, or explicitly approve the exploratory placeholder policy. Declare the target effort measurement point and nuisance placement. Select the branch. A surrogate is not a measurement of that plant. |
| Body-loop owner → export | Version `y` (velocity-increment acceleration equivalent), commanded effort, optional measured motor-side effort, timestamps, sample intervals, noise model, observation age and units. Downstream friction stays outside the measured-effort channel. All inputs to each detector must be enumerated. |
| Fixture producer → reference/checker | Freeze hypotheses, class metadata, covariance, contact onset convention and generator. Reference receives exported observations only; model parameters and a predeclared class are public protocol metadata. Neither realized nuisance nor the hidden contact label enters either detector. |
| Reference and detector → scene publisher | Separate analytic channel ceiling, detector confidence bounds and harness status, bound to contract/model/channel hashes. Export `UNKNOWN` on stale/mismatched scope. No `contact absent` inference from a failed certificate. |
| Scene publisher → decision core | Read-only report with expiry and scope; no feedback path. Export-on/off paired replay must have identical plant and command traces. No physical fallback maneuver is certified. |
| Claim adjudicator | Receives data and deviations; alone rules proposed C-P1-012 amendments and B.9.6 event accounting. Author B does not assign a zero event count or change existing claims. |

### Symmetric eligibility and amended-B alternative

Both branches require the common Prin-3 execution gate. Exploratory placeholders can authorize fixture execution only after explicit human approval; task acceptance/transfer requires a ratified task and a separate target-premise match. Candidate claims cannot veto either branch.

The independent amended-B question is: **for a fixed two-state coupled surrogate and one fixed controller, does a checked 200 ms tube remain in an owner-selected box across a declared support-mode transition, with sensing delay and actuator memory retained?** It is not a consequence of contact-detector failure. The concrete alternative contract is in PLAN §9: two synthetic modes, a declared reset, augmented-state ownership, CERTIFIED/VIOLATION/UNRESOLVED outcomes, and a fixed-mode/transition support criterion. It must undergo its own implementation-specific PLAN seal before execution. A full reachable-set solver is not part of the recommended spike.

## Claims table — new B hypotheses

These are engineering Candidate hypotheses, **grade N/A (sufficiency/contract)**; N/A is not a new necessity grade. No optional claim directory is needed for this proposal. Any later necessity reading needs a separate full claim record and cross-family adjudication (Opus for this author's claims).

| ID | Candidate statement, premises and scope | Falsifier / operational test |
|---|---|---|
| C-Eng2-B-01 | Under the PLAN's fixed Gaussian channel, the analytic likelihood-ratio reference and a separately implemented whitened calculation agree on achievable ROC at the registered deadline. Untested. | Disagreement above sealed tolerance; covariance/side-channel/pooling violation invalidates the reference. |
| C-Eng2-B-02 | At least one registered class/channel has a statistically established gap between the frozen detector and an attainable reference while the channel ceiling clears its requested operating point. Untested; detector-comparison sufficiency hypothesis. | No qualifying cell on the complete grid means NOT_SUPPORTED. Ceiling failure alone is not support for this hypothesis. |
| C-Eng2-B-03 | Version, scope, provenance and non-interference checks prevent an invalid certificate becoming accepted evidence. Untested contract hypothesis. | Any stale-version acceptance, hidden-label input, failed independence check or changed control trajectory fails the harness. |
| C-Eng2-B-04 | The independently chosen coupled envelope alternative can certify a fixed-mode and transition pair at the same delay without discarding memory. Untested alternative-only hypothesis. | No qualifying pair is NOT_SUPPORTED; an admissible replay outside a certified tube falsifies that certificate. An unresolved tube is not an impossibility proof. |

## Minimal spike PLAN (sealable)

See `packets/Eng-2/drafts/B/PLAN.md`. **DEFERRED; NOT EXECUTION-AUTHORIZED.** All synthetic parameters, full class grid, splits, analytic and sampled checks, bounds, decision rules and stopping rules are fixed there. Fill approval references and branch choice, inspect the implementation, then seal PLAN, implementation and contract together before drawing data. Any substantive change requires an amendment and reseal; old results remain attached to their original versions.

CPU/NumPy plus standard library, 15 minutes, 1 GiB, one frozen detector, one reference, 36 primary cells. The PLAN is a new controlled surrogate discriminator, not a reconstruction of inaccessible Eng-1 code. No historical A02 rerun or victory is claimed. Harness PASS is separated from every engineering status; **PASS = harness only, never hardware transfer**. PLAN-only keeps this proposal provisional.

## Failure modes

| Failure | Consequence / handling |
|---|---|
| Exact ceiling mistaken for a target-plant limit | Label every output with the Gaussian surrogate and known-onset protocol; no target conclusion without a new premise match. |
| Class/oracle metadata leaks event truth | Duration and magnitude are predeclared protocol settings shared by both hypotheses; onset time is a scheduled-probe assumption. Random unknown onset requires a separately sealed model. |
| A poor comparator manufactures a gap | Boxcar detector is transparent and frozen, not claimed to be Eng-1's detector or the best practical estimator. Gap supports only this fixture, detector and calibration. |
| Conditioning on convenient classes | Publish all 36 cells, including failed classes; no class removal or threshold loosening. Aggregate task support requires all designated classes. |
| False-event units or correlated windows change the inference | Use independent reset windows, one binary decision/window; report per-window probability and its restricted per-second conversion separately. No comparison to C-P1-012's registered test as if equivalent. |
| Tiny numerical margin or resource cap | Mark UNRESOLVED/INCOMPLETE, retain artifacts, do not retry with a changed threshold. |
| Downstream placement promoted to universal explanation | State only results for this fixture, detector and calibration; do not call placement the operative variable. |
| Waiting for approval becomes an architecture requirement | Contract ratification is a binding packet governance gate; it is not a physiological necessity or an S0/S2 ordering proof. |

## Non-claims

No hardware transfer, physical experiment, universal channel absence, unique export, rate necessity, new claim downgrade, Grade-1 lock, autonomous branch authorization, or ladder-order requirement. No UP/dedicated-sensor evidence enters C-P1-012. No refutation of C-P1-012 follows from this surrogate; mismatched scope is reported. Neither a favorable reference nor a new harness PASS repairs D-Eng-1-001 A02.

## Bypassed Grade-3 edges

Per the supplied Eng-1 inventory, the amended-A branch waives the ordering readings **E05/E06 (S0a → S2a), E08/E09 (S1 → S2a), and E14 (S0b → S2a)**. If run, record them as bypassed prerequisites in the run log, not experimentally refuted necessity claims. **E10/E11 (S2a → S1)** are listed but not bypassed because no S1 destination is pursued. **E17 acquisition/order reading (S2a → S2)** is not invoked; there is no S2 destination. The amended-B envelope-only alternative traverses no forward ladder destination. No bypass has been executed in this drafting task.

Provenance: only run `brief.md`, `roster.md`, `packets/Eng-2/source/*`, filed `packets/Prin-3/decision.md`, `claims/C-P1-*/claim.md`, and `claims/C-Eng1-A-01/claim.md`. No Eng-2 competing drafts/proposals were read. References embedded in those sources were not followed.
