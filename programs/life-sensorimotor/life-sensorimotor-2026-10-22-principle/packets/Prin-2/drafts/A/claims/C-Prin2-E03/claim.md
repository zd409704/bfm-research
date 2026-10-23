# C-Prin2-E03 — Edge S0a → S1 (availability reading)

| Field | Value |
|---|---|
| **Edge** | S0a → S1 |
| **Author family** | Opus (Prin-2 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family; not this author) |
| **Grade** | **Reading A: Grade 1, conditional, fixture-scoped** (author derivation; unverified). Companion Grade 2 via C-P1-002. **Reading P: Grade 3, quarantined.** |
| **State** | Candidate. No lock is proposed now. |
| **B.9.6 narrowing counter** | 0 |
| **Recommended adjudicator action** | Candidate-stay (Reading A). quarantine-Grade3 (Reading P). Nominate for lock only after the conditions in §"Lock path" are met. |

Stage meanings: Author-A W-defs (`proposals/A.md` §1). S1 is the policy tier at period `T_R2`.

## Premises

1. **Plant (fixture).** A scalar mode `ẋ = a x + u + d`, `x(0)=0`, with envelope `|x| ≤ b` that must hold robustly in both worlds (C-P1-001 premises 1, 2, 5). Here `a` may be any real value. C-P1-001 fixes `a = 10 s⁻¹`. This record extends the derivation to general `a`. The extension is flagged as an author derivation.
2. **Hidden disturbance.** `d ∈ {+D, −D}` is constant from onset `t₀`. The onset `t₀` is arbitrary, possibly off the policy sample grid. Before any world-dependent applied input, both worlds receive identical input (C-P1-001 premise 4).
3. **S1 competence includes S0a's envelope.** S1 competence (W-def) is required to hold *while* the declared hidden disturbances occur. **This is a premise about the S1 specification, not a derived fact.** If S1 is specified only for undisturbed conditions, the claim does not apply.
4. **S1 loop timing.** An implementation whose world-dependent applied input comes *only* from the policy loop has a common-input interval `L_S1`. For a robust guarantee over all onsets, the worst case is `sup L_S1 ≥ T_R2 + δ`, where `δ ≥ 0` is transport plus compute delay. The reason is that an onset just after a sample is not seen until the next sample.
5. "Channel" means any source of world-dependent corrective force: an active loop at any rate, embedded actuator feedback, or state-dependent passive mechanics (C-P1-002 premise 4). Passive mechanics that change `a` change premise 1 and require recomputing `L*`.

## Derivation (author; requires independent check per B.9.2)

Let `Δ = x₊ − x₋`. On the common-input interval, `Δ̇ = aΔ + 2D` and `Δ(t₀) = 0`. So `Δ(t₀+L) = (2D/a)(e^{aL} − 1)` for `a ≠ 0`, and `Δ(t₀+L) = 2DL` for `a = 0`. Both trajectories stay in the envelope only if `Δ ≤ 2b`. That gives

`L ≤ L*(a) = ln(1 + a b / D) / a` (with `L*(0) = b/D`, and `L* = ∞` if `a b / D ≤ −1`).

With C-P1-001's `b = 0.01` and `D = 1`: `L*(10) = 9.53 ms`, `L*(3.3) = 9.84 ms`, `L*(0) = 10.0 ms`. For `|a| b/D ≪ 1`, `L* ≈ b/D`. **The bound is set mainly by the envelope-to-disturbance ratio, not by the instability rate.** It disappears only for a stable mode with `D/|a| ≤ b`, meaning passive dynamics alone keep the state inside the envelope. Premise 1 must exclude that case for the edge to have force.

## Conclusion shape — Reading A (lower bound, conditional)

Under premises 1–5, if `T_R2 + δ > L*(a)`, then **any system with S1 competence must have available a channel whose world-dependent corrective input begins within `L*(a)` of disturbance onset. The S1 policy loop alone cannot supply that channel.** This is S0a's bounded-response property, available to S1 at runtime.

