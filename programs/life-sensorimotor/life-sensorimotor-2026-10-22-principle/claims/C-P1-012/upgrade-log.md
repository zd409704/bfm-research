# C-P1-012 — Upgrade log

Append-only. It records attempts to move a grade or state, plus every scope narrowing or added premise (B.9.6 counter).

| # | Date | Actor | Event | From → To | Evidence / note | Adjudicator ruling |
|---|---|---|---|---|---|---|
| 0 | 2026-10-22 | Author A (Opus), Prin-1 | Record created from inherited ID (origin P1 A-C7), flagged "confounded as written" | — → Candidate (P1 label "Grade 1 (formal) → contract") | P1 Proposal A claims table; P1 decision rationale + Alternate | pending |
| 1 | 2026-10-22 | Author A (Opus), Prin-1 | **Proposed** downgrade Grade 1 → Grade 2 (no formal proof; spike-only support) | proposed | claim.md H4 | pending |
| 2 | 2026-10-22 | Author A (Opus), Prin-1 | **Proposed** premise tightening: split into Factors R/E; replace "PF-1 sensitivity" with task-stated contact class; declare friction placement | proposed | claim.md H1, H3, H5. **Would count as narrowing #1 of 3 under B.9.6 if accepted** | pending |
| 3 | — | — | Grade-1 upgrade attempt (identifiability argument for Factor E; rate-floor for Factor R) | open target | Not yet attempted | — |

## Scope-narrowing counter (B.9.6)

Accepted narrowings: **0** (1 proposed, pending). Retirement review becomes mandatory at 3.

## Prerequisites outstanding before any recommend-for-lock (Grade 2 route, B.9.2)

- [ ] Factorial counterexample-search spike (sealed PLAN.md under `spikes/`) run and filed
- [ ] Implementation-class-independent argument for the role
- [ ] Operational realization test defined and run (effort-channel substitution)
- [ ] Logged serious failed attempt to reach the competence class without the role
- [ ] Cross-family adjudicator ruling + human lead signature


## Prin-3 adjudicator append — 2026-10-22 (current disposition)

Authority: [independent cross-family ruling](adjudication-prin3/ruling.md), applying Appendix B.9. The adjudicator did not author the claim. This append supersedes stale pending/count statements above without altering their historical text.

| # | Date | Actor | Event | From → To | Evidence / note | Adjudicator ruling |
|---|---|---|---|---|---|---|
| 4 | 2026-10-22 | Independent claim adjudicator, Prin-3 | Reconcile Prin-1 downgrade and accepted repair | Prior Grade-2 Candidate disposition → Grade-2 Candidate | Prin-1 decision and supplied summary-astra-on-A.md; earlier rows 1/2 resolved | Prior downgrade confirmed; inherited premise repair is accepted narrowing event #1 |
| 5 | 2026-10-22 | Independent claim adjudicator, Prin-3 | A-1 identifiable-set replacement | No text change | Reference-dependent class selection is not the prior competence repair | Reject; 0 accepted events |
| 6 | 2026-10-22 | Independent claim adjudicator, Prin-3 | A-2 restricted-mean/median replacement of p95 | No text change | Changes tail-latency contract; TPR-only fallback rejected | Reject; 0 accepted events |
| 7 | 2026-10-22 | Independent claim adjudicator, Prin-3 | A-3 dual-tuning admissibility | Existing H2 retained | Sensitivity artifact not reviewed; competent in-premise counterexamples remain admissible | Defer as written; 0 accepted events |
| 8 | 2026-10-22 | Independent claim adjudicator, Prin-3 | A-4 physical restatement / model-compensation search | Scope and role unchanged | Reject downstream-of-dominant-nuisance necessity; accept disjoint-data command/model cell for prospective in-scope search only | A-4a reject; A-4b accept with boundaries in ruling; 0 new events |
| 9 | 2026-10-22 | Independent claim adjudicator, Prin-3 | A-5 UP exclusion | Existing scope retained | UP remains an external comparator | Accept; 0 new events |
| 10 | 2026-10-22 | Independent claim adjudicator, Prin-3 | B-1 channel audit and competence prerequisite | Premise/realization clarification | Existing sensor/side-information premises; Prin-1 summary already required absolute competence criteria | Accept; implementation of event #1, no new event |
| 11 | 2026-10-22 | Independent claim adjudicator, Prin-3 | B-2 measurement semantics | Original all-class thresholds retained | No infinity-minus-infinity match; prospective miss/uncertainty policy; no rescoring or margin relaxation | Accept; no new event; same prior competence repair as B-1 |
| 12 | 2026-10-22 | Independent claim adjudicator, Prin-3 | B-3 evidence annotation; bounded search filed | Grade-2 Candidate → Grade-2 Candidate | Eng-1 S2a-XC verdict and metrics, qualified below | Accept; Candidate stay; 0 new events |

