# Prin-2 Proposal A — Ladder-edge necessity among S0a / S0b / S1 / S2a / S2

**Author:** Competing Author A (Claude Opus). **Packet:** Prin-2 (Principle track). **Method:** v1.0 Appendix B, especially B.8 and B.9.
**Claim adjudicator for all IDs here:** Codex gpt-6-astra high (cross-family, per roster).
**Status of every claim:** Candidate. Nothing is Locked. One recommended-for-lock nomination (E17, narrow formal form).

## 0. Thesis

1. **Necessity arguments here bear only on availability, never on order.** Every information, stability or resource argument that survives citation-ablation in this packet says what a competence needs **available at runtime**. That is Reading A of B.8's "must precede, *or be available to*". None of them says which stage must be **built, trained or acquired first** (Reading P). The only support for any acquisition order is:
   - the evolutionary S0-first narrative (C-P1-003, Grade 3, which collapses under B.8.7);
   - the planning choice D-P1-001 (Provisional acceptance gate, which B.8.3 forbids citing as evidence).

   So **Reading P is Grade 3 and quarantined for every edge**, including the edges whose Reading A upgrades. Nobody may cite an upgraded Reading A as an ordering.
2. **The edges that matter are the ones into S1/S2 from fast-tier properties, and the S2a → S2 information edge.** The upgradeable content is:
   - **(a) Timing.** A hidden-disturbance separation bound (generalizing C-P1-001) shows that a single policy-rate loop cannot alone deliver robust envelope maintenance when `T + δ > L* ≈ b/D`. This is E03 and E07.
   - **(b) Information.** The KL data-processing inequality plus a binary-test converse shows that any S2 contact competence at `(TPR ≥ q, FPR ≤ r)` needs a channel with class-conditional divergence of at least `d(q‖r)`. When there is no side channel, that channel is the S2a export. This is E17.
   - **(c) Passivity.** C-P1-010 Part B yields only **disjunctive**, class-restricted edges from S0b: fast loop OR physical compliance OR specification relaxation. These have no force until `b_j` and `K_req,j` are measured. This is E13 and E15.
3. **Several plausible-looking edges are not necessity edges at all.** S0a → S0b, S0a → S2a, S1 → S2a, S2a → S1 and S1 → S2 fail every upgrade route. They describe shared resources (a fast tier, effort sensing), test-condition enablers (a body that stays up during hardware evaluation), side-channel *contributions*, or definitional containment. They stay quarantined at Grade 3.
4. **Finding:** in the timing bound, `L* = ln(1 + ab/D)/a ≈ b/D` whenever `|a|b/D ≪ 1`. With the fixture's `b/D = 0.01 s`, `L*` is 9.53 ms at `a = 10`, 9.84 ms at `a = 3.3` and 10.0 ms at `a = 0`. **The force of the S0a edges comes from the envelope-to-hidden-disturbance ratio and the loop period, not from plant instability.** The target-plant premise match should therefore prioritize measuring `b/D` per support mode over measuring `a`.

## 1. Working stage definitions (Author-A W-defs)

The permitted sources do not define S1 or S2. The definitions below are working definitions. A ratified definition that differs re-scopes the affected claims and is logged as a B.9.6 event.

| Stage | W-def (generic home humanoid / target plant) |
|---|---|
| **S0a** | Bounded-response viability: the body envelope is robustly maintained under a declared set of initially hidden disturbances, within a declared response deadline (C-P1-001 fixture form; C-P1-002 role form). |
| **S0b** | Remaining reflex/impedance content: fast-tier rendering of impedance/compliance and reflexive responses beyond viability, e.g., a passive virtual impedance at a joint (C-P1-010 setting). |
| **S1** | Policy-tier goal-directed whole-body motor competence (posture, locomotion, reach) commanded at the policy period `T_R2` (≈ 20 ms placeholder), including support-contact handling but **no reasoning about non-support contacts**. |
| **S2a** | Contact observability floor: the body-loop export `X` carries at least a declared amount of information about a declared non-support contact variable `Z` (onset/wrench/link, window, resolution; C-P1-011 premise 1) for a declared contact class (C-P1-012 premise 3). |
| **S2** | Contact-aware interaction: detecting, localizing and responding to non-support contacts with unknown passive environments (objects, humans) to a declared task specification. |

