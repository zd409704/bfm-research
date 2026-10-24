# Mechanism vs Implementation Gap Table — Author A

**Columns**
- **Mechanism**: what the corrected mainline needs.
- **Production status**: per the owner audit and `baseline/02`, `baseline/05`. Production code is *outside* `/srv/claude` and not inspected here.
- **In this research tree**: what exists under `/srv/claude/research/fb-beyond-imitation-acceleration/`.
- **Missing**: what is absent or unmeasured.
- **Priority**: P0 = needed before E0/E1; P1 = needed for E2/C; P2 = deferred.

Tree fact: `gpu_experiments/fb_core.py` holds toy modules (`BackwardMapB`, `ForwardEnsembleF`, `ConditionedLowLevelActor`, `RecurrentLatentPlanner`, `RecurrentTaskTwinCritic`, `sample_ufo_mixed_z`). There is no `FBAgent`, `TaskLearner`, `Collector`, or `CandidateProvider` in this tree. The only grep hit is the draft `packets/B02/drafts/A/spike_sketch.py`.

| # | Mechanism | Production status (owner audit / baseline) | In this research tree | Missing | Priority |
|---|---|---|---|---|---|
| GAP-01 | Demo frame → current B → expert cue | Exists: frame sampled unfiltered from `[T,229]`, encoded `eval/no_grad` per macro (baseline/05 §3) | Toy `BackwardMapB` only | Evidence that the cue is *followed* (controllability ratio) in real physics | P0 (E0) |
| GAP-02 | Near cue (10–20° tangent rotation) | Exists | Formula in baseline/02 §3.3; B02 D4/D5 tangential diagnostics designed but not landed | Near ablation on real training; behavior-distance-vs-angle curve | P1 (E2) |
| GAP-03 | Planner-z exploration | **Missing**: planner emits deterministic z via the actor `.loc` mean; no z noise | None | Optional tangent noise on planner z held per macro; executed-z logging | P0 knob (off in E1), P1 use (E2) |
| GAP-04 | Executed vs training randomness separation | Training RNGs (z_update, target smoothing) are not executed exploration | Not represented | Per-source tag and executed-z log in replay or telemetry; no exploration claim may cite training RNGs | P0 |
| GAP-05 | Macro-K hold of z | Exists, K=10 (0.2 s) | Spec only | Within-macro goal-progress log; K sweep (deferred) | P0 log / P2 sweep |
| GAP-06 | Reward-free FB/actor update | Exists: `FBAgent.update` does not read task reward | Toy losses in `fb_core.py` | None for the theory match; production unit test of BN two-pass order planned externally | P1 (external unit test) |
| GAP-07 | 50/50 z_update (current-B next-motion / random sphere) | Exists | `sample_ufo_mixed_z` toy | Measurement of executed behavior quality for random-sphere z (never executed in env today) | P1 |
| GAP-08 | FB replay unfiltered by task return | Exists | n/a | Filtered-replay control arm (C design) to separate benefit vs negative transfer | P1 (C) |
| GAP-09 | Retention | Finite circular FB replay + separate task replay with age/height rules; **no permanence promise** | n/a | Three separate measures: readable (in buffer), executable (π_{B(m)} reaches m), findable (planner reproduces old task) | P1 |
| GAP-10 | Task Q / planner from macro returns | Exists: `TaskLearner` on executed `z_actual`, variable-k discount | Toy recurrent critic/planner | Q calibration vs replay age; actor-drift (KL on probe set) vs Q error | P0 log |
| GAP-11 | Source schedule expert/near/planner | Exists, **time-based** ramp to 0.70 planner by 100k steps | Spec | Competence signal (not a gate in E1; candidate revision only if E0 shows deadlock) | P0 log / P2 change |
| GAP-12 | Beyond-demo outcome panels | Designed (ID / interpolation / OOD panels, Wilson gate) | Wilson and quota arithmetic checked (B05 local) | Real per-seed panel curves | P0 (E1) |
| GAP-13 | Imitation and direct-action baselines | Listed as required in baseline/02 §6.4; **none run** | None | Direct-action off-policy RL, +action-repeat/correlated noise, on-policy PPO-family, tracking-reward baseline | P0 (E1) |
| GAP-14 | Terminal boundary `severe_penetration` vs `invalid` | Specified R2.1 | FSM checked on a toy multi-link simulator env (`gpu_experiments/physics_env.py`) with injected faults | Production terminate/replay/eval/recovery verification | P0 (external) |
| GAP-15 | Curriculum unlock + quotas | Specified | Formula checks only | Production verification of unlock events in logs | P0 (external, logged in E1) |
| GAP-16 | B Gram conditioning | Not measured on production replay | Synthetic spectrum by construction (B01 script) | κ / effective-rank log on production replay, **info only, no whitening** | P0 log |
| GAP-17 | Motion-only B under contact | B has no height, scan, or contact (charter §2.3) | Tautological aliasing check + supervised regression (B03 script) | Real contact-skill experiment (same-state branching across contact regimes) | P2 |
| GAP-18 | Height in B / same-height relabel | **Not applicable**: current B has no height | B03 6/7 waste theorem assumes height-in-B | Nothing; do **not** install 70% same-height sampling | — |
| GAP-19 | World-model pathwise gradients | Not in mainline; separate track | Toy plant (state 32, action 12, d_z 64) ablation | Everything; out of scope this round | P2 (separate track) |
| GAP-20 | Run identity and cost accounting | Unknown | None | Config hash, code revision, seed, env version, demo hash, GPU-hours, wall-clock per run | P0 |
| GAP-21 | Fair tuning budget | Unknown | None | Equal sweep budget per arm, recorded | P0 |
