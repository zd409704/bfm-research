# Blind Review A on Draft B (feedback-round-2026-10-24)

Reviewer: Blind Reviewer A (Claude Opus). Program: `fb-beyond-imitation-acceleration`. Date: 2026-10-24.

Scope of this review: the five files under `feedback-round-2026-10-24/drafts/B/`, read against `briefs/BRIEF.md`, `briefs/OWNER_FEEDBACK_EN.md`, `PROGRAM_CHARTER.md`, `program-ledger.md`, `gpu_experiments/README.md`, and targeted source in `gpu_experiments/` (to check claims Draft B makes about that source). `drafts/A/` was not opened. No training, no code execution against research artifacts, and no writes outside this file. The only computation I ran was a short standalone arithmetic check (Wilson bounds and Student-t interval half-widths) to audit Draft B's thresholds. Prior B01–B05 script/GPU PASS results are treated here as local checks only, not as evidence that the framework works.

---

## 1. Gate and hard-constraint audit

| Constraint | Finding | Evidence |
| --- | --- | --- |
| Deliverable inventory (FRAMEWORK_REVIEW, GAP_TABLE, CORRECTED_CONCLUSIONS, MINIMAL_EXPERIMENTS, STATUS) | **Pass.** All five present. | `drafts/B/` listing. |
| English only | **Pass.** | Full read. |
| No commercial robot/product/company brand names | **Pass.** A grep for common humanoid, simulator, accelerator, and lab brand tokens found nothing. Draft B also avoids the platform model name that appears in the owner's B01 correction row and uses "home-humanoid plant-class" throughout. It also leaves out the simulator and accelerator names that appear in the ledger. | grep over `drafts/B/*`. |
| Operate under `/srv/claude`; no invented production paths | **Pass.** Every relative Markdown link resolves inside the program tree (I checked each target exists). GAP_TABLE says it does not assert or access production paths. MINIMAL_EXPERIMENTS lists the production entrypoints (`FBAgent.update`, `TaskLearner`, etc.) as things to *resolve*, not as paths it has. | Link-existence check; GAP_TABLE line 3; MINIMAL_EXPERIMENTS "Entry gate". |
| Do not claim B01–B05 PASS as framework validation | **Pass, stated clearly.** CORRECTED_CONCLUSIONS opens with "script/GPU PASS applies to the assertions executed by that script on its inputs," and STATUS repeats it. | CORRECTED_CONCLUSIONS ¶1; STATUS ¶4. |
| Isolation from sibling author | **Pass as far as I can check.** The draft-B run log shows `drafts/A/**` excluded from searches and a write-guard asserting `/drafts/A/` is not a destination. The only `drafts/A` hits are file listings of the *sealed B01–B05 packet* drafts (`packets/B0x/drafts/A/`), which belong to an earlier round and are outside this round's isolation rule. | `logs/FR-draft-B-codex.log` lines 49, 193–265, 1957. |
| Production verification marked as planned external steps | **Pass.** | MINIMAL_EXPERIMENTS ¶2 and "Required external evidence bundle". |
| Owner-preserved semantics (standard expert/near encoding, UFO z_update 50/50, F·z actor readout, no "all z whitened") | **Pass.** These are preserved in FRAMEWORK_REVIEW, CORRECTED_CONCLUSIONS (B01 row), and the A-F arm definition. | FRAMEWORK_REVIEW "What the theory licenses" ¶3; MINIMAL_EXPERIMENTS A-F row. |
| No bundled whitening / same-height relabel / world-model loss / B-input expansion | **Pass.** These are explicitly excluded from A-F and from the corrected mainline. | CORRECTED_CONCLUSIONS last ¶; A-F row. |
| Charter §2.1 (no BC/tracking fallback) | **Pass, scoped correctly.** The imitation comparator A-I is explicitly exempted *as a baseline*, and the constraint is kept for A-F. | MINIMAL_EXPERIMENTS A-I row. |
| Owner deliverable 5 (production plan: configs, identities, per-seed curves, costs) | **Partial.** Identities, configs, curves, and lineage are listed in detail. **Costs are only placeholders:** there are no accelerator-hour or wall-clock estimates, even order-of-magnitude ones, and all resource ceilings are deferred to "measured throughput" from the entry audit. See §4 and fix M4. | MINIMAL_EXPERIMENTS lines 63, 102. |

