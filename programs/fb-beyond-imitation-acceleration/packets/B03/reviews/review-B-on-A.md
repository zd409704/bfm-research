# Blind Review B on Proposal A (Packet B03)

## 1. Gate & Hard-Constraint Audit

- **Recommendation:** revise before spike lock. The input contract is largely preserved, but the principal necessity theorem and failure-attribution protocol are not established.
- **Scope:** reviewed only the Charter, B03 brief, Proposal A, and the permitted `B03-SPIKE/VERDICT.json`. Baseline documents, `D-B01-001`, and Appendix B were not supplied within this review's permitted evidence.
- **Charter §2.1 — actor objectives:** no explicit violation. Supervised action probes are expressly detached; the task-gradient exception is restricted to single-step action-Q variants. Keep probe optimization demonstrably separate from actor training.
- **Charter §2.2 — behavior/update latents:** actual executed macro latents and immutable behavior fields are preserved. However, the fresh 50/50 update mixture and exact two-pass BN procedure are not fully specified for the synthetic FB updates; compliance remains unverified.
- **Charter §2.3 — motion-only B:** the proposed architecture complies. Contact-augmented B is discussed only as a rejected alternative, not as an implemented exception.
- **Charter §2.4 — failure classification:** severe penetration and invalid replay exclusions are mentioned, but the protocol omits the full finite-state/schema/divergence predicates, rejection from normalizers, and mandatory run/panel halt for invalid physics.
- **Charter §2.5 — evidence discipline:** no explicit learned-task or baseline-superiority claim. The existing CPU PASS supports neither the new force theorem nor task performance; the proposal appropriately limits its empirical interpretation.
- **Brief §2 — NPZ compatibility:** retained; no required force, scan, or ball trajectory input to demonstration encoding.
- **Brief §2 — prohibited admission machinery:** no reintroduction of the R1.3 static height filter or `infer_source_support_intent` is proposed.
- **Gate status:** no demonstrated hard-constraint violation in the intended architecture, but procedural compliance is incomplete. Full frozen-baseline alignment cannot be certified from the authorized files.

## 2. Rubric-Keyed Technical Objections

### Compatibility with Kinematic-Only Demo NPZ — 30%

- **[MINOR] Proposition 1.1 establishes invariance, not an exact learned fibre.** A deterministic B preserves descriptor collisions but can introduce additional collisions. The physically feasible state fibre also excludes arbitrary incompatible scene/contact assignments.
- **[MAJOR] Descriptor fidelity is assumed rather than demonstrated.** Spike (a) must construct both descriptors from transformed qpos/qvel through the actual feature definitions. Copying identical m rows only tests determinism and cannot validate the claimed vertical invariance or base-height exception.
- **[MINOR] Bitwise equality is stronger than geometric invariance.** Floating-point FK and coordinate subtraction can differ after translation. Separate exact equality on copied descriptors from a justified numerical tolerance on independently reconstructed descriptors.
- **[MAJOR] The rejected alternative's NPZ argument overclaims.** Imputation adds no information beyond m, but it need not make an encoder unusable on NPZs. The unconditional prohibition comes from Charter §2.3, not from missing fields alone.

### Rigor of Aliasing Analysis — 25%

