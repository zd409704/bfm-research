# Motor + two connecting rods: Upper layer call, local physical expression, B/z relationship and V2 implementation comparison

Revision date: 10/03/2026. This article answers in turn: * * What upper layers need to understand and call What local physical quantities are → used to express → information From where → B's feedback relates to the command of z → How to sample and train these relationships. * * This round further examines the availability of information by pressing “Let the upper layer see a localized body with geometry, moving, bearing and transmitting loads, and be able to invoke it to generate movement and interaction.”

The first five sections are designed according to the chain organization and list the current code at the corresponding location; Section VI focuses on the degree of achievement. The original mechanical condition, randomization range, data coverage and failure assessment are retained in the appendix as the factual basis for the design. The “needs” “options” in the text are interface design requirements or options to be validated; The current V2 is based on code, preservation weight and data and does not mix them.

2026-10-05 Supplemental Discussion: [Reverse carding ](Motor Proprioception and Representation.md) from motor body perception. This paper derives the motion/drive interaction semantics, physical sampling and upper-level invocation of the unit from the real telemetry, computable and unrecognizable quantities, and distinguishes the pure motor candidate scheme from the current privilege V2.

## 1. What does the upper layer need to understand and call?

# # 1.1 The value of the execution unit comes from the division of labor

The upper level knows the robot structure and tasks and is responsible for coordinating the timing, support distribution and whole-body balance of each unit. The smallest execution unit is a motor and its two adjacent rigid links, which are responsible for converting local intentions into continuous feedback control and reporting what actually happened.

It is desirable to alleviate the upper layer: each step requests from the motor to relearn the local inertia, friction, drive delay, loading changes, and how to continuously organize a movement. What you want to add is that the upper layers can choose movement and interaction, and adjust collaboration based on meaningful feedback. The upper layers still need to understand structural coupling, task geometry, contact feasibility, and systemic effects; the unit does not eliminate these problems.

Therefore, a pair of supporting interfaces are needed: **downlink behavior calls, and uplink feedback on local body status and execution effects. ** Simply replacing a torque or qpos target with 16 opaque numbers does not automatically reduce the learning burden; merely compressing the state into B does not automatically increase control capabilities.

| What the Upper Level Needs to Understand | What the Upper Level Wants to Call | Conditions for the Unit to Provide Value |
|---|---|---|
| How the two rods are currently connected, unfolded and moving | Change/maintain the relative configuration, rotation, braking, reverse, reciprocation | The continuous motion organization can be handed over to the unit and the real configuration and speed can be fed back |
| How local movement corresponds to rod end/centroid movement | Affects rod movement in the direction allowed by the current connection | There is a clear geometric and velocity relationship, and dq cannot be used as rod end or node velocity |
| Whether it is currently loaded, whether the outside world is driving it | Resist, follow, adapt, absorb mechanical energy or output mechanical energy | The same intention can adapt to certain load changes; feedback true response and drive state |
| Whether in contact, carrying or constrained | Establishing/maintaining contact, changing pressure in the controllable direction, unloading/withdrawing | With real interaction process and corresponding information, you cannot rely solely on the "in contact" label |
| Whether there is progress after the call, whether it is close to the capability boundary | Continue, change orders, or jointly release constraints with other units | Combine actual feedback, current intention and call time judgment; stillness itself is not a failure |
| How the motion of one unit affects adjacent units | Coordinate multiple z and shared rigid body motion | The upper layer retains the structure diagram, common reference system and task context; there is a unified convention for local feedback |

The calls in the table are the semantic scope that you wish to study, not the list of skills currently implemented in V2. A single motor can only actively apply torque along one joint axis, and cannot independently command any posture of the two rods, any node speed, or any six-dimensional force.

# # 1.2 Reducing the learning burden does not mean deleting qpos perception

q, dq, and computable geometry are still reliable body information and should be retained. What I want to change is the level of control of the upper organization, rather than forcing the upper layer to re-guess the angle and length that could have been known directly with latent variables.

The current [FrozenUnit](../interface.py) has returned the original Physical Observation, Structure, B-Code and Actor context, and does use this combined feedback. It proves that the interface already exists and that learning is not yet proven to be easier. When comparing the z call with the qpos/torque control in the future, it is necessary to keep the available sensing information fair with the task conditions; the z route should not be allowed to use the privileged state, but the baseline should only look at q.

# # 1.3 Review one by one by “local body” goal

* * The design direction is in line with the goal and only a part of it is covered by the current realization. * * The geometry, motion, and load need not be fully crammed into B, but must be expressible by the structural data, observations, conditional estimates, and learning feedback actually obtained by the upper layer.

| Requirements in Objectives | Documents must have a clear meaning | Current Implementation Determination |
|---|---|---|
| Has geometry | Shape/collision model, axis and mounting transformation, relative configuration, not just two masses and an angle | Local configuration can be reconstructed when the forward rod model and q are known; m28 itself is not a general shape model and does not output independent geometric feedback |
| In motion | Relative motion, common rotation, and overall translation are expressed separately, without replacing all motions with dq | V2 has the true value of plane world motion; the pure motor version can only directly cover relative motion, and the rest requires additional sources |
| Load bearing | Driving torque, equivalent load moment around the driving axis, and external contact effects are defined separately | There are real driving torques and some environmental effects; they do not cover all loaded states |
| Transfer loads | Clarify which connection/contact interface, load direction, point of application, and element's effect on adjacent bodies | **Currently no full feedback of connection loads on both sides**; B is not guaranteed to uniquely recover these loads based on current g23 alone |
| Callable motion and interaction | Change the actual motion/action through z within the scope of mechanical feasibility and sufficient information, and feedback the results | There are call interfaces and partial joint motions; complete link motion, specified contact force and cross-connection reliability have not been verified |

"Seeing" here means that the upper level has a physically based representation, and does not require humans to be able to explain B dimensionally. Static shapes known from the upper layer can come from the robot model; dynamic results can come from sensing and estimation; B provides encoding related to the behavior space. The unknown quantity must be clearly unknown, and we cannot rely on the network to output a number and call it perceived.

This sentence does not require each unit to output all six-dimensional load true values. It needs to be stated first whether the concern is driving power, equivalent load on the driving axis, force in the specified contact direction, or complete connection wrench. The first few may already have control value, but they cannot be collectively referred to as "complete load transfer".

## 2. Which local physical quantities are used to express these requirements?

### 2.1 Only after agreeing on the unit and coordinates can we talk about the "connecting rod state"

The two sides are marked P and D, which are the parent side and child side of the model tree respectively. They are used to agree on the joint axis, zero position and positive direction. They are not permanently fixed end/moving end. The motor exerts opposing torques on both sides; which side is supported and which side has the main movement is determined by the actual connection. When swapping two sides, the structure, coordinates, joint symbols, and moment conventions all transform consistently.

For the description of local geometry, the J-coordinate system can be established at the centre of the electrical chain, which will be rotated along the P-side agreed frame of installation. W for the formula in this section, fixation of inertia/world coordinates; When expressed in public coordinates, for example, to the upper torso, it is changed by consensus. ** The term “local” is the coordinates of the agreement and does not mean that all quantities can be measured by this motor. **

