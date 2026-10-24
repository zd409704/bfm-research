# Program Charter: Forward-Backward Reinforcement Learning Beyond Imitation Data and Model-Based Training Acceleration

## 1. Mission Statement

Establish rigorous theoretical, algorithmic, and empirical foundations for joint **Forward-Backward (FB) + Low-Level Actor + Task Critic $Q$ + High-Level Planner** reinforcement learning from scratch, enabling legged and humanoid robots to:
1. Utilize unindexed single-frame demonstrations purely as latent behavioral prompts ($z = B(m)$) rather than rigid trajectory-tracking constraints.
2. Discover contact-rich recovery, multi-height obstacle traversal, and dynamic ball-striking behaviors that lie outside the state-action support of the demonstration library.
3. Combine short-horizon differentiable world-model pathwise gradients with long-horizon FB successor representations without violating Bellman consistency or causal observability boundaries.

---

## 2. Hard Technical Constraints & Non-Goals

1. **No Behavioral Cloning or Tracking Penalty Fallbacks**:
   - The low-level actor $\pi_\theta(o_{\mathrm{low}}, z)$ is updated exclusively by maximizing the conservative FB value $F(o, a, z)^\top z$ (plus optional task-critic gradient in single-step action-$Q$ variants). Adding a supervised action MSE loss $\|a - a_{\mathrm{demo}}\|^2$ or a per-frame pose-tracking task reward to force convergence is strictly forbidden.
2. **Strict Separation of Rollout Behavior $z$ and FB Update Relabel $z$**:
   - During rollout collection, behavior $z$ is chosen at macro-step boundaries from the scheduled three-way mixture (`expert`, `near`, `planner`).
   - During off-policy FB updates, $z_{\mathrm{update}}$ is sampled fresh via the 50/50 mixture (`50%` uniform hypersphere $\mathcal{S}^{d_z-1}(\sqrt{d_z})$, `50%` current online $B$ encoding of permuted replay next-frame motion $m_{t+1}$) under frozen batch-normalization statistics after updating BN once on current $(o_t, m_t)$ and once on next $(o_{t+1}, m_{t+1})$.
   - `z_update` must never overwrite `behavior_z` in the replay buffer, and the task critic $Q$ must always train on the actual executed macro behavior $z_{\mathrm{actual}}$ (or executed action $a_{\mathrm{applied}}$).
3. **Single-Frame Motion-Only Backward Input**:
   - The backward representation network $B(m)$ receives only single-frame root-relative kinematics (`229` dims in obstacle traversal; `277` dims in ball striking). It must not receive obstacle height, terrain scan, ball position, task phase, or demonstration frame indices.
4. **Strict Separation of Physical Failure vs Numerical Corruption**:
   - Runtime contact penetration exceeding `0.03` m with finite state/contact tensors, valid schema/timing, and no solver divergence must be recorded as a credible task termination (`severe_penetration`, `terminated=True`, absorption potential $\Phi_{\mathrm{next}}=0$) and committed to replay.
   - NaN/Inf values, contact buffer overflow with lost contacts, corrupted state/schema/timing, or verified solver divergence must be classified as `invalid`, rejected from replay and normalizer updates, and halt the affected run or evaluation panel for inspection.
5. **Strict Separation of Verified Evidence vs Unproven Claims**:
   - Short CPU integration smoke tests prove only contract, gradient flow, and checkpoint/resume mechanics. No document or proposal may claim that obstacle traversal or ball striking has been learned, or that FB beats PPO/AMP/world-model baselines, until full multi-seed GPU training and held-out evaluation panels pass their pre-registered gates.

---

## 3. Falsifiable Hypotheses

- **H1 (Gram Matrix Conditioning & Reward Readout)**: Standard FB orthonormalization loss $\mathcal{L}_{\mathrm{orth}} = \frac{1}{2N(N-1)}\sum_{i\ne j}(B(x_i)^\top B(x_j))^2 - \frac{1}{N}\sum_i \|B(x_i)\|_2^2$ on a changing replay distribution $\rho$ leaves significant off-diagonal covariance in $\Sigma_B$ during early joint training; explicitly whitening via damped $\widehat{\Sigma}_B^{-1}$ in intrinsic state-matching rewards $r_z(y) = B(y)^\top (\widehat{\Sigma}_B + \lambda I)^{-1} z$ reduces value-target variance and improves single-frame goal-reaching accuracy compared to raw dot products $B(y)^\top z$.
- **H2 (Off-Policy Decoupling Under Non-Stationary $B$)**: In joint training from scratch, storing raw physical motion frames $m_{\mathrm{current}}, m_{\mathrm{next}}$ in FB replay and re-encoding goal latents on the fly with current $B_{\omega}$, while storing executed $(H_{\mathrm{start}}, z_{\mathrm{actual}}, R_{\mathrm{macro}}, H_{\mathrm{final}})$ in a shorter-window task replay with target-planner bootstrap $\min_{i=1,2} Q_{\bar{\phi}_i}(H_{\mathrm{final}}, P_{\bar{\psi}}(H_{\mathrm{final}}))$, bounds value staleness without requiring importance sampling over the low-level trajectory.
- **H3 (World-Model Horizon vs FB Terminal Bootstrap)**: A hybrid objective combining $H \in \{8, 16\}$ differentiable world-model steps of dense intrinsic/task rewards with an FB terminal value bootstrap $\gamma^H F(s_H, a_H, z)^\top z$ achieves lower policy gradient bias-variance tradeoff than either $H=1$ first-action FB differentiation or $H=32$ pure world-model unrolling without terminal value representation.
- **H4 (Three-Way Source Schedule & Out-of-Support Exploration)**: Annealing macro-step latent selection from `(0.60 expert, 0.30 near, 0.10 planner)` to `(0.10 expert, 0.20 near, 0.70 planner)` over $S_{\mathrm{ramp}} = 100,000$ control steps enables the task critic $Q$ to experience both structured high-return regions and off-support recovery transitions, unlocking obstacle heights (`0.10..0.70` m) under `100%` planner evaluation where only a single `0.704` m demonstration exists.

---

## 4. Rubric & Verification Gates

Every research brief (`B01`–`B05`) is evaluated under the following pre-agreed rubric before any empirical spike is locked:

| Criterion | Weight | Pass Requirement |
|---|---:|---|
| **Mathematical & Causal Rigor** | 25% | Zero circular definitions, exact tensor dimensions, explicit stop-gradient boundaries, and zero future/privileged leakage into deployable modules. |
| **Contract & Baseline Alignment** | 25% | Full compliance with the frozen baseline specifications (`baseline/01` through `baseline/05`) and zero violation of Hard Constraints (§2). |
| **Falsifiability & Ablation Design** | 25% | Concrete, compute-matched experimental comparisons that isolate the proposed mechanism against explicit null baselines. |
| **Failure-Mode & Edge-Case Coverage** | 25% | Explicit handling of degenerate regimes (e.g., singular $\Sigma_B$, `severe_penetration` vs `invalid` physics, short macro truncation $k < K$, RNN prefix burn-in). |