- **[CRITICAL] Proposition 1.4 confuses representability, training identifiability, and learnability.** Measurability in (o_low,z) characterizes unrestricted deterministic functions; it does not establish representation by the specified finite actor or successful FB optimization.
- Feeding e to both pi and F is neither universally necessary nor sufficient. e may be redundant with other inputs or irrelevant to the optimal action, while distinct geometries can still demand task distinctions absent from the FB objective.
- **[MAJOR] The omitted-context gradient is not generally the stated regime mixture.** An action-conditioned critic averages over p(c | xi_p,a,z), not necessarily p(c | xi_p); differentiating this conditional expectation can introduce action-dependent weighting terms.
- **[CRITICAL] Distinct successor features do not imply addressability of every intent.** Two distinct feature occupancies can be pairwise separated, but an occupancy inside the convex hull of other feasible occupancies cannot be uniquely selected by any linear reward.
- Case K needs an exposed-optimum condition over attainable occupancies, consistent continuation policies, and an explicit spherical z construction. The claimed margin does not follow from Delta_K > 0; the common centering term h cancels in pairwise comparisons.
- **[CRITICAL] Proposition 1.5 gives an instantaneous algebraic nullspace, not an exact boundary for future isokinematics.** Rank does not establish a dynamically realizable force schedule under unilateral contact, complementarity, compliance, actuator limits, or changing contact geometry.
- Nonempty relative interior of a friction-feasible set does not imply that every algebraic null direction remains feasible, nor that any feasible instantaneous pair preserves the same trajectory for all future time.
- **[MAJOR] Wrench redundancy need not imply distinct actions.** A null vector may satisfy Delta tau = 0 with nonzero self-equilibrating Delta lambda. The relevant quantity is the dimension of the torque projection of the feasible nullspace, not dim N alone.
- Joint-PD inversion additionally requires nonsingular gains and an unsaturated, unclipped actuator map. The rank arithmetic is conditionally valid; these missing physical assumptions invalidate its claimed universal interpretation.
- **[CRITICAL] The Bayes floor omits z.** The applicable bound is E tr Cov(a* | o_low,z), not a two-label variance conditioned only on common kinematics. Different planner latents can encode different intents even with identical observations.
- **[CRITICAL] Objective indifference does not imply zero parameter-gradient component.** Shared actor parameters couple action directions. A gradient orthogonal to n_a in action space can induce an update with nonzero n_a component through J_theta pi (J_theta pi)^T.
- Accordingly, pure FB training supplies no direct preference between exactly equal-return branches; it does not prove that the actor's reachable set excludes either branch or that planner selection cannot exploit existing variation.
- **[MAJOR] The critic comparison overstates blindness and stationarity.** Macro Q can value task differences among reachable z-dependent force choices. Action Q's immediate transition law is policy-independent, but its continuation value still changes with the policy; a 50k replay window alone supplies no staleness bound.
- **[MAJOR] AAMC does not identify macro dynamics.** Identical first actions can precede different later actions under changing theta. At K=1 the extra z input is redundant only under appropriate Markov-state and continuation assumptions, not by architecture alone.
- Planner differentiation of Q(h,z,pi(o,z)) also requires a defensible extension off the logged joint (z,alpha) support; adding an action anchor does not establish this identification.
- **[MAJOR] The striking asymptotic lacks a control and regularity model.** Fixed-gain position targets do not automatically vary impedance; the impact formula requires collision assumptions, and the FB bound requires Lipschitz B plus a discounted future-trajectory bound.
- The asserted O(1) task gap and divergent ratio do not follow merely by sending m_b/m_eff to zero; specify which quantities vary and how task reward scales.

### Diagnostic Precision — 25%

- **[CRITICAL] D_P uses the suspect Q as its own oracle.** CEM can exploit critic error, while a uniformly wrong Q yields a small gap. Validate candidate latents through paired simulator returns and report search coverage before assigning planner failure.
- **[MAJOR] D_F measures sensitivity, not useful perception.** Scan shuffling can create impossible observations; spurious dependence can pass, and appropriate local invariance can fail. Use feasible paired scene interventions and compare value/gradient accuracy against known outcomes.
- **[CRITICAL] D_B assumes the answer it should diagnose.** A successful privileged wrench is neither operationally specified nor necessarily realizable by the actor/actuator. Nullspace alignment and regression error cannot isolate B from hidden intent, inadequate observations, or optimization failure.
- The nullspace projection also needs a specified metric and force/torque scaling; a “50%” Euclidean norm threshold is otherwise representation-dependent.
- **[MAJOR] Sequential attribution is not exclusion evidence.** Negative D_F and D_P do not rule out critic error, planner search failure, or insufficient exploration. Include an unresolved/mixed category and intervention-based rescue tests.
- **[MAJOR] tau_dec is not directly observable in replay.** Contact reward derivatives may be undefined, unavailable, or noisy. Specify a causal intervention estimator, its temporal resolution, and uncertainty before using it to switch architectures.
- **[MAJOR] Diagnostics are incompletely transferred to striking.** Define ball-state interventions and action-Q versions explicitly; the stated scan test and Q(h,c,z) planner test do not cover the proposed action-Q implementation.

### Spike Falsifiability — 20%

- **[CRITICAL] The main positive result tests a detached supervised probe.** Accurate regime-conditioned action regression proves information availability for that probe, not that an actor trained exclusively with conservative FB value learns contact compensation.
- **[MAJOR] The linear-FB control is underspecified.** Transition kernels, rewards/features, discount, action domain, training budget, occupancy calculation, and oracle gradients are missing. Five seeds cannot make an undefined experiment reproducible.
- **[MAJOR] The proposed sufficiency test lacks its oracle arm.** C-B03-A-02 lists three ablations but requires comparison with an additional contact-oracle arm. Prespecify matched budgets, episode counts, and a confidence interval for the paired success difference.
- Non-overlapping marginal 95% intervals are not a calibrated test of a 10-percentage-point difference. Wilson intervals require a declared trial unit; pooling episodes must not erase seed-level variation.
- **[MAJOR] The overall PASS excludes diagnostic validation.** A verdict from (a)-(c) cannot establish Brief deliverable 2 or the planner-rescue claims. Report separate identity, information, learning, and attribution outcomes.

