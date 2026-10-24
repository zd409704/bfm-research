# V1 Training Design Instructions: Input, Environment, Task Sampling, z and Loss

Version: `SIM_PRIVILEGED_FF_MR_V1`. This article compiles the source code, running manifest, and design records of V1 after the fact, and records the actual solutions and inadequacies adopted at that time, which does not mean that these choices have been justified as necessary. The current implementation basis of V2 is still [training engineering implementation design ](Training Engineering Design.md).

V1 is "FB successor representation + artificial task bias + reward representation auxiliary supervision". Holding, speed, braking and compliance rewards both affect training z and supervise B through auxiliary loss; this version cannot be called pure reward-free FB.

## 1 Source code basis and historical record boundary

- SHA-256 of the [archived network ](../archive/v1/networks.py), [archived Learner ](../archive/v1/learner.py), [archived training cycle ](../archive/v1/train.py) is consistent with [V1 runningmanise ](../artifacts/train_v1/manifest.json).
- The hashes of the current `mechanics.py`, `kernels.py`, `history.py`, `bootstrap.py` are also consistent with the manifest, which can check the mechanical structure, attitude observation, historical structure and P0 acquisition at that time.
- There have been subsequent modifications to `tasks.py`, `replay.py`, and `environment.py`. V1 does not completely retain the original source code copies of these three files. This article explains them in conjunction with historical design records, call sites, and existing implementations; it does not claim to have restored the complete V1 runtime environment verbatim. In particular, the subsequently revised reset statistics, snapshot excitation supplementary logic and V2 sampling method cannot be written backwards into V1 facts.
- `archive/v1/` is an audit archive and cannot be run directly as an independent training package with complete dependencies.

## 2 What are the sinθ and cosθ of the two LINKs?

The simulation motion is limited to the world x-z plane, and the rotation axis is y. θP and θD respectively represent the attitude angle of the rigid body coordinate system of the near-end LINK P and the far-end LINK D relative to the world coordinate system and around the +y axis. They are not two new joint angles, nor do they represent position, velocity, or two additional controllable degrees of freedom.

In this planar model, the rigid body rotation matrix is:

\[
R_y(\theta)=
\begin{bmatrix}
\cos\theta&0&\sin\theta\\
0&1&0\\
-\sin\theta&0&\cos\theta
\end{bmatrix}.
\]

`kernels.observe` reads the MuJoCo rigid body world rotation matrix `xmat`, and directly takes `R[0,2]` and `R[0,0]` as sinθ and cosθ. Each LINK has two dimensions, totaling four dimensions. It does not first estimate these quantities using the motor encoder.

The connecting rod of the model extends along the local −z direction of the rigid body, so when θ=0, the connecting rod points in the world −z direction, that is, downward. The unit direction from the near end to the far end is `(−sinθ, 0, −cosθ)`; θ=0 cannot be mistakenly drawn as the connecting rod pointing upward. The attitude of a complete circle is represented by sin/cos to avoid the numerical jump of the direct angle at −π and π.

The current model has no additional joint zero-position posture offset, so:

\[
\theta_D=\theta_P+q\pmod{2\pi}.
\]

For example, q=0 only means that the two LINKs are aligned with each other. They may be vertical, inclined, or horizontal; the gravitational moment, grounding relationship, and load response are different in these cases. LINK World Pose complements the overall orientation that joint encoders alone cannot provide.

| Field | What does it mean | Whether it comes from a common single motor encoder |
|---|---|---|
| q | Relative joint angle between two LINKs | Usually OK |
| sinθP, cosθP | World posture of the proximal link | Can't be obtained only with this joint encoder |
| sinθD, cosθD | World pose of far-end LINK | Requires proximal/base pose and kinematics, or additional pose measurements |

If θP and q are already known, θD can be calculated in this model, so the three angle descriptions contain kinematic redundancy. Preserving the poses on both sides is a choice for local observations of V1 symmetry and is not the mathematically minimum necessary input. In R0, θP is fixed, and the redundancy is more obvious; in R1/R2/R3, the proximal end moves, and the overall orientation information is more useful.

