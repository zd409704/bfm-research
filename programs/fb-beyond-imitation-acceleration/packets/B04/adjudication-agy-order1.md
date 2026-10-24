# Cross-Family Adjudication Report: Packet B04 (Order 1)

- **Adjudicator**: Independent Cross-Family Adjudicator (`agy`, Order 1)
- **Packet**: `B04` — Pathwise World-Model Gradients vs. First-Action FB Successor Derivatives
- **Methodology**: v1.0 (§4 Step 4 & Appendix B.9)
- **Inputs Audited**: `PROGRAM_CHARTER.md`, `packets/B04/brief.md`, `anonymized/order1_P.md` (Candidate P), `anonymized/order1_Q.md` (Candidate Q), `reviews/review-B-on-A.md`, `reviews/review-A-on-B.md`, `spikes/B04-SPIKE/VERDICT.json`.

---

## 1. Eligibility Gate Check (Hard Constraints & Appendix B.5 Gates)

| Gate / Constraint | Candidate P (`order1_P.md`) | Candidate Q (`order1_Q.md`) | Technical Audit Note |
|---|---|---|---|
| **Charter HC1** (No BC / pose-tracking fallbacks) | **PASS** | **PASS** | Neither uses action MSE or pose tracking. Both maximize the Brief §3.1 hybrid objective $\hat{J}_H(\theta)$ in Arm D; synthesis must state explicitly that Brief §3.1 authorizes the $H$-step intrinsic reward head alongside the conservative FB tail. |
| **Charter HC2** (`behavior_z` vs. `z_update` separation) | **PASS (minor fix)** | **PASS** | Both enforce 50/50 frozen-BN `z_update` after two-pass BN updates. Q explicitly preserves `behavior_z` and task-$Q$ labels (§2 L151–152). P's spike (§5.3 L173) uses `B(m_demo)` for half the evaluation commands instead of online-$B$ permuted replay next-frames; must align in synthesis. |
| **Charter HC3** (Single-frame motion-only $B(m)$) | **PASS** | **PASS** | Production $B$ receives only root-relative kinematics $\kappa(s) \in \mathbb{R}^{229\text{ or }277}$. Both §5 spikes are explicitly scoped as low-dimensional mechanism/gradient verification panels. |
| **Charter HC4** (`severe_penetration` vs. `invalid`) | **PASS (minor fix)** | **PASS** | Q enforces the full contract (§2 L156: finite penetration $>0.03\text{ m}$ committed with $\Phi_{\mathrm{next}}=0$; `invalid` rejected from replay/normalizers and halts panel). P omits the normalizer-rejection and run-halt clauses and must separate smooth spike hazards from real replay collection. |
| **Charter HC5** (Verified evidence vs. claims) | **PASS** | **PASS** | Both treat `B04-SPIKE/VERDICT.json` (3.5 s CPU run) as a non-conclusive smoke check and make zero claims of learned robot competence. |
| **Brief HC1** (Zero future reference leakage in $W_\psi$) | **PASS** | **PASS** | $W_\psi(\hat{s}_t, a_t)$ takes only causal inputs. Future motion $m_{k+1}$ in P (§2.1 L67) and body positions $b_{i+1}$ in Q (§2 L126) are strictly supervised targets. |
| **Brief HC2** (Shared 4-arm substrate & dual compute) | **PASS (with mapping)** | **PASS (with mapping)** | Both share identical plants and report env steps + GPU-seconds. Both adopt the packet's 4-arm definitions (A=1-step FB, B=$n$-step real FB, C=$n$-step model FB, D=pathwise hybrid); P maps `baseline/03` §6 multi-task WM into control `D-V` (§2.4), while Q treats single-task/no-$F$ arms as optional auxiliaries (§2 L105). |
| **Appendix B.5 Gates** (Alternative, Claims, Spike) | **PASS** | **PASS** | Both provide formal rejected alternatives (§3), graded necessity claims with falsifiers (§4), and pre-registered spike protocols (§5). |

