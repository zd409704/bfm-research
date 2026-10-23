# C-P1-012 — Realized-effort export vs policy-rate commanded view for contact detection (confounded as written in P1)

| Field | Value |
|---|---|
| **ID** | C-P1-012 (inherited by ID from `inherited-ledger-P1.md`; origin A-C7) |
| **Short title** | Observer-vs-policy contact residual: is a realized-torque export above policy rate necessary? |
| **Author family** | Opus (P1 Proposal A). Record compiled in Prin-1 by Author A (Opus). |
| **Claim adjudicator (per roster)** | Codex gpt-6-astra high (cross-family), not this author. |
| **Grade** | **Grade 2** (Prin-1 downgrade accepted; reconciled in Prin-3). Necessity remains unproved. The Grade-1 form stays an open upgrade target. |
| **State** | **Candidate — stay** (Prin-3 adjudication). Not Locked; no recommendation for lock or retirement nomination. |

## P1 statement (verbatim intent, for traceability)

"Exporting `τ_realized` at ≥ R1 is necessary for contact detection at the PF-1 sensitivity; commanded setpoints at R2 are not enough." P1 supported this only by the planned SA-2 comparison of export contracts E-R0, E-R1 and E-policy, with PF-2 as falsifier. That spike was never run.

## Restated claim (two separable factors)

The P1 wording combines two independent factors:

- **Factor R (rate):** contact detection at the stated sensitivity needs body-state information above policy rate (R1 ≥ 200 Hz vs R2 ≈ 50 Hz).
- **Factor E (effort source):** contact detection at the stated sensitivity needs an effort signal measured downstream of the command (realized actuator effort). The commanded setpoints plus the nominal control law do not suffice, because unmodeled actuator effects are a nuisance input that would otherwise be confused with external contact torque.

**Grade-2 role (recommended form):** for a contact-rich home-humanoid / target-plant competence class with unmodeled actuator effects, the body loop must export an effort-information channel that cannot be reconstructed from upper-layer commands, at a rate set by the contact-duration class of interest. The implementation can vary: current-derived torque, joint torque sensors, or a fast-tier observer that exports its residual.

**Grade-1 upgrade target (not yet argued):** an identifiability statement. Take joint dynamics `M q̈ + h = τ_cmd + τ_act_unmodeled + J_cᵀF`, observed through `(q, q̇)` sampled at period `T`. If `τ_act_unmodeled` has unknown structure and overlaps `J_cᵀF` in time and frequency within the contact class, then `J_cᵀF` is not identifiable from `(q, q̇, τ_cmd)` without a measurement of `τ_cmd + τ_act_unmodeled`. A related rate-floor statement would hold for contact durations near `T`. This has to be proved, not shown by a spike.

## Premises (numbered, explicit)

1. Rigid-body joint dynamics with known kinematics and nominal inertial model.
2. Actuators have unmodeled effects: Coulomb or viscous friction, saturation, and transmission losses. The location of each effect relative to the effort sensor must be declared, as upstream or downstream of the current/torque measurement (see H3). Declare which effects each measurement contains, which remain unobserved, and which permitted signals can distinguish them from contact. “Realized effort” names no privileged implementation (Prin-3 B-1).
3. Contact class specified by duration `d`, magnitude `‖J_cᵀF‖`, and location. Detection is defined by TPR at a fixed false-event rate, plus a latency percentile.
4. Detector class stated. For the Grade-2 role, the detector is any detector. For the P1 spike, it was a generalized-momentum observer followed by CUSUM.
5. No independent contact channel (tactile, F/T, vision). See C-P1-011, premise 2.
6. Upper layer receives only the exported fields (C-P1-011 Markov premise).

## Conclusion shape

**Obligatory functional role (Grade 2, Candidate).** The P1 phrasing was "necessary", which reads as a lower bound. As P1 wrote it, that phrasing rests only on a planned spike, and a spike cannot carry necessity (B.3.5, B.5).

## Scope

**Covers:** contact detection and localization from proprioception on the target-plant class, for non-foot contacts, within the contact classes in premise 3.

**Does not cover:**
- Foot or stance contacts during locomotion. P1 deferred this to SA-3, which has not been run.
- Contact semantics or classification.
- Plants with dedicated torque or tactile sensing (premise 5). These satisfy the role trivially.
- Any claim about what an existing pretrained behavior model estimates.
- Any ordering of S0/S2a relative to S1 (see H6).

## Falsifier / challenge mode

- **Factorial falsifier (replaces P1 PF-2).** Run a 2×2 design: rate {R2, R1} × effort source {commanded + nominal law, realized}. Re-tune the detector per rate, and keep the friction placement physically explicit. A falsifying alternative must meet the same declared task’s absolute detection and latency contract (Prin-1 repair; clarified by Prin-3 B-1/B-2). Retain every registered class with `d ≥ 10 ms`; no reference-selected identifiable set replaces it.
  - If commanded-at-R1 matches realized-at-R1 (ΔTPR ≤ 0.05 and Δp95 ≤ 10 ms on every class with `d ≥ 10 ms`), **Factor E is falsified** for that plant model.
  - If realized-at-R2 matches realized-at-R1, **Factor R is falsified**.
  - If both are falsified, retire-nominate.
  - **Prospective comparison semantics (Prin-3 B-2):** preserve the matching thresholds and p95 statistic. Predeclare miss handling, event accounting, confidence family and comparison direction. Infinity minus infinity is not a finite latency match. Distinguish a competent match, an established failure of the matching rule, and an inconclusive comparison due to unresolved latency or uncertainty. Filed Eng-1 flags are unchanged.
