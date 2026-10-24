# Blind Review A on Proposal B (Packet B04)

Reviewer: Blind Reviewer A. Sources read: `PROGRAM_CHARTER.md`, `packets/B04/brief.md`, `packets/B04/proposals/B.md`. I read no other review or draft. I did not open `baseline/01` or `baseline/03`, so any claim in Proposal B that rests only on those files (the radius-4 latent convention, the 13-field g13 order, the x137 filter formula, the B02/B03 decisions) is marked *unverified by this reviewer*. It is not marked wrong.

I re-derived every closed-form quantity in §1 and §3.1 independently with float64 checks. A dynamics derivation that is correct but never tested against the benchmark's own numbers misses the most important result. Using the nominal parameters, I computed static stance actuator demand under the proposal's own equations of motion (EOM) at every commanded stance height:

| Hip height Ht (m) | Hip u1 | Knee u2 | Where it occurs in Proposal B |
|---|---:|---:|---|
| 0.80 (≈ full extension) | — | — | IK limit |
| 0.70 | −0.18 | −0.71 | hop extension target |
| 0.62 | −0.23 | **−0.92** | (B02 static-hold guard boundary) |
| 0.60 | −0.25 | **−0.97** | reset pose H0 for squat and hop |
| 0.55 | −0.27 | **−1.06** | hop final hold, landing h*, tucked pose |
| 0.50 | −0.29 | **−1.14** | hop pre-squat |
| 0.45 | −0.31 | **−1.21** | squat hold [3,6] s |

Method: rail base, quasi-static, Fn = m_t g, Ft = 0, joint torque S u = G − Jfᵀ F with the proposal's own M, G, Jf, IK and nominal masses. Results are identical for mp ∈ {0, 0.2} (see O-1.2).

This single table drives most of the severity in this review.

**Summary verdict.** The mechanics are clean and mostly correct. The fairness controls are unusually thorough, and so is the guarding of falsification semantics. However, the canonical benchmark as specified is **physically infeasible at nominal parameters for two of its three task families**, and that would yield a near-certain `INCONCLUSIVE` or a spurious modular-vs-raw comparison. The "payload" manipulation is null in stance. The support-qualification test is statistically miscalibrated in a way that also pushes toward `UNKNOWN`. All three problems can be fixed, but they must be fixed before the benchmark can close Audit Issue #9.

---

## 1. Gate & Hard-Constraint Audit

