# Claim C-B03-A-01

- **Author**: Author A (Claude Opus)
- **Packet**: `B03`
- **State & Grade**: Grade 1 (Candidate, tighten-premises)
- **Conclusion Shape**: Impossibility / Lower Bound
- **Premises**: Single-frame kinematic backward map B(m), non-empty torque-projected feasible contact nullspace N_tau along equal future kinematic occupancy Psi^{c1}=Psi^{c2}, and indistinguishable actor input U_t=(o_low, z_t).
- **Conclusion**: Any deterministic low-level policy pi_theta(U_t) suffers an irreducible Bayes action MSE lower bound E||pi_theta(U_t)-a*||^2 >= E tr Cov(A*|U_t), and FB actor gradients are orthogonal to K_p^{-1} N_tau on equal-occupancy branches.
- **Falsifier**: A deterministic policy taking only (o_low, z_t) that achieves action MSE strictly below E tr Cov(A*|U_t) across paired equal-occupancy contact regimes.
