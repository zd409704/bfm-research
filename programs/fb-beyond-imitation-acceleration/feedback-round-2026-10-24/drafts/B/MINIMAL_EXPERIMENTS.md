# Minimal decisive validation plan — Author B

**Priority: A first, C only if A passes; defer a full B exploration study.** These are two bounded checks, not a simultaneous A/B/C sweep. The numbers below are proposed pre-registered decision rules, not observed results or universal theoretical constants. Freeze the run manifest before training. No experiment in this document has been executed.

All learning uses actual environment transitions from the intended home-humanoid plant-class training chain. A faithful production simulator can provide that evidence; successful simulation alone must not be called physical-hardware validation. The local simplified plants and scripted checks cannot substitute for the intended chain. Production verification and training are planned external steps; this review creates no external code paths or artifacts.

## Entry gate: make a production result interpretable

Before either check, resolve the actual collector, environment step, replay writers, `FBAgent.update`, `TaskLearner`, evaluator, and resume entrypoints against one immutable revision. Record their real identities when available, without inventing paths now. Use the [obstacle specification](../../../baseline/05-autonomous-obstacle-traversal-v3-and-r2-plan.md), [B02 contracts](../../../synthesis/B02-synthesis.md), and [B05 contracts](../../../synthesis/B05-synthesis.md) as requirements to check, not presumed implementations.

Perform a bounded integration audit: at most 10,000 attempted control transitions plus targeted fixtures. Any failed integrity assertion blocks scientific interpretation until repaired and the protocol version changes. This is an engineering entry gate, not a third efficacy experiment.

| Audit | Required observation |
| --- | --- |
| Data provenance | Cue-only offline frames never appear as forged environment transitions. Valid low-return and credible failure rows enter FB replay. Task rows retain actual history, command, return, and elapsed k. |
| Update semantics | Current-B expert/near encoding; 50/50 current-B next-motion/random-sphere update conditions; standard F·z actor objective; no task reward in FB update; task returns used by the task learner. |
| Immutability and statistics | Zero executed-z mutations after repeated FB updates; zero normalizer changes from cue queries/evaluation; exactly the specified real-data statistics updates. Compare snapshots, not only returned flags. |
| Macro/recurrent targets | Independently reconstruct full and shortened macro returns and discounts; match scalar reference within 1e-6 absolute error. Compare recomputed recurrent outputs within 1e-5 on finite normalized fixtures; document precision. Distinguish termination from time-limit truncation. |
| Failure transaction | A finite credible penetration beyond 0.03 m is retained with terminal semantics. Later verified numerical corruption overrides it before any replay/statistics commit. Check actual mutable state across vector aborts and reservation release. A full contact buffer alone is not evidence of lost contacts without backend verification. |
| Evaluation and recovery | Invalid evaluation halts and is marked invalid. Check two consecutive curriculum panels, low-height regression behavior, quota conservation, checkpoint identities, replay/optimizer/random-stream restore, and resumed rollout against an uninterrupted short reference. |

Preserve finite physical failures in metrics. Invalid runs are not silently removed or replaced with a favorable new seed. Retain attempted-cost accounting and the failed artifact; any repaired rerun is separately identified.

## Shared statistical and cost rules

Use five paired independent training seeds: 24001–24005. Match environment randomization streams across arms where possible; do not assume identical realized trajectories. A seed, not an episode or checkpoint, is the unit for between-method inference. Evaluation randomness is independent of training and shared across compared arms.

For A's two baseline comparisons use paired seed differences with two-sided 97.5% Student-t intervals, giving Bonferroni family coverage of at least 95% under the interval assumptions. C uses a two-sided 95% paired interval. With five seeds these intervals are assumption-sensitive; publish every seed value, paired differences, and leave-one-seed-out sensitivity. Wide intervals mean inconclusive. No seed substitution, opportunistic extra runs, or favorable checkpoint selection.

Interaction counts mean aggregate attempted plant control transitions across all parallel environments, including warm-up, pretraining, unsuccessful episodes, and invalid attempts. Report accepted transitions separately. Evaluation, diagnostics, tuning, resets, and offline updates have separate counters and are included in total resource cost. Report both success versus training interactions and success versus elapsed time on matched hardware allocations; include accelerator-hours, peak memory, environment throughput, update counts, data volume, and tuning costs. An interaction advantage with higher compute cost is reported as that tradeoff.

Before test seeds, allow one non-test setup seed per A arm, capped at 100,000 transitions each. It selects one fixed working configuration from at most two declared configurations per arm, within that total cap. These runs cannot estimate efficacy or change the success definition. No additional tuning for C. If the allotted budget is inadequate, report that limitation; do not enlarge it after viewing test outcomes.

## Check 1 — A: does the framework improve task-learning efficiency?

**Question.** With equal interaction access and comparable tuning opportunity, does the joint body/task architecture beat two simpler ways to learn the same obstacle task?

Three arms, five seeds each, maximum 1,000,000 training control transitions per run:

| Arm | Frozen definition |
| --- | --- |
| A-F: framework | Audited FB + conditional actor + macro task Q/planner; motion-only B; K=10; standard update sampler; existing expert/near/planner schedule; deterministic planner/actor-mean execution as reported. No added planner-z noise, whitening, world model, or task gradient into the body actor. |
| A-I: imitation-assisted task learner | Direct-action policy with the same motion material used as a motion-imitation prior plus task reward. It may adapt to task outcomes and depart from demonstrations. Pose/velocity data do not supply nonexistent action labels. No pre-existing pretrained checkpoint. The framework's no-imitation-loss constraint applies to A-F, not this comparator. |
| A-D: direct-action task learner | Task-reward RL from scratch with the same deployable observations/history, actuator limits, control rate, task reward, and environment access. Normal executed-action exploration is allowed and documented. |

Use the intended plant dynamics and fixed training-height distribution, equally split between 0.10 m and 0.20 m. Fix resets, timeout at 1,000 control steps, task reward, termination rules, and physical success detector identically across arms. Fix these two training heights to avoid curriculum exposure confounding the first comparison; audit production curriculum behavior separately at the entry gate. Record any privileged critic inputs and match that access across arms. Match policy/critic capacity as closely as practical and report parameter and update-budget differences rather than pretending six networks cost the same as two.

At 0, 100,000, …, 900,000 training steps, evaluate 20 episodes at each of 0.10, 0.20, 0.15, and 0.25 m. At the final checkpoint run two independent panels of 100 episodes per height with frozen weights and no learning between panels. For A-F, evaluation is 100% planner with frozen statistics and no expert/near help. The two additional heights are held out from training; their results are secondary and do not select models or schedules.

**Primary endpoint:** normalized trapezoidal area under the success-versus-training-interactions curve, in [0,1], averaged equally over the two training heights. Use both final panels pooled for the final curve point. This measures learning efficiency across the fixed budget, including cold start. Time to a 70% Wilson lower-bound threshold is secondary, requires two qualifying panels, and is right-censored if never achieved. Do not assign failed runs a fictional threshold time.

**Advance to C only if all gates pass:**

1. Against each baseline, mean paired primary-endpoint improvement is at least 0.05 and the simultaneous interval lower bound is above zero.
2. At least four of five A-F seeds achieve a 95% Wilson lower bound of at least 0.70 at both training heights in both final panels. At 100 episodes this requires at least 79 successes in each relevant panel.
3. For final evaluation credible severe-penetration rates, the upper simultaneous paired interval for A-F minus each baseline is at most 0.05 absolute probability. This guards against buying mean success through materially more severe failures.
4. The entry integrity gate passes and no unresolved invalid run is omitted from the comparison.

If the framework improves only final success, report final performance rather than sample efficiency. If intervals cross zero, do not scale on an advantage claim. If direct-action learning succeeds and A-F remains unable to produce useful command-conditioned outcomes, revise the body/task design before more compute. If all arms fail, the result is unresolved task/budget adequacy, not a proof against the framework.

Add small descriptive branch panels at 0, 500,000, and 1,000,000 steps for A-F: eight saved physical starts and eight commands each, for at most 100 steps. Commands include planner, expert, near, and random-sphere probes plus a repeated-command control. Freeze networks and random seeds, retain ended states as absorbing, and record task progress, contact events, survival, actuator saturation, and endpoint differences. These probes do not enter replay. They distinguish actor collapse from planner selection failure; a finite command bank is not an oracle over all possible z. Random-sphere diagnostic probes are not a newly added training rollout source.

Training cap: 15,000,000 transitions, plus 300,000 setup and 10,000 audit transitions. Evaluation cap: 24,000,000 transitions at the specified timeout. Branch cap: 96,000 transitions. Count early terminations at their actual cost. Resource caps and allocations in accelerator-hours must be filled from the entry audit's measured throughput before launching test seeds; they may only shorten, not silently enlarge, the interaction plan.

## Check 2 — C: does low-current-return experience cause later utility?

Run only after A passes. This is an intervention on use of a common physical dataset, isolating body learning from collection differences and task-critic carryover.

Predeclare source task U as forward obstacle traversal and later task V as recovery to upright stability following a fixed distribution of lateral landing disturbances. V success requires avoiding fall/credible severe penetration and holding upright stability for the final 100 consecutive control steps of a 1,000-step episode. Freeze the exact upright angle, base-height, and velocity tolerances in the manifest from the plant's existing balance definitions before donor collection. Do not choose a later task after discovering where low-return data looks helpful. If the plant has no testable balance definition, C is not launch-ready.

For each paired seed, take the corresponding final A-F checkpoint as a common starting point. Collect at most 500,000 additional source-task transitions with that checkpoint frozen, including its declared exploration source schedule. The two learning branches receive the identical donor pool. No branch gets extra physics. Label a donor episode low-return if it is unsuccessful on U and its return is at or below the 25th percentile among unsuccessful donor episodes. Determine labels once before branch training. Valid transitions from those episodes form L; invalid records remain excluded. If L is less than 10% of valid donor transitions, mark the test ineligible and do not search alternative cutoffs.

