# Candidate P (Packet B02): E0–E4 Scene Synchronization, Inertia-Scaled Rule Calibration Wiring, and Coverage Gate Closure

**Author:** Primary Author B. **Status:** independent proposal; no experiment results claimed. **Method:** v1.0, `1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`. **Inherited constraints:** `X-BASE-001`–`X-BASE-005`, the program charter, and `D-B01-001` with its synthesis. All necessity claims below remain **Candidate**.

This proposal makes scene exposure and resident replay coverage deterministic. It does **not** assert that scheduling makes an arbitrary policy hold still. Physical holding, recovery, and learned-policy accuracy remain separate measured gates. The frozen files supply neither a complete simulator implementation nor existing numerical minima for the success counters; the numerical minima below are proposed B02 acceptance requirements, not purported inherited values. The 101-update baseline establishes pipeline execution only.

## 1. Synchronized E0–E4 Step-Level Generator Contract

### Episode allocation and physical feasibility

Use configuration IDs `c = 4 * geometry_seed + stroke_id`, `0 <= c < 144`, from the frozen physical configuration manifest. Preserve each seed's assigned capacity tier; do not create a spurious extra factor of three. Validate 36 seeds, four strokes per seed, and representation of all three capacity tiers before collecting. All episodes contain **80 control transitions**, indexed `t=0,...,79`, with four 5 ms physics substeps per 20 ms control interval. Integer indices, rather than floating-point timers, determine all phase changes.

Each configuration receives this exact repeating 20-episode scene sequence:

```text
[E0,E1,E2,E3,E4, E4,E0,E2,E1,E4, E3,E0,E2,E4,E1, E4,E0,E2,E3,E4]
```

Thus episode and executed-transition fractions are exactly `(4,3,4,3,6)/20 = (20,15,20,15,30)%` at complete allocation cycles. Loop over sequence position first, then configuration ID, to reach all 720 cells early. An incomplete cycle reports counts and outstanding obligations; it must not claim exact proportions. Let `j` be the per-cell episode ordinal, starting at zero. Save `c`, scene, `j`, cycle number, step index, configuration hash, and schedule hash in checkpoints. There are no random release times, load durations, or early-success resets.

Define the scalar signed plant convention

\[
J(q)\ddot q=\tau_a+G(q)+\tau_{ext}+\tau_{contact}+\tau_{stop}-\tau_{friction}.
\]

Here `G` is gravity torque, not its cancellation torque. Let `R=q_max-q_min`, `S=1.25 C0`, and `m=min(0.05 rad,0.10R)`. A mandatory preflight checks finite positive inertia, `R>0`, and actuator calibration. Choose static reference anchors from the ordered grid `q_min + k R/20`, `k=4,...,16`, keeping only points with `|G(q)| <= 0.75 S`. The manifest freezes three distinct feasible anchors nearest the 25%, 50%, and 75% stroke positions, resolving ties by smaller angle and removing duplicates before selecting the next nearest point. If fewer than three exist, report **INFEASIBLE_CONFIG** and fail the proposed panel; do not silently drop that configuration or weaken its load.

For E3/E4 use anchor `j mod 3` and required loaded equilibrium actuator fraction `lambda = [0.25,0.60,0.92][floor(j/3) mod 3]`. Choose `sigma` from `(-1,+1)` by maximizing

\[
|A|=|-G(q^*)-\sigma\lambda S|,
\]

breaking a tie with `(-1)^(c+j)`. Freeze `A=-G(q*)-sigma lambda S` at reset. Then loaded equilibrium requires exactly `sigma lambda S`, and `|A| >= lambda S >= 0.25 S`; unloaded equilibrium remains within `0.75 S`. The external torque may exceed the drive capacity when it opposes gravity: feasibility is checked on the **net** equilibrium torque, not external torque alone. The reference remains constant for the entire E3/E4 episode. Lambda `0.92` deliberately supplies near-saturation examples without demanding an impossible static torque above `S`.

This is a feasibility check at the anchors, not a global stability proof along transients. Stops, dynamic saturation, friction uncertainty, and simulator failures remain observable failure modes. Reset the parent/housing pose to its fixed panel pose, start E0/E3/E4 at `q=q*`, `qdot=0`, and clear controller integral and history validity masks. No fabricated acceleration or force history is inserted into replay. Initial history slots use reset values with the manifest's validity masks; evaluate late windows after history is populated.

### Exact scene state machine

All schedules below are held constant across each interval's four substeps. Gravity, friction, and mechanical stops remain physical in every scene. An external obstacle is enabled only in E2. Actual contact forces are solver outputs; their values and whether the robot actually touches a surface cannot be guaranteed by an episode label.

