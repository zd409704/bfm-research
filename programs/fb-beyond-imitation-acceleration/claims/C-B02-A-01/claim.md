# Claim C-B02-A-01

- **Author**: Author A (Claude Opus)
- **Packet**: `B02`
- **State & Grade**: Grade 1 (Candidate)
- **Conclusion Shape**: Invariant and Obligation
- **Premises**: Macro critic target g(tau) = R^{(k)} + gamma^k (1 - d) V_bar(H_{t+k}), stationary environment transition given action-observation history, macro actions drawn from pi_theta(.|o,z) with z held fixed, B_omega entering rollout only at boundary selection.
- **Conclusion**: (a) Conditional staleness bias b_Delta(H,z) of a stored macro row with executed label z is independent of (omega_{t-Delta}, omega_t) and depends on theta only through p_theta(tau|H,z). (b) |b_Delta| <= min(span(g) sqrt(KL_Delta / 2), sqrt(Var_then(g) chi^2_Delta)). (c) When theta_{t-Delta} = theta_t, keeping zeta = z_actual has zero bias while re-encoding zeta = B_{omega_t}(m) introduces bias whenever T_theta Q(H, .) is non-constant along the drift arc.
- **Falsifier**: A system satisfying P1-P5 where re-encoding stored macro labels through drifted B_omega has smaller bias than keeping z_actual when pi_theta is fixed.
