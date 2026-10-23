# Orchestrating AI Research Teams for Large Scientific Problems

A practical methodology for coordinating multiple AI agents (and human researchers) on open-ended research questions so that proposals converge on strong, testable solutions rather than consensus theater.

**Audience:** anyone running multi-agent research workflows (LLM agents, specialized bots, or mixed human–AI teams).  
**Scope:** process and governance only. Domain-specific architectures, products, and project names are intentionally omitted.  
**Method version:** 1.0 (2026-10-23). A run cites this version plus an immutable identifier (repository commit or file content hash) and executes under that version only (§10.1). Version 0 is every changelog entry before the 1.0 entry.

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
| **Adjudicator** | Fill the rubric, recommend / alternate / reject | Write proposal body text; author any candidate on the packet; run that packet's spike |
| **Experiment runner** | Execute the locked spike plan and return raw results | Change the goal mid-run; act outside the bounds in §12.2 |
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
- Authors must **not** see each other’s drafts during drafting. This is enforced by permissions, not requested by prompt (§11)  
- Deliverables go to a shared source of truth (repository or canonical doc), not only into chat. Drafts are sealed and published together (§11.2)

### Step 3 — Blind review (cross review)

- Reviewer A reviews B’s draft for holes and infeasibility  
- Reviews cite the rubric and the brief’s constraints  
- Reviewers do not rewrite the full document; they file objections  
- Reviews are written without sight of each other and published together (§11.2)

### Step 4 — Adjudication

- Adjudicator fills the same rubric for every candidate  
- **Eligibility before ranking.** Apply the gates first. A hard-constraint violation, or a conflict with a Locked Grade-1 claim, means **Reject**. A missing Locked Grade-2 role means **Incomplete**, which is not eligible for Recommend (Appendix B.5). The rubric ranks only eligible candidates. Scores on other rows never offset a gate failure.  
- **Independence.** The adjudicator authored no candidate on this packet and will not run its spike. With heterogeneous models, prefer an adjudicator from a model family that authored no candidate. If no such family is available, use one adjudicator per authoring family, each scoring every candidate (Appendix A.3).  
- **Stability.** Candidates are shown under neutral labels with model identity removed. Each adjudicator scores twice, with presentation order reversed.  
- **Tie.** The outcome is a tie if any of these holds: (a) the total-score margin is at most the tie margin declared in the brief (default: 10% of the maximum possible total); (b) the recommended candidate changes when order is reversed; (c) independent adjudicators recommend different candidates.  
- Output: **Recommend / Alternate / Reject**, plus one paragraph of rationale, plus a **Confounds** paragraph. Confounds lists every resource asymmetry, isolation risk, and amendment that touched the contest (§10, §11, A.5).  
- Ties go to the human lead; agents do not majority-vote

### Step 5 — Spike (minimal experiment)

- Only the recommended candidate gets a short empirical check  
- Success criteria for the spike are written in the brief or adjudication note  
- Raw logs / metrics are filed; narrative without data does not count as a pass  
- The spike plan is pre-registered and hashed before execution. The runner works within §12.2

### Step 6 — Lock

- Winning design is versioned in the canonical document, together with the method version it was decided under  
- In a multi-run program, the decision and its claims enter the program ledger by ID (§13)  
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
7. **Isolation is enforced, not requested** — If an auditor cannot show from artifacts that an author never saw a sibling draft, the packet's decision is capped at Provisional (§11).  
8. **One method version per run** — A run cites the method version it started under and keeps it to the end. Mid-run changes follow the amendment classes in §10.4.  
9. **Append-only evidence** — Logs are never overwritten. Every attempt, including failed ones, is kept (§12.4).

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

Runs that use more than one model, a wall clock, or more than one packet also need: `roster.md` (Appendix A.5), `method-issues/` (§10.2), an append-only `logs/` directory with a seal log (§11.2, §12.4), a `progress.md` state table (§13.5), and, for programs, a ledger (§13.2).

---

## 9. Summary

Treat AI agents as **parallel researchers plus a strict reviewer**, not as a committee that must agree. The human lead owns the brief and the final signature. Competition and rubrics create pressure; short experiments discard elegant nonsense. With that rhythm, large scientific questions can converge instead of diverging forever in shared chat. Appendix B states how to judge a claim by necessity, so a strong score cannot be promoted into a locked principle. Sections 10–13 cover real runs: versioning and mid-run amendment of the method itself, enforced isolation in shared workspaces, who may write which artifact, and programs that span many packets and wall-clock limits.

