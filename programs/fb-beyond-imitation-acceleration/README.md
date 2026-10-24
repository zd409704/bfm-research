# Forward-Backward Reinforcement Learning Beyond Imitation Data and Model-Based Training Acceleration

## 1. Program Overview

This research program investigates how a **Forward-Backward (FB) representation + low-level conditioned actor + independent task critic $Q$ + high-level planner** reinforcement learning paradigm can:
1. **Surpass finite demonstration trajectories** to discover novel contact interactions, disturbance recovery strategies, and autonomous multi-height obstacle traversal or dynamic ball-striking skills from scratch without behavioral cloning or reference-tracking penalties.
2. **Accelerate joint representation and control training** by analyzing the mathematical relationship between short-horizon differentiable world-model rollouts (pathwise gradients) and long-horizon FB successor representations (first-action derivatives vs shared-parameter trajectory gradients).

**Portfolio Priority**: **Priority 1** (Primary Queue Target).
**Queue Status**: `READY_NOT_STARTED` (awaiting explicit owner authorization to launch).

---

## 2. Core Scientific Questions

1. **Mathematical & Geometric Foundations of FB**:
   - In the FB decomposition of the normalized successor density $m_z(s,a,x) = M_z(s,a,x)/\rho(x) \approx F(s,a,z)^\top B(x)$, individual coordinates of $B(x)$ and $F(s,a,z)$ are non-identifiable under invertible linear transformations $(F, B) \mapsto (A^{-\top} F, A B)$.
   - Spherical normalization $\|B(x)\|_2 = \sqrt{d}$ only enforces $\operatorname{tr}(\Sigma_B) = d$, not $\Sigma_B = I$. How do deviations of the covariance matrix $\Sigma_B = \mathbb{E}_{x \sim \rho}[B(x)B(x)^\top]$ from the identity matrix distort zero-shot task reward encoding $z_r = \mathbb{E}_{x \sim \rho}[B(x)r(x)]$ and intrinsic state-matching rewards $r_z(y) = B(y)^\top \Sigma_B^{-1} z$?
2. **Surpassing Imitation Support Without Tracking Locks**:
   - How can single-frame unindexed demonstration poses $m_{\mathrm{demo}}$ be used strictly as latent exploration prompts $z_{\mathrm{exp}} = \operatorname{proj}(B(m_{\mathrm{demo}}))$ and local tangent-space perturbations $z_{\mathrm{near}}$ ($10^\circ$–$20^\circ$) during rollout, while keeping FB successor updates and task $Q$ Bellman backups strictly grounded in real physical transitions?
3. **Motion-Only Backward Map Aliasing in Contact-Rich Tasks**:
   - When $B(m)$ encodes only single-frame proprioceptive and root-relative link kinematics (e.g., 229-dim for obstacle traversal or 277-dim for ball striking) without terrain geometry, obstacle height, or ball state, two dynamically distinct contact scenarios can map to the same $B(m)$. Where is the exact boundary of what high-level task $Q(H, z)$ and planner $P(H)$ can compensate for vs where $B$ itself becomes a bottleneck?
4. **World-Model Pathwise Gradients vs FB Successor Gradients**:
   - Differentiable world-model rollouts propagate $\nabla_\theta J_H$ through all $H$ closed-loop actor evaluations and physics transitions, whereas standard FB actor updates differentiate $F(s_0, \pi_\theta(s_0, z), z)^\top z$ only with respect to the first action $a_0$ while treating future policy dependence inside $F$ as a stop-gradient target. Can a short-horizon differentiable world model ($H=8$ to $32$) combined with an FB terminal value tail $F(s_H, a_H, z)^\top z$ achieve sample-efficiency gains without suffering from long-horizon compounding model error or non-stationary $B$ drift?
5. **Engineering Integrity in Joint Multi-Module Training**:
   - Joint training from random initialization couples six networks ($F, B, \pi_{\theta}, Q_1, Q_2, P_{\psi}$) across two replay buffers (transition-level FB replay and macro-step or action-level task replay). How must batch normalization statistics, UFO-faithful $z$ relabeling (`50%` online-$B$ goal / `50%` uniform sphere), terminal absorption vs timeout bootstrapping, and credible physical failure (`severe_penetration`) vs numerical corruption (`invalid`) be isolated?

