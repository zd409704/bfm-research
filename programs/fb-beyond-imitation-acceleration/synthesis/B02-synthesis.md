# Synthesis B02 — Non-Stationarity, Batch-Norm Ordering, and Off-Policy Credit Assignment in Joint FB + Task-Q + Planner Training

- **Decision ID**: `D-B02-001`
- **Packet ID**: `B02`
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
- **Adjudicators**:
  1. `agy` (`gemini-4-argon-high`, Order 1: `P=A, Q=B`): `packets/B02/adjudication-agy-order1.md`
  2. `claude` (`sonnet`, Order 2: `P=B, Q=A`): `packets/B02/adjudication-sonnet-order2.md`
- **Pre-Registered Empirical Spike**: `packets/B02/spikes/B02-SPIKE/VERDICT.json` (`PASS`) and NVIDIA L4 GPU (`gpu_experiments/colab_gpu_results_cuda.json`, `PASS`)

---

## 1. Consolidated Order-Swapped Rubric Scores

| Proposal Track | Author Model | Order 1 (`agy`: P=A, Q=B) | Order 2 (`sonnet`: P=B, Q=A) | Mean Score |
|---|---|---:|---:|---:|
| **Proposal A** (`proposals/A.md`) | `claude` Opus | `86.5 / 100.0` (Sem 26.5, Contr 21.5, Overh 17.5, Spike 21.0) | `72.0 / 100.0` (Sem 22.0, Contr 19.0, Overh 14.0, Spike 17.0) | **79.25 / 100.0** |
| **Proposal B** (`proposals/B.md`) | `codex` `gpt-6-astra` | `84.5 / 100.0` (Sem 25.5, Contr 22.5, Overh 15.0, Spike 21.5) | `77.0 / 100.0` (Sem 26.0, Contr 22.0, Overh 10.0, Spike 19.0) | **80.75 / 100.0** |

- **Disposition**: **`Tie / Hybrid Co-Design (Lead Base: Proposal B at 80.75 vs 79.25, Δ = +1.50 < 5.0 tie margin)`** combining Proposal B's exact stopped-path measure formulation, `fp32`/`.clone()` storage boundaries, and whole-episode RNN prefix retention with Proposal A's $O(d_z)$ Procrustes gauge decomposition, snapshot-free pre-clip Gaussian KL drift gate, and `< 0.5%` production FLOP budget.

---

## 2. Key Adjudication Findings & Mandatory Merges Adopted into Synthesis

1. **Structural Split Between Step Action-$Q$ ($K_{\mathrm{hold}}=1$) and Macro-$z$ Critic ($K=10$)**:
   - **Step Action-$Q$ (`baseline/04` Ball Striking v2)**: Because $Q_{\phi_1,\phi_2}(H_t^Q, a_t)$ conditions directly on the executed low-level action $a_t \in [-1,1]^{29}$ and environment transitions $P_{\mathrm{env}}(s_{t+1}\mid s_t, a_t)$ are policy-invariant, single-step transitions carry **zero replay-age policy drift bias**. Non-stationarity enters only at bootstrap target evaluation $\pi_{\bar{\theta}}(o_{t+1}^{\mathrm{low}}, P_{\bar{\psi}}(H_{t+1}^{\mathrm{plan}}))$ and actor-chain planner gradients $\nabla_\psi Q_{\phi_1}(H_t^Q, \pi_\theta(o_t^{\mathrm{low}}, P_\psi(H_t^{\mathrm{plan}})))$, which is controlled via dedicated task-only EMA $\bar{\theta}$ ($\tau_{\mathrm{task}} = 0.005$) and delayed planner updates (`delay = 2`).
   - **Macro-$z$ Critic (`baseline/05` Obstacle Traversal R2.1, $K=10$)**: $Q_{\phi_1,\phi_2}(H_t, c_t^{\mathrm{geom}}, z_{\mathrm{actual}})$ evaluates the $k$-step stopped path measure $\mathbb{P}_{\theta_{\mathrm{then}}}^{z_{\mathrm{actual}}}(\tau_{t:t+k}\mid \mathcal{H}_t)$. As $\theta$ evolves under FB updates, the executed macro label $z_{\mathrm{actual}}$ induces a drifted path distribution $\mathbb{P}_{\theta_{\mathrm{now}}}^{z_{\mathrm{actual}}}$, whereas $B_\omega$ drift alone does **not** alter the physical semantics of a fixed stored $z_{\mathrm{actual}}$ (Proposition 1.2).
2. **Exact Two-Pass Normalizer Order & Immutability Contract**:
   - Update normalizers exactly twice per FB step: once on `(obs, m_current)` and once on `(next_obs, m_next)` (`bn_clean_update_calls = 2`), then immediately switch normalizers to frozen inference (`eval()` + `no_grad()`) before querying expert frames or sampling `z_update` (`50%` online-$B_\omega(m_{\mathrm{next}}[\mathrm{perm}])$ + `50%` uniform sphere).
   - Store `behavior_z` / `z_actual` as write-once cloned tensors at rollout collection; never overwrite `behavior_z` during `z_update` relabeling and never re-encode macro-critic targets with $B_{\omega_{\mathrm{now}}}(m_{\mathrm{prompt}})$.
