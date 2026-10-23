# Prin-6 — PASS1 adjudication score

**Adjudicator:** Packet Adjudicator, PASS1. I authored neither proposal and neither review.
**Pass mapping:** P = `proposals/A.md` (ceiling table, tiers T0–T3, row IDs E/R/ER/F/S/A/U/P/G). Q = `proposals/B.md` (witness-based table, four three-valued evidence components, overlap rule). Reviewer of P = `reviews/B-on-A.md`. Reviewer of Q = `reviews/A-on-B.md`.
**Inputs read:** packet `brief.md`, `roster.md`, every file in `source/` (packet brief, Appendix B, C-P1-012 claim, Prin-3 claim ruling, Prin-4 and Prin-5 decisions, Eng-1 S2a-XC verdict, current ledger), both proposals, both draft summaries, both reviews, and the run-level rubric.
**Effect:** planning only. **C-P1-012 stays Grade 2, Candidate.** The accepted B.9.6 narrowing count stays **1**. This adjudication makes no Locked Grade-1, no grade or state change, no change to the Eng-2 gate (D-Prin-3-001), and runs no spike. It registers and seals no PLAN, and it edits no claim file. Nothing below is a necessity order (B.8.3).

---

## 1. Gates (B.9.5, before ranking)

| Gate | P | Q |
|---|---|---|
| No grade/state change; no Locked Grade-1 | Pass. §2 "never available" list; §7 non-claims. | Pass. Header and packet boundary; the dossier row requires a human signature for any lock. |
| Claim adjudicator ≠ author (B.9.1) | Pass. CR and AM are restricted to the claim adjudicator; the orchestrator does not rule. | Pass. "Amend" is a submission; "review requests a ruling; it does not enact one." |
| Sufficiency ≠ necessity (B.3.5, B.4, B.5) | Pass. Favourable rows cap at AN. | Pass. Acceptance, substitution and sufficiency rows withhold necessity. |
| Runner files data only (B.9.8) | Pass. | Pass. |
| Grade-3 / planning order as necessity (B.8) | Pass. G-3 is N. | Pass. No ladder order becomes mandatory. |
| Eng-2 non-interference | **Pass, conditional.** §6 states no gate change. But T1 lists placeholder `(q,r)`, and T1 is capped at AN, so in practice no model-level counterexample could reach claim-adj review until the human ratifies `(q,r)`. That is an Eng-2 gate input. The effect is a coupling, not a formal gate; it must be removed (amendment P-a below). | Pass. "They do not create Eng-2 execution preconditions"; D-Prin-5-001 nonblocking preserved. |
| Fidelity to the filed record | Pass. Eng-1 = T1, B-3 annotation not reopened. | Pass. Verdict facts and PLAN hash match the JSON exactly; no cutoff or A02 threshold reconstructed. |
| Falsifier preservation (B.3.4; Prin-3 A-1/A-2/A-3 rulings) | **Pass, conditional.** Full `d ≥ 10 ms` set, thresholds and p95 preserved. However, three rules would change which counterexamples reach review without B.9.6 accounting: ER-1 needs "same sealed run", §5.6 sends unlisted evidence to AN, and the placeholder cap above. Prin-3 A-3 refused this kind of admission restriction. | Pass. It explicitly refuses two-design admission conditions and keeps the all-detector quantifier. The "common scope" clause needs a guard (amendment Q-4). |
| No named products/companies | Pass. | Pass. |

**Both are eligible for ranking. No Hard Reject. P carries two conditional gate findings, which its amendments must clear before any P text is merged.**

### Independent checks of the reviews' central objections

- **B-on-A #1 (tier contradiction): confirmed.** P §3 defines T2 as "T1 conditions, and: absolute contract met", while T1 is defined by the reference *missing* that contract or by placeholders. Also, `harness_pass` and reference competence are observed results, so §5.1 ("assign the tier … before opening results") cannot be executed as written.
- **B-on-A #2 (alternative competence): confirmed.** The claim's falsifier requires the *falsifying alternative* to meet the absolute contract. P's T2 checks only the reference.
- **B-on-A #5 (substitution inequality): confirmed.** The claim says "drop by more than a stated margin"; P's S-1 and S-2 use `≥` and `<`. P also asserts all-identifiable-class aggregation. The filed verdict reports `mean_drop` and `min_drop`, and the aggregation rule is not in the supplied sources.
- **A-on-B D1 (role absence undefined): confirmed.** The claim's Grade-2 role permits "a fast-tier observer that exports its residual" as a realization. A competent commanded-at-R1 system with such a residual is therefore not automatically "role-free". Q's direct-counterexample row needs a classification rule.
- **A-on-B D2 (factor-drop accounting): confirmed.** Q's single-factor rows do not say that restating the claim on the surviving factor is a countable B.9.6 event. P's E-1 does say it ("→AM, counted").
- **A-on-B D3/D5/D6 (side-channel row, artifact destinations, proof rows): confirmed as absent from Q.** P has all three (P-4; the AN destination in `upgrade-log.md`; P-1..P-3).

