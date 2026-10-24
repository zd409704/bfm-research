# B01 Synthesis — Causal Privileged Forward Inputs for LOCAL_RESPONSE_ASYM_FB_V3

## Engineering Norm to Merge

1. **Sanitize `p_5065` before every forward critic call**:
   - Exogenous open-loop generator Markov state `ξ_t` (timers, modes, open-loop envelopes) may enter `F`.
   - Endogenous post-action reaction/contact windows at `t+1..t+K` must be replaced by causal carriers (lagged impulses, past-reaction mirrors, or masked slots)—never by realized future forces correlated with `a_t`.
2. **Collector contract**: Every retained privileged field must have `sample_time ≤ action_latch_time`. Fail closed (mask + freeze normalizer) when provenance fails; do not repair by shifting timestamps or imputing future means.
3. **Actor gradient hygiene**: Prefer counterfactual evaluation where `p` is held at pre-action causal state while `a` varies. Stop-gradient on future windows does **not** restore causality if those windows remain in the input.
4. **Gate G-1**: Use composed sensitivity `‖J_fut Y_a‖₂ / ‖J_a‖₂`; large raw future Jacobians alone do not prove degeneracy.

## Relation to Charter H1

Causal sanitization is adopted as a hard training contract. Explained-variance retention vs leaked `p` remains an empirical H1 check on factual panels; actor-query counterfactual panels are the decisive Bellman-consistency test.
