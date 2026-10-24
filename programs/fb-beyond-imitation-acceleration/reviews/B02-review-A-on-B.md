# Blind Review A on Proposal B (Packet B02)

**Reviewer:** Blind Reviewer A. **Date:** 2026-10-23. **Inputs read:** `PROGRAM_CHARTER.md`; `packets/B02/proposals/B.md`; pinned method v1.0 (Appendix B, §4 Step 4); `baseline/02`, `baseline/04`, `baseline/05` (spot-checks of contract claims only). No file under `reviews/` or `drafts/` was opened.

**Provenance disclosure (for Confounds).** `packets/B02/brief.md` does not exist in this checkout. Like Proposal B, this review uses `briefs/B02-nonstationarity-and-off-policy-credit-assignment-in-joint-fb-task-training.md` as the brief. Its rubric rows are: Exactness of Off-Policy Semantics (30%), Compliance with R2.1 & v2 Contracts (25%), Computational Overhead (20%), Spike Falsifiability (25%). The orchestrator should record the missing path as a Class-0 path fix and confirm that both authors and both reviewers were bound to the same brief text. Proposal B itself reports unrestricted filesystem permissions, which is an isolation risk under §11.

**Derivations independently re-checked and found correct:** (3)–(5) including the variance identity; the $2M\cdot\mathrm{TV}$ bound and the KL chain rule in (6); the $M\sqrt K D$ reduction in (7); (8)–(9); the EMA algebra (10)–(12) and the cycle fixed points; (15) and its reduction to (16); the Gaussian second-moment bound $\mathbb E_gW^2\le e^{KD^2}$; the Test A constants ($\mu_*=0.2$, $\mu_{\rm dup}=0.38$); $C_k$ and the product-TV bound in Test D; and the Test E scalar witness ($0.9^6$ vs $0.8^6$ vs $0$). The ball-schema discrepancy B flags is real: the listed $o^{\rm low}$ components sum to 107, not 93. The mathematics is strong. The defects below are about whether the mathematics is linked to the gate, the alternative, and the spike.

---

## 1. Gate & Hard-Constraint Audit

| Constraint (source) | Verdict | Note |
|---|---|---|
| No BC / tracking fallback (Charter §2.1) | **Pass** | The actor objective is the scalar conservative FB value only. Alerts are explicitly barred from adding BC or tracking terms. $W$ in (18) is detached and never reaches the actor. |
| `behavior_z` / `z_update` separation; Q trains on `z_actual` / `a_applied` (Charter §2.2; brief §2) | **Pass** | §2.1 steps 2–4 match `baseline/05` §4: fresh storage, online $B$, permuted `m_next`, 50/50 mask, and clone-at-storage-boundary checks. |
| BN updated once on current and once on next, then frozen (brief §2) | **Pass** | Matches. B also correctly notes that `no_grad` ≠ `eval`, and that the actor-gradient path must not be wrapped in `no_grad`. |
| Single-frame motion-only $B$ input (Charter §2.3) | **Pass** | Ball contact and displacement are used only as diagnostic outputs. |
| `severe_penetration` vs `invalid` (Charter §2.4) | **Pass** | B adds a reasonable refinement: when `invalid` interrupts a partial macro, the macro target is withheld. |
| Evidence vs claims (Charter §2.5) | **Pass** | No competence or superiority claims are made. |
| No pretraining stage; no freezing of $B/\pi$ (brief §2) | **Conditional pass. See [MAJOR] G-1.** | The text complies. The gate dynamics can still produce an emergent task-learning blackout. |
| Full-prefix zero-hidden burn-in (brief §2) | **Pass** | §2.4 gives per-role reconstruction, separate target prefixes, and gradient checks detached at the slice boundary. |

**[MAJOR] G-1: the drift gate can make the no-pretraining-stage rule hold only on paper.** §2.3 makes a generation eligible only if p95 action RMS ≤ 0.05, p95 $\Delta_B$ ≤ 0.02, and age ≤ 1000. It keeps only the *contiguous suffix* of passing generations. If none pass, the task update is skipped while FB keeps learning. Early in joint training from scratch, one optimizer step on a 2048×6 residual actor can easily move post-tanh means by more than 0.05 RMS. If that persists, the planner and critic never update. The result is an FB-only phase that the proposal never declared, which amounts in effect to an FB pretraining stage followed by task learning. That is exactly the staging the brief forbids. No maximum skip fraction, fallback (e.g. reverting to the FIFO/age arm), or pre-registered failure verdict is specified. **Required:** pre-register a skip-rate ceiling (e.g. ≤ X% of task updates in any 10k-update window). Make breaching it a gate FAIL that falls back to the admissible null, not something to tune afterwards.