3. **Mandatory Merges Across Proposals A and B**:
   - **Merge 1 (Procrustes $O(d_z)$ Gauge Split from Proposal A)**: Decompose encoder drift into gauge-invariant structural deformation $\Delta_B^{\mathrm{def}} = \min_{R\in O(d_z)} \frac{1}{2d_z}\|B_{\mathrm{now}} - R B_{\mathrm{then}}\|_F^2$ and benign orthogonal rotation $\Delta_B^{\mathrm{gauge}}$.
   - **Merge 2 (FP32 Snapshot-Free Pre-Clip Gaussian KL Gate + Starvation Floor)**: Store `behavior_mu`, `behavior_log_std`, and `a_raw` in `fp32` (replacing Proposal A's `fp16` to eliminate $10^{-4}$ quantization error), gate macro replay age on pre-squash Mahalanobis / Gaussian KL rather than post-tanh Euclidean RMS (fixing Proposal B's `S-1` unit mismatch), and enforce a minimum active buffer floor $N_{\min} = 8,192$ with a task-update skip-rate cap (fixing Proposal B's `G-1` starvation blackout).
   - **Merge 3 (Shared-Prefix Deduplicated Zero-Hidden Burn-In + Whole-Episode Prefix Retention)**: Combine Proposal B's reference-counted whole-episode prefix retention from `step = 0` with Proposal A's episode-grouped prefix pass across online/target $Q$ and $P$, reducing recurrent burn-in FLOPs while achieving `4.77e-7` numerical parity against exact full-sequence evaluation (vs `0.277–0.383` error for stale cached hidden states).
   - **Merge 4 (Variable-$k$ Terminal Discounting $\gamma_{\mathrm{task}}^k$)**: Use actual elapsed sub-macro step count $k \in \{1,\dots,K\}$ (`gamma_task ** k`) on early termination (`severe_penetration` or `success`), eliminating the $(\gamma^K - \gamma^k)V$ exponent bias.

---

## 3. Principle Claim Rulings (Appendix B.9)

- **`C-B02-A-01`**: `tighten-premises` (Stay `Candidate` Grade 1; Parts (a)–(b) verified; tighten Part (c) to outcome-independent pre-transition relabeling maps $\zeta = f(\omega_t, H_t, z_{\mathrm{actual}}, m_{\mathrm{prompt}})$ after Reviewer B's outcome-dependent splitting counterexample).
- **`C-B02-A-02`**: `Stay Candidate` Grade 1 (Proof verified; exact cumulative/EMA stationary normalizer mixture bias and segment-end telescoping identity).
- **`C-B02-A-03`**: `tighten-premises` (Stay `Candidate` Grade 1; require paired task-return and contact/ball outcome interventions alongside kinematic controllability $\mathcal{C}(\alpha)$).
- **`C-B02-A-04`**: `Stay Candidate` Grade 1 (Proof verified; exact $O(d_z)$ gauge symmetry of the joint FB + $\mathcal{L}_{\mathrm{orth}}$ + whitened hybrid + macro-$Q/P$ objective).
- **`C-B02-B-01`**: `tighten-premises` (Stay `Candidate` Grade 1; restate as minimax TV bound $\sup_{\|f\|_\infty \le M}|\mathbb{E}_g f - \mathbb{E}_n f| = 2M\,\mathrm{TV}(\mathbb{P}_g^z, \mathbb{P}_n^z)$).
- **`C-B02-B-02`**: `Stay Candidate` Grade 1 (Proof verified; query-invariant prompt semantics require query-independent EMA normalizer state).

---

## 4. Empirical Verification Summary (`B02-SPIKE` & NVIDIA L4 GPU)

Verified on both CPU (`packets/B02/spikes/B02-SPIKE/VERDICT.json`, `PASS`) and **Google Colab NVIDIA L4 GPU** (`gpu_experiments/colab_gpu_results_cuda.json`, `PASS`):
- Clean two-pass BN update count: `2` (`bn_drift_under_frozen_queries = 0.0`), whereas buggy double-update + expert query pollution induces a mean bias of **`10.26` (CPU) / `10.43` (L4 GPU)**.
- In-place `behavior_z` mutation diff under `z_update` sampling: **`0.0`**.
- Coupled representation/policy drift recorded across joint updates (`step 20`: $\Delta_B = 0.666\text{ (CPU)} / 0.642\text{ (L4 GPU)}$, $\Delta_\pi = 1.697\text{ (CPU)} / 1.716\text{ (L4 GPU)}$).
- Full-prefix zero-hidden RNN burn-in matches exact sequence evaluation to **`4.77e-7` (CPU) / `5.96e-7` (L4 GPU)**, eliminating the **`0.277` (CPU) / `0.383` (L4 GPU)** stale hidden-state error.
