# Baseline 05: Autonomous 3D Obstacle Traversal on a 29-DoF Humanoid Plant (v3.1.1 Training Design & R2.1 Implementation Specification)

## 1. Task Definition and Physical Geometry Contract

The autonomous obstacle-traversal task requires a 29-DoF torso-base humanoid robot (`dt_physics = 0.005` s, `decimation = 4`, `dt_control = 0.02` s, 50 Hz control, action `scale = 1.0` across all 29 joint position channels) to start from flat ground in front of a 3D box obstacle, traverse over obstacles of varying heights $h$, and establish a stable bipedal landing on the flat ground behind the obstacle.

### 1.1 Obstacle Geometry and Curriculum Bank
- **Fixed Box Depth and Width**: Depth $D = 0.3559550643\text{ m}$, width $W = 10.0\text{ m}$, bottom face resting on the ground plane ($z = 0$).
- **Demonstration Reference Source**: A single 859-frame, 50 Hz retargeted motion file recorded on an obstacle of height $h_{\mathrm{demo}} = 0.7044943571\text{ m}$ (`SHA256: 1be258504c22886147b8739fb8e4bf3689e0d707f59c2ce1b0505686a7fa09c8`).
- **Discrete Training Height Bank**:
  $$
  \mathcal{H}_{\mathrm{bank}} = \{0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70\}\text{ m}.
  $$
  Training begins with active quota allocated only to `{0.10, 0.20}` m. Each environment instance maintains a fixed height $h$ throughout an episode.

---

## 2. Architecture and Data Flow (Macro-Step $z$-Critic Formulation)

Unlike ball striking ($K_{\mathrm{hold}}=1$ with physical action-$Q$), 3D obstacle traversal requires sustained multi-step coordination (approach, takeoff, hand/foot placement, clearance, and landing). Therefore, v3.1.1 / R2.1 uses a **macro-step $z$-conditioned task critic $Q_{\phi_1, \phi_2}(H_t, c_t^{\mathrm{geom}}, z_{\mathrm{macro}})$** with macro horizon $K = 10$ control steps ($0.20\text{ s}$).

| Module | Exact Input Schema $\to$ Output | Training Objective & Role of Demonstrations |
|---|---|---|
| **Backward Map $B_\omega$** | Single-frame `m[229]` $\to$ `z[256]` on sphere of radius $\sqrt{256}=16$ (`hidden = 256 x 1`) | Updated purely on real replay transitions via FB successor + orthogonality loss. Demonstrations are encoded in `eval/no_grad` mode only; zero supervised imitation loss. |
| **Forward Ensemble $F_{\eta_1, \eta_2}$** | Policy observation `o` (without reference motion), `z[256]`, applied action `a_applied[29]` $\to$ `[256]` per head (`residual 2048 x 6`) | Diagonal/off-diagonal FB Bellman loss + orthogonality regularizer; optional implicit-$Q$ coefficient defaults to `0`. |
| **Low-Level Actor $\pi_\theta$** | `o = {state[67], last_action[29], scan[S], scan_valid[S], goal_dir[2]}` and `z[256]` $\to$ 29-D action distribution (`residual 2048 x 6`) | Maximizes conservative $\min_{k=1,2}(F_{\eta_k}(o, a, z)^\top z)$; zero action MSE, zero mimic reward, zero PPO clipping. |
| **Recurrent Planner $P_\psi$** | Full episode history of `(o_t, z_{t-1}, first_flag)` $\to$ macro latent $z_{\mathrm{plan}} \in \mathcal{S}^{255}(16)$ | Delayed TD3-style policy gradient minimizing $-Q_{\phi_1}(H_t, c_t^{\mathrm{geom}}, P_\psi(H_t))$ (`delay = 2`); no demonstration phase clock. |
| **Macro Task Twin Critic $Q_{\phi_1, \phi_2}$** | History $H_t$, privileged `critic_geometry` $c_t^{\mathrm{geom}}$, and **actual executed macro $z_{\mathrm{actual}}$** $\to$ scalars $Q_1, Q_2$ | $k$-step macro TD target ($k \in [1, K]$): $R_{\mathrm{macro}} + \gamma_{\mathrm{task}}^k (1 - \text{terminated})\min_{i=1,2} Q_{\bar{\phi}_i}(H_{t+k}, c_{t+k}^{\mathrm{geom}}, P_{\bar{\psi}}(H_{t+k}))$. |

