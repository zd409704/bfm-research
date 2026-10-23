# C-P1-012 — Prin-6 claim adjudication (evidence-to-action table amendments and follow-ups)

Date: 2026-10-22. Role: claim adjudicator under B.9.1, **bound as ALTERNATE** for this ruling only. Adjudicator family: Opus. Disposition: **Grade 2, Candidate, stay.** No recommended-for-lock and no retire-nominate. This ruling asserts no Locked Grade-1, adds no Eng-2 gate, and runs, registers or seals no spike or PLAN. **Accepted B.9.6 narrowings: 1 before, 0 new, 1 cumulative.**

## Binding and role-separation disclosure

- **Alternate binding.** C-P1-012's usual claim adjudicator is the Astra family. The Prin-6 Recommend proposal (B) is Astra-authored. D-Prin-6-001 and score-pass1 §5 item 8 therefore require an alternate before anyone rules on B-derived text (P-1/Q-1, P-2/Q-2, P-4/Q-4). I am that alternate. The roster binding is otherwise unchanged.
- **Discrepancy in the binding prompt.** The binding prompt describes the claim's author family as "Astra-side compilation history". The record says otherwise: `claim.md` lists **Opus** as the author family (P1 Proposal A; record compiled in Prin-1 by Author A, Opus). Score-pass1 §6 and score-pass2 §5 agree. I follow the record.
- **Family relationships that follow.**
  - This ruling is **same-family with the claim author** (Opus/Opus). That breaks the cross-family guarantee B.9.1 asks for on high-stakes claims.
  - Recommend-B text is **cross-family** to me (Astra/Opus).
  - Alternate-A merge text is **same-family** to me (Opus/Opus).
  - Both score passes were also adjudicated by the Opus family.
  - I authored no proposal, review, score pass or prior ruling for this claim.
- **Mitigation.** A same-family adjudicator could lean toward keeping the claim alive. So wherever counting was in doubt, I resolved it toward counting, or I deferred. I accepted nothing that raises the grade or state, or that removes a route for an adverse result. I treated A-derived text with extra scrutiny. A human lead may re-bind and re-rule, and a cross-family re-ruling is still required before any lock path.
- This ruling is not B.9.2 verification and does not stand in for the human signature.

## Evidence read

- Claim records: `claims/C-P1-012/claim.md`, `upgrade-log.md`, `violations.md`, `adjudication-prin3/ruling.md`.
- Prin-6 packet: `packets/Prin-6/decision.md`, `proposals/B.md` (Recommend), `proposals/A.md` (Alternate merge source), `reviews/A-on-B.md` (D1–D7 only), `adjudication/score-pass1.md` §3–§6, `adjudication/score-pass2.md` §3–§6, `roster.md`, `source/method-Appendix-B.md` B.9, `source/Prin-5-decision.md`.
- Ledger: the program ledger rows for C-P1-011/012.

I did not review the sealed Eng-1 PLAN, the raw results, the sensitivity artifact, the filed substitution cutoff or the A02 thresholds. I infer none of them.

## Test applied

B.9.6 counts two kinds of event: a narrowing of the claim's scope, and a premise added so the claim can survive a counterexample. An item is not a narrowing if it only reads existing claim text, sets a routing or filing rule, or sets an evidence-classification default that creates no escape for an adverse result. Prin-3 B-1/B-2 is the precedent for that. Every item below is counted on its own, so bundling has no effect. Rejected and deferred text is not silently incorporated. **The table itself is a packet-level planning artifact. It does not become claim text.** Only items that read or govern the claim's existing text, or B.9.6 counting, are ruled here.

## Rulings — Recommend-B amendments (PASS2 P-1..P-9 = PASS1 Q-1..Q-9)

