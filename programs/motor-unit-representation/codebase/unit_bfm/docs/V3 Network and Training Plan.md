# V3 Network and Training Implementation: Local Response Representation, Privileged F and Combined Randomization

Revised date: 2026-10-10. (a) The definitive amendment of [cross-audit ](V3 Plan Cross Audit.md) has been incorporated; The simulation and collection items that are not accepted in the text remain the implementation threshold. Status: ** Implement design, V3 code not yet prepared or V3 training initiated.**

Designed on the basis of [the reverse combusture of the electron-based sensor. ](Motor Proprioception and Representation.md) This paper translates the identified information boundaries into data compacts, networks, simulations, sampling and training changes; [The original training project achieves the design ](Training Engineering Design.md) and the current code belongs to V2 and does not cover this V3 decision. The new version of the identifier is proposed as LOCAL_RESPONSE_ASYM_FB_V3, the code is placed in a stand-alone unit_bfm/v3/, data, weights and logs are saved independently and V2 is not covered.

* * Main chain: → unified extraction of system results and causal history → rules by physically generating local movements and loading processes together with online transfer into Replay → F Read true randomization condition training FB, Actor read-only available information → freeze Actor/B check call ability. * *

## 1. Determined scope and implementation principles

- The single execution unit is still one motor and two connecting rods P/D; housing_link (P) is fixed to the motor housing, output_link (D) is connected to the output shaft/flange, and the side sequence does not change with the steering direction; P/D is only an alias for the old field, and does not represent the near end/far end of the robot. When equipped with a reducer, the output side is not equal to the rotor side. The first round uses sagittal plane dynamics, and the interface space quantity uses the motor body system M.
- **This round determines the status representation of the learning results. ** B describes relative configuration, velocity, actual shaft moment and near-term acceleration response, using first wheel g13. Motor dynamics parameters such as capacity, response time, delay, friction, and armature are used for randomization and control conditions. They are not directly inserted into B, nor are motor models or hidden parameters set as supervision targets for z. The geometry/limits are still retained according to the existing result definition; B does not read the true value of the unknown load and does not read the original history directly.
- Actor reads g, known local model/driver configuration and causal history. **Training F also reads the randomized load and related dynamics, drive and boundary truth values ​​that actually take effect this time. This is the final solution. **
- Inherit V2's feedforward skeleton, 16-dimensional z, FB Bellman loss, B orthogonal terms, and Actor targets; no additions to task rewards, imitation losses, loaded regression losses, or GRU.
- Deployment calls Actor/B; F only for training and simulation diagnostics with emulation values. The first wheel axle torque still uses the simulation exact value and is marked as a privilege, and does not claim to complete the real machine adaptation.
- “Adequate randomization” requires that data for parameters, combinations of working conditions, continuous processes, actual visits, and entry gradients are examined; evidence cannot be replaced with a wide range of parameters, a large number of models, or a fully trained budget.
- This round does not train body balance. The existing four-joint biped access code is not equivalent to the originally proposed two-motor biped, which has been verified. The subsequent ontology and upper-level tasks will be clarified separately.

## 2. Current code review: what should be retained and what must be changed

The following is a factual review of this code, not an inference of the effect of the new protocol.

| Links | V2 Actual Implementation | V3 Must Implement Changes |
|---|---|---|
| B input | [networks.py] (../networks.py) deletes u from o24 to g23; no length, including world posture/COM speed and environment | Explicitly constructs the system g13, not sliced according to the old column number |
| Actor/F input | Actor and double F both use x336, and the input dimensions are hard-coded | Actor uses x137, F uses [x137,p]; the constructor takes the dimension from the schema |
| History | [history.py](../history.py) History includes world motion, contact and external forces | Only assembly allows motor telemetry, unified calculation of causal acceleration |
| Geometry library | [mechanics.py](../mechanics.py) 32 models per character, first 8 narrow ranges; P length .15–.4 m, D .25–.45 m, different mass ranges | Symmetrically layered on both sides, cross length, mass distribution, stroke and fixed side |
| Limits | XML, nominal, observation, rule control and query multiple write dead ± 1.2 | Geometric legitimate travel + random control limits as the only source |
| Environment combination | R0 fixed P; R1 elastic floating support; R2 floating ground; R3 two adjacent joints but no ground | Fixed P/D are available; contact, loading, support, and adjacency can be combined |
| Contact collection | environment._physics Accumulate contact only in role==2 | All working conditions that turn on contact are executed, especially adjacency + contact |
| Adjacency parameters | Peripheral length/mass fixed; PD gain 8/.5, upper limit 3.6 N·m fixed, mainly random sinusoidal reference | Peripheral structure, reference process, control gain and drive capability co-vary |
| Loading process | 16 .1–.5 s pulses, .5–2 s intervals, action point only .2–.8 L | Loading during lengthening, obstacles, release recovery, near the rod end and in different directions |
| Parameter writing | Set_const after changing mass/inertia, damping, friction, armature, geom_friction in each world, the driver has another queue | Keep the real physical path, add readback, combined model compilation and p export |
| True value visibility | m28 is the nominal model, the round multiplier/real queue, etc. are not completely given to F | F reads the actual value; Actor only reads the declared model and history |
| P0 data | [bootstrap.py](../bootstrap.py) saves raw; [train.py](../train.py) only takes reference and does not prefill raw. Bellman Replay | The rule sequence becomes a reserved sub-library and participates in transfer training |
| Rule reference | [tasks.py](../tasks.py) maintains ±.8, adapts to ±.6; the rule controller still uses ±1.2 | Reference is generated with the current trip, adding explicit loading/recovery phases |
 Replay  [replay.py ](../replay.py) fixes four roles, first opting for episode and then choosing the time; No p/p_next Double Source Sequence Library, Layer Transfer Sampling, Current/Next Privileged Match
| z | learner.sample_z arbitrarily disrupt the goals of this batch; collect goal unmatched structures | complete goal matching geometry/limit, current B encoding; ρ is defined separately |
| Discounts and updates | Fixed scalar γ=.99; training loop hardcoded /256, updates_per_W configuration not used for this expression | Terminate discounts row by row, update rate read from configuration |
| Evaluation web page | [parameters.py](../eval_web/parameters.py) The model limits/parameters can be changed, and training is still in the old range | Read the range/version from the V3 manifest, distinguish the evaluation changeable and training coverage |

V2 save status is P3, 20,032,000 W, 77,218 updates, validated=false. Near limit accumulation and retention failure, please refer to [Coverage Audit] (../artifacts/state_coverage_audit/20261001_v2_motion_coverage.json). There is no evidence that a single factor is the old root cause of failure.

## 3. Data contract: Actor, B and F are assembled separately

### 3.1 Two-level records and unified coordinates

The physical raw records use SI units and are not divided in advance by old constants such as 1.2/6 in the kernel; the unified featurer is responsible for normalization.

- actor_record: q, dq, tau_endpoint, and previously issued u after unified coordinates; each completed control interval saves tau_integral, u_integral, dt, interval_valid independently; saves the timestamp/valid bit and declaration model. The original hardware/simulation tree coordinates and calibration mapping are left for traceability and are not directly assigned to the network.
- privileged_record: actual parameters, current physical/driver/boundary status, force and time aperture, only for F and audit.
- metadata: structure, round, stage, source, random flow and future generation log, not automatically spliced ​​into the network.

The origin of M is at the center of the joint under study, the shaft is fixed to the shell and +z is along the side rod of the shell in the direction away from the joint; below, q uniformly refers to the calibrated mechanical angle q_c. When q_c=0, the endpoint of P is at +zᴹ and D is at −zᴹ. The original encoder qpos=0 is not required to correspond to this pose. The model_adapter manages the simulation tree coordinates/axis/ref, and the telemetry_adapter manages the original encoder on the output side. The two layers are recorded separately and connected through q_c. The tree is not inverted when the hardware direction changes and the reverse sign is repeated. The mapping of the model tree to P/D simultaneously converts the q/dq/u/torque/limit signs; fixed D does not swap side orders either. qposadr and dofadr are mapped separately, and the old planar model's assumption that they are exactly equal cannot be used.

#### 3.1.1 Zero position and direction are coordinate contracts that must be implemented

First change the sensor reading to output side rad, and then define `q_c=s*q_e+beta`, `dq_c=s*dq_e`, `tau_c=s*tau_e`, s∈{−1,+1}. beta is the known mechanical configuration angle when q_e=0; the zero position of q_c is the linear expansion of the two rods. Encoder calibration and flange mounting offset can be combined into this beta, but the original calibration/mounting sources are retained separately. The output side request is `tau_req,c=S*u_c`, and the adapter sends `tau_req,e=s*tau_req,c`; only when the original interface also uses the symmetry scale S, it can be abbreviated as `u_e=s*u_c`, keeping tau_c*dq_c=tau_e*dq_e; do not add beta to the speed or torque. The upper and lower original angle limits are sorted by s*q+beta; the upper and lower torque limits are sorted by s*tau. All history, rule references, goals, feedback and queries use q_c, one conversion, no frame-by-frame wrap across cuts.

