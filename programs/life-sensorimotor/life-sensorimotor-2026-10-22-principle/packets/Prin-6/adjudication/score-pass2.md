# Prin-6 — PASS2 adjudication score (order-swapped)

**Adjudicator:** Packet Adjudicator, PASS2. I authored neither proposal and neither review.
**Pass mapping (swapped from PASS1):** P = `proposals/B.md` (witness-based table, four three-valued evidence components, overlap rule). Q = `proposals/A.md` (ceiling table, tiers T0–T3, row IDs). Reviewer of P = `reviews/A-on-B.md`. Reviewer of Q = `reviews/B-on-A.md`.
**Inputs read, in this order:** packet `brief.md`, `roster.md`, `drafts/B/summary.md`, `drafts/A/summary.md`, `proposals/B.md`, `proposals/A.md`, `reviews/A-on-B.md`, `reviews/B-on-A.md`, and the run-level rubric. To check specific points I also read `source/C-P1-012-claim.md` (falsifier, substitution and role text) and `source/C-P1-012-prin3-ruling.md` (A-1..A-5, B-1..B-3). I read `score-pass1.md` only **after** I had drafted §1–§3. Reconciliation is in §4.
**Effect:** planning only. **C-P1-012 stays Grade 2, Candidate.** The accepted B.9.6 narrowing count stays **1**. This adjudication makes no Locked Grade-1 and no grade or state change. It does not change the Eng-2 gate (D-Prin-3-001) or the D-Prin-5-001 nonblocking ruling. It runs no spike, registers or seals no PLAN, and edits no claim file. Nothing below is a necessity order (B.8.3).

---

## 1. Gates (B.9.5, before ranking) — independent draft

| Gate | P (B) | Q (A) |
|---|---|---|
| No grade/state change; no Locked Grade-1 | Pass. Header and packet boundary. The dossier row needs the human lead's signature for any lock and allows no Grade-1 inference. | Pass. §2 "never available" list; §7 non-claims 1–2. |
| Claim adjudicator ≠ author (B.9.1) | Pass. "Amend" is a submission. "Review requests a ruling; it does not enact one." | Pass. AM/CR are reserved to the claim adjudicator, and §5.4 says the orchestrator does not rule. |
| Sufficiency ≠ necessity (B.3.5, B.4, B.5) | Pass. Every acceptance, substitution and sufficiency row withholds necessity. | Pass. Favourable rows are capped at AN. |
| Runner files data only (B.9.8) | Pass. | Pass. |
| Grade-3 / planning order as necessity (B.8) | Pass. | Pass. G-3 is N. |
| Eng-2 non-interference | Pass. "They do not create Eng-2 execution preconditions." | **Pass, conditional.** T1 includes placeholder `(q,r)` and is capped at AN. So no model-level counterexample can reach CR until the human lead ratifies `(q,r)`, which is an input to the Eng-2 gate. That is a coupling, not a formal gate change. It must be removed before any Q text is merged. |
| Falsifier preservation (B.3.4; Prin-3 A-1/A-3) | Pass. It keeps every `d ≥ 10 ms` class, `ΔTPR ≤ 0.05`, `Δp95 ≤ 10 ms` and p95, and it refuses two-design admission conditions. The "common scope" clause needs a guard. | **Pass, conditional.** Thresholds and classes are preserved. But four rules change which counterexamples reach review without B.9.6 accounting: ER-1 "same sealed run" (the claim says only "if both are falsified"); R-3 demotes a rate result to AN when it is bandwidth-confounded (Prin-3 A-3 said not to require two designs); §5.6 sends unlisted evidence to AN; and the placeholder cap above. |
| Fidelity to the filed record | Pass. Verdict fields, DOWN 0.1115 / 0.0625 at d50_M10, and the PLAN hash match. No cutoff or A02 threshold is reconstructed. | Pass. Eng-1 is T1 and the B-3 annotation is not reopened. One wording defect: S-1/S-2 use `≥`/`<`, but the claim says "drop by more than a stated margin". S-1 also asserts an all-identifiable-class aggregation that the sources do not supply. |
| No named products/companies | Pass. | Pass. |

**Both are eligible for ranking. No Hard Reject. Q carries two conditional findings (Eng-2 coupling and falsifier admission restrictions). They must be cleared before any Q text is merged.**

### Independent verification of each review's central objections

