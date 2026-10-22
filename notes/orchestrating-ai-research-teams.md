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

## Appendix A — Heterogeneous model roster (optional)

When several different AI systems (or model families) work the same research problem, keep the six-step cycle in §4 unchanged. Add only a **fixed role roster** so authorship, critique, execution, and judgment stay separated.

### A.1 Three slots (do not merge)

| Slot | Duty | Typical fit | Must not |
|---|---|---|---|
| **Orchestrator** | Write the brief and rubric; assign packets; fill the adjudication table; lock the decision | Strongest at long-horizon planning, structured writing, and process fidelity | Author *and* finally score its own proposal on the same packet |
| **Competing author** | Produce an independent proposal (and/or red-team another draft) under the same brief | Strong at broad synthesis, alternate framings, and finding holes | See the other author’s draft during drafting; rewrite the rubric mid-contest |
| **Experiment runner** | Implement the spike for the *recommended* candidate; return raw logs and metrics | Strong at coding, repo edits, and running scripts | Change goals, rewrite `decision.md`, or alter rubric scores |

You may rename the slots. You may swap which model sits in which slot across *different* packets. You may **not** collapse two slots into one agent on the same packet.

### A.2 Default binding pattern

For a high-stakes subproblem:

1. Orchestrator publishes `brief.md` (problem, constraints, rubric, spike criteria).  
2. At least two competing drafts: one from the Orchestrator track (or a domain specialist) and one from a **different** model family in the Competing-author slot — drafts isolated until review.  
3. Cross red-team: each side files objections keyed to rubric rows.  
4. Orchestrator adjudicates (Recommend / Alternate / Reject). Ties go to the human lead.  
5. Experiment runner implements only the recommended spike; artifacts go to the shared source of truth.  
6. Orchestrator locks the versioned `decision.md`. Spike failure returns to brief amendment or the alternate candidate — the runner does not redefine the goal on the fly.

### A.3 Extra hard rules for multi-model teams

1. **Model diversity is a competition requirement**, not a nice-to-have — when stakes are high, require at least two drafts from different model families.  
2. **Physical draft isolation** — separate directories or branches; no shared scratch chat for Step 2 drafting.  
3. **Execution ≠ judgment** — the Experiment runner may change code and deposit results; only the Orchestrator (or human lead) may edit the brief, rubric, or `decision.md`.  
4. **No dual hat on one packet** — the model that authored a proposal must not be the sole final adjudicator of that same proposal.  
5. **Human gate unchanged** — paid compute, production changes, and public releases still need explicit human approval.

### A.4 What not to change

The brief-first rubric, blind review, minimal spike, single source of truth, and human final authority remain exactly as in the main methodology. Heterogeneity only binds *who* fills each role.

---

## Changelog

- 2026-10-23: Initial methodology (generic multi-agent research orchestration).
- 2026-10-23: Appendix A — optional heterogeneous model roster (Orchestrator, Competing author, Experiment runner) for multi-model role separation.
