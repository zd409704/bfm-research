# Independent Cross-Family Adjudication: Packet B03 (Order 1)

- **Adjudicator**: Independent Cross-Family Adjudicator (`agy-order1`)
- **Packet**: `B03` — Motion-Only Backward Map Aliasing and Privileged/Perceptive Compensation in Contact-Rich Tasks
- **Methodology**: v1.0 (§4 Step 4 & Appendix B.9)
- **Reviewed Artifacts**: `PROGRAM_CHARTER.md`, `packets/B03/brief.md`, `order1_P.md` (Candidate P), `order1_Q.md` (Candidate Q), `review-B-on-A.md` (Blind Critique on P), `review-A-on-B.md` (Blind Critique on Q), `B03-SPIKE/VERDICT.json`

---

## 1. Eligibility Gate Check (Hard Constraints & Appendix B.5 Gates)

| Gate / Constraint | Candidate P | Candidate Q | Audit Summary |
|---|---|---|---|
| **Charter §2.1**: No BC or pose-tracking penalty fallbacks | **PASS** | **PASS** | P updates $\pi_\theta$ via $-\min_k F_k^\top z$ (plus single-step action-$Q$ gradient $\beta>0$ at $K=1$); §5 probes are detached diagnostics. Q uses $-\mathbb{E}\min_i F_i^\top z_{\mathrm{update}}$ and fixed analytical `nn.Linear` maps in §5(b)–(c). |
| **Charter §2.2**: Strict separation of `behavior_z` vs `z_update` | **PASS** | **PASS** | Both preserve immutable `behavior_z` / $z_{\mathrm{actual}}$ in `TaskReplay` and the 50/50 sphere/permuted-$B(m_{t+1})$ relabel mixture. P omits explicit `current`$\to$`next` two-pass BN ordering in §5(a) (flagged for merge). |
| **Charter §2.3**: Single-frame motion-only $B(m)$ (`229` / `277` dims) | **PASS** | **PASS** | Both keep $B_\omega$ strictly motion-only (`m[229]` and `m[277]`). Scene/contact-augmented $B'$ is discussed only as a rejected alternative in §3 of both proposals. |
| **Charter §2.4**: `severe_penetration` vs `invalid` corruption | **PASS** | **PASS** | Both commit finite `severe_penetration` ($>0.03$ m) as terminal ($\Phi_{\mathrm{next}}=0$) and exclude `invalid` rows from replay. Q explicitly states normalizer exclusion and run/panel halt; P omits the halt clause (flagged for merge). |
| **Charter §2.5**: Verified evidence vs unproven claims | **PASS** | **PASS** | Neither claims learned traversal/striking from `VERDICT.json`. Both note `irreducible_isokinematic_multi_force_mse = 0.8953` lacks an analytic floor and normalization metadata. |
| **Brief §2**: Zero-force NPZ compatibility & no R1.3 static filter | **PASS** | **PASS** | Both preserve zero-force kinematic NPZ encoding (`qpos`/`qvel`/FK) and reject static 8-height collision admission and `infer_source_support_intent`. |
| **Appendix B.5**: Serious alternative & necessity claim schema | **PASS** | **PASS** | Both analyze serious alternatives (§3), formulate structured necessity claims with premises/conclusions/tests/falsifiers (§4), and pre-register spike protocols (§5). |

**Eligibility Verdict**: Both **Candidate P** and **Candidate Q** pass all hard constraints and Appendix B.5 gates.

---

## 2. Rubric Scoring & Row-by-Row Technical Justification

| Rubric Dimension | Weight | Candidate P | Candidate Q | Weighted Delta (P − Q) |
|---|---:|---:|---:|---:|
| 1. Compatibility with Kinematic-Only Demo NPZ | 30% | **26 / 30** | **24 / 30** | +2 |
| 2. Rigor of Aliasing Analysis | 25% | **21 / 25** | **20 / 25** | +1 |
| 3. Diagnostic Precision | 25% | **19 / 25** | **18 / 25** | +1 |
| 4. Spike Falsifiability | 20% | **16 / 20** | **13 / 20** | +3 |
| **Total Weighted Score** | **100%** | **82 / 100** | **75 / 100** | **+7** |

