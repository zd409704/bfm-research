# Framework Review — Author A (feedback-round-2026-10-24)

**Program**: `fb-beyond-imitation-acceleration`
**Scope**: Independent critique of the corrected mainline in `briefs/OWNER_FEEDBACK_EN.md`. Each link of the owner's causal chain is split into three layers: **(T) theory holds**, **(I) implementation matches theory**, **(E) empirical benefit shown**.
**Evidence rule**: B01–B05 script and GPU PASS results are treated as unit or contract checks on artificial data (see `CORRECTED_CONCLUSIONS.md`). None of them counts as evidence for any (E) cell below. Production code is outside this tree. Its behavior is taken only from the owner audit, plus `baseline/02` and `baseline/05`. A grep of this tree finds no `FBAgent`, `TaskLearner`, or `CandidateProvider` implementation (the one hit is a draft sketch, `packets/B02/drafts/A/spike_sketch.py`). The toy modules in `gpu_experiments/fb_core.py` are not the production modules.

---

## 0. Verdict up front

**Judgment: REVISE-THEN-CONTINUE, at bounded small scale. Do not invest at full scale yet.**

- The architecture is theoretically coherent as a hierarchical design. It has a reward-agnostic, off-policy, relabeled body layer and a macro-level task layer.
- It has one real and checkable route to better experience utilization: FB relabeling trains a whole family of conditional policies from every real transition, including failures, while macro-K cuts the task credit horizon about 10×.
- It also has one load-bearing assumption with no evidence for it in real physics: that z is a *controllable* index of distinct, stabilized, task-useful closed-loop behaviors on the production humanoid.
- The current implementation also lacks a mechanism the owner's story depends on. There is no planner-z exploration. The planner executes deterministic means, so "z organizes exploration" is today only "demo-anchored expert/near prompts organize exploration".

Continued investment is justified only if a short controllability gate (E0) and one sample-efficiency comparison against direct-action task RL (E1) pass the thresholds pre-registered in `MINIMAL_EXPERIMENTS.md`. Decisive assumptions and kill criteria are in §9.

---

## 1. The causal chain, link by link

Chain: **body experience → conditional behaviors → z organizes exploration → new transitions expand body skill → planner uses new skill for task → experience serves later goals.**

| Link | (T) Theory holds? | (I) Implementation matches? | (E) Empirical benefit shown? |
|---|---|---|---|
| L1 body experience → conditional behaviors π_z | **Conditionally.** FB fits successor measures of π_z on the replay distribution ρ, and the actor ascends `F(o,a,z)^T z`. So π_z targets the reward `r(m)=B(m)^T Σ_B^{-1} z` ("reach/occupy kinematic features in the z direction"). This needs: near-Markov `o`, ρ coverage of the relevant (s,a), adequate rank/capacity, and an actor good across a *continuum* of z. | **Mostly.** Per the owner audit, `FBAgent.update` is reward-free, uses the 50/50 `z_update` mixture, and the FB replay is unfiltered. This matches FB theory. | **None.** No production measurement that π_z for a demo or near z actually moves the robot toward the cued kinematics. |
| L2 conditional behaviors → z organizes exploration | **Plausible, not implied.** Holding z for K steps runs a closed-loop policy that is optimal for *some* reward, so exploration is temporally coherent and (if L1 holds) stabilized. Nothing guarantees that nearby z gives nearby contact behavior (owner note; F is not shown Lipschitz in z on contact sets). | **Partial.** The exploration sources are the expert frame, near (10–20° tangent), and planner. The planner emits a deterministic z through the actor `.loc` mean, with **no planner-z noise**. Training RNGs (z_update, target smoothing) are not executed exploration. | **None.** The near ablation has never been run on real training. |
| L3 new transitions → expand body skill | **Yes, in the reward-free sense.** Newly reached m_next enter the 50% goal relabel, so new postures become trainable goals (HER-like). | **Yes, with a retention caveat.** The FB replay is a finite circular buffer, so old skill data is evicted. Retention lives in weights, with no guarantee against forgetting. | **None.** No measurement of the replay-coverage growth or of the controllable-goal set over time. |
| L4 planner uses new skill for task | **Weakest link.** The planner can exploit skill z* only if `Q_task(H,c,z)` is accurate near z*. That requires *executed* macros near z* with observed returns. `Q_task` is non-linear in z, and its ∇_z away from executed data is extrapolation (C-B02-A-03 already shows ∇_z Q is pure critic error without controllability). | **Gap.** Skills trained only through the random-sphere half of z_update are never executed in the environment unless the deterministic planner happens to emit them. Task-value evidence near the planner's own outputs comes only from its noise-free trajectory. | **None.** |
| L5 experience serves later goals | **Plausible.** Reward-free FB uses low-task-return transitions, and these can carry recovery or other-height behaviors. Negative transfer and capacity costs are real (§7). | **Data path exists** (FB replay is not filtered by task return). **Retention is not promised.** The circular FB replay and the separate task-replay age/height rules mean "retained" is undefined until measured. | **None.** The three retention senses (readable / executable / findable) have never been measured. |

