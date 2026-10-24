# Baseline 03: World-Model Pathwise Acceleration Mechanisms and Hybrid FB-Model-Based Designs

## 1. Motivation: Why Compare Differentiable World Models with FB?

Recent model-based imitation frameworks (exemplified by short-horizon differentiable world-model architectures for humanoid tracking) report **11x–26x faster per-step simulation throughput** and **~64x fewer environment/imagined steps** than model-free PPO on reference motion tracking. Understanding whether those gains come from **engineering throughput**, **multi-step pathwise policy gradients**, or **task simplicity**—and whether the same mechanism can accelerate **FB representation and control training**—requires a precise mathematical and systems decomposition.

---

## 2. Deconstructing Differentiable World-Model Acceleration

### 2.1 The Three-Network Loop (World Model $W_\psi$, Policy $\pi_\theta$, Critic $V_\phi$)

In the reference differentiable world-model paradigm, real simulator transitions are stored in a replay buffer $\mathcal{D}$, and policy optimization occurs inside a short imagined rollout of horizon $H$:

1. **World Model Training ($H_{\mathrm{wm}} = 8$ steps)**:
   - Autoregressively predicts normalized state deltas over 8 steps from real replay trajectories:
     $$
     \hat{s}_{t+1} = \hat{s}_t + \sigma_{\Delta s} W_\psi(\hat{s}_t, a_t, m_t) + \mu_{\Delta s}, \qquad \hat{s}_0 = s_0,
     $$
     minimizing multi-step MSE loss on state deltas and body positions.
2. **Critic Training ($H_{\mathrm{roll}} = 32$ steps, detached)**:
   - Unrolls $W_\psi$ and $\pi_\theta$ for 32 steps without policy gradients to compute $\text{TD}(\lambda)$ targets $G_t^\lambda$ from analytical tracking rewards $r(\hat{s}_t, a_t, m_t)$.
3. **Policy Training ($H_{\mathrm{roll}} = 32$ steps, pathwise differentiable)**:
   - Freeze world-model weights $\psi$ and critic weights $\phi$, but **preserve input gradients** $\partial W_\psi / \partial \hat{s}_t$, $\partial W_\psi / \partial a_t$, $\partial r / \partial \hat{s}_t$, and $\partial V_\phi / \partial \hat{s}_H$:
     $$
     \max_\theta J_H(\theta) = \mathbb{E}_{s_0 \sim \mathcal{D}}\left[\sum_{t=0}^{H-1} \gamma^t r(\hat{s}_t, a_t, m_t) + \gamma^H V_\phi(\hat{s}_H, m_H)\right], \qquad a_t = \pi_\theta(\hat{s}_t, m_t).
     $$

### 2.2 Disentangling Throughput Gains from Algorithmic Sample-Efficiency Gains

$$
\text{Total Wall-Clock Speedup} = \underbrace{\left(\frac{\text{Steps/s in MLP World Model}}{\text{Steps/s in Physics Engine}}\right)}_{\text{Engineering Throughput (11x--26x)}} \times \underbrace{\left(\frac{\text{Env Steps Required by Model-Free RL}}{\text{Imagined Steps Required by Pathwise Grad}}\right)}_{\text{Algorithmic Step Reduction (~64x in Tracking)}}.
$$

- **Why the 11x–26x throughput factor occurs**: Stepping an MLP `[512, 512, 256]` in batched GPU tensor memory avoids 200 Hz contact detection, constraint solving, and collision broadphase in the physics engine.
- **Why the ~64x step reduction occurs in reference tracking**:
  1. The tracking reward $r(\hat{s}_t, a_t, m_t)$ is a smooth, known differentiable function of the state and reference frame.
  2. Differentiating through $H=32$ steps provides low-variance **pathwise (reparameterization) gradients** $\partial r_{t+k} / \partial a_t$ rather than high-variance score-function (REINFORCE/PPO) estimators.
  3. **Crucial caveat**: In reference tracking, the world model receives the **future ground-truth reference motion sequence $m_{0:H}$** as an input hint, reducing dynamics learning to local residual tracking around a known trajectory rather than global open-ended dynamics prediction.

---

## 3. Exact Mathematical Comparison: World-Model Pathwise Gradient vs Standard FB Actor Gradient

A common misconception is that because $F(s_0, a_0, z)^\top w_r \approx Q_r^{\pi_z}(s_0, a_0)$ already represents the infinite-horizon discounted return, differentiating $F(s_0, \pi_\theta(s_0, z), z)^\top w_r$ with respect to $\theta$ is equivalent to unrolling a world model. **This is mathematically false.**

