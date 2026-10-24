# Single-joint double-link: from physical state, representation selection to sampling and FB input

Revision Date: 10-10-2026. Zero-position/drive/B input resolution and cross-audit amendments synchronized; design not yet implemented.

For the corresponding next version of the engineering scheme, see [V3 Network and Training Implementation Scheme ](V3 Network and Training Plan.md), including the current code gap, input contract, asymmetric FB update, and randomized sampling specific implementation arrangements; the scheme has not been implemented or trained.

The goal is to train the execution unit of a motor + two adjacent links, first distinguish and organize its own movement and driving output, and then provide the upper layer to coordinate multiple units. This round has confirmed that the characterization target is **result status**; the motor dynamics parameters are responsible for forming various execution conditions, B is not directly added, and the model/capability parameters themselves are not set as the characterization target of z. The known parameters are still given to the Actor and the upper layer, and the training F also reads the actual values. The logic is as follows: **What local states and processes are actually there → What differences are retained in this round B → How to collect these states and transitions → What conditions does F/Actor need to learn control. **

The B input determined this time is: **The fixed sequence of the lengths of both sides, q, dq, actual driving torque, joint limit information, calculated end relative velocity, and causally estimated angular acceleration and corresponding end relative acceleration. ** Acceleration estimates are marked valid. All spatial quantities are defined according to the motor body coordinate system M, and the world position, world speed or world attitude is not input to B; the contact point and the true value of the external force are not input to B. B does not receive the original history, but the acceleration feature has used the processed history and can no longer be called a purely instantaneous representation.

** Make sure to use asymmetric training: Actor does not read the true value of the unknown dynamic load. During training, F directly reads the randomized load and related dynamics and boundary true values. ** The known connecting rod mass, center of mass, and inertia are still directly given to F/Actor; Actor uses local action-response history adaptation to the unknown effects after connection, and F uses simulation true values ​​to learn subsequent predictions. Deployment preserves Actor with B and does not rely on privilege F. This is a confirmed design and is no longer listed as an option for validation, see Section 4.

The following are the next version of the design, and the current V2 code and weight have not changed. The first round still uses a planar one-joint model of known cross-section, shaft and mounting conventions; q/dq and precise shaft torque are first read from the simulation, where precise shaft torque continues to be marked as privileged. The acceleration is estimated from the same set of causal telemetry processes, and is not replaced by the simulated instantaneous truth value by default. The three-dimensional environment and arbitrary connecting rod geometry are different expansion problems.

## 1. Describe position, speed and force in the motor body coordinate system

### 1.1 First fix the order and coordinates of the two poles, and they cannot be exchanged with the direction of rotation.

The origin of M is at the center of the motor joint, and the coordinate axis is fixed to the stator/casing. P (housing_link) is the rigid connection side of the housing, D (output_link) is the output shaft/flange connection side; when equipped with a reducer, D is not called the rotor side, and P/D does not mean the near end/far end. Fixed ordered input is (L_P,L_D). It is agreed that the positive axis aᴹ, the increase of q means that D rotates in the positive direction relative to P around this axis. P/D is not exchanged when dq or torque changes sign.

"Sort by rotation direction" can only be used to establish this fixed forward direction convention, and can not be sorted dynamically by whether the current is rotating forward or reversing. When the parent-child order of the simulation model tree is inconsistent with the actual shell/output side, the interface must be explicitly mapped and the symbols of angle, speed, torque and limit must be unified.

P is fixed to the motor shell, which does not mean that P is fixed to the ground. The shell can be carried along by the entire body; this does not change the position of its attachment point in M. The network interface in this article only uses M. The global reference used internally in the physics engine is used for solving and is not used as a natural observation or additional behavioral target of the unit.

# # # Distinguish the original zero, model zero and geometric zero first

Below, q refers to the unified physical angle q_c. The zero angle is the linear expansion of the two rods of this geometric family. It is not assumed that the original qpos=0 of each motor is this posture. The original encoder angle q_e on the output side is converted by the known calibration `q_c=s*q_e+beta`, s=±1, beta is the physical angle corresponding to the original zero; dq, torque and history are converted in the same direction, sorted after the limit conversion, and the inverse transformation is requested. The power tau*dq remains unchanged. The model_adapter and device telemetry_adapter of the MuJoCo tree coordinates/axis/ref are registered separately. Fixed D is not equal to the encoder change number and cannot be repeated. If the telemetry comes from the rotor, it must first be switched to the output side according to the trusted transmission model, and the rotor torque must not be regarded as the output torque.

It is known that beta/s is the configuration input of the feature device and does not spell B repeatedly: the same original zero and different beta should have different entity postures and different unified q; the same entity posture and different encoder numbers should get the same g. The first round requires valid calibration. If it is missing, the valid geometric interface will be rejected and acc_valid will not be used as the calibration valid bit. Unknown zero biases are not guaranteed to be identified from local history, and will not be mixed into the main training in the first round; in the future single-column robustness group, Actor/B only uses statement calibration, and F can read the hidden truth value.

The zero-position difference of the first-round known planar coaxial straight rod can be handled by this mapping. Non-coaxial, eccentric, non-linear rod, flexible/differential drive needs to expand the geometric/transmission model, and can not follow the formula of length and angle only. See [Zero and Parameter Resolution ](V3 Zero Position and Motor Parameters.md).

### 1.2 What are the combinations of position, speed and drive output?

| Actual possible local situation | What is the difference between physical quantities | Is it the current state or the process |
|---|---|---|
| Expansion at different angles, or the same angle but different rod lengths | L_P/L_D, q, calculate the position of the ends of the two rods in M ​​according to the installation relationship | Current relative configuration |
| Stationary at the same position, forward and reverse rotation, or different speeds | dq, the position change rate of the end in M ​​| Current relative motion |
| Accelerating, decelerating or nearly constant speed under the same q/dq | Angular acceleration and terminal relative acceleration; network reading limited window estimation | Recent motion response, not an independent degree of freedom that can be assigned arbitrarily |
| Under the same movement, the motor output direction/size is different | actual shaft torque τα | current drive output |
 The current state of the q configuration conditions is explained jointly with the current q
| Maintenance, acceleration and deceleration, reverse, reciprocation, vibration, recovery after loading | Continuous change of the above amount over time | Need to shift or a trajectory |
| Similar motor responses but different external action points, directions and forces | Additional external action truth values ​​or estimates required | Physically different, epicycle B does not guarantee distinction |

Position-velocity-force are joint descriptions, not three mutually exclusive tasks. Maintaining means that q is approximately constant, dq is close to zero and the output is adjusted; one-way rotation means continuous movement in the same direction; vibration means reciprocating position, speed reversal and corresponding changes in output. A single frame cannot account for vibration frequency, phase, or persistence.

"Force" in this round B clearly refers to the motor driving torque. It can distinguish between a static light output force and a static large output force, but it cannot be concluded based on this alone whether the latter is pressing an obstacle, overcoming gravity, or maintaining normally. Completion of an order also requires intent, timing and actual progress.

# # 1.3 End velocity is the calculated relative motion, not the overall velocity measured externally

The end of this round refers to the end of each rod away from the study joint. When a fixed installation relationship is known:

\[
r_{\mathrm{tip},P}^{M}=r_{P0}^{M},\qquad
r_{\mathrm{tip},D}^{M}=f_D(q;L_D),\qquad
v_{\mathrm{tip},D}^{M}\equiv
\frac{d r_{\mathrm{tip},D}^{M}}{dt}=J_D^{M}(q;L_D)\dot q.
\]

