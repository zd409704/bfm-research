# Single Joint Dual Link FB: Engineering Decision, Review and Training Record

Revision: 10/01/2026. This document is the basis for the current implementation and continues the discussion between the original research training plan  and the original interface discussion . The task aids, B25, fixed ρ, etc. in the two research papers are old V1 candidates;  they cannot override the retraction decision of this document. Physical and x336 contracts remain;  training  method changes must use new versions, independently running directories, and new weights.

For the complete historical design of V2, the diagonal interpretation of the same batch, the exact difference from UFO, and the actual number of P0–P3, see [V2 Training Design Instructions ](V2 Training Design.md). The double F initialization gain difference found in this makeup did not modify the existing training or weights.

The itemized use and unused path of V2 to P0 are described in Sections 4.1–4.2 of this instruction: P0 only provides the initial reference, the result source and sampling cost when empty Replay, does not pre-fill online Replay, does not do behavioral cloning or offline FB updates, and replaces the end-of-batch query pool with online Replay results. For manual execution of the original freeze evaluation and playback trajectory, see [Evaluation page ](Evaluation Web App Guide.md).

This article first gives the reasons and verification conditions for the establishment of the design, and then implements and executes it. **"Necessary" is used only for mission or mathematical contract requirements; reasonably motivated but unproven options are marked as "attempted". ** You cannot claim that something has been demonstrated to be necessary just by putting it in a document.

## 1 Goals and Completion Standards

The minimum execution unit is one drive joint and two LINKs. It receives z, relies on local observations and history to generate constrained moments, and provides original feedback, B result representation and Actor context to the upper layer. The upper layer is responsible for the coordination of multiple units and the balance of the whole body.

This phase only implements and trains the unit. Unrewarded pre-training learns callable behaviors; hold, speed, braking, and compliance are queries and ability assessments after training and do not become pre-training rewards by default. Achieving run-through, numerical stability, callable behavior, and helping both feet learn are four different conclusions.

Completing unit training requires at least: physical and timing checks to be passed; loss/gradient to be consistent with the selected FB reference formula; independent evaluation to be able to distinguish actual responses of different z; semantic query, random z and switching cases all have real trajectories; failure scenarios are faithfully retained. Completing 20M W only means that the budget has been completed, but does not mean that the above conditions have been passed. The conclusion on bipedal learning acceleration is left to subsequent comparisons.

## 2 Review of Old V1: Facts and Unconfirmed Reasons

The complete historical description of V1, including the two layers of LINK World Posture, mechanical environment and mission sampling, calculation of mission to z and loss items, is kept separately in [V1 training design note ](V1 Training Design.md). This document does not cover the V2 implementation decision of this document.

The old run `artifacts/train_v1/` has stopped at 2,624,000 W (including P0 of 256,000 W), 9,250 critic updates. The average maintained final angle RMSE of the 2.048M evaluation is about 0.660rad, the compliance torque RMSE is about 5.242N·m; the last diagnostic reward projection NRMSE is about 0.504, and the critic gradient before clipping is about 1.18e8. The effective rank of the B second-order moment is 14 according to the 1e−3 threshold, and the spectrum range is about 7.06e−5 to 0.0668.

These results prove that the old training did not meet the ability requirements, * * do not prove that a change is the root cause * *. V1 changes multiple algorithm elements at the same time, and cannot reverse the "harmful task loss", "B must be normalized" or "the network is not large enough" from a single failure. Old checkpoints, data and logs are retained as diagnostic material and cannot be published as accepted modules.

| V1 design/modification | Motivation at the time | Review conclusion | Current decision |
|---|---|---|---|
| Four types of artificial tasks account for 80% of training z | Prioritize coverage of behaviors that are expected to be called by the upper layer | Task bias is not necessary for reward-free FB; the prior may compress exploration and lack control | V2 withdrawal; do not let artificial tasks control pre-training z |
| Linear Reward Projection Assisted Loss L_task | Forcing B to keep four types of rewards | Is an additional reward project; no proof of necessity, can not be regarded as FB default item | V2 Completely delete the item in the training path |
| Command cost 0.005u²+0.02Δu² | Reduce force and jitter | Weights are not calibrated; changing task preferences also forces B to encode commands | V2 has no such training cost; command changes are treated as independent physical statistics |
| BInput y25 contains u and Δu | Make the above command cost a result function | Not necessary for local motion/force targets | V2 B Remove two command fields and use 23-dimensional physics results; Actor history still retains commands |
| No normalization at the B end | Hope to represent the magnitude of the reward | Theoretically possible, but deviates from the local UFO default; no independent verification of scale stability | V2 uses sample-by-sample spherical normalization of the source code, still retaining the orthogonal terms |
| L_orth = C − I ²/16 | Fixed feature scale | The overall form is 8 times smaller than that of UFOs, and the gradient scale is 8 times smaller; the finite batch estimation is also different | Restore the non-diagonal estimation of UFO Gram matrix, coefficient 1, do not search for new weights |
| Fixed P0 reference ρ is used for FB integration | Let cross-stage result coordinates have a fixed reference | It can be a research extension, but the P1 source distribution is different from the full library ρ, which additionally introduces coverage and scale issues | V2 training uses the next results of the same Replay batch as the target sample, and first verifies the standard pairing |
| Independent target Actor, TD3-style smoothing, Actor update every other time | Stable off-policy learning | None of them are the default of the selected UFO FB; simultaneous changes make it difficult to locate the problem | V2 resumes online Actor generation to stop the next action of the gradient, and updates the Actor every time |
| PyTorch layer default initialization, F/Actor learning rate 3e − 4 | Common engineering starting point | Different from the reference initialization/learning rate, there is no necessary basis; Adam is not responsible for network initialization | V2 adopts orthogonal initialization gain1, zero bias, three network learning rates 1e − 4; the gain of UFO parallel F is √ 2, the difference is shown below |
| F/B joint global gradient clipping 10 | Prevent numerical anomalies | The large gradient of one module will affect the scaling of another module; it is not the default requirement | The V2 sub-module records the gradient and does not clip by default; non-finite numbers stop immediately |

