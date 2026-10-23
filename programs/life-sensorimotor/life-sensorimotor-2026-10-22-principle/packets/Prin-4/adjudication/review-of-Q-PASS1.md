# Prin-4 — Blind review of Proposal B (reviewer: A, Claude Opus)

**Scope of review.** I read `proposals/B.md`, `source/packet-brief.md`, `source/method-Appendix-B.md` and the run `brief.md` rubric. To check B's factual statements I also read the other supplied sources (`Prin-3-decision.md`, `Eng-2-decision.md`, `program-ledger-current.md`), `roster.md`, `claims/C-P1-001/claim.md` and the C-P1-001 row of `packets/Prin-1/decision.md`. I did **not** read `proposals/A.md` or `drafts/A/`. This review does not adjudicate. It changes no claim grade, state, narrowing count or ledger row.

## 1. Gates (B.9.5, applied before scoring)

| Gate | Finding | Risk |
|---|---|---|
| Conflict with a Locked Grade-1 claim (B.5.1) | None. No Locked claims exist. B asserts no lock and says plainly that a lock needs a verifier, an adjudicator and a human signature. | **Reject: none** |
| Missing Locked Grade-2 role (B.5.2) | No Locked Grade-2 roles exist. B proposes no new role-realizing design. | **Incomplete: none** |
| Grade-3 used as law / ladder order as evidence (B.8.3, B.8.7) | None. B says its priority list is "an allocation of research effort, not a sensorimotor necessity ladder", and repeats this in its Non-claims. C-P1-003 and the C-Prin2-E* claims stay quarantined under D-Prin-2-001. | none |
| Candidate used as veto (B.4) | None. B says C-Eng2-A-01 "cannot become a gate by appearing in this table", and C-Eng1-A-01 gets "no veto authority". | none |
| Score or spike changing a grade (B.4, B.8.4, B.9.8) | None. B repeats the Prin-3 limits: a FAIL is sufficiency-level only, and SUB_DOWN_NOT_MET does not show that effort information is absent. B says a failed counterexample search would not discharge the proof obligation. | none |
| Model agreement counted as grade evidence (B.9.7) | B handles this correctly. It says "a cross-family re-derivation alone is not one of these routes". This matters because the only verification on record is the Opus adjudicator's re-derivation of L*. | none |
| Eng-2 gate / human authority | Respected. B does not clear the `(q,r)` gate or the measurement-point gate, and it does not choose a branch. It also points out that the ledger's wording "PLAN sealed in drafts" does not clear D-Eng-2-001's seal preconditions. That is a useful catch. | none |
| Packet-brief constraints | No Locked Grade-1. D-P1-001 stays Provisional. D-Prin-2-001 provides no edge gate. No spike is run. No named platform appears. | none |

**Gate verdict: ELIGIBLE.** I found no reject trigger and no incompleteness trigger.

## 2. Principle integrity

This is strong, and it is B's main strength.

- **Provenance is checked, not assumed.** `claims/C-P1-001/claim.md` still says "Candidate-stay; obtain independent proof verification before considering recommended-for-lock". The Prin-1 ruling and the ledger say "recommended-for-lock (conditional)". B notices the mismatch and asks the authorized adjudicator to reconcile it in the dossier. B does not pick a side. This is the correct way to handle it.
- **Roles are bound correctly.** C-P1-001 was authored by Astra. Per the roster, its claim adjudicator is Opus. B correctly says that B, as an Astra author, cannot adjudicate its own claim.
- **Necessity and sufficiency stay separate throughout.** Examples: target-plant validation is "not a prerequisite for a narrowly scoped fixture lock". A lock would not establish architecture, stage order, control frequency or safety. A competent role-free alternative can support a falsifier referral for C-P1-012, but a weak alternative does not prove the role obligatory.
- **The B.9.6 discipline is followed.** B keeps the C-P1-012 narrowing count at 1 and refuses to rule on whether its own amendments are exempt.

One small weakness: B lists B.9.2 routes in the abstract but does not apply them to this proof. The C-P1-001 derivation is a closed-form solution of a linear scalar ODE (Δ̇ = aΔ + 2D) plus one inequality. That makes the qualified-human route, or a small formal-checker encoding, very cheap. A short statement that the proof object is elementary would have made the route recommendation concrete without overclaiming. This affects calibration only, not integrity.

## 3. Soundness of the lock path (packet decision 1)

The seven-row checklist covers B.9.2 for Grade 1 in full:

1. **Exact object.** Version/digest, premises, conclusion, scope and falsifier.
2. **Allowed independent check.** One of the three routes, with provenance recorded.
3. **Scope correspondence.** The fixture only. Target-plant use needs its own premise match.
4. **Objections.** Logged to violations/upgrade-log; any narrowing is counted.
5. **Adjudicator disposition.** By the roster-bound Opus adjudicator.
6. **Human signature.** Tied to the exact version. B notes that "a signature alone is not proof review".
7. **Recording.** Done by an authorized process, with history preserved.

Strengths:
- Row 1 (a version digest that every verification artifact must reference) is not stated in B.9.2, but it is needed so the check, the ruling and the signature all attach to the same text. It is a good addition.
- B separates the human *reviewer* qualification from the human lead *signature*. That prevents the two from being merged into one step.
- B's fallback is "submit a precise outstanding-obligations dossier". That is honest given the wall clock, and it does not let more model votes stand in for a check.

