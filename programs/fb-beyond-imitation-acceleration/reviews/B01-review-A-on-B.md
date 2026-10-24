# Blind Review A on Proposal B (Packet B01)

Reviewer: Blind Reviewer A. Inputs read: `PROGRAM_CHARTER.md`, `packets/B01/brief.md`, `packets/B01/proposals/B.md`. I read nothing in `reviews/`, `drafts/`, `baseline/`, or the pinned method document. So any statement about baseline/Appendix B compliance below is limited to what the charter and brief quote or what Proposal B itself says.

**Independent verification performed.** I re-derived every one of Proposal B's equations, from (1)–(10) through (12)–(13). I also checked these numerically (FP64, NumPy):

- the §1.5 gradient counterexample: $g=-1$, $\tilde g=0.5$;
- the §3.1 sphere counterexample: $S=\mathrm{diag}(4/3,2/3)$, whitened squared norms $3/2,3/2,3$;
- the fixture-A spectra: at $\kappa_0=30$, $\lambda_{\min}\approx0.117$ and $\lambda_{\max}\approx3.5$, and the RAW normalized reward MSE (NMSE) for uniform commands $=1-d/\sum_i\lambda_i^{-1}\approx0.59$; at $\kappa_0=1000$, $\lambda_{\min}\approx0.0068$;
- a quick re-implementation of fixture C's RAW reachability. Under my own choice of candidate actions, RAW agreed with the exact maximizer 86% of the time at $d=100$ and 75% at $d=256$, so the fixture can tell the arms apart.

I found no algebraic error. The objections below are about scope, how thresholds are calibrated, missing controls, and edge cases. None of them is an arithmetic mistake.

---

## 1. Gate & Hard-Constraint Audit

| Constraint (source) | Verdict | Evidence / note |
|---|---|---|
| Charter §2.1: no behavioral cloning (BC), action-MSE, or pose-tracking reward | **PASS** | §2.2 step 6 updates the actor only on $-\min_k F_k^\top z$. Expert frames only select commands (§2.3). |
| Charter §2.2: `behavior_z` / `z_update` separation; task critic uses $z_{\rm actual}$ | **PASS** | §2.2 steps 2–3: BN updated once on current and once on next frames, then frozen; online $B$ encodes permuted `m_next`; Bernoulli-0.5 uniform mix; detached. "`behavior_z` is never rewritten"; no whitened labels in task replay. |
| Charter §2.3: $B$ sees single-frame motion only | **PASS** | Hybrid reward uses $\bar B(\hat m)$ of predicted root-relative motion only (§2.2 step 7). The spike encoder takes only the descriptor, never the index (§5.2A). |
| Charter §2.4: `severe_penetration` vs `invalid` | **PASS with a minor deviation** | `severe_penetration` rows are retained (step 1). On nonfinite input, however, the proposal "aborts that update and triggers inspection". The charter requires that the affected run or panel **halt**. Aborting one update and continuing is weaker. [MINOR] |
| Charter §2.5: verified vs unproven claims | **PASS** | No results are claimed. Spike scope is explicitly algebra and estimator behavior (§5.1, §5.5). |
| Brief §2: keep the bilinear $F^\top B$ interface and the $\sqrt{d_z}$ sphere | **PASS** | Whitening sits only on the reward side (§2.3 iv). $W$ is never inserted into density products (step 5). |
| Brief §2: no tracking losses or phase clocks | **PASS** | — |
| Brief §2: estimator is causal, bounded, and its interaction with target EMA is specified | **PASS** | Eq. (11): detached FP64 EMA of target-$\bar B$ Gram on committed real frames; $O(d^2)$ state; checkpointed; frozen tuple per update. |
| Baseline compliance (baseline/01, 03, 05) | **UNVERIFIED** | Several mechanics are attributed to baselines I could not read: target modules *copying* online BN buffers (step 2); the 10–20° tangent rotation for `near`; the $\min_k$ ensemble tail; baseline-05 schedule wording. The BN-copy rule in particular does not appear in the charter. The adjudicator must confirm it is baseline rather than new mechanism. [MINOR, contingent] |