| Scene | External torque at interval `t` | Obstacle/target schedule |
|---|---|---|
| E0, 20% | `tau_ext=0` for all 80 intervals | No external obstacle. For even `j`, static middle feasible anchor throughout. For odd `j`, move between first and third anchors: first anchor on `[0,20)`, cubic `h(r)=3r^2-2r^3`, `r=(t-20)/40`, on `[20,60)`, third anchor on `[60,80)`; use the analytic reference velocity `Delta_q * 6r(1-r)/0.8 s`. |
| E1, 15% | `tau_ext=0` throughout | No external obstacle. Alternate lower/upper stop with `(c+j) mod 2`. Reset at distance `min(0.01 rad,0.02R)` inside that stop, zero velocity. On `[0,10)`, reference lies `0.02R` beyond that stop; on `[10,80)`, reference is the middle feasible anchor with reference velocity zero. This supplies an outward command and then a deterministic inward escape command. |
| E2, 20% | `tau_ext=0` throughout | Place a unilateral obstacle at `q_o=q_min+0.60R` for increasing-angle approach, or its reflected `0.40R` location for decreasing approach, alternating with `(c+j) mod 2`. Surface exists throughout; contact is enabled by actual penetration/touch. Reset `0.15R` before the surface; hold that position on `[0,10)`, command `0.05R` beyond the surface on `[10,50)`, then command `0.15R` back on `[50,80)`. Reference velocity zero for these position commands. Even `j`: compliant unilateral angular spring, `k=10S/R`, damping `b_c=2 sqrt(J_nom k)`, force/torque clipped to oppose penetration and zero when separated, restitution zero. Odd `j`: rigid unilateral constraint with restitution `0.1`, using the simulator's frozen solver settings. |
| E3, 15% | `0` on `[0,10)`; `A(t-9)/5` on `[10,15)`; **`A` on `[15,80)`** | No external obstacle; static reference throughout. Guaranteed 65 consecutive nonzero constant-load intervals. The canonical hold witness is `[40,65)`, 25 consecutive intervals after settling. |
| E4, 30% | `0` on `[0,5)`; `A(t-4)/5` on `[5,10)`; **`A` on `[10,40)`**; **`0` on `[40,80)`** | No external obstacle; static reference throughout. The release is the applied-torque edge between intervals 39 and 40. Thirty full-load intervals precede it and forty zero-load recovery intervals follow it. No subsequent pulse or target change is permitted. |

For E2's compliant branch, with approach direction `d in {-1,+1}`, penetration `delta=d(q-q_o)>0` gives `tau_contact=-d max(0,k delta+b_c d qdot)`; it is zero for `delta<=0`. A Cartesian implementation must reproduce this generalized torque using the documented contact Jacobian and the same unilateral geometry. An unrelated torque injection must not be recorded as obstacle contact.

The training schedule supplies an E4 release rather than an impulse; the brief permits either, and a release gives an unambiguous recovery interval. E0 resets to its interval-zero reference, so its static episodes start at the middle anchor and its moving episodes start at the first anchor. All boundaries are half-open. In particular, E3 `[40,65)` comprises results at control boundaries 41 through 65; E4 `[60,80)` comprises results at boundaries 61 through 80. At boundary 80 enter `DONE`, retain the final measured state/history, set generator phase to terminal and external torque to zero, and store bootstrap discount zero; no interval 80 is executed. All nonterminal rows retain the native baseline discount. Never bootstrap through an episode reset.

### Collector ordering and physical witnesses

At interval `t`: advance the deterministic generator to phase `t`; install current load and obstacle parameters; latch causal sensor/history state and the B01-sanitized `p_t`; select and latch action; integrate four substeps; record actual applied torque and solver impulses; compute `g_{t+1}` and `x_{t+1}`; advance the generator and pack the pre-action successor `p_{t+1}` for the next interval. The replay successor is the actual next pre-action context, with terminal/bootstrap semantics explicit. Never build `p_t` from the just-completed interval's reaction at `t+1`.

Retain the B01 slot manifest and `sample_time <= action_latch_time` checks. Exogenous phase, countdown, amplitude, and scheduled release may enter `F`; future endogenous contact/stop reactions may not. This proposal has no state-triggered release. Rule access to current privileged physics is training-only; `B` and the actor still receive only their declared inputs. Counterfactual actor-gradient calls hold causal `p_t` fixed while varying `a`.

Every completed episode emits a streamed certificate containing applied-load samples, target constancy, chronological validity, terminal flags, and measured velocities/errors. Verify applied `tau_ext` equals schedule within `1e-6 S`, release magnitude is at least `0.25S`, and no target changes occur in E3/E4. A crash, nonfinite state, or safety termination before the required windows is a **failed attempt**, not a completed episode or valid witness. The state machine guarantees opportunities conditional on physical execution; it cannot guarantee their completion after a simulator failure. Fail the readiness gate instead of synthesizing missing steps or relabeling a short trajectory. This closes the scheduling mechanism in Issue #1; §3 separately closes Issue #5.

## 2. Rule Calibration Wiring, Normalizer Contract, and Anti-Saturation Actor Loss

### P0 and the actual action source

Replace the legacy warmup dispatch with an explicit controller enum. `collector_mode=RULE` must call `rule_calibration`; missing helper/import/configuration raises an error, with no fallback. P0 is one complete 20-episode cycle over all configurations: **230,400 executed transitions**, streamed into a fixed **32,768-row** rule partition. Executed transitions are not resident transitions. The former `P0=800` cannot satisfy this proposal's coverage contract.

