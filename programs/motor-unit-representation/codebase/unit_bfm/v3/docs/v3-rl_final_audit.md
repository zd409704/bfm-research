# V3 Bounded RL pipeline independent CPU audit (delivered in this round)

2026-10-10 09:03–09:14 UTC. According to "Current Development Constraints and Acceptance.md", the old full archive performance requirements are no longer used as training acceptance. See `v3-rl_design_review.md` for advance design. Only modified two of its own reports, temporary script/output only in `v3/runs/rl_audit_unique`; no code modification or developer testing, no GPU, installation, certification, commit, sub-agent.

Environment: host = <dev-host>; cwd = `<project-root>`; uses `unit_bfm/.venv/bin/python` 3.10.12; OMP/MKL = 1; PYTHONDONTWRITEBYTECODE = 1. Start MemAvailable around 11.60 GiB on a conservative budget of 11GiB. Other modules are developed concurrently, and each of the following is subject to the reproduction hash.

## in conclusion

The new main path has been changed from full episode archiving to **fixed capacity RAM transfer, incremental bucket index, memory sampling, and legal partial rho can also be updated**. Independent CPU evidence supports core engineering directions: invalid rejection, over-capacity elimination, no disk sampling, independent matching goal, recovery of next learning update, real 96W/6 updates, complete fresh/P0 recovery, the network and target are completely consistent. No need to wait for all coverage status to be completed before learning.

**It is not recommended to directly amplify long training**: The P0 protected area currently only saves the last segment of P0 and is not retained by group layer; the complete recovery peak value of the default capacity has not been measured, and Python pickle may cause additional copying of large numpy arrays; the collection still temporarily stores the entire multi-world episode, and the length of num_worlds/episode needs to be budgeted or divided into shorter rollouts; some cost/failure statistics and actual snapshot hits need to continue to be tested. They are reserved contract/resource/acquisition engineering issues and do not require changes to the network or FB, nor do they require all random states to be covered before running the development short training.

## Last full training recovery trial version

The hash is exactly the same before and after running in `resume_result.json`:

| Module | SHA256 |
|---|---|
| replay | d4fcdff4bc8ddd1f69c232c34300827f3e123042747ba9f2877cf20d58e1743b |
| train | 07b32feb4b2d3b3c60339fbae7177c526c305e53fc519fb006e84be69bad357e |
| collect | 87fb0e19152eb43d0866fee4571feff67ec424f2bef38209b2b04c760753e9ca |
| physics | 8dff973ef8413b767a44f485899045b611a5cf756ede177226f0d52412d9acc7 |
| privileged | 8989b8dade0168def0da8aabf0399391809b8eba92efbaa0c2e5968e6cff0d38 |

09:14 Before submission, the physics changed to `4ed22b6ce0b6fe71ce5590283a699da9dbdc6a309bf21ff6b28858240bb24cf3`; the new hash was not used to pretend that the last complete recovery had been re-verified. The remaining four modules above remain unchanged. queries=`78e040805ba7281d465f3f5e40473e47185c7e77c1fb0125bff1a9bbd3e1bf8a`, features=`6bbfc9a965415dbd13009c8def663e2abb75c8dbd0d5c3e49bd3b96283f38e1d`.

# Independent Verified Items

### 1. Bounded writing, elimination, rho and fileless sampling

Script `runs/rl_audit_unique/audit.py`; the first/second output is `result.json` / `result_latest.json`, and the front and rear module hashes are saved respectively.

Capacity rule17 + policy23, a total of 60 7-step synthetic legal episodes (420) are written. Active Stable 40; only the last surviving ID is drawn. After blocking `builtins.open`, `np.load`, `gzip.open`, you can still add/sample (512), proving that the actual path does not read the compressed/archived file, but only the memory_report. Two source single bin fixture, return edge probability and `.5/source_count` maximum difference 0; length/limit of goal_g always matches x. Manual insertion of raw [3] .valid = false but explicitly valid all true was rejected by `valid mask admits invalid raw transition`.