**Gate verdict:** no hard-constraint violation. One deliverable is incomplete: owner item 5 has no cost figures.

---

## 2. Critique of FRAMEWORK_REVIEW (theory / implementation / empirical separation; value judgment)

### 2.1 Strengths (to keep through adjudication)

1. **Layer separation is real, not cosmetic.** The causal-chain table gives each link a mechanism ("why it could work") and a *decisive observation* that a mere loss decrease cannot satisfy. Examples: "reproducible physical outcomes for different commands, not only decreasing loss or different actor outputs"; "more replay entries or a larger latent spread alone do not show capability growth." This is the right falsification posture.
2. **FB readout is stated correctly and with its limits.** The draft keeps "linear in `w_r` under a fixed policy" separate from "Q_task or success linear in z," and distinguishes exact occupancy factorization from weaker feature-moment consistency. It also notes that a motion-only B cannot supply arbitrary terrain or contact rewards. This answers the owner's "FB theory applicability bounds" question directly.
3. **Extreme-point observation.** The point that optimizing linear preferences over motion occupancy favors *exposed* parts of the achievable occupancy set is a substantive theoretical caveat. It goes beyond paraphrasing the owner and deserves to survive adjudication. It is a concrete reason why "FB covers all reusable behaviors" is false, even with perfect function approximation.
4. **The strongest objection is well chosen.** The body objective never sees task reward, so the repertoire may lack task-necessary actions, and "a planner cannot select a behavior that its actor cannot execute." This is the right first-order risk for a body/task split.
5. **Macro-K vs FB compatibility is handled cleanly.** The FB critic evaluates a counterfactual fixed-z continuation, and the macro task critic evaluates the actual K-step execution followed by switching. The draft warns that uncorrected multi-step FB targets crossing a z switch are not fixed-z targets.
6. **Drift.** "Immutable executed z labels preserve what was commanded … neither makes an old macro transition current," plus the observation that deterministic `.loc` execution removes Gaussian likelihood correction. Both are correct and non-trivial.
7. **Retention is split into readable / executable / planner-usable**, as the owner requested, and the split is carried into the experiment design.

### 2.2 Weaknesses

**W1 [MAJOR]: the verdict is ambiguous between owner categories.** The owner's allowed outcomes are *support / conditional support / substantive revision required / do not continue*, plus the output-judgment phrasing *support / revise-then-continue / small-scale-only / do-not-continue*. Draft B's headline, "substantive revision of the claims and validation strategy; revise-then-continue at small scale only," spans three categories. It also revises *claims and validation*, not the *design*, so the reader cannot tell whether Author B thinks the architecture itself needs revision. The body text says the architecture is "coherent enough to test" and proposes testing it unchanged (A-F). That is closer to **conditional support / small-scale-only**. The draft should pick exactly one category and justify it.

**W2 [MAJOR]: decisive assumptions are not enumerated.** The owner asks for the verdict "with decisive assumptions." Draft B scatters necessary conditions across the causal-chain table but never states a short list whose falsification would flip the verdict. At minimum I would expect:
- (a) the body objective (motion-only B plus 50/50 sampler) yields a repertoire that *covers* task-necessary contact behaviors at the obstacle heights;
- (b) planner-selected z remains inside the region the actor was trained on;
- (c) cold start escapes the fall-dominated regime within budget;
- (d) macro-Q calibration survives actor drift at the chosen replay age.

**W3 [MAJOR]: "why z-space may help" is under-argued, and the obvious confounder is missing.** The draft correctly rejects the dimensional-compression and inner-product-smoothness arguments. Its positive argument, though, is one sentence ("coordinated temporal exploration through a learned controller"). It never separates the two components of that hypothesis:
- *temporal correlation* of exploration, which simple action-space methods also provide (temporally correlated or colored action noise, action repeat);
- *learned behavioral structure* (z indexes physically coherent closed-loop behaviors).

Only the second is a reason to prefer this framework. Without that separation, the "simpler alternatives" section misses the most direct cheap competitor to the macro-z mechanism, and the A design inherits the gap (§4, M2).

