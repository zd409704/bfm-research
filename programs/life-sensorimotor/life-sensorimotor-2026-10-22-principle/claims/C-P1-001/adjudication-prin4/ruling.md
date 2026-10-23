# C-P1-001 — Prin-4 claim adjudication

Date: 2026-10-22. Role: claim adjudicator for Astra-authored claims (`roster.md`), Opus family, cross-family to the author under B.9.1. I did not write this claim and do not write it here. Only the status fields in `claim.md` are edited.

**Ruling: recommended-for-lock (conditional). State: Candidate, Grade 1 (narrow formal, scalar fixture).** This is not a lock. No Locked Grade-1 is asserted or implied. Retirement is not nominated.

## Evidence and authority

I read [claim.md](../claim.md), [upgrade-log.md](../upgrade-log.md), [violations.md](../violations.md), the [Prin-4 decision](../../../packets/Prin-4/decision.md), [Appendix B (B.9)](../../../packets/Prin-4/source/method-Appendix-B.md), and the C-P1-001 row of `program-ledger.md`. For reconciliation I also read the [Prin-1 ruling](../../../packets/Prin-1/adjudication/ruling-C-P1-001.md) cited in the ledger row. For B.9.6 classification I read sealed [Proposal B](../../../packets/Prin-1/source/P1-proposal-B.md) (§ scalar fixture, around lines 30–32 and 58; claims table line 97) and the [P1 stub](../../../packets/Prin-1/source/P1-claim-C-P1-001-stub.md). I ran no spikes or computations. External artifacts and harness outputs were not inspected.

Pre-edit SHA-256 values, for provenance only. **These do not identify a signing version:**
- `claim.md` `281bf0a1b25e6ed4b463469435abc4e67449d0e6f2d081c49a5820e5fe1d62f4`
- `upgrade-log.md` `356b7f894a0a9a7ff96e6d6c1ace0abb2dcb66bf901c443c4a7bfe01b36f90ba`
- `violations.md` `196935f0f21bad120bf65bc1e06f05ca64e58e04fc5dbfb448345d1913c9a421`

## 1. Record reconciliation (Prin-4 closing-sequence step 1)

| Record | Text | Nature |
|---|---|---|
| `claim.md` l.6–7 | State **Candidate**. "Recommended adjudicator action: Candidate-stay; obtain independent proof verification before considering recommended-for-lock." | **Author's** recommendation in the author record, written before adjudication |
| `upgrade-log.md` items 4–5 | "Outcome: … Candidate-stay." Recommended-for-lock is considered only after a B.9.2 check. | **Author's** log entry |
| Prin-1 ruling item 4 | **recommended-for-lock (conditional)**. State remains Candidate. | **Adjudicator** disposition (Opus, cross-family) |
| `program-ledger.md` C-P1-001 | "Candidate; **recommended-for-lock** (conditional) … B.9.2 check + human signature outstanding" | Ledger record of the adjudicator disposition |

**Governing:** under B.9.1 the author proposes and the claim adjudicator decides. The Prin-1 adjudicator disposition governs, and the ledger records it correctly. The author's "Candidate-stay" is superseded as a disposition. It stays in the record as history and is not rewritten.

**No conflict on state.** Every record says **Candidate**. "Recommended-for-lock" is an adjudicator disposition, not a B.4 lifecycle state. The difference is only about when lock becomes eligible for consideration. The author would wait until after an independent check. The adjudicator says eligibility is conditional on that check plus everything else listed below. These two positions have the same operative effect: nothing locks until the conditions are met.

## 2. Disposition

**recommended-for-lock (conditional)** is reaffirmed. I considered and rejected the other two options:
- **Candidate-stay without recommendation** is rejected. All B.3 gates and citation-ablation (B.8.7) passed in Prin-1. The remaining blockers are verification and procedure, not substance. B.4 lets a narrow Grade-1 formal bound lock early, subject to B.9.
- **Retire-nominate** is rejected. `violations.md` lists no admitted in-premise counterexample and no admitted target-premise failure. The B.9.6 count is 0 (§3). The Prin-4 decision forbids an unqualified "no retire trigger" claim made without reading the logs. I read both logs, and nothing in them triggers retirement review.