The first round directly uses the simulation value, which belongs to the privileged information. The real machine can consider such sources as the base/connecting rod IMU and positive kinematics, and cannot equate universal motor telemetry with link world posture. This article does not modify existing networks accordingly.

In order to check the symbol convention, an uncontrolled positive kinematics check was performed on each of the four mechanisms: θP = 0.3rad, q = 0.4rad, and the read rotation matrix obtained θD ≈ 0.7rad. This is just a coordinate interpretation test, not a learning ability test.

## 3 Input and time meaning of Actor, F, B

# # 3.1 Current local observations o24

| Fields | Dimensions | Time/Source |
|---|---:|---|
| q, dq | 2 | Joint motion of the current control boundary |
| Sinθ, cosθ, COM vx/vz, ωy of each LINK | 10 | Current world attitude, center of mass velocity and angular velocity; simulation true value |
| Actual drive torque τm | 1 | Interval end torque after motor delay/response; simulation value |
| Previous sent torque request u | 1 | Known commands |
| Per link contact sign | 1 | Contact within 10ms of the end |
| Distance from upper and lower limits | 2 | Calculated by q and known limits |
| Fx/Fz/My per LINK environment | 6 | Just ended the average environment wrench of 10ms; simulation true value |

The LINK velocity takes the center of mass and world coordinate components; My is about the center of mass of each LINK. The environment wrench includes contacts, fixtures, and explicit external forces, but does not include gravity and complete internal joint reactions. The observation does not input the absolute translation position of the world, nor is it a complete simulation state.

The fixed divisors include: 1.2rad for q, 6rad/s for dq and ω, 2m/s for COM speed, 6N·m for τm and My, 20N for environmental force, and 2.4rad for limit distance. sin/cos, contact flags and u are not scaled separately.

### 3.2 Nominal structure m28 and history

m contains 14 nominal parameters and 14 active bits: 2 LINK length/mass/Iyy 6D, 2 LINK hythms having a relative control of a joint x/z bias of 4D, and upper and lower joints and a constant of nominal rectangular capacity/electricity 4D. These are known structural information and are not actual quality, friction, delay after the round is randomized.

- Slow history: 50Hz × 10 items, each item has o24 summary + padding + age, a total of 260 dimensions. The ten endpoints are 20ms apart, span 180ms from beginning to end, and the summary interval covers 200ms; at odd-numbered control steps, the latest slow endpoint lags behind the current one by 10ms.
- Quick-record: 100 Hzx8, each of which has been sent u, actual m and padding, for a total of 24 dimensions, covering eight 10 m drive compartments.
- The motion field of the slow summary takes the end point; u and τm take the mean of the two samples; the contact takes the OR; the environment wrench takes the mean. It is not a simple repeated stack of frames, nor is it a lossless history.
-Reset will clear the history, and changing tasks/z will clear the history. There is no GRU and no separate supervision of quality, friction, and latency estimates.

So `x336=o24+m28+260+24`.

### 3.3 Three types of networks

| Network | Input | Output |
|---|---|---|
| Actor | x336, z16 | Normalized torque request u1 |
| F1, F2 | x336, actual sent requests u1, z16 | Each 16-dimensional successor feature |
| B | y25 | 16-dimensional result characterization, V1 does not output spherical normalization |

For the decision moment t, the last command in x_t is u_(t − 1). After sending u_t and running 10ms:

\[
y_{t+1}=[o_{t+1},\;u_t-u_{t-1}],
\]

Among them, the command field of o_(t+1) is already u_t. What B receives is the partial result of a real transfer, without structure, history, z, task number or future disturbance plan. B contains u and Δu to express the additional command cost of V1, and is not a requirement of FB theory.

Actor and F use a feedforward double-branch structure with a width of 256; Actor-state branches produce cπ128. B is an MLP of 25→→ 256 256→ 16 with LayerNorm/Tanh behind the first floor. Number of parameters: Actor309,505, each F313,616, B77,072; online total 1,013,809, execution Actor + B = 386,577. The feedback interface is o24 + m28 + B16 + cπ128 + valid1 = 197 dimensions; its benefit to the upper layer is not proven in V1.

## 4 Mechanical environment and tasks are distributed at two levels

