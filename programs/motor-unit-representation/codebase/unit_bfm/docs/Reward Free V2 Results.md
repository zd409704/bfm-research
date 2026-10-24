# No Reward V2: Training completed, general execution ability has not yet passed

Date: 09/30/2026; 10/01/2026 Supplemental Design Index. Refer to [Training Engineering Implementation Design ](Training Engineering Design.md) for the basis of the method and each modification, and [V2 Training Design Description ](V2 Training Design.md) for the exact input, sampling, loss, UFO control, and actual completion quantity of P0–P3. The result directory is [rf_v2_full](../artifacts/rf_v2_full).

This round completed the non-reward FB pre-training, frozen query, random z-map and switching evaluation of single joint and dual LINK. ** Under nominal fixed support, hold and alternating motion can be called through z; the hold, speed and compliance performance across connection conditions are still insufficient, especially the contact condition that stops by the limit and continues to saturate. ** This round of candidates is not marked as accepted universal controller, nor is it proven to accelerate bipedal learning.

# 1 Actually completed training and modifications

The V1 did not continue as a successful model. First review its additional task loss, manual task z proportion, command cost, reference distribution and algorithm differences relative to UFO in the document, and then create a new non-reward V2. V2 training optimization terms only refer to FB loss, B orthogonal term and Actor target. The four categories of artificial rewards only appear in gradient-free queries/evaluations and are not used to drive pre-training gradients.

| Project | Actual Records |
|---|---|
| Unit | One drive shaft, two LINKs, plane motion, 100Hz torque request, 1kHz simulation/drive |
| Actor/F/B | x336 + z16→ u1; F input u1 separately; B input 23-dimensional→ physical result 16-dimensional spherical code |
| History | 50Hz×10 slow summary, 100Hz×8 fast recording; feedforward network, no GRU |
| Parameters | Actor 309,505; Actor+B execution parameter 386,065; Online Actor+double F+B is 1,013,297 |
| Formal total W | 20,032,000, of which shared P0 is 256,000, online 19,776,000 |
| Gradient update | 77,218 times; no loss, hyperparameter or core training code changed since start of current round |
| Structural Coverage | 128/128; R0 Fixed Support, R1 Limited Support, R2 Ground, R3 Peripheral Drive Chain |
| Time consuming | 2,059.9s, about 34.3 minutes; including cycle monitoring and partial parallel evaluation competition |
| Additional diagnosis cost | Nominal R0 additional training 2,048,000 online W, independent directory, P0 data sharing |
| Numerical State | Recorded learning is limited, B-spectrum threshold rank is always 16; endpoint spectrum 0.333–1.928 |
| Release Status | `budget_completed`; Candidate `validated=false` |

Physical CPU/GPU Verification, Motor Latency/Response Verification and 9 Item Formula, Gradient, History, Replay and Interface Check passed. Passing these checks is no substitute for behavioral validation. The source code snapshot/hash, checkpoint, and all monitoring results of the training process are retained.

! [Training Volume and Characterization Diagnostics ](../artifacts/rf_v2_full/analysis/training.png)

# 2 Query results across connection conditions

32 kinds of task parameters × 4 initial states × 8 structures, a total of 1024 5s trajectories. The analytical reference uses the same structure, initial state, dynamics and external force seeds; it is a fixed PD/speed/impedance control law, not an optimized optimal controller, nor a "qpos reinforcement learning baseline".

| Physical Indicators, Smaller is Better | FB Query | Parse Reference |
|---|---:|---:|
| Hold: End 1s angle RMSE / rad | 0.4509 | 0.1007 |
| Speed: Feasible interval speed RMSE / rad/s | 4.5397 | 2.7280 |
| Braking: Last 1s speed RMS / rad/s | 0.9986 | 1.2322 |
| Compliance: Full torque relationship RMSE/N · m | 3.9780 | 0.5103 |

Per-role index0 was used for repeated monitoring during training; index1 is the new structure that was eventually expanded. Looking only at the 512 trajectories of index1, the FB/reference retention error is 0.4328/0.0908rad, and the compliance is 3.9132/0.4875N·m. The conclusion is not reversed. No checkpoints were selected with the final score.

