# Blind Review B on Proposal A (Packet B01)

**Recommendation: revise before spike lock.** The distinction between density readout and embedding similarity, and the fixed-policy identities (1.1), (1.6), and (1.9), are useful. The stronger necessity claims and several empirical gates do not follow as written.

Review inputs: the charter, B01 brief, Proposal A, and the pinned method's Appendix B (for the requested necessity audit). No other proposal, review, or draft was read. Baseline alignment is assessed against the contracts reproduced in these inputs, not independently certified against all baseline files.

## 1. Gate & Hard-Constraint Audit

| Constraint | Finding |
|---|---|
| Charter §2.1: actor objective; no cloning/tracking | No action MSE or phase-indexed pose-tracking fallback appears. **[CRITICAL]** §2.2 explicitly updates the actor through a world-model reward head and target-F tail. This is outside the charter's literal requirement that actor updates exclusively maximize conservative Fᵀz, with only the stated action-Q exception. The charter's hybrid research mission creates tension with that restriction; Proposal A cannot silently treat the hybrid update as authorized. Keep it a diagnostic until the contract explicitly permits it. |
| Charter §2.2: behavior/update latent separation | Pass on the stated design: fresh 50/50 online-B relabeling, two BN updates then freeze, separate stored behavior latent, and Q trained on the executed latent. Colouring must preserve these assertions. |
| Charter §2.3: motion-only, single-frame B | Pass: dimensions and blocked task inputs are explicit. No future/frame-index input is proposed. |
| Charter §2.4: physical failure versus corruption | Partial. Severe-penetration rows are retained and invalid rows excluded in principle. The >0.03 m classification, terminated flag, and zero absorption potential are not operationally specified. **[MAJOR]** The two-failure tracker fallback cannot serve as the charter's immediate halt/quarantine rule for invalid physical transitions; distinguish estimator failures from invalid source data before BN/replay updates. §5.0's “as-is, no filtering” requires an already-validated input contract. |
| Charter §2.5: evidence boundary | Pass: algebra checks and synthetic diagnostics are explicitly separated from learned robot competence. Incorrect numerical examples remain a verification defect (§2 below). |
| Brief §2: bilinear interface and sphere | Pass for the default design: FᵀB and projected B/prompts remain intact. Colouring needs a defined response to a zero projected vector under singular covariance. |
| Brief §2: causal, bounded estimator; target EMA interaction | Causal buffers and bounded O(Nd²+d³) work are specified. Target interaction is explicit but its consistency argument is unproved under drift (§2). |

Appendix B gate: C-B01-A-01 is not ready for Grade-1 locking. Candidate status is correctly declared; candidate claims cannot veto alternatives (B.4).

## 2. Rubric-Keyed Technical Objections

**Exact Mathematical Derivation — 30%.**

- **[CRITICAL] C-B01-A-01(b,c) exceed the proof.** P3 says attainable F vectors span, not that an attainable F aligns with any specified residual. Equation (1.9) is a valid operator-norm bound; converting it to the same normalized bound at an actual state/action needs additional directional coverage. For general M, the hybrid bias is
  \[
  b_H=\Psi_H^\top(M-\Sigma^{-1})z,
  \]
  not \(\Psi_H^\top(\Sigma M-I)\Sigma^{-1}z\), unless M commutes with Σ. P4 does not impose that condition. Full-return span is also not, without an argument about the transition operator and horizon, the stated finite-head excitation premise.
- **[MAJOR] C-B01-A-02 substitutes the whole sphere for attainable embeddings.** A spherical image need not contain the Kantorovich extremizer; its supremum is bounded by, not necessarily equal to, the whole-sphere bound. For example, let B(i)=√d eᵢ with unequal positive replay probabilities. Then Σ=d diag(ρ), κ>1, yet every available goal has zero rotation and uniquely maximizes its density kernel over these embeddings. An identity-transition finite MDP realizes exact rank-d FB here. Thus isotropy is not necessary for self-identification on attainable goals. Nor does embedding equality imply unique physical-state identification when B aliases frames. “Not in the replay dataset” also does not establish exclusion from the underlying distribution's support.
- **[MAJOR] Reported algebra checks disagree with the displayed bound.** At κ=28.3, 2√κ/(1+κ)=0.36312, not 0.18799; its reciprocal is 2.75388, not 5.32. At κ=96, the overshoot bound is 4.95001, not 9.80. These discrepancies require correction and a reproducible check before accepting S0's claimed verification standard.

**Stability Under Non-Stationary ρ — 25%.**

- **[MAJOR] Bounded inversion is not tracked-value consistency.** A target F formed by EMA need not satisfy Ψ=Σ_target F_target for the current target B and replay distribution. Historical target embeddings are mixed in the covariance EMA. Comparing βΣ with the parameter EMA coefficient does not bound functional drift from network updates, normalizer updates, or replay shifts; a half-life is not a lag-error bound without a drift bound. Measure the learned target Bellman/readout residual separately from covariance error.
- **[MAJOR] Singular regimes are stabilized numerically but undefined in the gates.** S1 uses Σ⁻¹/² and S3 uses Σ⁻¹ exactly when rank deficiency is advertised as a target regime. Specify support-restricted/pseudoinverse diagnostics, null-space errors, and a separate SPD panel. Positive damping cannot recover unidentified null-space rewards. The assertion that near-null directions have zero in-support energy is false; only exactly null directions do.
- **[MAJOR] The leverage guard changes the objective.** Dropping a branch and its tail produces a policy-dependent truncation bias outside (1.11)/(1.13). A ≤1% step count does not bound lost value or gradient. Report removed discounted contribution and compare matched guarded/unguarded arms; do not attribute every difference to covariance correction.