**Gate Verdict**: Both Candidate P and Candidate Q **PASS** all eligibility gates and proceed to scored adjudication.

---

## 2. Rubric-Weighted Numerical Scoring & Technical Justification

| Rubric Dimension | Weight | Candidate P | Candidate Q | Summary Justification |
|---|---:|---:|---:|---|
| **1. Mathematical Rigor of Gradient Decomposition** | 30% | **24 / 30** | **26 / 30** | Q gives exact $C^1$ sensitivity/survival recurrences and variance bounds; P identifies the critical DPG occupancy correction and $\gamma^H H \epsilon_F^s$ growth but drops trajectory-drift terms in $E_J$. |
| **2. Strict Zero-Future-Leakage Guarantee** | 25% | **21 / 25** | **23 / 25** | Both forbid future reference inputs; Q explicitly specifies 16-step detached RNN prefix burn-in, causal $o_{\mathrm{low}} = O(s)$ boundaries, and full B01 gate hysteresis/leverage rules. |
| **3. Contact Stiffness & Rollout Stability** | 25% | **21 / 25** | **17 / 25** | P provides a concrete runtime Jacobian monitor and backward-only horizon truncation ($H_{\mathrm{grad}} \le H$) tested at $k \in \{10^3, 10^4\}$; Q relies on global clipping at 10 and post-hoc validation selection. |
| **4. 4-Arm Ablation Completeness** | 20% | **17 / 20** | **15 / 20** | P isolates $E_J, E_c, E_F, E_W$ via single-factor oracle substitutions, includes `D-V` and `D-no-tail`, and sweeps $\kappa(\Sigma_B) \in \{1, 30, 300\}$; Q's $A=I$ control is collinear and fixed-start MSE biases against $H=0$. |
| **Total Score** | **100%** | **83 / 100** | **81 / 100** | **Recommend P (83/100); Alternate Q (81/100).** |

