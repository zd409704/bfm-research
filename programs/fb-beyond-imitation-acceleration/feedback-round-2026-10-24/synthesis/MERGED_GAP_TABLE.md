# Merged Mechanism vs Implementation Gap Table — feedback-round-2026-10-24

Reconciles draft A `GAP_TABLE.md` (GAP-01…21, P0–P2 priorities) with draft B `GAP_TABLE.md` (provenance taxonomy, three-data-path audit). It applies MX-9 from `DISPOSITION.md`, which combines agy MF-6 with Sonnet fix 10. Production code lives outside `/srv/claude` and was not inspected. Every production claim below is either owner-reported or pending.

## Labels

**Provenance** (draft B taxonomy; both adjudications require it):
- **O = Observed**: local source in this research tree was inspected.
- **R = Reported**: owner production audit (`../briefs/OWNER_FEEDBACK_EN.md`).
- **S = Specified**: research contract or baseline spec (`../../baseline/02`, `../../baseline/05`, B01–B05 synthesis). A spec is not evidence of integration.
- **P = Pending**: requires external production verification. Nothing marked P is done.

**Priority** (draft A scheme, re-anchored to the staged plan in `MERGED_MINIMAL_EXPERIMENTS.md`):
- **P0**: required at Stage 0 (entry integrity gate), or required telemetry before Stage-1 test seeds.
- **P1**: required during Stage 1/2 analysis or before C.
- **P2**: deferred.

**Origin** gives the source row: A-xx = draft A GAP-xx, B = draft B row, Rv = added by a blind review or an adjudication.

**Tree fact (O):** `gpu_experiments/fb_core.py` contains only toy modules:
- `BackwardMapB`
- `ForwardEnsembleF`
- `ConditionedLowLevelActor`
- `RecurrentLatentPlanner`
- `RecurrentTaskTwinCritic`
- `sample_ufo_mixed_z`

**No `FBAgent`, `TaskLearner`, collector or evaluator class exists in this research tree. The production identity of these modules is *unresolved*, not absent.**

---

## A. Integration identity and data paths

| ID | Mechanism / obligation | Prov. | What exists | Gap | Minimal closing evidence | Pri. | Origin |
|---|---|---|---|---|---|---|---|
| G01 | Production module identities: collector, env step, replay writers, `FBAgent.update`, `TaskLearner`, evaluator, resume | O (absent here) / P | Toy modules only | The production revision and entrypoints have not been identified | Immutable revision + patch digest + entrypoint identities in the manifest. Unresolved entries block launch. | P0 | B, Rv (A-on-B m5) |
| G02 | **Three data paths kept separate**:<br>(i) offline pose/velocity frames are B cues only;<br>(ii) real transitions feed FB/actor;<br>(iii) real macro history/return/executed z feeds task Q/planner | S / P | Owner feedback spec | No audit exists. The risk is offline frames acquiring forged actions, rewards or next states. | Provenance IDs and schema assertions on every row class. **Zero** offline cue rows in transition replay. Task rows carry actual history, z_actual, return and elapsed k. | P0 | B, Rv (B-on-A F8) |
| G03 | Demo frame → current B → expert cue | R / S (baseline/05 §3) | Toy `BackwardMapB` | No evidence that cues are *followed* in real physics | E0 controllability ratio, both goal pools | P0 (E0) | A-01, B |
| G04 | Demonstration coverage: a single 859-frame 0.704 m file | S (baseline/05 §1.1) | Spec and hash reference | The field inventory (velocity present?) and the coverage of heights and contact modes are not recorded. Demo access is asymmetric across A arms. | Hash plus field inventory in the manifest. The information budget per arm is labelled. | P0 | Rv (A-on-B m5 G5) |

## B. Body layer (FB / actor)