## 3. Audit of Rejected Alternative & Necessity Claim

- **Alternative quality:** contact-augmented B is technically substantive because it can change replay successor features, particularly for controllable ball outcomes. It is nevertheless outside the hard constraints, so rejecting it does not establish superiority over feasible alternatives.
- A stronger comparison would retain motion-only B and compare macro Q, single-step action Q with beta=0, and the permitted beta>0 variant under matched observations and compute.
- **[MAJOR] Proposition 3.2 requires qualification.** Constant exogenous features have action-independent infinite-horizon return only under the specified continuing/absorbing convention. Action-dependent termination can change their discounted occupancy.
- Whitening and feature mixing also prevent identifying F^T u with f(h)/(1-gamma) without additional assumptions. Orthogonalization does not enforce an exact trace constraint throughout training.
- **Appendix B audit limitation:** its text is absent from the authorized context. Exact procedural compliance cannot be certified; the listed premises, conclusion, and falsifiers can still be assessed directly.
- **C-B03-A-01: not established as Grade 1.** P3 supplies only instantaneous redundancy; P4 does not require intent independence from z or planner history. Neither ensures feasible distinct torques with identical future discounted B occupancy.
- The conclusion conflates missing information with missing learning signal. Adding task gradients cannot recover an intent absent from all deployment inputs; exposing intent does not itself make an FB-indifferent actor learn the desired force ordering.
- Conversely, an FB-optimal actor can retain z-dependent choices between tied branches. A task-trained planner can select those choices without a task gradient reaching theta, contradicting the asserted universal planner insufficiency.
- **Required repair:** condition on all actor inputs, prove feasible equal-occupancy branches, and distinguish Bayes risk from optimization identifiability. A defensible theorem says equal occupancies give equal ideal linear FB returns, without imposing a unique actor or reachable set.
- **Falsifier 1 is not diagnostic:** beating the stated floor may reveal label leakage through z, an incorrect conditional floor, or finite-sample effects; the protocol must audit these before interpreting a counterexample.
- **Falsifier 2 tests critic fidelity:** unequal learned F estimates on equal-occupancy branches can be approximation or training error. They do not refute equality of the exact represented return. Use an analytic occupancy oracle and absolute-plus-relative tolerances.

## 4. Spike Protocol Critique

- **Physical controls:** random postures and twists need not admit the declared support/impact states. Construct feasible contacts, verify friction and actuator constraints, and distinguish impulsive impact from sustained-force dynamics.
- **Force controls:** integrate paired branches over a declared horizon and verify equal robot trajectories/occupancies, different realized torques/wrenches, and different task outcomes. An instantaneous SVD is insufficient.
- **Label control:** define whether a_+ - a_- equals K_p^{-1} Delta tau or twice that quantity. The stated per-dimension floor changes by a factor of four between these conventions.
- **Information controls:** balance labels conditional on the complete observation and z; use held-out posture groups, identical paired inputs, and a privileged-label probe. Specify train/test splits and uncertainty for all probe errors.
- **Gradient controls:** the majority-class probability is not a cosine bound. Minority and majority oracle gradients can align perfectly. Specify gradient geometry and handle zero-norm gradients explicitly.
- **Numerical controls:** stabilize every value-gap and diagnostic denominator near zero. Calibrate SVD tolerances against matrix scaling and report the torque-projected feasible rank separately from total nullity.
- **Statistical controls:** justify the 1%, 2%, 10%, and 50% cutoffs, report per-seed uncertainty, and calibrate synthetic training adequacy. An all-five-seeds rule alone gives neither an effect-size test nor a confidence guarantee.
- **Ball control:** replace monotonicity of a potentially singular ratio with separate task-gap and FB-gap measurements, fixed collision assumptions, and uncertainty across the mass sweep.
- **Architecture controls:** compare full conditioning, F-only withholding, pi-only withholding, and both withholding; test planner latent rescue and beta rescue separately. Match optimization and search budgets.
- **Edge cases:** specify timeout bootstrapping separately from true termination, full invalid-physics handling, actual applied-action clipping, frozen-normalizer procedures, and recurrent-prefix reconstruction where used.
- **Evidence disposition:** the existing verdict contains three scalar diagnostics and no analytic floor, uncertainty, or physical validation. Retain it as a limited smoke result; do not use its PASS to adjudicate C-B03-A-01 or perceptive sufficiency.