| Physical Quantity Groups | Suggestions for what is clearly expressed | Uses in the upper interface |
|---|---|---|
| Relative configuration and motion | q, dq, distance to limit; estimated from history as needed ddq | Describes expansion degree, direction, speed and local progress; also is the control result |
| Local link geometry | The relative posture of the two rods, the position of the center of mass/endpoint relative to the joint, joint axis and installation transformation | Let the upper layer know what body geometry corresponds to the unit motion; a large amount of content can be directly calculated kinematically |
| The real motion of the connecting rod and the node | The angular velocity in the clear reference system, the speed of the point relative to the node; the overall speed of the node when the task requires | Distinguish between relative rotation, overall being driven and node movement; not all independently controllable |
| Drive vs. local load | Request u, estimated/true drive torque, mechanical power, equivalent load torque around the drive shaft | Differentiate drive, back drag, braking and loading; support kinetic adaptation vs. effect feedback |
| Contact and connection effects | Contact objects/points/normal directions, relative sliding, forces and reference points; connection loads on both sides | Describe the results of bearing, slip, obstruction and force application, subject to sensing and controllability limitations |
| Structure and Boundary Context | Length, Mass Distribution, Inertia, Limit; Fixed/Elastic/Free/Adjacent Connection; Necessary Gravity or Public Motion Reference | Explain what the same local action does to produce different consequences, help the upper layer explain the feedback |

The sources and roles of physical states, structural parameters, driving memories, and boundary inputs need to be distinguished; they can be pieced together into the augmented control context of the network. Just because they are put into the same tensor, it does not mean that they are all measured by the motor or controlled by the motor.

### 2.2 Local geometry can be calculated, but there are two different "local velocities"

With known axes, installation transformation, two rod shapes and load side joint angle q, the relative attitude of the two rods and the position of the known rod end/surface point in the J system can be calculated without the need for world position. **The center of mass position must also come from known mass distribution, calibration or conditional identification; only the shape, total mass and rod length are not enough to determine the center of mass. ** For example, after knowing the fixed vector c_D of the center of mass of the D side relative to the hinge, its local position is

\[
r_{C_D}^{J}=R_{JD}(q)c_D.
\]

The mounting transformation is included in R_JD(q); the position of the P-side attachment point in the J system is constant. In this way, the upper layer can understand "where this joint rotation will take the end points of the adjacent rods" through the structure and q, without having to train B to reconstruct this kinematics first.

But `dr/dt = J_kin(q)dq` is just the rate of position change in the * * coordinate system that rotates with P * *. The difference between the true point velocity and the joint center velocity is

\[
v_X^W-v_J^W
=R_{WJ}\left(\dot r_X^J+\omega_J^J\times r_X^J\right).
\]

Among them, R_WJ transforms the J system component into the W system, and ω_J^J is the component of the angular velocity of J relative to the world in the J system. The latter item comes from public turns. When the entire unit rotates together while keeping q constant, the local position coordinates remain unchanged, and the velocity of the real point relative to the joint can still be non-zero. The overall node speed v_J is yet another term. Therefore, it is necessary to distinguish: the local geometric change rate, the true velocity of the point relative to the node, and the overall translation velocity.

**The current code comparison: **m28 's eccentric bias is compiled from the known simulation mass distribution, not from the historical estimates of the network. Round density multipliers are simultaneously scaled to mass and inertia and do not alter the physical and emotional bias; Nor can it be that the real substance is known after the launch of a random machine. The impact cross-section of the current pole is fixed at 0.04 x 0.04 m, and the axle/installation rules are written in the model; m28 The complete shape, grid, axis and randomly installed transformation are not carried independently and must be agreed upon in conjunction with these known models.

Planar local geometry is computed from the current model and q/dq, but these position fields are not output independently. o24 directly reads the world COM velocity and ωy; node velocity can be converted when this privileged information, true center of mass offset and attitude are available, there is currently no independent node velocity field/query. Unknown geometries cannot be universally and uniquely recovered from motion history: different shapes may also have the same mass, center of mass, and inertia, producing the same rigid body motion response.

### 2.3 "Force" needs to specify the object, direction and point of action

The motor drive torque, the equivalent external load torque about the drive shaft, and the complete connection/contact wrench must be separated. A single motor torque has only one scalar projection: for example, an external force passing through the center of a joint may have no moment around the driving axis, but produce a large connection load.

For the same contact, the force of the object acting on the rod and the force of the rod acting on the object are action and reaction, with opposite signs at the same coordinates and reference points, and are not two independent and freely specifyable variables. What needs to be distinguished is the component that can change the object, position, normal, load source and action.

the expression wrench also involves torque reference points. Change the stress at the COM to the expression of the center of the joint, both rotating the coordinates and adding the force arm term:

\[
f^J=R_{WJ}^{\top}f^W,\qquad
m_J^J=R_{WJ}^{\top}\left[m_C^W+(p_C^W-p_J^W)\times f^W\right].
\]

* * Current code comparison: * * V2 uses world Fx/Fz and My around their respective COMs, including explicit external disturbance, R1 spring support, external contact; P/D contact with each other is not counted in this field. It does not contain gravity and does not have a complete record of the internal joint reaction, the R0 fixed support reaction and the R3 adjacent hinge connection load. The current "environment wrench" is not a force on all the boundaries of the unit, and cannot be directly used as a force on the specified object.

The central P/D hinge reaction force is an internal effect on the "two rods as a whole", and it is reasonable to exclude it as an external boundary load; however, it may still be needed to describe the force on each rod. To describe load transfer to adjacent bodies, attention should be paid to the role of the external connections of the elements. The two cannot be confused with the same "missing force field". Even if the resultant external force of the two rods is known, it generally cannot be uniquely decomposed into the load of each connection and each contact point.

# # 2.4 Mechanical connections determine which descriptions can become commands

| Connection conditions | Degrees of freedom of movement of the mechanism | Restrictions on upper-layer calls |
|---|---|---|
 P-full position fixed  relative joints 1 freedom of configuration  node cannot be smoothed and can study joint swing/main/load
P outer end is attached to the ground, allowing the plane to rotate  to support the turn angle +q, which is two, with only one electric  having an undrived swing, energy transfer and a specific balanced response; Not a fixed whole P-tip.
| Plane free root | x/z/pitch+q, 4 in total | The two rods move together, and the contact changes the constraints at any time; the internal moment cannot arbitrarily change the trajectory of the overall center of mass |
| Free roots in space | 6 roots + q, 7 in total | There are three-dimensional movements and loads, but there is still only one drive channel |
| Adjacent body/two sides constrained | Determined by full body connection and contact | Same q and commands may correspond to different reachable results, boundary context required |

The space free unit has 7 configuration degrees of freedom and 7 independent velocities; the posture/velocity of the two rods satisfies the hinge relationship and cannot be independently random. A joint does not mean that the environment is only two-dimensional. Fixing the installation direction of the random joint on one side can change the gravity load; only the spatial root, adjacent motion and contact can further produce true three-dimensional overall motion. These two types of extensions are not interchangeable.

Straight, balanced, and a certain speed of nodes are a combination of the above-mentioned states and constraints and are not additional independent dimensions. Local support and instability can be captured, while the whole body-balanced tissue is handed over to the upper layer. Active force requires exposure, effective arm and capacity permission; No movement of any six-dimensional or two poles can be designated independently with the same driver.

## 3. Where does the information come from?

### 3.1 Determine whether it can be obtained relative to what information

"Motor information only" in this section refers to calibrated q, dq, drive current/torque estimates, and issued command history, and also allows the use of explicitly given structural configurations; does not default to a motor with an IMU, force sense, vision, or external position reference. **"This information alone cannot generally be uniquely recovered" does not mean "it can never be obtained after adding sensors or explicit constraints". **

