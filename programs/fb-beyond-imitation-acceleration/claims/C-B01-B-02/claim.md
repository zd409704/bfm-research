# Claim C-B01-B-02

- **Author**: Author B (Codex gpt-6-astra)
- **Packet**: `B01`
- **State & Grade**: Grade 1 (Candidate)
- **Conclusion Shape**: Impossibility (Nullspace Non-Identifiability)
- **Premises**: Replay measure rho with rank(Sigma_B) = r < d, where F is constrained solely by inner products with replay-supported B(x).
- **Conclusion**: Full readout F(s,a,z)^T z is non-identifiable for any command z with a non-zero component in ker(Sigma_B); only the support projection P z = Sigma_B Sigma_B^+ z is identifiable from replay density fitting, and no Tikhonov damping coefficient lambda_reg > 0 recovers unobserved nullspace dynamics.
- **Falsifier**: A replay-only estimator that distinguishes F from F + t n (n in ker(Sigma_B)) while all replay inner products F^T B(x) remain identical.
