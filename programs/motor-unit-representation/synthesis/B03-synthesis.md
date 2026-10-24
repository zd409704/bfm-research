# B03 Synthesis — Rank-16 Capacity Across 144 Morphology Regimes

## Engineering Norm to Merge

1. **Configuration-matched FB reference**: Draw negative / measure-term samples from the same morphology-stroke configuration as the anchor. Do not rely on pooled HS reference alone; under disjoint tip-radius shells a pooled right-span floor can dominate any shared rank-16 `B`.
2. **Rank-floor orthonormalization, not blind Σ→I**: Per-configuration PR / erank hinge (target ≥12–13/16). Prefer subspace-orthogonal isotropy if a linear λ-anchor is retained. Global mini-batch `L_orth` alone is insufficient (vacuous at π_k=1/144).
3. **IPW with fail-closed support**: Hierarchical sampler weights + small direct target-law mixture; `INSUFFICIENT_SUPPORT` instead of silent stratum drop / biased clip renormalization.
4. **Nondimensionalize tip kinematics inside `B`**: Parameter-free invertible `T_κ` (divide tip block by ρ̂, allometric time factor, explicit λ in the dead `v_z` slot). Preserve tip/lever-arm decodability with length-relative RMSE gates. Schema guards before transform.
5. **Spike hygiene**: Common physical outcome cells; separate pooled vs matched error; hold out geometry seeds from all fitting; isolate `T_κ` from normalizer and λ-anchor ablations.

## Relation to Charter / Audit Issues

Closes Audit Issue #7 as an engineering contract (stratified capacity + nondim). Charter H3 (`<0.20` worst-group successor error) remains Candidate until the repaired spike runs on B02-integrated physics. Inherited causal `p_5065` (`D-B01-001`) and E0–E4 coverage (`D-B02-001`) remain binding.
