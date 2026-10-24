# Baseline 01: Single-Actuator Proprioception, Calibrated Two-Link Kinematics, and Upper-Layer Calling Interface

## 1. Motivation: Bottom-Up Modularity from the Single Actuator Unit

In physical robots, every whole-body motion ultimately reduces to local rotary actuators applying torque between two adjacent links against gravity, link inertia, joint friction, mechanical end-stops, and external contact or payload forces. If each **single-actuator two-link unit** (consisting of a fixed housing link $P$, an active rotary joint with axis $\hat{u}$, and a driven output link $D$) is equipped with a standardized local behavioral representation $(B_\omega, \pi_\theta)$, then:
1. **Morphology Standardization**: Hardware differences (encoder zero offset, positive rotation sign, torque constant, link length $L_D$, and center-of-mass offset) are absorbed at the local unit boundary.
2. **Low-Dimensional Upper Interface**: Instead of learning raw torque commands from scratch for every new morphology, an upper-level controller or planner specifies desired local physical responses via a 16-dimensional latent vector $z_{16} \in \mathcal{S}^{15}(4)$ (or blends encoded target responses $z = \operatorname{proj}(B_\omega(g_{\mathrm{des}}))$).

---

## 2. Coordinate Frames, Encoder Calibration, and Causal Kinematics

### 2.1 Local Coordinate Frame Contract ($M$, $P$, $D$)
- **Motor Housing Frame $M$**: Origin at the rotary joint center; $z_M$-axis aligned with the calibrated positive rotation axis $\hat{u}$; $x_M$-axis aligned with the zero-angle reference line fixed to housing link $P$; $y_M = z_M \times x_M$.
- **Parent / Housing Link $P$**: Rigidly attached to the motor stator/housing. Its orientation relative to world gravity is captured by the local gravity unit vector $g^M \in \mathbb{R}^3$ (or parent attitude available to the unit).
- **Driven / Output Link $D$**: Rigidly attached to the motor rotor/output flange of length $L_D$, with tip position $p_{\mathrm{tip},D}^M \in \mathbb{R}^3$ expressed in housing frame $M$.

### 2.2 Encoder Direction and Zero-Offset Calibration
Raw motor encoders report uncalibrated angle $q_e$ and velocity $\dot{q}_e$ with hardware-dependent sign $s \in \{-1, +1\}$ and zero offset $\beta \in (-\pi, \pi]$. Before entering any representation or control buffer, raw readings are mapped to calibrated joint coordinates $(q_c, \dot{q}_c)$:
$$
q_c = \operatorname{wrap}_{(-\pi, \pi]}\bigl(s \cdot q_e + \beta\bigr), \qquad \dot{q}_c = s \cdot \dot{q}_e.
$$
The distance to lower and upper mechanical stops $(q_{\min}, q_{\max})$ is normalized into margins:
$$
d_{\min} = \operatorname{clip}\!\left(\frac{q_c - q_{\min}}{q_{\max} - q_{\min}}, 0, 1\right), \qquad d_{\max} = \operatorname{clip}\!\left(\frac{q_{\max} - q_c}{q_{\max} - q_{\min}}, 0, 1\right).
$$

### 2.3 Causal 5-Point Linear-Fit Angular Acceleration $\widehat{\ddot{q}}_t$
Single-step finite differences $(\dot{q}_t - \dot{q}_{t-1})/\Delta t$ amplify encoder quantization noise, whereas non-causal central differences leak future information. At $200\text{ Hz}$ sampling ($\Delta \tau = 5\text{ ms}$, so 5 samples span a $20\text{ ms}$ control interval / $40\text{ ms}$ causal window), the angular acceleration $\widehat{\ddot{q}}_t$ is computed via causal ordinary least-squares linear regression over the 5 most recent calibrated velocities $\{\dot{q}_{t-4}, \dot{q}_{t-3}, \dot{q}_{t-2}, \dot{q}_{t-1}, \dot{q}_t\}$:
$$
\widehat{\ddot{q}}_t = \frac{-2\,\dot{q}_{t-4} - \dot{q}_{t-3} + \dot{q}_{t-1} + 2\,\dot{q}_t}{10\,\Delta \tau}.
$$
This filter is strictly causal, linear, zero-bias for constant acceleration, and suppresses high-frequency encoder jitter by $5\times$ compared to 2-point differencing.

