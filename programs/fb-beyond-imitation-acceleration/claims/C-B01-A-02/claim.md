# Claim C-B01-A-02

- **Author**: Author A (Claude Opus)
- **Packet**: `B01`
- **State & Grade**: Grade 1 (Candidate)
- **Conclusion Shape**: Impossibility and Invariant
- **Premises**: Exact rank-d FB fixed point with Sigma_B > 0 and linear single-frame prompt map z = A B(g) under spherical normalization ||B(x)||_2 = sqrt(d).
- **Conclusion**: For raw prompt encoding A = I, worst-case goal misidentification angle between B(g) and argmax_{||u||=sqrt(d)} u^T Sigma_B^{-1} B(g) is arccos(2 sqrt(kappa)/(1 + kappa)) > 0 whenever kappa > 1. Inverse whitening A = Sigma_B^{-1} worsens this to arccos(2 kappa / (1 + kappa^2)). Embedding-matching self-identification k_I(y,g) = B(y)^T B(g) requires Sigma-colouring A = c Sigma_B.
- **Falsifier**: An SPD Sigma_B with kappa > 1 for which A = I yields zero misidentification angle across all unit eigenvectors.
