# Independent Cross-Family Adjudication Report: Packet B02 (Order 1)

- **Packet**: `B02` — Non-Stationarity, Batch-Norm Ordering, and Off-Policy Credit Assignment in Joint FB + Task-Q + Planner Training
- **Adjudicator**: Independent Cross-Family Adjudicator (`agy`, Order 1: Candidate P vs Candidate Q)
- **Method Version**: Methodology v1.0 (§4 Step 4 & Appendix B.9)
- **Inputs Audited**: `PROGRAM_CHARTER.md`, `packets/B02/brief.md`, `anonymized/order1_P.md` (Candidate P), `anonymized/order1_Q.md` (Candidate Q), `reviews/review-B-on-A.md` (Critique on P), `reviews/review-A-on-B.md` (Critique on Q), `spikes/B02-SPIKE/VERDICT.json`.

---

## 1. Eligibility Gate Check (Hard Constraints & Appendix B.5 Gates)

| Gate / Constraint | Candidate P | Candidate Q | Technical Audit Summary |
|---|---|---|---|
| **Charter §2.1**: No BC or pose-tracking fallback | **PASS** | **PASS** | Both update $\pi_\theta(o,z)$ solely via scalar conservative FB value $\min_k F_k(o,\pi(o,z),z)^\top z$ (plus task-critic path in $K_{\mathrm{hold}}=1$) with zero supervised action MSE or tracking rewards. |
| **Charter §2.2 & Brief §2**: R2.1 UFO BN order, 50/50 `z_update`, immutable `behavior_z` / `z_actual` | **PASS*** | **PASS** | Both update normalizers once on `(obs, m_current)` and once on `(next_obs, m_next)`, freeze in `eval/no_grad`, sample 50/50 `z_update` using online $B_\omega$, and keep `behavior_z` write-once. *In P's Stage G, non-acting shadow critic `N` (re-encoded labels) must be explicitly marked as a deliberate contract-violation negative control. |
| **Charter §2.3**: Single-frame motion-only $B(m)$ (`229`/`277` dims) | **PASS** | **PASS** | Neither feeds terrain scan, obstacle height, ball state, phase, or frame index into $B(m)$. P firewalls `prompt_frame_id` as diagnostic-only metadata via a forward-signature unit test; Q restricts ball/contact outcomes to diagnostic rollouts. |
| **Charter §2.4**: `severe_penetration` vs `invalid` separation | **PASS*** | **PASS** | Both commit finite `severe_penetration` (`>0.03` m) with `terminated=True`, $\Phi_{\mathrm{next}}=0$. Q explicitly rejects `invalid` intervals from replay/normalizers, withholds partial macros, and halts the run/panel; *P discards uncommitted `invalid` episodes and halts on D1 normalizer breaches, and must make the `invalid` run-halt explicit. |
| **Charter §2.5**: Verified evidence vs unproven claims | **PASS** | **PASS** | P explicitly labels its dry-run JSON as an author-side synthetic CPU check rather than learned competence; Q claims zero empirical results and separates contract checks from GPU training gates. |
| **Brief §2**: No pre-training or freezing $B_\omega / \pi_\theta$; full-prefix zero-hidden RNN burn-in | **PASS** | **PASS*** | Both train jointly from scratch with full-prefix zero-hidden burn-in across online/target $Q$ and $P$. *Q's contiguous-suffix gate (§2.3) skips task updates while continuing FB updates if generation lag `g=1` fails (`p95 RMS > 0.05`), risking an undeclared FB-only pre-training blackout (`G-1`) without a skip-rate cap. |
| **Appendix B.5 & §11.5**: Non-trivial rejected alternative & structured necessity claims | **PASS** | **PASS** | Both analyze serious alternatives (prompt/outcome re-encoding, row-level gating/IS, age-only null) and submit structured Grade-1 Candidate claims with explicit premises, operational tests, and falsifiers. |

**Eligibility Verdict**: Both **Candidate P** and **Candidate Q** pass all eligibility gates and advance to full rubric scoring.

---

## 2. Rubric-Weighted Numerical Scoring (Out of 100)

