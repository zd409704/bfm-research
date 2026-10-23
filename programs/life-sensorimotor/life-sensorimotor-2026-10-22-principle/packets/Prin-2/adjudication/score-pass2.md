# Prin-2 — Pass-2 score (order-swap), Packet Adjudicator

Scope: P = `proposal-P-pass2.md` (7 even-numbered edges, E02–E14). Q = `proposal-Q-pass2.md` (10 odd-numbered edges, E01–E19). Read: both proposals, both pass-2 reviews, both gate files, `brief.md`, Appendix B. Basis: reading of the files plus the reviewers' checks. I re-did only the E03/E07 arithmetic (`L* = ln(1+ab/D)/a`; a=10, b/D=0.01 s gives 9.53 ms). I did not independently verify the E10 or E17 proofs. No claim file was edited and no authorship is inferred. Nothing here is a B.9.2 verification or a lock.

## 1. Gate results (Appendix B, before ranking)

| Gate | P | Q |
|---|---|---|
| Grade-3 edge treated as Locked necessity / gate / veto? | No. All 7 edges are Grade 3 / Candidate / quarantined. None gates. | No. E01, E05, E09, E11, E19, every acquisition-order reading, and A-general of E13/E15 are explicitly quarantined. |
| Claims Locked Grade-1 without human signature? | No. No lock is nominated. States that Grade-1 and Grade-2 locks need the human signature. | No. Nothing is Locked. E17 is "recommended-for-lock (narrow formal form), conditional". Brief constraint 7 allows Candidate + recommended-for-lock. |
| Requires a missing Locked Grade-2 role as a veto without an operational test? | No. The snapshot has no Locked claims. Interface items (Z, window, ε, deadline, channel inventory) are framed as proposal completeness, not vetoes. | No. E17 is described as a possible future conditional gate on S2 proposals only, after verification and signature. E13/E15 are explicitly "no force yet". |
| Ladder graded as a whole / D-P1-001 promoted to necessity? | No. D-P1-001 is kept as a Provisional S0a acceptance gate. | No. D-P1-001 is cited only as a Provisional acceptance gate. |
| Planning order cited as evidence; three orders conflated? | No. | No. |
| Citation-ablation applied (B.8.7)? | Yes. | Yes, per edge and per reading. |

**P: ELIGIBLE** (no Hard Reject, no Incomplete trigger).
**Q: ELIGIBLE** (no Hard Reject, no Incomplete trigger). Two caveats do not change the gate result:
- The E17 "recommended-for-lock" nomination is not endorsed (see §5).
- The "Grade 1 conditional" labels on E13/E15 are unverified Candidate hypotheses.

## 2. Rubric scores (1–5)

| Dimension | P | Q | Concrete objection behind any score ≤ 3 |
|---|---:|---:|---|
| Constraint fit | 5 | 5 | — |
| Principle integrity | 4 | 3 | Q: the E17 zero-FPR assertion is false for q<1; the E13/E15 passivity converse is unestablished (a sufficient condition is presented as a necessary one); the stage-identity vs property-necessity conflation is carried into the E03/E07/E17 upgrades. P: the E04/E06 timely-response premise is self-contradictory as written (identical channels up to τ\* plus no common safe prefix make the task infeasible). P's E10 also duplicates inherited C-P1-011. |
| Falsifiability | 3 | 3 | Both give falsifier shapes but no sealed §12.2 PLAN. P's falsifiers are heavily templated across records. Q's E07 predictable-onset arm and E13/E15 falsifiers are misclassified or too weak. |
| Evidence demand | 5 | 4 | Q: leaves target b/D, T+δ, b_j and K_req,j measurement debt open. |
| Failure modes | 4 | 3 | Q misses the rare-event KL failure (high KL but unachievable TPR at FPR ≤ r) and overgeneralizes the predictability/passivity falsifiers. |
| Integrability | 3 | 4 | P: S0b/Q1 contracts are left undefined with no draft contract, so ownership is unresolved. |
| Latency / criticality | 3 | 4 | P: the E04/E06 content is a runtime timing matter but is not stated as a latency bound, and the premise defect blocks it. |
| Complexity cost | 4 | 4 | — |
| Reversibility | 5 | 5 | — |
| Stackability | 4 | 4 | — |
| **Total** | **40** | **39** | Near-tie. Totals are not decisive and gates already passed. |

Scores rely on the two blind reviews, adjusted where I found a reviewer's point load-bearing.

## 3. Stance on ladder edges and Eng-1 gating

Both packets reach the same operative stance: no edge gates Eng-1 today. All acquisition-order readings stay Grade 3. S2a can proceed without S0a/S1 completion, with the bypassed edges listed with their grades.

- **P: Recommend** as the baseline stance.
  - It is the most conservative, with no lock nomination.
  - Its quarantine of every registered edge is consistent with the claim-level rulings. The even-edge adjudication confirmed Grade 3 for all seven.
  - Its unresolved defects (the E04/E06 premise, E10 duplication) are fixable and do not touch the gating stance.
- **Q: Alternate.**
  - Its availability/acquisition split, X/W channel enumeration and E03/E07 separation bound add useful positive design structure.
  - It is held below Recommend because its headline upgrade (E17 recommended-for-lock) and the E13/E15 Grade-1 characterization are not sustainable as written.
  - Its gating stance (nothing gates today) is correct and adoptable now.
- **Reject:** neither.

## 4. Edges as design inputs vs gates (only edges cited in the proposals)

