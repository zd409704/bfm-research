# Baseline 02: V3 Asymmetric Network Architecture, 22-Boundary Schema, and E0–E4 Training Protocol (`LOCAL_RESPONSE_ASYM_FB_V3`)

## 1. Evolution from V2 to V3 Asymmetric Architecture

| Architectural Dimension | V2 Baseline (`SYM_PROPRIO_V2`) | V3 Specification (`LOCAL_RESPONSE_ASYM_FB_V3`) | Rationale for V3 Upgrade |
|---|---|---|---|
| **Backward Input $B$** | Symmetric 131-D history vector $g_{131} = x_{131}$ | **13-D single-step local outcome $g_{13}$** | $B$ should encode the reached physical outcome state, not the 160–480 ms history prefix. |
| **Actor Input $\pi$** | 131-D proprioceptive history + $z_{16}$ | **137-D fast/slow proprioceptive history $x_{137}$ + $z_{16}$** | Adds explicit stop margins, static geometry/drive descriptors, and 8-segment slow history. |
| **Forward Input $F_1, F_2$** | Symmetric $x_{131} + a + z_{16}$ (no privileged state) | **Asymmetric $x_{137} + p_{5065} + a_1 + z_{16}$** | Resolves contact/load/stop non-observability during Bellman target computation. |
| **Replay Architecture** | Unstratified policy ring buffer | **Stratified CPU FP32 Replay (`32,768` rule + `65,536` policy)** | Prevents early policy collapse from erasing stable holding/tracking transitions. |
| **Scene Regimes** | Unbalanced random torque/target sweeps | **5 Stratified Regimes E0–E4 (`20/15/20/15/30%`) across 144 morphology groups** | Explicitly enforces boundary, contact, sustained-load, and recovery coverage. |

---

## 2. Exact Tensor Schemas: $g_{13}$, $x_{137}$, and $p_{5065}$

### 2.1 Backward Outcome Vector $g_{13} \in \mathbb{R}^{13}$
Computed at the next control boundary $t+1$ in calibrated housing frame $M$:
1. $[\cos q_{c,t+1},\, \sin q_{c,t+1}] \in \mathbb{R}^2$: Continuous trigonometric joint angle representation.
2. $\dot{q}_{c,t+1} \in \mathbb{R}^1$: Calibrated angular velocity ($\mathrm{rad/s}$).
3. $\widehat{\ddot{q}}_{t+1} \in \mathbb{R}^1$: Causal 5-point linear-fit angular acceleration ($\mathrm{rad/s^2}$).
4. $p_{\mathrm{tip},D,t+1}^M \in \mathbb{R}^3$: Driven link tip position in housing frame $M$ ($\mathrm{m}$).
5. $v_{\mathrm{tip},D,t+1}^M \in \mathbb{R}^3$: Driven link tip linear velocity in frame $M$ ($\mathrm{m/s}$).
6. $\widehat{a}_{\mathrm{tip},D,t+1}^M \in \mathbb{R}^3$: Driven link tip linear acceleration in frame $M$ ($\mathrm{m/s^2}$).
*(Note: In variants where scalar torque effort or boundary margin replaces one tip coordinate, the exact 13-field layout is locked by the V3 schema manifest; total dimension is strictly `13`.)*

### 2.2 Fast/Slow Proprioceptive History Vector $x_{137} \in \mathbb{R}^{137}$
Constructed causally at control step $t$ ($\Delta t_{\mathrm{ctrl}} = 20\text{ ms}$, $50\text{ Hz}$):
- **Current Calibrated Instantaneous State (`17` dims)**:
  $[\cos q_c, \sin q_c, q_c, \dot{q}_c, \widehat{\ddot{q}}, d_{\min}, d_{\max}, p_{\mathrm{tip},D}^M(3), v_{\mathrm{tip},D}^M(3), \widehat{a}_{\mathrm{tip},D}^M(3), u_{\mathrm{prev}}]$.
- **Fast History Window (`8 steps x 9 dims = 72` dims, covering $160\text{ ms}$ at $20\text{ ms}$ intervals)**:
  Per step: $[\cos q_c, \sin q_c, \dot{q}_c, \widehat{\ddot{q}}, d_{\min}, d_{\max}, v_{\mathrm{tip},\parallel}, a_{\mathrm{tip},\parallel}, u_{\mathrm{clip}}]$.
- **Slow Summary Window (`8 segments x 5 dims = 40` dims, covering $320\text{ ms}$ via $40\text{ ms}$ segment averages)**:
  Per segment: mean angle $[\overline{\cos q_c}, \overline{\sin q_c}]$, mean angular velocity $\overline{\dot{q}_c}$, mean acceleration $\overline{\widehat{\ddot{q}}}$, and mean applied normalized torque $\overline{u_{\mathrm{clip}}}$.
