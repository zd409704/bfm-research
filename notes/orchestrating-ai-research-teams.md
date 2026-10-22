# Orchestrating AI Research Teams for Large Scientific Problems

A practical methodology for coordinating multiple AI agents (and human researchers) on open-ended research questions so that proposals converge on strong, testable solutions rather than consensus theater.

**Audience:** anyone running multi-agent research workflows (LLM agents, specialized bots, or mixed human–AI teams).  
**Scope:** process and governance only. Domain-specific architectures, products, and project names are intentionally omitted.

---

## 1. Core idea

Optimal outcomes do not come from “more agents talking.” They come from:

1. **Decomposing** the problem into independently checkable subproblems  
2. **Forcing competition** (independent drafts under the same constraints)  
3. **Adjudicating** with a fixed evaluation rubric written *before* solutions exist  
4. **Falsifying** the leading candidate with a short experiment before locking it

One-line definition of “best”:

> Under stated constraints, the candidate that scores highest on a pre-agreed rubric **and** is not immediately falsified by a minimal empirical spike.

Voting, eloquence, and group-chat agreement are not substitutes for that definition.

---

## 2. Three layers of work

Do not drop an entire large question into a shared chat. Separate layers and owners:

| Layer | Deliverable | Owner |
|---|---|---|
| **Problem definition** | Falsifiable problem statement, success criteria, hard constraints / forbidden moves | Human lead (final authority) |
| **Subproblems** | Task packets that can be accepted or rejected independently | One primary agent (or person) per packet |
| **Integration & adjudication** | Comparison table, recommendation, and rejection rationale | A designated adjudicator who does **not** author proposals |

Specialization beats generalists writing the same essay three times. Assign by capability (perception, planning, control, evaluation, documentation, etc.). Cross-review is allowed; co-authoring the same draft is not.

---

## 3. Roles (separation of concerns)

| Role | Responsibility | Must not |
|---|---|---|
| **Primary author** | Deliver an executable proposal for one subproblem | Score their own work as “best” |
| **Red team** | Attack failure modes, edge cases, and hidden assumptions | Replace the draft with a full competing design (that is a separate authorship track) |
| **Adjudicator** | Fill the rubric, recommend / alternate / reject | Write proposal body text |
| **Experiment runner** | Execute the locked spike plan and return raw results | Change the goal mid-run |
| **Documentation / release** | Clean external write-ups, repos, and citations | Silently change technical conclusions |

Keep authorship and judgment in different hands. The same agent may play different roles on different subproblems, but never both author and adjudicator on the same packet.

---

## 4. The research cycle

Run the same loop for every large question:

### Step 1 — Brief (human lead)

One short brief that includes:

- Problem statement (what is unknown or undecided)  
- Constraints and non-goals (what is out of scope or forbidden)  
- Rubric dimensions and how they will be scored (see §5)  
- Interfaces / contracts if the work spans modules (inputs, outputs, latency class, ownership of state)  
- Deadline and artifact format (markdown report, design note, experiment plan, etc.)

No drafting of solutions begins until the brief exists.

### Step 2 — Solo draft (primary authors)

- At least **two independent** proposals for the same subproblem when the stakes are high  
- Authors must **not** see each other’s drafts during drafting  
- Deliverables go to a shared source of truth (repository or canonical doc), not only into chat

### Step 3 — Blind review (cross review)

- Reviewer A reviews B’s draft for holes and infeasibility  
- Reviews cite the rubric and the brief’s constraints  
- Reviewers do not rewrite the full document; they file objections

### Step 4 — Adjudication

- Adjudicator fills the same rubric for every candidate  
- Output: **Recommend / Alternate / Reject**, plus one paragraph of rationale  
- Ties go to the human lead; agents do not majority-vote

### Step 5 — Spike (minimal experiment)

- Only the recommended candidate gets a short empirical check  
- Success criteria for the spike are written in the brief or adjudication note  
- Raw logs / metrics are filed; narrative without data does not count as a pass

### Step 6 — Lock

- Winning design is versioned in the canonical document  
- Later discussion may only open a **change request**; silent architecture drift is forbidden  
- Chat is never the source of truth

Shared discussion channels are useful for Steps 3–4 (disputes). They are harmful for Step 2 (independent exploration).

---

## 5. Rubric before solutions

Write the evaluation table when writing the brief. Typical dimensions (adapt as needed):

| Dimension | Question |
|---|---|
| **Constraint fit** | Does it obey hard constraints and non-goals? |
| **Falsifiability** | Can we tell within a defined spike that it failed? |
| **Evidence demand** | How much data / compute / hardware does it require to validate? |
| **Failure modes** | Are dominant failure modes named and mitigable? |
| **Integrability** | Does it respect module boundaries and interface contracts? |
| **Latency / criticality class** | Is it placed in the right real-time vs offline tier? |
| **Complexity cost** | Is added machinery justified by a clear gain? |
| **Reversibility** | How expensive is it to abandon if wrong? |

Rules:

- Rubric dimensions are fixed before drafts exist; changing them mid-contest requires an explicit brief amendment.  
- Scores without comments are weak; each low score needs a concrete objection.  
- “Looks coherent” is not a dimension.

---

## 6. Hard rules that prevent multi-agent failure

1. **Single source of truth** — Only the versioned repository (or named canonical doc) is authoritative. Chat threads are discussion, not decisions.  
2. **Interface contracts first** — When modules interact, define ownership, topics/APIs, and timing class before inventing internal algorithms.  
3. **No consensus theater** — Agreement among agents that never competed under a rubric is treated as weak evidence.  
4. **Human gate on irreversible actions** — Paid compute, production changes, public releases, and destructive ops require explicit human approval.  
5. **One primary owner per packet** — Parallel authors on the same packet only when they are *competing* tracks, not collaborative co-writing.  
6. **Spike or it didn’t happen** — A top-scoring design that skips the minimal experiment stays provisional.

---

## 7. What “optimal” is not

- Not the longest proposal  
- Not the proposal that cites the most papers without a spike plan  
- Not the proposal that wins a group-chat popularity contest  
- Not the average of all drafts (averaging often preserves every weakness)

Optimal means: **best under constraints, according to a pre-registered rubric, after a short attempt to break it.**

---

## 8. Minimal starter kit

For a new large question, create four artifacts and stop:

1. `brief.md` — problem, constraints, rubric, spike criteria  
2. `proposals/A.md`, `proposals/B.md` — independent drafts  
3. `reviews/` — objection notes keyed to rubric rows  
4. `decision.md` — filled rubric, recommendation, spike result, lock version

Everything else (slides, long essays, exploratory chat) is optional support material.

---

## 9. Summary

Treat AI agents as **parallel researchers plus a strict reviewer**, not as a committee that must agree. The human lead owns the brief and the final signature. Competition and rubrics create pressure; short experiments discard elegant nonsense. With that rhythm, large scientific questions can converge instead of diverging forever in shared chat.

---

## Changelog

- 2026-10-23: Initial methodology (generic multi-agent research orchestration).