For error `e=q_ref-q`, use `kp=64 s^-2`, `kd=16 s^-1`, `ki=32 s^-3`, and the manifest's nominal joint inertia `J_nom`:

\[
\hat\tau_{bias,t}=-G(q_t)-\tau_{ext,t}-\hat\tau_{contact,t}^{past},\qquad
v_t=\hat\tau_{bias,t}+J_{nom}(64e_t+16(\dot q_{ref,t}-\dot q_t))+I_t,
\]
\[
u_t=\operatorname{clip}(v_t/S,-1,1).
\]

The contact estimate is the previous completed interval's generalized contact torque, zero at reset. Gravity/current exogenous load are known from the causal training plant; compensation does not require a future solver force. The rule has no access to future reactions. Send exactly `S*u_t` through the actuator path and audit the resulting applied action.

After action selection, update

\[
I_{t+1}=\begin{cases}
I_t,& |v_t|\ge S\ \text{or}\ \min(d_{min,t},d_{max,t})\le m,\\
\operatorname{clip}(I_t+0.02 J_{nom}32e_t,-0.15S,0.15S),&\text{otherwise}.
\end{cases}
\]

Reset `I=0` at episode reset. Do not reset the integral secretly at E4 release or alter the physical disturbance based on controller error. The anti-windup decision uses the preclip torque; checking a floating-point equality after clipping is unnecessary. Log bandwidth coefficients, inertia, bias, integral, preclip and applied torque. Validate the rule using the same physical panels as the actor; an analytically reasonable gain choice is not evidence that it passes.

After P0, complete one identical scene cycle with the actor to initialize the policy partition; rule transitions cannot count as policy transitions. Thereafter alternate two full policy episodes and one full rule episode, each source advancing its own allocation sequence. The rule partition is refreshed during learning, including higher lambda tiers on later cycles. A source tag records the **actual action-producing controller**. No cached rule actions are relabeled as actor rollouts, and evaluation never updates replay or training statistics.

### Resident quotas, protected windows, and sampling

Allocate source/scene capacities by largest remainder using rational weights `(4,3,4,3,6)/20`, tie-breaking by smaller scene ID. Then distribute each scene's capacity over 144 cells: `q_s(c,e)=floor(N_s(e)/144)+1[c < N_s(e) mod 144]`. The exact numbers are:

| Source | E0 | E1 | E2 | E3 | E4 | Total |
|---|---:|---:|---:|---:|---:|---:|
| Rule scene rows | 6,554 | 4,915 | 6,554 | 4,915 | 9,830 | **32,768** |
| Rule rows per cell | 45–46 | 34–35 | 45–46 | 34–35 | 68–69 | |
| Policy scene rows | 13,107 | 9,831 | 13,107 | 9,830 | 19,661 | **65,536** |
| Policy rows per cell | 91–92 | 68–69 | 91–92 | 68–69 | 136–137 | |

Rounding in the finite replay is explicit; exact percentages apply to complete executed cycles and the sampler's reference weights. A single global FIFO is forbidden. Use 720 independent, fixed-capacity cells in each source partition. Keep a protected E3 block `[40,65)` (25 rows) and E4 block `[15,65)` (50 rows, including 25 loaded intervals, the release edge, and 25 recovery intervals) within each cell. These fit even the smallest rule quotas. The rule's protected block is replaced only by a complete newer block that passes the physical success predicate in §3; before the first successful block, preserve the latest complete attempted block and mark success false. Policy blocks preserve latest complete exposure irrespective of success; actor competence is measured separately.

The remaining slots use a deterministic per-cell FIFO of other executed transitions. Until the first protected block is complete, its slots are reserved and invalid. Buffer only one pending block in a reusable 80-row scratch area, then commit the block and its certificate together. No partially overwritten window is ever valid. For cells larger than one episode, subsequent episodes fill the remaining slots; the initial 20-episode cycle supplies at least 240 transitions per cell, exceeding every quota. Record `episode_id` and `t` so chronological scans cannot join different episodes. Resident counts decrease on invalidation/eviction; lifetime counts are distinct diagnostics and cannot substitute for residency.

Sample minibatches of 240: 80 rule and 160 policy, respectively `(16,12,16,12,24)` and `(32,24,32,24,48)` per scene. Cycle balanced configuration permutations within each source/scene, and sample uniformly among valid cell rows. Thus the intended measure is `P(source)=(1/3,2/3)`, `P(scene)=(.20,.15,.20,.15,.30)`, `P(config|source,scene)=1/144`, independent of rounded cell capacity. Do not start learning while any required cell is empty. The same weighting applies to `B` covariance regularization; this avoids introducing another unstratified sub-batch while working on B02, without claiming independent resolution of the broader Issue #7 audit.

### A single, frozen coordinate system

Store raw calibrated FP32 fields, never pre-normalized rows. Disable rollout-time running-stat updates and batch-dependent normalization on actor/encoder inputs. LayerNorm inside the frozen architecture remains unchanged. After both initial partitions are full, perform one streaming, balanced moment pass with the sampler's reference measure. For every field vector `y`, compute

