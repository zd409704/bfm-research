# C-P1-010 — Sampled-data passivity bound and its fast-tier corollary

| Field | Value |
|---|---|
| **ID** | C-P1-010 (inherited by ID from `inherited-ledger-P1.md`; origin A-C1, with A-C1′ folded in as Part B) |
| **Short title** | Passivity / fast-tier bound for unknown environments |
| **Author family** | Opus (P1 Proposal A). Record compiled in Prin-1 by Author A (Opus). |
| **Claim adjudicator (per roster)** | Codex gpt-6-astra high (cross-family). Not this author. |
| **Grade** | Part A: **Grade 1** (narrow formal bound). Part B: **Grade 1 conditional**, premises unverified on the target plant. |
| **State** | **Candidate** (both parts). Not Locked. A Grade-1 lock needs independent verification and the human lead's signature (B.9.2). |

## Statement

**Part A (formal core, A-C1).** Take a 1-DoF device with physical viscous damping `b > 0`. It renders a virtual spring–damper `(K, B)` through a zero-order hold at sampling period `T`. The coupled system is passive, and so is stable against any passive environment, iff `b > K·T/2 + |B|`. Equivalently, the largest passively renderable virtual stiffness is `K_max(T, b, B) = 2(b − |B|)/T`, which requires `b > |B|`. Holding `b` and `B` fixed, `K_max` scales as `1/T`. Going from `T = 1 ms` to `T = 20 ms` lowers `K_max` by a factor of 20.

**Part B (fast-tier corollary, A-C1′).** For a target-plant joint `j` with measured effective damping `b_j` and required task stiffness `K_req,j`: if `K_req,j > 2 b_j / T_R2`, where `T_R2` is the policy-rate period (about 20 ms), then a *passivity guarantee against unknown environments* at `K_req,j` cannot come from virtual stiffness rendered at `T_R2`. Some loop with a shorter period, or physical compliance, has to supply it.

## Premises (numbered, explicit)

1. Single degree of freedom. Linear time-invariant virtual impedance `F = −K x − B ẋ_d`, where `ẋ_d` is the discrete (backward-difference) velocity used in the cited result.
2. Zero-order hold on the actuator command at period `T`. Position is sampled at the same period. Position quantization is ignored and there is no extra computational or transport delay beyond the ZOH sample.
3. Physical damping `b` is linear viscous and acts in continuous time in parallel with the rendered impedance.
4. The environment (including any human or object) is passive. Nothing else is known about it.
5. Passivity of the device port is the property demanded. Stability for *some* specific environment is not the property being bounded.
6. (Part B only) Measured `b_j` per contact-critical joint, as reflected at the joint and including actuator/gear damping.
7. (Part B only) A required task stiffness `K_req,j` that is stated independently of any implementation.
8. (Part B only) The stiffness in question is *virtual* (digitally rendered). Intrinsic physical compliance (series-elastic elements, structural springs) is outside it.

## Conclusion shape

- Part A: **lower bound / impossibility.** No ZOH controller of the stated class renders `K > 2(b − |B|)/T` passively.
- Part B: **conditional lower bound on loop rate.** If premises 6–8 hold with `K_req,j > 2b_j/T_R2`, a rate faster than R2 (or physical compliance) is required for the passive guarantee.
- Part B is **not** an ordering claim. It does not say S0 must precede S1 as research. See Hygiene note H5.

## Scope

**Covers:** linear ZOH virtual impedance on a single joint of the home-humanoid / target-plant class, with passivity against unknown passive environments as the requirement.

**Does not cover:**
- Multi-DoF coupled impedance (inertial and Coriolis coupling between joints).
- Nonlinear friction (Coulomb, Stribeck, backlash), or `b` that varies with load or temperature.
- Delays beyond one ZOH sample (communication latency, filtering lag, compute time). The cited result does not cover them. Any delay-extended bound is a separate claim that needs its own source.
- Learned or nonlinear policies that output torques directly. Part A says nothing about them except where they reduce to the stated class.
- Non-passive designs that are stable for a known or restricted environment. Passivity is sufficient for coupled stability against unknown passive environments; it is not necessary for stability.
- Stiffness provided by physical compliance (premise 8).
- Any statement about locomotion balance (that is A-C6, not inherited here).

## Falsifier / challenge mode