### 3.1 What Standard FB Actor Optimization Differentiates

In standard FB, the actor loss at state $s_0$ is:
$$
\mathcal{L}_\pi(\theta) = -F\bigl(s_0, \pi_\theta(s_0, z), z\bigr)^\top w_r.
$$
By the chain rule, the gradient with respect to policy parameters $\theta$ is:
$$
\nabla_\theta \bigl(F(s_0, \pi_\theta(s_0, z), z)^\top w_r\bigr) = \bigl(D_\theta \pi_\theta(s_0, z)\bigr)^\top \left.\nabla_a \bigl(F(s_0, a, z)^\top w_r\bigr)\right|_{a = \pi_\theta(s_0, z)}.
$$
Because $F$ was trained via one-step TD with a stop-gradient target $\gamma F_{\bar{\theta}}(s_1, \pi_\theta(s_1, z), z)$, the dependence of future actions $a_1 = \pi_\theta(s_1, z), a_2 = \pi_\theta(s_2, z), \dots$ on $\theta$ is **frozen inside the parameters of $F$** during the single-step actor update. Thus, standard FB computes **only the first-action derivative** ($\partial Q_r^{\pi_z} / \partial a_0$), relying on iterative alternating updates between $F$ and $\pi_\theta$ (generalized policy iteration) for future policy improvements to propagate backward.

### 3.2 What $H$-Step World-Model Unrolling Differentiates

For a true trajectory value $J_H(\theta) = \mathbb{E}[\sum_{t=0}^{H-1} \gamma^t r(\hat{s}_{t+1}) + \gamma^H Q_r(\hat{s}_H, a_H)]$, the shared policy parameters $\theta$ appear at **every step $t = 0, \dots, H-1$** via $a_t = \pi_\theta(\hat{s}_t, z)$. Even under a deterministic world model $\hat{s}_{t+1} = f_\psi(\hat{s}_t, a_t)$:
$$
\frac{d J_H(\theta)}{d \theta} = \sum_{t=0}^{H-1} \gamma^t \bigl(D_\theta \pi_\theta(\hat{s}_t, z)\bigr)^\top \frac{\partial V_t^{\mathrm{tail}}(\hat{s}_t)}{\partial a_t},
$$
where the state-to-state Jacobian $\frac{d \hat{s}_{t+1}}{d \hat{s}_t} = \frac{\partial f_\psi}{\partial \hat{s}_t} + \frac{\partial f_\psi}{\partial a_t} \frac{\partial \pi_\theta(\hat{s}_t, z)}{\partial \hat{s}_t}$ couples all $H$ closed-loop calls to $\pi_\theta$.

| Property | Standard FB Actor Update ($H=1$) | $H$-Step Differentiable World-Model + FB Tail |
|---|---|---|
| **Policy Calls Differentiated per Update** | Only $a_0 = \pi_\theta(s_0, z)$ at $t=0$ | All $a_0, a_1, \dots, a_{H-1}$ along the $H$-step closed-loop trajectory |
| **How Future $\theta$ Dependence Enters** | Indirectly across training iterations via TD target updates of $F$ | Directly within the same backward pass via $\partial \hat{s}_{t+k} / \partial \theta$ |
| **Sensitivity to Long-Horizon Model Rollout Error** | Zero multi-step rollout compounding (uses 1-step real transitions) | Compounds dynamics error over $H$ steps; bounded by keeping $H \in [4, 16]$ |
| **Sensitivity to Critic Action-Derivative Bias** | High: relies entirely on accuracy of $\nabla_{a_0} F(s_0, a_0, z)$ | Lower for steps $0..H-1$: uses direct state-reward derivatives through $W_\psi$ |

---

## 4. Intrinsic Reward Formulation for Latent-Conditioned World-Model Rollouts

To unroll a world model for an arbitrary FB skill latent $z \in \mathbb{R}^{d_z}$ (including random spherical $z$ where no external task reward $r_{\mathrm{task}}$ is specified), we need a one-step intrinsic reward $r_z(s_{t+1})$ whose discounted sum matches the FB objective $F(s_0, a_0, z)^\top z$.

From Baseline 01 (§3.2 & §4.2), since $\Sigma_B F(s,a,z) = \mathbb{E}[\sum_{t=0}^\infty \gamma^t B(s_{t+1}) \mid s,a, \pi_z]$, the exact one-step intrinsic reward is:
$$
r_z(y) = B(y)^\top \Sigma_B^{-1} z = \phi(y)^\top z, \qquad \phi(y) := \bigl(\widehat{\Sigma}_B + \lambda_{\mathrm{reg}} I\bigr)^{-1} B(y),
$$
where $\widehat{\Sigma}_B = \mathbb{E}_{y \sim \rho}[B(y)B(y)^\top]$ is tracked via an exponential moving average (with damping $\lambda_{\mathrm{reg}} > 0$ for numerical stability). Only when $\Sigma_B \approx I$ does the approximation $\tilde{r}_z(y) = B(y)^\top z$ hold without bias.