| Information | Get conclusions and necessary conditions | Current V2 |
|---|---|---|
| q, dq, issued command | Encoder/speed estimation and command record can be given; q should be the relative angle of the load side, or converted by known rigid transmission. When only the rotor angle is read and the transmission has unknown elasticity/backlash, it is not equal to the exact relative angle of the connecting rod | Read the simulated joint status directly; there is no such sensing/transmission error |
| Relative attitude, rod end/surface point, local geometric change rate | Known complete shape, axis/mounting transformation + q/dq can be calculated; no world attitude is required | Current model conventions and parameters are in place, but there is no independent geometric feedback module |
| Center of mass position, mass and inertia | Known mass distribution/calibration can be given; when unknown, generally only part of the parameter combination can be identified under sufficient excitation and constraint conditions, and cannot be directly obtained from the rod length and shape | m is the nominal configuration; the center of mass is compiled from the simulation structure; the real round mass/inertia multiplier is hidden |
| The real output torque of the motor | The calibrated current can only be approximated; the accurate load side torque requires corresponding measurement or a sufficiently accurate transmission model | Input simulation accuracy τ, privilege |
| ddq, payload and driver response | Conditionally estimable. Differential/filtering has noise and delay; load estimation requires a dynamic model and sufficient excitation, and may only obtain synthetic residuals | Actor/F has a history, but no clear estimation head and error calibration |
| Public angular velocity, relative direction of gravity | Gyro can provide biased angular velocity measurement; the direction of gravity requires attitude estimation and corresponding assumptions/auxiliary observations. The specific force measured by the accelerometer cannot be directly regarded as the direction of gravity when it is dynamic; the ordinary six-axis IMU cannot determine the absolute heading alone | The world pitch/ω is a privileged true value; the gravity is fixed |
The world's location, the overall speed of the line, the electrical information alone, is generally not the only recovery. (a) Requires source base/whole state estimates, motor references or reliable exposure constraints; Only the IMU points still have initial and drift problems  world COM speed from simulation; It's not a historical assumption.
| Contact objects, points, normals, slips | Can only be obtained with known environment geometry and attitude, tactile/contact sensing, or estimates with sufficient constraints; only τ cannot universally locate and identify contacts | There are contact flags, but no complete object/point/normal/slip result fields |
| Complete loads at each connection/contact point | Corresponding force/torque sensing is required, or estimation of sufficient dynamics, motion and external load conditions is known; multi-contact/closed chain may have zero space for force distribution even with whole-body motion | Only partial synthetic environmental effects are input; no complete connection load feedback |
| Torque margin, cause of obstruction, future accessibility | is not a direct observation. Real capacity, call intent, model and boundary conditions are required; local history generally cannot uniquely determine the cause or guarantee future reachability | Nominal capacity and commands already exist, true cap is hidden; no calibration judgement |

This is still the first simulation prototype that explicitly uses privileged information. Changing the data to local coordinates does not change its origin: the privileged world speed remains privileged information after rotation. Future motor-only versions should independently define the available observations and upper-layer supplementary context, and the migration cannot be completed by setting the missing fields to zero.

The above-mentioned “no-sole” is a conclusion of the general situation, which does not preclude constraints from making the issue detached. For example, the attitude of the fixed base is known, and the structure of the entire chain and the angles of the joints are known and can be used by the world attitude of the sports calculator; Reliable, non-sliding contact can also constrain the base movement. These are additional known information/conditions that cannot be extended to a local encoder itself with a world-movement awareness.

# # 3.2 History helps adapt, and there is no guarantee that any hidden state will be restored

History should help to identify control-related response differences: delay in command to actual force rectangular, change in force rectangular to angular acceleration, and change in external drive, friction and exposure. It does not equal the assessment of all mass and external sources of the two poles, respectively.

The criterion is: whether there are two legitimate physical situations that produce the same available observation history but have different quantities to be estimated. At this moment, the network is not guaranteed to differentiate between the two. If only current incentives are insufficient, new incentives or a longer history may help; if the two remain indistinguishable under all allowed incentives, neither adding history, expanding the network, or using privileged teachers will remove the ambiguity. Guessing common situations based on training priors does not mean uniquely identifying the true value.

Unobservability cannot be solved by increasing the number of frames. For example, in free motion without fixed supports, no velocity-related environmental effects, and uniform gravity, superimposing a constant translation velocity on the entire unit can preserve the same q/dq/τ history. Motor telemetry alone therefore cannot universally restore world linear speed. Different masses, gravity projections and external forces at rest may also form the same resultant load.

There are three further categories of examples directly relevant to this project:

- **Parameter identification: **R0 When P is fixed and there is no external disturbance, changing the mass or inertia of P will only change the load-bearing capacity of the fixed support and will not be uniquely reflected by the q/dq/τ of this motor. For moving rods, the joint response is often constrained by the combination of equivalent inertia, mass × center of mass moment arm, etc.; unknown external loads will also be mixed with parameter errors, and "estimate effective response" cannot be written as "identify all real parameters".
- **Load decomposition:** The resultant load moment on an axis can be generated by different contact points, force directions or adjacency effects; forces passing through the joint center may also have no moment on the axis. Even if the synthetic wrench is the same, it does not guarantee that the force on each contact point is the same. Even if whole-body estimation is used, known external forces, contacts, and model assumptions must still be accounted for; "provided by upper management" cannot replace the source of information.
- **Capacity margin:** The current request never exceeds 6 N·m. With other conditions being equal and the same initial drive state, the capacities cap=6.5 and 7.2 N·m are not touched by these requests, producing the same drive response. Such history alone cannot discern the true capacity of either, let alone claim to know the exact residual moment.

"No progress" can be determined by a clear goal and movement history, but the cause may be obstacles, stiction, heavy loads, insufficient capacity, or faulty control. In the absence of additional evidence, observed no progress, command, and loaded responses should be reported back rather than outputting a confirmed cause of the block. The distance between any z and B is also not a physical progression truth.

**Current code comparison:** The control is 100 Hz; the slow history is 50 Hz×10, the summary endpoints are 180 ms apart, and the corresponding interval covers 200 ms; the fast history is 100 Hz×8, which only contains commands, torques and padding, corresponding to 80 ms drive records. Actor/F reads both, B does not read the history. The motion in the slow frame takes the endpoint, the contact takes the interval OR, and the force takes the mean, which is not a complete instantaneous state; odd-numbered control steps have a sampling phase difference of 10 ms, and the age field records this difference. Such history is an attempt at implicit adaptation, not a parameter identification window that has proven adequate.

### 3.3 Expressions oriented to the upper level should retain the source and meaning

In terms of design, the directly measured q, estimated dq, relative geometry calculated based on known models, and configuration parameters should retain source differences; the estimated load/contact requires clear assumptions and uncertainties; which layer the world/body motion is provided by and what observations are used should also be clearly stated. The learning characteristics of B can supplement this information and cannot replace the source description. The use of upper-level estimates should maintain causal timing, for example, provide next-step context based on information from the previous completed interval, and cannot refer to each other for outputs that have not yet been produced.

Current feedback preserves o/m, but does not provide a confidence level for each estimator, nor does it have a complete reachability or failure judge. In particular, `B_valid` is just "whether there is an execution result after reset", not a credibility, arrival, reachability or out-of-distribution flag.

the valid bits of m28 also only indicate that the corresponding nominal field is available; this round is all 1, so it cannot be claimed that it is equal to the real parameter of each round. The unknown quantity cannot be used as a measurement value; if missing markers are added in the future, it is necessary to synchronously train the corresponding input contract, rather than directly changing the existing weight input.

# # 3.4 Which information promises to achieve the “local body” goal

