# V3 physics handover (10-10-2026, final state)

## Actual status and access API

Delivered CPU E0–E4 physics, unified privilege export, real mujoco-warp/mjlab batch backend implementation; **Not completed for CUDA device pairing acceptance, does not claim to have completed full design scope or full GPU high-throughput acquisition**. This round has no sub-agents, no external messages, no installation, no training, no commits, and no V2 files have been changed.

```python
from unit_bfm.v3.physics import SceneConfig, make_scene, UnitEnv
from unit_bfm.v3.warp_backend import WarpBatchEnv, MjlabBatchEnv
cfg = make_scene(seed=0, scene='E4', fixed_side='D', capacity_nominal=6.)
env = UnitEnv(cfg, seed=0)
b0 = env.reset(episode_id=0)
b1 = env.step(.1)
# env.known / physics_schema / p_dim / metadata / close()
# Same compilation parameter bucket; each world can be used for independent actions, rounds reset
batch = WarpBatchEnv ([cfg, cfg], device = 'cuda: 0') # No CUDA explicit rejection, no automatic CPU fallback
```

Final `SCHEMA_VERSION=v3-physics-3`, `p_dim=4534`; initial handover 3176/4218 has been invalidated. Full E0–4 same ordered registry. **p has been normalized according to field scale**, core only spells feature memory, and does not perform secondary normalization. Read `env.p_dim`, do not write dead dimensions. The main window cross-module test has been run, and the physics→features→Replay→learner short CPU update passed.

The returned ndarray is a read-only independent copy; the dict is a serializable independent copy, allowing the pipeline to add collector truncation. `known` M-system representation of COM/I updated per boundary, hidden density/capacity errors do not enter declared parameters. `static_bias_torque(boundary=None)` is a new optional rule-specific gravity offset interface. The pipeline has been compatible with getattr; it is not used as an Actor observation.

## Actual environment and permissions

- host `<dev-host>`; `os.getcwd()` `<project-root>`.
- Python `.venv/bin/python`, 3.10.12; MuJoCo/mujoco-warp 3.8.1, Warp 1.14.0, mjlab can be imported.
- This session `nvidia-smi` driver communication failed; `torch.cuda.is_available() == False`, device_count=0; Warp reported CUDA error 100. It cannot be overridden by the GPU availability status of other windows on the system.
- The assigned V3 path is writable; the user cache is read-only, and the Warp compiled cache explicitly defaults to `/tmp/unit_bfm_v3_warp` and can be overridden by WARP_CACHE_PATH. pytest is missing, the standard library unittest is used, and there is no installation.

# Realized Physical Scope

- The research hinge is a double-pronged P capsule, a real pivot pin, a 16-segment hollow D bearing ring and an output rod; the counterweight has a real spherical geom, and the mass/COM/inertia is synthesized by the engine. What is disabled is MuJoCo **parent collision filter**, not collision, no contact exclude.
- Each model independently sweeps all P/D pairs (including default parent-child filter pairs), 0.5° grid, continuous displacement upper bound conservative margin, boundary indentation. 36 Geometry × 2 Fixed side all gate passes and exceeds ± 1.2 rad; gate saves the list of pairs, minimum distance, tolerance, grid and coverage. Each reset also scans all allogeneic geom pairs, rejecting illegal initial states.
- Fixed D real reverse tree, P always housing, D always output; tree_sign is separated from encoder_sign/beta, canonical q/dq/tau/request, M system endpoint, power equivalence passed assertion. The simulation uses canonical model zero; raw encoder=0 reflects the physical posture through true q=beta.
- Third gear C0=3/6/9; S=1.25*C0; real C multiplier .8–1.2; 11 slots old-to-new real queue, integer 0–10 ms delay, exponential first order response, real qfrc written every millisecond, 100 Hz integration direct accumulation of 10 substeps.
- E1 floating root, point spring damping/angle spring, moving reference and non-exact weight preload; E2 real force approach/continuation/retraction of planar dynamic sphere and ground; E3 bilateral adjacency real PD → independent homogeneous drive; E4 enable adjacency, dynamic contact, bilateral compliance support and loader at the same time, not replaced by role switching.
- External load P/D, take the action point from the study hinge, the direction of the world/rod fixation, the force and the free force couple, add it up after the real COM translation; each source retains the effective point/force/moment/phase. Load retention and release have a continuous dynamic response.
- schema covers actual rigid body complete symmetry inertia/COM/relative pose velocity, geometry/mounting/friction, tree joint parameters, actual drive/queue, current reference generator, two sets of supports/four slot loading/two object slots, 128 contact slots, rear constraint tree reaction. Non-existing slots are explicitly present=0; do not pass off zero as an existing unrealized quantity.
-  `forward→mj_rnePostConstraint→copy same-solve force, contact point, and M frame→Euler→refresh geometry` . p has time semantics for current geometry as compared to the last of the previous 1 ms Solve; reset solve_valid=0. Respond of the tree moving from subtree COM level to M origin; Contact is moving towards geom1, slide to solver. Weld, closed_chain_covered=False.
- Non-limited values, extreme speed, MuJoCo value warning and >2 cm penetration judgment are invalid; GPU contact/constraint capacity overflow directly reports an error and requires expansion and re-acquisition, and cannot be lost silently.
- Randomization supports layered length, mass/counterweight, density declaration error, drive declaration error, resistance/armature, mounting and coding mapping, external loading, support, adjacency, object; independent purpose flow. Optionally, `reset_mode='stratified'` determines the q tenth gear and ± speed according to the episode, and still must pass the initial state gate. The default configured reset facilitates reproducible pairing.

