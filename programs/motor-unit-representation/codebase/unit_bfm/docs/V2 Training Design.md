# V2 training design description: input, sampling, loss, UFO comparison and actual completion status

Recorded on 2026-10-01. Version: `SIM_PRIVILEGED_FF_MR_RF_V2`. This is the V2 history that has been executed, not the next round of training proposal. This round supplements the P0 data path and [evaluation webpage ](Evaluation Web App Guide.md); the webpage calls the existing freeze evaluation, without modifying the training algorithm, weights or restarting the training.

* * V2 has completed P0 and online P1–P3, and finally 20,032,000 transfers and 77,218 gradient updates; `validated=false` indicates that the general execution capability has not been accepted, which does not mean that only P0 has been completed. V1 stops early on P2. * *

This document undertakes [training engineering realization design ](Training Engineering Design.md), [V1 historical design ](V1 Training Design.md) and [no reward V2 results ](Reward Free V2 Results.md). Facts are subject to the current round [save source code ](../artifacts/rf_v2_full/source), [run configuration ](../artifacts/rf_v2_full/config.json), [batch log ](../artifacts/rf_v2_full/), [status ](../artifacts/rf_v2_full/status.json). The snapshot of the core source code of this check training is consistent with the manifest hash.

#1 Target, method selection and evidence boundary

The unit is a drive joint and two LINKs, first constrained to the sagittal plane. Actor accepts z and outputs the motor torque request using local motion, load, nominal structure and history; B provides local physical result encoding upwards. From now on, the upper level is responsible for coordinating multiple units and balancing the whole body. There is no training for the feet in this round.

**Scope check: The dynamics of V1/V2 themselves are flat, and the 2D played back is not a display projection. ** All hinges revolve around the y-axis, and the active roots are only x/z/pitch; g23 has no lateral speed, roll/yaw or full three-dimensional wrench. This FB model is for the current planar MDP and cannot prove three-dimensional reusability. An active motor's 1 DOF is not equal to the root and the two LINKs must only have plane motion; if the three-dimensional universal unit is targeted, the three-dimensional connection, motion/inertia/force observation, B result space and training sampling must be expanded at the same time, and the rendering cannot be changed. This time, the historical weight is retained and this boundary is clearly written into the evaluation webpage.

