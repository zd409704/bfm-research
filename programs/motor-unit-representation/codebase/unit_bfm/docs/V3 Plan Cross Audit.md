# V3 network and training implementation plan cross-audit

Date: 10-10-2026. Object: [V3 Network and Training Implementation Protocol ](V3 Network and Training Plan.md). Status: Tripartite independent audit, second round of mutual challenge and main window review have been completed. This document retains the first round of audit facts; subsequent document revisions authorized by the user have been implemented into the V3 program, see the status update in the last section, which still does not mean that V3 has been achieved.

1. Conclusions and borders

** The direction is established and the network skeleton does not need to be changed; the current solution cannot be recognized as a complete specification that can directly start full training, and there is no sufficient actual test evidence for randomization. ** The main issues discovered in this round are physical modeling, privileged power extraction, memory state, acquisition and Replay contracts, rather than hidden layer size or FB loss itself.

Maintain determined information boundaries: Actor does not read unknown dynamic load truths; F reads actual randomization parameters and boundary states during training; B uses g13 without adding raw historical inputs. Maintain dual-branch feedforward network, width 256, activation, z16, and existing FB/orthogonal/actor goals without increasing GRU, ancillary losses, or mission rewards. The F supplementary input field increases the number of its first layer parameters and still belongs to the input variation.

The V3 module has not been implemented. This article strictly distinguishes between: the migration risk of old code, the unclosed interface of the scheme, the actual measurement problem of relying on APIs, and the theoretical limitations of low-rank expression. No V3 training, GPU physics controls, or bipedal experiments were performed.

# 2. Randomization covers physical processes, first of all to ensure that the generated body is legal

# # 2.1 Wide stroke cannot be justified by “no contact”

The P/D of the old [mechanics.py](../mechanics.py) were square rods that met directly at the joints, lacking a physical hinge to give way. The CPU independent distance detection found that the two rods penetrated about 18.64 mm when q=1.2 rad; there was no P/D contact in the default collision set. After explicitly adding this pair of collisions, the same pose generates contact. The reasons include parent-child rigid body collision filtering; some old characters also have contact turned off.

V3 already requires hinges to give way, but acceptance must independently enumerate the geometry pairs that should be checked, including parent-child pairs that are filtered by the engine, rather than just looking at ncon, solution stability, or whether the model compiles. It is necessary to save the collision whitelist, filtering reasons, distance, tolerance, and angle sweep results. The combination chain also needs to scan adjacent poses and boundaries. The safe interval under a certain adjacent pose cannot be regarded as the safe interval for all scenarios.

Fixing D is still a new project: it is necessary to keep the motor identity of P/D unchanged and clarify the q/dq/u/τ/limit symbols after the model tree is reversed. The minimum acceptance is to mirror the local geometry and response of the two fixed sides and check that the sign of the power τ·dq is consistent; simply changing the character name to "Fixed D" does not work.

# # 2.2 2.88 M is the starting point for collection, not evidence of overlay establishment

144 geometry/constraint groups, 4/3/4/3/6 rounds each for E0–E4, does yield 2.88M 100 Hz, 10 s round transfers. But the lower aggregation limit of "20 episodes per operating case per ξ gear" may be filled by very few structures. It cannot independently prove that the remaining structure has load retention, bidirectional movement and release recovery.

On the other hand, if 20 episodes are changed to achieve each configuration and each working condition separately, even if all ξ files are accessed in each round, only this lower limit will require at least 14.4M transfers, and other cross-conditions have not been calculated. You cannot maintain the original budget and claim to have ensured that it will be sufficient group by group.

It is recommended to freeze the two-level list:

- **Core items that must be covered by configuration**: geometry/limit group, applicable working conditions, fixed side, entry and exit of legal ξ area, forward and reverse motion, achievable low-speed loading, and loading release. Each item holds an independent episode number, actual number of steps, and gaps.
- **Cross-configuration coverage**: Eight installation directions, mass/inertia gears, external force points/directions, adjacent phases, etc. use explicit cross lists to report which combinations are not adopted to avoid binding the structure to the fixed side, installation or load.