After the ring is overwritten, the state is restored, and all batch tensors/IDs in the next 32 lines are consistent; after continuing to restore the learner, the next update metrics are completely consistent. Only 40 slots are verified here, **the entire 4GiB library is not allocated or the RSS of the large library is claimed to have been accepted**. The new bucket updates four families and goals for each insertion/deletion. The old O (full database) reconstruction has exited Replay, and sampling only scans a limited group/bin table and N rows; the complexity changes from full database reconstruction to O (new transfer × 5) index update, O (N) sampling plus O (N × p_dim) gather.

## 2. The old cross-cub counter for searching for caches is really fixed

The two Replays of the first version of RAM each have revision=1, the same list but different g, `QueryPool.assert_current` has accepted the error pool; after adding instance_id to `replay=9fcf859...`, the same independent counterexample returns rejection (result_latest: foreign_rho_cache_accepted=false). The instance_id is saved and restored with the checkpoint, and the revision is advanced with the insertion. Do not continue to report this first version issue as unfixed.

This does not mean that any external modifications to the array will be detected; active arrays cannot be modified directly under the normal API. If there is asynchronous cache/multiple writers in the future, the effective generation still needs to be included in the immutable sampling snapshot.

### 3. Real CPU training is no longer blocked by coverage_ready

`smoke_01`: W96, P0=24, online36, 6 updates, invalid0, rule27/policy21 gradient lines, about 2.97s. Coverage_ready=false still performs legal optimization; new Replay capacity is 192, no raw resident, no disk sampling.

Then run the frozen import version of `resume_check.py` in the same process: fresh_02 and resume_02 restored from its p0.pt are both updated 96/6 times/invalid0; the final online parameters and target parameters of tensor by tensor `torch.equal` are all True, and the last_metrics are completely consistent. Finally active92 (rule56/policy36), P0 retains 24. It is verified that the **actual train checkpoint** is not just a retelling of the learner test.

For the first time, cross-process resume_01 happened to encounter a concurrent storage_version upgrade from bounded-ram-1 to bounded-ram-2-p0, and the old checkpoint was explicitly rejected; this was a correct version rejection and was not listed as a recovery defect. Later, the same version of fresh/resume was passed independently.

### 4. Snapshot’s strict process/history separation has passed a real example

`result_latest.json` record: E0 runs to physical t = .05 seconds, snapshot→ same action continues directly; restore (snapshot, episode_id = 7)→ FeatureHistory.reset→ same action. restore time still = .05, interval_valid = false, acc_valid = 0; next q/dq/p difference all * * 0 * *. Without resetting the process clock to 0, historical padding and physical process continuity have been satisfied simultaneously.

physics restore also maintains_episode_start_time, the new time truncation length is relative to the recovery boundary, and the source code is consistent with this semantics. The above is a single sample, not the same as all touch/multi-drive/Warp state accuracy acceptance. pipeline has added a limited snapshot_pool (8 items), not an unbounded snapshot archive.

# # 5. Early F-state gaps and failure isolation have been measured and repaired

`physics_check.py` / `physics_check.json`: E1 only changes support_k, reset p difference=.5207251241, the old identical p counterexample has been eliminated; E2 reset outputs floor.present=1, M series floor.offset=1.2m. `audit.py` injection saves qacc NaN, _validate_solve explicitly rejects it; a new PhysicalInvalidTransition is added to separate invalid values ​​from ordinary terminals. A universal Markov proof has not been given for all possible process states, nor has this been regarded as the threshold for RL operation.

# Now pending and reasonable advice

### P1: Although P0 has been protected from subsequent overwriting, it still only retains the last P0 fragment, not a hierarchical P0 sub-library.

Currently `Replay.p0_capacity=rule_capacity//2`, P0 is written only in p0_cursor loop, and the half area is protected after p0 ends. The protection behavior has been truly corrected: subsequent rules will not overwrite P0; **P0 phase itself is still FIFO, not hierarchically reserved**.

Independent `p0_check.py`: rule16, 8 slots in P0 area, 7 entries in each of 8 different groups, a total of 56 P0 entries. Finally, the P0 group is only group6/group7; then 12 more online rule episodes are added, still only protecting these two groups. Result `p0_result.json`, hash=d4fcdff…. The actual combination of 720 groups, 16K P0 protection capacity and 1000 episodes will only protect the last few groups, instead of about 22 in each group.

