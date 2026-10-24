# Merged Minimal Decisive Experiment Plan — feedback-round-2026-10-24

**Status: PRE-REGISTRATION DRAFT. Nothing here has been run.** All training is a planned external step on the production home-humanoid traversal chain outside `/srv/claude`. Only summaries return to this tree (§9).

**Structure:**
- **Base:** draft B's protocol (entry gate, AUC endpoint, seed and inference rules, causal C).
- **Merged from draft A:** DA-C, the E0 controllability probe (repaired), and the Z2 planner-z diagnostic.
- **Fixes applied:** MX-1…MX-12 from `DISPOSITION.md`.
- **Priority:** A first (Stages 1→2). C next, gated on controllability and not on A superiority. B (the full z-exploration / near study) stays deferred except for one conditional, capped diagnostic (Z2).

**Fixed semantics in every framework arm:**
- standard expert/near current-B encoding;
- UFO `z_update` 50/50;
- `F·z` actor readout;
- motion-only B;
- K = 10.

The following are never added:
- whitening;
- same-height relabel;
- world-model loss;
- B-input expansion;
- a task gradient into the body actor.

**Units:**
- **transition** = one control step of one environment instance, aggregated over all parallel environments.
- **vector step** = N transitions.

All caps are in transitions and count every attempted transition, including warm-up, failures, invalid attempts and rolled-back steps.

---

## 1. Stage 0 — Entry Integrity Gate (MX-2, both adjudications)

**Scope and budget:**
- ≤10,000 attempted control transitions, plus targeted fixtures, plus a throughput benchmark of ≤100,000 transitions per arm type.
- This is an engineering gate, not an efficacy experiment.
- **Any failed assertion blocks every later stage** until it is repaired and the protocol version increments.

| # | Audit | Pass condition | Gap rows |
|---|---|---|---|
| E-1 | Identity | Revision + patch digest; collector, env step, replay writers, `FBAgent.update`, `TaskLearner`, evaluator and resume entrypoints are named in the manifest. Unresolved entries are launch blockers. | G01 |
| E-2 | Three data paths | Zero offline cue records in transition replay. Valid low-return and credible-failure rows are present in FB replay. Task rows hold actual history, z_actual, return and elapsed k. | G02 |
| E-3 | Update semantics | No task-reward read in the FB update. Sampled-condition fraction is 0.50 ± 0.02 over ≥10⁴ draws. Task learner consumes macro returns. | G05, G06 |
| E-4 | Immutability (snapshot diff, not returned flags) | Zero executed-z mutations after repeated FB updates. Zero normalizer change from cue queries and from evaluation. Statistics update counts equal the specified real-data updates. | G07, G08, G27 |
| E-5 | Macro targets | Full and shortened macro returns and discounts reconstructed independently, within 1e-6 absolute error. Termination is distinguished from time-limit truncation. | G16 |
| E-6 | Recurrent prefix | Recomputed outputs within 1e-5 on finite normalized fixtures; precision documented | G21 |
| E-7 | Failure transaction (R2.1) | A finite >0.03 m penetration is committed with terminal semantics and Φ_next = 0. Verified NaN/overflow later in the same step overrides it before any replay/statistics commit. Vector abort and reservation release are checked on actual mutable state. | G25 |
| E-8 | Evaluation and resume | An invalid evaluation halts and is marked invalid. Replay and normalizer hashes are unchanged across an evaluation panel. Resume from checkpoint (replay, optimizer, random streams) matches an uninterrupted short reference. | G27 |
| E-9 | Telemetry present | Executed-z source tags; command before/after perturbation; actor mean; applied action after clipping; separate RNG stream identities; planner-z knob **present and off**; ‖z‖ / off-support log | G12, G13, G14, G18 |
| E-10 | Units and curriculum audit | Source-ramp unit resolved (vector steps vs transitions); two-panel unlock and quota conservation observed in logs | G17, G28 |
| E-11 | Throughput freeze | Measured transitions/s per arm. Stage caps = min(anchor, approved hours × measured throughput). Frozen in the manifest. If the shrink exceeds 2× → back to the owner. | G30 |

