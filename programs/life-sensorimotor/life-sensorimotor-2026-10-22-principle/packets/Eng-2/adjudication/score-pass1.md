# Eng-2 adjudication — PASS1 score (P, Q)

**Adjudicator:** Packet Adjudicator (Claude Sonnet); authored neither proposal.
**Pass:** PASS1 of an order-swap. Labels here are P and Q only. PASS2 swaps the labels.
**Inherited:** D-P1-001 Provisional (acceptance-gate, not necessity order). D-Prin-2-001: no ladder edge is an Eng-2 gate. D-Prin-3-001: the common hard gate binds both branches. D-Eng-1-001 is Closed FAIL.
**Read:** proposal-P/Q-PASS1, review-of-P/Q-PASS1, source/packet-brief.md, source/Prin-3-decision.md, brief.md rubric.
**Not read:** the two deferred PLAN files, claim records, and the logs. Statements about PLAN internals rely on the proposals and the blind reviews. The mandatory amendments below are phrased so that they can be checked against the PLANs.
**Status:** Provisional. This is a planning ranking. It authorizes no spike, changes no claim state, and signs no lock.

## 1. Appendix B gates (applied before ranking)

| Gate | P | Q |
|---|---|---|
| Hard Reject: Locked Grade-1 without human | Clear. P files a new Candidate Grade-1 narrow lemma (C-Eng2-A-01). Nothing is Locked and no lock is nominated. | Clear. New hypotheses are grade N/A. Nothing is Locked. |
| Hard Reject: Grade-3 as necessity | Clear. C-P1-003 is quarantined. The bypassed edges are logged as ordering readings, not refuted. | Clear. Same treatment. |
| Hard Reject: executing a spike despite the Prin-3 `(q,r)` / measurement-point gate | Clear. The spike is deferred and no results are asserted. The `PLACEHOLDER` carry-over is flagged below as an amendment. | Clear. The PLAN is marked "DEFERRED; NOT EXECUTION-AUTHORIZED" with approvals PENDING. No spike directory was created. |
| Incomplete: missing deferred-spike marking when the PLAN claims runnable now | Clear. The spike is labeled "deferred-runnable". Only Stage 1 (document-only XC-1) is called executable now. | Clear. Deferred marking is explicit in both the proposal and the PLAN. |
| Override of D-Eng-1-001 Alternate-B routing labeled as a proposed planning choice | Met, with the cost of delaying B stated. | Met. The cost is stated in CPU time only (see Q-A5). |
| Symmetric eligibility (placeholders for fixture work, ratification for acceptance, no Candidate veto) | Met. The B-skeleton is specified but does not make B executable. | Met. The B-contract numbers are weak (see Q-A4). |
| Channel-level upper reference that can fail informatively | Met in form. It is an exact-reference ceiling on the unchanged Eng-1 fixture. Interpretation labels are overreaching (see P-A1, P-A2). | Partial. The reference is a ceiling on a new surrogate, with parameters chosen by the author and an oracle comparator (see Q-A1, Q-A2). |
| No named products or companies | Clear. | Clear. |

**Gate outcome:** No Hard Reject and no Incomplete for either proposal. Both are eligible to rank. Neither is cleared for execution; that is blocked for both by the common gate (D-Prin-3-001).

## 2. Rubric scores (fixed rubric, 1–5; low scores carry an objection)

