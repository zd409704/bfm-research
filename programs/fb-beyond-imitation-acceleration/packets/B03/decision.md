# Packet B03 Decision — Motion-Only Backward Map Aliasing and Privileged/Perceptive Compensation in Contact-Rich Tasks

- **Decision ID**: `D-B03-001`
- **Packet ID**: `B03`
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
- **Adjudicators**:
  1. `agy` (`gemini-4-argon-high`, Order 1: `P=A, Q=B`): `packets/B03/adjudication-agy-order1.md`
  2. `claude` (`sonnet`, Order 2: `P=B, Q=A`): `packets/B03/adjudication-sonnet-order2.md`
- **Pre-Registered Empirical Spike**: `packets/B03/spikes/B03-SPIKE/VERDICT.json` (`PASS`) and NVIDIA L4 GPU (`gpu_experiments/colab_gpu_results_cuda.json`, `PASS`)

---

## 1. Consolidated Order-Swapped Rubric Scores

| Proposal Track | Author Model | Order 1 (`agy`: P=A, Q=B) | Order 2 (`sonnet`: P=B, Q=A) | Mean Score |
|---|---|---:|---:|---:|
| **Proposal A** (`proposals/A.md`) | `claude` Opus | `82.0 / 100.0` (NPZ 26, Alias 21, Diag 19, Spike 16) | `68.0 / 100.0` (NPZ 24, Alias 16, Diag 16, Spike 12) | **75.0 / 100.0** |
| **Proposal B** (`proposals/B.md`) | `codex` `gpt-6-astra` | `75.0 / 100.0` (NPZ 24, Alias 20, Diag 18, Spike 13) | `70.0 / 100.0` (NPZ 24, Alias 20, Diag 14, Spike 12) | **72.5 / 100.0** |

- **Disposition**: **`Tie / Hybrid Co-Design (Lead Base: Proposal A at 75.0 vs 72.5, Δ = +2.50 < 5.0 tie margin)`** combining Proposal A's Case R / Case K / Case I occupancy aliasing trichotomy, $F(o_F,a,z)$ regime-mixture gradient-bias proof, and 85.7% cross-height relabeling waste theorem with Proposal B's exact $U_t = (o_t^{\mathrm{low}}, z_t)$-conditioned Bayes variance floor, torque-projected feasible contact nullspace, and 128-latent same-state simulator branching diagnostic.

---

## 2. Key Adjudication Findings & Mandatory Merges Adopted into Synthesis

1. **Exact Aliasing Boundary & Three-Regime Trichotomy (`Case R / Case K / Case I`)**:
   - **Single-Frame Descriptor Invariance**: Under single-frame kinematic descriptors $m \in \mathbb{R}^{229}$ (`G_229 = {(x,y,z,\psi)}`) and $m \in \mathbb{R}^{277}$ (`G_277 = {(x,y,\psi)}` pinned by `base_height[1]`), identical body postures across free-air flight, compliant `0.40` m box support, and rigid `0.60` m face impact map to identical $B(m)$ vectors (`0.0` $B$-space separation).
   - **Case R (Perceptively Resolvable Transition Aliasing)**: When distinct contact/terrain regimes $c_1 \neq c_2$ share current kinematics $m_t$ but induce distinct action-dependent next-frame kinematic distributions $P(m_{t+1}\mid s_t, a, c)$ and are distinguishable in $U_t = (o_t^{\mathrm{low}}, z_t)$, feeding perceptive context (`scan[S]`, `ball_state[9]`, proprioceptive history) exclusively into $F(o_F, a, z)$, $\pi_\theta(o_{\mathrm{low}}, z)$, $P_\psi(H)$, and $Q_\phi(H, \cdot)$ is **both necessary and sufficient** to recover optimal regime-specific actions. Crucially, $F(o_F, a, z)$ must also receive exteroceptive context $e_t$; otherwise $\nabla_a F(o, a, z)^\top z$ averages over the posterior $p(c\mid o, a, z)$ and biases the actor toward regime-averaged actions.
   - **Case K (Kinematic Goal Ambiguity)**: Different regimes require distinct future kinematic trajectories; resolved by high-level planner $P_\psi(H_t)$ selecting regime-appropriate $z_t \in \mathcal{S}^{d_z-1}(\sqrt{d_z})$ when target occupancies are exposed on the convex hull of $\Psi$.
   - **Case I (Irreducible Isokinematic Multi-Force Bottleneck)**: When two contact regimes admit a non-empty **torque-projected feasible nullspace** $\mathcal{N}_\tau = \{\Delta\tau \neq 0 : \exists \Delta\lambda \in \mathcal{K}_{\mathrm{fric}} \text{ s.t. } S^\top \Delta\tau + J_c^\top \Delta\lambda = 0\}$ along equal future kinematic occupancy $\Psi^{c_1} = \Psi^{c_2}$ and indistinguishable $U_t = (o_t^{\mathrm{low}}, z_t)$, any deterministic policy $\pi_\theta(U_t)$ suffers an irreducible Bayes action MSE lower bound $\mathbb{E}\|\pi_\theta(U_t) - a^\star\|_2^2 \ge \mathbb{E}\,\operatorname{tr}\operatorname{Cov}(A^\star \mid U_t)$ (`0.8953` CPU / `0.9105` L4 GPU).
