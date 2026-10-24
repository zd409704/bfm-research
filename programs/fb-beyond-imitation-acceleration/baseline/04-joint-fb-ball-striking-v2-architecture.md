# Baseline 04: Joint FB + Task-Q + Planner Architecture for 29-DoF Humanoid Dynamic Ball Striking (v2 Specification)

## 1. Scope and Design Philosophy

This baseline specifies the **v2 Joint Training Architecture** for 29-DoF humanoid dynamic ball striking from random initialization. The system uses unindexed single-frame human/robot kicking motion capture data strictly to construct latent exploration anchors $z_{\mathrm{exp}} = \operatorname{proj}(B_\omega(m_{\mathrm{demo}}))$ and local tangent perturbations $z_{\mathrm{near}}$, while jointly training six modules from scratch:
- Backward motion encoder $B_\omega(m)$
- Forward successor ensemble $F_{\eta_1, \eta_2}(o_F, a, z)$
- Low-level conditioned actor $\pi_\theta(o_{\mathrm{low}}, z)$
- Recurrent high-level latent planner $P_\psi(H_{\mathrm{plan}})$
- Twin action-conditioned task critics $Q_{\phi_1, \phi_2}(H_Q, a)$

No pre-trained checkpoints, Stage-1 freeze phases, behavioral cloning losses, or per-frame tracking rewards are used.

---

## 2. Information Partitioning and Exact Tensor Schemas

### 2.1 Explicit `kick_leg` Task Conditioning
Because demonstration clips contain both left-foot and right-foot kicks while the pure task reward must specify which foot is required to strike the ball before contact occurs, each episode samples a fixed binary one-hot command:
$$
\text{kick\_leg} \in \{[1, 0], [0, 1]\} \in \mathbb{R}^2 \quad (\text{left foot vs right foot}),
$$
which remains constant throughout the episode and is provided to the task reward, low-level actor, planner, and task critic (as well as $o_F$), but **never** to the backward motion encoder $B_\omega$.

### 2.2 Module-by-Module Input Partition Table

| Input / State Tensor | Dim | Exact Coordinate and Physical Definition | Allowed Consumers | Explicitly Excluded From |
|---|---:|---|---|---|
| **Single-Frame Motion $m_t$** | `277` | `joint_pos_rel[29]` + `joint_vel_rel[29]` + `body_pos_local_yaw[14x3=42]` + `body_quat_local_yaw[14x4=56]` + `body_lin_vel_local_yaw[14x3=42]` + `body_ang_vel_local_yaw[14x3=42]` + `root_lin_vel_b[3]` + `root_ang_vel_b[3]` + `projected_gravity_b[3]` + `base_height[1]` + `feet_pos_b[2x3=6]` + `feet_lin_vel_b[2x3=6]` + `torso_pos_b[3]` + `torso_quat_b[4]` + `torso_lin_vel_b[3]` + `torso_ang_vel_b[3]` + `pelvis_ang_vel_b[3]` | $B_\omega(m)$ only | Task reward, ball state, `kick_leg`, `last_action` |
| **Low-Level Policy Obs $o_t^{\mathrm{low}}$** | `93` | `base_lin_vel[3]` + `base_ang_vel[3]` + `projected_gravity[3]` + `joint_pos[29]` + `joint_vel[29]` + `actions[29]` (previous step $a_{t-1}$) + `ball_state[9]` (`ball_pos_b[3]`, `ball_vel_b[3]`, `target_pos_b[3]`) + `kick_leg[2]` | $\pi_\theta(o_{\mathrm{low}}, z)$ | Demonstration frame index, privileged contact forces |
| **Planner Obs $o_t^{\mathrm{plan}}$** | `93` | Identical to $o_t^{\mathrm{low}}$; fed sequentially into recurrent state $H_t^{\mathrm{plan}}$ | $P_\psi(H_t^{\mathrm{plan}})$ | Privileged critic state, reference motion frames |
| **Forward Network Obs $o_t^F$** | `297` | `m_t[277]` + `ball_state[9]` + `kick_leg[2]` + `feet_contact_binary[2]` + `ball_contact_force_b[3]` + `root_height_error[1]` + `ball_to_target_dist[1]` + `kick_foot_to_ball_dist[1]` + `support_foot_slip_norm[1]` | $F_{\eta_1, \eta_2}(o_t^F, a_t, z)$ | Future demonstration frames |
| **Task Critic Obs $o_t^Q$** | `135` | $o_t^{\mathrm{low}}[93]$ + privileged body/contact features (`feet_pos_b[6]`, `feet_vel_b[6]`, `contact_forces_feet[6]`, `ball_ang_vel_b[3]`, `kick_window_timer[1]`, `has_kicked[1]`, `min_foot_ball_dist_in_ep[1]`, `ball_speed_toward_goal[1]`, `torso_upright_cos[1]`, `joint_torques_scaled[16]`) | $Q_{\phi_1, \phi_2}(H_t^Q, a_t)$ | Demonstration reference poses |

