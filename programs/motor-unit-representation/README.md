# Single-Actuator Two-Link Local Behavioral Representation (Asymmetric V3 Architecture)

**Program Slug**: `motor-unit-representation`
**Portfolio Priority**: Track 2
**Queue Status**: `COMPLETE` (B01–B04 adversarial round finished 2026-10-24)

---

## 1. Core Research Problem

Conventional robot control and behavior foundation models (BFMs) treat the entire multi-DoF robot body as an indivisible state-action space. Every morphology change, link replacement, or actuator upgrade invalidates the policy and representation. This program investigates the **bottom-up modularity hypothesis**:

> Can a single active rotary actuator and its two adjacent rigid links (fixed housing link $P$ and driven output link $D$), using only motor-side proprioception and calibrated link-frame kinematics at deployment time while leveraging high-dimensional privileged physical context during training, learn a **16-dimensional local Forward-Backward (FB) behavioral representation** $z \in \mathcal{S}^{15}(4)$ that serves as a morphology-agnostic local actuation interface?

Specifically, the V3 asymmetric local representation (`LOCAL_RESPONSE_ASYM_FB_V3`) separates deployment-time observability from training-time physical disambiguation:
- **Backward Outcome Encoder $B_\omega(g_{13})$**: Reads a 13-dimensional next-step local response vector $g_{13}$ (joint angle, angular velocity, causal 5-point linear-fit angular acceleration $\widehat{\ddot{q}}$, tip position/velocity/acceleration in housing frame $M$, and clipped normalized torque command $u_{\mathrm{clip}}$) and projects onto the 16-D sphere of radius $\sqrt{16} = 4.0$.
- **Fast/Slow History Local Actor $\pi_\theta(x_{137}, z_{16})$**: Reads a 137-dimensional causal proprioceptive history (8-step fast window at $20\text{ ms}$ + 8-segment slow summary over $320\text{ ms}$ + static motor/link geometry parameters) and a 16-D latent command $z_{16}$ to output a scalar normalized torque command $a \in [-1, 1]$.
- **Privileged Dual Forward Networks $F_{\eta_1, \eta_2}(x_{137}, p_{5065}, a, z_{16})$**: Read $x_{137}$ plus a 5,065-dimensional privileged physical context tensor $p_{5065}$ (comprising 4,822 physical/solver/contact/disturbance/constraint fields and 243 historical privileged summary dimensions across 22 explicit schema boundaries) during training only, and are discarded at deployment.

---

## 2. Verified Baseline Evidence vs Unproven Extrapolations

### 2.1 Verified Engineering Facts
- **V2 Purely Proprioceptive Baseline Failure**: A symmetric V2 baseline (`d_z = 16`, symmetric `x = g = 131` dims without privileged $F$ inputs) was trained to `20,032,000` transitions (`77,218` updates), but its evaluation ledger recorded `validated = false` (`post_gate_eval = null`), failing to disambiguate external loading, contact constraints, and multi-configuration dynamics.
- **V3 Asymmetric Prototype & Short-Run Verification**:
  - Parameter budget: Local Actor `207,617` + Backward $B$ `74,000` = **`281,617` deployed parameters**; each Forward network $F_1, F_2$ has `2,805,008` parameters = **`5,891,633` total online parameters**.
  - Bounded CPU FP32 replay buffer: `32,768` rule transitions + `65,536` policy transitions = `98,304` total transitions (`4.097 GB` tensor allocation, `4.694 GB` verified peak RSS).
  - Short-run verification ledger: `8,096` valid control transitions (`P0 = 800`), `101` CUDA updates, bitwise-exact checkpoint resume (`resume_diff_norm = 0.0`), and ONNX/TorchScript deployment export verified.
- **Current Scientific Gaps (`coverage_ready = false`)**:
  - In the short-run verification ledger, zero-velocity command tracking ($\dot{q} = 0$) still exhibits high RMSE (`5.89` to `13.88 rad/s`), and both sustained load-hold (`sustained_load_hold_count = 0`) and post-load recovery (`post_load_recovery_count = 0`) coverage gates remain unfulfilled.
  - Nine concrete code/specification audit findings remain open (see `baseline/03-v3-engineering-status-evidence-and-open-audit-issues.md`).

### 2.2 Claims Explicitly Not Yet Established
- **No validated general single-actuator competence yet**: The V3 short run proves engineering pipeline integrity, not converged multi-regime motor control.
- **No validated multi-joint / bipedal acceleration yet**: Whether freezing a converged V3 single-actuator $(B, \pi)$ module accelerates downstream 2-DoF leg or whole-body bipedal learning remains an untested downstream hypothesis.

---

## 3. Directory Structure

- `PROGRAM_CHARTER.md`: Scope, hard technical boundaries, falsifiable hypotheses, and verification gates.
- `QUEUE.md`: Research packet queue (`B01`–`B04`), status `COMPLETE`.
- `baseline/`:
  - `01-motor-unit-proprioception-and-representation-design.md`: Coordinate frames ($M, P, D$), encoder zero/direction calibration, causal 5-point acceleration estimator, tip kinematics, observability limits, and reverse-engineered upper-layer calling interface.
  - `02-v3-asymmetric-network-and-training-specification.md`: Full `LOCAL_RESPONSE_ASYM_FB_V3` specification, V2-to-V3 gap table, exact $g_{13}$, $x_{137}$, and $p_{5065}$ (22-boundary) schemas, parameter counts, E0–E4 scene distribution (144 configuration groups), rule calibration controller, and rank-16 Frobenius lower bound analysis.
  - `03-v3-engineering-status-evidence-and-open-audit-issues.md`: V2 vs V3 empirical ledgers, bounded memory verification, frozen evaluation metrics, and detailed specification of the 9 open audit issues.
- `briefs/`:
  - `B01-privileged-forward-causal-boundary-and-future-force-leakage.md`
  - `B02-sustained-load-schedule-rule-calibration-and-coverage-gates.md`
  - `B03-rank16-representation-capacity-across-144-morphology-regimes.md`
  - `B04-hierarchical-composition-of-local-motor-units-for-multi-joint-control.md`
- `reviews/`, `synthesis/`, `method-issues/`, `claims/`, `packets/`, `logs/`: Operational directories for the adversarial research cycle.