| Rubric Dimension | Weight | Candidate P | Candidate Q |
|---|---:|---:|---:|
| **1. Exactness of Off-Policy Semantics** | 30% | **26.5 / 30** | **25.5 / 30** |
| **2. Compliance with R2.1 & v2 Contracts** | 25% | **21.5 / 25** | **22.5 / 25** |
| **3. Computational Overhead** | 20% | **17.5 / 20** | **15.0 / 20** |
| **4. Spike Falsifiability** | 25% | **21.0 / 25** | **21.5 / 25** |
| **Total Weighted Score** | **100%** | **86.5 / 100** | **84.5 / 100** |

### Row-by-Row Technical Justification

1. **Exactness of Off-Policy Semantics (30%) — P: `26.5/30` | Q: `25.5/30`**
   - **Candidate P (`26.5`)**: Cleanly proves zero replay-age target bias in step action-$Q$ ($K_{\mathrm{hold}}=1$, disabling M1 gating in Ball v2) versus $\theta$-driven path-law drift in macro-$z$ ($K=10$). Proves fixed-label $B$-drift invariance (Prop. 1.2) and exact $O(d_z)$ gauge symmetry (Prop. 1.4, decomposing $\Delta_B = \Delta_B^{\mathrm{def}} + \Delta_B^{\mathrm{gauge}}$ via Procrustes SVD). Derives both Pinsker/KL and Cauchy-Schwarz/$\chi^2$ bounds, law-of-total-variance staleness decomposition, Welford (C) + EMA (E) stationary BN biases, segment-end telescoping $\mu_n-\mu_c = \frac{1}{\bar L}(\bar m_{\mathrm{last}}-\bar m_{\mathrm{first}})$, and train-mode BN error $3/(2n_e)$. *Deductions (-3.5)*: Overstates bucket-mean $\overline{\mathrm{KL}}_g \le 0.02$ as a worst-case $\chi^2 = e^{2\mathrm{KL}}-1$ certificate without state-uniform $\Delta\mu$; conflates fixed-$\bar V$ regression with $1/(1-\gamma^K)$ fixed-point amplification; minor sign flip in §1.6 prose ($(\gamma^k-\gamma^K)\bar V$).
   - **Candidate Q (`25.5`)**: Rigorous stopped-path measure formulation $d\mathbb P_g^z(\tau\mid\mathcal H_t)$ (Eqs. 1–7), exact variance shift identity (Eq. 5), exact EMA recursive algebra including the paired covariance term $2\alpha q\operatorname{Cov}(\mu_*,n)$ (Eqs. 10–16), distribution-free pushforward shift (Eqs. 13–14), and explicit distinction between pre-squash Gaussian densities and post-clipping boundary atoms. *Deductions (-4.5)*: **Unit mismatch (`S-1`)** between Bound (7) (pre-squash Mahalanobis $D_{g,n}$) and the §2.3 gate (post-tanh Euclidean RMS $\le 0.05$, which at $\sigma=0.1, d_a=29$ allows $\sqrt{K}D \approx 8.5$, leaving the bound vacuous and missing pre-squash drift near tanh saturation); **ungoverned IS variance (`S-2`)** in Eq. (18) ($e^{KD^2}$ explosion in 29-D over $K=10$ with no ESS floor); §3.1 omits direct analysis of raw expert prompt re-encoding $B_n(m_{\mathrm{demo}})$ (`A-2`).

2. **Compliance with R2.1 & v2 Contracts (25%) — P: `21.5/25` | Q: `22.5/25`**
   - **Candidate P (`21.5`)**: Enforces 2-call BN update + `D1` call-counter and 64-bit `(mean,var,count)` hash guard, disjoint `data_ptr()` + debug CRC32 immutability checks, firewalled `prompt_frame_id`, exact $\gamma^k$ short-macro discounting (M2), and shared-prefix deduplicated zero-hidden RNN burn-in. *Deductions (-3.5)*: Storing `behavior_mu` and `a_raw` in `fp16` (§2.0) introduces $\sim 10^{-4}$ quantization error that conflicts with the `<1e-6` equivalence check in `c1` and perturbs M3 log-density ratios; must explicitly specify whole-episode prefix retention against FIFO eviction and quarantine Stage G arm `N`.
   - **Candidate Q (`22.5`)**: Exemplary storage-boundary `.clone()` vs `.detach()` enforcement, explicit `eval()` vs `no_grad()` separation, preservation of $\partial\pi/\partial z$ during actor/planner steps, whole-episode/reference-counted prefix retention from `step=0`, exact withholding of partial macros interrupted by `invalid`, and explicit flagging of the `baseline/04` `93/107` obs-dim and `256/100` $B$-dim schema conflicts. *Deductions (-2.5)*: Contiguous-suffix gate skipping (`G-1`) risks starving $Q/P$ updates early in training (undeclared FB-only staging); hard-copying online normalizer buffers into EMA target networks (`G-2`) mismatches buffer/weight ages; planner `delay=2` behavior under skipped task updates is left unspecified (`C-1`).

