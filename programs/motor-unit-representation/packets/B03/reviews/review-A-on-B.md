# Blind Review A on Proposal B (Packet B03)

**Reviewer:** Blind Reviewer A. **Inputs read:** `PROGRAM_CHARTER.md`, `packets/B03/brief.md`, `packets/B03/proposals/B.md`. I read no other file in `reviews/` or `drafts/`, no baseline document, and no decision record. Where Proposal B relies on `baseline/0x`, `D-B01-001` or `D-B02-001`, I take those references as the proposal describes them and mark them **unverified under isolation**.

**Overall assessment.** The proposal is careful and honest. It fabricates no numbers. It correctly separates three distinct rank questions and gives a correct, useful refutation of the "Frobenius-orthogonal transition matrices" reading of the 0.943 bound (§1.4). Its algebra checks out where I tested it: the length congruence `D_L C_h D_L`, the tip-acceleration expression, `erank >= 256/(16+delta^2)`, the 144-group axis counterexample, the unbiasedness of the IPW cross-estimator, the `w <= 10` bound under the 10% mixture, and the slot-9 `v_z = 0` identity.

However, I found two structural defects that the proposal does not detect. Both sit on the two highest-weighted rubric dimensions:

1. **Common reference measure.** The successor operator is defined under a *pooled* outcome reference measure `rho_*`, and the target retains length. Under that formalization, the 0.943-type obstruction is not just a "valid warning under a stronger premise". It is a **provable physical fact**: rigid-link length is invariant along trajectories, so the operators of distinct-length geometries have disjoint right supports. With 36 geometry seeds, the worst-group error is bounded below by about 0.745. The successor gate (`< 0.20`) can therefore never pass by design. It escapes this bound only if the 128-cell dictionary is too coarse to resolve length, and then it no longer tests length retention.
2. **Conditional isotropy target.** The recommended conditional penalty pushes every `Sigma_k` toward `I_16`. That target is provably incompatible with the proposal's own affine zero-shot decoding gates for length and physical tip fields. The intervention the proposal recommends works against the rubric's "Preservation of Tip Kinematic Information" dimension.

Both defects can be fixed (see §2), but as written the spike's central gates are internally inconsistent.

---

## 1. Gate & Hard-Constraint Audit

| Constraint | Source | Verdict | Notes |
|---|---|---|---|
| `d_z = 16` fixed | Brief §2 | **PASS** | No extra latent coordinate; restated in the Architecture gate (§5.5). |
| Deployed budget `281,617` = `74,000` (B) + `207,617` (π) | Brief §2 | **PASS** | Arithmetic is correct. The transform in §2.4 is parameter-free. Normalizer statistics are serialized as non-trainable state. Reviewers should confirm the program's byte-count convention treats non-trainable buffers as outside the 281,617 *parameter* count. The proposal asserts this but does not cite the rule. |
| Physical interpretability of `g13` preserved | Brief §2 | **PASS, conditional** | Raw `g13` stays the external interface, and `T(g)` is internal to B and exactly invertible on the canonical manifold. The guard (`SCHEMA_INCOMPATIBLE` if the locked layout is not rigid housing-relative kinematics) is necessary and correctly specified. Residual risk: if the deployed `v_z` is *measured* rather than computed, replacing it discards sensor content (for example flex or bearing play). The FP64 identity check at `1e-6` would fail on real sensor noise, so the guard needs a stated noise tolerance, not FP64 tolerance, for measured fields. |
| Charter §2.1 Deployment proprioceptive purity | Charter | **PASS** | `r_L` comes from `||p||` inside `g13`, not from `p5065`, `x137` or a lookup. The reference PD policy uses `x137` stroke descriptors and `z16`. This assumes `q_min, q_max` are in the calibrated `x137` (unverified under isolation). |
| Charter §2.2 Causal integrity of privileged inputs | Charter | **PASS** | Future contacts enter only the measured successor *target*, never source inputs. The B01 audit is a launch prerequisite. |
| Charter §2.3 Zero fabricated coverage | Charter | **PASS** | All 720 `(k,e)` cells with real physics are a prerequisite. Synthetic checks are explicitly excluded from coverage, and B02's CPU surrogate PASS is correctly *not* treated as physics coverage. |
| Charter §2.4 Smoke run ≠ convergence | Charter | **PASS** | Stated explicitly (frozen-evidence paragraph and §5.1). |
| Rubric gate: pre-registered per-group `erank >= 12/16` | Brief §4 | **PASS on form** | Every one of 144 groups must pass, with a simultaneous 95% lower bound, per seed. However, see [MAJOR-4] on whether the bootstrap that supplies those bounds is valid at the stated sample sizes. |
| Deliverable 1: "exact per-configuration erank under global vs stratified" | Brief §3 | **PARTIAL** | The proposal does not compute numbers, correctly citing the lack of trained weights and the zero-fabrication rule. Instead it provides sufficient bounds and a counterexample. This is defensible, but it leaves unanswered whether the Audit #7 dominance mechanism exists after sphere projection. See [MINOR-1]. |
| Deliverable 2(c): "nondimensionalized angular/tip features + explicit scale ratio" | Brief §3 | **PARTIAL** | Tip channels are made length-free. Angular channels are only *unit-scaled* by a global `T_* = 0.10 s`, not nondimensionalized by a configuration-intrinsic time scale (for example `sqrt(I_k/tau_max,k)` or stroke duration). Capacity- and stroke-driven covariance differences in `(omega, a)` are untouched. See [MAJOR-3]. |