Specific minimum modification method: confirm the fixed P0/rolling rule split ratio in the main window (the code is currently privately determined in half, and should be entered into config); the P0 area is allocated a limited quota for each (scene, config), and the reserve is evenly distributed according to the cumulative visits within the group, and has nothing to do with success; if the bin reservation is required and the explicit selection strategy in the existing key family is required, the complete episode is not required. When the capacity is insufficient for all expected groups, partial support, supplementary acquisition/adjustment is reported, and the capacity cannot be expanded to two episodes/groups. The rule + online is still 50/50, and sampling can be done from the actual surviving set according to the original rho.

This is the gap in this round of bounded P0 contracts. It does not require all coverage to be learned. Short-term training can continue to verify; it must be completed before officially claiming "fixed P0 layered coverage retention".

### P1: The full capacity checkpoint/RSS peak value has not been accepted; the final candidate capacity only has about a hundred MB subsystem margin.

The current total p=5065, the current+next tensor of 98304 slots is about 3.81555GiB. The latest estimation formula has added 512B/slot and two batch512, which is about 3.90GiB; it is more accurate than the first version which only estimates tensors, but the temporary storage of simulation episodes is not included in this item. Exceeding 4GiB should remain rejected, and the final schema cannot inherit the old budget of 4777.

state_dict has been changed from copying active large arrays to direct references, which is acceptable for synchronous saving; it cannot be safely saved during asynchronous writing to the library. This restriction must be clearly documented. load avoids copying data by taking over loaded arrays, but still calls _allocate first and then replaces it; even if numpy zero pages are usually not physically committed, it is recommended not to pre-allocate a large placeholder library during construction.

More importantly: Replay in the `torch.save` object is a numpy ndarray, and the default pickle may construct extra bytes for a large ndarray; this round only runs small libraries, and it cannot be declared that the 4GiB storage peak value is low just because state_dict is not copied. Minimum choice: checkpoint converts numpy arrays into shared memory CPU torch.from_numpy tensors for torch.save storage path, and load takes over the corresponding CPU storage; or field-by-field sharding atomic checkpoint. **No fallback to full track archiving/compression system**. Observe the RSS using a proportionally increased memory benchmark (for example, 1/8 capacity), then estimate/accept the target capacity, arrange resources in the main window and then execute; this round has not touched the upper limit of available memory of about 11GiB.

# # P2: Multi-world acquisition is still staging the full episode, it is necessary to clarify the upper limit of rollout, not deny its RL correctness

collect_batch internally saves each world raw/known/fs/actions to max_steps before Replay.add; old episodes are not held for a long time, and the current temporary volume of 2 worlds×1000 steps is limited, so it should not be said that it is still doing full permanent archiving. But it is not a strict step-by-step flow; if num_worlds continues to enlarge, raw FP64 physics p+FP32 ep.p+x/g/existing memory is repeated, and the temporary amount grows linearly with worlds×horizon×p.

It is recommended that the first version fix the num_worlds, restrict the collection of horizon and include the suspense budget in the start-up inspection. The next step could be 32 - 128 steps rollout to continue the transfer of pairs, retaining each world22ring and behavior z cross rollout; The collection cut-off is a Bootstream cut-off without replacing physics/historical/z. There is no need to create complex cross-nodes for version 1 and not to write the correct 96W update because it has not yet been written by tick.

### P2: The hit rate of 8 items in the snapshot pool matching 720 configuration may be close to zero. It is only for diagnosis and cannot be stuck in learning.

The current train only uses snapshot when it has the same scene/config in the pool, otherwise it will fall back xi and count actual_reset. When rotating evenly across 720 groups, 8 items are usually eliminated before accessing the configuration again, and the 20% target may not be reached for a long time. Because the program memorizes the true fallback, * * it is not a forged recovery * *, and it should not prevent legitimate xi/velocity learning.

Minimum measure: count requested/actual reset and fallback; if 20% snapshots are really needed, you can continuously arrange snapshots of the same model in small batch configurations and then cut into groups, or allocate a bounded per-configuration snapshot index/appropriate amount of cache. The collection schedule should be selected from the main window to prevent the snapshot target from automatically expanding the pool/Replay.