- **A positive spike result does not establish the role.** When realized-at-R1 beats the alternatives, that is evidence that this detector, this export and this plant model are sufficient. It is not necessity. Promotion needs the B.9.2 Grade-2 route: an argument across implementation classes, an operational test, and a logged failed search for a role-free system.
- **Operational realization test (B.9.3):** intervene on the exported effort channel by replacing it with the command-reconstructed value. Detection TPR on the identifiable classes must drop by more than a stated margin at a fixed false-event rate. If it does not drop, the role is not realized by that channel on that fixture, detector and calibration; this is not proof that effort information is absent. Credit a positive intervention as realization only after the implementation meets the declared task’s absolute detection and latency contract (Prin-3 B-1). Future PLANs must state the substitution margin explicitly before execution; retain the filed criterion and negative DOWN outcome without lowering the margin or removing d50_M10 (Prin-3 B-2).

## Hygiene notes (from P1 decision and this review)

- **H1 — Two-factor confound (P1 decision: "ordering leans on confounded C7").** The P1 E-policy contract differs from E-R1 in rate (50 vs 200 Hz) **and** in effort source (commanded-reconstructed vs realized) at the same time. PF-2 therefore cannot attribute a difference to either factor. A result in either direction says nothing about whether `τ_realized` specifically is needed.
- **H2 — Detector tuning confound.** A single momentum-observer gain of 50 s⁻¹ was used for every contract. At the R2 period of 20 ms, gain × T ≈ 1. The discretized observer sits near its stability and aliasing margin there, so it is handicapped by construction compared with R1 (gain × T ≈ 0.25). The detector must be re-tuned per rate, for example by holding gain × T fixed or by an optimizing tuning applied identically to every cell.
- **H3 — Built-in conclusion / physical placement stretch.** The P1 sim put Coulomb and viscous friction *inside* the "realized" torque and *outside* the commanded torque. Physically, current-derived torque measures motor-side effort. Joint-side friction downstream of the motor is **not** in a current-derived signal. That made E-R1 privileged by construction, in a way real current sensing would not be. The planned spike would have partly measured its own assumption. Premise 2 now requires the placement to be declared, and the factorial must include a variant with friction downstream of sensing.
- **H4 — Grade mislabel.** "1 (formal)" had no proof or cited theorem. The only support offered was a spike, and spikes prove sufficiency only (B.4, B.5). Hence the downgrade.
- **H5 — Unused premise.** The P1 statement was tied to "PF-1 sensitivity". PF-1 is a pre-registered spike threshold, not an implementation-independent task requirement. A necessity claim cannot take its premises from a spike threshold. Premise 3 replaces it with a task-stated contact class.
- **H6 — Not an ordering necessity.** P1 used A-C7 as the "necessity basis" for merging S0 and S2a and for ordering them before S1. Even in its repaired form, this claim constrains *what the body loop exports*. It does not constrain the research order. Ladder edges belong to Prin-2, Grade 3 by default (B.8.2). **D-P1-001 is a Provisional S0a acceptance-gate recommendation, not a necessity ordering**, and the P1 Alternate (S2a next packet) is a planning choice. This claim must not be cited to turn either into necessity.
- **H7 — Citation ablation (B.8.7).** No evolutionary, developmental or anatomical citation is involved, so the ablation leaves it intact. The weakness is the missing formal argument (H4), not biology.
- **H8 — Dependence on C-P1-011.** The "upper layers cannot recover it later" part of the motivation rests on C-P1-011 together with its side-channel premise. If upper layers keep command history, Factor E's nuisance argument still holds, but nothing beyond that.

## Recommended adjudicator action

**downgrade-grade** (Grade 1 label → Grade 2 Candidate). Apply **tighten-premises** in the same step:
- split the claim into Factors R and E;
- replace "PF-1 sensitivity" with a task-stated contact class;
- declare where friction sits relative to the sensor.

It stays **Candidate**. It is not eligible for recommended-for-lock until the factorial spike has run and the Grade-2 route of B.9.2 is complete. If both factors are falsified, the adjudicator should consider **retire-nominate**.

## Counterexample-search spike registered?

**Yes.**
One-line PLAN: a sim-only, numpy-only 2×2 factorial (rate {50, 200} Hz × effort source {commanded + nominal law, realized}) on the P1 planar 2-link arm. It uses two friction-placement variants (upstream/downstream of current sensing), a per-rate re-tuned observer (fixed gain·T) and a fixed false-event rate of 0.01/s, with 3 seeds. A **counterexample** is any non-realized or R2 cell that matches realized-at-R1 within ΔTPR ≤ 0.05 and Δp95 ≤ 10 ms on every class with `d ≥ 10 ms`. Under B.9.8 the runner files data only and does not change state, and a PASS is sufficiency evidence only.