## Backend scope and performance boundaries

`WarpBatchEnv` actually calls batch Warp forward/rne_postconstraint/contact_force/euler; `MjlabBatchEnv` uses mjlab Simulation to allocate real model/data, and then solves it according to the same step-by-step pipeline. Different model constants/shapes must be bucketed, and different configurations are not implicitly broadcast. Real contact_force device results are used for privileged export; CPU get_data_into only moves, does not re-CPU solve fake GPU.

The drive/load calculation and same-solve export are currently performed on the host every millisecond, and the GPU solver has a synchronous copy. So this is the correctness reference batch backend, * * not a full device rollout/optimized throughput version * *. The CUDA code path has not been run on an accessible GPU; the Warp/mjlab test of the explicit CPU device only proves that its real CPU kernel/access path is operational.

## Test commands and results

```bash
python -m unittest unit_bfm.v3.tests.test_physics_cpu unit_bfm.v3.tests.test_physics_backend unit_bfm.v3.tests.test_integration_contract -v
```

The final results are updated at the end of the document. Test real assertions include: all E0–4×P/D API; three-speed capacity positive saturation, delay and integration; fixed D geometry/power/recoding; 72 wide stroke gates per model; tree connection independent linear momentum/angular momentum balance; E4 full-system finite difference Jacobian linear momentum balance (including world slide damping); same-solve freeze; hidden parameters are not known; bilateral E4 continuous ≥0.5s Contact + adjacent actual movement + force transmission and removal on both sides; real Warp CPU two world independent action pairing and mjlab CPU pairing; no CUDA rejection; 2 real cross-module integration in the main window.

CUDA E0-4xP/D, Warp/mjlab test for CPU has been prepared and the current equipment conditions have resulted in a unit **skip**, not pass.

## It is still not resolved and cannot be marked as completed.