**Net:** (T) is coherent for L1, L3, L5 and plausible for L2, but weak for L4 under the current exploration design. (I) has one material omission (planner-z exploration) and one undefined property (retention). (E) is empty for every link.

---

## 2. FB theory applicability bounds (what FB theory does and does not license here)

1. **Linear readout scope.** `w_r = E[B(m) r(m)]` and `Q ≈ F^T w_r` are exact only for rewards in the span of B, under a fixed π_z, at the FB fixed point. B is motion-only and root-relative, with no obstacle geometry, x/y/yaw progress, or contact. The traversal reward depends on box-relative position, clearance, contact release, and landing support (baseline/05 §5.1), so it is **not** in the span. Zero-shot FB readout is therefore *not* a task solver here, and the separate task Q is necessary, not optional. The design already reflects this, correctly.
2. **What FB contributes, then.** FB provides a parameterized *family of closed-loop policies* {π_z} plus a reward-free training signal that reuses every transition across all z. The framework stands or falls on whether this family, switched every K steps, contains a near-optimal traversal policy (§3). FB theory says nothing about that.
3. **z is not a smooth control knob.** Linearity in w_r does not make task success, `Q_task(H,z)`, or contact outcomes linear or smooth in z. Changing z changes F and the future occupancy. Arguments based on inner-product smoothness of z do not carry over to contact behavior.
4. **Dynamic frames.** A single frame m includes q̇ and root velocity. For a mid-transit frame (e.g., mid-climb), "maximize discounted occupancy of B(m)" can be best achieved by a cyclic or oscillatory behavior, or by nothing reachable. The K-step prefix of π_{B(m)} need not resemble the demo transit through m. Expert cues are cues, not a tracking reference, and their behavioral semantics must be measured.
5. **Partial observability.** F and π use `o` without history, while P and Q use history. FB's Bellman fixed point assumes Markov `o`. The proprioceptive state plus scan is probably close enough for body control, but contact-regime aliasing (B03 Case I) is a known violation.
6. **First-action derivatives.** An accurate F already integrates long-horizon consequences, so the 1-step actor derivative does *not* mean "FB sees one step" (owner correction, agreed). The B04 toy cosine for H=0 reflects a briefly trained F on a toy plant, not a property of FB.
7. **No NN convergence proof.** This is not grounds for rejection (owner, agreed). The useful theory is about *necessary* conditions (coverage, controllability, label integrity), and those can be measured.

---

## 3. Is the body/task division sufficient?

**Sufficiency condition (checkable):** there exists a switching schedule z_1, z_2, … (every K=10 control steps, 0.2 s) over the learned {π_z} whose closed-loop traversal success is close to that of the best direct-action policy at the same observation access.

- **Arguments for.** Traversal can be broken into approach, takeoff, support, clearance, and landing. Each phase is largely a body-posture/velocity objective, conditioned on terrain that π can see through `scan`. A planner that sequences posture-velocity goals is a learned keyframe controller with *planner-chosen* keyframes. That is a well-understood and expressive HRL structure.
- **Arguments against.**
  - (a) Where hands or feet land on the box is decided by π from `scan`, not by z. If two placements share kinematics but differ in contact force, z cannot select between them (B03 Case I, theory only).
  - (b) The actor capacity spent on the random-sphere half of z_update buys behaviors that the task layer never tests.
  - (c) Demo cues form a 1-D curve (859 frames of one 0.70 m motion) in a 256-d sphere. Near spreads a thin tube around it. Planner-discoverable z is effectively *tube + Q extrapolation* (§4, L4).
- **Assessment.** The division is sufficient *in principle* for this task family. It is **not shown** for the learned family. The cheapest discriminating check is the controllability/branching probe E0 (`MINIMAL_EXPERIMENTS.md`), which can reuse the 128-latent same-state branching design already specified in `synthesis/B03-synthesis.md` Merge 2.

---

## 4. Cold start: virtuous loop vs skill/exploration deadlock

**Benign loop:** expert/near prompts → coherent body motion → diverse replay → better FB → more controllable π_z → planner finds task-useful z → higher-return data → curriculum unlock.

**Deadlock path (specific to this design):**
1. Early π_z is uncontrolled, so falls dominate replay.
2. The 50% goal relabel draws m_next from fall/ground states, so the body layer becomes good at reaching fall-like postures.
3. Task returns are near-uniform across z, so `∇_z Q_task` is critic noise (C-B02-A-03).
4. The planner is deterministic with no z noise, so its executed z does not explore its own neighborhood.
5. The planner share ramps to 0.70 by 100k steps *on a schedule* (baseline/05 §3.1), regardless of whether the body layer is controllable yet.
6. Replay then fills with deterministic-planner data around an uninformed z.