| Dimension | P | Q | Objection or basis |
|---|---:|---:|---|
| Constraint fit | 4 | 4 | P carries the Eng-1 values as `PLACEHOLDER`, which is not the human's exploratory policy. Q pre-fills a motor-side measurement point that the gate reserves for the human lead. |
| Principle integrity | 3 | 4 | P: the new claim lacks upgrade-log and violations records, and the genie outcomes are over-read (P-A1, P-A2). Q: grades are inherited by paraphrase, not by decision ID. C-Eng2-B-01 is a unit test rather than a hypothesis. |
| Falsifiability | 4 | 2 | P's ceiling test runs on the real fixture and can return a data-dependent limit (P-A3 and P-A4 repair the threshold and tail issues). Q's SHORTFALL/clear split is a closed-form function of author-chosen parameters. Its detector gap is largely forced by a class-oracle comparator, the FPR test is underpowered, and the B-contract is probably non-discriminating. |
| Evidence demand | 4 | 5 | Q: CPU only, ≤ 15 min, ≤ 1 GiB. P: CPU only, but its CPU-minutes claim for nuisance quadrature is unsubstantiated. |
| Failure modes | 3 | 3 | P misses genie-success mis-inference and rare-tail numerical error. Q misses the oracle asymmetry, sample-size-driven UNRESOLVED, and degenerate envelope parameters. |
| Integrability | 4 | 4 | Both give clear ownership and use `UNKNOWN` on stale scope. P's placeholder-rejection check (C-Eng2-A-03) is not in its H-list. Q's non-interference gate is trivial. |
| Latency / criticality | 4 | 3 | P keeps genie computation off the reflex path, but deployment latency is unmeasured. Q's known-onset reset protocol avoids the latency question that Eng-1 asked. |
| Complexity cost | 3 | 3 | P: two genie tiers and quadrature need tighter justification. Q: a whitening checker plus a 36-cell grid mostly confirms what is known in advance. |
| Reversibility | 5 | 5 | Both are cheap to abandon, with no claim promotion. |
| Stackability | 4 | 3 | P stays tied to the S2a fixture and Eng-1's open question. Q's surrogate cuts its tie to Eng-1, so a result does not open the next stage. |
| **Total** | **38** | **36** | The gates do not alter the totals. |

The two blind reviews scored P at 37 and Q at 36. This adjudication differs from them by +1 on P, within one point per dimension on the dimensions where I diverge.

## 3. Ranking (PASS1)

| Role | Proposal | Basis |
|---|---|---|
| **Recommend** | **P** (38) | It answers the "detector or channel?" question on the actual Eng-1 fixture. Its ceiling is a real channel-level upper reference with data-dependent outcomes. Its defects are interpretation labels and PLAN specification, which are fixable by amendment before sealing. |
| **Alternate** | **Q** (36) | The governance is clean, but Q answers the question on a new author-parameterized surrogate and does not diagnose the Eng-1 miss. It can become the Alternate-class branch only after its discriminating-power fixes. |
| **Reject** | None as a whole. | Reject-class items within either proposal: (a) reading `DET_GAP_OPEN` or `NUISANCE_LIMIT` as a licence to route away from detector work, or as a detector opportunity, on genie evidence alone; (b) treating Q's oracle-referenced "gap" as detector inefficiency; (c) treating a placeholder-based or surrogate result as task acceptance or hardware transfer. |

The margin is 2 points. It is within the noise of order-swap and reviewer-family effects (see section 5). PASS1 alone does not settle the ranking.

## 4. Mandatory amendments (before sealing or trusting the ranking)

**Both proposals**
- B-1. Record the human lead's `(q,r)` table or placeholder policy, the measurement-point declaration, and the branch choice. Carry their identifiers into the reseal. The branch choice is not implied by clearing the common gate.
- B-2. Keep the label "proposed override of D-Eng-1-001 pending the human lead". State the cost of delaying B in program cycles (ratification, seal, adjudication), not only in CPU time.
- B-3. Add the verdict-precedence and default rules that cover currently unrouted outcome combinations.
- B-4. Leave B.9.6 event accounting and any C-P1-012 amendment to the claim adjudicator.

