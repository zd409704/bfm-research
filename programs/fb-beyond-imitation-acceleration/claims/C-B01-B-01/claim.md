# Claim C-B01-B-01

- **Author**: Author B (Codex gpt-6-astra)
- **Packet**: `B01`
- **State & Grade**: Grade 1 (Candidate)
- **Conclusion Shape**: Invariant and Obligation
- **Premises**: Finite outcome space with rho(x) > 0, SPD Sigma = E_rho[B B^T], exact density factorization, linear per-step reward r_z(x) = B(x)^T a_z, and spanning F(s,a,z).
- **Conclusion**: E_rho[B(x) r_z(x)] = z (and discounted return equals F(s,a,z)^T z across spanning states) iff a_z = Sigma^{-1} z. Raw coefficients a_z = z hold for all z iff Sigma = I.
- **Falsifier**: An SPD Gram matrix and command z where a_z != Sigma^{-1} z satisfies all spanning value equalities.