| Role | FB retention / rad | Reference retention / rad | FB compliance / N·m | Reference compliance / N·m |
|---|---:|---:|---:|---:|
| R0 fixed support | 0.2165 | 0.0483 | 1.2344 | 0.9385 |
| R1 limited support | 0.3231 | 0.0421 | 1.5376 | 0.4288 |
| R2 ground | 0.8957 | 0.1740 | 10.0017 | 0.3487 |
| R3 peripheral drive chain | 0.3683 | 0.1383 | 3.1383 | 0.3251 |

**There is a clear interpretation trap in the braking score:** Among the 64 braking cases of R2, all were at `|q|>1.1rad` at the end of 1s, and request saturation accounted for about 95% of the entire process. When the speed is close to zero, it mainly manifests itself as stopping near the limit. It cannot be said that it has learned high-quality braking that can be matched. The original rewards and indicators are retained here, and the physical trajectory is reported at the same time; there is no "far away from limit reward" added afterwards to modify the result as a success.

Original records: [FB](../artifacts/rf_v2_full/final_eval/metrics.json), [Analysis reference](../artifacts/rf_v2_full/final_eval_analytic/metrics.json), [Group and case-by-case pairing summary](../artifacts/rf_v2_full/analysis/summary.json).

# 3 Nominal R0: There is a callable behavior, but the query method cannot be mixed

For the same paired panel of 32 targets/initial states, the targets are ±0.15, ±0.35, ±0.5, and ±0.7rad.

| Freeze model | Complete target result B(g*) maintains RMSE | Bonus points query maintains RMSE |
|---|---:|---:|
| Front-end R0 diagnostic model | 0.1217rad | 0.3427rad |
| Final Four Character Models | 0.4954rad | 0.0977rad |

The final model's reward query terminal speed RMS is about 0.00133rad/s; it is able to stay close to different targets under these nominal conditions. The standard deviation of the random z end angle is about 0.931rad, which shows that there are changes in behavior, but there are a large number of limited results, and it cannot be regarded as a uniform and interpretable skill library.

The earlier conclusion that B (g *) was better than the reward query was not retained on the final shared model. Consistently reachable targets are physically constructed, and there is no guarantee that finite-dimensional B-point target coding can precisely control it. This reversal needs to be further positioned and cannot be directly attributed to a loss item, nor can it be assisted by an increase in rewards to skip the issue.

The fixed-index video retains the success and failure of two queries at the same time: [reward query negative target] (../artifacts/rf_v2_full/videos/query_negative.mp4), [reward query positive target] (../artifacts/rf_v2_full/videos/query_positive.mp4), [B target negative target] (../artifacts/rf_v2_full/videos/goal_negative.mp4), [B target positive target] (../artifacts/rf_v2_full/videos/goal_positive.mp4).

# 4 Continuous change of order: Reciprocating movements can be organized, and there are still obvious limitations to quick calls

The predetermined panel has 400 trajectories: the nominal R0 uses the B (g *) command, and four additional structures are set aside for pairs of random z; the fixed first command alternates with the 4/8/50/100-step command using matching primitives, dynamics, and incentives, and the replacement z is unclear in history.

After it was found that the final reward query was better than B(g*), 80 nominal R0 reward query switches were added based on the reasons in Engineering Document 13.1. This is a post-mortem diagnosis, keeping the independent directory and source code hash, and not covering the original main panel.

| Command interval | B(g*) tracks RMSE/rad throughout the process | Reward query tracks RMSE/rad throughout the process | Reward query average absolute Δu |
|---|---:|---:|---:|
| Fixed first line | 0.4780 | 0.1470 | — |
| 40ms | 0.8238 | 0.6871 | 1.4374 |
| 80ms | 0.7877 | 0.7513 | 0.8953 |
| 500ms | 0.5835 | 0.3934 | 0.8997 |
| 1000ms | 0.5243 | 0.2877 | 0.8934 |

