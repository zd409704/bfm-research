# Prin-5 — Adjudication PASS2 (order-swapped)

**Adjudicator:** packet adjudicator (did not author either proposal). **Order:** P = proposal B, Q = proposal A.
**Read:** `proposal-P-PASS2.md`, `proposal-Q-PASS2.md`, `review-of-P-PASS2.md`, `review-of-Q-PASS2.md`, `source/packet-brief.md`, `source/method-Appendix-B.md`, root `brief.md` rubric. For checking only: `source/C-P1-011-claim.md`, `source/Prin-4-decision.md`, `source/program-ledger-current.md`.
**Scope:** planning adjudication only. No claim grade or state changes. C-P1-011 stays **Candidate** (Grade 1, narrow form; tighten-premises). No Locked Grade-1. Nothing here is a necessity order (B.8.3).

## 1. Gates (before ranking)

| Gate | P (B) | Q (A) |
|---|---|---|
| Hard Reject: Locked Grade-1 without human | Pass. Candidate stays; lock needs human signature plus non-author transition. | Pass. Candidate stays; amendments routed to the claim adjudicator. |
| Hard Reject: Grade-3 as necessity | Pass. No evolutionary or anatomical citation. | Pass. No such citation. |
| Hard Reject: new Eng-2 spike preconditions beyond D-Prin-3-001 | Pass. "Unresolved" outcome explicitly does not block Eng-2. | Pass, with a wording defect. §5 "unknown → application unaudited" and item 13 (independent sign-off) bind only citation of C-P1-011, and §6 is stated as not a gate. The reviewer's required rewrite ("this theorem application remains unsupported", no effect on Eng-2 authorization) is mandatory. Not a Hard Reject as written. |
| Hard Reject: inventory treated as necessity order | Pass. Inventory completion is explicitly not proof of necessity, sufficiency or order. | Pass. §7 and §1 disclaim order. |
| Incomplete: inventory can yield a falsifiable tighten-premises checklist | Pass. §4 checklist items are checkable. A bypass found by an independent reviewer fails an application. | Pass. TP-1..7 plus a yes/no checklist with artifact pointers. Falsifiable by a missed upper-accessible input. |
| Other (no spike without sealed PLAN; no named products; claim-adjudicator ≠ author) | Pass. | Pass. The optional lemma needs its own claim record and is deferred, so it is not part of the deliverable. |

Both proposals are eligible for ranking. No Hard Reject and no Incomplete.

## 2. Rubric (adjudicator's own scores, 1–5; 5 favorable)

Reviewer totals (B 42, A 37) came from two different reviewers with uncalibrated leniency, so they are not used directly. Scores below are re-derived. I re-checked the algebra in both proposals' core claims.

| Dimension | P (B) | Q (A) | Objection behind any score ≤ 3 |
|---|---:|---:|---|
| Constraint fit | 5 | 4 | A: mandatory sign-off and attribution language, plus a bundling request, push past the minimum deliverable. |
| Principle integrity | 4 | 3 | A: a directed-path certificate does not establish the conditional-independence premise. The reviewer's XOR case (`Z`,`U` fair bits, `X=Z⊕U`, `Y=(X,U)`) gives `I(Z;X)=0`, `I(Z;Y)=1` although the path from `Z` crosses `X`. A also reads `I(Z;X|W)` as "what the export contributes", which is observational, not causal. M3/L1/I1 are stated as consequences of DPI when they are audit policies. The leak-alarm "probability ≥ 1−2α that the chain fails" overstates the inference. The prose says six amendments but the table has seven. B: grade not restated in its own text. The export-only sufficient condition omits `U` and the joint construction. |
| Falsifiability | 3 | 4 | B: no time-box and no closed-world criterion, so "unresolved" can persist. A: yes/no items with artifact pointers can fail within days, though the taxonomy-completeness falsifier is weak. |
| Evidence demand | 5 | 4 | A: exhaustive path certification and attribution estimates could exceed a document review. |
| Failure modes | 4 | 4 | |
| Integrability | 4 | 4 | |
| Latency / criticality | 4 | 4 | |
| Complexity cost | 3 | 2 | B: 7-field record, 8 classes × 9 attributes and no triage. A: 7 amendments, graph language, sign-off, attribution and a lemma overshoot the minimum. |
| Reversibility | 5 | 5 | |
| Stackability | 4 | 4 | |
| **Total /50** | **41** | **38** | |