---

## 2. Rubric (fixed brief, 1–5, higher is better)

I used both reviews as inputs. Where my reading differs, the reason is in the notes. For parity, I scored identical behaviours identically: both proposals preserve p95 and fair per-rate tuning without mandating any rate, so both get the same Latency score.

| Dimension | P | Q | Note |
|---|---:|---:|---|
| Constraint fit | 4 | 5 | P: the placeholder cap couples review routing to the Eng-2 human input, and the ceilings are framed as binding. Q stays inside the planning remit. |
| Principle integrity | 3 | 4 | P: the T1/T2 contradiction, the reference-only competence check, `≥` vs "more than", and asserted aggregation. Q: role absence is undefined (D1) and the factor-drop has no counter route (D2). |
| Falsifiability | 2 | 4 | P: the same-run ER-1, the placeholder cap, unlisted→AN and bandwidth demotion (R-3) can all keep competent adverse evidence away from review. Q: one competent in-premise witness earns review even with a weak reference. The composition guard is correct. |
| Evidence demand | 3 | 5 | P: T3 and the two-fixture S-2 trigger add future demands. Q adds none. |
| Failure modes | 4 | 4 | P names tier gaming and the F-2 boundary. Q names weak-reference suppression, the composition error, rescue bundling and UP leakage. Q's "common scope" clause is a latent escape (D4). |
| Integrability | 4 | 3 | P: row IDs, counter effects per action, artifact destinations, a C-P1-011 linkage row (P-4). Q: no row IDs, no destinations, no premise-6 row. |
| Latency / criticality | 4 | 4 | Both keep p95 and duration classes and mandate no rate. |
| Complexity cost | 3 | 4 | P: four tiers, about 30 rows, and overlapping ceilings with exceptions (A-3, S-2). Q: 16 rows and one overlap rule. |
| Reversibility | 5 | 5 | Paper artifacts. |
| Stackability | 4 | 4 | P: the P-rows route the priority-4 identifiability attempt; A-1's PLAN-family transfer overreaches. Q: no proof row, but it does not block one. |
| **Total** | **36** | **42** | |

The reviewers' totals were P = 36 (B-on-A) and Q = 41 (A-on-B). The ordering is the same. Only the within-pass ordering is used (see §6).

---

## 3. Decision (PASS1)

| Role | Proposal | Reason |
|---|---|---|
| **Recommend** | **Q** | Witness-based, asymmetric routing that follows the Prin-3 A-1..A-5 and B-1..B-3 rulings without reopening any. The composition guard is correct: two single-factor witnesses ≠ a competent commanded-at-R2 system. Its overlap rule blocks favourable-row selection. It adds no admission restriction to the falsifier. |
| **Alternate** | **P** | Better executable apparatus: row IDs, an action vocabulary with per-action counter effects, the formal-evidence rows (P-1..P-3), the C-P1-011 side-channel row (P-4), the process rows (G-1..G-4), artifact destinations, and the explicit factor-drop AM counting in E-1. |
| **Reject** | (i) Tiers as *binding ceilings* assigned before results are read. (ii) Placeholder `(q,r)` as a cap on model-level counterexample review. (iii) "Same sealed run" for the both-factors retire-nominate route. (iv) Unlisted evidence defaulting to AN until a later packet. (v) `≥`/`<` substitution wording, and any inferred aggregation or cutoff. (vi) The two-fixture S-2 trigger as a review prerequisite. (vii) PLAN-family competence transfer (P A-1). (viii) Treating actions as points on a single ordered strength scale. | |

### Merge notes (P → Q), conditional on PASS2 agreeing

Import into Q, **after** the P-side repairs listed:

1. **Row IDs** for every Q row, plus a filing that cites row ID, exact claim/PLAN/result versions and hashes, predeclared analysis rules, harness status, premise audit, class-wise absolute and relative outcomes, unresolved fields, and the requested action (B-on-A filing list).
2. **Action vocabulary with counter effects** (P §2), corrected: N / AN / AM / CR are distinct routes, not an ordered scale. AM counts +1 only for scope narrowings and added survival premises. The adjudicator classifies neutral clarifications at 0 (Prin-3 B-1/B-2 precedent). Not every wording change counts (B-on-A #6).
3. **Formal-evidence rows P-1..P-3**, corrected (B-on-A #7). Any Grade-1 argument is checked by one of the B.9.2 routes: formal checker, item-by-item premise-matched published result, or qualified human. A Grade-1 *lock* also needs the human signature; a grade reassessment needs its own packet. A formal counter-model gets its own premise and artifact audit, not spike-tier semantics. This packet authorizes neither.
4. **Side-channel row P-4**, merged with A-on-B D3. If a C-P1-011 / Prin-5 audit finds a joint channel carrying effort-relevant information to the upper layer, the route is CR on premise 6 (B.9.4(b) evidentiary standard) plus AN on which H8 motivation lapses. It does not by itself falsify Factor E, and it makes no automatic change to C-P1-012.
5. **Process rows G-1..G-4**: researcher agreement, rubric scores, ladder order → N for grade. Bundled rescues are logged individually.
6. **Artifact destinations** (A-on-B D5): AN → `upgrade-log.md` (append-only); an admitted counterexample → `violations.md`; AM or CR → an adjudication ruling file. All of these are written by the bound claim adjudicator only.
7. **F-1/F-2 friction-model split**: already in Q's identified-model row. Keep Q's wording and adopt P's F-3 (UP-only match → AN).
8. **Eligibility checklist (not tiers):** P's T2 list may be imported as a *pre-execution eligibility checklist*, kept separate from post-execution verification of provenance, harness validity, competence of *each* compared system, and premise fit. A missing element makes the affected comparison **unresolved**, not inadmissible, and does not cap review of a concrete in-premise witness.

Do **not** import P's tier ceilings, the placeholder cap, ER-1's same-run restriction, unlisted→AN, the S-2 two-fixture prerequisite, or A-1's PLAN-family transfer.

---

## 4. Mandatory amendments

### To Q (before it is used as the D-Prin-4-001 priority-3 deliverable)

1. **Q-1: Role-absence criterion (A-on-B D1).** A system counts as role-free for the direct-counterexample row only if no exported field carries information about `τ_cmd + τ_act_unmodeled` beyond what the upper layer can reconstruct from commands and permitted history. Check this against the C-P1-011 / Prin-5 access-boundary record. A competent system that exports an observer residual above policy rate is classified **"unresolved: role absence not established"** and still goes to CR, but as a possible alternative *realization*, not as a role-free witness. This criterion is a proposed classification rule for the claim adjudicator. It is not adopted into the claim here.
2. **Q-2: Factor-drop accounting (A-on-B D2).** Add to each single-factor row: if the adjudicator restates the claim on the surviving factor, record it as a proposed B.9.6 narrowing with before/after text. Its counting is provisional until ruled; current 1 → would be 2.
3. **Q-3: Premise-6 / side-channel row.** Per merge note 4.
4. **Q-4: Common-scope guard (A-on-B D4; parity with B-on-A #3).** "Common, premise-matched scope" is a comparability audit for the both-factors retire-nominate route. It is not a new admissibility premise and is not itself a B.9.6 event. Witnesses from different runs may combine after that audit. Witnesses from incompatible scopes each keep their own single-factor review (with Q-2 accounting).
5. **Q-5: Omitted-rule default (A-on-B D7).** If a future PLAN omits any of: miss handling, event accounting, confidence family, direction, uncertainty rule, substitution inequality, aggregation or margin, then the affected comparison is classified **unresolved**. It is never a match and never an established failure.
6. **Q-6: Substitution wording.** State that the claim reads "more than a stated margin". Future PLANs must declare the inequality, the aggregation across identifiable classes, the fixed false-event rate, the calibration policy and the uncertainty handling. The filed DOWN criterion governs the Eng-1 result by reference and is not reconstructed.
7. **Q-7: Unlisted-evidence route.** Evidence that fits no row may still be submitted for CR if it is a concrete in-premise counterexample, target-premise-failure evidence, or a conflict between table and claim. Otherwise it is filed without claim action. The table may be extended only by a packet decision.
8. **Q-8: Merge notes 1–7** (row IDs, vocabulary, P-rows, G-rows, destinations).
9. **Q-9: Premise-failure independence (B-on-A #4 applied to Q).** Keep Q's UP-row wording that target-measurement evidence goes to review under B.9.4(b). Add that it needs provenance, measurement and applicability checks only, with no competent detector, factorial or substitution margin. Reviewing a Candidate's applicability is distinct from admitting a challenge to a lock; a Candidate has no veto to pause. Neither route authorizes an Eng-2 run.

### To P (only for any text merged from it)

- **P-a:** Remove placeholder `(q,r)` as a cap on review. A model-level declared task contract suffices for a model-level counterexample. Target ratification matters only for target-scope rows.
- **P-b:** Replace tiers with the eligibility checklist and post-execution verification (merge note 8). Require competence of each compared alternative.
- **P-c:** Delete "same sealed run" from ER-1, replacing it with Q-4.
- **P-d:** Use "more than" for the substitution inequality, and do not assert an aggregation rule.
- **P-e:** S-2's repeated-fixture trigger becomes an optional prioritization heuristic. A-1 drops PLAN-family transfer. A-3's CR recommendation is reconciled with its AN annotation as separate routes.
- **P-f:** T1 failed interventions still defeat the local realization assertion (Prin-3 B-1). They are not just "uncredited".

---

## 5. Claim follow-ups (for the bound C-P1-012 claim adjudicator; none decided here)

1. **Factor-drop classification.** Rule prospectively whether restating C-P1-012 on a surviving factor, after an admitted single-factor counterexample, is a B.9.6 narrowing. Both proposals and both reviews expect yes.
2. **Role-absence vs alternative realization.** Rule whether the Q-1 criterion is a clarification of the existing Grade-2 role text (count 0) or a narrowing (count +1), before any filing relies on it.
3. **Retire-nominate combination semantics.** Clarify that "if both are falsified" requires a comparability audit, not a single run, and that this clarification adds no premise.
4. **Substitution criterion record.** Note in `upgrade-log.md` that the claim's "more than" wording and the filed DOWN criterion govern. Future PLANs must declare the inequality and aggregation. No retroactive rescoring of `mean_drop 0.1115 / min_drop 0.0625`.
5. **Premise 6 / H8 linkage.** Coordinate with the pending C-P1-011 tighten-premises ruling from D-Prin-5-001. A joint-channel outcome there is a review input for C-P1-012 premise 6, not an automatic change.
6. **Optional record note.** Future C-P1-012 filings cite a table row ID. This is an upgrade-log annotation, count 0.
7. **Priority-4 identifiability attempt.** It needs its own PLAN before any search. Rows P-1..P-3 (as amended) route its output, and no grade change follows from this packet.
8. **Role binding check.** Q's author shares a model family with the bound C-P1-012 claim adjudicator. Before that adjudicator rules on Q-derived text (Q-1, Q-2, Q-4), check the family overlap. Follow Prin-5 follow-up 4: disclose it, or bind an alternate cross-family adjudicator.
9. **Counter.** Accepted narrowings stay at **1**. Nothing in Prin-6 is an accepted event. Q-1/Q-2/Q-4 are proposals for ruling only.

---

## 6. Confounds

- **Adjudicator family = Author A family.** This PASS1 adjudicator shares a model family with Author A (P), with Reviewer A (who reviewed Q), with the orchestrator, and with the original C-P1-012 claim author. The roster's default packet adjudicator binding is a different model within that same family. Any family-level preference would favour P, and P was ranked lower, but that does not rule out bias in the margins or in the merge selections. Disclosed per roster.
- **Order swap incomplete.** This is PASS1 only. The recommendation is provisional until PASS2 (P = B, Q = A) agrees.
- **Reviewer asymmetry.** P was reviewed cross-family by B's family, and Q was reviewed cross-family by A's family. Strictness differs: B-on-A gave a "revise before adoption" disposition, while A-on-B gave "yes, with D1–D2". Reviewer leniency cannot be separated from proposal quality, so only the within-pass ordering is used.
- **Q follows the bound adjudicator's own prior ruling closely.** Q's author family wrote the Prin-3 claim ruling. Close fidelity to that ruling is weaker evidence of independent judgment (B.9.7), and it also means a same-family adjudicator would apply Q-derived rules.
- **Length.** P is about 16 kB and Q about 13 kB. Length was not scored. P's extra rows were credited only under Integrability and Stackability.
- **Common source packet.** Both authors and both reviewers read the same `source/` set. Agreement among them on objections is not independent confirmation. I independently checked only the gate language, the T1/T2 contradiction, the substitution inequality against the claim text, the role-text permission for observer residuals, and the verdict JSON fields.
- **Unavailable artifacts.** No original sealed PLAN, raw results, sensitivity artifact, filed substitution cutoff, A02 thresholds, or target measurement was supplied. No numeric criterion is inferred here.
- **Inherited evidence confounds** (unchanged; neither proposal resolves them, nor should it): rate vs observer bandwidth (H2; A-3 deferred); friction placement relative to sensing (H3; DOWN vs UP); weak reference (A02 unmet); `placeholder_qr = true`; a single planar 2-link sim fixture with 3 seeds; substitution drops that depend on the recalibration policy (`same r_w`).

---

DONE
