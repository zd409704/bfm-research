# V3 pipeline current handover (2026-10-10, final rework)

This document replaces previous cumulative handovers; "Current Development Constraints and Acceptance.md" shall prevail. Minimal functional repairs and CPU directional regression have been completed, source code writing has stopped, and it has been submitted to the main window for real GPU/CPU short training acceptance. No modifications to V2/core/physics/mainwindow tests, no installations, subagents, external messages, authentication reads, or commits.

Environment: host `<dev-host>`, cwd `<project-root>`, Python `unit_bfm/.venv/bin/python` 3.10.12, V3 writable, CPU only for this round.

## This round of implementation list and API

1. Scenario global debts, configure independent debts for each scenario; it is forbidden to share configuration rounds to cause synchronization.
2. snapshot requests to select the group that is actually recoverable and most suitable for debt from the limited pool; use its original SceneConfig to construct the same model environment, and publicly restore and verify the model/process hash; the actual group accounting.
3. Replay checkpoint only active rows; full library shares torch storage, part library gather; resumes taking over/filling field by field and releasing compact data.
4. If P0 expected groups can be put down, group reservoirs, otherwise specify global reservoirs, not infinite expansion or permanent training.
5. collect returns list-compatible `CollectionResult`, even if there is no legal prefix, `collection_diagnostics` is exposed.
6. Save the synchronization boundary, the latest two complete checkpoints; additional P0 reserved for small tests must be explicitly declared.

All of the above have been achieved. Network/FB, current state hierarchical rho, independent and identical structure goal and current B recoding remain unchanged.

API: `collection_schedulers / choose_collection_group / record_collection_group` is a shared implementation for training and scheduling tests. Schedule checkpoint to save `config_E0`… `config_E4`. `Replay.load_state_dict(s)` * * Consume `s['arrays']` * *, you can no longer use the training array in this dictionary after the call; the complete continuation does not depend on the historical archive. `Replay.state_dict()` Writing must be paused during serialization; train is saved synchronously at the batch boundary to meet this condition.

Version: Replay `bounded-ram-4-active`; Training checkpoint `v3-complete-2-active-scene-config`. The old storage/scheduling version is explicitly rejected, the old runs are retained, and it is not pretended that it can be accurately renewed across versions.

## Seven rework results

- **720 Group Scheduling**: full.json five scenes × 144 configuration, 7200 times of 2000 W each, pure scheduling actual access 720/720, 144 per scene. The test calls the production scheduling function, not creating additional access statistics.
- * * snapshot * *: allows switching from an 8-item pool to a cache-compatible group at the time of request, configuring the arrears according to the scenario, and then configuring the arrears according to the scenario; usually, a new group of arrears is still taken. `reset_requested/reset_counts/snapshot_fallbacks` keeps requested/actual/fallback, `config_visits` and scene/config steps record the actual group. The real CPU test confirms that the public restore is called, the first boundary time is equal to the snapshot time, history padding, the subsequent legal transfer, and the actual configuration accounting. It is not claimed that the long-term true recovery rate has reached 20%.
- * * active checkpoint * *: The first dimension of the partial library array is exactly equal to the active number, and storage does not hide the full capacity tail; the full library data_ptr is shared with Replay. load does not call the full library preallocation and then replace it, processing and releasing compact on a field-by-field basis; the RNG/bucket order/goal/next batch of samples is consistent after recovery.
- **P0**: Reservoir by group when there is a configured group that can be dropped; global uniform reservoir when expected is not configured or the capacity is less than the number of groups, public `p0_retention_mode/reason`. Regardless of success, fixed P0 and rolling rule/online capacities remain unchanged. Learning is based on the current partial rho and does not pretend to be a complete conditional distribution; strict still rejects missing groups of expected source/scene/config.
- **invalid**: If the first step is invalid, an empty list will be returned but diagnostics will not be lost. Log failed_worlds, aborted_valid_worlds, unattributed_failures, attempted_world_intervals and up to 8 failure examples. Only failed worlds are counted as failed; single columns of legal peers in the same batch are aborted; previously legal prefixes enter Replay normally. invalid_W/aborted_valid_W/physical_steps of train is also updated when there is no prefix. physical_steps represents the attempted world control interval. All physical sub-steps have been completed when no exception is declared.
- **Default training remains unchanged**: rule32768 (P0 anchor point 16384 + rolling 16384), policy65536; after both sources are combined, the sampling is based on the 50/50 target, and the limited minibatch is not forced to be exactly half and half. Covers continuous statistics/supplementary acquisition, and does not prevent legal standard FB updates; physical validity, field timing, and limited gradient thresholds are retained.
- * * Retention strategy * *: full `keep_p0_checkpoint=false`, P0/rolling/final share the upper limit of the latest two copies, final counts as two copies; smoke/dev = true, P0 plus the latest two copies, up to three copies. Write `checkpoint_retention.json` truthfully. The atom will temporarily have a third managed file while saving the new file, and the old one will be eliminated after success. Delete only the old checkpoints created by this run manager, do not scan or clean up historical runs; resume writing new directories.

## Actual measurement of RAM and checkpoint

Actual physics p4822+memory243, total p5065. The default 98304 slot requires 4,096,917,504 B of FP32 tensors; adding a 512 B/slot index budget and two batch512, the Replay startup estimate is 4,189,925,376 B (3.9022 GiB), which is lower than the 4 GiB hard threshold. The simulation batch temporary storage is estimated and limited to 512 MiB; the interpreter/network/optimizer does not belong to the Replay budget. Some library saves require an active gather staging and do not claim that the entire process is always under 4 GiB.

