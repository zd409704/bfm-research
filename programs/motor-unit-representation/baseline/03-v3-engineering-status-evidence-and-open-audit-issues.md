# Baseline 03: V3 Engineering Status, Empirical Verification Ledgers, and the 9 Open Audit Issues

## 1. Empirical Comparison: V2 Full Run vs V3 Short-Run Verification

| Metric / Verification Field | V2 Baseline Run (`SYM_PROPRIO_V2`) | V3 Short-Run Verification (`LOCAL_RESPONSE_ASYM_FB_V3`) | Status & Interpretation |
|---|---|---|---|
| **Total Valid Control Transitions ($W$)** | `20,032,000` | `8,096` (including `P0 = 800` warmup) | V3 run is a short pipeline verification smoke test, not a full training run. |
| **Total Gradient Updates** | `77,218` | `101` (CUDA) | Confirms forward/backward/actor optimization step execution. |
| **Replay Memory Footprint** | Unbounded / host-dependent | **`4.097 GB` tensor / `4.694 GB` peak RSS** (`98,304` CPU FP32 transitions) | Strictly within bounded host memory budget. |
| **Checkpoint Resume Parity** | Not bitwise audited | **`resume_diff_norm = 0.0`** (bitwise exact) | Verified deterministic state restoration. |
| **Deployment Export** | None | **Verified** (`B` + `actor` = `281,617` params) | Confirms $p_{5065}$ and $F_{1,2}$ are cleanly stripped at deployment. |
| **Zero-Velocity Holding ($\dot{q}=0$) RMSE** | Unvalidated (`post_gate_eval = null`) | **`5.89` – `13.88 rad/s`** (after 101 updates) | Far above target holding threshold; controller has not yet learned static holding. |
| **`sustained_load_hold_count`** | `0` | **`0`** | Gate failed (`coverage_ready = false`). |
| **`post_load_recovery_count`** | `0` | **`0`** | Gate failed (`coverage_ready = false`). |
| **Overall Validation Flag** | `validated = false` | **`coverage_ready = false`** | Pipeline is verified; scientific convergence and coverage remain open. |

---

## 2. Detailed Specification of the 9 Open V3 Audit Issues

A rigorous code-and-specification audit of the V3 implementation identified **9 concrete discrepancies** between the theoretical V3 design (`baseline/01` and `baseline/02`) and the current implementation. Resolving these 9 issues is the prerequisite for launching full-scale V3 training.

### Issue 1: Scene Label vs Step-Level External Torque Schedule Desynchronization
- **Mechanism**: Episodes labeled `E3_SUSTAINED_LOAD` or `E4_POST_LOAD_RECOVERY` at the scene-allocation level do not consistently enforce the step-level external torque generator to sustain load for $\ge 25$ consecutive steps (`0.5 s`) or trigger a deterministic release edge followed by a quiet recovery window.
- **Consequence**: The coverage evaluator scans rollout trajectories for valid sustained-load and post-load recovery windows, finds zero qualifying segments (`sustained_load_hold_count = 0`, `post_load_recovery_count = 0`), and permanently latches `coverage_ready = false`.

### Issue 2: `rule_calibration` Implemented in Standalone Helper Module but Not Wired into Main Collector
- **Mechanism**: The inertia-scaled PD + static gravity/load bias + anti-windup integral controller (`rule_calibration`) is implemented and unit-tested in its helper module, but the main rollout collector (`P0` warmup and the `32,768` rule replay partition) still falls back to a legacy uncalibrated open-loop/simple PD sampler.
- **Consequence**: The `rule` partition of the replay buffer lacks genuine static load-holding ($\dot{q} \approx 0, \widehat{\ddot{q}} \approx 0$ under non-zero gravity/external torque) transitions across the 144 morphology configurations, starving $B_\omega(g_{13})$ and $\pi_\theta$ of equilibrium anchors.

### Issue 3: Cross-Coverage Ledger Field Missing (`cross_coverage_144_x_5`)
- **Mechanism**: While marginal counts per scene (`E0..E4`) and per morphology seed are logged separately, the joint $144 \times 5 = 720$-cell cross-coverage matrix (`configuration_group x scene_regime`) is either omitted or not enforced as a hard readiness gate in the evaluation summary JSON.
- **Consequence**: Rare configuration-scene pairs (especially high-capacity $C_0 = 9\text{ N}\cdot\text{m}$ units under E3/E4) can be under-sampled without triggering a cell-starvation alert.

