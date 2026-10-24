# Blind Review B on Proposal A (Packet B04)

## 1. Gate & Hard-Constraint Audit

**Recommendation: major revision; do not lock the spike or accept C-B04-A-01.**
Scope: Charter, B04 brief, Proposal A, and the explicitly permitted VERDICT.json only.
Appendix B and the referenced baseline/B01 documents were not supplied in this review scope; compliance with their unseen provisions is unverified.

- **Charter §2.1 — conditional conflict [MAJOR].** No cloning or pose-tracking reward is proposed.
  The kinematic reconstruction loss trains the model, so it is not itself a prohibited actor tracking loss.
  However, D directly maximizes imagined intrinsic rewards, beyond the Charter's literal exclusive conservative-FB actor objective.
  The brief expressly requests this hybrid: resolve that governing-text tension explicitly rather than claiming unconditional Charter compliance.
- **Charter §2.2 — partial pass [MAJOR].** The shared substrate states the fresh 50/50 relabel sampler and frozen BN.
  It does not explicitly preserve replay behavior_z, specify actual executed task-Q labels, or restate the scheduled rollout mixture.
  These are omissions, not demonstrated overwrites; make inherited invariants executable contracts.
  The spike's half B(m_demo) commands differ from the mandated current-B encoding of permuted replay next frames.
  A separate diagnostic panel may use those commands, but must not silently replace the compliant training/evaluation panel.
- **Charter §2.3 — intended pass, toy exception unresolved [MAJOR].** Production B receives only kappa(s), with the prescribed 229/277 dimensions.
  The spike instead uses 24-dimensional motion and frozen random B; label this a toy mechanism test with limited contract coverage.
- **Charter §2.4 — incomplete [MAJOR].** Real terminal segments are masked and invalid replay rows excluded.
  The spike substitutes a sigmoid hazard for the mandated credible severe_penetration threshold.
  Separate the smooth surrogate from real collection: finite, valid penetration >0.03 m must terminate, enter replay, and have zero absorption potential.
  Explicitly reject numerical corruption from normalizers too, and halt the affected run/panel; replay exclusion alone is insufficient.
- **Charter §2.5 — pass with qualification [MINOR].** A correctly disclaims learned robot performance and treats the CPU verdict as smoke evidence.
  Its later inference that observed state error establishes u approximately 1 is nevertheless unsupported.
- **Brief §2, no future inputs — intended pass.** Future motion appears as supervised targets, not model inputs.
  The deployable state/observation contract is insufficiently specified to certify zero privileged leakage.
- **Brief §2, common substrate/accounting — partial pass [MAJOR].** Identical plant and GPU-second/environment-step reporting are promised.
  Replacing the requested four arms prevents the required comparison, even if all replacement arms share that substrate.

## 2. Rubric-Keyed Technical Objections

**Mathematical Rigor of Gradient Decomposition — 30%.**

- **[CRITICAL] The advertised gradient-error bound is incomplete (§1).**
  The assumptions introduce state error epsilon_f and epsilon_J_eff, but the final E_J uses only epsilon_J.
  Equal model/plant Jacobians with a constant transition offset can still change reward gradients and terminal gradients at visited states.
  Bound reward-gradient variation, policy-derivative variation, and off-trajectory critic error; retain epsilon_f and effective Jacobian errors.
  The sensitivity-product bound also drops K_a factors unless an unstated normalization bounds action Jacobians by one.
- **[MAJOR] The terminal model-Jacobian term cannot simply be “absorbed” into E_J.**
  It depends on Q'_s, whereas the displayed E_J coefficient contains only R'; no domination assumption connects them.
  Its stated gamma^H times u^(H-1) also inserts extra discounting relative to a terminal sensitivity proportional to gamma^H L^(H-1).
  Provide the actual telescoping constants and a valid bound for both model and true closed-loop products.
- **[MAJOR] Occupancy arguments overstate what follows from DPG (§1a–b).**
  The population identity needs an exact critic and a defined, normalized discounted occupancy, including termination/absorption conventions.
  Relabeling alone does not prove replay mismatch is “never small”; different commands can induce identical occupancies.
  A finite imagined rollout adds occupancy terms, but is not an unbiased occupancy correction for arbitrary replay starts.
  Normalize the compared gradients consistently; otherwise relL2 rewards horizon-dependent scale rather than directional accuracy.
- **[MAJOR] Value weights do not bound gradient importance.**
  Neither a 27.5% terminal discount reduction nor the head's 1-gamma^H value share bounds its share of policy-gradient error.
  For gamma L<1, the displayed S_1 is bounded; “at least cubically” is not a general growth law.
  No variance term is derived despite the required bias-variance deliverable.
- **[CRITICAL] Arm B's trace-cut target drops legitimate continuation (§2.2).**
  Setting c_n=0 after an action mismatch removes the tail while retaining the prefix, treating a policy mismatch like termination.
  Bootstrap at the last valid prefix state with gamma^n_eff and a target-policy action; physical termination alone removes continuation.
  A nonzero action tolerance also gives approximate, not exact, off-policy validity.
- **[MAJOR] The survival chain rule omits future policy dependence (§2.3).**
  For i>j, the logit's state sensitivity is partial_s ell_i + partial_a ell_i partial_s pi_i.
  The written expression retains only partial_s ell_i; it is incomplete unless explicitly defined as a closed-loop total derivative.
  The factor 1-p bounds the sigmoid contribution, not logit/state Jacobians or the accumulated rollout gradient.

**Strict Zero-Future-Leakage Guarantee — 25%.**

- **[MAJOR] “State s” is not a causal deployment specification (§2.1, §5.1).**
  Enumerate observable state coordinates, action mapping, kappa, normalization inputs, and any hidden simulator/contact variables.
  Explain how imagined actor inputs are reconstructed without privileged state or future information.
  State exact model input/output widths and the toy 12-state/5-DoF coordinate layout.