**Gate verdict:** I found no hard-constraint violation. Proposal B also notes (header) that isolation was not sandbox-enforced. That is an orchestrator matter, not a defect of the proposal.

---

## 2. Rubric-Keyed Technical Objections

### 2.1 Exact Mathematical Derivation (30%)

The derivation is correct and unusually careful. It does three things well:

- It separates three readouts: the density readout $f^\top b_g$, the raw-kernel return $q^\top b_g$, and the extra-inverse readout.
- It shows correctly that $z_g=B(g)$ is the exact point-reward encoding, so the FB goal readout has no Gram bias.
- It gives sharp bounds: Kantorovich (5), the Pinsker-derived $\delta$ bound, and the Rényi-2 lower bound (7).

Objections:

- **[MINOR] The effective-rank leg of $\epsilon(\kappa,R)$ is vacuous at the program's dimensions.** $\delta\le d\sqrt{D/2}$ gives $\epsilon<1$ only when $D<2/d^2\approx3\times10^{-5}$ at $d=256$. In practice (6) is a $\kappa$-only bound. Say so, rather than presenting it as a "joint" $(\kappa,R)$ bound. Bound (13) has the same problem: the factor $\sqrt d\|z\|=d$ makes it uninformative at $d=256$.
- **[MINOR] The premise of (10) is stricter than needed.** The resolvent bound needs only $e<a+\ell$, not $e<a$. As written, damping is excluded from rescuing a case where the premise fails.
- **[MINOR] A useful link to the FB loss is missing.** For fixed $B$, the population least-squares FB measure loss has minimizer $F^\star=\Sigma^{-1}q$, so $h=0$. Hence $h\neq0$ comes only from TD bootstrapping and limits on $F$'s capacity. That is exactly why the density readout needs no further correction. Stating this would tie §1.1 to the learning objective instead of to an "exact factorization" assumption.
- **[MINOR] Command and Gram coordinates are slightly mismatched.** The hybrid reward multiplies $W_t$, a target-$\bar B$ Gram, by a $z$ that comes from **online** $B$, whether `z_update` or an expert prompt. The dual conversion is coordinate-consistent only to $O(\tau)$ lag. §2.4 logs the online/target discrepancy but does not bound its effect on $r_z$. A one-line term $\|W_t\|\,\|z_{\rm online}-z_{\rm target}\|$ in (13) would close this.

### 2.2 Stability Under Non-Stationary $\rho$ (25%)

The damping rule (12) does guarantee $\|W\|\le20$ and $\kappa\le100$, and the rank-deficiency handling (support projector, C-B01-B-02, hybrid off) is sound. The gate thresholds, however, are badly calibrated for inverse-sensitive quantities:

- **[MAJOR] The calibration-agreement gate uses the wrong norm.** "Two halves differ by more than 0.10 *relative operator norm*" is dominated by $\lambda_{\max}$. Consider the moderate regime: $\lambda_{\max}\approx3.5$, $\lambda_{\min}\approx0.117$, smallest replay mass $\approx4.6\times10^{-4}$. Each 65,536-frame half then has about 30 samples in the weakest direction, a relative standard deviation of roughly 18%. The halves can therefore disagree by about 25% on $\lambda_{\min}$, and so on $W$'s largest gain, while the relative operator-norm difference stays near 1%. The gate should be the whitened discrepancy $\|\widehat\Sigma^{-1/2}(\Sigma_{(1)}-\Sigma_{(2)})\widehat\Sigma^{-1/2}\|_2$, which is what (10) actually controls.
- **[MAJOR] The representation-residual gate is not scaled by the inverse.** The gate is $\|q-\Sigma F\|/\|q\|\le0.10$. But the return error is $h^\top\Sigma^{-1}z$, bounded by $\|h\|\,\|W\|\,\|z\|$. With $\|W\|$ up to 20 and $\|z\|=\sqrt d$, a residual that passes can still produce an error larger than $f^\top z$ itself. Gate on $\|\Sigma^{-1/2}h\|/\|\Sigma^{-1/2}q\|$, or directly on $|h^\top Wz|$ for sampled commands.
- **[MAJOR] The gates are global, but the risk depends on the command.** The commands this program cares about are expert or out-of-support frames, such as the single 0.704 m demonstration. These are the ones most likely to load on low-$\rho$, small-eigenvalue directions. Those directions are where $W$ amplifies most (up to 20×) and where the tracker has the fewest samples. A gate that passes on $\lambda_{\min}\ge0.05$ globally can still yield poorly estimated, large-magnitude rewards for exactly those prompts. Proposal B notes that out-of-support prompts lack a $1/\rho$ interpretation (§1.4) but adds no per-command safeguard. Possible safeguards: a gate on $z^\top Wz/\|z\|^2$, the cosine $C(z)$ from (5), or command-wise split-half agreement of $Wz$.
- **[MAJOR] The actor objective switches discontinuously when the gate flips.** The standard actor uses **online** $F$ (step 6); the hybrid uses a damped prefix plus a **target** $\bar F$ tail (step 7). As the gate opens and closes with calibration noise, the optimized objective jumps between two non-equivalent functionals. §2.4 even notes that the damped-prefix/undamped-tail mismatch is not Bellman-consistent. No hysteresis, minimum dwell time, or blending is specified, and the spike never exercises toggling.
- **[MINOR] Two thresholds contradict each other.** The operational gate admits $\|W^{1/2}\Sigma_{\rm cal}W^{1/2}-I\|\le0.5$, which allows $\kappa(C)$ up to 3. The spike's corrected-metric gate requires $\kappa(C_t)\le2$. Production would therefore accept states the spike would count as failures.

### 2.3 Compatibility with the UFO Update Contract (25%)

This row is strong. The placement table (§2.3) is well argued: no whitening for (i) `z_update`, (ii) expert/near prompts, or (iii) the standard actor; whitening only for (iv) explicit hybrid rewards. This follows directly from §1.1/§1.4 (F already holds the dual factor). The update order and stop-gradient list are explicit, and the contract fixture asserts byte-identical `behavior_z`.

- **[MINOR] BN-buffer copying to target needs confirmation.** If target modules take online BN buffers every update (step 2), target coordinates are not EMA-smoothed with respect to BN. The tracker in "target coordinates" then lags BN-driven affine (non-rotational) jumps at the online BN rate. Proposal B concedes this in §2.4 but neither quantifies it nor models it in the spike (see §4). The baseline must confirm the copy rule is not new.

### 2.4 Spike Falsifiability (20%)

The pre-registration discipline is excellent: seeds, attempt limits, budget, `INCOMPLETE` semantics, and no subset passes. Its substance has gaps, detailed in §4. In rubric terms:

- **[MAJOR]** The brief asks for pre-registered thresholds on **effective rank and value error**. Proposal B registers *tracker estimation error* on $R$, but no threshold on the effective rank of any **learned** $\Sigma_B$. It also has no streaming gate on the value error $|J^\ell_H-J^\star_H|$ or $\Delta V_z$; only reward MSE and gradients are gated.
- **[MAJOR]** No fixture learns $B$, so the H1 premise is never tested: the claim that $\mathcal L_{\rm orth}$ leaves significant anisotropy early in joint training. A pass shows the correction works *if* anisotropy exists, not that it exists.

---

## 3. Audit of Rejected Alternative & Necessity Claim

### 3.1 Rejected alternatives: non-trivial, but the steelman is incomplete

**§3.1, hard batch whitening inside $B$.** This is a serious alternative, and counterexamples 1 and 2 are correct (verified numerically). Two problems remain:

