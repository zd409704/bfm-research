# C-Prin2-E07 — Edge S0a → S2 (contact-aware interaction)

| Field | Value |
|---|---|
| **Edge** | S0a → S2 |
| **Author family** | Opus (Prin-2 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family) |
| **Grade** | **Reading A: Grade 1 conditional, fixture-scoped, restricted to *externally initiated* contact disturbances** (author derivation; unverified). **Reading P: Grade 3, quarantined.** |
| **State** | Candidate |
| **B.9.6 narrowing counter** | 0. The restriction to externally initiated contacts is part of the *original* scope, not a later narrowing. |
| **Recommended adjudicator action** | Candidate-stay (Reading A). quarantine-Grade3 (Reading P). |

Stage meanings: Author-A W-defs (`proposals/A.md` §1).

## Premises

1. Fixture plant as in C-Prin2-E03 premise 1, scalar mode, any real `a`.
2. S2 competence (W-def) must keep the body envelope while non-support contacts apply wrenches. The contact wrench projected on the mode is a disturbance `d ∈ {+D, −D}` with arbitrary onset.
3. **Externally initiated contact.** Contacts are initiated by the environment, for example a human push or an unexpected obstacle. Before the body's sensing reveals the contact, nothing available to the controller distinguishes `+D` from `−D`. That includes upper-layer commands and efference copies. This is C-P1-001 premise 4 applied to contact.
4. The S2 decision/policy tier's world-dependent applied input has a worst-case common-input interval `L_S2 ≥ T_S2 + δ`. Here `T_S2` is that tier's update period. Any faster channel counts as an S0a realization (C-P1-002 premise 4).

## Derivation

Identical to C-Prin2-E03: `L ≤ L*(a) = ln(1+ab/D)/a`. Independent check required.

## Conclusion shape — Reading A (conditional lower bound)

Under premises 1–4, if `T_S2 + δ > L*(a)`, any S2-competent system must have available a corrective channel responding within `L*(a)`. That is S0a's bounded-response property. The S2 tier alone cannot supply it. The bound is implementation-independent within C-P1-001 premise 4.

## Why self-initiated contact is excluded

When the body itself commands motion into a contact, its commands and efference copies are correlated with the contact wrench. This is the C-P1-011 premise 3 side channel. A predictive controller can then differentiate its input *before* onset, so premise 3 fails. The edge then has no Grade-1 force for that contact class. Its residual (unpredicted) part may still qualify, but only with a separately declared residual-disturbance set. This is a substantive limit: much of planned manipulation is self-initiated.

## Reading P (quarantined)

Nothing here orders acquisition. S2 could be developed on a supported base and paired with S0a later. Citation-ablation of the S0-first narrative leaves no order argument → **Grade 3**.

## Citation-ablation (B.8.7)

Reading A uses no biological citation. **Survives.** Reading P **collapses**.

## Scope

Scalar fixture. Externally initiated contacts. Floating-base S2 only. A supported or fixed base, or a stable mode with `D/|a| ≤ b`, takes the plant out of premise 1. Target-plant premise match is open: `a`, `b`, `D` (contact-class magnitude), `T_S2`, `δ`, per support mode.

## Falsifier / challenge mode

Either of the following would refute the claim:
- an admissible common-input pair keeping both worlds in the envelope for `L > L*`;
- an error in the derivation.

Each of the following is a premise failure, not a refutation:
- contacts shown to be predictable from available signals before onset (premise 3 fails);
- a target mode with passive sufficiency;
- an S2 tier with `T_S2 + δ ≤ L*` (the edge is then non-distinct).

## Counterexample-search spike registered?

**No.** It shares C-Prin2-E03's PLAN. The disturbance set is reinterpreted as contact wrench and adds a predictable-onset arm. That arm is expected to "succeed" and must be filed as a premise-3 failure, not a counterexample.