| Gate / constraint | Source | Status | Notes |
|---|---|---|---|
| Charter §2.1: deployment proprioceptive purity | Charter | **PASS** | π and B see only their own x137 and z16/g13 (§2.2). The upper policy and critic get O = (x137,1, x137,2, h, hdot, d16), with no contact, payload, solver or future-reaction fields. The rail encoders feed only the upper layer, which Charter §2.1 does not restrict. Stage 1 adds randomization of inaccessible fields to test output invariance. |
| Charter §2.2: causal privileged forward inputs | Charter | **PASS (n/a downstream)** | F and p5065 are explicitly absent from downstream inference. The latch-timing audit ("no current-interval solver reaction reaches an action already latched") is appropriate. |
| Charter §2.3: zero fabricated coverage | Charter | **PASS** | Stage 0 requires a real-physics 144×5 qualification artifact, failures kept. A `coverage_ready` boolean or surrogate is rejected, and `BLOCKED_LOCAL_QUALIFICATION` is the fallback. |
| Charter §2.4: smoke run ≠ converged control | Charter | **PASS** | Stated explicitly in the preamble and in §6.1. |
| Brief §2: local (B, π) frozen | Brief | **PASS** | Hash checks; only upper parameters are in the optimizers; calibration-constant updates are limited to the existing schema. The ban on "repairing between cells" is explicit. |
| Brief §2: fair raw-torque baseline with identical proprioception | Brief | **PASS, with a caveat** | C receives the same 292-D O and the same scaler. Equal-upper-parameter (140,000) and total-deployment-budget (421,617) C variants are both specified, and I verified both counts: 149,056 / 147,508 / 141,316 dense; 421,617 = 140,000 + 281,617; 563,234 = 2 × 281,617; d16 sums to 16; O = 2·137 + 2 + 16 = 292. The caveat is the exploration-scale asymmetry in O-2.2. |
| Brief §3 D1: exact EL equations, coupling torque decomposition, inside/outside determination | Brief | **PARTIAL** | Equations are correct (O-1.1). The inside/outside determination is deferred entirely to future empirical envelopes, and the one decisive coupling term, stance contact torque, is never evaluated at task conditions (O-1.2). |
| Brief §3 D2: Modes A, B, C compared | Brief | **PASS** | All three arms are specified, and the proposal correctly separates C (raw torque) from baseline/01's blending interface. |
| Brief §3 D3: standardized 2-DoF benchmark (tracking, payload squat/hold, hop/landing; sample-efficiency; L2/C0 swap) | Brief | **FORMALLY PRESENT, SUBSTANTIVELY FAILING** | Fully specified, but the squat, hop and landing tasks violate actuator capacity at nominal parameters, and the squat payload has no stance effect (O-4.1, O-4.2). |
| Internal consistency with its own §1.4 rule ("static holds require r ≤ 0.92; exceeding this is an actuator feasibility violation") | Self | **FAIL** | Every stance hold the benchmark prescribes (H = 0.60, 0.55, 0.50, 0.45) violates the proposal's own guard at the knee. |
| No fabricated results | Self | **PASS** | It is a preregistration only; empty result files are banned. |

Gate summary: no charter boundary is breached. The packet-level deliverable D3 does not yet meet its purpose, because a benchmark whose nominal tasks are infeasible cannot "close Audit Issue #9".

---

## 2. Rubric-Keyed Technical Objections

### R1. Exactness of Serial-Chain Coupling Reduction (30%)

**What I verified as correct.** I checked M, c, G and Jf for the fixed-base two-link chain with foot payload, along with the A, D, H, K, d definitions. The rail augmentation [[m_t, aᵀ],[a, M]] is correct, with a = ∇_q Y(q) and c_h = ȧᵀq̇. I confirmed that the h-dot cross terms in the q-equations cancel, because the Hessian of Y is symmetric. The Schur form M − aaᵀ/m_t with load −(a/m_t)(Fn − c_h − m_t g) is correct. The τ_ext decomposition is an exact identity for any fixed J0j. All the numbers in §1.4 reproduce: A = 0.197333, D = 0.069333, H = 0.088, inertial bounds 10.93 / 3.79 N m, Coriolis bounds 4.22 / 1.41, gravity bounds 5.69 / 0.785, contact 24 / 12. The warnings against double-counting −τ2 and against relabeling Jeff are valuable.

