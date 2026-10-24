# Blind Review A on Proposal B (Packet B04)

Reviewer: Blind Reviewer A. Inputs read: `PROGRAM_CHARTER.md`, `packets/B04/brief.md`, `packets/B04/proposals/B.md`,
`packets/B04/spikes/B04-SPIKE/VERDICT.json`. I did not read any baseline, draft, or other review, so every claim below
about `baseline/03` §6 rests on how the brief cites it. I ran no code; every check here is analytic.
Overall: the gradient algebra is mostly correct and the stop-gradient rules are careful. But the four arms do not match
the brief's contract, the necessity claim is circular, and the spike's reference gradient makes larger H look better by
construction. Recommendation: **Major revision.** I found no Hard-Constraint violation that blocks the proposal outright.

## 1. Gate & Hard-Constraint Audit

| Constraint | Status | Evidence / Note |
|---|---|---|
| Charter HC1 (no BC / tracking) | PASS w/ note | No action-MSE or pose reward. However, Arm D's actor maximizes $\widehat J_H$ (model head + FB tail), not "exclusively" $F^\top z$. The brief's deliverable 1 asks for this, but B.md never says that the brief overrides HC1. It must say so explicitly. |
| Charter HC2 (z separation) | PASS | L151-152: fresh 50/50 frozen-BN `z_update`, `behavior_z` is never overwritten, and task $Q$ trains on executed commands. |
| Charter HC3 (single-frame B) | PASS | $B$ sees only $M(s)$. Terrain enters $W_\psi$ only (L123), which is allowed. The toy embedding (L205) is also allowed. |
| Charter HC4 (penetration vs invalid) | PASS | L156 handles real replay correctly. L145 and L202 keep the imagined soft hazard separate from the hard `severe_penetration` label. |
| Charter HC5 (evidence vs claims) | PASS | L3 and L234 assert nothing about measured gains. Note: the `PASS` in VERDICT.json comes from a 3.5 s CPU toy run. It must not be cited as evidence about $H$ until it has been reconciled with B's protocol (§4). |
| Brief HC1 (no future frames in $W_\psi$) | PASS | L123 and L124 use only a causal state/belief and a detached real-prefix burn-in. |
| Brief HC2 (4 arms = `baseline/03` §6, shared plant/compute) | **FAIL (contract)** | L5 replaces the §6 arms with "the user's four-arm definitions". That source is not part of the frozen context. Brief §3.3 asks for A/B/C at $H{=}1$ vs $H{=}32$ and D at $H\in\{1,4,8,16\}$. B's Arms B and C are critic-target arms whose actor uses $H{=}0$. The shared compute protocol itself (L230-231) is satisfied. |

## 2. Rubric-Keyed Technical Objections

### 2.1 Mathematical Rigor of Gradient Decomposition (30%)
- I checked these and they are correct: the sensitivity recurrences (L27), $g_\infty$ (L29), the adjoint form (L33), $\hat g_H$ including the
  $P_H$ terminal injection (L47), the $H{=}0$ reduction (L49), the oracle tail $T_H$ (L53), the $E_{t+1}$ recurrence (L71), and the
  closed form for $L{=}1$ (L79). The chain rule that separates first-action from shared-parameter terms is exact. This is the proposal's strength.
- **[MAJOR] The reference gradient favours large $H$ by construction.** All errors are measured against the fixed-start $g_\infty$ (L21, L223).
  Even with an oracle model and critic, $g_\infty-g^{\rm oracle}_H=R_{>H}$, which shrinks only like $\gamma^{H+1}$. So both cosine and MSE against $g_\infty$
  improve with $H$ by definition. The standard FB actor samples $s_0\sim\rho_{\rm replay}$, so the gradient it actually targets is a
  $\rho$-weighted DPG surrogate. L40-41 acknowledge this, but no occupancy-weighted reference appears in the metrics or gates.
  Required fix: report every panel against both $g_\infty$ and $\nabla_\theta\mathbb E_{s_0\sim\rho}J_\infty(s_0)$.
