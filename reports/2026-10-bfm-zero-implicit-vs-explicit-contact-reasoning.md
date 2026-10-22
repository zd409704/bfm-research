# Implicit vs. Explicit Contact Reasoning in BFM-Zero: Analysis and a Design for an Explicit Contact Belief Estimator

## Executive summary
- BFM-Zero (CMU LeCAR Lab and Meta; arXiv 2511.04131) shows strong evidence of implicit contact state estimation and contact-conditioned control, but not explicit contact reasoning.
- Its deployed actor sees only proprioception plus action history (4 frames); no contact or force signals. Contact-derived rewards and privileged critic information enter only during training, a form of implicit contact distillation.
- Proposed three-level taxonomy: contact-reactive control (confirmed), implicit contact estimation (strong evidence), explicit contact reasoning (absent).
- Proposed extension: a separate, explicit Contact Belief Estimator trained from simulator ground truth, plus linear probing of BFM hidden states, feeding a contact planner that sits above BFM rather than replacing it.

## 1. Evidence for implicit contact inference
**Actor inputs.** For the 29-DoF Unitree G1, o_t = {q_t − q̄, q̇_t, ω_root/4, g_t}, and the actor consumes o_{t,H} = {o_{t−H}, a_{t−H}, …, o_t}. The critic receives full privileged state. In the public code (`humanoidverse/config/obs/bfm_zero_obs.yaml`), `actor_obs` lists `base_ang_vel`, `projected_gravity`, `dof_pos`, `dof_vel`, `actions`, `history_actor` (4 frames of each) and `max_local_self`. No contact-force, foot-contact or force-sensor term appears.

**Mechanism.** Contact is not measured but is observable from the action → body-response transition: (a_{t−1}, q_{t−1}, q̇_{t−1}) → (q_t, q̇_t, ω_t, g_t). Sudden changes in ankle/knee velocity, impacts in base angular velocity, or joints deviating from free-motion trajectories reveal external constraints. A history encoder h_t = f(o_{t−H:t}, a_{t−H:t−1}) can thus form latent features resembling support, slip, impact, push and loss of support, without these ever being named. This mirrors biological proprioception: constraints are inferred from "command issued vs. body response".

**Contact-derived training rewards.** Active terms in code include `penalty_undesired_contact`, `penalty_slippage`, `penalty_feet_ori`, `penalty_ankle_roll`; `penalty_feet_contact_forces` and `penalty_stumble` exist but are commented out. The paper appendix lists Self Contact −1, Feet Orientation −0.4, Ankle Roll −4, Feet Slip −2. Contact information enters supervision via r_contact → Q_R → π(o_history) but is removed at inference: privileged contact information → implicit contact representation.

**Dynamics identification under domain randomization.** Training randomizes friction, mass, COM offset, joint offset, external pushes and sensor noise. Identical (q, q̇, a) can yield different s_{t+1}, so the network must implicitly estimate p(θ_dyn, c_t | history) with θ_dyn = {m, μ, COM, …}. The paper itself states that history narrows the information gap between the proprioceptive actor and privileged critic and improves adaptability under DR.

**Forward-Backward representation.** BFM-Zero learns M^{π_z}(ds′|s,a) ≈ F(s,a,z)ᵀB(s′)ρ(ds′). F encodes which future states will be visited; B embeds a state in the long-horizon dynamics space. Since contact changes P(s_{t+1}|s_t,a_t) (e.g., v_n ≈ 0 and ‖F_t‖ ≤ μF_n once a foot is planted), contact must be reflected in the FB latent dynamics for M^{π_z} to be predicted correctly.

**Behavioural evidence.**
- Slip: `penalty_slippage` requires distinguishing contact with tangential motion (c = 1, v_t ≠ 0); if it improves real-robot behaviour, the actor must recognize abnormal support from proprioception alone ("implicit tactile sensing").
- Fall recovery: the paper reports recovery from destabilization and falls, during which contact modes cycle (double support → single support → knee/hand/body contact → re-support), which is hard without some implicit ĉ_t.

**Action-conditioned sensing.** Because the history includes actions, the computation is action → observation change → latent state inference, structurally similar to a belief–action–observation–error loop (sensorimotor contingency), though not formulated as active inference.

## 2. Three levels of contact capability
| Level | BFM-Zero | Meaning |
|---|---|---|
| Contact-reactive control | Strong | Adjusts actions automatically after contact changes |
| Implicit contact estimation | Very likely present | Infers support, slip, collision, external force from proprioceptive history |
| Explicit contact reasoning | Absent | Explicit contact point, normal, force, mode, affordance |

Missing for level 3: per-limb contact labels c_i; normal/tangential forces F_n, F_t and friction μ; and future contact planning (where and with which limb to make the next contact, e.g., in climbing).

## 3. Proposed architecture
Perception → contact affordances A_t = {p_i, n_i, type_i, confidence_i} → contact planner producing intended contacts C*_{t:t+H} (e.g., LF→ground, RF→step, LH→wall) → mapped to a BFM latent z_t → whole-body action. BFM keeps balance, load transfer, transitions, coordination and perturbation recovery. This is argued to be more reasonable than an end-to-end vision-to-29-DoF model or feeding raw vision into BFM.

