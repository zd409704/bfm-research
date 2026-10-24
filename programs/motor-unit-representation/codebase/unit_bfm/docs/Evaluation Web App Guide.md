# Local review page

This tool converts the executed frozen weight evaluation into a manually operable local web page. The existing `diagnose_motion`, `evaluate`, `evaluate_switching` and `random_atlas` will be used without modifying the training loss, network, randomization or old evaluation results.

# Start

Run in the root directory of the repository:

```bash
unit_bfm/.venv/bin/python -m unit_bfm.eval_web.server --port 8766
```

The browser opens `http://127.0.0.1:8766`. A Python backend is required to run the weight assessment, and the emulation cannot be started by double-clicking on the HTML. The page does not depend on an external CDN. Select 8766 by default to avoid the 8765 already occupied by the current machine; other idle ports can be specified via --port.

## Operation and evaluation methods

1. Select the V2 checkpoint and evaluation project and click Run. One evaluation process is executed at a time, and the progress log can be viewed or stopped; existing weights and evaluation files will not be overwritten.
2. Select existing or newly completed assessments, data files and cases in the results area. Task type and switching period can be used for filtering.
3. Play, pause, and drag the time bar to view the actual saved planar mechanism animation of qpos, as well as q, dq, τ, u, environmental force and contact curves. The query target is shown in gold, and the parsing reference that can be matched is overlaid in gray.
4. View the current z-coordinate, download the original trajectory and metrics, or play an existing MuJoCo video. The z-coordinate is not named as a fixed physical axis.

| Project | Same methodology as original assessment |
|---|---|
| Nominal persistence query comparison | 8 q targets × 4 initial states, using complete target B encoding, bonus points, random z, a total of 96 trajectories; last 1 second retention error |
| Cross-condition query and parsing comparison | Each controller 8 structure × 32 tasks × 4 initial states, 1024 trajectories each; the same seed and task, the two controllers execute respectively |
| Original switching panel | Nominal R0 point target query + four additional structure random z pairs; 5 switching cycles × 16 initial states, a total of 400 trajectories |
| Reward query switching | Nominal R0, ±0.6rad reward query, fixed/40/80/500/1000ms, 16 initial states each, 80 trajectories in total |
| Random z-Graph | 8 structures × 256 z × 2 initial states with a total of 4096 trajectories; view coverage, saturation, limit and contact |

All trajectories 5 seconds, 100Hz control, 1kHz physical. Use frozen network, deterministic actor mean, no gradient update. The original switch and the reward query switch are displayed separately, and the fact that the latter is an ex-post diagnosis in the original study is retained. The parsing control is not qpos-RL, and the error of keeping the end segment cannot be mixed with the error of the entire switching process.

## Results and reproducibility

The new output is located at  `unit_bfm/artifacts/web_evaluations/<timestamp-and-job-id>/` . job.json records the selected weight, SHA256, review project, source hash of the call, status and time;  log retention standard output and errors. Only fully successful assessment groups enter the Result Selector, retention logs of stopped or failed tasks and existing partial files.

Inspection points are listed only from local training catalogues with V2 version; Checkpoint/mode files with learner status are supported, and the V1 or only Actor/B package is wrongly exported as a directly operational training check point. The historical results are identified separately, and the rotation of the upper weights does not alter the model to which the selected historical results belong.

The plane animation is calculated by MuJoCo forward kinematics from the saved qpos and XML in the same directory, and the existing motion is played back without re-simulating or forging the motion at the target angle; the curve comes from the original y. Geometry and position use this structured XML to show that the random dynamics of each world are restored. The time starts from 0.01 seconds of the first completed control interval.

Physical error in each case follows the original assessment definition, with saturation/limitation/exposure statistics being only observational indicators and no ex post facto threshold for success. The randomz case has no objective and does not give it a false tracking error. The panel is marked SIM_PRIVILGED and candidate for unaccepted status.

The service listens on 127.0.0.1 only; running requests come from the same origin webpage. The evaluation is performed in an independent subprocess, and the browsing history and charts can still be used; running the new evaluation requires the existing CUDA simulation environment of this project, and browsing the old results only uses CPU reading and positive kinematics.

## Real-time manual perturbation: recalculate actions on the fly

