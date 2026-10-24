# Claim C-B01-A-03

- **Author**: Author A (Claude Opus)
- **Packet**: `B01`
- **State & Grade**: Grade 2 (Candidate)
- **Conclusion Shape**: Obligatory Functional Role (R-Sigma)
- **Premises**: Policy optimization splicing an H >= 1 per-step B-reward head onto an FB successor tail under non-stationary replay rho_t where kappa(Sigma_B) > 1.
- **Conclusion**: Any such hybrid architecture must realize functional role R-Sigma: a causal estimator of Sigma_{bar_B, rho_t}^{-1} action on z in the target backward coordinate frame, reducing one-step Bellman splice residual by at least 50% compared to raw B^T z when kappa >= 10.
- **Falsifier**: A hybrid architecture without explicit or implicit Gram inversion whose Bellman splice residual and policy gradient cosine match whitened readout at kappa >= 30.