- **[CRITICAL] O-1.2: The dominant coupling term, stance contact torque, is never evaluated at the benchmark's own operating points. Evaluating it shows the nominal tasks exceed capacity.** §1.4 bounds contact torque with an arbitrary "30 N contact" and says "even moderate force can exceed actuator capacity", then moves on. But static stance alone forces Fn = m_t g = 36.3 N. Through the proposal's own Jf and IK, that gives a knee demand |u2| = 0.97 at the reset height and 1.21 at the squat bottom (table above). The rubric's core ask is to quantify coupling relative to E3/E4 amplitudes, which the proposal says top out at net demand 0.92. The answer the proposal's own algebra gives is that **body-weight transmission alone exceeds the E3 ceiling at every prescribed stance pose**. The proposal never states this. The entire §1.4 comparison is done for the fixed-base, contact-free case with mp = 0.2, which is not the configuration of any task (the tracking task uses mp = 0).
- **[MAJOR] O-1.3: The kinematic bounds (V = 4 rad/s, A = 20 rad/s²) are not derived from the task references, and they do not bound the declared stress tier.** At the 1.5 Hz tracking stress tier, the knee reference acceleration is 0.30·(3π)² = 26.6 rad/s² and the hip's is 22.2 rad/s². Both exceed A = 20 before any tracking error is added. No A_b value is given at all for the rail, even though the hop's 0.25 s extension and the landing impact are where A_b, and hence the (K+d)A_b term, are largest. The bounds should be computed from the reference trajectories by inverse dynamics, per task and per morphology cell. A table of nominal-design numbers is the minimal standard for a 30%-weight dimension.
- **[MINOR] O-1.4: "In free fall gravity can largely cancel" understates the result.** With a frictionless, non-rotating carriage, G(q) = g·a(q) identically, so in flight the Schur-reduced gravity term is exactly zero. For the knee and hip units this means τ_grav,j = −G0j exactly. Flight is therefore a deterministic "gravity-off" regime that is out of distribution for any unit trained with a gravity-loaded housing. The proposal should state this exactly and pre-classify flight windows as such, rather than leaving it to the envelope test.
- **[MINOR] O-1.5: For the hip, the "distal link" is an articulated chain, not a rigid D.** Choosing J01 = I1 + m1c1² (thigh only) is a stated convention, but the proposal does not say which geometry/inertia calibration constants the frozen hip unit receives. In single-unit training, D was rigid; at the hip it now includes a posture-varying shank. This affects §3.3, where changing L2 also changes the hip unit's distal plant and not only the knee's. The calibration mapping for each joint must be specified.
- **[MINOR] O-1.6:** The local equation carries both "b_j q̇_j" and "τ_fric,j" while the benchmark friction is a single law. State which part maps to which, or the τ_ext audit will double-count viscous friction. Also, the knee housing acceleration a_P2 is given for a fixed hip only; add the ḧ ŷ term for the rail case.

### R2. Fairness of Modular vs Raw-Torque Ablation (25%)

This is the proposal's strongest dimension. It has an identical 292-D observation, a 50 Hz decision rate, an identical transition budget and optimizer-step count, a masked equal-parameter policy, a total-deployment-budget C, a raw-policy pretraining control, paired seeds, and amortization reporting.

- **[MAJOR] O-2.2: The scale-invariant adapters create an exploration and optimization asymmetry that the sensitivity arm does not fix.** In A, z = 4v/‖v‖ with v ~ N(μ, σ²I₃₂). At initialization the head gain is 0.01, so μ ≈ 0, while σ = e^−0.5 ≈ 0.61. The latent direction is therefore effectively uniform on the sphere and independently redrawn every 20 ms. For commanded z to become consistent, ‖μ‖ must grow well beyond σ√32 ≈ 3.4. That is an interface-induced signal-to-noise problem with no counterpart in C, where tanh(N(0, 0.61²)) is a bounded, centered torque dither. B has the same issue through its 26-D raw output fed to Pκ. Matching "initial torque variance" on dev seeds does not equalize this, because the problem lies in how the policy-gradient signal scales with ‖μ‖, not in torque variance. The fix is to parameterize A's noise on the tangent space or as a von Mises–Fisher distribution, or to report a pre-registered arm with the head gain set so that ‖μ‖/σ is comparable. Without this, A − C conflates representational benefit with action-parameterization artifacts, in either direction.
- **[MAJOR] O-2.3: Pκ is discontinuous and computationally disproportionate, which confounds Mode B.** A 33-start SLSQP solve with a lexicographic tie-break and fallback-to-previous-target is a piecewise, discontinuous map from raw actions to g13. Small policy perturbations can switch basins, so PPO's likelihood-ratio updates see a noisy, non-smooth environment that is specific to B. The cost is also large: 2 joints × 33 starts × 2,048,000 transitions comes to about 1.35×10⁸ SLSQP solves per (task, seed), or about 4×10⁹ across 3 tasks × 10 seeds, at up to 200 iterations each. Inference latency within 20 ms is also not demonstrated. If B loses, the protocol cannot tell "the B∘Pκ image is restrictive" apart from "the Pκ discontinuity broke PPO". Pre-register a smooth surrogate (a single warm-started solve from the previous q*, or a closed-form kinematic parameterization of the g13 manifold), and report adapter-switch frequency as a diagnostic.
- **[MINOR] O-2.4: The evaluation action mode is unspecified.** The proposal does not say whether evaluation uses the deterministic mean or sampled actions. This affects reproducibility and the premise of C-B04-B-01, which assumes a deterministic policy. Specify the mode.
- **[MINOR] O-2.5: Reset-buffer realism differs by arm in effect.** Buffers are filled with zero-action proprioception while the fixture holds the stance. On release, the knee unit sees a near-capacity load step (≈0.97 C0) with a u-history of zeros. This is an E4-style onset of unknown support that A and B must absorb through a frozen prior, while C learns it directly. That may be acceptable, but it should be named as part of what is being tested and not left implicit.