coordinate_map saves `axis_sign`, `canonical_angle_at_encoder_zero_rad`, output side units, calibration_valid/source/version, mechanical installation/tree mapping. When there is no trusted calibration, the first-round interface refuses to claim that the geometric feedback is valid; acc_valid cannot replace the calibration valid bit. Angle and moment respectively register the measurement side, unit and source. If the angle comes from the rotor, it is converted into the output side angle according to the transmission model; the existing output shaft torque telemetry only performs unit/direction conversion, and does not multiply the gear ratio on the rotor side due to the encoder. Rotor torque or current estimation requires a clear transmission/loss model and does not pretend to be a precise output torque; formulas with only signs cannot be applied to gear ratios. If the normalized scale of the device is S_e, then u_e=s*(S/S_e)*u_c; if S_e=S is declared in the first round, the device range is insufficient and should be reported as limited, and it cannot be implicitly trimmed and still be called equivalent. The u of Actor output, history, Replay, and F are all u_c, and the original u_e only remains for traceability. There is no hysteresis/flexible transmission in the first wheel, and the output side model does not claim to have simulated any reducer.

q_e=0, different betas should have different physical postures; the same q_c, different beta/s are just different coordinate expressions, and the converted g/x and physical requirements should be consistent. M is not redefined according to the direction of the unknown world. The first-round single-axis planar straight rod installation can be expressed by beta and fixed coordinate transformation; eccentric rod ends, non-coplanar axes, and complex connecting rod shapes require expanded geometric schema and cannot be disguised as a zero deviation.

# # g13 for 3.2 B

The first round only supports known limited travel, and the type and limit existence are fixed by the schema; periodic/multi-turn models require new version coding.

| Index | Field | Dimension | Source |
|---|---|---:|---|
| 0–1 | L_P, L_D | 2 | Declaration Geometry |
| 2–4 | q, dq, τ_m | 3 | Current joint motions and axis moments; precise moments are still a first-round privilege |
| 5–6 | q_min, q_max | 2 | Known configurations |
| 7–8 | v_tip, x/z of Dᴹ | 2 | Current q/dq and geometry |
| 9 | ddq_hat | 1 | Causal Velocity Window Estimate |
| 10–11 | a_tip, x/z | 2 | same q/dq/ddq_hat with geometry |
| 12 | acc_valid | 1 | Valid window flag |

\[
v_D^M=(-L_D\cos q\,\dot q,\ L_D\sin q\,\dot q),
\]
\[
\widehat a_D^M=(L_D\sin q\,\dot q^2-L_D\cos q\,\widehat{\ddot q},
L_D\cos q\,\dot q^2+L_D\sin q\,\widehat{\ddot q}).
\]

This is the coordinate change rate and the second-order change rate relative to M, not the motion of the inertial system. The endpoint of P does not move in M ​​and does not complement a set of constant zero features. Acceleration cannot be randomly filled in independently.

#### The motor dynamics parameters do not directly enter the result characterization of this round.

The first round B is still g13, and q/dq/tau are absolute physical quantities under unified mechanical coordinates. The criterion is "whether the same g still needs to be scored differently by the result preference", not "static parameters cannot enter B". Length/limits are retained to describe geometry, linear motion and travel; calibrated beta/s does not re-enter B after signature conversion. Declare the mass/inertia, capacity, T, delay, damping, etc. that mainly affect the method to achieve the same result, give the Actor and the upper layer, F reads the actual value, and does not increase to g in this round. Motor randomization will still change g through true motion, output, and near-term response, and "no direct input parameters" cannot be misinterpreted as requiring B to be invariant to all dynamics changes.

Example: The same tau = 2 N · m, the capacity 3 and 6 N · m B can be the same; the upper layer obtains different ability configurations through known_drive, and you can't just judge the margin by B16. When the current motor wants to semi-declare the capacity, the caller first calculates the fixed physical target tau * = .5 * C_decl, and then queries according to the absolute torque r (g), without changing the global ρ. Cross-reference samples are not a function of the existing g13 according to their respective tau/C scores, and the result definition needs to be expanded separately; the sample capacity is not read in the query code instead of the theoretical modification.

The stated margin is a configuration reference, not a guaranteed net force/acceleration. In the future, when kinetic energy, capacity utilization per sample, or measured saturation state are clearly required as results, the corresponding B fields and sensing sources will be discussed; adding parameters to B does not guarantee FB lossless encoding. The first round does not require z to serve as both a motor model label and a capability estimate.

### 3.3 Actor x137

\[
x=[g_{13},k_{\mathrm{rigid},16},k_{\mathrm{drive},16},
h_{\mathrm{slow},60},h_{\mathrm{fast},32}].
\]

 Group  Accurate Fields  Dimensions
|---|---|---:|
| k_rigid | In P/D order, each rod has mass, COM_x, COM_z, I_yy, a total of 8 values ​​+ 8 valid bits | 16 |
| k_drive | Requested torque scale, declared output lower/upper limit, T, delay, damping, friction, armature, 8 values ​​+ 8 valid bits | 16 |
| h_slow | 10 items each q_endpoint, dq_endpoint, tau_interval_mean, u_interval_mean, padding, age | 60 |
| h_fast | 8 items, each u_previous, tau_endpoint, padding, age | 32 |

Planar model uses mass, planar centroid and I_yy; original URDF full tensor preserved, extracted by mounting transformation, file axes cannot be assumed to be the same as M. The relative study joint expression of the center of mass, I_yy is around the center of mass of the rod. The effective digit of a missing parameter is zero, and no zero value is used to pretend to be known.

The declared parameters in the first round can be accurately equal to the actual values; the model error group fixes the declared values ​​and changes the physical values. Actor does not read role ID, contact force, hidden magnification, future loading schedule or drive internal queue. Dynamic privilege amounts are mixed into actor paths without shared normalization statistics or encoders.

Continuous quantities are normalized to a fixed schema scale. First round candidates: length .4 m, angle/limit π rad, dq 6 rad/s, moment 6 N·m, terminal velocity 3 m/s, angular acceleration 200 rad/s², terminal acceleration 100 m/s². This is a numerical scale, not a physical limiter; by default, observations are not hard-cut, and superscale and non-finite quantities are recorded. If the scale is adjusted after P0, freeze the version before the first optimization and re-extract the data without normalizing by the round maximum value.

### 3.4 Causal History and Acceleration

Control 100 Hz, Phys/Drive 1 kHz. Cache at least 22 original boundaries for reconstructing the current and next features. Acceleration takes the last 5 real speed endpoints and performs straight line fitting with real timestamps, with a span of 40 ms; when the acceleration changes linearly, it is equivalent to a recent response with a lag of about 20 ms, and is not called the current instantaneous true value; when the window is insufficient, acc_valid=0, and the angular/terminal acceleration uses placeholders. Effective zero acceleration is not to be confused with missing history zero.

The slow history is updated every 20 ms: q/dq takes the endpoint, and u/tau is the summary of the previous two complete 10 ms intervals. The tau interval mean is obtained from the real integral of the physical substep, and the slow summary is the sum of the two interval integrals divided by the sum of the two dt; the same goes for u. Both the endpoint and the integral are required fields for the original sequence. There is no need to pretend to be the endpoint mean, and the integral cannot be remade from the old raw. Odd control steps retain the nearest even boundary and recalculate age. The 10 endpoints span 180 ms and the summary covers approximately 200 ms.

Fast history u_previous is the interval request that has just been completed, and tau_endpoint is its end moment. The 8 endpoints span 70 ms, and the related execution interval is 80 ms in total. The interval before reset must be padded. Changing z will make the history unclear.

All paths use the same feature. Acceleration only reads the data up to t; offline centering filtering is not allowed, and simulation qacc and next step force are not allowed to backfill the current g. Rule collection, online Actor, Replay, goal, and evaluation all save the estimator version.

# # 3.5 F privileged p and dimension management

F input y=[x,p]; p uses the actual effective quantity.

| Field Blocks | Contents | Storage and Sources |
|---|---|---|
| feature_memory | The original 22 boundaries q/dq/tau_endpoint/u_previous required for feature recursion, each interval tau/u integral and dt/effective bit, time age, slow sampling phase | F dedicated additional memory, not hiding the physical truth value; expanded in time order, the scale is consistent with the Actor feature |
| actual_rigid | P/D, adjacent body, mass of support/object, COM/I, shape, mounting/connection, real joint parameters | model/round constant once; M-series expression reconstructed according to current configuration |
| actual_drive | Actual capacity, T, delay, τ, time-ordered 11-slot 1 ms delay queue, same for adjacent drives | control boundary true; ring index not equal to time order |
 baseary_state  support/object relative to M position/motion, adjacent to q/dq and current state of control, necessary public motion and gravity projection  current real value; Distinguishing speed differentials from M-coordinate rate
