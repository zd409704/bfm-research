# V3 training project implementation design

This article records the actual design of the isolation project, covering the full sequence storage in the old scheme, and expands the terms of Replay according to the full episode. The network/FB semantics still follow the original V3 scheme. The implementation of the repair and evidence is subject to [acceptance record ](Development and Acceptance Record.md), which cannot be deduced from the interface in this article has been completed.

# From physics to learning

A world is a motor, P rod on the housing side and D rod on the output side, which can be supported, adjacent and contacted with objects. Emulator MuJoCo, 1ms physics/driver, 10ms control boundaries. CPU native solution and Warp/mjlab batch solution use the same integer physics tick to drive the external load/obstacle program to avoid staggering events by the floating-point accumulation clock. In each sub-step, the force and reference system of the same solve are first solved and extracted, and then integrated; the geometry of the next boundary and the force of the previous solve are explicitly time-marked.

the collector builds the complete feature update memory needed for x/g and F at the real boundary. Currently there are bounded multiple world episodes temporarily inserted into Replay, which is not a permanent archive or an infinitely long rollout; the temporal budget is 512MiB, which exceeds the explicit rejection. Invalid value transfer does not enter FB, legally blocking/loading/contact remains in the data. Normal time truncation uses the real last state bootstrap and cannot be connected to the state after reset.

The control action is the normalized output axis request u, and the actual request scale S, limiter, delay and first-order response are implemented by the driver. Replay records u instead of the measured torque after delay; tau is the response state. Rules PD/PI, speed, sweep, compliance and pulse are just collection behaviors and do not constitute supervision labels or training rewards. Rules can use explicitly annotated simulation feedforward, and Actors cannot derive the truth value from this.

## Why is the input divided like this?

B Use g13: P/D length, specification mechanical angles q, dq, output shaft tau, mechanical limit, M-series relative terminal velocity, causal angular acceleration/relative terminal acceleration and effective bit. This definition distinguishes local results and cannot claim that B uniquely identifies contact locations, world postures, or dynamic loads. The current precision shaft torque is simulated privileged telemetry; deployment requires a real measurement/estimation interface.

Actor uses x137: g13, known rigid body parameters 8 + valid bits 8, declared drive parameters 8 + valid bits 8, slow history 10×6, fast history 8×4. Slow history is 50Hz, fast history is 100Hz; no GRU is added. True unknown mass/capacity errors, environmental exposure and external loads do not mix into declared values. B does not directly read the motor model, capacity or unknown load.

F reads [x, p], p is the actual physical registry + 243-dimensional feature updater memory, currently 4822 + 243 = 5065. The real rigid body/connection/loading controller status, drive queue, support, ground, contact, tree reaction force, etc. come from the real model/current solution and do not fill in zeros out of thin air. The slot that does not exist has a mask; solve_valid=0 when reset has not yet solved the force. Fields have source, unit, scale, time, and coordinate conventions. Mask can only express the non-existence/no effective solve yet, and cannot cover up the necessary quantities that have not yet been realized.

B outputs z16 spherical vector; each z coordinate does not have a manually specified physical axis. The current B encodes the target g, or integrates the explicit query under a fixed reference distribution to obtain the command z. The subsequent result of F science condition is occupied, and B is optimized with the joint FB to shape the result representation; privileged entry into F does not make the Actor possess unobservable information. Complete Markovness is an engineering assumption that needs to be checked by counterexamples, and it does not automatically hold true if there are many fields.

The hidden structure remains unchanged: Actor/F double branch, 256→128, 256 heads after splicing; B is 13→256→256→16. Actor207617, B74000, a total of 281617 executions; F each 2805008 (current p dimension), a total of 5891633 online. The training F becomes larger from the real input without changing the deployed Actor/B size.

# Replay vs. Reference Distribution

The default CPU FP32 rule32768+policy65536; 16384 in the rule is the P0 fixed anchor point, and the rest are scrolling. The cumulative collection budget of P0 can far exceed the capacity of the anchor point. The reserve is reserved hierarchically according to the configuration. Online rules do not cover frozen anchor points. Reserved cannot be filtered by posterior success. If the parameters are different but g is the same, B does not require forced differentiation. F is responsible for the condition difference.

Cache Visible pairs x, p, u, x_next, p_next, g_next, discount, history-generation. The inspection of the 4Gib Replay budget on a physical p-dimensional basis, with an over-restricted small volume or a clear error reporting, cannot be forged by removing the true value of the physical meaning. The current default size is about 3.816 GiB, index/approve temporary save; The cumulative amount of 20M does not equal 20M permanent memory.