| Interface Promise | What Works | Can't be Defaulted to Known |
|---|---|---|
| Motor telemetry + known structure | Shape configuration, relative configuration and geometric changes, drive estimation, local load response; equivalent load estimation when conditions permit | Overall absolute motion, complete gravity direction, accurate load transfer on each side and real failure causes |
| Add sourced body context/additional sensing | Can supplement public rotation, overall motion, contact and certain connection loads, allowing the upper layer to obtain a more complete local body description | The degree of information completeness is still determined by actual sensing and estimated discriminability, and it cannot be claimed that any true value can be recovered |
| Simulation privileged prototype | The engine truth value can be used to check whether the representation and call are valuable, and the current V2 belongs to this category | Success does not mean that the motor telemetry version can achieve the same results; the current code does not export all the force information in the engine |

If you insist on using only single-motor telemetry, you should make it clear that the target range is "units with known geometry, relative motion, and the ability to sense partial equivalent load response". To achieve a more complete “local body that is moving, bearing and transmitting loads”, it is necessary to clarify the context from other sensations/estimates of the body, or supplement the corresponding measurements, rather than requiring B to recover all the information from the unrecognizable input. This can still keep the unit responsible for local control and adaptation, and the upper layer for collaborative division of labor.

# 4. How does B's feedback relate to z's command?

### 4.1 First distinguish the current results, behavioral commands and future effects

Use g_t to represent the local physical results that have occurred up to time t, use e_t=B(g_t) to represent its learning encoding; use x_t to represent the control context composed of current observations, structures and history. z_t is the behavioral preference for the next period of execution. The current g_t includes both the end point of motion and the contact/force summary just after 10 ms, and is not a complete instantaneous mechanical state.

\[
e_t=B(g_t),\qquad u_t=\pi(x_t,z_t),\qquad
(x_t, u_t,\ text {boundary action})\ longrightarrow g_{t +1}.
\]

The upper layer reads the real results and structure, combines the commands, call times and tasks it retains, and decides whether to continue or update each unit z. The unit continues feedback control during the call. **B(g_t) represents the result that has already occurred; z represents the outcome preference that is expected to occur subsequently; F connects the current action with future results. **The three have different responsibilities.

Feedback for the same dq ≈ 0, τ ≠ 0, may be normal under the "hold" call, and may not progress under the "keep moving" call. B does not read the current z or the duration of the call, and cannot judge for itself whether all commands are completed. The progress judgment must be combined with the intention; for the unit to report progress directly, this interface and basis need to be defined separately, and there is currently no independent implementation.

### 4.2 What relationship does FB use to connect them?

The core of FB can be written as a conceptual expression:

\[
M^{\pi_z}(x,u,dg)\approx F(x,u,z)^\top B(g)\,\rho(dg),
\qquad
\widetilde z_r=\mathbb E_{g\sim\rho}[r(g)B(g)].
\]

M is the discounted outcome access measure accumulated from the next outcome when performing the current action followed by π_z action; ρ is the reference outcome distribution. After F/B learns this relationship, the outcome preference r can be mapped to a command through an integral, and the inner product of F and the command corresponds to an approximate discount value. The current code then projects the command onto a sphere of norm 4, and the Actor optimizes the smaller of the two F's, `Fᵀz`.

“Linear” here refers to the integral mapping of outcome preferences to commands, the inner product of F and the value of the command. **It is not that the mechanical dynamics are linearized, each z dimension does not naturally correspond to angle/velocity/force, nor does it guarantee that the z interpolation corresponds to the linear interpolation of the physical trajectory. ** The command amplitude after spherical projection cannot be used to directly specify the force size.

B is not required to reconstruct the input losslessly, nor does it have naturally fixed physical coordinate axes. Even if the network inputs a certain link speed or force, it may not be retained with sufficient accuracy, let alone become a controllable command. Learning results can only support invocation within the scope of sufficient information, data coverage, feasible dynamics, and sufficiently accurate approximation.

B. Neither history encoding nor distillation can create information that does not exist in the input. If two real states produce the same motor observation history but require different privileged B feedback, a single deterministic telemetry network cannot accurately reproduce both; it can only add information, express uncertainty, or narrow the promised feedback semantics.

If a physical quantity or resultant reward is required to be linearly read out from B, the readout error needs to be verified separately. Generally, the linear readout coefficient is not the same as the command integral: let `Σ=E[BBᵀ]`, the least squares readout is about `Σ⁻¹ E[Br]` (can be regularized in implementation), `B(g_t)ᵀz` cannot be directly regarded as a physical error or arrival probability. The inverse covariance of the current code is only used for projection diagnostics and does not enter the command integration of `encode()`.

# # 4.3 Three Command Structures and Current Implementation

| Entrance | How to get the command | What can be expressed and what cannot be promised | Current code |
|---|---|---|---|
| Complete result target | `z=project(B(g*))` | Biased near the target result; g* must have a legal and consistent physical meaning. It does not only give one q, nor does it guarantee accurate arrival and retention | `diagnose_motion.py`, training result goal sampling has been used |
| Physics preference query | `z=project(E[r(g)B(g)])` | Can express preferences over a set of acceptable results, e.g. q is close to the reference and dq is small; query reward is not a pre-training task reward | `learner.encode()`, `FrozenUnit.encode_task()` implemented |
| The upper layer task strategy directly outputs z | The upper layer learns each unit z based on structure, feedback and task | There is no need to manually specify the physical semantics of each dimension, but the calling effect must still be reliable; interpretable queries can be used for diagnosis | The interface and bipedal adaptation of the unit receiving z have been implemented, and the upper layer task strategy has not yet been trained |

Currently, there are only four interpretable queries: maintenance, speed, braking, and compliance, which mainly rely on q, dq, and motor τ. The compliance query is the relationship between τ and q/dq, which cannot be directly called rod end spatial force control. **There are currently no query families that specify local rod end positions/velocities, nodal velocities, or specify object contact forces. ** Full g* encoding can bring in partial link information, and it cannot be claimed that these calls have been reliably implemented.

The existing web page maintains the query using the second entry; the failure of the negative angle is a measured problem of this call chain, and other angles to which z can be transferred cannot be used to replace the verification. See Appendix B for details.

# 4.4 Which step did the current network and feedback actually make?

| Component | Current input/output | Meaning cannot be attached |
|---|---|---|
| Actor | x336+z16 → u1, feedforward | Does not receive angle targets directly, not qpos server |
| F1/F2 | x336+sent action u1+z16 → 16 dimensions each | Not next frame physical state predictor or calibrated reachability probability |
| B | g23 → B16, norm 4, feedforward | no m, no history, no z; not a full geometry encoding or independent load estimator |
| Actor context | `embed_s(x)` → 128-dimensional, independent of current z | Not supervised as an explicit quality, friction or contact parameter |
| Upward feedback | `H197=[o24,m28,B16,context128,B_valid1]` | Having feedback does not mean that the feedback is more useful than the original physical quantity |

 `x336=o24+m28+slow history 260+fast history 24` . o24 contains q/dq, two rods each sin/cos world pitch, COM vx/vz, ωy, real τ, last u, contact sign, limit distance and two rod environment Fx/Fz/My. g23 deletes u in o;  training saves y25 with another Δu, but B also does not read it. m28 adds 14 significant bits for 14 nominal parameters. Field order and scaling is based on [schema.py ](../schema.py) .

That B does not contain m is not automatically an error: different ontologies can share representations of "physical consequences", leaving dynamical differences to F/Actors with m. However, currently g23 does not have rod length and center of mass position, and different geometries may correspond to the same g23 and different local rod end positions. So B16 alone cannot provide the complete local geometry; m/q is already in H197, and the upper layers are not completely lacking this information.

If you later want B to directly serve the link space results, you should first decide on the result definition: you can put the computable local geometry into g, or you can let the explicit geometry feedback run in parallel with B; whether to input m into B again is another option. You cannot jump directly from "hope to have connecting rod information" to "add m to B or expand the network". Changing g, reference distribution, or coordinate convention requires retraining/validation, and old weights cannot be considered automatically compatible.