| # | Item | Ruling | B.9.6 | Reason and operative boundary |
|---|---|---|---|---|
| P-1 / Q-1 | Role-absence criterion. A system counts as role-free only if no exported field carries information about `τ_cmd + τ_act_unmodeled` beyond what the upper layer can reconstruct from commands and permitted history. A competent system that exports an above-policy-rate observer residual is classified "unresolved: role absence not established" and goes to CR as a possible alternative realization. | **Accept with boundaries** (classification rule for the Grade-2 role row only) | **0.** It restates the existing Grade-2 role text ("effort-information channel that cannot be reconstructed from upper-layer commands … or a fast-tier observer that exports its residual"). It adds no premise and narrows no scope. No counterexample is pending, so it is not a survival premise. | **(i) It does not touch the registered factorial falsifier.** A competent commanded-at-R1 match to realized-at-R1 under the original full-class rule still falsifies **Factor E** for that plant model, whatever the system exports. Factor E concerns a *measured* downstream effort source, which is narrower than the Grade-2 role. Q-1 must never turn a Factor-E witness into "unresolved". **(ii)** "Permitted history" means only the history declared under premise 6 and the C-P1-011 access-boundary record. Undeclared or unaudited history cannot make a channel "reconstructible". **(iii)** "Unresolved" here is a routing state, not an outcome. The CR must decide between realization and witness. It may not stay open indefinitely as a shelter. **(iv) Vacuity flag.** Under an information criterion, almost any export of high-rate body state could count as realizing the role. If so, the Grade-2 role risks becoming near-vacuous, and its falsifiability would rest only on Factors E/R and the B.9.3 test. The implementation-independent B.9.2 argument must address this. If a later fix restricts which channels count as realizations, that is an AM and is counted. |
| P-2 / Q-2 | Factor-drop accounting. Restating the claim on the surviving factor after a single-factor counterexample is a proposed B.9.6 narrowing. | **Accept** (and see follow-up 1) | **0 now.** Prospectively, each accepted restatement is **+1**. | Dropping a factor to survive an admitted counterexample is the paradigm B.9.6 event. So is excluding the counterexample's plant model from the target-plant class to keep the factor. Each distinct change counts separately: dropping the factor *and* carving out the plant model is two events. From 1, a single restatement → 2, and a second → 3, which makes retirement review mandatory. Proposed values are provisional until ruled. |
| P-3 / Q-3 | Premise-6 / C-P1-011 side-channel row. A joint-channel outcome goes to CR on premise 6 under the B.9.4(b) evidentiary standard, plus an AN on which part of the H8 motivation lapses. It does not falsify Factor E and causes no automatic change. | **Accept** (routing) | **0.** Any resulting wording change to premise 6 or to H8 is a separate AM, and its count is ruled then. | H8 already limits what survives a joint-channel finding ("Factor E's nuisance argument still holds, but nothing beyond that"). This row only routes that case. The existing premise 6 stands unchanged: "Upper layer receives only the exported fields". Since the Prin-5 ruling, C-P1-011 distinguishes joint and export-only Markov forms. Premise 6 is the export-only form by its own words. I make **no** cross-reference edit (see Deferred, D-2). |
| P-4 / Q-4 | Common-scope guard on the both-factors retire-nominate route. A comparability audit, not a single run. Different runs may combine. Incompatible scopes each get their own single-factor review. | **Accept** (and see follow-up 3) | **0.** It reads "if both are falsified" together with each falsification's "for that plant model". It is not a new admissibility premise. | The audit is limited to the same plant model and premise declarations (including friction placement) and the same declared task contract. It may **not** require the same run, seeds, detector family or PLAN. The all-detector quantifier stands. Two witnesses are not a commanded-at-R2 system, and they do not show that every effort-information role is dispensable. The claim's retire-nominate route is still triggered as written. If the audit fails, each witness keeps its single-factor review with P-2 accounting. It does not drop out. |
| P-5 / Q-5 | Omitted-rule default. If a PLAN omits a required predeclared rule, the affected comparison is **unresolved**: never a match, never an established failure. | **Accept** | 0 | This implements the Prin-3 B-2 three-way distinction already in the falsifier text. Boundary: an "unresolved" registered comparison does not stop a concrete, competent, in-premise witness from going to CR on its own merits (Prin-3 A-3; P-7). |
| P-6 / Q-6 | Substitution wording. The claim says "more than a stated margin". Future PLANs declare the inequality, aggregation, fixed false-event rate, calibration policy and uncertainty handling. The filed DOWN criterion governs Eng-1 by reference. | **Accept** (and see follow-up 4) | 0 | The claim already says "drop by more than a stated margin". No cutoff or aggregation is inferred. Eng-1 is not rescored (mean 0.1115 / min 0.0625, d50_M10). Proposal A's `≥`/`<` wording has no effect. |
| P-7 / Q-7 | Unlisted-evidence route. A concrete in-premise counterexample, target-premise-failure evidence, or a table–claim conflict may go to CR. Anything else is filed with no claim action. The table may be extended only by a packet decision. | **Accept** | 0 | Under B.9.4 a claim adjudicator can always receive a concrete counterexample. A table cannot cap that. Proposal A's "unlisted → AN until a later packet" is not operative for this claim. If a table row and the claim text conflict, **the claim text and the adjudicator's rulings control.** |
| P-8 | Placeholder `(q,r)` limits only target-scope inferences and target acceptance. A model-level declared task contract is enough for a model-level counterexample to reach CR. | **Accept** | 0 | The falsifier requires "the same declared task's absolute detection and latency contract". It does not require human-ratified target parameters. A placeholder cap would be an uncounted admission restriction, and it would couple claim review to the D-Prin-3-001 Eng-2 gate. Target-scope rows still need target declarations. |
| P-9 / Q-8 + Q-9 | Merges: row IDs; corrected action vocabulary; P-rows; G-rows; artifact destinations; F-3; eligibility checklist in place of tiers. Plus premise-failure independence. | **Accept, with the clarifications on the right** | 0 | **Vocabulary.** N/AN/AM/CR are separate routes, not an ordered scale. AM counts +1 for each accepted scope narrowing or added survival premise. A 0 count needs a written reason from the adjudicator under the Prin-3 B-1/B-2 precedent. **Destinations.** AN → `upgrade-log.md`. Admitted counterexample or premise failure → `violations.md`. AM/CR → a ruling file. Only the bound claim adjudicator writes these. **Eligibility checklist.** A missing element makes the affected comparison unresolved. It is not inadmissible, and it does not cap review of a concrete in-premise witness. **Premise failure on a target.** Needs only provenance, measurement and applicability checks. No competent detector, factorial run or substitution margin is required. Reviewing a Candidate's applicability is not admitting a challenge to a lock, and it authorizes no Eng-2 run. |

