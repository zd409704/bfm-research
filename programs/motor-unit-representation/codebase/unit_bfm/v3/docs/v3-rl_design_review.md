# V3 Bounded off-policy FB/RL Phase Design Review

Starts at 2026-10-10 09:03 UTC. Role: Discussion first, then independent audit; this report is a suggestion for the main window decision and pipeline implementation, and does not modify the interface, algorithm or code without authorization. Based on the "Current Development Constraints and Acceptance.md", the old full permanent archiving/compression capacity threshold/incomplete coverage prohibition optimization requirements are abolished. This round will not continue the old performance archiving task and will not delete existing data.

Environment: host = <dev-host>, cwd = `<project-root>`; project `unit_bfm/.venv/bin/python` 3.10.12; CPU only, no sub-agent/GPU/installation/authentication/commit. Measured MemAvailable = 12,455,124,992 bytes (11.60 GiB), which is an instantaneous value and more secure on a budget of about 11GiB per user. Only this discussion report and v3-rl_final_audit.md are allowed; provisional evidence is limited to v3/runs/rl_audit_unique.

## Stage implementation checklist (this auditor’s own handoff)

1. Put down the original design first for the pipeline to use before implementation: capacity, sampling/retention semantics, required thresholds, history/termination/snapshot/checkpoint boundaries.
2. Read-only follow up on the new RAM Replay/streaming collect/train and physical public API, record SHA256; do not use developer handoff as test evidence.
3. Small-capacity overwrite CPU test to verify invalid exclusion, eliminated index, rho/goal, no disk read, recovery of the same sampling and next update; use real short physics to verify input closure and snapshot process continuity.
4. If the new implementation fails to deliver the design of the stage and the accurate status of "audit to be realized", the main window can resume the audit; do not wait indefinitely, and do not repeat the known problems with the old code.

# Conclusions and Least Reasonable Achievements

The direction of this round complies with off-policy FB: the cumulative W and the training buffer capacity are different amounts; the history can be eliminated, the fixed rule anchor points can be retained, the current buffer can be used to define explicit time-varying rho, and the GPU can only be moved during batch sampling. No need for permanent episodes, full trajectory compression, full coverage a priori completion, or larger networks. Keep the existing g13/x137/z16, complete physical p+memory and FB loss.

**It is recommended to use two fixed-capacity, transfer-by-transfer, and explicit current/next FP32 RAM libraries first. ** Rule 32768 and online 65536 are feasible candidates under the current p dimension and must be recalculated after the final physics schema is frozen. Don't do shared boundary references/complex compression first to save hundreds of MB: independent current/next directly guarantees that the covered slot will not be referenced after elimination, and is the simplest to implement and accept.

# # Upper bound of RAM quantification

Current physics p = 4534, memory = 243, total p = 4777. Each minimum training data: x/x_next each 137, p/p_next each 4777, g_next13, u1, discount1, a total of * * 39372 bytes * * (FP32). Total capacity 98304: * * 3,870,425,088 bytes = 3.6046GiB * *.

| Project | Budget |
|---|---:|
| 98304 current+next training tensors | 3.6046GiB |
| Optional g_current duplicate save (can be omitted from x [: 13] view) | 4.875MiB |
| 256B index/ID/position/state budget per slot | 24MiB |
batch 512 training fields 19.2225MiB
| Independent goal_g512 + valid | Approx. 27KiB |
| 2 CPU batch gather/transport temporary storage | About 39MiB |
| Conservatively allocated to small tables, abundant bucket capacity, limited diagnostics | 64MiB |
| Total recommended reserve for Replay subsystem | About 3.75GiB, less than 4GiB |

This budget requires **compact integer indexing, no Python dict/raw/list/episode objects saved per slot**. Encode id/phase/config/scene/structure as integers; position+goal position and other fixed arrays in each slot's four-key family bucket, use array/compact ndarray for the bucket and limit the expansion margin. Python dict only has limited group/bin granularity. CPU tensor/numpy shares rather than copies the entire library; do not deepcopy the 3.6GiB library before state_dict()/torch.save.

Update: For every p scalar added, the total current/next Replay is increased by about 0.75 MiB; about 400 fields have been able to eat the balance. The startup must calculate the actual `.nbytes` + index budget, which is explicitly rejected by 4GiB and reduced by the configuration/main window. Even if 3.6GiB is established now, 4777 cannot be written to death.

When the network is in p4777, the online parameters are about 5.60 M (22.4MB weight), the target is about 5.39 M (21.6MB), and the gradient/Adam is about 67MB, which is not the main CPU memory item. The actual framework workspace/blas and simulation model are not calculated. The N × N density and temporary cat of batch are much smaller than full Replay, but RSS should be measured.