Expand "Interactive Simulation", select the frozen weights above, the connection roles R0–R3, the existing query behavior, the target and the initial state, set the physical attributes for this time and click Start. It uses CPU MuJoCo and the existing CPUUnit and does not require CUDA; 100Hz control, each control contains 10 1kHz physical steps, and the history follows the original History. The wall clock progress is affected by the machine load, and the physical step size does not change with web page polling. This is an independent physics experiment, not pasting a perturbation arrow to an old replay, nor retraining weights.

During operation, select the P/D side, World Fx/Fz, Attach My, Point of Action and Duration, and click "Apply a Perturbation". The server arranges the events in the next control interval, and the real implementation is added to the two-stroke physical model; the 50ms cosine edge is consistent with the training external force. The force point is the ratio from the starting point of the corresponding rod to the end; the additional My is a pure force couple, and the torque generated by the force point is calculated at the same time physically. The P of R0 is fixed, the force applied to P may be absorbed by the support, and it should not be expected that it must cause q to change. The allowed amplitude of the interface may exceed the training coverage and the recovery cannot be claimed in advance accordingly.

Advance three branches with the same initial state/parameters at the same time:

1. Closed loop: Freeze the Actor to receive the actual disturbed state and continuous history, and re-output the action every 10ms; z is fixed.
2. Action playback: External disturbance is also received, but the action generated by the undisturbed branch is used at this moment, without modifying the action in its own disturbed state.
3. Disturbance-free reference: without manual external disturbance, run the same frozen Actor to generate playback actions and disturbance-free trajectories.

Gray shows the second branch; blue/orange shows the first branch; the red arrow shows the average manual disturbance in the 10ms interval, and the light red interval of the curve shows the start and end of the event. When the perturbation is removed, the arrow disappears and the response remains. The feedback correction effect is compared through q/dq/τ/u, the target error and the q RMS of the full run segment of the two branches relative to the disturbance-free reference. Action playback still has established drive and physical response, not qpos-RL or PD baseline; passive swingback is not enough to prove the learned anti-interference.

"Pause simulation" freezes the control clock and history, and the disturbance in the pause is discharged into the next simulation interval;  "Single step 10 ms" is only available when pausing, each time advancing one control interval and 10 physical steps, you can observe the disturbance, feedback and motor response frame by frame;  "Continue" maintains the current state;  "Stop  and save" preserves the y, qpos, work, query z, XML and events of the three branches, and does not overwrite the old results. Save to  `artifacts/web_evaluations/<time>_live_<ID>/` . After refreshing the results list, you can view the closed-loop/action playback and external disturbance as normal playback;   `reference/`  saves the original results of the third branch. The real-time simulation is still advancing  during the viewing history. Clicking "View Live Screen" or spoofing will switch back to real-time.

The real-time actor still uses the SIM_privileged input; its immunity cannot be directly equated to the deployment capability of only motor telemetry. See [Status Discussion ](Unit State and 3D Randomization.md) for the difference between two-sided labels, intact status, 3D observability, blocked, and active force.

## Customize physical attributes, limits and seed sampling

The following fields can be set in "Physical Properties and Randomization of this Experiment"; unapplicable items are hidden according to the connection role, the configuration is locked after startup, and manual external interference continues to be available. Changing parameters requires stopping and starting a new experiment. The original batch history evaluation entry still uses the original protocol; these settings apply to interactive simulation.

| Groups | Configurable content | What the network receives |
|---|---|---|
| Structure on both sides | P/D length, base mass, counterweight ratio and position along the pole | Corresponding nominal m; Center of mass and inertia are compiled by real geometry, not randomly filled independently |
| Physical limits | Motor upper and lower limits, within [-π, π] and stroke ≥ 0.1rad | Actual known limits in m, and the distance calculated based on the current limit; normalization still uses the original training fixed scale |
| Real dynamics | Density magnification of each rod, motor damping/dry friction/armature, ground friction, simulated gravity size | Do not fill in these random real parameters into m; density scales mass and inertia at the same time |
| Drive | Actual torque capacity, response time, 0–10ms integer delay | The command is still nominally 6N·m normalized, and the nominal capacity/T is still 6/.01; the network can only respond to these actual changes from existing feedback and history |
| Boundary initial state | R0 fixed parent side pitch; R1/R2 root attitude, speed, R1 position offset, R2 ground clearance | The current Actor still reads the corresponding simulation attitude/motion true value; this is not motor telemetry |
| R1 support | x/z/pitch stiffness and damping ratio of each axis | Support parameters are not input separately; physical damping is calculated based on actual mass and approximate inertia |
| R3 adjacency | target amplitude/frequency/phase on both sides, adjacency initial state q/dq | adjacency plan is not entered; only the motion/interaction that has occurred |
| Automatic external disturbance | Switch and random seed | Reuse the training amplitude, interval, duration and 50ms edge; only act on the two disturbed branches, the plan is not to input Actor |

