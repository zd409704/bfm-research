# B04 Synthesis — Hierarchical Composition of Frozen Local Motor Units

## Engineering Norm to Merge

1. **`LIMB2-v1` hybrid plant**: Keep A's verified `LIMB2-REF` geometry, pelvis-mounted sustained payload, and terminal-joint housing-transport / null-mode lemmas. Merge B's Schur-complement reduction, free-flight `G−ga≡0` identity, and intervention-based (not Class-X exogenous) coupling partition.
2. **Blocking feasibility before learning**: Inverse-dynamics demand over admissible contact forces; `FEASIBLE` iff ≤`0.92` (publish reserve); else `INFEASIBLE_CONFIG`. Pre-register `IN`/`EDGE`/`OUT` from controller-independent probes — never from the evaluated arm's own slip / force drift.
3. **Fair Modes A/B/C**: Frozen local `(B,π)` reuse; identical proprioceptive history / `50 Hz` / update budget; `140k` masked upper parameters; smooth `Kc` Mode-B adapter (no primary discontinuous `Pκ`); spherical entropy / exploration calibration for Mode A; `A-rand`/`C-PD`/`C-big` controls; rail `(y,ẏ)` in upper obs only.
4. **Coverage diagnostics, not over-claims**: Five-code evaluator (`A-AMP`…`A-NULL`) is Grade-2 diagnostic. Amplitude inclusion alone does not certify H4 coverage; quantify coupling at task operating points vs `S_max` / E3 `0.92`.
5. **Comparative morphology transfer**: Bounded `ΔS_ZS` + positive skill `R̃`; paired contrast vs Baseline C with worst-cell floor; clean `3×3` `L2×C02` grid (`C01` fixed) plus labeled stress panel; recalibrated joint-support / TOST gates.
6. **Numerical completeness**: float64 semi-implicit Euler `0.25 ms` + halving gate; stateful stiction contact; `FROZEN_HASH`; separate spec closure from scientific H4 evidence.

## Relation to Charter / Audit Issues

Closes Audit Issue #9 as an engineering composition contract (`LIMB2-v1` hybrid). Charter H4 (composition accelerates multi-joint control under coupled loads) remains Candidate until Stage-2 learning curves run after merges. Inherited causal `p_5065` (`D-B01-001`), E0–E4 coverage (`D-B02-001`), and rank-16 / nondim capacity (`D-B03-001`) remain binding for any frozen units composed downstream.
