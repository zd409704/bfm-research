# Blind Review A on Proposal B (Packet B03)

Reviewer: Blind Reviewer A. Inputs read: `PROGRAM_CHARTER.md`, `packets/B03/brief.md`, `packets/B03/proposals/B.md`,
`packets/B03/spikes/B03-SPIKE/VERDICT.json`. I read no baseline, synthesis, or method files. Because of that, claims about
baseline 04 schema sums (B.md:14) and method v1.0 Appendix B/§11.5 wording are judged only for internal consistency.
Overall: compliant and careful about caveats. But the theory and spike mostly certify tautologies, and they under-serve
brief deliverables 2(b)/2(c) and 3. Recommendation: **revise before spike lock** (no CRITICAL gate violation found).

## 1. Gate & Hard-Constraint Audit

| Constraint | Status | Evidence / note |
|---|---|---|
| Charter §2.1 no BC / tracking reward | PASS | Actor loss is $-\mathbb E\min_i F_i^\top z_{\rm update}$ (B.md:98-99). Spike (b)/(c) actors are fixed constructed `nn.Linear` maps, not trained (B.md:183). |
| Charter §2.2 behavior vs update $z$ | PASS | Critic trains on $z_{\rm actual}$/$a_{\rm applied}$ and "never substitute $z_{\rm update}$" (B.md:87). Labels are immutable and the 50/50 mixture is kept (B.md:117-118). BN two-pass ordering is only implied ("two real-data normalization passes"). [MINOR] State the order current→next and freeze BN explicitly. |
| Charter §2.3 motion-only single-frame $B$ | PASS | $B$ stays motion-only throughout (B.md:112). Alternative A, which would violate this, is rejected (§3). |
| Charter §2.4 penetration vs invalid | PASS | B.md:122, 215. Invalid panels keep their denominator as incomplete. |
| Charter §2.5 evidence vs claims | PASS | B.md:2, 163, 203, 216. VERDICT numbers are quoted with explicit non-inference caveats (B.md:161-162). |
| Brief §2 zero-force NPZ compatibility | PASS | No force, scan, or ball imputation enters $B$ or the demo encoding. Synthetic metadata is held in separate tensors (B.md:169). |
| Brief §2 no R1.3 admission / `infer_source_support_intent` | PASS | "No static admission or support-intent inference" (B.md:118). The 128-latent bank (B.md:208) is a diagnostic, not a filter. It must stay that way (see §4). |
| Charter rubric: no privileged leakage | PASS w/ note | The planner gradient comes from $Q(h^Q,c,z)$, i.e. it is shaped by privileged $c$ (B.md:82). This is legitimate asymmetric actor-critic. But the planner then optimizes $\mathbb E[Q\mid h^P]$ only if $h^Q\supseteq h^P$. [MINOR] State this inclusion as a contract. |

There are no hard-constraint violations. One contract risk remains: the proposal asserts that baseline 04's field sums are
278/107 rather than 277/93 (B.md:14), and that every theorem holds only for "declared abstract sizes". Until that is
reconciled, the ball-striking contract alignment is conditional. The packet should record it as an open blocker, not as a
footnote.

## 2. Rubric-Keyed Technical Objections

### Compatibility with Kinematic-Only Demo NPZ (30%)
- [MINOR] Compatibility is preserved, but by omission rather than analysis. The brief explicitly names (deliverable 2(c))
  an NPZ-derivable feature, causal acceleration $\widehat{\ddot q}$ from finite-differenced `qvel`, as the candidate $B$
  enrichment. The proposal never assesses whether such a feature counts as "single-frame" under Charter §2.3, or whether
  it is NPZ-compatible. That is the central compatibility question for this brief.

### Rigor of Aliasing Analysis (25%)
- [MAJOR] **Prop. 1 understates learned aliasing for ball striking.** B.md:26-27 says that extra collisions "may" exist
  and that distinct descriptors "can be separated by some motion-only map". For $D=277\to\mathcal S^{99}$, no continuous
  $B$ is injective (invariance of domain: $\dim 99<277$). So non-trivial fibers beyond $\sim_\kappa$ are certain. They,
  not exact descriptor equality, are the operationally relevant aliasing. Traversal ($229\to\mathcal S^{255}$) admits
  injective maps in principle. The two tasks therefore differ qualitatively, and the proposal treats them identically.