No hard constraint is violated. Gate-level concerns are about **internal consistency of the pre-registered gates**, covered below.

---

## 2. Rubric-Keyed Technical Objections

### Dimension 1: Mathematical Analysis of Cross-Morphology SVD (30%)

**[CRITICAL-1] Under the proposal's own pooled reference measure, length invariance makes the stacked successor operator block-diagonal across geometries, so a worst-group error floor of about 0.745 follows. The successor gate is unpassable by construction, or else blind to length.**

Section 1.3 defines `M_k` with columns `phi_j` orthonormal under a *common* reference measure `rho_*` (the pooled mixture over all 144 configurations). Section 1.4 then says the 0.943 premise (orthogonal right-side modes) is "not a proved property of the 144 physical configurations." For geometry it is a provable property:

- For a rigid link in the housing frame, `||p_tip,D^M|| = L_D` holds at every time step. Every future outcome `g_{t+1}` reached from configuration `k` lies on the shell `||p|| = L_{g(k)}`.
- So, as functions on outcome space, the rows of `M_k` are supported only on shell `L_{g(k)}`. Configurations with different lengths have **disjoint right supports**, and the corresponding normalized Gram blocks `R_g = X_g^T X_g` are mutually orthogonal.
- Let `P` be the projector onto the row space of the shared right factor `A_B` (rank ≤ 16). The captured fraction for configuration `k` of geometry `g` is `tr(P R_g)`. Summing over one configuration per geometry gives `sum_g tr(P R_g) = tr(P sum_g R_g) <= 16 * max_g ||R_g||_op <= 16`.
- Therefore `min_g (captured fraction) <= 16/G` and **`E_worst >= sqrt(1 - 16/G)`**, where `G` is the number of distinct-length geometries. This holds even in the model's best case, where every block is rank one, and even with optimal per-row left factors (the proposal's "oracle").
- With `G = 36` (generic random seeds in `[0.08, 0.45] m`), `E_worst >= sqrt(20/36) = 0.745`. The `< 0.20` threshold requires `G <= 16`.

I checked this numerically: with 36 orthogonal-support blocks and an optimal 16-dimensional subspace, the captured fractions sum to exactly 16.

This leaves the protocol in a dilemma:
- **The 128-cell Voronoi dictionary resolves the length shells.** Then the successor gate fails for a mathematical reason unrelated to weighting, normalization or the encoder. `RANK_LIMIT_FAIL` is pre-determined, and the comparison between arms is meaningless.
- **The dictionary does not resolve the shells.** This is likely: there are about 3.5 cells per geometry, and in `L_*`/`T_*` units the shells are separated by about 0.05 while the angular channels span several units. Then `M_k` is blind to tip length, and the successor gate tests nothing about the length/lever-arm semantics the proposal claims to retain. The floor is escaped only by coarse-graining away the information the brief asks us to preserve.