R0–R3 defines “the mechanical environment in which the unit is connected”; H/V/D/C defines “what behavior is expected to be performed this time”. They do not have a one-to-one binding relationship. R0 does not only train holding, nor does R2 specifically train braking or balance.

The role, the mechanical condition, the role and the boundary, the role, the boundaries, the relationship, the relationship, the relationship, the relationship, the relationship, the relationship between the two.
|---|---|---|
| R0 | P's complete posture is fixed, D moves around the controlled joint | Basic control; not just fixed, allowing P to rotate freely |
| R1 | P has plane translation/rotation degrees of freedom, supported by finite springs, damping, and gravity preload | experiences proximal motion and reaction |
| R2 | The double LINK floats in the plane as a whole and is in contact with the ground | Experiences support switching; there is no separate training balance task |
 R3  4LINK chains, fixed roots, learning control middle joints, and both sides are driven by a limited-strength PD  experience a neighbourhood drive; Not many of the modules are working together.

R0/R1/R3 Use free-space conditions without self-collision, R2 enable ground contact. The simulation adopts MuJoCo/MJLab/MuJoCo-Warp, physics and drive 1kHz, actor control 100Hz.

32 pre-built nominal structures per character: 8 narrow range, 24 wide range. Select one character and one structure at a time online to create 128 instances of the same geometry, each with independent random dynamics, initial states, and excitations. Run 500 control steps, that is, 5 seconds, resulting in 64,000 transitions, and then change the structure.

Roles are dispatched according to the cumulative quota difference: each batch is given the cumulative target weight of four roles, the role with the largest current debt is selected, and the quota is deducted once after selection; the structural index is shuffled and traversed within the applicable set. It is not a fixed division of 128 worlds into four groups at a time.

| Stage | Online budget threshold | Collection ratio R0/R1/R2/R3 | Replay source character ratio |
|---|---:|---|---|
| P1 | First 800,000 W | 70/30/0/0% | 70/30/0/0% |
| P2 | Next 4,000,000 W | Linear transition from upside to 25/30/20/25% | Transition to 25/25/25/25% |
| P3 | Remaining budget, total W target 20m including P0 | 25/30/20/25% | 25% for each of the four roles |

Stages switch at the full batch boundary, so the actual boundary can exceed the budget threshold. P1 only selected 8 narrow-range structures per character, and P2 expanded to 32; it was not a smooth change of geometry millimeter by millimeter.

## 5 How to select and execute tasks in a batch of 128 environments

Each world has its own command random stream and remaining call steps. At the beginning, the number of steps remaining is 0, and then whenever the countdown ends, the command is exchanged for the world. Changing tasks does not rebuild the environment, does not reset the mechanical state, and is unclear about the history.

The core process is consistent with the V1 archive training loop. The following is illustrative pseudocode:

```text
Select this batch of roles and nominal structures to create 128 random instances
For each control step:
world due for all calls:
Uniformly extract task categories and parameter alpha from H/V/D/C
If C is drawn, try to filter the initial expected torque according to the existing rules
Change command to random sphere z with 20% probability
Otherwise, calculate z_alpha using the currently cached B and bonus points
Draw the duration of this call independently, save z and countdown
Each world performs Actor (x, z) + Discovery Noise
Run 10 1ms physical sub-steps to obtain real motion and force
Save the original observation and reduce the countdown by 1; update the network from Replay according to the budget
```

| Final Order Source | Theoretical Probability of a Single Order Exchange |
|---|---:|
| H maintain | 0.8×0.25=20% |
| V speed | 20% |
| D brake | 20% |
| C Compliance | 20% |
| Random sphere z | 20% |

This is an independent random sampling with no forced integer quota. When the first 128 worlds are drawn at the same time, 25.6 are expected, and exactly 25 or 26 are not guaranteed. Subsequent calls expire asynchronously and do not permanently fix which world belongs to which task. In the same batch of R0, there can be simultaneously the holding of the target q = 0.3, the speed, braking, compliance and random z of the target dq = − 1.

Task classes do not automatically change mass, gravity, connection constraints, or the ground, nor do they apply additional external forces to pull joints to their targets. Online Actors always output torque requests. Only the P0 rule acquisition phase directly generates actions by the explicit PD/speed/impedance control law.