**Current B.9.6 counter: accepted narrowings = 1.** Prin-1 event #1 resolves the old pending tightening in row 2. New accepted Prin-3 narrowings: 0. Cumulative: 1. The historical “0 (1 proposed, pending)” is superseded, not erased. The Prin-1 summary explicitly required absolute competence criteria for the repaired factorial search, so B-1/B-2 do not introduce or double-count that condition. Rejected/deferred restrictions are not operative. Each future distinct narrowing must be counted; the third accepted event triggers mandatory retirement review. No such review is triggered now.

**Adopted B-3 evidence annotation:** Eng-1 S2a-XC: valid harness, A02 unmet; registered Factor-E/R counterexamples not found; DOWN realization test unmet; UP outside current scope. Necessity remains unproved. No export field, numeric sampling rate, research order or target-plant acceptance is authorized by this evidence alone.

Source: `packets/Prin-3/source/Eng-1-S2a-XC-VERDICT.json`; PLAN SHA-256 `3d7b9af6b08d8f1fe36e25c06780bcfca571969656669d9c6fbdd1c902e9ac41`; results SHA-256 `26da2f3f0a19f59ee561770596e918cd343dae09bce14b3eaa55ae1aff3064d3`. H1–H4/harness pass; A02 false; placeholder task thresholds; all Factor-E/R flags false. DOWN substitution unmet (mean 0.1115, minimum 0.0625); UP met but out of scope. The DOWN finding is limited to this fixture, detector and calibration and is not proof that effort information is absent. The exact substitution margin and sensitivity artifact were not reviewed; preserve the filed criterion and flags, including d50_M10, without retrospective reinterpretation.

**Prerequisite status update:** the previously unchecked factorial-run item is now filed as this bounded experimental search. It does not establish that the repaired, absolute-competence search requirement is complete: task/channel declaration, latency semantics and rate/bandwidth controls remain unresolved. The implementation-independent argument, successful task-qualified realization evidence, serious logged failed search for a competent role-free system and human signature remain outstanding. This adjudication supplies a cross-family ruling only; no signature, new PLAN, lock recommendation or retirement nomination is implied. Under B.9.8 the FAIL itself changes no grade. The violations log remains unchanged because no in-premise counterexample or target-premise failure is admitted in this ruling.

<!-- STAGED APPEND for ../upgrade-log.md. The target file is read-only (0444) and was not modified by the adjudicator. Whoever holds write authority over the log should append the text below verbatim. -->

## Prin-6 alternate claim adjudicator append — 2026-10-22

Authority: [Prin-6 alternate ruling](adjudication-prin6/ruling.md). The adjudicator is bound as ALTERNATE (Opus) because the Recommend-B author family matches the usual Astra adjudicator. **Disclosed: this ruling is same-family with the claim author (Opus).** A cross-family re-ruling is still needed before any lock path. Historical rows above are not altered.

| # | Date | Actor | Event | From → To | Evidence / note | Adjudicator ruling |
|---|---|---|---|---|---|---|
| 13 | 2026-10-22 | Alternate claim adjudicator, Prin-6 | D-Prin-6-001 table amendments P-1..P-9 (B) | No claim text change | Packet planning artifact; does not become claim text | Accept (P-1 with boundaries i–iv); 0 events |
| 14 | 2026-10-22 | Alternate claim adjudicator, Prin-6 | Alternate-A repairs a–f, R-3; formal-evidence routing | No claim text change | Tiers, placeholder cap, same-run, unlisted→AN, PLAN-family transfer not operative | Accept repairs; 0 events |
| 15 | 2026-10-22 | Alternate claim adjudicator, Prin-6 | Follow-up 1: factor-drop / plant-model carve-out after admitted single-factor counterexample | Prospective counting rule | Each accepted restatement or carve-out counts separately | Accept: +1 each when accepted; 0 now |
| 16 | 2026-10-22 | Alternate claim adjudicator, Prin-6 | Follow-ups 2–9 (role-absence clarification; combination semantics; substitution record; premise-6 routing; row-ID citation; priority-4 routing; binding; counter) | Grade-2 Candidate → Grade-2 Candidate | See ruling | Accept; 0 events; D-1..D-3 deferred |