**Compatibility with UFO Update Contract — 25%.**

- **[MAJOR] Optional colouring mixes online and target coordinates.** The sole tracker estimates target-B covariance, while expert prompts use online B and the ordinary actor uses online F. The claim that proj(Σ̂ B_online(g)) produces embedding-matching rewards therefore does not follow. Either estimate the matching online covariance or explicitly quantify and gate the cross-network mismatch. Specify zero-norm handling and target-update/normalizer timing. This is distinct from behavior/update latent separation, which is preserved.
- **[CRITICAL]** Resolve the hybrid actor objective conflict in §1 before integrating site (iv). Frozen model parameters and correctly stored behavior latents do not alone establish actor-objective compliance.

**Spike Falsifiability — 20%.**

- **[MAJOR] Effective rank is logged but never gated**, contrary to the brief's explicit scoring standard and §1.3's assertion that all three spectral statistics are gated. Its insufficiency as a value-error predictor justifies a separate collapse threshold, not omission.
- **[MAJOR] S3's G1 applies the wrong population identity.** Equation (1.7) assumes E[zzᵀ]=I; S3 uses a 50/50 sphere/goal mixture. For latent second moment C, the appropriate population relative MSE is
  \[
  \frac{\operatorname{tr}[(\Sigma-2I+\Sigma^{-1})C]}{\operatorname{tr}(\Sigma^{-1}C)}.
  \]
  Use a separate uniform-z identity panel and report the mixture with its measured C.

## 3. Audit of Rejected Alternative & Necessity Claim

**[MAJOR] R1 and R2 are non-trivial alternatives, but their rejection is overstated.** R1 with final spherical projection preserves the hard interface/norm constraints even when it fails to whiten exactly. Constant leverage is sufficient, not necessary, for whitening to survive projection: isotropically distributed directions with independent varying radii give a counterexample. Running-stat inference also permits single-frame encoding, and synchronized coordinate changes cannot be ruled out merely by saying TD cannot perform them. These are engineering costs to compare, not impossibility proofs. R2 with a sufficiently tight Frobenius constraint does bound the minimum eigenvalue; the loose-ε counterexample does not eliminate that alternative. Its alleged tracking lower bound lacks dynamics assumptions. The proposal additionally promises R2+W in §3.2 but registers R2 without W in S3.

**C-B01-A-01 against Appendix B.** Explicit premises, implementation independence within the linear-readout class, invariant/lower-bound conclusion shapes, and the ban on score-based promotion meet B.3 in form. Part (a) is defensible if M is one common matrix for all z and P3 holds for every z tested. If M may depend on z, only its action on that z is identified. Parts (b,c) need the repairs above; the package therefore fails independent proof verification under B.9.

**[MAJOR] Falsification is incomplete.** The listed falsifier tests unscaled raw-reward equality, not the “any scalar c” claim, the attainable lower bound, or the general-M hybrid identity. Register separate counterexample criteria for each. A low-rank SVD alone does not ensure spherical B rows, SPD Gram, full F span, or a common representation across policies; row normalization generally destroys the factorization. Construct and check all premises explicitly. A failed bound must not automatically be dismissed as approximate-FB scope failure without measuring P1/P3. Keep the corrected invariant Candidate pending the independent verification and human signature required by B.9; no benchmark can supply those.

## 4. Spike Protocol Critique

- **[MAJOR] Reference and spectrum controls:** finite samples estimate a population covariance; call it exact only for a defined empirical distribution. Diagonal scaling followed by spherical projection does not generally yield a prescribed κ, particularly κ=1. Supply a verified calibration procedure and reset/refit the tracker for each transformed B. Separate analytic, empirical-distribution, and learned-F panels.
- **[MAJOR] Damping can fail G2 with a perfect estimator.** At κ=1000, choose λ_min=d/(1000+d−1), repeated d−1 times, and λ_max=1000λ_min. The default μ=λ_max/1000=λ_min yields uniform-z damping relative MSE ≈0.25 for both d values, exceeding G2's 0.15 threshold. Thus failure need not mean a bad estimator. Include an exact-damped oracle and gate estimation error separately from damping bias.
- **[MAJOR] Compute/mechanism matching:** R2 retrains B and cannot share identical B checkpoints while differing “only” in readout. Specify matched training budgets, a fixed-B readout comparison, and separate representation-learning comparisons. An exact tail tests algebra but does not validate target-F drift, approximation, or conservative twin-min effects. Specify whether tail differentiation freezes policy parameters as a learned critic would; differentiating a full future policy rollout gives a different gradient oracle.
- **[MAJOR] Reachability controls:** explicitly include each goal in Y and specify tie handling; otherwise exact top-1 recovery of an independently sampled continuous goal is generally impossible. Generate known-reachable goals and report an oracle distance-objective optimizer, matched starts/actions/restarts, and a physically unreachable-goal stratum. The synthetic descriptor dynamics need not preserve valid rotations/kinematics. They test an algebraic surrogate, not physical motion reachability. A worse worst-case sphere bound does not imply G6's pointwise RAWPROMPT≥INVWHITE ordering.
- **[MAJOR] Statistical/threshold flaws:** the difference of two Wilson lower bounds is not a confidence interval for the paired success-rate difference, nor equivalent to +10 points; each support stratum has 512 goals. Use paired uncertainty and seed-level replication. Floor near-zero value denominators and define zero-gradient handling. G4's mandatory +0.05 cosine improvement is impossible whenever RAW already exceeds 0.95, even at large κ; κ alone does not force gradients into bad directions. Register inconclusive outcomes between S2's confirmation/refutation bands and resource-budget exhaustion rather than diagnosing every failed gate as estimator inadequacy.