Objections:
- **O1 — No batching with other narrow formal cores.** Prin-1's decision item 1 asks for a B.9.2 check for C-P1-001 "and narrow C-P1-010/011 cores". C-P1-010 Part A is recorded as formal. B puts C-P1-010 at priority 4 and C-P1-011 at priority 2 as a side-channel audit. It does not suggest sending C-P1-010 Part A to the same verifier in the same dossier, which costs little extra. This is a missed efficiency, not an error.
- **O2 — The B.9.2 route is not picked.** "Identify one available verification route" leaves the choice open. Given the deadline, B could have said which route it expects to be fastest, and what the dossier should contain if a qualified human cannot be found before the deadline. Minor.
- **O3 — Premise 6 is left implicit.** The claim record says the |u|≤3 actuator bound "is not used in the impossibility proof". A verifier should confirm that it can be dropped without effect. Row 3 (scope correspondence) does not mention this. It would be good to list it as a named item in the dossier. Minor.

The lock path is **sound**. Nothing in it asserts completion, and every row names who is responsible.

## 4. Priority list as planning, not necessity (packet decision 2)

- **Framing is correct.** B states its ranking criterion: "decision value and independence from missing human inputs". It filters out ineligible work before ranking, which mirrors gates-before-ranking. It also says the list is "an engineering research priority, not evolutionary, developmental or logical precedence among S0–S7". This meets B.8.3 and B.8.6.
- **Each priority has an exit condition.** Every row has a stopping rule and a dependency. This is the stopping-rule advantage B claims in its thesis.
- **O4 — Priority 1 does not fit B's own criterion well.** B ranks by "independence from missing human inputs". Priority 1 depends most on an external human, either the qualified reviewer or the signatory. The stopping rule ("stop at a … named missing verifier") limits the cost, so the ranking can be defended on decision value. But B should say that priority 1 ranks first *despite* this dependency, and that priorities 2–3 run in parallel while it waits. As written, the list reads as strictly sequential.
- **O5 — Priority 2 is three audits in one.** The C-P1-011 side-channel inventory, the pooled-window independence premise of C-Eng1-A-01, and the ceiling assumptions of C-Eng2-A-01 are separate audits. Each needs its own cross-family adjudicator binding. C-Eng2-A-01 is Opus-authored, so it needs an Astra adjudicator. With roughly an hour of wall clock left, bundling them risks an unfinished deliverable. B should either rank the three internally or name a minimum deliverable (e.g., C-P1-011 first). B does say C-P1-011 goes first, which partly answers this.
- **The case for priority 2 is good.** B argues that "detector failure vs privileged-information ceiling vs exported-channel limit answer different questions". Settling which question each artifact answers before any Eng-2 data arrives raises the value of the gated spike. That supports ranking it ahead of C-P1-012 interpretation work.
- **Priority 3 does not loosen anything.** B drafts the C-P1-012 evidence-to-action table prospectively, carries over the D-Prin-3-001 and D-Eng-2-001 interpretation limits, and adds "no extra narrowing to make existing failures disappear". Correct.

## 5. Retire / leave (packet decision 3)

"Retire-nominate now: none" is justified on the record. There is no new counterexample and no third narrowing event. B correctly calls this "an evidence-limited disposition, not a finding that every Candidate is sound". Every claim group gets a revisit trigger. The C-P1-012 trigger covers both falsifying factors and the third narrowing event, and notes that retirement is not automatic. B also says that missing Eng-2 data "is a reason to leave the empirical question open, not to retire the claim or loosen its tests". I agree with all of this.

Minor: B does not say whether any quarantined Grade-3 C-Prin2-E* edge has been quarantined long enough, with no upgrade path, to be worth tidying up. B.2 allows Grade 3 to stay as inspiration indefinitely, so this is optional.

## 6. Rubric scores (1–5)

| Dimension | Score | Rationale |
|---|---|---|
| Constraint fit | **5** | All hard constraints and packet-brief limits are respected, and the non-claims are explicit. |
| Principle integrity | **5** | Grades stated. Necessity and sufficiency kept separate. Provenance mismatch flagged. Role bindings and B.9.7 handled correctly. |
| Falsifiability | **3** | No spike is required. Each step has an exit or stop condition that can resolve within the run (dossier ready/not-ready). But no checkable counterexample search or verification output is scheduled. Appropriate for a planning packet, but there is little here that can fail within days. |
| Evidence demand | **5** | Documentation and one external check only. No compute or hardware. |
| Failure modes | **4** | Names repeated model votes, silent repair, scope creep and gate leakage. The deadline-driven failure of an unfinished, bundled priority 2 is under-addressed (O5). |
| Integrability | **4** | Clear owners for each role: author, adjudicator, verifier, human. Body-loop vs scene vs decision-core ownership does not really apply to this packet. |
| Latency / criticality | **4** | Correctly says C-P1-001 implies no control frequency or tier. Little else here bears on this dimension. |
| Complexity cost | **4** | Lean overall. The seven-row checklist is justified. Priority 2's three-way bundle adds some coordination cost. |
| Reversibility | **5** | Every action is a dossier or a draft. Nothing irreversible happens before the human signs. |
| Stackability | **4** | The information-access audit makes Eng-2 results interpretable without needing them early. Batching C-P1-010 Part A (O1) would make this stronger. |

**Total: 43 / 50.**

## 7. Requested amendments (non-binding; for the adjudicator)

1. Say explicitly that priority 1 is ranked by decision value despite its dependency on a human, and that priorities 2–3 run in parallel while verification is pending (O4).
2. Add C-P1-010 Part A, and the C-P1-011 core if it is narrow enough, to the same B.9.2 verification dossier, as Prin-1 decision item 1 asked (O1).
3. Split priority 2 into ranked sub-deliverables, each with its own cross-family adjudicator binding, and name a minimum deliverable that can be finished before the deadline (O5).
4. List the premise-6 (actuator bound unused) correspondence as a named verifier item (O3). Optionally, name the route expected to be fastest (O2).

None of these affects eligibility.

DONE
