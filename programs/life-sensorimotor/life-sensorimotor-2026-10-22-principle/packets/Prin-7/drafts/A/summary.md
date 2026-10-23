# Draft A summary — Prin-7 (C-P1-012 Grade-1 identifiability upgrade attempt, PLAN only)

**Author:** A (Claude Opus). Full proposal: `../../proposals/A.md`. No execution; grade stays **2, Candidate**; B.9.6 count 1; no Eng-2 gate change.

## Thesis (one paragraph)
At the joint level, unmodeled actuator effort and contact torque enter through the **same channel**. From `(q, q̇, τ_cmd)` one can recover only their sum (Lemma L0). Any identifiability therefore comes from **model-class priors**, and an oversized nuisance class makes "impossibility" trivially true: a built-in conclusion, and the formal version of the Prin-6 P-1 (iv) vacuity flag. The PLAN therefore spends most of its effort on the **admissible model class**, frozen before any proof work. It sets a **two-sided** target: detection is impossible without the effort measurement **and** possible with it. Downstream-of-sensing friction is mandatory (H3). A cross-family refuter battery is predeclared.

## Pieces
| Piece | Content |
|---|---|
| `K` schema | Plant, sampling, permitted signals `Π` (and `Π+m`), nuisance `U↑ ⊕ U↓` as hidden-state mechanism families with sourced envelopes, contact class (all `d ≥ 10 ms`), symbolic Spec, and a worst-case or Bayesian quantifier |
| Admissibility AD-1..AD-9 | Physical sourcing independent of `C`; placement declared, with `U↓ ≠ ∅` in some variant; realizable witnesses; two-sidedness; all-detector quantifier; full class coverage; added premises pre-ruled for B.9.6; no export or rate mandate; hash-freeze |
| Variants | K-1J, K-1J↓, K-2L, K-2L↓, K-nD |
| Targets | L0 channel coincidence; **T-E** (two-sided separation plus an explicit envelope condition, which is the real content); T-R rate floor (secondary) |
| Refuter RF-1..RF-8 | Cross-joint kinematic structure; state-repeat consistency; onset rate; adaptive identification; placement (m does not help); vacuity audit; sampling; premise-6 side channel |
| Routing O-1..O-7 | Uses Prin-6 N/AN/AM/CR. A proof → B.9.2 check → its own grade packet plus signature. `m` does not help → CR, and any restatement is +1. Subclass-only → proposed AM (default counted). Admitted refuter → formal counter-model audit → CR. Budget out → unresolved/AN |

## Non-claims
No proof, refuter round, numeric check or spike is executed. No PLAN is sealed. No grade movement; no lock, recommended-for-lock or retire-nominate. The registered factorial falsifier is untouched. No export field, sensor, rate or order is mandated. No named products or companies.

## Open weaknesses
Worst-case pessimism. Envelope sourcing is a judgment call. K-nD may be out of reach. The AD-7 pre-ruling may consume the narrowing budget. The Impossibility half may rest entirely on hysteretic nuisance, which turns the claim into a premise-match question about the target.