---

## 10. Method versioning and mid-run amendments

The method is itself a research object. Runs will find defects in it. This section says how a defect becomes an amendment without silently invalidating a contest that is already in progress.

### 10.1 Version and pinning

- The note carries a version `MAJOR.MINOR`. MAJOR increases when a rule in the freeze set (§10.3) or the role separation changes meaning. MINOR increases for added rules or clarifications that reverse nothing.  
- Each brief cites the method version and an immutable identifier: a repository commit, or a content hash of the file.  
- If the note may be edited while a run is active, the run's agents read a **pinned copy**, not the mutable path.  
- A run executes under exactly one method version. A newer version is adopted at the next packet boundary. Individual new rules may enter a running run only through §10.4.

### 10.2 Method issues

- Any participant in any role may file a method issue as `method-issues/ISSUE-NNN.md`. It contains: the observed defect; evidence (paths, log lines, timestamps, all of which must still exist at the cited path, §12.4); a proposed amendment; the amendment class (§10.4); and the contest impact.  
- The Orchestrator gives every issue a disposition before the run ends: *applied-in-run* (with class), *deferred-to-next-packet*, or *rejected* (with reason).  
- Filing is mandatory. A participant who observes a process defect and does not file it has failed a process requirement, even if the defect was worked around.  
- Between runs, the method maintainer (the human lead or a designee) turns accepted issues into edits of this note. Each edit gets a changelog entry citing the motivating issues, and a version bump. An amendment states the defect it fixes and the observation that would show it did not fix it.

### 10.3 Freeze set

When Step 2 starts, the following freeze for the packet:

- Brief text: problem, constraints, rubric (including aggregation and tie margin), spike criteria  
- Roster contract, including the adjudicator binding (Appendix A.5)  
- Author prompts, recorded by content hash  
- The set of files each author may read  
- Method version

The following do **not** freeze:

- Tooling and invocation mechanics  
- Logging  
- Scheduling, and retries with byte-identical inputs  
- Checks that only observe  
- What reviewers may object to

Time is recorded as epoch seconds or UTC. Local-time labels are display-only.

### 10.4 Amendment classes

