# Design resolution of V3 zero position, connecting rod identity and motor parameters

2026-10-10. After independent discussion by the three high relay auditors, the main window finalizes and writes back to [V3 Embodiment ](V3 Network and Training Plan.md) and [Reverse Logic Document ](Motor Proprioception and Representation.md). This round modifies the design without modifying the production network or starting training.

# From Mechanical Identity to Unified Physical Outcomes

The two fixed sides are housing_link (P, housing/stator connection side) and output_link (D, output shaft/flange connection side); when equipped with a reducer, the output end is not equal to the rotor. Which side is fixed, world installation direction, simulation tree parent-child order or motor forward and reverse will not change the identity. M is fixed to the shell, the origin is the research joint, and +z points to the outer end of the shell rod.

Entity gestures corresponding to different motors raw qpos = 0 may indeed be different and must be supported and verified. First, distinguish between the original zero of the hardware, the zero of the URDF/MuJoCo model, and the geometric zero of this scheme. The original angle q_e on the output side of the first wheel has been known to be calibrated `q_c=s*q_e+beta` into a specification mechanical angle; q_c = 0 means that the two rods are deployed in a straight line. Speed/torque multiplied by s, action inverse conversion, limit conversion sorting, keep power consistent. The beta cannot be applied to the speed or torque; nor can the rotor angle/torque be directly taken as the output side quantity. The angle and torque are registered on the measuring side respectively; the existing output shaft torque is not multiplied by the rotor side encoder. The normalization request is first converted into torque by pressing S_c, and then changed direction/equipment coding; only when the equipment scale S_e = S_c is abbreviated u_e = s * u_c. History, Replay, and F-motion are stored in the specification u_c.

telemetry_adapter pipes hardware readings to q_c; model_adapter pipes simulation tree coordinates, axes, and joint refs to q_c. Fixed D may require tree map negation, but does not automatically imply hardware encoder negation. The two layers cannot be reapplied.

The first beta/s is known as a feature configuration and is not spelled directly to B. Unknown calibrations cannot be emulated to correct Actor/B; the interface rejects valid geometric results when necessary calibrations are missing. The robustness group is independently formulated after the unknown error, and it is not guaranteed that the constant zero bias can be identified in the short history.

# How Randomization Reflects Real Zero Differences

The implementation specifies two sets of tests/builds:

- **Same as raw zero, different beta**: The real model/initial state satisfies q_c=beta, the rod end position and gravity effect can be different, and the specification q and B input are correspondingly different. It only changes the display reading but does not match the actual posture and is unqualified.
- **Same physical posture, different coding convention**: fixed q_c/dq/physical output, inverse solution of each raw, standard input and physical motion should be consistent. This group is evidence of interface invariance and cannot be counted repeatedly as dynamic coverage.

The beta candidate is dithered according to [−π,π) eight sectors, s equal; the ordinary initial state is independently sampled according to the legal physical angle domain, and raw=0 is not permanently fixed. raw=0 subgrouping is only done when beta is in the legal range. An example of P parent body/D rotating child body can compile the output body's `R_y(beta_model)`, axis `tree_sign*y`, ref=0, and then transform the geometry, inertia and downstream structure as a whole; this structure is not directly applied to the fixed D. The model uniformly uses independent tree_sign/beta_model/qpos_ref, and each fixed side template is subject to relative attitude, speed, and power acceptance; the equipment uses encoder_sign/beta_encoder, and the number cannot be changed repeatedly. Canonical models plus real sensing adapters can also be used, but the two mappings must not be mixed. Non-zero refs enter the model map alone. Acceptance requires the same device q_e=0, rather than forcing all implementations to have the same q_tree=0; the device raw zero of the canonical simulation model corresponds to q_tree=beta_encoder.

Only fixed plane coaxial straight rod installations are suitable for single beta treatment; eccentric, non-coplanar and hysteresis/elastic transmission require different schemas. World tilt is another physical variable that cannot pass for zero-bit randomization. If the real stop is fixed to raw, then changing beta will change the physical stroke at the same time, and additional legality checks must be done; pure recoding will not increase the stroke.

## The input of B is chosen according to the result semantics