---

## 5. Four Candidate Hybrid Architectures for Accelerating FB

| Track | Mathematical Formulation | What Changes vs Standard FB | Primary Pros & Cons |
|---|---|---|---|
| **Track 1: Multi-Step Real-Trajectory FB ($n$-Step Return)** | $Y_F^{(n)} = \sum_{k=0}^{n-1} \gamma^k \phi(s_{t+k+1}) + \gamma^n \bar{F}(s_{t+n}, \pi_\theta(s_{t+n}, z), z)$ | Replaces 1-step TD target of $F$ with $n$-step real replay target (with off-policy trace cutting when behavior $z_b \neq z$). | **Pro**: Zero world-model error; faster long-horizon propagation in $F$. **Con**: Still $H=1$ first-action derivative for $\pi_\theta$; off-policy truncation when $z_b \neq z$. |
| **Track 2: FB + Short-Horizon Differentiable World Model ($W_\psi$)** | $J_H(\theta) = \mathbb{E}_{s_0, z}\left[\sum_{t=0}^{H-1} \gamma^t \bar{\phi}(\hat{s}_{t+1})^\top z + \gamma^H \bar{F}(\hat{s}_H, \pi_\theta(\hat{s}_H, z), z)^\top z\right]$ | Adds $W_\psi(s_t, a_t) \to \hat{s}_{t+1}$ trained on real transitions (without future reference hints); unrolls $H \in \{4, 8, 16\}$ steps for $\pi_\theta$ with frozen $\bar{B}, \bar{F}$ terminal tail. | **Pro**: Combines multi-step pathwise policy gradients with infinite-horizon FB representation. **Con**: Requires $W_\psi$ to predict multi-modal contact transitions without reference hints; $\bar{B}$ drifts during training. |
| **Track 3: Pure-F Replacement by World Model + $B$** | Drops $F$ entirely; optimizes $J_H^{\mathrm{no\text{-}F}}(\theta) = \sum_{t=0}^{H-1} \gamma^t \phi(\hat{s}_{t+1})^\top z$ | Removes $F$ and successor Bellman loss; keeps only $W_\psi$, $B(y)$ with orthonormalization, and $\pi_\theta(s,z)$. | **Pro**: Eliminates $N \times N$ FB bilinear TD loss. **Con**: Truncates horizon to $H$; loses zero-shot long-horizon value readout $Q_r = F^\top z_r$. |
| **Track 4: World Model + Task Critic Only (Single-Task Baseline)** | Standard differentiable world model + $V_\phi$ + $\pi_\theta$ on a fixed task reward $r_{\mathrm{task}}$ | Drops both $F$ and $B$; learns only the single downstream task. | **Pro**: Fastest single-task convergence when $r_{\mathrm{task}}$ is dense and smooth. **Con**: Zero reusable multi-task behavioral representation $z$. |

---

## 6. Controlled 4-Arm Diagnostic Experiment Specification

To rigorously separate **representation overhead**, **pathwise horizon length ($H=1$ vs $H>1$)**, and **world-model approximation error**, Brief `B04` specifies a compute-matched 4-arm ablation on the same plant, action space, and observation contract:
1. **Arm A (Single-Task World Model, $H=32$)**: World model $W_\psi$ + task critic $V_\phi$ + policy $\pi_\theta$ without $z$ conditioning.
2. **Arm B (Multi-Task World Model, $H=32$)**: Same world model, but $\pi_\theta(s, z)$ and $V_\phi(s, z)$ are conditioned on a family of task/skill latents $z$.
3. **Arm C (Multi-Task World Model, $H=1$ First-Action Only)**: Same as Arm B, but unrolled for $H=1$ step ($r(\hat{s}_1, z) + \gamma V_\phi(\hat{s}_1, z)$), isolating the effect of $H=32$ pathwise gradients vs $H=1$ first-action gradients.
4. **Arm D (Hybrid FB + World Model, $H \in \{1, 8, 16\}$)**: Full FB representation $(F, B)$ with $H$-step differentiable world-model rollout and $\gamma^H F(\hat{s}_H, a_H, z)^\top z$ terminal bootstrap, comparing raw $B(y)^\top z$ vs whitened $B(y)^\top (\widehat{\Sigma}_B + \lambda I)^{-1} z$.