The coordinate change rate of the fixed point on the P side \(v_{\mathrm{tip},P}^{M}=0\) can be omitted from the network input. Both rods cannot be written to rotate by ±dq relative to the housing. When M move together, P may move in the physical environment, but there is still no relative motion in this system.

In order to facilitate checking, the convention is extended using the local + y-joint axis of the current model and the straight line of two rods q = 0: from the point of view of the study joint, the P end is at + z, and the D end is at − z. Thus:

\[
r_{\mathrm{tip},P}^{M}=(0,0,L_P),\quad
r_{\mathrm{tip},D}^{M}=(-L_D\sin q,0,-L_D\cos q),
\]
\[
v_{\mathrm{tip},D}^{M}
=(-L_D\cos q\,\dot q,\ 0,\ L_D\sin q\,\dot q).
\]

The planar version inputs its two components, xα and zα; different zero/axis conventions are calculated according to the corresponding kinematics. The relative velocity depends on the vertical distance from the end to the axis, only in this case there is\ (\ | v_{\ mathrm {tip}, D} ^ {M}\ | = L_D |\ dot q |\).

* * This speed is a derivative of known kinematics and does not require additional sensing information or world coordinates. * * Explicit input to B and F/Actor is to expect them to use linear velocity scales and directions directly, reducing the burden of relearning known mappings; whether this improves learning remains to be verified. You can't rotate the simulated COM velocity, just think of it as the relative velocity of the end here.

Angular acceleration can be estimated from the velocity history, such as \(\widehat{\ddot q}_t=(\dot q_t-\dot q_{t-k})/(k\Delta t)\). This is a response estimate over a period of time, with noise and time smoothing effects, and is not equivalent to a direct measurement of instantaneous acceleration without delay. The second-order change rate corresponding to the end coordinate is:

\[
\widehat a_{\mathrm{tip},D}^{M}
=J_D^{M}(q)\widehat{\ddot q}+\dot J_D^{M}(q,\dot q)\dot q
=\bigl(L_D\sin q\,\dot q^2-L_D\cos q\,\widehat{\ddot q},\ 0,
L_D\cos q\,\dot q^2+L_D\sin q\,\widehat{\ddot q}\bigr).
\]

The coordinate second-order change rate of the fixed connection point on the P side is still zero. The end relative acceleration here contains tangential and centripetal terms, and the entire vector cannot be replaced with L_D × angular acceleration alone. It is derived from q, dq and angular acceleration estimation, and does not add independent sensing information; it is also an approximate feature after using window estimation.

**Relative acceleration is not the terminal inertial acceleration. ** When the motor housing translates and rotates as a whole, there are also housing translation acceleration, angular acceleration, centripetal and Coriolis terms; this motor history alone cannot be generally restored. This article does not therefore add world motion or IMU truth values ​​as B input.

### 1.4 What are the request, actual torque, external force and limit respectively?

u is a normalized request sent to the driver. In V3, u∈[-1,1] corresponds to the declared and actually adopted S_req*u N·m. S_req is configured with the motor capability level (old V2 is fixed at 6); τₘ is generated after delay, capacity limit and drive response. The τ̂ obtained from the current calibration is an estimate of the actual shaft moment, and the first run uses simulation-accurate τₘ and is marked as privileged. u is the action that has been initiated or the action to be evaluated, not the upper layer z, nor the additional sensing amount.

τₘ cannot represent all external forces on the connecting rod. A vertical force of 10 N at 0.1 m from the axis and a vertical force of 5 N at 0.2 m both produce 1 N·m. Even if the rod length is known, it is not possible to generally locate the contact point and resolve the force simultaneously. τₘ·dq describes the total mechanical power of the motor; the absorption of mechanical energy does not automatically equal the recovery of electrical energy.

Limits come from assembly, collision, cable and control configurations and are provided directly if they are known, without requiring historical guesswork. Two joints with different limits can have the same history of motion in the middle area. The distance limits \(q-q_{\min}\) and \(q_{\max}-q\) are still derived features, not independent degrees of freedom; but the limits can enter B to help explain the current travel conditions of q/dq.

# # 1.5 Connecting rod inertia parameters can be known, the dynamic load after connection is not equal to these parameters

The inertial of URDF can record the mass of each rigid link, the position of the center of mass, and the inertia tensor about the center of mass, as well as its coordinate convention. When the field exists and the model is trustworthy, it can be provided directly; length and mass do not uniquely determine inertia. Missing inertia parameters cannot be pretended to be known with zero values. Simulation can obtain accurate parameters, and real machines are usually model values ​​obtained from CAD/calibration. The differences in source, validity and model errors should be retained.

Splicing does not automatically make each rod's own inertia unknown, but joint response also depends on body configuration, other joint motions and actuation, floating bases, contacts, and constraints. The so-called "joint equivalent inertia" also depends on how other degrees of freedom are constrained or responded. It is not a simple addition of the inertia of two adjacent rods, nor is it a fixed load field of the URDF.

In a simplified fixed-support, single-axis model one can write \(I_{\mathrm{eff}}\ddot q=\tau_m-\tau_{\mathrm{load}}\). The unit of I_eff is kg·m², describing the difficulty of acceleration; the unit of τ_load is N·m, describing other effects combined according to the model used. When the inertia is known and the acceleration can be estimated, the total load moment can be estimated; when the inertia and external load are unknown at the same time, it usually cannot be uniquely decomposed. Multi-joint couplings cannot directly apply this scalar formula, nor can the residuals be referred to as positioned contact forces.

URDF plus enough systemic state and constraint information can calculate the dynamics of model predictions; only URDF, real-time contact force or dynamic load truth cannot be obtained. Force sensors, full-body observers, or upper-level estimates can all supplement the information, so it can't be said that any robot “can only rely on local history.” * * These additional sensing interfaces are not contracted for this round of Actor online control, and unknown loads are mainly provided by their own historical responses; estimated conditional, may not be unique, and do not promise to output accurate loads at each step. * *

# 2. What is reserved for this round B, what can z organize

### 2.1 Clarify B input and source

This round uses:

\[
g_t^P=
(L_P,L_D,q_t,\dot q_t,\tau_{m,t},
\ell_{\mathrm{type}},b_{\mathrm{limit}},q_{\min},q_{\max},
v_{\mathrm{tip},D,t}^{M},
\widehat{\ddot q}_t,\widehat a_{\mathrm{tip},D,t}^{M},
b_{\mathrm{acc},t}),\qquad e_t=B(g_t^P).
\]

l_type means a body with a limited itinerary, cycle rotation or circle of meaningful bodies, and b_limit indicates whether the boundary exists/is available; b _acc indicates whether this acceleration estimate has a sufficiently effective history. When the first round only uses a known legal and limited itinerary, they may be fixed; Other types will be supported in the future by a visible code, which will not be used to impersonate an open rotation without the upper or lower limit. Superscript P reminds the first round to be precise and m is a privilege, and does not mean that neither the length of the pole nor the q or the end-of-general speed is available.

| Enter | Meaning and Origin | Reasons for joining B |
|---|---|---|
| L_P, L_D | Known rod lengths with fixed side order; remaining geometry is agreed upon by the current model | Distinguish between configuration and motion scale; rod lengths not inferred from motor history |
| q, dq | Load side relative angle and velocity estimation, first round read simulation value | Differentiate current configuration, steering and speed |
| τₘ | Actual shaft torque; the first wheel is the true value of the simulation, and the real machine can usually only obtain estimates | Distinguish different driving outputs under the same motion |
| Limit Information | Known Agency Configurations | Differentiating the Meaning of the Same q/dq in Different Available Trips |
| v_tip, D? | Simultaneous geometry, q, dq kinematically calculated velocity vectors | Explicitly provides the relative scale of motion and direction of the end of the link |
| Angular acceleration estimation, a_tip, Dᴹ, b_acc | Causal velocity history estimation and its kinematic mapping; see Section 4.2 for the estimation process | Distinguish between recent acceleration, deceleration and near-uniform speed response, mark invalid estimation after reset; cannot be regarded as the true value of the load |