- **Review of P, D1 (role absence undefined): confirmed.** The claim's Grade-2 role text lists "a fast-tier observer that exports its residual" as a permitted realization. P's direct-counterexample row ("command-reconstructible or other role-free system") has no rule for telling role absence apart from an alternative realization.
- **Review of P, D2 (factor-drop accounting): confirmed.** P's narrowing row lists class removal, statistic swap, sensing restriction and admissibility premise. It does not list restating the claim on the surviving factor after a single-factor counterexample. Q's E-1 does cover this ("→AM, counted").
- **Review of P, D3/D5/D6 (premise-6 row, artifact destinations, formal-evidence rows): confirmed absent from P.** Q has P-4, the AN → `upgrade-log.md` destination, and P-1..P-3.
- **Review of Q, #1 (tier contradiction): confirmed.** Q defines T2 as "T1 conditions, and: absolute contract met", but T1 is defined by the reference *missing* that contract or by placeholders. Harness validity and competence are also observed results, so §5.1 ("assign the tier … before opening results") cannot be executed as written.
- **Review of Q, #2 (alternative competence): confirmed.** The claim requires that "a falsifying alternative must meet the same declared task's absolute detection and latency contract". Q's T2 checks only the reference.
- **Review of Q, #3–#5: confirmed.** These are the same-run restriction, R-3 demotion, unlisted→AN, U-2 requiring T3 (and therefore every T2 detector condition) for a pure premise-placement measurement, and the `≥`/"more than" mismatch.
- **Additional finding (not raised by either review): P's third row could be read as a placeholder cap.** "A02-class acceptance met, but `(q,r)` are placeholders … → Annotate" applies to acceptance results only, and P's overlap rule keeps components separate. But P never says that placeholder `(q,r)` limits only target-scope inferences. For parity with Q's coupling defect, P should say so explicitly (amendment P-8).

---

## 2. Rubric (fixed brief, 1–5, higher is better) — independent draft

Both reviewers' totals (P 41 from the review of P; Q 36 from the review of Q) came from different reviewers with uncalibrated leniency. I re-derived every score below. Where the two proposals behave the same, they get the same score.

| Dimension | P (B) | Q (A) | Objection behind any score ≤ 3, or the difference |
|---|---:|---:|---|
| Constraint fit | 5 | 4 | Q: the placeholder cap couples review routing to the Eng-2 human input, and the ceilings are framed as binding on downstream text. |
| Principle integrity | 4 | 3 | Q: the T1/T2 contradiction, the reference-only competence check, `≥` vs "more than", and the asserted aggregation. P: role absence is undefined (D1) and the factor-drop has no counter route (D2). |
| Falsifiability | 4 | 3 | Q: the same-run ER-1, R-3 demotion, unlisted→AN and the placeholder cap can keep competent adverse evidence away from review. The concrete E-1/R-1/F-1 → CR routes remain, so I score 3, not lower. P: one competent in-premise witness earns review even with a weak reference. |
| Evidence demand | 5 | 4 | Q: U-2 needs T3 (human-ratified `(q,r)` plus every T2 detector condition) to review a placement measurement. S-2's two-fixture trigger is optional in the text, so I count it only lightly. |
| Failure modes | 4 | 4 | P names weak-reference suppression, ∞−∞, the composition error, rescue bundling and UP leakage, but its "common scope" clause is a latent escape. Q names tier gaming and the F-2 boundary, but it misses its own admission restrictions. |
| Integrability | 3 | 4 | P: no row IDs, no artifact destinations, no premise-6 / C-P1-011 row, no formal-evidence row. Q has all of these plus a filing procedure. |
| Latency / criticality | 4 | 4 | Both keep p95, the duration classes and fair per-rate tuning, and neither mandates a rate. |
| Complexity cost | 4 | 3 | Q: four overlapping tiers, about 30 rows, and exceptions (A-3, S-2) that conflict with the stated ceilings. P: 16 rows and one overlap rule. |
| Reversibility | 5 | 5 | Paper artifacts. |
| Stackability | 4 | 4 | Q: P-rows route the priority-4 identifiability attempt, but A-1's PLAN-family transfer overreaches. P: no proof row, but nothing blocks one. |
| **Total /50** | **42** | **38** | |

## 3. Decision (PASS2) — independent draft