**Annotations (count 0):**
- **Substitution criterion.** The claim's "more than a stated margin" and the filed DOWN criterion govern Eng-1 by reference. Future PLANs must declare the inequality, aggregation, false-event rate, calibration and uncertainty handling. The Eng-1 result (mean 0.1115 / min 0.0625, d50_M10) is not rescored.
- **Row-ID citation.** Future C-P1-012 filings should cite a D-Prin-6-001 table row ID. Row IDs do not bind rulings. Where a row conflicts with the claim text, the claim text controls.
- **Vacuity flag.** The information-based role-absence criterion may make the Grade-2 role near-vacuous. The B.9.2 implementation-independent argument must address this.

**Current B.9.6 counter: accepted narrowings = 1** (new in Prin-6: 0; cumulative: 1). Retirement review is not triggered. The grade stays 2 and the state stays Candidate. No lock recommendation, retire-nomination, Eng-2 gate change or spike.

<!-- STAGED APPEND for ../upgrade-log.md. The log is read-only (0444); the adjudicator did not modify it. Whoever holds write authority should append the text below this comment verbatim (omit this comment). -->

## Prin-7 alternate claim adjudicator append — 2026-10-22

Authority: [Prin-7 alternate ruling](adjudication-prin7/ruling.md). The adjudicator is bound as ALTERNATE (Opus) because the Recommend-B author family (Astra) matches the usual adjudicator family. **Disclosed: this ruling is same-family with the claim author (Opus).** Ruling F-2 favors the claim; cross-family confirmation is recommended before an execution packet relies on it. A cross-family re-ruling is still needed before any lock path. Historical rows above are not altered.

| # | Date | Actor | Event | From → To | Evidence / note | Adjudicator ruling |
|---|---|---|---|---|---|---|
| 17 | 2026-10-22 | Alternate claim adjudicator, Prin-7 | D-Prin-7-001 identifiability PLAN adjudicated (Recommend B + mandatory A merge) | No claim text change | PLAN only; no search, certificate or evidence filed | Annotation; 0 events |
| 18 | 2026-10-22 | Alternate claim adjudicator, Prin-7 | F-1 target classification rule (same / narrower / different); K-0 = different | Classification rule | K-S unclassified until sealed (D-4) | Accept; 0 events |
| 19 | 2026-10-22 | Alternate claim adjudicator, Prin-7 | F-2 exploratory-premise counting | Prospective counting rule | Pre-seal, pre-result model premises: 0 (listed, flagged, reason logged). Post-result repairs: proposed event, default +1 if offered as bearing. Adoption into claim text: +1 each. Deferred, not waived | Accept; 0 events |
| 20 | 2026-10-22 | Alternate claim adjudicator, Prin-7 | F-3..F-12 (detection vs identifiability; two-sidedness; premise-2 match; vacuity; binding; housekeeping; counter; K-0 AN-only) | Grade-2 Candidate → Grade-2 Candidate | See ruling | Accept; 0 events; D-4, D-5 deferred |

**Annotations (count 0):**
- **K-0.** If filed, K-0 is an AN on a free-disturbance model only: class D, not premise-matched. Its closed form `a_min ≤ 2·min(b,s)` is an unverified score-pass hand reading. K-0 is never Factor-E evidence, Grade-1 progress or a counter-model.
- **Detection vs identifiability.** A detection obstruction implies non-identifiability on the same class. Re-wording the target to detection over the same class counts 0. Each added restriction counts +1.
- **Two-sidedness.** The possibility half is a separate research target. Its failure does not refute the necessity statement.
- **Housekeeping.** The Prin-6 append was applied together with its staging comment. That comment is stale; no edit is made.

**Current B.9.6 counter: accepted narrowings = 1** (new in Prin-7: 0; cumulative: 1). Retirement review is not triggered. Grade 2, Candidate. No lock recommendation, retire-nomination, Eng-2 gate change, search or spike.