### R3. Morphology-Transfer Falsifiability (25%)

Positives: a full 3×3 L2 × C02 grid with paired changes; m2 held fixed while c2 and I2 are recomputed; IK recomputed; no new normalizer fitting or latent search; the "unseen by upper ≠ unseen by local" distinction; a both-unseen panel.

- **[CRITICAL] O-3.1: The transfer grid is dominated by physical infeasibility, so retention failures are uninterpretable.** At the 0.45 m squat hold, my static knee demand per cell is:

  | L2 \ C02 | 6.75 | 9.00 | 11.25 |
  |---|---:|---:|---:|
  | 0.32 | 1.35 | 1.01 | 0.81 |
  | 0.40 | 1.61 | 1.21 | 0.97 |
  | 0.48 | 1.81 | 1.36 | 1.09 |

  Only one of nine cells is statically feasible, and even that one exceeds the 0.92 guard at the shallower poses. For the hip, q1 at L2 = 0.48, H = 0.45 is −2.766, which is inside the 0.05 rad Pκ margin of the −2.8 stop, so E1 stop contact enters as well. "Swapped minus nominal success ≥ −0.10" would then mostly measure actuator saturation, not representational transfer. The grid must be redesigned around a feasible nominal: lighter carriage, shallower poses, or higher C0 (see O-4.1), with a per-cell inverse-dynamics feasibility certificate published before training.
- **[MAJOR] O-3.2: The transfer PASS criterion is not comparative.** The criterion "lower bound on mean zero-shot success difference ≥ −0.10" is applied per arm, in absolute terms. H4 and the brief ask whether modular composition transfers *better than* raw torque. An arm can PASS while C retains more, and can FAIL while C collapses further. Add the paired contrast (A_retention − C_retention), with its own interval, to the primary transfer endpoint.
- **[MAJOR] O-3.3: Pooling across the 8 swapped cells contradicts the proposal's own anti-pooling rule.** The proposal rightly requires that "no individual task's nominal success mean < 0.70" so that pooling cannot hide a failed task, but zero-shot retention is pooled as a mean over cells. Add a per-cell floor, or a pre-registered worst-cell criterion, so that a catastrophic failure at C02 = 6.75 cannot be averaged away.

### R4. Benchmark Reproducibility (20%)

Strengths: complete parameter set, contact law, integrator, timestep-halving numerics check, seed blocks, termination and failure taxonomy, reward formulas, artifact list and verdict schema. Reproducibility of *specification* is high.