**Reading A** (availability/runtime) and **Reading P** (precede/acquisition) are graded separately inside each claim record.

## 2. Proposed edge claims

| ID | Edge | Reading A | Reading P | Upgrade route attempted | B.8.7 ablation | Disposition |
|---|---|---|---|---|---|---|
| C-Prin2-E01 | S0a → S0b | 3 | 3 | Information, stability, resource, role. All fail. A shared fast tier is not an order. | Collapses | **Quarantine** |
| C-Prin2-E03 | S0a → S1 | **1 conditional** (fixture) + Grade-2 companion via C-P1-002 | 3 | Hidden-disturbance separation, general `a`. Requires S1 to be specified under disturbance and `T_R2 + δ > L*`. | A survives | **Upgrade attempt: Candidate-stay** |
| C-Prin2-E05 | S0a → S2a | 3 | 3 | Information, stability, resource. All fail. A test-condition enabler only. | Collapses | **Quarantine** |
| C-Prin2-E07 | S0a → S2 | **1 conditional** (fixture; externally initiated contact) | 3 | Same as E03, with contact wrench as hidden disturbance. Self-initiated contact is excluded (efference side channel). | A survives | **Upgrade attempt: Candidate-stay** |
| C-Prin2-E09 | S1 → S2a | 3 | 3 | Information (commands, excitation, static detection). Fails. | Collapses | **Quarantine** |
| C-Prin2-E11 | S2a → S1 | 3 | 3 | Action-dependence lemma. Its premise fails for non-support `Z`; for support `Z_s` it gives an S1-internal floor, not this edge. | Collapses | **Quarantine** + stage-definition note |
| C-Prin2-E13 | S0b → S1 | A-narrow **1 conditional, disjunctive** / A-general 3 | 3 | C-P1-010 Part B, under an S1 passivity specification | A-narrow survives | **Candidate-stay. No force yet** |
| C-Prin2-E15 | S0b → S2 | A-narrow **1 conditional, disjunctive** / A-general 3 | 3 | C-P1-010 Part B, under an S2 passivity specification | A-narrow survives | **Candidate-stay. No force yet** |
| C-Prin2-E17 | S2a → S2 | **1 formal, conditional** | 3 | KL data processing + binary converse (Fano form secondary) | Survives | **Recommended-for-lock (narrow formal form)**, conditional |
| C-Prin2-E19 | S1 → S2 | 3 | 3 | Role: definitional containment only | Collapses | **Quarantine** |

Each record is at `claims/<ID>/{claim.md, upgrade-log.md, violations.md}` and gives premises, conclusion shape, scope, falsifier and spike status.

## 3. Which edges stay Grade 3 (quarantined)

- **E01, E05, E09, E11 and E19**, in both readings.
- **Reading P of all ten edges.**
- **A-general of E13 and E15.**

These may not appear as theorem, gate or veto in any packet (B.7, B.8.7). A proposal that skips any of them lists the edge as bypassed and states its grade (B.8.5). No lock forbids the skip.

## 4. Which edges attempt upgrade, and why

- **E03 / E07 (S0a available to S1 / S2).** These are B.8.2 Grade-1 information/stability arguments. Before world-dependent information arrives, the two worlds' trajectories separate at `Δ(L) = (2D/a)(e^{aL} − 1)`, so any channel slower than `L*` cannot keep both inside the envelope. Three things limit them:
  - They rest on the S1/S2 specification premise ("competence holds *under* hidden disturbance").
  - The general-`a` extension of C-P1-001 is an author derivation awaiting independent check.
  - They hold for a scalar fixture only.

  E07 is additionally limited to externally initiated contacts. **No lock nominated.** The parent C-P1-001 is unverified, and the stage definitions are unratified.
- **E13 / E15 (S0b available to S1 / S2).** Their upgrade is honest but **disjunctive**: physical compliance or a non-passive specification discharges them. They are also class-restricted to linear ZOH impedance, which excludes direct-torque learned policies. They carry **no force** until `b_j` and `K_req,j` (task-stated) exist. Kept as Candidate so that the measurement debt is visible.
- **E17 (S2a available to S2).** This is the cleanest upgrade. It composes standard results, uses no stage-definition premise beyond "S2 has a task-stated `(q, r)`", and is implementation-independent. Its programmatic force on the target requires the C-P1-011 side-channel audit. With a non-empty `W`, the edge weakens to "S2a jointly with side channels". **Nominated recommended-for-lock (narrow formal form only)**, with the B.9.2 item-match route stated in the record.