**Checkpoint peak value is the most easily missed item**: During complete recovery, if you first pre-allocate an empty 3.6GiB Replay, then torch.load another 3.6GiB and copy it, the peak value will be at least 7.2GiB + network/interpreter; state_dict may exceed 11GiB if deepcopied again. Minimum implementation: rollout boundary synchronization pauses writing, directly serializes active arrays/cursors/buckets or integers required for index reconstruction, without deepcopy; load directly takes over the loaded array, or loads fields into allocated libraries and releases them in time, prohibiting three copies at the same time. Only keep the last + one previous checkpoint, and do not increase the checkpoint infinitely. Integrity check/atomic rename can be retained.

### Minimum reserved unit and P0

The minimum unit of training is * * one legal physical transfer * *: x_t, p_t, u_t, x_next, p_next, g_next, discount, and the current hierarchical label/structure ID, generation. The current and next must be frozen before/after the interval is completed, and next cannot take the first frame of the new round after reset. The data generated with the full episode is an optional collection organization and should not become a Replay holding and elimination unit.

P0 "reservation" is a fixed-capacity sub-library reservation, which cannot be understood as permanently retaining all 2.88M samples. Simple solution: Rule 32768 is used as a fixed P0 anchor point. The P0 phase is retained according to the declared layered reservoir, is not filtered according to success, and is frozen after the end. Online 65536 FIFO/ring rolling. If the new rule behavior is required to enter the gradient during training, the main window should explicitly split the rule capacity into a fixed P0 area + rolling rule area, or explicitly layer the rules and continuously replace the reserve; both are reasonable, but "completely freeze P0" and "each new rule can be entered into the rule library" cannot be implicitly committed at the same time. No need to increase total capacity.

A 50-50 sample of fixed P0+rollonline is an explanation for off-policy mixing. Ruled behaviour is not a teacher, and there is no need for behavior z as a target for training. The cumulative P0 budget only affects the cost of collection and does not provide for unauthorized offline updates of credit.

### Feasibility and limitations of 144 configs×5 scenes in bounded buffers

720 (scene,config) groups/sources. The average number of 32768 rules is 45.5 per group; the average number of 65536 online rules is 91.0 per group. **At least a small amount of transfer can be established group by group; two complete episodes of 1000 steps per group cannot be established** (at least 1.44M per source, far exceeding the capacity). The old automatic expansion based on this lower limit must be deleted.

After rare bins, fixed sides, installations and dynamic processes are crossed again, there is no guarantee that all crossed combinations will reside at the same time; this is not proof that the buffer is illegal or cannot learn. Global coverage statistics can be accumulated outside the buffer, but statistics cannot be disguised as current rho support. Vanishing can be mitigated by using disjoint group minimum quotas or configuring schedules; there is no need for complex optimal quotas in the first version. When a certain group of FIFO is temporarily vacant, the balance of the group will be recorded, re-normalized according to the currently available group, and legal updates will continue; coverage_ready=false cannot be used as a global optimization switch.

When activating only rule, you can first adopt the policy until both sources are non-empty, and then enable 50/50; if single-source training is allowed, the transition distribution must be explicitly approved in the main window. If the scenario/configuration is not filled, you can prefill a small amount or use partial distribution. The manifest declares the active group set and effective weight; **strict full group check is only used for user-specified sampling constraints/final acceptance, and cannot be stuck in learning by default**. Bin vacancies are normalized and reported according to the original contract, and samples are not selected according to the quality of unvisited successors.

### Necessary contract between rho, training target and goal

Retain the current layered form: source→scene→config→current key family (xi/dq/tau/phase)→non-empty bin→transfer within bin. Each row is sampled independently with replacement. The final edge probability is the sum of the path probabilities of the four-bond family reaching the same transition; it does not only record the probability of this selected path. g_next comes from **the real transfer**, the query reference must call an independent draw of the same distribution and take next g.

Independent and identical structure goals must be extracted from the complete g13 again, matched by length/limit/geometry family (cannot be compared with any integer config_id), goal acc_valid and valid boundary are qualified; the same sample is allowed to be drawn by chance, independence does not mean forcing different IDs. When there is no goal, only random z in this line will be recorded and fallback will be recorded; the current B will be encoded and detached each time. Don't fake independent matching goals by shuffling g_next from the current batch for throughput, and don't cache cross-B versions z.

* * Minimum required cache identity * *: Replay instance ID + schema/rho rule hash + active collection generation/epoch; slot override must increment generation repeatedly, pool/query records the identity. Using only the same integer revision and "which groups" will misidentify different Replay instances as the same rho. The reference pool can be frozen for freezing the model evaluation, but it must be clear that it is frozen rho, not real-time buffer rho. Sampling optimization can first extract row IDs independently and then sort the gather last recovery order by memory location; this does not change the probability. Fetching adjacent rows in batches by chunk or reusing the old target pool changes the distribution/correlation and cannot be used as a harmless cache.

The read-only old revision-2 microbenchmark has independently discovered that QueryPool.assert_current still passes for two libraries with the same revision/group list but different g; this is an identity risk that should be fixed in this round of RAM design, and does not require the retention of the old disk scheme. After adding new RAM, you need to reproduce it again, and do not use the old code as a new implementation conclusion.