\[
\mu_y=\sum_{s,e,c}w_{sec}\,\overline y_{sec},\quad
\sigma_y^2=\sum_{s,e,c}w_{sec}\,\overline{y^2}_{sec}-\mu_y^2,
\quad w_{sec}=P(s)P(e)/144.
\]

Use FP64 accumulators only for these small statistics, then store FP32 transforms. A cell mean includes all its valid rows with equal conditional weight. For continuous coordinates use `(y-mu)/sqrt(max(var,1e-6))` in canonical units; discrete masks, one-hots, and trigonometric coordinates retain documented identity transforms. All B01-masked privileged slots remain exactly zero with frozen `(mu,sigma)=(0,1)` and are excluded from estimated moments. Fit shared physical coordinates jointly where they occur in both `x` and `g`, so duplicated angle/velocity/tip fields have one transform. Use the same `g` transform for observed outcomes and desired targets.

Freeze this **single version** for the entire spike, including both sources, online and target networks, and evaluation/export. During initial policy-buffer filling, the untrained actor uses a fixed identity transform; once moments are sealed, initialize the trainable run and copy all target networks under the sealed transform. These initial raw policy transitions remain valid off-policy data. No optimization or readiness assertion occurs during provisional preprocessing.

Later distribution change is logged as out-of-reference feature rates; it does not silently update one source's coordinates. A new normalizer requires a separately versioned run and all-network reinitialization/revalidation, not an in-place policy-only update. This removes the **normalization-induced** rule/policy shift in Issue #6. It does not pretend the underlying rule and policy occupancy distributions are identical, or that all future policies stay in initial support.

### Direct pre-activation recovery from saturation

Let `h_theta(x,z)` be the scalar actor logit, `a=tanh(h)`, and `h0=atanh(0.95)=1.831780823`. Add the direct logit loss

\[
L_\pi=-\mathbb E[\min_i F_i(x,p,\tanh h,z)^Tz]
+0.01\,\mathbb E[\max(|h|-h_0,0)^2]
+0.10\,\mathbb E_{rule,hold}[(h-h_r)^2],
\]
\[
h_r=\operatorname{atanh}(\operatorname{clip}(u_{rule},-0.98,0.98)).
\]

The last term uses only certified static E0/E3/E4 rule witnesses, with `z=stop_gradient(B(g_hold(q*)))` from their fixed desired target. Do not pair a rule action with an unrelated random latent. Recompute these latents with the current encoder and sealed transform. Rule target actions and encoder outputs are detached for this auxiliary actor term. Critic gradients reach the actor through action only, with causal privileged context held fixed. The main actor term retains the program's latent sampling outside these supervised anchors.

Above `h0`, the penalty's logit derivative is `0.02 sign(h)(|h|-h0)`, which bypasses `sech^2(h)`; supervised logit error likewise bypasses the output squash. At `|a|=0.92`, `sech^2(h)=1-0.92^2=0.1536` and the saturation penalty is zero. Therefore the regularizer does not penalize the registered heavy-load equilibrium. It is a soft penalty, not an action cap: actions above `0.95` remain possible. This addresses Issue #8's gradient path but does not prove actor convergence, prevent all hidden-layer gradient failures, or guarantee recovery for a physically infeasible load. Log `Pr(|a|>.99)`, logit quantiles, direct-logit gradient norms, and post-release recovery.

### Memory and implementation binding

The transition count is fixed at **98,304**, split exactly as above. No full-rollout tensors, normalized replay copies, replacement-buffer clones, or full-batch privileged-device caches are allowed. Stream episode certificates and evaluation traces to disk.

A dense illustrative row `(x137,p5065,a1,g_next13,x_next137,p_next5065,discount1)` contains 10,419 FP32 numbers; 98,304 rows cost **4,096,917,504 bytes**, before metadata and training workspaces. This matches the inherited approximately 4.097 GB replay measurement but cannot, by itself, establish a stricter **all-tensors** 4.10 GB limit. This proposal treats 4.10 GB as decimal bytes and enforces the stronger aggregate cap rather than hiding that distinction.

Use lossless static-field factoring: the schema preflight identifies **512 privileged slots** that are either immutable functions of the frozen configuration or B01-required constant masked slots. Store them once per configuration and reconstruct them in both `p_t` and `p_next` at minibatch assembly. Dynamic thermal/drive scales, contacts, generator phase, and history are ineligible. The slot list must be justified by field provenance and checked for exact equality on rollouts; “appears constant in a short sample” is insufficient. The remaining privileged slots stay CPU FP32. Logical dimensions remain 5,065, and all 98,304 logical transitions remain available.

This layout costs **3,694,559,232 bytes** for the logical dense schema after factoring, including `144*512*4` bytes for the shared table. Reserve at most 8,000,000 bytes for typed resident metadata and 350,000,000 bytes for **all** other live tensors: models/targets/gradients/optimizer state, moment accumulators, scratch windows, and batches. The aggregate ceiling is **4,052,559,232 bytes**, leaving about 47.4 MB under 4.10 GB. Minibatches are assembled and backpropagated in microbatches of at most 16, with loss weights preserving the 240-example objective; avoid optimizer implementations with large transient tensor copies. Serialize checkpoints in streams rather than cloning tensors.