Step 5 is a design hazard: **the source schedule is time-based, not competence-based.**

**Escape mechanisms that exist:** low-height start {0.10, 0.20} m, potential-based dense reward, and expert/near prompts at 0.60/0.30 early.
**Escape mechanisms missing:** planner-z exploration; a competence gate on the source schedule; any deadlock detector.

**Measurable deadlock signature (pre-registered in E0):**
- the controllability ratio CR does not fall below 0.95 by 25% of the budget, **or**
- the upright-state fraction of the FB replay falls monotonically over the first 25% of the budget, **or**
- planner-source macro return is not above the uniform-random-z macro return by 25% of the budget.

---

## 5. Why z-space exploration *might* help (not from inner-product smoothness or dimension)

z_dim=256 is larger than action dim 29, so lower dimension cannot be the argument (owner, agreed). The candidate mechanisms, each conditional on L1 controllability:
1. **Temporal coherence with feedback.** A held z runs a *closed-loop* policy for K steps. Its deviations are correlated over 0.2 s and corrected by proprioceptive feedback. Independent per-step joint noise mostly produces high-frequency jitter or falls. The fair control is temporally correlated action noise (OU/pink-style held over K) at matched action variance. Without that arm, "z helps" cannot be told apart from "correlated noise helps".
2. **Exploration in the space of stabilized behaviors.** If π_z is trained to keep the body in reachable kinematic-occupancy patterns, then perturbing z perturbs *which* stabilized pattern runs, not whether the robot is stable.
3. **Relabeled reuse.** One real transition trains every z via the relabel. This is experience utilization rather than exploration, but it is the main efficiency lever.
4. **Shorter task credit horizon.** A 12 s episode is 600 control steps but 60 macro decisions.

The skeptic's null: mechanisms 1 and 4 can be reproduced without FB (correlated action noise; action repeat or option-style macro actions in direct-action RL). Only mechanisms 2 and 3 are FB-specific. E1 and E2 are designed to separate them.

---

## 6. Macro-K switching vs long-horizon conditional learning

- FB trains π_z as if z were held indefinitely (bootstrap through `F(s', π(s',z), z)` with the same z), with effective horizon about 1/(1−γ_FB). Execution holds z for K=10 steps and then switches.
- **Consistency of the task layer:** fine. Q_task learns the realized macro returns of the *switched* behavior from executed `z_actual`, and the variable-k discount (B02 Merge 4) handles early termination.
- **Body-layer optimality under switching:** not guaranteed. π_z's first K actions are optimal *if continued*. A "wind-up" prefix (e.g., crouch before a later jump) is wasted if the planner switches. This is a mismatch, not a contradiction. The planner can learn to exploit prefixes, but prefix usefulness is an empirical property.
- **Off-policy FB data:** the switched trajectories are valid off-policy data for FB, so the body layer itself is not corrupted by switching.
- **Check:** K ∈ {5, 10, 20} only *after* E1 (not in the minimal set), plus logging the within-macro progress of the kinematic goal distance in E0.

---

## 7. Joint-training drift vs off-policy tolerance; capacity and negative transfer

**Drift**
- From the planner's view, the low-level policy is part of the environment, and that environment changes as θ updates.
- A stored `(H, z_actual, R_macro, H')` describes an older π_θ (B02 §2.1, theory). B drift alone does not change a stored z vector's meaning to the actor, but actor drift does.
- So the macro task replay is **not** off-policy-safe in the usual sense. Its tolerance depends on the actor's drift rate per macro-replay age. The owner-confirmed short task replay with age/height rules is the right *kind* of mitigation, but its adequacy is unmeasured.
- **Check:** in E1, log TD error and realized-return calibration of Q_task as a function of replay age (in control steps), plus actor KL drift on a frozen probe set (B02 Merge 2 metric). The gate: Q calibration slope on fresh rollouts within [0.7, 1.3] in the second half of training.

**Capacity / negative transfer of "irrelevant" experience**
- The FB actor and F must cover all z on S^255 with a finite network. Unfiltered failure-heavy replay shifts ρ, changes the Gram, and pulls the goal-relabel distribution toward failure postures. That can lower F accuracy where the task operates.
- The benefit claim (failures teach recovery and other-height behaviors that later serve the task) and the cost claim are both plausible. They are separated *only* by a filtered-replay control arm (`MINIMAL_EXPERIMENTS.md` C-design).
- The circular buffer also means the data may be gone when the "later" goal arrives.
- **"Retained" has three separate senses that must be measured:**
  - (i) readable: the transition is still in a buffer
  - (ii) executable: π_{B(m)} still reaches m from relevant starts
  - (iii) findable: the planner, under 100% planner evaluation, still produces z that achieves the old task (e.g., the low-height regression panel already in baseline/05 §6.1)