| Branch | Body-learning intervention |
| --- | --- |
| C-use | 10,000 FB/actor updates, batch size 256: sample 25% from L and 75% from the remaining valid donor transitions. |
| C-omit | Same number and size of updates; replace each L slot with a sample from the remaining donor transitions. |

Both branches start with identical weights and optimizer state, use identical update random-stream schedules, the standard 50/50 condition sampler, and frozen common normalizer statistics. Rebuild each branch's FB sampling pool accordingly: C-omit must not draw L as a transition, a permuted next-motion condition, or any other update input. Hash and log sampled IDs. Only the inclusion of L differs; task Q/planner do not train during this intervention. This controlled enrichment tests the usefulness of L, not the efficacy of the production buffer's natural sampling frequency. Audit that natural admission and sampling separately.

After the intervention, freeze each body controller and train a freshly initialized V task Q/planner for at most 250,000 transitions per branch, with paired initialization and identical task observations/exploration. Carry over no U task replay, task critic, planner, or recurrent hidden states. Frozen body training isolates reuse of acquired capability; it does not test joint V skill growth.

Evaluate V with 20 episodes at 0, 50,000, …, 200,000 steps and 100 episodes at 250,000. The primary endpoint is normalized success AUC over these V steps. **C passes** if C-use exceeds C-omit by at least 0.05 mean paired AUC with a 95% interval lower bound above zero, and its final U success degradation is no worse than 0.05: the lower 95% paired interval for C-use minus C-omit on the U retention panel must be at least -0.05. Evaluate U once after the intervention using the common original U planner, 100 episodes at each source height. This retention check deliberately includes compatibility with an existing planner.

Measure the three retention meanings independently:

1. **Readable data:** trace L admission, sampling, and eviction. Remove the donor pool from access before V training and verify neither branch reads it. This explicit removal tests survival after data access ends; it does not establish the natural circular buffer's long-term behavior.
2. **Executable behavior:** before and after body updates, run the same bounded physical start/command panel, with raw prompt frames re-encoded using the respective current B. Also report fixed numerical commands to expose interface drift. Count useful recoveries, not mere trajectory divergence.
3. **Planner use:** compare fresh-planner V learning curves under frozen bodies. A larger branch-search repertoire without improved planner learning supports executable potential only, not realized task reuse.

C-use superiority supports the causal utility of this selected low-U-return pool under this intervention. It does not establish that every low-return transition is useful, that records must be permanently retained, or that the body representation is the unique reason for the benefit. A null result limits this source/target pair and budget; a reproducible negative result supports filtering/sampling or capacity research, not automatic deletion of credible physical failures.

C caps: 2,500,000 donor transitions plus 2,500,000 V-training transitions; 100,000 offline updates across ten branches; at most 2,000,000 V-evaluation and 2,000,000 U-evaluation transitions. Two before/after body panels per branch add at most 128,000 diagnostic transitions. All costs are reported in addition to A. Total planned training/donor cap across A and C is 20,000,000, excluding the separately enumerated setup, audit, evaluation, and diagnostics.

## Deferred B and interpretation of outcomes

Do not launch a near/no-near, planner-noise, and K sweep alongside A/C. If A succeeds but collection diagnostics leave the mechanism uncertain, a later B study should first compare the unchanged source schedule with near probability reassigned to expert, preserving planner probability, update-condition distribution, K, and all other settings. Independent executed planner-z noise is another separate factor. Do not attribute either manipulation to training-target random draws. Macro-duration comparisons require matching control-step budgets, not macro counts.

Passing A warrants a narrow task-learning efficiency claim on the tested plant/distribution. Passing C adds a narrow causal reuse result. Neither establishes general home-humanoid competence, universal retention, optimal macro duration, or world-model acceleration. Beyond-demo task success and physically novel contact outcomes may be reported as secondary evidence with predeclared support-distance definitions; unindexed single frames do not establish absence of a behavior from all demonstration trajectories.

## Required external evidence bundle

Before launch, fill an immutable manifest with: revision and patch digest; actual module/entrypoint identities; configuration hash; plant model and physics build; observation/action schemas and units; demonstration identity/hash and available fields; train/evaluation/reset split identities; seed streams; source schedule; K and discounts; normalizer rules; replay capacities/age/height eligibility; loss weights and optimizer/update ratios; network sizes; hardware allocation; and cost ceilings. Unresolved entries are launch blockers, not assumed defaults.

For every seed preserve complete per-checkpoint curves and success/failure numerators, event traces, attempted/accepted/evaluation counters, replay lineage, model/optimizer/normalizer/recurrent-state identities, checkpoint/resume records, wall time, accelerator-hours, memory, and interrupted-run records. Produce one comparison table with seed-level effects and intervals, plus each failed gate. Store actual production evidence through the external execution workflow; any later copies reviewed in this sandbox must remain under `/srv/claude`.
