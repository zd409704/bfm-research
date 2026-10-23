# Proposal P

**Packet:** P1 · **Track:** Opus (competing author) · **Date:** 2026-10-23
**One line:** The first lock is not a competence score. It is a **contract** that sets (i) which impedance the fast loop can physically render and (ii) the most contact information any higher layer can ever get. Both are Grade-1 bounded. S1 is the first *consumer* of that contract, not the first lock.

---

## Thesis (first lock)

**Lock a split/merge stage "S0+S2a" (Body-Loop Contract, BLC):**

- **S0 (as a contract, not as a new algorithm):** a fast joint-level impedance loop (inner rate class R0 ≥ 1 kHz; reflex/body rate class R1 ≥ 200 Hz). It accepts impedance setpoints from above and **enforces a declared passivity envelope** `K_j ≤ K_max(T, b_j)` per joint.
- **S2a (contact *observability floor*):** the same loop **exports the realized torque** (current-derived, not commanded), plus `q, q̇`, IMU, and a generalized-momentum contact residual `r(t)` with its noise covariance, a change-detection statistic, and an **identifiability flag**. These are timestamped at ≥ R1.
- **Deferred, not locked:** S2b (contact localization/classification/semantics, multi-contact wrench distribution), all of S1 policy internals, and everything from S3 to S7.

**Why not S1 first:** S1 (proprioceptive locomotion) already has strong *sufficiency* evidence (existing learned policies walk). Its main necessity content is a balance-under-delay bound, and that bound is **not binding** at policy rates (C6 below). Locking S1 first would lock a phenomenology result and leave contact information as an unexamined side effect of whatever observation set S1 happens to use. That is the failure the prior reviews found ("contact is a latent already estimated").

**Why not S2 whole:** Localization, classification and wrench distribution run into identifiability limits (C3) that depend on the robot's morphology and sensor suite. Those are Candidate claims that need platform-specific premises. Only the *floor* (what gets exported, and at what rate) is premise-light enough to lock now.

**Why merge S0 with S2a:** Contact observability from proprioception depends on S0. The residual needs the **realized** torque at the rate the impedance loop runs. Commanded setpoints at policy rate do not carry it, because unmodeled friction, saturation and sub-sample transients are not in them. If S0 is specified without this export, S2 to S5 inherit an information ceiling that cannot be recovered later (C2). The two must be specified together.

---

## Necessity argument (Appendix B)

The argument has three steps. Each rests on a Grade-1 statement with explicit premises. Engineering convenience is used only to *choose among* admissible options, never to establish them.

1. **The impedance-rendering role must sit in a fast tier (C1, Grade 1).** Premises: sampled-data zero-order-hold (ZOH) virtual spring–damper `(K, B)` at period `T`, physical joint damping `b`, coupled to an arbitrary passive environment. Colgate & Schenkel's passivity condition is `b > K·T/2 + |B|`, so `K_max = 2(b − |B|)/T`. Holding `b` fixed, going from `T = 1 ms` to `T = 20 ms` (a 50 Hz policy) cuts the passively renderable stiffness by **20×**. Any architecture whose stiffness is rendered only by a ~50 Hz policy is therefore either soft or non-passive in contact. This is a bound, not a benchmark. Whether it *binds* on the target plant depends on measured `b_j` and the stiffness the tasks need (premise check C1′, Candidate).
2. **What higher layers can know about contact is capped by what the body loop exports (C2, Grade 1).** This is the data-processing inequality. If `Y_up = f(Y_export)`, then `I(contact; Y_up) ≤ I(contact; Y_export)`. No later stage (S3 prediction, S4 probing, S5 relation, BFM latents) can recover contact information the contract dropped. So the export contract is a **gate** for S2–S5, and it has to be fixed before they stack.
3. **Even the export has hard blind spots, so the contract must report them, not hide them (C3, Grade 1).** For a contact wrench `F` at contact Jacobian `J_c`, proprioception sees only `J_cᵀF` (plus noise). Components in `null(J_cᵀ)` cannot be observed from joint/base proprioception. Multi-contact distribution can be identified only if the stacked `[J_1ᵀ … J_kᵀ]` has full column rank. This formalizes the reviews' rejection of "contact already estimated": in general it **cannot** be fully estimated from proprioception alone. The contract must carry an identifiability flag.
4. **Detection latency has a floor set by noise and rate (C4, Grade 1 under a noise model; Candidate until noise is measured).** For a mean shift with per-sample KL divergence `D` and false-alarm run length `γ`, the expected detection delay is asymptotically `≳ log γ / D` samples (Lorden/Lai). This ties the rate class R1 and the sensor noise to the earliest reflex response, as a bound and not a tuning outcome.
5. **The balance bound does not force S1 first (C6, Grade 1, used negatively).** For a plant with unstable pole `p` and delay `τ`, `‖T‖∞ ≥ e^{pτ}` (Skogestad & Postlethwaite, ch. 5). A linear-inverted-pendulum humanoid has `p = √(g/z_c) ≈ 3.3 rad/s` (z_c ≈ 0.9 m). With `τ ≈ 30 ms` (50 Hz policy plus compute), `e^{pτ} ≈ 1.10`, which is not binding. The binding fast-time-scale constraint is at **contact/impedance** (step 1), not balance. So the necessity ordering puts S0/S2a under S1, not the other way around.

