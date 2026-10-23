# Red-team review of Proposal P

# Review B-on-A

## Summary (3-6 sentences)

Proposal A is not ready to Recommend as a locked research mainline. Its narrow mathematical statements do not establish the necessity of the merged S0/S2a contract, and the decisive spike cannot distinguish sampling-rate benefits from realized-torque benefits. The proposed passivity guarantee also exceeds the controller assumptions supporting C1. Although the proposal separates biological inspiration from necessity and specifies useful ownership boundaries, unresolved measurement semantics, identifiability dependencies, and verdict rules prevent its spike from supporting the intended decision. These objections concern A alone; Proposal B was not opened or used in this review.

## Rubric objections

### 1. Constraint fit

- **score_suggestion:** 3
- **objection_or_pass:** **Objection.** The proposal respects the local-compute restriction, avoids comparative performance claims, and permits a deferred spike. However, its proposed lock depends explicitly on C7 “surviving PF-2,” which would turn a benchmark comparison into authority for a necessity-based architectural lock. That conflicts with the brief’s hard constraint 6 and Appendix B.3–B.5. I5 and the locked ownership rules also prescribe Life Core access and control restrictions beyond what is necessary to establish the first S0–S2 packet; these restrictions need justification as interface requirements rather than premature S7 decisions.

### 2. Falsifiability