---

## 3. Exact Task Reward and Termination Specification

### 3.1 Pure Task Reward (4 Terms, Zero Imitation Tracking Terms)
Let $p_{\mathrm{foot}} \in \mathbb{R}^3$ be the world position of the designated `kick_leg` ankle/foot link, $p_{\mathrm{ball}} \in \mathbb{R}^3$ and $v_{\mathrm{ball}} \in \mathbb{R}^3$ be the ball position and linear velocity, and $p_{\mathrm{goal}} \in \mathbb{R}^3$ be the target goal position. Define unit direction vectors:
$$
\hat{d}_{\mathrm{fb}} = \frac{p_{\mathrm{ball}} - p_{\mathrm{foot}}}{\|p_{\mathrm{ball}} - p_{\mathrm{foot}}\|_2 + 10^{-6}}, \qquad \hat{d}_{\mathrm{bg}} = \frac{p_{\mathrm{goal}} - p_{\mathrm{ball}}}{\|p_{\mathrm{goal}} - p_{\mathrm{ball}}\|_2 + 10^{-6}}.
$$
A valid foot-ball contact impulse occurs on step $t$ when $\|p_{\mathrm{ball},t} - p_{\mathrm{foot},t}\|_2 < r_{\mathrm{contact}}$ and $\|v_{\mathrm{ball},t} - v_{\mathrm{ball},t-1}\|_2 > \Delta v_{\mathrm{min}}$, setting `has_kicked = True` and starting a 5-step post-impact evaluation window (`window_steps = 5`, $\tau_{\mathrm{win}} \in \{1, 2, 3, 4, 5\}$).

The step task reward $r_t^{\mathrm{task}}$ is the weighted sum of four terms:
1. **`ApproachBallReward` (weight $= 50.0$, active only while `not has_kicked`)**:
   $$
   r_{\mathrm{app},t} = \max\!\bigl(0,\, \langle v_{\mathrm{foot},t},\, \hat{d}_{\mathrm{fb},t} \rangle\bigr) \cdot \exp\!\bigl(-2.0\,\|p_{\mathrm{ball},t} - p_{\mathrm{foot},t}\|_2\bigr).
   $$
2. **`KickBallVelReward` (weight $= 50.0$, active during the 5-step post-kick window $\tau_{\mathrm{win}} \in [1, 5]$)**:
   $$
   r_{\mathrm{vel},t} = \max\!\bigl(0,\, \langle v_{\mathrm{ball},t},\, \hat{d}_{\mathrm{bg},t} \rangle\bigr).
   $$
3. **`BallTargetDistanceReward` (weight $= 30.0$, active after `has_kicked`)**:
   $$
   r_{\mathrm{dist},t} = \exp\!\bigl(-0.5\,\|p_{\mathrm{goal},t} - p_{\mathrm{ball},t}\|_2\bigr) - \exp\!\bigl(-0.5\,\|p_{\mathrm{goal},t-1} - p_{\mathrm{ball},t-1}\|_2\bigr).
   $$
4. **`PostKickRecoveryReward` (weight $= 10.0$, active for $t > t_{\mathrm{kick}} + 5$)**:
   $$
   r_{\mathrm{rec},t} = \exp\!\bigl(-4.0\,\|g_{\mathrm{proj},t} - g_{\mathrm{upright}}\|_2^2 - 0.5\,\|v_{\mathrm{root},t}\|_2^2\bigr).
   $$