**W4 [MAJOR]: the consequence of fully deterministic planner-mode execution is under-weighted.** The draft records the owner's fact that the planner emits z, the actor executes `.loc`, and there is no planner-z noise. It does not draw the consequence: as the charter schedule anneals toward 70% planner, the share of collection with *any* executed stochasticity falls to the expert and near share. The framework's own exploration story (owner: "real exploration expands behavioral capability") therefore rests on a shrinking channel. This is a theory-and-implementation mismatch on the central mechanism, not a footnote. It also matters for fairness in A (§4).

**W5 [MINOR]: the cold-start analysis lists both outcomes but does not say which is more likely or why.** "A benign loop is possible … a deadlock is equally possible" is symmetric hedging. The review would be stronger if it identified the specific early signal that discriminates the two. Draft B's own branch panels suggest one: by 100k steps, whether at least some commands yield reproducibly distinct non-fall outcomes from fixed starts. It should then make that signal an early-stop criterion.

**W6 [MINOR]: planner-output distribution mismatch is not discussed.** The actor and F are trained on z drawn from the sphere of radius √d_z or from B-encodings. Nothing in the reviewed design constrains planner outputs to that support, so `∇_z Q` can drive z off-manifold, where the critic is unconstrained. This is one concrete form of "planner exploits critic errors" and has a cheap mitigation (project onto the sphere or regularize toward the B-image). It should be named.

**W7 [MINOR]: negative transfer and capacity cost get one sentence.** The owner explicitly asks *why currently irrelevant experience may help later, and the negative-transfer and capacity costs*. The draft lists "capacity competition, forgetting, skewed sampling, negative transfer" but gives no mechanism. For example: finite circular replay plus non-task-filtered admission means fall-heavy early data can dominate FB updates, and the 50% random-sphere conditions spend capacity on behaviors no task may ever request.

### 2.3 Value judgment

On substance I agree that the design is worth a bounded test and not worth scaling on current evidence. The judgment is defensible, but it is stated loosely (W1, W2).

---

## 3. Critique of GAP_TABLE and CORRECTED_CONCLUSIONS (scope errors, overclaims, missed corrections)

### 3.1 GAP_TABLE

**Strengths.** The Observed / Reported / Specified / Pending labeling is the right epistemic device and is applied consistently. I spot-checked the "Observed" claims:
- The sampler in `gpu_experiments/fb_core.py` (`sample_ufo_mixed_z`) does draw current-B permuted `m_next` versus random-sphere z with `goal_ratio=0.5`.
- No `FBAgent` or `TaskLearner` class exists in the program's Python sources.

Both observations are accurate. Every row has a "minimal evidence to close," which is what makes the table usable.

**Issues.**
- **G1 [MINOR]: wording blur in the first row.** "found no production `FBAgent` … in the program's inspected Python sources" mixes "production" with "local research tree." It should say: *no class of that name exists in this research tree; production identity is unresolved.* As written, a reader could think production code was searched.
- **G2 [MAJOR]: missing row for executed stochasticity by source.** Per W4, the table should have a row giving, for each collection source (expert / near / planner), what executed randomness exists today: actor mean vs sample, and command perturbation. The current "Planner exploration" row covers only planner-z noise and omits the deterministic `.loc` actor mean as a gap on the *low-level* exploration side.
- **G3 [MINOR]: the Bernoulli 50/50 is "per sample, not exact."** The observed sampler draws `rand < 0.5` per row, so each batch's mix varies. This is harmless, but the entry-gate audit row "50/50 … update conditions" should specify the expected mixture *in distribution* so that a strict auditor does not flag batch variation as a contract violation.
- **G4 [MINOR]: no row on the evaluation/collection protocol mismatch.** A-F is evaluated 100% planner while collection mixes sources. The table should record whether the production evaluator matches this, because the A primary endpoint depends on it.
- **G5 [MINOR]: demonstration coverage is not tabulated.** The charter records a single 0.704 m obstacle demonstration. Whatever motion material actually exists is a direct input to both A-F (expert cues) and A-I (imitation prior), and its coverage should be a gap row with "Pending: hash and field inventory."

