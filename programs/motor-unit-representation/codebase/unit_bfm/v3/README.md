# V3 Local Result State FB: Isolation Implementation

V3 is at `unit_bfm/v3/`, the old `unit_bfm/*.py`, configuration, artifacts and weights remain intact. The running directory can only be located in `runs/` of the new package; recovery requires the same version configuration and schema. This round of isolation training project has passed the integration acceptance. The current weight is still the short-training diagnostic version, and the general control skills have not yet been verified.

## Training logic

The simulation produces real transfer → fixed capacity RAM Replay → minibatch FB/Actor update → limited checkpoint with independent evaluation. 20m is the cumulative interaction budget and is independent of cache capacity. The default training does not permanently save the full trajectory and does not rely on disk decompression; a small number of calibration/evaluation trajectories are used for diagnostics.

The network concealment structure and standard FB loss remain unchanged. B reads g13, the actor reads x137 and z16, and the physical truth value and feature update memory are additionally read during double-F training. No GRUs, bonus training, or added ancillary loss. The rule controller is only used for acquisition, and the query function is only used to construct the evaluation command, not to enter the learning loss.

| Section | Actual input/output |
|---|---|
| B | Ordered length of two rods, q/dq/output shaft moment, limit, relative terminal velocity, causal acceleration and effective position, a total of 13 dimensions; output 16-dimensional spherical representation |
| Actor | g13 + declares rigid body/drive parameters and significant bits + 50Hz ten-frame slow history + 100Hz eight-frame fast history, total 137 dimensions, additional input z16; output normalized torque request u |
| F1/F2 | x + real physical state p + u/z; p dynamically determined by the physical registry, plus 243-dimensional feature update memory |
| Execution | 100Hz control; request via actual capacity, 1ms delay queue and first order drive, 1kHz force/integration |

Actor 207,617 parameters, B 74,000 parameters, the two executions total 281,617; each F parameter is `211728 + 512*p_dim`. The statement that only F is sent for privileges refers specifically to **additional environment/load truth value**: the precise axis torque in g13 of this simulation experiment is also privileged telemetry, which has been marked in the schema, and the deployment input cannot be claimed to have been verified.

The length, mechanical limits, and known parameters come from the declared model; the Actor does not have world speed, gravity direction, or unknown contact truth values. The relative terminal motion is a joint kinematic quantity, not the absolute speed of the world system. Ten frames of 50Hz cover the first and last 180ms, and the latest slow frame may be 10ms behind the current; eight frames of 100Hz cover the first and last 70ms. The acceleration is a 40ms causal fitting of five endpoints, with initialized valid bits.

# Runnable entrance

Run from the workspace, using the existing environment; the run name must not exist:

```bash
unit_bfm/.venv/bin/python -m unit_bfm.v3.train --mode smoke --run-dir unit_bfm/v3/runs/my_smoke
unit_bfm/.venv/bin/python -m unit_bfm.v3.train --mode dev --run-dir unit_bfm/v3/runs/my_dev
unit_bfm/.venv/bin/python -m unit_bfm.v3.evaluate --run-dir unit_bfm/v3/runs/my_dev --output unit_bfm/v3/runs/my_dev/evaluation
unit_bfm/.venv/bin/python -m unit_bfm.v3.interface --checkpoint unit_bfm/v3/runs/my_dev/final.pt --output unit_bfm/v3/runs/my_export
```

`dev` is a 3200-step E0 engineering check and cannot prove E1–E4 coverage. Custom configuration passes `--config`, and its mode must be consistent with the command. `--device cuda:0` only changes the learning network device; GPU physics also needs to configure `physics.backend` to `mujoco-warp` or `mjlab`, `physics.device=cuda:0`. The backend does not automatically pretend to be CPU.

Full recovery: using original configuration, `--resume <checkpoint.pt>` and new run directory. Just loading Actor/B for inference does not mean resuming training. Snapshot reset saves the physical process of the same model and then fills in the new observation history; it has a different interface from the training checkpoint.

## Randomization and Bounds

E0 fixed connection, E1 flexible connection, E2 contact, E3 adjacent motor, E4 combination scenario; P always motor housing side, D always output side, fixed which side is individually random. Actual model randomization includes two-rod length, mass/counterweight, declaration error, torque capacity/response/delay/resistance, mounting/encoding zero, mechanical limit, external force point/direction/timing, abutment and support. The physical gate refuses to be illegally assembled; the data to be legally blocked is to be extracted, and the value collapse cannot enter Bellman as an ordinary termination.

Replay baseline capacity rule32768 (half of which is fixed with P0 anchor point), policy65536, and check the 4GiB budget according to the actual p dimension. After both sources have data, they are sampled 50/50, and then binned and stratified according to scenarios, configurations, and statuses; missing groups clearly report partial, and complete coverage is not considered as a prerequisite for updating. Training does not store the target z calculated by B for a long time; the learning goal is re-encoded with the current B, and the same z is maintained during the acquisition call period.

The real GPU backend currently has host driver/force data handling every millisecond, which is a batch physical correctness implementation, and has not yet completed full device high-throughput optimization. Any closed-loop weld, free 3D mechanism and final bipedal verification are not in the validated range in this round.

## Acceptance evidence

The implemented training path is described in [Training Engineering Design](docs/Training Engineering Design.md). See the [Development and Acceptance Record](docs/Development and Acceptance Record.md), [Current Development Constraints and Acceptance](docs/Current Development Constraints and Acceptance.md), and [Independent CPU Audit](docs/v3-rl_final_audit.md) for evidence and limitations. Short diagnostic training does not establish general control ability.

The final weights are retained at `runs/coordinator_release_01/final.pt` only if that run was kept in this copy. Generated run logs and evaluation records were deliberately omitted from this English distribution; see `ENGLISH_PROJECT_SUMMARY.md` for their important conclusions.