1. CUDA pairing/reaction/contact numerical tolerance, GPU performance and throughput; the main window is required to run the same test in the execution context where GPU permission is obtained. Currently, I do not have a GPU, so I can continue the acceptance from the main window.
2. The adjacent connection is already a quality real power tree, but the adjacent electrical complete shell/connector CAD, the full adjacent attitude combination continuous sweep and cable limitations have not yet been modelled. The current wide process gate only confirms the body P/D; The combination of scenes can only be used through the initial state of pass-through reset gate and allow real obstruction without declaring that the entire qx adjacent space is not collision-free.
3. 36 geometry × 4 limits × all dynamic combination coverage/access, equal quota for each gear, actual sampling of the complete randomization range and long-term process statistics have not been completed; passing the current test fixture does not mean that all random configurations are controllable or stable. Snapshot reset hybrid, two dynamic objects used at the same time, one-sided adjacency topology, any non-tree connect/weld is not implemented; empty slots have masks, and weld is explicitly disabled.
4. The support currently only has translational sinusoidal reference + fixed angle reference, and has not yet covered all angular motion/horizontal and angular preload combinations in the design; load defaults to a set of explicit rod loading plus object servo (remaining slot mask), and is not used by four loaders at the same time.
5. p Record the current process state/constant, but do not prove that the external program is strictly Markov closed; do not leak to p the time of the event that has not yet taken effect. The object servo target/phase, the complete recursive state of the support process still needs to be further reviewed, and it cannot be claimed that F has been strictly Markov.
6. The geometric gate uses conservative Lipschitz indentation, without additional 0.05° boundary bisection refinement; the conservatism is asserted, but the complete design details are not fully realized. The dynamic contact penetration of 2 cm is only a numerical rejection upper bound and cannot replace the accuracy calibration of each soft contact.
7. The current inertia parameter adjustment of Pipeline RuleProgram always takes D; when D is fixed, the inertia parameter adjustment of the free side P should be corrected by the pipeline coordinated by the main window and is not within the scope of modification by this agent. The new static_bias_torque only gives a generalized bias to gravity and cannot replace the full coupling/external load feedforward capability calibration.

## File list (only for this agent)

- `unit_bfm/v3/physics.py`
- `unit_bfm/v3/mechanics.py`
- `unit_bfm/v3/randomization.py`
- `unit_bfm/v3/privileged.py`
- `unit_bfm/v3/warp_backend.py`
- `unit_bfm/v3/kernels.py`
- `unit_bfm/v3/tests/test_physics_cpu.py`
- `unit_bfm/v3/tests/test_physics_backend.py`
- Ben `unit_bfm/v3/docs/v3-physics_handoff.md`

Delivery is within the operating range described above; missing items remain missing and are not offset by CPU smoke or schema slots for full GPU/design acceptance.

### Final execution result

The above combined command: `Ran 14 tests in 25.733s — OK (skipped=1)`, which is **13 passed, 1 CUDA pairing skip**. GPU Skip Original: `CUDA inaccessible; CPU/GPU parity NOT validated`. The real Warp CPU world and mjlab CPU paths are both within the pass items. This result does not extrapolate to CUDA.

There are 12 final physical-specific tests (9 CPU oracle + 3 backend), of which 11 passed and 1 was skipped by CUDA; the other 2 are cross-module tests that have appeared in the main window (read-only running, the test has not been modified).

An additional random seed check found that the initial obstacle of E2/E4 with seed=2 intersected 0.67 mm with the counterweight, and the independent gate was correctly rejected. The initial offset of the corrected object is radius+0.04 m, and the continuous approach stroke is synchronously increased to 0.067 m; the minimum distance of the four E2/E4×P/D counterexamples reset is restored to 0.004 m. There is no closing collision or relaxing the gate.

After fixing the above counterexample of initial counterweight installation, the joint test was completed again: 14 items, 13 passed, 1 CUDA skipped, 25.733 s.

## The second round of repairs is in progress: Stable interface preview (priority to the above first round status)

Read incremental-review-1/2, diagnostics-contract, random_scene_failure, gpu-handoff, resource-transfer, gpu-pair-first-result, and core_cross_audit. The GPU belongs to the main window, and this round is only CPU.

API that will be stable soon: `make_scene(..., geometry_seed=0, episode_id=0, variant_id=None, **overrides)`; seed only controls the round dynamics, and the lengths/limits of fixed `(geometry_seed, geometry_id, limit_id)` do not change with the episode seed. `neighbour_sides='P'/'D'/'both'`, `fixture_mode='none'/'P'/'D'/'both'` explicitly compile/force variants; E4 defaults to only one of the four variants, both. metadata outputs the actual topology/variant/tags.

`env.snapshot()` returns the full model-physical/driver/process state of the pickle; `env.restore(snapshot, episode_id=...)` returns the first boundary of the historical padding (no last integral, no valid solve), and verifies the model hash. pipeline is responsible for 50/30/20 selection and compatible snapshot cache; reset supports configured/xi/velocity, and does not say that the reset tag that does not provide a snapshot has been restored.