| applied_load | Force side, point of action, force/force couple, loader currently active reference/phase/state | Source single column, coordinate and torque reference points unified |
| contact_state | Object/Local Geometry, Actual Contact Point/Normal/Force, Slip, Friction/Softness and Effective Marking | Current Geometry + Recently Completed Solved Interval Function and Timestamp |
 connection_load  backlash/crack, reference point and source for supporting or adjacent connections  restraining/gone subject to decomposition and proofing, not impersonating qfrc_applied

Do not provide F with just a random range, an initial value, or a mixed resultant force. The inertia, point of action and boundaries may be different for the same resultant force. The current deterministic program status of the loader is readable, but independent random events/future random numbers that have not yet taken effect are not readable.

p is generated from a field registry with name, unit, coordinate and time semantics. The first round of templates limits a maximum of two adjacent active joints, two sets of external supports, two external objects, and four explicit loaders; other connections require new templates/schema. Variable objects use fixed slots + present mask, and each template declares the slot identity. The contact capacity is configured according to the most complex model; overflow reporting and expansion and re-extraction are performed without silent truncation.

* * D_p is generated by the fields and sets of all templates after the model is compiled and frozen before starting. * * Do not write unverified values as final dimensions; all models output the same ordered schema, F reads dimensions from manifest. See Section 4 for the number of network parameters. Save the full physical state as a reproduction snapshot, and do not put the original world coordinates directly into the network.

feature_memory is assembled at the control boundary and only needs to save the integral of the latest complete interval; if the internal accumulation is based on 20 ms rather than reconstructed from the interval record, the unfinished half-window accumulator must also be saved. Slow sampling of x137 with a fitted slope is generally not sufficient to recurse to the next x/g, and Replay can reconstruct information not equal to F that has been received in the recursion. F inputs complementary memory, Actor/B does not add the original frame number, and does not add RNN. By passing feature update closure checks first and then reviewing external process states, one cannot claim that these fields automatically guarantee full Markovness.

##3.6 Specific path for the extraction of privileges and the receiving and inspection threshold

Local MuJoCo/mujoco-warp 3.8.1 has a post-constraint API: CPU `mj_rnePostConstraint`, Warp `rne_postconstraint`; it can also be triggered when there is a corresponding force/torque sensor, you must confirm that the sensor is on. The constraint reaction has been updated after there is no guarantee in the ordinary forward/field, and the formal collection incorporates the call and copy into the same solution pipeline.

| Sources | Extraction and Transformation | Not Allowed Substitutions |
|---|---|---|
| motor output | project driver state tau; prototype written via qfrc_applied | not read fictitious actuator_force for nu=0 model |
| Explicit force/elastic fixture | Press loader before adding to save points, forces, force couples and program states | Do not guess from final synergies |
 Contact CPU mj_contactForce / WarpContact_Force; Power, force, rectangular sequence, CPU transfers to the world with contact. frame[1] positive, geom[0] counter-colon  does not direct the method to the multiplier or old contact ID when the current vernch  is complete
| Tree connection | Post-constraint cfrc_int in order of torque, force, reference point C = subtree_com [body_rootid [b]] | Not considered purely external, single contact force or equivalent motor tau |
| Non-tree constraints | connect/weld taxonomies; map multipliers by constraint space Jacobian and verify | do not treat all efc_force directly as N/N · m |

Assume M origin O is the research joint anchor point, direction R is the fixed shell, and the tree function is converted to `F_M=R.T@F_W`, `T_M=R.T@(T_C+cross(C-O,F_W))`. Contact moves from the contact point to O in the same way. The order of xfrc_applied is force, moment and the moment is in body COM, and the array order of cfrc_int cannot be applied. Various types of fields may contain the same physical effect and cannot be added again to call the total external load. When armature is used, the moment transmitted by the tree rigid body does not have to be equal to the driving tau.

**weld special case threshold: **The audit has been reproduced in the local CPU. When torquescale=1, the post-binding torque is inconsistent with the independent angular momentum balance; the same source of the sensor and the consistency of the CPU/GPU cannot replace physical verification. Correctly mapped by spatial Jacobian, attitude error, and torquescale; must not be uniformly divided by 2. The tree balance will be corrected if it is affected. The bilateral clamping of the first round of E4 uses explicit compliance force by default, the weld template is disabled until independent balance calibration is completed, and the closed chain is marked as not covered, and the compliant clamp is not used to pretend to be a rigid closed chain acceptance.

The timing is fixed as follows: Freeze before action x_t/p_t → Substep write drive and effective load Extract and copy force, contact geometry, reference gesture and solve_time after the → same solution Finish saving and → refreshing the → next boundary geometry before the next forward and assemble p_next. implicitfast q/time and contact cache may be in different stages after step; the historical role transformation must use the reference gesture for this role. The role of the current geometry and the recently completed interval is blocked, including sample_age/interval/valid; reset is invalid when there is no interval, and future force backfilling is prohibited.

Driver clock=n means that when the next write tick is made, the queue is exported from old to new according to `ring[(n+arange(11))%11]`, which represents n−11…n−1; it is initialized with clear zero input and valid bit before reset. Adjacency drivers need to truly implement the same state and cannot claim to have delays by filling in zeros when there is no model. Frequency configuration uses frequency_hz, internal omega_rad_s=2πf, only converted once.

All fields register units, coordinates, reference points, times, scales and validity. Reject no extractor/no scale fields on startup. Candidate scales: mass 2 kg, COM .4 m, inertia .1 kg·m², T/delay .02 s, damping .08 N·m·s/rad, friction .1 N·m, armature .006 kg·m², other p refers to the same registry according to the SI dimension; prevents startup when there are insufficient parameters, and does not mix privileges into Actors according to batch statistics.

## 4. Network: retain the skeleton and change the input boundary

Inherit the existing UFO-simple style and do not load full body weights. definition:

\[
E(n):\mathrm{Linear}(n,256)\to\mathrm{LayerNorm}(256)
\to\tanh\to\mathrm{Linear}(256,128)\to\mathrm{ReLU}.
\]

| Network | Implementation | Output |
|---|---|---|
| Actor | E (x137) stitched with E ([x137, z16]); Linear (256,256)→ ReLU→ Linear (256,1)→ tanh | u ∈ [-1,1] |
| Independent F1/F2 | E([y,u]) and E([y,z]) splicing; Linear(256,256)→ReLU→Linear(256,16) | 16 dimensions each |
B Linear (13,256) LNtanehLinear (256,256) RLULinear (256,16) 16D, 4

Actor and F do not share privileged encoders. Actor.context(x) still feeds back 128 dimensions, but not a supervised validation load estimate. History requires no additional RNN.

The Linear orthogonal initialization gain=1, zero bias, and LN default value of V2 are used; the difference from the UFO DenseParallel gain has been recorded in the old document, and the initialization and loss will not be changed at the same time this time. F/B has target, Polyak=.01, and no Bellman target Actor. Collection snapshots are distinguished from target Actors, see Section 8.

| Project | Parameter amount |
|---|---:|
| Actor | 207,617 |
| B | 74,000 |
| Deployment Actor + B | * * 281,617 * *, FP32 weights ~ 1.07 MiB |
| Each F | 211,728+512 D_p |
| Online Actor+B+Double F | 705,073+1,024 D_p |
| target B+Double F | 497,456+1,024 D_p |

When D_p=512, the total amount online is 1,229,361, which is just an example. V2 was deployed at 386,065 parameters; V3 was smaller due to deletion of the Actor's world/contact history fields, and the hidden capacity was not reduced. Inference latency still needs to be measured in practice, and the amount of parameters is not equal to the 100 Hz guarantee. The instantiation prints counts and checks them with the formula, and the export does not package F as a running dependency.

## 5. Simulation structure: combined scenarios replace mutually exclusive roles

Continue to use MuJoCo+mujoco-warp/mjlab, and the CPU does independent physics and field comparison. Physics/Drive 1 ms, Control 10 ms, Initial turn 10 s. The real gravity is maintained at 9.81 m/s², and the direction of gravity in M ​​is covered by the installation angle and floating motion, without changing the magnitude of gravity as the main generalization method.

The environment configuration is divided into unit, support, neighbor, contact, loader, initial_state, and program. The kernel acts according to component existence, and role==2/3 is no longer used to limit contact/adjacency. The working condition number is only used for quota audit and does not enter Actor/B.

| Working conditions | Implementation content | Collection and Replay starting ratio |
|---|---|---:|
| E0 fixed support | Complete pose with fixed P or D, each accounting for half of the group | 20% |
| E1 elastic/moving support | Planar floating root + spring damping/compliant fixture, fixed or moving reference | 15% |
| E2 Contact/Block | Ground, moving blocks or dynamic objects, P/D contact and release of different parts | 20% |
| E3 adjacent drive | P-side, D-side or both-side adjacent active joints, driven by a real motor | 15% |
| E4 Adjacency + Contact/Support | Adjacent motion and contact/support exist at the same time; 25% of the steps in the group are used for legal bilateral restraint/compliant clamping | 30% |

E4 must record the actual active time at the same time and cannot alternate between two separate environments. E2 contains retractions after blocking, not just drops and bumps; E1 does not write qpos mandatory tracking. The two-sided constraint checks the closed chain passed with a compliant connection or degrees of freedom, and does not force incompatible endpoint trajectories.