### P2: 50/50 behavior and failure costs must be calculated based on effective steps, not just world parity allocation

The current train is divided into sources according to the odd and even world/episode, which is equal to 50/50 when the bucket lengths are the same; there is a source scheduler.record but the source selection has not yet used choose, and the effective step ratio cannot be guaranteed when the invalid/early-end lengths are not equal. 50/50 sampling is established after the two sources of Replay itself are non-empty; it is necessary to separate the behavioral cost and gradient distribution, do not confuse them and say that both are accurate 50/50. The first version can use the accumulated effective step balance to allocate sources to the next world.

When collect_batch fails, it is the correct choice to truncate the unknown next and retain the previous legal prefix; however, the exception branch truncates all prefixes, and the number of failed sub-steps and .exception.diagnostics persistence are not necessarily included in invalid_W. The result invalid0 cannot be used as proof of no failure. Just add the failure count/limited diagnosis, and do not insert the failed terminal lines back into the gradient.

# Executable evidence orders #

All paths are temporary directories exclusive to this audit, and existing products will not be covered. Please change the unique run subdirectory when re-running the training script.

```bash
PYTHONPATH=. OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
unit_bfm/.venv/bin/python unit_bfm/v3/runs/rl_audit_unique/audit.py
PYTHONPATH=. OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
unit_bfm/.venv/bin/python unit_bfm/v3/runs/rl_audit_unique/p0_check.py
PYTHONPATH=. OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
unit_bfm/.venv/bin/python unit_bfm/v3/runs/rl_audit_unique/physics_check.py
```

The complete fresh/resume script of the same version is `resume_check.py`, which creates fresh_02/resume_02 and has been successfully executed. If you rerun, you must first change the unique output name in the **Audit Script Copy** and cannot overwrite the existing run. Evidence JSON: result.json, result_latest.json, physics_check.json, p0_result.json, resume_result.json; real operation log smoke_stdout.txt/resume_check_stdout.txt.

`audit.py` is an audit probe, not a production test, partial direct state injection is only used to verify the deny/isolate path. After result_latest, the P0 area has been modified as a protection partition, so "p0_still_active=false" belongs to the old version of evidence; the current P0 problem is expressed as "only the last group is retained" in p0_result, and it is not repeated to claim that subsequent rules still cover P0.

## Main window handover

Bounded memory main chain and the above CPU small-scale engineering evidence can be accepted; this round of design/audit has been substantially completed, not only the list of missing items. Prioritize P0 hierarchical reservation + memory peak, and then promote more legitimate CPU/GPU rollout. GPU/large-capacity RSS/long training/control skills have not been accepted by this agent; old V2, network skeleton and FB losses have not changed. No need to wait for all 144 × 5 × rare bins to be complete for valid data optimization.


## Formal rework independent re-inspection: stage design (in progress)

Time: 2026-10-10T09: 29:37.119536+00. Range by `.ssh/relay-agents/agents/v3-pipeline/final-corrections.md`; This round only reports and `runs/rl_audit_unique/` new evidence is available, CPU, no source/test modification. The former Hashi ' s defects are not automatically considered current; The following results are checked first.

It is planned to use short probes to verify: (1) configure the P0 reservation/partial of all 720 groups, insufficient capacity and undeclared groups; (2) 7200 times of pure scheduling coverage and snapshot compatible pool real restore calls, and actual group accounting; (3) the tensor storage size of the active checkpoint, the exact recovery of the same version of RNG/rho/goal/after the retirement, and the latest two reservations; (4) the first invalid and mixed world failure diagnosis, so that invalid subsequent gradients are not allowed; (5) 1/8 candidate capacity CPU checkpoint measurement, which does not account for GPU and does not repeat the full library resource acceptance of the main window. Network/FB hash before and after this round of recording. Concurrent changes use hashing to qualify the evidence, and do not report incomplete interfaces as accepted.


# Official Rework Independent Review Conclusion (2026-10-10 09:30 – 09:33 UTC)