### Issue 4: Acausal Future External Force Window Inside Privileged Input $p_{5065}$
- **Mechanism**: Within Groups 18–21 of $p_{5065}$, the privileged tensor packs future external disturbance torque values $\tau_{\mathrm{ext}, t+1:t+K}$ alongside current solver states, without cleanly separating **exogenous open-loop generator parameters** (which are causally fixed at episode/regime sampling time) from **state-dependent contact/reaction forces** at future steps $t+1..t+K$.
- **Consequence**: Feeding endogenous future reaction forces into $F_{\eta}(x_{137,t}, p_{5065,t}, a_t, z_{16})$ violates temporal causality in the Bellman backup and inflates training-time critic accuracy on transitions that cannot be predicted causally.

### Issue 5: Frozen Evaluation Panel Samples Non-Stationary Target Trajectories for $\dot{q}=0$ Holding Diagnostics
- **Mechanism**: In the frozen diagnostic evaluation panel, the zero-velocity holding metric (`zero_vel_rmse`) is evaluated on trajectories where the reference generator continues to inject step perturbations or moving target angles rather than clamping $g_{13}^{\mathrm{des}}$ to a pure static equilibrium target ($\dot{q}^\star = 0, \widehat{\ddot{q}}^\star = 0$) across all 5 regimes.
- **Consequence**: Conflates trajectory-tracking lag with static holding drift (`5.89–13.88 rad/s`).

### Issue 6: Batch Normalizer Update Asymmetry Between Rule Partition and Policy Partition
- **Mechanism**: Running mean/variance normalizers for $x_{137}$, $g_{13}$, and $p_{5065}$ are updated on every online policy rollout step before replay insertion, whereas transitions drawn from the `32,768` rule partition during mini-batch updates experience shifting normalizer statistics without balanced re-normalization.
- **Consequence**: Induces covariate shift on the `1/3` rule mini-batch slice as online policy exploration expands the state distribution.

### Issue 7: Orthonormalization Loss $\mathcal{L}_{\mathrm{orth}}$ Computed on Unstratified Sub-Batches
- **Mechanism**: The Gram matrix penalty $\mathcal{L}_{\mathrm{orth}}(B_\omega)$ is evaluated over raw mini-batch samples without inverse-probability weighting when scene quotas deviate from the nominal `(20%, 15%, 20%, 15%, 30%)` distribution during early P0/P1 ramp-up.
- **Consequence**: Early E0 free-space motions dominate the 16-D spherical subspace of $B_\omega(g_{13})$, compressing the angular distance allocated to E2 contact and E3/E4 load-holding outcomes.

### Issue 8: Action-Gradient Saturation Near $\tanh$ Boundaries in $\pi_\theta(x_{137}, z_{16})$
- **Mechanism**: Under heavy E3 loads requiring $|u_{\mathrm{clip}}| > 0.9$, the deterministic $\tanh$ output head of $\pi_\theta$ saturates, causing the policy gradient $\nabla_\theta F_{\eta}(x_{137}, p_{5065}, \pi_\theta(x_{137}, z_{16}), z_{16})^\top z_{16}$ to vanish ($\operatorname{sech}^2(\cdot) \to 0$) if $F_{\eta}$ has not yet learned a steep negative slope outside $[-1, 1]$.
- **Consequence**: Slows recovery once the actor saturates against a mechanical stop or heavy load.

### Issue 9: Absence of a Standardized 2-DoF / Multi-Joint Downstream Transfer Benchmark
- **Mechanism**: Although the stated goal of the project is to provide a reusable local behavioral interface for multi-joint limbs and bipedal locomotion, the repository currently contains only the single-actuator environment and lacks a canonical 2-DoF serial link (hip-knee or shoulder-elbow) benchmark that tests frozen $(B_\omega, \pi_\theta)$ under inter-joint inertial and Coriolis coupling.
- **Consequence**: Prevents direct empirical falsification of whether single-unit representations transfer when parent link $P$ undergoes large dynamic accelerations.