| Class | Definition | Allowed mid-run? | Who decides |
|---|---|---|---|
| **0 — Infrastructure** | Changes how a step is executed, not what any participant sees or how anything is scored. Examples: fixing a command invocation or path; retrying with an identical prompt; a timebase note that leaves the deadline value unchanged | Yes, immediately | Orchestrator |
| **1 — Symmetric observation** | Adds a check, log, seal, or publication-order rule. It applies identically to all candidates and changes no author input and no scoring input | Yes | Orchestrator |
| **2 — Evaluation-affecting** | Changes the rubric, aggregation, tie rule, adjudicator, spike criteria, roster, or anything else that could change a score or the recommendation | Only if all three hold: (a) the affected step has not started; (b) the change applies identically to all candidates; (c) the human lead signs before that step starts. Otherwise it is deferred to the next packet | Human lead |
| **3 — Integrity breach** | A participant saw, or could have seen, information the contest denies it (a sibling draft, a competitor's reasoning, scores). Or an author's input changed after any competitor output existed | This is an event, not an option | Orchestrator reports; human lead rules |

How to record each kind of change:

- **Brief amendments (any class):** append to the brief as a dated `Amendment vN.M` block stating class and reason. Never edit the brief in place.  
- **Class 0 and 1 changes:** one line each in the run's amendment log.  
- **Class 3 (breach):** the human lead chooses one of two remedies. (i) Re-run the affected track from scratch, in a clean environment, with the original inputs. (ii) Continue with the packet's decision capped at Provisional and the breach disclosed under Confounds.

### 10.5 Contest-neutrality test

An amendment is contest-neutral, and therefore Class 0 or 1, only if all three of these checkable conditions hold:

1. No author's input changed after that author started. This covers the prompt hash, the readable file set, and the brief text. Appended Class-0 notes that change no constraint value are exempt.  
2. No scoring input changed: rubric, aggregation, tie rule, adjudicator binding, spike criteria.  
3. The change applies identically to all candidates.

If any condition fails, the amendment is Class 2 (if the affected step has not begun) or Class 3 (if it has).

### 10.6 Run retrospective

Every run ends, or pauses, with a short `retrospective.md` covering:

- issues filed and their dispositions  
- amendments applied, with class  
- breaches  
- planned versus actual step timings

The next brief's author reads it before writing.

---

## 11. Isolation in shared workspaces (preventing consensus theater)

Agreement only means something if it was reached independently. When agents share a filesystem, independence is a property of permissions and logs, not of instructions.

### 11.1 Enforced drafting isolation

- Each author drafts in its own directory, and the author's process cannot read sibling directories. Enforce this with filesystem permissions, separate checkouts, or a sandbox read-allowlist.  
- A prompt line such as "do not open other drafts" is **not** isolation.  
- If enforcement is impossible, cap the packet's decision at Provisional and record the gap under Confounds.

### 11.2 Seal and publish

- When an author finishes, record the draft's content hash and UTC time in an append-only seal log.  
- Drafts move into the shared `proposals/` directory only after **all** drafts are sealed (publish-after-all). Reviews follow the same rule.  
- If a sealed artifact's hash later changes, that is a Class 3 breach.

### 11.3 Orchestrator–author firewall

If the Orchestrator also authors on a packet:

- The prompt for its drafting process is fixed and hashed before any competitor output exists.  
- That process must not see competitor output (draft, log, or stdout) before its own draft is sealed.  
- After seeing competitor output, the Orchestrator authors nothing further for its own track on that packet. If rebuttals or revisions are needed, a fresh process does them, given only the published files.

### 11.4 Prompt parity

- Competing authors' prompts are instantiated from one template. File the diff between instances.  
- Instances may differ only in author identity, output location, and the roster settings declared in A.5. Reviewer prompts follow the same rule.

### 11.5 When agreement counts

Agreement between candidates counts as independent evidence only if both of these hold:

1. §11.1–§11.4 held, and that can be shown from logs.  
2. The agreed point is not stated or implied by the shared brief.

Agreement on a point the brief already frames (for example, an ordering supplied as context) is recorded as **framed agreement** and adds no weight. Each draft must name at least one serious alternative it rejected, with the reason. When drafts converge on the same conclusion and also reject the same alternatives, the adjudicator records that as possible framing-driven convergence.

### 11.6 Auditability

- Every agent process that can read files runs with tool-call logging enabled.  
- Before publication, run a breach audit: search each author's tool log for sibling paths. Zero hits are required.  
- If a process has no tool log, its isolation is recorded as **unauditable**, and §6 rule 7 applies.

---

## 12. Artifact write permissions

### 12.1 Who writes what

| Artifact | Writer | Notes |
|---|---|---|
| Brief | Orchestrator, before Step 2 | Afterwards: appended amendments only (§10.4). Class 2 needs human signature |
| `roster.md` | Orchestrator, before Step 2 | Frozen afterwards |
| Author drafts | That author, inside its own sealed directory, or by mechanical deposit (§12.3) | Nobody else reads them until publish-after-all |
| `reviews/` | Each reviewer, its own file | Published together |
| Scores in `decision.md` | The bound adjudicator(s) | The Orchestrator may format the file but not alter scores |
| `spikes/<id>/PLAN.md` | Orchestrator, before execution | Hashed into the seal log |
| `spikes/<id>/` (everything else) | Experiment runner | Code, configs, raw outputs, `runs.log`, `deviations.md`, `BLOCKED.md` |
| Claim records | Claim author proposes. State changes only per B.9 | |
| `method-issues/` | Anyone | New files only |
| `logs/` | Each process writes its own files | Append-only (§12.4) |
| Program ledger | Orchestrator, at lock or pause | Append-only (§13.2) |

Writing outside one's own rows is a process defect and must be filed (§10.2), even when it is harmless.

### 12.2 Experiment runner: when it may touch code

**Input.** A `PLAN.md`, written and hashed before the runner starts. It states:

- the mechanism under test  
- the metric and threshold  
- seeds or trials  
- the maximum number of attempts  
- the control or null condition, if any  
- the exact command  
- the output format

**May:**

- write harness code, environment setup, instrumentation, and data plumbing  
- fix defects so the code does what `PLAN.md` says

**Must not:**

- change the mechanism under test, the metric, the threshold, the seed or trial count, the attempt cap, or the pass rule  
- choose which runs to report  
- edit the brief, rubric, decision, or claim records  
- write outside `spikes/<id>/` and its own logs

**Bug fix or design change?** A change is a bug fix only if `PLAN.md`, read literally, already specifies the corrected behavior. Anything `PLAN.md` does not specify is a **plan gap**. The runner then stops and writes `BLOCKED.md`. The Orchestrator either amends `PLAN.md` before any further execution (Class 2 for that spike, logged) or caps the decision at Provisional.

**Every run is reported.** Each execution is appended to `runs.log` with the command, the code hash, the seed, and the result. The harness computes the verdict against the pre-registered threshold and prints it machine-readably. Prose never overrides it.

**Limits on the runner's role:**

- It may file data that supports a challenge (B.9), but it does not change claim state.  
- It is not an adjudicator of the packet whose spike it runs.  
- It receives `PLAN.md`, not the adjudication reasoning.

### 12.3 Deposits and transcripts: when the Orchestrator may write on another agent's behalf

**Deliverable deposits.** These are allowed only when the producing agent's sandbox prevents it from writing.

- The raw output stays unmodified in `logs/`.  
- The deposited file comes from a pre-declared mechanical extraction rule, for example "from the first line matching the required heading to the end of the final message". It is never produced by a model retyping, cleaning up, or summarizing.  
- Hashes of both the raw output and the deposited file go into the seal log.  
- If the depositor must stay blind to the content (§11.3), the deposit runs as a script, and the content never enters the depositor's context.

**Transcripts.** The Orchestrator may deposit any agent's raw transcript into `logs/` at any time.

- Transcripts are evidence, not deliverables. A transcript never substitutes for a missing deliverable.  
- Nobody else's deliverable may be reconstructed from a transcript, except by the mechanical extraction rule above.

### 12.4 Logs and evidence

- Use one file per process attempt (for example `<step>-<role>-attempt<N>`). Never truncate or reuse one. Keep failed attempts.  
- Evidence cited by an issue or a decision must exist at the cited path when the run ends.

---

## 13. Long-horizon programs

A **program** is a sequence of runs, and each run contains one or more packets. Programs fail differently from contests. Decisions get paraphrased across briefs. Provisional results get stacked on each other. Locks get retired while their dependents stay in place. Wall clocks cut steps in half.

### 13.1 Unit hierarchy

| Unit | Owns |
|---|---|
| Program | One ledger |
| Run | One brief, one pinned method version, one progress file |
| Packet | One decision |

### 13.2 Program ledger

The ledger is an append-only record at program level. Its entries have stable IDs:

- **Decisions** (`D-…`): status (Locked / Provisional / Rejected / Superseded); method version; run id; decision-file hash; `depends_on` (list of IDs); spike status.  
- **Claims** (`C-…`): grade; state (Candidate / Locked / Challenged / Retired); premises; scope; falsifier; scope-narrowing count (B.9); history.  
- **External conclusions adopted as context** (`X-…`), such as prior reviews or literature: source, what it asserts, who adopted it.

Entries are never edited. A change is a new entry that `supersedes` the old one.

### 13.3 Inheritance across packets

- A new brief names the ledger snapshot it inherits (a hash or the last entry ID) and cites inherited items **by ID**.  
- Restating an inherited item in prose without its ID is not allowed, because paraphrase is where drift enters.  
- How each inherited item binds the new packet:

| Inherited item | Binds as |
|---|---|
| Locked decision or Locked claim | A constraint |
| Candidate claim | Guidance only, with no veto |
| Provisional decision | An explicit assumption, listed in the brief as such |

- **Provisional cap.** A packet may depend on Provisional decisions only to depth 1. It may not build on a Provisional decision that itself depends on another Provisional decision. Raising the cap requires the human lead's signature in the brief.  
- Inherited decisions keep the method version they were made under. A MAJOR method bump appends a "re-review due" entry for each affected item. Nothing is re-adjudicated automatically.

### 13.4 Dependency propagation

When an entry becomes Challenged (admitted, B.9), Superseded, or Retired:

- Every entry whose `depends_on` includes it gets an **at-risk** entry in the ledger.  
- No new packet may build on an at-risk item until it is re-confirmed or re-decided.

### 13.5 Pause, resume, and wall-clock limits

**Before the run**

- Each step has a done-predicate: the artifact exists, is non-empty, has the required headings, and its hash is sealed.  
- Each step has a time budget set in the brief.  
- The brief names the degraded outcome for every step that may be skipped. Example: no spike execution means a spike plan only, and the decision is Provisional.

**During the run**

- A step does not start if the remaining wall clock is less than its budget.  
- `progress.md` is a state table. Each step is in one of these states: PENDING; RUNNING (attempt, start epoch); DONE (hash); SKIPPED (reason); ABORTED (reason).  
- Before each agent call (preflight): check the input is non-empty and log its hash.  
- After each call: check the output satisfies the done-predicate. A failed check is a logged failed attempt, never a silent retry.

**At pause**

- Start no new calls.  
- A RUNNING step may finish only within its budget. Otherwise it is stopped and marked ABORTED.  
- Partial outputs stay in `logs/` and are never published.  
- Flush `progress.md`.

**At resume**

- RUNNING and ABORTED steps re-run from scratch with byte-identical inputs, under a new attempt number. A partial output is never continued in a new context.  
- Resumed agents rebuild context only from files.  
- The resumed run keeps its pinned method version, even if the note has changed in the meantime.

---

## Appendix A — Heterogeneous model roster (optional)

When several different AI systems (or model families) work the same research problem, keep the six-step cycle in §4 unchanged. Add only a **fixed role roster** so authorship, critique, execution, and judgment stay separated.

### A.1 Three slots (do not merge)

| Slot | Duty | Typical fit | Must not |
|---|---|---|---|
| **Orchestrator** | Write the brief and rubric; assign packets; fill the adjudication table (unless it authored on the packet); lock the decision | Strongest at long-horizon planning, structured writing, and process fidelity | Adjudicate a packet on which it authored a candidate; break the firewall in §11.3 |
| **Competing author** | Produce an independent proposal (and/or red-team another draft) under the same brief | Strong at broad synthesis, alternate framings, and finding holes | See the other author’s draft during drafting; rewrite the rubric mid-contest |
| **Experiment runner** | Implement the spike for the *recommended* candidate; return raw logs and metrics | Strong at coding, repo edits, and running scripts | Change goals, rewrite `decision.md`, fill or alter rubric scores on a packet whose spike it runs, or act outside §12.2 |

You may rename the slots. You may swap which model sits in which slot across *different* packets. You may **not** collapse two slots into one agent on the same packet.

If the Orchestrator authors on a packet, the roster (A.5) names a separate **adjudicator binding** for that packet. The binding is chosen under §4 Step 4. Neither the Orchestrator nor the Experiment runner may be it.

### A.2 Default binding pattern

For a high-stakes subproblem:

1. Orchestrator publishes `brief.md` (problem, constraints, rubric, spike criteria) and `roster.md` (A.5).  
2. At least two competing drafts: one from the Orchestrator track (or a domain specialist) and one from a **different** model family in the Competing-author slot. Drafts are isolated until review (§11). If the Orchestrator track drafts, §11.3 applies.  
3. Cross red-team: each side files objections keyed to rubric rows.  
4. The bound adjudicator(s) adjudicate under §4 Step 4 (Recommend / Alternate / Reject). The Orchestrator adjudicates only if it authored no candidate on this packet. Ties go to the human lead.  
5. Experiment runner implements only the recommended spike; artifacts go to the shared source of truth.  
6. Orchestrator locks the versioned `decision.md`. Spike failure returns to brief amendment or the alternate candidate — the runner does not redefine the goal on the fly.

### A.3 Extra hard rules for multi-model teams

1. **Model diversity is a competition requirement**, not a nice-to-have — when stakes are high, require at least two drafts from different model families.  
2. **Physical draft isolation** — separate directories or branches, with no read permission across them and no shared scratch chat for Step 2 drafting. See §11 for enforcement, sealing, and audit.  
3. **Execution ≠ judgment** — the Experiment runner may write code only under the spike directory and only within §12.2, and it deposits raw results there. Only the Orchestrator (or human lead) may edit the brief, the rubric, or `decision.md`. Only the bound adjudicator fills scores.  
4. **No dual hat on one packet** — the model that authored a proposal must not adjudicate that packet. A model from an authoring *family* may adjudicate only in the arrangement of §4 Step 4: one adjudicator per authoring family, every candidate scored by each, and disagreement treated as a tie.  
5. **Human gate unchanged** — paid compute, production changes, and public releases still need explicit human approval.  
6. **Judge ≠ executor** — the adjudicator of a packet does not run that packet's spike. The runner receives the pre-registered plan, not the adjudication reasoning.  
7. **Roster contract frozen** — the A.5 contract is recorded before Step 2 and is part of the freeze set (§10.3).

### A.4 What not to change

The brief-first rubric, blind review, minimal spike, single source of truth, and human final authority remain exactly as in the main methodology. Heterogeneity only binds *who* fills each role, and with what settings (A.5). Appendix B adds a Principle track with its own roles, bound in B.9. That track is an addition to the cycle, not a replacement for any step.

### A.5 Roster contract (models, effort, tools)

With heterogeneous models, a slot is bound to a *configuration*, not just a model name. Reasoning budget, tools, and readable context change outputs as much as model choice does. Record `roster.md` before Step 2, with these fields for each slot:

| Field | Example content |
|---|---|
| Role and packet | Competing author, packet P |
| Model family and exact model identifier | as reported by the tool |
| Reasoning / effort setting | the vendor's named level |
| Limits | output tokens, turns, wall-clock cap |
| Tools enabled | file read, file write, shell, network |
| Sandbox | mode, readable roots, writable roots |
| Invocation | exact command template, and how the prompt is delivered |
| Prompt | template id and instance hash (§11.4) |
| Context files given | list |

Rules:

1. **Actual over intended.** Record the settings the tool itself reports in its run header or log. Any mismatch with the contract goes into the decision's Confounds paragraph.  
2. **Parity among competing authors.** Competing authors get the same wall-clock cap, the same readable context, and the same affordances (for example, all write files, or all are deposited mechanically). Effort labels are vendor-specific and not commensurable. Pick one rule for all authors, such as "each family's highest generally available setting", and apply it to every author.  
3. **Declared handicap.** If parity is impossible, the brief declares the asymmetry before Step 2. The adjudicator repeats it under Confounds. An undeclared asymmetry discovered later is filed as a method issue.  
4. **Substitution.** If a model is unavailable or fails irrecoverably, replacing it is a roster change. The slot is re-run from scratch with the substitute; no partial reuse. For an author slot after any competitor output exists, the Class 3 rules of §10.4 apply.  
5. **Frozen.** The contract freezes at Step 2 (§10.3). An invocation fix that leaves every field above unchanged is Class 0.

---

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

- 2026-10-23: Initial methodology (generic multi-agent research orchestration).
- 2026-10-23: Appendix A — optional heterogeneous model roster (Orchestrator, Competing author, Experiment runner) for multi-model role separation.
- 2026-10-23: Appendix B — Principle necessity protocol (necessity grades, principle versus performance tracks, minimal claim artifacts).
- 2026-10-23: Appendix B.4 — claim lifecycle (Candidate, Locked, Challenged). Scores may open a challenge; they do not promote or rewrite a lock.
- 2026-10-23: **v1.0.** Version header and pinning (entries above are v0). New §10: method issues, freeze set, amendment classes 0–3, contest-neutrality test, run retrospective. New §11: enforced isolation, seal and publish-after-all, Orchestrator–author firewall, prompt parity, conditions under which agreement counts. New §12: write-permission matrix, Experiment-runner code bounds, mechanical deposits and transcripts, append-only logs. New §13: program ledger, inheritance by ID, provisional cap, dependency propagation, pause/resume, step budgets. §4 Step 4: gates before ranking, independent and order-swapped adjudication, tie definition, Confounds paragraph. §6 rules 7–9. Appendix A: Orchestrator–adjudicator contradiction resolved, A.3 rules 6–7, new A.5 roster contract (model, effort, tools, parity). Appendix B: operational Grade-2 realization, challenge admissibility, new B.8 (capability ladders) and B.9 (claim governance). Motivated by process defects found in a live run: isolation enforced only by prompt, failure evidence overwritten on retry, an unversioned brief amendment, adjudicator role conflicts, and unequal author resources.