**Grade-2 role (Candidate):** multi-timescale separation, with a fast corrective loop below policy rate (C5). Steps 1 and 4 support it. It stays Candidate because the *numeric* rates depend on C1′ and C4 premises.

**Grade-3 (motivation only, no veto power):** spinal stretch/cutaneous reflex arcs, and the "animals walk before they manipulate" ordering. They are used for naming only. No claim in this proposal depends on them.

---

## Interface contracts

Rate classes: **R0** ≥ 1 kHz (actuator/impedance inner loop) · **R1** ≥ 200 Hz (body loop/reflex) · **R2** ~50 Hz (policy) · **R3** ≤ 5 Hz/event (Scene Graph, Life Core).

| ID | Direction | Signal (schema) | Rate | Owner | Notes / invariants |
|---|---|---|---|---|---|
| **I0** `ImpedanceSetpoint` | down: S1 policy (or any R2 client) → S0 | per joint `{q*, q̇*, τ_ff, K, D, t_valid}` | R2 in; held/interpolated at R0 | Body loop | S0 **clamps** `K, D` to the envelope `K ≤ K_max(T_R0, b_j)` and reports clamping in I3. Stale setpoint (`now > t_valid`) → S0 falls back to the declared safe-hold impedance. |
| **I1** `BodyState` | up | `{t, q, q̇, τ_realized, imu(ω, a), base_est?}` (one clock, monotonic timestamps) | ≥ R1 (raw R0 buffer readable on request) | Body loop | `τ_realized` = current-derived torque, **not** the command. A missing field is a contract violation, not "best effort". |
| **I2** `ContactResidual` | up | `{t, r ∈ ℝ^{n(+6)}, Σ_r, g_cusum, event?: {t_onset_est, t_detect, dir = r/‖r‖, ident_flag ∈ {full, partial, none}, null_dim, conf}}` | stream ≥ R1; events pushed async | Body loop | `ident_flag` comes from the rank of the candidate `J_cᵀ` set (C3). `none`/`partial` must be reported, never filled in silently. Σ_r is calibrated in free motion. |
| **I3** `ReflexStatus` | up | `{t, envelope_clamped[j], reflex_fired: {id, t, params}, safe_hold: bool}` | ≥ R1 on change | Body loop | Reflexes (e.g. stiffness drop or retract on residual spike) run inside S0 and are only *parameterized* from above. |
| **I4** `ContactEpisode` | up: body loop → Scene Graph | `{t_start, t_end, link_candidates[], wrench_est ± cov or "unidentifiable", peak ‖r‖, reflex_ids[]}` | R3 / event | **Produced** by the body loop, **owned/persisted** by Scene Graph | The body loop does **not** assert object identity or relation. Association to objects is Scene Graph's job (S5+). |
| **I5** `ReflexProfile` | down: Life Core/Scene Graph → S0 | named preset `{gain schedule id, reflex thresholds}` | R3 | Body loop executes; Life Core may *select* | Bounded authority: presets cannot exceed the envelope. Life Core never writes I0 directly. |

