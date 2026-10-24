# Packet B01 Decision — FB Density Factorization, Gram Matrix Conditioning, and Intrinsic Reward Identifiability

- **Decision ID**: `D-B01-001`
- **Packet ID**: `B01`
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
- **Adjudicators**:
  1. `agy` (`gemini-4-argon-high`, Order 1: `P=A, Q=B`): `packets/B01/adjudication-agy-order1.md`
  2. `claude` (`sonnet`, Order 2: `P=B, Q=A`): `packets/B01/adjudication-sonnet-order2.md`
- **Pre-Registered Empirical Spike**: `packets/B01/spikes/B01-SPIKE/VERDICT.json` (`PASS`)

---

## 1. Consolidated Order-Swapped Rubric Scores

| Proposal Track | Author Model | Order 1 (`agy`: P=A, Q=B) | Order 2 (`sonnet`: P=B, Q=A) | Mean Score |
|---|---|---:|---:|---:|
| **Proposal A** (`proposals/A.md`) | `claude` Opus | `75.0 / 100.0` (Math 22, Stab 18, UFO 21, Spike 14) | `74.0 / 100.0` (Math 22, Stab 18, UFO 20, Spike 14) | **74.5 / 100.0** |
| **Proposal B** (`proposals/B.md`) | `codex` `gpt-6-astra` | `88.0 / 100.0` (Math 28, Stab 21, UFO 24, Spike 15) | `83.0 / 100.0` (Math 27, Stab 19, UFO 23, Spike 14) | **85.5 / 100.0** |

- **Winning Track**: **Proposal B (`codex` `gpt-6-astra`)** by a unanimous cross-family, order-invariant margin of **+11.0 points** (`+13.0` in Order 1, `+9.0` in Order 2; pre-registered tie margin `5.0`).
- **Disposition**: **`Recommend: Proposal B` with Mandatory Merges from Proposal A and Blind Reviews**.

---

## 2. Key Adjudication Findings & Mandatory Merges Adopted into Synthesis

1. **Exact Four-Site Whitening Decision Rule (Convergent Proof)**:
   - **(i) `z_update` off-policy goal relabeling**: **No whitening**. Keep the frozen UFO 50% uniform-sphere + 50% online-$B_\omega(m_{\mathrm{next}}[\mathrm{perm}])$ sampler under frozen BN after the two-pass statistics update.
   - **(ii) `expert` / `near` rollout prompt encoding**: **No whitening**. Under exact rank-$d_z$ density factorization, for an in-support point reward $r_g(x) = \mathbf{1}_{x=g}/ho(g)$, $z_g = \mathbb{E}_ho[B(x)r_g(x)] = B(g)$ holds identically because the $ho(g)$ factors cancel. Applying $\Sigma_B^{-1}$ to $B(g)$ injects an extraneous inverse ($\Sigma_B^{-2}$) and degrades goal alignment.
   - **(iii) Standard 1-step low-level actor gradient $
abla_	heta \min_k F_k(o, \pi_	heta(o,z), z)^	op z$**: **No whitening**. $F(s,a,z) = \Sigma_B^{-1}\Psi(s,a,z)$ already embeds the dual Gram factor from the bilinear density loss.
   - **(iv) Explicit $H$-step world-model intrinsic reward head**: **Mandatory causal damped Gram solve** $r_z(\hat{y}) = ar{B}(\hat{m}(\hat{y}))^	op W_t z$ in target $ar{B}$ coordinates, paired with terminal bootstrap $\gamma^H \min_k ar{F}_k(\hat{o}_H, \pi_	heta(\hat{o}_H, z), z)^	op z$.
2. **Dual-Bound Tikhonov Damping Rule (`Proposal B` Eq. 12)**:
   - Adopt $\ell_t = \max\left(10^{-3},\ 0.05 - s_{\min},\ rac{s_{\max} - 100 s_{\min}}{99}ight)$ on the causal FP64 target-$ar{B}$ Gram EMA $\widehat{\Sigma}_t = (1-eta_\Sigma)\widehat{\Sigma}_{t-1} + eta_\Sigma G_t$ ($\widehat{\Sigma}_0 = I_d$, $eta_\Sigma = 0.01$), guaranteeing both $\|W_t\|_2 \le 20$ and $\kappa(\widehat{\Sigma}_t + \ell_t I_d) \le 100$ across all PSD regimes including rank deficiency.
