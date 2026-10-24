# v3-core Chinese handover

Status: The schema/features/networks/fb_loss/learner assigned by this agent has been implemented; 17 core CPU tests passed, including the real E0 short integration of the current shared area. There are no GPUs, long trainings, full case coverage, or final V3 engineering acceptance conclusions.

# Environment and boundaries

- host: <dev-host>; cwd: `<project-root>`.
- Python: `.venv/bin/python`, 3.10.12; NumPy 1.26.4; Torch 2.7.1+cu128. CPU only, OMP/MKL = 1.
- V3 allocation path is writable; reads coordination API, scheme, zero design resolution and cross-auditing. rg does not exist, use find/sed, etc.; dependencies are not installed.
- No changes to V2 code, old tests/configs/artifacts/weights; no git commits, no subagents, external messages or long training started. Other agent files are read-only.

## Current round file

- `unit_bfm/v3/schema.py`
- `unit_bfm/v3/features.py`
- `unit_bfm/v3/networks.py`
- `unit_bfm/v3/fb_loss.py`
- `unit_bfm/v3/learner.py`
- `unit_bfm/v3/tests/test_core_features.py`
- `unit_bfm/v3/tests/test_core_learning.py`
- `unit_bfm/v3/tests/test_core_physics_bridge.py`
- `unit_bfm/v3/docs/v3-core_handoff.md`

# Actual realization/API

`schema.py` is registered as g13, x137, memoory by name/scale/units/source/time/reference. No statistical integration, no hard cutting observations. `registry()` returns a JSON-enabled dictionary; SCHEMA_VERSION=v3-core-si-1,ESTIMATOR_VERSION=causal-5point-linear-dq-1. Currently SCHEMA_HASH=8da341738a7cf6c8a2889e618f22b14b51f85fbe75860077c17f027be4931.

Fixed scales: g uses .4 m, π rad, 6 rad/s, 6 N·m, 3 m/s, 200 rad/s², 100 m/s². Declare rigid body mass/COM/I scale to be 2 kg/.4 m/.1 kg·m²; actuation S/lower/upper=6 N·m, T/delay=.01 s, damping=.08 N·m·s/rad, friction=.08 N·m, armature=.006 kg·m². mask is 1; missing declared values ​​are masked first and then normalized, and zeros are not used to pretend to be valid values. The above are numerical scales explicitly frozen this time, not physical limits.

`CoordinateMap` is a known calibrated * * output side telemetry * * adapter, q_c = s * q_e + beta, dq/tau is only multiplied by s, request is converted by S_c/S_e, the limit is sorted, no wrap; invalid calibration is rejected. It does not implement rotor/gear models and does not convert MuJoCo tree coordinates. Environment boundary is already canonical, FeatureHistory does not reapply mapping.

`FeatureHistory.reset/append/features` follows the coordination API; copies and only reads whitelisted telemetry and known, ignoring p/diagnostics/world volume. Strictly continuous 100 Hz, check that the valid interval_dt is consistent with the time difference; missing tests can be expressed by valid/interval_valid=false at the continuous boundary, and reject when jumping. The last five real timestamp velocities are least squares fitted; the insufficient/failure angle and terminal acceleration are zero, acc_valid=0 (the centripetal term is not pretending to be valid).

The slow history is the even boundary, the sum/total dt of the integral of the first two intervals of the true, and the odd step preserves the nearest even boundary and recalculates the age. Fast History uses the previous interval u_previous with the current tau_endpoint. Both oldest→ newest; padding = 1, padding row remaining value and age = 0. reset is the real motion endpoint, which can participate in the subsequent five-point fitting; the front interval of reset cannot offset the slow/fast history.

The memory is fixed to **22×11+phase=243**: each row is q, dq, tau_endpoint, u_previous, tau_integral, u_integral, interval_dt, interval_valid, age, valid, present; if the leading all-zero slot is insufficient, the row is oldest→newest. The integration scale is .06 N·m·s/.01 s, dt=.01 s, age=.22 s; slow_phase=control step%2. `FeatureHistory.from_memory(memory,known,current_time=...)` Rebuildable recursor; absolute time given by caller, network read-only age. Measured reset/start/full ring, odd and even phases, and next step closure; dynamic known should be passed in with physical boundary updates.