* * Five rework master functions have independently passed short CPU counterexamples; newly discovered P1: P0 hierarchical quota balances are permanently empty, allowing checkpoints close to full libraries to continuously replicate almost the entire Replay. This affects the acceptance of resources and does not constitute a reason for partial valid data to prohibit learning. * * This section covers the previous P0 FIFO, full-capacity checkpoint, snapshot low hit, first step invalid silence and other conclusions. The source code/test has not been modified; there is no GPU, no training run, and no long polling; only write this report and audit exclusive new evidence.

Environment: host = <dev-host>; cwd = `<project-root>`; Python = unit_bfm/.venv/bin/python 3.10.12; command settings CUDA_visible_devices = '', PYTHONDONTWRITEBYTECODE = 1, OMP_num_threads = 1, MKL_num_threads = 1. Uninstalled, unread certifications, uncommitted. The read .ssh path is only a rework instruction file explicitly authorized by the user.

### Fixed and independently verified

| Project | Direct evidence and results of this round |
|---|---|
| 720 cross-scheduling | Production collection_schedulers/choose/record function, 7200 rounds, 2000W per round: 720/720 groups, 144 configurations in each of the five scenarios. After adding a simulated snapshot pool of real size 8 and 20% of requests, it is still 720/720; the compatible pool item is selected for 1440 requests, and the actual reset count is xi3600/velocity2160/snapshot1440. This is a scheduling probe and cannot pretend to be a 720 group of real physical collections. |
| P0 layering/freezing | 720 groups, P0 capacity 1440, each group has exactly 2 items, subsequent rules are written into uncovered anchor points. No expected_configs is changed to global_reservoir; the expected group with insufficient capacity also clears global_reservoir, seed 90 reserves episode 1/3/6/7/8/9/40/43, non-end FIFO. |
| partial/strict and loss | When the missing configuration is missing, partial samples normally and executes Learner.update; strict explicitly throws EmptyReplayGroup. The two sources 50/50 are still given by the current rho; there are no new loss or network parameters. |
 Active checkpoint  100 tv active at 13, all tensor.shape[0]=13 and the byte number of storage strictly equals the active element and does not hide the big Backing story. Torch store save instead of numpy pickle.  |
| Same version recovery | After the production save_checkpoint/read_checkpoint is placed, the Replay elimination sequence and the next 64 rows of ID/tensors/rho probability/goal are exactly the same; all metrics of the next update of the Learner are exactly the same; and the tags after the P0 reservoir is inserted are also exactly the same. This time to verify the real checkpoint API, the complete train.run has not been run; the complete integrated continued training will be accepted by the main window. |
| No disk sampling/invalid/goal | Blocking builtins.open, numpy.load, and gzip.open still sampled successfully; raw.invalid cannot be re-enabled with an explicit full true mask. After regenerating the legal mask, it becomes invalid and the two adjacent lines are not drawn; the goal length/limit match. The foreign library query pool was rejected. |
| First step invalid | Failure injection after real CPU dual world step world0 valid = false/p = NaN: The first step returns 0 episode, but there is evidence that the public diagnostics are failed = [0], aborted_valid = [1], attempted = 2, and limited failure_examples. Step 3 When it expires, the two worlds each retain the first 2 legal transfers, p all limited, invalid and subsequent did not enter Replay. |
| snapshot actual restore | Real CpuBatch first round takes a snapshot t = .01 in 6 steps, and the next round actually calls batch.restore once through collect_batch (reset_snapshots =...); the initial physical time is still = .01, interval_valid = false, acc_valid = 0, the next 3 are legal, metadata.reset_snapshot_used = true. The integer tick/GPU acceptance was not redone. |
| checkpoint retention | CheckpointRetention is actually written to the small placeholder file: keep_p0=false, only rolling2+final is left; true means these two plus additional p0, and the manifest declares it truthfully. Old runs are not cleaned up. |

The test_integration_ram and developer test_pipeline_ram owned by the main window are rerun by this agent: * * 11 tests/0.766s/OK * *. Not a reference to a developer handoff. The log is ram_regression_03.log. The old core bridge public add compatibility change was not touched.

### P1: The tiered quota loses the remainder, and the full database zero-copy can never be triggered.