### Row-by-Row Justification
1. **Compatibility with Kinematic-Only Demo NPZ (30% — P: 26/30, Q: 24/30)**
   - *Candidate P*: Formalizes the exact invariance group $G_D$ of the descriptor $\Phi_D(\xi)$ ($G_{229}=\{(x,y,z,\psi)\}$ vs $G_{277}=\{(x,y,\psi)\}$ pinned by `base_height[1]`) and proves two concrete failure modes of scene/contact-augmented $B'_\omega(m,c)$: (i) *prompt-side collapse* under deterministic imputation $\bar{c}(m_{\mathrm{demo}})$ alongside uncontrolled off-support prompt leverage $B'^\top W_t B'/d_z$ (Prop. 3.1), and (ii) *exogenous-rank waste* where episode-constant $h$ yields $\nabla_a F^\top u = 0$ (on continuing rollouts) while rendering $6/7 \approx 85.7\%$ of 50/50 permuted-goal relabels unreachable across the 7-height bank (Prop. 3.2). Deducted 4 pts because Spike §5(a) must reconstruct descriptors from transformed `qpos`/`qvel` via FK rather than copying rows, and Prop. 3.2 requires non-terminating rollouts.
   - *Candidate Q*: Enforces strict demo normalizer isolation (two real-data passes only) and identifies baseline 04's schema sum discrepancy (`278` vs `277` for `m`, `107` vs `93` for `o_low`) as a pre-integration blocker. Deducted 6 pts because compatibility is preserved by omission: Q never evaluates whether NPZ-derivable finite-difference acceleration $\widehat{\ddot{q}}$ (Brief Deliverable 2c) is single-frame admissible under Charter §2.3, nor analyzes masked-context prompt distribution mismatch or cross-height relabel unreachability.
2. **Rigor of Aliasing Analysis (25% — P: 21/25, Q: 20/25)**
   - *Candidate P*: Establishes the critical distinction between *single-frame aliasing* ($B(m_t)$ coincidence) and *future occupancy aliasing* ($\Psi(o,a,z)$ coincidence), partitioning contact resolution into **Case R** (geometry-resolved via exteroception $e$ in both $\pi_\theta$ and $F$), **Case K** (kinematically distinguishable trajectories selected by planner $z$), and **Case I** (isokinematic multi-force trajectories where $\Psi^{c_1}=\Psi^{c_2}$). Proves why omitting $e$ from $F(o,a,z)$ biases $\nabla_a F^\top z$ toward the regime mixture, derives the constrained dynamics nullspace $\dim\mathcal{N}=29+n_c-\operatorname{rank}[S^\top\ J_c^\top]\ge n_c-6$ across $n_c\in\{0,6,12,15\}$, and models ball impact as $\varepsilon$-isokinematic in $O(m_b/m_{\mathrm{eff}})$. Deducted 4 pts for three overclaims identified in Review B: (i) equating instantaneous algebraic nullity $\dim\mathcal{N}$ with persistent future isokinematics while ignoring pure internal wrench redundancy ($\Delta\tau=0, J_c^\top\Delta\lambda=0$), friction-cone boundaries, and PD saturation; (ii) omitting $z_t=P_\psi(H_t)$ conditioning in Prop. 1.5's Bayes floor; and (iii) claiming zero objective preference along $n_a$ prevents $\mathcal{A}(o)$ from spanning $n_a$ (ignoring parameter coupling $J_\theta\pi J_\theta\pi^\top$ and convex-hull exposure in Case K).
   - *Candidate Q*: Formulates exact conditional-variance risk bounds $\mathbb{E}\,\mathrm{tr}\operatorname{Cov}(A^\star\mid U_t)$ conditioned on full actor input $U_t=(o_t^{\mathrm{low}},z_t)$, separates internal wrench redundancy from required actuator separation $\tau_1\ne\tau_2$, and gives the sphere-tangent local accessibility test $\delta\tau\notin\operatorname{im}(D_a T\,D_z\pi_\theta\,\Pi_z)$ with $\Pi_z=I-zz^\top/d_z$. Deducted 5 pts because it provides no observability/gradient-bias proof for $F(o_F,a,z)$, misses topological non-injectivity of $B:\mathbb{R}^{277}\to\mathcal{S}^{99}$ in ball striking ($\dim 99 < 277$), and treats future $B$-occupancy equivalence (Case I) in two qualitative sentences without contact-rank or impact-mass analysis.
