# Single Joint, Two Link Forward-Backward Model

This directory contains the unit-level forward-backward (FB) experiments. V1 was stopped after failing held-out evaluation. V2 completed reward-free pretraining, but the candidate remains unvalidated. V3 is a separate implementation with a local outcome state, bounded replay, and a broader physics model. Its current weights are diagnostic and have not demonstrated general control ability.

Read the [English project summary](ENGLISH_PROJECT_SUMMARY.md) first. The detailed records are in [docs](docs) and [v3/docs](v3/docs). Generated training logs and V3 run records were omitted from this copy; retained V2 artifacts and configuration remain under `artifacts/` and `configs/`.

## Run the existing V2 checks

From the directory containing `unit_bfm`:

```bash
unit_bfm/.venv/bin/python -m unittest discover -s unit_bfm/tests -v
unit_bfm/.venv/bin/python -m unit_bfm.validate_physics
```

To start the local evaluation site:

```bash
unit_bfm/.venv/bin/python -m unit_bfm.eval_web.server --port 8766
```

Open <http://127.0.0.1:8766> and select a checkpoint or historical result. The [evaluation guide](docs/Evaluation Web App Guide.md) explains the metrics and playback controls. The web app uses simulation state, including privileged telemetry; it is not a validated motor-only controller.

## V2 outcome

V2 completed 20,032,000 transitions and 77,218 gradient updates. Under nominal fixed support, latent commands can produce holding and alternating motion. Contact and cross-structure queries still fail substantially, so `validated=false` remains the correct release status. See [Reward Free V2 Results](docs/Reward Free V2 Results.md).

## V3 outcome

V3 passed short engineering checks for physics, collection, replay, checkpoint resume, and frozen evaluation. Those checks do not establish sustained holding, speed, force, obstacle release, unseen-structure generalization, or faster biped learning. See the [V3 README](v3/README.md) and [Development and Acceptance Record](v3/docs/Development and Acceptance Record.md).

## Adversarial research

English master synthesis for B01–B04: [MASTER_SYNTHESIS.md](docs/adversarial-reviews/MASTER_SYNTHESIS.md) (pointer to `../../synthesis/` under the research tree).