These errors include command change transients and cannot be directly compared with the 1s holding error at the end of the previous section. 40/80ms cannot require the mechanical system to complete ±0.6rad displacement in each segment, but the larger required jump is an actual observation, and the interface cannot be claimed to be naturally smooth.

500ms alternating calls produce discernible reciprocating motion, with negative steady-state deviations and transient spikes still present. It proves that z can be called by an external command sequence; it has not proven that multiple coupled execution units can cooperate to complete the walk.

![500ms reward query switching, first scheduled initial state](../artifacts/rf_v2_full/videos/query_switch_500ms.png)

[500ms bonus query video ](../artifacts/rf_v2_full/videos/query_switch_500ms.mp4), [40ms bonus query video ](../artifacts/rf_v2_full/videos/query_switch_40ms.mp4), [original B target 500ms video ](../artifacts/rf_v2_full/videos/goal_switch_500ms.mp4).

#5 Randomz override with failed borders

The other 8 independent structures are reserved, each structure has 256 z×2 initial states, a total of 4096 trajectories. The average q motion range of each 5s is about 1.15–1.83rad; this is just the trajectory distribution, including the contribution of external excitation and initial state change.

The request saturation rate of the two structures of R2 is about 86.6%/87.1%, and `|q|>1.1rad` occupies about 84.6%/84.4%. A large number of dispersed final states in the map are contributed by limits on both sides, which cannot be used as sufficient evidence for rich motion semantics. The maximum limit of this panel exceeds approximately 0.0316rad, and the soft limit is not a mathematical hard constraint.

Fixed Article 0 cases: [R0](../artifacts/rf_v2_full/videos/R0_random.mp4), [R1](../artifacts/rf_v2_full/videos/R1_random.mp4), [R2](../artifacts/rf_v2_full/videos/R2_random.mp4), [R3](../artifacts/rf_v2_full/videos/R3_random.mp4). All original trajectories with z in [random atlas catalog ](../artifacts/rf_v2_full/final_eval/random_z).

## 6 Interface delivery and running costs

[With schema candidate weight] (../artifacts/rf_v2_full/candidate_unit_with_schema.pt) retains Actor, B, reference results and query mapping, and the original checkpoint is not overwritten. Field order, scale, time summary and privileged information source are written to the file; 197-dimensional feedback is o24+m28+B16+cπ128+valid1.

| Native 1000 Measurements | CPU Single Threaded P99 | GPU P99 |
|---|---:|---:|
 One unit  0.297ms  2.417ms
| Two Unit Batch Processing | 0.362ms | 2.412ms |

There is no 10ms timeout. The boundary is the history, B/context feedback and Actor reasoning after the observation is ready, including host action retrieval; it does not include sensor communication, motor communication and upper-layer strategies, and hard real-time is not guaranteed. GPU small batch inference is affected by startup/synchronization overhead. This time the CPU is faster, and other hardware will not be extrapolated based on this.

Execution inputs contain simulated true values; there is currently no real machine module that can run on ordinary motor telemetry alone. Neither the old V1 nor the candidates of this round were marked as having passed the general capability acceptance.

## 7 The conclusion of this round and the basis for subsequent modifications

This round of support: standard unrewarded FB can train local hold and alternate motion through z calls on this unit; the predetermined feedforward network meets the 100Hz inference budget on the machine. It also does not support: any z is a valid skill, B (g *) is semantically stable across conditions, contact interaction is reliable, history can accurately identify dynamics, and the reuse module will be superior to the direct qpos/torque RL.

The next set of priority locations for R2 is limited and the performance of two types of queries varies: a distinction between result expression/question error, strategic response and sampling coverage, with quarantine conditions and fixed weight diagnosis. L_task, limit incentive, GRU or network width cannot be increased directly according to the performance of the current round. This round of tasks is defined, complete failure tracks and results are maintained, and any subsequent changes are compared in a separate version according to the access rules of the project document.

This round of main evaluation, post-mortem diagnosis, 12 fixed index videos and code hashes have all been saved; bipedal training has not been started, nor has the hypothesis of "reducing upper-level learning burden" at the core of the project been verified.