---

## 2. Shared statistical rules

- **Seeds.**
  - Setup seed: 24000 (non-test).
  - Test seeds: 24001–24005.
  - Pre-declared extension seeds: 24006–24010 (§4.4).
  - Training environment randomization streams are paired across arms. Evaluation randomness is independent of training and shared across arms.
- **Unit of inference.** The **seed**: never an episode, branch or checkpoint. Every seed value, every paired difference and a leave-one-seed-out sensitivity analysis are published. Bootstraps resample seeds.
- **Confirmatory family for A.** Two comparisons, A-F vs best-DA and A-F vs A-I. Each uses a two-sided **97.5%** paired Student-t interval (Bonferroni ≥95% family coverage).
  - The other DA arm is reported descriptively with an interval of the same width.
  - C uses a two-sided 95% paired interval.
- **Critical effect and power at 5 seeds** (t₄,₀.₉₈₇₅ = 3.495).
  - The smallest observed mean difference with lower bound > 0 is 3.495·s/√5 = **1.563 s**: 0.078 if the seed SD of the paired AUC difference is s = 0.05, and 0.156 if s = 0.10.
  - The approximate 80%-power MDE is ≈ 1.98 s.
  - At 10 seeds (t₉,₀.₉₈₇₅ = 2.685): critical effect 0.849 s (0.042 / 0.085); approximate 80% MDE ≈ 1.13 s.
- **Endpoint (MX-1).**
  - **Primary:** normalized trapezoidal area under the success-vs-training-transitions curve on [0, stage cap], in [0,1]. It is averaged equally over the two training heights. The final point pools both final panels.
  - **Secondary, censor-aware:** T70. A seed's T70 is the first checkpoint at which **two consecutive intermediate panels pooled (n = 40 per height) reach ≥34/40** (Wilson LB95 ≥ 0.70) at both training heights, confirmed by the final 100-episode panels when it occurs at the end.
    - Non-attainment is right-censored. Report per-arm attainment counts and Kaplan–Meier curves.
    - **No fabricated threshold time is ever used.**
    - A median ratio is reported only when ≥4/5 seeds attain in both arms.
    - **Both arms fail to attain → `INCONCLUSIVE`, never ratio 1** (MX-12 fixes the n = 20 Wilson inconsistency, since a single 20-episode panel needs 19/20).
- **Wilson reference values (LB95, verified):**
  - 79/100 → 0.7002 (78/100 → 0.689);
  - 39/100 → 0.3002;
  - 16/100 → 0.101;
  - 34/40 → 0.709;
  - 19/20 → 0.764.
- **Setup and tuning fairness.**
  - Per arm: ≤2 declared configurations × 1 setup seed × ≤1.5M transitions.
  - Selection by setup AUC on 5 small panels (20 episodes × 2 training heights).
  - Frozen before any test seed.
  - **best-DA** = whichever of A-D or A-DC has the higher setup AUC; a tie goes to A-DC, the stronger null.
  - No later re-tuning, seed substitution or favorable-checkpoint selection.
- **One confirmatory look.** The A verdict is computed once, at the end of the last stage actually run. A Stage-1 analysis is an interim go/no-go report, unless the owner declines Stage 2; in that case the identical rules applied at Stage 1 become the confirmatory result, scoped to the 15M budget.

---

## 3. Fault protocol (Charter §2.4; MX-2 replaces draft A's auto-restart and exclusion)

1. A **credible physical failure**, including finite `severe_penetration` > 0.03 m, is committed experience. It is never a fault and is never removed.
2. A **verified `invalid`** event halts the affected run or evaluation panel immediately. Artifacts are frozen.
3. An **inspection record** assigns a root-cause class:
   - (a) transient backend fault, no code change;
   - (b) implementation defect;
   - (c) unresolved.
4. A **documented disposition** follows from the class:
   - (a) resume from the last verified-clean checkpoint with the identical seed stream;
   - (b) bump the protocol version; rerun every arm that shares the defective code, under new run identities, and keep the failed artifacts;
   - (c) the seed is recorded as `invalid-unresolved`.
