# Brief B02: Non-Stationarity, Batch-Norm Ordering, and Off-Policy Credit Assignment in Joint FB + Task-Q + Planner Training

**Packet ID**: `B02`
**Status**: `READY_NOT_STARTED`
**Baseline References**: `baseline/02-fb-paradigm-beyond-imitation-and-exploration.md`, `baseline/04-joint-fb-ball-striking-v2-architecture.md`, `baseline/05-autonomous-obstacle-traversal-v3-and-r2-plan.md`

---

## 1. Problem Statement

When training FB ($F, B$), the low-level actor $\pi_\theta(o, z)$, the task critic $Q_{\phi_1, \phi_2}$, and the high-level recurrent planner $P_\psi$ **jointly from random initialization**, two distinct off-policy credit-assignment regimes arise across our baselines:
1. **Macro-$z$ Critic Regime (Obstacle Traversal, $K=10$)**: $Q_{\phi_1, \phi_2}(H_t, c_t^{\mathrm{geom}}, z_{\mathrm{actual}})$ evaluates a 10-step macro latent $z_{\mathrm{actual}} \in \mathcal{S}^{255}(16)$. As $B_\omega$ and $\pi_\theta(o, z)$ evolve during training, a historical $z_{\mathrm{actual}}$ stored in `TaskReplay` no longer induces the same 10-step physical trajectory distribution that generated $R_{\mathrm{macro}}$.
2. **Step Action-$Q$ Regime (Ball Striking v2, $K_{\mathrm{hold}}=1$)**: $Q_{\phi_1, \phi_2}(H_t^Q, a_t)$ evaluates the 1-step physical action $a_t \in [-1, 1]^{29}$, and $P_\psi$ updates via $\nabla_\psi Q_{\phi_1}(H_t^Q, \pi_\theta(o_t^{\mathrm{low}}, P_\psi(H_t^{\mathrm{plan}})))$. Here, rapid updates to $\pi_\theta$ from the FB loss shift the mapping $z \mapsto a$, requiring a dedicated task-only actor EMA $\bar{\theta}$ for target action bootstrapping.

**Core Question**: How can off-policy representation drift between `FBReplay` and `TaskReplay` (including batch normalizer statistics, historical `z_actual` staleness, and full-prefix RNN hidden-state reconstruction) be bounded and diagnosed during joint training from scratch?

---

## 2. Hard Constraints & Non-Goals

- Must strictly enforce the R2.1 UFO update order: update BN once on `(obs, m_current)` and once on `(next_obs, m_next)`, freeze BN (`eval/no_grad`), sample `z_update` (`50%` online-$B$ permuted `m_next`, `50%` random sphere), and never overwrite `behavior_z`.
- Must not introduce pre-training stages or freeze $B_\omega$ / $\pi_\theta$.
- Must preserve full-prefix zero-hidden burn-in for recurrent $P_\psi$ and $Q_{\phi_1, \phi_2}$.

---

## 3. Deliverables Required from Primary Authors

1. **Drift Quantification Metric**: Define an exact, online-computable metric measuring **behavioral drift** $\Delta_\pi(z) = \|\pi_{\theta_{\mathrm{now}}}(o, z) - \pi_{\theta_{\mathrm{then}}}(o, z)\|_2$ and **encoder drift** $\Delta_B(m) = 1 - \frac{1}{d_z}\langle B_{\omega_{\mathrm{now}}}(m), B_{\omega_{\mathrm{then}}}(m) \rangle$ across the age distribution of `TaskReplay` (`generation` tags are already stored in R2.1 macro rows).
2. **Mitigation & Replay Horizon Design**: Compare (a) fixed FIFO `TaskReplay` capacity, (b) generation-lag-weighted TD updates or trust-region filtering on stale macro rows, and (c) re-encoding raw expert frames vs keeping executed planner $z_{\mathrm{actual}}$ in macro-$z$ critic updates.
3. **Minimal Empirical Spike Protocol**: Specify a bounded test verifying BN invariance to expert queries, invariance of `z_update` to `behavior_z` mutations, and bounded TD error under synthetic representation drift.

---

## 4. Adjudication Rubric

| Dimension | Weight | Scoring Standard |
|---|---:|---|
| Exactness of Off-Policy Semantics | 30% | Clearly distinguishes transition-level $a$-critic from macro-level $z$-critic requirements. |
| Compliance with R2.1 & v2 Contracts | 25% | Zero violation of BN ordering, `z_update` sampling, or RNN prefix reconstruction. |
| Computational Overhead | 20% | Diagnostic and mitigation add $< 5\%$ wall-clock cost per update. |
| Spike Falsifiability | 25% | Pre-registers unit and integration checks on generation lag and value stability. |