# 4.5 closed loops for one call and semantic stability across units

The current execution timing of `FrozenUnit` is: reset establishes o/m and history, clears the result valid bit; every 10 ms physical execution is completed, observe updates the real result, B and control context; feedback provides H197; the upper layer gives or continues to maintain z; act calculates the next action. B does not participate in the torque solution online, and Actor directly reads x/z; the frozen execution package uses Actor/B and does not require F to be run online.

This allows the upper layer to adjust the command according to the actual result, but the current H does not contain the z it is executing and the duration of the call, the upper layer needs to save itself. B_valid becomes 1 after the first observe, indicating only that the result exists.

The coordinates of B will change during the pre-training process. The current code recodes the extracted results with the current B during ordering and learning updates; Replay saves the physical data instead of the long-term z. The current command is maintained within a limited call window, which does not mean fixed semantics throughout the training process. Sharing the same version of Actor/B after freezing can keep the encoding base consistent, but there is still no guarantee that the same z will produce exactly the same results on all topologies; connection reachability and distribution changes still exist.

If you fine-tune B/Actor in the future, you need to recheck the meaning of upper-layer commands and feedback. You cannot just retain the old upper-layer weights and leave the default interface semantics unchanged.

## 5. How to sample and train these relationships

# # 5.1 Acquisition targets should come from relationships that are invoked and understood by the upper layers

The collection should not only answer "whether there is a certain angle", but also answer: what changes will the action cause under what structure, boundary and load; what changes come from the adjacency/external world; whether different forces can be distinguished under the same configuration; what will happen after the command is continued to be executed, the command is changed, and the constraints are released.

Therefore, the acquisition sequence is: select target mechanical conditions and parameters → generate generalized coordinates/velocities that satisfy constraints → apply continuous actions and boundary excitations → record actions, responses and results → check process coverage. The two-pole world states cannot be spliced ​​independently, and the contact force cannot be filled into B as a random number that has nothing to do with geometry/action.

The comparison relationships that need to be covered include: different speeds/loads under the same configuration; different driving/braking actions under similar loads; different structures under the same local motion intention; no-load maintenance, load-bearing, obstacle resistance and unloading under similar stationary configurations. External perturbations and passive motion are also valid data, but it is necessary to distinguish between forced changes and changes that the motor can actively influence.

# # 5.2 How each movement/interaction is picked up, and what is picked up by V2

The following state families can overlap, instead of artificially dividing all physical states into several mutually exclusive tasks. Rule controllers can be used for collection without requiring task rewards to be added to the FB for each row.

| Relationships/processes that upper management cares about | Legal collection methods | V2 existing content and gaps |
|---|---|---|
| Static, low speed, load hold | Hierarchical acquisition of legal angles and loads; feedback is maintained until the end of the transient, then loading/unloading | P0 has a hold rule, and there is a low speed load frame online; continuous hold coverage across angles/loads has not been confirmed, and the freeze call has failed |
| Bidirectional rotation, acceleration and deceleration, braking, reverse | Starting from different q/dq, continuous torque/speed/smooth sweep angle excitation; save the entire process from startup to reverse | P0 rules, random initial velocity and online exploration are available; complete coverage audit of missing angle × speed × load |
| Period, reciprocation and switching | Change legal amplitude, frequency, phase, save duration and order transition | There are related processes and partial alternation queries; full amplitude/frequency and cross-connection capabilities have not been accepted |
| Limit approach, compression, and reverse disengagement | Different approach speeds, torques toward the limit, unloading, and reverse direction are adopted at both ends | There is a large amount of near-limit data, but the limit is fixed, and the online data is obviously concentrated at the ends |
| Substantial folding, span ±π, continuous rotation | First establish a collision/axis offset/cable allowed model, and then cover the legal interval and circle crossing process | The current ±1.2 prototype is not covered; expanding the range of the web page does not increase training data |
• The whole side is driven, co-ordinated, moving carrier/neighbor joint, changing the continuous border movement, cross-mining resistance/attached/self-movement  R1 is flexiblely supported and R3 has a adjacent sine-driven; Only specific flat structure, no complete two-sided exchange and space boundary
| Falling, airborne, free relative rotation | Legal root attitude/speed start, recording non-contact segments and action effects | R2 has a short time to leave the ground, and is not specifically designed for free flight/weightless floating conditions |
| Support, upright, sway, instability/recovery | Cover near equilibrium in end-hinged or contact environments, record recovery and fall | R2 has associated initial state and grounding; no independent end-hinged two-pole library, no sustained equilibrium/recovery coverage statistics |
| Node/rod end movement | Use boundaries that allow node motion to record the relationship between nodes, endpoints, COM and actions | R1/R2/R3 has motion; there is no independent node velocity result and corresponding command verification |
| Disturbance, anti-drag, compliance, energy absorption | Different force arms on both sides apply pulse/continuous load/motion boundary, and save the application and cancellation process | There are external disturbances and adjacent drives, and P0 has compliance; short pulses cannot represent all sustained loads and interactions |
| Contact establishment, impact, adhesion, slippage, detachment | Change approach attitude and speed on the ground/wall/object, record point, normal direction, reaction force and relative motion | R2 has ground contact, the field only has contact mark and mixed force; not audited according to mode, no dedicated wall/object library |
| Blocked movement, insufficient capacity, release of constraints | Block movement with obstacles/resistance, withdraw or release after continuous call, save intention and progress | Limiting and grounding provide partially restricted conditions; there is no clear intention of the system → blocked → release collection and annotation |
| Active force application, pressure maintenance, and unloading | Change drive under real contact and effective force arm, covering different pressures and releases that are approximately the same q | There is natural reaction force, but there is no dedicated pressure control collection, object-specific force application results or specified force query and verification |
| Constrained at both ends, closed chain load-bearing | Preloading, releasing under legal fixture/closed chain and limited compliance | No independent working conditions; R3 series drive cannot replace the internal force of the closed chain |
| Spatial installation and three-dimensional interaction | Legal three-dimensional geometry/inertia, changing installation direction, spatial boundary movement and contact | All V2 is a plane, not covered |

The mechanical range is not as wide as it can be; The client needs to be declared. Institutions that are meaningful in terms of limited travel, rotation and circle should be defined separately, as detailed in appendix C. Inversely, it is not possible to keep the wrong coordinates agreement by simply exchanging mass fields.

# # 5.3 Where data should go

| Data/Information | Role to play | Current V2 |
|---|---|---|
| Continuous physical transfer and sent actions | Learn the relationship between actions, control context and subsequent results | Online Replay saves o24, m28, turn information, and can reconstruct history and y25 |
| Boundary/contact truth values ​​and acquisition command logs | Check cases, process coverage and failure reasons; do not have to all be entered as Actors | Original training replay does not have complete contact event sources and does not save step-by-step z/named task intents |
| Results description g | Decide which results B can distinguish and which preferences can be expressed from the results | Use g23; no local location, structure, history, and full connection loads |
| Control Context x | Provides Actor/F with currently available state, structure, and history | x336 is implemented with privileged information; full Markov state is not guaranteed |
| Physical goals/preferences | Constructing queries, validating calls, and readout semantics | Four categories of frozen queries implemented; not named reward supervision for online FB |

Simulation can record the true center of mass, load decomposition and contact mode as audit/supervision labels, but "having labels" does not mean that they can be identified by the motor side. Inputs to deployable Actor/B must come from actually allowed information; if labels are not unique to these inputs, training errors cannot be eliminated simply by more data, nor can results from privileged prototypes be substituted for deployment validation.