---

## 3. Verified Baseline Evidence vs Unproven Claims

| Claim Category | Verified Baseline Evidence | Unproven / Open (Must Not Be Claimed as Established) |
|---|---|---|
| **Mathematical Theory** | Exact derivation of $M_z$, density $m_z$, TD loss without explicit $\rho(x)$, one-step contribution $c(s,a,z)$, $\Sigma_B F(s,a,z) = [Q_{B_1}^{\pi_z}, \dots, Q_{B_d}^{\pi_z}]^\top$, and $Q_r^{\pi_z}(s,a) = F(s,a,z)^\top z_r$ under $\Sigma_B \lambda = z_r$. | Empirical conditioning and spectrum drift of $\Sigma_B^{-1}$ during joint online humanoid training from scratch. |
| **3D Obstacle Traversal (29-DoF Plant)** | v3.1.1 / R2.1 design contracts frozen; action mapping contract T0 (`scale=1.0` across 29 channels, `dt_physics=0.005` s, `dt_control=0.02` s, 229-D frame descriptor) and Torch FB core T1 verified on bounded CPU tests; short real-backend CPU smoke completed (320 control rows, 120 FB updates, 111 task updates, 100% `final_valid`, resume verified). | Autonomous obstacle traversal across the `0.10..0.70` m height curriculum (`95%` Wilson lower bound $\ge 0.70$), multi-seed superiority over PPO/AMP baselines, and full R2.1 production integration on GPU. |
| **Dynamic Ball Striking (29-DoF Plant)** | v2 architecture and mathematical specification completed, resolving 5 structural audit defects from v1 (reward window state leak, $B$ input pollution, ensemble scalar inner-product order, $K_{\mathrm{hold}}=1$ action-Q alignment, full-prefix RNN burn-in). | Full closed-loop training convergence, multi-leg striking success rates, and out-of-distribution ball placement generalization. |
| **Model-Based Acceleration** | Architectural analysis of 8-step world-model training / 32-step imagined policy optimization (`11x-26x` per-step throughput and `64x` step reduction in reference tracking) and formulation of 4 FB hybrid modification tracks. | Controlled 4-arm ablation isolating world-model throughput vs multi-step pathwise gradient vs representation overhead on the same plant and task. |

---

## 4. Directory Structure

```text
fb-beyond-imitation-acceleration/
├── README.md                                              # Program overview, scientific questions, and status
├── PROGRAM_CHARTER.md                                     # Scope, hard boundaries, falsifiable hypotheses, and gates
├── QUEUE.md                                               # Ordered research queue (status: READY_NOT_STARTED)
├── baseline/
│   ├── 01-fb-theoretical-derivation-and-q-readout.md      # Complete mathematical derivation of FB and Q readout
│   ├── 02-fb-paradigm-beyond-imitation-and-exploration.md # Paradigm mechanics for surpassing imitation data
│   ├── 03-model-based-acceleration-and-fb-hybrid-design.md# World-model gradient acceleration vs FB analysis
│   ├── 04-joint-fb-ball-striking-v2-architecture.md       # 29-DoF ball-striking v2 joint FB+task-Q+planner spec
│   └── 05-autonomous-obstacle-traversal-v3-and-r2-plan.md # 29-DoF obstacle traversal v3.1.1 and R2.1 spec
├── briefs/
│   ├── B01-fb-density-gram-geometry-and-intrinsic-reward-identifiability.md
│   ├── B02-nonstationarity-and-off-policy-credit-assignment-in-joint-fb-task-training.md
│   ├── B03-motion-only-backward-map-under-contact-and-terrain-aliasing.md
│   ├── B04-pathwise-world-model-gradients-vs-fb-successor-derivatives-ablation.md
│   └── B05-obstacle-traversal-r2-terminal-boundary-and-curriculum-verification.md
├── claims/                                                # Claim ledger directory
├── packets/                                               # Task packet artifacts directory
├── reviews/                                               # Blind peer-review artifacts directory
├── synthesis/                                             # Adjudication & synthesis artifacts directory
├── method-issues/                                         # Methodology audit directory
└── logs/                                                  # Execution and verification logs directory
```
