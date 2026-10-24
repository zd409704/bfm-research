# Blind Review B on Proposal A (Packet B03)

## 1. Gate & Hard-Constraint Audit

**Recommendation: major revision before adoption or necessity-claim locking.** The conditional pooled-reference lower bound is a substantive contribution. The explicit distinction between input rank and nonlinear encoder rank, the per-configuration second-moment penalty, and the invertible preprocessing proposal also merit further investigation. However, the proposed spike can reject a valid representation for mathematically unjustified reasons, and its pooled operator construction does not faithfully represent the stated outcome space. The claim that the proposed reference change is necessary is stronger than the proof.

**Review scope.** I read only the supplied charter, B03 brief, and Proposal A as research evidence. References in A to baseline documents, earlier decisions, scripts, and ledger appendices are treated as assertions, not independently verified evidence. I did not consult other reviews or drafts. No V3 experiment was run for this review; the numerical counterexample below is an elementary calculation.

| Gate or boundary | Assessment |
|---|---|
| Fixed latent dimension, 16 | Pass at design level. All proposed deployed representations retain 16 outputs. |
| Fixed deployed budget, 281,617, including 74,000 for B | **Unresolved.** A §2.5 explicitly reports a 70,800-versus-74,000 discrepancy. Preserving an unknown baseline count does not establish the exact hard constraint. Supply an instantiated module inventory and distinguish learned parameters from frozen buffers. The training-only anchor itself need not violate the budget. |
| Deployment proprioceptive purity | Conditional pass. T uses only g, and configuration labels remain training-only in the recommended design. The asserted dead v_z slot and coordinate convention must match the actual calibrated outcome contract. |
| Single-step physical interpretation | Conditional pass for raw storage and T on its stated manifold. Invertibility of T does not establish preservation through B, and the reference change alters downstream reward semantics. See Section 2. |
| Causal privileged forward inputs | No violation demonstrated. A explicitly inherits a causal partition and proposes a causal surrogate. The supplied packet does not independently establish the implementation. |
| Real-physics coverage; no fabricated metrics | Pass in evidence labeling. Synthetic illustrations and the planned surrogate are clearly distinguished from V3 physics; no coverage closure is established or claimed. |
| Smoke verification versus converged control | Pass. A explicitly excludes converged control and H4 conclusions. |
| Required SVD/rank analysis | Partial. Conditional operator bounds and useful identities are supplied; exact learned per-configuration ranks are not derived. The linear feature model is not the deployed sphere-projected encoder. |
| Quantitative spike with per-group rank ≥12 | Present, but not yet valid. G3, G6, operator construction, and several estimators require revision before execution. |

The budget discrepancy is a gate to resolve, not evidence that T adds deployed parameters. Likewise, absence of a physics run is appropriate for a proposal, but the adoption language must remain conditional on later verification.

## 2. Rubric-Keyed Technical Objections

### Mathematical Analysis of Cross-Morphology SVD — 30%

**[CRITICAL] M1 — A conditional lower bound is promoted to an unconditional V3 impossibility and a unique remedy (A §§1.2, 4; C-B03-A-01).** The projection/Ky Fan argument is valid for fixed, nonzero Hilbert–Schmidt successor operators, the specified row measures, and a common outcome reference. The disjoint-support corollary is also valid under its premises. But the frozen brief supplies 36 geometry seeds, not a verified list of 36 distinct lever arms. A surrogate deliberately constructed with 36 distinct lengths cannot establish this premise for V3. Nor does the charter define H3's error measure finely enough to identify it automatically with this particular pooled-density Hilbert–Schmidt norm. Require an explicit mapping between the target operator, reference, row weighting, and H3 metric before declaring H3 impossible. Section 3 gives the narrower claim that can survive review.

Theorem 1 is an unrestricted rank-subspace optimum. For the fixed MLP with pointwise norm four it is a lower bound, not necessarily an attainable optimum: an arbitrary leading singular subspace need not admit a basis with constant pointwise squared norm. Also, F-conditioning cannot improve the optimum **for a fixed operator**; changing the policy can change that operator. The universal statement about π should retain this qualification, even where the shell-based bound remains applicable across policies.