## Rulings — Alternate-A merge repairs (same-family text; extra scrutiny)

| # | Repair | Ruling | B.9.6 | Note |
|---|---|---|---|---|
| a | Remove the placeholder `(q,r)` cap | **Accept** | 0 | Same as P-8. |
| b | Replace tiers with a pre-execution checklist plus post-execution verification; require competence of **each** compared system | **Accept** | 0 | Tiers set as binding ceilings before results are read are **rejected** for this claim. They would add uncounted admission restrictions. |
| c | Delete "same sealed run" from ER-1 | **Accept** | 0 | Same as P-4. A same-run rule would be an uncounted narrowing of the falsifier. |
| d | Use "more than" for the substitution inequality; assert no aggregation | **Accept** | 0 | Same as P-6. |
| e | S-2 repeated-fixture trigger becomes optional prioritization only; drop A-1 PLAN-family competence transfer; separate the A-3 routes | **Accept** | 0 | Competence is shown per compared system and per run. It does not transfer by PLAN family. |
| f | A T1 failed intervention still defeats the local realization assertion | **Accept** | 0 | This is already the claim text (Prin-3 B-1): it defeats realization on that fixture, detector and calibration, and does not establish that the information is absent. |
| R-3 | A bandwidth confound may *recommend* a matched control for a future PLAN, but must not demote a competent, premise-matched rate counterexample below CR | **Accept** | 0 | This is consistent with H2 and the Prin-3 A-3 deferral. A-3's dual-tuning rule stays deferred as written. |
| A P-1 | Formal-evidence rows, corrected | **Accept routing** | 0 | A Grade-1 argument must be checked by a B.9.2 route: a formal checker, an established published result matched premise by premise, or a qualified human. A grade reassessment needs its own packet, and a Grade-1 lock also needs the human signature. A formal counter-model gets its own premise and artifact audit and may then be a §4a-type witness. |