Location: `size=self.p0_capacity//len(self.p0_groups)` and `offset=group_number*size` in replay.py Replay.add, `len(slots)==self.capacity` branch in Replay.state_dict. See the table below for current hashes.

Minimal counterexample p0_remainder_probe_01.py: rule10/policy10, P0cap5, expected group a/b/c, fill in the scrolling rules and online after writing 16 P0s each. Results P0 is only 3, and the slot 3/4 is permanently empty; the total active18/cap20, all seven checkpoint tensors are not zero-copy. The default P0cap16384/720 group is 22 per group, only 15840 is active, * * 544 slots are permanently empty * *; the actual maximum is active97760/98304. In the P0 stage, it is forbidden to fill in the anchor points in the future. Even if the total acquisition W continues to grow, it cannot become full.

This is not a problem of only losing 544 entries: state_dict does `v[slots]` to the partial, so each save of the official long training copies an additional large array of about **3.794GiB** instead of the about 10MB metadata increment of the full slot. You cannot rely on "full shared storage" to declare the default configuration long-term checkpoint low peak.

The specific minimum modification method (determined and implemented by the pipeline/main window, this agent has not changed): use `base,rem=divmod(p0_capacity,num_groups)`, the jth group size=base+(j<rem), offset=j*base+min(j,rem), so that all P0 slots have legal quotas, the reserve and rule in the group are still unified rho, and checkpoint replay retains the same mapping. **If P0 prefill is not enough to fill the quota, partial replication will still occur; remainder repair does not mean eliminating all partial peaks. ** In the first version, current Replay+active checkpoint copy can be explicitly included in the main window resource budget, or the official save path can be written out in bounded field order; it does not require a new compressed archive structure, no modification of FB, and no requirement for 720 groups to be updated before updating.

Actual measurement of 1/8 candidate capacity (p_dim5065, CPU, two independent processes):

| Scenario | active/capacity | checkpoint file | RSS before saving | RSS/sampling peak when saving | Conclusion |
|---|---:|---:|---:|---:|---|
| Quarter active | 3072/12288 | 128257427 B | 614969344 B | Peak 746135552 B | Compact replicates around 128MB, as expected |
| Really filled | 12288/12288 | 512982700 B | 1003155456 B | Peak 1013530624 B | arrays shared storage, 0.299s saved |
| actual 720 layered remainder | 11680/12288 | 488079085 B | 977571840 B | 1476186112 B after saving | compact extra 486775680 B, 0.626s saved |

Full slot loading: release the old Replay first, RSS490188800 B before load, 1006305280 B after torch.load, 1007669248 B after recovery, arrays are consumed item by item, active12288. It proves that the small-scale path does not copy another full database; it does not claim that the full capacity peak value has been accepted. The 1/8 capacity 720 group P0cap2048 can only reserve 1440 slots, leaving 608 slots permanently empty, so the counterexample is more obvious than the default. Physical schema, model/optimizer, acquisition buffer, system page cache and other processes in the main window need to be included in the complete resource acceptance.

# # Acceptance and diagnostic boundaries not yet

- This round has not confirmed the complete 20M training, control skills, full library RSS or GPU; the completed integer tick in the main window and the five scene 200W/40 updates are not repeated. Existing legal short training will not be declared invalid due to these non-covered items.
- 720 scheduling and snapshot actual restore are directly tested separately, and the long-term hit rate has not been verified with 720 real configuration continuous acquisition; failure rate/pool compatibility requires the actual count of the main window short training. Pure dispatch 1440/1440 cannot be used as the actual physical hit rate.
- The first step invalid and the third step mixed-world have passed. When the backend only throws an exception without world_id, the program has an unattributed_failures branch. This round does not provide full backend proof for this branch, and does not treat the unknown peer health status as known.
- Collect_batch is still the only remaining episode; There is already a rollout budget check for the worlds xhorizon xp in the train. There is no conclusion that a new fluid structure is necessary to allow legitimate partyial to learn.

### Current round files, commands and versions

