# Brief B03: Motion-Only Backward Map Aliasing and Privileged/Perceptive Compensation in Contact-Rich Tasks

**Packet ID**: `B03`
**Status**: `READY_NOT_STARTED`
**Baseline References**: `baseline/02-fb-paradigm-beyond-imitation-and-exploration.md`, `baseline/04-joint-fb-ball-striking-v2-architecture.md`, `baseline/05-autonomous-obstacle-traversal-v3-and-r2-plan.md`

---

## 1. Problem Statement

In both 3D obstacle traversal (`m[229]`) and dynamic ball striking (`m[277]`), the backward representation network $B_\omega(m)$ is intentionally restricted to **single-frame robot-local body kinematics**, excluding obstacle height $h$, raycast terrain scan `scan[S]`, contact forces, and ball state `ball_state[9]`. This design allows a single unindexed motion capture clip to provide universal kinematic prompts across arbitrary obstacle heights (`0.10..0.70` m) or ball placements without scene-specific retargeting.

However, this creates **contact and geometric aliasing in $B$-space**:
- A posture with the hands or feet at height $z_{\mathrm{local}}$ above the root maps to the exact same $B(m)$ whether the robot is supported by a `0.40` m box, colliding with the front face of a `0.60` m box, or suspended in mid-air.
- Similarly, a kicking swing through empty air and an impact swing through a soccer ball at the same kinematic state map to the same $B(m)$.

**Core Question**: Under what mathematical and physical conditions is feeding perceptive/contact context exclusively into $F(o_F, a, z)$, $\pi_\theta(o_{\mathrm{low}}, z)$, $P_\psi(H)$, and $Q_\phi(H, \cdot)$ **necessary and sufficient** to resolve $B$-space contact aliasing, and when does motion-only $B(m)$ create an irreducible bottleneck in controllable contact behavior?

---

## 2. Hard Constraints & Non-Goals

- Must not break the ability to encode demonstration NPZ files that lack ground-truth contact forces, terrain scans, or ball trajectories (`prepare_data.py` only has access to kinematic `qpos`/`qvel` and FK).
- Must not re-introduce the rejected R1.3 8-height static collision admission pipeline or `infer_source_support_intent`.

---

## 3. Deliverables Required from Primary Authors

1. **Observability & Controllability Analysis**: Formalize the two-stage mapping $H_t \xrightarrow{P_\psi} z_t \xrightarrow{\pi_\theta(o_t, \cdot)} a_t$ and prove when a kinematic latent $z_t \in \mathcal{S}^{d_z-1}(\sqrt{d_z})$ combined with perceptive observation $o_t$ in $\pi_\theta(o_t, z_t)$ can represent distinct contact-force regimes (e.g., hand push-off on box vs swing-over) vs when $\pi_\theta(o_t, z_t)$ collapses them to a single action.
2. **Diagnostic Protocol for Aliasing Bottlenecks**: Define quantitative diagnostics measuring whether failures on intermediate/high obstacles (`0.30..0.70` m) or ball impacts stem from (a) planner $P_\psi$ selecting poor $z$, (b) $F(o, a, z)$ failing to use `scan[S]` / `ball_state[9]`, or (c) $B(m)$ lacking contact/load velocity-response features (analogous to causal acceleration $\widehat{\ddot{q}}$ in the single-actuator unit representation).
3. **Minimal Empirical Spike Protocol**: Design a controlled test on obstacle contact / hand-support transitions and ball-impact transitions that isolates $F/\pi$ perceptive conditioning from $B(m)$ input features.

---

## 4. Adjudication Rubric

| Dimension | Weight | Scoring Standard |
|---|---:|---|
| Compatibility with Kinematic-Only Demo NPZ | 30% | Preserves zero-force NPZ compatibility without static scene filtering. |
| Rigor of Aliasing Analysis | 25% | Distinguishes planner expressivity from low-level actor/forward observability. |
| Diagnostic Precision | 25% | Provides actionable metrics separating $B$-aliasing from $Q/P$ exploration failure. |
| Spike Falsifiability | 20% | Defines a minimal, reproducible test with clear pass/fail criteria. |