**Ownership rules (locked with the contract):**
1. Only the body loop writes torque. Only the body loop can relax the envelope, and only through a challenge packet against C1.
2. Life Core reads nothing faster than R3 and gets body information only through Scene Graph (I4) or I3 summaries.
3. Every upper-layer module declares which of I1 to I4 it consumes. Any contact-dependent claim upstream must cite the I2 fields it relies on (this enforces C2).

---

## Claims table

| ID | Grade | State (proposed) | Scope / premises | Statement | Falsifier / downgrade mode |
|---|---|---|---|---|---|
| **C1** | 1 | **Locked (narrow)** | 1-DoF, linear ZOH virtual spring–damper, period T, physical damping b, passive environment | Passive iff `b > KT/2 + |B|` (Colgate–Schenkel). | A demonstrated violation inside these premises means a sim or derivation error. Outside the premises (nonlinear friction, multi-DoF coupling, delay) the claim does **not** apply. Spike SA-1 reproduces the boundary as a sanity check, not as promotion evidence. |
| **C1′** | 1 (conditional) | Candidate | target-plant joints: measured `b_j`, required task stiffness `K_req` | At R2 (50 Hz), `K_max < K_req` for contact-critical joints, so impedance must be rendered at R0/R1. | Measured `b_j` and `K_req` give `2b_j/T_R2 ≥ K_req` → the claim is retired for those joints (a policy-rate impedance becomes admissible). |
| **C2** | 1 | **Locked** | Any processing chain above the export | `I(contact; upper) ≤ I(contact; I1∪I2)`. | None within information theory. It is challenged only if an upper layer gets an *independent* contact channel (vision, tactile). That is not a counterexample; it adds premises. |
| **C3** | 1 | **Locked (linear-algebra statement)**; detectability *margins* Candidate | Rigid-body model, known kinematics, proprioception only (joint + base) | Only `J_cᵀF` is observable. `null(J_cᵀ)` components are invisible. Multi-contact distribution is identifiable only if the stacked Jacobian has full column rank. | SA-2 PF-3: "null-space" contacts detected above the false-alarm floor → model/sim error or an unmodeled sensing channel (record in violations.md). |
| **C4** | 1 under noise model | Candidate | i.i.d. (or whitened) residual noise, mean-shift contact onset, CUSUM-type detector | `E[delay] ≳ log γ / D` samples, so the latency floor is `(log γ / D)·T_s`. | SA-2 PF-4: a detector beats the bound by >10% → the noise model is wrong, so revise the premises. target-plant noise spectra pending. |
| **C5** | 2 | Candidate | Contact-rich humanoid, policy at R2 | A corrective loop faster than the policy (R0/R1) is an obligatory functional role. | A policy-only (R2) system shown to be passive and stable in contact at the required stiffness on home-humanoid-class actuators → downgrade (this is the same evidence that retires C1′). |
| **C6** | 1 | **Locked (narrow)**, used negatively | LTI unstable pole p, delay τ | `‖T‖∞ ≥ e^{pτ}`. With LIP `p ≈ 3.3 rad/s` and τ ≈ 30 ms the bound is ≈1.10, so it does not bind at 50 Hz. | It would bind only if the effective τ reached ≳ 200 ms (`e^{0.66} ≈ 1.9`). The claim's *use* (S1 not forced first) is rechecked if target-plant latency is an order of magnitude worse. |
| **C7** | 1 (formal) → contract | Candidate (contract-necessity) | Actuators with unmodeled friction/saturation | Exporting `τ_realized` at ≥ R1 is necessary for contact detection at the PF-1 sensitivity. Commanded setpoints at R2 are not enough. | **SA-2 PF-2** (decisive): if the policy-view export matches the R1 export (ΔTPR ≤ 0.05 and Δp95 latency ≤ 10 ms across all classes ≥ 10 ms), downgrade C7. The S0/S2a merge then loses its necessity basis and S1-first becomes admissible. |
| **G3-a** | 3 | Inspiration only | Vertebrate spinal reflexes | Fast segmental reflexes precede and underlie voluntary movement. | — (never used as a veto) |
| **G3-b** | 3 | Inspiration only | Phylogeny | "Locomotion before manipulation". Explicitly **not** used to order S1 vs S2. | — |