- [MAJOR] **Single-frame aliasing is conflated with FB-level aliasing.** FB values are
  $F(o,a,z)^\top z\approx\mathbb E\sum_t\gamma^t B(m_{t+1})^\top z$, which integrate $B$ over *future* frames. B.md:23
  concedes that equal frames do not imply equal next frames (impact velocity jumps). Contact regimes are therefore
  generically separable in successor-measure space even when $B(m_t)$ coincides. Only the degenerate case at B.md:68
  (identical future $B$-occupancy) is a true $B$ bottleneck. That case is the brief's case (c), yet it gets one sentence,
  and nothing estimates how often it occurs.
- [MAJOR] **There is no observability argument for $F$.** Prop. 2 covers the actor fiber $U=(o^{\rm low},z)$. The brief's
  core question also routes context into $F(o_F,a,z)$ and asks for necessity there. The required statement is missing: if
  $o_F$ omits geometry $g$ and future occupancy depends on $g$ at fixed $(m,a,z)$, then $F$ can only learn
  $\mathbb E_g[\cdot\mid o_F]$. The actor gradient $\nabla_a F^\top z$ is then biased toward the $g$-averaged contact
  response. Without this, "necessary" is proven for $\pi$ only, not for $F$, $P$, or $Q$.
- [MINOR] Prop. 2 conditions on "deterministic memoryless actor" but evaluates fibers of $U$ with $z=P_\psi(\mathcal H_t)$.
  The planner can pack history into $z$, so the effective actor information is $(o^{\rm low},\sigma(\mathcal H_t))$
  restricted to the latent image. B.md:64 acknowledges this. The fiber definition should be stated in those terms.
- [MINOR] The rank test (B.md:66) leaves $T$ (action→torque) undefined and ignores the `clip`/`tanh` saturation that the
  table itself flags (B.md:83). A saturated channel has a zero Jacobian and falsely reports inaccessibility. The fix is to
  mask active bounds before the rank computation.

### Diagnostic Precision (25%)
- [MAJOR] **No positive test for cause (c), "$B$ lacks contact features".** Cause (a) (planner) gets the 128-latent bank
  and cause (b) ($F$ ignores scan) gets mask/shuffle (B.md:208-211). Cause (c) is inferred only by elimination
  ("residuals with reachability intact implicate prediction"). It needs a direct probe. For example: a linear/MLP probe of
  regime $C$ from $B(m_{t+1})$ and from $F(o,a,z)$ on simulator-branched pairs, against a $\widehat{\ddot q}$-augmented
  diagnostic encoder arm.
- [MAJOR] **The 128-latent bank is underspecified.** The source distribution is not given (uniform sphere,
  $B(\text{demo})$, perturbations of planner $z$), and there is no success threshold, no branch count, and no statistic.
  In $d_z=256$, 128 uniform draws cover a vanishing neighborhood, so "no success" is almost uninformative. The proposal
  admits this (B.md:209) but then gives the diagnostic no decision power.
- [MINOR] Eval-time masking of scan in a network trained *with* scan conflates "uses the context" with covariate shift.
  The diagnostic needs arms retrained with the context masked (see §4).

### Spike Falsifiability (20%)
- [MAJOR] Spike parts (a)-(c) cannot fail except through implementation bugs (detailed in §4). The rubric asks for "a
  minimal, reproducible test with clear pass/fail criteria" that isolates $F/\pi$ conditioning from $B$ features. An
  algebraic identity check is reproducible but does not isolate any learned mechanism.

### Failure-Mode & Edge-Case Coverage (charter gate)
- Coverage is good: $k<K$ truncation, timeout vs termination, replay cuts inside held macros, full-prefix RNN burn-in,
  kick-flag reset, penetration/invalid. [MINOR] Full-prefix burn-in from zero (B.md:115) is $O(T)$ per sample, and its
  compute cost should be budgeted in the $K$-arm compute match.
- [MINOR] Singular $\Sigma_B$ is handled by deferring to B01, but the proposal does not say whether whitening is applied
  in the 128-bank $F^\top z$ calibration metric (B.md:210, "B01-compatible coordinates" is ambiguous).

## 3. Audit of Rejected Alternative & Necessity Claim

