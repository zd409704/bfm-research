# Prin-4 — Adjudication score, PASS1

**Adjudicator:** Packet Adjudicator (Sonnet). Did not author either proposal.
**Inputs read:** `proposal-P-PASS1.md`, `proposal-Q-PASS1.md`, `review-of-P-PASS1.md`, `review-of-Q-PASS1.md`, `source/packet-brief.md`, `source/method-Appendix-B.md`, run `brief.md` rubric. I also read `source/Eng-2-decision.md` and `source/Prin-3-decision.md` for context. I did not read the PASS2 files, so PASS1 stands as an independent first pass.
**Effect on claims:** none. This document changes no claim grade, state, narrowing count or ledger row. Inherited by ID, authority unchanged: D-P1-001 (Provisional), D-Prin-2-001 (no edge gates), D-Prin-3-001 (Eng-2 spike gate unchanged), D-Eng-2-001, X-Eng-1-001.

## 1. Gates (Appendix B, applied before ranking)

| Gate | P | Q |
|---|---|---|
| Locked Grade-1 without human (Hard Reject) | Clear. Says the claim stays Candidate until the human lead signs. | Clear. Same. Human signature is tied to the exact claim version. |
| Grade-3 used as necessity (Hard Reject) | Clear. C-P1-003 stays quarantined. | Clear. Same. |
| Planning priority treated as necessity order, B.8.3 (Hard Reject) | Clear. The list is labelled planning only and creates no Eng-2 precondition. | Clear. The list is labelled an effort allocation and is not a ladder. |
| Candidate used as a veto, B.4 | Clear. | Clear. States that C-Eng2-A-01 cannot become a gate. |
| Score or spike moves a grade, B.8.4 / B.9.8 | Clear. | Clear. |
| Model agreement counted as grade evidence, B.9.7 | Clear. Explicitly excludes its own arithmetic check and the adjudicator's re-derivation. | Clear. Explicitly excludes cross-family re-derivation. |
| C-P1-001 lock-path skips B.9.2 cross-family verification or the human signature step (Incomplete) | Clear. Checklist C2 requires one of the three allowed routes. C10 binds a non-author adjudicator. C11 requires the human signature. | Clear. The seven rows cover the exact object, the allowed check, scope, objections, a non-author adjudicator disposition, the human signature and an authorized recording step. |

**Verdict:** neither proposal triggers Hard Reject or Incomplete. Both are eligible for ranking.

**Qualifications on P's lock path.** These are amendments, not gate failures.
- P's closing sequence names the human signature as the last step, but it has no step where the non-author adjudicator records the transition after the signature. The adjudicator appears only in C1 and C10. Signature must not look sufficient by itself.
- The review flags that route (b), published-result match, as written only covers the ODE solution identity. It does not cover the whole impossibility argument.
- P calls mechanization "cheapest" with no cost basis.
- P labels the C3 premise confirmations "precision only", but several of them could change scope or quantifiers.

## 2. Rubric scores (1–5)

| Dimension | P | Q | Objection behind any score ≤3 |
|---|---:|---:|---|
| Constraint fit | 5 | 5 | |
| Principle integrity | 4 | 5 | P states "grade stays 2 until B.9.2 is met", which mixes grade with lock state. P also asserts "No Candidate has met a retire trigger" and "not narrowed" for C-P1-001 after saying it did not read the histories (C9 is still *confirm*). |
| Falsifiability | 3 | 3 | P's rank-3 identifiability upgrade has no admissible model class, so it has no defined counterexample. Q has no checkable output beyond a ready/not-ready dossier and drafts. This is acceptable for a no-spike planning packet but gives little that can fail within days. |
| Evidence demand | 4 | 4 | Both are desk work. P's cost claim for formalization is unsupported. Q's priority 2 bundles three audits. |
| Failure modes | 4 | 4 | P handles fixture-versus-target transfer and delay-versus-interval conflation well. Q handles silent repair and gate leakage. Q does not address the deadline risk of its bundled priority 2. |
| Integrability | 4 | 4 | |
| Latency / criticality | 5 | 4 | Q does state that the lock implies no control rate or tier. P does more to separate the common-input interval from measured delay. |
| Complexity cost | 4 | 4 | |
| Reversibility | 4 | 5 | |
| Stackability | 4 | 4 | |
| **Total** | **41** | **42** | |

The margin is one point. The scores support "Q slightly ahead on Principle discipline and lock-path completeness". They do not support "Q clearly better".

## 3. Recommendation (planning only; no claim state change)

### 3a. C-P1-001 lock-path

- **Q: Recommend.**
- **P: Alternate.**
- **Reject: none.**

Q's seven rows are the more complete B.9.2 route. They add a version or digest of the exact claim, separate the qualified human reviewer from the human lead's signature, include a non-author adjudicator disposition, and record the transition through an authorized process. Q also catches that the ledger's "PLAN sealed in drafts" wording does not satisfy D-Eng-2-001's seal preconditions.