**[MINOR] G-2: unspecified baseline additions.** B adds versioned target normalizer buffers with a "hard copy at target-update event" (§2.1 step 4) and new replay fields (pre-actuator actions and behavior log-densities). Neither is in `baseline/04` or `baseline/05`. They are additive and do not violate the contract, but they must be logged as contract extensions. The hard copy also creates a mismatch: EMA-averaged target weights are calibrated to a mixture of past buffer states, while the copied buffer is the latest one. B should either justify this or EMA the buffers too.

**Gate verdict:** no hard-constraint violation found. G-1 must be resolved before the spike is locked.

---

## 2. Rubric-Keyed Technical Objections

### 2.1 Exactness of Off-Policy Semantics (30%)

B separates the macro-kernel shift (2)–(7), transition-level action-Q (§2.4), and encoder drift vs fixed-command drift (§1.3) more cleanly than the brief requires. The objections are:

- **[MAJOR] S-1: the gate metric and the bound metric are in different units, so the empirical gate is not linked to the bias bound.** Bound (7) is stated in pre-squash Mahalanobis distance $\|\mu_n-\mu_g\|_{\Sigma_a^{-1}}$. The KL is invariant under tanh, so pre-squash geometry is what matters. The gate thresholds post-tanh Euclidean action RMS at 0.05. Two consequences follow:
  - With exploration std σ = 0.1, RMS 0.05 corresponds to a per-step Mahalanobis distance of about $0.05\sqrt{29}/0.1\approx2.7$. That gives $\sqrt K D\approx8.5$, so the gate admits generations whose bias bound is vacuous ($\min(2,\cdot)=2$).
  - Near saturation, post-tanh RMS can be ≈0 while pre-squash KL is large. B's own saturated-actor fixture demonstrates this mechanism and the gate ignores it.

  **Required:** log the pre-squash Mahalanobis drift and the per-step Gaussian KL as gate quantities, at least as a parallel arm. Also state what 0.05 RMS means in bias units at the deployed σ.
- **[MAJOR] S-2: the variance of correction mode is acknowledged but not governed.** For $K=10$, $d_a=29$ and realistic $D$, the bound $e^{KD^2}$ is astronomically large and ESS will collapse. B forbids normalization, clipping, and retroactive removal (all correct for unbiasedness) but provides no pre-registered ESS floor or arm-level abort rule. "Unbiased with unbounded variance" is not a usable credit-assignment design. **Required:** a registered ESS/N floor below which correction mode is declared FAIL for that window, instead of being silently dominated.
- **[MINOR] S-3: planner-side extrapolation is not analyzed.**
  - **Ball:** the planner differentiates $Q_{\phi_1}(H^Q,\pi_\theta(o,P_\psi(H)))$ through the *current* $\pi_\theta$. The actions it queries may lie outside the replay action support that Q was trained on.
  - **Obstacle:** $P_\psi$ queries $Q$ at $z$ values that may lie off the three-way-mixture support.

  This is a second staleness channel, separate from target drift, and §2.4 should at least name it.
- **[MINOR] S-4: stationarity premise.** The analysis assumes stationary dynamics "with episode geometry held fixed". The curriculum quota changes the geometry *distribution*. That is harmless only because $c^{\rm geom}$ enters $Q$. Say so explicitly, and note that the low-level actor sees the scan but the drift panel is stratified by height only.

### 2.2 Compliance with R2.1 & v2 Contracts (25%)

These items are strong: update order, storage-boundary cloning, the ball $\bar\theta$ target with clipped smoothing, and the explicit refusal to resolve the 93/107 and 256/100 schema conflicts silently. Remaining items:

- **[MINOR] C-1: planner delay counter.** "Planner delay = 2 task updates" is undefined when the gate skips task updates. Does a skipped update count? Specify this.
- **[MINOR] C-2: replay window.** The baseline mitigation (`baseline/02`) is a 50k-macro window. B keeps 50k physical rows but adds an age ≤ 1000 gate. For collection rates above ~50 macros per update, that cap governs and the effective window is much shorter than the baseline's. This is a sampling rule, not a violation, but it changes the baseline coverage assumption. Report effective window size.

### 2.3 Computational Overhead (20%)