The same mechanism is present in *training*. Section 5.1 draws FB outcome references from the pooled target law, so the FB loss asks `F_k^T B(g')` to vanish on other-geometry outcomes `g'`. That is exactly the block-orthogonal demand. This is the real, physically grounded form of the brief's "rank bottleneck" question, and the proposal's SVD analysis misses it.

*Required remedy:* define the successor target and the FB reference draws under the **configuration-restricted** measure `rho_k`. Columns are restricted to cells with positive `rho_k` mass, and `A_B^{(k)}(:,j) = E_{rho_k}[B(g) phi_j^{(k)}(g)]`. Because length is identifiable from `g13` alone, a shared B can then reuse its 16 output directions independently on each shell. The cross-geometry rank obstruction disappears, and the residual sharing constraint applies only among the four strokes of a geometry, whose supports overlap, and to B's 74k-parameter capacity. The proposal should state the theorem above, adopt the restricted measure, and justify any retained pooled-measure diagnostic as a deliberate stress test. That would actually "rigorously resolve" the 0.943 objection the rubric asks about. The current text only relabels it as unproven.

**[MAJOR-1] The 128-indicator dictionary is too coarse for a meaningful `< 0.20` relative error claim, and its coarseness interacts with the result.** With 144 configurations whose within-configuration outcome manifolds are about 3-dimensional `(q, omega, a)`, 128 global Voronoi cells give each configuration only a handful of occupied cells. Relative error on such a coarse panel is dominated by cell-boundary effects. A 60 × (few occupied columns) `M_k` can be nearly rank-limited by its own occupancy, which makes a small tail cheap. The proposal concedes that a finite projection "can miss difficult functions," but it gives no resolution argument. Specify a per-configuration dictionary (for example ≥ 64 cells per `rho_k`) or a smooth basis, and report sensitivity of `E_worst` to dictionary size as a pre-registered secondary analysis.

**[MINOR-1] The Audit #7 mechanism is asserted, then argued to be weakened, but not analyzed.** Section 1.2 correctly notes that sphere projection equalizes encoded trace, which undercuts the brief's "long links dominate `Sigma_B`" premise. It then defers the remaining channels (Jacobians, occupancy, angular allocation) to experiment. A short analysis of a linear-then-normalize encoder `b = 4Wg/||Wg||` under global whitening would show whether the `L^2` input scaling biases the allocation of directions, and by how much. It would also give the spike an a-priori predicted sign for `G -> W` and `WS -> NWS`.

**Credit.** Sections 1.3–1.4 are the strongest analysis of the bound I would expect under this rubric. The `M_k = a_k v^T` counterexample (Frobenius-orthogonal blocks with a rank-one stack) is correct and important. So is the observation that conditioning `F` cannot enlarge the shared right span.

### Dimension 2: Resolution of Audit Issue #7 (25%)

**[CRITICAL-2] The recommended conditional target `Sigma_k = I_16` for every k is provably incompatible with affine decodability of any physical field whose conditional second moment varies across configurations. This includes length, tip position, tip velocity and tip acceleration. The penalty therefore fights the proposal's own zero-shot semantics gates.**

Suppose `Sigma_k = E_k[b b^T] = I` for all `k`. For any affine probe `y_hat = w^T b + c`, it follows that `E_k[(w^T b)^2] = ||w||^2` for **every** configuration. If the probe decodes a scalar field `y` with conditional RMS error `eps_k`, Minkowski gives

`| sqrt(E_k[(y - c)^2]) - ||w|| | <= eps_k` for all `k`.

- **Length** (`y = ||p|| = L_k`, constant within a configuration): this requires `|L_k - c|` to lie in the band `||w|| ± 0.05 L_k` for all 36 lengths in `[0.08, 0.45]`. At most two length clusters can satisfy that. The §5.4 gate ("decoded length relative RMS ≤ 5%") is therefore unattainable at the penalty's optimum.
- **Tip fields** (`y = p_x`, for example): `E_k[p_x^2] = L_k^2 E_k[cos^2]` varies by up to `(0.45/0.08)^2 ≈ 31.6` across configurations, which again contradicts a configuration-invariant `E_k[(w^T b)^2]`. The same argument applies to the *centered* conditional covariance with `Var_k`, because `Var_k(v_x) ∝ L_k^2`.

