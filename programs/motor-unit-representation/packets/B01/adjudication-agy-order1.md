# Independent Cross-Family Adjudication Report — Packet B01 (Order 1)

- **Packet ID**: `B01` (Privileged Forward Input Causality, Exogenous vs Endogenous Future Load Boundaries, and 22-Group Schema Audit)
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`), §4 Step 4 & Appendix B.9
- **Inherited Ledger Snapshot**: `X-BASE-001`..`X-BASE-005`
- **Inputs Audited**:
  1. `PROGRAM_CHARTER.md`
  2. `packets/B01/brief.md`
  3. Candidate P (`packets/B01/anonymized/order1_P.md`)
  4. Candidate Q (`packets/B01/anonymized/order1_Q.md`)
  5. Blind Review on Candidate P (`packets/B01/reviews/review-B-on-A.md`)
  6. Blind Review on Candidate Q (`packets/B01/reviews/review-A-on-B.md`)

---

## 1. Eligibility Gate Check (Hard Constraints & Appendix B.5 Gates)

Both candidates are audited against the four Hard Technical Boundaries in `PROGRAM_CHARTER.md` (§2), the two Hard Constraints and three Required Deliverables in `brief.md` (§2–§3), Methodology v1.0 §11.5 (serious rejected alternatives), and Appendix B.4/B.5/B.9 gates (Candidate claim discipline, explicit premises, admissible conclusion shape, implementation independence, operational test, falsifier, and absence of premature lock/veto).

| Gate / Constraint | Candidate P | Candidate Q | Technical Verification |
|---|---|---|---|
| **Charter HB-1 & Brief HC-1**: Deployed modules $\pi_\theta(x_{137}, z_{16})$ and $B_\omega(g_{13})$ (`281,617` parameters total) 100% free of privileged inputs | **PASS** | **PASS** | **P** (§0.4, §6) and **Q** (§1.4) restrict all changes to the training-only forward critics $F_{\eta_1, \eta_2}$ (`5,065`-D privileged port, `2,805,008` parameters per head). Neither adds a deployed estimator or alters the `281,617`-parameter deployment graph. |
| **Charter HB-2**: Causal integrity of privileged forward inputs $p_{5065,t}$ | **PASS** | **PASS** | **P** (§1.1–1.5) defines $\mathcal{F}_t^-$-measurability at pre-action boundary $t^-$, separates exogenous $\xi_t$ from endogenous $y_{t+k}$, and sanitizes post-action slices via pre-action assembly and stateless generator preview $\Psi_t(\xi_t)$. **Q** (§1.1, §1.3–1.4) defines interventional exogeneity $P(\xi_{t+1} \mid \xi_t, s_t, \mathrm{do}(a_t = a)) = P(\xi_{t+1} \mid \xi_t)$, seals $p_t^{\mathrm{causal}}$ prior to action latching, and replaces `[4096:4822)` with pre-action generator encoding $E_{726}(s_t^{\mathrm{gen}}, \xi_t)$. |
| **Charter HB-3**: Zero fabricated coverage metrics; real physics across $144 \times 5 = 720$ cells | **PASS** | **PASS** | Both **P** (§0, §5.2, §5.4, §6) and **Q** (§5.1, §5.2, §5.6) state explicitly that Section 5 is a pre-registered spike protocol with zero executed or fabricated metrics, and both require stratification across all $36 \times 4 \times 5 = 720$ configuration/regime cells while separating diagnostic spike counts from behavioral `coverage_ready` gates. |
| **Charter HB-4**: Strict separation of 101-update V3 smoke run vs converged motor control | **PASS** | **PASS** | **P** (§6) and **Q** (§5.1, §5.6) explicitly disclaim any interpretation of the 101-update checkpoint as converged control. |
| **Brief HC-2**: Account for all 22 schema boundaries (`4,822 + 243 = 5,065` dims) with R / G / M classification | **PASS** *(manifest reconciliation gated in Step 0)* | **PASS** *(manifest join gated in Stage B)* | As verified in `review-A-on-B.md` (§1), `baseline/02` freezes only the five aggregate block widths (`1,920 + 1,024 + 1,152 + 726 + 243 = 5,065`) and group semantics, not internal per-group index offsets. **P** (§1.4) assigns every group `1..22` to `R` (`3,929` dims), `G` (`816` dims), or `M` (`320` dims) summing to `5,065` and mandates Step 0 manifest reconciliation. **Q** (§1.2) maps the five exact aggregate intervals (`5,065` dims), assigns default `R`/`G` classes to all 22 groups with slice-level `M` overrides on provenance failure, and mandates a 5,065-slot manifest join before training. |
| **Brief Deliverables 1–3 & Method §11.5**: Formal partition, Bellman bias proof, spike protocol, and $\ge 1$ serious rejected alternative | **PASS** | **PASS** | Both provide all three deliverables and reject stop-gradient (`detach`) and EMA-only masking (zeroing Groups 18–21) with mathematical proofs (**P** §3.1–3.3; **Q** §3.1–3.2). |
| **Appendix B.4 / B.5 Gates**: All necessity claims entered as `Candidate`, explicit premises, admissible conclusion shape, implementation independence, operational test, falsifier, no unilateral lock/veto | **PASS** | **PASS** | **P** submits `C-B01-P-01`, `C-B01-P-02`, `C-B01-P-03` as `Candidate` (§4). **Q** submits `C-B01-Q-01`, `C-B01-Q-02` as `Candidate` (§4). Neither asserts a unilateral lock or veto. Mathematical defects in specific premises are adjudicated under §2 and §3 below rather than treated as eligibility disqualifications. |

**Eligibility Verdict**: Both **Candidate P** and **Candidate Q** pass all eligibility gates and are admitted to full scoring.

---

## 2. Rubric-Weighted Numerical Scoring & Technical Justification

### Summary Score Table

| Rubric Dimension | Weight | Candidate P (Raw /100) | Candidate P (Weighted) | Candidate Q (Raw /100) | Candidate Q (Weighted) |
|---|---:|---:|---:|---:|---:|
| 1. Action-Jacobian Degeneracy Proof | 35% | 85.0 | 29.75 | 84.0 | 29.40 |
| 2. Completeness of 22-Group Audit | 25% | 90.0 | 22.50 | 78.0 | 19.50 |
| 3. Preservation of E0–E4 Disambiguation | 20% | 88.0 | 17.60 | 82.0 | 16.40 |
| 4. Spike Falsifiability | 20% | 86.0 | 17.20 | 88.0 | 17.60 |
| **Total Score** | **100%** | — | **87.05 / 100.00** | — | **82.90 / 100.00** |

- **Raw Score Differential**: $\text{Score}(P) - \text{Score}(Q) = +4.15$ points in favor of **Candidate P**.
- **Tie-Margin Check**: Because `brief.md` sets **Tie Margin = `5.0` points**, $|\text{Score}(P) - \text{Score}(Q)| = 4.15 \le 5.0$ falls within the formal tie band, with **Candidate P** (`87.05`) ranking ahead of **Candidate Q** (`82.90`) on raw score.

---

### Row-by-Row Technical Justification

#### Row 1: Action-Jacobian Degeneracy Proof (Weight: 35%)
- **Candidate P (`85.0 / 100` $\rightarrow$ `29.75`)**:
  - *Strengths*:
    1. Derives the **Bypass Identity (Lemma 1)** $\partial_a F^c(x, p^c, a, z) = \mathbb{E}_\omega[\partial_a F^\star] + \mathbb{E}_\omega[\partial_y F^\star\,\partial_a Y]$ and **Theorem 1**, showing how replay evaluation on a leaf tensor $y_t$ ($\partial y_t / \partial a \equiv 0$) omits the bypass channel $J_y Y_a$ on-support and adds counterfactual mismatch $(a_t^\beta - \pi_\theta(x_t, z))$ off-support (§2.2, §2.6).
    2. Covers **both** degeneracy mechanisms in **Theorem 2 (§2.3)**: (i) the **stochastic / interior conditional action-support branch (zeroing)** where screening off $a_t$ forces the unique population-optimal critic to have $\partial_a F^\star \equiv 0$ on the interior of the conditional support, and (ii) the **deterministic / singleton conditional action-support branch (corruption / non-identification)** where $a_t = A(x, p^c, y)$ leaves off-manifold partial derivatives $\partial_a F^\star = c(x, p, z)$ unconstrained by replay MSE.
    3. Derives a closed-form **Linear-Gaussian Partial-Leak model (Proposition 2, §2.4)** yielding action-port retention $\chi = 1/(1 + \mathrm{SNR})$ for outcome-measuring leaks and proving the exact condition $\kappa \lambda_a / \lambda_w > c$ under which **stiff end-stop or rigid obstacle reactions ($c \to 0, \lambda_a \gg 0$) invert the sign of the policy gradient ($J_a < 0 < c$)**.
  - *Deductions (validated from `review-B-on-A.md` §2)*:
    1. **Collider-bias gap in Theorem 2(a)**: If physical transition noise in $s_{t+1}$ and exogenous innovation in $\xi_{t+1}$ shared a common noise source $w$ ($s' = a + w, \xi' = w$), conditioning on $y = s'$ would make $\xi' = y - a$ depend on $a$, giving $\partial_a \mathbb{E}[s' + \gamma \xi' \mid y, a] = -\gamma \ne 0$. Theorem 2(a) requires the explicit premise that physical transition innovations and exogenous generator innovations are conditionally independent given $Z_t$ ($\omega_{t+1}^{\mathrm{phys}} \perp \omega_{t+1}^{\mathrm{exo}} \mid Z_t$) or that $(x_t, p_t^c, y_t)$ reveals the full target-generating state $Z_{t+1} = (s_{t+1}, \xi_{t+1}, \theta)$.
    2. **Overreach of Theorem 2(d) ($z$-collapse) onto the singleton-support branch**: When $y_t$ deterministically reveals $a_t^\beta$, off-manifold evaluations at $\pi_\theta(x_{t+1}, z) \ne a_{t+1}^\beta$ are unconstrained by replay loss (by Theorem 2(b) itself), so reduction to the behavior Bellman operator $\mathcal{T}^\mu$ holds unconditionally only on the interior-support zeroing branch where $\operatorname{supp}(a_t \mid x_t, p_t^c, y_t) \supseteq \operatorname{range}(\pi_\theta)$.
    3. **Submultiplicative converse flaw in $D$ (§2.5)** and **fixed-target vs self-bootstrapped target conflation in Lemma 1**: Because $\|J_{\mathrm{fut}} Y_a\|_2 \le \|J_{\mathrm{fut}}\|_2 \|Y_a\|_2$, large $D = \|J_{\mathrm{fut}}\|_2 \|Y_a\|_2 / \|J_a\|_2$ is necessary for $\varepsilon$-degeneracy, not sufficient if $Y_a \in \ker(J_{\mathrm{fut}})$.

- **Candidate Q (`84.0 / 100` $\rightarrow$ `29.40`)**:
  - *Strengths*:
    1. Formulates the causal Bellman target with explicit interventional conditioning $\mathrm{do}(a_t = a)$ vs observational replay conditioning $\widetilde{F}(S, a, l, z) = \mathbb{E}_\mu[Y_t^\pi \mid S_t=S, a_t=a, L_t=l]$, and shows that differentiating $\bar{F}(S, a) = \int \widetilde{F}(S, a, l) P(dl \mid S, \mathrm{do}(a))$ requires the missing score-function or reparameterization term $(J_L H_a)^\top z$ (§2.1, §2.3).
    2. Provides a clean, bug-free **constructive non-identifiability proof (§2.2)** on the deterministic consistency manifold $l = b + a$: the family $F_c(S, a, l) = v[(1-c)(b+a) + c l]$ has **identically zero Bellman residual** on every valid transition while producing $J_a F_c = (1-c)v$ ($0$ at $c=1$, sign-reversed at $c>1$) and counterfactual actor error $c v (a_b - a')$.
    3. Uses the exact composed norm $\|J_L H_a\|_2$ in the sufficient degeneracy bound $\|J_a\|_2 \le \epsilon \|J_L H_a\|_2 \implies \|J_a\|_2 / \|J_{\mathrm{physical}}\|_2 \le \epsilon / (1 - \epsilon)$, avoiding P's submultiplicative converse error while reporting standardized $R_{a/L}$ separately (§2.3).
  - *Deductions (validated from `review-A-on-B.md` §2.1)*:
    1. **Omits the determinate zero-gradient (screening-off) theorem for stochastic windows**: Q's $F_c$ construction covers only the deterministic manifold $\operatorname{Var}(L \mid S, a) = 0$, where partial derivatives are *unidentified* and left to inductive bias. It omits the stronger result that when $\operatorname{Var}(L \mid S, a) > 0$ (as occurs in V3 over $K=10$ steps under the stochastic `1/3` rule + `2/3` policy replay continuation $\mu$ or contact restitution noise) and $L$ screens off $a_t$, the MSE population minimizer has $\partial_a \widetilde{F} \equiv 0$ **uniquely on the interior of the support**.
    2. **Omits partial-leak attenuation and physical contact sign-inversion mechanics**: Unlike P's Proposition 2, Q does not explain *why* stiff contact/end-stop reactions cause gradient sign reversal in a learned critic beyond choosing $c > 1$ in the algebraic counterexample.
    3. **Continuation policy mismatch in $J_L H_a$ for $K > 1$**: In §2.3 and §5.3, $J_L$ is trained on replay windows generated by $\mu$, whereas $H_a$ is computed on simulator branches under a fixed evaluation policy $\pi$.

---

#### Row 2: Completeness of 22-Group Audit (Weight: 25%)
- **Candidate P (`90.0 / 100` $\rightarrow$ `22.50`)**:
  - *Strengths*:
    1. Explicitly classifies all 22 groups across the full `5,065` dimensions (`3,929` `R`, `816` `G`, `320` `M`) with specific width-preserving causal replacements for every acausal slice (§1.4–1.5):
       - **Groups 1–5 (`1,600` dims) & Group 19 (`102` dims)**: Retained (`R`) as the 4 completed substeps of $[t-1, t]$ ending at $t^-$ (one-step index shift if currently logged post-`step(a_t)`).
       - **Group 6 (`320` dims, solver residuals/iterations)**: Masked (`M`) to `0` with frozen normalizer $(\mu, \sigma) = (0, 1)$ to prevent Issue #6 normalizer drift from leaking post-action solver work.
       - **Group 14 (`256` dims, normal/tangential contact forces)**: Replaced (`G-s`) by the impulse-averaged contact force $\frac{1}{\Delta t_{\mathrm{ctrl}}}\int_{t-1}^t \lambda_c(\tau)\,d\tau$ over $[t-1, t]$ concatenated with the pre-action substep force $\lambda_c(t^-)$.
       - **Group 20 (`280` dims, future external load window)**: Replaced (`G-ξ`) by the stateless open-loop generator preview $\Psi_t[k] = (m(\xi_t, k), F^W(\xi_t, k))_{k=1}^{4K}$ computed by `generator.preview(xi_t, K)` without access to robot state.
       - **Group 21 (`280` dims, future reaction window)**: Replaced (`G-h`) by the causal past reaction mirror $\tau_{\mathrm{react}, t-K:t}$ over the preceding 40 substeps.
    2. Identifies **three non-obvious endogeneity traps inside the disturbance generator itself (§1.3)**: (i) motion-opposing/assisting sign modes $\tau_{\mathrm{ext}} = m(\xi_t)\operatorname{sign}(\pm\dot{q}_c)$, (ii) world-frame wrenches $F^W(\xi_t, k)$ whose joint-axis projection $\hat{u}^\top(r_D(q_{t+k}) \times F^W)$ depends on future $q_{t+k}$, and (iii) state-triggered E3$\to$E4 release schedules, plus retrospective scene-label leakage.
  - *Deductions (validated from `review-B-on-A.md` §2)*:
    1. In §1.5, calling bitwise action-invariance under common random numbers "the operational definition of admissibility" is weaker than $\mathcal{F}_t^-$-measurability if a stochastic generator draws post-$t$ innovations $\omega_{t+1:t+K}$ independently of $a_t$ (exogenous clairvoyance)—although P's actual `preview(xi_t, K)` function takes only $\xi_t$ at $t^-$ and outputs conditional mean/hazard for stochastic arrivals.
    2. For a state-triggered release schedule, the causal progress counter up to $t^-$ is admissible pre-action state $s_t^-$, not exogenous state $\xi_t$, because its step-$t$ increment depends on $a_t$.

- **Candidate Q (`78.0 / 100` $\rightarrow$ `19.50`)**:
  - *Strengths*:
    1. Defines a rigorous 11-field manifest-binding join schema `(group_id, start, stop, source, sample_time, action_latch_time, update_order, frame, units, normalization, R/G/M)` across the five frozen aggregate intervals (`1,920 + 1,024 + 1,152 + 726 + 243 = 5,065`) without inventing unverified internal group offsets (§1.2).
    2. Provides a clean, explicit 64-slot parametric generator state layout $E_{726}(s_t^{\mathrm{gen}}, \xi_t)$ (`[0:64)` active schedule/flag/timer parameters + `[64:726)` deterministic zero padding) and properly separates clock-triggered exogenous countdowns ($\xi_t$) from threshold-triggered reactive generator states ($s_t^{\mathrm{gen}}$) (§1.1, §1.3).
  - *Deductions (validated from `review-A-on-B.md` §2.2)*:
    1. **Wholesale replacement of all 726 dimensions of Groups 18–21 deletes current physical/load states in Group 19 and past reaction window capacity in Group 21**: `baseline/03` Audit Issue #4 states that Groups 18–21 pack future external disturbances *alongside current physical/solver states*. Replacing the entire `[4096:4822)` block with a 64-slot scalar generator template and **662 constant zeros** discards Group 19's completed-interval applied load substeps and leaves multi-event, 6-D world-wrench, and moving-obstacle schedules without a specified encoding (`[40:64)` is zero for the scalar template).
    2. **Defaulting to "Mask (`M`)" rather than specifying a causal lag-1 replacement for post-action slices in Groups 1–17**: For Groups 4, 5, 14, and 16 (actuator, constraint, contact, and stop forces), Q's rule masks slices computed during the $[t, t+1]$ solve to zero rather than specifying the completed-interval $[t-1, t]$ / $t^-$ pre-action replacement, failing the rubric's requirement to specify the *causal replacement* for every acausal slice.

---

#### Row 3: Preservation of E0–E4 Disambiguation (Weight: 20%)
- **Candidate P (`88.0 / 100` $\rightarrow$ `17.60`)**:
  - *Strengths*:
    1. Explicitly maps every regime (E0–E4) and all three `baseline/01` §3.1 aliasing cases to concrete admissible carriers in $p_t^{\mathrm{causal}}$ (§1.4–1.5): E1 end-stop stall ($\delta, \dot{\delta}, k_s, d_s$ in G16/G12), E2 obstacle contact (signed distance, material params, $[t-1, t]$ impulse-averaged + $t^-$ contact force in G13/G14/G15/G17), E3 sustained load (bias/ramp/hold timer in G18, $[t-1, t]$ load in G19, open-loop envelope $\Psi_t$ in G20, 320 ms EMA in G22), and E4 post-load recovery (release countdown & quiet-window timer in G18, $\Psi_t$ in G20, past reaction mirror in G21, EMA in G22).
    2. Proves **Lemma 3 (Schedule-phase aliasing)** and pre-registers dedicated empirical disambiguation tests in the spike: Arm `Z` (Groups 18–21 zeroed, EMA-only) and Arm `C-ξ` (timers + preview zeroed), plus E4 release-countdown MAE probes and timer-permutation interventions (Gates G-6 and G-7).
    3. Quantifies the exact relationship between Charter H1 and acausal variance ($\mathrm{AEV}$ in §1.5 Corollary), preventing a drop in hindsight variance from being misdiagnosed as a loss of physical regime observability.
  - *Deductions (validated from `review-B-on-A.md` §2–§4)*:
    1. Gate G-6's linear probe for E0–E4 balanced accuracy on the 512-D compressor can trivially read Group 18's scene-allocation one-hot without verifying physical transition observability (though G-6's E4 countdown MAE probe $\le 1$ step and counterfactual TD residual $\delta_{cf}^C$ vs $\delta_{cf}^Z$ do test true schedule observability).
    2. Needs explicit enumeration of persistent actuator-delay / backlash / solver warm-start states in $s_t^-$ and a matched-hold-age constraint on Gate G-7's timer permutation so impossible timer/EMA pairs are not created.

- **Candidate Q (`82.0 / 100` $\rightarrow$ `16.40`)**:
  - *Strengths*:
    1. Carefully distinguishes causal availability ($\mathcal{H}_t^-$-measurability) from Markov sufficiency (§1.1) and proves a clean **Grade-1 conditional information lower bound (`C-B01-Q-02`, §3.2, §4)**: two equally likely generator states sharing identical retained history up to $t^-$ with distinct target means $u \ne v$ incur MSE $\ge (u-v)^2 / 4$ under any history-only predictor.
    2. Correctly handles reactive threshold-triggered release schedules by setting the `reactive_generator` flag and encoding threshold/controller state rather than a future release countdown (§1.3), and explicitly enforces step-level E3/E4 schedule synchronization (Audit Issue #1) in Stage B (§1.4, §5.2).
  - *Deductions (validated from `review-A-on-B.md` §2.3, §4)*:
    1. Masking post-action contact/constraint forces in Groups 4, 5, 14, and 16 (instead of replacing them with completed-interval $[t-1, t]$ forces) and zero-padding `[64:726)` in Groups 18–21 risks stripping away the current/recent contact force and multi-axis wrench features needed for E1/E2/E3 disambiguation.
    2. Includes no empirical ablation arm (`EMA-ONLY` or `EXO-PREVIEW`) or latent probe in Section 5 to test whether E3/E4 schedule-phase disambiguation (`C-B01-Q-02`) is actually realized by the trained critic.

---

#### Row 4: Spike Falsifiability (Weight: 20%)
- **Candidate P (`86.0 / 100` $\rightarrow$ `17.20`)**:
  - *Strengths*:
    1. **Comprehensive 6-arm ablation matrix (§5.3)**: `L` (leaky baseline), `C` (sanitized $p^{\mathrm{causal}}$), `L-sg` (stop-gradient control for Lemma 2), `Z` (EMA-only control for Lemma 3), `C-ξ` (timers + preview masked for `C-B01-P-03`), and `X` (realized exogenous window). Every theoretical claim and rejected alternative in the paper has a dedicated experimental arm.
    2. **Two-tier execution architecture (§5.4)**: Pairs a fast, controllable CPU PyTorch single-joint physics plant (Tier S, 10,000 updates, exact CRN rollouts across all 2,560 states) with the full V3 replay/simulator pipeline across all $144 \times 5 = 720$ cells (Tier V), plus a complete decision-rule table (§5.8).
  - *Deductions (validated from `review-B-on-A.md` §2, §4)*:
    1. **Gate G-1 uses the submultiplicative upper bound $D = \|J_{\mathrm{fut}}^L\|_2 \|\hat{Y}_a\|_2 / \|J_a^L\|_2 \ge 4$** instead of the exact matrix-vector product $\|J_{\mathrm{fut}}^L \hat{Y}_a\|_2 / \|J_a^L\|_2$ (even though line 511 already computes `bypass = einsum("nij,nj->ni", jl["J_fut"], Y_a)` for `BIR`).
    2. **Self-bootstrapped targets in $\delta_f, \delta_{cf}$, and $\mathrm{BIR}$**: Because each arm bootstraps from its own $\bar{F}$, residual and Jacobian comparisons across arms mix one-step input causality with multi-step bootstrap drift unless evaluated against a common reference target.
    3. **Unfiltered finite-difference step size ($\delta = 0.05$ for $\hat{Y}_a$, $\pm 0.1$ for $q'_{\mathrm{FD}}$)**: Lacks a smoothness/step-size consistency check across contact/stop switching boundaries.

- **Candidate Q (`88.0 / 100` $\rightarrow$ `17.60`)**:
  - *Strengths*:
    1. **Superior measurement metrology (§5.2–5.5)**:
       - **Stage A FP64 analytic control**: Evaluates $F_c$ for $c \in \{0, 1, 2\}$ with $10^{-10}$ tolerance to verify the Jacobian harness before training critics.
       - **Shared Monte Carlo reference target $Y_{\mathrm{ref}}$ (§5.5)**: Uses a common arm-independent continuation target $Y_{\mathrm{ref}} = B(g_{t+1}) + \gamma(1-d_t)\widehat{F}_{\mathrm{ref}}^\pi(S_{t+1}, \pi(x_{t+1}, z), z)$ to compute Normalized RMS Bellman Residual ($\mathrm{NRBR}$) and Explained Variance ($EV$) on both factual and actor-query counterfactual panels, eliminating bootstrap confounding.
       - **Smoothness and controllability filtering for $D_{\mathrm{ref}}$ (§5.3)**: Cross-checks $h = 0.01$ vs $0.02$ and $H = 100$ vs $200$ (requiring $\le 10\%$ discrepancy and $\|D_{\mathrm{ref}}\|_2 \ge 0.05$), separates contact switches from smooth interiors, and defines an explicit underpowered-test rule ($<50\%$ overall or $<10\%$ in any regime).
       - **Exact bypass product $\|J_L H_a\|_2$** in the RAW bypass reproduction gate (`\|J_a\|_2 <= 0.1 \|J_L H_a\|_2`).
  - *Deductions (validated from `review-A-on-B.md` §4)*:
    1. **Missing `EXO-PREVIEW`, `EMA-ONLY`, and `RAW-PERMUTED` arms**: Running only `RAW`, `DETACH`, and `CAUSAL` confounds removing endogenous forces with removing exogenous schedule previews and swapping raw slices for a 64-D template + 662 zeros, and leaves `C-B01-Q-02` untested in the spike.
    2. **64-step episode vs $H = 200$ rollout horizon mismatch & 1.4-epoch update budget**: Stage B collects 64-step episodes (`2,000` updates $\times$ `128` batch = `256,000` draws over `184,320` transitions) while $D_{\mathrm{ref}}$ rolls out $H = 200$ steps without specifying how the generator schedule is defined past step 64 or whether episode end is terminal ($d=1$) vs time-limit truncated.

---

## 3. Principle Claim Adjudication (Appendix B.9)

Per Appendix B.9.2, no claim may be promoted to `Locked` in this step; locking requires independent proof verification and human-lead signature after the pre-registered spike. Each proposed necessity claim is adjudicated below as **`Candidate` (stay)**, **`Candidate` (tighten-premises)**, or **`downgrade`**.

| Claim ID | Candidate & Proposed Grade | Adjudication Verdict | Required Premise Tightening / Scope Modification |
|---|---|---|---|
| **`C-B01-P-01`** *(Action-Port Non-Identifiability under State-Revealing Privileged Leakage)* | Candidate P — Grade 1 (Impossibility) | **`Candidate` (`tighten-premises`)** | 1. **Close the shared-innovation collider gap in Premise (P3)**: Require either that physical transition noise and exogenous generator innovations at step $t+1$ are conditionally independent given $Z_t$ ($\omega_{t+1}^{\mathrm{phys}} \perp \omega_{t+1}^{\mathrm{exo}} \mid Z_t$), or that $(x_t, p_t^c, y_t)$ is sufficient for the full target-relevant next state $Z_{t+1} = (s_{t+1}, \xi_{t+1}, \theta)$, not physical $s_{t+1}$ alone.<br>2. **Split the conclusion into two explicit branches**: (a) *Interior-support branch* ($\operatorname{int}\operatorname{supp}(a_t \mid x_t, p_t^c, y_t) \ne \emptyset$, e.g. $\operatorname{Var}(y_t \mid Z_t, a_t) > 0$): $\partial_a F^\star \equiv 0$ uniquely on the interior, and if the conditional support covers $\operatorname{range}(\pi_\theta)$, the Bellman backup collapses to $\mathcal{T}^\mu$ ($z$-collapse); (b) *Singleton-support branch* ($a_t = A(x_t, p_t^c, y_t)$): $\partial_a F^\star$ is unidentified by replay value fit (matching `C-B01-Q-01`), without claiming off-support $z$-collapse.<br>3. **Fix Gate G-1 metric**: Replace $D = \|J_{\mathrm{fut}}\|_2 \|Y_a\|_2 / \|J_a\|_2 \ge 4$ with the exact composed ratio $\|J_{\mathrm{fut}} Y_a\|_2 / \|J_a\|_2 \ge 4$. |
| **`C-B01-P-02`** *(Bypass Conservation Invariant and Acausal Variance Accounting)* | Candidate P — Grade 1 (Invariant) | **`Candidate` (`tighten-premises`)** | 1. **State the invariant for a common fixed Bellman target $T_t$ and nested information sets $\mathcal{F}_t^{\mathrm{causal}} \subset \mathcal{F}_t^{\mathrm{leaky}}$**: Lemma 1 ($\partial_a F^c = \mathbb{E}_\omega[\partial_a F^\star] + \mathbb{E}_\omega[\partial_y F^\star \partial_a Y]$) and the residual identity $\mathbb{E}[(T_t - F^c)^2] - \mathbb{E}[(T_t - F^\star)^2] = \mathrm{AEV} \ge 0$ hold strictly when both critics regress onto the same target $T_t$ and $\sigma(x_t, p_t^c, a_t) \subset \sigma(x_t, p_t^c, y_t, a_t)$.<br>2. **Operational test alignment**: Evaluate Gate G-4 (`BIR`) and $\widehat{\mathrm{AEV}}$ using a shared reference target ($Y_{\mathrm{ref}}$ from Candidate Q §5.5) and sum $J_{\mathrm{fut}} \hat{Y}_a$ across all action-variant slices identified in Step 0. |
| **`C-B01-P-03`** *(Exogenous Schedule Phase Is an Obligatory Critic Input for E3/E4)* | Candidate P — Grade 2 (Functional Role / Lower Bound) | **`Candidate` (`stay` at Grade 2, with `tighten-premises`)** | Retain as a Grade-2 structural role claim (since V3 applicability depends on Packet B02's E3/E4 schedule design). Tighten the premise so that target separation $\|M^\pi(Z, a) - M^\pi(Z', a)\| > 0$ is defined in the projected $B_\omega(g_{13})$ successor-feature space on pairs $(Z, Z')$ with identical 320 ms history $(x_{137,t}, \text{G22}_t)$, and restrict Gate G-7's timer permutation to states matched on hold age. |
| **`C-B01-Q-01`** *(Observational Bellman Fit Does Not Identify a Partial Action Gradient Through an Endogenous Proxy)* | Candidate Q — Grade 1 (Impossibility) | **`Candidate` (`tighten-premises` & merge with `C-B01-P-01` Branch B)** | 1. **Remove circularity in Premise (iv)**: Replace Premise (iv) (*"the admissible function class contains two differentiable extensions that agree on the manifold but differ in their partial action derivative"*) with a standard structural premise that the function class contains $C^1$ functions on a neighborhood of the manifold $\mathcal{M} = \{(S, a, l) : l = h(S, a)\}$ closed under addition of linear combinations of $(S, a, l)$ (as in $F_c$).<br>2. **Add empirical applicability check**: Measure $\widehat{\operatorname{Var}}(L \mid S, a)$ across common-random-number vs continuation-resampled branches in Stage B to classify each endogenous slice into the deterministic-manifold branch (`C-B01-Q-01`) vs the stochastic screening-off branch (`C-B01-P-01` Branch A). |
| **`C-B01-Q-02`** *(Distinguishing Generator States Is Necessary for State-Specific Load Prediction)* | Candidate Q — Grade 1 (Lower Bound) | **`Candidate` (`stay`)** | The conditional MSE lower bound $\ge (u - v)^2 / 4$ for equally likely pre-action states mapping to the same retained observation with distinct scalar Bellman target means $u \ne v$ is mathematically sound and implementation-independent. Pair it with Candidate P's Arms `Z` and `C-ξ` as its empirical realization test in the merged spike. |

---

## 4. Disposition, Mandatory Merge Items & Confounds

### Disposition
- **`Recommend`**: **`P`** *(Primary / Base Track: Candidate `P` at `87.05` vs Candidate `Q` at `82.90`, $\Delta = +4.15$; triggers the formal `Tie` synthesis rule under the `5.0`-point Tie Margin in `brief.md`, with Candidate `P` selected as the primary architectural base and Candidate `Q` designated for mandatory merge)*
- **`Alternate`**: **`Q`**

### Mandatory Merge Items from Alternate Track (`Q` $\rightarrow$ `P`) and Blind Critiques

Before sealing the Packet B01 specification and executing the spike, the winning base (`Candidate P`) **must** incorporate the following five items from `Candidate Q` and the validated review objections:

1. **Manifest-Join Schema Contract & Reactive Generator State Separation (from Q §1.1–1.3 & Review B-on-A)**:
   - Retain Candidate P's 22-group width-preserving replacement layout (`G-s` completed-interval $[t-1, t]$ impulse-averaged + $t^-$ contact forces in Group 14; `[t-1, t]` pre-action load substeps in Group 19; `G-ξ` stateless world-frame/magnitude open-loop preview $\Psi_t$ in Group 20; `G-h` 40-substep past reaction mirror $\tau_{\mathrm{react}, t-K:t}$ in Group 21; masked Group 6 with frozen $(\mu, \sigma) = (0, 1)$ normalizer), **bound via Candidate Q's explicit 5,065-slot manifest join** `(group_id, start, stop, source, sample_time, action_latch_time, update_order, frame, units, normalization, R/G/M)`.
   - Adopt Candidate Q's `[0:40)` explicit flags/timers/phase/mode encoding inside Group 18 (`64` dims), and classify any state-triggered release progress counter as endogenous pre-action state $s_t^{\mathrm{gen}}$ (with Q's `reactive_generator` flag) rather than exogenous $\xi_t$, preserving strict action-invariance of $\xi_{t+1}$ under Definition 1 and Gate G-0.
2. **Unified Two-Branch Degeneracy Theorem (from Q §2.2 & Review B-on-A)**:
   - Tighten Theorem 2(a) / `C-B01-P-01` premise (P3) to require $\omega_{t+1}^{\mathrm{phys}} \perp \omega_{t+1}^{\mathrm{exo}} \mid Z_t$ (or full $Z_{t+1}$-recovery), and merge P's interior-support zeroing theorem ($\operatorname{Var}(L \mid S, a) > 0 \implies \partial_a F^\star \equiv 0$ uniquely on interior support + $z$-collapse) with Q's constructive $F_c$ deterministic-manifold theorem ($\operatorname{Var}(L \mid S, a) = 0 \implies$ unidentifiable partial derivative $J_a F_c = (1-c)v$ at zero replay Bellman residual, without off-support $z$-collapse).
3. **Exact Composed Bypass Product $\|J_{\mathrm{fut}} \hat{Y}_a\|_2$ & Stage A Analytic Control (from Q §2.3, §5.2–5.3)**:
   - Replace the submultiplicative product $\|J_{\mathrm{fut}}\|_2 \|\hat{Y}_a\|_2$ in P's Gate G-1 (`degeneracy_D`) with Q's exact matrix-vector product $\|J_{\mathrm{fut}} \hat{Y}_a\|_2 / \|J_a\|_2$ (and scalar projection $|z^\top J_{\mathrm{fut}} \hat{Y}_a| / |z^\top J_a|$) summed across all action-variant fields identified in Step 0, alongside unit-standardized $R_{a/L}$.
   - Prepend Q's Stage A FP64 analytic control ($F_c$ for $c \in \{0, 1, 2\}$, error $\le 10^{-10}$) before Tier S and Tier V execution, and enforce the replay behavior policy mixture $\mu$ on continuation rollouts when estimating $\hat{Y}_a$ for $K > 1$.
4. **Shared Reference Target $Y_{\mathrm{ref}}$ & Smooth/Controllable Finite-Difference Filtering (from Q §5.3, §5.5)**:
   - Evaluate Normalized RMS Bellman Residual ($\mathrm{NRBR}$), Explained Variance ($EV$), $\widehat{\mathrm{AEV}}$, and Gate G-4 (`BIR`) against Q's common Monte Carlo reference target $Y_{\mathrm{ref}}$ (in addition to self-bootstrapped TD residuals) so multi-step bootstrap drift is separated from one-step input causality.
   - Apply Q's finite-difference step-size filter ($h \in \{0.01, 0.02\}$ agreeing within $10\%$) and physical controllability screen ($\|D_{\mathrm{ref}}\|_2 \ge 0.05$) to P's $q'_{\mathrm{FD}}$ sign-agreement and magnitude gates, reporting contact switches separately.
5. **Post-$t$ Innovation Resampling Check & `RAW-PERMUTED` Control (from Review B-on-A & Review A-on-B)**:
   - In Step 0 BAIA (Gate G-0), check both bitwise action invariance under common random numbers *and* bitwise invariance under resampling of post-$t$ RNG streams $\omega_{t+1:t+K}$ so exogenous clairvoyance is blocked alongside endogenous reaction leakage.
   - Add a `RAW-PERMUTED` control arm (permuting Groups 20–21 across transitions within each configuration/regime cell) to separate information leakage from input-scale/normalizer effects.

### Confounds Paragraph

Two structural confounds were identified during adjudication and controlled out of the scores: (1) **Underspecification of internal group boundaries in `baseline/02`**: Because `baseline/02` (§2.3, lines 41–45) specifies only the five aggregate block totals (`1,920 / 1,024 / 1,152 / 726 / 243`) rather than 22 individual slice offsets, Candidate P supplied a nominal 22-group width reconstruction deferred to Step 0 manifest reconciliation, while Candidate Q supplied the five exact block intervals deferred to a Stage B manifest join. Review B-on-A penalized Candidate P heavily for not providing code-level offsets that do not exist in the frozen baseline documents; this adjudication verified against `baseline/02` and `review-A-on-B.md` that neither author had access to an external code manifest, and therefore scored Dimension 2 strictly on the causal completeness and physical fidelity of the replacement rules rather than penalizing either candidate for the missing baseline offset table. (2) **Presentation style vs mathematical scope**: Candidate P writes in a theorem-heavy style with three claims and six experimental arms, whereas Candidate Q writes in a conservative verification style with two claims and three arms. To avoid rewarding sheer volume or penalizing conservative scoping, Candidate P was docked strictly for its two real mathematical overreaches (the missing independent-innovation premise in Theorem 2(a) and the extension of Theorem 2(d) $z$-collapse to singleton support, plus the submultiplicative $D$ metric), while Candidate Q was docked strictly for omitting the stochastic screening-off theorem ($\partial_a \widetilde{F} \equiv 0$), discarding 662 dimensions of Groups 18–21 as zeros, defaulting to masking rather than lag-1 replacement for post-action contact forces, and omitting an exogenous-preview ablation arm.
