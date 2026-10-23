# Prin-5 — PASS1 adjudication score

**Adjudicator:** Packet Adjudicator (Sonnet). I authored neither proposal.
**Pass mapping:** PASS1 P = Proposal A (graph audit, 7 path classes, TP-1..7, leak-alarm lemma). Q = Proposal B (information-access certificate, B01–B08, two analytic stress cases).
**Inputs read:** `proposal-P-PASS1.md`, `proposal-Q-PASS1.md`, `review-of-P-PASS1.md`, `review-of-Q-PASS1.md`, `source/packet-brief.md`, `source/method-Appendix-B.md`, `source/C-P1-011-claim.md`, `source/Prin-4-decision.md`, the rubric in `brief.md`.
**Effect:** Planning only. No claim grade or state is changed here. No Locked Grade-1. No Eng-2 precondition is added beyond D-Prin-3-001. Nothing below is a necessity order (B.8.3).

---

## 1. Gates (before ranking)

| Gate | P | Q |
|---|---|---|
| Locked Grade-1 without human | Pass. Stays Candidate. | Pass. Stays Candidate; any lock needs the human signature. |
| Grade-3-as-necessity | Pass. No biological premise. | Pass. Same. |
| Extra Eng-2 spike preconditions beyond D-Prin-3-001 | **Pass, conditional on rewording.** §5 says an "unknown" leaves the application unaudited and bars citing the claim. Item 13 asks for an independent auditor sign-off. Taken alone those could be read as prerequisites. §6 says the lemma is not a gate. Wording must be scoped to "this theorem application is unsupported", with no bearing on authorization to run Eng-2. | Pass. "Unresolved" is stated not to block Eng-2. D-Prin-3-001 is inherited unchanged. |
| Inventory treated as necessity order | Pass. §7 disclaims ordering. | Pass. Inventory completion is explicitly not proof of necessity, sufficiency or order. |
| Inventory can yield a falsifiable tighten-premises checklist for C-P1-011 (Incomplete test) | Pass. 14 yes/no items with artifact pointers, and a stated falsifier in §9. The falsifier is weakened because the categories are broad enough to absorb almost any missed path. | Pass. 11 checklist items and 8 access classes with a disposition rule. Every row starts as unresolved. Falsification is a reviewer finding a bypass, with no time-box. Needs a closed-world criterion (amendment 1 below). |
| Hard constraints (no named products or companies; no experiments) | Pass | Pass |

**Both proposals are eligible for ranking. No Hard Reject. No Incomplete.**

---

## 2. Rubric (1–5; 5 favorable)

I used the two blind reviews as inputs and adjusted where my own reading differed. I checked the main math claims independently.
- Q's XOR case (`X = Z⊕K`, `W = K`) is correct: `I(Z;X) = I(Z;W) = 0` and `I(Z;X,W) = 1`.
- The review's counterexample to P's directed-path certificate (`X = Z⊕U`, `Y = (X,U)`) is also correct. A directed path crosses `X`, yet `I(Z;Y) = 1` while `I(Z;X) = 0`. Conditioning on `X` couples `Z` and `U`.