5. **Accounting:**
   - Every scheduled seed stays in the reliability table.
   - Rolled-back and repeated transitions are charged to cost.
   - In the primary analysis, an `invalid-unresolved` seed contributes its observed AUC up to the halt and zero thereafter, which is conservative. A sensitivity analysis excluding it is reported.
   - **Any arm with ≥2 `invalid-unresolved` seeds makes every comparison involving that arm `INCONCLUSIVE`.** Exclusion is not used.
6. Scientific non-attainment, implementation failure and unresolved invalidity are reported as three separate categories.

---

## 4. Check A — task-learning efficiency (Stages 1 and 2)

### 4.1 Task and evaluation

- **Task.** Intended home-humanoid plant-class obstacle traversal.
  - Training heights are **fixed**, equally split between 0.10 m and 0.20 m. There is no curriculum, which removes curriculum exposure as a confound; the curriculum is audited at Stage 0 only.
  - Held-out heights 0.15 m and 0.25 m are secondary only.
  - Timeout is 1,000 control steps.
  - Reward, termination, resets and success detector are identical across arms.
  - Privileged critic inputs, if any, are matched across arms and recorded.
- **Stage-1 evaluation schedule (cap 15M):**
  - Intermediate panels every 1.5M transitions (10 panels): 20 episodes × 4 heights.
  - Final panels: two independent 100-episode panels per height, frozen weights.
  - Evaluation is capped at ≤1.6M transitions per run (≤10.7% of training).
  - A-F evaluation is 100% planner, with frozen statistics and zero replay writes.
- **Stage-2 evaluation (cap 100M):** additional intermediate panels every 10M, plus a new final pair. ≤1.6M additional transitions per run.

### 4.2 Arms (4 × 5 test seeds)

| Arm | Frozen definition |
|---|---|
| **A-F** framework | Audited FB + conditional actor + macro task Q/planner with the existing expert/near/planner source schedule. Execution is deterministic (planner mean, actor `.loc`), as reported. The planner-z knob is present but **off**. This tests the *as-implemented* configuration. |
| **A-D** direct-action | Off-policy twin-critic task RL from scratch. Same deployable observations plus a recurrent history encoder of planner-matched size, same actuator limits and control rate, per-step independent Gaussian exploration. |
| **A-DC** temporal null | A-D with held or OU action noise over K = 10 steps at matched marginal action variance. The process (held or OU) is declared at setup. |
| **A-I** imitation comparator | Direct-action policy that uses the same motion material as a motion-imitation prior plus task reward. Pose/velocity data do not supply action labels.<br>• Reference phase: nearest-frame phase by root-relative pose.<br>• Recovery: the imitation term is gated off after a fall is detected, so task reward drives recovery.<br>• Task adaptation is allowed.<br>Charter §2.1 binds A-F only. |

**Information asymmetry, labelled:** A-F and A-I see the demonstration; A-D and A-DC do not. Gains of A-F over A-D/A-DC measure demo cues + hierarchy + relabeling jointly. A-F vs A-I compares cue-based hierarchy against an imitation prior under equal demo access.

**Descriptive branch panels:**
- At 0 / 50% / 100% of each stage, for A-F: 8 saved starts × 8 commands (planner, expert, near, random-sphere, repeated-command control) × 3 repeats × ≤100 steps.
- The same structure for **best-DA with correlated-noise action draws**, which is the matched direct-action probe.
- Panels never enter replay. Terminated branches are absorbing and stay in denominators.
- They feed the D4 bounded command-search diagnostic (G19).

### 4.3 Gates

