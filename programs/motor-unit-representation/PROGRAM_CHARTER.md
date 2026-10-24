# Program Charter: Single-Actuator Two-Link Local Behavioral Representation

## 1. Mission Statement

Establish a mathematically rigorous, physically causal, and empirically verified local behavioral representation for a single active rotary joint and its two adjacent links ($P$ and $D$), resolving the 9 open V3 audit defects, closing the `coverage_ready` multi-regime training gates (E0–E4), and defining a falsifiable protocol for composing frozen local motor representations into multi-joint limb controllers.

---

## 2. Hard Technical Boundaries

1. **Deployment Proprioceptive Purity**: At deployment time, only the calibrated 137-D proprioceptive history $x_{137}$ and 13-D single-step outcome $g_{13}$ may be accessed by $\pi_\theta(x_{137}, z_{16})$ and $B_\omega(g_{13})$. No privileged force, contact, or environment solver fields from $p_{5065}$ may leak into deployed modules.
2. **Causal Integrity of Privileged Forward Inputs**: Even during training, the privileged context $p_{5065}$ fed to $F_{\eta_1, \eta_2}(x_{137,t}, p_{5065,t}, a_t, z_{16})$ must represent the physical regime, active load/contact state, and historical disturbance generator state at time $t$—or explicitly separate exogenous environment schedule parameters from endogenous future robot reactions.
3. **Zero Fabricated Coverage Metrics**: Coverage gates (`sustained_load_hold_count`, `post_load_recovery_count`, `limit_escape_rate`, `zero_vel_rmse`) must be computed on real physics rollouts across all 144 morphology/stroke configurations (`36` geometry seeds $\times$ `4` stroke profiles) and all 5 scene regimes (E0–E4).
4. **Strict Separation of Short-Run Pipeline Verification vs Converged Control**: No document may claim that the 101-update V3 smoke run demonstrates converged motor control.

---

## 3. Core Falsifiable Hypotheses

- **H1 (Causal Privileged Disambiguation)**: Replacing acausal future force lookahead in $p_{5065}$ with causal exogenous disturbance generator parameters + current/historical contact-force states preserves $> 95\%$ of $F$'s TD target explained variance while eliminating temporal causality violations.
- **H2 (Synchronized E3/E4 Load-Hold and Rule Calibration)**: Synchronizing the step-level external load schedule with `E3_SUSTAINED_LOAD` / `E4_POST_LOAD_RECOVERY` labels and routing P0 warmup + rule-replay quotas through the inertia-scaled PD + static-bias + anti-windup rule controller drives `sustained_load_hold_count` and `post_load_recovery_count` past their minimum readiness gates and reduces $\dot{q}=0$ RMSE below `0.35 rad/s`.
- **H3 (Rank-16 Cross-Morphology Factorizability)**: Although 144 completely orthogonal transition matrices would bound rank-16 Frobenius approximation error at $\sqrt{1 - 16/144} \approx 0.943$, conditioning $F(x_{137}, p_{5065}, a, z_{16})$ on explicit geometry/capacity features while keeping $g_{13}$ in normalized housing-frame coordinates allows a shared 16-D $B(g_{13})$ to achieve relative successor approximation error $< 0.20$ across all 144 configurations.
- **H4 (Multi-Joint Composition Gain)**: An upper-level 2-DoF or 6-DoF limb controller commanding $z_{16}^{(k)}$ across coupled local V3 motor units achieves faster sample convergence under payload/link-length perturbations than a flat torque policy of equal parameter count, provided inter-joint coupling forces are represented inside each unit's E2/E3 training distribution.