### 3.2 CORRECTED_CONCLUSIONS

**Strengths.** Every owner correction in the "Corrections to prior delivery claims" table is reflected:
- B01: no production whitening warrant.
- B02: no macro-Q, near, or cold-start proof; D4/D5 are not landed.
- B03: 0.9105 is not a physics floor; the 85.7% waste and 70% same-height sampling claims are rejected.
- B04: no acceleration, no optimal H; first-action derivatives can carry long-horizon effects.
- B05: no production integration.
- H4 is open.

The B03 analysis is a real added correction. I verified it against `gpu_experiments/run_b03_contact_aliasing_spike.py` lines 84–95:
- the targets are ±0.75;
- the predictor is trained on *different* targets (lines 66–76) and then evaluated on the ±0.75 pair without retraining;
- the equal-weight squared error is `mean(p²) + 0.5625`.

Draft B's statement is correct.

**Issues.**
- **C1 [MAJOR]: the B03 analysis stops one step short.** Because `mean(p²) + 0.5625 ≥ 0.5625 > 0.40` for *any* prediction, the B03 pass condition `irreducible_same_z_mse > 0.40` **cannot fail**. That subtest is vacuous as a check, not merely mis-scoped. Draft B quotes the 0.40 acceptance but does not say this. The correction ledger should record "unfalsifiable assertion" explicitly, because it is the strongest possible scope correction and it generalizes into a process lesson: every future local check should state the value that would make it fail.
- **C2 [MAJOR]: headline numbers in the ledger are not individually re-scoped.** The ledger still advertises the B01 "17.23x MSE reduction," the B04 cosines (`-0.0338` vs `0.3191`/`0.3871`) with "optimal rel_l2 0.949 at H=16," the B04 step throughput, and the B02/B05 GPU numbers. Draft B corrects these generically ("old cosines," "constructed distributions") but does not list each advertised number with its correct scope. The append-only reconciliation will need exactly that list, so it should be supplied now. The B04 H=0 cosine also deserves an explicit note: a near-zero cosine for the first-action FB arm is the expected symptom of the arm-definition misalignment the owner flagged. It is not evidence that FB first-action gradients are uninformative.
- **C3 [MINOR]: the B05 correction misses a carried-forward threshold.** "79/100 → 0.7002" is fine arithmetic, but MINIMAL_EXPERIMENTS reuses it as gate A2. The correction table should say the Wilson rule was *checked as a formula only*. Its suitability as a curriculum unlock or efficacy gate is untested.
- **C4 [MINOR]: B02 should name the drift-gate artifact.** The ledger says B02 adopted a "pre-clip Gaussian KL drift gate." Draft B's own FRAMEWORK_REVIEW notes that deterministic `.loc` execution makes Gaussian likelihood correction unavailable. CORRECTED_CONCLUSIONS should connect these: the KL drift gate's applicability to deterministic execution is unestablished. As it stands, the insight sits in one file and the correction is missing from the other.
- **C5 [MINOR]: H1 status could be sharper.** "Production conditioning … unmeasured" is right, but the owner also asks not to generalize to "all z whitened." H1 as written in the charter *is* a whitening-benefit hypothesis. The status should say H1 is *untested and deprioritized* for this round's mainline, not merely "unmeasured."

No overclaims found in CORRECTED_CONCLUSIONS. Its errors are omissions.

---

## 4. Critique of MINIMAL_EXPERIMENTS (thresholds, sequence, missing controls, budget realism)

### 4.1 Strengths