The adjudicator may downgrade any "Locked (narrow)" above to Candidate. The proposal does not depend on C1/C3/C6 being Locked rather than Candidate. It depends on **C2** (trivially Locked) and on **C7 surviving PF-2**.

---

## Minimal spike (sim-only, numpy-only; ≤ 15 min CPU; deferred-runnable)

The environment check on 2026-10-23 found `numpy 2.5.4` available and **no** `mujoco`/`scipy`. The spike is therefore specified as pure numpy with batch-vectorized trials. All outputs go to `spikes/A/` as JSON plus a one-line PASS/FAIL.

### SA-1 Passivity boundary reproduction (sanity for C1, informs C1′)

```
cd /srv/claude/research/life-sensorimotor-2026-10-23
python3 -I spikes/A/passivity_sweep.py --out spikes/A/passivity.json --seed 0
```

- Port test, independent of mass: impose velocity `v(t) = A sin(ωt)` on the port. The controller is a ZOH virtual spring `K` (B = 0) at period `T`, in parallel with physical damper `b`. The continuous plant is integrated at `dt = T/200`. Compute the absorbed energy `E(ω) = ∫ (b v + F_K) v dt` over ≥ 50 periods, on an ω grid of 200 log-spaced points in (0.01, π/T) rad/s.
- Grid: `T ∈ {0.5, 1, 2, 5, 10, 20} ms`, `b ∈ {0.1, 0.5, 2.0} N·m·s/rad`, K on a 60-point log grid.
- Metric: empirical `K_crit(T, b)` = smallest K with `min_ω E(ω) < 0`.
- **PASS:** `K_crit / (2b/T) ∈ [0.8, 1.25]` for all 18 (T, b) cells. **FAIL:** any cell outside → the harness is wrong. Fix the harness; do not touch C1.
- Also print `K_max` at T = 1 ms vs 20 ms for each b, as the C1′ input table. The comparison to target-plant `K_req` is deferred to hardware data.

### SA-2 Contact observability vs export contract (decisive for C7; checks C3, C4)

```
python3 -I spikes/A/contact_obs_spike.py --trials 200 --seed 0 --out spikes/A/contact_obs_s0.json
python3 -I spikes/A/contact_obs_spike.py --trials 200 --seed 1 --out spikes/A/contact_obs_s1.json
python3 -I spikes/A/contact_obs_spike.py --trials 200 --seed 2 --out spikes/A/contact_obs_s2.json
python3 -I spikes/A/aggregate.py spikes/A/contact_obs_s*.json --out spikes/A/summary.json
```

**Plant:** planar 2-link arm, fixed base, vertical plane with gravity, `l = 0.4 m`, `m = 2 kg` per link, uniform rods. Dynamics are closed-form `M(q), C(q,q̇), g(q)`, integrated with RK4 at `dt = 0.1 ms`. Joint PD tracks a 0.5 Hz sinusoidal reference at R0 = 1 kHz with `Kp = 60, Kd = 2`. **Unmodeled actuator effects:** Coulomb friction 0.3 N·m, viscous 0.05, torque saturation ±25 N·m. The realized torque includes all of them. The commanded torque does not.