This round of measurement is **synthetic data in the actual schema dimension, non-physical throughput test**. The capacity is 1/8 of the default: rule4096, policy8192, a total of 12288 slots; separate new processes save/restore.

| Active slot | Necessary array storage | checkpoint file | Save RSS increment | RSS after new process resumes | Save/restoration time |
| --- | ---: | ---: | ---: | ---: | ---: |
| 3072 (1/4 active) | 128,028,672 B | 128,256,401 B | 123.67 MiB | 584.08 MiB | 0.091/0 .124 s |
| 12288 (full) | 512,114,688 B | 512,983,274 B | 10.66 MiB | 956.91 MiB | 0.296/0.284 s |

Some libraries have restored a high water level of about 641.96 MiB, reflecting field-by-field replication and temporary storage; full libraries are directly taken over. VmRSS and ru_maxrss are collected by different kernel interfaces, and the original readings are retained. Their small differences are not used for additional memory guarantees. The next batch of training tensors, goals, IDs, and probability SHA256 of the two groups after recovery are exactly the same. There is no test of the default full capacity 4 GiB process peak; resource acceptance is arranged by the main window.

Evidence directory: `unit_bfm/v3/runs/pipeline_active_checkpoint_vp3yEE/`: `measure.py`, `measurement.json`, four staged JSON, partial/full.pt, regression log, source code SHA256. Command (please copy the script to a new directory to run again to avoid overwriting this evidence):

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python unit_bfm/v3/runs/pipeline_active_checkpoint_vp3yEE/measure.py save partial
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python unit_bfm/v3/runs/pipeline_active_checkpoint_vp3yEE/measure.py load partial
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python unit_bfm/v3/runs/pipeline_active_checkpoint_vp3yEE/measure.py save full
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python unit_bfm/v3/runs/pipeline_active_checkpoint_vp3yEE/measure.py load full
```

# Test commands and results

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest unit_bfm.v3.tests.test_pipeline_final_revision unit_bfm.v3.tests.test_integration_ram unit_bfm.v3.tests.test_pipeline_ram unit_bfm.v3.tests.test_pipeline_contract unit_bfm.v3.tests.test_pipeline_real -v
```

**33 tests / 7.027s all passed**, `regression.log`. Contains main window read-only `test_integration_ram` 4 items, 720 group scheduling, P0 degradation, active storage, first step invalid real train control flow, over-capacity/no disk sampling, probability/goal/accurate sampling recovery, real CPU E0–E4 collection/FB update/export, 96W smoke accurate checkpoint continued training with the same version.

Finally, a real snapshot interface test was added to run separately:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest unit_bfm.v3.tests.test_pipeline_final_revision.FinalRevisionTests.test_selected_snapshot_really_restores_with_padding -v
```

**1 test / 0.225s passed**, `snapshot_test.log`. A total of 34 different tests have been passed in this round; no 3200W training was repeated.

The previous engineering evidence is still retained: `runs/pipeline_ram_frozen_process/comparison.json`'s 3200W/37 update and 1600W boundary are accurately restored, and the old checkpoint cannot be input as this new storage version; `pipeline_ram_calibration_02` is a light/heavy × P/D × two corners with a total of 8 points and the rule remains passed; `pipeline_ram_warp_cpu`/`pipeline_ram_mjlab_cpu` It is a real CPU two-world back-end collection. They are not new code GPUs or full conditional acceptance for this round.

# SI Diagnostics and Operable Entrances

coverage Read-only physics disclosed `contact_normal_force_N`, `adjacent_max_abs_dq`, `adjacent_max_abs_tau_Nm`, `adjacent_declared_capacity_Nm`, `adjacent_axes`, `fixture_P/D_force_N`, `fixture_P/D_torque_Nm`, `applied_load_norm_N`, `solver_valid`; do not guess old field mappings, do not use full geom contact instead of research unit contact, and do not use fixture OR contact to impersonate joint conditions. The rule qref (t) is paired with response (t +1); the real E0–E4 test missing_diagnostics is empty. The semantics shall be governed by the contract between physics and the main window "Module Interface and Division of Labor".

Existing access is maintained: `train --mode smoke|dev|full --run-dir <new-directory> [--resume checkpoint]`;  `collect --config ... --output <new-directory> --episodes N --backend cpu|mujoco-warp|mjlab --physics-device ...` ; `programs --config ... --output <new-directory> --quick` calibration;  `evaluate --run-dir ... --output <new-directory>` ; `interface --checkpoint ... --output <new-directory>` Export. Use `python -m unit_bfm.v3.<module>`. Training in GPU physics was designated by JSON physics.back/device, and set up by Actor to study device; No quiet fallback. No F extra p is exported, but tau is still an accurate simulation of privileged telemetry, Hardware_validated=false.

## Documents and remaining acceptance

This round of source code/configuration changes: `replay.py`, `collect.py`, `train.py`, `configs/{smoke,dev,full}.json`; new `tests/test_pipeline_final_revision.py`; rewrite this handoff. The remaining pipeline modules follow the existing implementation. `source_hashes.json` records the delivery version and the read-only core/physics version to facilitate identification of concurrent modifications.

Main window to be accepted: real CUDA batching/learning and CPU pairing, default full-capacity RSS, long-term snapshot ratio, final coverage/regular wide-angle accessibility/control skills. Multiworld is still choreographed for bounded episode batches with physics host, and does not claim high throughput or tick-by-tick streaming has been completed. This round is to complete the minimum repair and stop the source code writing. It does not replace the delivery with full blocked, nor does it declare that the 20m effect has been accepted.
