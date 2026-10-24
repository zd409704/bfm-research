# Claim C-B01-A-01

- **Author**: Author A (Claude Opus)
- **Packet**: `B01`
- **State & Grade**: Grade 1 (Candidate)
- **Conclusion Shape**: Invariant / Obligation and Lower Bound
- **Premises**: P1: Exact rank-d FB fixed point for policy pi_z on fixed replay distribution rho. P2: Sigma_B > 0. P3: {F(s,a,z): (s,a)} spans R^d. P4: Linear per-step intrinsic reward r_M(y) = B(y)^T M z.
- **Conclusion**: (a) E_{pi_z}[sum_t gamma^t r_M(s_{t+1})] = F(s,a,z)^T z for all (s,a,z) iff M = Sigma_B^{-1}. (b) For any scalar c > 0 (M = c I), worst-case relative value discrepancy is at least (kappa - 1)/(kappa + 1). (c) Splicing an H-step head with M != Sigma_B^{-1} onto an F^T z tail introduces non-zero Bellman splice bias Psi_H^T (Sigma_B M - I) Sigma_B^{-1} z.
- **Falsifier**: An SPD Sigma_B with kappa > 1 and a scalar c > 0 where M = c I satisfies exact value identity across spanning F(s,a,z).