2. **Why Contact/Scene-Augmented $B'(m, c)$ Is Rejected**:
   - **Prompt-Side Collapse on Zero-Force Demo NPZs (Prop. 3.1)**: Because `prepare_data.py` has only kinematic `qpos`/`qvel`/FK, any deterministic imputation $\bar{c}(m_{\mathrm{demo}})$ collapses $B'(m, \bar{c}(m))$ back onto the same $m$-fibers while driving demo prompts out of replay support (inflating B01 leverage $B'^\top W_t B'/d_z$).
   - **Exogenous-Rank Waste Under 50/50 Off-Policy Relabeling (Prop. 3.2)**: Encoding episode-constant obstacle height $h$ into $B'$ makes $6/7 \approx 85.7\%$ of permuted $m_{\mathrm{next}}$ goal relabels across the 7-height pool physically unreachable within the current episode.
3. **Mandatory Merges Across Proposals A and B**:
   - **Merge 1 (Torque-Projected Nullspace & $U_t$-Conditioned Bayes Floor from Proposal B)**: Exclude self-equilibrating internal contact forces ($\Delta\tau = 0, J_c^\top \Delta\lambda = 0$), mask saturated PD channels in the sphere-tangent accessibility test $\delta\tau \notin \operatorname{im}(D_a T\,D_z \pi_\theta\,\Pi_z)$, and condition the Bayes lower bound on full actor input $U_t = (o_t^{\mathrm{low}}, z_t)$.
   - **Merge 2 (Same-State 128-Latent Simulator Branching + Paired Scene Interventions)**: Replace Proposal A's critic-only CEM gap $D_P$ with Proposal B's same-state simulator branching over a 128-latent bank (64 local vMF perturbations around $P_\psi(h_t)$, 32 demo prompts, 32 uniform sphere draws) so critic delusion is separated from actor reachability $\mathcal{R}_\theta(o_{\mathrm{low}})$.
   - **Merge 3 (2×2 Learned FB Factorial & Causal $\widehat{\ddot{q}}$ Probe)**: Evaluate `{motion-only B(m), B(m) + causal finite-difference acceleration}` $\times$ `{perceptive F/\pi, context-masked F/\pi}` under the pure FB actor loss $-\min_i F_i^\top z_{\mathrm{update}}$, and record `baseline/04`'s `278 vs 277` / `107 vs 93` field-sum discrepancy as a pre-integration schema check.

---

## 3. Principle Claim Rulings (Appendix B.9)

- **`C-B03-A-01`**: `tighten-premises` (Stay `Candidate` Grade 1; formulate over torque-projected feasible nullspace $\mathcal{N}_\tau$ with equal future $B$-occupancy $\Psi^{c_1} = \Psi^{c_2}$ and condition Bayes floor on $U_t = (o_{\mathrm{low}}, z_t)$).
- **`C-B03-A-02`**: `tighten-premises` (Stay `Candidate` Grade 2; include 4th contact-oracle reference arm and paired seed-level CI).
- **`C-B03-A-03`**: `Stay Candidate` Grade 1 (Proof verified; prompt-side impossibility of deterministic contact imputation $\bar{c}(m_{\mathrm{demo}})$ on zero-force NPZs).
- **`C-B03-B-01`**: `tighten-premises` (Stay `Candidate` Grade 1, merged with `C-B03-A-01`; conditional variance lower bound $\mathbb{E}\|\hat{\tau} - \tau_C\|_2^2 \ge \Delta^2 / 4$ under indistinguishable $U_t$).
- **`C-B03-B-02`**: `downgrade` (Definitional set-theoretic fiber representability lemma; merged into §1 observability propositions).

---

## 4. Empirical Verification Summary (`B03-SPIKE` & NVIDIA L4 GPU)

Verified on both CPU (`packets/B03/spikes/B03-SPIKE/VERDICT.json`, `PASS`) and **Google Colab NVIDIA L4 GPU** (`gpu_experiments/colab_gpu_results_cuda.json`, `PASS`):
- Kinematic-only $B(m)$ contact aliasing across distinct contact/friction regimes with identical kinematics: **`b_space_kinematic_aliasing_max_diff = 0.0`**.
- Perceptive context disambiguation in $\pi_\theta(o_{\mathrm{low}}, z)$ (Case R): action MSE reduced to **`3.31e-4` (CPU) / `6.80e-4` (L4 GPU)**.
- Irreducible isokinematic multi-force bottleneck when external wrench is unobserved (Case I): **`0.8953` (CPU) / `0.9105` (L4 GPU)**, matching the theoretical conditional-variance lower bound.