3. **Mandatory Merges from Proposal A and Blind Reviews**:
   - **Merge 1 (Harmonic-Mean Eigenvalue Identity & $\mathcal{L}_{\mathrm{orth}}$ Asymmetry from Proposal A)**: Incorporate Proposal A's exact uniform-$z$ identity $\mathrm{relMSE} = 1 - \lambda_H$ ($\lambda_H = d/\operatorname{tr}(\Sigma_B^{-1})$) and the proof that $\mathcal{L}_{\mathrm{orth}}$ penalizes $rac{1}{2}\sum_i(\lambda_i - 1)^2$ (at most $rac{1}{2}$ for a collapsed direction $\lambda_d 	o 0$) while intrinsic reward MSE diverges as $1/\lambda_d$.
   - **Merge 2 (Correction of Proposal A's Arithmetic & Non-Commutative Bias Errors)**: Correct Proposal A's §1.2 numerical check ($rac{2\sqrt{\kappa}}{1+\kappa} = 0.363125$ at $\kappa=28.3$, not $0.18799$) and fix the general-$M$ $H$-step Bellman splice bias to $b_H(s,a,z) = \Psi_H(s,a,z)^	op(M - \Sigma_B^{-1})z$.
   - **Merge 3 (Per-Command & Per-State Leverage Routing without Truncation Bias)**: Track leverage $\ell(\hat{y}) = ar{B}(\hat{y})^	op W_t ar{B}(\hat{y})/d$ and command gain $g(z) = z^	op W_t z / d$; when $\ell(\hat{y})$ or $g(z)$ exceeds threshold, route that command to the standard 1-step actor gradient $-
abla_	heta \min_k F_k^	op z$ rather than Proposal A's zero-tail branch dropping.
   - **Merge 4 (Whitened Split-Half & Residual Gates + Hysteresis from Review A-on-B)**: Replace unwhitened operator-norm gates with whitened split-half discrepancy $\|W_t^{1/2}(\Sigma_{(1)} - \Sigma_{(2)})W_t^{1/2}\|_2 \le 0.15$ and whitened factorization residual $\|W_t^{1/2}(q - \Sigma F)\|/(\|W_t^{1/2}q\| + 10^{-8}) \le 0.10$, with 200-update dwell-time hysteresis on the hybrid gate.

---

## 3. Principle Claim Rulings (Appendix B.9)

- **`C-B01-A-01`**: `tighten-premises` (Stay `Candidate` Grade 1; fix non-commutative splice bias to $\Psi_H^	op(M - \Sigma_B^{-1})z$ and tighten P3 directional alignment).
- **`C-B01-A-02`**: `downgrade` (Refuted on attainable manifold by unequal-$ho$ orthogonal prototype counterexample $B(x_i) = \sqrt{d}e_i$; downgraded to a whole-sphere geometric lemma).
- **`C-B01-A-03`**: `tighten-premises` (Stay `Candidate` Grade 2; add bounded whitened representation residual premise).
- **`C-B01-B-01`**: `tighten-premises` (Stay `Candidate` Grade 1; proof verified; generalize outcome space to measurable $(\mathcal{X}, ho)$ and split encoding-invariant vs value-equivalence premises).
- **`C-B01-B-02`**: `Stay Candidate` Grade 1 (Proof verified; nullspace non-identifiability under $\operatorname{rank}(\Sigma_B) = r < d$).

---

## 4. Empirical Verification Summary (`B01-SPIKE`)

Executed via `/srv/claude/research/fb-beyond-imitation-acceleration/gpu_experiments/run_b01_gram_spike.py` (`packets/B01/spikes/B01-SPIKE/VERDICT.json`, status `PASS`):
- Spherical trace identity $\operatorname{tr}(\Sigma_B) = d_z$ verified to $< 10^{-4}$ across $d_z \in \{100, 256\}$ under $\kappa(\Sigma_B) > 220$.
- Zero-shot linear reward readout $z_r = \Sigma_B \lambda$ verified invariant to $\kappa(\Sigma_B)$ (`max_abs_err = 3.10e-06 < 1e-4`).
- Causal EMA + damped Cholesky whitening (`EMAWhiteningTracker`) achieved **17.23x** ($d_z=256$, `0.5784 -> 0.0336`) and **11.34x** ($d_z=100$, `0.5621 -> 0.0496`) reduction in intrinsic reward MSE over raw inner products $B(y)^	op z$.
- Single-state goal gradient cosine improved from `0.3344` (raw) to `0.9815` (whitened).