In the planar version with a fixed geometric family and a fixed finite stroke type, the continuous field is 12 scalars: there are 9 components in the original two lengths, q/dq/τα, upper and lower limits, and two components in the end velocity, and then there are 3 components in the angular acceleration estimation and the end relative acceleration. Add b_acc valid bits; limit type/validity is counted according to configuration. This is just an input field count, and does not change the defined latent dimension or hide the layer width, nor does it introduce a GRU.

B does not read the original history, u, or z to be performed, but acceleration estimates explicitly rely on past data and can no longer be called B with no historical information at all. Mass, inertia, drive queue, and contact/external force truth values do not belong to this version of g; end positions can be calculated from length and q and explicitly fed back, and do not continue to superimpose on this input. The geometry, q, limit and velocity must be uniformly unitized/normalized, and the velocity cannot be divided by the length of the rod and then the linear velocity scale to be retained is lost.

# where the electrical parameters go, the semantics of the results

Do not use "static parameters are not allowed to enter B" as an excuse. Length and limit have been used to describe geometry and stroke and are retained; the known zero position/direction has been eliminated through preprocessing and is no longer used as an independent result label. Nominal mass/inertia, driving capacity, time constant, delay, damping/friction/armature affect how to achieve the same motion result. The first round declares the value to the Actor and the upper layer. F reads the actual value and does not increase to g13.

The same q/dq/tau/ddq and geometric/limit, but with capacities of 3 and 6 N · m respectively, can have the same B; it does not mean that the two execution units have the same capacity. The upper layer must read known_model/known_drive (source, valid bit, version) at the same time, not read-only B16. If the current call requires semi-declared capacity, first calculate the fixed tau * = .5 * C_decl from the current device C_decl, and then use the absolute torque query. If you want each sample in the reference pool to define the same "utilization result" as its own tau/C, the current g does not contain C, and the result field must be redesigned; just giving C to F does not hold.

In the same way, in the future, the kinetic energy/measured saturation state, etc. must be queried before the required B field is evaluated; all model parameters are not put into B in advance. Even if known parameters can enter the network, there is no guarantee that FB will retain them losslessly. The additional unchanged configuration under global ρ also represents the capacity cost, and priority is given to retaining the result definitions related to the current round's position-speed-output-recent response.

### 2.2 Limit the capability commitment to the range that this input can really distinguish

Epicycle expectations B distinguish: relative configurations, angular and terminal relative velocities, actual driving torque, recent angular acceleration and terminal relative acceleration under different geometries and strokes, and feasible combinations of these quantities. Acceleration is the response information of "how the motion changes", not the recognized equivalent inertia or external load. The space where z is located is used to organize behaviors such as reaching, passing, maintaining, acceleration and deceleration, torque adjustment, and joint compliance. It does not require a dimension-by-dimensional correspondence to a certain physical quantity.

If the g of the two contacts are exactly the same, then B must be the same; even if F knows the contact point and external force, it will not allow B to output two different state codes. From this, this round:

- You can study how to adjust the action under different loads/contacts with the same local intention. Obstructed acquisition, reverse drag and release are still necessary.
- B is not required to locate contact, read pressures on specified objects, or fully connect loads, nor does it claim to have a universal z-interface that specifies contact forces.
- Torque adjustment and compliance can be learned; when the single contact geometry is known and the motion/other load conditions are sufficient, the conversion of torque and a certain force component can be discussed separately, but it cannot be generalized to arbitrary external force control.

Holding, reciprocating, or vibrating is a continuous process generated by the strategy and does not add a "vibrating" label to B; a short window acceleration estimate is not sufficient to determine frequency and phase. Different recent accelerations will produce different B inputs for the same q/dq/τₘ, but whether B retains this difference still depends on training. Different inertias and external loads may also produce the same all g, especially when stationary; in this case, B must be the same, and it cannot be required to know in advance who is more difficult to start. Actors adapt using known parameters and action-response histories; training F also reads load truth values ​​to distinguish conditions that are not directly observable to the actor. Additional information about F cannot eliminate the indiscernibility of the Actor itself.

### 2.3 Structure and stroke are characterization conditions, not targets that require the motor to change

Entering the length and limit into B does not mean asking z to change the length or limit. The complete state goal should be constructed according to the length and limit of the current unit; if the preference query only requires a certain speed or moment, there is no additional requirement to copy the configuration of other samples.

The limit distance can be calculated from the existing field and no longer need to be used as an independent state dimension. The perspective of the cycle institutions indicates that the necessary circles are to be kept in multiple circles for continuity across the spectrum; These changes need to be synchronized with sports and training. Nor does input type support mean that the counterpart institution has been trained to be covered.

## 3. Derivation of sampling and randomization engineering from these representation differences

### 3.1 First determine the changes and continuous transitions corresponding to each input

| Differences/relationships you want to learn | How it happens in simulation | Actual coverage check |
|---|---|---|
| Configuration and length | Cross-take the length of the rods on both sides and the legal initial angle, sweep the angle in two directions or smooth excitation, enter and leave the angle range from the inner area | The order of both sides is fixed, length × q combination and entry/exit transfer |
| Different movements in the same position | Change the initial speed, direction and excitation, through the same angle interval | Positive and negative, near zero and different amplitudes of q × dq |
| Same angular velocity, different tip velocities | Repeated angular velocity range under different L_D | L_D×dq and calculated v_tipᴹ; cannot only adopt a single length |
| Similar end speeds, different angular velocities | Cross-select length and dq in the same q interval, for example, calculate dq=s/L_D according to the signed tangential speed s, and then check the corresponding relationship between the direction/size of v_tipᴹ and dq in the speed range; the speed cannot be filled in independently |
| Same motion, different output | Change inertia and continuous load, repeat hold/speed rules and load and unload | q×dq×τₘ, static belt force, drive and back-drag |
| Same q/dq, different feasible boundaries | Change the limit in the legal mechanism, and then approach, stay, and leave in the opposite direction | Stroke center, span and asymmetry; avoid all data concentrating on the limit |
| Same request or output, different responses | Change the drive delay/capacity, respectively, or change the damping, external loading and adjacent motion | Separate the two responses→ of u τα and τα→ motion |
| Similar q/dq/τₘ, different recent accelerations | Cross inertia, continuous load and loading time under the same geometry; match similar motion/output intervals from the real trajectory | Acceleration estimation positive and negative/magnitude, dq×acceleration and estimated delay; negative angular acceleration is not collectively called deceleration |
 Adaptation after the unknown load changes  physically loads, removes or alters the adjacent effect in a continuous trajectory; Actor does not read the change schedule or load real, F reads the current real values that are in effect  before the change, the response appears, adjusts and recovers; The same currently observed but different loads/historic samples are retained
| Adjacency coupling in contact | Establishment of contact, loading, moving support, unloading or disengagement while adjacency drive remains on | Simultaneous adjacency movement, contact and release; cannot be replaced by two independent environments |
| Maintain, reciprocate, adapt, recover after being blocked | Continuous rule incentive, external push/drive, obstacle removal or reverse | Continuous segment, commutation, load change and true transfer after release |