Shapes, anchors, limits, contact topology and mounting are compiled together; geometric replacement synchronous mass distribution/inertia and collision shapes. Multiple worlds in a bucket share a topology/shape; round variable fields are written after being expanded into a per-world array, and set_const/forward if necessary. The backend does not support world-by-world modification of parameters to compile items, and cannot rely on broadcasts that happen to run.

nconmax/njmax is calibrated against the most complex E4, not directly assuming that old 64/256 is sufficient. Contact/constraint overflow, penetration and solution exceptions are logged independently. Model bucket sequential scheduling does not require all GPUs to reside.

6. Random distribution and generation methods

### 6.1 First implement adequacy as cross design

The initial library for training uses 36 geometric seeds: P/D short, medium and long, with a total of 9 length combinations, 4 consecutive instances per grid, covering .15–.45 m on both sides; and equal-length calibration instances are retained. The mass and length are not fixedly bound, and hierarchical/shuffled log-mass distribution is used to complement paired rounds with geometrically different mass distributions.

Create at least 4 verified strokes for each geometry: full legal interval, narrower center, lower bias, upper bias; at least 25% of the full interval. So the base has 144 geometry/limited goal groups, then spanning E0–E4 with fixed side, contact/adjacency variants. The number of models is a starting point and does not mean that all consecutive combinations have been collected.

Validation/testing used separate lists of 12 geometry instances each in the first round, including E4 parameter combinations not seen during training. Just changing random seeds but reusing the same small set of models does not count as structural generalization; unseen topology and unseen parameters of the same topology are reported separately.

###6.2 Parameters, physical path and information destination

| Project | First round scope and sampling | Physical implementation and information destination |
|---|---|---|
| P/D Length | .15–.45 m on both sides, short/medium/long crossed; equal lengths swapped with long and short | Compile Geometry/Anchors, lengths to g/B/Actor/F |
| P/D base mass | .15-2 kg on both sides, logarithmic stratification, light/heavy crossing | Consistent mass/inertia; declare parameters to actor, actual value to F |
| Mass distribution | Counterweight ratio 0–.2, position .2–.8 L, different distributions at the same length | Real geometric synthesis COM/I, non-independent random pumping of illegal inertia |
| Model error | Basic accurate statement; set up another group with unchanged statement and actual density .8–1.2 | Mass/inertia common ratio; Actor does not read the magnification, F reads the actual value |
| Joint response | damping .01–.08, friction 0-.08, armature .001-.006; armature hierarchy with log | write physical fields, recalculate constants; actual value to F |
| Driver | Capability benchmark C0=3/6/9 N·m Equivalent three levels, request scale S=1.25*C0; actual capacity C=C0*r, r∈[.8,1.2], T 5–20 ms, delay integer 0–10 ms | Output side model, S*u→millisecond queue→real capacity limit→first-order response; declare value to Actor/upper layer, actual parameters/queue to F|
| Zero position/direction | beta is layered according to a circle of eight sectors, s=±1 equal; known calibration | Actual zero angle assembly and tree axis are compiled simultaneously; enter B/Actor/F after unifying q_c, and the mapping is retained in metadata |
| Installation/public motion | E0 Installation angle is stratified in 8 circumferential directions; E1–E4 Legal root posture and positive and negative movement | Real change installation/initial state; gravity projection and public motion only give F |
| Explicit loading position | P/D symmetry; position .05-.95 L is divided into 5 segments; direction 8 sector jitter | actual acting point applies force, moment translates to COM; actual point/force/force couple gives F |
| Loading amplitude | No load/near zero, compensable, medium and high load crossover; initial upper limit .5 M_unit g, couple ±1.8 N·m | M_unit refers to the actual mass of P+D and does not change with the number of scene objects; records the load ratio relative to the available axis moment |
| Contact | Friction .4–1.0; normal, gap, contact side/position, object motion layering | Legal initial state, real solution contact, F read current condition |
| Support | kx 20–200 N/m, kz 100–500 N/m, kθ .1-5 N · m/rad, damping ratio .3-1 | Real spring damping; preloaded/mobile reference independent grouping, not always accurate offsetting gravity |
| Adjacent structure | Peripheral length .15–.45 m, mass .15–2 kg Layered | Compile the entire chain, cannot continue to fix A/T; actual structure/status given to F |
| Adjacent action | Amplitude .1–.7 rad, frequency .3–2 Hz; phase, same/reverse, unilateral/bilateral crossover | Feedback torque drive, reference subject to adjacent stroke constraints; target and actual motion recorded separately |
| Adjacency control | Old kp=8, kd=.5, cap=3.6 as baseline, gain and capacity multiplier .5–1.5 | First round candidate; multiplexed millisecond drivers and independently randomized, true value given to F |
| reset | φ = (q − q_min)/(q_max − q_min) 10 points; speed zero/plus or minus low medium high, initial wide range ± 4 rad/s | legal generalized state, q/dq is consistent with the contact constraint, no false ddq is specified |

The range must pass physical and coverage checks, and most samples must not become numerically explosive or permanently uncontrollable. Restricted processes that are physically legal but exceed the capabilities of the motor remain. Areas without evidence of access cannot be automatically marked as physically inaccessible.

Parallel loading along the rod or at a paraxial point may barely change the shaft response and can be checked for indiscernibility, but cannot be counted as induced load adaptation. When the old request is ≤ 6, the capacity 6.5/7.2 will not produce different limits; V3 uses S=1.25*C0 to exceed the maximum capacity of the file 1.2*C0, and includes short segments and legal continuous segments with positive and negative u=1 in the rules. Proving capacity is stimulated depends on the actual target limiter and drive output, not just the configuration. Fixed physical unit scales (such as tau/6) do not change with C0, and only tiering and capability queries use declared capacity.

The quality model error group accounts for 20% of the number of rounds, and the remaining 80% accurately declares; the two groups of results are respectively counted to avoid confusing the modeling error and unknown external load as a change. This ratio is a configurable starting point and does not change other operating conditions quotas.

The proportion of the explicit loading point is measured from the study joint to the end of each rod, and the force application position cannot be shifted by using the origin of the model tree for P. The direction reference system is divided into half groups according to the "fixed direction of the inertial system" and the "direction of rotation with the connecting rod". The physics engine updates the force in the sub-step accordingly; the actual force given to F is uniformly converted into M, and the Actor does not read the direction plan.

The support preload is no longer always equal to the exact weight: the vertical preload coefficient is initially taken to be 0/.5/1/1.5 times the nominal load-bearing weight of the support, the horizontal offset is ±.25 times the weight, and the angular preload is ±1.8 N·m. Whether preload is compensable is judged by the actual response; the command, actual effect and F fields are recorded separately.

The starting point of the support initial state velocity follows the old range: translation ±.5 m/s, angular velocity ±1.5 rad/s, and is combined with model/constraint checking. The moving support is referenced to an initial translation amplitude of .01–.05 m, a rotation angle of .05–.3 rad, and a frequency of .2–1 Hz. The initial mass of the dynamic contact object is .1–2 kg, the size is from the rod cross-section to .2 m, the velocity direction is positive and negative, and the amplitude does not exceed .5 m/s; the specific shape and trajectory must first fall into the template and field contract in Section 3.5. The newly added ranges are initial configurations, not tested capabilities.

# # # 6.2.1 Zero bit randomization of two experimental and motor model boundaries

The zero bit must be covered, but there are two types of evidence:

1. **Physical posture group corresponding to the original zero angle**: unified equipment contract `q_c=encoder_sign*q_e+beta_encoder`; the model also has `q_c=tree_sign*(q_tree-qpos_ref)+beta_model`, and the two sets of parameters are registered independently. For the example where P is the parent body and D is the rotating child body, you can compile the R_y (beta_model) and axis tree_sign*y of the output body; the reverse tree of fixed D cannot fit this structure as it is, and the mapping should be verified according to the relative attitude, speed, power and limit of the template (a common coaxial reverse tree tree_sign=−1, but this is not a universal assumption). Actual rod end, inertia, collision and overall transformation of downstream mechanisms. It is forbidden to only change the observation/ref but treat the default qpos as the same physical initial state.

beta_encoder candidate [−π,π) eight-sector jitter, encoder_sign equal, zero bias left for calibration; the physical initial state is first extracted from the legal q_c interval, and then inversely solved for q_e and q_tree respectively, the original angle does not need to fall in [−π,π). The zero-read subgroup must satisfy q_e=0, q_c=beta_encoder and be physically legal; q_tree=0 is only required when the original coordinate template satisfies q_tree=q_e, ref=0. When canonicalizing the simulation model q_tree=q_c, the original zeros naturally correspond to q_tree=beta_encoder. Device configurations that are unreachable at zero point will only be adapted within the legal range and will not be illegally reset to zero.
2. **Coordinate equivalent pairing group**: The same legal q_c/dq_c, the same physical parameters and boundaries, after changing beta_encoder/encoder_sign, reversely solve the device readings/requests, and generate the tree status according to the independent model_adapter; when changing the model coordinate template, the q_tree/dq_tree is also synchronously reversely solved; compare the rod end/COM/inertia, physical trajectory and unified g/x. Pairings where beta only changes the notation but does not change the physics does not count the new dynamic coverage, nor does it increase the number of goal configuration groups. The first group with different real physical zero angles must save the attitude difference of the same device q_e=0, and the generation check cannot be canceled with unified preprocessing.