The full Cartesian product is not necessary, but the marginal histogram of each variable cannot be treated as a joint overlay. 2.88 M is retained as the lower bound of the initial acquisition; `coverage_ready` must read the conditionalized debt, if it is not full, it is appended, and the budget and overlay are reported separately.

# # 2.3 The rule controller must be able to generate the desired state

The old hold PD is `6*(q_ref-q)-0.6*dq`. Independent CPU review: D rod 2 kg, 0.45 m, q_ref=1 rad, q≈0.596 rad after 2 s, the error is about 0.404 rad. The gravity moment at the target is about 3.715 N·m, which is lower than the 6 N·m motor capability; however, this PD can only give a maximum of about 0.33 N·m to maintain the threshold, so it does not have the ability to carry the load within the threshold.

This is **collector deficiency**, not that the motor cannot reach it; saving the failed trace is valuable, but it cannot make up for the missing successful load holding data.

Capacity calibration of the rule program should be done before P0. PDs with well-documented gravity/known-load feedforward, integral anti-windup, or inertia-configured PDs are allowed; they only generate behavior transfers and cannot be lost as an Actor teacher, nor can they spell their privileged input to an Actor. Record "mechanically infeasible", "driving capability limited", "rule failure" and "numerical failure" respectively, and do not delete the coverage target just because the rule cannot be reached.

### 2.4 E4 requires actual active count

The fact that the scene is E4, the presence of the subject and the proximity reference is not zero does not mean that the combination effect has been captured. At least separate records:

| Process | Actual quantities to be checked |
|---|---|
| Contact load bearing | Solve for normal force/impulse and duration of effective contact |
| adjacency driven | adjacency actual dq or window displacement, not reference amplitude |
| Adjacent stall force | Small displacement but real driving torque and transmission reaction force, single row category |
| Bilateral constraint force transmission | The reaction force from a clear source on both sides continues to be non-zero, rather than the existence of two clamps |
| Release and recovery | The established load, actual unloading, and subsequent continuous responses are completely saved |

Thresholds shall be given at the base of the sensor/value noise, by the force rectangular capacity or by the weight scale, and shall be written to the configuration before P0; It cannot be relaxed to “pass” after seeing the results. The main observation duration follows the starting point of the programme at least 0.5 s. Preparation, proximity and failure frames are retained but cannot be offset by the amount owed for the target active category. E4 30% Configure step numbers and 25% of the target on both sides of the group must be reported separately for actual conformity.

## 3. F’s privileged information is basically available, and the extraction method must be separated by source.

| Information | How to obtain | Must pay attention |
|---|---|---|
| Actual mass, COM, inertia, damping, friction, armature | Effective model/per-world array | Can't substitute random range or unsynchronized CPU nominal model for actual value |
| Project drive state | τ, capacity, time constant, delay, ring, clock | is not an actuator state automatically exported by MuJoCo; current model nu = 0 |
| Support/Loader | Record the current state of points, forces, force couples, programs during loading | Combined forces cannot invert each source and must be saved before addition |
| Contact | Contact geometry + solution multipliers are converted by contact-force API | Contact coordinates, symbols on both sides, reference points, effective constraints, and solution time must be retained |
| Tree connection wrench | cfrc_int of post-constrained RNE, verified and reference point transformed | Includes the resultant effect transmitted through the tree edges, not equal to some external contact force or motor τ |
| Non-tree connect/weld constraints | Physical effects mapped by constraint type | All efc_force cannot be directly treated as N/N·m |
| Contact slip | Difference in velocity between two rigid body points at the same contact point | Calculated amount, no general "direct read slip" field |
| Public motion, gravity direction | Simulation pose/velocity and gravity projection | Only for F; does not claim that the motor body is observable |

