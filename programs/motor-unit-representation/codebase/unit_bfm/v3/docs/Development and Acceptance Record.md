# V3 Development and Acceptance Records

Date: 2026-10-10. Status: This round of quarantine training works has been completed and has been received through integrated inspection; Common skills and the 20M formal experiment were not completed. The current version is retained in unit_bfm root package; The new version is located in unit_bfm/v3, and the original program is recorded with the old baseline of artifices at .ssh/relay-legents/v3-development-baseline.json.

# Frozen design boundaries

- B: g13 result status, known length/limit + unified mechanical angle/speed/actual torque + relative end speed + causal recent acceleration and effective position.
- Actor: x137, known local model/driver parameters and history, no extra load/contact/world truth values ​​read.
- F: x plus actual physics/boundary/drive state and feature update memory; the latter does not hide the physical truth, but only sends F.
- z16, Dual Branch 256, Predefined Activation/Spherical Normalization, Standard FB/Orthogonal/Actor Objectives; No Reward Works or Additional Supervised Losses.
- Control of 100 Hz, physical/driving 1 kHz; The output side regulates the power rectangular request. Original equipment and model tree coordinate map separated.
- E0-E4, true parameter write, wide stroke geometry check, load/block/release/abutment and contact combination; weld not calibrated disabled.

## Development division of labor