F The only convention for splicing: `schema.concatenate_privileged(boundary['p'],features['memory'])`; total p_dim=env.p_dim+MEMORY_DIM. The parameters of `Networks/Learner(p_dim)` refer to the total dimensions. F calls `(y,u,z)`, y=[x137,p_physics,memory]. No guessing of physical dimensions, no import of physics modeling. The current physics module exports 3176, and the short integration total p_dim=3419; this number is only the current registry reading value, and the core has no constant binding.

The network maintains double E branches and hidden layers, B input 13, Actor input 137, z16; B SphereNorm radius 4, Linear orthogonal gain 1 (Learner initialization), no additional parameters/auxiliary loss/GRU. counts: Actor=207617, B=74000, deployment=281617; single F=211728+512*p_dim. The current total p_dim=3419 orders F=1962256, online=4206129.

FB loss strictly requires discount[N,1] and becomes [1,N,1], rejecting [N]; the independent scalar formula and gradient have been checked. target double F average, target B and all successors stop gradient; min after Actor dot product, frozen F parameters still retain action gradient. All input batches are detachable, and F/Actor is not returned to Replay; there is no new loss. The target has no copy of the Actor. The next action of the current Actor is used according to the plan.

Learner batch is required independent goal_g[N,13]/goal_valid[N], training z is not constructed from g_next. Per row .5 Bernoulli Configure complete goal using current B encoding, no shuffle; fallback to random sphere z for rows without valid goal, metrics report goal_fraction. The length/limit of the effective goal is checked against the current x; independent sampling itself is guaranteed by the pipeline, and the core cannot prove independence with tensor alone. `sample_z(n)` supports purely random acquisition calls.

Learner config supports LearnerConfig or just a dict of lr/polyak/action_std/action_clip; default 1e-4/.01/.2/.3. The checkpoint is saved online/target/optimizers/independent generator, version/schema hash/estimator/config/p_dim; V2, core schema or dimension/config does not match and is rejected. After recovery, the next update and all network parameters will be consistent bit by bit.

## Commands and results

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
python -m unittest discover -s unit_bfm/v3/tests -p 'test_core*.py' -v
```

Final run: * * Ran 17 tests in 1.139s — OK * *, exit code 0.

- 8 features: registry/scale/padding, causal fitting and endpoint finite difference, compressed history counterexample in audit, slow parity and true integral, memory current/next reconstruction, missing/reset/copy isolation, p with declaration driven input boundary, qcanon equivalent/power/limit.
- 7 learning items: Independent scalar FB loss and gradient/line discount/target detached, Actor min, precise parameter quantity/SphereNorm/gain1, freeze F retention action gradient and abnormal recovery, dual target mean used with p_next, independent goal interface/no shuffle/invalid fallback, real update/Actor input hook/gradient isolation/full recovery/V2 rejection.
- 2 CPU bridges: The current physics E0 fixes the p/memory and recursion of 25 control steps each; the E0 30-step rule episode is updated once by→ collect→ reconstruct Replay.sample→ Learner. Replay only comes with a memory episode, does not call add/save, and does not write training data or weights.

The two test fixture problems in the initial test (integer ndarray in-situ floating point multiplication, FP32 exact equal sign) have been corrected; another test found that goal is invalid and still calls empty batch for B, which has been changed to choose.any () before calling, and then passes the whole set. There was no concealment of passing the first time after failing the test.

# Main window needs to be integrated/not accepted

1. **psyscheschema Hash**: core only p_dim; The physical field reordering of the same dimensions cannot be automatically found by this checkpoint. Please check the complete pysics_schema (and core registry/hash). does not add new model input.
2. `FeatureHistory.from_memory` recursion requires the next boundary known (D COM will change with q); this comes from physics/deployment of known models, and memory does not contain known repeatedly. The closure of the absolute clock/externally loaded state is the responsibility of physics p, and the closure test of core is not equivalent to a strict Markov proof of the entire system.
3. Original equipment rotor conversion, movement wear and tear, or unknown calibration not achieved and is not part of the current output side adaptor; The qcanon algebra test cannot be calibrated by claiming real hardware.
4. E1–E4 physical correctness, complete scene coverage, GPU, long training, query success rate and 100 Hz deployment delay are not accepted by this agent; this round is only verified by core CPU and short E0 wiring.
5. There are currently no core tests to be repaired that have failed; other modules are still being developed concurrently, and subsequent changes should be repeatedly integrated and accepted by the main window. Other agent files are not modified, nor are declarations completed in place of them.