v_tipᴹ is always calculated from the geometry, q, dq of the same sample; the angular acceleration is estimated from the continuous velocity history preceding this sample, and a_tipᴹ is calculated as in Section 1.3. Accelerations cannot be independently assigned randomly; there may still be different implicit loads at the same g. The initial state of q/dq satisfies the mechanism constraints; the external force is generated by the loader or real contact, and the desired contact force cannot be directly written into the observation. Different truth values ​​of external forces under similar g can be used to check conditional differences and indiscernibility, without requiring B to distinguish the same input.

The generation, scheduling and data paths that can be implemented are given below. The values ​​are the starting point for the first round of engineering and should be written in versioned configurations; they are not FB theoretical requirements or verified optimal ratios. This time we only modify the design and do not start collection or training.

### 3.2 The model is compiled according to structure and topology, and the boundaries must be combined and covered.

An active joint of the unit is retained, and the adjacent motor belongs to the outer body boundary. The shape, joint limits, contact switches and connection topology are compiled into the model library, and multiple worlds with the same model structure are run in batches; only the mass/inertia, damping, drive and boundary parameters allowed by the engine are modified in each round, and the relevant model constants are recalculated after the update. You cannot claim that physics has been randomized while only changing observations.

• Initial collection of quotas for the full period
|---|---|---:|
| Fixed support | The P or D side is completely fixed and the other side moves; change the installation load and record the identity of the fixed side | 20% |
| Elastic/moving support | Support carrier or spring-damped connection, moving reference on feasible trajectory | 15% |
| Contact and loading | Ground, object or movable stop; approach, restraint, sustained force and release | 20% |
| Adjacency drive | Planar series adjacent joints continue to move, and the independent output of the joints is studied u | 15% |
| Adjacency Drive + Contact/Support | Both adjacency action and contact exist in the same physical model, entering and exiting constraints during execution; about a quarter of this quota is for legal bilaterally constrained/limited compliant clamping | 30% |

The quota is calculated according to the actual effective control transfer statistics, not according to the number of models or "how many probabilities are written in the configuration". The combination condition has a high initial quota to cover the simultaneous role of subsequent stitching; it is not for the unit to assume the task of full-body balance in pre-training. Bilateral constraints need to check the degree of freedom of the mechanism and the consistency of the constraints, and it is not possible to arbitrarily designate two endpoint trajectories to make a closed chain that is not feasible.

First use a small amount of fixed support data to verify the coordinates, drivers and samplers, and then start all working conditions; when the combined model, recording or inspection is not completed, it is not allowed to silently allocate the corresponding quota to simple working conditions and then declare the course completed. After opening, each statistical window will check the actual proportion, record the reasons for the shortfall and make up for it.

All sides, lengths, masses, strokes and dynamics must meet geometric/constraint legality; "all combinations must be uniform" is not forced to generate an infeasible closed chain or collision state. The fixed side is the boundary selection and the P/D is the fixed mechanical identity. Even if D is clamped, B's L_P/L_D or coordinate signs cannot be swapped. The influence of P length/mass on local motion also needs to be collected in P movable or coupled working conditions, and cannot only rely on a model in which P is completely fixed.

### 3.3 Randomized configuration of body, limit, drive and load

The generation sequence is fixed as: **Geometry and physical legal range → Known limit configuration → Mass distribution and drive → Connection/external load → Legal initial state → Continuous excitation. ** Parameter random streams are derived separately according to configuration version, structure, round, and purpose to avoid parallel world numbers changing all sampling; model rejection and fallback retain counts.

| Random items | First round configuration and generation method | Relationships that must be checked |
|---|---|---|
 Both lengths L_P, L_D are given as the initial range of 0.15 - 0.45 m, cross-cutting by short/medium/long stratum; (a) Retain the symmetric extension candidate for the existing length range, P and D, and check the installation and collisions on a model basis; It's not just an exchange of fields.
| Mass distribution | The base mass on both sides is a logarithmic stratification candidate of 0.15–2 kg; the counterweight ratio is 0–20%, the position on the pole is 20%–80%, and the center of mass/inertia is compiled from real geometry | Covers different inertias of the same length to avoid permanent one-to-one binding of length and mass; invalid or insufficient control capabilities are marked separately |
| Joint response | Damping 0.01-0.08 N · m · s/rad, Friction 0–0.08 N · m, armature 0.001-0.006 kg · m ² as the starting point of the existing scope of work | Actual random values are given to training F and saved; Actor reads only declared/nominal values, unknown deviations are retained as factors to be adapted; covering zero-speed/low-speed response |
| Drive | V3 capability benchmark C0=3/6/9 N·m equivalent, request scale S=1.25C0; real capacity C0×[.8,1.2], time constant 5–20 ms, delay 0–10 ms | Output side equivalent model; high requests can indeed trigger the capacity limit of each gear, the declared/actual fields are separated, and the fixed SI scale does not change the torque |
| Zero position/direction | beta circle of eight sectors, s = ± 1; each configuration is fixed, known calibration | true q_raw = 0 corresponds to different attitudes, and is equivalent to the physical state after conversion across the coding convention; coordinate recoding is not used as a new dynamic coverage |
| Limited travel | Each model first obtains the legal connected interval [a,b] approved by the collision/cable agreement; takes the width w=f(b−a), f∈[0.5,1], then takes the center c∈[a+w/2,b−w/2], and sets the upper and lower limits c±w/2; at least a quarter of the configuration remains intact [a,b] | The legal model and control limits are recorded separately; offset/asymmetric travel is generated. If the legal range is still only ±1.2, it cannot be claimed that the mechanism travel has been extended |
| Loads and contacts | Explicit forces cross between the currently covered sides, points of action and directions; the upper limit of the initial amplitude can be 0.5Mg, with an additional plane force couple of ± 1.8 N · m; contact friction 0.4–1.0 as the starting point | Both near-zero and compensable loads are retained and recorded; contact forces are solved by actual interaction and are not directly specified |
| Support and adjacency | The legal elastic support range is used; the adjacency reference amplitude 0.1–0.7 rad, frequency 0.3–2 Hz is the starting point, and is limited by the adjacency’s own stroke and drive | The actual implementation is driven by feedback and does not directly cover the physical speed; recheck penetration, impact and numerical stability after combined contact |

Random parameters hold both the "physical truth value" and the "model value declared to the Actor". The mass, center of mass, and inertia of the two rods in the first round can be accurately declared to simulate a credible URDF; after unknown external loads, adjacent dynamic effects, and uncalibrated drive changes take effect in physics, the actual values ​​are provided to the training F and cannot be written to the Actor's observations or history. The first round of mass group 80% accurate declaration, 20% fixed Actor declaration model and perturbation of physical mass/inertia at .8–1.2 density multiplier, F still reads the actual parameters; mass and driving errors are counted separately and can be combined independently; Actor's historical adaptation and F's privileged prediction are expressed separately. Round constants are recorded as configured, time-varying loads are updated at each control boundary, and F cannot just be provided with initial sampled values. See Sections 4.1 and 4.3 for fields.

These candidate ranges come from existing prototypes and their symmetric coverage requirements and do not represent any robot parameter ranges. If the base mass weight and round scaling are used at the same time, the final value must be recorded, and not only the nominal parameters before sampling can be audited. Continuous rotation model, three-dimensional geometry and larger folding range are created and checked separately; it is not possible to just loosen the q input or close the self-collision even if the machine is feasible.