The above is a set of * * baseline changes to the restoration reference method * *, not a univariate causal experiment. Even if V2 improves, the improvement cannot be attributed to a single line. To study additional designs in the future, one must be added at a time to the baseline passed.

## 3 Which FB to use and what to learn

The source code is based on the local UFO base FB: agent.py (external FB reference), simple network/B normalization/initialization  (external FB reference). The theoretical decomposition basis is Touati and Ollivier, 2021. No loading of full body weights, no use of motion capture or full body discriminators.

The F condition is the current local information x, the executed action u, and the subsequent z that continues to be executed; B describes the local physical result g that you want to access. The approximate relationship is:

$$
M^{\pi_z}(dg\mid x,u)\approx F(x,u,z)^\top B(g)\rho(dg).
$$

Here M is the discounted subsequent visit measure. g is the physical result after projection, not the complete robot state; x is only an information state approximation due to hidden dynamics and limited history. Sharing B does not mean that different mechanical structures have the same reachability, the structure and history are handled by F/Actor conditionalization.

**There is no artificial "reaching threshold". ** The next result of the real transfer g_{t+1} is the immediate access positive sample of the sample; the results of other indexes in the same batch are used for reference integral estimation, and the square term excludes diagonals specifically related to the current transfer. Replay may resample and does not interpret off-diagonals as negative samples whose status must be different or unreachable. The next visit and future visits are recursive through the Bellman relationship. Continuous spaces do not require that two state floating point values ​​be equal; dot products are not arrived at Boolean values ​​and are not a substitute for physical evaluation.

### 3.1 V2 fixed loss formula

The batch contains N real transfers, and g_j comes from the jth next result of the same batch. The two F's are defined respectively:

$$
M^i_{kj}=F_i(x_k,u_k,z_k)^\top B(g_j),\quad
\bar M_{kj}=\tfrac12\sum_{i=1}^2\bar F_i(x'_k,u'_k,z_k)^\top\bar B(g_j).
$$

The next action u' is sampled by the online Actor at the same z, and the entire target stops gradient; the acquisition trajectory actually does not enter the target at the next z. Define δ^i=M^i−γ sg(\bar M), then:

$$
L_{FB}=\sum_{i=1}^2\left[\frac{1}{2N(N-1)}\sum_{k\ne j}(\delta^i_{kj})^2-\frac1N\sum_k\delta^i_{kk}\right].
$$

The target in the diagonal term of the positive sample is just a gradient-free constant, which is retained to make the numerical log consistent with the reference implementation. Let G_{kj}=B(g_k)^TB(g_j):

$$
L_{orth}=\frac{1}{2N(N-1)}\sum_{k\ne j}G_{kj}^2-\frac1N\sum_kG_{kk},\quad L_{critic}=L_{FB}+L_{orth}.
$$

Actor minimizes `−mean(min_i F_i(x,π(x,z),z)ᵀz)`, sampling noise on Actor actions and preserving heavy parameter gradients as per the reference implementation. The output spherical radius of B is √16=4; this normalization does not equal whitening, and C still needs to check. The F/B target is Polyak 0.01; no target Actor is created. No L_task, no additional Q regression, no dynamic prediction loss, no artificial task reward.

Items that are not completely equivalent to the reference: input/action dimensions and result projection belong to this task; use two independent F modules instead of parallel Dense implementation; batch 512 instead of the source code default 1024; the unit is 10ms; Replay is sampled by role/episode. They must be stated in the manifest or supporting design record, and cannot claim to reproduce full-body training step by step.

2026-10-01 Accurate verification: All nn.Linear in V2 are orthogonally initialized with gain=1, UFO's nn.Linear also uses gain=1, but its default double F uses DenseParallel, and `weight_init` uses ReLU gain=√2 for this layer. Therefore the initial scale of the double F's is not completely aligned and cannot just be called an implementation layout difference. Both do not clip gradients by default; if UFO enables positive threshold, it will clip F/B/Actor respectively, and V1 will jointly clip F/B by 10. There are no univariate controls proving which initialization or clipping settings are better, existing training remains as is.

# 3.2 z and action exploration

The training z is 50% of the spherical random direction and 50% of the normalized B(g) obtained by scrambling the next results of this batch. The ratio directly follows the source code default. The latter favors results that have already been visited and does not require external rewards or arrival labels.

Acquisition also tries the same kind of unrewarded mixing first: half random orientation, half B-coding of the Replay result; empty Replay can use P0 to access the physical result. This is the acquisition choice of this project. It cannot be misnamed as the reference default, nor can it be guaranteed to be superior to pure randomness; record the proportion of both and the actual behavior coverage. Each call to z is fixed, and the history of z is unclear.

The action standard deviation is 0.2 and the training sampling noise clipping ±0.3 adopts the source code default. The noise is added to the normalized torque request, and u is actually sent into Replay after limiting; the F action is not replaced with the delayed torque.

## 4 Input, Network and Feedback: Why does each item exist?

The new method version is `SIM_PRIVILEGED_FF_MR_RF_V2`. The learning method and B input have changed, prohibiting loading of V1 weights and continuing to claim the same experiment.

| Network | Input | Output | Necessity/Test Basis |
|---|---|---|---|
| Actor | x336, z16 | u1 | Execute current behavior and feedback closed loop; from task definition |
| F1/F2 | x336, actual u1, z16 | 16 each | required for FB conditional relations; double estimation is a reference method choice |
| B | g23 | 16, spherical normalization | Express future local motion/interaction results; do not perform dynamic identification |

x336= `current o24 + nominal m28 + slow history 10×26 + fast history 8×3` . The structure is set out in [networks.py ](../networks.py) and the history in [history.py ](../history.py). The hidden width 256 is the determined starting point for capacity, and there is no evidentiary requirement to narrow or increase; It's not the same as the number of machines. z16 is an attempt to demonstrate the necessity of using the “16 Incentive Algebra” no longer.

| Field | Dimension | Why give Actor/F | Whether to give B |
|---|---:|---|---|
, dq 2 Current joint motion closed ring
| Each of the two LINKs is sinθ/cosθ, COM vx/vz, ωy | 10 | Distinguish between overall drive and relative joint motion | Yes |
 Real drive rectangular  m  1  has achieved delay between drive and request  Yes, expressable driver interactive result
 Previous sent u  1  known control history no; Not a V2 physical target field