### 3.2 Resolution of the Cross-Segment Window Leak (Audit Fix #1)
In v1, `has_kicked` and the 5-step post-kick timer were stored in un-reset environment attributes or leaked across episode resets when an episode terminated inside the 5-step window. In v2:
- `has_kicked[env_id]` and `kick_window_remaining[env_id]` are explicitly zeroed inside `reset_idx(env_ids)` before computing initial observations.
- All replay transitions record `pre_reset` terminal flags (`terminated_t`, `truncated_t`) prior to auto-reset.

---

## 4. Network Architectures and Mathematical Loss Functions

### 4.1 Backward Map $B_\omega$ and Forward Ensemble $F_{\eta_1, \eta_2}$
- **Backward Map $B_\omega(m)$**: Input $m \in \mathbb{R}^{277}$ (running mean/std normalized) $\to$ MLP `[512, 512, 256]` with LayerNorm + SiLU $\to$ L2 spherical projection onto radius $\sqrt{d_z}$ ($d_z = 100$, radius $10.0$):
  $$
  B_\omega(m) = \sqrt{d_z}\,\frac{\tilde{B}_\omega(m)}{\|\tilde{B}_\omega(m)\|_2 + 10^{-8}}.
  $$
- **Forward Ensemble $F_{\eta_k}(o_F, a, z)$ ($k \in \{1, 2\}$)**: State-action branch $(o_F, a) \in \mathbb{R}^{297+29} \to [1024, 512]$ concatenated with state-latent branch $(o_F, z) \in \mathbb{R}^{297+100} \to [1024, 512]$ $\to$ trunk `[1024, 1024, 100]` outputting $F_{\eta_k}(o_F, a, z) \in \mathbb{R}^{100}$.
- **Exact Ensemble Scalar Inner-Product Before Aggregation (Audit Fix #3)**:
  For a batch of $N$ transitions $(o_{F,i}, a_i, o_{F,i}', m_{i}')$ and relabeled latents $z_i$, define the $N \times N$ successor logit matrix for each head $k \in \{1, 2\}$ **before** taking any ensemble minimum or pessimistic combination:
  $$
  M_{ij}^{(k)} = F_{\eta_k}(o_{F,i}, a_i, z_i)^\top B_\omega(m_j'), \qquad \bar{M}_{ij}^{(k)} = F_{\bar{\eta}_k}(o_{F,i}', a_i', z_i)^\top B_{\bar{\omega}}(m_j'),
  $$
  where $a_i' = \pi_\theta(o_{\mathrm{low},i}', z_i)$. The target scalar matrix is aggregated over scalar inner products (never coordinate-wise $\min(F_1, F_2)$ before the dot product, because coordinates of $B$ can be negative):
  $$
  \bar{M}_{ij} = \frac{1}{2}\bigl(\bar{M}_{ij}^{(1)} + \bar{M}_{ij}^{(2)}\bigr), \qquad \delta_{ij}^{(k)} = M_{ij}^{(k)} - \gamma_{\mathrm{FB}}(1 - d_i)\operatorname{stopgrad}(\bar{M}_{ij}).
  $$
  The total FB loss is:
  $$
  \mathcal{L}_{\mathrm{FB}}(\eta_1, \eta_2, \omega) = \sum_{k=1}^2 \left[\frac{1}{2N(N-1)}\sum_{i \neq j} \bigl(\delta_{ij}^{(k)}\bigr)^2 - \frac{1}{N}\sum_{i=1}^N M_{ii}^{(k)}\right] + \lambda_{\mathrm{orth}} \mathcal{L}_{\mathrm{orth}}(B_\omega).
  $$

