# GPU & MuJoCo Simulation / Verification Package (`gpu_experiments/`)

This directory contains the self-contained PyTorch + MuJoCo simulation, verification, and 4-arm ablation suite for `fb-beyond-imitation-acceleration` (`B01`–`B05`), designed for both **Google Colab GPU execution** (`colab_gpu_runner.ipynb`) and **local pre-registered spike execution** (`run_all_experiments.py`).

## Files

- `fb_core.py`: Core neural architectures and operators (`BackwardMapB`, `ForwardEnsembleF`, `ConditionedLowLevelActor`, `RecurrentLatentPlanner`, `RecurrentTaskTwinCritic`, `RunningMeanStdNormalizer`, `EMAWhiteningTracker`, `sample_ufo_mixed_z`).
- `physics_env.py`: Real MuJoCo 3.17 multi-link 3D obstacle traversal environment (`MuJoCoObstacleTraversalR21Env`) with the 4-substep R2.1 terminal boundary state machine (`invalid` > `severe_penetration` > `success` > `timeout`) plus batched `DifferentiableContactPlant`.
- `run_b01_gram_spike.py`: Spectral conditioning $\kappa(\Sigma_B)$, effective rank, linear reward cancellation vs single-state goal bias, and damped Cholesky whitening (`B01`).
- `run_b02_nonstationarity_spike.py`: UFO BN single-pass update & freeze invariance, `behavior_z` immutability, behavioral/encoder drift metrics, and full-prefix zero-hidden RNN burn-in (`B02`).
- `run_b03_contact_aliasing_spike.py`: Kinematic-only $B(m)$ contact aliasing, perceptive $F/\pi$ disambiguation, and isokinematic multi-force bottleneck verification (`B03`).
- `run_b04_four_arm_ablation.py`: Controlled 4-arm ablation comparing first-action FB successor derivatives ($H=0$) vs $H \in \{1, 4, 8, 16, 32\}$ pathwise differentiable world-model rollouts with FB terminal bootstrap (`B04`).
- `run_b05_r21_verification_suite.py`: Three-part R2.1 terminal boundary verification on real MuJoCo substeps and `PoolQuotaSchedule` / Wilson lower-bound curriculum verification (`B05`).
- `colab_gpu_runner.ipynb`: Self-contained Google Colab GPU notebook packing all modules and outputting `colab_gpu_results.json`.