Resetting to a certain state only shows that it has entered data, but does not prove that the action can bring the unit there from elsewhere. Passing through an angle briefly, staying under load, and returning after being disturbed are different processes. A large static moment cannot be automatically marked as stalled, and many contact frames cannot automatically prove active force application.

The regular trajectory of P0 can provide organized transfer, but currently V2 * * is not pre-populated with P0 raw online Replay * *. P0 only provides the initial result goal source when the initial reference pool and Replay are empty, after which the reference pool is updated from the online Replay. Therefore, the success of the P0 rule control cannot be used to show that the actor has learned the same behavior. Keeping the rule transfer as a training data source is a follow-up option that can be discussed, and this article does not write it as implemented or the only way to fix it.

The current Replay sampling first selects characters according to their weight, and then evenly selects rounds and intra-round transfers. There is no coverage balancing based on angle, movement direction, loading, contact or obstruction mode. P0 also only saves the aggregate count of the command category, and does not save the rule reference α step by step; it is not possible to directly label all processes with the truth value "intent completed/blocked" from the ready-made raw.

### 5.4 How FB and Actor actually train these relationships

The current implementation proceeds in order:

1. Reconstruct `(x,u,x′,g′)` from online continuous data. The result g ′ comes from the physical response after the action has just been completed, the action is the actual sent u, not the τ after the drive response.
2. Re-extract z when updating: about half is a random spherical direction, and half is extracted from the current B code; the command does not require the same as the acquisition. Replay does not store z whose semantics change over time.
3. F/B is trained together with the Bellman relation accessed by subsequent results and the B orthogonal regularity: paired in the same batch, the square error term excludes the diagonal, and the corresponding positive sample term is retained. There are no naming task rewards and no loss of q/force/geometry reconstruction or prediction of true dynamic parameters.
4. Actor learns actions by maximizing `F(x,π(x,z),z)ᵀz`, the smaller of the double F; target F/B updates slowly.
5. After freezing, construct a query using the physical preference integral or the complete result goal to check the actual execution. To verify that B's structured readout of geometry/forces needs to be checked separately, FB loss reduction does not automatically replace it.

This is a type of off-policy training: the acquisition command can vary, and the learning goal still considers subsequent execution under a given z; its effectiveness relies on sufficient data support and contextual approximation. The environment does not tell the network all the real parameters, future plans of external disturbances, and adjacent follow-up intentions, and F cannot be regarded as an accurate future predictor.

If you subsequently want B to explicitly retain certain local physical relationships, you should first ensure that the result definition and source of information are sufficient, and then check the readout and callout errors. Assisted reconstruction/readout loss is only an option that needs to be demonstrated separately and is not automatically added to the training because of the reconfiguration logic in this article.

### 5.5 Coverage, representation, calling, and upper-layer benefits are judged separately

| Levels of Judgment | Questions to Answer | Current Evidence |
|---|---|---|
| Data coverage | Whether the legal range and key state-action-boundary relationship enter the actual training data | P0 and four character online data exist, but the final Replay is concentrated near the limit, see Appendix B for details |
| Representation and information | Whether g can distinguish the required results, B/context retains the required differences in the upper layer | Yes g23/B16; There is no guarantee of complete geometry/force readout, B cannot independently recover the entire connecting rod geometry when the structure is missing |
| Callable behavior | Whether the selected command can be reached, sustained, and performed under disturbance | Partial local movement, nominal R0 maintenance There is also obvious failure; general ability has not been accepted |
| Benefits of upper-layer collaboration | Do these interfaces make task learning easier, better controlled, or easier to reuse across structures | The physical access of the four units has been completed, but there is no upper-layer walking training and fair comparison results |

Therefore, the current gap cannot be collectively referred to as "adding randomization", nor can it be repaired simply by "expanding the q range", "adding force fields", and "increasing network capacity". You must follow this five-step chain to determine whether what is missing is physical scope, available information, representation, command association, or execution and coordination.

# 6. Comparison of current code implementation: The interface exists, but the full semantics have not yet been completed

| Logical link | Currently implemented | Not yet/not verified | Code basis |
|---|---|---|---|
 Multi-unit upper-level organization  FrozenUnit acceptancez; Actor/B, historical independence  Evidence of upper mission strategy, mobility and reduced learning burden  [interface.py ](../interface.py), [biped/runtime.py ](../biped/runtime.py)
| Explicit physics feedback | o24 and m28 are retained as they are, supplemented by B/context | Explicit local geometry, fully connected loads, intent-related progress interface | [schema.py](../schema.py), [kernels.py](../kernels.py) |
| Information sources and history | Privileged simulation observations, 50 Hz/100 Hz historical assembly | Students of motor telemetry, explicit load estimators and their credibility | [history.py](../history.py), [networks.py](../networks.py) |
| B result encoding | g23→16-dimensional spherical features | Complete geometric encoding, linear readout of physical quantities, failure/reachability judgment | [networks.py](../networks.py), [learner.py](../learner.py) |
| Command and execution | Point target/reward point encoding; Actor output u, generated by driving τ | Link position/speed/specified contact force query and reliable full-stroke execution | [tasks.py](../tasks.py), [diagnose_motion.py](../diagnose_motion.py), [cpu.py](../cpu.py) |
| Training correlation | Pure FB + orthogonal term, Actor value target; online result sampling | Not all required relationships have entered the data, and not all have been proven to be readable/controllable | [fb_loss.py](../fb_loss.py), [train.py](../train.py), [replay.py](../replay.py) |
| Candidate export and access validation | Actor/B candidate, schema, 197-dimensional feedback; four-unit 1s concatenation | Not unit semantics or standing/walking acceptance; candidate still validated = false | [export_candidate.py](../export_candidate.py), [biped/compatibility.json](../biped/compatibility.json) |

The current [FrozenBiped](../biped/runtime.py) is a four-motor hip-knee biped adapter, which receives `z[4,16]` each time and returns `H[4,197]` after 10 ms of execution. Shared rods in the physical world only exist once and enter the P/D observations of adjacent units respectively; multiple units cannot be regarded as dynamically independent robots.

Existing validations include model and observation mapping, drive, shared rod force mapping, batch and independent unit call consistency, independent history, and limited signal checking of 100-step random z. * * It verifies access, not walking. * * Shared torso, leg grounding and simultaneous action of multiple learning controllers are still new combinations of V2: R2 has grounding without adjacent drive, R3 has adjacent drive without ground. Local parameters in the numerical range do not mean that the complete combination relationship has been trained, see [Bipedal Access Instructions] (../biped/README.md) for details.

# Appendix A. V2 Mechanical Conditions, Randomization and Training Data Paths

The following retains the actual scope of implementation checked for the purposes of sections 2, 3, and 5; this does not imply that a new training programme has been implemented.

### A.1 Four types of plane working conditions and driving


V2 uses MuJoCo/MuJoCo-Warp, with a physical step size of 1 ms, a control period of 10 ms, and each round of 5 s. The motor output is a normalized torque command `u∈[-1,1]`, with a nominal request of `6u N·m`, applied to the joint after capacity limitation, delay, and first-order response; not a qpos target drive.

| Roles | Actual mechanical connections and captured process sources | What cannot be claimed for coverage |
|---|---|---|
| R0 | P complete posture fixed; D swing, gravity, joint friction and external impulse effects | Not an end-point articulated double pendulum; no node translation, ground contact, free overall motion |
| R1 | P has x/z/pitch root degrees of freedom and is supported by spring damping; two-rod motion is coupled to the support reaction | No ground contact; the support is on the P side; not any body connection |
| R2 | Plane floating root + ground; the two poles can move and touch the ground, and may have short-term airborne, collision and constrained movements | It is not an independent ground-free flight environment; there is no space movement, and there is no dedicated wall/obstacle force application condition |
| R3 | Fixed lateral side A, connect P via drive joint q1, study motor connection P/D, then connect to lateral side T via drive q3 | Generate adjacent drive and inertial load, but still a specific planar series structure; the two ends are not arbitrary independent motion boundaries or closed chains |