beta/s Each model or equipment configuration is fixed and does not change randomly within a round. Each geometric/physical limit group covers two symbols, at least four legal beta configurations throughout the entire acquisition window, and eight sectors across the entire library; each capability profile has at least two cross-beta pairings. Beta uses independent random flows with quality, drivers and scenarios, and the correlations caused by legality screening are truthfully recorded. The world mounting angle tilt is another physical condition and is not equal to beta.

* * Accurate calibration in the first round without injecting unknown bias into the main training. * * Unknown beta_true − beta_decl will make the calculated endpoint geometry no longer true, only F knows and cannot magically recover the Actor/B; the constant bias may not be recognizable without a reference. In the future, the single column noise/calibration error robustness scheme will compensate for the semantic and based error range of validity, and do not use acc_valid to cover unknown calibration.

The motor family is an approximation of the ideal torque drive on the output side, and no specific product motor is specified. C0 three levels are used to test the calling of the same local result under known changes in capabilities; the same structure is paired across three capability levels. T, delay, damping, friction, and armature use the range in the table. The first round of independent stratification is a verification distribution and does not claim to meet the joint distribution of the real motor model.

Declaration vs. actual rules fixed: 80% drive round accurate group, Actor k_drive equals real constant (queue still not read); 20% model_error group, Actor declaration ±C0, T=.01 s, delay=.005 s, damping=.03, friction=.02, armature=.003, real constant sampled by table and only extra F. Both sets of S are known and actually valid request criteria; the quality statement error can be an independent random stream and does not need to be permanently grouped with the driving error. First, keep the positive and negative capacities symmetrical, keep the upper and lower limits of the field in both directions, and do not claim that the asymmetric drive has been tested.

The first round does not simulate temperature rise derating, speed-torque envelope, current/torque calibration error, backlash, gear elasticity, and independent torque climb limit. The armature is an approximation of the reflected inertia on the output side and does not simulate the rotor/gear separately. Each subsequent extension must have a physical path and source statement, and the gear ratio/rotor inertia/capacity that is not coupled to each other independently is called a real motor generalization.

# # 6.3 The itinerary must be genuinely expanded, not just changed to show q

The old ±1.2 rad was not a universal motor range. The model generator first checks the legal connected interval of the current assembly in the candidate angle domain of approximately [-π+.05,π−.05]; this is just a search domain, and there is no guarantee that each assembly can cover the entire domain.

Check for adjacent pole collisions, hinge yield, non-adjacent poles/objects, and cable restrictions. The hinge clearance must be reflected in the fixed geometry family and collision shape, and all self-collision cannot be turned off to obtain false large travel. After static mesh filtering, check near the boundary and continuous sweep angles, and save a list of tolerance, mesh and collision pairs. The check set is independent of the actual contact set of the engine and contains the default filtered parent and child rods; whether internal contacts are counted in the "external load statistics" is separately defined. The starting point grid is 0.5°, and the boundary is refined to 0.05°; the non-contact initial state independent distance is not less than 0, and the distance numerical tolerance is 1e−5 m. Penetration of contact is allowed to be solved and the acceptance is based on contact compliance. Scanning cannot be used as proof of continuous collision-free, and the deployment range must be conservatively indented, check the minimum spacing between adjacent samples, or conservatively continue the collision boundary. The legality of adjacent motions, objects and closed links is re-checked in each scene state, and the body's empty field sweep angle is not mistakenly said to be unobstructed in all working conditions.

The legal interval [a,b] takes the width w=f(b−a), f∈[.5,1], the center c∈[a+w/2,b−w/2], and the limit is c±w/2. Preferential complement assembly spans the range of the old ±1.2 and approaches/dwells/leaves the actual boundary. If it ends up being all old angle fields, report "Wide stroke model not completed".

Rule reference, initialization, limiter, normalization, query, web page read the same configuration. The margin and soft limit parameters are distinguished from the control limit, and the .03 rad activation in advance cannot be false alarmed as a full available trip. When an infinite rotation model is not established, it is not claimed to cover the continuous rotation motor.

### 6.4 Randomized three-layer landing

- Compile Layer: Length/Collision, COM/I Shape, Installation, Limit, Adjacent Topology, Object/Fixture, Output XML/Configuration/Hash.
- reset layer: mass/inertia scaling, resistance, driving parameters, legal initial states and boundary states supported by the backend; readback, recalculation of constants, generation of declared models and p.
- Trajectory layer: loading/unloading, obstacle movement, support/adjacency references, commands and exploration; no instantaneous modification of quality/geometry per frame to replace real loading.

Random streams are derived by run_seed, geometry_id, limit_id, scene_variant, episode_id, purpose. reset, dynamics, external load, rules, z, exploration, Replay, evaluation independent; num_envs changes should not change the random conditions of the same episode.

# 7. What process to collect and how to collect it

# # 7.1 The rule controller generates only behavioral data

Rule execution is truly driven and does not give the Actor a teacher label nor assign a permanent task z. Rule targets/stages are only used for scheduling audit; F reads the real external loader status and does not use future joint rule actions or targets as additional conditions.

| Procedures | Reference Generation | Procedures Needed to Be Preserved |
|---|---|---|
| Full stroke hold/change point | take q_ref according to 10 segments, and arrive in both directions | enter, stable/unstable, output, exit, not only in the target reset |
| Sweep angle/reciprocation | Triangular/sinusoidal/smooth segment within the stroke, direction and amplitude crossing | Same as q but different from dq, acceleration, deceleration, reversal |
| Speed/brake | ± .5/1/2/4 rad/s starting point, the near limit decelerates according to the stopping distance | Different speeds, positive and negative power, real stops in the same position |
| Torque adjustment | Near zero, positive and negative medium/high amplitude requests, record limiter | Same movement, different output, saturation/reverse drag; no contact, no designated end force |
 tau_ref=bias+K (q_ref-q)—Ddq, K/D Retain the scope of the old rules
| Block/Release | Establish motion→ stops to prevent→ continuous/reverse→ movement | Not reached but sustained output, overshoot/recovery after release |
| Load switching | Persistence, adjacency reference or support change | Actor adapts after seeing the response, F reads the effective truth value |

The source of the gain and whether a privileged model is used are recorded; rule targets must not directly override qpos/qvel. Calibrate the rule collector before P0: the fixed support is maintained using the model's static bias force feedforward + PD, and the coupling/external load scenario is supplemented with anti-saturation integrals. The initial value of PD is ωn=6 rad/s, ζ=1, Kp=I0ωn², Kd=2ζI0ωn according to the fixed boundary small signal inertia I0; the initial value of the integration time is 1 s, Ki=Kp/(1 s), the integration stops when it is saturated and the error continues to push the saturation, and the release/change process is reset according to the configuration. I0 is the basis for adjusting parameters of the rules and does not give the Actor full-time dynamic load. All requests go through the same real limiting/delay channel; the speed/adaptation program has corresponding reference, and there is no need for points to force the blocked process to be successful.

Each motor capability/configuration bin is first checked for achievable holding points using independent static balancing before verifying true convergence. You cannot directly retain the old Kp=6 and Kd=.6 and then judge the heavy-load steady-state deviation as unreachable. Four categories are recorded: mechanical infeasibility, insufficient capacity, rule failure, and numerical failure; insufficient collection of feasible points requires adjustment of rules and additional collection, and failure transfers are still retained. Rule feedforward and model truth are only used to collect actions and do not increase imitation/task loss.

### 7.2 Allocate time according to control steps

Rule start budget: short transient 20%, continuous movement 30%, continuous load/release recovery 50%. Short transient of 40/80 ms, continuous period of .5-2 s; loaded subjective observation period of at least .5 s and more than 5 driving time constants; proximity/recovery is given a maximum of 2 s each first. 10 s rounds accommodate full cycles, extended by version when insufficient.

Maintain the initial audit value: | q − q_ref | ≤ .05 rad, | dq | ≤ .05 rad/s continuous .2 s; this is the process label/evaluation threshold, not the FB positive sample judgment or reward. Timeout to save the true transfer; speed/reciprocation is checked according to the corresponding trajectory error.

Loading covers both short perturbations and 1–3 s sustained loads, with the original .1–.5 s pulses being the short category only. Loading start/continuation is independent of z, and the complete "load-unload-resume" is counted separately. The obstacle is truly withdrawn through the controlled object, and the force transmission object is not deleted instantly.