### Row-by-Row Technical Audit
1. **Mathematical Rigor of Gradient Decomposition (30% — P: 24/30, Q: 26/30)**:
   - **Candidate Q**: Derives exact forward sensitivity and adjoint recurrences on the augmented state $x=(s,c)$ (§1 L24–87), including closed-loop policy feedback $p_a A_t = p_a(K_t S_t + P_t)$ inside survival derivatives, the $(H+1)$-th terminal policy injection $P_H$ inside $\bar{Q}_F(\hat{s}_H, \pi_\theta(\hat{s}_H, z), z)$, trajectory-tube state divergence $\delta_t = \|\hat{x}_t - x_t\| \le \epsilon_0 A_t(L)$ with derivative Lipschitz constants $(K_G, K_r, K_v)$, and an explicit minibatch + ensemble variance bound (L83–87). Its primary weakness is evaluating all bounds and gates solely against the fixed-start gradient $g_\infty(s_0)$, which penalizes $H=0$ by $R_{>0}$ even under an oracle critic.
   - **Candidate P**: Contributes the crucial DPG occupancy insight (§1a–b: omitted future policy Jacobians $\sum_{k \ge 1} \gamma^k D_\theta \pi_k^\top \nabla_a Q^\star_k$ integrate to $(1-\gamma)^{-1}$ over on-policy occupancy $d^{\pi_z}_\gamma$, so Arm A's true population bias stems from $\epsilon_F^a$ plus relabeled replay mismatch $\|\rho - d^{\pi_z}_\gamma\|_{\mathrm{TV}}$, which $H$-step model rollouts shrink by $\gamma^{H+1}$) and tabulates $\gamma^H H \epsilon_F^s$ amplification across $H \in \{1, 4, 8, 16, 32\}$ at $\gamma=0.99$ (Table 1). However, P's theorem (L35) drops $\epsilon_f$, $\beta$, and $K_a$ from $E_J$, improperly absorbs terminal $Q'_s$ Jacobian error into $R'$, omits $\partial_a \ell_i \partial_s \pi_i$ in the survival chain rule (L104), omits a variance bound, and zeros out Arm B's bootstrap when $n_{\mathrm{eff}} < n$ (L85).
2. **Strict Zero-Future-Leakage Guarantee (25% — P: 21/25, Q: 23/25)**:
   - Both candidates strictly exclude future reference frames $m_{t+1..t+H}$ from $W_\psi(\hat{s}_t, a_t)$, using future kinematics solely as supervised loss targets, and both freeze $(\bar{B}, \bar{F}_{1,2}, W_\psi)$ in eval mode while retaining input Jacobians during actor unrolls.
   - **Candidate Q** explicitly separates deployable causal observations $o_{\mathrm{low}} = O(s)$ from state/belief inputs (§1 L12), specifies a 16-step detached real-prefix burn-in for partial-observability RNNs (§2 L124), states the full B01 Gram EMA ($\beta=0.01$), split-half (0.15), 200-update hysteresis, and $2\times$ 99.9% leverage routing rules (§2 L147–150), and indexes $W_u, \ell_u$ by update $u$, avoiding **Candidate P**'s symbol collision on $\ell_t$ (damping vs. survival logit) and underspecified deployable coordinate map.
3. **Contact Stiffness & Rollout Stability (25% — P: 21/25, Q: 17/25)**:
   - **Candidate P**: Directly addresses Brief §3.2's adaptive horizon requirement via per-step Jacobian monitoring ($\hat{\sigma}_t = \|\hat{A}_t v\|/\|v\|$) and backward-only horizon truncation when cumulative expansion $\prod_{i \le t} \hat{\sigma}_i > \Lambda_{\max}=10$, logging realized $H_{\mathrm{grad}} \le H$ (§2.3 L112). P also proves why hard boolean penetration masks have zero pathwise gradient a.e. (missing the boundary Dirac integral, L108) and tests two contact stiffnesses $k \in \{10^3, 10^4\}$ on a 5-DoF hopper (§5.1). (Caveat: 1-step JVP can underestimate non-normal $\|\hat{A}_t\|_{\mathrm{op}}$, and backward detachment alters earlier action weights relative to later $P_t$).
   - **Candidate Q**: Uses a 5-member MLP ensemble and a clean multiplicative survival recurrence (L140), but provides no runtime contact-stiffness truncation or adaptive horizon mechanism—relying only on global gradient norm clipping at 10 and post-hoc validation selection (L154–157), while testing a 1-D toy at a single stiffness $k=1000$ where $L \approx 10$ renders $B_H$ vacuous by $H=4$.
4. **4-Arm Ablation Completeness (20% — P: 17/20, Q: 15/20)**:
   - **Candidate P**: Cleanly decomposes gradient error via single-factor oracle substitutions ($W_\psi \to f$, $\hat{p} \to p^\star$, $\bar{F} \to Q^\star$, $W_t \to \Sigma_B^{-1}$ yielding $E_J, E_c, E_F, E_W$ across $H$, §5.3 L180), includes `D-V` (`baseline/03` §6 multi-task WM) and `D-no-tail` (Charter H3), reports both per-state and occupancy-aggregated metrics (§5.4), and sweeps calibrated $\kappa(\Sigma_B) \in \{1, 30, 300\}$. (Caveat: P trains dummy $W_\psi$ in Arms A/B to equalize model-consumption compute but omits unburdened native Arm A wall-clock).
   - **Candidate Q**: Adds a matched-segment diagnostic for Arm B/C and a 200k-step / 3,600 GPU-second online follow-up budget (L232), but its primary Arm B cuts with zero tolerance ($n_{\mathrm{eff}}=1$ a.s. on continuous actions, L115), its $A=I$ spike control on $q \in [-0.02, 0.20]$ is nearly collinear ($\cos q \approx 1$), and its C vs. D comparison confounds critic target horizon with actor pathwise depth.

---

## 3. Principle Claim Adjudication (Appendix B.9)

### Candidate P Necessity Claims (§4)
1. **`C-B04-CAND-01` (Terminal-critic state-gradient amplification — proposed Grade 2; Grade 1 envelope)**: **Tighten-premises (`Candidate` stay at Grade 2)**.
   - *Ruling*: While the envelope derivative condition $\frac{d}{dH}[\gamma^H(\epsilon_F^a + \epsilon_F^s K_a H)] \ge 0$ for $H \le 32$ whenever $\epsilon_F^s K_a \ge 0.015 \epsilon_F^a$ ($\gamma=0.99, L=1$) is algebraically valid, an increasing upper bound does not imply increasing realized error without bounding directional coherence. Tighten P3 to require positive alignment $\cos(\nabla_s \bar{F} - \nabla_s V^\star, \partial \hat{s}_H / \partial \theta) \ge c_{\min} > 0$, and replace the non-additive norm difference $\Delta_F(H) = \mathrm{relL2}(\hat{g}_D) - \mathrm{relL2}(\hat{g}_D^{F\to\star})$ with the isolated critic-error vector norm $\|\hat{g}_D(f_{\mathrm{true}}, p^\star, \bar{F}) - \hat{g}_D(f_{\mathrm{true}}, p^\star, Q^\star)\|_2 / \|g^\star\|_2$.
2. **`C-B04-CAND-02` (Soft survival is necessary for pathwise hazard avoidance — proposed Grade 1)**: **Candidate stay (Grade 1, with closed-loop formula repair)**.
   - *Ruling*: Deductively valid. Multiplying hard indicator masks $\tilde{c}_t = \prod_{j<t} \mathbf{1}[g(\hat{s}_j, a_j) > 0]$ produces $\nabla_\theta \tilde{c}_t = 0$ a.e., omitting the boundary Dirac surface integral and zeroing out pathwise hazard avoidance. Retain at Grade 1, substituting Q's complete closed-loop survival derivative (including $\partial_a \ell_i \partial_s \pi_i$) into P's §2.3 equation.
3. **`C-B04-CAND-03` (Whitening necessity is $\kappa$-conditional — inherited from B01 site (iv), proposed Grade 1)**: **Tighten-premises (`Candidate` stay at Grade 1)**.
   - *Ruling*: $\kappa(\Sigma_B) = 1$ implies $\Sigma_B = c I$ ($c > 0$). If $c \neq 1$, $W_t = I$ vs. $\Sigma_B^{-1} = c^{-1} I$ alters the head-to-tail scale ratio against $\bar{F}^\top z$, shifting gradient cosine even for isotropic features. Tighten the $\kappa=1$ premise to unit-trace $\Sigma_B = I$ and merge with Q's `C-B04-CAND-02`.

### Candidate Q Necessity Claims (§4)
1. **`C-B04-CAND-01` (Direct parameter-path coverage — proposed Grade 1)**: **Downgrade (to algebraic verification check; reject as necessity principle)**.
   - *Ruling*: Circular. Q adds the premise $R_{>H} := \mathbb{E}\sum_{t>H} \gamma^t c_t P_t^\top Q_a^{\theta_0} \neq 0$ to conclude $g_\infty - g_H^{\mathrm{oracle}} \neq 0$, which is a one-line identity ($g_\infty - g_H^{\mathrm{oracle}} = R_{>H}$). Its $10^{-6}$ falsifier tests only PyTorch autodiff mechanics, conflicts with L209's $10^{-4}$ truncation tolerance, and ignores occupancy-weighted actor updates.
2. **`C-B04-CAND-02` (Head/tail coordinate compatibility — proposed Grade 1)**: **Candidate stay (Grade 1, merged with P's `C-B04-CAND-03`)**.
   - *Ruling*: Under full-rank $\Sigma_{\bar{B}}$, exact rank-$d_z$ FB factorization, and reachable one-step expected features spanning $\mathbb{R}^{d_z}$, one-step Bellman splice identity $\mathbb{E}[\bar{B}(s')]^\top (M - \Sigma_{\bar{B}}^{-1}) z = 0 \ \forall z$ deductively forces $M = \Sigma_{\bar{B}}^{-1}$.

---

## 4. Disposition, Mandatory Merge Items & Confounds

- **Disposition**: **Recommend `P`** (`order1_P.md`, **83 / 100**); **Alternate `Q`** (`order1_Q.md`, **81 / 100**).
- **Mandatory Merge Items (from Candidate Q and blind reviews into Candidate P)**:
  1. **Exact $C^1$ Compounding Error & Variance Bound**: Replace P's incomplete $E_J$ (§1 L35) with Q's trajectory-tube recurrence $E_{t+1} = L E_t + [\epsilon_D + K_G \delta_t](1 + M_t)$ (§1 L64–81), keeping state drift $\delta_t$, action Jacobian $K_a$, separate terminal $Q'_s$ Jacobian error, and Q's minibatch + ensemble variance bound (L83–87).
  2. **Closed-Loop Survival Chain Rule**: Add the missing policy-feedback term $\partial_a \ell_i \partial_s \pi_i$ from Q (§1 L27, §2 L140) into P's survival gradient (§2.3 L104) and rename B01 ridge damping to $\ell_u$ to resolve symbol collision with survival logit $\ell_t$.
  3. **Arm B Trace-Cut Bootstrap & Matched-Segment Diagnostic**: Fix P's Arm B loss (§2.2 L85) so trace cuts at $n_{\mathrm{eff}} < n$ bootstrap at $\gamma^{n_{\mathrm{eff}}} \bar{F}(s_{n_{\mathrm{eff}}}, \pi_\theta(s_{n_{\mathrm{eff}}}, z), z)$ rather than zeroing $\bar{c}_n$, and include Q's matched-segment diagnostic (§2 L117).
  4. **Contact-Stiffness Norm Certification & Detached-Rollout Control**: Replace P's 1-step JVP heuristic with a $k$-step SVD/power bound or ensemble-disagreement gate, quantify backward-detachment bias against a fully detached $H$-step value-expansion control (isolating model throughput from pathwise depth), and log native Arm A wall-clock without dummy $W_\psi$ updates alongside the compute-equalized arm.
  5. **Full Charter/B01 Contract & Online Follow-Up**: Incorporate Q's 5-member ensemble $W_\psi$, 16-step detached RNN prefix burn-in (with start-distribution logging), full HC2/HC4 normalizer-rejection and panel-halt rules, a drifting-$B_\omega$ evaluation panel, and Q's 200k-step / 3,600 GPU-second online training follow-up (§5 L232) with pre-registered task-return gates.

### Confounds Paragraph
Three methodological confounds must be controlled before locking empirical claims on H3. First, **Fixed-Start vs. Occupancy-Aggregated Reference Bias**: evaluating actor gradients at isolated states $s_0$ against $\nabla_\theta J_\infty(s_0)$ penalizes $H=0$ for omitting future policy injections $R_{>0}$ that vanish up to $(1-\gamma)^{-1}$ scaling under on-policy occupancy $d^{\pi_z}_\gamma$; therefore, all horizon gates must report both per-state and occupancy-aggregated ($\rho$ and $d^{\pi_z}_\gamma$) metrics. Second, **Model Throughput vs. Pathwise Differentiation vs. Representation Overhead**: varying $H \in \{1, 4, 8, 16, 32\}$ simultaneously changes imagined sample volume, backpropagation depth, and B01/FB evaluation cost; isolating these requires pairing Arm D with a detached-state $H$-step rollout control, `D-V` (`baseline/03` §6), `D-no-tail`, and both dummy-model-equalized and native unburdened Arm A wall-clock accounting. Third, **Smoke-Test Artefacts in `B04-SPIKE/VERDICT.json`**: the existing 3.5 s CPU verdict exhibits an uncalibrated critic at $H=0$ ($\cos = -0.0019$) and diverging gradient scale at $H=32$ ($\mathrm{relL2} = 1.024$ despite $\cos = 0.556$), confirming it serves strictly as an execution smoke test and cannot license horizon selection prior to running the merged multi-seed protocol.