Call duration: 50% of the events take 4 or 8 steps, that is, 40/80ms; 50% of the events take 10-100 steps, that is, 100-1000ms. Short events account for about 9.8% of the expected physical time, and the event proportion cannot be said to be the time proportion. Online request is to superimpose Gaussian exploration noise with standard deviation 0.15, and then limit it to [−1,1].

The nominal requested torque is 6u N·m, which becomes τm after 0–10ms delay, actual capacity limit and first-order motor response. F takes sent u as the action condition; it does not pretend that τm after delay is the action issued by the controller at that time.

### 5.1 Task parameters and filtering

| Family | Parameter Sampling |
|---|---|
| H | q* uniform −0.8 to 0.8rad |
| V | dq* discretely sampled from ±0.5, ±1, ±2, ±4rad/s |
D  velocity square weight a equilibria of 0.5 to 2; Positive weight b. evenly 0.05-0.2
| C | q_ref uniform ± 0.6rad; K log uniform 0.3–12; D log uniform 0.02–0.5; bias uniform ± 1N · m |

For the C drawn during collection, there is an 80% probability of trying to re-collect the parameters, making `abs(bias+K(q_ref−q)−D dq)≤4.8N·m` at that time. The maximum number of attempts is 32, which cannot be said to be a hard constraint that is strictly guaranteed to be met. This filtering occurs before random z replacement, so some filtered tasks still end up being replaced by random z.

Filtering will make the collected C parameter distribution dependent on the current q/dq, but does not change the 20% final event probability of the C family. There is no C filtering based on the current state when resampling z during the optimization phase; the acquisition task parameter distribution is not exactly the same as the training task parameter distribution.

## 6 How to determine which z corresponds to a task

There is no pre-specified "first dimension of z is hold, second dimension is speed", and there is no fixed z list by task category lookup table. The task alpha first defines a reward function and then maps the reward function to a potential direction with the help of the current B.

The fixed reference pool ρ contains 65,536 actual results collected by P0, 16,384 for each character. V1 fixed draw 4,096 results as coding cache. For reward r_alpha:

\[
c_\alpha\approx\frac1{4096}\sum_{j=1}^{4096}
B(y_j)r_\alpha(y_j),\qquad
z_\alpha=4\frac{c_\alpha}{\|c_\alpha\|}.
\]

For example, "Keep q*=0.3rad": Instead of putting 0.3 directly into z, the 4096 reference results are calculated one by one to keep the rewards, and then the respective 16-dimensional B results are multiplied by the corresponding rewards, averaged and normalized. Rewards have positive and negative signs, and this process cannot be interpreted as probability weighting or selecting only the highest reward samples; the code does not implement softmax.

What is calculated is the task encoding based on the current representation, not the verified "this z must succeed". In the early stage of training, B is initialized randomly. There is no physical guarantee that the code has been learned, and F/B/Actor need to learn together.

### 6.1 Why is the code calculated through cross and reward_weights?

V1 expands the four categories of rewards into 16 known algebraic features h(y), so that:

\[
r_\alpha(y)=h(y)^T w_\alpha.
\]

These features include constants, q, dq, τm and their square/cross terms, command costs, positive power terms, and speed limit reduction terms. They are reward calculation tools, not B's input, nor the 16 physical coordinates that B has learned.

Let `cross=Eρ[B(y)h(y)^T]`, then:

\[
c_\alpha=\mathrm{cross}\,w_\alpha.
\]

The source code uses the batch row vector writing method `reward_weights(alpha) @ cross.T`, and is finally projected to a radius of 4. It is the same algebraic operation as calculating B multiplied by the reward on a result-by-result basis and then averaging.

### 6.2 What are the restrictions on the correspondence between tasks and z?