| Gate | Rule |
|---|---|
| **A1 efficiency** (vs each confirmatory comparator) | Mean paired AUC difference ≥ 0.05 **and** 97.5% lower bound > 0 |
| **A2 absolute competence** (reported; gates only "deployment-grade" language, **not** C) | ≥4/5 seeds with ≥79/100 at both training heights in both final panels |
| **A3 safety** | Simultaneous upper bound of the paired difference (A-F minus comparator) in final severe-penetration rate ≤ 0.05. If violated, SUPPORTED is downgraded to "efficiency with safety cost". |
| **A4 integrity** | Stage 0 passed; no arm has ≥2 `invalid-unresolved` seeds |
| Investment hurdle (draft A; reported only) | median T70 ratio A-F/best-DA ≤ 0.67, when identifiable (§2). Not a falsification criterion. |
| Compute ratio (reported) | Accelerator-hour ratio A-F/best-DA. If > 3, the claim is phrased "interaction-efficient, compute-expensive". |

### 4.4 Stage logic and verdicts

**Stage 1 → Stage 2:**
- **L-gate (learning signal):** ≥1 arm has ≥3/5 seeds with ≥16/100 at 0.10 m in the pooled final panel (Wilson LB ≥ 0.10), **or** A-F passes E0 (§5).
- L-gate fails → **stop** and report "task/budget adequacy unresolved". Owner decision. No framework conclusion.
- L-gate passes → Stage 2 subject to owner spend approval.
- If Z2 was triggered and passed (§6), the revised framework replaces A-F in Stage 2, and **all arms restart on fresh seeds 24006–24010**. Under the revision, this is a different configuration from the one tested at Stage 1.

**Stage-2 seed count:**
- Fixed **before any Stage-2 outcome** from the Stage-1 paired-AUC SD s₁ (A-F minus best-DA).
- If s₁ ≤ 0.064, so that the 5-seed critical effect is ≤ 0.10 → 5 seeds.
- Otherwise → 10 seeds (adds 24006–24010).
- Assumption: Stage-1 variance approximates Stage-2 variance. This is the single allowed extension.

**Futility (symmetric, Stage 2 only, pre-registered):**
- A seed with zero successes at both training heights in every panel up to 50M stops.
- Its AUC records zero for the remainder.
- Sensitivity analysis without the stop is reported.

**Confirmatory A verdict** (final stage reached):

| Verdict | Rule |
|---|---|
| `SUPPORTED` | A1 passes vs both comparators, and A3 and A4 hold |
| `PARTIAL` | A1 passes vs exactly one comparator |
| `BASELINE-WINS` | A comparator − A-F ≥ 0.05 with 97.5% LB > 0 |
| `NO-ADVANTAGE` | Both 97.5% intervals lie within (−0.05, +0.05) |
| `INCONCLUSIVE` | Otherwise, including A4 failure or both-fail (all compared arms with mean final success < 0.10 at 0.10 m) |

**Interpretation map:**
- `BASELINE-WINS` with the comparator meeting A2 and E0 FAIL → substantive architectural revision (DISPOSITION §1).
- `NO-ADVANTAGE` / `INCONCLUSIVE` with E0 PASS → small-scale-only; C remains eligible.
- An all-arms failure is unresolved task/budget adequacy, never evidence against the framework.

### 4.5 Secondary diagnostics (non-gating, MX-11)

- **Q-calibration.**
  - Target: realized discounted macro return to episode end (0 at termination), with bootstrap from the target critic only at time-limit truncation, under the logging planner.
  - Report slope, intercept and RMSE by replay-age bin.
- **Actor drift.** Action-space RMS between the current actor mean and the actor mean lagged by 1M transitions, on a frozen probe set of 4,096 states. This replaces the Gaussian KL under `.loc` execution. Physical branch comparison under old and current actors is also reported.
- **Executed-z telemetry.** Angular dispersion by source; fraction of off-support planner z (G18).
- **Beyond-demo outcome.** Held-out heights 0.15 m and 0.25 m; frequency of contact modes absent from the demo, using a predeclared support-distance definition, reported for A-F vs A-I.
- **Information only.** Production B Gram κ and effective rank.

---

## 5. E0 — controllability probe (diagnostic + launch gate; MX-3)

### 5.1 Procedure