**P**
- P-A1. Rename `DET_GAP_OPEN` as genie-only success with unresolved exported-channel headroom. Require a witness that uses only the exported channel before it makes a detector family eligible.
- P-A2. `NUISANCE_LIMIT` requires G-full to meet a valid floor and G-marg to fall below a valid ceiling. Otherwise report the marginal ceiling with unresolved attribution. Do not route away from detector work on the weaker label.
- P-A3. Fully specify the reference likelihood: the null-window template, the joint nuisance and template laws under each hypothesis, and the marginalization rule. If the analytic form is unavailable or mismatched, the ceiling is `UNRESOLVED`. Agreement at three MC thresholds is a diagnostic, not proof of optimality.
- P-A4. Assign the ceiling threshold `t*` to a calibration split, or justify a selection-valid sweep. Check convergence of the actual tail probabilities and of the decision at `r = 0.001`, not AUC. State the actual quadrature dimension and timeout outcome.
- P-A5. Resolve the H5 versus "PASS iff all H" conflict. Specify the apples-to-apples reproduction of the Eng-1 window sampling against the fresh-episode estimator. Fix the D0 `MET` condition for d50. Do not give the aggregated routing decision a per-cell 95% guarantee.
- P-A6. Add the C-Eng2-A-03 mutation test (placeholder certificate, stale certificate, out-of-scope request) as an explicit deferred check. Supply the upgrade-log and violations records for C-Eng2-A-01 through the claim workflow. Use a per-cell `(q,r)` table in XC-1 and the PLAN.

**Q**
- Q-A1. Add a class-agnostic reference (mixture or GLRT with calibrated null), or report the oracle gap and the class-agnostic gap separately. Rename "attainable" to "attainable given a class oracle".
- Q-A2. Pre-register the analytic 36-cell upper-reference table and the predicted status per cell, and state that only the comparator side is empirical.
- Q-A3. Raise the null sample sizes or calibrate at about r/3. State the predicted rate of FPR-driven `UNRESOLVED`.
- Q-A4. Rescale the envelope contract so that at least one delay is predicted non-CERTIFIED, or label its numbers illustrative. Offer the measurement point as one option among several, not as the default.
- Q-A5. Cite inherited grades by decision or ledger ID. Move C-Eng2-B-01 into the harness gates. Do not count the trivial non-interference gate as evidence for C-Eng2-B-03. Register the paired test or drop the pairing claim. State that this branch postpones the unknown-onset question rather than narrowing it.

## 5. Confounds (order-swap)

- **Position and label effect.** In PASS1, P is the first-listed proposal. PASS2 reverses the labels, so the two passes must agree for the ranking to count as consistent. A one-pass 2-point margin does not establish the ranking.
- **Reviewer-family asymmetry.** Each proposal was reviewed by the rival family. The reviewer of P gave 37 and the reviewer of Q gave 36. Their stringency may differ. The reviews also differ in kind: one is mostly statistical-specification critique, the other is mostly pre-computation and design-adequacy critique. Q's reviewer ran a binomial bound and flagged hand estimates that need owner confirmation.
- **Anonymization leak.** Both proposal files and reviews state the author or reviewer family in their headers. P's text also discloses that a directory listing exposed the first lines of the rival's task prompt. No draft content was read, so the confound is minor.
- **Unread artifacts.** This adjudicator did not read the PLAN files, so PLAN-level defects are credited from the reviews. They are not independently confirmed.
- **Review-derived estimates.** Q's reviewer's O1, O2, O3, and O4 figures are hand or generic-binomial estimates. They need confirmation by the PLAN owner before they can be treated as fact. They drive Q's low falsifiability score, so a reversal of those estimates would raise Q's total.
- **Prior-pass interaction.** The Prin-3 decision showed a flip between passes on a close margin. Treat a PASS1 margin of this size as provisional.

## 6. Disposition

**Provisional (D-P1-001).** The common gate (D-Prin-3-001) binds both branches. No ladder edge is an Eng-2 gate (D-Prin-2-001). PASS1 outcome: P Recommend, Q Alternate, pending PASS2 and the mandatory amendments. The human lead decides between amended-A, amended-B, and neither after the common gate.