- When fixing the same B, the same cache and the same alpha, z is determined; however, during training, B is updated, the cache is refreshed every 100 critic updates, and the round batch end diagnosis is also refreshed, so the value z of the same task changes with training.
- The z value saved during an actual call remains unchanged and will not be recalculated until expiration. The trained network may still be updated during this call, and one cannot claim that the behavioral semantics are completely drift-free.
- Under the same cache, the task code does not read the current x, structure m, or role R0–R3. Therefore, the same alpha corresponds to the same z; the Actor/F needs to condition the response in different institutions according to their respective x. Sharing z does not guarantee that all agencies will achieve their goals.
- Different tasks or parameters may be mapped to the direction of proximity; normalization also removes the overall magnitude. There are no one-to-one, conflict-free, or per-dimensional interpretable guarantees.
- The z coordinates of different training runs and different frozen models cannot be directly interchanged numerically.

FB decomposition provides the basis for this mapping: if `M(dy|x,u,z)≈F(x,u,z)^T B(y)ρ(dy)`, the task return is approximately `F(x,u,z)^T Eρ[B(y)r_alpha(y)]`. Coding dependencies represent approximation, data coverage, and policy optimization; the formula itself is not a proof of actual arrival.

# # 6.3 Command z cannot be confused with reward readout coefficient β

The command for V1 is the normalized `Eρ[B r]`. The auxiliary loss additionally calculates `β=(C_cache+εI)^−1 Eρ[B r]`, which is used to predict the reward `B(y)^T β`. **The inverse covariance appears in the auxiliary readout coefficient β, it is not used to replace the Actor's z. **

## 7 P0, Replay, and training z are three different data paths

P0 uses 128 structures × 4 rounds × 500 steps = 256,000 W. Each command event selects maintaining rules, speed rules, braking rules, impedance rules or colored random actions with about 20% probability; the actual results are saved, and 16,384 are drawn from each of the four characters to form a fixed ρ. The regular actions are not labeled as Actor imitations, and the P0 original transfer is not directly pre-filled with online replay. P0 still introduces artificial priors to the data distribution.

Online Replay saves the 100Hz original observations and nominal structure, retains rounds according to role quotas, selects the source role first, then selects the round and transfers among them; reconstructs x_t, x_(t+1) from the original window in the round. Records do not need to rely on collection task tags to update FB. The batch size is 512, and the online transfer is updated every 256 new items; V1 does not have a dedicated online pre-fill waiting stage.

Each update reselects z for the drawn transfer: 80% of the four types of reward codes, 20% of the random spherical direction, which does not have to be the same as the actual collection command. For example, the real transfer taken by a hold command can also be used to train F under another brake z. The target uses the same z newly selected during training. What z changes at the next moment of the actual trajectory does not enter the target. This relies on off-policy learning; there is no relabeling of trajectories as "new tasks completed".

The real transfer of F/B comes from the current Replay; the results of FB point reference and reward auxiliary supervision come from the fixed P0 pool. Even if P1 only adopts R0/R1 online, fixed ρ still contains all four types of connection conditions. The two distributions are different, this is an additional method choice for V1, and it cannot be claimed to be equivalent to the standard paired implementation of the same Replay batch.

# 8 Randomization and Lawful State Sampling

The geometry is random when the structure library is constructed; the stochastic dynamics and initial state at the time of round reset; the external force/adjacency drive in the process changes according to an independent plan. Not every 10ms re-random mass, nor every dimension of o24 sampled directly independently.

| Project | Narrow Range or Nominal | Full Range/Implementation |
|---|---|---|
| P/D length | 0.225–0.275 / 0.315–0.385m | 0.15–0.40 / 0.25–0.45m; uniform sampling |
| P/D body mass | 0.85–1.15 / 0.2125–0.2875kg | 0.40–2.00 / 0.15–0.60kg; log uniform |
| Counterweight | Narrow structure without counterweight | Each LINK body mass 0–20%, along the rod 20–80%, real geometric composite COM/inertia |
| Fixed support orientation | Narrow R0 is 0 | Wide R0 inclination angle ±0.5rad |
| Rigid body density | Multiplier 1 | 0.8–1.2; mass and inertia have the same multiplier |
 Motor blocker/fragment 0.03 / 0.02  0.01 – 0.08 N.m.s/rad 0–0.08 N.m