- **Checkpoints:** A-F at 25%, 50% and 100% of each stage cap.
- **Starts:** N = 256 valid upright starts per seed from recent FB replay. Simulator state is fully restorable (verified at Stage 0). History is re-rolled for 20 steps under the logged actor before branching. This upright stratum does not stand for recovery from failed states.
- **Goal pools:** both are always reported.
  - (a) demo frames;
  - (b) held-out replay next-frames.
- **Branches:** matched z = B(m_g) and mismatched z = B(m_other), with m_other a permutation within the same pool. Distances are recorded at k = 10 and k = 50 in one 50-step rollout.

### 5.2 Frozen metric (not B, to avoid self-reference)

- **Features:**
  - joint positions;
  - joint velocities;
  - root height;
  - gravity vector in the base frame;
  - root linear and angular velocity.
- Each feature is standardized by the replay-pool SD, frozen at Stage 0.
- d = RMS of standardized differences.
- **Progress-adjusted CR** = E[d_k | matched] / E[d_k | mismatched] on the same starts. Initial distance d₀ is also reported.
- Terminated branches keep their terminal-state distance and count as falls. They are never dropped.

### 5.3 Repeatable non-fall branching (RB)

- On the branch panels, compare:
  - between-command endpoint dispersion among non-fall branches;
  - within-command dispersion across the 3 repeats with different simulator noise seeds.
- RB holds if that ratio is ≥ 1.5 **and** the non-fall fraction is ≥ 0.5.

### 5.4 Outcomes

Seed-level bootstrap, 10,000 resamples of seeds.

| Outcome | Rule |
|---|---|
| `PASS` | At the 50% checkpoint, ≥4/5 seeds have CR(k = 10) ≤ 0.80 in **either** goal pool (pool reported) with bootstrap upper bound ≤ 0.90, **or** ≥4/5 seeds satisfy RB |
| `FAIL` | In ≥3/5 seeds, CR ≥ 0.95 in both pools at both horizons **and** RB fails |
| `INCONCLUSIVE` | Otherwise |

**Deadlock flag** (single Boolean, MX-12):
- Flag = CR(k = 10) ≥ 0.95 in both pools at 25% **AND** (planner-source macro return − uniform-random-z macro return ≤ 0 **OR** the upright fraction of FB replay is non-increasing over the first 25%).
- Diagnostic only.

**Authority:**
- E0 gates Stage 2 (via the L-gate), C, and the Z2 trigger.
- **E0 FAIL alone never rejects the framework.** It triggers Z2.

**Cost:** ≈70k transitions per seed-checkpoint, so ≤1.4M per stage including the best-DA probes.

---

## 6. Z2 — capped planner-z exploration diagnostic (conditional; MX-4, routing option)

- **Trigger** (evaluated at the end of Stage 1), either of:
  - E0 FAIL or INCONCLUSIVE for A-F;
  - A-F Stage-1 interim A1 not met vs best-DA **and** planner-source executed-z angular dispersion < 0.5× the dispersion of expert+near cue z over the last 20% of Stage 1.
- **Arm:** A-F with the planner-z knob on. Tangent noise θ ~ U[5°, 15°] on the planner mean, held for the macro, planner source only. Nothing else changes.
- **Size:** 5 seeds (24001–24005, paired with Stage 1) × 15M; evaluation ≤1.6M per run; E0 at 25% / 50% / 100%.
- **Outcomes:**
  - Z2 E0 PASS → the revised framework enters Stage 2 on fresh seeds (§4.4).
  - Z2 E0 FAIL → D1 escalation: substantive architectural revision. If `BASELINE-WINS` also holds later, or already holds at the interim → stop this configuration (DISPOSITION §1).
- Z2 is **one** capped diagnostic, not the E2 sweep. Its result is scoped to "planner-z tangent noise at this magnitude".

---

## 7. Check C — does low-current-return experience cause later utility? (MX-5)

### 7.1 Launch gate (independent of A1)

All of the following must hold:
- Stage 0 PASS;
- E0 PASS on A-F (or on the Z2-revised framework);
- A-F ≥3/5 seeds with ≥39/100 at 0.10 m in the final panel of the last stage run (Wilson LB ≥ 0.30).