Model agreement on any of this is not grade evidence (B.9.7). Spike PASS cannot move any of these grades (B.8.4).

## 5. Gates before ranking (B.9.5)

For adjudication of Prin-2 proposals, and for any downstream packet, apply these checks **before** rubric ranking:

1. **Ladder-as-a-whole.** No grade is assigned to the ladder (B.8.1). Reject any proposal text that does assign one.
2. **Planning order.** D-P1-001 is cited only as a Provisional S0a acceptance gate, never as an edge or necessity order (B.8.3; brief constraint 8). This proposal does not promote it.
3. **Edge identity.** Every edge has its own ID (B.8.1). Check that availability and acquisition readings are graded separately; a check that conflates them fails.
4. **Citation-ablation.** Every claimed upgrade survives B.8.7. Any edge whose argument collapses is Grade 3 and quarantined.
5. **Three orders.** No evolutionary or developmental evidence is used as more than Grade 3 about engineering order (B.8.6).
6. **No locks.** No Locked Grade-1 without the human signature. No Grade-2 lock without the full B.9.2 evidence.
7. **Bypass declaration.** Any engineering proposal (Eng-1) lists bypassed edges with grades (B.8.5).

Only after these pass should the rubric (Principle integrity, Falsifiability, and so on) rank proposals.

## 6. Can any edge GATE Eng-1?

**No. No edge in this proposal can gate Eng-1 today.**

- Candidate claims cannot veto (B.4).
- The Grade-3 edges cannot be gates at all (B.8.7).
- The edges directly upstream of S2a are E05 (S0a → S2a) and E09 (S1 → S2a). Both are **Grade 3**. **An Eng-1 packet on the S2a contact observability floor may therefore proceed without S0a or S1 completion.** It must list E05 and E09 as bypassed, Grade 3.

What Eng-1 *should* take from this packet, as design inputs and not as gates:

1. **E17 → specification form.** Eng-1 proposals should state the following, so that E17 becomes testable and S2a acceptance is expressed as an implementation-independent floor rather than a spike threshold:
   - the contact variable `Z` (class, window, resolution);
   - task-stated `(q, r)` per class;
   - the resulting divergence floor `d(q‖r)`;
   - an explicit side-channel `W` enumeration, including efference copies of commands.

   If E17 is later locked (after the check and the signature), it becomes a **conditional gate on S2-stage proposals**: an S2 proposal with no channel able to meet `d(q‖r)` would be rejected. It would still not be a gate on S2a work itself.
2. **C-P1-012 factorial.** The question of which signals achieve the floor (rate × effort source) remains with C-P1-012's registered factorial. E17 does not answer it.
3. **E03/E07 hardware note.** Hardware evaluation of S2a on a floating base needs the body to remain in the operating region. S0a, a support fixture, or a stable mode provides that. **This is a test-condition enabler, not an edge** (see E05).

## 7. Debts and requests to Orchestrator / human lead

- Ratify the S1 and S2 definitions. E03, E07, E11 and E19 depend on them.
- Decide whether support-contact observability belongs to S1 or to S2a (E11 planning note).
- Arrange the independent B.9.2 checks:
  - E17 item-match against published KL data-processing and binary-hypothesis-testing converse statements;
  - the general-`a` extension used by E03/E07, together with C-P1-001.
- Measure or specify `b/D` per support mode, `T_R2 + δ`, `b_j` and task-stated `K_req,j`. Without these, E03, E07, E13 and E15 have no target force.
- Optional counterexample PLANs (one-liners in each record): E03/E07 common-input optimization; E05/E09 fixed-base detection floor.

## 8. Non-claims

- No claim that any stage must be acquired first.
- No claim that any stage is a separate module, process or processor.
- No hardware-transfer claim.
- No claim that S0a-first (D-P1-001) is necessary.
- No grade for the S0–S7 ladder.
- No named robot, product or company.