"Load truth" is not a unique, fixed equivalent inertia scalar under any topology. F can obtain the actual physical parameters, states, and sources of action; they collectively determine the load response without having to be forcibly pressed into an equivalent load label. Geometric, quality, or simulation values are available and do not indicate that the Actor is readable on a real machine.

### 3.1 Verified API and coordinates

Local MuJoCo/mujoco-warp are both 3.8.1, mjlab is 1.4.0. Warp has publicly provided `rne_postconstraint` and `contact_force` with force/torque sensor paths; there is no need to assume that the GPU does not have these APIs. However, the current V2 call chain is not fully exported.

The CPU needs to execute `mj_rnePostConstraint` in the same solution state, Warp uses the corresponding public API, or confirms that the sensor that will trigger it is configured and enabled. The existence of the field does not guarantee that it has been updated; when the CPU minimum model has no sensor, the forward value may still be zero, and the ordinary RNE intermediate value of Warp cannot pretend to be a post-constraint reaction force.

The order of `cfrc_int` is **torque, force**, world direction, with the root subtree COM as the moment reference point; the order of `xfrc_applied` is **force, moment**, the latter uses body COM as the reference point. The transformation of the tree connection at the study motor origin O_M is:

```python
C = d.subtree_com[m.body_rootid[b]]
T_C, F_W = d.cfrc_int[b, :3], d.cfrc_int[b, 3:]
F_M = R_M.T @ F_W
T_M = R_M.T @ (T_C + np.cross(C - O_M, F_W))
```

According to the convention that the parent acts on the child; the reverse connected edge is negative as a whole. To study the joint origin, use joint anchor points or special sites. You cannot directly use the P body origin. The difference between the old model and the old model is P rod length.

The contact API returns force and torque; the CPU contact coordinate to the world uses `contact.frame.reshape(3,3).T`, which acts positively on geom[1] and takes negative effects on geom[0]. Then move the torque from the contact point to O_M. Contact, load, drive, and tree connection have overlapping effects, and these fields cannot be added again as "total external force".

### 3.2 Counterexamples of weld must serve as implementation thresholds

The main window reproduces independently: the free sphere is connected through the world weld, and when 2 N·m is added and torquescale=1, the constrained physical moment is obtained by both the angular momentum balance and `Jᵀλ` -1.384615 N·m; the post-constraint `cfrc_ext` minus the explicit external force is obtained by −2.769231 N·m. This special case of torquescale=2 happens to be consistent and the general case cannot be accepted on this basis.

This indicates that there is an inconsistency in the local estimation of the extraction path,** which does not indicate that the power score of the neld is necessarily equally incorrect.** Force/torque sensor relies on the same path and cannot be used as evidence of full independence.

The minimum correction is to establish an extraction contract for the tree, connect, and weld respectively; the rotation constraint of weld requires correct spatial Jacobian mapping, torquescale, and attitude error handling. `J_rows.T @ λ_rows` can directly give a definite generalized role to the source, but it cannot arbitrarily and uniquely invert the complete space wrench in the under-degree-of-freedom system. If the closed chain affects the reaction force of the tree, the corresponding rigid body balance needs to be corrected simultaneously; it is not possible to fix only one field.

The reversibility of the chain of closure shall not be marked as a genuine and effective privilege until the independent/angular momentum balance has been achieved. A soft-stringed path can be developed first, but the unadopted weld category cannot be marked as covered. CPU/GPU Consistency and independent physical balance must be checked simultaneously.

### 3.3 The solution time cannot be confused

In the current implicitfast path, step is solved first and then integrated; q/time is advanced when returning, and the contact point, force, and geometry caches can still be solved before integration. Subsequent forwards will cover them again. The contact force of recalculating different actions under the same q/dq is also different, so the solution result acting on u_t cannot be backfilled as p_t before the action.

The order of implementation shall be fixed as:

1. Freeze the boundary x_t/p_t before issuing u_t; the contact/connection function adopts the previously completed interval record, with timestamp and valid bit.
2. Sub-step update driver, load, solve, immediately copy the force, point, reference attitude and time of the solution, and then enter the next refresh.
3. The current geometry and the completed interval force are stored separately; the new geometry and the old contact number cannot be blindly matched.
4. Assemble p_next; if there is no interval before reset, the recorded time scale is invalid and the next round result will not be borrowed.

# 4. History, B and F inputs must form a reconstructable closed loop

The dimensions of g13/x137 and the local endpoint kinematics formula pass the check. The endpoint change rate is a quantity relative to the motor rotation coordinate system, not the inertial system motion. The P-terminus is fixed in M ​​and does not require constant zero-repeat features.

The five 100 Hz velocity endpoints span 40 ms, and the straight line fit approximately corresponds to the midpoint of the window when acceleration changes linearly, with a lag of 20 ms. It should be called "the recent acceleration response of causal estimation" and the time caliber is recorded; it cannot be called the current instantaneous true value. B does not eat history directly, but this input already carries processed history.

# 4.1 F also needs the memory of the feature updateer

The slow history of x137 takes even boundaries, the fast history has no dq; a single acceleration fit cannot recover the discarded odd boundary velocities. Algebraic counterexample: the last five velocities `[0,0,0,0,0]` and `[0,.1,0,.1,0]`, the slow sampling endpoints are the same as the current fitted slope; after appending the same zero velocity, the next fitted slopes are 0 and −2 rad/s² respectively.

This retrogressive summary is generally not sufficiently retrogressive,** not having constructed two complete MujoCo tracks with exactly the same x/p**. However, the document cannot declare F to be in a strict Marko state by simply "x with history".

It is recommended to explicitly add **feature_memory** to the F-specific input: the telemetry ring buffer needed to generate the next x/g, valid bits, real time intervals, slow sampling phase, and the currently outstanding interval summary accumulator. A normalized expansion of the 22 original boundaries can be used as an easily verifiable contract, and then compressed when proof is available; without increasing the length of the Actor/B history or hiding the network. It is an additional memory on the training side, not an unknown physical truth value, and should be named separately from privileged blocks such as actual_load.

# # 4.2 Points must be saved for the original record

The program already requires real sub-step points, but the persistence list is not clear enough. You must save `tau_endpoint`, `tau_integral_previous_interval`, `u_integral_previous_interval`, interval duration and valid bits independently; the slow history is divided by the integral of the two completed intervals and the total duration. The average value of the endpoint cannot recover the torque changed during the process, and it cannot be repaired by offline recalculation after leakage storage.

All variable fields also need to specify units, scales, coordinates, time meaning, default values, and mask; actor rigid body/drive fields, all p-blocks cannot just be written "normalized". The actual p-dimension must be generated after these fields and templates are frozen. D_p = 512 is currently just an example of the number of parameters.

# 5. The FB mathematical backbone is correct, but the sampling and implementation details need to be closed

### 5.1 No need to change the loss or network skeleton

Actual number of parameters after replacing only the input layer: Actor 207,617; B 74,000; Actor+B 281,617. Each F is `211,728+512*D_p`, which is 473,872 when D_p=512. Dual branching, 256 hidden width, activation and z16 are all maintained.

The FB scalar loss is consistent with the independent formula; the target stop gradient, the double F successive average, the Actor dot product min, and the reserved action gradient are all established when the F parameter is frozen. Rule control data entering Replay is not equivalent to increasing reward engineering, and querying preferences does not enter pre-training losses.

There is a reoccurring pitfall in row-by-row termination discount migration: the old interface multiplied by `[N]` will broadcast along the **reference column** of `[2,N,N]`, which should correctly be along the transfer row. V3 explicitly uses `[1,N,1]`, rejects ambiguous shapes, and tests for mixed termination/truncation and gradients. Old V2 used the scalar .99, so this is not a V2 termination error that has occurred.

