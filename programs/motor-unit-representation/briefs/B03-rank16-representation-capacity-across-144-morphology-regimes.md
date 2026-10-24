# Brief B03: Rank-16 Bilinear Bottleneck Across 144 Morphology-Stroke Regimes and Orthonormalization Regularization

**Packet ID**: `B03`
**Status**: `IN_PROGRESS`
**Baseline References**: `baseline/01-motor-unit-proprioception-and-representation-design.md`, `baseline/02-v3-asymmetric-network-and-training-specification.md` (§6), `baseline/03-v3-engineering-status-evidence-and-open-audit-issues.md` (Audit Issue #7)

---

## 1. Problem Statement

As noted in `baseline/02` §6, if $K = 144$ morphology-stroke configurations induced mutually orthogonal transition operators sharing an unconditioned rank-$d_z$ ($d_z = 16$) representation, the minimum relative Frobenius approximation error would be $\sqrt{1 - 16/144} \approx 0.9428$. In V3, $B_\omega(g_{13}) \in \mathcal{S}^{15}(4)$ is shared across all 144 configurations without receiving static geometry parameters (since $g_{13}$ contains only angle, angular velocity, causal acceleration, and link tip kinematics in housing frame $M$), whereas $F_{\eta}(x_{137}, p_{5065}, a, z_{16})$ and $\pi_\theta(x_{137}, z_{16})$ receive morphology/capacity conditioning.

However, two structural tensions arise:
1. Because link tip position $p_{\mathrm{tip},D}^M$, velocity $v_{\mathrm{tip},D}^M$, and acceleration $\widehat{a}_{\mathrm{tip},D}^M$ in $g_{13}$ scale linearly with link length $L_D \in [0.08, 0.45]\text{ m}$, raw $g_{13}$ vectors from short links ($L_D = 0.08\text{ m}$) and long links ($L_D = 0.45\text{ m}$) occupy different radial shells of $\mathbb{R}^{13}$.
2. Under Audit Issue #7, unstratified mini-batch orthonormalization $\mathcal{L}_{\mathrm{orth}}(B_\omega)$ allows high-variance long-link E0 motions to dominate the 16 orthogonal directions of $\Sigma_B$, collapsing the representation resolution available for short-link and E1/E3 boundary/load states.

**Core Question**: Does the 16-dimensional shared outcome encoder $B_\omega(g_{13})$ suffer from cross-morphology variance domination and rank bottleneck across the 144 configurations, and how should $g_{13}$ scaling and regime-stratified orthonormalization $\mathcal{L}_{\mathrm{orth}}$ be formulated to maximize effective rank per configuration?

---

## 2. Hard Constraints & Non-Goals

- Must keep $d_z = 16$ and the deployed parameter budget fixed at `281,617` parameters (`74,000` for $B_\omega$, `207,617` for $\pi_\theta$).
- Must preserve the physical interpretability of $g_{13}$ as a single-step local outcome vector.

---

## 3. Deliverables Required from Primary Authors

1. **Singular-Value Decomposition of the 144-Configuration Outcome Operator**: Analyze how link-length scaling $L_D$ in $(p_{\mathrm{tip},D}^M, v_{\mathrm{tip},D}^M, \widehat{a}_{\mathrm{tip},D}^M)$ couples with angular kinematics $(\cos q_c, \sin q_c, \dot{q}_c, \widehat{\ddot{q}})$ in $g_{13}$, and derive the exact per-configuration effective rank $\operatorname{erank}(\Sigma_B^{(k)})$ under global vs stratified orthonormalization.
2. **Stratified Orthonormalization & Nondimensionalization Proposal**: Compare (a) global mini-batch $\mathcal{L}_{\mathrm{orth}}$, (b) scene-and-capacity inverse-probability weighted $\mathcal{L}_{\mathrm{orth}}$, and (c) decomposing $g_{13}$ into nondimensionalized angular/tip features + explicit scale ratio so that all 144 configurations share a common isotropic covariance $\Sigma_B^{(k)} \approx I_{16}$.
3. **Minimal Empirical Spike Protocol**: Define a quantitative SVD diagnostic across the 144 configurations measuring per-configuration $\operatorname{erank}(\Sigma_B^{(k)})$, worst-group successor prediction error, and zero-shot outcome decoding accuracy.

---

## 4. Adjudication Rubric

| Dimension | Weight | Scoring Standard |
|---|---:|---|
| Mathematical Analysis of Cross-Morphology SVD | 30% | Rigorously resolves the $\sqrt{1 - 16/144} \approx 0.943$ lower-bound objection. |
| Resolution of Audit Issue #7 | 25% | Provides an exact stratified/weighted $\mathcal{L}_{\mathrm{orth}}$ formulation. |
| Preservation of Tip Kinematic Information | 25% | Does not discard lever-arm/tip momentum semantics needed by upper layers. |
| Spike Falsifiability | 20% | Pre-registers quantitative thresholds on per-group effective rank $\ge 12/16$. |
