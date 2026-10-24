# Independent framework review — Author B

Round: feedback-round-2026-10-24. Program: fb-beyond-imitation-acceleration. Date: 2026-10-24.

**Judgment: substantive revision of the claims and validation strategy; revise-then-continue at small scale only.** The corrected architecture is coherent enough to test. Neither its sample efficiency nor its ability to acquire and reuse task-relevant skills has been demonstrated by the reviewed evidence. A full neural convergence proof is not a prerequisite for testing; favorable conditional theory is not a substitute for training evidence.

The most promising benefit is that each valid interaction can improve a reusable conditional controller even when its current task return is poor. The strongest objection is objective sufficiency: a body objective that never sees task reward can learn an extensive repertoire that still lacks the actions needed for the task. A planner cannot select a behavior that its actor cannot execute. Joint training also makes the planner's effective transition dynamics move.

Evidence authority and scope: [owner correction](../../briefs/OWNER_FEEDBACK_EN.md) takes precedence over historical interpretation in the [charter](../../../PROGRAM_CHARTER.md), [ledger](../../../program-ledger.md), and B01–B05 synthesis. Implementation facts attributed to the owner are audit reports, not independently verified production code. Local source inspection covered the experimental modules and selected packet specifications. No production training or new scientific experiment was run. The companion [gap table](GAP_TABLE.md) distinguishes those levels.

## The causal chain and what could break it

| Link | Why it could work | Necessary condition and decisive observation |
| --- | --- | --- |
| Body experience → conditional behaviors | Real transitions train a shared successor representation and actor under multiple conditions, amortizing dynamics learning. | Sufficient action/state coverage and a learnable conditional objective. Check reproducible physical outcomes for different commands, not only decreasing loss or different actor outputs. |
| Conditional behaviors → organized z exploration | Holding a condition lets closed-loop control coordinate many joint actions over time. | Commands must produce useful, distinct trajectories. Same-state branching must distinguish useful variation from extra falls and action saturation. |
| Exploration → expanded body capability | New valid transitions become real FB training examples and current-B conditioning cues. | Acquired outcomes must become executable on held-out starts. More replay entries or a larger latent spread alone do not show capability growth. |
| Expanded capability → task success | Task returns train a separate Q/planner to select and sequence body conditions. | The repertoire must cover task requirements and task Q must remain calibrated as the actor changes. Compare planner outcomes with a bounded command-search diagnostic. |
| Present experience → later goals | Shared dynamics and previously acquired recovery/contact behaviors may reduce later interaction needs. | Relevant information must survive finite replay and parameter interference, and a new planner must discover it. Measure data availability, skill execution, and planner use separately. |

## What the theory licenses

For a fixed conditional policy, a sufficient state or history x, and motion outcome m, write the discounted motion occupancy as M_z(x,a,dm). If it has density relative to replay measure rho and that density is represented by F(x,a,z)^T B(m), then

`w_r = E_rho[B(m) r(m)]`, and `Q_r^{pi_z}(x,a) ≈ F(x,a,z)^T w_r`.

This is linear in the reward readout w_r for a fixed policy. It is not a statement that task Q(history,z) or success probability is linear in z. Changing z changes the actor, future occupancy, and F. Low-rank approximation, missing support, history insufficiency, and changing networks introduce error. An exact motion-occupancy factorization supports integrable motion rewards; weaker feature-moment consistency supports the represented reward span. Neither condition supplies arbitrary terrain/contact/task rewards from a motion-only B. See [the local derivation](../../../baseline/01-fb-theoretical-derivation-and-q-readout.md).

The current B excludes obstacle height and other task context. A separate task Q is consequently appropriate. Identical current B encodings do not imply identical future occupancy or optimal action: context in the actor and F can distinguish different physical situations. Conversely, context does not guarantee that optimization learns the required behavior. The strong “necessary and sufficient” wording in B03 requires additional representability, observability, coverage, and optimization premises.

Optimizing linear preferences over motion occupancy can favor exposed portions of the achievable occupancy set; it does not guarantee access to every task-useful behavior. Two behaviors can have equivalent represented occupancy but different task effects. Before changing B, establish a physical counterexample using full actor inputs and future behavior, not equal single-frame descriptors alone.