- **[MAJOR] The strong version argued against is the exact-batch variant.** The competitive practical variant is different: a running-statistics ZCA/decorrelation layer *before* the sphere projection, trained jointly with $F$ (decorrelated-BN style). The proposal dismisses it in one sentence ("reintroduces covariance lag"). But the proposal's own tracker has exactly that lag, so the dismissal does not separate the two designs.
- **[MAJOR] Counterexample 3 proves too much.** Its point that changing $B$ invalidates historical `behavior_z` semantics applies to *every* gradient step on $B$. The baseline already accepts this drift by storing raw frames and re-encoding (charter H2). A slowly updated, jointly trained whitening layer is a reparameterization of $B$, not a contract break. The rejection therefore holds only for drop-in, batch-dependent forward whitening. That is what §3.1's final paragraph concedes, so the "rejected" alternative is in substance still open.

**§3.2, adaptive orthogonality dual ascent.** The atom bound ($\lambda_{\max}\ge pd$) and the collapsed-encoder radial-gradient argument are correct. Proposal B calls this "an empirical comparator", yet neither alternative appears in the spike's arms (§5.3). [MAJOR, see §4]

### 3.2 C-B01-B-01: premises, grade, falsifiability

- **Correctness:** The proof is correct. $\mathbb E_\rho[B\,B^\top a_z]=\Sigma a_z$, SPD gives uniqueness, and the value-equivalence half is right given a spanning family of $f$.
- **Premises (Appendix B structure as quoted by B):** The state, grade, premises, conclusion, proof, implementation-independence, operational test, and falsifier fields are all present.
  - **[MINOR]** "Exact density factorization" is listed as a premise but is needed only for the value-equivalence half; the encoding invariant holds without it. Separate the two halves so a reader does not think the invariant fails whenever factorization is approximate.
  - **[MINOR]** "Fixed finite outcome space" excludes the program's continuous motion space. A measurable-space version, with $\rho$-a.e. statements, is immediate and should be given.
- **Informativeness / necessity force [MAJOR]:** The necessity is definitional. Once you require the explicit reward's $\rho$-encoding to equal $z$, $a_z=\Sigma^{-1}z$ is forced by linear algebra. That is a restatement of brief §1(1) and charter H1's premise, not a new constraint on design. It does not show that dual conversion is necessary for anything the program values, such as goal-reaching, gradient quality, or the hybrid objective. Proposal B's own §1.1 shows the standard actor and goal readout do *not* need it. Under the proposal's own §11.5 standard ("framed agreement ... not independent evidence"), C-B01-B-01 should be presented as an invariant or lemma, not as a necessity claim with veto potential. Grade 1 is fair for its truth, not for its weight in decisions.
- **Falsifiability [MINOR]:** The falsifier is purely proof-theoretic: exhibit $a_z\neq\Sigma^{-1}z$ with $\Sigma a_z=z$, which is impossible. The "operational test" (FP64 residual $\le10^{-10}$ at $\kappa\le10^3$) tests solver numerics, not the claim. That is acceptable for a mathematical claim. The proposal should state plainly that no empirical outcome can refute it, only premise violations, which are logged as applicability limits.

---

## 4. Spike Protocol Critique

**Missing controls / arms**

1. **[MAJOR] No learned-$B$ arm.** All fixtures construct $B$ analytically. Brief deliverable 3 asks for measurement "on the 229-D / 277-D motion representation". Here, $q\in\{229,277\}$ enters only through Gaussian prototypes and a kernel interpolant, so it is a nuisance dimension. That makes the "pass separately for every $(q,d)$" rule look more stringent than it is. At minimum, add one arm that trains $B$ with $\mathcal L_{\rm orth}$ on a non-stationary synthetic $\rho_t$ and records $\kappa$ and $R$ trajectories. That would test whether the anisotropy premise holds.
2. **[MAJOR] The rejected alternatives are absent from the arms.** Neither adaptive-$\alpha$ orthogonality (§3.2) nor a running-ZCA pre-projection layer (§3.1) is compared, even though §3.2 promises an empirical comparator. Only "solve vs no solve" is isolated, not "solve vs representation-side fix".
3. **[MAJOR] The hybrid gate's residual condition is never exercised.** Every fixture has exact $F=\Sigma^{-1}q$, so $h\equiv0$. Neither the $\|q-\Sigma F\|$ gate nor $h$'s amplification by $\Sigma^{-1}$ (§1.5) is tested. Add a fixture with a controlled $h\neq0$, for example a rank-limited or noise-perturbed $F$.
4. **[MINOR] Gate toggling is not simulated.** No stream measures the actor-objective discontinuity from §2.2 above.