### 2.1 Exact 229-Dim Single-Frame Motion Descriptor `m[229]`
In the heading-aligned root frame $H$ (where global $(x, y)$ translation and yaw $\psi$ are removed using the `torso_link` quaternion):
$$
m_t = \bigl[\underbrace{v_H[3],\, \omega_H[3],\, g_{\mathrm{root}}[3],\, q[29],\, \dot{q}[29]}_{\text{policy.state}[67]},\, \underbrace{\Delta p_{H,1..18}[18 \times 3],\, \mathrm{rot6d}_{H,1..18}[18 \times 6]}_{\text{18 named links}[162]}\bigr] \in \mathbb{R}^{229}.
$$
The 18 named links are ordered strictly as: `pelvis`, `torso_link`, `left/right_shoulder_roll_link`, `left/right_elbow_link`, `left/right_wrist_roll_link`, `left/right_wrist_pitch_link`, `left/right_wrist_yaw_link`, `left/right_hip_roll_link`, `left/right_knee_link`, `left/right_ankle_roll_link`.

---

## 3. Unfiltered Single-Frame Expert Provider and Three-Way Source Schedule (R2.1)

### 3.1 Elimination of Scene-Eligibility and 8-Height Static Admission
Earlier drafts attempted to filter or statically place the 859 demonstration frames against all 8 obstacle heights (`8 x 859` static collision/support sweep). R2.1 eliminates all scene-eligibility filtering based on a foundational principle:
> **$z$ is a policy conditioning vector, not a physical reset state or open-loop joint command. Whether a demonstration frame can be statically placed without collision against the current obstacle height does not determine whether $B(m_{\mathrm{demo}})$ is a useful latent directional prompt.**

1. `prepare_data.py` runs forward kinematics once on the 859-frame 50 Hz source NPZ to produce `[T, 229]` raw descriptors, finite-difference velocities (never substituting `velocity_command`), and a numerical quality mask.
2. `CandidateProvider.sample()` draws a valid frame uniformly from `[T, 229]` without querying obstacle height $h$, task stage, or current robot pose.
3. At each macro boundary, if source `expert` or `near` is selected, `selector` encodes the sampled `[1, 229]` frame once via `FBModel.encode_motion` (`eval/no_grad`). For `near`, it samples a tangent-space rotation with angle $\theta \in [10^\circ, 20^\circ]$ ($\cos\theta \in [\cos 20^\circ, \cos 10^\circ]$) and projects back to radius 16.
4. Rollout source probabilities $(p_{\mathrm{expert}}, p_{\mathrm{near}}, p_{\mathrm{planner}})$ follow a piece-wise linear schedule over committed control steps $S$ with $S_{\mathrm{ramp}} = 100,000$:
   $$
   (0.60, 0.30, 0.10) \xrightarrow{S = 0.5 S_{\mathrm{ramp}}} (0.30, 0.30, 0.40) \xrightarrow{S = S_{\mathrm{ramp}}} (0.10, 0.20, 0.70).
   $$
   All evaluation and curriculum-advancement panels use `100%` planner ($p_{\mathrm{planner}} = 1.0$).

---

## 4. Freezing UFO Update Semantics: Separation of `behavior_z` and `z_update`

R2.1 restores exact fidelity to the reference UFO update order (`sample_mixed_z` with `train_goal_ratio = 0.5`, `train_neighborhood_z = False`):
1. `Collector` records both `m_current` and `m_next` alongside immutable `behavior_z` in `FBReplay`.
2. In `FBAgent.update`, batch normalizers are updated **once** on real `(obs, m_current)` and **once** on real `(next_obs, m_next)`, eliminating the bug where `m_next` was fed into running statistics twice. Expert frames never update batch normalizers.
3. Under frozen normalizer statistics (`eval/no_grad`):
   $$
   z_{\mathrm{random}} = \operatorname{proj}(\mathcal{N}(0, I_{256})), \quad \mathrm{perm} = \operatorname{randperm}(n), \quad z_{\mathrm{goal}} = \operatorname{proj}\bigl(B_\omega(\tilde{m}_{\mathrm{next}}[\mathrm{perm}])\bigr),
   $$
   $$
   \mathrm{mask} = (\operatorname{rand}(n, 1) < 0.5), \qquad z_{\mathrm{update}} = \operatorname{where}(\mathrm{mask}, z_{\mathrm{goal}}, z_{\mathrm{random}}).
   $$
4. `z_update` is passed only to the current batch's FB loss and low-level actor loss. Task critic $Q_{\phi_1, \phi_2}$ always reads the macro's actual executed `z_actual`.

---

## 5. Task Reward, Event Chain, and R2.1 Terminal Boundary (`severe_penetration` vs `invalid`)