The initial reset value is recommended to be 50% stroke layering, 30% legal wide speed/initial contact state, and 20% access snapshot. Snapshot restores physical, driver, and boundary processes, and re-pads telemetry history; records requests/actual recovery/rollback, and does not treat 20% of the plan as a result. Initial state coverage is not equal to motion transfer coverage.

### 7.3 P0 and persistence rule data

144 geometry/limit groups, E0/E1/E2/E3/E4, 4/3/4/3/6 10 s rounds each, the initial lower bound is about 2.88M effective transfer. Fixed side, contact side, E4 bilateral constraint cross-group rotation; shortfall recovery. Extra rounds generated by GPU batch processing count towards W and are not covered by the nominal count. 2.88M is just a starting point. The balance in the configuration can be requested to be added, and the adequacy cannot be inferred from this number; see Section 11 for the specific lower limit.

P0 does not reuse V2 raw: it lacks p, change limit and new loading process, and cannot be zero-filled and forged. Verify the model and sampler first and then generate them in batches.

After starting the online training, the new physical transfers are still collected according to 50% of the rules/actor, and both sources cover E0-E4 internally. The rule base continuously replenishes scarce groups and retains key sequences, avoiding taking only the most accessible state of the Actor at a later stage.

# 8. Replay, z and Reference Distribution

# # 8.1 Sequence storage, real transfer sampling

Each episode saves model/declaration parameters, actual round parameters, version/ID; T +1 telemetry and dynamic p boundaries; T actual u, tau/u interval integral, dt/significant bit, terminated/truncated, stage/behavior version. Complete original sequences or equivalent causal prefixes are used for x/g reconstruction, not across resets.

batch returns x, p, u, x_next, p_next, g_next, discount, and audit ID. The F action is the uniformly oriented, normalized actual request u_c; scale S is in k_drive of x. Hardware/tree raw requests are audited by the adapter switch, do not mix it with u_c, and do not use delayed post-torque replacement actions. The current/next p is paired with the corresponding boundary, and the next round's true value cannot be connected to the end point.

Rules/online sub-library. The rule capacity is at least reserved for P0 and key processes. Online 1M is the starting point for configuration. It is actually automatically expanded according to the minimum group capacity in Section 8.2. It is reserved for complete rounds. Scarce processes are filled through scheduling. Bellman samples are not selected based on posterior success. Capacity is transferred efficiently and does not rely on a fixed 500-step episode.

### 8.2 Gradient distribution and ρ synchronization

After sufficient online pre-filling, each batch of rules/online expectations are halved; in the source, according to 20/15/20/15/30 of E0-E4, and then the actual transfer is stratified by position, speed, torque and process stage. Joint stratification uses practical groups and does not impose complete Cartesian product uniformity.

The first round of accurate sampling is: the source is weighted by 1/2 of the → working conditions according to the table. → The geometry/limit configuration of the working conditions → covers the key family .4/.2/.2/.2 of the current program stage → can be put back with the right of true transfer within the → bin equal weight bin. It is ten equal width gears; dq presses [− ∞, − 4, − 2, − .5, .5,2,4, ∞]; tau presses the relative declaration capacity [− ∞, − .8, − .2, .2, .8, ∞]; the stage takes the current program's proximity/main process/uninstall/recovery, and sets the policy when there is no program online. The capacity on both sides of the symbol is set to a positive amplitude, and the hierarchical normalization does not change the absolute SI characteristics of B. Configure that physical categories that do not exist are flagged in the manifest, and that exist but are not accessed to report arrears.

All keys take the t-bounded known state and the current program state; do not filter Bellman transitions with t+1 response, final success, or future recovery tags. The result label is used for coverage diagnosis. If you want to filter by subsequent filtering in the future, you must reprocess the conditional transfer deviation and cannot just synchronize ρ. Each row independently samples the source, working conditions, and current coverage level, and then independently samples the book, with replacement and sharing the same rules; do not fix the rules for the first half of the batch and fix the second half online, but still say that the non-diagonal reference is independently and identically distributed. If the mandatory batch quota is adopted in the future, the estimated weights must be processed synchronously.

Record the sampling probability: The probability of each row is the sum of all the key family path probabilities that can generate the transfer, not just the selected path. The number of transitions in the group is uniform, and the implied short round weighting of the first uniform episode is not followed. When the source or working condition is empty, stop formally mixing, updating and replenishing; if there is a configuration/bin vacancy, this window will re-normalize the sample item, record the actual weight/gap and synchronize ρ, and it is forbidden to record the return as an overlay.

Rule P0 will not be eliminated; the new rules retain the complete episode according to source/scenario/configuration, the uniform reservoir within the group, and the entire round retains the independent success label. The online capacity is automatically rounded to the full episode capacity by `max(1M, max_c(2*N_config,c*T_episode_max/w_c))` to ensure that each storage group has at least two rounds after equal allocation according to scene weights; when there are 144 groups/working condition and 1000 steps per round, the lower limit is only about 1.92M. When the quota is exceeded, the oldest complete round will be eliminated, and the length of one round is allowed to exceed; the capacity can accommodate at least two complete episodes per group, otherwise the startup will fail. Process scarcity is compensated by acquisition scheduling, and diagnostic archives can retain failed/rare fragments, but Bellman libraries must not be silently weighted by posterior success. The capacity of the rule base is calculated according to P0 + additional plan. If it is not enough, the disk budget will be expanded and silent overwriting will not be performed. Sampling probability, empty group and rollback records; vacancies in key working conditions trigger replenishment, and coverage cannot be said to be completed after silent redistribution. Define the training distribution hierarchically, and by default do not add additional weights corrected to the natural access distribution.

FB uses g_next for the same batch, so the old one is the next distribution induced by the sample program. (a) The same rule for the use of search pools; Synchronized version of the distribution change. The P0 reference pool cannot be used as a pre-training exercise forever.

## 8.3 z generation and use

The training batch is still 50% spherical random direction + 50% real complete goal of the current B encoding. The goal is independently extracted from the same length/physical limit/geometry family group; only beta/s recoding does not split into new groups, and the real installation accessory changes the geometry. The goal requires that the acceleration is valid and no longer randomly disrupted across structures; results with different loads are only candidates and are not guaranteed to be currently reachable. If there is no matching sample, fall back to the random direction and record the results.

The same configuration goal * * does not change the global ρ or FB non-diagonal mask * *. The preference query is still pressed Eρ [r (g) B (g)]; when only speed/torque is required, other fields are not randomly zeroed. A large number of unchangeable structures/limits may occupy the limited representation capacity of z16. To check the fitting and global statistics within the structure, it is not necessary to only look at the overall effective rank or secretly modify the conditional FB.

The collection uses the supporting Actor/B snapshot encoding at the beginning of each call, fixes z within the call, and then encodes again at the end; the semantic z is not cached across training versions. Each complete rollout can synchronize a behavioral snapshot, and the learner is continuously updated; this is off-policy acquisition, not target Actor.

The online call start is budgeted according to the control step: short 40/80 ms accounts for 20%, lasting .5–2 s accounts for 80%, and uses time under-scheduling to avoid confusing event proportions. The target always predicts the same z successor, regardless of the acquisition of the next command change; the short-call capability is evaluated separately.

# 9. FB Updates and Training Cycles

y_i=(x_i,p_i), g_j is the next result of the true transfer of section j of this instalment, N2:

\[
M^k_{ij}=F_k(y_i,u_i,z_i)^\top B(g_j),\qquad
\bar M_{ij}=\tfrac12\sum_{k=1}^2\bar F_k(y_i',u_i',z_i)^\top\bar B(g_j),
\]
\[
u_i'=\operatorname{sample}(\pi(x_i',z_i)),\qquad
\delta^k_{ij}=M^k_{ij}-\gamma_i\operatorname{stopgrad}(\bar M_{ij}),
\]
\[
L_{\mathrm{FB}}=\sum_{k=1}^2\left[
\frac{\sum_{i\ne j}(\delta^k_{ij})^2}{2N(N-1)}
-\frac1N\sum_i\delta^k_{ii}\right],
\]
\[
G_{ij}=B(g_i)^\top B(g_j),\quad
L_{\mathrm{orth}}=\frac{\sum_{i\ne j}G_{ij}^2}{2N(N-1)}
-\frac1N\sum_iG_{ii},
\]
\[
L_\pi=-\mathbb E_i\min_k F_k((x_i,p_i),\pi(x_i,z_i),z_i)^\top z_i.
\]

The true next g is the visiting positive sample, without the angular threshold or B-z distance determination. Non-diagonal samples are not equal to "negative samples not reached", and different indexes may also be drawn to a duplicate state.

Follow Adam lr = 1e − 4, batch512, γ = .99, Polyak = .01, action standard deviation .2, training noise cropping .3, no cropping gradient by default; the actor updated action uses the same heavy parameter sampling as V2, and the π in the formula represents the sampling action. The discount time constant at 100 Hz is about .995 s. The target double F is averaged first, and the actor dot product is taken as the smaller value. The actor updates the frozen F parameter but retains the action gradient, p does not pass through the actor forward. Non-finite loss/gradient isolation and stopping the current run without adding loss masking issues.