The source recommends not adding force sensing directly to the actor (π(o, F_foot)); instead keep π(o_history) and train a separate estimator E_c(o_history, a_history) → Ĉ_t, not necessarily fed back to the actor.

## 4. Explicit Contact Belief Estimator design
**Belief state (per limb i):** b_t = {c_i, p_i, n_i, f_i, s_i, μ_i, γ_i} — contact, contact point, surface normal, force, slip state, friction/grip estimate, confidence.

**Stage 1 (MVP): distillation from simulator ground truth.**
- Input: x_t = [q, q̇, ω_base, g, a]_{t−H:t}, plus Δq, Δq̇, Δω and tracking error e_q = q_cmd − q (a strong "external constraint" signal, analogous to efference copy).
- Output per limb: [P(contact), P(slip), F_n, F_tx, F_ty, Δp_contact, confidence]; MVP keeps P(contact), F_n, F_t, P(slip) — about 4 × 5 outputs.
- Network: temporal encoder (TCN preferred over GRU over Transformer) → h_t → contact / force / slip heads; history of 100–300 ms (H = 8–16 at 50 Hz); hundreds of thousands to a few million parameters, cheap on embedded edge compute.
- Labels from Isaac/MuJoCo: contact body ID, position, normal, normal and tangential force, relative velocity, friction.
- Loss: L = L_contact + λ₁L_force + λ₂L_slip (later add λ_p L_position).

**Breaking phase correlation.** Heavily randomize ground height, step height, sudden removal of support, early foot-wall collisions, hand-table contacts, friction, soft/hard ground, slope, pushes, joint delay, motor strength and payload. Key sample design: same pose + same command + different contact → different proprioceptive response, so the model learns interaction dynamics rather than gait phase.

**Unexpected contact.** Separate c_expected from c_unexpected (e.g., knee hits a step 80 ms into a planned 200 ms foot placement → P(contact_knee) = 0.95, P(unexpected) = 0.9), triggering reactive recovery.

**Stage 2: prediction-error features.** Train a small proprioceptive forward model ô_{t+1} = F(o_t, a_t); e_t = o_{t+1} − ô_{t+1}; estimator E(o_t, a_t, o_{t+1}, e_t) → C_t (e.g., predicted ankle velocity 1.2 vs. measured 0.1 plus a base angular-velocity impulse ⇒ contact).

**Stage 3: vision fusion.** Proprioception/force determines whether contact occurs; vision supplies where and what surface. Project the limb's FK position onto the nearest visible surface, p_c = argmin_{p∈surface} ‖p − p_RH‖, to obtain {contact, p_c, n_c, F_c}. A planner keeps current contacts (e.g., LF on ground A stable, RH free) and desired next contacts (RH → hold D).

## 5. Evaluation plan
- Four-limb observer: {c_LF, c_RF, c_LH, c_RH, slip_LF, slip_RF, F_LF, F_RF} from 0.2 s of history.
- Scenarios: normal walking/running; randomized height/friction/slope; deliberate wall collisions, missed steps, pushes.
- Metrics: accuracy vs. ground truth, and detection latency Δt = t_estimate − t_physical; < 20–40 ms is considered practical.
- Representation probing: freeze BFM, train a small linear probe W h_t → c_t for foot/hand contact, slip, contact force and friction bin. High probe accuracy would demonstrate an internal contact representation; neuron-level correlation analysis (simulation contact as "electrophysiology labels") could locate dimensions encoding support phase, slip or perturbation.

## 6. Conclusions
- BFM-Zero learns a proprioceptive, action-conditioned, history-dependent whole-body dynamics belief in which contact is a necessary latent variable: implicit contact inference holds; explicit contact reasoning does not.
- It knows roughly how the body is currently constrained, but not that a surface is a graspable handrail where a limb should deliberately make contact.
- The natural extension is a three-layer system: perception (where contact is possible) → contact planner (where, when, which limb) → BFM (how the whole body moves under those constraints).
- If BFM hidden states linearly decode contact, the most economical design is contact heads on the BFM internal state itself rather than a separate estimator.

## Open questions
- Do linear probes on BFM hidden features recover contact, slip, force and friction, and with what latency?
- Does `penalty_slippage` measurably improve real-robot slip handling?
- How should desired contacts be encoded into the FB latent z?

## Verification notes
- Reward weights in the public `reward_bfm_zero.yaml` differ from the paper appendix values quoted in the source (code: undesired contact −1, feet orientation −0.1, ankle roll −0.5, slippage −1.0; appendix as quoted: −1, −0.4, −4, −2).
- The public `actor_obs` also includes `max_local_self`, which the source did not mention; whether it is available on the real robot was not checked.
- Interpretive claims (latent features, probing outcomes, latency targets) are the source's hypotheses, not reported results.

## References
- BFM-Zero paper: https://arxiv.org/abs/2511.04131
- BFM-Zero code: https://github.com/LeCAR-Lab/BFM-Zero