**[MAJOR] M2 — Matching references removes one obstruction, but does not establish simultaneous attainability or required isotropy (A Theorem 2).** Four stroke profiles of one geometry can overlap in outcome space. On overlap, a shared B has one value and cannot independently choose its restrictions for each stroke. Distinct-length support separation frees restrictions between those shells, not between all 144 configurations. Theorem 2's attainment condition is useful, but the proposal has not shown it is feasible under overlap, sphere projection, network capacity, or held-out geometries. At eigenvalue ties or rank below 16, “spans the top-16 eigenspace” also needs the usual nonuniqueness qualification.

The condition E_k[BBᵀ]=I is a chosen identification/normalization convention, not a consequence of merely defining a bilinear density approximation. Nonorthonormal full-rank features can be used with a Gram correction. If a particular FB update or reward-to-z construction requires identity moments, derive that requirement for the specified update. It does not follow solely from changing the negative sampler.

**[MAJOR] M3 — The “exact” feature-model analysis omits sphere projection and overstates its optimization domain (A §1.4; C-B03-A-03).** For preprojection features y=Wφ, the deployed second moment is

\[
\Sigma_k=16\,\mathbb E_k\left[\frac{W\phi\phi^\top W^\top}{\phi^\top W^\top W\phi}\right],
\]

not WΦ_kWᵀ. Second moments Φ_k alone do not determine this expression. The table's eigenvalues 1 and x_k do not generally even sum to 16. Its numerical bounds therefore cannot be transferred directly to the sphere-projected B. Further, a finite grid over one tip/angular gain ratio establishes a result for that restricted family, not a proof over every shared linear head. State and prove the reduction to that family, or label it a numerical restricted-model illustration.

The model does not establish that every successful nonlinear encoder must divide out lever-arm scale. A first-layer linear probe failing to detect invariance cannot exclude a later or nonlinear realization. C-B03-A-03 should remain a testable architectural hypothesis, not an obligatory functional role.

**[MINOR] M4 — The global-rank lower bound is valid but not generally tight as stated (A Proposition 2; C-B03-A-02).** PR≥16π_k is below the universal PR≥1 when π_k=1/144. Equality via a projection of rank 16π_k is impossible unless that rank is an integer. More precisely, under eigenvalue cap c=1/π_k and trace 16, the maximal squared trace is r c²+t², where r=⌊16/c⌋ and t=16−rc; this gives PR≥256/(r c²+t²). The underlying warning that global whitening cannot certify group rank remains correct. Also distinguish the uncentered second moment Σ=E[BBᵀ] from centered covariance throughout; the constant-trace identity applies to the former.

### Resolution of Audit Issue #7 — 25%

**[MAJOR] O1 — The U-statistic is unbiased only under conditions the sampling recipe does not preserve (A §§2.1–2.5).** With independent stratum draws, fixed counts, all strata present, and exact weights, the stated pair statistic correctly estimates tr(Σ²). Dropping strata and renormalizing changes the target to the present-stratum distribution. Clipping importance ratios likewise changes the target unless an explicit correction is supplied. Thus the resulting penalty is not generally unbiased for the nominal ν_k on which every gate is said to be evaluated. This matters most during the P0 imbalance that motivates the packet.

Specify the exact clipped weights, normalization, and fallback target. Guarantee sufficient samples from all positive-mass strata, or quantify the bias and mark affected updates. Separate the anchor distribution from the negative/reference distribution in the FB objective; give the sampling estimator for each. Inclusion of i=j in its double sum also needs justification if the intended population expectation uses independent draws. Trajectory correlation must be addressed before invoking the i.i.d. calculation.

**[MAJOR] O2 — Configuration-averaged isotropy does not protect the boundary/load cells named in Issue #7.** Averages over scenes can be isotropic while an E1 or E3 conditional representation is nearly constant. Scene aggregates over configurations can also hide this failure. The 720 configuration×scene cells are only reported, and the fallback is triggered only if the configuration-level gate fails. Consequently A4 could pass while preserving the original short-link boundary/load failure. Add a pass-critical criterion for these cells, or an explicitly justified alternative based on state spread and prediction/decoding error. Do not require impossible rank on genuinely degenerate hold distributions merely to satisfy a uniform numerical target.

**[MAJOR] O3 — A finite penalty is not a per-configuration rank guarantee.** The identity between population PR and population orthogonality error is correct. It does not guarantee that optimizing a competing FB loss, a noisy EMA hinge, and an anchor will attain that error. Averages over configurations can trade one group against another. The table's “direct” guarantee and “yes” resolution claims should be changed to “directly penalizes; tested by gates.”

