# Brief B01: FB Density Factorization, Gram Matrix Conditioning, and Intrinsic Reward Identifiability

**Packet ID**: `B01`
**Status**: `IN_PROGRESS`
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Inherited Ledger Snapshot**: `X-BASE-001`..`X-BASE-005`
**Tie Margin**: `5.0` points out of `100.0`
**Baseline References**: `baseline/01-fb-theoretical-derivation-and-q-readout.md`, `baseline/03-model-based-acceleration-and-fb-hybrid-design.md`

---

## 1. Problem Statement

In Forward-Backward (FB) reinforcement learning, the normalized successor density $m_z(s,a,x) = M_z(s,a,x)/\rho(x)$ is approximated by $F(s,a,z)^\top B(x)$, where $B(x) \in \mathbb{R}^{d_z}$ is projected onto the sphere of radius $\sqrt{d_z}$. As proven in `baseline/01`, spherical projection guarantees only $\operatorname{tr}(\Sigma_B) = d_z$ for $\Sigma_B = \mathbb{E}_{x \sim \rho}[B(x)B(x)^\top]$, not $\Sigma_B = I$. Moreover:
1. While zero-shot linear reward readout $Q_r^{\pi_z}(s,a) = F(s,a,z)^\top z_r$ with $z_r = \mathbb{E}_{x \sim \rho}[B(x)r(x)] = \Sigma_B \lambda$ automatically cancels $\Sigma_B^{-1}$ against $\Sigma_B$, **single-state goal encoding** $z_g = B(g)$ and **one-step intrinsic state-matching rewards** $r_z(y) = B(y)^\top \Sigma_B^{-1} z$ do **not** cancel $\Sigma_B^{-1}$ unless $\Sigma_B = I$.
2. During joint online training from scratch (where $\rho$ shifts continuously from ground-standing/falling transitions to obstacle-traversal or ball-striking transitions), mini-batch orthonormalization $\mathcal{L}_{\mathrm{orth}}$ can leave severe eigenvalue anisotropy in $\Sigma_B$.

**Core Question**: How does spectral ill-conditioning of $\Sigma_B$ during non-stationary online replay evolution affect (a) single-frame expert prompt encoding $z = \operatorname{proj}(B(m_{\mathrm{demo}}))$, (b) low-level actor gradients $\nabla_\theta (F(o, \pi_\theta(o,z), z)^\top z)$, and (c) multi-step intrinsic rewards $r_z(y) = B(y)^\top (\widehat{\Sigma}_B + \lambda_{\mathrm{reg}} I)^{-1} z$?

---

## 2. Hard Constraints & Non-Goals

- Must preserve the bilinear inner-product interface $F(o, a, z)^\top B(m)$ and spherical norm $\sqrt{d_z}$.
- Must not introduce supervised demonstration tracking losses or per-frame phase clocks.
- Any proposed whitening or covariance tracking estimator $\widehat{\Sigma}_B$ must be causal, bounded in memory/compute ($d_z \in \{100, 256\}$), and explicitly specify how it interacts with target EMA networks $(\bar{F}, \bar{B})$.

---

## 3. Deliverables Required from Primary Authors

1. **Spectral Error Analysis**: Derive the exact bias in $F(s,a,z)^\top B(g)$ and in unwhitened intrinsic rewards $\tilde{r}_z(y) = B(y)^\top z$ as a function of the singular value spectrum $\sigma_1(\Sigma_B), \dots, \sigma_{d_z}(\Sigma_B)$ when $\Sigma_B \neq I$.
2. **Algorithmic Proposal**: Specify whether and where EMA covariance whitening $(\widehat{\Sigma}_B + \lambda_{\mathrm{reg}} I)^{-1}$ or modified orthonormalization weighting should enter (i) `z_update` goal relabeling, (ii) `expert`/`near` rollout encoding, or (iii) multi-step hybrid world-model rollouts.
3. **Minimal Empirical Spike Protocol**: Define a self-contained Torch diagnostic on the 229-D / 277-D motion representation measuring $\kappa(\Sigma_B) = \lambda_{\max}(\Sigma_B)/\lambda_{\min}(\Sigma_B)$, effective rank, and single-state reachability accuracy with vs without covariance correction.

---

## 4. Adjudication Rubric

| Dimension | Weight | Scoring Standard |
|---|---:|---|
| Exact Mathematical Derivation | 30% | Correct treatment of $\Sigma_B$, $\Sigma_B^{-1}$, and spherical projection constraints. |
| Stability Under Non-Stationary $\rho$ | 25% | Handles rank deficiency early in training without matrix inversion blowup. |
| Compatibility with UFO Update Contract | 25% | Preserves exact separation of `behavior_z` and `z_update`. |
| Spike Falsifiability | 20% | Pre-registers quantitative pass/fail thresholds on effective rank and value error. |