3. **Computational Overhead (20%) — P: `17.5/20` | Q: `15.0/20`**
   - **Candidate P (`17.5`)**: Concrete FLOP and forward-pass budget for production R2.1 (`2048×6` residual actor $\approx 25\text{M}$ params, FB update $\gtrsim 1\text{ TFLOP}$): snapshot-free D2 via stored `behavior_mu` costs $\le 16,000$ actor forwards per $U_d=250$ updates ($\approx 0.3\%$ amortized); D3 6-snapshot $B$-ring ($\le 13\text{ MB}$) + $256\times 256$ SVD + D4 $r=4$ `jvp` probes add $\approx 0.2\%$; shared-prefix RNN burn-in deduplication cuts prefix cost from $O(\sum_{\mathrm{slices}} t_0)$ to $O(\sum_{\mathrm{episodes}} \max t_0)$. *Deductions (-2.5)*: Excludes D5 64-env rollout wall-clock share from the per-update percentage and slightly understates per-step replay byte overhead in §2.0.
   - **Candidate Q (`15.0`)**: Amortizes panel diagnostics every 100 updates, limits exact `jacrev` to 8 pairs, runs 8-state trajectory rollouts every 5,000 updates, and registers a 95% bootstrap CI timing gate (<5%). *Deductions (-5.0)*: Provides **zero analytical FLOP or forward-ratio calculation at production `2048×6` widths (`O-1`)**, and §5.7 only times a toy CPU network (`288→64→29` MLP, LSTM-16) where the relative overhead of $K=10$ extra actor forwards per macro in correction mode does not transfer to GPU production runs.

4. **Spike Falsifiability (25%) — P: `21.0/25` | Q: `21.5/25`**
   - **Candidate P (`21.0`)**: Directly aligns Stage S with `B02-SPIKE/PLAN.md` (verified `PASS` in `VERDICT.json`: `elapsed_sec=1.0509`, `bn_clean_update_calls=2`, `bn_drift_under_frozen_queries=0.0`, `behavior_z_mutation_max_diff=0.0`, `rnn_burnin_vs_exact_max_error=4.77e-7`, `rnn_stale_cached_hidden_max_error=0.277`), adds closed-form BN/telescoping/Procrustes/bias-bound checks (`a2`–`d3`), and pre-registers Stage G value-calibration ($\epsilon_Q$ vs 32-rollout MC return). *Deductions (-4.0)*: Making B02 drift/bias checks (`[A+]`) non-blocking allows `PLAN` to pass even if drift bounds fail; omits reverse `behavior_z` mutation check (`b1`); Stage G Wilcoxon test pools correlated checkpoints across 3 seeds (pseudoreplication) and normalizes by arm-specific $\mathrm{sd}(\hat G)$.
   - **Candidate Q (`21.5`)**: Pre-registers five deterministic FP64 test families (A–E, `1e-10` tolerance, 5 seeds) covering bidirectional `behavior_z`/`z_update` independence, `no_grad` vs `eval` BN corruption, exact $\gamma^k$ vs $\gamma^K$ error $2(0.99^{10}-0.99^3)$, coordinated $O(d_z)$ rotation, exact $2^{10}$ Bernoulli path enumeration (Test D), and scalar recurrence witness $0.9^6$ vs $0.8^6$ vs $0$ + boundary-detached gradients (Test E). *Deductions (-3.5)*: **Test D contradicts §2.3's contiguous-suffix rule (`P-1`)** (setting lag-1 to $p_g=0.10$ and lag-100 to $p_g=0.50$ yields an empty contiguous suffix and skips the update instead of selecting lag-100); **lacks an iterative bootstrapped TD value-stability test (`P-2`)** (Test D fits a 1-step static normal equation); alert thresholds (`0.05` RMS, `0.02` $\Delta_B$) lack false-alarm calibration (`P-3`), and Test A omits `obs_normalizer` and online-vs-target $B$ checks (`P-4`).