See [Evaluation webpage instructions: query target and execution judgment  ](Evaluation Web App Guide.md#query-target-and-execution-assessment) ] for the visualization and judgment method of the target of the frozen evaluation. The page displays the target pole attitude, velocity or torque relationship and error from the saved physical query, and does not claim to invert the only target from any z. The q error of the complete point  target is only a projection indicator, and does not prove that the motion, torque and interaction results of the two rods all reach g *.

V2 uses FB pre-training without artificial rewards to test whether it can obtain queryable movement and interaction behaviors. Hold, speed, braking, and compliance are queries and evaluations after freezing and are not used as pre-training supervision. There are no L_task, command amplitude costs, command change costs, or dynamics parameter prediction losses.

The logic of choosing V2 is to withdraw a number of additional designs introduced at the same time as V1, and establish a baseline close to the local UFO basic FB implementation. We cannot claim that every V2 choice is optimal based on this, nor can we treat V1/V2 as a univariate ablation that “only deletes task z”. Training length, input, loss, sampling, and optimization all vary.

UFO in this article refers to the basic `FBAgent` and simple network paths and their class default values ​​in a local external FB reference tree. It does not generally refer to all experiments, all configurations or additional modules in the paper. No humanoid pre-trained weights, expert actions, or full-body discriminators were ported to the unit.

# 2 Network, Information Input and Motor Actions

 Network  Input  Output  Parameters
|---|---|---|---:|
| Actor | x336, z16 | u1, tanh throttling | 309,505 |
| F1/F2 | x336, actual sending u1, z16 | 16 dimensions each | 313,616 each |
| B | g23 | 16 dimensions, norm 4 | 76,560 |

Online network with 1,013,297 parameters; Implementation of Actor+B for a total of 38,065 parameters. All ahead, no GRU. F/B target is a slow-up copy and does not participate in the gradient; No target Actor.

Actor two branches encode x and [x, z] respectively; F two branches encode [x, u] and [x, z] respectively. Each branch is Linear→ 256, LayerNorm, Tanh, Linear→ 128, ReLU; after splicing, Linear→ 256, ReLU, and then output the action or 16-dimensional F. B = 23→ 256, LayerNorm, Tanh,→ 256 256, ReLU, 256→ 16, re-spherical normalization. The width 256 and z16 are the starting points of capacity and are not derived from the number of motors or the number of reward algebraic items.

##2.1 x 336 and g23

 `x336 = current o24 + nominal m28 + slow history 10×26 + fast history 8×3` .

| Current field | Dimension | Whether B is entered | Physical meaning |
|---|---:|---|---|
| q, dq | 2 | Yes | Relative joint angle and angular velocity |
| Sinθ, cosθ of each of the two LINKs | 4 | Yes | The posture of the LINK relative to the world around the +y axis; not an extra joint |
| Two LINKs each COM vx, vz, ωy | 6 | Yes | Translational velocity and angular velocity of the world center of mass |
| Actual driving torque τm | 1 | Yes | Torque after driving delay and response |
| Last command u sent | 1 | No | Control history |
| Two link contact marks | 1 | Yes | External contact that occurred at the end of the control interval |
| Joint upper and lower limit distance | 2 | Yes | Constraint information redundant with q |
| Two LINK environments Fx, Fz, My | 6 | Yes | The interval average effect of explicit external force, R1 support, and R2 external contact |

The environment wrench does not include all joint transfer forces, nor does it include all internal constraint reactions and gravity. The motion takes the end point of the control interval, and the contact and environmental force takes the summary of the 10ms just ended, so g is not a complete instantaneous Markov state.

`m28` has 14 nominal parameters and 14 valid markers: two-rod length, mass, Iyy, x/z offset of each COM relative to the joint, joint upper and lower limits, nominal torque capacity, and motor time constant. The valid marks for this round are all 1; the actual random parameters are not directly entered.

Slow history 50Hz×10: motion takes the endpoint, u/τ and wrench take the mean of the two control intervals, contact takes the OR, and each entry is attached with padding and age. The endpoints are 180ms apart in total, and the summary interval covers 200ms. Fast history 100Hz×8: u, τ, padding, covering 80ms drive record. The history is re-accumulated after reset and cannot be cleared after changing z. It is an attempt at implicit dynamics adaptation and does not guarantee recognition of mass, friction, or arbitrary slow modes.

The original transfer result is saved as `y25=[o_next, Δu]`; B only reads g23 after removing u and Δu, and does not enter m, history, z, hidden parameters or future incentive plans.

Fixed scale: q/1.2, dq/6, COM speed/2, ω/6, τ/6, environmental force/20, environmental torque/6; sin/cos and contact marks are not scaled. See [Observation Realization ](../artifacts/rf_v2_full/source/kernels.py) and [Historical Assembly ](../artifacts/rf_v2_full/source/history.py) for detailed field order.

LINK attitude, center of mass velocity, true torque, and environmental force currently contain simulation privileged truth values ​​and cannot be called deployment inputs that can be directly provided by ordinary motor telemetry. B is not a parameter identifier; the Actor's 128-dimensional state branches serve as contextual feedback but are not supervised into explicit physical parameter estimates.

### 2.2 Action chain and feedback

Actor sends u ∈ [− 1,1] at 100Hz; nominal request is 6u N · m. Drive every 1ms execution: command delay queue→ actual capacity clipping→ first-order response→ τm. F takes the actual transmission of u as the action condition, and does not replace u with the τm after the response.

The feedback up is  `o24+m28+B16+Actor context 128+B_valid 1=197 dimensions` . Providing this interface does not prove that it is more conducive to upper-level learning than the original q/dq feedback.

# 3 Environmental Organization and Randomization Course

MuJoCo 3.8.1, MuJoCo-Warp 3.8.1, Warp 1.14, MJLab 1.4; physics and drive 1kHz, control 100Hz. Each batch has 128 worlds and runs for 500 steps, which is 5 seconds each, resulting in a total of 64,000 transfers.

The role, the connection, the role of learning data, the role of learning data, the role of learning data.
|---|---|---|
| R0 | Complete proximal position fixation | Local movement with clear control under fixed support |
| R1 | The proximal plane root is supported by finite spring, damping, and gravity preload | The proximal end reacts and the whole is driven |
| R2 | Planar floating double LINK in contact with the ground | Contact constraints, load-bearing side changes; no balance bonus |
| R3 | Four LINK chains, learning middle joints, bounded PD drives on both sides | Adjacency drives and dynamic loads; not trained unit collaboration |

There are 32 fixed structures per character, 8 narrow ranges and 24 wide ranges, a total of 128 types. Only one structure is used in one batch, 128 world independent random round parameters, initial state, excitation and z; the structure is changed at the end of the batch. It is not a permanent division of the world into four groups. Roles are scheduled according to accumulated quota arrears, and the structure index is shuffled and traversed.

| Stage | Plan Online Budget | Collection Ratio R0/R1/R2/R3 | Replay Sampling Ratio | Randomization |
|---|---:|---|---|---|
| P1 | First 0.8M | 70/30/0/0% | Same as left | Narrow structure, level=0 |
P2  and then 4M  gradually to 25/30/20/25%  to 25% each  to reach the entire structure, to reach the level of
| P3 | Remaining budget, total W including P0 target 20M | 25/30/20/25% | 25% each | level=1 |

# # 3.1 Specific Randomization

| Hierarchy | Actual scope and implementation |
|---|---|
 narrow structure  P/D length 0.225 – 0.275/0.315 – 0.385 m; Basic mass 0.85-1.15/0.2125 – 0.2875 kg
| Wide structure | P/D length 0.15–0.40/0.25–0.45m; base mass 0.40–2.00/0.15–0.60kg |
| Distribution and counterweight | Uniform length, logarithmically uniform mass; 0–20% counterweight for each rod in wide structure, 20–80% along the rod, x offset 0.01m; real geometric synthesis COM/inertia. Wide R0 support inclination angle ±0.5rad |
| Turn Density | Co-multiplied by 0.8–1.2 per rigid body mass and inertia; nominal m does not change with actual magnification |
| Local joint parameters | Damping 0.01-0.08N · m · s/rad, Friction 0-0.08N · m, armature log uniform 0.001-0.006kg · m ² |
| Contact | Sliding friction 0.4–1.0; contact is generated by actual physics calculations. R0/R1/R3 has no self-collision, R2 enables grounding |
| Motor | Capacity 4.8–7.2N·m, time constant 5–20ms, integer delay 0–10ms; nominal request still up to 6N·m |
| R1 support | kx20–200N/m, kz100–500N/m, kθ0.1–5N·m/rad; damping ratio 0.3–1, damping calculated based on mass/approximate inertia |
| External force | 0.5-2s interval, lasting 0.1–0.5s, 50ms smooth edge; force amplitude 0-0.5Mg, random direction, additional torque ± 1.8N · m, random P/D and 20–80% position along the rod; M is the total mass of the mechanism |
| R3 adjacent drive | Sinusoidal target amplitude 0.1–0.7rad, frequency 0.3–2Hz, random phase; PD(8,0.5), torque limit ±3.6N·m |

Parameters are sampled at structure construction or round reset, rather than changing mass every control step. External force plans are independent of z, and the network does not read future plans.

P1 level=0 turns off changes in density, motor parameters and external force amplitude; P2 interpolates most continuous disturbances. The initial state, R1 damping ratio, and R3 peripheral drive are still random; as long as level>0, the delay takes the complete integer range; the structure is expanded in P2. So this is part of the course, not all factors are continuously synchronously annealed.

# # 3.2 Initial State Sampling

Normal 50%: motor q±0.6rad, dq±2rad/s; wide range 30%: q±1.1rad, dq±4rad/s; access snapshot 20%. When there is no available snapshot of the same structure, fall back to normal/wide according to 5:3.

R1 also adopts root translation ±0.05m, pitch±0.35rad and root speed; R3 additionally adopts peripheral q±0.6 and dq±1.5. R2 adopts the root posture from ±0.35rad near 0 or π, and determines the height according to the lowest point of the actual box; 80% is 1mm above the ground, 20% is 2–10cm above the ground, and the root is vx±0.5m/s, vz±0.3m/s, and ω±1.5rad/s. The legal generalized state is first adopted, and then the LINK attitude and velocity are calculated, and inconsistent observations are not independently spliced.

Each batch saves snapshots of the first 8 worlds in 1.25/2.5/3.75 seconds, with a maximum of 128 entries per structure. The snapshot retains q/qvel, actual parameters, driver queues and clocks, and network history is re-accumulated after recovery. This is not full-trajectory uniform state sampling.

## 4 P0, online Replay and z life cycle

P0 is 128 structures × 4 rounds × 500 steps = 256,000 rule controls/random action transfers, and 65,536 balance reference results are saved. The regular actions are not labeled as Actor imitations, and the original P0 transfer is not prefilled into the online training Replay. V2 only uses P0 in the result encoding when the initial query reference and Replay are empty; the online warmup is 8,192 transfers. Reward-free optimization does not mean that data collection is completely free of human priori.

The replay capacity is about 1M, and each of the four characters has a reserved quota; first select the characters according to the stage proportion, and then select the episode evenly and one of them for effective transfer. There are 512 records in each batch, x/x' is causally reconstructed from up to 22 frames of original records, and does not span reset. Updated every 256 new online transfers. 5 seconds is a time truncation, the bootstrap is maintained, and is not considered to be the end of absorption; if the value fails, it will be isolated and stopped.

Two z-paths in training:

1. Acquisition exchange: 50% random spherical direction, 50% original result from Replay using current B encoding; use P0 result when Replay is empty. Half of the calling events lasted 4/8 steps, and half lasted 10–100 steps. The proportion of events is not the proportion of time taken. Short calls account for about 9.8% of the expected physical time. The acquisition command noise is Gaussian with a standard deviation of 0.2, and is finally limited to [−1,1].
2. Gradient update: discard the original acquisition intention, and reacquire z; 50% random, 50% of the scrambled next results of this batch are encoded by the current B code. The entire FB target in the sample uses this same z, and the next command is not used when collecting.

* * Replay does not save old z and does not cache old B vectors as training tags. * * Information such as original physical records and structures are saved and extracted and re-encoded. Update the inner z-stop gradient, and do not derive B through the command encoding path.

However, the current z will be saved for 40ms–1 second during acquisition, during which the network is still updating; the original target g* of each active command is not persisted and re-encoded with the network version. Therefore, what is solved is the problem of long-term replay of old encoding, not the full consistency of fixed physical intentions. There was no monitoring of semantic drift and no proof that this phenomenon caused the current failure.

When freezing the evaluation, use the B, Actor and reference results of the same checkpoint to recalculate z; record z for recurrence and do not feed back training. The numbers z of different checkpoints cannot be directly interchanged according to the same physical semantics.

# 4.1 V2 to use P0 data-by-line path

The P0 file is `artifacts/p0_limits_v2/bootstrap.pt`, including `reference[65536,25]`, `raw[512,501,24]`, `m[512,28]`, roles, keys, W and seed. Each structure also saves complete y, work, rule call counts and physical snapshots. V2's `train.run()` reads the entire file, but what actually enters this round of training process is reference and W; **raw, m, roles, and keys are not imported into the online Replay, and the P0 snapshot is not loaded into the online snapshot library**. Saving some kind of data does not mean consuming it for training.

| Timing | Specific execution | Whether to generate gradient | Dependence on P0 |
|---|---|---|---|
| Learner initialization | `Learner(bootstrap['reference'])`; set_reference saves the result pool, draws up to 4096 indexes, refresh calculates the second moment, reward cross matrix and diagnostic inverse matrix of the current B | No, all are no_grad | The initial reference comes from P0, but B/Actor/F is still randomly initialized, without P0 pre-training |
| Training count initialization | `p0=bootstrap['W']; W=p0` | No | 256,000 credited to total sampling cost; not 256,000 gradient updates |
| First Initial Replacement Order | If Replay does not have a valid transfer, extract the original result from P0 reference, and generate a partial command with the current B (g); the other half is replaced with a random sphere z | No | Provide physical results that have occurred, do not use the P0 action label, and do not have a fixed table of tasks to z |
| Exchange order after Replay starts with data | Draw the result from the online Replay according to the current role weight and re-encode it with the current B | No | No longer draw new targets from P0; the previously generated active z can still be retained until the call expires |
| The first 8192 items online | Online Actor collection, fill in the newly created empty Replay | No | This is not P0 data prefilling, nor is the rule controller continuing to execute |
| Every FB update | Extract x, u, x', y from online Replay; `sample_z(N,y)` uses the current batch of next results and random direction; F/B loss also uses the same batch of next results | Yes | This call explicitly passes in y, so there is no backup branch for sample_z to use reference when goals is empty; P0 does not serve as FB integral column, positive sample or supervision label |
| The end of each 64k batch | Draw 65536 results from online Replay according to the stage role ratio, replace the query/diagnosis reference with `set_reference`, and draw another 4096 indexes to refresh the approximate points | No | At the end of the first batch, the reference has been replaced by P0; later refreshed with Replay |
| Save checkpoint and freeze export | Save statistics for current reference, B/Actor and query | No | Final reference comes from online Replay, not the initial P0 pool |

The order was subject to whether Replay had been effectively transferred, or had not reached the 8192 warmup threshold. All worlds will need orders at the start of the standards and therefore use P0; After the physical steps produce a valid record, the subsequent expiry order is taken from Replay. The P0 goal may cross the role, while the first has only one structure and therefore cannot be guaranteed that the goal will be met in that structure.

There are still algebraic features and linear readout statistics for four types of query rewards in `refresh()`, but these operations do not enter the optimizer. Initializing B is random, and it cannot be considered that Z acquires semantics as soon as P0 is read. `reference` doubles as a query/diagnosis pool here, and is a different data object from the same batch of Replay reference distribution used by V2 for FB loss.

When resuming training, the Learner is constructed first, and then `load_state_dict()` overwrites the initialization content with the reference, network, and cache indexes saved in the checkpoint; the restored Replay also comes from the checkpoint. Evaluating the `--bootstrap` of the CLI is also only the initial input to construct the Learner. After loading the formal checkpoint, use the checkpoint reference. The webpage review directly constructs the Learner with a checkpoint reference, no additional reading of P0 is required, and the semantics of the frozen query are the same.

### 4.2 What does P0 provide and what does it not provide?

P0 produces real transfers using maintenance, speed, brakes, adaptability and colour random actions, with 20 per cent of the rule calling event theory. All structures are collected at level = 1; The actual initial theory is 62.5 per cent common and 37.5 per cent wide. There is no incentive for optimization, Actor ' s behaviour cloning, task alpha-monitoring z, or only the retention of a successful track. The original result pool was drawn 16,384 by role, and the role balance was not equal to a uniform coverage of q/dq/power/exposure.

V1 uses P0 as FB independent point pool and task reward readout supervision for a long time. The P0 role of V2 has been reduced to * * initial result reference, acquisition command source when empty Replay, and data cost record * *. It may indirectly affect the distribution of early visits, but this round does not ablate to prove benefits. The P0 full 256k trajectory cannot be described as having participated in V2 offline FB pre-training.

Using P0 to transfer offline pre-training, pre-fill Replay, or online continuous mixed rule data are all new designs that have not yet been implemented; these methods do not require behavioral cloning, but will change the training distribution, update budget, and offline coverage requirements. They need to be demonstrated and recorded separately, and cannot be counted as functions that the current V2 already has.

# 4.3 z means a linear relationship

z denotes the direction of future access preferences, and B (g) denotes the encoding of local physical results. FB approximation:

\[
M^{\pi_z}(dg\mid x,u)\approx F(x,u,z)^\top B(g)\rho(dg).
\]

Given the reward r (g), the points get `c_r=Eρ[B(g)r(g)]`, the command is `z_r=4c_r/‖c_r‖`. This is not a predefined 16 physical coordinates and there is no B-input reconstruction supervision. B sees the force, which is not equal to the arbitrary control of the actor; the reachability of the same z on different bodies is conditioned by F/Actor.

Direct B(g*) is a finite-dimensional approximation of the point target access query and does not guarantee accurate arrival; random z does not guarantee independent and useful skill semantics. Normalization is not equal to whitening, and orthogonal coordinates are not anchored; B/F/z synchronized rotation can retain the original behavioral relationship. FB's reward query linearity does not mean that z linear interpolation necessarily produces linear interpolation of physical quantities.

## 5 Independent reference samples paired with the same batch: what exactly is the diagonal

"Diagonal" is the index relationship of the batch matrix, not the diagonal of the neural network weight, nor does it determine whether the floating point values ​​of two physical states are equal.

Assume that three transfers t1, t2, and t3 are extracted from Replay, and the actual next results of each are g1, g2, and g3. V2 calculates `M_ij=F(t_i,z_i)ᵀB(g_j)`:

| row/column | g1 | g2 | g3 |
|---|---|---|---|
| t1 | own real next result | the result of another transfer | the result of another transfer |
| t2 | The result of another transfer | Your own real next result | The result of another transfer |
| t3 | Another Transfer Result | Another Transfer Result | Own True Next Result |

Diagoni=j has a special link “is the next result of this actual arrival”; The non-reverse angle is used to estimate the result reference points taken separately from the current transfer. The non-opposition is not a negative sample that has to be inaccessible, nor is it the probability of classification. Replay may draw duplicate records to exclude diagonals of the index that do not equal the weighting or exclude all state equivalents.

The FB target contains two different expectations: a square consistency term on the reference result and a linear positive sample term on the real next result. Even if the diagonal in the finite sample matrix is only 1/N, the diagonal with a special correlation cannot therefore be directly used as an independent reference sample. Standard same batch non-diagonal estimates are used here; the actual Replay and target z-mixing still have a finite sample dependency, which is not overstated as proof that all variables are completely independent.

# # 5.1 V1 Why not exclude the integral matrix diagonal

V1 also independently draws `ĝ1,ĝ2,ĝ3` from the fixed P0 pool as the points column. At this time, `t1—ĝ1` is only the first index of the two groups of samples. There is no relationship of "ĝ1 is the actual next of t1", and all N² items of the integral matrix can be used. The real positive sample is calculated as `F(t_i,z_i)ᵀB(g_i)`.

Therefore "V1 does not exclude diagonals" does not mean missing masks; as long as the columns are indeed sampled independently, there is no reason to delete them by the same subscript. The motivation for V1 to fix P0 is to keep the cross-stage integral reference distribution consistent and facilitate query and diagnosis; however, fixing the reference distribution does not fix the coordinate semantics of B, nor does it prove that this distribution is better than Replay. It will bring about the coverage difference of P1 online only R0/R1 while the reference pool contains all characters.

### 5.2 Why does V2 exclude the diagonal of the square term but still retain the positive samples?

V2 directly uses the next results of this batch as the integration column, eliminating the additional selection of fixed external reference distribution and aligning the data path of the UFO basic FB. The square term only takes i≠j; the diagonal still uses a linear positive sample term to enter the loss, which is not a learning signal that deletes the real one-step transfer**.

UFO's `update()` is passed in `goal=next_obs`; `update_fb()` constructs an N×N matrix, multiplies the square term by `1−I`, and takes the diagonal for the positive sample term. The estimated structure of V2 is consistent with UFO. The input of B is the g23 projection of this task, and the batch is 512 instead of the default 1024 for the UFO class.

The two estimates can target the same FB overall target under the same reference distribution and other conditions; the reference distributions of V1 and V2 in this project are themselves different, and it cannot be claimed that they are just completely equivalent vectorization techniques. V2 was chosen to reduce additional design relative to the selected reference implementation, not to experimentally prove that the same batch estimate is necessarily better.

Source code basis: UFO update and loss (external FB reference), [V1 archive] (../archive/v1/learner.py), [V2 loss snapshot] (../artifacts/rf_v2_full/source/fb_loss.py).

## 6 Precision loss and optimization of V2

Let N=512, `g_i` is the i-th real next result, and k∈{1,2} is the two F:

\[
M^k_{ij}=F_k(x_i,u_i,z_i)^\top B(g_j),\quad
\bar M_{ij}=\frac12\sum_{k=1}^2\bar F_k(x'_i,u'_i,z_i)^\top\bar B(g_j).
\]

`u'` is sampled by the online actor, and the entire target stops the gradient; let `δ^k=M^k−γ sg(M̄)`, γ = 0.99:

\[
L_{FB}=\sum_{k=1}^2\left[
\frac{1}{2N(N-1)}\sum_{i\ne j}(\delta^k_{ij})^2
-\frac1N\sum_i\delta^k_{ii}\right].
\]

The target in the diagonal corner is just a gradient-free constant, which is retained to be consistent with the writing method of UFO's log value; the positive sample gradient is equivalent to `−F(x_i,u_i,z_i)ᵀB(g_i)`. If no state reaches the threshold, the real next step is to access the positive sample in one step.

Let `G_ij=B(g_i)ᵀB(g_j)`:

\[
L_{orth}=\frac{1}{2N(N-1)}\sum_{i\ne j}G_{ij}^2-\frac1N\sum_iG_{ii},
\qquad L_{critic}=L_{FB}+L_{orth}.
\]

Both UFO and V2 use this Gram form, coefficient 1. Under ideal independent sampling, it estimates `½ tr(C²)−tr(C)`, C=E[BBᵀ], which differs from `½‖C−I‖²` by a constant. V1 is `‖C_batch−I‖²/16`, which has both scale differences and estimated differences for the same finite batch of squares. You cannot write two formulas with exactly the same numerical target.

Actor target:

\[
L_\pi=-\mathbb E\min_{k=1,2}F_k(x,\tilde u,z)^\top z.
\]

The training action `ũ` adds 0.2 standard deviation and ± 0.3 noise to the actor average, and the action boundary retains the gradient through straight-through clipping. By default, two F and FB pessimistic coefficients 0 correspond to the target average; the Actor pessimistic coefficient 0.5 corresponds to the minimum value of two Q. V2 Write the mean/minimum value directly, no extra method variation.

F, B, and Actor each use Adam, the learning rate is 1e−4, and the Actor is updated each time; F/B target Polyak=0.01, there is no target Actor. There is no additional Q loss, and the default q_loss_coef of the UFO basic class is also 0. All gradients are kept limited before running, but loss or clipping is not automatically adjusted.

100Hz and γ=.99 correspond to a discount time constant of approximately 0.995s. The target assumes that the same z will continue in the future, and the actual collection switching is from the policy data source; the coordination performance of the 40ms command change cannot be guaranteed based on this. The normal 5-second time truncation still bootstraps; UFO universal implementation supports the real terminated discount to be reset to zero, and the current unit does not mark the time truncation as terminated.

# 7 Initialization and gradient cropping: why and where it differs from UFOs

Initialization, B orthogonal regularization in training, and B output normalization are three things and cannot be confused.

# # 7.1 Initialization

| Implementation | Actual behavior |
|---|---|
| V1 | Uses PyTorch layer default initialization; no orthogonal initialization is uniformly called. Adam is the optimizer and is not responsible for initializing the network |
| V2 | All nn.Linear orthogonal initialization, gain=1, bias=0; LayerNorm restores default parameters |
| UFO basic path | nn.Linear orthogonal initialization gain=1, bias=0; DenseParallel orthogonal initialization with ReLU gain=√2, bias=0 |

The UFO defaults the double F through DenseParalel, and the V2 is the two independent nn.Linear networks. The linear layer initialization rules of **Actor/B are therefore corresponding to the UFO; The initialization of F is not identical**. The previous reference to “initiation alignment of UFOs” was not accurate, and the discrepancy in the note did not modify the existing V2 or retrainment.

The motivations for orthogonal initialization are to control the singular value scale of the initial linear mapping, reduce initial orientation scaling differences, and adopt the initialization conventions of the selected reference method. Rectangular matrices may only have orthogonal rows or columns; multi-layer nonlinearity, LayerNorm, and training updates do not guarantee that the entire network is equidistant. Therefore it does not guarantee faster convergence, more interpretable z, or better physical control.

Default initialization is not an error. There is no pairing multiple sub-experiment that only changes the initialization, and it cannot be proved which initialization is better based on V1 failure/V2 limited stable operation. V2 is currently selected as the documented baseline on the grounds that referencing consistency versus reducing unverified additional designs is not a claim of proven superiority. If the F-gain difference needs to be tested separately, it should be a new experiment that clearly establishes the item, and the historical version cannot be silently modified.

Source code: UFO weight_init (external FB reference), UFO parallel layer selection (external FB reference), [V2 network](../artifacts/rf_v2_full/source/networks.py).

### 7.2 Gradient clipping

Norm clipping is approximately `grad ← grad × min(1, c/(‖grad‖+ε))`, instead of clipping each element to ±c. It constrains the gradient norm, does not directly guarantee Adam's parameter update norm, and does not fix incorrect Bellman objectives, inputs, or physical models.

| Implementation | Crop Rules |
|---|---|
 V1  F1/F2/B is defined as a global standard with a threshold of 10; Actor's cut by a threshold of 10.
| V2 | Do not crop by default; record F, B and Actor gradient norms separately, stop when not finite |
| UFO base FBAgent | `clip_grad_norm=0.0` is disabled by default; if a positive threshold is configured, F, B, and Actor are cropped separately |

The motivation of V1 is to limit abnormal gradients, but the threshold of 10 has not been proven to be suitable for this task through comparison; F/B joint cropping will also reduce the large gradient of B while reducing the gradient of F. The pre-cropping critic gradient of about 1.18e8 in the last batch shows that the cropping did not solve the training problem, but does not mean that the cropping itself caused the failure.

V2 Uncrop Default is to align the UFO base configuration and remove an uncalibrated modification, not because gradient cropping is generally harmful. Crop under occasional abnormal gradients may be beneficial; if it has been triggered, the scale and target problem should be located first. Existing results are not sufficient to justify "do not crop better". UFOs support configuration overrides, and default 0 cannot be described as all UFO experiments are never cropped.

Source: UFO Default Settings  (external FB reference), UFO F/B separate tailor  (external FB reference), UFO Actor tailor  (external FB reference).

## 8 Complete comparison of V1, V2 and UFO basic FB

| Project | V1 | V2 | UFO base class default/implementation |
|---|---|---|---|
| Training z | 80% manual task points, 20% random | 50% current B(next) encoding, 50% random | Default 50% current B(next) encoding, 50% random |
 Additional task supervision  L_task  No basic fB
| B input/norm | y25; aspheric normalization | g23; norm 4 | Configure filtered observations; default spherical norm √d |
| Result reference | Fixed independent P0 pool | Same batch Replay next | Same batch Replay next |
 FB square item  All stand alone pairs  Non-opposite  non-opposite
| Orthogonal term | ‖C_batch−I‖²/16 | Off-diagonal Gram + diagonal term | Same as V2 form |
| Next Action | target Actor | Online Actor, Stop Target Gradient | Online Actor, Stop Target Gradient |
| Learning Rate F/B/Actor | 3e − 4/1e − 4/3e − 4 | Average 1e − 4 | Average 1e − 4 |
| Actor update | every other time | every time | every time |
| target Polyak | 0.005 w/Actor | 0.01 w/F/B | 0.01 w/F/B |
| Initialization | Default layer initialization | Orthogonal gain1 | Linear gain1; Parallel F gain√2 |
| Cropping | F/B joint 10, Actor10 | None | Default None; separate modules when enabled |
| Optimize batch | 512 | 512 | 1024 |
| Input normalization | Fixed physical scale | Fixed physical scale | obs_normalizer path |
| Collect z | Mainly manual tasks | Random + current B (Replay result) | Default is random, 150 control steps change order; other paths such as z_buffer mixing can be enabled |

UFO does have z_buffer and writes z when updating. It can be used for acquisition after enabling `use_mix_rollout`; the basic class defaults to this switch as false. Just because this unit Replay does not store z, we cannot conclude that UFO never caches z, nor can we equate UFO cache acquisition commands with permanently fixed semantic training labels.

Some local recovery configurations overwrite the basic defaults, such as use_mix_rollout=true and clip_grad_norm=0 in `configs/resume/piplus40v_original/agent_config.json`. This further shows that "comparison with UFO" must specify the specific path, rather than just reporting the frame name. This document does not reproduce the entire algorithm for this recovery configuration.

## 9 How much has P0–P3 been completed?

W is the cumulative number of single-world transfers, not the number of parallel control steps, nor the number of updates. The following is obtained by summing the batch-by-batch log differences from a complete run:

| Stage | Actual transfer | 128×500 batches | Gradient update | End of accumulated W | level |
|---|---:|---:|---:|---:|---|
| P0 rule collection | 256,000 | Not applicable: 128 structure × 4world | 0 | 256,000 | Full strength for P0 collection |
| P1 | 832,000 | 13 | 3,218 | 1,088,000 | 0 |
| P2 | 3,968,000 | 62 | 15,500 | 5,056,000 | Batch value 0.008–0.984 |
| P3 | 14,976,000 | 234 | 58,500 | 20,032,000 | All 1 |
| Total | 20,032,000 | 309 batches online | 77,218 | 20,032,000 | P3 budget completed |

P1 plans 0.8M but actually 0.832M, which is caused by the whole batch of 64k boundaries; P2 is therefore 3.968M, and the total of the two phases is still 4.8m. P3 completes the current batch when it reaches the total budget, ending up slightly above 20m.

There are 19,776,000 items online, and R0/R1/R2/R3 are 6,208,000/5,952,000/3,392,000/4,224,000 respectively. The entire online process accesses 128/128 structures; P3 itself accesses 125 types. The entire 128 types cannot be mistakenly written as each structure is accessed at level=1. A single training seed is 20260930, and this round of recording took 2,059.9 seconds.

V1 status is 2,624,000 total W, 9,250 updates, P2, stopped. V2 status is 20,032,000 total W, 77,218 updates, P3, budget_completed. Both are validated = false, but the reason cannot be reduced to the same training schedule.

* * Randomized course and budget completion does not equate to mastering all random conditions, nor does it equate to verified upper-level learning acceleration. * * There are currently no ongoing training sessions.

# 10 Post-Freeze Evaluation How Conclusions Arise

All use the final frozen checkpoint, deterministic Actor mean, and no new parameters are trained. The query reward is only used to find z and does not enter the optimizer.

### 10.1 Nominal R0 preservation: distinguishing two types of queries

8 targets q*=±0.15, ±0.35, ±0.5, ±0.7rad, each with 4 initial states, each running for 5 seconds; level=0, no external force pulse amplitude. Three queries use the paired initial state:

- Complete physical static target: given q *, zero velocity, positive kinematic attitude, gravity compensation torque, calculate B (g *).
- Incentive points: `r=−((q−q*)/0.5)²−0.1(dq/3)²`, calculated by freezing B and final reference distributionz.
- Random spherical z as reference for specified target control.

The track-by-trajectory averages of the last 1 second position RMSE are 0.4954, 0.0977, and 1.0771rad respectively; the reward query end speed RMS is about 0.00133rad/s. Therefore, it can only be said that reward query has partial retention ability under these conditions, but it cannot be said that direct B(g*) is reliable.

The 65,536 reference results for bonus points come from the final Replay sampling, of which 4,096 are fixed to calculate the point approximation; it is not just which z is scanned with the best effect, and the Actor is not optimized again for each target.

### 10.2 Query across 1024 conditions

There are 2 structures for each of the four characters, 8 in total; 32 sets of task parameters (8 for each of the four categories) × 4 initial states/random conditions, each of 5 seconds. The index0 structure was used for training monitoring, and index1 was the final extension; all panels cannot be called untouched independent final tests.

All tasks use bonus points to find z, paired with analytic controllers of the same structure, initial state, dynamics, and external force seeds. The analytical reference is PD/velocity feedback/impedance control, not the qpos-RL baseline.

| Metrics | FB | Insights |
|---|---:|---:|
| Hold: Last 1 second angle RMSE, rad | 0.4509 | 0.1007 |
| Speed: the speed RMSE away from the limit interval along the target direction, rad/s | 4.5397 | 2.7280 |
| Braking: Last 1 second speed RMS, rad/s | 0.9986 | 1.2322 |
| Compliance: RMSE, N·m | 3.9780 | 0.5103 |

Compliance is a driving torque relationship, not arbitrary contact force control. The end of R2's 64 braking cases are all close to the limit, requiring about 95% of the time to be saturated. Low speeds cannot be regarded as high-quality braking.

### 10.3 Continuous switching and random z coverage

The original switching panel has 400 items: the nominal R0 uses two complete target codes, and the remaining four structures use random z pairs; fixed first command or 4/8/50/100 step switching, each with 16 paired initial states, and the history of the order is unclear.

After discovering that the final reward query is better than the point target query, 80 nominal R0 reward query switches were added, clearly for post hoc diagnosis. The script alternates between two z corresponding to ±0.6rad; the full RMSE of fixed/40/80/500/1000ms is 0.1470/0.6871/0.7513/0.3934/0.2877rad respectively. This proves that the external command sequence can organize part of the reciprocating response, but does not prove the autonomous periodic motion of a single z or the cooperation of multiple units. The full transient error cannot be mixed with the terminal hold indicator.

Random atlas: another 8 structures × 256 z × 2 initial states = 4096. R2 about 87% request saturation, 84% time close to the limit. The panel also changed the initial state and dynamics, and the trajectory dispersion could not all be attributed to z; the independent physical semantics of each dimension were not proven.

Evaluation source: [full results ](Reward Free V2 Results.md), [execution record ](../artifacts/rf_v2_full/evaluation_execution.json), [main evaluation source code ](../artifacts/rf_v2_full/evaluation_source/main), [supplemental evaluation statement ](../artifacts/rf_v2_full/supplementary_evaluation_manifest.json).

## 11 Judgments that can be made currently

V2 has completed the scheduled training course, the loss and sampling have verifiable implementations, and some queries after freezing produce hold and alternate responses; there are still obvious failures under complex connections. The existing evidence does not isolate the respective contributions of B representation, query mapping, actor response and data coverage, nor does it prove that z semantics are stable during the training period, can be deployed on real machines, or can accelerate upper-level bipedal learning.

This comparison of UFOs is clear: the same non-reverse FB estimates and the default cut-off are consistent with the basis, but there is a difference between the two Fs being initialized. Retain this fact and do not modify the existing source code, configuration or historical results in order to make the narrative appear consistent.