**Gates now: none.** Every cited edge is Candidate, and Candidate cannot veto (B.4). D-P1-001 stays an S0a acceptance-gate recommendation, not an edge.

**Design inputs only (shape Eng-1 proposal completeness, never reject a route):**
- **E10 (S2a→S1), with C-P1-011:** specify Z, window, ε, deadline, and the full joint-channel inventory including side channels W.
- **E17 (S2a→S2) KL/binary-test floor:** state the task-stated (q, r) and the resulting divergence floor. Add an achievable operating-point test; the floor is a necessary screening bound, not an acceptance criterion.
- **E03/E07:** report the loop period against the timing ceiling, using b/D per support mode. This is a conditional fixture bound.
- **E04/E06:** a timely-response/safe-probing note, once repaired.
- **E13/E15:** record the measurement debt only. They carry no force.

**Declared as bypassed Grade-3 edges** (B.8.5) for an S2a-first Eng-1: E05 and E09 (Q numbering) and E06, E08 and E14 (P numbering). If S1 is developed without a prior S2a stage, also list E10 (P) and E11 (Q).

**Could gate later, only after verification and human signature:**
- E17 or E10, as a conditional gate on online contact-conditioned or S2 decisions. It would constrain runtime information availability, not S2a work itself and not packet chronology.
- E03/E07/E04/E06 as timing requirements, after a Grade-2 route or a Grade-1 check, with a target premise match.

**Never gates:** E01, E02, E05, E08, E09, E11, E12, E14, E19, and all acquisition-order (Reading P) claims.

## 5. Mandatory amendments before any lock

1. **E17 zero-FPR premise:** correct it. Zero FPR with positive TPR does not imply mutual singularity; that holds only for perfect detection (q=1). Specify the log base.
2. **E17 channel scope:** require W empty or Z ⟂ W | X for the X-only form. Keep the joint-channel theorem distinct from the named S2a edge. Add an achievable-operating-point criterion (the rare-event counterexample: KL 6.56 bits yet max TPR 0.0199 at FPR 0.01).
3. **E13/E15:** supply the exact necessary condition (converse) with item-matched premises and fixed coefficients, covering B, damping and the sampled-port class. Port passivity must be distinguished from stability of one interconnection. Relaxing the specification or adding compliance is a premise change, not an in-premise disjunct, and any narrowing is logged under B.9.6.
4. **E04/E06:** restate the premise with an information-arrival time t0 < τ\* so it is feasible. Reclassify it as a latency lower bound (Grade-1 shape) plus a Grade-2 role claim, and decide whether the safe-probing variant belongs on E06 at all.
5. **E10:** cite or merge into C-P1-011 and request a single independent verification. Resolve the S2a-contract vs information-in-H bridge.
6. **E03/E07:** keep the theorem (latency impossibility under the disturbance-inclusive specification) separate from the stage interpretation. State the source-stage mapping before any B.8.2 promotion. Replace the E07 predictable-onset preclassification with the observable-history premise.
7. **Stage definitions:** ratify canonical S1, S2, S0b and S2a contracts (human lead, planning level). Q's working definitions and P's S2a contract are unratified.
8. **B.9.8 PLANs:** seal at least one runnable counterexample PLAN per upgrade candidate (the E10 finite-fixture check, the E03 paired-world optimization, the E05/E09 fixed-base probe). One-line sketches do not count.
9. **B.9.2:** an independent proof check (formal checker, item-matched published result, or qualified human) and the human lead's signature. No author signs its own transition. Model agreement is not grade evidence (B.9.7).
10. **Falsifier deduplication (P):** replace the templated closing paragraphs with per-edge variables, thresholds and bypass-witness artifacts.

## 6. Confounds

- **Order-swap duplication.** The pass-2 files are byte-identical to the pass-1 files with the P/Q labels exchanged: `proposal-P-pass2` = `proposal-Q-pass1`, `proposal-Q-pass2` = `proposal-P-pass1`, and likewise the reviews. Pass 2 therefore adds no new evidence. It only tests label or position bias, and any difference from pass 1 should be read that way.
- **Label leakage.** The body text of several files (author labels, reviewer headers, packet inventories) carries source-label headings that do not match the P/Q anonymization. I did not use them to attribute and did not rely on them.
- **Disjoint edge sets.** P covers the even-numbered edges (7), Q the odd-numbered ones (10). Edge-level coverage is not like-for-like (for example, Q has S0a→S2 and S2a→S2, P has neither), so total scores are not comparable on coverage. The two proposals also number their edges differently.
- **Review asymmetry.** Each review read only the one proposal and its own edge set. Reviewers were blind to the other, and the claim-level rulings were produced per edge parity by different adjudicators with different scrutiny levels (the odd-edge ruling tightened premises; the even-edge ruling quarantined all). This may inflate the apparent conservatism difference.
- **Template and length effects.** P's claim records are templated, which may flatter or penalize falsifiability depending on how the reader weighs boilerplate. Q's greater detail (numbers, fixtures) may read as stronger than its verified status.
- **Narrowing counts.** E04, E06 and E10 carry one proposed narrowing each, none adopted. Any adopted E13/E15 restriction counts toward B.9.6, with retirement review at the third.
- **Score margin.** A 1-point total difference sits within rater noise, and the reviewers' rubric scores may anchor mine.
- **LLM-checked mathematics.** The proofs for E10, E17 and E03/E07 have only been checked by LLM reviewers and adjudicators. No B.9.2 verification has occurred.

D-P1-001 remains a Provisional S0a acceptance gate, not a necessity order.