| Two LINK contact flags | 2 | Information about changes in support conditions that have occurred | Yes |
| Joint upper and lower limit distance | 2 | Explicitly known constraints; redundant with q, retaining the existing contract | Yes; its redundancy is not an additional control degree of freedom |
| Two LINK environments Fx/Fz/My | 6 | Contact, fixture and external push and pull have occurred | Yes; it does not mean that external forces can be controlled arbitrarily |
| 14 nominal parameters + valid bits | 28 | Known structures are used for conditional control | No; result coordinates are shared across structures, and reachability is not shared |
| 50Hz ten frame summary, padding, age | 260 | Recent Commands — Response and Load Trends | No |
| 100Hz eight command/torque records + padding | 24 | Keep the recent fast drive sequence | No |

B's g23 is obtained by removing the u field from o24; it does not contain Δu, structure, history, z, hidden parameters and future information. It encodes the results of motion and interaction. **B cannot be called an estimator of mass/friction/delay**. Actor state branch cπ128 does not contain the current z and learns the context with the control goal; it does not guarantee that the physical parameters can be identified.

The velocity of the two links is the COM world velocity; the pose and velocity take the end point, and the contact/environment wrench takes the summary of the just ended 10ms, so g is the result of the mixing time, not the full instantaneous Markov state. The first round clearly adopts the privilege truth value, and the deployment version is trained separately.

V2 parameters: Actor309,505; each F313,616; B76,560; online 1,013,297; perform Actor + B386,065. F/B target totals 703,792, excluding the training gradient. The upward feedback is still o24 + m28 + B16 + cπ128 + B_valid1 = 197 dimensions.

### 4.1 Frequency and history are not arbitrary stack frames

Control 100Hz to ensure that the current status is updated in 10ms; slow history 50Hz×10, endpoint spans 180ms, summary interval covers 200ms; fast history 100Hz×8 covers recent 80ms drive records. This window is an attempt to test and does not guarantee sufficient status, nor can any slow mode be identified. It is based on the modeled motor's 5-20ms time constant, 0-10ms delay and hundreds of milliseconds of load changes, and the historical length is directly derived from the mechanical cycle.

The motion field of the slow summary takes the end point, u/τ_m takes the mean of two samples, the contact OR, wrench and other duration averages; the fast record retains the order of commands. It cannot be said that it is lossless and anti-aliasing. Age is recalculated for each control step. The first valid fast/slow record appears 10/20ms after reset, and it will not be cleared when changing z.

## 5 Physics and Randomized Decision Making

| Design | Classification, justification | Implementation/validation and boundaries |
|---|---|---|
| Single joint + double link, planar motion | User-defined first minimum unit | Does not train machine balance, does not guarantee any three-dimensional topology |
The mission needs motion and interaction; (b) The force rectangular is a design choice that allows both to be expressed directly, and is not the only legitimate action space; Variable resistance/PD targets are also comparable and are not currently mixed
| MuJoCo/MJLab/Warp | Project selection, locally available dependencies | CPU independent verification, GPU batch; no clipping of humanoid environment |
| 1ms physical step/drive step | To analyze millisecond delay and contact; 1ms itself is an attempt | 0.5ms comparison; cannot rely solely on simulation without error acceptance |
| R0 fixed support | Obtain a diagnostic institution with clear control rights first | What is fixed is the complete proximal posture and does not cover the entire machine control |
| R1 Limited support | Unit action requires proximal reaction | Limited spring/damping/gravity preload, does not cover qpos forced tracking |
| R2 contact | Need to experience load-bearing side changes and contact constraints | Legal initial state and real ground; contact is calculated by physics |
| R3 peripheral chain | Need to experience adjacent driving and changing loads | The peripheral controller does not read this unit z; the current version of free space turns off self-collision and cannot claim to have learned chain collision avoidance |
| Geometry/mass structure library | Needs to be cross-body; geometry/anchor points/inertia must be kept consistent | 32 per character (8 narrow, 24 wide); counterweights use real geometry to synthesize inertia, and do not change COM independently |
| Density 0.8–1.2 | Try to override the nominal model error | Each rigid body mass and inertia share the magnification, set_const after per-world writing; do not enter the magnification |
| Damping/friction/armature | Try to cover local resistance and rotor differences | Single physical implementation to avoid repeated friction; scope inheritance research plan |
| Delay 0-10ms, T = 5–20ms, Capacity 0.8–1.2 | Attempt to overwrite drive dynamics | Queue/response by 1ms; sample of capacity > nominal request does not mean a larger drive was used |
 Smoothing external pulses, traps/outside parameters  need to experience being carried and driven; The specific scope is to try to be independent with z, which has already worked, visible, hidden in future plans; Give me a little bit of a sense of rectitude.
| Normal/Wide Range/Access Snapshot Initial State | Try to cover movement direction with actual access state | Contact/velocity generated from legal generalized state; Snapshot along with real parameters and process clock recovery |

R0/R1/R3 off self-collision, R2 ground enabled is the current coverage limit. No alignment force was added, gravity was changed, floating roots were locked, or peripheral trajectories were written to qpos for training success.

### 5.1 Physical modifications and evidence that have occurred

The old `p0_full/` appears to have crossed the border at about 0.56 Rad under the default soft limit. Tighten `solreflimit=.002 1`, `solimplimit=.99 .999 .001`, margin=03rad to retake `p0_limits_v2/` in advance. The latter total data is about 1.20882 Rad, with a >0.1rad ratio. Old P0 should not be used for formal training.

The CPU/GPU four-character short trajectory comparison passed; the maximum normalized q/dq error after correction is about 2.86e−6, and the wrench is about 4.67e−5. The 10ms pure delay and 10ms first-order response analysis inspection passed, and the world parameter isolation and the reset reproduction of the same seed passed. The q RMSE of the fixed control sequence 1ms/0.5ms: R0 is about 0.00206, R1 is about 0.00249, R2 is about 0.01383, R3 is about 0.00241rad, and the speed RMS is close. This is evidence of the panel, not a guarantee of arbitrary high-energy impact.

## 6 The destination and reason of each reward

