# Independent Cross-Family Adjudication Report: Packet B01 (Order 1)

**Adjudicator**: Independent Cross-Family Adjudicator (`agy-order1`)
**Packet ID**: `B01` — FB Density Factorization, Gram Matrix Conditioning, and Intrinsic Reward Identifiability
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`, §4 Step 4 & Appendix B.9)
**Inputs Audited**:
1. `/srv/claude/research/fb-beyond-imitation-acceleration/PROGRAM_CHARTER.md`
2. `/srv/claude/research/fb-beyond-imitation-acceleration/packets/B01/brief.md`
3. **Candidate P**: `/srv/claude/research/fb-beyond-imitation-acceleration/packets/B01/anonymized/order1_P.md` (Primary Author A)
4. **Candidate Q**: `/srv/claude/research/fb-beyond-imitation-acceleration/packets/B01/anonymized/order1_Q.md` (Primary Author B)
5. **Blind Critique on P**: `/srv/claude/research/fb-beyond-imitation-acceleration/packets/B01/reviews/review-B-on-A.md`
6. **Blind Critique on Q**: `/srv/claude/research/fb-beyond-imitation-acceleration/packets/B01/reviews/review-A-on-B.md`

---

## 1. Eligibility Gate Check (Hard Constraints & Appendix B.5 Gates)

Both candidates were audited against the five Hard Technical Constraints of `PROGRAM_CHARTER.md` (§2), the three Packet Hard Constraints of `packets/B01/brief.md` (§2), and the Method v1.0 Appendix B.5 / §11.5 structural gates (serious rejected alternatives and properly structured `Candidate` necessity claims).

| Gate / Constraint | Candidate P (`order1_P.md`) | Candidate Q (`order1_Q.md`) | Technical Audit Note |
|---|---|---|---|
| **Charter §2.1**: No behavioral cloning (`\|a - a_demo\|^2`) or per-frame pose-tracking penalty fallbacks | **PASS** | **PASS** | Neither candidate introduces action-MSE or pose-tracking rewards. *Adjudicator ruling on Review B-on-A §1*: Reviewer B flagged P's hybrid world-model + $\bar{F}$ actor objective as a `[CRITICAL]` violation of Charter §2.1's literal phrasing. That objection is **overruled**: Charter §1.3, Charter §3 (H3), and Brief B01 §1(c)/§3(2)(iii) explicitly mandate analyzing the multi-step hybrid world-model + FB terminal bootstrap objective, and Q (§2.2 Step 7, §2.4) specifies the exact same hybrid objective. Charter §2.1 forbids imitation/tracking fallbacks, not H3 hybrid rollouts. |
| **Charter §2.2**: Strict separation of rollout `behavior_z` and FB relabel `z_update`; two-pass BN order; $Q$ trained on `z_actual` | **PASS** | **PASS** | Both P (§2.2–2.3) and Q (§2.2 Steps 2–3, §2.3) preserve the exact two-pass BN update-then-freeze schedule, keep `z_update` unwhitened under the 50/50 uniform-sphere / online-$B$ mixture, never overwrite `behavior_z`, and isolate the task critic $Q$ to `z_actual`. |
| **Charter §2.3**: Single-frame motion-only backward input ($D \in \{229, 277\}$) | **PASS** | **PASS** | Both candidates restrict $B(m)$ and $\bar{B}(\hat{m})$ strictly to single-frame root-relative motion descriptors without obstacle height, terrain scan, ball state, task phase, or frame indices. |
| **Charter §2.4**: Strict separation of physical failure (`severe_penetration`) vs numerical corruption (`invalid`) | **PASS** *(with minor defect)* | **PASS** *(with minor defect)* | Both include committed `severe_penetration` rows in $\rho$ and exclude `invalid` rows prior to normalizer/tracker updates. *Defects penalized in rubric*: P's `SigmaTracker` (§2.1) permits one non-finite/trace failure (`fail < 2`) before raising `FloatingPointError`, and Q (§2.1) writes that non-finite input "aborts that update and triggers inspection" rather than immediately halting the run/panel. Neither violates replay quarantine, and both are tightened in the Mandatory Merge. |
| **Charter §2.5**: Strict separation of verified evidence vs unproven claims | **PASS** | **PASS** | Neither claims learned traversal/striking or baseline superiority. P's §0 float64 NumPy check is explicitly scoped to closed-form algebraic identities (though its reported numbers in §1.2 contain a calculation bug penalized in §2 below). |
| **Brief §2.1**: Preserve bilinear interface $F(o,a,z)^\top B(m)$ and spherical norm $\sqrt{d_z}$ | **PASS** | **PASS** | Both leave the bilinear FB density loss and $\sqrt{d_z}$ sphere projection unmodified, applying $\widehat{\Sigma}_B$ correction at reward readouts. |
| **Brief §2.2**: No supervised demonstration tracking losses or per-frame phase clocks | **PASS** | **PASS** | Fully respected by both candidates. |
| **Brief §2.3**: Causal, bounded memory/compute ($d_z \in \{100, 256\}$), explicit target EMA $(\bar{F}, \bar{B})$ interaction | **PASS** | **PASS** | Both specify detached FP64 EMA Gram trackers on target $\bar{B}(m_{\mathrm{next}})$ with $O(Nd^2 + d^3)$ update compute and $\le 1.3$ MB buffer state. |
| **Appendix B.5 / §11.5 Gate**: Serious alternatives considered & rejected; principle claims in Appendix B format with `Candidate` status | **PASS** | **PASS** | Both analyze two serious alternatives (hard forward-pass whitening inside $B$ and adaptive $\lambda_{\mathrm{orth}}$ dual ascent) with mathematical counterexamples, and format all necessity claims as `Candidate` with explicit premises, grades, operational tests, and falsifiers. |

**Eligibility Verdict**: **Both Candidate P and Candidate Q PASS all eligibility gates** and advance to full rubric scoring.

---

## 2. Rubric Scoring and Technical Justification

Scores are assigned according to the pre-agreed rubric in `packets/B01/brief.md` (§4).

| Rubric Dimension | Weight | Candidate P Score | Candidate Q Score |
|---|---:|---:|---:|
| **1. Exact Mathematical Derivation** | 30% | **22.0 / 30.0** | **28.0 / 30.0** |
| **2. Stability Under Non-Stationary $\rho$** | 25% | **18.0 / 25.0** | **21.0 / 25.0** |
| **3. Compatibility with UFO Update Contract** | 25% | **21.0 / 25.0** | **24.0 / 25.0** |
| **4. Spike Falsifiability** | 20% | **14.0 / 20.0** | **15.0 / 20.0** |
| **TOTAL** | **100%** | **75.0 / 100.0** | **88.0 / 100.0** |

---

### Row-by-Row Technical Justification

#### 1. Exact Mathematical Derivation (Weight: 30% — Candidate P: 22.0/30, Candidate Q: 28.0/30)

- **Candidate P (22.0 / 30.0)**:
  - *Strengths*:
    1. Formulates a clear feature-space ($\Psi, B(y), z=B(g)$) versus dual-space ($F = \Sigma^{-1}\Psi$) typing rule (§1.4) that immediately explains why $z = \Sigma^{-1}B(g)$ inserts a second inverse ($\Sigma^{-2}B(g)$) and worsens goal alignment.
    2. Derives the closed-form uniform-$z$ relative reward MSE $\mathrm{relMSE} = 1 - \lambda_H$ and population cosine $\cos_{\mathrm{pop}} = \sqrt{\lambda_H}$ in terms of the harmonic-mean eigenvalue $\lambda_H = d/\operatorname{tr}(\Sigma^{-1})$ (Eqs. 1.6–1.7), alongside the local Taylor expansion $\mathrm{relMSE} \approx 2\log(d/\operatorname{erank}(\Sigma_B))$ and global counterexamples showing why $\operatorname{erank}$ is a collapse detector rather than a sufficient statistic for inverse error (§1.3 Eq. 1.10).
    3. Identifies the exact mechanism behind Charter H1 (§1.3): under spherical projection $\|B(x)\|_2 = \sqrt{d}$, $\mathcal{L}_{\mathrm{orth}}$ in expectation penalizes $\frac{1}{2}\sum_i (\lambda_i - 1)^2$, which charges at most $\frac{1}{2}$ for a completely collapsed direction $\lambda_d \to 0$, whereas the intrinsic reward error $\sum_i (\lambda_i - 1)^2/\lambda_i$ diverges as $1/\lambda_d$.
  - *Technical Deductions (-8.0 pts)*:
    1. **False numerical verification in §1.2 (Critical arithmetic bug confirmed)**: Candidate P claims in §0 and §1.2 (lines 56, 70) to have verified Eq. 1.3 and Eq. 1.5 in float64 NumPy, reporting that at $\kappa = 28.3$ the Kantorovich lower bound $\frac{2\sqrt{\kappa}}{1+\kappa}$ is $0.18799$ (with reciprocal overshoot $5.32$), and at $\kappa = 96$ the bound is $0.10205$ (with reciprocal overshoot $9.80$). In fact, at $\kappa = 28.3$, $\frac{2\sqrt{28.3}}{29.3} = 0.363125$ and its reciprocal is $2.75388$; at $\kappa = 96$, $\frac{2\sqrt{96}}{97} = 0.202020$ and its reciprocal is $4.95001$. Author A mistakenly computed $\sqrt{\kappa} = 5.3198$ ($\kappa=28.3$) and $\sqrt{\kappa} = 9.7980$ ($\kappa=96$) and their reciprocals $1/\sqrt{\kappa} = 0.18798$ and $0.10206$ instead of $\frac{2\sqrt{\kappa}}{1+\kappa}$ and $\frac{1+\kappa}{2\sqrt{\kappa}}$.
    2. **Non-commutative matrix algebra error in `C-B01-CAND-01(c)`**: Writes the general-$M$ $H$-step hybrid splice bias (line 314) as $\Psi_H^\top(\Sigma M - I)\Sigma^{-1}z$. Because $\Psi_H^\top M z - \Psi_H^\top \Sigma^{-1} z = \Psi_H^\top(M - \Sigma^{-1})z = \Psi_H^\top(M\Sigma - I)\Sigma^{-1}z$, P's formula is wrong whenever $M$ and $\Sigma$ do not commute.
    3. **Conflation of whole-sphere maximization with attainable manifold self-identification (§1.2 Eq. 1.5 & `C-B01-CAND-02`)**: P maximizes $u^\top \Sigma^{-1} B(g)$ over all $u \in \mathcal{S}^{d-1}(\sqrt{d})$ and concludes that $k_\Sigma(y,g) = B(y)^\top \Sigma^{-1} B(g)$ fails self-identification whenever $\kappa > 1$. As Reviewer B proved, the attainable embedding set $B(\mathcal{X}) \subset \mathcal{S}^{d-1}(\sqrt{d})$ need not contain the Kantorovich extremizer: on orthogonal prototypes $B(x_i) = \sqrt{d} e_i$ with unequal replay probabilities $\rho_i$ ($\kappa > 1$), every attainable $B(g)$ is an eigenvector of $\Sigma^{-1}$, $\theta_{\mathrm{mis}}(g) = 0$, and $k_\Sigma(y,g) = \delta_{y,g}/\rho(g)$ uniquely identifies $g$. Moreover, under exact rank-$d$ FB, $F(s,a,z)^\top B(g)$ is already the unbiased relative successor density $m_z(s,a,g)$ for point reward $\mathbf{1}_{y=g}/\rho(g)$, whereas $\Sigma$-colouring changes the task to cosine similarity $B(y)^\top B(g)$.
    4. **Omission of representation-factorization residual $h = \Psi - \Sigma F$**: All derivations assume exact P-FB ($\Psi = \Sigma F$) without analyzing how $\Sigma^{-1}$ amplifies approximation residuals $h \neq 0$.

- **Candidate Q (28.0 / 30.0)**:
  - *Strengths*:
    1. Every equation (1)–(13) and counterexample in Candidate Q was independently checked in FP64 by Reviewer A and by this adjudicator with **zero algebraic or arithmetic errors**.
    2. Cleanly separates the three readouts in §1.1 ($f^\top b_g = q^\top \Sigma^{-1} b_g$, $q^\top b_g = f^\top \Sigma b_g$, and $f^\top \Sigma^{-1} b_g$) and proves that for an in-support point reward $r_g(x) = \mathbf{1}_{x=g}/\rho(g)$, $z_g = \mathbb{E}_\rho[B(x)r_g(x)] = B(g)$ holds **exactly**, so the standard FB single-goal density readout $F(s,a,z)^\top B(g)$ suffers no covariance-induced bias.
    3. Explicitly distinguishes the one-step reward MSE under uniform spherical commands ($\mathbb{E}_z E_z = \sum_i \lambda_i^{-1} - d$) from that under replay-distributed goal commands $z = b_g$ ($\mathbb{E}_g E_{b_g} = \sum_i (\lambda_i - 1)^2$) in §1.2 Eq. (4).
    4. Derives the sharp Kantorovich cosine bound (Eq. 5), explicit Rényi-2 entropy lower bounds connecting effective rank $R = \operatorname{erank}(\Sigma)$ to Frobenius error $\sum_i (\lambda_i - 1)^2 \ge d^2/R - d$ and reward MSE $\mathbb{E}_z E_z \ge (d^2/R - d)/b_\kappa$ (Eq. 7), and an exact actor-gradient Jacobian analysis (Eq. 8) with a concrete 2D counterexample ($\Sigma = \operatorname{diag}(1.5, 0.5), z = (1,1), J = (1,-2)^\top \implies \cos(g, \tilde{g}) = -1$) proving that $\kappa$ and $R$ alone cannot bound policy-gradient cosine without critic-Jacobian structure.
    5. Explicitly incorporates the approximate-factorization residual $h = q - \Sigma f$ (showing that exact whitening yields return $f^\top z + h^\top \Sigma^{-1} z$, potentially amplifying $h$), the resolvent perturbation bound (Eq. 10), and the rank-deficient support projector $P = \Sigma\Sigma^+$ (§1.5).
  - *Technical Deductions (-2.0 pts)*:
    1. The Pinsker-derived upper-bound leg $d\sqrt{\frac{1}{2}\log(d/R)}$ in $\epsilon(\kappa, R)$ (Eq. 6) is vacuous at $d \in \{100, 256\}$ unless $R/d > 1 - 2/d^2$, and the worst-case norm bound in Eq. (13) carries a conservative factor $\sqrt{d}\|z\| = d$.
    2. Eq. (13) omits the $O(\tau)$ cross-coordinate lag term $\|W_t\|\|z_{\mathrm{online}} - z_{\mathrm{target}}\|$ arising when online-encoded prompts $z$ multiply the target-coordinate matrix $W_t$.

---

#### 2. Stability Under Non-Stationary $\rho$ (Weight: 25% — Candidate P: 18.0/25, Candidate Q: 21.0/25)

- **Candidate P (18.0 / 25.0)**:
  - *Strengths*:
    1. Causal FP64 EMA covariance tracker (`SigmaTracker`) initialized at $I_d$ (matching the exact spherical trace prior $\operatorname{tr}(\Sigma)=d$ with zero warmup discontinuity), updated once per step on target $\bar{B}(m_{\mathrm{next}})$ after BN freeze, and applying $W^{(t-1)}_\mu$ from strictly prior batches.
    2. Eigenvalue clamping (`lam.clamp_min(0.0)`) plus relative damping $\mu_t = \max(\mu_0, \hat{\lambda}_1/\kappa_{\mathrm{cap}})$ guarantees $\kappa(\widehat{\Sigma} + \mu_t I) \le \kappa_{\mathrm{cap}} + 1$ and prevents matrix-inversion blowup under rank deficiency.
    3. Identifies the reward-hacking vulnerability where a differentiable world model drives imagined states $\hat{y}$ into near-null eigendirections of $\widehat{\Sigma}$, and introduces the per-state leverage diagnostic $\ell(\hat{y}) = \bar{B}(\hat{y})^\top W \bar{B}(\hat{y}) / d$ (§2.3 iv).
  - *Technical Deductions (-7.0 pts)*:
    1. **Unbounded absolute gain in rank-deficient regimes**: Because $\mu_t = \max(10^{-3}, \hat{\lambda}_1/10^3)$ only caps the relative condition number at $10^3$, when $\hat{\lambda}_d \to 0$ and $\hat{\lambda}_1 \approx 1$, $\|W_t\|_2 = 1/\mu_t$ reaches $1000$ (compared to Q's hard gain cap of $20$), allowing massive amplification of representation or estimation errors in near-null directions.
    2. **Truncation bias in the off-support leverage guard**: When $\ell(\hat{y}_t)$ exceeds the threshold, P masks out the rollout branch from step $t$ onward **without** bootstrapping a terminal value (§2.3 iv: "not truncated with a tail bootstrap"). Replacing the tail with $0$ injects an uncalibrated step-function penalty/bonus whenever the trajectory crosses the leverage threshold.
    3. **Delayed halt on tracker corruption**: `SigmaTracker.update` increments `fail` and halts only at `fail >= 2`, reusing the previous $W$ on the first non-finite or trace-violating batch rather than immediately halting on numerical corruption as required by Charter §2.4.
    4. **No gate on target representation-factorization drift**: Does not check whether the EMA target critic $\bar{F}$ actually satisfies $\Psi \approx \Sigma_{\bar{B}} \bar{F}$ under non-stationary $\rho_t$.

- **Candidate Q (21.0 / 25.0)**:
  - *Strengths*:
    1. **Dual-bound damping rule (Eq. 12)**: $\ell_t = \max\left(10^{-3},\ 0.05 - s_{\min},\ \frac{s_{\max} - 100 s_{\min}}{99}\right)$ simultaneously enforces an absolute operator-norm ceiling $\|W_t\|_2 \le 20$ and a condition-number ceiling $\kappa(\widehat{\Sigma}_t + \ell_t I) \le 100$ for *every* PSD matrix $\widehat{\Sigma}_t$, completely eliminating inversion blowup even at $\operatorname{rank}(\widehat{\Sigma}_t) = 1$.
    2. Uses FP64 Cholesky factorization (`torch.linalg.cholesky_ex`) and `torch.cholesky_solve` to compute $v_z = W_t z$ in $O(d^2)$ per command without materializing an explicit inverse.
    3. Explicitly derives the non-stationary tracker lag bound under coordinate drift $v = \|\Sigma_t^* - \Sigma_{t-1}^*\|$ (§2.4), exposes the damped-prefix / undamped-tail Bellman mismatch (Eq. 13), and gates hybrid rollouts on a 500-update warmup, 131,072-frame split-half target calibration, minimum eigenvalue $\lambda_{\min} \ge 0.05$, whitened calibration residual $\|W_t^{1/2}\Sigma_{\mathrm{cal}}W_t^{1/2} - I\|_2 \le 0.50$, and held-out feature-return residual $\|q - \Sigma F\|/(\|q\| + 10^{-8}) \le 0.10$, gracefully falling back to the 1-step standard actor when the gate is closed.
  - *Technical Deductions (-4.0 pts)*:
    1. **Calibration split-half gate uses an unwhitened norm**: As Reviewer A proved, gating on $\|\Sigma_{(1)} - \Sigma_{(2)}\|_2 / \|\Sigma_{\mathrm{cal}}\|_2 \le 0.10$ is dominated by $\lambda_{\max}$ and can pass at $1\%$ while the two halves disagree by $25\%$ on $\lambda_{\min}$ (where $W_t$ has its highest gain).
    2. **Representation-residual gate is unwhitened**: $\|q - \Sigma F\|/\|q\| \le 0.10$ does not weight the residual $h = q - \Sigma F$ by $W_t$, even though the hybrid return error is $h^\top W_t z$.
    3. **Lack of per-command leverage safeguard and gate hysteresis**: Global spectrum gates do not catch an out-of-support prompt $z$ aligned with the weakest eigendirections, and binary toggling of the hybrid gate switches the actor objective discontinuously between online $F$ and target $\bar{F}$ without hysteresis.

---

#### 3. Compatibility with UFO Update Contract (Weight: 25% — Candidate P: 21.0/25, Candidate Q: 24.0/25)

- **Candidate P (21.0 / 25.0)**:
  - *Strengths*:
    1. Preserves strict separation between rollout `behavior_z` and off-policy `z_update`, executes the two-pass BN update before freezing normalizers and running `SigmaTracker.update`, leaves `z_update` (50% uniform sphere, 50% online $B_\omega$ on permuted `m_next`) unwhitened, and keeps task critic $Q$ training on `z_actual`.
    2. Provides a clear stop-gradient table (§2.2) and correctly rules out whitening at site (i) `z_update` and site (iii) 1-step actor gradient $\nabla_\theta F(o, \pi_\theta(o,z), z)^\top z$, while requiring it at site (iv) $H$-step world-model intrinsic rewards.
  - *Technical Deductions (-4.0 pts)*:
    1. **Cross-network gauge mismatch in Gated Option C (`COLOR`) at site (ii)**: In §2.2, P argues that $\widehat{\Sigma}$ must track target $\bar{B}$ and warns that mixing online $B_\omega$ and target $\bar{B}$ mixes two gauges whenever $B_\omega \neq \bar{B}$. Yet in §2.3(ii) and §5 S4, P's gated option `COLOR` encodes rollout prompts as $z = \operatorname{proj}(\widehat{\Sigma}_{\bar{B}}\, B_\omega(m))$—applying the **target** Gram estimate $\widehat{\Sigma}_{\bar{B}}$ to the **online** backward network $B_\omega(m)$, and feeding that command to the standard actor which differentiates **online** $F_\eta$! Furthermore, P does not specify a fallback if $\widehat{\Sigma} B_\omega(m) = 0$ under rank deficiency.

- **Candidate Q (24.0 / 25.0)**:
  - *Strengths*:
    1. Provides a crystal-clear, unambiguous 8-step update sequence (§2.2) and 4-site decision table (§2.3): **no whitening** on (i) `z_update` goal relabeling, (ii) `expert`/`near` rollout encoding, or (iii) standard low-level actor $\nabla_\theta F^\top z$; **damped dual solve** $v_z = W_t z$ applied exclusively to (iv) explicit hybrid intrinsic rewards $r_z(\hat{y}) = \bar{B}(\hat{m}(\hat{y}))^\top v_z$.
    2. Avoids any modification to `expert`/`near` prompt encoding, thereby preserving a single consistent command coordinate system across rollout collection, `behavior_z`/`z_actual` task replay, online $F$, and target $\bar{F}$.
    3. Specifies a dedicated deterministic contract fixture in §5.3 that programmatically asserts: exactly two BN statistics passes, zero expert/imagined/target BN updates, zero gradients into covariance or target parameters, nonzero input gradients through predicted motion $\hat{m}$, byte-identical stored `behavior_z`, and bit-exact FP64 save/restore continuity across 100 updates from update 2173.
  - *Technical Deductions (-1.0 pt)*:
    1. Step 2 copies online BN running buffers directly into target modules at every update, which introduces unsmoothed BN coordinate jumps into $\bar{B}_t$ (acknowledged in §2.4, but not isolated from EMA target smoothing), and §2.1's wording on non-finite input ("aborts that update") needs tightening to an immediate run/panel halt per Charter §2.4.

---

#### 4. Spike Falsifiability (Weight: 20% — Candidate P: 14.0/20, Candidate Q: 15.0/20)

- **Candidate P (14.0 / 20.0)**:
  - *Strengths*:
    1. **Directly tests the H1 anisotropy premise with a learned-$B$ mini-FB loop (Stage S2)**: Trains $B$ and $F$ MLPs with $\mathcal{L}_{\mathrm{orth}}$ and the UFO 50/50 $z_{\mathrm{update}}$ sampler on a drifting + abruptly shifting 229-D / 277-D distribution, pre-registering explicit confirmation ($\kappa \ge 10$ or $\lambda_H \le 0.8$ for $\ge 20\%$ of updates) and refutation ($\kappa < 3$ and $\lambda_H > 0.95$ throughout) criteria, plus a Spearman correlation test between $\operatorname{tr}(\Sigma^2)-d$ and $\operatorname{tr}(\Sigma^{-1})-d$.
    2. **Pre-registers a quantitative pass/fail threshold on multi-step value error (Gate G3)**: Requires $|b_H^{\mathtt{W}}| \le 0.5 |b_H^{\mathtt{RAW}}|$ on $H$-step value bias $|J_H^M - J^\star|/|J^\star|$ at $\kappa \ge 10$, and includes the rejected alternative `R2` (adaptive dual-ascent $\lambda_{\mathrm{orth}}$) as a compute-matched ablation arm.
  - *Technical Deductions (-6.0 pts)*:
    1. **Omits any quantitative pass/fail threshold on effective rank**: Brief B01 §4 explicitly requires pre-registered quantitative pass/fail thresholds on *both* effective rank and value error. Although P claims in §1.3 (line 108) that "§5 gates on all three", $\operatorname{erank}$ is only logged in S1/S2 and has **no pass/fail threshold** in S0, S1, S2, S3, or S4.
    2. **Mathematically inconsistent thresholds in S3 Gates G1 and G2**:
       - *G1 mismatch*: Gate G1 tests `RAW` empirical relMSE against $1 - \lambda_H$ (Eq. 1.7), which holds only when $\mathbb{E}[zz^\top] = I$. However, S3 draws $z$ from the 50/50 uniform + goal-encoded mixture whose second moment is $C = \frac{1}{2}(I + \Sigma) \neq I$, for which true relMSE is $\frac{\operatorname{tr}[(\Sigma - 2I + \Sigma^{-1})C]}{\operatorname{tr}(\Sigma^{-1}C)} \neq 1 - \lambda_H$.
       - *G2 impossibility at $\kappa=1000$*: Gate G2 requires `W` relMSE against `EXACT` $\Sigma^{-1}$ to be $\le 0.15$ at $\kappa = 1000$. Under P's own damping rule $\mu_t = \hat{\lambda}_1 / 1000$, for a spectrum with $\lambda_1 = 1000\lambda_d$ and $\lambda_2 = \dots = \lambda_d$, $\mu_t = \lambda_d$ yields a deterministic damping bias (Eq. 1.13) of $\approx \left(\frac{\lambda_d}{2\lambda_d}\right)^2 = 0.25 > 0.15$, causing even an **exact** covariance estimator ($\widehat{\Sigma} = \Sigma$) to fail Gate G2.
    3. **Uncalibrated $\kappa$ transformation in S3 and flawed paired statistics in S4**: $B_\kappa(x) = \operatorname{proj}(D_\kappa B(x))$ does not achieve a prescribed $\kappa$ because spherical re-projection alters the covariance spectrum, and S4 G7's difference of two individual 95% Wilson lower bounds is not a valid paired confidence interval.

- **Candidate Q (15.0 / 20.0)**:
  - *Strengths*:
    1. **Exemplary pre-registration rigor and arm separation**: Pre-registers exact CLI invocations, 5 seeds $\times$ 4 $(q,d) \in \{229,277\}\times\{100,256\}$ cells, strict `INCOMPLETE` budget rules, and 6 well-designed arms (`RAW`, `ORACLE`, `ORACLE-DAMP`, `EMA-DAMP`, `DIAG-DAMP`, `STALE-DAMP`) that cleanly isolate estimation error from damping bias (`EMA-DAMP` vs `ORACLE-DAMP`), off-diagonal covariance (`EMA-DAMP` vs `DIAG-DAMP`), and non-stationary tracking (`EMA-DAMP` vs `STALE-DAMP`).
    2. **Pre-registers quantitative pass/fail thresholds on effective rank**: Explicitly gates both tracker effective-rank estimation error ($|\widehat{R} - R^*|/d \le 0.03$) and whitened metric effective rank ($R(C_t)/d \ge 0.98$ and $\kappa(C_t) \le 2$ on $\ge 95\%$ of checkpoints).
    3. **Exact finite-MDP transition enumeration and rank-16 rejection test**: Fixture C computes exact multi-step policy gradients $\mu_{h+1} = \mu_h P_\theta$ with an analytical continuation tail $Q_B^{\mathrm{tail}}(\theta) = P_\theta(I-\gamma P_0)^{-1}B$, avoiding Monte-Carlo rollout variance, and Fixture A/B includes a rank-16 singular stream that tests mandatory gate closure.
  - *Technical Deductions (-5.0 pts)*:
    1. **Omits a quantitative pass/fail threshold on multi-step value error**: While Q bounds $|J_H^\ell - J_H^*|$ in Eq. (13) and gates 1-step reward NMSE and multi-step hybrid gradients in §5.4, it omits a pre-registered pass/fail threshold on multi-step value error $|J_H^\ell - J_H^*|$ or $\Delta V_z$ (missing the second half of Brief B01 §4 Row 4).
    2. **No learned-$B$ fixture testing the H1 premise or rejected alternative R2**: All fixtures construct $B$ analytically on $d$ prototypes ($|\mathcal{X}| = d$) with zero representation residual ($h \equiv 0$) and orthogonal plane-rotation drift. Because $B$ is never trained with $\mathcal{L}_{\mathrm{orth}}$, Q's spike cannot falsify whether online FB training actually produces spectral anisotropy (H1's premise) or whether adaptive $\lambda_{\mathrm{orth}}$ dual ascent (§3.2) mitigates it.

---

## 3. Principle Claim Adjudication (Appendix B.9)

Under Methodology v1.0 Appendix B.9, every proposed necessity claim is audited for mathematical validity, premise completeness, implementation independence, and operational falsifiability. No claim may be promoted to `Locked` without independent proof verification and the human research lead's signature.

### 3.1 Candidate P Claims (`order1_P.md` §4)

| Claim ID | Proposed Grade & Status | Adjudication Disposition | Required Action / Technical Ruling |
|---|---|---|---|
| **`C-B01-CAND-01`** *(No scalar-calibrated raw intrinsic reward is FB-consistent when $\kappa > 1$)* | Grade 1 (`Candidate`) | **`tighten-premises`** *(Stay `Candidate`)* | **Sub-claim (a)** ($\mathbb{E}_{\pi_z}[\sum_t \gamma^t B(s_{t+1})^\top M z] = F(s,a,z)^\top z \iff M = \Sigma_B^{-1}$) is valid **only if** P4 explicitly states that $M$ is a single matrix independent of $z$ (if $M$ can depend on $z$, only $M z = \Sigma_B^{-1} z$ is identified along $z$). **Sub-claim (b)** requires tightening P3: linear span of $\{F(s,a,z)\}$ does not guarantee that an attainable $F(s,a,z)$ aligns with the Chebyshev worst-case vector $(c\Sigma - I)z$; either tighten P3 to directional coverage of the extremal eigenspace or include the attainable cone alignment factor in the lower bound. **Sub-claim (c)** contains an algebraic error: replace $\Psi_H^\top(\Sigma M - I)\Sigma^{-1}z$ with the exact non-commutative identity $\Psi_H^\top(M - \Sigma^{-1})z = \Psi_H^\top(M\Sigma - I)\Sigma^{-1}z$, and add a premise that truncated $\Psi_H(s,a,z) \not\perp (M - \Sigma^{-1})z$. |
| **`C-B01-CAND-02`** *(Single-frame prompts are self-identifying only under isotropic Gram, and the consistent prompt correction is $\Sigma$-colouring)* | Grade 1 (`Candidate`) | **`downgrade`** | **Refuted as an impossibility claim over attainable states.** Maximizing $u^\top \Sigma^{-1} B(g)$ over all vectors on the sphere $\mathcal{S}^{d-1}(\sqrt{d})$ does not imply misidentification over the attainable embedding image $B(\mathcal{X}) \subset \mathcal{S}^{d-1}(\sqrt{d})$. Counterexample: on a finite state space $|\mathcal{X}| = d$ with $B(x_i) = \sqrt{d} e_i$ and non-uniform replay probabilities $\rho_i$, $\Sigma = d\operatorname{diag}(\rho_i)$ has $\kappa > 1$, yet every attainable goal $g \in \mathcal{X}$ satisfies $\theta_{\mathrm{mis}}(g) = 0$ and uniquely maximizes $k_\Sigma(y,g) = \delta_{y,g}/\rho(g)$. Moreover, under exact rank-$d$ FB, $z = B(g)$ is the exact encoding of the point-density reward $\mathbf{1}_{y=g}/\rho(g)$, whereas $z = \Sigma B(g)$ switches the task to dense cosine similarity $B(y)^\top B(g)$. Downgrade from a necessity claim to a whole-sphere geometric lemma (requiring surjective $B(\mathcal{X}) = \mathcal{S}^{d-1}(\sqrt{d})$). |
| **`C-B01-CAND-03`** *(A Gram-tracking role `R-Σ` is obligatory for hybrid FB + world-model heads)* | Grade 2 (`Candidate`) | **`tighten-premises`** *(Stay `Candidate`)* | Valid functional-completeness framing (explicitly permitting EMA tracking, exact representation isotropy, or a learned dual head as admissible realizations of `R-Σ`). However, the premises must be tightened to include: (1) bounded representation-factorization residual $\|\Sigma_{\bar{B}}^{-1/2}(\Psi - \Sigma_{\bar{B}}\bar{F})\| \ll \|\Sigma_{\bar{B}}^{-1/2}\Psi\|$ (since when $\bar{F}$ has large factorization error $h$, applying $\Sigma_{\bar{B}}^{-1}$ amplifies $h$ and can increase splice error), and (2) non-degenerate truncated excitation $\Psi_H$. Remains `Candidate` pending the empirical `R2` vs `W` falsifier test. |

### 3.2 Candidate Q Claims (`order1_Q.md` §4)

| Claim ID | Proposed Grade & Status | Adjudication Disposition | Required Action / Technical Ruling |
|---|---|---|---|
| **`C-B01-CAND-01`** *(Unique dual reward for a fixed full-rank FB command)* | Grade 1 (`Candidate`) | **`tighten-premises`** *(Stay `Candidate`; proof verified)* | **Proof verified.** Given $\Sigma = \mathbb{E}_\rho[BB^\top] \succ 0$ and linear intrinsic reward $r_z(x) = B(x)^\top a_z$, the encoding invariant $\mathbb{E}_\rho[B(x)r_z(x)] = z$ holds iff $a_z = \Sigma^{-1}z$, and value equivalence $\Psi(s,a,z)^\top a_z = F(s,a,z)^\top z$ over a spanning set of $F(s,a,z)$ vectors holds iff $a_z = \Sigma^{-1}z$. Implementation independence is properly stated. *Minor premise tightening required before human signature*: (1) state the outcome space as any measurable space $(\mathcal{X}, \rho)$ with $\|B(x)\|_2 = \sqrt{d}$ $\rho$-a.s. and $\Sigma \succ 0$ (removing the "finite outcome space" restriction so it applies directly to $\mathbb{R}^{229}$ and $\mathbb{R}^{277}$), and (2) separate the premises for the encoding-invariant half (which requires only $\Sigma \succ 0$) from the value-equivalence half (which additionally requires exact density factorization $F = \Sigma^{-1}\Psi$ and a spanning family of $F$). |
| **`C-B01-CAND-02`** *(Unobservable latent directions cannot be recovered from replay rewards)* | Grade 1 (`Candidate`) | **Stay `Candidate`** *(Proof verified)* | **Proof verified.** When $\operatorname{rank}(\Sigma) = r < d$, any nullspace vector $n \in \ker(\Sigma)$ satisfies $\mathbb{E}_\rho[(n^\top B(x))^2] = 0 \implies n^\top B(x) = 0$ $\rho$-a.s., so $F$ and $F + tn$ yield identical replay density products $F(s,a,z)^\top B(x)$ for all $t \in \mathbb{R}$ while differing by $t(n^\top z)$ on $F(s,a,z)^\top z$. Thus only the support projection $Pz = \Sigma\Sigma^+ z$ is identifiable from replay density fitting, and Tikhonov damping regularizes norms without recovering unobserved skills. Ready for human research lead signature per Appendix B.9. |

---

## 4. Final Disposition, Mandatory Merge Items, and Confounds

### 4.1 Disposition

- **Recommend**: **`Q`** (`order1_Q.md`, Primary Author B) — **88.0 / 100.0**
- **Alternate**: **`P`** (`order1_P.md`, Primary Author A) — **75.0 / 100.0**
- **Margin**: **+13.0 points** in favor of Candidate Q (exceeds the pre-registered Tie Margin of `5.0` points in `packets/B01/brief.md`).

### 4.2 Mandatory Merge Items (Required Before Locking `spikes/B01-gram/PLAN.md`)

Before executing the pre-registered empirical spike, the winning track (**Candidate Q**) must integrate the following five concrete items from **Candidate P** and the cross-review audit:

1. **Merge Stage S2 Learned-$B$ Mini-FB Anisotropy & Mechanism Test from Candidate P (§1.3 & §5 S2)**:
   - Add a fourth stage (`--stage learned_b`) to `spikes/B01-gram/PLAN.md` that trains a miniature online FB network ($B_\omega: \mathbb{R}^q \to \mathbb{R}^d$ and $F_\eta: \mathbb{R}^{q+29+d} \to \mathbb{R}^d$ with $\mathcal{L}_{\mathrm{orth}}$ and the exact UFO 50/50 $z_{\mathrm{update}}$ sampler) across 20,000 updates on a non-stationary 229-D / 277-D stream with non-orthogonal scale drift and a step shift.
   - Pre-register P's quantitative H1-premise confirmation/refutation gates ($\kappa \ge 10$ or $\lambda_H \le 0.8$ for $\ge 20\%$ of updates vs $\kappa < 3$ and $\lambda_H > 0.95$ throughout) and report the Spearman rank correlation between the $\mathcal{L}_{\mathrm{orth}}$ Frobenius excess $\operatorname{tr}(\Sigma^2) - d$ and the exact uniform-$z$ reward MSE $\operatorname{tr}(\Sigma^{-1}) - d$.
2. **Merge Empirical Comparator Arm `R2` (Adaptive $\lambda_{\mathrm{orth}}$ Dual Ascent) from Candidate P (§3.2 & §5 S3)**:
   - Within the learned-$B$ stage, include Candidate P's `R2` arm (dual ascent on $\alpha_t$ for $\|\widehat{\Sigma} - I\|_F^2 \le \epsilon$ with raw readout $v_z = z$) and `R2+EMA-DAMP` to test empirically whether representation-side orthonormalization pressure can substitute for or complement the reward-side damped solve.
3. **Merge Multi-Step Hybrid Value-Error Gate from Candidate P (§1.3 Eq. 1.11 & §5 S3 Gate G3)**:
   - Add an explicit quantitative pass/fail threshold to Candidate Q's §5.4 gate table on the $H$-step hybrid value discrepancy $|J_H^\ell - J_H^*| / \max(|J_H^*|, 1)$ for $H \in \{8, 16\}$ in Fixture C (requiring normalized value error $\le 0.05$ in the moderate window and $\le 0.25\times$ the `RAW` value discrepancy), completing Brief B01 §4 Row 4's requirement for pre-registered thresholds on both effective rank and value error.
4. **Merge Per-Command / Per-State Leverage Diagnostic from Candidate P (§1.2 & §2.3 iv) with Safe 1-Step Actor Fallback**:
   - Incorporate Candidate P's leverage metric $\ell(y) = \bar{B}(y)^\top W_t \bar{B}(y) / d$ and command gain $g(z) = z^\top W_t z / d$. Rather than P's unbootstrapped branch dropping (which injects zero-tail truncation bias) or Q's purely global binary gate toggle, route any individual command $z$ with $g(z) > \tau_{\mathrm{cmd}}$ (or any rollout where $\ell(\hat{y}_h)$ exceeds $2\times$ the 99.9th replay percentile) to the standard 1-step actor gradient $-\nabla_\theta \min_k F_k(o, \pi_\theta(o,z), z)^\top z$, and add a minimum dwell-time hysteresis (e.g., 200 updates) to global hybrid gate transitions.
5. **Apply Review A's Norm-Calibration and Contract Tightening Fixes to Candidate Q (§2.1, §2.4, §5.2, §5.4)**:
   - Replace the unwhitened relative operator norm in Q's split-half calibration gate with the whitened operator norm $\|W_t^{1/2}(\Sigma_{(1)} - \Sigma_{(2)})W_t^{1/2}\|_2 \le 0.15$.
   - Replace the unwhitened feature-return residual gate $\|q - \Sigma F\|/\|q\| \le 0.10$ with the whitened residual $\|W_t^{1/2}(q - \Sigma F)\| / (\|W_t^{1/2} q\| + 10^{-8}) \le 0.10$, and add a fixture variant with controlled non-zero residual $h = q - \Sigma F \neq 0$ and $n = 2048 \gg d$ states.
   - Align the operational and spike whitened condition-number gates at $\kappa(C_t) \le 2.0$, pre-register the exact candidate-action sampling distribution $\tanh(\mathcal{N}(0, I))$ in Fixture C, and tighten §2.1 so that any verified non-finite input (`invalid` row) reaching the update immediately halts the affected run or evaluation panel per Charter §2.4.

### 4.3 Confounds Paragraph

Three methodological and technical confounds must be recorded alongside this adjudication. First, as documented in Candidate Q's header and Review A-on-B §1, the primary author and reviewer processes executed in an environment without kernel-enforced read sandboxing; behavioral isolation rests on audited tool-call logs rather than OS-level filesystem enforcement, so under Methodology v1.0 §11.1 this adjudication remains **Provisional** until the orchestrator attaches compliant isolation verification. Second, neither Candidate P nor Candidate Q had direct read access to the full text of `baseline/01`–`baseline/05` during blind review (Reviewer A explicitly flagged Q's Step 2 online-to-target BN running-buffer copy rule as `UNVERIFIED` against `baseline/05`); the orchestrator must verify before locking `B01-gram` whether target networks in the frozen UFO baseline copy online BN buffers per update or maintain independent/EMA normalizer statistics, as unsmoothed BN buffer copies inject affine coordinate drift into $\bar{B}_t$. Third, even after merging Candidate P's learned-$B$ mini-FB stage into Candidate Q's spike protocol, synthetic 229-D and 277-D surrogate streams with exact transition dynamics isolate only the algebraic, estimation, and gradient-consistency properties of $(\widehat{\Sigma}_B + \ell_t I)^{-1}$; they do not measure world-model rollout compounding error, contact-discontinuity Jacobian variance, or multi-body humanoid kinematic aliasing, which remain deferred to Packet B03 and full GPU integration gates per Charter §2.5.
