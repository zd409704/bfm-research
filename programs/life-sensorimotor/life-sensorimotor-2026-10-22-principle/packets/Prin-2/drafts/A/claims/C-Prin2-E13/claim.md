# C-Prin2-E13 — Edge S0b → S1

| Field | Value |
|---|---|
| **Edge** | S0b → S1 |
| **Author family** | Opus (Prin-2 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family) |
| **Grade** | **Reading A-narrow: Grade 1 conditional, disjunctive, class-restricted.** It is inherited from C-P1-010 Part B, whose premises are unmeasured. **Reading A-general: Grade 3. Reading P: Grade 3.** All readings are quarantined from gate use. A-narrow has no force until its premises are measured. |
| **State** | Candidate |
| **B.9.6 narrowing counter** | 0 |
| **Recommended adjudicator action** | Candidate-stay (A-narrow). quarantine-Grade3 (A-general, P). |

Stage meanings: Author-A W-defs (`proposals/A.md` §1).

## Premises

1. C-P1-010 premises 1–8. Single joint. Linear ZOH virtual impedance. Linear viscous `b_j`. Passive but otherwise unknown environment. Virtual stiffness only.
2. **S1 specification demands a passivity guarantee** at task stiffness `K_req,j` on joint `j` against unknown passive environments, for example ground or support surfaces of unknown stiffness. **This is a specification choice.** Passivity is sufficient, not necessary, for coupled stability (C-P1-010 scope).
3. The S1 tier renders the stiffness of joint `j` at period `T_R2`.

## Conclusion shape — Reading A-narrow (conditional lower bound, disjunctive)

If `K_req,j > 2(b_j − |B|)/T_R2`, then S1 competence under premises 1–3 requires **one of** the following:
- (i) a loop faster than `T_R2` rendering that stiffness, which is S0b content;
- (ii) physical compliance supplying it, which is a plant property and not a stage;
- (iii) relaxing the passivity requirement, which is a specification change.

So S0b is available to S1 **only if** (ii) and (iii) are excluded. Even then, the conclusion holds only for implementations in the linear-ZOH-impedance class.

## Why A-general is Grade 3

S1 policies that output torques directly, or are nonlinear or multi-DoF, are outside C-P1-010 Part A (scope exclusions). The record contains no argument that such an S1 needs S0b. Citation-ablation of the reflex/spinal-motor inspiration leaves nothing → **Grade 3.**

## Reading P

There is no acquisition-order argument → **Grade 3.**

## Citation-ablation (B.8.7)

A-narrow uses no biological premise and **survives**. A-general and P **collapse**.

## Scope

Premise-matched joints only. `b_j` and `K_req,j` are not measured or specified (C-P1-010 H3). Until they are, A-narrow constrains nothing. `K_req,j` must come from the task, not from an existing controller's gains.

## Falsifier / challenge mode

- **Retire for joint `j`:** measured `2(b_j − |B|)/T_R2 ≥ K_req,j`.
- **Premise failure:** physical compliance supplies the stiffness, or S1 is specified with non-passive stability for a known environment class.
- **In-premise counterexample:** a passive coupled system above `K_max`. That would challenge C-P1-010 itself.

## Counterexample-search spike registered?

**No.** It relies on C-P1-010's registered frequency-domain sanity PLAN. The real need is measurement of `b_j` and a task-stated `K_req,j`.