Zero position beta, model joint ref/shaft and solid assembly are checked together. Normal initial state is still stratified by physical q_c, and then raw is reversed to avoid all rounds of fixed raw = 0 to bind the beta to the initial state; special raw = 0 pairing is only performed when the beta is a legitimate physical stroke. Real stops/accessories are re-checked for mechanical legitimacy with installation changes; only recoding limits will not increase the physical support range. The random distribution on the output side of the motor is a validation model, which is not equal to the joint distribution of true models; the first round does not simulate temperature rise, speed-torque envelope, current calibration error, tooth gap or elasticity, and cannot claim to have supported all motors.

The driver's accurate declaration group accounts for 80%; the 20% error group declares ±C0, T=.01 s, delay=.005 s, damping=.03, friction=.02, armature=.003, and is actually sampled according to the range. S is the interface scale that is known and actually effective for both groups. The quality and driving errors use independent random streams and are not permanently bound. The specific fields and backend paths are subject to Section 6 of V3.

The initial angle of the limited stroke is stratified by\ (\ xi = (q-q_{\ min})/(q_{\ max} -q_{\ min})\): [0,1] is divided into ten rotation samples, each long window covers the entire interval, and the true angle and limit are retained. Avoid initial state penetration into the hard limit; the position near the constraint is obtained by legal reset or dynamic approach. The velocity initial state is first grouped close to zero, positive and negative low/medium/high, and the wide range is ± 4 rad/s. The initial state near the limit and the speed pointing to the boundary needs to be within the impact range allowed by the model; if it is feasible but cannot be stopped in time, it is classified as a restricted process and cannot be marked as maintaining success.

The three-dimensional expansion is based on the new load/coupling relationship, and the relative velocity definitions of M and B of this system remain unchanged; the simulation is not upgraded to gather the three velocity components.

### 3.4 Write transient, sustained and recovery as acquisition process

Each rule trajectory has a clear process stage and a predetermined budget that records the actual moment of switching. The hold/velocity reference is generated from the current configuration and does not continue to use the fixed ± 0.8/ ± 0.6 reference angle common to all models. The intent and stage of the rule are for scheduling and auditing only and do not assign a permanent z to each type of process and do not go into B.

| Process | Generation and persistence rules |
|---|---|
| Short transient | Initial use of 40/80 ms bidirectional torque or command switching, check for u→τₘ delay and motion start; approximately 20% of rule data control step budget |
| Continuous movement | Sweep angle, one-way finite segment, braking and reciprocating, initially 0.5–2 s per segment, accounting for about 30% of the regular budget; trajectory speed/amplitude needs to adapt to the current limit and drive |
| Sustained loading and recovery | "Approach or establish motion→Maintain/continue→Load or block→Unload or reverse→Recover"; accounts for about 50% of the rule budget, and sets aside observation sections before loading, during loading and after release |
| Online strategy process | Current B-encoded legal goal or random direction generates z, Actor exploration; retains short/long calls and repeated perturbations, and does not use rule references to replace its actual actions |

The initial duration of each main observation segment of the continuous process is at least 0.5 s, and exceeds five driving time constants; the initial duration of the approach/recovery segment is at most 2 s. The five time constants only indicate that the drive output is close to stability, but do not indicate that the machine is stable. The first round of audit thresholds in the retention process can start from the angle error not exceeding 0.05 rad, |dq| not exceeding 0.05 rad/s and continuous for 0.2 s. The configuration is written and reviewed according to the application standards; if it is not reached, a timeout will be recorded, and its true transfer will continue to be retained, and cannot be remarked as a retention success. The speed/reciprocating process is audited according to the corresponding trajectory error and continuity, and zero speed is not required.

The initial budget of the round is 10 seconds to accommodate establishment, loading and recovery; the process can be truncated if it exceeds the budget, but the truncation stage must be recorded, and the truncation cannot be regarded as an environment failure or physical termination. The necessary extension budget is determined by the measured mechanical response, and should be adopted after modifying the configuration version; you cannot wait without an upper limit or discard slow response structures all the time.

Rule reference and gain are also configurations and are performed with the current real drive channel and record saturation. V3 performs reachability/carrying calibration on the rules before P0, and uses clearly recorded static offset compensation, inertia calibration PD and anti-saturation integral; if the steady-state deviation of the old PD cannot be used, it will be judged that the motor is unreachable. Rules can use privileges to generate actions without incurring actor teacher losses. Obstacle release is achieved by withdrawing the drive or the actual movement of the object, retaining the movement process; not instantly deleting the object to create false impulses when there is contact force. Snapshot restart needs to restore dynamics, drive queue and current boundary process, and re-padding the history; the new trajectory and the original trajectory cannot be combined into a continuous history.

### 3.5 Separate collection scheduling, Replay sampling and target/reference distribution

| Data link | First-round project decision | What should not be confused |
|---|---|---|
• Collecting and dispatching initial completion of the rule library, with rules/strategy each accounting for about 50 per cent of the control step budget; Both paths are allocated according to 3.2 knots.  This is the ratio of behavioral data sources, not the name reward weight, not the skill ratio Actor has.
| Replay reserved | Rules and online sub-library store real adjacent transfers, recording sources, configurations, working conditions, rounds, stages, times and termination reasons; the rule base will not be completely flushed with the online FIFO | The key rule transfers acquired must participate in Bellman learning and are not only used as goal pools |
| Replay sampling | After the online data is sufficient, the initial batch is divided into half from each source; the source is sampled independently according to the working condition → geometry/limit group → current boundary coverage key family → bin → real transfer; the weight and empty group processing are subject to the fixed configuration in Section 8 of V3, and Bellman data is not screened according to the posterior success | The data collection ratio and the gradient usage ratio are counted separately; the joint stratification adopts practical groups and does not pursue full Cartesian product uniformity |
| FB reference distribution ρ | When retaining the same batch reference estimate of V2, ρ is the next g distribution induced by the above transfer sampling; the independent query pool is built according to the same stratification/weight and records the version | Changing the Replay weight will also change the actual ρ; queries cannot continue to use the unsynchronized old pool/cache |
| goal z sampling | The first round still mixes the random direction with the complete goal encoding of the current B; the complete goal is preferentially drawn from the real results of the same geometry/limit configuration group | The goal distribution is not equal to the FB reference distribution; the goal extraction does not change the Bellman transfer itself |
| Physics preference query | Constructed according to the ρ integral declared by the training; length/limit is not used as the desired change quantity; cache is updated with B and reference pool versions | "Only draw goals for the same configuration" cannot be mistakenly written as "Query points are automatically conditionalized according to this configuration" |

When the rule base is not ready, only the startup phase is reported, and a large number of repeated few frames cannot be used to pretend that coverage is complete. The ratio is the starting point for the first round of actual access to the organized transfer and coverage strategy, and subsequent adjustments and records are only based on coverage and learning evidence to avoid confusion with reward projects.

Geometry/limits are grouped into fixed structure libraries so that the same configuration goal can be supported by real data. When there are no samples in the group, the record will fall back to random z or continue to collect additional data. You cannot copy the fields of other structures and pretend that it is a real visit state. If it is changed to continuous structure sampling or conditional ρ in the future, data estimation and query rules need to be derived simultaneously, and the FB theory definition will not be silently changed in this project supplement.

The same batch loss of the old V2 can still be used as a starting point; after the number of configurations is increased, it is necessary to check whether the reference matrix mainly reflects the inaccessible differences between different structures, and the motion relationship within this structure is insufficiently fitted. This is a limited capacity and distribution problem that cannot be ignored because it formally supports shared networks, and does not immediately increase loss or network capacity accordingly.

### 3.6 Check whether the parameters actually change the response to prevent "random but not learned"