### 5.1 Ordered Traversal Event Chain and Potential-Based Reward
- **Success Criteria**: The robot must pass the front edge $x_{\mathrm{front}}$ within the legal lateral corridor, clear the rear edge $x_{\mathrm{rear}}$ with its entire whole-body and foot bounding footprint (`shapes_from_snapshot`), release all box contact, establish bipedal support on the rear ground with low foot slip and COM inside the support polygon, and maintain stable upright posture for **0.75 s** within the **12.0 s** episode timeout.
- **Allowed vs Failed Contacts**: Hand support on the obstacle box is explicitly permitted (`allow_hand_on_box = True`). Standing on top of the box, hanging by the hands, crawling on the ground, lateral bypass around the obstacle, or sustained ground non-foot contact with root clearance $< 0.45 L_{\mathrm{leg}}$ for $0.5\text{ s}$ triggers failure termination.
- **Step Reward**:
  $$
  r_t^{\mathrm{task}} = \alpha\bigl(\gamma_{\mathrm{task}}\Phi_{t+1} - \Phi_t\bigr) + \mathbf{1}_{\{\text{first\_success}, t\}} - c_{\mathrm{ctrl}}(a_t, \dot{q}_t), \qquad \alpha \le 0.2,
  $$
  with terminal absorption $\Phi_{t+1} = 0$ on failure termination and true end-state potential $\Phi_{t+1}$ on timeout truncation.

### 5.2 R2.1 Narrow Terminal-Boundary Revision: Credible `severe_penetration` vs Data `invalid`
Prior to R2.1, any runtime contact penetration exceeding $0.03\text{ m}$ raised an `InvalidPhysicsError` that aborted the training run or evaluation panel—turning ordinary exploratory falls and hard box impacts by an untrained random policy into fatal process exits. R2.1 establishes a strict two-category boundary:

| Classification | Exact Trigger Conditions | Required Runtime & Replay Handling |
|---|---|---|
| **Credible Task Failure (`severe_penetration`)** | Runtime contact depth exceeds $0.03\text{ m}$ on at least one substep, **AND** all 4 physics substeps complete with finite state/contact tensors, valid schema/indices/timing, no contact buffer overflow (`ncon < nconmax`), and no solver divergence. | Latches failure on first offending substep (`terminated = True`, `failure_reason = severe_penetration`), continues checking remaining substeps in the 4-substep control interval, sets absorption potential $\Phi_{\mathrm{next}} = 0$, commits the real pre-reset final transition to replay once, and resets the environment for the next episode. In evaluation panels, counts as a valid failed trial while preserving the seed and denominator. |
| **Data Corruption (`invalid`)** | Any `NaN`/`Inf` in state or contacts, contact buffer overflow with dropped contacts, corrupted schema/geometry/timing, missing pre-reset final state, or verified solver divergence (including if corruption occurs on a substep after an initial penetration). | `invalid` takes strict priority over `severe_penetration`. Rejects the entire uncommitted control transition (never enters replay or normalizers, never increments committed step count, never fabricates a zeroed terminal state), logs detailed diagnostic fields, and halts the affected run or evaluation panel. |

---

## 6. Multi-Height Curriculum Advancement and Evaluation Panels

### 6.1 Curriculum Controller (`PoolQuotaSchedule` + Active Unlock State)
- Advancement from current frontier height $h_{\mathrm{front}}$ to $h_{\mathrm{front}} + 0.10\text{ m}$ is evaluated every `eval_interval_control_steps = 100,000` using an independent `100%` planner evaluation panel (`100` independent ground starts on $h_{\mathrm{front}}$ and `100` on the lowest two heights `{0.10, 0.20}` m, frozen weights/BN, zero replay writes).
- **Unlock Gate**: Requires the 95% Wilson score lower bound on success rate to satisfy $\mathrm{LB}_{0.95} \ge 0.70$ across **two consecutive non-overlapping evaluation panels**, with no confirmed degradation $> 10$ percentage points on the lowest two heights.
- **Sampling Quota Allocation**: Once unlocked, each `quota_epoch_control_rows = 4096` allocates `50%` of control steps to the frontier height, `30%` uniformly across intermediate unlocked heights, and `20%` to the lowest two heights.

### 6.2 Held-Out Generalization Panels
1. **In-Distribution (ID) Panel**: Heights $\{0.10, 0.20, \dots, 0.70\}\text{ m}$ with standard depth $D = 0.356\text{ m}$ and unseen reset seeds.
2. **Interpolation Panel**: Unseen intermediate heights $\{0.15, 0.25, 0.35, 0.45, 0.55, 0.65\}\text{ m}$.
3. **Out-of-Distribution (OOD) Panel**: Unseen heights $\{0.05, 0.75, 0.80\}\text{ m}$ and perturbed obstacle depths $D \in \{0.25, 0.45\}\text{ m}$.