The decomposition in §2.3 makes the conflict explicit: `L_cfg` contains `(1/144) sum_k ||Sigma_k - Sigma_*||^2`, which penalizes *any* configuration-dependent second-moment structure. That is exactly where linearly accessible scale information has to live. At `lambda_cfg = 1`, frozen, the result is a tug-of-war whose equilibrium is not analyzed. The selection rule in §5.5 can then end up rejecting WS/NWS for a reason the proposal itself created.

The brief's own phrasing ("share a common isotropic covariance `Sigma_B^{(k)} ≈ I_16`") contains the same tension. A primary author should have flagged it rather than adopted it, since the rubric weights tip preservation at 25%.

*Required remedy:* replace the exact-isotropy conditional term with a **rank-floor** term aligned with the actual gate. Options:
- a hinge on eigenvalues, `sum_k sum_i relu(tau - lambda_ki(Sigma_k))^2`;
- a hinge on `erank(Sigma_k)` or on the Rényi-2 surrogate `256/tr(Sigma_k^2)`, using the proposal's own bound;
- isotropy imposed only on the centered covariance restricted to a learned subspace, leaving the means `mu_k` and a reserved scale direction free.

By the Rényi bound already in §1.5, a floor such as `tr(Sigma_k^2) <= 64/3` certifies `erank >= 12` without forcing identical moments. Then re-check the length and tip decoding gates against the new optimum.

**[MAJOR-2] The conditional estimator is too sparse to bite, and the IPW pooled machinery is redundant given the samplers the proposal already requires.**
- *Sparsity:* one configuration per update over 12,000 updates gives about 83 penalty visits per configuration, each with 2 × 64 samples. Against a pooled term that acts every update, the per-configuration constraint is weak and noisy. "Additional configurations can be processed sequentially" is offered but not registered, so the registered arm is the sparse one. Register `m` configurations per update (for example 16, giving about 1,300 visits each), with the loss rescaled to stay unbiased, and log per-configuration penalty trajectories.
- *Redundancy:* the conditional micro-batches are drawn directly from the target law `(alpha, beta)`, and the 10% mixture already requires a direct target-law sampler. The pooled orthogonality batch can therefore be drawn from the target law too, with no importance weights, no ESS loss and no `w <= 10` clipping concern. IPW is needed only if the orthogonality loss must reuse FB replay batches, and the proposal does not state that requirement. As written, arm W tests an estimator that a simpler exact sampler dominates. Either justify the batch-reuse constraint or make W a direct-sampling arm.

**[MINOR-2] `rho_{k,e,r}` is not fully specified for training.** Within a resident cell, the training-time conditional law is whatever the buffer contains, which depends on collection history. The proposal states that the *evaluation* law is frozen, but `L_cfg` is computed against the training-time law. State which law the training penalty targets and how it is kept identical across arms (the common frozen transition bank in §5.1 appears to do this; say so explicitly).

**Credit.** The hierarchical IPW formulation (§2.2), the "no zero-probability target mass → `INSUFFICIENT_SUPPORT`" rule, the unbiased two-batch cross estimator, and the refusal to force static-hold or single-scene cells to isotropy (§2.3) are all correct and well specified. The formulation the rubric asks for is present. What is wrong is the target it optimizes toward.

### Dimension 3: Preservation of Tip Kinematic Information (25%)

**[CRITICAL-2 applies here as well; it is the primary objection on this dimension.]**