- An **entry integrity gate** (≤10k transitions plus fixtures) that blocks interpretation without counting as an efficacy experiment. It covers provenance, update semantics, immutability by snapshot rather than by returned flag, macro and recurrent reconstruction tolerances, failure transactions, and resume parity. This is the correct response to the owner's "B05 does not replace real production verification."
- **Statistical hygiene.** The seed is the unit of inference. The design uses paired seeds, Bonferroni intervals for the two A comparisons, no seed substitution, leave-one-out sensitivity, right-censoring for time-to-threshold, invalid runs retained, and capped setup tuning per arm with no post-hoc enlargement.
- **Cost accounting rules.** Attempted transitions include warm-up, pretraining, failures, and invalid attempts. Evaluation and tuning are counted separately. Sample efficiency and wall-clock efficiency are reported as a tradeoff.
- **C as an intervention on a common donor pool.** This removes collection confounds and task-critic carryover, and the design explicitly measures all three retention meanings. Freezing the low-return label definition and the ineligibility rule (L < 10% → no cutoff search) is good practice.
- **Interaction arithmetic is internally consistent.** I recomputed the training cap (15 × 1M = 15M), the evaluation cap (per run: 10 × 4 × 20 + 2 × 4 × 100 = 1,600 episodes × 1,000 steps = 1.6M; × 15 = 24M), the branch panels (8 × 8 × 100 × 3 × 5 = 96,000), and the C caps. All match.

### 4.2 Problems

**E1 [CRITICAL]: the A budget is very likely too small to be decisive, which makes the A→C sequence likely to stop with no information.** A caps each run at **1,000,000 aggregate attempted control transitions across all parallel environments**, and gate A2 requires **≥79/100 success at both training heights in both final panels for 4 of 5 seeds**. That is a high absolute-competence bar for 29-DoF obstacle traversal learned from scratch. One million aggregate transitions is a small budget for that class of problem. The B05 checks themselves assumed thousand-environment batches (4,096-env quota). At that width, 1M transitions is a few hundred control steps per environment, and each training episode can last up to 1,000 steps.

The draft does pre-declare "if all arms fail, the result is unresolved," which is honest. But combined with "C only if A passes," the most probable outcome of the full plan is *no efficacy information and no reuse information*.

Required fix:
- (i) justify the 1M budget from measured or literature-typical learning curves for this plant class, or make the budget a pre-registered function of measured entry-gate throughput with a stated rationale;
- (ii) separate the *efficiency* gate (A1, AUC) from the *absolute competence* gate (A2), so a framework that is clearly more efficient but not yet at 0.70 by 1M is not discarded as "failed";
- (iii) see E4 on decoupling C.

**E2 [MAJOR]: the A comparison is asymmetric in exploration, in the direction that disadvantages the framework.** A-F is frozen as "deterministic planner/actor-mean execution as reported, no added planner-z noise," while A-D gets "normal executed-action exploration." This tests the framework in a configuration known to lack one of its intended mechanisms (W4) against a baseline that has its standard one. Fidelity to the audited production state is the right *default*. But a negative A-F result would then be confounded between "the architecture does not help" and "the current collector under-explores." Two options:
- Add a pre-declared A-F′ variant with a minimal, fixed executed exploration (for example a small actor-sample or planner-z perturbation, chosen in the setup budget, not tuned on test seeds). This makes A a three-way family comparison and needs the Bonferroni correction adjusted.
- Or state up front that an A-F failure cannot discriminate the two explanations, and route that outcome to a targeted B-type check rather than to "revise the body/task design."

**E3 [MAJOR]: a temporal-exploration control is missing.** The owner's hypothesis is that macro-steps holding z give *more coherent exploration than independent joint noise*. A-D with "normal" (presumably i.i.d.) action noise does not isolate learned behavioral structure from mere temporal correlation. At minimum, the A-D arm definition should specify its noise process and include temporally correlated action noise as one of the two setup configurations it may select. Ideally the branch panels should include a correlated-noise direct-action probe from the same starts, so that "z-commands produce more distinct useful outcomes than correlated action noise of matched magnitude" becomes a measurable diagnostic.

**E4 [MAJOR]: gating C on A superiority conflates two independent claims.** C asks whether low-current-return experience trained into the body later serves a different task. That question is meaningful whenever the body controller has *nontrivial controllability*, whether or not the framework beats two baselines on U efficiency. The owner lists cross-behavior/task reuse as a co-priority. Proposed gate for C: entry integrity passes, and A-F branch panels show reproducible command-conditioned non-fall outcomes, and A-F reaches some pre-declared minimal U competence (for example a Wilson lower bound ≥ 0.30 at 0.10 m). The A1 efficiency result should stay a separate claim.