Margin is small (3 points). The deciding difference is principle integrity: B's math survived re-derivation, and its three wording defects in the claim are real. B's joint-without-marginal example (`X=Z⊕K`, `W=K`) and the incremental form `I(Z;Y|W) ≤ I(Z;X|W)` under the joint Markov premise both check out. A's main certificate is the weaker object. A's inventory content is nonetheless richer in places (see merges below).

## 3. Ranking

- **Recommend: P = proposal B.** Access-boundary certificate with three honest outcomes (export-only justified / joint-channel justified / unresolved), an access-class inventory with every row defaulting to unresolved, and a checklist that corrects three real wording defects in C-P1-011.
- **Alternate: Q = proposal A.** Use as the merge source for inventory content and checklist form (see amendments). Do not adopt its d-separation certificate, attribution reading, leak-alarm lemma, or sign-off wording as written.
- **Reject:**
  1. Treating a directed-path or taxonomy-membership check as proof of the Markov premise.
  2. Any reading of an "unknown/unaudited/unresolved" outcome as an Eng-2 precondition or block.
  3. Making the leak-alarm lemma, an attribution calculation, or an independent sign-off a prerequisite of this packet's inventory.
  4. Reading inventory completion as necessity, sufficiency, or research order.
  5. An open-world "every path accounted for" criterion with no frozen manifest.

## 4. Mandatory amendments to the recommended proposal

1. **Compact register and triage.** Reduce to one register per application: receiver/input or retained state; provenance and temporal extent; assignment (`X`, `W`, blocked, unknown); evidence pointer; owner; consequence of uncertainty. First pass on commands/feedback (B03) and retained history (B04), then expand on demand.
2. **Closed-world premise made explicit.** Certify relative to a frozen, versioned interface manifest reconciled against actual subscriptions, handles, configuration and initialization paths (not design intent). A later-found bypass is a B.9.4(b) premise failure of the application, not a theorem failure.
3. **Merge realized-stream definition of `X`.** Adopt from A that timing, ordering, drops, mode/fault/saturation flags and schema version are inside the declared `X` (or explicitly in `W`) and cannot be left unassigned. Fold into B01.
4. **Merge label provenance.** Add the label source and fixed window/resolution to the Target field: if `Z` is a function of `X` or `W`, mark the application definitional; label sources differ between instances; windows chosen after viewing `Y` are a premise-4 problem.
5. **Merge infrastructure items** (shared seeds and clocks, debug/ground-truth endpoints, shared memory, health/power telemetry) into B02/B06/B07 without adding new categories. Keep A's "config-derived enumeration" requirement.
6. **Fix the export-only sufficient condition.** State: `Y_t = f(X_t,W_t,U)` and `(W_t,U)` conditionally independent of `Z` given `X_t`. Keep "unresolved" wording for anything weaker.
7. **Restate the grade** in the proposal text: Grade 1, narrow form, Candidate. Use one checklist label scheme (no repeated "P2").
8. **Name two missing paths:** (i) the recipient controlling export parameters, so `X` depends on earlier `Y`; (ii) the recipient boundary when the upper layer is composite.
9. **Placeholder sub-items** for C-Eng1-A-01 and C-Eng2-A-01 (one line each, cross-reference only, no gate), as D-Prin-4-001 priority 2 asked.
10. **Eng-2 wording.** Any "unresolved/unaudited" consequence reads: "this particular application of the theorem remains unsupported; no effect on D-Prin-3-001 authorization." No certificate, estimate, sign-off or lemma run is required before Eng-2 proceeds under its existing gate.
11. **Anti-vacuity caution.** A very large `W` can make a valid bound practically empty. An attribution note, if given, must be labeled qualitative or bounded and described as observational, not causal.
12. **B.9.6 accounting.** Log each proposed claim edit by type (explicates an existing premise / narrows scope / adds a premise to survive a counterexample). Grouping is the claim adjudicator's call. Do not pre-bundle.
13. **Role separation.** The bound claim adjudicator for C-P1-011 may share a model family with the author of whichever amendment text is adopted. Check author family against the bound adjudicator before any ruling, and bind an alternate if they match. Currently the adopted text is from the other-family author while the bound adjudicator may be in that family.