Three independent relay CLI sessions, high inference, and inheritance models; each writes only the new package allocation file, and the GPU is exclusive to the main window (the agent's own environment CUDA is not available). The main window manages common APIs, legacy version isolation checks, integrations, and independent acceptance.

| Modules | Responsibilities | Current Evidence |
|---|---|---|
| Features and learning | v3-core | Passed the first round of 17 tests; the main window accepts core and adds read-only cross-auditing |
| Mechanical/Randomization/Privileges/CPU and Warp | v3-physics | Under development |
| Collection/Replay/Training/Evaluation/Export | v3-pipeline | Under development |
| Old version isolation | Main window | Initial baseline check passed; recheck before delivery |
| Complete Physics and Learning Links | Main Window | 96W/6 updates of the original CPU full link passed; coverage and capability threshold not reached |

## The state that cannot be confused

CPU operator test, CPU physics, GPU batch physics, learning update, frozen export, and actual control evaluation are accepted separately. Short training only proves that the project can be run, but does not prove that V3 reaches the expected skills or has sufficient coverage; formal data/training status is reported by actual counts and manifest.

# First round of independent inspections (first edition code, subsequent modification of this evidence to expire)

- `test_integration_contract`: 26 steps each for E0–E4/P+D, real points/features, privilege isolation, memory next-step reconstruction, complete rules/policy episode→Replay→FB, and the next update after recovery is consistent bit by bit; 2 tests passed.
- `test_integration_mechanics`: Independent finite difference of end position/velocity/acceleration at different world installation angles and fixed side, motor delay + first-order response analytical solution with real 10 sub-step integration, requested power sign; 2 tests passed.
- `python -m unit_bfm.v3.train --mode smoke --run-dir unit_bfm/v3/runs/coordinator_smoke_01`: 96 active transfers, P0 24, online 36, 6 updates, no invalid transfers, CPU about 2.22 seconds; save checkpoint/query library/Actor + B export. `coverage_ready=false, validated=false`, cannot be used as proof of V3 capability.
- Two quarantine checks on the size and timing of the old version of the benchmark Hashi/old artifices, no V2 component imported.
- The turn_context of three actual relay sessions confirms gpt-6-astra/high.

Review to be implemented: actual parameter range/layered independence, initial state mixing, rule loading process coupling, F external process state, same solution coordinates, coverage diagnostic contract, full data disk memory and GPU batch acquisition. The detailed incremental issue has been sent to the corresponding relay session, and the queue receipt is not equal to execution.

### The first real GPU pairing (first version of schema3176)

Main window RTX5060Ti, `python -m unittest unit_bfm.v3.tests.test_physics_backend -v`, Warp/Mjlab each E0–4/P+D/2world/10 control step, CPU q/dq/integral/p assertion passed, 94.678 seconds including the first CUDA compilation. Unavailable CUDA reject test skipped because natively available. The unavailability of CUDA in the agent's own permission environment is an independent fact, and its permissions have not been changed. It must be rerun after subsequent modifications; the backend host transmission per ms is not yet equal to the full available training throughput.

## Cross-audit and rework

[Independent Audit](v3-core_cross_audit.md) gives 7 reproducible or clear static risks. 4 new regression items have been added to the main window, the raw valid repair has been passed, and the reset support parameter/ground relative M/strict missing group 3 items still failed. Physics/pipeline marks needs_changes in the first round, and continues the second round of repairs in the original relay session. If it is not accepted, it will only record the missing items and then stop.

The main window's random 100 scenes were initially installed with 72 passing and 28 illegal for the first time; after the fixed offset of the object was modified, 80 passing and 20 were illegal and still need to be repaired according to the real geometry. The failure list remains in audits/random_scene_first/second.json.

Running benchmark (early p4534 version): CUDA Actor+B p99 is about 0.20ms, 512-line FB update median is 10.5ms (excluding sampling), CPU rule collection is about 92.7W/s; 50-step archiving averages 21193bytes/transition, linear extrapolation of 20M is about 424GB, more than the current 133GB available. This is the additional overhead caused by the old full archiving solution; this direction has been withdrawn. 20M is the cumulative interaction budget, not the Replay capacity. Currently, bounded RAM Replay is used, the full trajectory is not saved by default, and compressed archives are no longer used as the main training path. This number is only reserved for error correction records of the old scheme.


# Supervised development round (current acceptance basis)

[This round of development constraints and acceptance ](Current Development Constraints and Acceptance.md) replaces the old full-volume archiving requirements. The roles are physics development, pipeline development, and core read-only discussion and audit. The main window is independently re-run and does not accept the developer's self-report to complete alternative acceptance.

- RAM Replay overcapacity write, P0 not overwritten by subsequent rules, no disk sampling, next batch/update exact recovery has been measured. The main window `supervised_ram_02` still found that P0's own FIFO lost the early group and the checkpoint saved the empty slot, which has been reworked.
- `supervised_physics_inputs_01`: The two F counterexamples of reset support parameters and ground M system distance have been repaired and passed; `supervised_snapshot_01`: The next step is consistent after restoring the physical clock, process/driver, and historical padding and passed.
- `supervised_cpu_revision_01`: 100 random 30 steps each, wide initial state, loading, snapshot, old V2 isolated pass. Only other test files were changed during the test, and the physics source code was unchanged.
- `supervised_gpu_final_01`: The latest schema4822 real CUDA pairing failed, and the conclusion cannot be adopted using the original version. The main window is positioned to the 0.06 s event boundary, the CPU/GPU load.active is different, and then the dynamics diverge; the unified physical tick clock is being repaired, and the tolerance masking is not relaxed.
- The pipeline has been updated 3200W/37 times to develop short training, only proving that the link is running, and the above rework and independent re-inspection are still pending; complete random coverage, skill success or 20m training is not claimed.

The original test output and hashes before and after running are saved in `v3/audits/`. For independent discussion, see [v3-rl_design_review](v3-rl_design_review.md), and for audit, see [v3-rl_final_audit](v3-rl_final_audit.md).

GPU event clock rework accepted: `supervised_gpu_clock_02` original tolerance all passed (29.83 seconds), 2 back-end × 5 scenarios × 2 fixed side × 2world. The physics source code did not change during the test. Unified integer 1ms tick, snapshot v2, physical p still 4822; no input deleted or tolerances relaxed.

Real GPU learning integration in the main window: `runs/coordinator_gpu_learning_01`, Warp double world, 40 each of E0-E4, a total of 200 real transfers, 100 rules/policy each, five scenarios/two sources enter the gradient, CUDA performs 40 standard FB updates, all are limited, Actor/B export passed. It takes 15.35 seconds including environment/network establishment and export. Long-term throughput cannot be inferred based on this. Actor+B281617 parameter, single F2805008 parameter, total online5891633; this time p_total=5065, the execution end size has not changed. The hashes are consistent before and after the code is run. This check does not represent a verification of skills.


Finally, the pipeline rework has been placed on the order and passed the targeted re-inspection in the main window: all four items of `supervised_ram_fixed_03` passed; P0 general/grouped reserve replaces FIFO; checkpoint only saves active rows. `scheduling_fixed.json` accesses the 720/720 combination with 7200 schedules and 8 snapshot pools. The actual reset is 3600/2160/1440 (this is a schedule check and cannot be pretended to be physical coverage). The first step failure, legal peer suspension and useful prefix are counted separately; a full set of independent regression and 8000W mixed scenario training are still in progress.


## Mixed scene real training and frozen evaluation

Main window `runs/coordinator_mixed_01`: CPU real physics + CUDA learner, E0–E4, 4 lengths/limit configurations, 8018 effective W (slightly more than 8000 budget according to rollout boundary), P0800, policy3609, 100 updates, 66.43 seconds; two sources/five working conditions all enter the gradient. reset actual xi11, velocity6, snapshot4, fallback0. Replay capacity is 3072, active is 2610, and P050 is reserved (the small P0 budget is only used for some groups, clearly partial). The source code remains unchanged before and after running.

If an E2 contact penetrates 11.25mm and exceeds the 10mm failure threshold, it will be counted as invalid1 and isolated. A legal peer will be counted as aborted1; the valid prefix is ​​retained. No relaxing thresholds or pretending failure looks like termination. This failure illustrates that extreme exposures still require long-term diagnosis and cannot be used to claim that fully stochastic conditions are calibrated.

All five scenario freezing evaluations can be performed; 0.5s with dq = 0 diagnoses RMSE of about 4.91-10.57 rad/s, which is obviously insufficient. The success kept short in a single case does not meet the standard as generalized/closed-loop control, and the overall validated = false. The purpose of the short course is engineering inspection, not general motions/forces that have been learned.

`supervised_full_cpu_01`: All 82 CPU regressions passed, 48.62 seconds, source code unchanged; including V2 isolation. Later, the audit discovered problems with the P0 layered rounding remainder slot and the evaluation partial failure boundary, which must be repaired in a targeted manner before acceptance. 82 items cannot be used to cover up new counterexamples.


The last two fixes for the main window takeover (after confirming that the pipeline writer has exited): P0 allocates the remainder according to divmod, and all slots have quotas; Replay storage is raised to `bounded-ram-5-active-p0-remainder`, the old layout is explicitly refused to be restored, and the old weight export is still available. When the evaluation fails, the substep does not update the 100Hz history, retains stale feedback/failure diagnosis, and the success criterion is forced to false; non-limited diagnosis is saved in JSON null. `supervised_last_edges_01` passed 26 items, including the 3ms failure counterexample, P0 remainder slot and accurate recovery under real export. The old 82 pieces of evidence will continue to be valid for unchanged modules.


## Final delivery (currently valid version)

- The code is in `unit_bfm/v3/`, and the old V2 source code, configuration and original weight benchmark passed. The network skeleton/FB has not changed, new input, physical randomization, collection, Replay, training/recovery/export/evaluation have been implemented.
- `runs/coordinator_release_01` is the final storage5 and physics integer tick version: 8096 valid W, 101 CUDA updates, E0–E4 mixed, 4 configurations, 66.81 seconds; invalid1, aborted_valid1, 4 actual snapshots, fallback0. There is no change in the production code SHA256 before and after running. Export `export/actor.pt`, `export/b.pt`, and train the weight `final.pt`.
- From its `p0.pt` to `runs/coordinator_release_resumed_01`, the complete endpoint network, target, indicators, Replay tensors and learning random flow are exactly the same, all 8096W/101updates. Evidence`audits/final_release/resume_comparison.json`.
- Real GPU batch physics and learning evidence, 82 CPU full regressions, and the last changed 26 directional regressions have been retained; independent audits accept the final P0 remainder and failed evaluation repairs.
- The default 98304 Replay resources have been measured. The peak RSS saved in the full library is 4.694GB, and the restored resource is 4.664GB. See `runs/coordinator_full_replay_01/checkpoint_memory_01.json`. This does not include all components of the entire training process; partial active row copying costs are still there, and no peak zero is claimed.
- The final five scene dq=0 diagnosis RMSE is about 5.89–13.88rad/s. Some cases that fall into the zero speed threshold for a short time can stop due to hitting the limit, which cannot be interpreted as calling speed control; all runs are still validated=false. Formal long-term training, endurance/speed/maintenance/impeded release capabilities, no structural generalization, and bipedal learning acceleration have not yet been verified.

What was completed in this round was the isolated development, role division, cross-discussion/audit, defect repair and repeatable real training verification required by users. The rest is formal training/capability experiments and full-device throughput optimization. The current short training check cannot be used to pretend that the BFM has been successfully trained. The GPU backend's host transfer per ms is still a clear performance limit.