### 2.4 Driven Link Tip Position, Velocity, and Causal Acceleration in Frame $M$
Given calibrated joint angle $q_c$, angular velocity $\dot{q}_c$, causal angular acceleration $\widehat{\ddot{q}}_t$, and link tip vector $r_D(q_c) = p_{\mathrm{tip},D}^M(q_c) \in \mathbb{R}^3$ rotating about axis $\hat{u} = [0, 0, 1]^\top$:
$$
p_{\mathrm{tip},D}^M(q_c) = R_z(q_c)\,r_D^0, \qquad v_{\mathrm{tip},D}^M = (\dot{q}_c\,\hat{u}) \times p_{\mathrm{tip},D}^M(q_c),
$$
$$
\widehat{a}_{\mathrm{tip},D}^M = (\widehat{\ddot{q}}_t\,\hat{u}) \times p_{\mathrm{tip},D}^M(q_c) + (\dot{q}_c\,\hat{u}) \times \bigl((\dot{q}_c\,\hat{u}) \times p_{\mathrm{tip},D}^M(q_c)\bigr).
$$
Notice that $v_{\mathrm{tip},D}^M$ and $\widehat{a}_{\mathrm{tip},D}^M$ couple the angular response $(\dot{q}_c, \widehat{\ddot{q}}_t)$ with the physical lever arm $L_D = \|r_D^0\|_2$, naturally encoding linear momentum and centripetal/tangential tip kinematics across varying link lengths.

---

## 3. Observability Boundaries and the Need for Asymmetric Training

### 3.1 What Proprioception Alone Can and Cannot See
From a single transition $(q_c, \dot{q}_c, \widehat{\ddot{q}}_t, u_{\mathrm{clip}})$, the net generalized load torque $\tau_{\mathrm{load}}$ can be inferred implicitly via the rotor/link equation of motion:
$$
J_{\mathrm{eff}}\,\widehat{\ddot{q}}_t + b\,\dot{q}_c + \tau_{\mathrm{fric}}(\dot{q}_c) + \tau_{\mathrm{grav}}(q_c) - \tau_{\mathrm{ext},t} = S \cdot u_{\mathrm{clip},t},
$$
so the short-term history $x_{137}$ (spanning $160\text{ ms}$ at full $20\text{ ms}$ resolution plus $320\text{ ms}$ of slow summaries) allows an online actor $\pi_\theta(x_{137}, z_{16})$ to estimate current inertia, gravity bias, and persistent external torque.

However, during **Bellman bootstrapping of the multi-step successor representation $F$**, a purely proprioceptive forward network $F(x_{137}, a, z_{16})$ faces fundamental observability aliasing:
1. It cannot distinguish whether a sudden stall ($\dot{q} \approx 0, \widehat{\ddot{q}} \approx 0$ under high torque $u$) is caused by a rigid mechanical end-stop, an elastic spring-damper contact obstacle, or a temporary external disturbance pulse that is about to release.
2. It cannot see the exact contact geometry, friction coefficients, or solver constraint states of the surrounding physical scene.

### 3.2 Asymmetric Resolution (`LOCAL_RESPONSE_ASYM_FB_V3`)
To prevent representation collapse without sacrificing deployment autonomy:
- **Deployed Modules ($B_\omega$ and $\pi_\theta$)**: Strictly restricted to local observable vectors $g_{13}$ and $x_{137}$.
- **Training-Only Dual Forward Critics ($F_{\eta_1}, F_{\eta_2}$)**: Provided with both $x_{137}$ and the full 5,065-dimensional privileged physical context $p_{5065}$ so that Bellman targets accurately separate free-space motion (E0), boundary stops (E1), elastic/rigid contact (E2), sustained external loading (E3), and post-load recovery (E4).

---

## 4. Upper-Layer Calling Modes Over the Frozen Local Unit

Once $(B_\omega, \pi_\theta)$ are trained and frozen, an upper-level controller can drive the motor unit through three mathematically equivalent interfaces:
1. **Direct Latent Policy Mode**: Upper planner outputs $z_{16} \in \mathcal{S}^{15}(4)$ at $50\text{ Hz}$, which $\pi_\theta(x_{137}, z_{16})$ translates into $u_{\mathrm{clip}} \in [-1, 1]$.
2. **Target Outcome Encoding Mode**: Upper planner specifies a desired next-step local kinematic/torque state $g_{13}^{\mathrm{des}}$ (e.g., target angle $q^\star$, zero velocity $\dot{q}^\star = 0$, zero acceleration $\widehat{\ddot{q}}^\star = 0$) and queries $z_{16} = B_\omega(g_{13}^{\mathrm{des}})$.
3. **Weighted Multi-Objective Blending Mode**: Given a set of candidate outcome features $\{g_{13}^{(m)}\}_{m=1}^M$ with weights $\{w_m\}$, the upper layer commands:
   $$
   z_{16} = \sqrt{16}\,\frac{\sum_{m=1}^M w_m B_\omega(g_{13}^{(m)})}{\bigl\|\sum_{m=1}^M w_m B_\omega(g_{13}^{(m)})\bigr\|_2 + 10^{-8}}.
   $$
