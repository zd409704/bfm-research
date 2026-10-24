# Unit FB project: English summary

This project studies a motor driving a joint between two links. The original V1 work was stopped after failing held-out evaluation. V2 completed reward-free forward-backward (FB) pretraining, but its candidate remains unvalidated. V3 is a separate implementation that changes the observation contract, physics scenarios, and replay pipeline. Its short diagnostic runs establish engineering behavior, not general control ability.

## V2: completed training and limits

The V2 run completed 20,032,000 transitions, including 256,000 shared P0 transitions, and 77,218 gradient updates. Its release flags are `budget_completed=true` and `validated=false`. Under nominal fixed support, a queried latent command can produce holding and alternating motion. Across connection conditions, holding, velocity, and compliance remain weak. Contact cases can settle at joint limits with sustained saturation. Completion of the interaction budget must therefore not be read as acceptance of a general controller.

V2 uses planar dynamics. Its saved results do not establish transfer to three-dimensional units or improved biped learning. The existing evaluation artifacts and checkpoints remain available under `artifacts/`; generated training logs and web evaluation sessions are omitted from this English copy.

## V3: architecture and training path

V3 keeps the FB network structure and standard FB, orthogonality, and actor objectives. The outcome encoder B reads a 13-dimensional local result state and produces a 16-dimensional spherical representation. The actor reads a 137-dimensional context and the 16-dimensional command, then requests normalized output-shaft torque. The two F networks additionally read privileged physical state and feature memory during training. There is no GRU, reward-training objective, or new auxiliary loss.

The physics model runs at 1 kHz and control runs at 100 Hz. The five scenario families cover fixed connection, compliant support, contact, a neighboring motor, and combinations. P always identifies the motor housing side and D the output side. Known geometry and drive parameters are distinguished from hidden loads and contact truth. Exact simulated shaft torque in the B input is itself privileged telemetry; a real deployment would need a validated measurement or estimator.

The main training path collects real transitions into bounded RAM replay, samples minibatches for FB/actor updates, and saves limited checkpoints and independent evaluations. The 20M interaction budget is cumulative and is not replay capacity. The baseline replay capacities are 32,768 rule transitions and 65,536 policy transitions, subject to an explicit memory check. The original V3 design documents contain historical proposals; the later development and acceptance record describes the implemented pipeline.

## V3: verified state and open evidence

The isolated V3 engineering pipeline passed integration checks for collection, replay, checkpoint/resume, and short frozen evaluation. Short training is still diagnostic. In the final five-scenario zero-velocity diagnostic, reported RMSE is roughly 5.89–13.88 rad/s. Brief apparent success may result from stopping at a joint limit. All reported runs remain `validated=false`.

Long training, sustained force, velocity, holding and obstacle-release behavior, transfer to unseen structures, and faster biped learning remain unverified. The GPU physics backend was checked for physical correspondence but still has per-step host transfers; high-throughput full-device collection was not established. These limits should accompany any claim made from the saved V3 weights.

## Code-language audit

The original code contained Chinese user-facing strings in the evaluation web app, two tests, and the V3 coverage heading. These strings and their paired tests were translated in this copy. A scan of readable project files found no remaining Han characters; third-party files under `.venv` and binary training artifacts were left intact.

## Source documents

The documents in `docs/`, `v3/docs/`, and the READMEs have been translated into English. This summary highlights the conclusions and implementation boundaries across those detailed records.