The baseline does not reveal individual privileged slot widths or which 512 are immutable. Therefore the slot audit is a required implementation-binding check, **not a claim that this optimization has already been verified**. If fewer than 512 eligible slots exist, or actual allocated tensors exceed 4.10 GB, report MEMORY_LAYOUT_BLOCKED and do not run this design under an assumed exemption. Never quantize dynamic replay, reduce the row count, silently use FP16, or mask valid information to meet the cap. Separately require measured process-tree peak RSS **<=4.694 GB**, one run at a time. Both allocator accounting and RSS include evaluation and checkpoint peaks. The audit may discover a smaller native schema that already satisfies both limits; it must demonstrate the byte accounting before using that layout.

## 3. Frozen Static-Holding Evaluation and 720-Cell Cross-Coverage Gate

### Exact equilibrium target and measured panel

Freeze the baseline's canonical 13-field layout; do not activate an effort/margin substitution variant in this packet. With the parent/housing fixed and calibrated forward kinematics `f_D^M(q)` using the actual geometry, define

\[
\boxed{g_{13}^{hold}(q^*)=
[\cos q^*,\sin q^*,\underbrace{0}_{\dot q},\underbrace{0}_{\widehat{\ddot q}},
f_D^M(q^*)_x,f_D^M(q^*)_y,f_D^M(q^*)_z,
\underbrace{0,0,0}_{v_{tip}^M},\underbrace{0,0,0}_{\widehat a_{tip}^M}]^T.}
\]

For a planar calibrated housing this is equivalently `p_joint^M + R_axis(q*) r_tip,D`, with the manifest's calibrated axis and tip vector; assuming an arbitrary global Cartesian orientation is unnecessary. This is a desired outcome, never a replacement for measured `g_next`. Estimate actual accelerations causally with the existing five-point fit. Form `z*=B(normalize(g_hold))` once per evaluation episode and hold it fixed with a frozen checkpoint/encoder. The actor uses only `x137,z*` and has no teacher correction during evaluation.

Run all `144 x 3 anchors x 2 signs x 3 lambda tiers x 3 scenes = 7,776` static episodes for each evaluated controller/checkpoint. In this panel signs are explicitly both `-1,+1`, with `A=-G(q*)-sigma lambda S`; if `|A|<0.15S`, increase `|A|` to `0.15S` in its existing sign (zero uses `sigma`), provided the loaded equilibrium remains within `0.95S`. If that fails, flag an infeasible panel case and fail; no case is omitted. Store the resulting amplitudes before any actor evaluation. E0 repeats the same anchors under these paired case IDs with zero external torque. This redundant pairing gives matched initial conditions and case counts.

Use §1's E3/E4 torque schedules but override **all reference generators with the same static target for all 80 intervals**. E0 is static as well. Auxiliary E1/E2 panels can retain their operational commands, but they never contaminate `zero_vel_rmse`. A target-hash assertion fails if a moving reference or perturbation leaks into the static panel.

For each case, compute velocity RMSE over E0 `[40,80)`, E3 `[40,80)`, E4 `[60,80)`, using physical `qdot_{t+1}` in rad/s. Publish E4 whole-recovery `[40,80)` RMSE and peak speed separately; late recovery does not conceal the transient. Define aggregate `zero_vel_rmse` as the square root of the equally weighted mean of case mean-squared errors, not the mean of their roots. **Every case**, every `(configuration,scene)` aggregate, every scene aggregate, and the full aggregate must have RMSE **strictly <0.35 rad/s**. Aborted/nonfinite cases fail regardless of the mean over remaining cases.

Also require each scored window to have position-error RMS `<=0.02R` and peak `<=0.05R`, no stop contact, and no obstacle contact. Velocity zero at a wrong angle or against a stop is not holding. For E4 require a contiguous 20-interval suffix after release with `|qdot|<0.35 rad/s` and `|q-q*|<=0.02R`; it must occur by interval 79. Frozen test manifests and hashes precede training, and evaluation RNG/state is separate from collection.

### Count semantics and hard readiness predicate

Maintain `cross_coverage_144_x_5` as an explicit 144-by-5 integer array of **currently resident valid transitions**, with equally shaped `rule` and `policy` component arrays, allocation quotas, and a separate lifetime-executed array. Validate array shape, exact configuration labels, checksums, and `total=rule+policy`. Any missing cell, absent field, stale certificate, or invalid configuration fails closed; a scene marginal never repairs it.

An E3 successful rule witness is a single complete 25-interval `[40,65)` block with constant physical load `|tau_ext|>=0.15S`, constant target, velocity RMS `<0.35`, position RMS `<=0.02R`, peak position error `<=0.05R`, and no termination/stop/obstacle contact. An E4 successful rule witness uses retained `[15,65)`: 25 loaded intervals, the applied edge at 40, 25 post-release intervals with no reloading, and success on the final 20 `[45,65)` intervals with pointwise `|qdot|<0.35` and `|q-q*|<=0.02R`. This rule-replay anchor criterion is intentionally earlier than the final actor-panel suffix, and may fail independently. Count at most **one protected successful witness per configuration** in the current replay; overlapping windows cannot inflate counts. Thus proposed minima are `sustained_load_hold_count=144` and `post_load_recovery_count=144`, each with all 144 per-configuration bits true.

