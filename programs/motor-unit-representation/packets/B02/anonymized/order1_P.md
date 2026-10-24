# Candidate P (Packet B02): E0–E4 Scene Synchronization, Inertia-Scaled Rule Calibration Wiring, and Coverage Gate Closure

**Packet ID**: `B02`
**Author Slot**: Primary Author A
**Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
**Inherited Ledger Snapshot**: `X-BASE-001`..`X-BASE-005`, plus `D-B01-001` (causal `p_5065` partition, merged norms in `synthesis/B01-synthesis.md`)
**Frozen Context Read**: `PROGRAM_CHARTER.md`, `packets/B02/brief.md`, `baseline/02`, `baseline/03`, `packets/B01/decision.md`, `synthesis/B01-synthesis.md`
**Audit Issues Addressed**: #1, #2, #3, #5, #6, #8 (#4 is inherited as solved by `D-B01-001`; #7 and #9 are out of scope, but §2.4 notes a side effect on #7)
**Status of Every Claim Below**: `Candidate` (Appendix B.4). Nothing in this draft is empirical evidence. §6 is a pre-registration, not a result. The only numbers computed while drafting are arithmetic checks (buffer residency, memory headroom, discrete PID eigenvalues, `tanh` derivatives). They are labelled as arithmetic wherever they appear.

---

## 0. Summary of Position