### 5.2 Replay needs to clarify "current conditions" and "posterior filtering"

The hierarchical field must indicate whether to take t or t+1. By default, the current y/u knowable conditions are used to select the transition; all true successors are retained within the same condition. If the posterior results such as "recovery is successful" and "the next acceleration is large" are retained or re-collected, the conditional successor distribution may be changed in a random transition or incomplete state; such deviations should not be unconditionally claimed to be inevitable in a complete deterministic state. The synchronization reference ρ cannot automatically repair such deviations.

It is recommended that the sampling contract clearly state that the → geometry/limit configuration of the source → working condition is uniformly and truly transferred within the → current boundary cover → layer. The probability of each layer, the fallback of empty groups, and the retention policy can all be tracked; the target stage can belong to the current program state, and the success tag cannot quietly replace it. The rare procedure keeps the diagnostic library separately; access to Bellman's extraction is verified separately. Query references are generated with the same distribution version as g_next.

In the old Replay, the average episode is averaged and the length of rounds 1 and 9 is about half each, and the probability of each transfer is about nine times higher for a short round. If the new realization remains the same, the longer procedure would change the implied weight. Checks must be made with small man-made reservoirs of known probabilities. The choice of the episode and the timing itself is not an illegal distribution. The error is that it is not intended to introduce such weights, misalign or not coordinated with reference distributions and coverage targets.

# # 5.3 Global ρ, immutable configurations and explicit limitations of z16

Fix the same z, aggregate real subsequent visits according to the length/limit configuration that is invariant and distinguishable within K rounds. Only this configuration is reachable, and a K-order identity matrix is ​​formed after normalization. The corresponding aggregation matrix of FᵀB has rank at most 16. When K=144 and the equal-weighted Frobenius metric is used, the best relative error lower bound is `sqrt((144−16)/144)=0.942809`.

Here 144 is the planning quantity; the real K must be represented by the unique `(L_P,L_D,q_min,q_max)` statistic in the manifest that has positive access quality and can be distinguished by g, and cannot be directly replaced by the model ID or the number of installed variants. The script calculates the mathematical bound assuming K=144 and does not measure the actual training error.

**This is not a 94% control failure rate, nor is it a general lower bound on raw FB training loss. ** Non-uniform weights, continuous parameters, and specific task control need to be analyzed separately. But it clearly states that increasing the amount of training cannot allow z16 to accurately encode this global separation structure. Sampling with the configured goal does not eliminate separation in global reference items.

Keeping the network with the current FB backbone by user constraints, first testing configuration aggregation error at fixed z, per-configuration dynamic query/control and B differentiation of local differences. Passes may not be declared based on the overall effective rank or the pool average. If the results show that global configuration isolation occupies the main representation capability, "conditional FB/different representation definition" should be regarded as an algorithm choice that needs to be discussed separately. It cannot be changed implicitly in this audit, and there is no guarantee that the current solution will necessarily support any form.

## 6. Prioritization and verification boundaries before development

| Sequence | Deeds/evidence that must be completed | Impact |
|---|---|---|
| 1 | Hinge yield, independent collision pair scans, fixed D notation and geometry | Deciding which wide travels are real and legal |
| 2 | Sources of separate forces/reactions, weld calibration, solution times, and reference points | Determining whether the privileged quantities of F are credible |
| 3 | feature_memory, integral original field, field-by-field schema | Determines whether the transfer can be reconstructed and whether the state condition of F is closed |
| 4 | Rule capability calibration, condition coverage table, E4 activity criterion | Determine whether the required motion and load are actually generated |
| 5 | Replay probability, hierarchical time attribution, row-by-row discount | Determine these data to enter FB with correct semantics |
| 6 | Small-scale complete training and configuration-by-configuration evaluation | Observe the actual local calling capability under fixed z16, and then expand the budget |

