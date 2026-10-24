# Blind Review B on Proposal A (Packet B02)

Scope: `packets/B02/brief.md` is absent. I used `briefs/B02-nonstationarity-and-off-policy-credit-assignment-in-joint-fb-task-training.md`, also identified by A, plus the charter, Proposal A, and the pinned method's §11.5 and Appendix B. No other review or draft was read. Author-reported dry runs were not independently verified.

## 1. Gate & Hard-Constraint Audit

**Disposition: revise before acceptance; C-B02-A-01 is not eligible for locking as written.**

| Constraint | Audit |
|---|---|
| Charter §2.1: no BC/tracking fallback | Pass at specification level: no such actor loss or reward is proposed. |
| Charter §2.2 and brief §2: BN order, fresh 50/50 relabeling, executed critic labels | Main method preserves these requirements. **[MAJOR]** Stage G's shadow critic N explicitly trains on re-encoded labels; being non-acting does not make that critic compliant. A §3.1 itself rejects this loophole. Designate N an isolated deliberate contract-violation control, rather than claiming the entire protocol satisfies the constraint. |
| Charter §2.3: single-frame motion-only B | Pass as specified: frame IDs are diagnostic metadata, excluded from network inputs. |
| Charter §2.4: credible failure versus corruption | Severe penetration is correctly retained with zero absorption potential. **[MAJOR]** Invalid-row exclusion is specified, but mandatory run/evaluation-panel halt and exclusion from normalizer updates are not explicit. Episode discard alone is insufficient. |
| Charter §2.5: verified evidence versus claims | Pass: synthetic checks are explicitly distinguished from registered experiments and learned competence. |
| Brief §2: joint training without pretraining/freezing | Pass: temporary frozen-weight diagnostic rollouts do not constitute a frozen training stage. |
| Brief §2: full-prefix zero-hidden burn-in | Correct in principle, conditional on retaining complete prefixes. FIFO prefix availability and actual recurrent input dimensions remain unresolved below. |

No compliance certification of implementation or unread baseline files is implied.

## 2. Rubric-Keyed Technical Objections

**Exactness of Off-Policy Semantics — 30%**

- **[CRITICAL] M1/M3's advertised certificate does not follow (§§1.2, 2.2).** The conditional trajectory KL is an expectation; a realized path sum and a 32-row bucket average are estimators over different conditioning states. Small average KL neither controls every `(H,z)` nor upper-bounds chi-square divergence. The identity `chi² = exp(2 KL) − 1` requires stronger restrictions than the gate enforces: fixed variance, state-independent likelihood increments and, for the stated simple identity, fixed horizon. Random early termination also needs separate treatment. Thus `KL̄ ≤ 0.02` does not certify `|b| ≤ 0.2 sd(y)` or rare IS truncation. Rare high-drift states can dominate chi-square while being missed by the sample. Supply a justified upper confidence bound under explicit tail assumptions, or call M1 a heuristic and remove its guarantee.
- **[MAJOR] Policy-independent filtering is assumed, not established (§1.0).** Past actions alone are insufficient: require full relevant observation history, a common initial hidden-state law, and no behavior-policy information outside that history. A finite LSTM representation need not preserve the filtering belief. Under these premises the action-Q/macro-z distinction is sound; the unconditional assertion of zero action-Q age bias is too strong.
- **[MAJOR] Fixed-target regression and Bellman fixed points are conflated (§1.2).** With fixed `V̄`, the target map is constant in the fitted Q; a roughly 10-fold fixed-point amplification is not established. A genuine contraction argument must define an operator depending on its Q argument, hold the continuation policy fixed, evaluate the operator discrepancy at a specified fixed point, and bound contraction uniformly across old/current kernels and stopping times. Also, §1.6 reverses the sign of the `gamma^K` substitution error: wrong minus correct is `(gamma^K − gamma^k)V̄`.
- **[MAJOR] Gate edge cases undermine its interpretation (§2.2).** Floors can knowingly admit over-threshold generations; the subsequent monotone cutoff can defeat those floors. The case where even the newest bucket fails has no defined cutoff. Specify precedence, startup and starvation behavior, and report every certificate override. A held-out subset removes direct self-selection but does not establish independence for temporally correlated rows from shared episodes/adaptive collection.

**Compliance with R2.1 & v2 Contracts — 25%**

- **[MAJOR] Exact drift is incompatible with the proposed fp16 storage (§2.0, c1).** Quantizing a mean near one commonly introduces error around `1e-4`, already above the `1e-6` snapshot threshold; quantized standard deviations and raw actions also perturb likelihood ratios. Preserve collection precision or derive quantization bounds and test the actual serialization path.
- **[MAJOR] Prefix reconstruction is underspecified (§2.3).** Complete prefixes must survive FIFO eviction even when their TD rows are excluded. Stage S's 135-dimensional LSTM input is not reconciled with the explicit additional 256-dimensional previous-z input; specify concatenation/projection and reset semantics. Validate online/target Q and P separately, including bootstrap beyond the sampled slice. `no_grad` alone does not freeze BN updates; the guard must verify the actual update mechanism.

**Computational Overhead — 20%**