**[MAJOR-3] The transform `T(g)` makes physical tip kinematics multiplicative, and its angular "nondimensionalization" is only a unit change.**
- After dividing by `L`, the planar tip channels `(p/L, T v/L, T^2 a/L)` are deterministic functions of `(q, omega, a)`, which are already present in slots 0–3. Within a configuration they are redundant, and **all** lever-arm information is carried by the single scalar `r_L`, which is constant within a configuration. Physical tip velocity `L omega (-sin q, cos q)`, which is linear in the raw inputs, becomes a product `r_L × (normalized term)` that the MLP must synthesize. Exact invertibility of the *preprocessing* (credited) does not make the *learned* embedding preserve tip semantics, and under CRITICAL-2 the conditional penalty actively discourages it. The proposal states this limitation honestly in C-B03-B-03, but it does not offer a mitigation. For example, it could keep one or more raw-scale tip channels alongside normalized ones in redundant slots (`p_z/L` is constant for a planar link and is a second redundant slot), or show that the WS → NWS comparison isolates this cost.
- `T_* = 0.10 s` is a global constant. Capacity tiers and stroke profiles change `(omega, a)` distributions through inertia and torque limits. The brief asks for a common covariance "so that all 144 configurations share" one, so a configuration-intrinsic time scale is the natural nondimensionalization. Using it is either deployment-pure (if derivable from calibrated `x137`, which B does not see) or not. The proposal should state why B cannot be given it and what residual anisotropy is expected.
- `L(g) = ||p||` is the lever arm only if `p_z = 0` and the housing origin lies on the joint axis. The proposal's claim "`r_L` lies in `[0.4, 2.25]`" depends on this, and so does calling `r_L` the lever arm. Use `sqrt(p_x^2 + p_y^2)` as the lever arm, or add the axis-origin condition to the schema guard.

**[MAJOR-5] Zero-shot decoding thresholds are absolute in SI units and therefore non-uniform across the length range under study.** The tip-position gate is `0.02 m`. For `L = 0.08 m` that is 25% of the radius, an angle-equivalent error of about 14°, which is laxer than the 5° angle gate. For `L = 0.45 m` it is about 2.5°, which is stricter. Tip velocity and acceleration gates have the same issue. The gate therefore favors short links precisely on the dimension (length) being studied. Use length-relative thresholds (for example `0.10 L_k`, `0.10 L_k/T_*`), keep the separate length gate, and report both forms.

**Credit.** The rejection of `p/L` without a scale carrier (C-B03-B-03), the explicit inverse, the `SCHEMA_INCOMPATIBLE` guard, applying the same transform to reached, desired, replay and target inputs, and retaining raw outcomes for reproducibility are all sound. The proposal also correctly declines to claim momentum observability, since `g13` contains no mass.

### Dimension 4: Spike Falsifiability (20%)

The proposal pre-registers per-group `erank >= 12` with simultaneous bounds, per seed, plus centered checks and negative controls. That meets the rubric's literal requirement. The objections concern whether the gates are *jointly satisfiable* (CRITICAL-1, CRITICAL-2) and whether the statistics are valid. See §4 below for [MAJOR-4], [MAJOR-6] and the minor protocol issues.

---

## 3. Audit of Rejected Alternative & Necessity Claim (`C-B03-B-01`)

### 3.1 Rejected alternative: global replay balancing + single shared whitening

- **Reason 1 (an invertible common `A` preserves the algebraic rank of each `Sigma_k`; in the counterexample `A = I`): correct.**
- **Reason 2 (sphere reprojection after whitening breaks exact whitening and bilinear preservation): correct.**
- **Reason 3 (per-configuration whitening needs a deployment-time selector): overstated.** Geometry, though not stroke, is exactly identifiable from `g13` via `||p|| = L`. A geometry-conditional whitening map indexed by `r_L` would need no external selector. What actually stops it is (i) its table of fitted matrices, which consumes budget or requires a parametric family in `r_L`, and (ii) the stroke-level ambiguity. More importantly, **per-configuration whitening to `I` has the same defect as the proposal's own `L_cfg` target (CRITICAL-2)**. The proposal rejects the former for interface reasons while adopting the latter, which is inconsistent. The correct reason for rejecting both is that conditional exact isotropy destroys linearly accessible scale structure.
- **Missing alternative:** a conditional **rank-floor** penalty (eigenvalue hinge or Rényi-2 bound) is the obvious competitor to `||Sigma_k - I||^2`. It targets the pre-registered gate directly and leaves configuration-dependent means and scale directions free. It is neither considered nor rejected. Given CRITICAL-2, it is probably the right recommendation, and its absence is the main gap in this section.
- The second rejected shortcut (`p/L` with no scale carrier) is correctly rejected.

### 3.2 Necessity claim `C-B03-B-01`: "Pooled isotropy cannot certify conditional resolution"