### Preservation of Tip Kinematic Information — 25%

**[CRITICAL] T1 — The linear scale anchor conflicts with exact isotropy for multiple scales (A §2.5).** Write the anchor as hλ(B)=wᵀB+b. Exact prediction of the configuration-constant λ_k entails wᵀB=λ_k−b almost surely within k. If the simultaneously requested Σ_k=I holds, then

\[
(\lambda_k-b)^2=w^\top\Sigma_k w=\|w\|^2\quad\text{for every }k.
\]

For nonzero w, this permits at most two distinct λ values. It cannot hold across 36 distinct lengths. With approximate isotropy,

\[
\|\Sigma_k-I\|_F\ge
\left|\frac{(\lambda_k-b)^2}{\|w\|^2}-1\right|
\]

under an exact anchor. Thus the claimed identification condition and scale preservation have a quantifiable conflict, not merely an automatic loss of about one PR unit. This does **not** prove PR≥12 and useful decoding are impossible; it requires replacing the exact-isotropy story with an explicit tradeoff and feasible tolerances, or considering a nonlinear training-only decoder. Centered variance losing one direction does not imply the stated bound on uncentered PR.

**[MAJOR] T2 — An invertible input transform does not prove that z retains tip semantics (A §2.6).** T is plausibly invertible on the specified manifold and is a promising zero-parameter change. B can still discard λ or other variables. G4 is therefore essential, rather than confirmation of an already-proved property. Momentum also requires effective mass, which A correctly says is unavailable from g; the defensible claim is preservation of existing kinematic information, not recovery of absolute momentum from z alone.

Require per-geometry/per-scene physical decoding errors, including short-link loaded and boundary states. State how desired outcomes are made consistent with the current unit's lever arm and stroke before T and B are called. A Dirac-goal argument based on a pointwise reference density needs a measure or finite-cell convention and a goal in the reference support. It does not by itself justify unchanged goal behavior for off-support targets.

**[MINOR] T3 — Several scaling assertions exceed the derivation (A §§1.1, 2.4).** A power law is a useful candidate family, not the only admissible function of observable ρ. Matching a single κ cannot generally remove capacity/stroke effects or make normalization statistics independent of the seed mix. Proposition 4 gives a necessary Lipschitz/spread inequality; minimizing a ratio of input traces is a heuristic surrogate, not an optimizer of decoding accuracy or of the required Lipschitz constant. Label these choices accordingly.

### Spike Falsifiability — 20%

**[CRITICAL] S1 — The pooled operator manufactures configuration separation (A §5.3).** Independently fitted per-configuration cells are treated as a disjoint union, with successor density set to zero on every other configuration's cells. Different strokes on the same geometry can assign positive density to the same physical outcomes. Their cells cannot be made disjoint by attaching a configuration ID without changing the target from g to (k,g). The proposed construction would mechanically create 144 disjoint blocks and a bound of at least √(1−16/144)≈0.943, rather than evaluating the stated 36-shell outcome problem. This is a target-space error, not evidence for C-B03-A-01.

**[CRITICAL] S2 — G3 and decision rule 3 test the wrong implication (A §§5.6–5.7).** The lower bound concerns pooled error. It does not imply that an encoder trained with shuffled/pooled references has configuration-matched error ≥0.70. For example, on disjoint shells whose successor density is constant within each shell, a shared constant feature gives zero matched error while pooled error remains large. Richer features can preserve that constant direction while having high group rank. Therefore A1/A2 can perform well on G1 and matched G2 without violating C-B03-A-01, and A4-shuf can have low matched error without invalidating anything. Remove those alleged falsifiers. A large spectral tail also does not certify disjoint supports: a high-rank operator on one shared support can have a large tail.

**[MAJOR] S3 — Requiring the whitening control to fail prejudges an empirical result (G6).** Invertible whitening may preserve useful information and need not exceed the chosen Lipschitz threshold. A successful W should narrow the criticism of that alternative; it should not invalidate A4. The claimed automatic whitening property is itself false after sphere reprojection, as detailed next.

## 3. Audit of Rejected Alternative & Necessity Claim (`C-B03-A-01`)