**V2 optimizer, pre-training z-sampling and physical reset do not use the artificial rewards in the table below. ** The reward is only used to answer whether the specified behavior can be queried after training, which is consistent with the purpose of using r to infer z after FB training. The query itself is a task definition, and trade-offs still need to be explained, but rewards are not adjusted to promote pre-training convergence.

| Query | Definition | Why query and limit like this |
|---|---|---|
| Keep H | −((q−q*)/0.5)²−0.1(dq/3)² | Position error + terminal motion suppression; q* is not used as a pre-training label. Scale affects query preference and must be fixed reported |
| Speed V | − ((dq − v_eff (q))/3) ² | Limited stroke approach limit must be decelerated; v_eff drops smoothstep to 0 within 0.15 rad, cannot claim infinite uniformity |
| Braking D | −a(dq/3)²−b max(τ_m dq,0)/36 | Query the speed attenuation and reduce the positive driving power; it does not specify which angle to stop at, it is not equal to the exact interval energy |
| Complies with C | − ((τ_m − [bias + K (q_ref − q) − D dq])/3) ² | Queries a moment-motion relationship that must be compared to the direct resolving impedance; learning the formula alone is not a proof of FB value |
| Old command cost | 0.005u²+0.02Δu² | V2 withdrawn; observed with independent saturation rate/command change/mechanical work indicators, no implicit query added |
| Old L_task | Reward linear projection supervision | V2 withdrawn; NRMSE only diagnoses whether the query can be expressed, does not enter the gradient, and does not use 0.1 as the universal threshold for termination of training |

After training, `z_r=Eρ[B(g)r(g)]` is inferred from the same result distribution and normalized to radius 4. The original award value should be evaluated using F with non-normalized z_r and conditioned on normalized z. C is not necessarily I, and linear readout uses a regularized inverse matrix for diagnosis only; therefore, the whitening module is not secretly added during training.

The numerical implementation saves 65,536 reference results, of which 4,096 are currently extracted at a fixed time to calculate C and the reward cross matrix; this is the Monte Carlo approximation of the integral, not the exact expectation. The 16-term `reward_features` is only used to quickly and accurately calculate the algebraic expansion of the defined reward, **not the input of B, nor the training labels of B**. The code still retains the diagnostic expression for the old command cost, but the V2 query coefficient is explicitly set to 0 and all current behavior evaluations are explicitly turned off.

The unknown z must also be evaluated. If you only select z that performs well in the four categories of rewards and display them, you cannot explain the behavioral coverage; the trajectories of random spherical z and 40/80ms changes are also saved.

#7 Sampling, curriculum, budget and equity

P0 = 128 structures × 4 rounds × 500 control steps = 256,000 W, saving the actual transfer. Rule controllers are just bootstrap behavior strategies and have no tags for Actor imitation or supervision. P0 contains manual control behaviors that will still affect data distribution and must be accounted for. "No reward optimization" cannot be equated with "no a priori data."

First, a fixed R0 diagnosis is carried out, then the four players are expanded. The rationale is to distinguish between the problem of the realization of algorithms and the problem of complex connections; Successful single R0 does not count the completion of the generic module. The actual V2 starts with an empty Replay, P0 provides only initial reference and replay is empty-time result code, does not add the P0 rule action to the Actor oversight, and does not optimize Replay with its original transfer prefill. Started 8192 online Ws for prefilling. The cost of sharing P0 collection is still accounted for in W, and R0 diagnostics and formal training costs are reported separately and cannot be confused with the results of the generalization. The conditions for passing the diagnosis are predetermined as: no limit, no gradient, no continuous explosion; B to remain multidimensional; Different zs produce differentiated responses; Maintaining/pacing more random Actor queries has improved. Check formulae, sample alignment and data first if not met, without automatic incentive.

The extension is still distributed in four roles, P1 narrow R0/R1, P2 and P3 in full; Finally, 25/30/20/25 per cent will be collected to optimize the four roles of the batch. The old P1 is about 0.8M, P2 is about 4M and a total of 20M is the starting point of the budget and does not require the failure of the diagnosis to continue the course.

Replay original 100Hz, retain episodes according to character quota, select episodes evenly within the character and then select transfer; adjacent x is reconstructed from up to 22 original frames. Zero padding must have padding, and cross-reset is prohibited. Normally, the bootstrap is cut off in 5 seconds; when the value fails, it is stopped and isolated, and there is no early ending mechanism to "escape subsequent negative rewards".

Fifty per cent of the call time is 4/8 moves and 50 per cent is 10/1000 moves. Short events amount to approximately 9.8 per cent of physical time and the logs cannot impersonate the proportion of events as a percentage. This long distribution is used as a cover attempt for future upper 25Hz and is not a standard FB theoretical requirement.

Baseline uses batch512, updated every 256 W, network-wide 1e − 4, γ = .99, target τ = .01, without weighting first. Parallel 128 world/single activity buckets are good for traversing structure libraries within budget, 512 are configurable but must adjust the Replay capacity per character. 512 Measuring higher simulation throughput does not prove faster learning; real training throughput is reported separately.

γ=.99 with 10ms step size, discount time constant `−0.01/log(.99)≈0.995s`, the average number of effective steps is about 100; it does not mean that the strategy can only be called for 1s. The training target assumes that the same z will continue in the future, and collecting and changing z is just a source of data away from the strategy. When the upper layer changes z every 40ms, the combined strategy is no longer the long-term strategy for the fixed z; therefore, the switching capability must be measured and cannot be automatically derived from FB decomposition.

V2 training ρ from Replay batch. When freezing, save the independent result sample according to the final sampling rule, record the ρ source/role ratio, and recalculate the C and query mapping with the same freeze B. The P0 fixed pool is only retained for historical data and optional unified diagnosis, and cannot be used silently as training ρ.

# 8 Project Quality Amendment and Evidence Rules