- **[MINOR] Target-only supervision is a sound design choice, but needs a leakage check.**
  Perturb/shuffle future target frames with fixed current inputs and verify predictions remain unchanged before optimization.
  Freeze normalization and target networks per actor rollout; clarify the overloaded ell_t symbol for damping versus survival logit.

**Contact Stiffness & Rollout Stability — 25%.**

- **[CRITICAL] One warm-started JVP is not an upper bound on operator norm (§2.3).**
  It can miss an expanding direction, especially for non-normal matrices; multiplying these estimates cannot certify stability.
  Use a defensible conservative bound or report the heuristic's false-negative rate against explicit toy Jacobians.
- **[MAJOR] Backward-only state detachment changes the estimator being bounded.**
  The §1 derivation is for the unmodified pathwise derivative; detachment discards selected earlier action sensitivities.
  It leaves later actor parameter contributions intact, so a single H_grad does not fully describe the resulting gradient.
  Bound or measure this truncation bias and report per-time sensitivity survival plus clipped/unclipped controls.
- **[MAJOR] Smooth contacts and hazards evade the discontinuity central to the brief.**
  The log-survival assumptions fail at deterministic p=0; threshold events require boundary terms or a separately justified surrogate.
  Test smoothing-temperature dependence and real threshold termination; do not equate surrogate autograd with the hard-contact policy gradient.

**4-Arm Ablation Completeness — 20%.**

- **[CRITICAL] A explicitly supersedes the required baseline arms (§2.4).**
  It removes single-task WM and adds real/model FB-target variants; D-V cannot replace the missing single-task versus multi-task comparison.
  Restore the brief's baseline-indexed four-arm matrix and required C/D horizons; treat the new target variants as additional controls.
- **[MAJOR] Training an unused world model in every arm hides representation overhead.**
  Retain that control for model-use attribution, but also report the native FB baseline without dummy model training.
  C versus D changes both critic-target construction and actor differentiation; add detached versus differentiated versions of the same rollout/objective.
  Fixed-policy gradient measurements alone cannot establish training acceleration, sample efficiency, or throughput attribution.

## 3. Audit of Rejected Alternative & Necessity Claim

- **[MAJOR] Alternative L is substantive, but its impossibility argument is narrower than claimed (§3).**
  Non-injectivity of B does not imply positive conditional variance of successor B; aliased states must have different successor embeddings on positive-probability support.
  The ascending/descending example assumes velocities are absent, which the supplied motion-only contract does not establish.
  The state-decoding/actor-input objection is credible for T_lat(B,a), but does not eliminate causal recurrent or task-conditioned latent models.
  Gauge drift is a real concern; the stated expression is not a general lower bound without specifying coordinate transport and latent-model equivariance.
- **[MINOR] Alternative U gives a valid delayed-reward counterexample, not a universal necessity proof.**
  It establishes failure for a task family, not every finite-horizon problem; the asserted universal value-bias lower bound is unjustified.
- **[CRITICAL] C-B04-A-01 confuses a growing error envelope with growing realized error (§4).**
  At L=1, the derivative condition for gamma^H(a+bH) is correct for fixed nonnegative a,b; its 0.015 threshold is approximately consistent.
  But P2 supplies no positive lower bound, and P3's “coherence” supplies neither alignment magnitudes nor horizon-invariant errors.
  Thus the necessity conclusion about all H3 gains does not follow, even conditionally from the listed premises.
  Oracle substitution changes interactions among model, critic, and truncation errors; a difference of relL2 norms is not an additive critic error component.
- **[MAJOR] Appendix B compliance remains unverified; falsifiability is only partial.**
  The claim has identifiable premises and a numerical rejection rule, but no supplied Appendix B permits checking its prescribed grades or format.
  Define a measurable coherence premise, horizon-specific critic-gradient errors, and a paired critic-only gradient contrast.
  Delta_F can be negative or near zero, making its multiplicative 0.8 test misleading; specify an absolute effect and uncertainty procedure.

## 4. Spike Protocol Critique

- **[MAJOR] Oracle horizon:** gamma^460<0.01 bounds a discount factor, not the gradient tail when sensitivities grow.
  Demonstrate convergence at longer horizons; finite differences validate the same truncated objective, not its infinite-horizon accuracy.
- **[MAJOR] Calibration:** held-out value R^2>=0.8 does not certify action/state derivatives or remove shared target bias.
  Report derivative errors separately, gate-failure counts, the oracle-tail construction, and fixed train/validation splits across all arms.
- **[MAJOR] Confounds:** frozen B removes representation drift; transition-count sweeps do not isolate Jacobian error from coverage and fit quality.
  Add a controlled drifting-B panel, paired replay/data budgets, model-error interventions, and joint oracle substitutions to measure interactions.
- **[MAJOR] Thresholds:** specify seed-level paired inference and selection correction over horizons, stiffnesses, condition numbers, and model budgets.
  “Within CI” is not an equivalence test; H3 support/refutation rules need disjoint outcomes and an explicit inconclusive category.
  Condition number one means Sigma=cI, not necessarily I; equal whitening cosine with a fixed tail requires scale/splice normalization too.
- **[MAJOR] Reproducibility:** specify dynamics/integrator, friction sign, checkpoints, fitting budgets, D-V training, and hardware/timing boundaries.
  Include model fitting, normalizer/Gram updates, synchronization, and routing overhead in GPU seconds; report the required arms in the spike itself.
- **[MINOR] Existing verdict:** its metrics support no causal inference about L, critic training quality, or the optimum horizon.
  It lacks controls and uncertainty; the scalar PASS cannot repair the omitted arm matrix or validate the necessity claim.