---

## 3. Principle Claim Adjudication (Appendix B.9)

| Claim ID | Candidate & Summary | Adjudication Disposition | Technical Rationale & Required Scope Revision |
|---|---|---|---|
| **`C-B02-CAND-01` (P)** | Macro-label $B$-invariance, KL/$\chi^2$ bias bounds, and executed-label obligation (Grade 1) | **`Candidate (tighten-premises)`** *(narrowing count: 0 → 1)* | Parts (a) ($\omega$-invariance of fixed-$z$ macro targets) and (b) (chain-rule KL and $\chi^2$ bounds) hold once P4 explicitly requires a belief-sufficient causal history $H_t$, fixed target functional $\bar V$, and $\chi^2_\Delta < \infty$. Part (c) is refuted for unrestricted outcome-dependent relabeling by Review B-on-A's 3-command Bernoulli splitting counterexample; tighten (c) to **outcome-independent (pre-transition) relabeling maps $\zeta = f(\omega_t, H_t, z_{\mathrm{actual}}, m_{\mathrm{prompt}})$** at fixed $(H_t, z_{\mathrm{actual}})$. |
| **`C-B02-CAND-02` (P)** | Single-pass normalizer invariance, stationary mixture bias, and segment-end telescoping (Grade 1) | **`Candidate (stay)`** *(narrowing count: 0)* | Algebraically exact Grade-1 invariant for cumulative (C) and EMA (E) normalizers over contiguous replay segments. The double-`m_next` bias $\frac{1}{6}(\mu_n-\mu_c)$, telescoping identity $\mu_n-\mu_c=\frac{1}{N}\sum_G(m_{\mathrm{last}}-m_{\mathrm{first}})$, and Gaussian train-mode batch-statistics error $3/(2n_e)$ are sound and verified. |
| **`C-B02-CAND-03` (P)** | Zero low-level controllability makes planner gradient $\nabla_z Q$ pure critic error (Grade 1) | **`Candidate (tighten-premises)`** *(narrowing count: 0 → 1)* | The theorem ($p_\theta(\tau\mid H,z)$ independent of $z$ on $\mathcal Z \implies \nabla_z(\mathcal T_\theta Q)\cdot u = 0$) is exact, but operational test D5 only measures kinematic distance in $m \in \mathbb R^{D_m}$. Tighten the operational falsifier to require paired-noise task-return and contact/ball-outcome interventions alongside $\mathcal C(\alpha)$. |
| **`C-B02-CAND-04` (P)** | Exact $O(d_z)$ gauge symmetry of the joint objective; $\Delta_B$ alone cannot certify staleness (Grade 1) | **`Candidate (stay)`** *(narrowing count: 0)* | Exact Grade-1 distributional invariance under $R \in O(d_z)$ across FB, $\mathcal L_{\mathrm{orth}}$, B01 four-site whitening, and macro-$Q/P$ losses (given no coordinate-wise pre-linear op on $z$). Proves $\Delta_B$ neither upper- nor lower-bounds $b_\Delta$. |
| **`C-B02-CAND-01` (Q)** | Path-law equality $\mathbb P_g^z = \mathbb P_n^z$ iff unweighted expectation agrees for all bounded $f$ (Grade 1) | **`Candidate (tighten-premises)`** *(narrowing count: 0 → 1)* | As written, $\mathbb E_g f = \mathbb E_n f\ \forall f \iff \mathbb P_g^z = \mathbb P_n^z$ is a measure-theoretic definition with a vacuous falsifier (`N-1`), and its relabeling corollary fails under exact gauge conjugacy (`N-2`). Tighten to the **minimax TV lower bound** $\sup_{\|f\|_\infty \le M}|\mathbb E_g f - \mathbb E_n f| = 2M\,\mathrm{TV}(\mathbb P_g^z, \mathbb P_n^z)$ under unverified conjugacy. |
| **`C-B02-CAND-02` (Q)** | Query-invariant prompt semantics require query-independent EMA normalizer state (Grade 1) | **`Candidate (stay)`** *(narrowing count: 0)* | Cleanly scoped Grade-1 impossibility result for EMA normalizers ($0<\alpha<1$) and non-constant downstream prompt maps, backed by constructive witness (Eq. 11 and Test A). |