## 5. Claim follow-ups (C-P1-011; list, not rulings)

1. Reword conclusion: "unless a channel independent of `X` is added" → "unless additional accessible information is added", conditional and joint (`I(Z;W|X)`), not statistical independence.
2. Reword premise 5: "can only lower" → "cannot increase" (equality possible); processing with `Z`-dependent control (adaptive/event-triggered) belongs inside `X`.
3. Premise 2: noise `U` independent of `Z` given `X` fails after feedback (internal seeds, probe actions). Tie to premise 3: include command/seed state in `W` or narrow to an observation-only setting, and log any narrowing.
4. Premise 4: restate as one joint law per assertion with re-audit on a law change, not "deployment equals evaluation forever".
5. Premise 1: separate target interval from information cutoff and online vs retrospective mode; add label provenance.
6. H4: `I(Z;I1∪I2)=I(Z;I1)` only if I2 is a function of the declared published I1 transcript plus fixed configuration; record I2 provenance.
7. H5: add the closed-world manifest premise as the route by which the claim constrains anything.
8. Reconcile the record's "recommended-for-lock (conditional)" wording against the ledger's "Candidate; tighten-premises" disposition. Bound adjudicator appends the note; authors do not.
9. B.9.2 verification of the exact final statement (whole conclusion, not formula only) by an independent checker, then the human lead's signature on that exact version. Neither is done.
10. Independently re-verify the toy examples used here (B's `X=Z⊕K`/`W=K` and constant-export probe-seed case; the reviewer's `X=Z⊕U` case against A's path certificate). They are stipulated finite variables, not target-stack evidence.
11. Inspect `claims/C-P1-011/upgrade-log.md` and `violations.md` for the B.9.6 history. They were not supplied to either proposal.
12. Leak-alarm lemma: if kept, needs its own claim record, joint coverage specification for detector TPR/FPR and the ceiling, and correct inference wording (controlled false-alarm rate, not a posterior probability; not unique to a side channel). Stays deferred and non-gating.
13. Record that D-P1-001 and the P1 Alternate are not upgraded by this packet (H3 unchanged).
14. Suggested ledger append (append-only): D-Prin-5-001 packet decision (Recommend B with amendments; Alternate A as merge source); no claim-grade changes.

## 6. Confounds and limits

- **Order swap with unequal reviewers.** Each proposal got a different blind reviewer (one reviewed B, the other reviewed A). The reviewers scored with different leniency (42 vs 37), so the raw gap overstates the difference. My re-derived gap is 3 points. Reviews are cross-family with respect to each author, which is symmetric.
- **Pass-1 not consulted here.** This PASS2 judgment is made from PASS2 materials and may be compared with PASS1 afterward. The two passes use the same proposals under swapped labels; consistency across them is the check on position bias.
- **Reviewer and adjudicator did not run anything.** All math is by hand re-derivation. No target-stack manifest exists, so inventory completeness was assessed against hypothetical paths only.
- **Proposals were scored on a different basis from reviews.** One reviewer saw only the brief and appendix; the other also read claim sources for checking. This difference could shift Principle-integrity scores.
- **Small margin.** A different weighting of falsifiability (A better) and complexity (B lighter) could close the gap. The Recommend/Alternate order rests chiefly on principle integrity and on A's certificate not establishing what it claims.
- **No evidence about the target stack.** Neither proposal's access classes were checked against a real implementation. That is the work the audit itself would do.