All new evidence is in runs/rl_audit_unique: final_corrections_probe_01.py/.json/.log, probe_01_checkpoint.pt, retention_probe_01/, ram_regression_03.log, checkpoint_memory_0 1.py/.json/.log, memory_01_quarter.pt, memory_01_full.pt, p0_remainder_probe_01.py/.json, checkpoint_remainder_memory_01.py/.json/.log, memory_remainder_01.pt. Keep evidence and do not roll back or delete other people's files.

```bash
# The following script has been executed; re-running the script with create-exclusive output must be copied to a new number and the audit output name must be modified.
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' unit_bfm/.venv/bin/python unit_bfm/v3/runs/rl_audit_unique/final_corrections_probe_01.py
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' unit_bfm/.venv/bin/python -m unittest unit_bfm.v3.tests.test_integration_ram unit_bfm.v3.tests.test_pipeline_ram -v
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' unit_bfm/.venv/bin/python unit_bfm/v3/runs/rl_audit_unique/checkpoint_memory_01.py
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' unit_bfm/.venv/bin/python unit_bfm/v3/runs/rl_audit_unique/p0_remainder_probe_01.py
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' unit_bfm/.venv/bin/python unit_bfm/v3/runs/rl_audit_unique/checkpoint_remainder_memory_01.py
```

The following SHA256 is the same before and after the main probe; the replay/train/collect and network/loss/learner end at 09:33 are still the same. The network, FB, and Learner have the same hash as the start of this round.

| Module | SHA256 |
|---|---|
| replay | `794cb63d578f4826dab54940d854c677302e5fcd67f53e4894758fa0d0eaa97e` |
| train | `56d2bcf9745feaf204728a421917ca1a81273557bc86861c671b7b6f87d2b96c` |
| collect | `d6a42d0203f2b6efd27a74733a6907baf3ab308f3ebe2951360b4af5d3c25edd` |
| programs | `e3bf9b45136bd426f469ad32c595ccd583186d10e1be3f0b25472305373b4671` |
| queries | `78e040805ba7281d465f3f5e40473e47185c7e77c1fb0125bff1a9bbd3e1bf8a` |
| physics | `6d5a9489f15cd2ea431d963521ffecb31a906ef6bc486d650d424a9e95c66271` |
| privileged | `2505b1fc6f4bf862843a12ad1a496bee6a275e87bcf86bca0956e069accbc4c5` |
| schema | `738fd5d2add0db71750653d001053056de3b032c0c2ea1af3926e735d2df98e6` |
| features | `6bbfc9a965415dbd13009c8def663e2abb75c8dbd0d5c3e49bd3b96283f38e1d` |
| networks | `024514d815ad7133431a2cca51f78ae484ad47071f4ca859287248bb87709454` |
| fb_loss | `8fc2fd44b79300dcc7c886c3a999d1021242dadc264fff1400c5ebf1748f8a7b` |
| learner | `85d4f763316c9b9785e4cda86749a503de6bc00140d06e9649a48890150519b5` |

Handover: The five rework items can be accepted according to the above clear scope, retaining the P1 surplus/partial checkpoint resource risk, and coordinating with the main window; this agent has not repaired it without authorization.


## The last two repairs and re-inspections of the main window (2026-10-10 09:38–09:40 UTC)

** Final increment conclusion: this restricted replay divimod quota/storage5 and evaluate lapse substep treatment is acceptable; No new blockage logical errors were found to have been introduced into the two changes. The P1 in the preceding section, “P0 excess resulting in the default permanent emptiness of 544 slots”, has been repaired and should no longer be the current failure item. ** Actual resource costs for reproduction of active Tensor when partial is not fully filled still exist, with the retention window eventually blended short training/resource acceptance. There was no re-testing of long experiments, GPUs or full-stock resources in this round.

Version note: replay.py/evaluate.py are all untracked files in the current Git. `git diff -- ...` being empty is not evidence of "no changes"; this time, the current source code is directly reviewed, and the front-round hash/counterexample is used for behavioral comparison. There is no fictitious Git baseline diff.

### Directly verify the results