For the E1 physical rule panel, run both stops for each configuration (288 trials), using the E1 target schedule. A success moves at least `m` inward by interval 59, stays at least `m` inside both stops on `[60,80)`, and has no stop-contact reentry in that suffix. Require **288/288** successes, `limit_escape_rate=1.0`; publish actor E1 performance separately. For E2, require at least one actually measured obstacle angular impulse with magnitude `>1e-6 S * 0.02 s`, followed by separation in **each** of the 144 configuration cells and in both compliant/rigid variants. Separation means angular clearance `>=0.005R` and zero active obstacle constraint for at least ten consecutive intervals before the end. A label alone does not satisfy contact coverage.

Define exactly:

```text
resident_ok = for every c,e:
    rule[c,e] == q_rule(c,e) and policy[c,e] == q_policy(c,e)
    and cross_coverage_144_x_5[c,e] == rule[c,e] + policy[c,e]
exposure_ok = every scheduled E3/E4 attempt has a valid schedule certificate
              and every cell has completed physical episodes
anchors_ok = sustained_load_hold_count == 144
             and post_load_recovery_count == 144
             and all corresponding per-config success bits
physical_ok = limit_escape_rate == 1.0 and E2_contact_and_release_cells == 144
              and both E2 material-variant matrices are complete
integrity_ok = causal_schema_ok and target_static_ok and normalizer_version_ok
               and source_dispatch_ok and resume_ok and memory_ok
actor_hold_ok = all static-panel cases pass the RMSE, position, and recovery gates
coverage_ready = resident_ok and exposure_ok and anchors_ok and physical_ok
                 and integrity_ok and actor_hold_ok
```

Use source-qualified names as well as the legacy counter names so rule competence cannot masquerade as actor competence. Exposure counts, successful witness counts, and frozen actor evaluation are three different artifacts. Rule-panel failure and actor-panel failure are both visible. No upward-latched flag survives eviction, checkpoint change, normalizer change, or invalidated provenance; recompute at every evaluation. Structural closure is guaranteed once the scheduled valid transitions are collected and retained; **full `coverage_ready=true` is an empirical conjunction**, not a theorem about neural optimization.

## 4. Serious Alternative Considered and Rejected

The serious alternative is a deficit-weighted stochastic collector, a global source-specific reservoir, and continuously updated importance-weighted normalizers. It can preserve the reference distribution in expectation, adapt to a changing policy, and use memory efficiently without fixed cell partitions. It is appropriate when probabilistic coverage and moving coordinates are acceptable.

I reject it for this packet's deterministic finite-capacity contract. With independent scene/configuration draws, a rare cell has positive probability of no visits after any finite number `n`: `(1-p_cell)^n > 0`. More importantly, separately correct row and column totals do not imply positive entries in the joint matrix. A 2-by-2 submatrix with counts `[[k,0],[0,k]]` has identical positive marginals to `[[k/2,k/2],[k/2,k/2]]` but lacks two pairs. Reservoir replacement can also evict the only release boundary even after lifetime coverage passed. Deficit scheduling could eliminate these failures if supplemented with hard per-cell minima and window protection, but then it supplies the functional mechanisms adopted here; the rejection does not establish that this particular array layout is uniquely necessary.

Importance-weighted adaptive moments are a stronger alternative than policy-only moments and are not mathematically wrong. They nevertheless change the coordinates of all old rule anchors as the policy distribution changes. Maintaining function-preserving transformations across nonlinear encoders, their targets, optimizer state, and desired-goal encoding is additional work that a short B02 spike would have to validate. A single sealed balanced transform removes that confound at the cost of less adaptation to later distribution drift. A later version can test adaptive normalization with explicit coordinate-consistency checks.

I also reject action-space behavior cloning alone as the saturation fix: differentiating `(tanh(h)-u_rule)^2` retains the vanishing `sech^2(h)` factor precisely where recovery is needed. A direct logit penalty is an explicit alternative gradient path. None of these arguments asserts that rule calibration, PD gains, or frozen normalization is universally necessary for control. Agreement on the brief's requested schedules and coverage gates is **framed agreement** under method §11.5, not independent evidence for necessity.

## 5. Candidate Necessity Claims (Appendix B)

### C-B02-P-01 — Marginal coverage cannot certify joint coverage