The physical limit of the old training was fixed at ± 1.2rad, and the stroke was never randomized. The old webpage ± 0.8rad is the input limit of the evaluation target, which has been removed: angle reference support [-π, π]. The initial state q must be within this physical limit; the target can be outside the limit and clearly marked. Changing the physical limit is an off-training experiment, and it cannot be said that the training has covered it. Continuous joints with infinite turns of rotation are not in the current interface range.

“Sampling by Training Wide Range” to regenerate structural/kinetic and boundary parameters for the filled seed, preserving the current physical limit, the initial q/dq of the motor, and the selected target. The same seeds and roles get the same value; changing seeds gets another set. It multiplexes a wide range of uniform/log uniform marginal distributions and R2 initial mixed distributions, instead of extracting the old training world, it does not reproduce the course, role ratio or snapshot reset. "Restore Nominal Parameters" restores the physical settings and closes the automatic external disturbance, and the selected behavior and motor initial state remain the original value.

The physical settings are written to `session.json`, the actual model is saved as `model.xml` and the XML of each branch, and the nominal structure is saved as `nominal.xml`; the three branches use exactly the same actual model, initial state and driver. Each NPZ comes with `joint_limits`, which plays back target speed reduction, error statistics and limit line reading in this range. If the old file does not have this field, the old protocol ±1.2 will be used. m still describes the nominal structure under different densities, avoiding leakage of hidden random mass to the network.

Hold, brake and comply with the original frozen query. In the speed query, only the upper and lower limits in the original 0.15 rad boundary deceleration formula are replaced with the current physical limit, and `normalize(E[r B])` is calculated using the reference samples in the same frozen B and checkpoint; the same boundary is used for display and statistics. There is no change in FB training loss, fitting B, or updating the actor; the reference data is not covered by the new limit, and the effect of the call must be measured.

## Why is training flat and what can it explain?

The physical models of both V1 and V2 are bound to x-z plane and are not a 3-D training 2-D projection. All of the chains in `mechanics.Structure.xml()` are orbiting the y-axis; R1/R2 roots are only x, z-zided and pitch, R0 fixed in the near end, and the adjacent joint of R3 is also a flat-swidth chain. The g23 for observation and B is also coded only for flat gestures, motion and Fx/Fz/My; Random support, disturbance and proximity drive does not provide side-direction, roll/yaw movement.

This is to verify the range limit of the sagittal bipeds first. FB can model this constrained MDP, but training coverage and characterization cannot be extrapolated to three-dimensional connection conditions. An active hinge has only 1 DOF and does not require the absolute movement of its two rods and roots to be only two-dimensional. Future three-dimensional unit versions need to simultaneously expand the root/adjacent degrees of freedom, three-dimensional motion and force observation, inertia information, B result space, and corresponding sampling; simply replacing it with 3D rendering or rotating plane pictures cannot make up for dynamic coverage. There is no retraining or change to the old weights for this webpage revision.

# Query target and execution judgment

The page shows the target specified when generating this z, `targets`, `q_target`, `alpha` from NPZ and `nominal_query` corresponding to the evaluation. It does not use the z coordinate to back-solve a physical target. FB's reward points project the reward function into the learned behavior space. Multiple different goals/rewards may obtain similar z; random z does not have a naturally unique angle or speed goal.

The old `rf_v2_full/switching/metrics.json` did not save `nominal_query`. Its origin is confirmed by the registered history panel and `evaluation_source/main/evaluate_switching.py`: nominal R0 uses B(g*) and the rest of the structure uses random z. In addition, final freeze B is used to re-encode ±0.6rad on the CPU, and compared with all forward/reverse sequence pairs of the old `command_pairs`, the maximum coordinate difference is 5.96×10⁻⁷. Subsequent results with clear `nominal_query` will use this field first; when there is no field and no known panel source, it will be marked as "query source not recorded" and will not be automatically guessed.