- **score_suggestion:** 2
- **objection_or_pass:** **Objection.** SA-2 can test a particular detector and export combination, but its interpretation is not adequately falsifiable:
  - E-R1 versus E-policy changes sampling rate, torque access, and torque reconstruction together. Failure of E-policy cannot identify which change matters.
  - PF-2 requires equivalence on **every** eligible class. Its negation can arise from one class and is not evidence that realized-torque export is necessary throughout the proposed scope.
  - Detection windows, missed-detection treatment in latency statistics, temporal sampling phase, whitening, and the definition of “identifiable classes” remain unspecified. These choices can change the verdict.
  - PF-5 failure has no assigned overall outcome when the other criteria pass. INVALID and FAIL-thesis conditions can also occur simultaneously without precedence.
  - PF-4 treats an asymptotic detection-delay expression as a finite-sample bound with a fixed 10% tolerance. The proposed half-sine pulses and pooled mean delay do not establish the conditions needed for that interpretation. Asymptotic change-detection guarantees require an explicit statistical model and limiting regime; nonstationary changes require additional treatment. [Lorden’s original paper](https://authors.library.caltech.edu/records/n9ryc-0sr08), [Liang, Tartakovsky, and Veeravalli](https://arxiv.org/abs/2110.01581).

### 3. Evidence demand

- **score_suggestion:** 2
- **objection_or_pass:** **Objection.** The advertised “≤15 min CPU” budget is unsupported by the literal SA-1 procedure. At the low-frequency end near `ω = 0.01 rad/s`, 50 periods span approximately 31,416 seconds of simulated time. For `T = 0.5 ms`, `dt = T/200` implies roughly **12.6 billion integration samples for one frequency evaluation**, before the remaining frequency, stiffness, and damping sweeps. An exact integration shortcut could change this cost, but none is specified. Separately, the evidence needed for the proposed lock includes actuator telemetry semantics, physical damping, task stiffness requirements, and locomotion transfer; those remain deferred, so inexpensive fixed-base results cannot validate the full contract.

### 4. Failure modes

- **score_suggestion:** 2
- **objection_or_pass:** **Objection.** The failure table names relevant risks but understates their consequences.
  - SA-2 defines realized torque as including unmodeled friction and other actuator effects, while I1 calls it current-derived torque. The proposal does not establish that this measurement provides the same net generalized torque used in the simulator. Supplying that value directly could give the observer privileged cancellation of the uncertainty it is supposed to tolerate.
  - F2 permits a learned residual model without specifying how calibration avoids absorbing contact signals or how changes in motion affect false alarms.
  - Thresholds are calibrated on contact-free data, but no independent contact-free evaluation is specified.
  - F3’s fallback to quasi-static, non-foot contact detection materially changes the scope of a humanoid stacking foundation. It cannot preserve the original lock without re-adjudication.
  - “Safe-hold” is named but not defined for a floating-base robot in an unstable stance.

### 5. Integrability

- **score_suggestion:** 3
- **objection_or_pass:** **Objection.** Body-loop ownership of torque and Scene Graph ownership of object association are clear. The principal integration gap is I2: `ident_flag` depends on a candidate contact Jacobian set, yet localization and classification are deferred to S2b. The contract does not specify who supplies contact hypotheses, their geometric uncertainty, or what the flag means when hypotheses are missing. Full rank conditional on a known contact location does not establish identifiability when location itself is unknown. Additionally, `dir = r/‖r‖` is a direction in generalized-force coordinates, not automatically a physical contact-force direction, and requires defined behavior near zero.

### 6. Latency / criticality class

- **score_suggestion:** 2
- **objection_or_pass:** **Objection.** Fast actuation and slow cognition are sensibly separated, but the mandatory rates are not derived from measured premises. More seriously, C1 does not justify the passivity guarantee attached to I0. The cited analysis assumes a particular sampled controller and actuator model; I0 additionally permits moving references, feedforward torque, gain changes, interpolation, and fallback switching. A per-joint stiffness clamp alone does not account for energy introduced through those channels or establish the coupled robot’s passivity. [Colgate and Schenkel’s original analysis](https://cim.mcgill.ca/~hayward/Teach/papers/Part-II/Colgate-Schenkel-94.pdf).
  
  R1’s update frequency also leaves acquisition delay, filtering, communication jitter, execution deadlines, and actuation delay unspecified. Consequently, PF-1’s detection latency does not establish a corresponding reflex-response guarantee.

### 7. Complexity cost

- **score_suggestion:** 3
- **objection_or_pass:** **Objection.** The locked package is larger than “a schema plus two invariants.” It requires a dynamics model, momentum observer, covariance calibration, whitening, change detection, contact-hypothesis rank analysis, episode formation, reflex management, and potentially a learned residual model. PF-5 makes link localization a pass requirement despite deferring localization to S2b. The proposal has not shown which of these mechanisms is necessary to establish the first contract, and the proposed spike cannot attribute benefit among them.

### 8. Reversibility

- **score_suggestion:** 4
- **objection_or_pass:** **Pass, with a qualification.** A local simulation and unadopted schema are inexpensive to abandon. The claimed low abandonment cost becomes less credible after adoption: mandatory telemetry can require firmware work, passivity clamps can change policy behavior, and downstream consumers can become dependent on I2. Removing `τ_realized` would not reverse those commitments automatically. The score assumes the contract remains provisional during evaluation.

### 9. Necessity discipline (Appendix B)

- **score_suggestion:** 1
- **objection_or_pass:** **Objection.** This is the central blocker.
  - **C2 does not select this contract.** The data-processing inequality constrains a specified information chain. It does not prove that the proposed fields, rates, module boundary, or stage ordering are necessary. Applying it to S4 also requires accounting for action-dependent future observations; information unavailable in one passive observation need not remain unavailable after probing.
  - **C7 lacks implementation independence.** One generalized-momentum observer under two unequal observation configurations cannot establish an impossibility across admissible estimators and sensing arrangements. Surviving a falsifier is not proof. Appendix B explicitly prohibits promoting performance differences into necessity.
  - **C1′ and C5 remain Candidate but carry architectural force.** Until their premises bind for the scoped tasks and hardware, they can guide exploration but cannot exclude other mainlines.
  - **C6 reverses the force of a lower bound.** Even accepting `‖T‖∞ ≥ 1.10`, a small lower bound does not establish attainable performance, adequate robustness, or that balance constraints are nonbinding. No task-specific admissible norm is supplied, and the proposed 200 ms threshold is not derived.
  - **The lock boundary is blurred.** Narrow formal claims may lock early under Appendix B. That does not transfer Locked status to a robot interface merely because its rationale cites them.

### 10. Stackability

- **score_suggestion:** 2
- **objection_or_pass:** **Objection.** Timestamped state and residual exports could support later stages, but several gates are assumed rather than established.
  - S1 cannot be described as working “unchanged” while also requiring a change from raw torque outputs to impedance setpoints and imposing gain clamps. Compatibility needs an explicit check.
  - SA-3 requires stance-conditioned subtraction to make the residual usable during locomotion. The proposal therefore defers a major S1/S2 dependency while presenting S2a as the foundation that should precede S1.
  - S4 needs more than a null-space dimension: it needs sufficient contact hypotheses and uncertainty information to choose an informative action.
  - Making reduced free-motion residual variance the initial S3 target does not establish preserved contact sensitivity. A predictor could improve that metric while suppressing useful contact evidence.

## Fatal risks (if any)

The following are fatal to **Recommend as a locked mainline in the present form**, not evidence that the underlying engineering direction is impossible:

1. **Invalid necessity promotion.** The proposal explicitly makes its ordering depend on C7 surviving a confounded benchmark comparison. Even a complete numerical PASS would not supply the non-score evidence Appendix B requires.
2. **Unsupported passivity invariant.** The declared envelope is applied to a controller interface outside the demonstrated theorem assumptions. Clamping gains cannot, by itself, establish the promised guarantee.
3. **Measurement mismatch in the decisive experiment.** If simulated `τ_realized` contains net torque information unavailable from the specified current measurement, the experiment evaluates a materially different sensing contract.
4. **An incomplete decision procedure.** Unassigned verdict cases, unspecified statistical conventions, and PF-4’s unsupported finite-sample interpretation prevent the spike from producing a reliable adjudication.

## What would need to change for Recommend

- Establish a precise boundary between narrow formal locks, Candidate necessity claims, and provisional engineering choices. A favorable spike must not automatically promote C7 or the merged stage ordering.
- Supply implementation-independent necessity evidence for the claimed mandatory information role, or withdraw the claim that this particular export contract is necessary.
- Demonstrate that the passivity claim applies to the actual permitted commands, gain changes, timing, and system coupling, or narrow the guarantee accordingly.
- Define torque measurement semantics and uncertainty consistently across the interface and simulator; resolve the contact-hypothesis dependency behind `ident_flag`.
- Repair the experiment so rate and torque-access effects can be distinguished, define all scoring conventions, evaluate false alarms independently, and assign an unambiguous verdict to every outcome.
- Replace the unsupported runtime estimate with a demonstrated feasible execution method. File either executable evidence or the complete deferred plan required by the brief; a plan-only decision must remain provisional.
- Resolve or explicitly bound S1 compatibility and locomotion-dependent observability before describing this contract as the locked foundation for later stages.
