# Stage-2 status

Stage-2 lives in this repository under `programs/motor-unit-representation/`. Hypotheses H1–H4 stay **Candidate**. The smoke file `stage2/stage2_results.json` sets `scientific_lock` to false. A scale-conditional PASS is not a charter lock.

## What landed

- `codebase/unit_bfm/`: sanitized local motor-unit FB tree. The import name remains `unit_bfm`. See `codebase/SANITIZE_NOTE.md`.
- Sealed B01→B04 merge norms are implemented once, in `codebase/unit_bfm/v3/stage2_norms.py`, and called from the V3 learner:
  - B01: `Learner.update` sanitizes privileged tensors before every forward call. A declared future slice is replaced by the lagged carrier.
  - B02: pre-activation logit hinge on the actor. The gate plant uses `make_program` and the inertia-scaled rule in the same module. The MuJoCo collector `RuleProgram` is unchanged.
  - B03: `BackwardMap` applies length-relative tip scaling (`nondim_v3_g`) and keeps the 16-D sphere. Optional `config_id` restricts the FB pairs to the same configuration. Charter `T_κ` remains the housing-frame map used by the gate plant.
  - B04: demand labels `IN` / `EDGE` / `OUT` and the frozen-local hash. The limb learning curve is the scaled plant in `stage2/`, not a second copy of the V3 network.
- `stage2/`: scaled full-physics smoke (analytic rotary unit and two-joint limb) plus `colab_stage2_runner.ipynb`.
- `stage2/run_stage2.py` writes `stage2_results.json` and a short V3 learner probe.

Packet decisions under `packets/` and `synthesis/` are unchanged.

## Smoke metrics

Executed tier: `scaled_full_physics_smoke`. Device for the recorded file: CPU. The Colab notebook uses CUDA when the runtime provides it.

| Gate | Smoke verdict | What was measured |
|---|---|---|
| H1 | PASS | Kinematic-block explained variance about 0.991 causal and 0.992 leaked. Retention about 0.999. Consumed causality violations: 0. The 48-row counterfactual was not better for the causal arm on this draw. |
| H2 | PASS | Joint 720-cell array populated. Sustained-load holds 144/144. Recoveries 144/144. Worst zero-velocity RMSE 0. Limit escape rate 1. |
| H3 | FAIL | Holdout worst-group relative successor error about 0.213 (threshold 0.20). Stratified effective rank about 4.5 (smoke floor 8, charter floor 12). Tip length-relative RMSE about 0.156. |
| H4 | PASS | Mode A worst-cell position-RMSE area about 0.106 versus about 0.633 for equal-parameter flat torque (4192 parameters). Final worst-cell RMSE about 0.039 versus about 0.376. Oracle worst-cell RMSE about 0.027. Frozen hash unchanged. |

Spec closure for the smoke plant passed (Schur, gravity finite difference, center-of-mass identity, IK round trip, 0.25 ms halving probe, distinct E4-R / E4-RI keys).

H3 fails closed: a code on the sphere can show a small relative error while the per-configuration rank is still low, so rank is part of the smoke gate. That FAIL blocks any claim that H3 is settled.

## How to run

From this program directory, with PyTorch and NumPy available:

```bash
export PYTHONPATH="$PWD/codebase${PYTHONPATH:+:$PYTHONPATH}"
python3 -m unittest unit_bfm.v3.tests.test_core_learning unit_bfm.v3.tests.test_stage2_norms unit_bfm.v3.tests.test_core_features
cd stage2
python3 run_stage2.py --output stage2_results.json
```

Colab: upload `stage2/colab_stage2_runner.ipynb`, choose a GPU runtime, run all cells. The notebook writes `/content/stage2/stage2_results.json` and offers a download. It does not install a MuJoCo backend. A full V3 scene rollout uses `codebase/unit_bfm/v3/physics.py` when that physics backend is installed.

## Not claimed

- No hypothesis is locked.
- The upper policy in the smoke has 4192 trainable parameters, not the charter 140,000.
- Privileged width in the smoke is 24, not 5065. The V3 learner probe uses a 32-wide synthetic tensor, not a logged scene.
- The limb episodes are 16 control steps at 50 Hz with a 5 ms substep. The 0.25 ms step is the halving probe only.
- Mode B is not trained.
