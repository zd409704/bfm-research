# Review A-on-B

Reviewer: Proposal A author (Opus track), acting as Red Team on Proposal B. Drafts/A and proposals/A.md were not consulted during this review. Objections are keyed only to the brief's fixed rubric.

## Summary

Proposal B splits S0 into S0a (a bounded-response viability contract) and S0b (implementations), and proposes certifying S0a first. Its necessity discipline is careful: B-N1's derivation is correct (L* = ln(1.1)/10 = 9.531 ms; |x| at 20 ms = 0.0221403), grades and scopes are stated, and the non-claims are honest. The main weakness is that the spike cannot fail in an informative way. The reviewer extracted `run.py` verbatim and ran it in a scratch directory outside the run root (not filed under `spikes/`). It returns PASS with large margins: candidate peak 0.00609 against a 0.01 bound, maximum command 1.17 against a 3.0 limit, and a grid difference of 8.7e-18. No condition probes the L* boundary or anything transferable to the target plant. The second weakness is that a contact-agnostic "body envelope" is ill-posed for a legged humanoid, whose viability region depends on support and contact mode. That puts the separation of S0a from S1/S2 at risk. B is a credible Alternate, and could become Recommend if the spike is made discriminating and the envelope definition confronts contact dependence.

## Rubric objections

### 1. Constraint fit — score_suggestion: 4
Pass, with minor notes. The proposal stays CPU-only and sim-only, needs no training or BFM, writes only under the run root, keeps Grade 3 out of Locked, claims no comparative superiority, and makes no S7 decision. The brief allows the S0a/S0b split ("justified split/merge"). Minor: the brief treats the S0–S7 ladder as context "not free to rewrite". Introducing S0a/S0b sub-stages and an "envelope version" concept should be filed as an explicit ladder amendment in `decision.md`, not adopted implicitly.

### 2. Falsifiability — score_suggestion: 3
Objection: the spike runs in seconds, but nothing at stake can fail.
- **It passes by construction.** It uses a deterministic scalar plant with exact zero-order-hold integration, and the candidate gain is far inside the stable region. Measured candidate peak: 0.00609 against a 0.01 bound, about 40% margin.
- **Checks 2 and 5 are vacuous.**
  - Check 2: the oracle sets u = −200x − d, cancels the disturbance exactly, and has a measured peak of 0.0.
  - Check 5: every phase, delay and sample instant lies on both grids, so the peaks differ by 8.7e-18.
- **Checks 3 and 4 only test the integrator.** The phase-0 50 Hz arm samples at t = 0, before the disturbance has had any effect. It is therefore open-loop for 20 ms by construction, so these checks verify the integrator, not the bound.
- **No condition sits near L*.** Nothing tests effective response latency between about 5 ms and 20 ms. The one quantitative claim (9.53 ms is the deadline) is never stressed from either side.
- **The program-level hypothesis is untested.** "S0a is the right first lock for the target plant" has no falsifier that runs within days. The proposal itself states that scalar results do not transfer.

### 3. Evidence demand — score_suggestion: 4
Pass for the spike, which needs near-zero compute. Objection: the evidence that would actually decide whether S0a is the right first lock is left unspecified and is not small. That evidence is an identified disturbance set, a tolerance, and an end-to-end sensor-to-actuator latency budget for the target plant (or a credible multi-body sim). The proposal should state at least the order of magnitude of that follow-on demand.

### 4. Failure modes — score_suggestion: 3
The listed failure modes are good (artificial envelope, unmodeled coupling, mistaking nominal rate for latency, overcorrection, redundant controller, stale requests). Two dominant failure modes are missing or understated:
- **The envelope-specification problem.** Choosing D and b for the target plant is the hard, unsolved part, and the proposal does not say who supplies those numbers or how. Without that, S0a cannot be certified on any real body.
- **The vacuous-gate outcome.** Existing kHz joint current and PD firmware may already satisfy any reasonable S0a. B's mitigation ("certify and reuse") then means the first locked packet yields almost no research information. That directly weakens its claim to be the first mainline packet.

### 5. Integrability — score_suggestion: 4
Mostly a pass. Ownership is clean: the body loop exclusively owns deadline-critical correction, the Scene Graph owns persistent relations, the Life Core is slow and never deadline-critical, and simulator ground truth is evaluator-only. Objections:
- **Envelope ownership is unassigned.** The policy "requests an envelope ID", but no owner is named for authoring, versioning and approving envelopes (Life Core? a human gate? the body loop?).
- **"Constraint margin where justified" is undefined.** It is the one upward signal likely to need contact or support information, which sits awkwardly with "S0a exports no mandatory contact latent".