- **[MAJOR] The error bound becomes vacuous exactly where it matters.** $\epsilon_W=\|W_u-\Sigma^{-1}\|\approx 1/s_{\min}-1/(s_{\min}+\ell_u)$ blows up as
  $s_{\min}\to0$, which is the singular-Gram regime the charter rubric lists. During contact, $L\gg1$ (in the L198-200 plant,
  $\partial v'/\partial q\approx-\Delta k=-10$), so $A_t(L)\sim10^t$ and $B_H$ is uninformative once $H\ge2$. Without a contact-local
  or expected-Jacobian refinement, the bound cannot guide the choice of $H$, which is what deliverable 1 asks it to do.
- **[MINOR] The proof's coupling assumes the model shares the true noise.** "Coupling with identical noise" (L70) presumes the
  ensemble is a reparameterized copy of $f(\cdot,\xi)$. A deterministic MLP member does not share $\xi$, so $\epsilon_s$ also contains aleatoric spread that more data cannot shrink.
- **[MINOR] Normalizer and dimensions.** With termination, the occupancy normalizer in L40 is $\mathbb E\sum_t\gamma^tc_t$, not $1/(1-\gamma)$.
  For the humanoid case, $d_s$, $d_z$ and $\dim b$ are never given numerically, although the charter requires exact tensor dimensions.

### 2.2 Strict Zero-Future-Leakage Guarantee (25%)
- **[MINOR] Coordinate mismatch.** $z$ is encoded by the *online* $B$ (L151), but the actor head uses *target* $\bar B$ with $W_u$ (L44).
  The proposal measures the resulting splice mismatch for critic targets (L113) but not for the actor pass.
- **[MINOR] Selection bias from burn-in.** Requiring a 16-step real prefix and rejecting segments without one (L124) removes all early-episode
  starts from imagination. The resulting start-state shift should be reported. Apart from these two points, the leakage contract is sound.

### 2.3 Contact Stiffness & Rollout Stability (25%)
- **[MAJOR] No contact-handling mechanism is specified.** L154 defers to "event/saltation treatment or a declared surrogate-bias panel".
  A SiLU MLP is smooth by construction, so near impacts it will either over-smooth the Jacobian or produce very large ones. Neither gradient clipping
  at 10 (L155) nor post-hoc selection of $H$ (L157) addresses this. Deliverable 2 calls for an *adaptive* horizon, yet B only picks a fixed $H$ on validation data.
  Possible mechanisms include per-rollout truncation when ensemble disagreement or $\|\hat G_x\|$ crosses a threshold, $\lambda$-mixing across horizons, or per-step Jacobian-norm caps.
- **[MAJOR] Model exploitation is unguarded.** Pessimism is applied only at the tail ($\min_k$). The $H$-step head has no penalty for ensemble
  disagreement, so the actor can climb on model errors. This also weakens the charter's "conservative FB value" requirement.
- **[MAJOR] Training and rollout horizons differ.** $\mathcal L_{\rm wm}$ unrolls 8 steps (L125), but $H\in\{16,32\}$ rollouts are evaluated, which extrapolates beyond what the model was fitted on.
  The loss also contains no Jacobian/Sobolev term, while the bound depends on $\epsilon_J$ and on the derivative part of $\epsilon_c$. L130 admits that BCE does not certify these derivatives.

### 2.4 4-Arm Ablation Completeness (20%)
- **[CRITICAL] The multi-task-$z$ / representation confound is never isolated.** L104 keeps the representation networks in every arm,
  and L105 makes the single-task/no-$F$ variants optional. The rubric explicitly asks for a separation of throughput, $H$, and multi-task $z$.
- **[CRITICAL] Throughput is not separated from pathwise depth.** D at $H{=}1$ vs $H{=}32$ changes two things at once: the number of imagined transitions and the
  differentiation depth. The missing control is the same $H$-step rollout with $\hat S_t$ detached between steps
  (MVE-style value expansion), matched on imagined transitions and GPU-seconds.
- **[MAJOR] Arm B collapses into Arm A.** The policy is deterministic and continuous, and $\theta$ changes every update. So "consistent with current target policy"
  (L115) is a measure-zero event, and $n_{\rm eff}=1$ almost surely. No tolerance is specified. As a result, A–B tests essentially nothing in primary training.
- **[MAJOR] Pure world-model $H{=}32$ without a tail (charter H3) is not an arm.** It appears only as a gradient diagnostic (L175, L219), not in the
  online follow-up.

## 3. Audit of Rejected Alternative & Necessity Claim

**Rejected alternative (B-only latent model, L161-171): trivial (a strawman).** The impossibility witness depends entirely on
removing terrain from the latent input, and HC3 already forbids terrain in $B$. So "$T_{\rm lat}(\bar B(m),a)$ cannot see terrain"
is a restatement of the constraint, not a finding. L170 concedes that an augmented latent ($h_t=E(o_{\le t})$ with a $\bar B$ reward
head, i.e. a Dreamer-style model) could remove the obstruction. That augmented latent is the serious alternative, and it is never evaluated.
L171 also undercuts the selection rationale. Under partial observability ("observed terrain *where available*", L123), the full-causal-state
model faces the same omitted-variable lower bound. Its claim that "residual error can shrink with data" holds only when the state is fully observed.
The secondary alternative (no tail, L173-175) is a one-line counterexample and does not count as a considered design.
A non-trivial rejection would compare against (a) the latent model with causal terrain/belief inputs, and (b) value-expansion
(stopped-path) rollouts or occupancy-corrected actor gradients.

**C-B04-B-01: premises are stated, but the claim is circular and its falsifier is not empirical.**
- *Circularity [MAJOR].* The "additional premise" $R_{>H}\neq0$ (L181) is the conclusion $g_\infty-g^{\rm oracle}_H\neq0$, because L184
  proves $g_\infty-g^{\rm oracle}_H=R_{>H}$ by definition. Once that premise is granted, the Grade-1 necessity has no content.
- *Scope.* The premises (exact frozen-policy critic, exact dynamics, fixed start) never hold in any arm. L186 explicitly excludes the
  occupancy-weighted actor, which is the actual standard-FB comparator. So the claim says nothing about A vs D in practice.
- *Falsifiability.* The falsifier (relative mismatch above $10^{-6}$) tests whether the autodiff implementation is correct, not a statement about the world.
  It is also inconsistent with the reference-convergence tolerance of $10^{-4}$ (L209), so it could fire on truncation or round-off alone.
  A falsifiable version would bound $\|R_{>H}\|$ relative to $\|g_\infty\|$ under the replay distribution and predict the $H$ at which it drops below the model-error terms.
- I cannot check the formal Appendix B template because it is not in the frozen context. The proposal does supply premises, a grade, an operational test, and a falsifier.

## 4. Spike Protocol Critique

1. **[MAJOR] The reference artifact (§2.1) carries through to the gates.** The L227 gate (20% MSE improvement against A and D32) is computed
   against $g_\infty$, so the $H{=}0$ arm is penalized by $R_{>0}$ even when its critic is perfect. An occupancy-weighted reference panel is required.
2. **[MAJOR] Multiplicity and metric choice are unresolved.** "Some $H\in\{4,8,16\}$" is three comparisons across 10 seeds with no correction. Cosine and MSE can
   rank horizons differently. In VERDICT.json, $H{=}32$ has the best cosine (0.556) but the worst relative error (1.024). The proposal must name one primary metric.
3. **[MAJOR] The online follow-up (L232) has a budget and cadence but no pre-registered success metric or threshold,** and no task-return gate.
   Gradient MSE on a 1-D plant does not answer the brief's acceleration question.
4. **[MAJOR] The "isotropic" control is not isotropic.** With $A{=}I$ and $q\in[-0.02,0.20]$, $\sin q\approx q$ and $\cos q\approx1$. The features are therefore nearly
   collinear, $\Sigma$ is ill-conditioned, and $\epsilon_W$ is large in the supposed null panel. Either pick a well-conditioned feature map as the null,
   or report the condition numbers as a covariate.
5. **[MAJOR] The non-stationary $B_\omega$ is untested.** $\bar B$ is a fixed analytic map (L205), but the brief's challenge 2 is an evolving $B_\omega$.
   Add a drift panel in which $A$ is rotated or rescaled between the critic and actor snapshots.
6. **[MINOR] Unspecified details.** The near-zero exclusion threshold for cosine (L224) is not given. Ensemble use during rollout (random member, mean, or fixed) is not given.
   Surrogate perturbation magnitudes are not tied to measured $\epsilon_J$ ranges for the real humanoid plant.
7. **[MINOR] VERDICT.json does not match the protocol.** It reports cosine and relative L2 only: no seeds, no CIs, no MSE, no B/C arms, no raw-head control
   at any $H$ other than 8, and no Gram eigenvalues. Taking point estimates at face value, MSE ∝ rel.err². $H{=}16$ is about 28% below A and 30% below D32
   (it would pass L227 if the CI holds), while $H{=}8$ is only about 16% below A (fails). The `PASS` label is therefore not traceable to B's gate. The spike must be rerun under B's protocol before any $H$ is locked.