**Not operative for this claim:** tier ceilings, the placeholder cap, ER-1's same-run restriction, unlisted → AN, the S-2 prerequisite, PLAN-family transfer, and actions as an ordered scale. The packet's Reject list stands.

## Rulings — claim follow-ups (score-pass1 §5 / score-pass2, items 1–9)

| # | Follow-up | Ruling | B.9.6 |
|---|---|---|---|
| 1 | Is restating the claim on a surviving factor after an admitted single-factor counterexample a B.9.6 narrowing? | **Accept: yes, +1 per accepted restatement, prospectively.** The same applies to carving the counterexample's plant model out of the target-plant class to keep a factor. Each is counted on its own. Keeping the current text unchanged while an admitted in-premise counterexample stands is not an option. The claim must be restated (counted) or retire-nominated. | 0 now |
| 2 | Is Q-1 a clarification or a narrowing? | **Clarification, count 0**, under boundaries (i)–(iv) in P-1. If a later operationalization restricts which channels count as realizations, it is a separate AM and is counted. | 0 |
| 3 | Retire-nominate combination semantics | **Accept as a clarification adding no premise.** Combining needs a comparability audit (P-4 boundary), not a single run. | 0 |
| 4 | Substitution criterion record | **Accept.** Upgrade-log annotation: "more than a stated margin" and the filed DOWN criterion govern. Future PLANs declare inequality and aggregation. No retroactive rescoring. | 0 |
| 5 | Premise 6 / H8 linkage to C-P1-011 | **Accept routing (P-3).** C-P1-011 changed in Prin-5 (premises tightened; ledger). That changes nothing in C-P1-012 automatically. A joint-channel audit outcome is a CR input for premise 6. | 0 |
| 6 | Optional record note: filings cite a table row ID | **Accept** as an upgrade-log annotation. Row IDs are filing aids. They are not claim text and do not bind the adjudicator's ruling. | 0 |
| 7 | Priority-4 identifiability attempt | **Accept routing.** It needs its own PLAN before any search. Its output goes through the corrected formal-evidence rows. No grade change follows from Prin-6. The Grade-1 form stays an open upgrade target only. | 0 |
| 8 | Role-binding check | **Done by this alternate binding**, disclosed above, including the conflict with the claim author's family. | — |
| 9 | Counter | **Confirmed: accepted narrowings = 1.** Prin-6 has no accepted event. | 0 |

## Deferred

- **D-1 — How to audit Q-1 in practice.** How "carries information beyond what is reconstructible" is to be measured (probe, estimator bound, or architecture argument) is deferred to a future PLAN or to the C-P1-011 audit. I endorse no measurement method. Until one is declared, P-5 applies: the classification is unresolved.
- **D-2 — Premise-6 cross-reference after Prin-5.** C-P1-011 now separates joint and export-only Markov forms. Premise 6's parenthetical "(C-P1-011 Markov premise)" could be made explicit as the export-only form. The words of premise 6 already state that form, so the meaning is unchanged. I make no edit. A future ruling may tidy the reference with a written 0-count reason.
- **D-3 — Prin-3 A-3 dual-tuning rule** stays deferred as written. It is not reopened.

## Record changes

- `upgrade-log.md`: **not modified.** The file is read-only (0444), which looks like an append-only guard, and the adjudicator did not override it. The required append is staged verbatim in [`upgrade-log-append.md`](upgrade-log-append.md). Someone with write authority over the log needs to apply it. Until then, this ruling is the operative record of the Prin-6 dispositions.
- `claim.md`: **no edit.** No accepted item changes a premise, the scope, the conclusion shape or the falsifier thresholds. All accepted items are routing, classification or counting rules that read the existing text.
- `violations.md`: unchanged. No counterexample and no premise failure is admitted.

## Disposition

**Grade 2, Candidate, stay.** B.9.2 items outstanding:
- the implementation-independent argument, which must now also address the P-1 (iv) vacuity flag;
- a task-qualified operational realization result;
- a serious, logged search for a competent role-free system;
- a cross-family re-ruling and the human signature.

Retire-nominate is not warranted: no factor has an admitted counterexample. D-Prin-3-001's Eng-2 gate, D-P1-001 (Provisional) and the research order are untouched. No export field, numeric rate or ladder order is mandated.