- Save code copy/hash, input schema, algorithm profile, dependency version, structure list, random seed, actual W, and update times for each run. V1/V2 prohibits mixing.
- The old reset statistics preheat the reset when blending into the construction. This is a log error; after correction, only the formal collection reset will be counted, and the physical state will not be changed. The old count cannot be used to infer the actual ratio of 50/30/20.
- After the old process is stopped, the status is still written training, and it is also called frozen_unit without acceptance. Correct the stop state; candidate modules can be exported, but `validated=false` and phases must be attached, and cannot be marked as completed without acceptance.
- Separate dynamic/reset/incentive/command/exploration random flows by structure + episode ID sample by sample; Replay and optimized random flows are saved separately. Checkpoints are resumed at the boundary of a complete batch and do not claim any millisecond-accurate continuation.
- The snapshot retains the process clock of the occurrence and current excitation, replenishing future pulses can only occur after the retention plan, avoiding repeated recovery and exhaustion of all external force sequences.
- In addition to the single test of the finite difference formula, the numerical loss and F/B/Actor gradient must also be compared; only verifying the dimensionality, limited output, or fixed target z is not enough to claim that the algorithm is correct.

## 9 Admission rules to be modified in the next step

| Candidate modifications | When is it worth doing | What reasons cannot be used to do it directly |
|---|---|---|
| Add history or GRU | Clearly find that the same current input corresponds to different control responses, the existing history cannot be distinguished, and longer information has measurable contributions | Simple training is not good and the mechanical cycle is long |
| Increase z/network | The reference FB has stabilized, and the representation/fitting error continues to be limited by capacity with sufficient data | Only look at the number of motors or lose the absolute value |
| Add task loss | No reward baseline passes, specific required queries cannot be expressed, explicitly do independent supervised ablation | Want to make the curve look better |
| Modify orthogonal weights/normalization | First confirm that it is consistent with the reference value and gradient, and then have stability control evidence | Call all instability a scale problem |
• Clear research into fixed old earnings and cover costs, new versions of independent comparisons  easy to cache by default on their theoretical equivalents
| Add Q loss, conservative regularization, etc. | Have corresponding value error evidence and can be independently verified | Directly superimpose when you see Actor saturation |
| Shorten the time domain of the diagnostic task | Interface calls do require this time domain, and record the physical temporal meaning of gamma | Cover subsequent learning problems with short-sighted scores |

## 10 Current execution status and records

- Completed: Physics/frequency division history/Replay/network engineering main chain; P0 correction and re-acquisition; V1 diagnostic operation and failure record.
- Completed: regular R0 diagnostic and fourth role 20M budget training without V2 incentive; Formula/Gradient check passes before startup.
- Completed: Freezing behaviour assessments, random z spectrographs, switching diagnostics, video and interface delayed measurements, see [result report ](Reward Free V2 Results.md). The generic module has not yet been captured and accepted through capacity; Double-foot training is not within the scope of the current round.

The commands, results, failure reasons and subsequent decisions recorded in order of execution are retained below; the final results are recorded at the end. The end of training does not automatically equate to successful ability, nor does it endorse subsequent modifications in advance.

### 10.1 No reward V2 implementation record

The V1 algorithm source files have been archived to `archive/v1/`. V2 passed 8 checks, including the new independent scalar loop formula and double-precision value of vectorized FB loss and F/B gradient comparison, target gradient isolation, Actor dot product first and then double Q minimum, and B exclusion command field. Single tests do not replace learning ability assessment.

Started:

```bash
unit_bfm/.venv/bin/python -m unit_bfm.train \
  --config unit_bfm/configs/diagnostic_r0.json \
  --out unit_bfm/artifacts/rf_v2_r0
```

The operation uses new weights, fixed nominal R0, and is scheduled to be online at 2.048M W; the log W also includes a shared P0 cost of 256k, and the end point is 2.304M. At the beginning, 8192 W is only collected for forming Replay, without gradient update, to avoid repeatedly constructing 512 batches by only taking the 128 results of the first step. This short pre-fill is an attempt at data sampling, not additional supervision or reward. Training z is relabeled according to the Replay results, and training does not invoke any artificial task rewards. Query results are cached only on paths evaluated without gradients.

(a) Current 1.024MW inspection: to keep the last paragraph of RMSE from 1.170rad which was never trained to about 0.598rad; RMSE has been reduced from 1.881 to approximately 1.238rad/s. B to maintain 16 effective dimensions, with an output model of 4; The unit capacity has not yet been declared approved accordingly. The predefined diagnosis is completed before deciding whether or not to enter the four roles.

Record correction: `train_v1/status.json` ' s old tripining tag has been changed to stopped with reasons for correction. The V2 output `candidate_unit.pt`, which is visible, is no longer accepted only by implication by a file name.

### 10.2 Reasons for the next read-only assessment

At 2.048 M W, the nominal R0 compliance query error is about 0.509 N · m, maintaining about 0.441 rad, and the projected NRMSE is still about 0.4. Using only the reward points query, it is impossible to distinguish between "B is not enough to project the reward" and "π can not keep the target at all". Therefore, add * * static reachable target result query * *: in fixed R0, construct zero velocity, gravity balance driving torque and consistent link attitude g * for legitimate angles such as q * = ± 0.7, ± 0.35, etc., and call with standard target code `z=normalize(B(g*))`. The goal is a complete and consistent physical result, rather than feeding a single angle directly to B.

This evaluation does not modify the training data, objective function, rewards, or network, and does not assume that B(goal) is guaranteed to be reached. Pair with the original reward points query to record the actual q/dq at the end; if both fail, the policy/coverage should be checked. If only the reward query fails, there is evidence to continue to review the task projection. The results have not yet been obtained and the training will not be modified in advance accordingly.

### 10.3 R0 diagnosis completion and expansion decision

`rf_v2_r0` completed 2.048M online W (total log W2.304M including P0), 7,968 updates, nothing more than limited loss. The last F gradient norm is about 208, B is about 2,497, and Actor is about 5.31; the B spectrum is about 0.267–1.905, all 16 dimensions are valid, and there is no sustained scaling loss of V1. Absolute losses from different loss definitions cannot be directly compared.

Pairing 32 fixed initial state results: the maintained RMSE of the complete static target code B(g*) is about 0.122rad, the terminal speed RMS is about 0.000961rad/s; the bonus point query is about 0.343rad; the standard deviation of the terminal angle of the random z result is about 0.746rad, and the average motion range is about 0.901rad. The target query is significantly better than the random z of the same model, but 0.122rad is still not a high-precision control. Random z has no target angle, and its "error to the specified angle" is only used as a reference for pairing, and is not called a random skill failure.

