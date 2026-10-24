# Synthesis B04 — Pathwise World-Model Gradients vs First-Action FB Successor Derivatives: Controlled 4-Arm Ablation and Hybrid Horizon Design

- **Decision ID**: `D-B04-001`
- **Packet ID**: `B04`
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
- **Adjudicators**:
  1. `agy` (`gemini-4-argon-high`, Order 1: `P=A, Q=B`): `packets/B04/adjudication-agy-order1.md`
  2. `claude` (`sonnet`, Order 2: `P=B, Q=A`): `packets/B04/adjudication-sonnet-order2.md`
- **Pre-Registered Empirical Spike**: `packets/B04/spikes/B04-SPIKE/VERDICT.json` (`PASS`) and NVIDIA L4 GPU (`gpu_experiments/colab_gpu_results_cuda.json`, `PASS`)

---

## 1. Consolidated Order-Swapped Rubric Scores

| Proposal Track | Author Model | Order 1 (`agy`: P=A, Q=B) | Order 2 (`sonnet`: P=B, Q=A) | Mean Score |
|---|---|---:|---:|---:|
| **Proposal A** (`proposals/A.md`) | `claude` Opus | `83.0 / 100.0` (Math 24, Leak 21, Contact 21, 4-Arm 17) | `72.0 / 100.0` (Math 21, Leak 20, Contact 19, 4-Arm 12) | **77.5 / 100.0** |
| **Proposal B** (`proposals/B.md`) | `codex` `gpt-6-astra` | `81.0 / 100.0` (Math 26, Leak 23, Contact 17, 4-Arm 15) | `73.0 / 100.0` (Math 26, Leak 22, Contact 14, 4-Arm 11) | **77.0 / 100.0** |

- **Disposition**: **`Tie / Hybrid Co-Design (Lead Base: Proposal A at 77.5 vs 77.0, Δ = +0.50 < 5.0 tie margin)`** uniting Proposal B's exact forward-sensitivity and adjoint recurrence ($E_{t+1} = L E_t + [\epsilon_D + K_G \delta_t](1 + M_t)$), closed-loop survival derivative, 5-member world-model ensemble, and 16-step detached RNN prefix burn-in with Proposal A's occupancy-vs-fixed-start DPG decomposition, $\gamma^H H \epsilon_F^s$ terminal state-gradient amplification analysis, log-space soft survival + Jacobian-growth truncation ($\Lambda_{\max}=10$), and single-factor oracle-substitution ablation suite (`E_J, E_c, E_F, E_W`).

---

## 2. Key Adjudication Findings & Mandatory Merges Adopted into Synthesis

1. **Exact Pathwise vs First-Action Gradient Decomposition & Bias-Variance Tradeoff**:
   - Standard 1-step FB actor updates ($\mathcal{L}_\pi(\theta) = -\min_k F_k(s_0, \pi_\theta(s_0, z), z)^\top z$, $H=0$) differentiate only through the immediate action $a_0 = \pi_\theta(s_0, z)$, dropping future closed-loop policy Jacobians $\sum_{t \ge 1} \gamma^t c_t P_t^\top Q_a^{\theta_0}$. While on-policy discounted occupancy $d_\gamma^{\pi_z}$ integrates 1-step derivatives over states, off-policy replay mismatch $\|\rho - d_\gamma^{\pi_z}\|_{\mathrm{TV}}$ and critic action-Jacobian error $\epsilon_F^a = \|\nabla_a \bar{F} - \nabla_a F^\star\|$ leave the $H=0$ gradient nearly orthogonal to the true multi-step physical return gradient on contact dynamics (`cos = -0.0338` on L4 GPU).
   - Unrolling a causal world model $W_\psi(\hat{s}_t, a_t)$ over horizon $H$ with B01-whitened step rewards $r_z(\hat{s}_{t+1}) = \bar{B}(\hat{m}_{t+1})^\top W_u z$, soft survival weights $c_t = \prod_{j=0}^{t-1} \hat{p}_{\mathrm{surv}}(\hat{s}_j, a_j)$, and terminal FB bootstrap $\gamma^H c_H \min_k \bar{F}_k(\hat{s}_H, \pi_\theta(\hat{s}_H, z), z)^\top z$ obeys the trajectory-tube compounding bound:
     $$
     E_{t+1} \le L E_t + (\epsilon_D + K_G \delta_t)(1 + M_t), \qquad \|\hat{g}_H - g_\infty\|_2 \le E_H^{\mathrm{head}} + \gamma^H \bigl(\epsilon_F^a K_a + \epsilon_F^s \|S_H\|_2 + L_Q \delta_H\bigr) + R_{>H}.
     $$
   - Because compounding dynamics Jacobian error grows as $L^H$ across stiff contact transitions (`compounded_state_error = 0.193` at $H=8$, `0.464` at $H=16$, `1.132` at $H=32$ on L4 GPU), **short-to-medium horizons $H \in [8, 16]$** hit the optimal bias-variance sweet spot (`cos = 0.319` at $H=8$, `0.387` at $H=16$, minimal relative $L_2$ gradient error `0.949` at $H=16$, vs degradation to `1.230` at $H=32$).