| ID | Mechanism | Prov. | What exists | Gap | Minimal closing evidence | Pri. | Origin |
|---|---|---|---|---|---|---|---|
| G05 | Reward-free FB/actor update | R; O (toy losses) | `FBAgent.update` reads no task reward (owner audit) | No real transition has been traced end to end | Trace one real transition through the FB loss and actor update, then observe a changed held-out behavior | P0 | A-06, B |
| G06 | 50/50 `z_update`: current-B permuted next motion / random sphere | R; O (`sample_ufo_mixed_z`) | Sampler exists in toy form | Sampled-condition source is not logged. "Sampled condition" is not the same as "executed or learned skill". | Log the sampled source per batch. Expected fraction 0.50, verified within ±0.02 over ≥10⁴ draws at the entry gate. Report how often valid transitions are used. | P0 | A-07, B, Rv (A-on-B m5 G3) |
| G07 | BN two-pass order; normalizer frozen on cue queries and evaluation | O (artificial tests, `run_b02_nonstationarity_spike.py`) / P | Prototype contract | Not verified in production. Draft A had this at P1, inconsistent with its own plan; both reviews flagged that. | Before/after snapshot hashes of normalizer statistics. Statistics update counts match the specified real-data updates. | **P0** (was P1) | A-06, B, Rv (B-on-A §3) |
| G08 | `behavior_z` immutability across FB updates | O (local check) / P | Prototype contract | Not verified in production | Hash of executed macro z before/after repeated FB updates. Zero mutations. | P0 | B |
| G09 | Motion-only B under contact/terrain aliasing | R (no height, scan or contact in B); O (B03 supervised artificial-context test) | Conditional theory | The B03 premises — equal future occupancy and an indistinguishable full actor input U_t — have **not** been shown on the plant | Paired physical context interventions with full actor inputs. No B-input expansion without that counterexample. | P2 | A-17, B |
| G10 | Height in B / same-height relabel | R (current B has no height) | B03 6/7 waste theorem assumes height in B | Not applicable | Nothing. **Do not install 70% same-height sampling.** | — | A-18 |
| G11 | B Gram conditioning on production replay | Not measured | Imposed synthetic spectrum (`run_b01_gram_spike.py:33`) | Not measured | κ and effective-rank log on production replay, **information only, no whitening** | P1 | A-16 |

## C. Exploration and execution

| ID | Mechanism | Prov. | What exists | Gap | Minimal closing evidence | Pri. | Origin |
|---|---|---|---|---|---|---|---|
| G12 | Planner-z exploration | R: the planner emits a deterministic z; no planner-z noise | None | The owner's "z organizes exploration" story has no executed planner-side mechanism | Knob: tangent noise θ ~ U[5°, 15°] on the planner mean, held for the macro, planner source only. **Present but off** in Stage-1 A-F; used only in the conditional Z2 diagnostic. | P0 (knob present) / P1 (Z2) | A-03, B |
| G13 | **Executed stochasticity by source** (expert / near / planner; low-level actor executes `.loc` mean) | R | Not represented | As the ramp moves to 70% planner share, executed exploration shrinks to whatever expert/near cue diversity supplies. This is unmeasured. | Per macro, log:<br>• source;<br>• command before/after perturbation;<br>• actor mean;<br>• applied action after clipping;<br>• random-stream identity.<br>Report executed-z angular dispersion by source. | P0 | Rv (A-on-B M6; agy MF-6) |
| G14 | Training RNGs (z_update, target smoothing) separated from executed exploration | R | Not represented | Risk that exploration claims cite training randomness | Separate stream identities. No exploration claim may cite training RNG draws. | P0 | A-04, B |
| G15 | Near cue (10–20° tangent rotation) | S (baseline/02 §3.3); B02 D4/D5 diagnostics designed, not landed | Formula | No near ablation; no behavior-distance-vs-angle curve | Deferred E2 (Z1). Stage-1 branch panels include near probes descriptively. | P2 | A-02, B |
| G16 | Macro-K = 10 hold; shortened macros; actual-k discount | S; R | Spec only | Return/discount reconstruction and macro-boundary behavior are unverified | Independent reconstruction of full and shortened macro returns within 1e-6. Log within-macro goal progress. | P0 | A-05, B |
| G17 | Source schedule: **time-based** ramp to 0.70 planner share by 100k steps | R / S | Spec | (a) The unit is ambiguous: vector steps or aggregate transitions.<br>(b) A time-based ramp risks cold-start deadlock. | (a) Resolve the unit at Stage 0 and record it in the manifest.<br>(b) Record a deadlock flag (single Boolean, Experiments §5.4). A competence-gated schedule is a candidate revision only if the flag fires. | P0 (unit) / P2 (change) | A-11, Rv (B-on-A F10) |
| G18 | Planner-output off-support z (off-sphere extrapolation, far from the cue set) | Not measured | — | A planner can emit z that is outside the cue/update distribution | Log ‖z‖ and the angular distance to the nearest cue z and to the update-condition support. Report the fraction of planner z beyond the 99th percentile of cue-to-cue distances. | P1 | Rv (A-on-B m4; agy MF-6) |
| G19 | **Objective sufficiency / planner findability**: is a task-useful command executable but unused, or not executable at all? | Not measured | — | Distinguishes D4 failure (body lacks the skill) from D5 failure (planner does not find it) | Branch-panel bounded command search: task progress of the best probed command vs the planner's command from the same starts | P1 | B, Rv (Sonnet fix 1) |

## D. Task layer, replay, retention