This supports that "callable, different behaviors have appeared in fixed R0" and also shows that reward projection is a restriction that requires single-column observation; it cannot be proved that all mechanical connections can be controlled or that the four types of tasks have been passed. Therefore, complete pre-training of four characters is allowed, **keeping the V2 loss and hyperparameters unchanged, and not adding L_task**. The official expansion starts with a new weight, an independent directory `rf_v2_full/`, and a separate column for R0 diagnostic costs; P0 data is shared and re-collected without repeated claims.

```bash
unit_bfm/.venv/bin/python -m unit_bfm.train \
  --config unit_bfm/configs/train.json \
  --out unit_bfm/artifacts/rf_v2_full
```

The full budget of 20M W includes shared P0, and the last batch of rounds can align the actual W upwards. Each 1M four-character panel is reserved for monitoring, and random z, switching and video are completed after training. A failure is recorded when the ability is insufficient, and the assessment task cannot be temporarily changed in order to obtain a passing conclusion.

### 10.4 Delivery interface completion (without changing the learning method)

The candidate module requires verifiable observation field order, fixed normalization scale, B field selection and calling timing, and cannot rely solely on input dimensions to guess the meaning. Complete the schema list and round-trip verification of frozen interfaces; this is necessary engineering work to prevent subsequent upper-layer connections to incorrect interfaces, and does not increase network input or training targets.

Latency measurements are reported separately for CPU and GPU, and the measurement boundary is "obtained normalized o → history construction → B and cπ feedback → Actor → action retrieval". This does not include real sensor communication or motor communication, nor does it treat simulated throughput as a single control delay. The CPU can be tested independently during training; the GPU should be tested idle after formal training. Report median/P95/P99/Maximum observation time/10ms overdue number, passing the test still does not equal hard real-time guarantee.

After completion, 9 individual tests were passed. Under the CPU single thread and 1000 measurements, the R0 candidate has a single-unit P99 of about 0.294ms and a two-unit batch inference P99 of about 0.350ms, with no 10ms overtime; this is a local observation and is not extrapolated to the embedded motor controller.

### 10.5 Final evaluation and completion: clarify the problem first, then write the code

* * Necessity: * * The upper layer needs to continuously call and change z, just checking the terminal error of the fixed z is not enough to indicate that the interface can be called. Added a read-only toggle panel to freeze training weights, losses, reference distributions, and query definitions. “Necessary” here refers to overriding the declared interface usage and does not refer to requiring all switching durations to precisely reach the target.

- The same structure and 16 identical initial states/dynamics/external force random seeds, the first z is fixed, and the two z's are alternated every 4, 8, 50, and 100 control steps; only commands are changed in the same environment, and the history is not reset. 500 steps per trajectory.
- Nominal R0 is encoded with a consistent `q*=−0.6,+0.6` static result; each of the four characters is selected to reserve a structure and use a pair of spherical random zs, without forcing all structures to any complete target state. 80 tracks per structure for a total of 400 tracks.
- 40/80ms is the future 25/12.5Hz upper layer call stress test; 500/1000ms is used to observe whether the actual movement can respond. If the target is not reached within a short period of time, it will not be judged as a failure. The trajectory difference of q/dq/torque, command change Δu, mechanical power, saturation rate, limit violation and paired fixed z will be reported. Keep the complete time series to prevent only reporting the average value from covering up the transient state.
- Original 32 tasks × 4 initial states × 8 reserved structures = 1024 trajectory panels, paired with the exact same random seeds used by the analytical PD/velocity/impedance controller. The analytic controller is an interpretable reference, not an optimized optimal controller; beating it is not the sole acceptance criterion without user confirmation.
- Random z-maps are 8 independent reserved structures × 256z × 2 independent initial states. It answers the case of behavior distribution and saturation/limitation, * * and cannot prove controllability or the same z cross-structure semantic invariance just by the dispersion of the final state * *.
- Fixed index pre-select visualization: first state of the nominal R0 negative/positive target, toggle first state of the panels 40 ms and 500 ms, and randomly z article 0 of the first structure of each character. Failures are shown as usual, and cases are not selected on the basis of merit.

The trajectory chart also plots the existing target q curve, which is easy to see the steady-state deviation directly; the random z does not specify the q target, and the pairing reference angle is not disguised as a command. The diagram and video are from the save trajectory and do not replace the original case with another random simulation.

Each 1M panel in the training belongs to the repeated monitoring set and cannot be called an unseen test set again. In the final 8-structure panel, each role index 0 is repeated with the monitoring set, and index 1 is the expanded new structure, and the statistics are reported separately. Random maps and switching structures use additional independent seeds, and leaving within the distribution does not equal generalization outside the topology.

Post-processing can export a separate schema file for the candidate, recording the original checkpoint hash, post-processing code hash, physics/learning method version, `validated=false`. Do not overwrite the original training source code snapshot and claim that the completion code participated in this training.

The evaluation summary program reads only the existing JSON/trajectory: the original unit error is reported by role, monitoring multiplexed structure and new structure, and the parsing reference is matched on a case-by-case basis; at the same time, the end-state distribution, motion range, saturation/limit occupancy, and training gradient and B spectrum of random z are summarized. Save the original record, do not introduce the success threshold afterwards, and do not write the average score of a single seed as a statistically significant improvement. The control law of the parsing controller does not use the network, so it can be independently evaluated in advance; the characterization diagnosis in its file comes from the intermediate checkpoint at loading, and cannot be mixed with the final model diagnosis. Throughput during parallel evaluation includes GPU competition, a non-exclusive performance benchmark.

## 11 Precise ledger and applicable boundaries of randomization implementation

The following table corresponds to `mechanics.py`, `environment.py`, and `kernels.py`, which is used to avoid writing "randomization into consideration" as an unreproducible slogan. Except for the structure determined by the user, the numerical range is the first round of coverage attempts; it is not the optimal distribution derived from FB theory.

 Level  Samples have been achieved  Reasons and boundaries