The standard actor readout F·z, expert/near encoding, and the existing 50/50 update-condition sampler remain intact. B01's covariance solve concerns matching a separately introduced explicit reward head to its FB tail under specified rank assumptions. It does not justify whitening every command. The first-action derivative of an accurate successor value can already include long-horizon consequences; “first-action derivative” does not mean “one-step knowledge.”

## Body/task division and cold start

The separation is useful when diverse motion objectives create a task-sufficient repertoire and task adaptation mainly requires selecting and ordering its behaviors. It is inadequate if task success requires a missing contact intention, action direction, or observation unavailable to the body controller. Task reward reaching the planner does not directly repair that missing body objective in the audited macro-z design.

At random initialization, demo frames are cues to an untrained B/actor, not competent motion demonstrations for the controller. A benign loop is possible: initial real transitions make some commands controllable, those commands improve exploration, and new outcomes broaden training. A deadlock is equally possible: immediate falls provide narrow support, random conditions remain ungrounded, and the planner exploits critic errors. Report survival, nontrivial controllability, novel successful outcomes, and planner-only learning curves from initialization. Do not hide pretraining or successful reset states in the interaction budget. Failed physical transitions remain useful negative evidence; numerical corruption does not.

## Why z and macro steps might help

The hypothesis is coordinated temporal exploration through a learned controller. It is not dimensional compression: 256 latent coordinates exceed 29 action coordinates. Inner-product readout and angular proximity do not ensure locally similar contact behavior. Contact switches can make a small latent perturbation discontinuous in outcome.

Holding z for K control steps reduces high-level decision frequency, while the actor still responds each control step. The FB critic evaluates a counterfactual continuation under fixed z; the macro task critic evaluates the actual K-step execution followed by planner switching. These are compatible roles if their targets remain distinct. Off-policy one-step FB training can reuse transitions collected under switching commands, subject to coverage and correct target actions. An uncorrected multi-step segment that crosses a z switch is not automatically a fixed-z target.

Switching too early can interrupt preparation or recovery; holding too long can prevent timely reaction. Use actual elapsed k for macro returns and discounting, including early termination. K=10 is a baseline choice, not a proven optimum. Audit termination versus time-limit truncation semantics explicitly.

## Joint drift and retention

Re-encoding raw motion with current B avoids stale prompt caches. Immutable executed z labels preserve what was commanded. Neither makes an old macro transition current: changing the actor changes the path distribution induced by the same z. Short replay windows and target smoothing are mitigations, not a bound by themselves. With deterministic executed actor means, Gaussian likelihood correction cannot be assumed available. Record generation identities, actual command/action paths, recurrent prefixes, replay age, and paired old/new physical outcomes.

The three data paths must remain distinct:

1. Offline pose/velocity material supplies B cues. It is not a source of invented action/next-state transitions.
2. Valid real transitions update FB and its actor without task-return filtering.
3. Executed macro commands, histories, elapsed durations, and task returns update task Q/planner.

Update-condition random draws and target-smoothing draws do not constitute executed exploration. The owner reports expert/near environment exploration and deterministic planner/actor-mean execution, without independent planner-z exploration noise.

“Retained” has three tests: a record is still readable; a skill remains executable from specified states; a planner can find and use it. Finite circular replay only promises bounded storage. Capacity competition, forgetting, skewed sampling, and negative transfer can erase the purported benefit or increase its cost.

## Investment decision and alternatives

Continue only with the bounded [A-then-C plan](MINIMAL_EXPERIMENTS.md). A tests net task-learning efficiency; C then isolates whether low-task-return experience caused reusable capability. Near is one deferred exploration ablation. Beyond-demo success is a secondary outcome, not the research mainline. World-model acceleration remains a separate track.

Simpler alternatives are direct-action task RL, a motion-imitation prior with task adaptation, and a fixed pretrained body controller with a new task planner. The first two are required A comparators; the third is a later alternative if joint drift dominates. Count demonstrations, pretraining, tuning, interactions, memory, updates, and elapsed/accelerator cost. Do not weaken the imitation baseline by denying it task adaptation or requiring unavailable action labels.

Advance only if the framework clears the pre-registered advantage and reliability gates. An inconclusive budget-limited result supports no efficiency claim. Persistent controllability failure, or an adequate simpler baseline winning while the framework fails its gate, warrants substantive architectural revision before additional scaling. These are checkable reasons to stop this configuration, not a claim that all FB architectures are impossible.