- **Part A:** inside premises 1–5, a demonstrated violation (a passive coupled system with `K ≥ 2(b−|B|)/T`, or a non-passive one with `K < 2(b−|B|)/T`) means the derivation or the premise match is wrong. That is a challenge against the premise mapping, not an empirical refutation of the theorem. Outside premises 1–5 the claim does not apply, so a violation there is not a counterexample (B.9.4a requires the claim's stated premises).
- **Part B:** retired for joint `j` if measured `b_j` and `K_req,j` give `2b_j/T_R2 ≥ K_req,j`. It is challenged under B.9.4(b) if premise 6, 7 or 8 fails on the target plant (for example, physical compliance supplies the needed stiffness).
- Simulation reproduction of the boundary (P1 spike SA-1) is a harness sanity check only. Under B.4/B.5 it cannot promote the claim.

## Hygiene notes (from P1 decision and this review)

- **H1 — Stretch beyond cited assumptions (P1 decision rationale: "passivity stretch beyond cited assumptions").** Proposal A stated Part A correctly in its claims table (1-DoF, linear ZOH). Its necessity argument (step 1), however, generalized to "any architecture whose stiffness is rendered only by a ~50 Hz policy is either soft or non-passive in contact." That sentence extends the cited result to multi-DoF humanoid joints, nonlinear friction, extra delay and nonlinear learned policies. None of these are in the cited premises. The general sentence is **not** part of this claim. Only Parts A and B, with premises 1–8, are.
- **H2 — "Soft or non-passive" is a false dichotomy as stated.** A third option, "stable but not passive (no guarantee against unknown environments)", exists and is admissible. Proposal A acknowledged this in its non-claim 3. The record keeps the conclusion to *passivity guarantees* (premise 5).
- **H3 — Unused or unverified premises.** Part B depends on `b_j` and `K_req,j`. Neither has been measured or specified for the target plant. Until they are, Part B has no force on any route (Candidate cannot veto under B.4 in any case). `K_req,j` must come from task requirements, not from an existing controller's gains, or the argument is circular.
- **H4 — SA-1 runtime infeasible as written (P1 decision).** The A spike grid, with 200 ω points down to 0.01 rad/s, at least 50 periods each and `dt = T/200`, implies simulated spans on the order of 10⁴ s at microsecond steps per cell. That cannot run within the stated ≤ 15 min CPU budget. In any case the spike is sanity only.
- **H5 — Not an ordering necessity.** Part B constrains *where impedance is rendered* (a loop-rate requirement). It does not establish that S0 work must precede S1 or S2 work. Such ladder edges belong to Prin-2 and are Grade 3 by default (B.8.2). **D-P1-001 is a Provisional S0a acceptance-gate recommendation, not a necessity ordering.** This claim must not be cited as making it one.
- **H6 — Citation ablation (B.8.7).** The claim cites no evolutionary, developmental or anatomical source (A's G3-a spinal-reflex note is not a premise). Ablation leaves the argument intact. The claim does not fall to Grade 3 by B.8.7.
- **H7 — Implementation independence (B.3.3).** Part A holds for every controller in the stated class (classical or learned) that reduces to linear ZOH impedance. It does not hold across *all* implementation families; see Scope.
- **H8 — Author/adjudicator family.** This record was compiled by an Opus author, the same family as the originating proposal. Per the roster, adjudication must be cross-family (Astra).

## Recommended adjudicator action

**tighten-premises.** Adopt premises 1–8 and the Scope exclusions above in place of the P1 wording. Separate Part A from Part B.

After tightening:
- **Part A → recommended-for-lock (narrow).** Verification route (B.9.2): match each item of premises 1–5 to the published sampled-data passivity result for a ZOH virtual wall (Colgate–Schenkel), checked by someone other than the author. Then the human lead signs. Until both happen it stays **Candidate**.
- **Part B → Candidate-stay** until `b_j` and `K_req,j` are measured or specified.

## Counterexample-search spike registered?

**Yes (sanity / premise-match only; cannot promote).**
PLAN (one line): replace the time-domain SA-1 with an exact discrete-time frequency-domain passivity check on a reduced grid (T ∈ {1, 5, 20} ms × b ∈ {0.1, 0.5, 2.0}); a "counterexample" is any in-premise cell where empirical `K_crit/(2(b−|B|)/T)` falls outside [0.95, 1.05], which flags a harness or premise-mapping error and never changes claim state (B.9.8).