**Sensors:** `σ_q = 1e-4 rad`; `q̇` from filtered finite differences; `σ_τ ∈ {0.05, 0.2, 0.5} N·m` (sweep; the 0.2 main row is pre-registered).

**Contact classes** (200 trials each, per seed): half-sine force pulse. Duration `d ∈ {5, 10, 20, 50, 200} ms` × magnitude `{2, 5, 10, 20} N`. Point uniform on link 1 or link 2, direction uniform. Plus the **null class:** force along the link-1 axis applied on link 1 (`J_cᵀF = 0` exactly). Plus 600 s of contact-free motion per seed for threshold calibration.

**Export contracts compared** (same detector: generalized-momentum observer, gain 50 s⁻¹, then a two-sided CUSUM on whitened `r`):
- **E-R0:** `q, q̇, τ_realized` at 1 kHz.
- **E-R1 (proposed contract):** the same at 200 Hz.
- **E-policy:** `q, q̇` at 50 Hz plus the commanded PD setpoints. Torque is reconstructed from the known PD law. No realized torque.

**Threshold:** set per contract so that false events are ≤ 0.01 per second on the contact-free data.

**Metrics per contract × class:** TPR; onset-to-detect latency (median, p95); link localization accuracy (link 1 vs link 2, from the residual pattern); null-class detection rate; and the ratio of mean CUSUM delay to the C4 bound computed from the measured residual noise.

**Pre-registered pass/fail** (main row σ_τ = 0.2, pooled over 3 seeds):

| ID | Criterion | Role |
|---|---|---|
| **PF-1** | E-R1: TPR ≥ 0.90 and p95 latency ≤ 15 ms for all classes with `d ≥ 10 ms` and `‖J_cᵀF‖ ≥ 1 N·m` | Contract **sufficiency** |
| **PF-2** | **Falsifier of C7:** E-policy within 0.05 TPR **and** within 10 ms p95 latency of E-R1 on **every** class with `d ≥ 10 ms` | If triggered: C7 downgraded; the S0/S2a merge loses necessity; recommend S1-first |
| **PF-3** | Null-class detection rate ≤ 2× the contact-free false-event rate (same window), for all contracts | Grade-1 sanity (C3). If violated: the spike is **invalid** (bug), not a fail of the thesis |
| **PF-4** | No contract's mean CUSUM delay is below 0.9 × the C4 bound | Premise sanity (C4). If violated: noise model wrong, C4 premises revised |
| **PF-5** | E-R1 link localization ≥ 0.90 on identifiable classes with `d ≥ 20 ms` | Floor is useful upward (I2 `dir` field) |

**Overall spike verdict:** **PASS** iff SA-1 PASS ∧ PF-1 ∧ PF-3 ∧ PF-4 ∧ PF-5 ∧ ¬PF-2. **FAIL-thesis** iff PF-2 is triggered or PF-1 fails. **INVALID** iff SA-1 fails, PF-3 fails or PF-4 fails (fix the harness first).

**Machine-readable output (`summary.json`):** `{verdict, sa1:{cells:[…], pass}, sa2:{per_contract:{E-R0|E-R1|E-policy:{per_class:{tpr, lat_med_ms, lat_p95_ms, loc_acc, null_rate}}}, pf:{PF-1..PF-5: bool}, seeds, sigma_tau, runtime_s}`.

**Deferred stage SA-3 (not in this wall clock):** a floating-base legged model in MuJoCo once it is installed (no paid compute). Known foot contacts are subtracted using stance estimation. The same PF-1/PF-2 are re-run during locomotion. This is where the S1 interaction is tested.

---

## Failure modes & reversibility