Each new random item is conditionally compared before formal batch collection: keep the structure and initial state the same, repeat the request, and then look at the actual changes of τα, dq, q and the continuous stage. There may be three outcomes after the parameter change: the effect is activated; it is not activated in the current excitation; and only the other constraining reactions are changed without changing the selected state of this unit. They are recorded separately, and the random number range cannot be used as an effective kinetic coverage.

The counterexample of the old V2 is that capacity 6.5 and 7.2 will not have different limits under the same other conditions when the request always exceeds 6 N · m; retaining them may indicate unsaturated conditions, but it cannot be claimed that the two capacities will be distinguished. When P is completely fixed, changing the mass of P may only change the fixed support load, and its effect on motion needs to be tested in the P movable/coupling condition.

Statistics are initially output for every 100,000 accumulated effective control transfers: scheduled and actual operating conditions/process ratios, parameter quantiles, initial state and visit coverage, acceleration efficiency/amplitude/top-cutting conditions, proportion of rules/online entry gradients, near-limit dwell and departure transfers, loading and release completeness rates, timeout/rejection/back-off counts. Comparing causal estimates to time-caliber matched simulation references, noise and response lag are reported separately; finite window averages at contact impacts cannot pass off instantaneous peaks. The planned snapshot ratio is also separated from the actual recovery ratio, and the planned 20% cannot be regarded as achieved like old data.

Model failures such as numerical divergence and illegal penetration are marked and repaired, and are not mixed into training as physically blocked samples; transfers that are physically legal but cannot be completed are retained. Resampling cannot splice history across rounds; real termination and time truncation are recorded separately and bootstrap is processed separately, and the state after reset cannot be regarded as the next physical state.

The list of independent seed and structure/boundary combinations for training and verification, in particular, sets aside unseen parameter instances of the "adjacency + contact" combination; the randomization actually works and the strategy can be reliably invoked and checked separately. All records use the same coordinates, timestamp, and schema version.

Original records per step can be reconstructed:

\[
(x_t^P,p_t,u_t,x_{t+1}^P,p_{t+1},g_{t+1}^P).
\]

g is aligned to the current control boundary, the velocity is calculated by the corresponding value; the acceleration only uses the data obtained up to that boundary, and retains the valid bits, the estimated configuration version, and the elapsed time window. Each Replay transfer preserves the causal prefix or equivalent estimator state needed to reconstruct x/g at the same time, and the adjacent rows after scrambling sampling cannot be regarded as history. External actions, real random parameters, drive internal state, and boundary truth values make up p_t/p_{t +1} separately for training F and audit reads; these privileged fields cannot be accessed by the input assembly of Actors and Bs. Each current/next privileged record is strictly paired with the corresponding observation and history, and the true value of the new round after reset is not spliced; the future random incentive plan is only saved as the generation log. The above new working conditions and data paths belong to the design to be implemented, not the training results obtained this time.

# 4. Input and Sources of Information for B, F, Actor

### 4.1 Asymmetric interface: Actor reads the available information, and F reads the randomized truth value

Confirm to use:

\[
x_t^P=(g_t^P,k_{\mathrm{rigid}},k_{\mathrm{drive}},h_t),\qquad
y_t=(x_t^P,p_t),
\]
\[
e_t=B(g_t^P),\qquad
u_t=\pi(x_t^P,z),\qquad F_i(y_t,u_t,z),\quad i=1,2.
\]

x is the input context of the Actor, and the superscript P continues to remind you that the actual torque in the first round should be the simulation-accurate value, which does not mean that the Actor contains all the true values ​​of the environment. p is a randomized physical parameter and the current loading, boundary, and driving truth values ​​only for training F; y combines the two to retain the historical context of the same Actor; F-specific p also contains feature_memory, which clearly distinguishes additional memory and hidden physical truth values.

| Field Group | Content and Source | B | Actor | Training F |
|---|---|---|---|---|
| g | Length, limit, q/dq/τₘ, terminal relative velocity, angular/terminal relative acceleration estimation and effective bits | Read | Read | Read |
| k_rigid | Known quality, centroid, centroid inertia and mounting conventions for both rods; URDF/CAD/calibration can be provided, the first round accurate declaration group uses an accurate model, the error group uses a nominal declaration | Do not read | Read the declaration model, there is a source and validity | Read the same declaration model; p Provide the actual value |
| k_drive | Known request scale, configured output limit; friction, damping, reflected inertia and drive response parameters with configuration or calibration basis | Do not read | Read the declared value | Read the same declared value; p Also provide the actual value |
| h | As of the current q/dq/tau/issued u, time interval or age, padding | does not receive the original sequence; acceleration has used partial information | read, supports local dynamic adaptation | read, used to predict subsequent behavior of the same historical actor |
| Randomized physics parameters in p | Actual mass distribution, inertia, friction/damping, drive parameters, support/object/adjacency model parameters | Do not read | Do not read undeclared true values ​​| Read the values ​​actually in effect in this physics |
| Dynamic loads and boundaries in p | Actual loading, contact points/forces, connection loads, support/adjacent motions and current control states, necessary gravity projections and body common motions | Not read | Not read | Read current true values, recorded by source and reference frame |
The original 22 boundary, time/validity, inter-area fraction and sample phase required for the rollover of the feature_memory  feature device in p., including uncompleted semi-window accumulations, if necessary  no reading  no increase in the current x frame number  reading; Compressed x does not guarantee that the next feature can be extrapolated
| Driver internal state in p | True delay queue, response status, current effective capacity, etc. | Do not read | Do not read undisclosed internal state | Read current true value |

k_rigid only provides declarative models of two adjacent rigid bodies, and does not simply add the entire mass of the entire machine to one side. Fixed attachments incorporate inertia into the known assembly model; this cannot be done through a body with articulated joints. The reference points/coordinates of the center of mass and inertia must be unambiguous and the required M-frame expressions inputted by the mounting and q transformations. The missing inertia parameter cannot be disguised as zero mass/zero inertia; nor is the upper limit of the effort of the URDF equal to the actual available moment under all operating conditions.

The first round allows for "accurate model parameters" but cannot be called pure sensor observations. If the model is not punctual, Actor obtains compensation clues from history, and F obtains actual conditions from p; this solution does not add a new load regression loss, nor does it automatically name the Actor's historical characteristics as accurate load estimates. F Just because a payload is known, does not mean that the Actor can predict it if the telemetry is not yet responsive.

Known installation/support data or adjacency telemetry shared by future upper layers can be used as explicitly declared actor extension interfaces; training case numbers are not considered a replacement for this information. Other robots may have force sensors, IMUs, or full-body observers, which the current actor does not yet rely on. The spatial privileged quantity of F is still uniformly expressed as M, and the unified coordinates do not change its privileged attributes.

### 4.2 Explicit calculation of acceleration, history is still used for dynamic adaptation

Keep the established historical scale: 50 Hz×10 slow record, q/dq takes the endpoint, u/τₘ takes the completed interval summary; the original sequence saves the endpoint, sub-step integral, interval duration and valid bits separately, and the endpoint mean cannot be used to replace the integral; 100 Hz×8 fast drive record. The slow endpoint spans 180 ms and the summary is about 200 ms; 8 consecutive fast endpoints span 70 ms. If eight completed 10 ms intervals are recorded, the coverage is 80 ms. The field must be clear whether it is an endpoint or an interval summary, and the time meanings of the two cannot be mixed.

Acceleration reuses the original 100 Hz velocity cache, and the base estimator first takes the slope of a straight line fit over the last 5 valid velocity endpoints and real timestamps, covering 40 ms. This is a configurable starting point: smoother than the difference between two adjacent frames, it will also smooth out short transients; under uniform sampling, it reflects the response within the window, and the changing acceleration may show about half a window lag, which cannot be called a delay-free instantaneous true value. Check the estimation error, response lag and control effects before adjusting the window. Do not expand the network history to 128 frames or introduce GRU accordingly.