- **[CRITICAL] O-4.1: The specification reproducibly defines infeasible tasks.**
  - Squat: holds at 0.45 m require knee |u| ≈ 1.21.
  - Hop: the pre-squat at 0.50 m requires about 1.14 before any acceleration is added. The quiet hold at 0.55 requires about 1.06.
  - Landing diagnostic: the final h* = 0.55 is infeasible. A drop of about 0.30 m (v ≈ 2.4 m/s, about 11 J) must be absorbed by 9 N m knees within the peak-force cap Fn ≤ 6 m_t g.
  - Reset: the H0 = 0.60 stance itself requires 0.97 C0.

  The "inverse-dynamics feasibility audit precedes training" clause would catch this, but the canonical benchmark meant to close Issue #9 should be feasible by construction, with a stated reserve. The static demand drops below 0.92 only for Ht ≳ 0.62 m. With m_b = 0.5 kg, the 0.45 m hold falls to |u2| ≈ 0.67. I recommend reducing m_b, or raising C0, or both, and publishing a per-pose demand table with a reserve of at least 20%.
- **[CRITICAL] O-4.2: The "payload squat/hold" payload has zero static effect in stance.** The payload is a point mass at the foot, which is the contact point. Its weight passes directly into Fn, and its joint-torque contribution in stance is exactly zero; my static demands are bit-identical for mp ∈ {0, 0.2}. It only matters in swing and flight, which the squat task does not have. The task therefore does not exercise E3-like load variation at all. The proposal explicitly rejects the torso payload ("optional separate experiment"), which is the only placement that produces a sustained-load manipulation. Make the carriage or torso payload the primary squat condition, or place the payload mid-shank (which still changes distal inertia but also loads the knee).
- **[MAJOR] O-4.3: There is no static friction and no horizontal stiffness, so the foot drifts.** Ft = −0.8 Fn tanh(v/0.01) is zero at rest, so any horizontal force imbalance in a quiet hold produces slow drift resisted only by viscous-like regularization. The |x_foot| ≤ 0.05 criterion over [4,10] s then depends on the regularization constant. Either justify this as intentional (the policy must actively balance the horizontal force through the hip, about −0.25 to −0.31 C0) or add a stiction model. Run the 0.125 ms numerics check on drift as well.
- **[MINOR] O-4.4:** "evaluate at 0,25,600,51,200 and 102,400" is ambiguous because of the thousands separators. Use 0; 25,600; 51,200; 102,400.

---

## 3. Audit of Rejected Alternative & Necessity Claim (`C-B04-B-01`)

### 3.1 Rejected alternative (§4)

The rejection of centralized computed-torque/MPC cancellation as the *primary* test is sound: an oracle model that cancels coupling supplies the missing load model, and success would no longer isolate the frozen representation. Two weaknesses remain.

- **[MAJOR] It conflates oracle contact compensation with proprioceptive model-based feedforward.** The M(q), c(q, q̇) and G(q) terms are computable from joint and rail encoders plus a known geometry, which is information every arm has. Only the contact force and the true payload are privileged. A non-privileged variant would have the upper layer add a feedforward τ̂_coup(q, q̇, q̈_ref) or route it as a calibrated bias. That is a legitimate fourth arm that tests whether *the representation*, rather than *the model*, carries the benefit. Rejecting it on equal-information grounds is incorrect. It should be at least a pre-registered secondary arm.
- **[MAJOR] The privileged positive control is "optional", but it should be mandatory and gating.** Given O-4.1, a model-based feasibility control is the cheapest way to detect infeasible references before spending about 10⁸ PPO transitions. Make it a Stage-1 gate: if the privileged controller cannot reach ≥80% success on a task, that task is blocked from Stage 2.

The secondary rejection (local fine-tuning answers a different question; the legitimate repair is upstream retraining with moving housings and a new frozen checkpoint) is correct and well guarded.

### 3.2 C-B04-B-01: same-input incompatible-action obstruction

**Correctness.** The algebra holds. With equal J and an additive scalar action, the two accelerations differ by Δ = (ℓa − ℓb)/J regardless of u. The 2ε separation argument is valid. The expected squared-error bound Δ²/4 is correct (the minimum of ½(e_a² + e_b²) subject to e_a − e_b = Δ), and the midpoint action is admissible because both required actions are in range and the range is convex. The set-intersection generalization is also correct.