| Dimension | P | Q | Note |
|---|---:|---:|---|
| Constraint fit | 4 | 5 | P's mandatory audit language, sign-off and lemma stretch the priority-2 minimum. Q stays inside it. |
| Principle integrity | 3 | 4 | P: the "d-separation certificate" is really directed-path coverage, which is insufficient. The attribution reading of `I(Z;X\|W)` and the leak-alarm "probability ≥ 1−2α" are overstated. Several categorical dispositions are policy, not DPI consequences. Q: the math is correct and it finds real wording defects in the claim. It does not restate the grade in its own text. |
| Falsifiability | 4 | 3 | P has concrete audit questions and a stated falsifier. Q has no time-box and no closed-world criterion, so "unresolved" can persist. |
| Evidence demand | 4 | 5 | Both are document review. P's exhaustive path certificate and independent sign-off cost more. |
| Failure modes | 4 | 4 | P: metadata, labels, infrastructure. Q: vacuity (`W = Y`), marginal screening, feedback seeds, invalidation on change. Q misses open-world non-termination. P risks false assurance from the certificate. |
| Integrability | 4 | 4 | P assigns ownership more concretely. Q leaves the composite-recipient boundary open. |
| Latency / criticality | 4 | 4 | Both offline. Both treat timing as an information channel. |
| Complexity cost | 2 | 3 | P: 7 amendments, graph language, sign-off, attribution, lemma. Q is heavy for a minimum deliverable (seven-field record plus 8 classes with 9 attributes each), but has no optional lemma. |
| Reversibility | 5 | 5 | Paper artifacts. |
| Stackability | 4 | 4 | Both carry over to later audits. P's lemma ties in C-Eng sub-items. Q defers them. |
| **Total** | **38** | **41** | |

The reviews' own totals were P=37 and Q=42. The ranking is the same.
**Confound:** the two reviewers are cross-family. Each scored the other family's proposal and never saw the opponent's text, so absolute scores may carry reviewer leniency. Only the within-pass ordering is used. See §6.

---

## 3. Decision (PASS1)

| Role | Proposal | Reason |
|---|---|---|
| **Recommend** | **Q** | Correct math. Finds real tighten-premises defects in the claim. Fits the minimum scope. Its "unresolved" outcome prevents missing evidence from becoming a ceiling assertion. |
| **Alternate** | **P** | Better concrete channel classes for the first-pass audit. These include timing and metadata, label provenance, infrastructure, and published-versus-internal provenance of derived fields. Its certificate language and lemma are not adopted. |
| **Reject** | (i) Any reading of an unchecked or "unknown" row as "absent". (ii) Treating inventory completion as necessity, sufficiency or order. (iii) Mandatory independent sign-off, attribution calculation or lemma run as a condition of Eng-2. (iv) "d-separation certificate" wording for directed-path coverage. (v) The leak-alarm "probability ≥ 1−2α" statement. | |

PASS2 must be read with the order swapped. The ranking is final only if it is consistent.

---

## 4. Mandatory amendments

To Q, before it is used as the Prin-5 deliverable:

1. **Closed-world manifest premise.** Certify relative to a frozen, versioned interface and configuration manifest. A later-found bypass counts as a B.9.4(b) premise failure in the target setting, not as a counterexample to the theorem. Add a time-box for "unresolved".
2. **Falsifiable failure criterion for the checklist.** Failure means an upper-accessible input or retained state that is absent from the audited boundary record. It can also mean a claimed conditional independence contradicted by an explicit model that satisfies the recorded assumptions. This replaces category-membership as completeness evidence.
3. **Triage order for the minimum deliverable.** Do B03 (commands and feedback) and B04 (retained history) first, since the claim's H2 identifies them as the likeliest omissions. Expand to other classes on demand. This is audit sequencing, not necessity order.
4. **Tighten the export-only sufficient condition** to `(W_t, U) ⊥ Z | X_t` under `Y_t = f(X_t, W_t, U)`.
5. **Name two missing paths.** (a) The upper layer setting export parameters (filter gains, probe requests), so that `X` depends on earlier `Y`. (b) The composite-recipient boundary, where one upper module passes contact-informative data to another.
6. **Import from P** as additional rows or sub-rows. These are inventory content, not new gates.
   - The timing and metadata list: arrival jitter, event-triggered publication, drops, mode/fault/saturation flags, schema presence.
   - Label provenance (`Z` defined from a signal in `X` or `W`). Mark the application "definitional" if `Z = h(X)`.
   - Published-versus-internal provenance for derived fields (TP-6).
   - Enumeration from deployment configuration, not design intent.