**Unmeasured confounds**

5. **[MAJOR] The fixtures stay in the regime where at most $d$ distinct states exist.** In fixture C (and A) the number of prototypes equals $d$ and $B$ is invertible. The whitened kernel is then *exactly* $\delta_{jg}/\rho_g$, so ORACLE reachability is perfect by construction. With far more states than $d$, as in real replay, both kernels are projections and the reachability benefit of correction is unknown. That is the regime behind charter H1's "improves single-frame goal-reaching accuracy". Add a fixture with $n\gg d$ states and a rank-$d$ $B$.
6. **[MAJOR] The drift model is only a rotation.** A plane rotation of 2×10⁻⁴ rad per update plus a 0.15 rad jump preserves the spectrum. Real drift (BN-buffer copies, encoder learning, replay shifts) is affine and changes the spectrum continuously. A rough calculation gives an EMA lag of about $\omega/\beta=0.02$ rad, $\kappa(C)\approx1.24$, so the moderate-stage gates are easy to pass under this drift. Add a non-orthogonal drift, e.g. $B_t=\mathrm{proj}((I+\epsilon_tE)B)$ with time-varying scale on the low-variance directions.
7. **[MINOR] Gradient and reachability are tested only when stationary.** Fixture C uses a stationary stream at $\kappa_0$ derived from $10\times$ replay skew. No gradient or reachability gate is evaluated under drift or at $\kappa_0=1000$.

**Threshold flaws**

8. **[MAJOR]** The calibration-agreement gate uses an unwhitened relative operator norm (see §2.2). Its threshold of 0.10 cannot detect inverse-relevant disagreement.
9. **[MAJOR]** There is no value-error gate. Add streaming gates on $|J^\ell_H-J^{\star}_H|/|J^{\star}_H|$ and on the damped-prefix/undamped-tail mismatch, per brief rubric row 4.
10. **[MINOR] The reward-MSE gates are lenient relative to the known effect size.** At $\kappa_0=30$, RAW NMSE is about 0.59 by closed form, so "≤0.25×RAW" (≈0.15) is non-binding next to the absolute 0.02 gate. The effective-rank gate (±0.03$d$) checks tracker accuracy, not representation quality.
11. **[MINOR] Fixture C's candidate-action distribution is not specified.** "256 seeded candidate actions" is the only description. The RAW baseline agreement, and so the "+5 pp" gate, depends on it: my rough re-implementation gave 75–86% RAW agreement. Pre-register the distribution, e.g. $\tanh(\mathcal N(0,I))$, and the expected RAW agreement.
12. **[MINOR] The seed bootstrap is not meaningful.** 10,000 resamples of 5 seeds draw from only 126 distinct multisets. Report exact paired-difference ranges instead of implying bootstrap precision.
13. **[MINOR] The gate scale contradicts production.** The spike gates on $\kappa(C)\le2$ while production accepts up to about 3 (see §2.2).

**Summary judgment.** The mathematics is correct, contract compliance is very good, and the placement decision (reward-side solve only) is well justified. The main weaknesses are:

- stability gates calibrated in norms that do not control the inverse, with no per-command safeguard for out-of-support prompts;
- a necessity claim that is a definitional invariant;
- a rejected alternative left open in substance, with no empirical comparator;
- a spike that, with analytic $B$, at most $d$ states, rotation-only drift, and $h\equiv0$, cannot test H1's premise or its practical benefit.

None of these violates a hard constraint, and all can be fixed without changing the core design.