Before learning, ensure that both rules and strategies have valid data. Each row is independently sampled: source 50/50 → working condition weight → configuration equal weight within the working condition → ξ/dq/tau/current process key family .4/.2/.2/.2 → existing bin equal weight → intra-bin transfer equal weight. Sum the marginal probabilities of repeated paths. The partial and renormalized distributions are disclosed when working conditions/configurations are missing; the strict integrity check rejects the missing groups individually, and does not regard coverage shortfalls as the reason why legal samples cannot be learned.

The goal is a complete g independently extracted under the same geometry/limit, and the old network z is not saved as a learning target. B is re-encoded every time it is updated; the rollout snapshot Actor/B is used to collect, the internal z is called to hold, and the next call is re-selected. The query library records Replay instances, content revisions and ρ, and cannot be silently reused across libraries/old ρ.

## Update and restore

Use the given FB Bellman non-diagonal term, diagonal positive term, B orthogonal term, and Actor target; the double F target is averaged, and the Actor takes the double F minimum after the dot product z. No task reward, no imitation/load regression loss, no default gradient cropping. Non-finite loss/gradient explicitly fails and cannot silently skip masking.

Each row has discount=.99×(1-terminated), shape [N,1]; normal time limit bootstrap. The update credit is accumulated by the number of new effective interactions after warmup × the configuration updates_per_W. The offline training quota will not be issued for P0 installation. Randomized coverage statistics guide the next round of supplementary acquisition, and running to a certain stage cannot replace actual visits and gradient usage evidence.

Checkpoint pauses writing at the rollout boundary and saves network/targets/optimizers, RNG, scheduling debt, current bounded Replay, schema/configuration version and count. Only model hot start and accurate continued training are separated. Snapshot reset saves the physical/driver/external process of the same model, restores its ticks, and generates new history padding; snapshot is not a training checkpoint.

By default only limited full checkpoints are scrolled; limited reviewable trajectories can be saved for evaluation/calibration. Old run and V2 products are not deleted. The training main path does not have a gzip/npz full episode dependency.

# How Randomization Becomes Data

Parameters are written to the real MuJoCo model or real drive/external loader; separate seeds are used, the geometry catalog is fixed, and the round dynamic conditions are redrawn. The mechanical limit comes from the independent P/D collision stroke gate post-indentation and four stroke configurations, not dead ± 1.2. The object is placed in the normal direction according to the real surface, and the initial installation is illegal to refuse/re-open; do not close the self-collision to obtain false range.

E0 fixed, E1 soft, E2 contact, E3 neighbour, E4 combination movement by effective step; Each scene is independently constructed to avoid two global cycle bindings. Dynamic variants include mass/weighting/declaration error, driver response/delayed/capacity/resistance, code zero/direction, installation, loading side/point/direction/time series, single/double-neighborship and support. Reset has three types of position-level, velocity-level and model-based physical snapshot reporting instead of only target ratios.

Override statistical sub-parameter distribution, local state sub-boxing, continuous loading/blocking/release response, combinatorial conditions, and actual gradient usage. full requires 144 configurations x 5 scenarios for long-term checks; E0 results for short devs do not compensate. The implementation of free three-dimensional, arbitrary closed chain, bipedal upper layer and high-throughput pure equipment in the original scheme is not considered complete because of the existence of this round of code.

# The receiving and inspection boundary #

Check V2 unchanged, input source/time, physical force balance and same solve, CPU/GPU pairing, over-capacity replay and distribution, failure isolation, real optimization, accurate recovery, export and freeze evaluation in order. The latest independent GPU pairing and 40 times of CUDA learning in five scenarios have been passed; the final rework of P0/scheduling/save and failure statistics is subject to the acceptance record. The success of a skill must also look at target accessibility, maintenance, speed/force, disturbance response and unseen connection conditions, not just loss reduction.


## Actual measurement of default capacity resources (final Replay layout)

The main window is measured under p_total5065, rule32768 + policy65536: 98304 tensors 4096917504 bytes, full library synchronization checkpoint4104281452 bytes; process peak RSS4694069248 bytes, save 2.67 seconds. Full load/takeover after release of old library, RSS4664262656 bytes, 2.17 seconds. When a quarter is active, only the corresponding 1024MB tensor is saved, but compact temporarily copies this part, with a peak RSS of about 2.56 GB. This is a Replay special, not including all training environments/optimizers; partial near full library may copy nearly 4GB, together with rollout and network computing host margin, can not claim 4GiB is the upper limit of the entire process.

Layered P0 allocates the remainder through divmod. By default, 720 groups are divided into a total of 16384 anchor points, leaving no permanent empty slots. If the P0 budget is too small and not all groups have been accessed, partial training is still allowed and unfilled slots are truthfully recorded; there is no pretense of full database zero replication.