**Mandatory amendments** (apply before the lock path is executed or cited):
1. **Reconcile the record.** `claim.md` says Candidate-stay pending verification. The ledger says recommended-for-lock (conditional). The bound adjudicator appends a note, without rewriting history, that names the governing state and lists the conditions behind "conditional".
2. **Choose one allowed B.9.2 route.** The check must cover the whole final statement, not only the solution formula: the common-input premise, the paired disturbance construction, the triangle bound, the horizon and the quantifiers. Do not call formalization "cheapest" without an estimate. Keep published-result match available only if an established result covers the conclusion.
3. **Name the premise-6 correspondence** (actuator bound unused in the proof) as a verifier item.
4. **Add the veto-scope paragraph** from P's C5 to the signing package: fixture only, no target-plant route vetoed without a separate premise match. Carry P's C6 as well: a measured delay is not the common-input interval.
5. **Treat P's C3 confirmations as potential scope changes.** Compare each with the current claim text and log any premise addition under B.9.6. Verification applies to the final statement.
6. **State the B.9.6 narrowing count**, classifying the Prin-1 expansion as a clarification or a narrowing event.
7. **Use this closing sequence.** Reconcile the record. Verify the exact statement. Assemble the package, including the irreversibility notice. Obtain the human signature. Then the non-author adjudicator records the transition.
8. **Optional batching.** If a qualified verifier is found, consider sending the narrow formal core of C-P1-010 Part A in the same dossier, as Prin-1 asked.

Until signed, every artifact says Candidate. No artifact says Locked.

### 3b. Principle priorities while Eng-2 is gated (planning order, not necessity; B.8.3)

- **Q: Recommend**, with the amendments below.
- **P: Alternate.** Keep its audit-first idea for C-Eng2-A-01 and its identifiability work as parallel items.
- **Reject: none.**

Proposed merged order. It is a planning order only, it is not evidence, and it adds no precondition to Eng-2 beyond D-Prin-3-001's existing gate:
1. **C-P1-001 dossier.** Rank it first on decision value despite its dependency on a human reviewer and signatory. Run items 2–4 in parallel while verification is pending.
2. **Information-access and certificate-premise audit.** Split it into ranked sub-deliverables, each with its own non-author, cross-family adjudicator binding. The minimum deliverable that can be finished within the wall clock is the C-P1-011 side-channel inventory. After that come C-Eng2-A-01 and C-Eng1-A-01. P ranks the C-Eng2-A-01 ceiling audit first; either order is acceptable if the bindings are recorded.
3. **C-P1-012 prospective evidence-to-action table.** Q's version. It stays a draft, and the grade stays Candidate.
4. **C-P1-012 identifiability upgrade attempt.** This is P's rank 3, kept as an optional parallel item. It needs an explicit admissible model class, two decompositions that give identical allowed observations, and a stated refuter. File any counterexample search under a PLAN (B.9.8).
5. **C-P1-002 and C-P1-010 target premise matches.** Template drafts only until the human declares the effort measurement point.
6. **Prin-2 edge claims.** Dormant. Revisit only if a proposal cites an edge.

### 3c. Retire / leave

Both proposals nominate no retirement, and I agree. The evidence supports this only as "no retirement is justified by the materials inspected". It is not a finding that no trigger has fired. Neither author read the C-P1-001 `upgrade-log.md` or `violations.md`, and I did not either.
- Narrowing counts stay attributed. The C-P1-012 count of 1 comes from Prin-3 claim adjudication.
- At a third narrowing event B.9.6 requires a retirement review, not automatic retirement.
- Missing Eng-2 data is a reason to leave the question open. It is not a reason to retire a claim or loosen its tests. An Eng-1 FAIL and SUB_DOWN_NOT_MET are sufficiency-level evidence only.
- Quarantined Grade-3 notes (C-P1-003 and the C-Prin2-E* set) stay quarantined. Retiring one would not mean it was refuted.

## 4. Claim IDs needing follow-up (list only)

C-P1-001; C-P1-010; C-P1-011; C-P1-012; C-P1-002; C-P1-003; C-Eng1-A-01; C-Eng2-A-01; C-Prin2-E*

## 5. Confounds

- **Order-swap not completed.** This is PASS1 only. The recommendation is provisional until PASS2 with swapped labels agrees. If PASS2 disagrees, report the split and take no step on the disputed item until it is resolved.
- **Position and label bias.** The 1-point margin is small enough to be within position effect. Do not treat it as a decisive ranking.
- **Asymmetric review inputs.** The reviewer of Q read extra sources (the other decision files, the roster, the C-P1-001 claim and the Prin-1 ruling). The reviewer of P read only the packet files. This lets Q's reviewer check more of Q's factual statements.
- **Reviewer strictness differs.** One review was more demanding on process detail (41 against 43). Review scores are inputs, not substitutes for the gates.
- **Unequal source depth.** Neither author read the claim histories, so factual statements about retire triggers and narrowing counts rest on the same unverified basis for both.
- **Family overlap.** The adjudicator shares a model family with one of the authors. Self-preference is possible and is not controlled here.
- **Size.** The two proposals differ by about 4% in length. This is small, but the longer one may read as more thorough.
- **Unverified facts.** No ledger, decision or claim record was independently verified beyond the supplied packet files.