If the value is invalid, `PhysicallyInvalidTransition` will be thrown, carrying `.diagnostics`, `.boundary`; boundary valid=False, terminated=False, and shall not be used as a normal terminal Bellman line. This round of schema will be upgraded. Please press dynamic p_dim to rebuild the network/library. It is not compatible with the first round weight. Exact version and CPU acceptance will be updated later.

## This round of stable API (revision 4, implementation has been released, CPU is returning)

- `make_scene(seed=..., geometry_seed=0, geometry_id=..., limit_id=0..3, episode_id=0, variant_id=None, ...)`: geometry_seed/id produces two poles of length alone; I'm not sure if I'm going to be able to do this, seed/episode. varant_id separate layered by each purpose, fixture 1 both for every 4; ** Retained from geometry. Visible overlay parameters support `neighbour_sides=none/P/D/both`, `fixture_mode=none/P/D/both/auto`, `load_mode=single/sustained/pulse/repeated`, `load_period/load_repeats`. The actual number of trees/fixture_sides and actual_tags can be readable.
- `reset_mode=xi/velocity/configured`; pipeline is responsible for the 50/30/20 mix. `snapshot()` saves mjSTATE_INTEGRATION, all drives queue/tau/target, anchors/angles, object base/normal/travel/tracking origin; `restore(s,episode_id=...)` verifies the complete XML hash and process config hash. data.time retains snapshot_time; new episode elapsed starts from 0, and duration is retimed after recovery. The first boundary interval_valid=False, solve_valid=False, integral 0, history must reset padding. WarpBatchEnv supports list snapshot/restore.
- `PhysicallyInvalidTransition` has been implemented, `.diagnostics`/`.boundary`; boundary valid=False, terminated=False, interval_valid=False, episode stops immediately. Check q/qvel/qacc/constraint/wrench limited, warning, capacity, solver convergence, scene penetration, P/D self-penetration and limit every 1ms. The pipeline should be captured and isolated without failure boundaries to form a normal terminal transition. When completely nonfinite, boundary.p=None, 0-padded playback is not possible.
- diagnostics has directly output all SI fields of the module contract, dq/tau/capacity of adjacent axis, actual P/D clamp force/moment, research unit load (excluding object servo), solver_valid/invalid_reasons/interval_solve_count.
- schema=`v3-physics-4` (please read P_DIM for the final dimension): reset support parameters, current M plane of floor, complete tree parent/weld/dof, object controller reference/speed/normal/tracking anchor point, and current deterministic loader program are all in F. The event time program here is a deterministic controller configured by reset, which needs to be given to F to eliminate counterexamples of the same input but different next events; **There is no independent random event stream in the future**. If it is added later, only the current sampled control state needs to be exported. Actor path remains unchanged.
- Estimated RAM for this round: less than a few MB for a single CPU environment; probe runs sequentially; physics p is about 4.8k, FP64 is about 39KB per boundary, and network/replay is budgeted according to the actual p_dim. The 128 contact slots have about 2816 dimensions and the 64 geometry slots have 1024 dimensions accounting for the main part. The fixed template union facilitates mask/overflow rejection; the capacity is currently conservative and the necessary true values ​​are not deleted or the network is changed to save Replay.
- GPU main window exclusive; this agent only runs the Warp/mjlab path of `device=cpu`. The back-end retains the same-solve full force readback, only the integral post-readback is changed to the batch kinematics field, and does not claim that the full GPU rollout or 20m throughput has been reached. The new schema and contact/limit parameters expire the old GPU acceptance.

# Deliver the acceptance results of this round (10-10-2026, covering the corresponding items in the incomplete items of the first round)

### CPU Actual Evidence

Order:
```bash
python -m unittest unit_bfm.v3.tests.test_physics_cpu unit_bfm.v3.tests.test_physics_revision unit_bfm.v3.tests.test_integration_audit_regressions.InputSufficiencyRegressionTests.test_support_parameters_visible_before_first_solve unit_bfm.v3.tests.test_integration_audit_regressions.InputSufficiencyRegressionTests.test_ground_distance_visible_in_privileged_state -v
python -m unittest unit_bfm.v3.tests.test_physics_backend.BackendContract.test_explicit_warp_cpu_batch_reference_path -v
```