**Alternative A ($B'(m,g,\lambda,b)$) is not a serious admissible alternative.** Charter §2.3 already forbids it, so
rejecting it is required by the rules, not a finding. The argument for rejection is also partly a strawman. It attacks
*imputation* $\hat\lambda(m)$ (B.md:128-130), whereas the usual design is a masked-context encoder: $g$ is present for
replay frames and masked for demos. That design is still charter-forbidden, but its real failure mode is different
(train/prompt distribution mismatch in $B$-space) and goes unanalysed.
The genuinely non-trivial *admissible* alternative is a kinematic-only dynamic enrichment of $m$ (finite-difference
$\widehat{\ddot q}$, joint-velocity jumps, or a causal impact indicator derived from FK/qvel). The brief points to it
directly, and it is the alternative that would compete with "route context into $F/\pi/P/Q$". **Alternative B**
(monolithic recurrent policy) is non-trivial and fairly treated. Its proposed compute-matched comparator should be put
into §5, not left as "deserves" (B.md:136).

**C-B03-B-01 audit.**
- *Premises.* These are explicit and verifiable in a constructed fixture: deterministic encoder, identical $M$ and
  histories, balanced independent load, unique targets, $\Delta>0$. That part passes. One premise, "identical deployable
  histories", excludes the brief's headline case: the 0.40 m vs 0.60 m box *is* distinguishable by `scan[S]`. So the claim
  covers only hidden load/intention, not geometric aliasing.
- *Title vs conclusion mismatch* [MAJOR]. The title asserts that "information *separation*" (routing context into
  $F/\pi/P/Q$) is necessary. The conclusion establishes only that *some* distinguishing information is necessary, which is
  a trivial consequence: the conditional variance of a balanced binary target is $\Delta^2/4$. Nothing shows that routing
  into non-$B$ modules is necessary rather than merely sufficient. Retitle it to "distinguishing information is necessary
  for incompatible commands", or add a premise that excludes $B$ as the carrier.
- *Falsifiability* [MAJOR]. The falsifier ("paired population risk $<\Delta^2/4$ with premises verified") is impossible by
  algebra. The claim is a theorem, and its "operational test" can only detect bugs. That is acceptable for Grade 1 if it
  is labeled honestly. The empirically falsifiable content lies in the *scope* line (whether real simulator snapshots
  satisfy the premises), and that is where a test belongs.
- *Loss mismatch* [MINOR]. The bound is in squared torque error, while the actor is trained on $F^\top z$, not MSE. Using
  the acceptable-set form (B.md:40-42) with a return-gap bound would tie the claim to the actual objective.

## 4. Spike Protocol Critique

1. **(a) is tautological.** `torch.clone` inputs into a frozen eval-mode deterministic net give an exact 0.0 difference
   by construction. This tests determinism only. Missing: a learned-collision measurement, i.e. the distribution of
   $\|B(m)-B(m')\|$ against $\|m-m'\|$ on real extracted frames, especially for 277→100. The negative control
   (B.md:175) "records separation" without a threshold, so it has no pass/fail.
2. **(b) and (c) are analytic fixtures with guaranteed outcomes.** The checks are $R=0$ vs $2/3$ with a hand-set
   $\pi=-c\,e_1$, and the `paired_risk` identity with $\|a\|^2+1$. Tolerances of $10^{-12}$/$10^{-10}$ check float64
   arithmetic, not mechanism. Keep them as unit tests, not as the spike.
3. **Missing minimal learned spike (core gap).** A 2×2 factorial is needed: {motion-only $B$, $B$+$\widehat{\ddot q}$}
   × {context in $F/\pi$, context masked *at training*}. Train each arm with the unchanged FB objective (no BC), compute-
   and seed-matched, on one hand-support transition and one ball-impact transition. Pre-register the metrics:
   regime-conditional action separation, contact-regime probe accuracy from $F$, and branch success rate. Gates should be
   numeric with Wilson/bootstrap bounds. Only this design isolates $F/\pi$ conditioning from $B$ features, as deliverable
   3 requires.
4. **VERDICT reconciliation is not gated.** With exact pairing, identical inputs, and the sum convention with $\Delta=2$,
   per-pair risk is deterministically $\ge1$, so the reported 0.895 would be *impossible*. Under elementwise mean over 29
   channels the floor is $1/29\approx0.034$. Either convention, the absence of pairing, or a different $\Delta$ explains
   the number. Re-deriving it under the declared convention should be a pre-lock gate, not a remark (B.md:162).
5. **Confounds in the simulator diagnostics.** (i) Eval-time masking/shuffling vs retrained-masked arms (covariate shift).
   (ii) The same-state branching RNG must be shared across ablation arms (common random numbers), or paired differences
   inflate. (iii) Planner choice is confounded with $Q$ ranking error; report $Q$ rank correlation *within* the 128 bank
   on the same branches. (iv) The heights 0.30-0.70 m get no stratification or per-height $n$.
6. **Thresholds.** Only the analytic parts have numeric gates. The simulator extension reports "paired differences and
   95% intervals" with no pass/fail line, and with 5 seeds a t-interval is wide. Pre-register a minimum detectable effect,
   or declare the extension descriptive-only.
7. **Missing null baseline.** The Alternative B monolithic recurrent policy and a context-blind hierarchy should appear as
   explicit compute-matched nulls in the simulator extension (charter rubric "explicit null baselines").