3. **Diagnostic Precision (25% — P: 19/25, Q: 18/25)**
   - *Candidate P*: Provides concrete metrics and cutoffs for all three failure sources ($D_P>0.1$ via CEM on $Q_1$, $D_F<0.02$ via scan shuffling, $D_B>50\%$ nullspace torque share with probe MSE $\ge 0.8L^\star$) plus a replay autocorrelation rule $\tau_{\mathrm{dec}}$ for switching between $K=10$ and $K=1$. Deducted 6 pts because $D_P$ uses the suspect critic $Q_1(h,c,z)$ as its own oracle (confounding planner suboptimality with critic error), $D_F$'s scan shuffling induces out-of-distribution states, and $D_B$ relies on an undefined counterfactual privileged wrench and sequential elimination without an unresolved/critic-fault category.
   - *Candidate Q*: Avoids critic delusion in planner diagnosis by proposing **same-state simulator branching** over a 128-latent candidate bank per snapshot (separating actor reachability $\mathcal{R}_\theta(o)$ from $Q$ ranking correlation) and checking $F^\top z$ calibration in B01 coordinates. Deducted 7 pts because it specifies no sampling distribution or coverage calculation for 128 draws in $d_z=256$, no numeric pass/fail thresholds, and no direct positive diagnostic for Brief Deliverable 2(c) ($B(m)$ lacking velocity-response / $\widehat{\ddot{q}}$ features).
4. **Spike Falsifiability (20% — P: 16/20, Q: 13/20)**
   - *Candidate P*: Designs a multi-part falsifiable protocol in §5 with explicit numeric gates and VOID controls: $G_{229}/G_{277}$ invariance vs $q_1+10^{-3}$ and `base_height[1]` vertical shifts; 35-DoF linearized regime disambiguation including an arm withholding scan from $F$-only; SVD rank checks across $n_c\in\{0,6,12,15\}$ against $L^\star$; and a mass-ratio sweep $m_b/m_{\mathrm{eff}}\in\{10^{-3},10^{-2},10^{-1}\}$. Deducted 4 pts because §5(b)'s primary actor test trains a detached supervised MLP probe rather than an FB-trained actor ($\mathcal{L}_\pi=-F^\top z$), under-specifies the toy chain MDP transition kernel, and must fix the $\Delta\tau$ vs $2\Delta\tau$ factor-of-4 floor convention.
   - *Candidate Q*: Correctly identifies the 29-channel sum-vs-mean and $\Delta$ scaling audit required to interpret `0.8953` in `VERDICT.json`. Deducted 7 pts because its executable spike parts (a)–(c) are purely tautological algebraic unit tests (`torch.clone` equality and fixed `nn.Linear` weights verifying $\|a-v\|^2+\|a+v\|^2=2\|a\|^2+2$) that cannot fail absent floating-point bugs, while its simulator extension has no numeric pass/fail thresholds.

---

## 3. Principle Claim Adjudication (Appendix B.9)