- In the first article, all **17 items passed, 91.539s** (measured when the parallel main window was working); including the original 100 configuration × 30-step true assertion, reset support/ground counterexample, snapshot with successor, numerical fault injection, stable geometry catalog, true single/double adjacency, quarter E4 double clamp, actual repeated loading/release, independent force balance, etc. Later, a new wide initial state/diagnostic test was added, and the command was changed to 18 items; the final rerun is shown below.
- Item 2 * * 1 passed, 7.905s * *, the actual Warp CPU 2-world reverse action + mjlab CPU, including q/dq/integral/p/contact force control; CUDA was not started.
- After the independent `random_scene_probe` had reached 100/100, the independent arrangement changed the sample; instead of following the old pass, it rerun and repaired the newly discovered counterweight billiard ball 11mm soft penetration. The latest 100 cases have all passed the above test_random_initialization_probe without deleting any installation or collision.
- The initial installation uses the mj_geomDistance closest surface point/normal direction of the actual candidate geom, searches along the normal direction after projection to the plane, and saves all attempts/rejections/acceptances, source_geom and actual distance; no longer radius+.04 world x offset. Double adjacent rods are separated by y=+.12/−.12, and true geom collision remains on.
- The high-speed collision limit of about 58rad/s is handled by the * * true limit constraint * * change process: solreflimit = .002, solimplimit = .999, activation margin = .08rad, the metadata is clear margin, and it is not claimed that this 0.08 rad is free to move. Contact solref = .003, still reject with scenario penetration > .01m, do not relax the legal threshold.
- 40 new cases of xi/velocity E4×P/D wide initial state independent distance pass; velocity mode root translation ±.5m/s, angular velocity ±1.5rad/s, research joint ±.5/1/2/4rad/s. `configured` respects the specified value and does not automatically change it to avoid illegal initial installation.

### Determine stable interface/semantics

- physics p_dim **4822**, schema `v3-physics-4`; memory is appended by core, g13/x137/network/loss is completely unchanged. The fields include name/source/scale/units/time/reference/mask/invariants, and the length is consistent to prevent zip from missing columns silently.
- The actual composite shape of P/D is only described by the full size/installation of each geom; body `max_geom_radius` is the maximum size [0] of all the geom of the body, and no longer pretends to be the counterweight/adjacency radius under the name .01.
- `UnitEnv.snapshot()/restore()`, `WarpBatchEnv.snapshot()/restore()` has been made public; To accurately restore the next physical state, without copying the last round of history. ** Recovering with the model Hash+process config Hash**. It is recommended that the Pipeline compatible pool key use both of these items at the same time or directly try restore and record the rejection as incompatible. snapshot saves snapshot_time; After recovery, Data.time continued the external process, pisode_elapsed to zero, post-durbanization.
- Default `variant_id=None` random condition; to achieve equal amount tiering by configuration, pipeline arranges `variant_id` continuously. Each purpose is arranged independently within the block, avoiding fixture = both total binding and installation sectors; 144 groups are determined by fixed geometry_seed and 36geometry × 4limit. The mass/counterweight is no longer fed into the length to generate the flow.
- The current controller is a deterministic program configured starting from reset. Start/end/period belongs to the current generator state and will enter F; future independent random events are not realized and there is no leakage of future independent sampling. You can no longer use "the future has not yet been activated" to hide the deterministic countdown to create different successors of the same p.
- `PhysicallyInvalidTransition` must be captured and isolated; it is not terminated normally and does not reset automatically. Warp exception has world_id, and all current reference batches are stopped to prevent half intervals of other worlds from being mixed into Replay. If you want to partially recover, you need to reset after the adapter explicitly discards half the interval of this batch.
- `contact_normal_force_N` only statistically studies the contact between P/D and the outside, removes the internal contact of P/D, and does not include the ground contact of independent objects. Other SI fields are provided directly by physics, and coverage does not need to be guessed from the label.