---

## 4. Disposition, Mandatory Merge Items, and Confounds

- **Recommend**: **`P`** (Candidate P — `86.5 / 100`)
- **Alternate**: **`Q`** (Candidate Q — `84.5 / 100`)

### Mandatory Merge Items from Alternate (`Q`) and Blind Reviews into Recommended Track (`P`)
1. **Precision & Storage-Boundary Hardening (from Q §2.1 & Review B-on-A)**:
   - Store `behavior_mu`, `behavior_log_std`, and `a_raw` in **`fp32`** (not `fp16`) so snapshot-free $\Delta_\pi$, KL, and M3 log-density ratios avoid $10^{-4}$ quantization error.
   - Enforce `.clone()` at all replay sample boundaries and adopt Q's bidirectional immutability check in Stage S (`b1` must also mutate a private clone of `behavior_z` under fixed RNG/motion frames and assert bitwise-identical `z_update` and online-vs-target $B$ separation).
2. **Gate Starvation Governance, Precedence, & ESS Floor (from Q §§1.2, 2.3 & Both Reviews)**:
   - Retain P's pre-clip Gaussian $\overline{\mathrm{KL}}_g$ gate metric (avoiding Q's post-tanh RMS unit mismatch), but relabel $\chi^2 \approx e^{2\mathrm{KL}}-1$ as an empirical diagnostic proxy rather than a worst-case certificate unless state-uniform bounds hold.
   - Specify that the floor $N_{\min}=8,192$ overrides `g_cut_prev` monotonicity with a logged starvation alert (preventing Q's `G-1` FB-only blackout), and register an explicit ESS floor ($\mathrm{ESS}/N \ge 0.25$) for M3 importance weighting.
3. **Whole-Episode Prefix Retention & Explicit `invalid` Halt (from Q §§2.1, 2.5 & Review B-on-A)**:
   - Enforce reference-counted or whole-episode prefix retention from `step=0` in `TaskEpisodeReplay` so FIFO eviction never orphans active macro rows.
   - Explicitly codify Charter §2.4 on `invalid` transitions: reject the uncommitted interval from replay and normalizers, withhold incomplete partial macros, and halt the affected run/panel.
4. **Blocking Mechanism Verdicts & Seed-Level Calibration (from Q §5 & Both Reviews)**:
   - Promote P's `[A+]` drift/bias checks (`a2`–`a5`, `b2`–`b3`, `c1`–`c6`, `d3`) to mandatory blocking gates for the B02 mechanism verdict; add Q's `jacrev` on 8 pairs as an exact cross-check on D4's Hutchinson `jvp`; and include a multi-step tabular/linear TD-bootstrapping value-stability test across generation lag.
   - In Stage G, aggregate $\epsilon_Q$ at the independent seed level normalized by a common baseline $\mathrm{sd}(\hat G_{\mathrm{A0}})$ while isolating shadow critic `N` as an explicit non-compliant negative control.

### Confounds
Both primary authors and both blind reviewers noted that `packets/B02/brief.md` was absent in their execution checkouts and substituted `briefs/B02-nonstationarity-and-off-policy-credit-assignment-in-joint-fb-task-training.md`; direct inspection confirms the two files are identical in problem statement, deliverables, hard constraints, and rubric weights (`30/25/20/25`), so zero rubric skew occurred. Second, Author B (Candidate Q) disclosed unrestricted session filesystem permissions during drafting; while no cross-contamination evidence appears in the drafts, the orchestrator must log this under Method v1.0 §11.1 isolation auditing. Third, per §11.5, both candidates' rejection of overwriting `behavior_z` and of pre-training/freezing $B_\omega,\pi_\theta$ reflects compliance with explicit Charter §2.2 and Brief §2 mandates (framed agreement) rather than independent discovery. Finally, Q's discovery of the `baseline/04` dimension discrepancy (`93` vs `107` policy obs dims; `256` vs `100` $B$ output dims) is recorded as a baseline documentation defect to be reconciled prior to Ball v2 integration, without confounding B02's R2.1 obstacle-traversal contract.