**The user has confirmed that what this round wants is the result status characterization: retain g13 and do not increase the motor model or dynamic parameters. ** The judgment criterion is not whether the parameter is static, but whether the selected result needs to distinguish it:

| Information | First Round Go | Reasons |
|---|---|---|
| Rod Length, Normal Limit, q_c/dq/tau, Local Speed and Recent Acceleration | B/Actor/F | Define Geometry — Motion — Output — Response Results |
| Known beta, direction, unit/drive adaptation | Characteristic and command adapter, metadata | Unified physical meaning, no network relearning number required |
| Declare quality, COM, inertia, capacity, T, delay, resistance/armature | Known context of Actor, F, upper layer explicit feedback | Change the method and ability to achieve the same result |
| Actual hidden load/drive parameters/queue | Training F | Actor/B not directly observed |

The same g with a capacity of 3 or 6 N.m. can be obtained with the same B; The upper level sees a difference in abilities from known_drive. The "half capacity" of the current device is intended to be a fixed absolute power rectangular target, followed by an existing r(g) query. If cross-referenced samples are to be used for their respective tau/C search capabilities, C cannot be found in g, and the existing FB cannot be claimed to have such semantic results; At that time, the result definition will be re-defined.

B16 is not a lossless encoding of all parameters, nor is it an estimate of instantaneous available capacity or contact force. Adding invariant parameters to B also increases the configuration separation of the global reference distribution; only explicit query gains are increased, and just because F can read true values ​​does not mean that z contains the distinction.

## This round of motor randomization additions

Previously only randomly driven around fixed 6 N · m requests, now added to the declared output capability slot to test local multiplexing at different capability levels:

- C0 = 3/6/9 N.m. equivalent; S_req=1.25C0; Real symmetric capacity C = C0 x Uniform(8,1.2). S In excess of the maximum real capacity, each tranche has saturated requests.
- T=5–20 ms, delay=0–10 ms, damping=.01–.08, friction=0–.08, armature=.001–.006, follow the prototype range.
- 80% of the drive group accurately declares the actual constant; 20% declares the nominal value, the actual value still changes according to the range, and the hidden difference is only given to F; the queue is always only given to F. The request scale S is a known and effective interface configuration.
- The torque in B still uses a fixed global SI scale and cannot be changed to each motor's own utilization. known_drive directly feeds back to the upper layer along with the source/significant bit.

These are synthetic output side validation models, not three validated commodity motors. The first round does not add temperature rise, electrical model, speed-torque envelope, backlash, or gear elasticity at the same time; it does not claim to support any motor because of random parameters. The limitation of weak motors under heavy loads is valuable data, but the insufficient capacity of the rule collector must be listed separately, which cannot all be interpreted as insufficient motor capacity.

## This round of documentation and project status

Fixed fixes from the last round of audits have been written back into the implementation: collision checking, reaction API and timing, weld enablement threshold, F feature_memory, endpoint/integration fields, rule capability calibration, condition coverage/E4 active threshold, explicit replay sampling probability, and row-by-row discounting. Network branches, hidden layers, activations, z16 and loss remain unchanged.

The range, controller initial value and coverage threshold given in the document are the starting point for development and are subject to independent physical and acquisition testing for acceptance. The field registry/model manifest still needs to be frozen by the implementation, and the complete D_p is not filled in out of thin air. The original audit report is a historical finding, and the status update is subject to this revision.

Final acceptance: After cross-checking the revised draft by three high relay auditors, the directional review is conducted through device/model mapping, request scale, F action, measurement side, error group and goal grouping for consistency. Add [Zero CPU Fixture] (../audits/v3_20261010/check_motor_coordinates.py) to the main window and run it again to verify the attitude difference with raw zero, the same physical state across symbols/zero equivalence, ref/limit/power and request to trigger limiting; this does not replace the production template and training acceptance.

Document integrity check: the result marking and input boundary have been determined; Field registration forms, actual templates/freezing criteria still need to be developed, as detailed in section 15 of the [V3 programme] ](V3 Network and Training Plan.md#15-document-completeness-and-items-to-freeze-before-implementation). No design logic has been frozen through what is called full training specifications.