1. **Issue #1 has one root cause: two independent samplers.** The scene label and the step-level torque generator are drawn separately, so they can disagree. The fix is a single pure function `make_program(run_seed, config_id, scene, ordinal) → SceneProgram`. It emits the label, the full open-loop `τ_ext[0:T]` array, the reference trajectory, the initial state and the declared event windows together. The environment only reads from the program. The label is a field of the program, not a separate draw. Episodes are never terminated early, so a declared window can't be truncated.
2. **The episode clock is fixed at T = 64 control steps (1.28 s) for every scene, plus a 16-step unstored history pre-roll.** E3 has a plateau of ≥ 46 steps (≥ 25 required). E4 has a time-triggered release edge at `t_rel ∈ [24, 32]` and ≥ 30 quiet recovery steps (≥ 20 required). Release is time-triggered, never state-triggered, so all of Group 18 stays exogenous in the sense of `D-B01-001`.
3. **Both replay partitions are slot-addressed by (config, scene) cell, not global FIFOs.** Each cell has a fixed capacity: rule `45/34/45/34/68` and policy `91/68/91/68/137` transitions per config for E0..E4. Every policy cell can hold at least one complete 64-step episode (minimum capacity 68 ≥ 64). The 720-cell minimum quota is therefore structural, not statistical. A global FIFO under i.i.d. scheduling leaves about 186 of 720 cells empty at any time (arithmetic, §4).
4. **The rule partition can't store a complete episode for every cell**, because 32,768 / 64 = 512 < 720 (Claim `C-B02-P-01`). It stores declared windows of 34–45 transitions cut from complete rule rollouts. The windows are anchored to the program's event times, so every E3 rule window lies inside the load plateau and every E4 rule window contains the release edge plus ≥ 26 recovery steps.
5. **Normalizers (#6)**: replay stores raw FP32. Statistics are recomputed exactly over the resident buffer with the sampling weights ρ (1/3 rule, 2/3 policy, scene quotas). Every refresh is applied through a function-preserving re-parameterization of each network's first linear layer. Both slices of every mini-batch see the same normalizer, and no refresh changes any network output.
6. **Anti-saturation (#8)**: a pre-activation hinge penalty on `y` (with `a = tanh(y)`) beyond `y_max = 2.0` bounds gradient attenuation at `sech²(2.0) = 0.0707` instead of letting it go to zero. All E3/E4 load programs are built so the required static holding effort satisfies `|u*| ≤ 0.92 < tanh(2.0) = 0.964`, so the penalty never binds at a holding optimum (Claim `C-B02-P-02`).
7. **Static-holding panel (#5)**: z is constant per episode, `z_hold(q*) = B_ω(N_g(g13_hold(q*)))`, and no reference generator runs during evaluation. RMSE is computed on simulator-truth `q̇` over fixed scoring windows, separately for E0, E3 and E4, and each must be < 0.35 rad/s. The rule controller must pass the same panel at < 0.10 rad/s as a positive control, otherwise the panel itself is invalid.
8. **Cross-coverage (#3)**: `cross_coverage_144_x_5` is a 720-record JSON matrix. Its event counts are computed from simulator readbacks (applied external torque and contact torque), not from labels. `coverage_ready` is the AND of all per-cell gates, a zero `scene_sync_violation_count`, and a passing evaluator negative control.

---

## 1. Synchronized E0–E4 Step-Level Generator Contract

### 1.1 Plant convention and timing

Control step Δt = 20 ms with four 5 ms physics substeps and zero-order hold on `u_clip,t` over `[t, t+1)`. The joint equation used for the schedule definitions (simulator ground truth) is

$$
J\,\ddot q \;=\; S_{\max}\,u_{\mathrm{clip}} \;+\; \tau_g(q) \;+\; \tau_{\mathrm{ext}} \;-\; b\,\dot q \;-\; \tau_c\,\mathrm{sgn}(\dot q) \;+\; \tau_{\mathrm{stop}} \;+\; \tau_{\mathrm{contact}},
\qquad S_{\max} = 1.25\,C_0 .
$$

The static holding effort at target `q*` under external torque `τ_ext` is

$$
u^\star(q^\star,\tau_{\mathrm{ext}}) \;=\; -\,\frac{\tau_g(q^\star) + \tau_{\mathrm{ext}}}{S_{\max}}\qquad(\text{ignoring stiction, which only helps}).
$$

`τ_ext[t]` is held constant across all four substeps of step `t` and is written to the simulator before substep 1. Every load edge therefore falls exactly on a control boundary.

### 1.2 The `SceneProgram` object (single source of truth)

```text
SceneProgram (frozen, immutable):
  config_id ∈ [0,144)   scene ∈ {E0..E4}   ordinal n ∈ ℕ   domain ∈ {TRAIN_RULE, TRAIN_POLICY, PANEL}
  T = 64, T_pre = 16
  q0, qd0                                  # initial state at end of pre-roll
  q_ref[0:T], qd_ref[0:T]                  # used by rule controller and z_hold episodes only
  tau_ext[0:T]                             # open-loop external torque (N·m), exogenous
  obstacle: {q_obs, side, k_c, zeta_c, e_rest} | None     # E2 only
  mode, t_on, t_rel, plateau_level, impulse  # generator parameters → Group 18 timers/modes
  windows: {hold:[a,b), sustain:[a,b), release_edge:t_rel, recovery:[a,b),
            contact_phase:[a,b), escape_cmd_onset:t, rule_insert:[a,b)}
  kappa                                    # rule feedforward flag (§2.1)
make_program(run_seed, config_id, scene, n, domain) -> SceneProgram   # pure function
```

* **Randomness**: Philox-4x32 counter RNG keyed by `(run_seed, domain, config_id, scene, n, draw_index)`. No global RNG state is consumed. A program is reproducible from its 4-tuple key, so the replay sidecar stores only the key (§2.6) and checkpoint/resume parity (`resume_diff_norm = 0.0`) is preserved: the scheduler pointer is the only collector state.
* **Feasibility redraw**: if a drawn `q*` violates a feasibility precondition (below), `make_program` redraws with `draw_index += 1`, up to 16 attempts, and otherwise raises `ProgramInfeasible(config_id, scene)`. The cell is marked `infeasible` in the coverage ledger, which forces `coverage_ready = false`; nothing is dropped silently. The redraw depends only on exogenous parameters. It is not rejection on rollout outcomes.
* **Self-check at reset (fail-closed)**: `env.reset(program)` evaluates the window predicates of §1.5 on the program arrays themselves and raises on any violation.
* **No early termination**: episodes run all 64 steps. Stop contact, saturation or large velocity never terminate an episode. Only a NaN or solver failure terminates, in which case the episode is tagged `invalid`, its inserted transitions are rolled back slot-for-slot (§2.6), and the cell is re-collected with `n+1`. `invalid_episode_count` is a ledger field.
* **Pre-roll** (`t = −16..−1`, not stored, not counted): the joint is kinematically locked at `q0` and `τ_ext = τ_ext[0]`. The behaviour controller (rule or policy) runs, so the 160 ms fast and 320 ms slow windows of `x137` are valid at `t = 0`. The lock is released at `t = 0`.
* **Group 18 exogenous carriers** (compatible with `D-B01-001`): `scene one-hot`, `mode`, `t − t_on`, `t_rel − t` (clipped at 0), `plateau_level / S_max`, `impulse flag` and `impulse amplitude`. All of them are functions of `(program, t)` only. Because the release is time-triggered, there are no state-triggered release counters in this design.

Common draws (all uniform on the stated range via Philox unless stated otherwise):

* `q*` ∈ `[q_min + 0.15 Δq, q_max − 0.15 Δq]`.
* **Feasibility precondition F1**: `|u*(q*, 0)| = |τ_g(q*)| / S_max ≤ 0.70`. This leaves load headroom for E3/E4.
* **Load magnitude** is drawn as a target holding effort, not a raw torque. Draw sign `σ ∈ {+1, −1}` (`σ = +1` if `n mod 2 = 0`) and magnitude `m` from the scene bin, then set `τ_ext = −σ m S_max − τ_g(q*)`. If `|τ_ext| < 0.15 S_max`, flip `σ`. This gives `|τ_ext| ≥ 2m S_max − 0.15 S_max ≥ 0.25 S_max` for `m ≥ 0.2`. By construction `|u*| = m ≤ 0.92`, which is the feasibility margin used by §2.5.

### 1.3 Episode-level allocation (exact scene quotas)

Per configuration, scenes are allocated in **20-episode rounds**: E0 ×4, E1 ×3, E2 ×4, E3 ×3, E4 ×6, which is exactly 20/15/20/15/30 %. A global round is 144 × 20 = 2,880 episodes, ordered by a fixed low-discrepancy interleave. The episode at round position `j` is the `j`-th entry of a van der Corput permutation of the 2,880 `(config, scene, k)` tuples, so each cell's episodes are spread evenly through the round. Under slot addressing (§2.6) this ordering is not required for correctness. It only equalizes data age across cells. The policy-episode ordinal for cell `(c, s)` is a monotone counter `n_{c,s}`.

### 1.4 Step-level schedules (T = 64; indices are control steps; ranges half-open)

**E0 `FREE_SPACE_NOMINAL`** (`τ_ext ≡ 0`, no obstacle)

* `n mod 4 = 0` (**pure hold**): `q_ref ≡ q*`, `q0 = q* + δ` with `δ ∈ [−0.05, 0.05]` rad. `windows.hold = [12, 64)`.
* Otherwise (**hold–move–hold**): `q_ref = q*₁` on `[0, 24)`, min-jerk to `q*₂` on `[24, 40)`, `q*₂` on `[40, 64)`, with `|q*₂ − q*₁| ≥ 0.2 Δq`. `windows.hold = [12, 24) ∪ [48, 64)`.
* `windows.rule_insert = [10, 55)` (45 transitions).

**E1 `BOUNDARY_LIMIT_ESCAPE`** (`τ_ext ≡ 0`)

* Stop side alternates with `n`. `q0` is placed so that the stop margin is `d ∈ [0, 0.04]` (schema units of `d_min`/`d_max`, so `< 0.05` always holds).
* `n mod 3 = 0` (**press-then-escape**): outward `q_ref` 0.05 rad beyond the stop on `[0, 16)`, then inward `q_ref = stop ± 0.30 Δq` (min-jerk over 8 steps) on `[16, 64)`. `escape_cmd_onset = 16`.
* Otherwise (**escape**): the inward command starts at `0`. `escape_cmd_onset = 0`.
* **Escape event** (physics-verified): within 25 steps of `escape_cmd_onset`, the true margin exceeds 0.10 and does not fall back below 0.01 before `t = 64`.
* `windows.rule_insert = [escape_cmd_onset, escape_cmd_onset + 34)` (34 transitions; ends ≤ 50).

**E2 `COMPLIANT_AND_RIGID_CONTACT`** (`τ_ext ≡ 0`)

* `q_obs ∈ [q_min + 0.3 Δq, q_max − 0.3 Δq]`, approach side alternating.
* Stiffness bin `n mod 3`: compliant `k_c ∈ [10, 100]`, medium `[100, 1000]`, rigid `[1000, 10000]` N·m/rad (log-uniform), with `ζ_c ∈ [0.1, 1.0]` and restitution `e ∈ [0, 0.5]`.
* `q0 = q_obs ∓ 0.25 Δq` (free side). `q_ref`: hold `q0` on `[0, 8)`, min-jerk to `q_obs ± 0.10` rad (0.10 rad into the surface) on `[8, 24)`, hold on `[24, 48)`, min-jerk back to `q0` on `[48, 64)`. `contact_phase = [24, 48)`.
* **Contact event**: `|τ_contact| ≥ 0.05 S_max` for ≥ 5 consecutive steps inside `[16, 48)`.
* `windows.rule_insert = [6, 51)` (45 transitions).

**E3 `SUSTAINED_EXTERNAL_LOAD`**

* `q_ref ≡ q*`, `q0 = q*`.
* Magnitude bin `n mod 3`: low `m ∈ [0.2, 0.5]`, mid `[0.5, 0.8]`, high `[0.8, 0.92]`. The high bin exercises #8.
* `t_on ∈ {6, …, 10}`. Onset mode `n mod 2`:
  * **step-on**: `τ_ext = 0` on `[0, t_on)` and `τ_L` on `[t_on, 64)`. Plateau start `p₀ = t_on`.
  * **ramp-on**: linear `0 → τ_L` on `[t_on, t_on + 8)`, then `τ_L`. Plateau start `p₀ = t_on + 8 ≤ 18`.
* Optional plateau drift for `n mod 4 = 3`: `τ_ext[t] = τ_L + β (t − p₀)` with `|β| ≤ 0.002 S_max`/step, keeping `|τ_ext|` within the effort bound `|u*| ≤ 0.92`. Per-step change ≤ 0.002 S_max, which is far below the 0.02 S_max edge threshold.
* **The load is never released in E3.** Release belongs to E4, so the two regimes can't alias.
* `windows.sustain = [p₀, 64)`, length **≥ 46 ≥ 25**. `windows.rule_insert = [p₀ + 4, p₀ + 38)` (34 transitions, ends ≤ 56). It starts 4 steps after plateau onset to skip the onset transient.

**E4 `POST_LOAD_IMPULSE_RECOVERY`**

* `q_ref ≡ q*`, `q0 = q*`, `m ∈ [0.3, 0.85]`. Step-on at `t = 4`: `τ_ext = τ_L` on `[4, t_rel)` with `t_rel ∈ {24, …, 32}`. The loaded phase is ≥ 20 steps.
* **Release edge at `t_rel` (every E4 episode)**: `τ_ext[t_rel − 1] = τ_L` and `τ_ext[t] = 0` for `t ≥ t_rel`, except as follows.
  * Variant `n mod 3 ∈ {0, 1}` (**R**, pure release): no further changes.
  * Variant `n mod 3 = 2` (**RI**, release + counter-impulse): `τ_ext = −sgn(τ_L) ι S_max` on `[t_rel, t_rel + 2)` with `ι ∈ [0.3, 0.6]`, then 0.
* `windows.recovery = [t_rel + r₀, 64)` with `r₀ = 0` (R) or `2` (RI). Length **≥ 64 − 34 = 30 ≥ 20**.
* `windows.rule_insert = [t_rel − 6, t_rel + 28)` (34 transitions, ends ≤ 60): 6 loaded steps, the edge, then ≥ 26 quiet recovery steps.

### 1.5 Window predicates (enforced twice: on the program at reset, and on simulator readback after rollout)

All thresholds are in units of the config's `S_max`. `τ̃_t` is the external torque read back from the simulator's applied-force channel at step `t`, never the program array.

| Event | Predicate (physics readback) | Required |
|---|---|---|
| Sustained load (E3) | `∀t ∈ W: |τ̃_t| ≥ 0.15` and `|τ̃_t − τ̃_{t−1}| ≤ 0.02`, with `W` contiguous | `|W| ≥ 25` |
| Release edge (E4) | `|τ̃_{t_rel−1}| ≥ 0.15` and `|τ̃_{t_rel}| ≤ 0.01` (R), or the sign flips with a drop ≥ 0.15 (RI) | exactly 1 |
| Recovery (E4) | `∀t ∈ W: |τ̃_t| ≤ 0.01`, `W` immediately follows the edge (or the impulse), constant `q_ref`, no contact | `|W| ≥ 20` |
| Contact (E2) | `|τ_contact| ≥ 0.05` for ≥ 5 consecutive steps | ≥ 1 |
| Stop-proximal start (E1) | true margin `< 0.05` at `t = 0` | yes |
| Cross-regime exclusion | E0/E1/E2: `max |τ̃| ≤ 0.01`; E3: no release edge; E0/E1/E3/E4: no contact torque | yes |

**`scene_sync_violation_count`** is the number of episodes whose readback predicates disagree with their label, in any direction (for example a label of E3 with a broken plateau, or a label of E0 with load present). It must be 0. Each episode contributes **at most one** count per event type. Overlapping sliding windows are never counted multiple times, which closes the "sliding window inflation" route to fabricated counts.

**This resolves #1.** Label, torque schedule and windows come from one pure function. The predicates are checked on the program before rollout and on physics after rollout. Because E3/E4 episodes are never terminated early, the declared windows are guaranteed to be present in the physics regardless of what the behaviour policy does: the torque is open-loop and exogenous, and the policy can't remove it.

### 1.6 Evaluation programs (resolves the generator half of #5)

The frozen panel uses the same `make_program` with `domain = PANEL`. Panel keys are disjoint from every training key, and no reference generator runs: `q_ref` and `qd_ref` are not passed to the policy, which sees only the constant `z_hold(q*)` (§3.1). The panel scene programs are specified in §3.2.

---

## 2. Rule Calibration Wiring, Normalizer Contract, and Anti-Saturation Actor Loss

### 2.1 Exact `rule_calibration` law

$$
\begin{aligned}
e_t &= q_{\mathrm{ref},t} - q_{c,t}, \qquad \dot e_t = \dot q_{\mathrm{ref},t} - \dot q_{c,t},\\
\hat\tau_{\mathrm{bias},t} &= -\bigl(\hat\tau_g(q_{c,t}) + \kappa\,\tau_{\mathrm{ext},t-1}\bigr),\\
v_t &= \frac{\hat\tau_{\mathrm{bias},t} + J_{\mathrm{nom}}\bigl(k_p e_t + k_d \dot e_t\bigr) + \tau_{I,t}}{S_{\max}},\qquad
u_{\mathrm{rule},t} = \operatorname{clip}\bigl(v_t + \varepsilon_t,\,-1,\,1\bigr),\\
\tau_{I,t+1} &= \operatorname{clip}\Bigl(\tau_{I,t} + \mathbb 1[\neg\mathrm{freeze}_t]\, J_{\mathrm{nom}}\,k_i\, e_t\,\Delta t,\; -0.6\,S_{\max},\; 0.6\,S_{\max}\Bigr),\\
\mathrm{freeze}_t &= \bigl(|v_t| \ge 1 \wedge \mathrm{sgn}(e_t) = \mathrm{sgn}(v_t)\bigr) \vee d_{\min,t} < 0.05 \vee d_{\max,t} < 0.05 \vee \mathrm{contact}_t .
\end{aligned}
$$

* `J_nom = I_{D,zz} + n_g² J_rotor` comes from the config's nominal descriptor (Groups 7–12). `τ̂_g` is the nominal gravity model. The rule is a **training-time behaviour policy**: it may read privileged nominal plant data and `contact_t`, and it is never exported. The tripwire is that the deployment-export test asserts no `rule_calibration` symbol is reachable from the exported graph.
* Gains: closed-loop natural frequency `ω_n = 15 rad/s`, `ζ = 0.9`, which gives `k_p = 225 s⁻²` and `k_d = 27 s⁻¹`. The integral pole is at `ω_n/5`, so `k_i = ω_n³/5 = 675 s⁻³`. Arithmetic check on the inertia-normalized double integrator with 20 ms ZOH: the max closed-loop eigenvalue modulus is **0.898** with no delay and **0.902** with a one-step compute delay, so it is stable with margin. The inertia scaling makes this bandwidth identical across all 36 geometry seeds, up to the nominal-vs-true inertia mismatch.
* Feedforward flag `κ`: `κ = 1` (one-step-delayed, observer-like) in E3, which produces genuine equilibrium anchors. `κ = 0` in E4, so the integral has absorbed `τ_L` before release and the release produces a real wound-integrator recovery transient. A κ = 1 controller would cancel the release instantly and leave nothing to learn. `τ_ext = 0` in E0–E2 makes κ irrelevant there.
* Exploration `ε_t ~ N(0, σ²)`: `σ = 0.01` inside `windows.hold`, `windows.sustain` and `windows.recovery`, and `σ = 0.05` elsewhere. Action diversity for F comes mainly from the policy partition. The rule partition's job is anchors.
* `τ_I` is reset to 0 at the start of the pre-roll. Because the controller acts during the lock, the integral has already absorbed any `τ̂_g` model error by `t = 0`.

### 2.2 Wiring into P0 and the rule partition (resolves #2)

Proposed module contract. The names are illustrative; the binding requirement is the behaviour, mapped onto the existing legacy-sampler call sites.

```text
collector.collect_episode(program, behavior)          # behavior ∈ {RULE, MIXED(β), POLICY}
  RULE   -> rule_calibration.RuleController(cfg_descriptor).act(state_priv, program, t)
  MIXED  -> clip((1-β)·u_rule + β·π(x137, z) + ε)
  POLICY -> clip(π(x137, z) + ε_explore)
  "legacy_pd" / open-loop sampler -> raise LegacyBehaviorForbidden   # tripwire
ledger: rule_controller_impl_sha256, rule_gain_table (per config: J_nom, k_p, k_d, k_i)
```

**P0 is redefined as two deterministic phases**, replacing the 800-transition legacy warmup.

* **P0-R (rule fill)**: for each of 144 configs, run 6 rule episodes (E0, E1, E2, E3, E4-R, E4-RI) with `domain = TRAIN_RULE` and ordinal 0. Each episode inserts only its `windows.rule_insert` into that cell's rule slots: 45 + 34 + 45 + 34 + (34 + 34) = **226 transitions per config, 32,544 in total**. The remaining **224 reserve slots** are filled by 7 extra episodes of 32-step windows from E3/E4 cells chosen by a rotating pointer over the 288 E3/E4 cells. Cost: (864 + 7) × 80 = 69,680 simulator steps.
* **P0-M (mixed warm start of the policy partition)**: one episode per cell (720 episodes, 46,080 transitions), with `β` cycling over `{0.25, 0.5, 0.75, 1.0}` by ordinal and tagged `MIXED(β)`. Gradient updates begin after P0-M. Cost: 720 × 80 = 57,600 simulator steps.
* **Rule partition refresh during training**: every 64 updates, one config (round-robin) re-runs its 6 rule episodes at `ordinal += 1`. The new transitions overwrite that config's slots **slot-for-slot in place** as they are produced, so the per-cell counts never change and no staging copy is allocated (§2.6). A full refresh cycle takes 144 × 64 = 9,216 updates. This diversifies `q*`, load bins and modes without breaking quotas.
* **Rule validity gate per config (fail-closed)**: after P0-R, every config's E3 rule window must show `RMS(q̇) ≤ 0.10 rad/s` and `|q − q*| ≤ 0.02 rad`. If it doesn't, the config is flagged `rule_infeasible`, which blocks `coverage_ready`. Nothing is dropped.

### 2.3 Policy-side holding episodes

In online collection, 25 % of the E0, E3 and E4 policy episodes use `z = z_hold(q*_program)` (§3.1), computed at reset with the current `B_ω` and normalizer. The other 75 % use the baseline z sampler unchanged. This puts on-policy holding attempts in exactly the cells the holding gate scores, without touching the FB objective.

### 2.4 Stratified mini-batch sampler

Each update draws `B_mb` transitions. `B_mb` is inherited from the baseline; the example uses 512.

1. Partition split `⌈B_mb/3⌋` rule and the rest policy. For `B_mb = 512` that is 171 / 341.
2. Within each partition, split across scenes by 20/15/20/15/30 using largest-remainder rounding. The remainder bonus rotates across updates, so long-run proportions are exact. For 512 this gives rule `34/26/34/26/51` and policy `68/51/68/51/103`.
3. Within each scene slice, pick configs by sampling without replacement over the 144 configs (reshuffled per epoch), then pick a uniform slot within the cell.

Side effect on #7, not claimed as a resolution: realized batch scene proportions now match the nominal quotas exactly, so the quota-deviation premise of #7 no longer occurs once P0-M completes. Inverse-probability weighting remains the subject of another packet.

### 2.5 Normalizer contract (resolves #6)

1. **Replay stores raw FP32 values.** The layout is unchanged; only the semantics change if the legacy path stored normalized values. Normalization happens at batch time with one shared normalizer, so the rule and policy slices of a batch are always normalized identically.
2. **Statistics are ρ-weighted buffer moments, not rollout-stream moments.** For each normalized input coordinate `j` (all of `x137`, `g13`, and the retained/replaced `p5065` slots),

   $$
   \mu_j = \sum_i w_i\, v_{ij},\qquad \sigma_j^2 = \sum_i w_i (v_{ij}-\mu_j)^2,\qquad
   w_i = \frac{\rho_{\mathrm{part}(i)}\,\rho_{\mathrm{scene}(i)}}{144\; n_{\mathrm{cell}(i),\mathrm{part}(i)}},
   $$

   with `ρ_rule = 1/3`, `ρ_policy = 2/3` and `ρ_scene = (0.20, 0.15, 0.20, 0.15, 0.30)`. These are exactly the marginal weights of the §2.4 sampler, so the normalizer describes the distribution the networks are trained on.
   * Accumulation is an exact two-pass FP64 computation over resident slots, in chunks of 256 rows (256 × 10,418 × 8 B ≈ 21 MB of scratch, which is no larger than one batch's existing working set).
   * Floor: `σ_j ← max(σ_j, 10⁻³ · max(|μ_j|, 1))`.
   * Categorical and one-hot fields, plus `a` and `z`, are passed through unnormalized.
   * Slots masked by `D-B01-001` stay frozen at `(0, 1)` and are excluded from updates.
3. **Cadence**: one refresh at the end of P0-M, then every `K_norm = 2,048` updates. Running per-step updates are removed entirely.
4. **Function-preserving refresh.** For every first linear layer `y = W x̂ + b` consuming normalized input `x̂ = (x − μ)/σ`, in `π_θ`, `B_ω`, `F_{η1}`, `F_{η2}` and their target copies, a change `(μ, σ) → (μ', σ')` is applied as

   $$
   W' = W\,\mathrm{diag}(\sigma'/\sigma),\qquad b' = b + W\bigl((\mu'-\mu)/\sigma\bigr),
   $$

   which makes `W' x̂' + b' ≡ W x̂ + b` for all `x`. A downstream LayerNorm sees identical pre-activations. Adam moments of `W` are rescaled column-wise: `m` by `σ'/σ`, and `v` by `(σ'/σ)²`.

   Consequence: **a normalizer refresh changes no network output.** Normalizer drift therefore can't create covariate shift on either slice. What remains is the genuine rule/policy difference in raw data, which the stratified sampler presents at fixed proportions by design.
5. **Test hooks**: `norm_refresh_max_rel_output_change` must be ≤ 10⁻⁵ (FP32) on a fixed probe set of 1,024 rule and 1,024 policy transitions. `norm_stats_recompute_rel_err` (ledger stats versus an independent recomputation) must be ≤ 10⁻⁶.

### 2.6 Slot-addressed replay and memory accounting

* **Rule partition** has 32,768 slots: 144 configs × 226 per-cell slots (E0 45, E1 34, E2 45, E3 34, E4 68) = 32,544, plus 224 reserve slots.
* **Policy partition** has 65,536 slots: 144 × 455 per-cell slots (E0 91, E1 68, E2 91, E3 68, E4 137) = 65,520, plus 16 reserve slots that are never sampled (they hold the in-flight write cursor for rollback).

Each policy cell is a FIFO ring over its own slots. Because the minimum cell capacity is 68 ≥ T = 64, **the most recent complete episode of every policy cell is always resident**, so a full E3 plateau or a full E4 release + recovery is always in the buffer for every config.

Per-scene shares of the combined buffer are E0 19.9 %, E1 15.0 %, E2 19.9 %, E3 15.0 % and E4 30.1 % of rule slots, and 20.0 %, 14.9 %, 20.0 %, 14.9 % and 30.1 % of policy slots.

| Item | Size | Notes |
|---|---:|---|
| Replay tensors (98,304 × 41,677 B) | 4.0969 × 10⁹ B | Inherited. 41,677 B ≈ 10,419 FP32, consistent with `2·(137+5065) + 1 + 13 = 10,418` plus one flag (inferred, not read from code) |
| Sidecar `uint8 config, uint8 scene, uint8 step, uint8 flags, uint32 ordinal` | 0.79 MB | 8 B/transition. Programs are regenerated from keys, never stored |
| Normalizer FP64 sums (3 × 10,418 × 8 B) | 0.25 MB | |
| Coverage ledger (720 × 16 int64) | 0.09 MB | |
| Rule refresh staging | 0 | In-place slot-for-slot writes |
| **Tensor total** | **≈ 4.0980 × 10⁹ B ≤ 4.10 × 10⁹ B** | Headroom before additions was 3.0 MB (30.5 B/transition). Additions use 1.13 MB |

Peak RSS: no new long-lived allocation exceeds 1.2 MB. The normalizer pass (21 MB scratch) and the evaluation panel run between updates, using no more scratch than one batch. The peak must still be measured. §6 gates it at ≤ 4.694 × 10⁹ B and treats exceeding it as a hard failure.

### 2.7 Anti-saturation actor loss (resolves #8)

Write `a = tanh(y)`, where `y` is the actor's pre-activation. The actor loss becomes

$$
\mathcal L_\pi = -\,\mathbb E\!\left[\frac{F_{\min}(x_{137}, p_{5065}, \tanh y, z)^\top z}{\overline{|F^\top z|}}\right]
\;+\; \lambda_{\mathrm{pre}}\;\mathbb E\bigl[\operatorname{relu}(|y| - y_{\max})^2\bigr],
\qquad y_{\max} = 2.0,\ \lambda_{\mathrm{pre}} = 0.1 .
$$

* `F_min` is the baseline's existing twin-critic reduction (unchanged). `F^⊤z` is divided by its running mean absolute value (EMA 0.99), so `λ_pre` doesn't depend on the scale of `F`.
* Per B01 counterfactual hygiene, `p5065` is held at its causal pre-action value while `a` varies.
* **Gradient bound**: for `|y| ≤ y_max`, `|∂L/∂y| ≥ sech²(2.0) · |∂(F^⊤z)/∂a| = 0.0707 · |…|`, which is at most a 14× attenuation. Without the penalty, an actor drifting to `y = 5` sees `sech² = 1.8 × 10⁻⁴`, roughly 5,500×. Once `|y| > y_max`, the penalty contributes the restoring gradient `2λ_pre(|y| − y_max)` regardless of `F`'s slope.
* **Non-binding at holding optima**: every E3/E4 program has `|u*| ≤ 0.92 = tanh(1.589) < tanh(2.0) = 0.964` (§1.2). Exact static holding is therefore always achievable inside the penalty-free region. The authority cost is 3.6 % of `S_max`, and it applies only when the true optimum is beyond 0.964, which never happens for holding in the training distribution.
* **TD target smoothing (secondary)**: the next action in the Bellman target is `a' = clip(tanh(y') + clip(N(0, 0.1²), ±0.25), −1, 1)`. This regularizes `F` along `a` near the ±1 boundaries, where the rule partition supplies real data at `|u| ∈ [0.8, 0.92]`.
* **Logged metrics**: `sat_frac = P(|y| > y_max)`, `sat_frac_E3_high`, and the actor's `|∂L/∂y|` on the E3-high probe set.

---

## 3. Frozen Static-Holding Evaluation and 720-Cell Cross-Coverage Gate

### 3.1 Static target vector `g13_hold(q*)` (resolves the target half of #5)

For the baseline 02 layout (L13-A):

$$
g_{13}^{\mathrm{hold}}(q^\star) = \bigl[\cos q^\star,\ \sin q^\star,\ 0,\ 0,\ p_{\mathrm{tip}}^M(q^\star),\ 0_3,\ 0_3\bigr],
\qquad
p_{\mathrm{tip}}^M(q^\star) = o_J^M + L_D\bigl(\cos q^\star\, e_1^M + \sin q^\star\, e_2^M\bigr),
$$

with `q̇* = 0`, `q̈̂* = 0`, `v_tip = 0` and `â_tip = 0`. The tip position comes from the calibrated forward kinematics: joint axis `e_3^M`, encoder zero along `e_1^M`, joint origin `o_J^M`, all from the 8-D static descriptor and the calibration record. Every quantity is deployment-available, with no privileged fields. This assumes the baseline 01 calibration convention, which wasn't in my read set. The spike must assert agreement with the FK used to compute `g13` on the first 1,000 transitions (max error < 10⁻⁵ m).

If the locked manifest uses variant **L13-U** (scalar effort `u_clip` replaces the constant out-of-plane tip coordinate), the effort slot is set to the deployable gravity-only value `u*_g = −τ̂_g(q*)/S_max`. Under E3/E4 load this slot is deliberately "wrong", because the upper layer can't know the load. The spike reports the RMSE sensitivity with the slot masked versus set. The manifest's actual layout must be recorded in the spike ledger.

$$
z_{\mathrm{hold}}(q^\star) = B_\omega\bigl(N_g^{\mathrm{snap}}(g_{13}^{\mathrm{hold}}(q^\star))\bigr) \in \mathcal S^{15}(4),
$$

where `N_g^snap` is the normalizer snapshot frozen with the evaluated checkpoint. `z` is held constant for the whole episode. The actor runs deterministically, with no exploration noise and no reference trajectory.

### 3.2 Frozen panel

The panel uses `domain = PANEL` and seed `PANEL_SEED = 0xB02A` (fixed and pre-registered).

* **Targets**: per config, `q* ∈ {q_min + 0.25 Δq, q_min + 0.50 Δq, q_min + 0.75 Δq}`, subject to precondition F1; an F1 violation shifts the target by ±0.05 Δq up to 3 times, deterministically.
* **Episodes**: per `(config, q*)`, 1 E0, 2 E3 (mid and high bins, opposite signs) and 2 E4 (one R, one RI).
* **Size**: 144 × 3 × 5 = **2,160 episodes**. Each is `T_eval = 100` steps plus a 16-step locked pre-roll in which the joint is locked at `q0 = q*` and the **evaluated controller** runs, so its own history fills `x137`. Total 250,560 simulator steps. Panel rollouts don't compute `p5065`, because no `F` is evaluated.

| Scene | `τ_ext` program (eval clock) | Scoring window `W_s` |
|---|---|---|
| E0 | `≡ 0` | `[10, 100)` (90 steps) |
| E3 | `0` on `[0, 10)`, step to `τ_L` at 10, sustained to 100 | `[35, 100)` (65 steps; excludes the 25-step onset transient) |
| E4 | `τ_L` on `[0, 40)` (also present during pre-roll), release (R or RI) at `t_rel = 40` | `[60, 100)` (40 steps, starting 20 steps after release) |

**Metric.** `q̇_t` is the **simulator ground-truth** joint velocity; the calibrated `q̇_c` is also reported. With `𝒫_s` the panel episodes of scene `s`:

$$
\mathrm{zero\_vel\_rmse}_s = \sqrt{\frac{\sum_{e \in \mathcal P_s}\sum_{t \in W_s} \dot q_{e,t}^2}{|\mathcal P_s|\,|W_s|}},\qquad s \in \{E0, E3, E4\}.
$$

**Pass iff** `zero_vel_rmse_E0 < 0.35`, `zero_vel_rmse_E3 < 0.35` and `zero_vel_rmse_E4 < 0.35` rad/s, each separately. Pooling across scenes is not allowed. All 144 configs must be present, there must be no NaN or invalid episode, and the evaluation must use the frozen checkpoint and normalizer snapshot.

Reported but not gating:

* per-config max episode RMSE and its 95th percentile;
* steady-state position error `|q − q*|` over `W_s`, which is required because of `C-B02-P-03`: a constant load can produce zero velocity at a wrong angle;
* E4 peak `|q̇|` and 2 %-band settling time after release;
* the same metrics stratified by `C_0` tier.

**Positive control**: the rule controller (κ = 1 in E3, κ = 0 in E4) must score `< 0.10` rad/s on every scene of the panel. If it doesn't, the panel is declared infeasible and the policy result is void.

This resolves #5. The panel contains no moving targets, no step perturbations of the reference, a constant `z` derived from an equilibrium outcome vector, scoring windows that exclude declared transients, and a positive control proving the panel is achievable by physics.

### 3.3 `cross_coverage_144_x_5` (resolves #3)

The coverage ledger is emitted at every checkpoint into the evaluation summary JSON and is recomputed from the replay sidecar plus readback event flags (each transition's flags byte carries the physics-verified event bits of §1.5):

```json
"cross_coverage_144_x_5": {
  "schema": "B02-A-v1",
  "cells": [ { "config": 0, "scene": "E3",
      "rule_resident": 34, "policy_resident": 68, "rule_quota": 34, "policy_quota": 68,
      "complete_policy_episodes_resident": 1,
      "sustained_load_events": 2, "sustained_anchor_events": 1,
      "release_events": 0, "recovery_events": 0, "contact_events": 0, "escape_events": 0,
      "label_physics_mismatch": 0, "invalid_episodes": 0, "infeasible": false, "rule_infeasible": false }
    /* … 720 records … */ ],
  "sustained_load_hold_count": 0, "post_load_recovery_count": 0,
  "limit_escape_rate_rule": 0.0, "scene_sync_violation_count": 0,
  "starved_cells": [], "coverage_ready": false
}
```

**Definitions** (resident data only; each episode counts at most once per event type):

* `sustained_load_hold_count`: the number of resident E3 episodes, rule windows included, with a physics-verified sustained window ≥ 25. A rule insert window of 34 steps lies entirely inside the plateau, so it qualifies on its own.
* `sustained_anchor_events`: the subset of those with `RMS(q̇) ≤ 0.35` rad/s over the window. This is the equilibrium-anchor count.
* `post_load_recovery_count`: the number of resident E4 episodes or windows with a verified release edge followed by ≥ 20 quiet recovery steps.
* `limit_escape_rate_rule`: the fraction of E1 rule windows with a verified escape event.

**Hard per-cell gates**: every one of the 720 cells must pass all of these.

| Gate | Requirement |
|---|---|
| GC-1 | `rule_resident = rule_quota` and `policy_resident = policy_quota` once policy rings are full. Before that, `policy_resident ≥ 64` (one P0-M episode) |
| GC-2 | `complete_policy_episodes_resident ≥ 1` |
| GC-3 | E3 cells: `sustained_load_events ≥ 2` (rule + policy) and `sustained_anchor_events ≥ 1` |
| GC-4 | E4 cells: `release_events ≥ 3` and `recovery_events ≥ 3` (2 rule + ≥ 1 policy) |
| GC-5 | E2 cells: `contact_events ≥ 2`. E1 cells: `escape_events ≥ 1` (rule) |
| GC-6 | `label_physics_mismatch = 0`, `infeasible = false`, `rule_infeasible = false` |

**Global gates**:

* `sustained_load_hold_count ≥ 288`
* `post_load_recovery_count ≥ 432`
* `limit_escape_rate_rule ≥ 0.95`
* `scene_sync_violation_count = 0`
* the evaluator negative control of §6 S2 has passed on this build

`coverage_ready = (all 720 cells pass GC-1..GC-6) ∧ (all global gates pass)`. Any failing cell is listed in `starved_cells` with the failing gate IDs. The online scheduler then moves that cell to the front of the queue until it passes. If legacy code defines lower thresholds, the stricter value applies.

Why these gates can be met by construction rather than by luck:

* GC-1 and GC-2 follow from slot addressing (§2.6).
* The coverage events in GC-3, GC-4 and GC-5 come from exogenous open-loop programs that can't be terminated early (§1.4–1.5).
* The anchor and escape events depend only on the rule controller, whose validity is separately gated (§2.2).

None of these counts depends on policy competence. Policy competence is measured only by §3.2.

---

## 4. Serious Alternative Considered and Rejected

**Rejected alternative: a global-FIFO replay with an event-driven scene state machine and coverage-driven top-up.** In this design, E3/E4 episodes run until a state-triggered predicate fires (for example, release once `|q̇| < ε` has held for K steps, which mimics "load held"). A coverage monitor detects starved cells and schedules extra episodes or rejects episodes without qualifying windows. The rule controller fills a FIFO rule partition with full episodes. This is the closest patch to the current V3 code, and it would plausibly drive the two marginal counters above zero. I reject it for four reasons.

1. **It breaks the B01 causal contract.** A release triggered by robot state is an endogenous generator state. `D-B01-001` explicitly classifies state-triggered release progress counters as endogenous, so they can't be passed to `F` as exogenous `ξ_t`. The Group 18 timers would then have to be masked, which reintroduces the E4 phase aliasing that B01 was built to remove. A time-triggered release with jitter gives the same coverage with a fully exogenous `ξ_t`.
2. **A FIFO can't provide a per-cell guarantee at this capacity.** With T = 64, the policy partition holds 1,024 episodes. Under i.i.d. scene/config draws at the nominal quotas, the expected number of resident episodes per cell is λ = 1.42 (E0/E2), 1.07 (E1/E3) and 2.13 (E4). The expected number of empty cells is `144 · Σ_s e^{−λ_s}` ≈ **185.6 of 720**. A 200-draw simulation gave mean 185.5 and range 161–207. These are arithmetic checks, not rollouts. A deterministic evenly spaced schedule rescues the FIFO only barely: the worst cell spacing is 960 episodes (E1/E3) against a 1,024-episode window, a slack of 6.25 % that any invalid-episode re-collection or top-up burst destroys. The rule partition can't hold full episodes for 720 cells at all, since 512 < 720 (`C-B02-P-01`).
3. **Rejection on rollout outcomes biases the data.** Discarding episodes whose policy behaviour failed to produce a window (for example, a policy that never reached `|q̇| < ε`, so the release never fired) removes exactly the failure transitions the critic most needs. It also makes the coverage counts depend on policy competence, which conflates the coverage gate with the competence gate.
4. **Coverage-driven top-up makes counts path-dependent and hard to audit.** Two runs with the same seed but different update timing would hold different cell mixtures. Under the proposed design, `cross_coverage_144_x_5` is a deterministic function of the scheduler pointer.

**Also considered and rejected, with briefer reasons:**

* **Freezing normalizers after P0** for #6. This is simple, but it fixes the statistics to warm-start data whose state distribution the online policy will leave, so they go stale as exploration expands. Function-preserving refresh gives the benefit of current statistics at zero output shift.
* **A clipped-linear actor head** (`a = clip(y, −1, 1)`) for #8. It has a zero gradient beyond the clip, which is strictly worse than tanh plus a hinge.
* **Shorter episodes (T ≤ 45)** so that full rule episodes fit per cell. This is arithmetically feasible, but it would shrink the E3 plateau to about 25–30 steps after settle and onset, leaving no margin over the 25-step requirement. It would also cut the E4 recovery window to about 20 steps with no tail for settling-time measurement.

---

## 5. Candidate Necessity Claims (Appendix B)

### `C-B02-P-01` — Window-residency feasibility bound (Grade 1, lower bound)

**Premises**:

* A replay partition of capacity `N` transitions, `K` cells, and episodes of fixed length `T`.
* A qualifying event of scene `s` needs a contiguous span of at least `ℓ_s` transitions to be resident.
* Each cell must contain at least `m_s` such events at every audit time.

**Conclusion**:

* (a) A necessary condition is `N ≥ Σ_cells m_s ℓ_s`. Guaranteeing a complete resident episode per cell needs `N ≥ K T`.
* (b) For the rule partition, `N = 32,768`, `K = 720` and `T = 64` give `K T = 46,080 > N`. Any rule design that covers every cell must therefore store sub-episode windows with mean length ≤ ⌊32,768/720⌋ = 45, or use T ≤ 45.
* (c) For a global FIFO holding `N/T` episodes and filled by i.i.d. cell draws with probabilities `w_c`, the probability that every cell is resident is at most `∏_c (1 − (1 − w_c)^{N/T})`. At the B02 numbers this is effectively 0, with ≈ 185.6 cells expected empty. A deterministic schedule needs `max_c spacing_c ≤ N/T`.

**Implementation independence**: this is pure counting, and it holds for any learner, buffer implementation or controller.

**Falsification mode**: a demonstrated replay scheme that guarantees every cell event under strictly smaller capacity would refute the claim. Since the claim is a counting identity, such a scheme must violate a premise (for example, events sharing transitions across cells, or `ℓ_s` defined smaller), which would narrow the scope rather than refute the bound.

**Use**: it rules out "full rule episodes for all 720 cells at T = 64" and "global FIFO with a hard per-cell gate", without a bake-off.

### `C-B02-P-02` — Bounded saturation attenuation with a non-binding margin (Grade 1, narrow invariant)

**Premises**:

* A deterministic actor `a = tanh(y)`.
* A critic differentiable in `a`.
* A hinge penalty that keeps `|y| ≤ y_max` at stationarity of `L_π`.
* Every training-distribution holding optimum has `|u*| ≤ u_bar < tanh(y_max)`.

**Conclusion**:

* (i) The actor gradient through the head satisfies `|∂(F^⊤z)/∂y| ≥ sech²(y_max) |∂(F^⊤z)/∂a|`. For `y_max = 2`, `sech²(y_max) = 0.0707`.
* (ii) For `|y| > y_max`, the penalty contributes a restoring gradient that is independent of `F`.
* (iii) The penalty's gradient is zero at every static holding optimum, because `atanh(u_bar) < y_max`, so the penalty cannot shift any holding fixed point.

**Falsification mode**: a training-distribution holding program with `|u*| > tanh(y_max)` violates the premise, which shows up as `sat_frac_E3_high > 0` at the panel optimum. That would require either relaxing `y_max` or tightening the load generator. Part (iii) says nothing about non-holding optima, such as maximal-speed z directions.

### `C-B02-P-03` — Internal-model role for load holding (Grade 2, structural; Candidate)

**Premises**:

* The plant of §1.1 under an unknown constant `τ_ext` (the E3 plateau).
* The deployed controller `π_θ(x_137, z)` is memoryless apart from its 320 ms input window.
* The task is zero steady-state angle error at `q*` for all `τ_ext` in the E3 bins.

**Conclusion** (internal-model principle, Francis–Wonham): any controller achieving zero steady-state error against an arbitrary unknown constant disturbance must realize an integrating mode driven by the error. In `π_θ(x137, z)`, the only channel through which persistent state can survive beyond 320 ms is the closed loop through its own past outputs, `u_prev` and the `u_clip` fields in the fast and slow history. A law of the form `u_t ≈ u_{t−1} + k (q* − q_t) − d q̇_t` realizes the integrator.

Corollary for gate design: `zero_vel_rmse` alone can't detect the absence of this role. A proportional-only policy reaches `q̇ = 0` at an offset angle `q* + Δ(τ_ext)`. This is why §3.2 reports position error.

**Operational test (absence detection, B.2)**: at evaluation, replace the `u_prev` and history `u_clip` inputs with their panel-mean constants.

* If the integrating role exists and is realized through this channel, E3 steady-state `|q − q*|` grows by ≥ 3× and becomes proportional to `|τ_ext|`, with slope R² ≥ 0.8 across load bins.
* If it doesn't grow, either the role is absent (E3 position error was already ∝ `|τ_ext|` before the ablation) or it is realized another way (for example through the slow `q` and `q̇` segment means acting as a surrogate). Both outcomes are recorded.

**Grade note**: the internal-model principle is Grade 1 for linear time-invariant plants. Its application to this nonlinear, stiction-bearing, saturating plant through a learned policy is claimed only at Grade 2 (an obligatory functional role), and it remains Candidate.

---

## 6. Pre-Registered Empirical Spike Protocol

**Device honesty**: on the drafting host, `torch` isn't importable and no CUDA device is present. The spike runner records `device`, `torch.__version__`, `torch.get_num_threads()`, the CPU model, wall-clock time and peak RSS (`/proc/self/status VmHWM`). A CPU-only result is reported as CPU-only. Results are never extrapolated to longer runs, and no claim of converged control is made from any stage (Charter boundary 4).

**Pre-registration**: this section, the `make_program` source and the gate constants are hashed with SHA-256 before execution. Seeds `{0, 1, 2}`, `PANEL_SEED = 0xB02A`. Every stage writes `VERDICT.json`, with each gate's value, threshold and `PASS`/`FAIL`, plus the raw per-cell ledger.

### S0 — Program-generator audit (pure, no physics; minutes)

Generate 720 cells × 64 ordinals × {TRAIN_RULE, TRAIN_POLICY} = 92,160 programs, plus the full panel.

| Gate | Pass criterion |
|---|---|
| S0-1 | 0 predicate violations on program arrays (§1.5) |
| S0-2 | Regeneration from keys is byte-identical (SHA-256 of all arrays) |
| S0-3 | Group 18 carriers are functions of `(program, t)` only (static analysis + randomized re-evaluation) |
| S0-4 | Panel keys are disjoint from training keys |
| S0-5 | All E3/E4 programs have `|u*| ≤ 0.92`, and `|τ_ext| ≥ 0.25 S_max` on plateaus |
| S0-6 | Per-config episode-round counts are exactly 4/3/4/3/6 |

### S1 — Rule fill on real physics (P0-R, all 144 configs; CPU)

| Gate | Pass criterion |
|---|---|
| S1-1 | `scene_sync_violation_count = 0` |
| S1-2 | Exactly 144 verified E3 rule sustained windows (each ≥ 25 contiguous steps by physics readback) |
| S1-3 | 288 verified E4 release + recovery windows |
| S1-4 | E3 anchor quality: `RMS(q̇) ≤ 0.10` rad/s in ≥ 95 % of configs, and no config > 0.35. `|q − q*| ≤ 0.02` rad in ≥ 95 % of configs |
| S1-5 | `limit_escape_rate_rule ≥ 0.95` |
| S1-6 | E2 contact verified in 144/144 |
| S1-7 | Rule positive control on the frozen panel: `zero_vel_rmse < 0.10` rad/s on E0, E3 and E4 separately |
| S1-8 | Rule partition tensor = 32,768 × 41,677 B, and sidecar 8 B/transition |

If S1-7 fails, the panel is infeasible: stop and report. Proceeding with an unachievable panel is not allowed.

### S2 — Pipeline closure (P0-R + P0-M + 4,096 updates; 2 normalizer refreshes; 64 rule refreshes; CPU; seeds 0–2)

| Gate | Pass criterion |
|---|---|
| S2-1 | **`coverage_ready = true`** at update 4,096 on all 3 seeds: all 720 cells pass GC-1..GC-6, `sustained_load_hold_count ≥ 288`, `post_load_recovery_count ≥ 432`, `limit_escape_rate_rule ≥ 0.95`, `scene_sync_violation_count = 0` |
| S2-2 | `coverage_ready` remains true at every checkpoint (every 512 updates) after P0-M. No cell is ever below quota during rule refresh |
| S2-3 | **Evaluator negative control**: on a copy of the build, inject (a) a 40-step left shift of E3 `τ_ext` on 10 % of programs and (b) label swaps E3↔E4 on 10 %. The evaluator must report `scene_sync_violation_count` equal to the injected count (±0) and `coverage_ready = false` |
| S2-4 | **Legacy arm L** (legacy sampler + unsynchronized labels, otherwise identical) reproduces `sustained_load_hold_count = 0` or reports violations, which confirms the evaluator distinguishes the arms. A nonzero legacy count is reported as a finding and does not invalidate S2-1 |
| S2-5 | Tensor allocation ≤ 4.10 × 10⁹ B. Peak RSS ≤ 4.694 × 10⁹ B |
| S2-6 | `norm_refresh_max_rel_output_change ≤ 10⁻⁵` for π, B, F₁, F₂ and targets. `norm_stats_recompute_rel_err ≤ 10⁻⁶` |
| S2-7 | Checkpoint at 2,048, resume to 2,560: `resume_diff_norm = 0.0` and an identical `cross_coverage_144_x_5` |
| S2-8 | Deployment export contains no `rule_calibration` or `p5065` reachable symbols, and the parameter count is still 281,617 |
| S2-9 (secondary, #8) | **Saturation probe**: set the actor head bias so `y ≈ 4` on the E3-high probe set, then train 256 updates. The penalty arm must bring `sat_frac_E3_high` below 5 % at least 3× faster, in updates, than the `λ_pre = 0` arm. If neither arm recovers within 256 updates, the result is INCONCLUSIVE |

### S3 — Holding gate (all 144 configs; CPU budget-limited)

* **Arms**:
  * **Full**: S2 build. Seeds 0–2.
  * **−AS** (`λ_pre = 0`, no target smoothing). Seed 0.
  * **−R** (rule partition filled by the legacy sampler, but synchronized programs). Seed 0.
* **Budget**: 20,000 updates per seed at `B_mb = 512`. The estimated cost is ~70 GFLOP per update (arithmetic estimate from the parameter shapes), and the runner records measured throughput. The cap is 12 h of wall-clock per seed on CPU. If the cap is reached first, the stage reports the last checkpoint with `budget_exhausted = true`.
* **Evaluation**: the frozen panel (§3.2) every 2,500 updates, with the final value taken at the last checkpoint.
* **Primary gate (H2 holding)**:
  * **PASS** iff, for Full, `zero_vel_rmse_E0`, `_E3` and `_E4` are each < 0.35 rad/s **on all 3 seeds**.
  * **FAIL** iff any scene is ≥ 0.35 on all 3 seeds.
  * Otherwise **MIXED**, which counts as not passed.
  * A FAIL with `budget_exhausted = true` is recorded as *"not reached within CPU budget"*. It is not evidence against H2, and it is not evidence for it.
* **Attribution** (reported only, single seed): the Full − (−R) and Full − (−AS) differences in per-scene RMSE and E3 position error. No necessity is inferred from these scores (B.3.5).
* **`C-B02-P-03` operational test**: apply the `u_prev`/`u_clip` ablation of §5 to the final Full checkpoint, and report E3 `|q − q*|` before and after, with the slope against `|τ_ext|` (pre-registered thresholds: ≥ 3× growth, R² ≥ 0.8).
* **Reporting**: per-`C_0`-tier RMSE, per-config 95th percentile, E4 settling time and `sat_frac` trajectories.

**What would falsify this proposal's engineering contract** (as opposed to H2 competence): any failure of S0, S1-1/2/3/5/6/8 or S2-1/2/3/5/6/7/8. Any of these means the synchronization, wiring, normalizer or coverage design is wrong as specified, regardless of training budget.