R0, R1, R3 close the geometric contact. R2 Turn on contact with the ground, etc. `9.81 m/s²` with fixed gravity in the world − z direction, no random gravity size or spatial mounting direction.

The motor joint limit of all training models is fixed as * * [− 1.2, +1.2] rad * *, with a total stroke of 2.4 rad, about 137.5°; the limit is not randomized. `margin=0.03 rad` intervenes with a limit constraint of about ± 1.17 rad; MuJoCo uses a flexible numerical constraint, which may transiently cross the nominal limit in the trajectory. Such overruns do not count as effective training coverage for larger itineraries.

# # A.2 Actual scope of ontology, drive and initial state randomization

32 structures per character, 128 total; first 8 are narrow distribution, remainder are wide distribution. The following is the sampling range of the basic parameters in the library. The actual mass is also affected by the counterweight and round density multiplier.

| Project | Implemented Scope | Coverage Boundary |
|---|---|---|
| P/D length | Narrow: P 0.225–0.275 m, D 0.315–0.385 m; Width: P 0.15–0.40 m, D 0.25–0.45 m | The range on both sides is different, and complete physical exchange coverage is not done |
| P/D base mass | Narrow: P 0.85–1.15 kg, D 0.2125–0.2875 kg; wide: P 0.4–2 kg, D 0.15–0.6 kg, uniformly sampled on a logarithmic basis | Mainly biased toward P being heavy and D being light; not an arbitrary mass ratio |
| Mass distribution | Wide structure with 0–20% counterweight, 20–80% along the rod, lateral offset 0.01 m; center of mass and inertia compiled from geometry | Planar geometry family only, general space inertia not covered |
 Round dynamics  density factor 0.8 – 1.2; Interception 0.01 – 0.08; friction rectangular parameter 0-0.08; (a) Electrical 0.001 – 0.006 radiums, without models such as visible dents, soft motion, heat decay, etc.; N.m.s/rad, friction N.m., armature kg.m2
| Drive | Capacity 4.8-7.2 N · m; Response time 5–20 ms; Delay 0–10 ms | Request is still limited to 6u, maximum absolute value 6 N · m, capacity parameter greater than 6 does not mean that 7.2 N · m can be actively requested; not all actual motor effects are covered |
| Boundary excitation | Two-sided plane Fx/Fz/My impulse; R1 support stiffness/damping; R3 adjacent joint sinusoidal drive; R2 ground friction 0.4–1.0 | No dedicated continuous top wall, contact force tracking or revocable obstacle course |
| Limit and spatial direction | Limit fixed ±1.2; joint axes are all y; wide structure R0 fixed inclination angle can vary within ±0.5 rad | No random joint travel; R0 inclination angle is still a plane change |

The external disturbance lasts 0.1–0.5 s, with a gap of 0.5–2 s between adjacent events, with a 50 ms smooth edge; the upper limit of the force amplitude is set according to the total mass of the model `0.5Mg`, with an additional My of ±1.8 N·m, acting at 20–80% of the rod length on a random side. It provides the process of being loaded and does not directly provide active force application skills. R3 adjacent target amplitude is 0.1–0.7 rad, frequency is 0.3–2 Hz, and phase is random. It is driven by adjacent PD and is not directly specified to arbitrarily specify the true speed on both sides.

The initial state is generated according to the following range, rather than independently randomizing the world state of the two rods:

| Initial state source | Implementation |
|---|---|
| Normal/wide joint status | q is ±0.6 / ±1.1 rad, dq is ±2 / ±4 rad/s respectively |
| R1 root | x/z offset ±0.05 m, pitch ±0.35 rad, vx/vz ±0.5 m/s, ωy ±1.5 rad/s |
| R2 root | pitch is ±0.35 rad near 0 or π; vx ±0.5, vz ±0.3 m/s, ωy ±1.5 rad/s; the legal height is calculated based on the geometric corner point of the rod, 80% is 1 mm from the ground, 20% is 2–10 cm from the ground |
| R3 adjacency state | q1/q3 initial angle ±0.6 rad, initial angular velocity ±1.5 rad/s |
| Trajectory snapshot | Restart from existing physical trajectory, save kinetic parameters and drive memory; network history restart |

The design ratio is 50% normal, 30% width, and 20% snapshot; it will fall back when the snapshot library is insufficient. The full run actually had 39,552 online rounds: 21,806 normal, 13,054 wide, 4,692 snapshots, and an additional 3,336 snapshot rollback events recorded (counted into normal/wide rounds and cannot be added together). So the actual snapshot back to the contract is 11.9%, not 20%.

# A.3 P0, Online Collection and Replay 's Practical Data Path

| Stage | How the data is generated | How the data is used |
|---|---|---|
 P0 rules collected 128 structures x 4 world x 500 moves = 256,000 transfers per role 64,000; There are positions to maintain, speed control, brakes, adapt, associated force rectangular noises, and to save raw and result reference pools. **V2 did not prefill online Replay with P0 Raw, nor did it train directly on these P0 transfers FB Bellman losses**
V2 Online Collection  50% random ballside z, 50% extract from current B code g; The Actor action adds a noise with a standard deviation of 0.2 and limits the range of the caps itself generated by the continuous transfer into Replay as a source of updates for F/B/Actor. Goal encoding is then B at the time of the change order, and does not contain long-lived fixed semantic z
| Reference pool update | P0 provides the initial reference results; when Replay is empty, the initial goal source is also provided; after that, the reference pool update from online Replay | P0 is not a permanent proportion of the regular action data source, and can not directly replace the online training coverage with the good coverage of P0 |

The five types of P0 acquisition behaviors are each about 20% at the command sampling level; the reference angle is maintained at ±0.8 rad, the compliance reference angle is at ±0.6 rad, and the speed reference is ±0.5, ±1, ±2, and ±4 rad/s. They add initial state, inertia, disturbance and limiting effects to enable the trajectory to exceed the reference angle range; the reference angle range cannot be mistakenly written as the q range of all data.

Both P0 and the online phase have mixed command durations: about half are 40/80 ms and the rest are 100–1000 ms. Short commands are good for generating switching transients but do not guarantee steady-state maintenance or sustained contact loading. Whether to cover these processes depends on the actual trajectory.

V2 complete training has gone through P1, P2, P3, and the final count is W=20,032,000, of which P0 is 256,000, online is 19,776,000, and updated 77,218 times. The four online characters collected R0 6,208,000, R1 5,952,000, R2 3,392,000, and R3 4,224,000 transfers respectively. P1 favors narrow structures R0/R1; P2 gradually introduces four characters and stronger randomization; P3 uses complete randomization. **Completion of P0 does not mean completion of the course, but completion of the course does not equate to passing proficiency acceptance. **

## Appendix B. Constraints of saved data on current design

### B.1 Coverage audit: The scope exists, but the access bias is limited


This time, the original 256,000 transfers of P0 are read, as well as the 1,000,000 online Replay transfers retained in the final checkpoint. The latter is 250,000 per character, **only represents the final retained data, not the statistics of the entire 19,776,000 online history**. Both exclude the initial frame and padding, and restore the normalized data to physical units.