### 4.2 High-Level Recurrent Planner $P_\psi$ and Action-Conditioned Twin Critic $Q_{\phi_1, \phi_2}$
- **Single-Step Planner Hold ($K_{\mathrm{hold}} = 1$, Audit Fix #4)**:
  Because the ball-striking task critic $Q_{\phi_1, \phi_2}(H_t^Q, a_t)$ is conditioned on the **physical 29-DoF action $a_t$** rather than a multi-step macro $z$, setting $K_{\mathrm{hold}} > 1$ caused credit-assignment misalignment between step-level $Q(H_t^Q, a_t)$ and held $z$. In v2, $K_{\mathrm{hold}} = 1$: the recurrent planner updates $H_t^{\mathrm{plan}}$ and outputs $z_t^{\mathrm{plan}} \in \mathcal{S}^{d_z-1}(\sqrt{d_z})$ at every control step ($50\text{ Hz}$).
  - Architecture of $P_\psi$: `2-layer LSTM (hidden_size=128)` over $o_t^{\mathrm{plan}}[93]$ $\to$ MLP `[128, 64, 32]` with ELU $\to$ linear readout to $\mathbb{R}^{100}$ $\to$ spherical projection $\sqrt{100}\,\hat{z}$.
  - Architecture of $Q_{\phi_1, \phi_2}$: `2-layer LSTM (hidden_size=128)` over $o_t^Q[135]$, concatenated with $a_t[29]$ $\to$ MLP `[256, 256, 1]`.

- **Task Critic Bellman Target with Task-Only Actor EMA $\bar{\theta}$**:
  To prevent rapid FB representation updates on $\pi_\theta$ from destabilizing the one-step target action in $Q_{\phi}$, v2 maintains a dedicated target actor $\pi_{\bar{\theta}}$ alongside target planner $P_{\bar{\psi}}$ and target critics $Q_{\bar{\phi}_1, \bar{\phi}_2}$:
  $$
  z_{t+1}^{\mathrm{targ}} = P_{\bar{\psi}}(H_{t+1}^{\mathrm{plan}}), \qquad a_{t+1}^{\mathrm{targ}} = \operatorname{clip}\bigl(\pi_{\bar{\theta}}(o_{t+1}^{\mathrm{low}}, z_{t+1}^{\mathrm{targ}}) + \operatorname{clip}(\epsilon, -c, c), -1, 1\bigr),
  $$
  $$
  y_t^Q = r_t^{\mathrm{task}} + \gamma_{\mathrm{task}}(1 - \text{terminated}_t)\min_{k=1,2} Q_{\bar{\phi}_k}\bigl(H_{t+1}^Q, a_{t+1}^{\mathrm{targ}}\bigr).
  $$

- **Low-Level Actor $\pi_\theta$ and Planner $P_\psi$ Objectives**:
  - Low-level actor $\pi_\theta(o_{\mathrm{low}}, z_{\mathrm{update}})$ maximizes the conservative FB scalar inner product:
    $$
    \mathcal{L}_\pi(\theta) = -\mathbb{E}_{o_F, o_{\mathrm{low}}, z_{\mathrm{update}}}\left[\min_{k=1,2} \Bigl(F_{\eta_k}\bigl(o_F, \pi_\theta(o_{\mathrm{low}}, z_{\mathrm{update}}), z_{\mathrm{update}}\bigr)^\top z_{\mathrm{update}}\Bigr)\right].
    $$
  - High-level planner $P_\psi$ maximizes $Q_{\phi_1}$ through the frozen low-level actor $\pi_\theta$:
    $$
    \mathcal{L}_{\mathrm{plan}}(\psi) = -\mathbb{E}_{H^{\mathrm{plan}}, H^Q, o_{\mathrm{low}}}\Bigl[Q_{\phi_1}\bigl(H^Q, \pi_\theta(o_{\mathrm{low}}, P_\psi(H^{\mathrm{plan}}))\bigr)\Bigr].
    $$

### 4.3 Full-Prefix Zero-Hidden RNN Burn-In (Audit Fix #5)
Storing stale LSTM hidden states in the replay buffer introduces severe off-policy representation drift as $P_\psi$ and $Q_{\phi_1, \phi_2}$ evolve. In v2:
- `TaskEpisodeReplay` stores complete variable-length episode trajectories from $t=0$ with zero initial hidden states $(h_0=0, c_0=0)$.
- For sampled slice $[t_0, t_0 + L_{\mathrm{train}})$, the prefix $[0, t_0)$ is unrolled from $(h_0=0, c_0=0)$ under `torch.no_grad()` using the **current** online/target network weights to produce exact hidden states at $t_0$, and backpropagation through time (BPTT) runs over $[t_0, t_0 + L_{\mathrm{train}})$.