### Current round performance and GPU boundaries

Limited practical optimization completed in this round: Registry block name caching avoids repeated scanning of 4822 fields per boundary; after Warp integration, the kinematics is batched once per field instead of getting_data_into every world, and the same-solve reaction/contact still retains the true extraction. This optimization is controlled by the CPU kernel, not the stub or the CPU fake GPU.

Full device drives/loader/support/integral kernel and only 100Hz export are still not achieved; 1kHz host scheduling is still a throughput bottleneck. According to the correct CPU/parameter coverage project in this round, * * GPU performance optimization is not completed * *. The main window needs to rerun GPU pairing and throughput; the original RTX5060Ti early 3176 schema evidence cannot accept the current 4822 version.

# # Scope of the document for this round

Only the `physics.py/mechanics.py/randomization.py/privileged.py/warp_backend.py`, `tests/test_physics_cpu.py`, newly added `tests/test_physics_revision.py`, and its own handoff assigned by this agent have changed; `kernels.py/test_physics_backend.py` retains the original interface and is read-only for verification. Core/pipeline/V2/main window test has not been edited; not installed, not committed, not trained, not GPU, and no subagent.

The remaining main window work is independent GPU/cross-module acceptance and long-term conditional access coverage. The above CPU correctness should not be regarded as proof of the 20M skill effect. Uncalibrated weld is still disabled in the production template; compliant clamps are supported and do not pretend to be rigid closed chains.

# # Final CPU rerun (after registry lookup optimization)

The first command listed above is now **18 tests, 27.994s, all passed**; including the original 100 cases of actual rollout (30 control steps per case) and the new 40 cases of wide initial state, not just configuration and constructability. Warp/mjlab explicit CPU pairing is still 1 pass (7.905s). No GPU tests were run in this round, nor were they skipped as GPU verification.

Finally, compatible protection is added: when Pipeline only covers load_start/end and not period, make_sense automatically increases the repetition cycle to at least active_demission+.5s, retaining the time required for successive withdrawals; The explicit introduction of illegal period is still denied. All 100 tectonic assertions of independent feed, unified coverage of 3s, were approved. This change does not change the 100 probes that do not have timing overrides.

This round of delivery file SHA256 (for the main window to identify concurrent versions):

- `physics.py`: `8eadef58619c64e5266618d5111c3a8bfd7f99e5a505b8b2495892fee7af62f4`
- `mechanics.py`: `9256c67bf49c58b49bd02080a661ef7f2f3a6ef32fd03bc4d4101883cb7a66f9`
- `randomization.py`: `7de35c087823c9185921b354def16483236f42e4f14e63261e3fdd455bb10a5a`
- `privileged.py`: `24c8b6dd0e0dfff768cd804ecae39a767c4bb462ab81494ee0f9a95d17cbbd62`
- `warp_backend.py`: `b89a6ef4061091d34d0264b5348af049e35a192df1531b69811e550ad171f398`
- `kernels.py`: `a39b0545c1d4d31aac9848d5770c2dc3b3de32039bbd7d6a17bb34f9e0f77a12`
- `tests/test_physics_cpu.py`: `fdf66ab119d86955d14621a7b6cd1f802b1d949eac9c258a7dba5b800bd4fe93`
- `tests/test_physics_revision.py`: `b91e03c953248d80ef963b514d689b41dfcd817db013d64a277944c890a05aa2`
- `tests/test_physics_backend.py`: `8bccd92ab93804c950c405a282b88a0a32fb65ba75f2c12aa0b636e557aa6e97`

# CUDA 60 ms event boundary anti-routine directional repair (source code stops writing after delivery)

Read "This Round of Development Constraints and Acceptance" and `audits/gpu_debug_01/log.txt`. The real first diff is E0 P k5: CPU controller.load.active = 0, GPU = 1; float32 is still less than .06 per ms, resulting in more force in the next step, and the subsequent contact/motion difference is not a tolerance problem.

# Fix and stabilize the clock contract #