| Query | Visualization | Judgment range of original evaluation |
|---|---|---|
| Hold / Angle switching | Golden dotted target pole, current q*; target, actual q and error; static reference dq=0 | Keep looking at the angle RMSE and residual speed in the last 1 second; switch to look at the full angle RMSE, including necessary transients |
| Complete B (g *) | The above angle reference, plus static gravity compensation τ; indicating the complete target constraints such as two-rod attitude, zero angle/linear velocity, zero contact/environmental stress | The current main indicator is still q error; it cannot prove that the complete g * has been achieved, and other states need to be viewed together |
| Speed ​​| The golden arc arrow next to the motor indicates the target rotation direction, and the numerical value and error display dq* after boundary deceleration | The original indicator calculates the RMSE for the nominal speed in a sample with a limit of >0.15rad from the target direction; the card shows the current instantaneous error |
| Braking | Ring and speed error of dq*=0, no fictitious stopping attitude is drawn | Speed ​​RMS at the last 1 second, and check the limit, saturation and positive work; the original evaluation does not have a complete success threshold |
| Comply | The golden arc arrow indicates the direction of τ*; displays τ*=bias+K(qref−q)−D·dq and the current error | Full torque relationship RMSE; qref is the spring balance parameter, not the q target that must be reached; this is not a contact force control indicator |
| Random z/Random z-switching | Clearly mark no preset targets, no target poles or target errors | Can only observe behavioral coverage, initial state sensitivity, contact, saturation and limitations, can not claim to have completed hidden tasks |

The arc length of the arc arrow is only a direction indication, and the value is read using cards and curves; the direction of torque does not guarantee the actual direction of movement. The target display switch controls the gold rod/arrow and target curve. When dragging the time bar, the current `q_target`, `phase`, actual state and z use the same index. The switching period 0 means that the first command is always called.

The golden rod is calculated from the original XML forward kinematics: copy the currently saved qpos, only replace `jnt_qposadr` of `motor` with q*, and the root and other joints are completely retained. It expresses the geometric effect of relative joint angles and does not command the root or the entire mechanism to reach a certain world coordinate. For full point targets, the additional τ shown comes from the same XML rest configuration bias force as the original `static_goals`; it is not a compensation controller calculated in real time under perturbations.

To judge "correct execution", you must first look at what variables are specified in the query, and then look at the corresponding physical errors and side effects; the z-bar chart or the appearance of movement are not used as the basis for success. This time there is no increase in training rewards, changes in FB loss, or addition of post-pass thresholds.

# 2026-10-01 Verification Record

- Through 5 semantic and path checks: random z not fictitious target, keep only the last 1 second of calculation, switch to full-trip target, speed exclusion limit interval, parent directory and symbolic link out of bounds are rejected.
- The actual evaluation was started in the name of final weight through the same HTTP running interface on the web page, and 96 tracks were completed. The output is at `artifacts/web_evaluations/20261001_024947_be35a7/nominal/`; all y and qpos of the three queries are element-wise consistent with the original `rf_v2_full/motion_panel/`.
- The trajectory APIs for maintaining, cross-conditional pairing parsing reference, switching, and random graphs all returned successfully; the JavaScript syntax check and the simulated Canvas drawing logic check driven by real trajectories passed.
- The original training core and original evaluation source code hashes have not changed. The web page only adds a new calling layer, data viewing layer and new evaluation output.
- The browser list was empty when the first version of the web page was verified, and the layout screenshot of the real browser and click acceptance were not completed at that time; the supplementary verification after this browser is available is recorded below.

## 2026-10-01 Target visualization supplementary verification

