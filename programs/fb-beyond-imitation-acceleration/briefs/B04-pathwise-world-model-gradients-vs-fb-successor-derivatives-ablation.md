# Brief B04: Pathwise World-Model Gradients vs First-Action FB Successor Derivatives: Controlled 4-Arm Ablation and Hybrid Horizon Design

**Packet ID**: `B04`
**Status**: `READY_NOT_STARTED`
**Baseline References**: `baseline/03-model-based-acceleration-and-fb-hybrid-design.md`, `baseline/01-fb-theoretical-derivation-and-q-readout.md`

---

## 1. Problem Statement

As established in `baseline/03`, standard FB actor updates optimize $\mathcal{L}_\pi(\theta) = -F(s_0, \pi_\theta(s_0, z), z)^\top z$, which differentiates only with respect to the **first action $a_0 = \pi_\theta(s_0, z)$** while treating future policy calls inside $F$ as a stop-gradient TD target. In contrast, differentiable world-model rollouts of horizon $H$ propagate pathwise gradients through all $H$ closed-loop policy evaluations $a_0, \dots, a_{H-1}$ and state transitions $\hat{s}_1, \dots, \hat{s}_H$, achieving large sample-efficiency gains in reference tracking where future reference frames $m_{0:H}$ are known.

However, in **autonomous FB reinforcement learning without future reference hints**, unrolling a learned world model $W_\psi(\hat{s}_t, a_t)$ faces two fundamental challenges:
1. Without future ground-truth reference frames $m_{t+1}$ as an input hint, contact-rich humanoid dynamics error compounds rapidly over $H=32$ steps.
2. Evaluating intrinsic rewards along the imagined rollout requires $r_z(\hat{s}_{t+1}) = B(\hat{m}_{t+1})^\top \Sigma_B^{-1} z$ and a terminal bootstrap $\gamma^H F(\hat{s}_H, \pi_\theta(\hat{s}_H, z), z)^\top z$, both of which depend on an evolving backward representation $B_\omega$.

**Core Question**: What is the optimal rollout horizon $H \in \{1, 4, 8, 16, 32\}$ for hybrid **World-Model + FB Terminal Tail** training when no future reference trajectory hint is available, and how much of the acceleration comes from $H > 1$ pathwise gradients vs world-model step throughput?

---

## 2. Hard Constraints & Non-Goals

- The world model $W_\psi(\hat{s}_t, a_t)$ must **never** receive future demonstration frames $m_{t+1..t+H}$ during autonomous task rollouts or FB skill learning.
- All 4 experimental arms (`Arm A`, `Arm B`, `Arm C`, `Arm D` in `baseline/03` §6) must share the exact same physics plant, observation space, action mapping, and compute measurement protocol (reporting both environment steps and wall-clock GPU seconds).

---

## 3. Deliverables Required from Primary Authors

1. **Bias-Variance & Compounding Error Bound**: Derive the gradient error bound for the hybrid objective:
   $$
   J_H(\theta) = \mathbb{E}_{s_0, z}\left[\sum_{t=0}^{H-1} \gamma^t \bar{\phi}(\hat{s}_{t+1})^\top z + \gamma^H \bar{F}(\hat{s}_H, \pi_\theta(\hat{s}_H, z), z)^\top z\right]
   $$
   as a function of one-step world-model Jacobian error $\|\nabla W_\psi - \nabla f_{\mathrm{true}}\|$, horizon $H$, and terminal critic action-gradient error $\|\nabla_a \bar{F} - \nabla_a F^\star\|$.
2. **Adaptive Horizon / Hybrid Architecture Design**: Specify the exact architecture of $W_\psi$, its multi-step state-delta training loss on `FBReplay`, the stop-gradient rules on $(\bar{B}, \bar{F}, \widehat{\Sigma}_B^{-1})$, and how contact discontinuity stiff gradients are handled across $H$ steps.
3. **Pre-Registered 4-Arm Spike Protocol**: Detail the exact execution plan for Arms A, B, C ($H=1$ vs $H=32$), and D ($H \in \{1, 4, 8, 16\}$) to isolate throughput vs multi-step pathwise differentiation vs representation overhead.

---

## 4. Adjudication Rubric

| Dimension | Weight | Scoring Standard |
|---|---:|---|
| Mathematical Rigor of Gradient Decomposition | 30% | Exact chain-rule treatment of first-action vs $H$-step shared-parameter gradients. |
| Strict Zero-Future-Leakage Guarantee | 25% | World model uses only causal $(s_t, a_t)$ inputs without reference motion lookahead. |
| Contact Stiffness & Rollout Stability | 25% | Addresses gradient explosion/bias through hybrid contacts and truncation horizon $H$. |
| 4-Arm Ablation Completeness | 20% | Cleanly separates all three confounding factors (throughput, $H$, multi-task $z$). |