- **Mathematical validity: confirmed.** With 9 groups per axis and `b = ±4e_j`, each `Sigma_k = 16 e_j e_j^T` (rank one, and also centered rank one since the mean is zero), while the uniform average equals `I_16`. Exact IPW leaves this unchanged. Grade 1 (mathematical counterexample) is appropriate.
- **Scope of "necessity": correctly narrow but easily misused.** The claim shows that conditional *evidence* is necessary to *certify* per-group rank. It does **not** show that a conditional *training loss* is necessary to *achieve* it, and the proposal says so ("A particular conditional loss is not logically necessary"). However, §2.3 and the recommendation lean on this claim to motivate `L_cfg`. The adjudicator should record that `C-B03-B-01` supports **conditional measurement in the gates**, which I endorse. It does not support the specific `Sigma_k → I` training term, which CRITICAL-2 shows is harmful.
- **The physical-relevance disclaimer is too modest.** The proof's premise ("an encoder that can distinguish the constructed groups") is said not to assert anything about physical V3 supports. In fact it is **physically satisfied at geometry granularity**: `||p||` identifies the length shell exactly from a single raw `g13`, and under NWS `r_L` makes this linearly trivial. So pooled-only certification is not just logically insufficient; V3's outcome geometry actively permits the collapse pattern (up to 36 separable groups, which exceeds the 16 axes). The claim should be upgraded to say so. Note also that NWS makes group identification *easier*, which slightly raises the collapse risk the claim warns about.
- **The boundary is incomplete.** The text names only "identical conditional outcome laws" as the structural restriction that would remove the need for conditional evidence. A weaker, **measurable** restriction gives a partial certificate. If `rho_k >= c rho_*` pointwise (a density-ratio overlap bound), then `Sigma_k ⪰ c Sigma_* = c I`, so `lambda_min(Sigma_k) >= c`. By Schur-concavity, the worst case is `(16 - 15c, c, …, c)`, and `erank >= 12` holds once `c ≳ 0.735` (computed: `c = 0.73 → 11.90`, `c = 0.74 → 12.12`). For distinct-length geometries `c = 0`, so no certificate exists and the claim's conclusion stands. For the four strokes sharing a geometry, overlap is plausible, and this route can be checked on data without reference to the encoder. Add it to the boundary statement. It also gives a cheap pre-training diagnostic of where conditional collapse is even possible.
- **Falsification route:** correctly identifies that only an implementation can be falsified, not the algebra. That is acceptable for a Grade-1 claim.

**Recommended disposition:** **accept `C-B03-B-01` as Grade 1** with three amendments: (a) state that the distinguishability premise is physically met at geometry level; (b) add the density-ratio partial-certificate boundary; (c) explicitly restrict its use to justifying conditional *gates*, not the `Sigma_k = I` training target.

*(Related, for the adjudicator: `C-B03-B-02` is correct as stated, but CRITICAL-1 shows its floor can be **derived**, not merely measured, under the pooled measure: `>= sqrt(1 - 16/G)`. Under that measure its own conclusion, that no weighting or normalization change can reach `< 0.20`, is already true analytically.)*

---

## 4. Spike Protocol Critique

**Design strengths.** The protocol has paired seeds and arms on a common frozen transition bank, a single registered ladder (`G → W → WS → NWS`) with a no-fifth-method rule, all-seeds-must-pass, simultaneous bounds by bootstrapping the minimum or maximum directly, an encoder-independent successor target, `UNDERPOWERED` instead of silent replacement, constant, axis and high-frequency negative controls, sensor-resolution-aware rank, and a genuine morphology holdout with separately renormalized training laws. This is well above the bar for pre-registration.

**[CRITICAL-1 / CRITICAL-2, protocol consequence] The successor gate and the decoding gates are not jointly satisfiable as specified.** Under the pooled reference measure with a length-resolving dictionary, `E_worst < 0.20` is impossible (`>= 0.745`). Under a length-blind dictionary, the gate does not test length. Under the recommended `L_cfg` optimum, the length and tip affine-decoding gates are unattainable. A spike whose PASS region is empty, or reachable only by under-resolving the target, is not a falsification test of H3. Fix the measure (use `rho_k`) and the conditional target (use a rank floor) before freezing.