| Character | q < − 0.6 in P0 | q < − 0.6 in Final Replay | Approaching Limit in P0 | Approaching Limit in Final Replay | Any contact in Final Replay |
|---|---:|---:|---:|---:|---:|
| R0 | 18.51% | 27.82% | 15.30% | 37.21% | 0 |
| R1 | 18.03% | 31.25% | 16.14% | 42.37% | 0 |
| R2 | 18.19% | 41.66% | 18.95% | 71.30% | 67.46% |
| R3 | 15.85% | 31.72% | 12.62% | 32.95% | 0 |

"Proximity Limit" is defined as `|q| > 1.1 rad`, which contains a small number of numeric outliers and is not an exact label for solver constraint activation. In the nominal legal interval, the two segments at both ends only account for about 8.3% of the trip, but they carry 33% –71% of the final Replay sample, indicating that the status access is highly concentrated at the end. * * This does not prove a single cause of failure, but negates the default assumption that random z will naturally produce sufficiently balanced motion data. * *

In the final Replay, R0's `−1.1 ≤ q < −0.6` still accounts for 10.60%, and R2 accounts for 8.02%. Therefore, it cannot be said that there are no samples below −0.6 at all; what is really unconfirmed is whether there are enough diverse loads, continuous holds, in and out movements, and closed-loop recovery transfers at these angles.

For example, the ratio of  `|dq|<0.05 rad/s and |τ|>1 N·m`  in R2 is 58.88%. It may include pressure limit, static load or obstruction, and cannot be directly written as "58.88% blocked state has been reached". High exposure is not a substitute for evidence of active force or balance.

Statistical definitions, source file SHA256, count by angle interval and summary of evaluation are saved in [this data audit ](../artifacts/state_coverage_audit/20261001_v2_motion_coverage.json). These statistics are reads of old data and no new training samples are generated.

### B.2 Keep actual records of failed calls


This time, the saved results of three webpage experiments were read, and the same final weight, R0 nominal institution, and physical limit ± 1.2 rad were used. The following table takes the last 1s of each record; the "disturbance-free branch" runs the same strategy from the same initial state and does not receive manual thrust.

| Maintain target q | Actual mean value of disturbed branch with feedback | Actual mean value of unperturbed branch | Unperturbed terminal angle RMSE | Unperturbed terminal maximum absolute command |
|---|---:|---:|---:|---:|
| −1.0 rad | −0.5614 | −0.5614 | 0.4386 rad | 0.0604 |
| −1.2 rad | −0.6028 | −0.6028 | 0.5972 rad | 0.0788 |
| +1.2 rad | +1.1700 | +1.1700 | 0.0300 rad | 0.1381 |

The angular velocity RMS at the end of the negative target experiment was approximately 0.0046 and 0.0094 rad/s respectively, indicating that it stopped near the wrong position. They are far from the negative limit, and the command is not close to ±1 saturation; manual perturbation is not necessary for this steady-state error. The positive target stopped near +1.17 is also affected by the limit margin in Appendix A.1, and cannot be regarded as an accurate +1.2 maintenance success.

This is not a phenomenon caused solely by the web display or the mechanical −0.6 limit. The current complete call chain of "Angular Target → Z Query → Actor Execution" does not pass the hold targets that should be checked.

### B.3 Distinguish access range, query and execution failure

There are three layers of evidence:

1. **Data layer: **P0 and online Replay both have a large number of samples with q < −0.6.
2. * * Sports layer: * * `motion_panel` has the same final weight, and the direct result goal query can bring the institution to about − 1.11 rad. Therefore, institutions and strategies can cross − 0.6 at some z; but the query does not correctly achieve the goal it originally requested.
3. **Calling layer:** The web page retention query requires −1.0/−1.2 but stops at −0.561/−0.603, indicating that the accessible angle has not become a reliable and optional retention behavior.

The web page hold query uses the frozen bonus points encoding to construct z; the Actor does not directly receive the numerical angle target. Existing evidence has yet to isolate the effects of reference data distribution, B/FB representation approximation, target-to-z mapping error, actor optimization, and data coverage bias, and this phenomenon cannot be used to declare any one of them as the sole cause. P0 keeps the reference only to ±0.8, and the final Replay close limit concentration are both design facts that need to be retained; neither can complete causal attribution alone.

It can be concluded that: * * The current V2 does not achieve a reliable full trip hold call, and the original positive judgment based on a few goal successes or average indicators is not sufficient. * * It is not yet possible to enter the multiplex conclusion as a “trained general-purpose execution unit”. The form of FB loss is simple, there is no task reward for training, and there is no automatic guarantee of data coverage, accurate query, or reliable actor control.

# Appendix C. Full range of joints shall be defined by mechanical structure


The user indicated that ±1.2 was not sufficient to represent the existence of the generic unit: it was a limited process selected by the prototype, with a total of approximately 137.5°, without covering a larger fold, full-angle installation and continuous rotation. While there are upper and lower limits fields in the nominal parameters, they have been constants and do not indicate that the network has learned to change the limit.

Three ranges need to be distinguished:

- ** Limited trip joint: ** Full range determined by mechanical limit, collage, cable and target agencies. The full legal itinerary and the different limits of the declaration should be covered, rather than changing the relevant section unconditionally to " .
- **Periodic rotating joint: **The posture can be modeled in one circle; ±π is an angle representing the cut, not a physical stop that automatically exists. Continuous motion across representation boundaries is required, and a consistent state representation is used.
- ** Mechanisms with multiple turns and meaningful number of turns: ** Winding, transmission, etc. make the number of turns a part of the state and cannot be replaced by just the modulo angle.

The first two rods extend downward along the same straight line at q=0. Large folds may allow intersection of simplified rod geometries; it is necessary to clarify whether axis offset, zero position, collision and continuous rotation are mechanically feasible before extending the scope. The webpage relaxes the angle input or changes the evaluation limit, which only expands the test range. It neither completes the training coverage nor fixes the erroneous call of the existing target to z.

# Appendix D. Verification Basis and Version Boundaries

- Physical models and acquisitions: [mechanics.py](../mechanics.py), [environment.py](../environment.py), [kernels.py](../kernels.py), [cpu.py](../cpu.py).
- Input, history, feedback and commands: [schema.py](../schema.py), [history.py](../history.py), [networks.py](../networks.py), [interface.py](../interface.py).
- P0, Reflay online, Learning and Query: [bootstream.py ](../bootstrap.py), [train.py ](../train.py), [replay.py ](../replay.py), [fb_loss.py ](../fb_loss.py), [learner.py ](../learner.py), [tasks.py ](../tasks.py).
- Completion status: [status.json](../artifacts/rf_v2_full/status.json), [metrics.jsonl](../artifacts/rf_v2_full/). Coverage and failure data: [20261001_v2_motion_coverage.json](../artifacts/state_coverage_audit/20261001_v2_motion_coverage.json), [motion_panel/summary.json](../artifacts/rf_v2_full/motion_panel/summary.json). The three experiments on the web page are `20261001_052805_live_0a230a`, `20261001_052822_live_be7e50`, and `20261001_052846_live_a64399`. The audit JSON contains source data path, hash, unit and statistical definitions.
- Current four unit access: [biped/README.md] (../biped/README.md), [biped/runtime.py] (../biped/runtime.py), [validate_compatibility.py] (../biped/validate_compatibility.py), [compatibility.json] (../biped/compatibility.json).
- Full V2 training history [V2 Training Design Note ](V2 Training Design.md) and evidence of freezing behaviour [without reward V2] training results ](Reward Free V2 Results.md). The old V1 reward projection training, B input/merger etc. cannot be combined into the current V2.

This article follows the data audit of 2026-10-01, completed the five-step logic and code comparison on 2026-10-02, and supplemented the "partial body" target compliance and availability/identification review on 2026-10-03. These revisions do not modify the network, training algorithm, acquisition contract or weights, and are not new training or capability acceptance.