**Rejected whitening alternative: serious, but inaccurately formulated.** Ordinary whitening of a full-rank second moment produces identity before renormalization. The proposed B_k=4 normalize(Σ_k^−1/2 B) does not do so in general. A counterexample already on the required sphere is B=4e_i with probabilities p_1=1/2 and p_2=⋯=p_16=1/30. Its second moment is diag(16p_i). Whitening followed by sphere reprojection returns exactly 4e_i, leaving PR=3.75, not 16. Singular moments cannot be inverted at all without an additional convention. This directly refutes “trivially passes” the rank gate.

The added 136 independent symmetric entries are a credible budget concern for the specific stored-adapter design. However, establish the actual accounting convention for frozen matrices and deployment purity before treating that concern as a general theorem against all whitening implementations. The noise argument is a possibility, not a universal failure: an operator norm can bound perturbation amplification, but there need not be noise in the amplified direction, and sphere reprojection changes the map again. Proposition 4 does not establish the claimed mandatory amplification factor.

A configuration-dependent transform is also not generally a single linear change of basis “inside V.” If configuration is recoverable from g, the adapted encoder remains a 16-feature function of g and the pooled lower bound still applies, but its function span can change. If the adapter uses a stroke ID not determined by g on overlapping supports, it changes the B(g)-only interface. Distinguish these cases. Matched-reference training does not make an adapter automatically redundant, and the recommended configuration-matched method itself permits configuration-dependent latent orientations; cross-unit semantic alignment needs evidence in both designs.

**Necessity claim: retain a conditional impossibility lemma, reject the exclusive remedy.** For finite, nonzero HS operators and the stated shared reference, the accepted proof is:

1. A shared B defines a subspace V of dimension at most 16; unrestricted left factors achieve row projection onto V.
2. The average normalized residual is 1−tr(P_V W̄), bounded below by the spectral tail of W̄.
3. Under a verified disjoint-support partition, W̄ is block diagonal. Any 16 eigenvalues touch at most 16 blocks, and their total mass cannot exceed the sum of the 16 largest block traces m_j/K.

This proves the displayed conditional bound, including approximately 0.745 for **verified** 36 classes of size four. Preprocessing B alone cannot remove it when the evaluated target remains the original pooled density. Conditioning F cannot overcome a bound that already grants free left factors.

Before applying this lemma to V3, establish absolute continuity and finite HS norm, including the treatment of deterministic transitions or singular successor components; specify state-action weighting and whether M is a state or outcome operator; verify the support partition on the actual calibrated outcome definition; and connect the norm to H3. These assumptions hold straightforwardly for a suitable finite discretization, but not automatically for an ideal continuous deterministic system. R²≥0.999 for predicting length is not a proof of disjointness: arbitrarily narrow overlapping noisy shells can satisfy it.

The proof implies that a successful design must change at least one binding premise. It does not prove that configuration matching is the unique admissible change. A concrete within-interface alternative is a partially local reference

\[
\nu_{k,\epsilon}=(1-\epsilon)\nu_k+\epsilon\nu_{\rm pool},\qquad 0<\epsilon<1,
\]

with an explicitly revised objective and metric. This abandons the single common-reference premise without exact matching and allows a controlled residual penalty on spillover. Whether it meets the threshold is empirical, but the present theorem cannot exclude it. Support-class matching is another less granular option already acknowledged by A and should be compared against full configuration matching. These alternatives change the estimation target too; none automatically rescues the original pooled H3 metric.

**Claim disposition:** C-B03-A-01 may remain Candidate as a conditional mathematical lower bound after its missing regularity assumptions are supplied. Do not lock the V3-specific number, the unconditional H3 impossibility, or “unless configuration/support-class matched” as established necessity. This review does not supply a ledger lock or human-lead signature.

## 4. Spike Protocol Critique

The proposed experiment has useful elements: all configurations, a frozen held-out geometry split, multiple seeds, both reference metrics, physical decoding, explicit thresholds, and clear surrogate labeling. The following changes are necessary for an interpretable result.

1. **Repair the outcome-space discretization first.** Use a common measurable partition of physical outcome space, optionally separate by genuinely disjoint shell classes. All four strokes sharing a shell must use compatible cells, with their densities evaluated on those common cells. Estimate pooled cell masses as the mixture of component masses; do not force cross-stroke zeros. Whiten matrix coordinates by the declared row and column measures before SVD. Specify cell mass floors, empty-cell handling, and SVD tolerances. A discrete shell-separable toy problem with known spectra should verify the implementation before learning.