| ID | Mechanism | Prov. | What exists | Gap | Minimal closing evidence | Pri. | Origin |
|---|---|---|---|---|---|---|---|
| G20 | Task Q / planner trained from macro returns on z_actual | R; S; O (toy critic/planner) | `TaskLearner` consumes macro returns (owner audit) | Calibration under actor drift is unmeasured | Q-calibration: full-return Monte-Carlo target with bootstrap only at truncation. Slope, intercept and RMSE per replay-age bin. **Non-gating.** | P1 | A-10, B, Rv (MX-11) |
| G21 | Recurrent prefix recomputation (zero-hidden full-prefix burn-in) | S; O (random-data parity) | Prototype contract | Not verified on production fixtures | Parity within 1e-5 on finite normalized fixtures. Generation-tagged prefixes. | P0 | B |
| G22 | Drift tolerance under deterministic execution | S (B02 Gaussian-KL drift gate) | Analysis assumes a stochastic policy | **The Gaussian KL is undefined or uninformative under `.loc` execution** | Action-space RMS between the current and lagged actor mean on a frozen probe set, plus physical branch comparison | P1 | B, Rv (A-on-B m1) |
| G23 | FB replay is unfiltered by task return; admission ≠ use | R | No filter | Admission does not show sampling, gradient use, retention or later benefit | Instrument low-return row IDs at collect / commit / sample / update / evict | P1 (C) | A-08, B |
| G24 | Retention, in three senses | R (finite circular FB replay; task replay age/height rules; no permanence promise) | — | The three senses are not measured separately | (i) readable: trace and evict counts;<br>(ii) executable: before/after body panel;<br>(iii) findable: fresh-planner learning on V | P1 (C) | A-09, B |

## E. Terminal semantics, evaluation, protocol, accounting

| ID | Mechanism | Prov. | What exists | Gap | Minimal closing evidence | Pri. | Origin |
|---|---|---|---|---|---|---|---|
| G25 | `severe_penetration` (credible failure, committed, Φ_next = 0) vs `invalid` (quarantined before any mutation); terminal priority latch | S (R2.1, Charter §2.4); O (toy FSM with injected faults, `run_b05_r21_verification_suite.py`) | A returned commit flag in a toy environment | A flag is not an atomic production transaction. Vector abort, backend warning interpretation and reservation release are all unverified. | Production fixtures: a finite >0.03 m penetration is committed; later NaN/overflow overrides it before any replay/statistics commit. Snapshot all mutable state before/after. | P0 | A-14, B |
| G26 | **Fault inspection / recovery protocol** (no auto-restart, no arm exclusion) | Absent in draft A; partial in draft B | — | Draft A's restart-and-exclude rule biases the comparison | Experiments §3: halt → inspect → documented disposition. All seeds retained. Rollback charged to cost. | P0 | Rv (B-on-A F2; MX-2) |
| G27 | **Evaluation / collection protocol**:<br>• evaluation makes zero replay writes;<br>• frozen statistics;<br>• 100% planner for A-F;<br>• independent evaluation RNG shared across arms | S | Spec | Not verified | Replay and normalizer hashes are unchanged across an evaluation panel. Evaluation seed streams are logged. | P0 | Rv (A-on-B m5 G4) |
| G28 | Curriculum unlock and quotas (two-panel Wilson, 4096-env quota) | S; O (formula only) | Arithmetic check | Unlock behavior in real training is unobserved | Audited at Stage 0 only. A Stage 1/2 uses fixed training heights, which removes the curriculum confound. | P0 (audit) / P2 (use in A) | A-15, B |
| G29 | Comparator arms A-D, A-DC, A-I | S (baseline/02 §6.4 lists baselines) | None run | No baseline evidence | Frozen arm definitions (Experiments §4.2) | P0 | A-13 |
| G30 | Run identity and cost accounting | None | — | No counters exist | Counters for attempted / accepted / rolled-back / evaluation / probe / setup transitions. Accelerator-hours, wall-clock, peak memory, update counts, config hash, seeds. | P0 | A-20, B |
| G31 | Fair tuning budget | None | — | Not defined | ≤2 declared configurations × 1 setup seed × ≤1.5M per arm. Selection by setup AUC, then frozen. | P0 | A-21, B |
| G32 | World-model pathwise gradients | Separate track; O (toy plant: state 32, action 12, d_z 64) | Toy ablation | Everything | Out of scope this round | P2 | A-19, B |

---

## Counts and priority summary

- **P0 (Stage 0 entry gate or pre-test-seed telemetry):** G01–G08, G12 (knob), G13, G14, G16, G17 (unit), G21, G25–G31.
- **P1:** G11, G12 (Z2), G18–G20, G22–G24.
- **P2:** G09, G15, G17 (schedule change), G28 (curriculum in A), G32.
- **Not applicable:** G10.

**Reconciliation notes:**
1. Draft A's single "Exists" column has been split into R and S throughout.
2. Draft A GAP-07 claimed random-sphere z are "never executed". It is restated as "random-sphere update sampling is not an executed exploration source; actual overlap must be measured" (G06, G13).
3. Draft A GAP-03 mixed planner output with actor mean execution. These are now separated into G12 (planner) and G13 (executed stochasticity).