**Necessity value.**
- **[MAJOR] It is not a necessity claim about any design choice.** The proposal concedes that A, B and C all share the obstruction and that sensing, history, coordination or tolerance changes all avoid its premises. It therefore constrains no architectural decision in B04, so nothing in the proposal is shown *necessary*. It is a restatement of non-identifiability (same input, same output). As a Grade-1 lemma it is true but nearly tautological. Its only operational content is a determinism and leakage check.
- **[MAJOR] The proposed test violates the claim's own premises.**
  - A hidden *foot* payload changes D, and hence M22 and M12, so the equal-J premise fails exactly in the case the test proposes. The proposal anticipates this ("use the general set-intersection version").
  - In stance, a foot payload produces no joint load difference at all (O-4.2), so the test cannot create disjoint action sets there.
  - With the reset fixture locking joints and rail during buffer fill, the histories are identical by construction, so the test reduces to checking that the first action is identical. That is a determinism unit test, not an empirical falsifier.
- **[MAJOR] ε is never specified.** The task success criteria are on episode-level RMSE (0.10 rad), not one-step acceleration. Without a pre-registered ε and a stated link from ε to task success, "individually feasible but disjoint action tolerance sets" cannot be constructed reproducibly. For reference, in fixed-base tracking the maximal hidden-payload gravity difference is about g·mp·L2 = 0.785 N m. Disjointness at J ≈ D = 0.069 then needs ε < about 5.7 rad/s², which is far tighter than anything the tasks require. The obstruction therefore never binds task success, because one step later the histories diverge and recovery is allowed.
- **[MINOR]** The claim is stated for deterministic controllers, but the policy class is a PPO Gaussian and the evaluation mode is unspecified (O-2.4).

**Recommendation.** Downgrade C-B04-B-01 to a supporting lemma or a determinism audit, not a candidate necessity claim. C-B04-B-02 (marginal support does not certify joint law) is the more useful claim, because it actually motivates the joint-bin support test. It is correctly scoped as non-necessary for controller success.

---

## 4. Spike Protocol Critique

**Stage 0 (freeze and qualify).** This is excellent and fully charter-aligned. One addition: it should also freeze the *feasibility certificate* from O-4.1 and the per-joint calibration mapping from O-1.5.

**Stage 1 (mechanics, causality, coverage).**
- **[MAJOR] The mechanics spike has no feasibility gate, although it already contains the tool for one.** The "analytic reference tracker" run on 32 seeds per task would expose the saturation in O-4.1 immediately. The protocol should declare that if the analytic or privileged tracker saturates (|u| > 0.92 for more than 10% of static-window samples) or fails success predicates on a task, that task is `INFEASIBLE_REFERENCE` and does not enter Stage 2. As written, these results "do not determine H4 success" and have no blocking role.
- **[MAJOR] The support test is miscalibrated: with N ≈ 20 it rejects truly matched distributions at a high rate.**
  - Mean threshold: the per-bin requirement is a mean discrepancy ≤ 0.25 source SD with ≥ 20 episodes. With n = 20 against a holdout of similar size, the standard error of a standardized mean difference is about √(1/20 + 1/20) ≈ 0.32 SD. Identical distributions fail each component about 40% of the time, and a three-component conjunction fails most of the time.
  - Covariance threshold: a Frobenius discrepancy ≤ 25% at n = 20 is similarly below sampling noise (relative standard error of a covariance entry ≈ √(2/n) ≈ 0.32).
  - Bin count: 5⁴ bins over (q, q̇, r, M_jj/J0) × 2 signs × 5 regimes is about 6,250 bins per configuration. Requiring ≥ 20 independent source episodes per bin, plus z cosine ≥ 0.95, makes most bins `UNKNOWN`.
  - Combined with the ≥ 95% supported-window requirement, the "operational supported-load panel" will almost surely be empty, and every H4 result will be `INCONCLUSIVE` by construction.

  These are equivalence-testing questions. Use TOST-style equivalence margins with power computed for the realized bin counts, coarser or adaptive bins (for example, quantile bins on r and M_jj/J0 only, conditioned on regime), and a pre-registered minimum power. Then report false-rejection rates calibrated on source-vs-source splits. The proposal's statement that "these stringent checks may fail" is honest, but a falsification instrument that fails under the null cannot falsify anything.
