# Prin-8 Author A — summary

**Author:** Claude Opus (Author A). Isolated; B's draft was not seen. Full text is in `proposals/A.md`.

**Deliverable:** premise-match templates for C-P1-002 (T-002) and C-P1-010 (T-010). Design only: no execution, no spike, no fill with target values.

**Core structure**
- **Field statuses:** UNDECLARED → OWNED → SPECIFIED / DERIVED → MEASURED, plus NOT-APPLICABLE and CONTESTED. Updates are append-only.
- **Phases:** Phase 0 (now) allows only PENDING / SCOPE-EXIT / CIRCULARITY-FLAG verdicts, never MATCH or FAIL. When the human lead declares a measurement point, each instance is version-frozen and becomes the PLAN. Phase 1 (a separate packet) fills MEASURED fields. The runner does not change claim state.
- **Scope exits** are neither counterexamples nor B.9.6 narrowings. Post-value changes to premises, sets or tolerances are logged as candidate B.9.6 events for the adjudicator.
- **T-002:** one instance per (plant config, support mode, disturbance pair). It has rows for premises 1a–1f, 2, 3, 4, 5a and 5b. Realization and absence fields are carried: Δ_req, ε_F/δ_t resolution rule, interventions, and passive / embedded / active classes. Guards: G-1 (incompatibility from failure), G-2 (envelope from capability), G-3 (success ≠ realization), G-4 (evolution), G-5 (scalar fixture ≠ target match).
- **T-010:** one instance per (plant config, joint, rendering loop). Part A rows (premises 1–5) test in-class membership; they do not test the theorem. Part B rows (premises 6–8) cover `b_j`, `K_req,j`, physical compliance and `T_R2`, with an uncertainty-banded comparison: applies / retire trigger / unresolved. Guards: G-6 (gain circularity), G-7 (H1 stretch), G-8 (H2 dichotomy), G-9 (sanity spike ≠ match), G-10 (no ordering / Eng-2 use).
- **Routing:** outcomes go to the claim adjudicator (Opus for C-P1-002, Astra for C-P1-010) as B.9.4(a)/(b) evidence. The templates decide no transition themselves.

**Disclosed:** same-family authorship on C-P1-010. Three [A-choice] negligibility thresholds (A1a coupling, A2b delay, A2c quantization) are declare-at-freeze fields and are flagged for the adjudicator to accept or strike.

**Unchanged:** C-P1-002 Grade 2 Candidate; C-P1-010 Part A Grade 1 Candidate, Part B Grade 1 conditional Candidate. No change to D-P1-001, D-Prin-3-001, D-Eng-2-001 or Eng-2 gates. No Locked Grade-1. No named products or companies.