**[MAJOR-4] The uncertainty quantification is not valid at the registered successor sample sizes.** Each `(k, e)` cell contributes **two** source states (60 rows per configuration = 5 scenes × 2 states × 3 actions × 2 latents). An "episode bootstrap preserving cells" over n = 2 units per cell is degenerate, since only three distinct resamples exist. The simultaneous 95% upper bound on a *maximum over 144 groups* computed from it will be badly anti-conservative. The 32 → 128 continuation expansion reduces branch noise but not source-state sampling variance. Register at least about 10–20 source states per `(k, e)` cell, or define the successor gate conditional on the fixed source panel (which then supports no population claim), and state which inference is intended.

**[MAJOR-6] The reference-policy family exercises only one latent dimension.** `q_ref` depends on `z` only through `tanh(z_1)`, and the panel uses two latents differing in `z_1`. The successor operator's `z`-dependence is therefore one-dimensional. A rank-16 bilinear test on a policy family indexed by one scalar is a weak test of H3, which concerns "all 144 configurations" under the bilinear `F(…, z) B` structure. Fixing the actor to make the operator encoder-independent is a good idea, but the family should vary along several registered `z` directions (for example the target, gain scale and velocity-damping scale from three `z` coordinates), with at least four or more latent vectors per row block. The gains are also stated ambiguously ("2 per radian and 0.2 s per radian"). Write the units of `u` explicitly.

**[MINOR-3] The `WS → NWS` attribution is confounded.** NWS changes both the transform and the normalizer ("balanced frozen normalization" versus "frozen baseline normalization"). The proposal acknowledges this, but a fifth control is cheap: WS with balanced normalization. It isolates the transform, which is the only part of NWS the brief asks about. Register it now rather than forbidding it.

**[MINOR-4] The morphology holdout mixes interpolation and extrapolation.** Withholding the shortest and longest seed in each tier forces `r_L` extrapolation, while the lower-median seed is interpolation. Report the two separately; a combined gate will be dominated by the extrapolation endpoints. G is not retrained on the 108-configuration split, so the `G → W` effect cannot be attributed on the holdout. State this as a limitation or include G.

**[MINOR-5] A fixed 12,000-update budget has no convergence diagnostic.** A FAIL could reflect under-training of FB/B, especially given the sparse conditional term ([MAJOR-2]). The `FIT_FAIL` code exists, but no criterion separates "fit had not plateaued" from "intervention failed". Register a training-loss plateau statistic computed on the frozen validation split, without changing the stopping rule. This keeps FAIL interpretable without inviting checkpoint selection, and it is consistent with Charter §2.4.

**[MINOR-6] The cost is not "minimal".** The protocol needs 720 cells × 160 test episodes (about 115k), plus calibration (up to 4× doubling), plus 8,640 rows × 32–128 continuations × `H`, where `H ≈ 527` steps if `gamma = 0.99`. That is about 1.5 × 10^8 to 5.8 × 10^8 simulator steps for the successor panel alone. Then come three seeds × four arms plus a three-arm holdout retrain. Give a compute estimate and a staged plan (a synthetic negative-control stage, then a subset-of-geometries pilot, then the full panel), since the whole spike is blocked until B02 physics integration exists.

**[MINOR-7] There is a small specification gap in `T(g)` validation.** The FP64 `1e-6` identity check suits computed fields but not measured ones; see the gate audit. Say which fields of the locked layout are computed kinematics and which are sensor readings.

### Summary of required changes before freezing

1. Redefine the successor target and the FB reference draws under per-configuration `rho_k`. State the `sqrt(1 - 16/G)` pooled-measure theorem (CRITICAL-1).
2. Replace `||Sigma_k - I||^2` with a rank-floor conditional penalty. Re-derive compatibility with the length and tip decoding gates (CRITICAL-2).
3. Increase source states per cell so the simultaneous bootstrap is valid (MAJOR-4). Diversify the `z` directions in the reference policy (MAJOR-6).
4. Densify the conditional estimator. Justify IPW over direct target-law sampling or drop it (MAJOR-2).
5. Make the decoding thresholds length-relative (MAJOR-5). Address multiplicative tip synthesis and the global `T_*` (MAJOR-3).
6. Amend `C-B03-B-01` as described in §3.2.