---

## 8. Most promising benefit vs strongest objection

**Most promising benefit.**
- A reward-agnostic body layer turns **all** real experience, including low-task-return experience, into training signal for a reusable conditional controller, through off-policy relabeling.
- Meanwhile a macro-level task layer does credit assignment over about 60 decisions instead of about 600.
- Demonstrations act only as cues, so the system is free to go beyond them.
- This is a concrete and checkable experience-utilization claim, and it does not depend on dimension arguments.

**Strongest objection.**
- The task layer can only exploit behaviors that are (a) controllable through z in real contact physics and (b) *executed* near the planner's z so that Q_task is locally accurate.
- Neither is evidenced. (b) is structurally weakened by the absence of planner-z exploration and by a time-based source schedule.
- So the framework may collapse to "demo-anchored prompts + an off-policy task critic over a thin tube of z", at a higher per-sample cost (six networks, relabeling, recurrent burn-in) than direct-action off-policy task RL with correlated noise and action repeat. That simpler baseline captures mechanisms 1 and 4 of §5 at much lower complexity.

---

## 9. Value judgment and decisive assumptions

**Conclusion: REVISE-THEN-CONTINUE (bounded, small-scale first).** This is not "support": no (E) cell is filled. It is not "do-not-continue": the theory is coherent, the needed checks are cheap compared with full production training, and the failure modes are detectable early.

| ID | Decisive assumption | If false → | Check |
|---|---|---|---|
| D1 | **Controllability**: in real physics, π_z for demo or replay-goal z moves the body toward the cued kinematics clearly better than a mismatched z (CR ≤ 0.80 by 50% of the E1 budget). | Body layer is not a skill library; the chain breaks at L1/L2 → **stop** or redesign the body objective. | E0 |
| D2 | **Framework efficiency**: the framework reaches the traversal threshold at ≤ 0.67× the steps of the best direct-action task-RL baseline (median, ≥4/5 seeds). | No efficiency case under the corrected mainline → **small-scale-only / do-not-continue** at production scale. | E1 |
| D3 | **z-exploration specificity**: z-space exploration beats matched temporally correlated action noise. | The FB-specific exploration claim is dropped; keep the framework only if D2 holds through relabeled reuse. | E2 (staged) |

**Revisions required before E1 (minimal, all instrumentation or one exploration knob — no new losses):**
1. Log executed z with a per-source tag, separate from training RNG draws.
2. Add an *optional* planner-z exploration knob (tangent noise on the planner mean, held for the macro). Default **off** in E1 so E1 tests the as-implemented framework; it is used in E2.
3. Add E0 probes (controllability ratio, same-state branching) on checkpoints.
4. Measure the production FB replay Gram spectrum (κ, effective rank) for information only. **No whitening, same-height relabel, world-model loss, or B-input expansion** (owner rule, agreed).

**Not recommended now:**
- whitening (B01 itself prescribes no whitening at sites i–iii)
- height in B (current B has none; the B03 waste theorem is inapplicable)
- world-model horizon work (separate track)
- a competence-gated source schedule (a candidate revision, but it changes the system under test; propose it only if E0 shows the deadlock signature)

---

## 10. Simpler alternatives and fair comparison cost

| Alternative | Isolates | Relative engineering cost | Fairness requirements |
|---|---|---|---|
| Direct-action off-policy task RL (SAC/TD3-family) + same obs, reward, curriculum, terminal semantics | Value of the body/task division + FB | Low (reuses env, replay, eval panels) | Same committed steps, same tuning budget (equal number of sweep configs), same seeds, same eval panels |
| The same + action repeat K and temporally correlated action noise | Temporal-abstraction / coherence nulls for §5 mechanisms 1 and 4 | Low (two flags) | Matched action variance; matched K |
| Massively parallel on-policy direct-action RL (PPO-family) | Practical wall-clock reference | Low–medium | Report both env steps and GPU-hours; the efficiency claim is on env steps |
| Reference-tracking reward + task reward (imitation baseline) | "Beyond imitation" outcome metric | Medium (tracking reward from the 859-frame demo) | Same demo, same curriculum; report off-demo heights |
| Goal-conditioned RL with hindsight relabel on kinematic goals + high-level planner | FB vs a simpler reward-free relabeled body layer | Medium–high | Second-wave only, if D2 passes |
| Two-stage (FB pre-trained on prompt-driven exploration, then frozen) | Joint-training drift cost | Medium | Second-wave only |

The first three rows form the fair minimal comparison set (E1). The rest are deferred.