7. **Checklist labels and grade.** Use one numbering scheme (P2 appears twice, and P2/P3 once). State "Grade 1, narrow form, Candidate" in the text.
8. **Wording of consequences.** Replace any "unknown ⇒ claim may not be cited" by "this theorem application remains unsupported". State that no Prin-5 certificate, attribution, auditor sign-off or lemma run is required before Eng-2 proceeds under D-Prin-3-001.
9. **Sub-items per D-Prin-4-001 priority 2.** Add one-line placeholder sub-items for C-Eng1-A-01 and C-Eng2-A-01, as map-to-B01/B04/B05/B07/B08 cross-references only, with no gate and no execution condition.
10. **Leak-alarm lemma.** Keep it deferred. If it is revived, it needs its own claim record, a joint coverage specification for the TPR and FPR bounds, and wording as a controlled false-alarm test, not a posterior probability.
11. **Attribution wording.** Any use of `I(Z;X|W)` must be called observational incremental information, not a causal contribution of the export. A qualitative ranking must be labelled qualitative.
12. **Role separation.** See §5, claim follow-up 4.

---

## 5. Claim follow-ups (for claim adjudicators; none decided here)

1. **C-P1-011 wording defects** (proposed tighten-premises edits):
   - "channel independent of `X`" should become "additional accessible information", since statistical independence from `X` is neither required nor typical.
   - "can only lower" should become "cannot increase".
   - Premise 2's noise `U` independent of `Z` given `X` no longer holds after feedback if a seed shapes the later contact.
   - Premise 4's "does not change between deployment and evaluation" should become one law per assertion, with a re-audit on change.
   - Premise 1 needs the target interval and the information cutoff separated (online versus retrospective).
2. **B.9.6 event log.** The adjudicator classifies each amendment as explication, narrowing, or added survival premise, and rules on grouping. Authors' requests for bundling count for nothing. P's prose says six amendments but its table lists seven; reconcile. The upgrade and violation logs were not supplied to the proposals, so no count or retirement clearance is asserted here.
3. **Record reconciliation.** The claim file says recommended-for-lock (conditional) and the ledger says Candidate / tighten-premises. The bound adjudicator appends the reconciling note. The authors may not do it.
4. **Role separation.** Q's author family is the same as the bound claim adjudicator for C-P1-011 (the claim author is the other family). Check author family against the bound adjudicator before any ruling on Q-derived amendment text, and bind an alternate if they match.
5. **H4 amendment (TP-6)** and **event-triggered subsampling inside `X`** (TP-5): rule on whether each is a clarification or a narrowing.
6. **Label-provenance rule** (`Z` definitional): rule whether it belongs in premise 1.
7. **M3 / L1 / I1 policy statements** in P (parameter overlap, label coupling, ground-truth access): decide whether each is a theorem premise, an application-audit rule, or neither.
8. **Verification.** B.9.2 independent check of the whole statement and premise match, and the human signature, remain outstanding for any Grade-1 lock. Nothing in Prin-5 substitutes for them.
9. **C-Eng1-A-01 / C-Eng2-A-01.** Any later link from the audit stays a sufficiency-side cross-reference and creates no new Eng-2 condition.

---

## 6. Confounds

- **Order-swap incomplete.** This is PASS1 only. The recommendation is provisional until PASS2 (P=B, Q=A) agrees.
- **Reviewer asymmetry.** Each proposal was reviewed by a different family, so scoring strictness differs. P received lower marks from one reviewer, Q higher marks from the other. A reviewer-leniency effect cannot be separated from a proposal-quality effect.
- **Blind review.** Neither reviewer saw the opposing proposal. Gaps one proposal covers and the other misses were found only here.
- **Author-adjudicator family overlap** for Q (follow-up 4).
- **Reviewer scores reused.** My table agrees with the reviews on the ordering and the key objections, but this is not independent confirmation. I checked only the two small information-theory examples and the gate language.
- **No target stack manifest.** Neither proposal has been run against a real implementation. Completeness of either taxonomy is untested.
- **Lengths differ** (P is the longer text). I did not score for length.

---

DONE
