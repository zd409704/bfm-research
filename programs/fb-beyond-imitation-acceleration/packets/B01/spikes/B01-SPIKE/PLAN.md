# Pre-Registered Spike Plan: `B01-SPIKE`

**Packet**: `B01`
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Mechanism Under Test**: Causal EMA Gram covariance tracking $\widehat{\Sigma}_B$ and damped Cholesky whitening $W_\lambda = (\widehat{\Sigma}_B + \lambda_{\mathrm{reg}} I)^{-1}$ on spherical backward representations $B(x) \in \mathcal{S}^{d_z-1}(\sqrt{d_z})$ ($d_z \in \{100, 256\}$).

## 1. Metrics and Pass Thresholds
1. **Spherical Norm & Trace Invariant**: $\operatorname{tr}(\Sigma_B) = d_z \pm 10^{-2}$ while condition number $\kappa(\Sigma_B) > 10.0$ under anisotropic replay $\rho$.
2. **Zero-Shot Linear Task Readout Cancellation**: $|Q_r^{\pi_z}(s,a) - F(s,a,z)^\top z_r|_{\max} < 10^{-3}$ for $z_r = \Sigma_B \lambda$ without explicit inversion.
3. **Whitened Intrinsic Reward MSE Reduction**: $\operatorname{MSE}(r_z^{\mathrm{whitened}}, r_z^\star) < 0.15 \cdot \operatorname{MSE}(r_z^{\mathrm{unwhitened}}, r_z^\star)$ at $d_z = 256$.
4. **Single-State Goal Direction Cosine Alignment**: $\cos(W_\lambda B(g), \Sigma_B^{-1} B(g)) > 0.95$ vs unwhitened $\cos(B(g), \Sigma_B^{-1} B(g)) < 0.50$.

## 2. Execution Command & Bounds (§12.2)
- Seed: `20261023`
- Maximum attempts: `2`
- Exact command: `/srv/claude/.venv/bin/python /srv/claude/research/fb-beyond-imitation-acceleration/gpu_experiments/run_b01_gram_spike.py`
