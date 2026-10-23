## Appendix B — Principle necessity protocol

This appendix is about **judging claims by necessity**, not by benchmark score. The goal is to extract constraints that can **rule routes in or out before the fact**—closer to physical laws and mathematical theorems—rather than justifying a technique only because some implementation performed well.

It does not replace the main orchestration cycle (§4) or Appendix A (model roster). It adds a **Principle track** that can veto purely phenomenological justifications.

### B.1 Two different kinds of judgment

| | **Phenomenological / performance judgment** | **Principle / necessity judgment** |
|---|---|---|
| Evidence | Scores, demos, correlations from a specific implementation | Constraints, invariants, impossibilities, obligatory functional roles |
| Force | “This can work” (sufficiency) | “That path is blocked / any solution must …” (necessity) |
| Analogy | Trying many machines; one is fastest | Thermodynamics: perpetual motion need not be tried again |
| Output | Engineering baseline | Transferable theorem-like conclusions |

Multi-agent research on open scientific programs should **pursue both**, but must not let the left column quietly promote itself into the right.

### B.2 Three grades of necessity (do not conflate)

#### Grade 1 — Hard necessity (theorem-like)

Under stated assumptions, prove **impossibility** or **obligation**:

- Information: without information gain, states cannot be distinguished (sensing lower bounds)
- Control: unstable plants cannot be arbitrarily stabilized under given delay/bandwidth limits
- Computation: a class of maps is unrealizable under given resource bounds
- Embodiment: without force/contact channels, some manipulation classes are impossible

**Use:** routes that violate a locked Grade-1 claim may be rejected **without** further bake-offs.

#### Grade 2 — Structural necessity (obligatory functional roles)

Implementation need not be unique, but certain **functional roles** must appear for a competence class, for example:

- State estimation (explicit or implicit)
- Error-driven corrective closed loops
- Multiple timescales (fast reflexive versus slower intentional)
- Treating body dynamics as part of prediction, not as decorative outputs

Neuroscience and convergent evolution often supply **candidates** for Grade 2 (recurring functional decomposition), not a unique wiring diagram.

**Use:** a proposal must state how each locked role is realized, and name an operational test that would show the role is absent (B.9). Missing roles mark the design **incomplete** in principle—not “maybe it will emerge, so lock it as the mainline.” A role claimed to be realized “implicitly”, with no such test, counts as missing.

#### Grade 3 — Path contingency (historical fact, not law)

“Earth life happened to take this path” is **not** “every intelligence must.” Specific cortical maps, receptor layouts, or phylogenetic accidents are often Grade 3.

**Use:** strong inspiration and existence proofs (the path is feasible). **Do not** write them as the only admissible road unless upgraded to Grade 1 or 2 (missing it is impossible, or the functional role is obligatory).

**Core research action for agents:** try to **upgrade** literature and anatomy from Grade 3 → 2 → 1. If the upgrade fails, keep the claim labeled as inspiration and **forbid theorem-style use**.

### B.3 What a valid necessity claim looks like

A principle claim eligible for locking must have:

1. **Explicit premises** (organism/machine class, environment, task, resources)
2. A conclusion of only these shapes: impossibility; lower bound (“any solution must…”); functional completeness (roles R1…Rk); invariant (conserved or monotonic relation)
3. **Implementation independence** (applies across model families and classical methods alike)
4. A clear **violation / falsification mode** (a counterexample downgrades the claim or adds premises)
5. **Ban:** benchmark wins alone must never prove necessity—scores support sufficiency only

Special cautions:

- **Evolution:** lawful use is feasible-region shrinkage under constraints; unlawful use is “mammals did X, therefore every robot must copy X.”
- **Neural structure:** lawful use is candidate Grade-2 roles (for example, fast/slow pathways → multi-timescale loops); unlawful use is renaming a brain area as a mandatory network module.

### B.4 Lifecycle: Candidate / Locked / Challenged

A necessity claim is not fixed at the start, and it is not endlessly fluid. Each claim is in exactly one of three states:

| State | May | Must not |
|---|---|---|
| **Candidate** | Guide exploration and shape proposals | Veto the mainline |
| **Locked** | Veto routes justified only by phenomenology. An implementation obeys the claim or files a challenge | Depart from the claim without a challenge packet |
| **Challenged** | Stay on record. Once the challenge is *admitted* (B.9), pause the old lock’s veto until adjudication or until the challenge’s deadline | Apply that lock as a veto while an admitted challenge is open |

Path for one claim:

propose → grade (1, 2, or 3) and scope → **Candidate** → proof or other non-score evidence → **Locked** → counterexample or a change of premises → **Challenged** → upgrade, downgrade, narrow the scope, or retire.

Rules:

- Phenomenology scores never promote **Candidate → Locked** and never rewrite a **Locked** claim. A score may only open a challenge packet.
- A narrow Grade-1 formal bound may lock early, subject to the verification and signature requirements in B.9.
- Grade 2 often stays **Candidate**, then locks as the role converges.
- Grade 3 stays inspiration unless it is upgraded. It does not enter **Locked** on its own.

### B.5 Principle track versus phenomenology track

| Track | Output | Authority |
|---|---|---|
| **Principle track** | Premise → necessity claim → grade (1/2/3) → scope of validity | May **veto** lines of work justified only by phenomena |
| **Phenomenology / baseline track** | Performance, demos, correlations | Proves sufficiency only; cannot alone promote a claim to necessity |
| **Implementation track** | Algorithms and systems | Must declare which locked principles it obeys; if it violates one, challenge the principle first—do not silently ignore it |

Priority when judging a viewpoint:

1. Conflicts with a locked Grade-1 claim → reject (no need to try)
2. Missing a locked Grade-2 role → mark incomplete (exploration allowed; not eligible as the locked mainline)
3. Performance advantage with no principle support → baseline only; not “essentially correct”
4. Proposal to upgrade a principle → proof or counterexample, not leaderboard climbing

### B.6 Honest scope

For life-like perception–action, stable yields today are mostly **information/control/embodiment lower bounds** plus **Grade-2 structural candidates**. Evolutionary narratives more often give **constructive existence proofs and inspiration** than hard laws.

The aim is not to pretend biology-grade Newtonian laws already exist. The aim is to **maintain an explicit necessity ladder**, upgrade what can be upgraded, and forbid theorem-style wording for what cannot—thereby **shrinking the trial-and-error space**.

### B.7 Minimal artifacts

For each candidate principle, keep a short record:

- `claim.md` — premises, conclusion shape, grade, scope
- `upgrade-log.md` — attempts to move 3→2→1 and outcomes
- `violations.md` — known counterexamples or failed transfers

Orchestration rule: no implementation work package may treat a Grade-3 note as a hard constraint; no phenomenology result may rewrite a locked Grade-1 claim without an explicit challenge packet.

### B.8 Capability ladders and the Principle track

A **capability ladder** is an ordered list of competence stages, often taken from evolutionary or developmental history, and used to sequence work. A ladder carries two kinds of statement, and they are graded separately:

- **Stage content:** “competence *k* exists and is useful.” This is usually a sufficiency claim or Grade 3.  
- **Edge order:** “*k* must precede, or be available to, *k+1*.” Each edge is its own claim.

Rules:

1. **No grade for the whole ladder.** The ladder as a whole is never Locked. Only individual edges and stage-role claims can be.  
2. **Edges start at Grade 3.** An edge taken from biology or development is Grade 3 by default. An upgrade needs one of:  
   - *Grade 1:* an information-flow, stability, or resource argument, under stated premises, that *k+1* needs a signal, bound, or property that only *k* supplies.  
   - *Grade 2:* an argument that *k* realizes a functional role obligatory for the competence class of *k+1*, with an operational test (B.9).  
3. **Planning order is not evidence.** The human lead may adopt a ladder as a planning order. That is a brief constraint, scoped to the run or program. It binds the work but is not evidence, and a proposal may not cite the ladder's order as a necessity argument.  
4. **Passing a gate is sufficiency only.** A stage gate (a passed spike) is sufficiency evidence about that stage. It never establishes the necessity of the next edge and never changes a grade.  
5. **Skipping is allowed unless locked.** Skipping or reordering stages is allowed unless a Locked edge forbids it. A proposal that skips must list the edges it bypasses and the grade of each.  
6. **Three different orders.** Evolutionary order, developmental order, and engineering order are distinct. Evidence about one is at most Grade-3 evidence about the others.  
7. **Citation-ablation test.** For any argument that cites evolution, development, or anatomy, delete the citation and re-read the argument. If it still stands on its stated premises, the citation was inspiration, which is allowed. If it collapses, the argument is Grade 3 and may not be used theorem-style: not in claims, gates, or vetoes.  
8. **Convergence can nominate, not lock.** Convergence across independent lineages under a shared constraint may nominate a Grade-2 candidate more strongly than a single lineage can. It still needs the operational test, and it still locks only under B.9.

### B.9 Claim governance

1. **Separate roles.** A claim author proposes a claim record (premises, conclusion shape, grade, scope, falsifier). A **claim adjudicator**, who is not the claim author, decides state transitions. With heterogeneous models they are different models, and for high-stakes claims, different families.  
2. **Locking requires verification and signature.**  
   - **Grade 1:** a proof checked independently of its author. Acceptable checks: a formal checker; an established published result whose premises are matched item by item to the claim's premises; or review by a qualified human. The human lead must also sign. A Grade-1 lock prunes routes with no contest, so it is an irreversible action in the sense of §6 rule 4.  
   - **Grade 2:** an argument from premises that applies across implementation classes; a defined operational realization test (rule 3); a logged, serious attempt to find or build a system that reaches the competence class without the role, which failed (`upgrade-log.md`, `violations.md`); and the human lead's signature.  
3. **Operational realization test.** A proposal claiming to realize a Grade-2 role must name a test that would show the role is absent. Examples: a probe that must recover the estimated quantity within a stated error; an intervention on the named signal that must produce a stated effect; a timescale separation measurable in the closed-loop response. Without such a test, the role is not realized.  
4. **Challenge admissibility.** A challenge pauses a lock's veto only once it is *admitted*. Admission requires either (a) a concrete counterexample, with artifacts, that satisfies the claim's stated premises, or (b) evidence that a premise fails in the target setting. The claim adjudicator rules on admission and sets a deadline. If the challenge is unresolved by the deadline, the human lead decides whether the veto resumes. A challenge that is not admitted is filed and pauses nothing.  
5. **Gates before ranking.** Appendix B gates apply before rubric ranking (§4 Step 4). A rubric row about necessity discipline may score the quality of reasoning, but it never substitutes for the gate.  
6. **Scope-narrowing counter.** Log every narrowing of a claim's scope, and every premise added so the claim can survive a counterexample. At the third such event (the brief may set a different default), the claim goes to mandatory review for retirement. A claim that survives only by shrinking is degenerating.  
7. **Researcher agreement is not grade evidence.** Several researcher model families agreeing that a claim holds is evidence about how persuasive the argument is. It is not evidence of implementation independence (B.3.3), and it moves no grade.  
8. **Counterexample searches are experiments.** They run under §12.2, with a `PLAN.md` stating what counts as a counterexample. The runner files the data and does not change claim state.

---

## Changelog