The order of controlling bound t must be: **Read telemetry up to t → Update causal estimate with h → Construct g_t/x_t → Actor produces u_t → Simulation advance → Get next bound data. ** The sent request in h ends with the action actually sent before; F additionally receives the u_t currently to be evaluated. The simulation qacc obtained after the current action cannot backfill the current g_t, otherwise future information leakage will occur.

The same estimation implementation is used for rule collection, online training, Replay reconstruction, goal/reference samples and evaluation. Centered differences, two-way smoothing, or future velocities must not be used offline and causal estimates online. History is reinitialized after reset/snapshot restart; when there are less than 5 valid endpoints, b_acc=0, acceleration-related fields use conventional placeholders, and padding cannot be interpreted as static. After missing testing, b_acc=1 will be restored only if the valid window conditions are met. The complete goal gives priority to real samples with b_acc=1; invalid frames can still be retained as real transitions, and one-step transition cannot be forged across them.

Velocity, angular acceleration, and terminal acceleration are fixed and versioned in units/normalization; the physical amplitude is not normalized by the current maximum per round. When the estimator version changes, rebuild the entire set of data features and reference pools, and do not mix old codes with different semantics. The simulated instantaneous acceleration is only used as a control, and is compared according to the corresponding time window; it does not secretly substitute the estimated value into B.

Angular acceleration provides unambiguous recent response; history also includes previous requests, output, response delays, and ongoing changes. The two cannot completely replace each other. Whether the current history of about 0.2 s is enough to cope with the specific connection load remains to be verified: first distinguish between indiscernibility, noise/delay and insufficient memory, and then decide whether to change the historical sampling or add upper-layer known information. Do not default that a longer history can solve everything.

### 4.3 F Which true values ​​are read and how to enter training

**Training F to directly read the true value of the randomized load is the solution determined in this round. ** These inputs are used to explain "why the same local observation and action produce different consequences" and do not require F to first re-identify the loads that the simulation already knows from the Actor's limited history.

| Privileged Content | Actual Information Provided to F | Time and Physical Implications |
|---|---|---|
| Randomized inertia and loaded objects | The actual mass, center of mass, inertia, installation and connection relationships; adjacent/object dynamic parameters participating in the coupling | Distinguish rigid body parameters from the dynamic effects of the whole machine; do not pretend that the sum of adjacent masses is used as the equivalent inertia of a joint |
| Explicit external load | The effective force side, action point, force vector, additional force couple, and the current reference/phase or internal state of the loader | Force/moment is expressed in M ​​and the reference point is marked; only the actual applied amount is recorded, and the current value is not replaced by a randomization range |
 Exposure and binding payload  Actual contact point, exposure, connection/package binding reaction; The contact force is generated by the solver and cannot be considered as having achieved the desired contact strength; Need for status to explain subsequent exposure changes
| Support and adjacency coupling | Current support motion and internal state, adjacency q/dq, drive/control state, necessary gravity projection in M ​​and shell common motion | Distinguish between different subsequent couplings under the same instantaneous resultant force; do not add these sensing assumptions to B or Actor |
| Randomize drive and joint response | Actual friction/damping, reflected inertia, capacity, delay, response parameters and internal queue/state | Distinguish between u→torque and torque→motion, not combined with external load into a sourceless scalar |

Maintain sources, action points, reference points, and valid markers for multiple source roles; avoid double counting the same role when aggregation is required. The relative velocity of the support/object shall be distinguished from the coordinate change rate of the system, and the common angular velocity of the shell shall be recorded separately. A total load torque is not a complete simulation state and cannot replace the relevant dynamics, boundary and drive information.

The training records the current p_t and the next p_{t+1}, which are aligned with x_t and x_{t+1} respectively. The existing force and loader state of the control boundary can be entered into the current F; the contact reaction force obtained after applying u_t belongs to subsequent transfer and cannot be backfilled into the state field of the current F. When the solver only provides reaction forces from the last completed interval, it retains its timestamp/interval meaning and also provides the current geometry and velocity. Random perturbation sequences that are pre-generated but have not yet taken effect are not used as current input.

Bellman's successor uses the same Actor that does not read the true value of the payload:

\[
u'=\pi(x_{t+1}^P,z),\qquad
F_{\mathrm{target}}\bigl((x_{t+1}^P,p_{t+1}),u',z\bigr).
\]

Actor uses \(\pi(x_t^P,z)\) to generate actions, and then obtains training signals through \(F_i((x_t^P,p_t),\pi(x_t^P,z),z)^\top z\); p only enters the forward direction of F and cannot be mixed into the Actor input through shared feature assembly or encoder. F retains the history in x because the future execution is of the Actor with that history, rather than another strategy that chooses an action directly based on p.

**The deployment unit only calls Actor and B, not privilege F. ** Therefore, the deployment does not need to provide p, and there is no problem of filling F with zero by default; the upper layer calls the Actor through z, and observes the effect and capability conditions through B, basic physical feedback and the statement known_model/known_drive; these known parameters do not need to be detoured to B16. The precise motor torque of the first round is still an established ideal condition. "Actor does not read the true value" here specifically refers to not reading the additional dynamic load/boundary/drive internal true value and not erasing the marked motor torque privileges.

# # 4.4 Check the division of labor between B, F and the upper level with the corresponding examples

Same geometry, limit, q/dq/τα, different inertia: If there is an acceleration response, the estimated acceleration may be different, and B has the opportunity to distinguish; if it is just about to start, the history is static, or the external load just compensates for the inertia difference, all g may still be the same, and B must be the same. The actor can use the known link inertia to distinguish some conditions, but the dynamic load of the whole machine cannot be obtained only from the parameters of the two rods; F additionally reads the actual load and the coupling true value of the operating condition.

The same known model, different unknown external loads: F can be distinguished according to p, and the Actor adjusts according to the historical response that has appeared. If the model, current observation and history of the Actor are also exactly the same, it cannot select different actions in the same z because of different hidden loads; the additional information of the training F will not become the online sensing of the Actor. The upper layer needs to retain the structure and task context, but does not require it to take over all local dynamics identification. It can read known parameters, basic physical feedback and e = B (g), and combine past z, call duration and actual response to judge the execution effect; only history z is not enough to identify the load.

This round B encodes the local configuration—motion—output—recent response, F uses actual load conditions to train subsequent predictions, and the Actor uses available models and history to organize execution. If the upper layer requires independent load estimation or capacity feedback, the source and verification must be separately defined, and unverified historical characteristics cannot be called estimated physical quantities.

## 5. Synchronous adjustment of the training and calling range of FB and z

The goal of FB is still the discounted number of visits of subsequent g when π_z continues to be executed after the current action. g contains causal acceleration estimates; Actor uses x and training F uses y=(x,p):

\[
M^{\pi_z}(y,u,dg^P)
\approx F(y,u,z)^\top B(g^P)\rho(dg^P),\qquad
\widetilde z_r=\mathbb E_{\rho}[r(g^P)B(g^P)].
\]

Preserve the FB Bellman target, B orthogonal regularization and Actor maximized double F in the smaller Fκz; the real next g provides the direct term, and the current Actor and target F/B constitute the successor term. No additional mission rewards or ancillary losses due to new fields. The B input determines what it is based on, and the joint training and data distribution determines the final retention and control. FB rationale (citation link removed)

Privileged inputs to F are used to reduce hidden conditional aliasing in subsequent predictions. Bellman's required state sufficiency is examined for y=(x,p): p needs to contain the current evolution conditions of the corresponding environment/driver, x retains the compressed history available to the Actor, and F supplements the estimator/history update memory; one cannot claim a complete Markov state just by adding a load scalar. The Actor still uses a restricted F-specific feature_memory supplements the original window/integration/sampling phase required for feature recursion, and cannot claim complete Markov simply because x has a compression history. These information bounds do not change the established asymmetric training scheme and do not increase task rewards or load estimation losses.

The physical preferences of this round can rely on q, dq, τₘ, v_tipᴹ, effective acceleration estimates and currently known geometry/limits, such as holding, rotation, acceleration and deceleration response, torque and joint compliance relationships. When only checking the speed/torque, the irrelevant acceleration conditions should be integrated according to the reference distribution instead of randomly adding an acceleration to complete the goal. Queries that rely on acceleration handle b_acc explicitly; invalid placeholders cannot be treated as "acceleration zero" targets.

The end velocity target must be located in the feasible tangential direction of the current joint, the end relative acceleration must meet the same kinematic relationship of q/dq/angular acceleration, and the spatial vector cannot be specified arbitrarily. Limited travel cannot permanently maintain non-zero velocity, let alone non-zero angular acceleration; transient acceleration targets need to combine call duration with subsequent braking judgment.

The contact force is not a function of this version of g. You cannot just rely on F to read the true value of the contact and apply the above query formula to obtain a universal specified contact force command. If you want to query the contact force directly in the future, you need to expand the result definition or demonstrate the control mechanism separately; this round first verifies the motion, driving torque adjustment and feedback control under different loads.

The full-state goal adopts the consistent q/dq/τα generated by the current length/limit and true continuous fragments, relative velocity and acceleration estimation; it is not possible to splice an acceleration independently or fill the old sample with zero by default. It describes the result with a recent response, not a static point that must be reached under instantaneous torque, nor can it require the unit to reach another set of structural configurations. Refer to the distribution and query synchronization definition; after resampling/conditionalization, the old integral cache cannot be directly used. Replay saves the physical data, uses the current B code, and freezes the use of the supporting Actor/B; the old semantic z cannot be fixed for a long time.

e = B (g) Feeds back the current state and z expresses subsequent preferences. The z-norm is not the magnitude of the force applied and the distance between B and z is not the error of arrival. Maintenance, compliance, reciprocation, etc. need to be verified during the true persistence and perturbation process; covering some transient states does not automatically guarantee the correct frequency, phase or timing.

The upper layer coordinates the units according to tasks and structures, reads known parameters, basic physical feedback and e, and maintains a call and response history. The base programme does not provide dynamic load realities to the upper layer; If a separate, exclusive, privileged comparison must be made, its proceeds cannot be attributed to B or historical estimates. History context is not an unverified parameter estimate, History and Information Status Conditions  already needs to be checked during this round. The upper tier uses the same information, driver limits and timescale baseline comparisons.

## 6. The gap between the current V2 and the new solution

| New protocol decision | Current V2 | Required changes or evidence boundaries |
|---|---|---|
| Fixed shell P/output D side sequence and this system M | Model tree P/D convention; existing world motion observation | Verify side sequence and installation mapping when accessing, do not exchange according to instantaneous steering |
| B input length, q/dq/τₘ, limit, relative speed and causal angle/end relative acceleration | g23 no length; including world attitude/COM speed, contact and environmental resultant force; B output 16 dimensions | g, training data and network input need to be redefined, not directly compatible with old weights |
| Terminal velocities/accelerations from relative kinematics | These fields are not currently exported; world COM motion is not an alternative | Calculated with axis/mount, q/dq and causal angular acceleration estimates; sync valid, estimator, Replay and query versions |
| B's limit comes from a known configuration | m28 has an upper and lower limit, o24/B has a derived distance, but always ± 1.2 rad | Training is required to change the stroke, clarify the type/significant bit and legal collision range |
| Actor uses g, known model/driver configuration and causal history; train F and then read p |
 Random loads, kinetics and boundary truths are determined to enter the training F  per round world Fx/Fz/My Mixed Outload, R1 Support to external contact R Record the current/next p by source and send it to F/target F; The next action is still made by an unread p-based Actor, and the deployment is maintained Actor/ B
| Rule Data Overrides Local Motion — Output and Loading Process | P0 Has Hold/Speed/Brake/Compliance/Noise, raw Unprefilled Online Replay | Transfer Subbanks as per Section 3 Retention Rules, Train and Audit Usage Ratio with Online Transfer |
| Adjacent action and contact occur simultaneously | R2 has grounding but no adjacent drive, R3 has adjacent drive but no ground | New combined working conditions and legal bilaterally constrained processes; cannot be replaced by independent working conditions |
| Randomization, persistence process and data scheduling configuration | V2 fixed limits, 5 s rounds, short/long command mix; sampling not stratified by joint status | Section 3 defines candidate range, initial quota, stage timeout and 10 s round starting point, not yet implemented |
| Cover joint status and continuous process | Replay samples by role/turn/transfer, focusing on near-limit frames | Audit length×q×dq×τₘ×limit and acceleration response, load recovery, not just single variable range |
| Plane prior is not equal to any three-dimensional coverage | R0–R3 full plane, fixed gravity, P/D random range asymmetry | Spatial expansion is for loads and couplings and cannot be replaced by adding velocity fields |
 Actual call capacity needs to be independently validated to P3, Valaided=file; Four units are fully connected, and access does not mean walking or learning speed, and new inputs do not automatically fix old failures.

In the saved audit, about 33%–71% of the frames of each role of Replay are finally retained to satisfy |q|>1.1 rad; the nominal R0 of −1.0/−1.2 keeps the end of the query at about −0.56/−0.60, while other z can exceed −0.6. Visits and reliable calls are still two types of evidence, and the cause has not yet been isolated. These are facts of the old V2, not new scheme results.

in accordance with:

- Information and network: [schema.py](../schema.py), [networks.py](../networks.py), [history.py](../history.py), [interface.py](../interface.py).
- Physics and sampling: [mechanics.py](../mechanics.py), [environment.py](../environment.py), [kernels.py](../kernels.py), [bootstrap.py](../bootstrap.py), [replay.py](../replay.py).
- Training and query: [train.py](../train.py), [learner.py](../learner.py), [fb_loss.py](../fb_loss.py), [tasks.py](../tasks.py).
- Actual test records: [covering audit ](../artifacts/state_coverage_audit/20261001_v2_motion_coverage.json), [training status ](../artifacts/rf_v2_full/status.json). [Old State and 3D Discussion ](Unit State and 3D Randomization.md) retains historical review and data evidence, where a wider body movement/load characterization target does not represent the B interface identified this time.

## 7. Implement constraints after auditing

This logical document gives the characterization and information boundaries. The specific randomization/acquisition/field specifications are based on [revised V3 protocol ](V3 Network and Training Plan.md): independent collision pair inspection, fixed side mapping, extraction and calibration of connection reactions by source, time pairing before and after action, F feature update memory, true interval integration, rule ability calibration, conditional coverage and true E4 activity criteria, Replay sampling probability, line-by-line termination discount. weld extraction Disable relevant templates before not passing physical balance calibration, cannot be filled with zero privileges or refer to compliant clamping as rigid closed chain covered.

The global ρ/z16 remains unchanged. The exact global successor density of an invariant configuration is bounded by low rank, subject to intra-configuration dynamics versus actual call acceptance; the theoretical bound is not a control failure rate. Document revisions are not marked as project complete without V3 implementation, coverage, GPU, and training results.