|---|---|---|
| Structure library | 32 fixed structures for each character; the first 8 narrow ranges: P length 0.225–0.275m, D length 0.315–0.385m, P mass 0.85–1.15kg, D mass 0.2125–0.2875kg; the rest: length 0.15–0.4/0.25–0.45m, mass 0.4–2/0.15–0.6kg | The length is uniform and the mass is logarithmically uniform; first control the difficulty and then add different inertia/leverage, it cannot be called continuous. All structures have been trained |
| Consistent counterweight | Each LINK counterweight of the wide structure is 0–20% of the body mass, 20–80% along the length, x offset 0.01m; real sphere geometry synthetic mass/inertia/COM; R0 base inclination angle ±0.5rad | Provides mass distribution changes to avoid independent random changes in inertia resulting in non-physical bodies |
| Round dynamics | Density multiplication per rigid body 0.8–1.2; motor damping 0.01–0.08N·m·s/rad, friction 0–0.08N·m, armature logarithmic uniformity 0.001–0.006kg·m²; ground sliding friction 0.4–1 | Mass and inertia are multiplied together; no actual random parameters are provided; nominal parameter m remains unchanged |
| Motor | Capacity 4.8–7.2N·m, T uniformity 5–20ms, integer delay 0–10ms | The command amplitude is still defined by the nominal 6N·m; the internal state of the first-order drive is continuously retained, and the request u cannot be regarded as the actual torque |
| R1 support | kx20–200N/m, kz100–500N/m, kθ0.1–5N·m/rad; damping is calculated according to damping ratio 0.3–1 and mass/approximate inertia; vertical gravity preload | limited reaction boundary; damping is not critical damping of the exact coupled mode; actual support parameters are not given to the network |
 External force  0.5-2s, continuous 0.1-0.5s, 50 ms cosine edge; (b) Power band 0-0.5 mg, direction 0-2 gill, extra-power rectangular ± 1.8 N m, random P/D and 20-80% force point along the pole  change load; M is the overall quality of the institution, and R3 contains the outer LINK; The future plan is hidden. Actor only sees what's happening.
| R3 Peripheral | Sinusoidal target amplitude 0.1-0.7rad on both sides, frequency 0.3-2Hz, phase 0-2π; PD (8,0.5), torque limit ± 3.6N · m | Adjacent action with limited bandwidth/torque, independent of this unit z; not representative of a whole body strategy or any neighbor |
| Ordinary/wide initial state | motor q±0.6/±1.1rad, dq±2/±4rad/s; R1 root translation ±0.05m, pitch±0.35rad; R3 peripheral q±0.6, dq±1.5 | First adopt generalized coordinates/velocity, then obtain the LINK state from forward kinematics, and splice inconsistent observations independently |
| R2 initial state | The root pitch is sampled from ±0.35rad near 0 or π; the root height is translated according to the actual lowest point of the box, 80% is 1mm above the ground, and 20% is 2–10cm above the ground; root speed vx±0.5, vz±0.3m/s, ω±1.5rad/s | No deep penetration initially; contact marks, impulses and contact points are not forged |
| Access snapshot | Normal 50%, width 30%, snapshot 20%; independent library for each structure, save the first 8 world in 1.25/2.5/3.75s, up to 128 entries; empty library returns to normal/wide according to 5:3 | Save accessed dynamic status and driver queue/physical parameters; network history restarts. The first 8world is not uniformly sampled across all trajectories and does not claim optimal coverage |

P1's `level=0` turns off density, motor parameters and pulse amplitude changes; P2 linearly amplifies most continuous parameters, P3=1. Realize that not all random quantities are continuously annealed: as long as level>0, the delay is taken as a whole 0-10ms; the R1 damping ratio, initial state and R3 peripheral parameters are still random. The structure also expands from 8 structures to 32 when entering P2, rather than continuous interpolation. **Therefore, it can only be called a partial course, and cannot be called a smooth increase in dynamics from easy to difficult. ** The actual mechanism of this round is retained. You cannot build another distribution midway but still use the same run label.

## 12 Logical Boundaries of Representation and Physical Control

`z` is the 16-dimensional potential direction of future visit preferences, and `B(g)` is the 16-dimensional encoding of the current result. They do not guarantee that each dimension corresponds to a certain q, velocity or force, nor do they mean that the upper layer can arbitrarily specify 23 result components. The control rights of a single degree of freedom are limited, and many LINK movements and forces are determined by supports/neighbors/contacts; F should learn this conditional accessibility, and the Actor can only respond within the actual controllable range.

This is also the reason why B does not undertake dynamic identification: the current result g can be produced by multiple ontologies, and the structure m and history are left to F/Actor. Whether B feedback is helpful, whether cπ contains transferable dynamic information, and whether the 200ms history is sufficient all require subsequent upper layers and information ablation to prove. The true value of this round of privilege verification is "whether useful behaviors can be learned when there is sufficient local feedback." It cannot be claimed based on this that real machines can be deployed or that the difficulty of bipedal learning has been reduced.

## 13 Complete V2 training result record

`rf_v2_full/` has been completed, with total W=20,032,000, including shared P0=256,000, online W=19,776,000, updated 77,218 times, and took 2,059.9s. The extra 32,000 W comes from the full 500-step parallel round alignment. There is also 2,048,000 W for R0 diagnosis online, which is accounted for separately.

The training has complete access to 128 structures. The online W of the four characters are 6,208,000/5,952,000/3,392,000/4,224,000 respectively; the overall proportion is affected by the P1/P2 course and cannot be written as 25/30/20/25 for the whole process. . In 39,552 online rounds, there were 21,806 normal resets, 13,054 wide resets, and 4,692 snapshots. Another 3,336 snapshot samples were returned to normal/wide due to the library not being ready; the actual usage rate of snapshots is about 11.9%, not the nominal 20%.

All records have a limited amount of learning, and the B threshold rank is always 16. The end point F/B/Actor gradient norm is about 2,138/2,645/5.20, the B second-order moment spectrum is 0.333–1.928, and the query projection NRMSE is about 0.655. **These only prove the numerical operation and cannot prove the performance of the four types of queries. ** It has been verified that the learning, network, physics, history, Replay and training loop source code hashes are consistent with the startup snapshot, and these codes have not been modified midway in this round.

