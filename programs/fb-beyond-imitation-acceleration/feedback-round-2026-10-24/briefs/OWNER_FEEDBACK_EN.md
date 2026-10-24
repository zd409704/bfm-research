# Owner Feedback Round — Framework Refocus (2026-10-24)

Audience: research agents on program `fb-beyond-imitation-acceleration` under `/srv/claude/research/fb-beyond-imitation-acceleration/`.

## Corrected mainline

Build a training framework that improves exploration and experience utilization:
- FB + conditional actor learn reusable body behaviors.
- Task planner learns to call and organize behaviors in z-space.
- Real exploration expands behavioral capability.
- Experience that does not serve the current task can still train the body layer and be reused later.
- Demonstrations provide initial motion cues; task learning and capability growth can expand with interaction.

Prior narrowing to "near" and "success beyond demonstration" was incorrect. Those remain: near = one exploration ablation; success beyond demonstration = an outcome metric of framework effectiveness.

Priority this round: sample/learning efficiency of the framework itself (task vs body division; temporally structured conditional exploration; cross-behavior/task reuse). World-model acceleration is a separate track. Existing FB theory and UFO implementation are foundations; next validation needs real robot-training evidence, not only local mechanism spikes.

Independent critique is mandatory. Agents must judge whether the design is theoretically sound and worth continued investment. Conclusions may be: support, conditional support, substantive revision required, or do not continue — each with checkable reasons. Maturity of FB theory does not prove this combination works; absence of a full NN convergence proof is not alone grounds to reject.

## Mechanism sketch

Demo motion frames -> current B -> expert/near conditioning cues.
Observation history -> task planner -> z -> conditional actor -> real physics.
Real transitions update FB/actor (body capability). Real task returns update task Q/planner.
Later calls/exploration/new experience feed both layers.

z organizes learned behavioral conditions and long-horizon motion tendencies; the actor turns them into closed-loop control. Macro-steps holding z may yield more coherent exploration than independent joint noise. Benefits depend on learned control structure and coverage, not on claiming "acceleration from lower dimension" (`z_dim=256` vs action dim 29).

FB reward readout `w_r = E[B(m)r(m)]`, `Q ≈ F(x,a,z)^T w_r` is linear in `w_r` under a fixed conditional policy. Changing z changes F and future occupancy. Do not assume task success or `Q_task(history,z)` is linear in z, or that nearby z yields nearby contact behavior. Current B is motion-only; full obstacle rewards still use a separate task Q.

Three data paths must not be conflated: offline pose/velocity material as B cues (not forged off-policy transitions); real transitions for FB/actor; real interaction with task returns/history/macro-z for task Q/planner. "Retained" means readable data vs still-executable skill vs planner can find/use it — measure separately.

## Implementation facts (from owner audit)

- `FBAgent.update` does not read task reward; `TaskLearner` updates task Q/planner from macro returns.
- Default multi-condition reuse: 50% current-B next-motion condition, 50% random sphere.
- FB replay does not filter by task return.
- Finite circular FB replay + separate task replay age/height rules — no promise of permanent retention.
- Environment exploration today: expert frame + near; planner emits z with actor `.loc` mean — no independent planner-z exploration noise yet.
- Training RNGs for FB z / task target smoothing are not the same as executed exploration.

Keep existing tip/update semantics from sealed B01 (standard expert/near encoding, UFO z_update, standard F·z actor readout). Do not generalize covariance solving into "all z must be whitened."

## Corrections to prior delivery claims

| Material | Keep | Correct |
| --- | --- | --- |
| Charter H4 | Research question on three-source beyond-demo exploration | Mark incomplete pending real training; not closed by B01–B05 process end |
| B01 main | Matrix relations / numerical checks on artificial distributions | Condition number is not measured on production G1 replay; not production whitening warrant |
| B02 main | BN freeze / label isolation / RNN recompute prototypes | Random-data checks do not prove macro-Q stability or near effectiveness |
| B02 D4/D5 | Tangential z perturbation diagnostics | Valuable but not landed in main experiments |
| B03 main | Supervised same-input checks with artificial context | Not a real contact-skill experiment; 0.9105 is predictor error, not verified physics floor |
| B03 6/7 waste | Came from a specific height-in-B assumption | Current B has no height — do not claim 85.7% waste or install 70% same-height sampling |
| B04 main | Gradient prototypes on simplified dynamics | Do not declare acceleration or optimal H; old spike cosines / arm defs were misaligned |
| B05 main | Independent FSM / quota formula checks | Does not replace real production terminate/replay/eval/recovery verification |

F first-action derivatives of an accurate F can include long-horizon consequences. Do not interpret "derivative w.r.t. first action only" as "FB sees only one step." Identical single-frame B encodings do not imply identical long-horizon behavior across contacts/terrains.

## Required deliverables this round (order)

1. Whole-framework theoretical review and value judgment answering the causal chain:
   body experience -> conditional behaviors -> z organizes exploration -> new transitions expand body skill -> planner uses new skill for task -> experience serves later goals.
   Separate: theory holds / implementation matches theory / empirical benefit.
2. Mechanism vs implementation gap table (what code does vs missing).
3. Corrected research conclusions: re-slot B01–B05 as theory / local check / pending real experiment; keep review limitations; script PASS != framework validated.
4. Minimal decisive experiments chosen from A/B/C after the review (not all at once):
   - A: framework vs imitation baseline vs direct-action task RL (sample efficiency)
   - B: z-space exploration (incl. near ablation)
   - C: low-task-return experience enters learning and serves later tasks
5. Real code/evidence plan for production climb training chain (outside this sandbox): configs, identities, per-seed curves, costs. This sandbox may only write under `/srv/claude`.

Do not batch-add whitening, same-height relabel, world-model losses, or B-input expansion from toy tests without targeted evidence.

## Review questions that must be answered

FB theory applicability bounds; body/task division sufficiency; cold-start benign loop vs skill/exploration deadlock; why z-space may help (not from inner-product smoothness alone); macro-K switching vs long-horizon conditional learning compatibility; joint training drift vs off-policy tolerance; why currently irrelevant experience may help later (and negative transfer / capacity costs).

Output required judgments:
1. Most promising benefit vs strongest objection.
2. Support / revise-then-continue / small-scale-only / do-not-continue, with decisive assumptions.
3. One or two bounded decisive checks with pre-registered thresholds.
4. Simpler alternatives and fair comparison costs.