1. **`C-B03-CAND-01` (Candidate P — Isokinematic blindness of FB-only channels, proposed Grade 1)**: **Tighten-Premises** (retain as `Candidate`, Grade 1).
   - *Mandate*: Replace P3's algebraic nullity $\dim\mathcal{N}>0$ with a **non-empty torque-projected feasible nullspace** $\mathcal{N}_\tau=\{\Delta\tau\ne 0:\exists\Delta\lambda\in\mathcal{K}_{\mathrm{fric}}\text{ s.t. }S^\top\Delta\tau+J_c^\top\Delta\lambda=0\}$ over a multi-step horizon with identical future $B$-occupancy $\Psi^{c_1}=\Psi^{c_2}$ and unsaturated PD gains. Condition P4's Bayes floor on full actor input $U_t=(o_{\mathrm{low}},z_t)$, separate *information absence* in $U_t$ from *objective indifference* ($\mathbb{E}[\nabla_\theta\mathcal{L}_\pi]\perp K_p^{-1}\mathcal{N}_\tau$ on equal-occupancy branches), and test Falsifier 2 against an exact occupancy oracle rather than learned-$F$ approximation noise.
2. **`C-B03-CAND-02` (Candidate P — Perceptive sufficiency for geometry-resolved aliasing, proposed Grade 2)**: **Tighten-Premises** (retain as `Candidate`, Grade 2 empirical sufficiency claim).
   - *Mandate*: Explicitly include the 4th contact-oracle reference arm in the ablation design, require convex-hull exposure when Case K co-occurs, replace non-overlapping marginal 95% Wilson intervals with a paired seed-level confidence interval on the $\le 10$ pp gap, and validate $D_P$ via simulator rollout branching.