| armature | 0.003 | Log even 0.001-0.006kg · m ² |
| Ground Sliding Friction | 0.8 | 0.4–1.0 |
 Power rectangular capacity  6N.m  4.8-7.2N.m.
 Electric T/Delay 10ms / 0 T even 5-20 ms; Integer delay 0-10 ms
| R1 support | Limited support | kx20–200N/m, kz100–500N/m, kθ0.1-5N · m/rad; damping ratio 0.3–1, vertical gravity preload |
R3 Externally driven  Limited PD  target range 0.1-0.7rad, frequency 0.3-2Hz, random phase; PD (8,0.5), forceRange ± 3.6N.m
| External force pulse | P1 amplitude off | Interval 0.5–2s, duration 0.1–0.5s, 50ms smooth edge; force 0–0.5Mg, additional torque ±1.8N·m; random LINK and force application points along the rod |

P1 level = 0, P2 gradually extends most of the continuous disturbance parameters to the full range. The delay takes the full integer range after level > 0; the initial state, partial support and peripheral drive are still random. Therefore, it is only part of the course, not all parameters are synchronized continuous annealing. V1 has not reached full level = 1 at stop.

Initial state nominal branches are normal 50%, wide range 30%, accessed snapshot 20%; when snapshot is unavailable, fall back at normal/wide ratio. Ordinary q at ± 0.6rad, dq at ± 2rad/s, wide q at ± 1.1rad, dq at ± 4rad/s.

R1 separately adopts root translation, pitch and velocity; R2 samples from the root attitude near 0 or π, and then determines the height from the ground by the lowest point of the actual box to avoid deep penetration, and the contact force is generated by simulation; R3 separately adopts the position and velocity of the peripheral joint. Take the generalized coordinates/velocity first, and then positive kinematics to obtain the link state to avoid spelling out inconsistent θP, θD, q, and COM velocities.

Snapshots retain accessed q/qvels, physical parameters, driver status and process clocks, and reset network history. V1's reset statistics include construction warm-up statistics, and the actual 50/30/20 ratio cannot be inferred from old log counts; subsequent corrections are not V1 results.

## 9 Loss of actual use of V1

Let the training batch be `(x_i,u_i,x_i',y_i^+)`, with size N=512. Independently sample N reference results `ỹ_j` from fixed ρ. The F/B input has been normalized to a fixed scale, and q, dq, and τ in the reward formula below use the restored physical units.

### 9.1 FB subsequent losses

\[
M^k_{ij}=F_k(x_i,u_i,z_i)^T B(\tilde y_j),
\]

\[
T_{ij}=0.99\left[\frac{\bar F_1(x_i',u_i',z_i)+\bar F_2(x_i',u_i',z_i)}{2}\right]^T\bar B(\tilde y_j),
\]

\[
L_{FB}=\frac12\sum_{k=1}^2\mathbb E_{i,j}(M^k_{ij}-\operatorname{sg}T_{ij})^2
-\sum_{k=1}^2\mathbb E_i\left[F_k(x_i,u_i,z_i)^T B(y_i^+)\right].
\]

u 'is generated by an independent target actor, added with a standard deviation of 0.1, cropped with a target motion noise of ± 0.2, and then restricted to [− 1,1]. The entire target stops the gradient. Because the reference results are sampled independently, this version of the integral does not have a diagonal mask of the form next-result in the same batch.

"Arrival" is not marked as a Euro-Ridge threshold or a successful label. The real next result is a sample of immediate visits, with future visits being carried out by Bellman relationships; The point of F and B is not a Boolean value.

### 9.2 B orthogonal term

\[
C_{\mathrm{batch}}=\frac1N\sum_j B(\tilde y_j)B(\tilde y_j)^T,
\qquad L_{orth}=\frac{\|C_{\mathrm{batch}}-I\|_F^2}{16}.
\]

B does not output spherical normalization at that time; this term is used to constrain scale and correlation. This limited batch form and 1/16 scaling is a V1 selection, and it cannot be said that it is exactly the same as the UFO default orthogonal estimation.

# # 9.3 Manual task rewards and additional L_task

The common command cost is `c=0.005u²+0.02(Δu)²`, with all four categories of awards less c:

| Rewards | Formula |
|---|---|
| Hold H | `−((q−q*)/0.5)² − 0.1(dq/3)² − c` |
| Speed ​​V | `−((dq−v_eff(q))/3)² − c` |
| Brake D | `−a(dq/3)² − b max(τm dq,0)/36 − c` |
 C `−((τm−[bias+K(q_ref−q)−D dq])/3)² − c`

v_eff gradually decreases to 0 using smoothstep within 0.15rad from the limit along the desired direction, which does not mean infinite travel uniform speed. τm dq in braking is the end point power proxy, not the precise interval work; it complies with the definition of an expected torque relationship and does not specify any environmental contact force.

Estimate `C_cache` and `E[B r_alpha]` with 4096 cached reference results, refreshed every 100 updates and end of batch diagnostics. Order:

\[
\beta_\alpha=(C_{\mathrm{cache}}+\epsilon I)^{-1}\mathbb E_\rho[B(y)r_\alpha(y)],
\quad \epsilon=10^{-3}\operatorname{tr}(C_{\mathrm{cache}})/16+10^{-6}.
\]

Each time another 64 tasks and 1024 reference results are collected, minimizing:

\[
L_{task}=\mathbb E_{\alpha,y}
\left(B(y)^T\operatorname{sg}(\beta_\alpha)-r_\alpha(y)\right)^2.
\]

β stop gradient, this is direct training B. The motive was to allow B-linear reading of these specified incentives without first proving that it was required by the FB and that it was an additional monitoring objective.

The total critic loss is `L_FB+L_orth+L_task`, and the explicit coefficients are all 1. Artificial rewards both determine 80% of the z direction and feed into the gradient via L_task; they are not limited to evaluation.

# # 9.4 Actor and Optimization Settings

\[
L_\pi=-\mathbb E\min_{k=1,2}
F_k(x,\pi(x,z),z)^Tz.
\]

Actor did not add any additional direct cost to the order; This cost affects learning through task z and B-aided supervision. Freezes the F parameter when you update Actor, but retains the gradient for the action.

| Settings | V1 Actual Selection |
|---|---|
 Optimizer  Adam; F and B are updated by different groups of parameters of the same critic optimizer
| Learning rate | F and Actor are 3e−4, B is 1e−4 |
| Update frequency | F/B is updated every 256 online transfers, Actor is updated every two critics |
| Gradient Clipping | F1/F2/B Joint Norm 10, Actor Individual Norm 10 |
 target  F1/F2/B, Actor updated with Actor; Polyak coefficient 0.005
 Initialization  Default initialization of the network layer; V1 has no subsequent visible positive initialization steps.

## 10 Actual implementation and design conclusions

V1 was originally scheduled to be 20M W, but actually stopped at 2,624,000 W, of which P0 was 256,000, online was 2,368,000, critic updated 9,250 times, and is still at P2. Only 35 different structures are accessed online; the P0 reference pool previously covered 128 structures, and P0 coverage cannot be equated to the fact that the Actor has learned these structures online.

| Roles | Online W |
|---|---:|
| R0 | 1,536,000 |
| R1 | 704,000 |
| R2 | 64,000 |
| R3 | 64,000 |

R2/R3 have only one 128world × 500 step batch each. The last batch of records has a pre-crop critic gradient of about 1.18 e8, and the rank of B second-order moments is 14 according to the 1e − 3 threshold. The model has not passed the ability verification. [Status record ](../artifacts/train_v1/status.json) has been explicitly marked as stopped, validated = false; the old file name `frozen_unit.pt` is not an acceptance conclusion.

A reasonable goal of V1 is to learn callable behaviors from local motion, load, structure, and historical information. However, task bias, command cost, B reward supervision, fixed ρ and multiple optimization changes were introduced at the same time, lacking independent control. They are not necessary designs that naturally follow from the concept of minimum execution units, nor can one infer that an item is necessarily harmful from a failure.

This paper only explains and preserves the historical design, does not retrain V1 and does not change the current learning algorithm. The subsequent discussion should distinguish between mechanical observational designs, mission interfaces, FB methods and engineering to achieve four levels, avoiding the expression “a mission code formula” as “a reliable and transferable behavioural syntax”.