At `T_R2 = 20 ms` the fixture condition holds for every `a` listed above. The conclusion is implementation-independent across classical, learned, predictive and randomized controllers whose applied inputs are identical in both worlds until `L` (C-P1-001 premise 4).

**What it does NOT say:**
- It does not say S0a is a separate module, processor or process.
- It does not say S0a must be engineered, trained or acquired first (Reading P).
- It does not say an active controller is needed. Passive mechanics or embedded feedback can realize the property (C-P1-002).

If the policy loop itself is run with `sup L_S1 ≤ L*`, the property is still required, but the policy loop may realize it. In that case the edge reduces to "the property is available", not "a distinct stage".

**Programmatic content:** under premise 3, a single policy at `T_R2 > L*` with no faster channel is excluded from robust S1 competence. That is the strongest statement this record can support.

## Grade-2 companion (via C-P1-002)

If C-P1-002's incompatible-history premise 3 holds for an S1 support mode, then S1 competence requires the C-P1-002 role: timely world-dependent corrective force histories. The operational absence test is C-P1-002's: replay or intervene to remove the differentiating response, then check whether the total corrective histories stay indistinguishable through the required window. This companion is Grade 2 Candidate only, and it inherits C-P1-002's open issues (tighten-premises, no target premise match, no failed counterexample search).

## Reading P (quarantined)

"S0a must be built or acquired before S1." No information, stability or resource argument here bears on acquisition order. Two examples:
- S1 could be trained in simulation first and the fast channel added later.
- Both could be co-designed.

The only support for an order is the evolutionary S0-first narrative (C-P1-003) and D-P1-001. **Citation-ablation removes the first, and B.8.3 forbids the second → Grade 3.** A hardware-safety rationale ("do not run disturbed S1 trials on hardware without envelope protection") is an engineering-risk planning argument. It is admissible as a planning reason, but it is not necessity evidence (B.8.6).

## Citation-ablation (B.8.7)

Reading A uses no evolutionary, developmental or anatomical premise. Deleting all such citations leaves the derivation intact. **Reading A survives.** Reading P collapses (above).

## Scope

The scalar fixture plus the S1 W-def only. Target-plant transfer requires measured or specified `a`, `b`, `D`, `T_R2`, `δ` and support mode per mode. That is the same premise-match debt as C-P1-001 and C-P1-002. Multi-DoF coupling, actuator saturation (C-P1-001 premise 6 not used) and stochastic or expected-cost objectives are out of scope.

## Falsifier / challenge mode

- **In premises:** an admissible common applied-input history keeping both worlds inside `|x| ≤ b` for some `L > L*(a)`, or an error in the general-`a` derivation. Either one refutes the claim.
- **Premise failure (B.9.4b):** S1 is ratified as an undisturbed-only competence (premise 3 fails). Or the target mode has `D/|a| ≤ b` with `a < 0`, so passive stability suffices. Or the target policy already runs with `sup L_S1 ≤ L*`, in which case the edge is non-distinct.
- A successful S1 run with a fast channel is sufficiency evidence only.

## Lock path (not nominated now)

The narrow fixture form becomes eligible for a recommended-for-lock nomination only after all three of the following:
1. C-P1-001 passes its B.9.2 independent check.
2. The general-`a` extension is independently checked.
3. The human lead ratifies an S1 definition that includes premise 3.

Even then, it is a fixture statement. Target-plant force needs the premise match.

## Counterexample-search spike registered?

**No (PLAN proposed).** One-line PLAN: for `a ∈ {−5, 0, 3.3, 10}` s⁻¹, `b/D ∈ {0.005, 0.01, 0.02}` and off-grid onsets, optimize paired common-input histories on `[t₀, t₀+L)` for `L` from `0.8·L*` to `1.5·L*`, with preregistered numerical error bounds. A counterexample is any verified dual-envelope satisfaction with `L > L*(a)·(1+ε_num)`. The runner files data only (B.9.8).