3. **`C-B03-CAND-03` (Candidate P — Prompt-side impossibility of augmented $B'$, proposed Grade 1)**: **Stay** (`Candidate`, Grade 1).
   - *Mandate*: Deductively valid under Prop. 3.1 for deterministic imputation $\bar{c}(m_{\mathrm{demo}})$ on zero-force kinematic NPZs; append Review A's masked-context train/prompt distribution mismatch corollary.
4. **`C-B03-CAND-01` (Candidate Q — Information separation necessity for contact commands, proposed Grade 1)**: **Tighten-Premises** (retain as `Candidate`, Grade 1; merge into P's `CAND-01`).
   - *Mandate*: Retitle to *"Distinguishing causal information in $U_t=(o_t^{\mathrm{low}},z_t)$ is necessary for incompatible torque commands"*. Its conditional-variance bound $\mathbb{E}\|\hat{\tau}-\tau_C\|^2\ge\Delta^2/4$ supplies the exact $U_t$-conditioning needed by P's `CAND-01`, while its operational test must check whether real simulator contact snapshots violate the equal-$U_t$ premise rather than testing an algebraically impossible falsifier.
5. **`C-B03-CAND-02` (Candidate Q — Context sufficiency requires action availability, proposed Grade 1)**: **Downgrade** (reclassify as a §1 Representability Proposition).
   - *Mandate*: Set-theoretic fiber consistency ($\bigcap_{(x,\iota):U=u}\mathcal{A}^\star(x,\iota)\ne\varnothing$) plus latent image intersection ($\mathcal{R}_\theta(o_{\mathrm{low}})\cap\mathcal{A}^\star\ne\varnothing$) is a definitional representability lemma for deterministic functions, not a falsifiable necessity claim about FB learning. Merge its sphere-tangent Jacobian test into §1.

---

## 4. Disposition, Mandatory Merge Items & Confounds

- **Recommend**: **`P`** (Candidate P / Primary Author A — **82 / 100**)
- **Alternate**: **`Q`** (Candidate Q / Primary Author B — **75 / 100**)

### Mandatory Merge Items from Alternate (Q) & Blind Reviews into Recommended Track (P)
1. **Torque-Projected Nullspace, Saturation Masking & $U_t$-Conditioned Bayes Floor (from Q §1 & Review B)**:
   - Reformulate Prop. 1.5 around the torque-projected feasible nullspace $\operatorname{proj}_\tau(\mathcal{N}\cap\mathcal{K}_{\mathrm{fric}})$, excluding self-equilibrating internal contact forces ($\Delta\tau=0, J_c^\top\Delta\lambda=0$).
   - Mask clipped/saturated actuator channels before computing Q's local tangent-space rank diagnostic $\delta\tau\notin\operatorname{im}(D_a T\,D_z\pi_\theta\,\Pi_z)$ with $\Pi_z=I-zz^\top/d_z$.
   - Condition the Bayes risk floor explicitly on full actor input $U_t=(o_t^{\mathrm{low}},z_t)$.
2. **Same-State Simulator Branching & Direct Deliverable 2(c) Probe (from Q §5 & Reviews A/B)**:
   - Replace $D_P$'s critic-only CEM gap with Q's same-state simulator branching over a 128-latent candidate bank (64 local von Mises–Fisher perturbations around $P_\psi(h_t)$, 32 demo prompts $B(m_{\mathrm{demo}})$, 32 uniform sphere draws, evaluated with common random numbers) to decouple actor reachability $\mathcal{R}_\theta(o)$ from $Q_1$ ranking error.
   - Replace $D_F$'s scan shuffling with feasible paired scene interventions and retrained context-masked arms.
   - Add Review A's direct Deliverable 2(c) diagnostic comparing motion-only $B(m)$ against a causal finite-difference acceleration probe ($\widehat{\ddot{q}}$) on paired impact branches, plus an explicit unresolved/critic-fault attribution bucket.
3. **2×2 Learned FB Spike & `VERDICT.json` Normalization Gate (from Q §5 & Review A)**:
   - Incorporate Q's explicit 29-channel sum-vs-mean and $\Delta\tau$-vs-$2\Delta\tau$ scaling audit as a pre-lock check to reconcile `irreducible_isokinematic_multi_force_mse = 0.8953`.
   - Reconstruct Spike §5(a) features via full `qpos`/`qvel` FK transforms under Charter §2.2's two-pass BN order (`current`$\to$`next`, then frozen BN).
   - Upgrade Spike §5(b) from a detached supervised MLP probe to a compute-matched $2\times 2$ learned FB spike (`{motion-only B, B + causal \hat{\ddot{q}}} × {perceptive F/\pi, context-masked F/\pi}`) trained exclusively with $\mathcal{L}_\pi = -\min_i F_i^\top z_{\mathrm{update}}$.
4. **Baseline 04 Schema Reconciliation, AAMC Option-Consistency & Invalid-Physics Halt (from Q §1–§2 & Review B)**:
   - Log baseline 04's field-sum mismatch (`278` vs `277` for `m` and `107` vs `93` for `o_low`) as a pre-integration gate.
   - Enforce Charter §2.4's normalizer-update exclusion and mandatory run/panel halt on `invalid` physics.
   - Restrict AAMC ($Q_\phi(h,c^{\mathrm{geom}},z,\alpha)$) to an explicit ablation arm until off-support planner differentiation $\nabla_z Q_\phi(h,c,z,\pi_\theta(o,z))$ is validated against standard Design 1 ($K=10$) and Design 2 ($K=1, \beta\in\{0,>0\}$).

### Confounds
Three potential confounds were controlled during adjudication:
- **Formalism vs. Caveat Density**: Candidate P writes in compact theorem-proof notation with sharp architectural proposals (Case R/K/I, AAMC, numeric spike cutoffs) that expose surface area to technical counterexamples, whereas Candidate Q writes defensive prose caveats and reduces executable spike steps (a)–(c) to tautological float64 identities. P was penalized for every overclaim where algebraic nullity or detached probes exceeded their premises, while Q was credited for its exact conditional-variance conditioning but penalized for tautological spike tests and omitting $F$-observability proofs.
- **Reviewer Asymmetry**: Blind Review B on P was exceptionally thorough on contact mechanics and optimization dynamics, while Blind Review A on Q sharply identified topological non-injectivity ($277\to\mathcal{S}^{99}$) and missing $F$-conditioning analysis; cross-applying both standards confirmed P's +7 point structural lead.
- **Pre-Existing `VERDICT.json` Anchoring**: Both candidates read the 3-metric smoke output (`0.0`, `0.00033`, `0.8953`); neither over-claimed task learning, and merging Q's normalization audit with P's multi-regime dynamics test yields a self-contained, falsifiable protocol.