- 10 semantic checks passed, new coverage: relative angle target only changes the motor coordinates, retaining the root and adjacent joints; the angle between FK rods is consistent with q*; static compensation torque; switching target/phase; complying with τ* depends on the actual q/dq; random z has no target channel; unknown sources do not pretend to be point targets.
- Check JSON and frame indexes for full target, bonus hold, random z, speed, braking, compliance, point target switch, bonus switch, and random z switch using actual saved tracks. The target pole posture, phase, z and actual movement are all 500 frames, and random z does not generate tracking targets.
- The complete target, random z, velocity arrow, compliance torque relationship and 500ms angle switch have been viewed in the real Codex built-in browser; after clicking on the time bar to 2.52 seconds, the current command 2/2, q * = +0.600rad, actual q = − 0.414rad, error = − 1.014rad is displayed, which is consistent with the corresponding record. The browser did not report a page JavaScript error.
- Save [Target Visualization Screenshot] (../artifacts/eval_goal_preview.jpg), with gold as the target and orange as the actual far-end rod. The screenshot retains the switching transient, and this frame cannot be used to replace the entire evaluation indicator.
- Re-launching the new data interface once it has been confirmed that the service has no running tasks; No new training or changes of old weights were implemented.

# 2026-10-01 Real-Time Disturbance Supplemental Validation

- `test_live_eval` and `test_eval_web` passed a total of 16 inspections, including the consistency of the three branches before the disturbance, external disturbance not leaking to the non-perturbation reference, the interface displaying the average force in the real control interval, fixing the force on the parent side without falsifying motion, pausing a single step to accurately advance 10 physical steps, and pairing playback reading after saving. JavaScript syntax check passed.
- Finally, the V2 frozen weight completes the startup, disturbing, saving and trajectory reading of R0–R3 on the CPU. It verifies that the interactive tool is compatible with Category 4 connections, not acceptance of Category 4 control capabilities.
- Actual browser completes startup, pause, single step, scramble, resume, stop saving and select new result playback. Case `web_evaluations/20261001_043732_live_7fe259/` applies a pulse of Fx = 4N, 0.25 s to D at 1.28 s, saving 164 frames. The q RMS of the relatively disturbance-free reference of all running segments: closed-loop 0.042rad, action playback 0.400rad; this amount is the disturbed deviation, not the target error of relative q * = 0.3rad. Before the disturbance q is about 0.103 rad, there is a holding deviation; it is still in the motion transient when it stops.
- The new result playback is positioned at 1.32s, and the golden target, red actual disturbance, motion status and gray control are all displayed. The browser did not report JavaScript errors. Save [real-time panel screenshot] (../artifacts/eval_live_perturbation_preview.jpg) and [save trajectory perturbation playback screenshot] (../artifacts/eval_live_replay_preview.jpg).
- The source code of the original training, physics and main evaluation remains unchanged. The above-mentioned single short trajectory only supports the existence of feedback correction and the control effect, and cannot prove universal interference immunity, precise assurance holding, telemetry deployment or active force application.

## 2026-10-01 Parameter setting and limit review and verification

- 20 web pages/physical checks passed: Added coverage of actual mass/inertia consistent changes, hidden density does not leak into nominal m, custom limits enter physical constraints and observations, save XML reduction, velocity deceleration/statistics after changing limits, and seed sampling reproduction. The original test continues to pass.
- Using the final freeze weight, R0-R3 each advances 200 control frames with random parameters and [-0.8,1.6] rad limit, and saves and pairs and decodes; R3 additionally performs a speed query to check the encoding and display path after changing the limit. In all four cases, limited data were generated. This is tool validation and therefore no acceptance control capability.
- The browser actually completes the seed sampling, input q * = 1.4rad, limit [-0.8,1.6] rad, start, pause, continue to 15s, save 1,500 frames and 9 automatic external disturbances; for example, `web_evaluations/20261001_052153_live_c7c1b9/`. The number of limit, target, and triple branch frames re-read is consistent with the event. The example keeps the RMSE at about 0.794rad at the end of 1 second, indicating that supporting this query does not mean that the old weight can complete it.
- The page clearly displays the limits of privileged input and super-training ranges; Browser does not report JavaScript error. [Setting interface screenshot ](../artifacts/eval_limits_preview.jpg). (a) Run configuration locks, with the parameters for actual effectiveness retained separately; Restores the display of its parameters when reconnecting with an ongoing experiment.
- `cpu.py`, `history.py`, `networks.py`, `mechanics.py`, `learner.py`, `tasks.py` and the SHA256 of the previous experiment have been checked one by one and have not been modified. Limit adaption and editable attributes are located in the evaluation layer, without retraining or extending the old training distribution.