- **[MAJOR] The <5% requirement remains unverified (§2.1).** FLOP estimates omit prefix reconstruction across six recurrent networks, replay cloning/transfers, hashes, snapshot maintenance, SVDs, and diagnostic simulation. D5 cannot be excluded merely because it uses separate environments. Equal committed steps are not equal compute across IS, soft-weighting, and shadow-critic arms. Measure synchronized end-to-end time against the same baseline, with an explicit diagnostic/evaluation accounting policy.
- **[MINOR] Replay memory is understated (§2.0).** Three 29-element fp16 columns require 174 B/step before prompt anchors, IDs, and existing fields; fixed scalar standard deviation reduces this, but must be specified. A 256-element anchor adds 512 B per stored expert/near step. State whether anchors are deduplicated per macro and include prefix retention in the budget.

**Spike Falsifiability — 25%**

- **[CRITICAL] PASS need not establish the brief's drift deliverable (§5.1).** Every drift/bias check is optional `[A+]`; all may fail while PLAN passes. Burn-in equality is not bounded TD error under representation drift. Require a distinct B02 mechanism verdict with generation-lag and value-bias checks, without silently changing the registered PLAN verdict.
- **[MAJOR] Stage G's significance test uses pseudoreplication (§5.2).** Checkpoints within a seed are correlated. Three independent seed pairs cannot attain one-sided exact signed-rank `p < 0.05` (minimum `1/8`). Predefine seed-level aggregation and enough independent runs, or an appropriately justified dependence-aware analysis. A 1–14% improvement also falls between the ≥15% prediction and the stated non-improvement falsifier; specify success, failure, and inconclusive outcomes.

## 3. Audit of Rejected Alternative & Necessity Claim

**Rejected alternative: substantive analysis, limited novelty.** A distinguishes prompt-coordinate refresh from outcome-dependent hindsight relabeling and identifies a real label/kernel mismatch. However, the brief explicitly asks for this comparison and the charter already forbids changing task-critic labels. Under method §11.5, agreement on retaining executed labels is framed agreement, not independent necessity evidence. The additional comparison against row filtering/untruncated IS is more informative. “Strictly dominated whenever actor drift is zero” is excessive: endpoint values can coincide, and non-constancy along an arc does not imply unequal endpoints.

**C-B02-A-01: retain only a narrowed Candidate.** Parts (a) and (b) have a defensible invariant/bound form and implementation-independent reasoning. Appendix B.3 nevertheless requires explicit scope: a common sufficient history and initial belief, a fixed target functional during comparison, support conditions for the relevant KL direction, and finite span or finite variance/chi-square for useful bounds. P5 alone does not make reverse KL finite.

**[CRITICAL] Part (c) overgeneralizes deterministic label replacement to arbitrary outcome-dependent maps.** For a concrete terminal one-step counterexample, let a fixed Gaussian actor produce Bernoulli reward probabilities `1/4, 1/2, 3/4` under three commands (reward is the indicator of positive action). Collect only the middle command. Let the terminal state also contain independent `u ~ Uniform[0,1]`; relabel high iff `u < 1/4 + r/2`, otherwise low. Then `E[r | high] = 3/4` and `E[r | low] = 1/4`, exactly matching their true operators, although the executed command's value is `1/2`. P1–P5 can hold, and terminal targets are independent of Q, so this works for all Q. It is contract-forbidden but mathematically refutes the unrestricted necessity statement. Restrict (c) to outcome-independent, unweighted replacement at fixed original `(H,z)`, with explicit treatment of pooling and operator-equivalent commands.

The falsifier's assertion that any counterexample “must violate a premise” prejudges the result. Appendix B.3.4 permits a counterexample to invalidate the conclusion itself. The exact-zero/common-random-number demonstration verifies an implementation identity, not universal necessity; one re-encoding failure cannot prove the universal obligation. Appendix B.9 independent verification and human signature remain necessary for any eventual lock.

## 4. Spike Protocol Critique

- **[MAJOR] Missing independence direction.** b1 checks that FB updates do not mutate behavior labels. The brief also requests that mutating behavior labels not change `z_update`. With identical RNG, motion inputs, weights and frozen statistics, alter only `behavior_z` and require identical relabel samples. Test 50/50 composition, online versus target B, permutation, sphere norm, and actual critic consumption; unequal `data_ptr()` values alone do not exclude overlapping storage.
- **[MAJOR] Missing mechanism controls.** Add matched-capacity FIFO/random-age controls to separate drift selection from smaller replay and shifted source/height distributions. Exercise state-dependent drift, rare high-KL states, changing variance, clipping, short termination/timeout macros, fp16 round trips, and gate starvation. Include both actor-only and normalizer-only drift and a step action-Q control.
- **[MAJOR] Calibration endpoint is confounded.** Fix diagnostic histories/states and commands across arms, define MC horizon/tail and terminal handling, and match the continuation policy to the critic's intended target. Separate online-versus-target policy lag from replay-age bias. Report raw error and a common normalization: arm-specific `sd(G)` can manufacture apparent improvement. Account for MC uncertainty in both calibration and estimated divergence bounds, not only the bias estimate.
- **[MAJOR] D5 does not certify uncontrollability.** A motion-distance ratio near one under independent noise can hide reward-relevant contact/ball effects; non-monotone distance versus latent angle is not itself failure. Add paired-noise interventions and task/contact outcomes with confidence intervals. A noisy proxy cannot establish the exact distribution-independence premise of C-B02-A-03.
- **[MINOR] Thresholds need scope.** A stale hidden state need not exceed `1e-2` if the chosen regression barely changes recurrent dynamics; demonstrate that the injected fault is active before interpreting the negative control. Clarify that `3/(2 n_e)` is an asymptotic normalized mean-square error, not a 19% latent or RMS error, and distinguish same-batch normalization from independent query normalization.