### 6. Latency / criticality class — score_suggestion: 3
The tiers are placed correctly (body ≥200 Hz class, policy about 50 Hz, Life Core 1–5 Hz), and the rate-versus-latency distinction is handled well. The objection is about the fixture:
- **The parameter a = 10 s⁻¹ makes the deadline look tighter than it is for balance.** For an inverted pendulum, a = √(g/l), and a = 10 s⁻¹ corresponds to l ≈ 0.1 m. A humanoid centre of mass near 0.8–1 m gives a ≈ 3.3 s⁻¹. With comparable relative tolerance, that implies a much longer L*, potentially compatible with a 50 Hz loop.
- **The urgent tier then needs a different source.** If it exists, it must come from other modes (joint-level impacts, foot-strike transients, actuator saturation), and the proposal does not identify which.
- **The 1 kHz acquisition and 250 Hz targets are therefore unsupported by B's own argument.** They should be marked as placeholders until a mode-specific L* is computed.

### 7. Complexity cost — score_suggestion: 4
Pass. The spike is minimal. Mild objection: the interface spec introduces envelope IDs, reference expiry, a three-state validity flag, versioning, and fallback semantics before any envelope has been measured. Some of this belongs in S0b or should be deferred.

### 8. Reversibility — score_suggestion: 5
Pass. No learned representation or Scene Graph schema depends on the scalar implementation. Abandoning it costs a contract file and logs.

### 9. Necessity discipline (Appendix B) — score_suggestion: 4
Strong overall. Grades are explicit, Grade 3 (B-N4) is quarantined, sufficiency and necessity are separated, and B correctly says the spike cannot promote B-N1. Objections:
- **B-N1 does not answer brief question 1.** B-N1 is a valid narrow Grade-1 claim, but it is close to the textbook pure-delay or indistinguishability bound. Its premise ("identical applied control until L") is exactly the information restriction that feedback removes. B concedes that the ordering argument "does not prove that research on S1 or S2 must wait". The answer to "why this stage first, in necessity terms" therefore rests on acceptance-gate logic, not necessity. `decision.md` should say this explicitly.
- **B-N2 risks being unfalsifiable.** Its disjunction "timely disturbance-dependent correction **or** an equivalent physical mechanism" can absorb any counterexample. "Equivalent" needs a definition that does not depend on the outcome; otherwise B-N2 should be downgraded to a design heuristic.
- **The actuator bound plays no role.** |u| ≤ 3 is stated as a premise, but the proof never uses it and the spike never reaches it (max |u| = 1.17). That is harmless but misleading: it suggests the claim covers authority limits, which it does not.

### 10. Stackability — score_suggestion: 3
Objection: B claims that S0a "does not require identifying contact state" and that "no later stage may silently enlarge the certified operating envelope". For a legged body, the set of tolerable disturbances and the correction obligation change with support configuration (single versus double stance, unilateral contact, friction cone). As a result:
- **Either S0a must be re-certified per contact mode**, which imports S2-like distinguishability into S0a,
- **or S1 locomotion is blocked by the no-enlargement rule**, because every gait transition changes the envelope.

The stackability table does not address this. Separately, the S3–S7 rows are reasonable and do not require later stages prematurely.

## Fatal risks (if any)

No fatal risk to the proposal's internal validity was found: the math is correct and the script runs and passes as specified. One risk is close to fatal for its claim to be the *first mainline packet*. If the envelope is undefined for the target plant (risk 4) and contact-dependent (risk 10), S0a cannot actually be certified on the target body without S1/S2-level information. The gate would then be either vacuous (certify existing firmware) or circular (it needs contact state it disclaims). Adjudication should not lock B as mainline until this is answered.

## What would need to change for Recommend

1. **Make the spike discriminating.**
   - Add a pre-registered sweep of effective response latency across L* (for example 2–20 ms) for the two-world indistinguishable pair. Pass requires a violation above L* and envelope satisfaction for some controller below it, within a stated tolerance.
   - Drop or replace the vacuous checks (oracle exact cancellation, on-grid resolution check) with checks that can fail, such as off-grid onsets, sensor noise, and actuator lag.
2. **Re-derive the deadline for at least one physically plausible humanoid mode** (for example a CoM-height LIP with a stated push set and tolerance, plus one fast joint-level mode). State which mode actually needs the ≥200 Hz tier. Mark the rate targets as placeholders until then.
3. **Address contact-mode dependence of the envelope explicitly.** Either define envelopes per support mode and state how S1 transitions are admitted without violating the no-enlargement rule, or narrow S0a's scope (for example a fixed-support or joint-level envelope) and say so.
4. **Name an owner and approval path for envelope definitions and versions.**
5. **Tighten B-N2** with a non-circular definition of "equivalent physical mechanism", or downgrade it.
6. **State in the proposal that S0a-first is justified as an acceptance gate**, not as necessity-ordered research. Also state what research information the packet yields if existing firmware already satisfies it.