- Each world of CPU/Warp/mjlab uses an independent Python integer `physics_tick` (public read-only property) as the only process clock; every time it is completed, the 1ms integral is incremented by 1, `process_time=physics_tick/1000`. The device float32 Data.time is only a projection of the clock, synchronized every sub-step, and never reverses the event tick.
- Loading start/end/period and episode duration are converted to integer ticks when created: `ceil(Decimal(str(seconds))*1000)`; start is included, end is not included, and non-integer millisecond parameters take effect on the first physical boundary that is not earlier than the SI time. metadata.clock_contract records the quantization rules and each tick.
- The segmented judgments of loader loop/active/phase and obstacle approach/withdraw use integers; support/adjacent sine uses double seconds derived from integer ticks, and does not use device accumulation time. The current program time parameter in p is the actual quantized SI value, and the original field is retained intact.
- The same-solve snapshot stores the tick time before solving and the corresponding second, and the tick time after the boundary integration, keeping the previous 1ms force timing. The episode truncation is also used as an integer difference.
- The snapshot version is upgraded to **2**, and physics_tick and clock_version=`integer-ms-v1` are added; restoration is subject to saving ticks and is not rebuilt by float integration time. snapshot_time needs to be consistent with tick. Old v1 explicitly rejected this to avoid silent guessing about drift times. The first boundary is restored with padding, no previous solve/points, and the new episode is recalculated from the saved tick to the duration.
- The schema field/dimensional remains unchanged: **4822**; Version updated to **v3-physics-4-tick1** and the time semantics of identifying old data cannot be impersonated as a modified version. No pinging, relaxation of test tolerance or modification of mechanics parameters.

### CPU evidence (GPU is not used in this round)

```bash
python -m unittest unit_bfm.v3.tests.test_physics_clock -v
python -m unittest unit_bfm.v3.tests.test_physics_cpu unit_bfm.v3.tests.test_physics_revision.RevisionPhysics.test_snapshot_exact_successor_and_new_episode_clock unit_bfm.v3.tests.test_physics_revision.RevisionPhysics.test_topology_variants_and_repeated_events -v
```

All 4 new clock tests passed (the final running time is shown below), including:
1. The real numpy float32 accumulates 60 steps to get less than .06, leaving the original counterexample; the integer 19/20/59/60/repeat 420/460 and other tick asserts the exact active state, and the non-grid time quantitative assertion.
2. Fixed P/D E4, equipment time to collect the adjacent lower value of float32, complete p and barrier/support reference strictarray_eqal, proving that the program does not depend on drift time.
3. When saving/restoring at release tick 60, the precision of the integration_state floating point time is deliberately reduced. After restoration, the next p of the same action is strictly equal; the truncation clocks of the original episode and the restored episode are different and correct; the old snapshot version is rejected.
4. The real Warp CPU and mjlab CPU are paired at the .02/.06 event boundary, snapshot recovery, and the active/solve load state and time are exactly the same. The original rtol = 1e-2/atol = 2e-3 is still used for p, and it is not relaxed.

Article II **11 tests, 8.171s, all adopted**, balance of retention, same-solve, E4 simultaneously flow, capacity fraction, fixed D and restored return. The GPU is still in the main window and requires independent verification of original CUDA pairing/debug scripts, and cannot claim that GPU has been accepted from the CPU results of this round.

In this round, only `physics.py`, `warp_backend.py`, `privileged.py` (version number only), `tests/test_physics_clock.py` and your own handoff have been added; other modules have not been changed or expanded. The source code has been delivered, stop writing, and wait for the main window to accept.

Final clock command: `Ran 4 tests in 3.753s — OK`.

Directed Repair Delivery SHA256:

- `physics.py`: `6d5a9489f15cd2ea431d963521ffecb31a906ef6bc486d650d424a9e95c66271`
- `warp_backend.py`: `cc7c5008555581eb344cb000912808e3ba919bc7460fd9bd834514573f9ff246`
- `privileged.py`: `2505b1fc6f4bf862843a12ad1a496bee6a275e87bcf86bca0956e069accbc4c5`
- `tests/test_physics_clock.py`: `7efecb042069b8c354dee88f2983ff20006229644929682f5e7548ff141066eb`
