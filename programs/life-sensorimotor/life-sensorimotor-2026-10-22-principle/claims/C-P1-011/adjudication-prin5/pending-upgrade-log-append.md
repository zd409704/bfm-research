<!-- PENDING: append verbatim to the end of claims/C-P1-011/upgrade-log.md. That file is sealed (mode 444), so an actor authorized to write it must do the append. Not yet applied. Earlier rows are not rewritten. -->

## Appended 2026-10-22 — Prin-5 claim adjudication (alternate-bound)

| # | Date | Actor | Event | From → To | Evidence / note | Adjudicator ruling |
|---|---|---|---|---|---|---|
| 2 | 2026-10-22 | Prin-5 alternate claim adjudicator (Claude Opus) | **Reconciliation of row 1.** The Prin-1 cross-family ruling (Astra) accepted the definition, side-channel and ordering repairs as **B.9.6 event #1**. That acceptance was not logged here before now | proposed → accepted (event #1) | `packets/Prin-1/adjudication/ruling-C-P1-011.md` justification 5; `summary-astra-on-A.md` | tighten-premises-then-Candidate-stay (Prin-1) |
| 3 | 2026-10-22 | Prin-5 alternate claim adjudicator (Claude Opus; alternate because the Recommend-B author shares the usual adjudicator's family; same family as the claim author, disclosed) | Rulings on the Prin-5 Recommend-B checklist and on Alternate-A TP-1..7 and channel classes. Accepted: joint and export-only Markov premises with cutoff `t`; "additional accessible information" replaces "independent channel"; feedback and random state; one law per assertion; "cannot increase"; realized `X_t` including metadata; label provenance; H4 provenance correction; application failure criterion. Rejected: "d-separation certificate" wording; the "TP-4 violation" label; the leak-alarm "≥1−2α" wording. Deferred: mandatory attribution report (TP-7); leak-alarm lemma; time-box value for "unresolved" | Candidate (Grade 1) → Candidate (Grade 1); premises tightened | `adjudication-prin5/ruling.md`; `packets/Prin-5/decision.md`; `proposals/B.md` §4; `proposals/A.md` §4; `score-pass1.md` §4–§5 | **Candidate stay**. Not recommended-for-lock: B.9.2 match of the amended text and the human signature are outstanding. Not retire-nominate |

### Scope-narrowing counter (B.9.6), corrected

The line above reading "Accepted narrowings: **0**" is stale and is superseded here, not erased.

- Accepted narrowings: Prin-1 event #1 = **1**.
- New accepted in Prin-5: **0**. Every accepted item is a correction, an implementation of event #1, or an application-audit or usage rule.
- **Cumulative: 1 of 3.** Retirement review is not triggered.
- **Would count if adopted later:** narrowing to an observation-only setting; excluding recipient or channel classes from the theorem's scope; any premise added after an admitted B.9.4 challenge.

### Lock prerequisites (status after Prin-5)

- [ ] Independent item-by-item match of the **amended** statement and premises to the published DPI statement
- [x] Claim adjudicator ruling on Prin-5 amendments (alternate-bound; same family as the claim author, disclosed). A cross-family reconsideration is still needed before any recommended-for-lock
- [ ] Human lead signature
- [ ] (For application, not lock) side-channel / access-boundary audit of the target stack. All target dispositions remain **unresolved**. This does not block Eng-2.