| Role | Proposal | Reason |
|---|---|---|
| **Recommend** | **P = proposal B** | Witness-based, asymmetric routing that follows Prin-3 A-1..A-5 and B-1..B-3 without reopening any of them. It has the correct composition guard (two single-factor witnesses ≠ a competent commanded-at-R2 system), an overlap rule that blocks favourable-row selection, and no admission restriction added to the falsifier. Its defects are omissions that can be repaired by adding wording. |
| **Alternate** | **Q = proposal A** | Merge source for executable apparatus: row IDs, the action vocabulary with per-action counter effects, P-1..P-4, G-1..G-4, artifact destinations, E-1's explicit factor-drop AM counting, and F-3. |
| **Reject** | (i) Tiers as binding ceilings assigned before results are read. (ii) Placeholder `(q,r)` as a cap on model-level counterexample review. (iii) "Same sealed run" for the both-factors route. (iv) Bandwidth confound as automatic demotion of a competent rate counterexample. (v) Unlisted evidence defaulting to AN until a later packet. (vi) The `≥`/`<` substitution wording, and any inferred aggregation or cutoff. (vii) The two-fixture S-2 trigger as a review prerequisite. (viii) PLAN-family competence transfer (Q's A-1). | |

---

## 4. Reconciliation with PASS1 (`score-pass1.md` read after §1–§3 were drafted)

### Score comparison (same proposal, both passes)

| Dimension | B: PASS1 / PASS2 | A: PASS1 / PASS2 | Reconciled |
|---|---|---|---|
| Constraint fit | 5 / 5 | 4 / 4 | Agree. |
| Principle integrity | 4 / 4 | 3 / 3 | Agree. |
| Falsifiability | 4 / 4 | **2 / 3** | A: one-point split. PASS1 weighted the four admission restrictions more heavily. I weight the surviving concrete CR routes (E-1, R-1, F-1) more heavily. Both readings agree that the restrictions are defects and must not be merged. **Reconciled A = 2.5 (midpoint, reported).** The ordering does not depend on this. |
| Evidence demand | 5 / 5 | **3 / 4** | A: one-point split. PASS1 counted the S-2 trigger as a demand. I treat it as optional in the text. Both agree that U-2's T3 requirement is a real added demand. **Reconciled A = 3.5.** |
| Failure modes | 4 / 4 | 4 / 4 | Agree. |
| Integrability | 3 / 3 | 4 / 4 | Agree. |
| Latency / criticality | 4 / 4 | 4 / 4 | Agree. |
| Complexity cost | 4 / 4 | 3 / 3 | Agree. |
| Reversibility | 5 / 5 | 5 / 5 | Agree. |
| Stackability | 4 / 4 | 4 / 4 | Agree. |
| **Total** | **42 / 42** | **36 / 38** | **B 42, A 37 (reconciled).** |

- **Gates:** identical findings in both passes. Both proposals are eligible. A carries the same two conditional findings (Eng-2 coupling via the placeholder cap; uncounted admission restrictions).
- **Review-objection verification:** identical. Every objection that PASS1 confirmed, I confirmed independently.
- **Ranking:** identical. B is Recommend and A is Alternate in both passes, under both presentation orders. The Reject lists match. PASS2 also lists R-3 bandwidth demotion separately (iv), which PASS1 cited under Falsifiability but left out of its Reject list. This is an addition, not a disagreement.

### Order-swap outcome

**The PASS1 Recommend survives.** Proposal B is Recommend and proposal A is Alternate whether B is presented as Q (PASS1) or as P (PASS2). The margin is 6 points in PASS1, 4 in PASS2 and 5 reconciled. The deciding dimensions are the same in both passes: falsifiability and principle integrity, specifically A's uncounted admission restrictions and tier contradiction. B's defects are omissions, and A's are restrictions. Presentation order changed no gate, no ranking and no Reject item.

### Amendments: PASS1's list is adopted, with one addition

The PASS1 mandatory amendments Q-1..Q-9 (to proposal B) and P-a..P-f (to any proposal A text merged in), and merge notes 1–8, are **adopted unchanged** as the packet's amendment set. For ease of reference, B's amendments are relabelled **P-1..P-9** in this pass, and A's repairs keep the letters **a–f**. Summary:

1. **P-1 (= PASS1 Q-1) Role-absence criterion.** A system with an exported observer residual above policy rate is classified "unresolved: role absence not established" and goes to CR as a possible alternative realization. This is a proposed classification rule for the claim adjudicator, not adopted into the claim.
2. **P-2 (= Q-2) Factor-drop accounting.** Restating the claim on the surviving factor is a proposed B.9.6 narrowing with before/after text. The count stays provisional until ruled (1 → would be 2).
3. **P-3 (= Q-3) Premise-6 / C-P1-011 side-channel row.** CR on premise 6 under the B.9.4(b) standard, plus AN on which H8 motivation lapses. It does not falsify Factor E and makes no automatic change.
4. **P-4 (= Q-4) Common-scope guard.** This is a comparability audit, not a new premise, and not a B.9.6 event. Results from different runs may combine after the audit. Results from incompatible scopes each keep their single-factor review.
5. **P-5 (= Q-5) Omitted-rule default.** If a predeclared rule is missing, the affected comparison is **unresolved**: never a match and never an established failure.
6. **P-6 (= Q-6) Substitution wording.** Use "more than a stated margin". Future PLANs declare the inequality, aggregation, fixed false-event rate, calibration and uncertainty handling. The filed DOWN criterion governs Eng-1 by reference.
7. **P-7 (= Q-7) Unlisted-evidence route.** Unlisted evidence may go to CR if it is a concrete in-premise counterexample, target-premise-failure evidence, or a conflict between table and claim.
8. **P-8 (new in PASS2) Placeholder scope.** State that placeholder `(q,r)` limits only target-scope inferences and target acceptance. A model-level declared task contract is enough for a model-level counterexample to reach CR. This is the B-side counterpart of repair a.
9. **P-9 (= Q-8 + Q-9) Merges and premise-failure independence.** Merge notes 1–8 from PASS1 (row IDs, corrected action vocabulary with routes that are not an ordered scale, P-1..P-3 corrected to B.9.2 verification routes, P-4, G-1..G-4, artifact destinations, F-3, and the eligibility checklist replacing the tiers). A target-measurement premise-failure submission needs provenance, measurement and applicability checks only. Neither route authorizes an Eng-2 run.

Repairs to any proposal A text that is merged: **a** remove the placeholder cap; **b** replace the tiers with a pre-execution eligibility checklist plus post-execution verification, requiring the competence of each compared system; **c** delete "same sealed run" from ER-1; **d** use "more than" and assert no aggregation; **e** make S-2 an optional heuristic, drop the A-1 PLAN-family transfer, and separate the A-3 routes; **f** a T1 failed intervention still defeats the local realization assertion (Prin-3 B-1). **Also (new):** R-3 may *recommend* a bandwidth-matched control for a future PLAN, but must not demote a competent, premise-matched rate counterexample below CR.

### Claim follow-ups

PASS1 §5 items 1–9 are carried forward unchanged. All of them go to the bound C-P1-012 claim adjudicator, and none is decided here. The counter stays at **1**, and nothing in Prin-6 is an accepted event.

---

## 5. Confounds

- **Same-family adjudication in both passes.** This PASS2 adjudicator shares a model family with Author A, Reviewer A (who reviewed proposal B), the orchestrator, the original C-P1-012 claim author and the PASS1 adjudicator. The roster's packet-adjudicator binding names a different model within that same family, so this pass is a further deviation from the roster, and I disclose it as such. The order swap controls for presentation order only, not for family. A family-level preference would favour proposal A, and A ranked lower in both passes. That limits the direction of any such bias, but it does not rule out bias in the margin or the merge selections. Class-2 dual cross-family adjudication was not applied.
- **PASS2 is not independent of PASS1 at the input level.** Both passes read the same proposals, reviews and sources. Agreement between them shows the result is robust to order, not that two independent judges agree. I read PASS1 only after drafting, to limit anchoring.
- **Reviewer asymmetry.** Proposal B's reviewer gave "adopt after D1–D2", while proposal A's reviewer gave "revise before adoption". Reviewer leniency cannot be separated from proposal quality. I used the reviews' totals only as inputs and re-derived every score.
- **Proposal B follows the bound adjudicator's family's own prior ruling closely.** Proposal B's author family wrote the Prin-3 claim ruling and is the bound claim adjudicator for C-P1-012. Close fidelity is weaker evidence of independent judgment (B.9.7), and a same-family adjudicator would apply rules drafted by B. PASS1 follow-up 8 (disclose, or bind an alternate cross-family adjudicator before ruling on P-1/P-2/P-4) applies.
- **Length.** Proposal A is about 16 kB and proposal B about 13 kB. Length was not scored. A's extra rows are credited only under Integrability and Stackability.
- **Unavailable artifacts.** No original sealed PLAN, raw results, sensitivity artifact, filed substitution cutoff, A02 thresholds or target measurement was supplied. No numeric criterion is inferred.
- **Inherited evidence confounds** (unchanged and not resolved by either proposal): rate vs observer bandwidth (H2; A-3 deferred); friction placement relative to sensing (H3; DOWN vs UP); weak reference (A02 unmet); `placeholder_qr = true`; a single planar 2-link sim fixture with 3 seeds; substitution drops that depend on the recalibration policy (`same r_w`).

---

## 6. Order-swap recommendation (final)

- **Recommend: proposal B**, with amendments P-1..P-9. **The PASS1 Recommend survives the order swap.**
- **Alternate: proposal A**, used as a merge source only after repairs a–f and the R-3 repair.
- **Grade stays Candidate:** C-P1-012 remains Grade 2, Candidate, with 1 accepted narrowing. No Locked Grade-1. No Eng-2 gate change. No spike.

DONE