Physically legitimate but uncontrollable blocking, carrying and release processes remain valid data and should not be deleted because they are not on target. Numerical explosion, penetrating assembly or error privilege fields cannot be included in the valid coverage. These two types of failures must be separated.

# 7. Audit Execution and Evidence

A local multi-agent orchestrator skill, three independent read-only CLI sessions, auditing randomization/mechanical, network/learning/replay, privilege extraction, respectively. The actual session turn_context confirms the inheritance model gpt-6-astra, reasoning strength high; the second round reads the first round report and checks the main window counterexamples. Existing extraneous child session is not used.

The main window saves [Reproducible CPU scripts and results] (../audits/v3_20261010/README.md): network input substitution count, terminal difference, historical counterexamples, discount broadcast, collision filtering, tree reaction force, weld, rule control and Replay. A total of **8 passes** for the current V2 formula/contract/learning test. The agent's read-only sandbox was unable to run a learning test due to temporary directory permissions, and the main window has been independently rerun; it still only verifies V2 existing paths.

The CPU test covers specified small models and operators and does not prove GPU batched implementation, complex closed chains, V3 leakage-free, successful training, or 100 Hz latency. The adequacy of complete randomization must still be demonstrated by actual coverage, gradient usage, and freeze call results after implementation.

Original sessions, native reports and round-by-round acceptance records are saved in a project-local relay control directory. The first round of startup failed because the session database was read-only; after running the normal permission process, it was interrupted by an environment switch. It was verified that the original process exited and the same session was restored. Log exceptions and recovery processes are recorded separately, and interruptions are not recorded as audit completion.

### Second round of ruling and delivery status

All three auditors completed two other reports and added a short CPU inspection. (a) The main findings remain; The following extrapolations were explicitly denied or narrowed:

- Old adjacent frequency **No missing multiplication by 2π**: environment has converted Hz to rad/s, and kernel is calculated based on angular frequency. It is recommended to only unify the naming of `frequency_hz` / `omega_rad_s`, and do not list the correct implementation as a bug.
- The independent kinematic example of fixed D supports existing formulas and power mapping; it is not a production template, wide stroke or closed chain acceptance. "Negate All" only applies to the measured coaxial reverse tree and cannot be generalized to all installed generic transformations.
- Historical tests only prove recursive information gaps in summaries; script annotations have been corrected to avoid claiming to be fully proven true y non-Markov.
- The weld counterexample for the local version with the given constraints does not extrapolate to all tree reactions or dynamics integration errors, nor can it be fixed by a simple uniform division by 2.
- P/D internal contact can have reasonable semantics without counting offload statistics; load statistics filtering and engine collision filtering must be distinguished.

During the first round of audit delivery, only new reports, CPU verification scripts/results, and relay records were added, and the original plan remained unchanged; subsequent document changes are described in the next section. The production code, network skeleton, and training weights are unchanged, and design revisions cannot be automatically recorded as implemented.

# Revision of the user-mandated programme (2026-10-10)

The three parties further discussed the boundary between the zero position and the motor parameter of B. For the conclusion, see [V3 Zero Position and Motor Parameter Design Resolution ](V3 Zero Position and Motor Parameters.md). The V3 scheme has been written into Section 3 Coordinate/Calibration/Privilege Extraction/Recursive Memory, Section 6 Zero and Motor Family Randomization, Section 7 Rule Capability Calibration, Section 8 Traceable Replay Probability, Section 9 Discount Shape, Section 11 Conditional Coverage and E4 Activity Criteria. Reverse comb the document sync information boundaries.

B Retain g13, unified physical angle input; The power is known to be visible to Actor/upper, and the actual hidden condition is F. Using the new requested scale S = 1.2.5C0, the reverse of the old fixed 6N.m here is still historical migration evidence, not a new configuration description. Weld disables the template before calibration. (b) Fixed D, complete physical generation, GPU and training still require acceptance and inspection; The limitations identified in this report have not been automatically adopted by the modification of the text.