- **[MINOR] Unclear role of the scripted downstream probes.** The envelope is built from upstream rollouts (correct), but it is unclear whether the support panel used for H4 attribution is computed on the scripted probes or on the learned arms' evaluation episodes. It must be the latter, per arm, because different arms visit different states.
- **[MINOR] Missing physics tests.** The physics checks are thorough (symmetric positive-definite M, finite-difference EL, Schur vs full solve, power identity, timestep halving). Add the exact flight identity G − g·a = 0 (O-1.4) and a static-friction drift test (O-4.3).

**Stage 2 (downstream comparison).**
- The budget arithmetic is consistent: 1,000 iterations × 2,048 transitions = 2,048,000; 10 epochs × 8 minibatches = 80,000 steps; evaluation every 50 iterations gives 21 points. Paired seeds and episode keys independent of failure length are good design.
- **[MAJOR] Ten seeds with a percentile bootstrap is anti-conservative.** A 97.5% percentile bootstrap over 10 paired seeds for a ratio of restricted means (with heavy right-censoring expected for C on hop) under-covers. Use BCa or a studentized bootstrap, plus a pre-registered exact or permutation test on the paired differences. Better, run a power analysis on dev seeds to justify n = 10, or raise n. Also state that the 97.5% level is a Bonferroni split over the two primary contrasts, and that the bounds are one-sided as used.
- **[MAJOR] Censoring both arms at the horizon biases the T80 ratio toward 1.** If both A and C censor at 2,048,000 on a task, the ratio is exactly 1, which counts against PASS even if A is much closer to threshold. Pair the RMST ratio with the AUC endpoint as a co-primary, or pre-specify the handling when both arms are censored.
- **[MINOR]** The 20% effect-size falsification and the "OOD failure falsifies unrestricted reuse, not the conditional hypothesis" semantics are well constructed and should be kept.

**§6.4 Artifacts and stopping.** The artifact list and verdict schema are good. Add `feasibility_certificate.json`, carrying per-task and per-cell inverse-dynamics demand and reserve, plus a `support_calibration.json` with source-vs-source false-rejection rates, and make both blocking.

---

### Indicative rubric assessment (reviewer's view, for adjudication only)

| Dimension | Weight | Indicative | Main driver |
|---|---:|---:|---|
| Coupling reduction | 30 | 19 / 30 | Exact and verified, but the dominant stance-contact term is never evaluated, and it reveals the infeasibility (O-1.2). |
| Ablation fairness | 25 | 20 / 25 | Best-in-class controls; latent-exploration and Pκ asymmetries remain (O-2.2, O-2.3). |
| Transfer falsifiability | 25 | 14 / 25 | 8 of 9 cells statically infeasible; criterion not comparative to C (O-3.1, O-3.2). |
| Reproducibility | 20 | 11 / 20 | Fully specified but infeasible, with a null payload (O-4.1, O-4.2). |
| **Total** | 100 | **≈ 64** | |

**Required for acceptance:**
1. Re-parameterize the benchmark so every stance pose has knee demand ≤ 0.75 C0 at nominal, and publish the per-cell demand table.
2. Move the sustained-load payload to the carriage or torso.
3. Make the feasibility control a blocking gate.
4. Recalibrate the support test against source-vs-source splits.
5. Add a comparative retention contrast with a per-cell floor.
6. Fix or justify the A and B exploration parameterization and the Pκ smoothness.