- Reload the full `unit_bfm.v3.tests.test_integration_final_edges` as required by the main window: **2 tests, 0 failures, 0 errors, 0 skipped**, coordinator_mixed_01/export actually exists. The test assertion or source code has not been modified; the default temporary directory for testing is next to other runs. This agent only redirects the dir of tempfile.mkdtemp to the audit authorization directory during execution. The evaluation still uses the real frozen Actor/B, query pool and evaluation spec.
- The new quota for P0cap5 and Group 3 is a=2/b=2/c=1. The offsets allocated by divmod are continuous and do not cover each other, and the sum of sizes is equal to cap; if the capacity is insufficient, the expected group will still use global_reservoir, and no zero quota group sampling error will be introduced. After filling the rule/policy, active20/20 and state_dict share all seven tensor storages, and the original minimum counterexample is closed.
- Supplementary verification of continued collection of the same version: After saving and restoring, continue 12 rounds of a/b/c, each group has 7 P0s in each round. The tags are exactly the same item by item. It is verified that the quota mapping, seen count and RNG are restored together. storage_version is `bounded-ram-5-active-p0-remainder`; when the same state is declared as `bounded-ram-4-active`, `ValueError: incompatible RAM checkpoint` is thrown immediately, and the old version is rejected before changing the object. There is no silent reinterpretation of old quotas.
- Partial checkpoint still only contains active rows, and the number of tensor storage bytes is equal to the actual elements; the previous statement of "save the entire capacity" does not apply to the current hash. The old P0 FIFO/full capacity statement must also not cover this round of actual measurement.
- The second step failure of the real UnitEnv was injected into physics_tick13: Interface.observe asserted valid passage (no call to observe for failed borders); Case classification = numerical_failure, access = false, case JSON.gz retains fair _reason and diagnosis, feedback.stare =true and acc_valid = false. The failure was not due to the fact that hestory requested a complete 100 Hz partition to break down the report.
- The np.ndarray/np.float64/nested tuple of finite_json contains NaN/+Inf/-Inf and is converted to JSON null; `json.dumps(...,allow_nan=False)` is successful. Fault case file reads back successfully with a JSON parser that rejects non-standard NaN constants. This supplement proves the serialization function without creating another full physics NaN solution experiment.

### Boundaries and remaining matters

This evaluate failure records is filtered out of the indicator and includes invalid time access = false at any stage; Saves the old feedback clearly tags shale and does not treat old feedback as an effective new response. Case compressed diagnosis uses Finite_json+allow_nan=False; Ultimately, the report.json is still in plain/json.dumps, and the currently validated failure indicators are limited or non-one, and therefore the failed path passed does not export NAN. Do not expand this conclusion to include all extreme overflood indicators; There is no independent recurrence of such reporting anomalies, which are not listed as new disruption deficiencies.

storage5 rejects the old Replay as an intentional version boundary, and the old storage4 checkpoint cannot be accurately continued; recovery of the same version has been verified. The main window is still responsible for the peak budget and final mixed run of partial replication, and all 720 groups are not required to be resident as a prerequisite for learning. The network/FB hash is the same as the previous round.

### New evidence and recurrence

Only `runs/rl_audit_unique/final_edges_review_01.py`, `.json`, `.log` and `eval_failure_*` evaluation output in this directory are added; only this report is updated. The script uses unittest loader to run the original test, and additionally verifies storage rejection, P0 continued recovery, partial storage and JSON purification. Run command:

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' unit_bfm/.venv/bin/python unit_bfm/v3/runs/rl_audit_unique/final_edges_review_01.py
```

The source code hashes before and after this round are exactly the same:

| File | SHA256 |
|---|---|
| replay.py | `a031d4967baf46c2b21b43541d7d22783cba8e92256042d70d1ed24c8b517ea7` |
| evaluate.py | `06e78e7fc178ec90b3d63566488760ad11324f517651c2b77393395ab25b2173` |
| networks.py | `024514d815ad7133431a2cca51f78ae484ad47071f4ca859287248bb87709454` |
| fb_loss.py | `8fc2fd44b79300dcc7c886c3a999d1021242dadc264fff1400c5ebf1748f8a7b` |

Final handover: Remainder P1 has been closed; the two modifications have been independently re-verified by the CPU, and the source code/network/FB has not been modified by this agent. Keep the partial resource acceptance boundary and wait for the final integration result of the main window.