**E5 [MAJOR]: C lacks a size-matched control and a positive control.**
- *Size-matched control.* C-use vs C-omit changes both "L present" and "pool diversity/size." Add **C-rand**: omit a random non-L subset of the same transition count as L, rebuilt identically. Then C-use > C-omit ≈ C-rand supports value specific to low-return data. C-use ≈ C-rand > C-omit supports a generic data-quantity effect. The latter is still a reuse result, but a different one.
- *Positive control.* 10,000 offline updates on a frozen pool may be too few to move a body controller measurably. Add a small **C-pos** branch that enriches with V-relevant data (for example transitions from scripted disturbance episodes collected inside the donor budget), to show the pipeline *can* detect a body-side effect on V. Without it, a null C cannot be distinguished from an insensitive protocol.

**E6 [MAJOR]: the statistical power at five seeds is not stated, and the effective threshold is far above 0.05.** With 5 paired seeds, the 97.5% two-sided t quantile (4 df) is ≈ 3.495. Requiring the lower bound to exceed zero therefore needs a mean improvement above `3.495·s/√5`. That is ≈ 0.078 if the seed-level SD of the AUC difference is 0.05, and ≈ 0.156 if it is 0.10. The "≥ 0.05" threshold is not the operative one. The plan should state an assumed seed SD, the implied minimum detectable effect, and either accept that or raise the seed count. The same applies to the severe-penetration gate A3.

**E7 [MINOR]: the secondary time-to-threshold criterion is inconsistent with the primary gate.** Intermediate panels have 20 episodes. A 95% Wilson lower bound ≥ 0.70 at n=20 requires 19/20 (LB ≈ 0.764; 18/20 gives ≈ 0.699). That means 95% observed success on two consecutive intermediate panels, a much stricter bar than the final 79/100. Either raise intermediate panel size for this secondary metric or define the threshold on the AUC curve.

**E8 [MINOR]: V task selection is favorable to L.** L consists of the worst unsuccessful U episodes, which are plausibly falls. V is recovery after lateral disturbance. The pairing is pre-declared, which is good, but it is the most favorable pairing for "low-return data helps." The conclusion text should say so: a pass establishes reuse for a *matched* failure-to-recovery transfer, not generic cross-task reuse. A second, less aligned V (for example a different obstacle approach) would be a stronger claim but can be deferred.

**E9 [MINOR]: the C retention check uses the original U planner on a modified body.** This intentionally tests planner–body compatibility, as the draft notes. A U drop could then be planner miscalibration rather than body forgetting. Report the executable-behavior panel on U starts alongside it, so the two can be separated.

**E10 [MAJOR]: budget realism in compute terms is absent.** Interaction caps are carefully enumerated (≈ 15.3M + 24M evaluation for A; ≈ 5M + 4M evaluation for C). There is no accelerator-hour, wall-clock, or memory estimate, not even a range conditional on assumed throughput. Evaluation alone (24M transitions) exceeds training for A, which is a budget-shape choice that should be justified. The owner's deliverable 5 asks for costs. A "fill in after the entry audit" placeholder is acceptable only alongside a back-of-envelope range, so the owner can decide whether to fund the round.

**E11 [MINOR]: no early-termination rule.** No futility rule is pre-declared, for example stopping an A-F seed whose 300k-step branch panels show zero command-conditioned controllability. A deadlocked run will otherwise consume its whole budget. Futility stops do not bias efficacy claims if the rule is pre-registered and stopped runs keep their observed AUC (zero after the stop).

---

## 5. Agreement and disagreement with Draft B headline judgment

**Agree.**
- The B01–B05 process is complete and framework validation is not. Script PASS ≠ framework works.
- The design is coherent enough to warrant a *bounded* real-training test and not enough to justify scaling or bundled add-ons (whitening, same-height relabel, B-input expansion, world-model losses).
- The strongest objection is objective sufficiency of a task-blind body objective. The most promising benefit is that every valid transition trains a reusable body controller regardless of task return.
- Near is one ablation, beyond-demo success is an outcome metric, and world-model acceleration is a separate track.
- A (efficiency vs imitation-assisted and direct-action baselines) is the right *first* question, and a full B sweep should not run alongside it.