- **State/grade:** Candidate, Grade 1; proposed impossibility/information claim, not Locked.
- **Premises:** At least two configuration categories and two scene categories; a verifier sees only marginal nonnegative integer counts; success requires positive counts in every joint cell; no additional structural constraints rule out concentrated joint allocations.
- **Conclusion:** No verifier based only on those marginals can both accept all fully covered feasible matrices and reject all matrices with missing cells. Joint allocation information, or a verified allocation invariant with equivalent information, is required for such a sound and complete certificate.
- **Proof:** The two matrices in §4, with even positive `k`, have identical marginals and different coverage truth values. Embed them in a larger matrix with identical positive remaining cells. Any marginal-only verifier returns the same answer on both and is therefore wrong on at least one. A verifier that rejects everything is sound but fails the stated completeness requirement.
- **Scope/implementation independence:** Applies to neural, classical, and hand-scripted collectors. It requires information sufficient to distinguish joint allocations, not necessarily a dense 720-cell array. It does not prove that every successful controller must train on every cell.
- **Operational test:** Feed the verifier the paired matrices with `k=100`; the proposed joint verifier must accept the complete matrix and reject the sparse one despite equal marginals. Repeat after eviction of a protected cell's last valid row.
- **Falsifier:** A marginal-only verifier that distinguishes both inputs under exactly these premises, or proof that an added allocation invariant forbids the sparse input. The latter narrows the premises rather than defeating the unconstrained result.
- **Upgrade/violation record:** Proof supplied here, no independent verification yet; zero scope narrowings; no known counterexample under the stated premises. Promotion requires independent proof verification and human-lead signature under Appendix B.9, not a spike score. No veto authority is claimed.

### C-B02-P-02 — A uniformly bounded action derivative cannot prevent squash-gradient decay

- **State/grade:** Candidate, Grade 1; lower-bound/impossibility statement about one gradient path.
- **Premises:** Scalar `a=tanh(h)`; differentiable objective `Q(a)` with `|dQ/da|<=M<infinity`; gradients reach `h` solely through this action, without direct logit regularization or another path.
- **Conclusion/proof:** `|dQ/dh|<=M sech^2(h)<=4M exp(-2|h|)`, which tends to zero as `|h|` grows. No uniform positive lower bound on the magnitude of that gradient path is possible on unbounded logits.
- **Implementation independence:** Applies to any differentiable controller using this squash/path, not only the specified actor. It makes no necessity claim for one particular penalty, nor for bounded logits in architectures with alternative gradient paths.
- **Operational test:** Use `Q(a)=a`, logits `0,2,4,8`, and check the derivative against `sech^2(h)`; then enable the proposed direct penalty and verify its nonzero analytic derivative at `h=8`.
- **Falsifier:** A derivative exceeding the bound while all premises hold; an unbounded critic derivative or additional loss path instead violates a premise and must be reported as such.
- **Upgrade/violation record:** Analytic argument only; no independently checked proof, zero scope narrowings, no recorded empirical claim. Remains Candidate pending Appendix B.9 adjudication/signature. Superior RMSE would establish sufficiency of the implementation, not necessity of its wiring.

These records are proposed here for later claim-file extraction by the authorized workflow. They do not modify the program ledger or claim lifecycle.

## 6. Pre-Registered Empirical Spike Protocol

### Scope, manifests, and fixed attempt budget

Proposed spike ID: **B02-B-SYNC-HOLD-v1**. This section is the author's pre-registration proposal; the orchestrator must seal the executable PLAN and implementation manifest before an experiment runner executes it. No experiment has been run for this draft. In particular, the prior B01 CPU result is not B02 evidence.

Use seeds **2301, 2302, 2303**, all 144 configurations, and the fixed schedules/panels above. Freeze configuration hashes, field manifest, factored-slot audit, evaluation targets/amplitudes, normalizer rules, code revision, simulator solver settings, and the selected native FB objective before running. The frozen context does not specify that objective's optimizer hyperparameters, so the executable binding must record the existing baseline values and hashes rather than inventing a claimed repository command. A missing binding is BLOCKED before execution, not discretion to tune during the run.

Run five arms, sequentially under the same memory cap:

| Arm | Change from the full proposal | Intended discriminating result |
|---|---|---|
| FULL | All proposed mechanisms | All structural and empirical gates pass. |
| SHORT-LOAD | Set E3 full-load duration to 10 intervals; E4 release to 70, leaving only 10 recovery intervals | Schedule validator and witness gates must fail even with correct scene labels. A positive result is a validator bug. |
| LEGACY-RULE | Replace rule dispatch with the existing legacy warmup controller; preserve schedules/quotas | Measures the contribution of calibrated bias and inertia-scaled feedback. Source audit identifies the substitution; report physical metrics even though this control is ineligible for readiness. |
| POLICY-NORM | Restore policy-only running moments with the same initial transform | Measures coordinate drift and rule-anchor errors; intended integrity gate fails, while physical performance is still reported. |
| NO-LOGIT | Set both added logit-loss coefficients to zero | Measures saturation frequency, gradient behavior, and heavy-load/release performance. Do not predict failure as a logical necessity. |

Run the structural checks once per arm/seed and the learning comparison for FULL, LEGACY-RULE, POLICY-NORM, and NO-LOGIT; SHORT-LOAD requires no neural training after its expected rejection. Keep actor initialization, environment case IDs, and update budget paired. The changed behavior controller naturally changes physical states; do not pretend replay can be held identical for that intervention. These are mechanism tests, not an exhaustive factorial attribution study.