### 7.2 Tasks (frozen before donor collection)

- **U:** source obstacle traversal.
- **V:** recovery to upright stability after a fixed distribution of lateral landing disturbances.
  - Success = no fall and no credible severe penetration, plus upright stability for the final 100 of 1,000 control steps.
  - Tolerances (upright angle, base height, velocity) are taken from the plant's existing balance definitions.
  - If there is no testable balance definition, C is not launch-ready.
- **V is the most favorable transfer target for fall-dominated low-return data.** Any positive C claim is scoped to **failure-to-recovery reuse** unless it is replicated on a second target (deferred).

### 7.3 Donor pool and branches

**Donor pool:**
- Per seed, the final A-F checkpoint of the last stage is frozen.
- It collects ≤500,000 U transitions with its declared source schedule.
- ≤50,000 of these are a **C-pos pool P**: scripted V-distribution disturbance episodes under the same frozen checkpoint. P is excluded from every other branch.

**L definition:**
- Among valid non-P episodes, L = unsuccessful episodes with return ≤ the 25th percentile of unsuccessful episodes.
- Labels are assigned once, before any branch training. Invalid records stay excluded.
- **Eligibility:** 10% ≤ |L| ≤ 45% of valid non-P transitions. Otherwise the seed is ineligible, and **no alternative cutoffs are searched**.

**R and S:**
- R = a random, size-matched set of non-L valid episodes (episode-level, length-matched).
- Common base pool S = valid non-P transitions \ (L ∪ R).

**Branches:**
- Each branch runs 10,000 FB/actor updates at batch size 256.
- All branches share initial weights, optimizer state, update RNG schedule, the 50/50 condition sampler and frozen normalizer statistics.
- Task Q/planner do not train during the intervention.
- A pool excluded from a branch is excluded from **every** input in that branch: transitions and permuted next-motion conditions. Sampled IDs are hashed and logged.

| Branch | Sampling |
|---|---|
| **C-use** | 25% L, 75% S |
| **C-omit** | 100% S |
| **C-rand** (specificity control) | 25% R, 75% S |
| **C-pos** (sensitivity control) | 25% P, 75% S |

### 7.4 Transfer and retention

**Transfer:**
- Freeze each branch body.
- Train a **fresh** V task Q/planner for ≤250,000 transitions per branch, with paired initialization.
- No carry-over of U task replay, critic, planner or hidden states.
- V evaluation: 20 episodes at 0 / 50k / … / 200k, plus 100 episodes at 250k.
- **Primary endpoint:** V success AUC.

**Retention in three senses** (measured separately):
1. **Readable.** L admission, sampling and eviction traces. The donor pool is removed before V training, and the orchestrator verifies that no branch reads it.
2. **Executable.** Before/after body panel: 8 starts × 8 commands × 100 steps. Raw prompt frames are re-encoded with each branch's current B; fixed numeric commands are also run. Useful recoveries are counted, not mere divergence. Body-execution panels on U starts are reported next to the U retention result.
3. **Findable / planner use.** Fresh-planner V learning curves on the frozen bodies.

### 7.5 Verdict

| Claim | Rule |
|---|---|
| **Protocol sensitive** (precondition for interpreting a null) | C-pos − C-omit V-AUC 95% LB > 0 |
| **C passes** (low-return data adds later utility) | C-use − C-omit mean V-AUC ≥ 0.05, 95% LB > 0, **and** U retention non-inferiority: 95% LB of C-use − C-omit on U success ≥ −0.05 (100 episodes per training height, original U planner) |
| **L-specific** (stronger claim) | C passes **and** C-use − C-rand 95% LB > 0. Otherwise the claim is "added donor data helps; not specific to low-return experience". |
| **Null** | Not protocol-sensitive → "protocol insensitive", with no conclusion. Sensitive but C fails → a null limited to this U→V pair and budget. |
| **Negative** | C-omit − C-use ≥ 0.05 with 95% LB > 0. This supports filtering/sampling or capacity research, **not** deletion of credible physical failures. |