- **[MAJOR] O-1: no a-priori cost estimate, and the measured gate cannot test production cost.** The resource gate (§5.7) times toy modules (a `288→64→29` actor) on CPU. Production uses residual `2048×6` actor/F networks on GPU. Correction mode needs up to $K=10$ extra actor forwards per sampled macro. Relative to a critic update with LSTM prefixes, that ratio depends strongly on width and batch, so toy ratios do not transfer. B admits this, but the 20% rubric row then has no evidence at all. **Required:** an analytic FLOP or forward-count ratio at production widths and batch size, *or* a GPU micro-benchmark using production-width modules on random tensors, registered in the spike. The diagnostics are amortized (Jacobians every 100 updates, trajectories every 5k), and B should also estimate their simulator cost per 5k updates.

### 2.4 Spike Falsifiability (25%)

See §4. In short: unit-level algebra checks are excellent and nearly complete. Integration-level "value stability under generation lag" (brief deliverable 3, rubric "integration checks") is missing.

---

## 3. Audit of Rejected Alternative & Necessity Claim

### 3.1 Rejected alternative (§3.1, retroactive re-encoding)

- **Non-triviality:** partially satisfied. Rejecting outcome-based relabeling of $z$ (re-encoding realized successor frames into $\tilde z$) is a real alternative. The selection-bias argument (that $\tilde z$ is a descendant of action and environment noise) is correct and is the strongest part of the section.
- **[MAJOR] A-1: the counterexample breaks a premise of the alternative it targets.** The one-step example takes old $a=z$, new $a=-z$, and $B_n(x')=x'$. Under joint FB training, a converged $(\pi_n,B_n)$ pair would satisfy $B_n(x')=-x'$ for that actor, and then re-encoding is *exact* in that example. So the counterexample defeats re-encoding only when encoder and actor are mutually inconsistent. That is plausible early in training, but it is a premise, not a universal fact. The universal rejection should rest on (i) the selection-bias argument and (ii) the charter's immutability rule, and the counterexample should be scoped to FB-inconsistent regimes.
- **[MAJOR] A-2: the brief's option (c) is not the alternative B rejected.** Brief deliverable 2(c) asks for a comparison of "re-encoding raw expert frames vs keeping executed planner $z_{\rm actual}$". The natural reading is re-encoding the *prompt* frame that generated an expert or near macro, i.e. $\tilde z=B_n(m_{\rm prompt})$ with the same near rotation, not re-encoding the outcome. Its failure mode is different. It is a "semantic prompt" target whose validity depends on $\pi_n\circ B_n$ preserving prompt semantics, and Test C's coordinated-rotation fixture is the right tool to probe exactly that. B dismisses this in one sentence and the spike has no arm for it. Deliverable coverage is incomplete.
- §3.2 (freezing) is settled by constraint, so it is a trivial rejection. §3.3 (age-only replay) is the genuinely non-trivial admissible alternative, and B handles it well: it is retained as a compute-matched control and is the winner if B's gates fail.

### 3.2 `C-B02-B-01` against Appendix B

| B.3 requirement | Assessment |
|---|---|
| Explicit premises | Met. |
| Conclusion shape | Nominally an invariant/obligation. |
| Implementation independence | Met (measure-theoretic). |
| Falsification mode | **Fails in substance. See [CRITICAL] N-1.** |
| Not score-derived | Met. |

- **[CRITICAL] N-1: the claim is a tautology, so its falsifier is vacuous.** "$\mathbb E_g f=\mathbb E_n f$ for all bounded measurable $f$ iff $\mathbb P_g=\mathbb P_n$" is the definition of equality of measures. The stated falsifier ("exhibit unequal measures with equal integrals for all bounded $f$") is mathematically impossible, so B.3.4 is met only formally. More importantly, the claim has no route-pruning force under B.1/B.2. The program uses *one* task reward and *one* $V_n$, and unbiasedness for that functional ($\mathbb E_gY_n=\mathbb E_nY_n$) does not require path-law equality. So the claim cannot veto age-only replay, gating, or anything else in this packet. A Grade-1 lock on it would be harmless but empty.
- **[MAJOR] N-2: the "consequently" clause goes beyond the proof.** "Relabeling a numeric command alone supplies neither" does not follow from the iff. B itself concedes in §3.1 that a proved conjugacy $\pi_n(o,Tz)=\pi_g(o,z)$ makes relabeling yield $\mathbb P_n^{Tz}=\mathbb P_g^{z}$, which satisfies the claim's conclusion. Either delete the clause or add premise "no conjugacy holds", and log that as scope-narrowing event #1 (B.9.6).
- **Suggested repair (would give the claim real force):** restate it as a *tight minimax lower bound*. For any unweighted historical estimator and the return class $\{f:\|f\|_\infty\le M\}$,
  $$\sup_f|\mathbb E_gf-\mathbb E_nf| = 2M\,\mathrm{TV}(\mathbb P_g^z,\mathbb P_n^z).$$
  Therefore no unweighted method can certify worst-case bias below $\epsilon M$ without certifying $\mathrm{TV}\le\epsilon/2$. This version is falsifiable (exhibit an unweighted method with a smaller certified worst-case bias over the class), and it directly constrains which gate statistics can be called certificates. That is the role B actually wants the claim to play in §2.3.
- **Operational test.** Enumerating the Bernoulli fixture verifies the identity, not whether the premises hold in the target setting (stationary kernel given $c^{\rm geom}$, common support). Add a premise-check item, e.g. a support/absolute-continuity audit on logged densities.
- **Grade 1 / Candidate / count 0:** labeling is honest, and B correctly states that a spike PASS is not a lock.

---

## 4. Spike Protocol Critique

- **[MAJOR] P-1: Test D contradicts the gate rule in §2.3.** §2.3 keeps only the *contiguous suffix* of passing generations. Test D sets a 1-update-old generation with $p_g=0.10$, which fails $|p_g-p_n|\le0.05$, and a 100-update-old generation with $p_g=0.50$, which passes. That fixture is meant to show that drift, not age, should select data. But under the contiguous-suffix rule the suffix is empty, so the gate excludes the good old generation and skips the task update. The expected outcome is unregistered, and the fixture does not exercise the property it claims to show. **Required:** either drop the contiguity requirement (and justify per-generation eligibility) or pre-register the empty-suffix/skip outcome as the expected result.
- **[MAJOR] P-2: no integration test of bounded TD error or value stability under lag (brief deliverable 3).** Test D fits a *constant* critic by normal equations against a fixed readout $V(x_k)=x_k$. There is no bootstrapping recursion, no target network, and no learning over updates. **Missing:** a small tabular or linear macro-MDP in which the actor drifts on a known schedule, a twin critic is trained by TD with target updates across FIFO, age, gate, and correction arms, and $\|Q-Q^{\pi_n}\|$ (exactly computable) is tracked against generation lag, with registered pass bands. This is the only test that would let the "value stability" claim fail.
- **[MAJOR] P-3: alert thresholds are not calibrated.** Test C only checks detection of injected changes at 1e-8 and no-change drift at 1e-10. The operational thresholds (0.05 RMS, 0.02 $\Delta_B$, "2× prior median + 1e-6") are never tested for false-alarm rate under compliant training noise or for detection power at bias-relevant drift. The pass rule's specificity clause covers BN alarms only. Add a run in which a known-small drift ($\sqrt K D\le0.05$) must not trigger and a known-large drift ($\sqrt K D\ge1$) must trigger.
- **[MINOR] P-4: normalizer coverage.** Test A covers only the motion BN. Add (i) a check that collector, evaluation, and planner forwards of the actor, F and planner do not mutate the *observation* normalizer, and (ii) a check that relabels use the *online* $B$, not the target $B$, by perturbing the target $B$ and requiring identical `z_update`.
- **[MINOR] P-5: negative controls missing for two prohibitions B itself states.** (a) Outcome-based path filtering (by reward, termination or TD error) should be shown to bias the enumerated target. Without that, the §2.3 prohibition is asserted, not tested. (b) Evaluating Gaussian densities at hard-clipped actions should be shown to give wrong $W$. B argues both in the text but tests only $p_g=0$ as `UNSUPPORTED`.
- **[MINOR] P-6: unregistered thresholds.** Test A.5 ("report target variance error") and the Test D failure-coverage fixture have no numeric pass criteria. Either register a criterion or label them report-only so they cannot be read post hoc as PASS.
- **[MINOR] P-7: fixture fidelity.** Affine-free BN and the `229→256→256` encoder differ from the production module definitions. That is acceptable for contract tests, but each production-fidelity gap should be listed so a PASS is not over-read.
- **Strengths to keep:** FP64 with deterministic algorithms; a cap of two invocations with harness-only fixes; timeout reported as `INCOMPLETE`; no seed selection; boundary-detached gradient references in Test E; the coordinated-rotation fixture separating coordinate consistency from replay consistency; the explicit wrong-$K$ discrepancy check.

---

**Summary.** B's off-policy mathematics is exact and the R2.1/v2 contract work is exemplary. No hard-constraint violation was found. To be lock-ready, B needs to resolve the following:

1. G-1: bound the gate's skip rate and specify a fallback.
2. S-1: align gate units with the bound.
3. A-2: address brief option (c) as written.
4. N-1: recast `C-B02-B-01` as a minimax TV lower bound so it has non-vacuous force.
5. P-1: fix the Test D contiguity contradiction.
6. P-2: add a TD-learning integration test of value stability under lag.
7. O-1: supply production-scale overhead evidence.