Maximum learning budget per learning arm/seed: initial **230,400 rule + 230,400 policy** executed transitions, then **4,608,000** further executed transitions and **20,000** gradient updates. After each group of two policy episodes and one rule episode, add 25 to an integer update accumulator and execute `accumulator // 24` updates, retaining `accumulator mod 24`. Thus 19,200 complete groups reach both limits together. No online updates are inserted during diagnostic evaluation. Evaluate at update 0, 5,000, 10,000, and 20,000, if reached; **checkpoint 20,000** determines success, not the best intermediate checkpoint. Earlier stopping for resource exhaustion is INCOMPLETE, even if an intermediate panel passes. Replay remains 98,304 rows throughout. One numerical attempt per arm/seed; resume after interruption is permitted only with identical saved state. Infrastructure repair is logged and cannot erase a failed numerical attempt.

### Stage A: executable structural rejection tests

Before expensive learning, verify exact per-cycle scene counts, all 720 cells and quota totals, every E3/E4 schedule boundary, actual controller call counts/actions, static target hashes, chronological windows, and protected-window eviction behavior. Inject one missing cell with unchanged marginals: `coverage_ready` must turn false. Inject one corrupted source tag, one stale normalizer version, one action-dependent future reaction in `p`, and one interrupted E4 window: each must fail the corresponding check. These small deliberate faults must not enter the training run.

Run actual physics for one complete rule cycle and the initial policy cycle; compute measured success bits without substituting scheduled opportunities. A valid static scheduler with failed physical hold is **structural pass / control fail**, never a full pass. Run the 288 E1 and paired E2 checks as specified. Snapshot midway through an E4 episode and restore once; require identical schedule/cell metadata and `resume_diff_norm=0.0` for the next 100 transitions and next optimizer update under the same device/runtime. Report device-specific determinism separately; do not infer CPU/GPU bitwise parity.

For the saturation unit intervention, initialize actor output bias to `+8` and then `-8` with other parameters fixed, use the analytic `Q(a)=a` control, and check the two derivatives from Claim 02 within `1e-6` absolute error in FP32. This confirms the gradient path only; physical recovery must still pass the rollout panel. Check rule-only and policy-only batch ordering produces identical sealed statistics and transformed raw rows within `1e-6` absolute error.

### Stage B: quantitative pass rules and reporting

For **each of all three FULL seeds**, require at the last checkpoint:

1. All **720/720** resident cells satisfy their exact source quotas; totals are **32,768**, **65,536**, and **98,304**. All E3/E4 schedule certificates pass; missing field or aborted required episode is failure.
2. `sustained_load_hold_count == 144`, `post_load_recovery_count == 144`, every per-configuration success bit true, E1 **288/288** successful, and E2 **144/144** cells successful in both material variants.
3. Every frozen actor case and aggregate has **zero-velocity RMSE <0.35 rad/s**, with the position/contact/recovery constraints of §3. Publish rule-controller panel results separately under the same thresholds.
4. `coverage_ready == true`, and every conjunct in §3 is present and true. SHORT-LOAD and the synthetic missing-cell case must produce false readiness, independently of actor scores.
5. Resident transitions never exceed **98,304**, aggregate live tensors never exceed **4,100,000,000 bytes**, and peak process-tree RSS never exceeds **4,694,000,000 bytes**. Hash/provenance, deployment purity, normalizer consistency, and resume checks all pass.

Report per-case and per-cell data, worst-case RMSE, scene aggregates, capacity-tier breakdowns, exposure/success counts, saturation fractions, training updates, actual physics transitions, device, elapsed time, peak tensor allocation, RSS, and all attempt outcomes. Report ablation differences and their three paired-seed values without upgrading observed differences to necessity claims. If FULL and an ablation both pass, the proposed addition may be unnecessary for this spike despite its plausible mechanism.

The proposed runner output consists of immutable manifests plus `episodes.jsonl`, `cell_coverage.json`, `static_panel.jsonl`, `normalizer.json`, `memory.json`, `runs.log`, and a machine-computed `VERDICT.json` carrying `PASS`, `FAIL`, `INCOMPLETE`, or `BLOCKED`, reason codes, and all readiness conjuncts. The executor writes these only in its authorized spike directory after sealing the plan. This author writes only this proposal.

### CPU-honest execution and stopping

Probe CUDA in the future runner and record the result. CPU FP32 execution is valid, including full-network training if it completes within the registered resources; a toy surrogate cannot stand in for the specified actor/critics. Use a **24-hour wall-clock cap per arm/seed** and the same transition/update limits. If CPU time permits only structural checks, report them and mark the full spike **INCOMPLETE** with learned-policy gates false or unevaluated. Do not call the old 101-update smoke test converged control, infer missing cases from a small CPU subset, or print `coverage_ready=true` from synthetic certificates. A future accelerated rerun uses the same manifests and registers a fresh execution record; unfinished CPU evidence remains visible.

The proposal is falsified as a sufficient B02 closure if a feasible FULL run completes its registered budget but fails any required gate. An infeasible configuration, unverified memory layout, missing simulator binding, or unfinished CPU run is an explicit blocking limitation, not evidence of successful closure and not permission to alter the thresholds after seeing outcomes.