2. **Separate target quality from representation/optimization error.** The oracle tail is a squared relative error; compare its square root with ε. Specify the number of independent Monte Carlo continuations per anchor, the anchor distribution, terminal conditions, and the continuation state of disturbances. At γ=0.98, truncating at horizon 150 leaves about 0.0483 of normalized discounted mass; bound or correct the resulting target error. Fit evaluation partitions on a separate calibration split and estimate occupancy, masses, and B averages on independent evaluation samples where practical. Otherwise the 0.01 theorem tolerance and 0.02 arm-comparison margins are not justified. G3 should be an algebraic consistency test on the same correctly weighted finite operator, not certification of physical support geometry.

3. **Correct the gates and decisions before running.** Retain a pooled-bound consistency check, remove the A4-shuf matched-error requirement, and remove the rule that A1/A2 matched success challenges the pooled theorem. Permute sample assignments across blocks for a genuinely pooled negative control; a mere permutation of configuration names changes nothing. Let W pass or fail on its merits. Report support-premise failure separately from estimator invalidity. Label G2≤0.30 as an exploratory PARTIAL outcome; it does not satisfy the charter's <0.20 H3 target. Even G2≤0.20 tests a matched-reference, behavior-policy surrogate version of H3 and should be named accordingly.

4. **Make rank inference statistically coherent.** U estimates tr(Σ²) without bias under its assumptions, but 256/U is not an unbiased PR estimator. At finite sample size it can exceed 16, and the plug-in Σ identity need not agree with the U-derived statistic to 10^−4. Use the same plug-in matrix on both sides of the algebraic identity; report the U-based estimate separately with its sampling behavior. Bootstrap independent episodes or suitable trajectory blocks within strata, preserving the nominal weighting. If claiming simultaneous confidence for the minimum over 144 groups, use simultaneous intervals or a bootstrap of the minimum. The current lower bound of 11.5 supports a weaker uncertainty claim than PR≥12 for every population group.

5. **Resolve the held-out/training and replay contracts.** Removing eight geometries leaves 112 training configurations. The recipe “144 configurations every nine updates” must become a training-only schedule, with no held-out replay in FB, orthogonality, anchor training, κ selection, or normalization. Clarify whether the 600 training transitions for excluded seeds are generated but discarded. Define the rule/policy partitions under the fixed behavior-policy experiment: 30% OU exploration is not itself the nominal 1:2 replay split. Specify all controller/plant constants needed to reproduce the surrogate, rather than relying on an uninstantiated earlier decision.

6. **Unconfound the essential ablations.** A3 versus A4 changes both T and the anchor; use A3 versus A4−λ to isolate T, and A4−λ versus A4 to isolate the anchor. The arm named A4−λ retains λ in T and removes only its supervision, so it is not the ρ-blind alternative described in §3. Rename it and add a genuinely scale-removed arm only if that hypothesis is to be tested. Include a matched-reference/global-orthogonality comparison to separate the benefit of reference selection from per-configuration regularization. Keep fixed data splits and paired training seeds across comparisons.

7. **Strengthen semantic and robustness diagnostics.** Report physical decoding by held-out geometry and by E1/E3/E4 cells, with explicit RMSE denominators near zero. A pooled λ R² can obscure bad seeds, while within-configuration λ R² is undefined because λ is constant. Define an appropriate cross-seed scale error and groupwise physical errors. Compute perturbation sensitivity in one common physical/normalized metric across raw and transformed arms; arm-specific denominators confound the comparison. Within-shell neighbors do not test sensitivity to radial measurement noise or interpolation across geometry. Define those probes without admitting privileged deployment inputs.

8. **Stage the compute budget and report all outcomes.** Validate the analytic identities, common-cell operator, anchor tradeoff, and sphere-reprojected whitening on small cases before the approximately eleven-hour learning experiment. The runtime reduction rule needs a predetermined timing checkpoint and must apply consistently before examining outcomes. The VERDICT should retain per-configuration and relevant per-scene arrays, confidence intervals, occupancy uncertainty, oracle errors, and the exact reference definition, not only aggregate extrema. A failed prediction about a control arm is evidence to update the proposal, not automatically an invalid experiment.

With these changes, the spike could distinguish pooled-density capacity limits, within-configuration approximation, and preservation of usable physical outcomes. As written, those questions are conflated in the pass/fail rules, so a PASS would not yet justify adoption of design (d) or the advertised necessity claim.