**Disagree or qualify.**
1. **Verdict category.** I would label it **conditional support (small-scale only)**, conditional on the decisive assumptions in W2. "Substantive revision" should be reserved for the claims ledger, which does need it. Draft B's own A-F tests the architecture unchanged, which is inconsistent with a "substantive revision of the design" reading.
2. **The sequence is too strict.** "C only if A passes" combined with a likely-insufficient 1M budget and a 0.70 absolute gate makes it probable the round yields nothing (E1, E4). I would gate C on demonstrated controllability, not on A superiority.
3. **Exploration is not safely deferrable in its entirety.** Deferring the *full* near / planner-noise / K sweep is right. But the framework is tested with its central exploration channel partly disabled (deterministic planner execution), and there is no temporal-correlation control. So a minimal exploration-fidelity element (E2, E3) belongs *inside* A. Otherwise an A failure is uninterpretable on the owner's top-priority question ("temporally structured conditional exploration").
4. **Severity of the B03 correction.** It should be stated as "the subtest was unfalsifiable," not only "mis-scoped" (C1).

---

## 6. Mandatory fixes before adjudication

- **[CRITICAL] F1 — Make A capable of yielding information.** Justify the 1M-transition per-run budget for this plant class, or tie it to measured throughput with a stated rationale. Separate the efficiency gate (A1) from the absolute-competence gate (A2), so efficiency can be established, or refuted, without requiring 0.70 Wilson success by 1M. State the minimum detectable AUC effect at five seeds under an assumed seed SD (E1, E6).
- **[MAJOR] M1 — One verdict category plus enumerated decisive assumptions.** Replace the compound verdict with exactly one owner category. List 3–5 decisive assumptions whose failure would change it (W1, W2).
- **[MAJOR] M2 — Exploration fidelity and a temporal-correlation control inside A.** Either add a pre-declared minimal-executed-exploration A-F′ variant, or state that an A-F failure cannot be attributed to the architecture. Specify A-D's noise process and allow temporally correlated action noise as a declared setup configuration. Add a correlated-noise direct-action probe to the branch panels (E2, E3, W3, W4).
- **[MAJOR] M3 — Decouple C from A superiority, and add the C-rand and C-pos controls.** Gate C on integrity plus demonstrated command-conditioned controllability plus a minimal U competence level. Add a size-matched random-omission branch and a positive-control enrichment branch, and adjust the C budget accordingly (E4, E5).
- **[MAJOR] M4 — Cost ranges.** Provide order-of-magnitude accelerator-hour, wall-clock, and memory ranges for A and C under stated throughput assumptions, and justify evaluation transitions exceeding training transitions in A (E10; owner deliverable 5).
- **[MAJOR] M5 — Complete the scope corrections.** Mark the B03 `> 0.40` subtest as an unfalsifiable assertion. Add a per-number re-scoping list for every headline figure the ledger advertises (B01 17.23x / 11.34x; B02 drift and burn-in numbers; B03 0.9105 / 6.80e-4; B04 cosines, rel-l2, steps/s; B05 Wilson and quota results) (C1, C2).
- **[MAJOR] M6 — GAP_TABLE row on executed stochasticity by collection source,** including deterministic `.loc` actor execution as a low-level exploration gap (G2).
- **[MINOR] m1** — Connect B02's Gaussian KL drift gate to the deterministic-execution caveat in CORRECTED_CONCLUSIONS (C4). Re-label H1 as untested and deprioritized (C5). Note that the Wilson rule was formula-checked only (C3).
- **[MINOR] m2** — Fix the time-to-threshold inconsistency at n=20 panels (E7). Add a pre-registered futility stop (E11).
- **[MINOR] m3** — Say explicitly that V is the most favorable transfer target for L and limit the C claim accordingly. Report body-execution panels on U starts next to the U retention result (E8, E9).
- **[MINOR] m4** — Name planner-output off-support risk and a mitigation (W6). Give a mechanism-level account of negative transfer and capacity cost (W7). Name a discriminating early cold-start signal (W5).
- **[MINOR] m5** — GAP_TABLE wording: "no such class in this research tree; production identity unresolved" (G1). Specify the in-distribution 50/50 expectation (G3). Add rows for the evaluation/collection protocol and for demonstration coverage (G4, G5).

**Recommendation: revise-then-adjudicate.**