2. **Strict Zero-Future-Leakage & Stop-Gradient Contract**:
   - $W_\psi(\hat{s}_t, a_t)$ receives only causal state/observation history (with 16-step detached real-prefix burn-in) and current action $a_t$; future demonstration frames $m_{t+1..t+H}$ are strictly prohibited at inference/rollout time and appear only as offline transition targets.
   - During the actor unroll, $(\bar{B}, \bar{F}_{1,2}, W_\psi, W_u)$ hold frozen parameters (`requires_grad=False`, `eval()` mode) while preserving active input Jacobians $\partial \bar{B}/\partial \hat{s}_t$, $\partial \bar{F}/\partial \hat{s}_H$, $\partial \bar{F}/\partial a_H$, and the full closed-loop survival derivative $\frac{d}{d\theta}\log c_t = \sum_{i<t}(\partial_s \ell_i + \partial_a \ell_i \partial_s \pi_i)\frac{d\hat{s}_i}{d\theta} + \partial_a \ell_i \partial_\theta \pi_i$.
3. **Mandatory Merges Across Proposals A and B**:
   - **Merge 1 (Complete $C^1$ Tube Bound + Closed-Loop Survival Derivative from Proposal B)**: Retain state-drift term $\delta_t$, action Lipschitz factor $K_a$, terminal critic state-Jacobian error, and minibatch/ensemble variance $G_H^2 / N_H$, plus the $\partial_a \ell_i \partial_s \pi_i$ policy feedback term in survival gradients.
   - **Merge 2 (Contact-Stiffness Jacobian Guard + Ensemble Disagreement Gate from Proposal A & Reviews)**: Monitor cumulative sensitivity growth along imagined rollouts and apply backward-only horizon truncation (or route high-disagreement/high-leverage branches to the 1-step FB actor per B01 Merge 3) when cumulative Jacobian amplification exceeds $\Lambda_{\max} = 10$.
   - **Merge 3 (Complete 4-Arm + Detached-Rollout & Oracle-Substitution Controls)**: Pair Arms A ($H=0$ 1-step FB), B ($n$-step real-segment FB target with $\gamma^{n_{\mathrm{eff}}}$ terminal bootstrap at trace cuts), C (world-model multi-step $F$ target + 1-step actor derivative), and D ($H \in \{1, 4, 8, 16, 32\}$ pathwise hybrid) with a detached-rollout MVE control (isolating model step throughput `414,771 steps/s` from pathwise differentiation depth) and single-factor oracle substitutions (`E_J, E_c, E_F, E_W`).

---

## 3. Principle Claim Rulings (Appendix B.9)

- **`C-B04-A-01`**: `tighten-premises` (Stay `Candidate` Grade 2; require directional coherence $\cos(\nabla_s \bar{F} - \nabla_s V^\star, \partial \hat{s}_H/\partial \theta) \ge c_{\min} > 0$ and measure isolated critic-error vector norm).
- **`C-B04-A-02`**: `Stay Candidate` Grade 1 (Proof verified with closed-loop survival formula repair; hard boolean masks have zero pathwise gradient a.e. across contact/hazard boundaries).
- **`C-B04-A-03` / `C-B04-B-02`**: `Stay Candidate` Grade 1 (Proof verified; head/tail Bellman splice compatibility uniquely requires $M = \Sigma_{\bar{B}}^{-1}$ under full-rank $\Sigma_{\bar{B}}$; at $H=8$ on L4 GPU, B01 whitening improves hybrid gradient cosine from `0.0432` to `0.3191`, a **7.38x** gain).
- **`C-B04-B-01`**: `downgrade` (Tautological autodiff identity $g_\infty - g_H^{\mathrm{oracle}} = R_{>H}$; retained as an implementation unit test rather than a necessity claim).

---

## 4. Empirical Verification Summary (`B04-SPIKE` & NVIDIA L4 GPU)

Verified on both CPU (`packets/B04/spikes/B04-SPIKE/VERDICT.json`, `PASS`) and **Google Colab NVIDIA L4 GPU** (`gpu_experiments/colab_gpu_results_cuda.json`, `PASS`, `414,771.3` batched world-model steps/s):
- **Standard 1-step FB derivative ($H=0$)**: gradient cosine vs true long-horizon physics = **`-0.0338` (L4 GPU) / `-0.0019` (CPU)** (`rel_l2_error = 1.012`).
- **Whitened vs Unwhitened Hybrid Rollout at $H=8$**: B01 whitening boosts pathwise gradient cosine from **`0.0432` (unwhitened) to `0.3191` (whitened)** on L4 GPU (`0.0499 -> 0.4150` on CPU).
- **Horizon Sweep ($H \in \{1, 4, 8, 16, 32\}$ on L4 GPU)**:
  - $H=1$: `cos = -0.0037`, `state_err = 0.027`, `rel_l2 = 1.008`
  - $H=4$: `cos = 0.1649`, `state_err = 0.099`, `rel_l2 = 0.987`
  - $H=8$: `cos = 0.3191`, `state_err = 0.193`, `rel_l2 = 0.951`
  - $H=16$: `cos = 0.3871`, `state_err = 0.464`, `rel_l2 = 0.949` (**optimal relative $L_2$ error**)
  - $H=32$: `cos = 0.4380`, `state_err = 1.132`, `rel_l2 = 1.230` (compounding state error degrades relative $L_2$ accuracy).
