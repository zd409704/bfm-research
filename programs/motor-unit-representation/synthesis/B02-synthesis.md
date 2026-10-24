# B02 Synthesis — E0–E4 Sync, Rule Calibration, Coverage Gates

## Engineering Norm to Merge

1. **Single source-of-truth episode program**: `make_program(run_seed, config_id, scene, n, domain, variant)` with Philox keys; every E3 episode guarantees a ≥25-step sustained-load window; every E4 episode guarantees a load-release edge and ≥20-step recovery. E4-R / E4-RI must have distinct keys.
2. **Deterministic load-sign coverage**: Alternate `σ` in training; enforce `|τ_ext| ≥ 0.25 S_max` and `|u*| ≤ 0.92` or flag `INFEASIBLE_CONFIG`. Never train a single sign and evaluate the opposite as in-distribution.
3. **Rule law**: Inertia-scaled PD + bias + anti-windup with explicit `J_nom`; delayed feedforward in E3 (`κ=1` on `τ_ext,t−1`); `κ=0` in E4 so recovery is a true integrator transient. Lag privileged load knowledge at release edges.
4. **Joint 720-cell gate**: Track `configuration × scene` as a hard fail-closed array. Marginals are insufficient. De-synchronize sub-cases across configs; require a `λ=0.92` rule witness per config.
5. **BN + saturation**: Dual-partition BN without rule/policy covariate shift; pre-activation hinge / direct logit path mandatory — action-space TD gradients alone die under `sech²` saturation.
6. **Static-hold panel**: Canonical zero-vel/acc `g_hold`; both signs; position+contact guards; evaluator negative control and rule positive control; `CONTROL_FAIL` separate from physical infeasibility.

## Relation to Charter / Audit Issues

Closes Audit Issues #1, #2, #3, #5, #6, #8 as engineering contracts. `coverage_ready=true` is a necessary readiness gate, not a convergence claim (Charter B4). Inherited causal `p_5065` contract from `D-B01-001` remains binding for any privileged fields the rule or collector reads.
