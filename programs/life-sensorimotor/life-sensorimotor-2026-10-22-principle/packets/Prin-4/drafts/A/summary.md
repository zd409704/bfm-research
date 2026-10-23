# Prin-4 Draft A — Summary

**Author:** A (Claude Opus). Full text: `packets/Prin-4/proposals/A.md`. Proposal only. No claim states or grades are changed.

**Thesis.** While Eng-2 is gated, spend Principle effort on items that need no Eng-2 data and that either de-risk the gated spike or can be closed by verification and signature alone. No new Eng-2 preconditions should be added. C-P1-001 is ready for a lock decision once it has had one independent proof check and its record is reconciled. Its veto, if it is locked, covers the scalar fixture only. No Candidate has met a retire trigger.

**C-P1-001 lock path (B.9.2 Grade 1).** Open items:
- C1: reconcile `claim.md`, which says "Candidate-stay", with the ledger, which says "recommended-for-lock (conditional)", and list the conditions.
- C2: one allowed independent check: a formal checker (preferred; Lean/Mathlib scalar linear ODE), a published-result premise match, or qualified human review. Model re-derivation does not count (B.9.7).
- C3: premise-precision confirmations.
- C9: B.9.6 narrowing count. Confirm against `upgrade-log.md`, which this draft did not read.
- C11: signing package with the veto-scope and irreversibility notice.

Done in the record: actuator bound excluded, measured delay kept distinct from the common-input interval, citation ablation, falsifier stated. A counterexample-search PLAN is optional and does not block signing. Arithmetic re-checked: L* = 0.0095310 s, and at L = 20 ms the gap is 0.0221403 > b.

**Priority while Eng-2 is gated.** This is a planning order and is not necessity (B.8.3).
1. C-Eng2-A-01 cross-family claim adjudication.
2. C-P1-001 signing package.
3. C-P1-012 Grade-1 identifiability upgrade attempt.
4. C-Eng1-A-01 independence audit.
5. C-P1-011 side-channel audit.
6. C-P1-002 / C-P1-010 target premise match. Templates now; filled in after the human measurement-point declaration.
7. Prin-2 edges stay dormant.

**Retire/leave.** No retire-nominations. Leave every claim:
- C-P1-012: Eng-1 FAIL is sufficiency-only, the retire trigger has not fired, and the narrowing count is 1.
- C-P1-002: blocked on the human declaration. Flag it if no tightened text appears by the next Prin packet.
- C-P1-003: quarantine is enough.
- Prin-2 edges: keeping them costs nothing.

**Non-claims.** Nothing is Locked. No grade has changed. Nothing here bears on the target plant, controller rate, or architecture. The priority list is not a ladder or a gate. Nothing about the `(q,r)` content or the choice of Eng-2 branch.