gamma_i=.99×(1−terminated_i). Replay returns [N,1], and the loss entry is checked and organized into a transfer line of [1,N,1] multiplied by [2,N,N]; rejecting the direct transmission of [N] results in broadcasting along the reference column. Normal 10 s truncation continues bootstrap, using the last physical state before truncation; illegal/numeric failure isolation, cannot be packaged into ordinary termination. When the true physical termination is not defined, terminated is always false, and no early termination is added for the training effect.

~~~text
Compile/validate all scene templates, freeze schemas, save models and random flow manifest
Collect and audit P0, the real rule sequence enters rule_replay; initialize a new network
Obtain at least 8192 different online transfers to avoid reusing the initial small sample
Press "Source→Working Conditions→Override Debt" to select the next batch of processes:
The original record generates the current x/p; the rule or freeze acquisition Actor generates u
Really advance 10 1 ms substeps, generating next telemetry, p_next and termination information
Save continuous sequences and real transfers, and accumulate valid/ineffective physical costs
credit += number of new valid transfers × updates_per_W
    while credit >= 1:
Independent double-source watch, reconstruction x/p/x_next/p_next/g_next
Current B generation training z; Actor (x_next,z) Generate target actions
target F ([x_next, p_next], u_next, z) followed by target B
Update F/B; freeze F parameters update Actor; Polyak update F/B target
        credit -= 1
Regular output coverage; freeze supporting Actor/B for independent evaluation
~~~

updates_per_W initial value is 1/256, configuration must be read. P0 counts the physical cost, and the new interactive update quota will not be repeatedly issued for library installation, and undeclared offline training rounds will not be added; gradients will only be generated when the rule samples are actually selected. After the online warmup is completed, credits will be accumulated and updated.

The state adequacy of F is checked for y=[x,p]: p cannot have only one resultant scalar, and must contain the corresponding environment/drive evolution conditions and feature_memory; the compressed summary of x cannot replace the entire recursive memory of the feature updater. The Actor is still a constrained information policy and cannot treat hidden states known by F as being perceived by the Actor; this does not change the already established privileged F training decision.

## 10. Scheduling, Budgeting and Resources

Movement control transfer dues: target quota w_c, actual W_c, priority is given to the largest operational group w_c W_tontal_W_c; Sources, performance and critical processes are accounted for separately. Failures/overspills are not effectively covered and actual costing is still reported.

| Stage | Product and promotion conditions |
|---|---|
| S0 Contract/Physics | Coordinates, fixed D, combined contact, parameter writing, truth value extraction and CPU/GPU comparison are established |
| S1 P0 | Continuous sequence and coverage report for all working conditions, continue to make up for the lack of combined working conditions, not downgraded to only R0 |
| S2 training | Dual sources cover all working conditions; the total 20M effective W includes P0 as the budget starting point, and the course is completed without relying on the old W threshold |
| S3 Freeze Evaluation | Random z, Physical Query, Load Release, Switching and Unseen Structures, Preserving True Failure |
| S4 upper layer access | Compare the two feet after the unit evidence/interface is clear, and add the upper layer task budget |

A single R0 can be performed independently for short duration; Check formulae, time series, physics when you do not pass. Formal training cannot be limited to narrow R0/R1 for a long period of time, followed by “entry P3” instead of E4 actual coverage.

Replay does not release all GPUs by default. The rules use disk sharding/memory mapping, the online uses bounded CPU cache, and only the staging batch uses pinned memory to transfer to the GPU. Static parameters are stored once per model/round, and the next record refers to the same sequence to avoid repeated storage of x/x_next and p/p_next.

~4M bounds With 512 FP32 scalars per dynamic p, that's ~7.6 GiB for p alone, plus telemetry, indexing, and caching. Calculated based on the actual number of dynamic fields, the static model will not be expanded repeatedly. The current session has about 31 GiB of visible host memory; nvidia-smi cannot connect to the driver. **It has not been confirmed that the session can run the GPU** and no hardware damage can be inferred. Reconfirm dependencies/drivers/memory when development starts.

First test the complete "simulation+features+replay+update" throughput and peak memory, and then set num_envs/cache. Maintain a single active model bucket, cache a small number of compiled buckets, and do not require all models to reside. Payload or complex contact data cannot be deleted for throughput.

## 11. Coverage audit: randomization is not just written in the configuration

New valid transfer output coverage.json/html every 100,000 new entries:

| Level | Verification content | Processing if failed |
|---|---|---|
| Configuration | Length Pair, Mass Ratio, COM/I, Stroke Span/Center, Fixed Side, Topology Variant Plan vs. Actual | Makeup Model/Repair Generator, No Instance Duplicated |
| Effective | Parameter readback, response to the same request under different inertia/delay/resistance | Distinguish between inactive, unexcited, and only reaction force changes, modify physics/excitation |
| Process | Adjacency + active duration of contact at the same time, continuous loading/anti-towing/release/two-sided restraint times | Complementary continuous process, not only reset |
 State, dq, qx, dqx, dqxdq, L_Dxdq, and structural/routing conditions overwhelming  Compensatory groups, with harmonized coordinates and physical values reported
| Transfers | Entry/Exit, Direction Switching, Load Response and Release Recovery by Interval | More than Statistical Static Frames Near Targets |
| Use | Source/working condition collection and gradient ratio, sample retention/elimination | Fix Replay, do not use reference pool coverage to pretend to be training coverage |
| Quality | Acceleration efficiency/hysteresis/overscale, p consistent with physics, contact overflow/reset alignment | Repair extractor/schema and re-extract |

A two-level list is implemented for coverage acceptance at the same time. The lower limit in the first round is only to prevent vacancies and is not a proof of statistical adequacy:

- By Geometry/Limit/Applicable Condition: Each confirmed accessible gear comes from at least 2 independent episodes, and a total of at least 20 real control steps; configure at least 2 independent processes for internal positive and negative motion, approach and departure boundaries, and achievable low-speed bandwidth and load release. E0 Check the fixed P/D separately for each configuration, and do not fill the data on one side to the other. E4 Each configuration has at least 2 consecutive ≥ 0.5 s adjacencies + contact with the actual active process and 2 complete unloading recoveries. Actionable items that cannot be done remain in arrears.
- Cross-configuration crossover: There are still at least 20 episodes for each applicable working condition and each feasible ξ gear; there is an explicit combination list for installation of 8 directions × fixed side, 9 lengths × capacity level, 3rd level mass ratio × 5th level external force point, and adjacent single/double sides × contacting sides, and the legal combinations are at least 2 episodes. A full Cartesian product of all variables is not required, but the uncovered list must be preserved and generalization claims restricted. A check of motor families and calibration maps is provided in Section 6.

The reference active criteria are frozen before acquisition: contact normal force > max(.2 N,.02 M_unit g), adjacent motion |dq|>.05 rad/s; stall force alone is |dq|≤.05 and |tau|>.1×the declared capacity of the side; clamp transmission force is |F|>.02 M_unit g or |T|>.02×declared capacity of the research joint. The threshold must be at least 5 times higher than the unloaded numerical noise, and when not met, calibrate first rather than relax after harvesting. In E4, the number of steps that are adjacent to the actual movement and contact load-bearing is established at the same time is ≥ 20%; the number of actual force transmission steps for bilateral clamping in the group is ≥ 25%, and each segment is continuous for ≥ 0.5 s. Stalls belong to another valid category and do not pretend to be in motion; ready/waiting/failed are saved as usual but do not fill these active balances. The default compliant clamp, weld is explicitly not included in the closed chain coverage when it is not calibrated.

Feasibility is reviewed by models/constraints and independent rules; no policy or rule cannot be automatically determined to be unfeasible without access. Additional collection is required when more samples are needed for any one condition, and the starting point of the 20m total budget is not guaranteed to reach coverage_ready.

Within the complete statistical window, the starting tolerance of the actual proportion of large working conditions is ±5 percentage points; the balance can be tracked and replenished. The near limit dwell, number of departures and the longest continuous limit pressure are reported separately. Failed frames cannot be deleted to beautify the histogram. Improve the collection first, and then explicitly synchronize the Replay distribution changes.

At least one pairing condition check shall be performed for each random item: with the legal initial state/request, the parameters shall be changed, and the affected torque, dq/q, estimated acceleration or reaction force shall be compared. The mass of the fixed P may only change the bearing of the support, and the effect of motion must be checked under the P moving conditions.

## 12. Evaluation, query and export

Evaluate the freezing of the supporting Actor/B/schema, save the reference with the actual q/dq/τ/acceleration, u, significant bits, declaration configuration, privileged load diagnosis and stage; the webpage clarifies the privilege curve.

- Random z motion/output/response distribution, not just showing selected successful queries.
- Hold, speed, shaft torque, acceleration, deceleration and compliance at different lengths/limits; reference covers legally trained areas other than old − 6 and ± 1.2.
- The same query spans light/heavy inertia, sustained load, blocking release, adjacency + contact; distinguishes between visit, arrival, hold and restricted failure.
- Short-term switching does not reset the history, recording overshoot, call delay and recovery.
- Unseen parameters, geometry/stroke, and topology are marked separately; unknown z has no unique reference trajectory and does not forge the target skeleton.