### Streaming collection, history and snapshot reset

Each world holds only the latest 22 original boundaries and the current known and current x/p, plus a control interval that is being completed; a small rollout (for example, 32–128 steps) can be collected at a time and updated alternately, without accumulating the entire raw/fs/p list. For the low-risk first edition, a single, capped episode can be allowed to exist temporarily (about tens of MB to 100 MB), but it must be released immediately, not enter the long-term replay, and not grow as a cumulative W; the true streaming push transfer is more direct.

z is maintained within a call, and the FeatureHistory is unclear when changing z; the snapshot Actor/B is refreshed at the agreed rollout boundary. Multiple worlds maintain z/phase/history separately; different world next cannot be mismatched.

Snapshot reset is separated from checkpoint continuation training: snapshot needs to restore the same model physical time/process phase/anchor point/object reference/driven tau and ordered queue/qpos/qvel/required solution state**, and at the same time start a new feature history (padding, interval_valid=false, no previous interval integration), and do not inherit the old memory. Keep the process clock, and set this rollout elapsed for truncation to avoid restoring t=8s but mistakenly calling the new 10s process or only 2s left. Do not just set q/dq and drive and then time=0: the loader/adjacency reference will be restarted, making the next response different from the same physical snapshot. The snapshot pool must have a fixed number/bytes limit and do not copy large snapshots in each piece of metadata.

If the training checkpoint is saved at the end boundary of all worlds, complete recovery only requires Replay/Network/Optimizer/RNG/Scheduler/credit/Cost and rebuild the next episode to ensure accurate follow-up; if it is saved in a rollout midway, it will also require a physical snapshot of each world, the original ring/phase of FeatureHistory, the remaining behavior controller points/z/call, etc. The snapshot reset of padding should not be used to claim accurate continuation of training. The first version recommends only using complete rollout/episode boundary checkpoints and not extending and complicating midway recovery.

### Required thresholds and diagnostic-only matters

Must: Physically legal, invalid transfer isolation, correct source/unit/moment, next pairing, target stop gradient, limited loss/grad, capacity upper limit, no disk sampling, explicit rho, independent goal with configuration, self-contained recovery, V2 isolation. The numerical failure is not a physical terminal, and cannot be quietly changed into a normal training line with gamma = 0; the real terminal state of the bootstrap is truncated at normal time.

Diagnosis/continuation and acceptance of final capacity: 144 complete, rare bin ratio, E4 active time, coverage of ready, unknown morphological skills, model error success rate, total 20M budget, original trajectory permanently re-emergible. The absence of these does not prevent the already legitimate optimization. F-physical input closed missing items are input correctness and require pysics correction, but cannot be made an unachievable “strictly sufficient universal mathematical certificate” for Markov.

## Current implementation status (first read at 09:03)

the replay is still a compressed episode path; the pipeline has written a RAM implementation checklist in its own handoff, which is generally consistent with this recommendation, and has not yet obtained RAM code test evidence. physics has announced snapshot/restore and PhysicallyInvalidTransition, which cannot be announced before the order is placed. Subsequent independent audits are written in v3-rl_final_audit.md; this document will be delivered to the design first, and will not be available to the main window until development is complete.


#09:08 Dynamic capacity update interface with early measurements

Physics is implementing subsequent corrections, and the total p has become **5054**. The training tensor with the same capacity of 98304 becomes **3.80750GiB**; adding 256B per slot is about 3.83093GiB, and the batch dual temporary storage is about 41MiB. After adding 64MiB small table margin, it is close to but still less than 4GiB. If the old 2048B/slot is used, it is estimated to be 3.994995GiB, leaving only 5.125MiB. We cannot count the batch in addition to this and claim that the total Replay peak is less than 4GiB. It is recommended that the capacity of the main window be reserved for allocation, and the final schema be tested again; there is no demand that the candidate capacity must be fully used.

A new implementation of RAM has emerged, with a small capacity of 17 +23 writing 420 stripes and stabilizing 40 stripes. Reading of blocked files can still add/sample, invalid rejection, sampling probability and resumption of the next update pass. It was found that p0 = True currently only counts, and then the rule FIFO can eliminate all P0; this is inconsistent with the semantics of the current round of "fixed P0 subbank", and the main window must determine the partition/retention strategy. The independent report will list the hash of the actual measurement, and do not consider the ongoing development as completed.


# 09:14 Delivering updates

The new implementation has independently completed small-capacity diskless replay verification and real 96W/6 update, which is completely consistent with the final parameters of version P0 recovery; see v3-rl_final_audit.md for details. The final observation of total p is 5065, and the initial reading of 4777 is no longer used. P0 has added a protection half area, but the retention in the group is still the end of the loop; the correction should be retained in a fixed capacity hierarchy. query Cross-library cache identity, snapshot time/historical semantics and some physics closure gaps have been fixed and this agent has been tested, and the report does not repeat the old problem.