The final candidate is saved as `validated=false`. The results of 1024 semantic queries, paired parsing references, 4096 random z trajectories, 400 switching trajectories and nominal R0 target panels are summarized separately; errors in repeated monitoring must not be regarded as the final independent test conclusion.

#13.1 Additional diagnostic access after final panel

The results of the 32 cases of R0 in the final name are different from those of the early R0 diagnosis: the incentive score is about 0.09777rad and the complete target result B (g*) is about 0.4954rad. ** The "Target code better than reward query" of 10.3 cannot be extended to the final shared model. ** Complete static physical objectives are achievable and the point-coding strategy of limited-dimensional FB is not guaranteed to reach it precisely; Current evidence can only confirm that there are differences in performance between the two inquiries, the cause of which has not yet been determined.

The original scheduled switching panel uses B(g*), so it cannot independently answer whether the better-performing reward point interface can continuously change orders. It is allowed to add a set of **post-mortem diagnosis**: still using the same nominal R0, 16 initial states, fixed/40/80/500/1000ms, the same ±0.6rad target and random seeds, only changing the command encoding to the already defined retention bonus points. The original 400 tracks are not covered, and the new 80 tracks are saved `switching_reward/`. Do not change reward coefficients, networks, training weights or training samples, nor pass new diagnostics off as pre-agreed main tests.

#13.2 Evidence of final conduct and current round of decisions

The main evaluation and supplementary diagnosis have been completed. For detailed original unit indicators, videos, graphs, input contracts and source code basis, see [No Reward V2 Training Results ](Reward Free V2 Results.md).

| Mean of 1024 paired trajectories | FB | Analysis reference |
|---|---:|---:|
| Maintain final angle RMSE / rad | 0.4509 | 0.1007 |
| Feasible interval speed RMSE / rad/s | 4.5397 | 2.7280 |
| Braking end speed RMS / rad/s | 0.9986 | 1.2322 |
| Compliance moment relationship RMSE / N·m | 3.9780 | 0.5103 |

The final stages of the 64 cases of R2 braking are all at `|q|>1.1rad`, and the request saturation is about 95%; its low speed cannot be used as evidence of high-quality braking. In the independent random map, R2 request saturation is about 87%, and near-limit occupancy is about 84%. Currently, a reliable contact interaction behavior library has not yet been formed.

The nominal R0 reward keeps the query RMSE around 0.0977rad. The 500/1000ms alternating ±0.6rad command in the supplementary switching panel can organize reciprocating motion, and the RMSE of the whole process is about 0.393/0.288rad; this includes the command change transient, which is different from the final holding indicator. The average absolute Δu of the 40ms command change is about 1.44, which cannot be called a natural smooth interface. All scheduled B target switching failure cases are still retained.

The native single-threaded CPU single/dual unit P99 is 0.297/0.362ms; the idle GPU is 2.417/2.412ms, and there is no 10ms overtime within the measurement. Deliver independent candidate weights, schema, 197-dimensional feedback interface, 12 fixed index videos and original trajectories, still labeled `validated=false`.

**Decision of this round: Complete and retain this baseline, and do not chase the current panel results by increasing task rewards, changing limit rewards, or expanding the network. ** The results support local callable motion prototypes and are not yet sufficient for acceptance of the general execution unit. Subsequently, you should first check the differences between R2 control/coverage and the two queries in isolation, and then demonstrate the modifications one by one according to Section 9; if there is no evidence, jump directly to "FB is worthless" or "just need a larger network". Whether upper-level bipedal learning burden is reduced still needs to be independently verified.

### 13.3 Design review of two sides, three-dimensional state, obstruction and force application

2026-10-01 New [Unit status, observation and 3D randomization discussion ](Unit State and 3D Randomization.md), as a follow-up design discussion, do not modify the training contract or weight of this round. P/D is the parent/child side coordinate convention of the model tree, not the permanent support/output end; the current structural distribution on both sides and the R0/R1 support selection have a prototype bias, which cannot be claimed to be suitable for mechanical splicing in any direction. Future exchange coverage must simultaneously transform geometry, axes, coordinates, and behavioral semantics.

The review distinguishes between control rights for the current g23, complete mechanical status, motor telemetry observable information, and single torque. Three-dimensional connections require the co-expansion of three-dimensional motion, gravity, inertia, and interactive representations; motor history does not guarantee recovery of world translation speed or arbitrary contact wrench. Upright, node speed, blocked and specified contact forces require legal boundaries and continuous physical processes, and the result vector cannot be filled in independently and randomly. The existing limited/ground contact coverage does not mean that the blocked call has been trained and verified; the random extrapolation force does not mean the active force application capability.

The ](Evaluation Web App Guide.md) website has been added to freeze Actor feedback, simultaneous disturbance action playback and undisturbed reference three branches to support operational disturbance, pause, 10 ms single step, preservation and playback. It checks the actual correction of the feedback control, does not add a training incentive or a FB loss, nor does it replace the upper learning difficulty and three-dimensional generic validation.

Additional review and confirmation: The physical joint limit of this round is always ± 1.2rad, and the limit has not been changed in the structure library and round randomization; the inclusion of the limit field does not constitute variable limit training. The original webpage ± 0.8rad is from the query parameter check and has been expanded to [-π, π] in the interactive evaluation. The webpage also opens up the actual structure, dynamics, drive, connection boundary and limit editing; the variable limit is only used as a clearly marked outside training evaluation, and has not yet been trained. The initial state, model, m and result records are consistent, and the old training source code has not been modified.

The world posture, velocity and environment wrench belong to the simulation privileged input; gravity is a fixed environmental parameter, and the pole world pitch provides implicit information relative to the fixed gravity direction. They are not ordinary motor telemetry. The current Actor and B use these fields, and subsequent telemetry versions cannot use the→ current weights by simply→ setting zero→. 2026-10-02 [Unit interface→ and V2 implementation are compared to ](Unit State and 3D Randomization.md), distinguishing design requirements, existing implementation and verification capabilities; original mechanical scope, Replay limit set, and evidence of failure to maintain the target are retained in the appendix. The paper also verifies the realized 197-dimensional feedback and four-unit bipedal access, and the access inspection is not equal to the upper-level walking or reuse revenue acceptance.