**C caps:**
- donor ≤2.5M;
- offline updates ≤200k (4 branches × 5 seeds × 10k);
- V training ≤5M;
- V evaluation ≤4M;
- U evaluation ≤4M;
- body panels ≤0.26M.

---

## 8. Cost ceilings (MX-10; assumptions to be replaced by E-11)

**Assumptions:**
- Training throughput is 2k–20k transitions/s per accelerator for the off-policy arms with recurrent updates. The B04 toy figure of 414,771 steps/s must **not** be used.
- Evaluation throughput is 20k–200k transitions/s.
- Overhead factor ×1.5.
- Peak host memory per run is ~2–20 GB for FB replay of 1–5M transitions at roughly 2–4 KB per transition (motion frames, observation, action, history pointers). Accelerator memory follows the network sizes; record it at Stage 0.

| Stage | Training / donor transitions | Evaluation + probes | Accelerator-hours (range) | Wall-clock with 8 accelerators in parallel |
|---|---|---|---|---|
| S0 | ≤0.41M | fixtures | ≤8 | ≤1 day including engineering |
| S1 | ≤312M (300M test + 12M setup) | ≤34M + ≤1.4M | ~6–70 | ~1–9 h compute |
| S1-Z2 (conditional) | ≤75M | ≤8M + ≤0.5M | ~2–17 | ~0.3–2 h |
| S2 (5 seeds / 10 seeds) | +1.70B / +3.70B | ≤32M / ≤64M | ~35–350 / ~75–770 | ~4–44 h / ~9–96 h |
| S3 C | ≤7.5M + 200k updates | ≤8.3M | ~1–5 | <1 h |

**Evaluation share:** evaluation is ≤11% of training at Stage 1 and ≤2% at Stage 2. This replaces draft B's 24M evaluation vs 15M training.

**Comparison with the drafts:** draft A's design ran to ~8.22B before C. The staged ceiling here is ≤0.4B before the Stage-2 decision.

---

## 9. External evidence bundle (planned external; return path inside this tree)

**Immutable manifest per run:**
- revision + patch digest;
- entrypoint identities;
- config hash;
- plant model and physics build;
- observation/action schemas and units;
- demo hash and field inventory;
- train / evaluation / reset split identities;
- seed streams;
- source schedule (with resolved units);
- K, discounts and normalizer rules;
- replay capacities and age/height eligibility;
- loss weights and update ratios;
- network sizes;
- hardware allocation;
- frozen caps and hour ceilings;
- protocol version.

Unresolved entries are launch blockers.

**Per seed:**
- per-checkpoint panel rows: (stage, transitions, height, successes / n, Wilson LB, severe-penetration count, invalid count, return mean);
- E0 and branch-panel outputs;
- Q-calibration bins and drift metric;
- executed-z telemetry;
- counters for attempted / accepted / rolled-back / evaluation / probe / setup transitions;
- accelerator-hours, wall-clock, peak memory, update counts;
- fault inspection records and dispositions;
- checkpoint and resume records.

**Return path:**
- Summaries only, under `feedback-round-2026-10-24/evidence/<S0|A|E0|Z2|C>/<arm>/<seed>/`, each with a `manifest.json`.
- One `VERDICT.md` per check, applying §4.4 / §5.4 / §7.5 verbatim, with seed-level effects and intervals and every failed gate listed.
- Nothing is written outside `/srv/claude` from this sandbox.

---

## 10. Deferred (not launched this round)

Each of the following needs its own pre-registration:
- **Full E2:**
  - Z1 near ablation: p_near reassigned to expert, with planner share, update-condition distribution and K unchanged;
  - Z3 / Z4 matched independent and held action-noise nulls for D3.
- K sweep, which needs matched control-step budgets rather than matched macro counts.
- A competence-gated source schedule, only if the deadlock flag fires.
- A second C target task.
- Hindsight-goal and frozen-body alternatives.
- The world-model track.
- Whitening, height-in-B and B-input expansion. None of these is warranted by current evidence.