**Conditions.** Every one must hold before any lock. Meeting them does not make lock automatic.
- **C1 Exact object.** Freeze the signing version of `claim.md` and identify it by hash. The signed statement is the **whole conclusion**, not just the formula: \(L\le L^*=\ln(1+ab/D)/a\), with premises 1–5 as written. Premise 6 (\(|u|\le3\)) stays a fixture constraint that the proof does not use. The scope sentence, the necessity-not-sufficiency sentence ("equality at the bound does not establish continued viability"), and the no-unique-architecture/frequency sentence are part of the object.
- **C2 Independent check by a B.9.2 route.** Acceptable routes: a formal checker; a published result matched item by item to premises 1–5; or review by a qualified human. Model re-derivations do not count, including the Prin-1 adjudicator's (B.9.7). The check must cover the full statement in C1. That includes the non-strict boundary case at \(L=L^*\) and the step "envelope through the interval ⇒ \(\Delta(L)\le2b\)", which relies on continuity of \(\Delta\).
- **C3 Scope-limited veto.** The lock text must say the veto applies only to routes whose premises match the scalar fixture item by item (a, b, D, x(0)=0, paired constant disturbances, common applied input on [0,L), ordinary-input regularity). It is not a home-humanoid hardware deadline, not a control-frequency requirement, and not support for C-P1-002 / B-N2 or any ladder edge. D-P1-001 stays Provisional.
- **C4 Measured delay ≠ common-input interval.** The signing package must state that a measured total sensor-to-actuator delay does not by itself establish the common-input interval L. Harness results (attempt 1 FAIL, attempt 2 PASS, crossing near 8 ms) are neither counterexamples nor tightness evidence, and no lock rests on them.
- **C5 Objection log.** Collect and dispose of all open objections against the exact version, including this ruling and the Prin-1 ledger-hygiene item (see §4).
- **C6 Human-lead signature** on the exact version from C1, with the C3 scope recited.
- **C7 Authorized recording.** A non-author adjudicator records the transition. This ruling does not record one.

None of C1–C7 is satisfied by this ruling. Per the Prin-4 decision, the claim is **not** "ready for signature after one proof check": C2 alone is insufficient.

## 3. B.9.6 classification of the Prin-1 expansion

I compared the expanded claim with sealed Proposal B, not with the abbreviated stub.

| Prin-1 element | Proposal B source | Classification |
|---|---|---|
| a=10, b=0.01, D=1, x(0)=0, \(d=\pm D\) from t=0 | Fixture text (l.30–32) | Restatement — not an event |
| Identical applied control until L; randomized controllers coupled on the same realization; predictive controllers covered only while uninformative | l.32 | Restatement — not an event |
| Earlier distinguishing predictive information excluded | l.32, l.58 (such information "alters the premises") | Restatement — not an event |
| Robust both-world guarantee rather than an average | B-N1 "guaranteed invariance" (l.97) | Clarification of existing quantifier — not an event |
| Disturbance constant through L | Constant ±D in fixture and spike | Restatement — not an event |
| Premise 5: locally integrable u, continuous x, no impulsive resets | Not stated verbatim. Proposal B's own \(|u|\le3\) already restricts inputs to bounded ones, which excludes impulses. | Clarification of ODE solution semantics. Relative to Proposal B the admissible input class is **broadened** (bounded ⊂ locally integrable), not narrowed. It was not added to defeat an observed counterexample — not an event |
| Premise 6: actuator bound marked unused | l.30 | Annotation — not an event |
| Scope "scalar research fixture only" | B-N1 "for the stated scalar plant" | Restatement — not an event |

**Count: 0 accepted B.9.6 events (cumulative 0 of 3).** This agrees with the author's count and the Prin-1 adjudicator's count. If a future signing edit removes \(|u|\le3\) from the fixture, or restricts the input class or the information premise, that edit must be re-assessed under B.9.6.

## 4. What must still happen before human signature

Use the seven-row B.9.2 dossier adopted in the Prin-4 decision (Recommend B) as the checklist. This ruling verifies **none** of the rows.

1. **Exact object** (C1): freeze and hash the signing version. — *open*
2. **Independent check** (C2) through an allowed B.9.2 route, attached as an artifact. — *open*
3. **Scope match** (C3, C4): signing package with fixture-only veto wording and the measured-delay ≠ L statement. — *open*
4. **Objection log** (C5). It must include the open Prin-1 item 4: `inherited-ledger-P1.md` gives run date 2026-10-23 and cites `proposals/B.md`, while the claim cites `P1-proposal-B.md`. Confirm these are the same sealed artifact. — *open*
5. **Non-author adjudicator disposition**: this ruling (recommended-for-lock, conditional) and the Prin-1 ruling. It must be re-confirmed against the frozen version if the text changes after this date. — *disposition supplied; not a verification*
6. **Human-lead signature on the exact version** (C6). — *open*
7. **Authorized recording** of the transition by a non-author adjudicator (C7). — *open*

The counterexample-search spike is optional. Prin-1 found no mandatory spike, because the bound is analytic and B.9.2 requires a logged failed search only for Grade 2. A run would be harness or sufficiency evidence and would not replace row 2.

## 5. Files changed by this adjudication

- This ruling (new).
- **Not applied — sealed record.** `claim.md`, `upgrade-log.md` and `violations.md` are read-only (mode 444). This adjudicator did not override that. The exact intended edits are deposited for an authorized actor to apply:
  - [pending-upgrade-log-append.md](pending-upgrade-log-append.md): item 6, append only.
  - [pending-claim-status-edit.md](pending-claim-status-edit.md): l.7 status field only. The author's "Candidate-stay" is kept and labeled as the author's, and a governing-disposition line is added.
  
  Until these are applied, this ruling is the governing reconciliation note. The pre-edit hashes above remain the current hashes.
- `violations.md` is unchanged: no counterexample or premise failure is admitted. `program-ledger.md` is unchanged: its C-P1-001 row already records the governing disposition.