- **Static Calibration & Nominal Unit Descriptor (`8` dims)**:
  $[q_{\min}, q_{\max}, \Delta q_{\mathrm{range}}, L_D, r_{\mathrm{com},D}, S_{\mathrm{nom}}, \dot{q}_{\mathrm{lim}}, \mathbf{1}_{\mathrm{calibrated}}]$.
  **Total**: $17 + 72 + 40 + 8 = 137$ dimensions.

### 2.3 Privileged Physical Context Vector $p_{5065} \in \mathbb{R}^{5065}$
Used **exclusively** by $F_{\eta_1, \eta_2}$ during training. It consists of **4,822 physical/solver/environment dimensions** plus **243 historical privileged feature-memory dimensions** partitioned across **22 explicit schema boundaries**:
- **Groups 1–6 (Multi-Substep High-Rate Trajectory & Solver States, `1,920` dims)**: Substep-level ($4 \times 5\text{ ms}$) generalized positions, velocities, accelerations, actuator forces, constraint forces, and solver residuals.
- **Groups 7–12 (Link Inertial, Mass, Friction, and Drive Plant Parameters, `1,024` dims)**: Exact link mass $m_D$, inertia tensor $I_D$, COM vector, viscous damping $b$, Coulomb stiction $\tau_c$, gear backlash/compliance, thermal/saturation scale $S = 1.25 C_0$, and nominal capacity $C_0 \in \{3, 6, 9\}\text{ N}\cdot\text{m}$.
- **Groups 13–17 (Contact Geometry, Obstacle Field, and Mechanical Stop Constraints, `1,152` dims)**: Signed distances to contact surfaces, normal/tangential contact forces, contact Jacobian projections, end-stop spring-damper penetration states, and active constraint masks.
- **Groups 18–21 (External Load & Disturbance Generator States, `726` dims)**: External torque profile parameters (constant bias, ramp slope, sinusoidal frequency/phase, impulse countdown/magnitude, post-load release timer) and scene regime one-hot `E0..E4`. *(See Audit Issue #4 in `baseline/03` regarding causal vs future-window entries inside this block.)*
- **Group 22 (Privileged Feature Memory Summary, `243` dims)**: Exponential moving averages and multi-scale summaries of privileged load, contact impulse, and slip history across the preceding $320\text{ ms}$.
  **Total**: $4,822 + 243 = 5,065$ dimensions.

---

## 3. Exact Network Parameter Budgets

| Network Module | Input Dim | Architecture Specification | Output Dim | Parameter Count | Deployed? |
|---|---:|---|---:|---:|---|
| **Local Actor $\pi_\theta$** | `153` (`137 + 16`) | Two-branch stem (`x[137]->256`, `z[16]->128`) + residual MLP `[256, 256, 128]` with LayerNorm & SiLU $\to \tanh$ | `1` | **`207,617`** | **Yes** |
| **Backward Encoder $B_\omega$** | `13` (`g13`) | MLP `[128, 256, 128]` with LayerNorm & SiLU $\to$ L2 sphere projection $\sqrt{16}=4.0$ | `16` | **`74,000`** | **Yes** |
| **Deployed Unit Total** | — | $B_\omega + \pi_\theta$ | — | **`281,617`** | **Yes** |
| **Forward Critic $F_{\eta_1}$** | `5,219` (`137+5065+1+16`) | Privileged compressor (`5065->512`) + state-action-latent fusion `[1024, 1024, 512]` $\to$ linear readout | `16` | **`2,805,008`** | No (Train only) |
| **Forward Critic $F_{\eta_2}$** | `5,219` (`137+5065+1+16`) | Identical independent twin architecture | `16` | **`2,805,008`** | No (Train only) |
| **Total Online Model** | — | $\pi_\theta + B_\omega + F_{\eta_1} + F_{\eta_2}$ | — | **`5,891,633`** | — |

---

## 4. Physical Diversity Matrix (144 Configurations) and E0–E4 Scene Regimes

### 4.1 144 Morphology-Stroke Configuration Groups
- **36 Geometry & Inertial Seeds**: Spanning link lengths $L_D \in [0.08, 0.45]\text{ m}$, payload masses, COM offsets, friction/damping parameters, and three nominal drive capacity tiers:
  $$
  C_0 \in \{3.0,\, 6.0,\, 9.0\}\text{ N}\cdot\text{m}, \qquad S_{\max} = 1.25\,C_0 \in \{3.75,\, 7.50,\, 11.25\}\text{ N}\cdot\text{m}.
  $$
- **4 Mechanical Stroke Profiles**: Varying angular travel ranges $\Delta q_{\mathrm{range}} = q_{\max} - q_{\min}$ and asymmetric stop placements relative to gravity.
- **Total Configuration Matrix**: $36 \times 4 = 144$ distinct physical unit configurations.

### 4.2 Five Stratified Physical Regimes (E0–E4)

| Scene ID | Regime Name | Target Quota | Physical Dynamics & Disturbance Specification | Primary Representation Goal |
|---|---|---:|---|---|
| **E0** | `FREE_SPACE_NOMINAL` | **20%** | Unobstructed rotation under gravity, link inertia, and internal joint friction across full stroke. | Smooth velocity/position tracking and static gravity holding ($\dot{q}=0$). |
| **E1** | `BOUNDARY_LIMIT_ESCAPE` | **15%** | Initialization near or against mechanical stops ($d_{\min} < 0.05$ or $d_{\max} < 0.05$) with inward/outward commands. | Non-oscillatory stop departure without integral windup or limit slamming. |
| **E2** | `COMPLIANT_AND_RIGID_CONTACT` | **20%** | External obstacle surfaces inside the stroke with varying stiffness/damping and restitution. | Contact transition stability and bounded contact force modulation. |
| **E3** | `SUSTAINED_EXTERNAL_LOAD` | **15%** | Persistent external torque bias/ramp opposing or assisting motion for $\ge 25$ consecutive steps ($0.5\text{ s}$). | Steady-state load compensation and zero-velocity holding under sustained torque. |
| **E4** | `POST_LOAD_IMPULSE_RECOVERY` | **30%** | Abrupt external torque step release or impulse perturbation followed by recovery window. | Fast transient damping and return to steady holding/tracking without overshoot. |

---

## 5. Rule Calibration Controller and Stratified Replay Distribution $\rho$

### 5.1 Inertia-Scaled Rule Calibration Controller (`rule_calibration`)
Because a randomly initialized policy $\pi_\theta(x_{137}, z_{16})$ cannot naturally generate sustained static holding ($\dot{q} \approx 0, \widehat{\ddot{q}} \approx 0$) under heavy gravity or E3 external loads, V3 defines an analytical rule controller used during P0 warmup and for populating the `32,768`-transition rule replay partition:
$$
u_{\mathrm{rule},t} = \operatorname{clip}\!\left(\frac{\hat{\tau}_{\mathrm{bias},t} + J_{\mathrm{nom}}\bigl(k_p(q_{\mathrm{ref},t} - q_{c,t}) + k_d(\dot{q}_{\mathrm{ref},t} - \dot{q}_{c,t})\bigr) + \tau_{I,t}}{S_{\max}},\, -1,\, 1\right),
$$
where $\hat{\tau}_{\mathrm{bias},t}$ compensates estimated static gravity/load torque, $(k_p, k_d)$ are scaled by nominal inertia $J_{\mathrm{nom}}$ to maintain uniform closed-loop bandwidth across all 36 geometry seeds, and $\tau_{I,t}$ is a bounded anti-windup integral term that freezes whenever $|u_{\mathrm{rule},t}| = 1$ or the joint is within mechanical stop margins.

### 5.2 Stratified Replay Buffer and Reference Distribution $\rho$
- **Replay Split**: Fixed CPU FP32 buffer of `98,304` transitions = `32,768` rule transitions (`1/3`) + `65,536` online policy transitions (`2/3`).
- **Mini-Batch Sampling**: Each training update samples a stratified batch across `(rule vs policy)` and across scenes `E0..E4`, inducing the reference outcome distribution $\rho(g_{13})$ over which $\Sigma_B = \mathbb{E}_{g \sim \rho}[B_\omega(g)B_\omega(g)^\top] \approx I_{16}$ is regularized.

---

## 6. Theoretical Rank-16 Bottleneck Across 144 Configurations

Suppose $K = 144$ configuration groups had completely disjoint, mutually orthogonal successor operators $\{M^{(k)}\}_{k=1}^{144}$ sharing a single unconditioned rank-$d_z$ ($d_z = 16$) representation. By the Eckart-Young-Mirsky theorem, any rank-16 subspace shared across $K = 144$ orthogonal unit-Frobenius operators incurs a minimum root-mean-square relative Frobenius approximation error of:
$$
\mathcal{E}_{\min}(d_z=16, K=144) = \sqrt{1 - \frac{d_z}{K}} = \sqrt{1 - \frac{16}{144}} = \sqrt{\frac{8}{9}} \approx 0.9428.
$$
V3 avoids this worst-case orthogonal lower bound by two structural mechanisms:
1. **Shared Physical Outcome Coordinates in $g_{13}$**: $B_\omega(g_{13})$ encodes normalized kinematic/tip outcomes in housing frame $M$, which share a low-dimensional manifold across all 144 configurations.
2. **Configuration Conditioning in $F$ and $\pi$**: Both $x_{137}$ (via the 8-D static descriptor and 480 ms history) and $p_{5065}$ (via explicit mass, inertia, link length, and capacity $C_0$) condition the forward map $F_{\eta}(x_{137}, p_{5065}, a, z_{16})$ and actor $\pi_\theta(x_{137}, z_{16})$, so $F$ rotates the configuration-specific dynamics into the shared 16-D outcome basis of $B_\omega(g_{13})$.