| # | Failure mode | Detection | Mitigation | Cost to abandon |
|---|---|---|---|---|
| F1 | target-plant drivers do not expose current/realized torque at ≥ 200 Hz | Hardware audit before any S1 work | Use a motor-current proxy, raise the driver-firmware request, or narrow C7's scope to the joints that do. If none do, the contract is unmeetable and S2a stays open | Low. Schema-only change |
| F2 | Unmodeled dynamics (friction, backlash, cables) dominate `r` → high FPR | Contact-free FPR on calibration runs | Free-motion residual calibration, still owned by S0. A learned residual model is allowed **inside** S0 if it is reported in Σ_r | Low |
| F3 | Floating base plus continuous foot contacts swamp the residual during locomotion | SA-3 | Stance-conditioned subtraction, and foot F/T if present. If PF-1 fails under locomotion, narrow I2 scope to "non-foot contacts during quasi-static phases" | Medium. Narrows usefulness |
| F4 | The passivity envelope is too conservative and limits agility | Envelope-clamp rate in I3 during S1 training | The envelope is a declared bound. Relaxing it requires a challenge against C1′ with measured `b_j`, plus a time-domain passivity observer as the alternative | Low. A parameter, not an architecture |
| F5 | The 2-link spike over- or under-states observability vs a humanoid | SA-3 discrepancy | Treat SA-2 as the necessity test of the *contract* only. Claim nothing about target-plant performance | — |
| F6 | Locking too low-level stalls the program | Calendar: if BLC isn't spiked within 1 week, escalate | BLC is a message schema plus an envelope rule. It does not block parallel S1 training, which consumes I0/I1 | Very low |

**Reversibility summary:** what gets locked is a **schema plus two invariants** (envelope clamp, realized-torque export). There are no learned weights, no training runs and no hardware changes. If PF-2 triggers, the remedy is to drop `τ_realized` from the mandatory set and re-adjudicate P1 with S1 first.

---

## Stackability to S3–S7

| Stage | What it consumes from BLC | Why the gate is not skipped |
|---|---|---|
| **S1** locomotion | I0 (writes setpoints in the envelope), I1 | Works unchanged on today's policies. It must just emit impedance setpoints rather than raw torques |
| **S2b** localization/semantics | I2 `r, Σ_r, ident_flag` | Bounded by C3. `ident_flag` tells S2b where it must not guess |
| **S3** forward sensory prediction | Predicts I1 and I2. The residual `r` *is* the rigid-body prediction error, so S3's first target is to shrink Σ_r in free motion | Gives S3 a quantitative, falsifiable target (residual variance reduction) instead of a narrative |
| **S4** active probing | I2 `ident_flag`, `null_dim` | C3 supplies the probing objective: choose motions that move contact wrench components out of `null(J_cᵀ)` |
| **S5** contact-as-relation | I4 episodes (Scene Graph-owned) | Relation and object identity live in Scene Graph. The body loop never asserts them |
| **S6** self-motion-conditioned vision | I1 (ego-motion: `q̇`, IMU) on the same clock | Common timestamps are part of the contract |
| **S7** composition/memory (Life Core) | I4 via Scene Graph, I3 summaries; writes only I5 presets | Life Core is kept out of R0/R1 by construction. S7 is not settled here |

---

## Explicit non-claims

1. **Not** claiming BFM-Zero, or any pretrained BFM, estimates contact. This proposal assumes it does not, and builds the floor so the question becomes measurable.
2. **Not** claiming the frozen-BFM-plus-contact-planner route is feasible. BLC is agnostic to which R2 policy sits above it.
3. **Not** claiming passivity is necessary for stability. C1 is a passivity bound, and non-passive designs can be stable for specific environments. The claim is only that a *passive guarantee against unknown environments* requires the fast tier.
4. **Not** claiming an explicit (vs implicit) contact representation is necessary. I2's explicit fields are an **engineering/audit choice**. The necessity content is C2 and C7, which are about *information availability*.
5. **Not** claiming S1 is unimportant or that locomotion should wait. S1 development proceeds in parallel as the first consumer of I0/I1.
6. **Not** claiming any biological ordering (G3-a, G3-b) as a constraint.
7. **Not** claiming spike results transfer quantitatively to the target plant, or any superiority over Light-Loco-Parkour/PHP.
8. **Not** settling S2b, S3–S7 internals or the Life Core design.