Queries use g13/schema and do not reuse the old fixed 16-item algebraic cache of reward_features. Calculate r(g) directly and perform Monte Carlo integration according to the statement ρ; the acceleration query processes the significant bits. 65,536 reference results, 4,096 integrated samples can be used as a starting point for legacy projects, distribution/B versions are saved and integrated errors are reported. Query rewards do not enter pre-training.

Immutable structures/strokes with finite z16 may restrict low-rank expressions, reporting projections and control errors by structure, and not just looking at the full pool mean. The true value of F has a contact force that is not equal to B/z, and any contact force can be directly queried. The normalized access aggregation matrix for fixed z, K distinguishable and intra-round invariant configurations is I_K, and the aggregate rank of FᵀB is at most 16; the equal-weighted Frobenius optimal relative error lower bound for K=144 is about .943. K takes the actual unique valid configuration and does not take the model ID number. This bound is not a general bound controlling failure rate or original FB loss; there is no impossible global exact fit through the line. Keep the global ρ/z16 and check the task and response fitting within each configuration; if there is a local capability failure, explicitly discuss the algorithm changes and do not change the conditional FB implicitly.

The interface suggestions are reset(known_model,telemetry), observe(telemetry), feedback(), and act(z). Feedback uses named physical (unified q/dq/tau/derived motion), B16, acc_valid, known_model, known_drive, parameter source/valid bits/calibration version, optional actor_context128, replacing the old 197-dimensional hardcoding. known_drive feeds back the amount of claims known by the actual deployment; does not bring simulation hidden derating or real external load entrainment to the upper layer. B16 does not promise to include all capabilities; the upper layer can directly use the declared capacity to convert the relative force intention into an absolute torque target. Deployment only requires Actor/B, features/estimators/schema and query data, and does not require the upper layer to supplement p.

The bipedal comparison maintains the same known models, telemetry/privilege conditions, drive limits, control frequency, and cost calibre; the unit pre-training and upper-level training costs are recorded separately, without the prior commitment that "qpos cannot learn and z can learn".

## 13. File changes and development sequence

The following paths are for modules to be created and do not mean that the code already exists.

| Planning module | Changes | Completion product |
|---|---|---|
| v3/schema.py, features.py, history.py | Replace old o24/x336, unified SI and causal processing | g13/x137, p registry and timing |
| v3/mechanics.py, scene.py | Elements and supports/adjacencies/contact decoupling | Fixed P/D, E0–E4, legal travel reports |
 v3/randomization.py, programs.py  3-layer random flow, reference process generation  cross-distribution and continuous loading/release
| v3/environment.py, kernels.py, cpu.py | All exposure scenarios, actual parameters and load export | p/p_next, readback and CPU/GPU comparison |
| v3/networks.py | Parameterized input dimensions, Actor/F separation | counts and input isolation |
| v3/replay.py, collect.py | Dual-Source Sequence Library, Hierarchical Transfer Index | P0 Fill Library, Rare Process Retention |
| v3/learner.py, fb_loss.py | F changes y, row-by-row discount, loss structure is retained | Asymmetric update and gradient isolation |
| v3/train.py, coverage.py | Quota Shortfall and Configuration Driver | Reproducible Run and Override Report |
| v3/queries.py, evaluate.py, interface.py | Remove old column numbers/fixed angle domain assumption | Current query and frozen interface |
 v3/configs/, test/  Harmonized configuration version and cross-module check  Denied missing field/ old weight before startup

The order is: schema/kinematics/real load extraction → E0–E4 physics and randomization → P0/Replay → network/learner → training/evaluation/interface. A small number of samples can be penetrated first, but the full V3 project cannot be declared completed until E4/continuous load is completed.

V2 tests are retained, V3 checks focus on substantive errors:

1. Coordinates and physics: fixed P/D, symbols, resolution of limited differences in kinetics and independence; The public movement does not mix into g.
2. Information isolation: only change p, the input and output of Actor/B remain unchanged, and the corresponding field of F changes; do not regard random F output differences as physical proof.
3. Cause and effect timing: online/Replay consistent, parity slow sampling, reset, snapshot, missing and truncated correctly.
4. Randomization: real writing, world isolation, wide limit, E4 contact, reaction force reference point, continuous loading/unloading, CPU/GPU and step size check.
5. Learning: Independent scalar formula checks loss/gradient, p_next pairing, target stop gradient, F freeze unblocked action gradient, termination mask.
6. Data: rules really enter the gradient, empty groups are reported, goals do not secretly change configurations, and slots are not silently truncated.
7. Export: The new process can call Actor/B without providing p; the V2 weight/schema is explicitly rejected.

#14 Configure and Recording

Core configuration diagram:

~~~yaml
version: LOCAL_RESPONSE_ASYM_FB_V3
physics: {dt: 0.001, control_dt: 0.01, episode_s: 10}
representation: {g_dim: 13, actor_x_dim: 137, z_dim: 16}
history:
  slow: {hz: 50, count: 10}
  fast: {hz: 100, count: 8}
  acceleration: {method: causal_linear_fit, samples: 5, hz: 100}
coordinate_map: {angle: canonical_output_rad, zero: calibrated, random_beta_sectors: 8, signs: [-1, 1]}
drive:
  capacity_nominal_Nm: [3, 6, 9]
  request_scale_ratio: 1.25
  actual_capacity_ratio: [0.8, 1.2]
  accurate_fraction: 0.8
privileged: {enabled_for_F: true, enabled_for_actor: false, feature_memory: true, schema: generated_and_frozen}
collection:
  sources: {rule: 0.5, policy: 0.5}
  scenes: {E0: 0.20, E1: 0.15, E2: 0.20, E3: 0.15, E4: 0.30}
  rule_process_time: {transient: 0.20, motion: 0.30, load_release: 0.50}
learning:
  batch_size: 512
  lr: 0.0001
  gamma: 0.99
  polyak: 0.01
  updates_per_W: 0.00390625
  online_warmup_W: 8192
  extra_task_loss: false
audit: {every_valid_W: 100000}
budget: {initial_total_valid_W_including_P0: 20000000}
~~~

The full configuration must also include the scope of sections 6–8, templates, collision/limit checks, replay tiering, valid windows, and cache budget. The actual schema/dim/model hash is frozen after compilation without filling in the unverified D_p first.

The checkpoint saves network/target/optimizer, random flow, collection version, Replay index/sharding, scheduling balance, schema/model/estimator/ρ version and actual W. First, it supports full rollout boundary continuation; if any sub-step recovery is supported, all physical/driver/program states must be additionally saved. It cannot just restore the network and call it continuation of the same trajectory.

Record implementation_ready, coverage_ready, budget_completed, and validated respectively. It is only true if the corresponding evidence is available. What this article has completed is the implementation design, which does not change V2 validated=false, nor does it mean that V3 has been trained.

## 15. Document integrity and items to be frozen before implementation

This time the user confirms: The goal is to represent the result status, and the random parameters of the motor are not directly added to B. The logic chain, g13/x137, network skeleton, asymmetric FB, coordinates and zeros, randomization range and data usage principles are determined and implementation can begin. **Currently, not all configurations have been frozen and formal training can be started directly. ** The following differences indicate clear design direction and complete actual configuration/acceptance:

| Items to be frozen | Determined content | Must be delivered before official operation |
|---|---|---|
| F field registry | p blocks, source/timing, feature_memory, input isolation | shape, units, coordinates/reference points, scale, validity and extractor for each field; slot capacity and final D_p; corresponding F parameter amount and storage budget |
| Mechanical and Service Templates | P/D identity, fixed side mapping, E0–E4, wide travel and compliant clamping | Actual geometry/joint/collision list, legal range, initialization and loader; per-template CPU checksum target backend comparison, weld remains disabled if not calibrated |
| Acquisition/training manifest | Layering range, process duration, Replay probability, coverage conditions | Loadable complete configuration and ID list; actual condition coverage of capability file/error group, reserved capacity of each group, original points/history reconstruction and throughput memory check; 2.88M/20M is not covered as a coverage guarantee |
| Freeze Evaluation Specifications | Categories such as Hold, Speed, Torque, Response, Hindered Release, Switching, and Unseen Structures | Each type of query/target distribution, duration, error indicator, feasibility determination, number of repetitions, and success threshold; distinguish between visits/reliable calls/physical limitations, lock before training, can not see the results and then pass the line |

These are not reasons to add new networks or rewards. Fields and templates can be iterated in development, but the physical/record contract must be passed before formal P0, and the corresponding data and evaluation version must be frozen before formal training. The currently given numerical threshold is the starting point of the candidate project and does not mean that it has been verified by physical testing.

The status should be reported separately: `design_logic_ready` (the result representation logic of this round has been determined), `spec_frozen` (all the above configurations are implemented), `implementation_ready`, `coverage_ready`, `validated`; the former cannot replace the latter.
