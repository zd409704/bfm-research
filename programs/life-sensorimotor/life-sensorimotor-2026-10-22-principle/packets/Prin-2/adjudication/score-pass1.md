# Prin-2 — Score, pass 1 (proposals P and Q)

Adjudicator: Packet Adjudicator (Sonnet). I did not author either proposal and I make no attempt to identify their authors. This file changes no claim record and no claim state. Inputs: the two proposals, the two blind reviews, the odd-edge and even-edge claim rulings, `brief.md`, and Appendix B. Edge IDs below are the ones used inside each proposal. P uses the odd namespace and Q uses the even namespace. See §6 for how the two namespaces overlap.

## 1. Gate results (Appendix B, applied before ranking: B.9.5, §4 Step 4)

| Check | P | Q |
|---|---|---|
| Treats a Grade-3 edge as Locked necessity, gate or veto | No. E01, E05, E09, E11, E19 and every acquisition-order reading are quarantined. E13/E15 A-general is quarantined. | No. All seven edges are Grade 3, Candidate and quarantined. |
| Claims Locked Grade-1 without the human signature | No. Every claim is Candidate. E17 is *nominated* recommended-for-lock, and the signature and independent check are requested, not assumed. | No. No lock is nominated. |
| Requires a missing Locked Grade-2 role as a veto | No. No Locked claims exist, and neither proposal vetoes on a role. | No. Same. |
| Grades the ladder as a whole | No (P §5.1 and §8) | No |
| Cites D-P1-001 as evidence of necessity | No. It is a Provisional acceptance-gate recommendation (P §5.2). | No. It is preserved as such. |
| Evolutionary or developmental order used as more than Grade 3 | No | No |
| Bypass declaration for Eng-1 | Yes: E05, E09 | Yes: E06, E08, E14, plus E10 if S1 is developed without S2a |

**P: ELIGIBLE.** It has two blemishes, neither a gate failure, and both must be fixed before any promotion:
- The E17 recommended-for-lock nomination rests on a record with a false statement. The zero-FPR mutual-singularity claim is false for q < 1.
- The E13/E15 "Grade 1 conditional, disjunctive" label is disputed. The review shows a sufficient passivity inequality cannot simply be contraposed into a necessity result.

**Q: ELIGIBLE.** One premise defect (E04/E06 premises 3 and 4 are jointly unsatisfiable as written) and one coverage gap (§6). Neither is a gate failure.

Neither proposal is Incomplete or Rejected.

## 2. Rubric scores (1–5)

Both are eligible, so both are scored. The reviewers' tables were used as input, not copied. A low score has a concrete objection.

| Dimension | P | Q | Basis |
|---|---:|---:|---|
| Constraint fit | 5 | 5 | Both respect Candidate status, the human signature, generic plant scope and D-P1-001. |
| Principle integrity | 3 | 4 | P: the strict separation of availability from acquisition is excellent. It is offset by the E17 zero-FPR error, which sits in the one edge nominated for lock. It is also offset by the unverified E13/E15 converse and by stage-versus-property conflation. Q: grade discipline is clean and nothing is overclaimed. It is docked for the inconsistent E04/E06 premise and for the E10 kernel duplicating C-P1-011. |
| Falsifiability | 3 | 3 | P has a concrete paired-world numeric falsifier for E03/E07 (9.53 / 9.84 / 10.0 ms). Its E13/E15 falsifier is wrong, and it has no sealed PLAN. Q names bypass witnesses and a cheap finite-fixture check for E10, but the records are templated and no PLAN is sealed. |
| Evidence demand | 4 | 5 | Q is purely analytic. P needs target `b/D`, `T+δ`, `b_j` and `K_req,j`, plus an independent proof check and a side-channel audit. |
| Failure modes | 3 | 4 | P misses the rare-event KL failure (large KL with a low achievable TPR at the allowed FPR) and overgeneralizes the predictability and passivity falsifiers. Q names a bypass per edge and guards against relabelling the source stage. |
| Integrability | 4 | 3 | P's X/W channel split and Z/(q,r)/d(q‖r) specification form give Eng-1 a usable interface contract. Q lists interface items but leaves S0b and Q1 undefined. |
| Latency / criticality | 4 | 3 | P has an explicit tier argument (`T_R2 + δ` against `L*`). Q recognizes the timing content but never states it as a bound, and O1 blocks the argument as written. |
| Complexity cost | 4 | 4 | Neither mandates architecture. P's disjunctive labels and overlapping information-floor forms add some bookkeeping. Q's boilerplate is repeated. |
| Reversibility | 5 | 5 | All claims are Candidate. |
| Stackability | 4 | 4 | Both free S2a work from S0a and S1 predecessors. P adds a conditional S2 constraint. Q adds less structure. |
| **Total** | **39** | **40** | A statistical tie. The totals do not decide the recommendation; the content in §3 does. |

Scores apply only after the gates. They cannot repair any proof or scope defect.

## 3. Packet stance on ladder edges and Eng-1 gating

The two proposals agree on every point that matters for Eng-1:
- No edge gates Eng-1 now.
- No lock is currently supportable.
- S2a work may proceed without finishing S0a or S1.
- The skipped edges must be listed with their grades.
- D-P1-001 stays a Provisional S0a acceptance gate, not a necessity order.

The independent claim rulings confirm this. Of the 17 edges ruled on, 12 are Grade 3 and quarantined (five odd, seven even). The other five stay Candidate at best (E03, E07, E13, E15, E17), with conditional Grade-1 labels that have not been verified. None has any Eng-1 gate authority.

| Item | Verdict | Reason |
|---|---|---|
| **Common stance: no edge gates Eng-1. Edges are design inputs and bypass-declaration items only.** | **Recommend** | Both proposals reach it. Both blind reviews and both claim adjudications support it. |
| **Q as submitted (seven edges, all Grade 3, quarantined, no lock)** | **Recommend** (with the §5 amendments) | It is the safest stance and is fully consistent with the gates. Its weakness is thin coverage, and it covers no S2 edge. |
| **P as submitted (ten edges, E17 nominated for lock, three conditional Grade-1 labels)** | **Alternate** | It carries more usable content than Q: the E03/E07 timing bound and the E17 specification form. But the E17 nomination is premature, and the E13/E15 Grade-1 labelling is not supported. |
| Any text promoting an edge into a gate or veto now | **Reject** | Violates B.4 and B.8.7. |

Recommended synthesis: adopt Q's grading (everything Candidate; the Grade-3 edges quarantined) as the packet disposition. Adopt P's E17 specification form and E03/E07 timing bound as *design inputs*. Treat the E17 lock nomination as not yet supportable.

## 4. Which edges may influence Eng-1, as design inputs or as gates

**Gates: none.** Candidate and Grade-3 claims cannot veto (B.4, B.8.7). There are no Locked claims.

**Design inputs (shape proposals and tests; no veto):**

| Edge (ID in proposal) | Use in Eng-1 | Conditions |
|---|---|---|
| E17 (P): S2a → S2 | Require the specification form: contact variable `Z` (class, window, resolution), task-stated `(q, r)`, the floor `d(q‖r)` with the log base stated, and an explicit side-channel `W` enumeration including efference copies. Treat the floor as a *necessary screening bound*, never an acceptance criterion. | Add an achievable-operating-point test (TPR at FPR ≤ r). Correct the zero-FPR statement. |
| E10 (Q) ≈ E11 (P): S2a → S1 | Total-variation kernel: worlds with disjoint acceptable actions need `TV ≥ 1−2ε` on the joint history. Use it to shape the decision-interface contract (the information must be present at the online decision). | Cite C-P1-011 and state the kernel as a corollary. Keep it separate from the named S2a export. |
| E03 (P) ≈ E04 (Q): S0a → S1; E07 (P): S0a → S2 | Timing contract: state the response deadline and loop period against `L* ≈ b/D`. Measure `b/D` per support mode first, not plant instability `a`. | E04's premise must be repaired (§5). E07 is limited to externally initiated contacts, or to a stated history condition. |
| E13 (P) ≈ E12 (Q); E15 (P): S0b → S1/S2 | Measurement debt only (`b_j`, `K_req,j`, damping convention). No force until the converse is verified. | Do not use as a rendering mandate. |
| E05/E06, E09/E08, E01/E02, E19, E14 | Hypothesis organizers. They are listed as *bypassed* with Grade 3. A hardware test needing the body to stay in its operating region is a test-condition enabler, not an edge. | None. |

**Conditional future gates (not active now):**
- E17: only after a corrected statement, an independent B.9.2 check, a side-channel audit, task `(q, r)` and the human signature. It could then reject an S2-stage proposal whose verified complete-channel bound is below `d(q‖r)`. It would never gate S2a work or chronology.
- E10: the same lock path applies. It could constrain runtime information availability at an online contact-conditioned decision. It would never constrain packet chronology.
- E03/E04/E07: only after the Grade-2 realization test, a logged serious counterexample search and the signature. They would be a timely-response role for a specified online task. They would not make S0a a build-order prerequisite.

## 5. Mandatory amendments before any lock

Common to both packets:
1. Ratify the S1 and S2 definitions. P's working definitions are unratified. Q's single Q1 is undefined. Several rulings depend on them (E03, E07, E11, E19; E04, E06, E10).
2. Seal a runnable counterexample PLAN under §12.2 for each upgrade-attempt edge. One-line proposals and prospective falsifiers do not meet B.9.8.
3. Reconcile the two claim namespaces (§6) so that each edge has exactly one canonical record. Merge duplicated records.
4. Obtain independent B.9.2 verification and the human signature for any Grade-1 lock. Add the logged failed counterexample search for any Grade-2 lock. Model agreement counts for nothing (B.9.7).
5. Keep D-P1-001 explicitly labelled Provisional, a non-necessity acceptance-gate recommendation.

For P:
6. E17: correct premise 2. Zero FPR with positive TPR does not give mutual singularity; that follows only for q = 1. Add the condition Z ⟂ W | X (or an empty W) for the X-only edge. State the log base. Add the achievable-operating-point test, since a large KL is not an acceptance certificate. Distinguish mutual information from directional KL.
7. E13/E15: either supply the exact converse, with the sampled port, impedance class, B convention and what is held fixed, or downgrade the label to "unverified conditional". Fix the falsifier. Port passivity is not stability of one interconnection.
8. E03/E07: keep the theorem (scalar separation bound) separate from the stage interpretation. State the source-stage mapping before any B.8.2 promotion. Have the general-`a` extension checked independently. For E07, make the observable-history condition the operative premise.
9. E01/E05/E09: counterexample fixtures must operationalize the missing source competence. Absence of a controller is not absence of the property.

For Q:
10. E04/E06: restate with a pre-deadline indistinguishability time t0 < τ* and a distinguishing channel in [t0, τ*]. As written, premises 3 and 4 are jointly unsatisfiable. The result is then a response-latency bound, not a stage edge.
11. E10: cite C-P1-011 and present the kernel as a corollary, with one verification. Do not run a parallel Grade-1 track. Do not spend a narrowing event on E06's active-probing variant if it is better filed elsewhere. All proposed narrowings count toward B.9.6, and the third triggers mandatory retirement review.
12. De-template the claim records. Give each edge a specific falsifier, with variables, a threshold and what counts as a bypass witness.
13. Add a minimal S2a contract (Z, window, ε, deadline, channel inventory) and cover the S2-involving edges, or state explicitly that they are out of scope.

## 6. Confounds

1. **Different edge sets under different namespaces.** P's records are the odd IDs and Q's are the even IDs. The mapping is partial: S0a→S0b (P:E01, Q:E02), S0a→S1 (E03/E04), S0a→S2a (E05/E06), S1→S2a (E09/E08), S2a→S1 (E11/E10) and S0b→S1 (E13/E12) appear in both. P alone covers S0a→S2 (E07), S0b→S2 (E15), S2a→S2 (E17) and S1→S2 (E19). Q alone covers S0b→S2a (E14). The two proposals therefore do not compete on identical items. The rubric totals compare unequal scope. Q has no S2 edge and so has no analogue of the one upgrade candidate with the most Eng-1 value (E17).
2. **Duplicate claims for one edge.** Each shared edge has two records with possibly different grades and wording. This is a governance risk unless merged. It also inflates "agreement". Where the proposals agree, the content was not independently derived from the same record.
3. **Different reviewers and different scoring calibration.** Each proposal was reviewed by a different reviewer. Their scale use differs: the review of Q rates Evidence demand 5 where the review of P rates comparable analytic cost 4. The review of Q also read less of the other side. The rubric totals differ by one point and are within reviewer noise.
4. **Unequal verification depth.** The review of P re-derived the E03/E07 numerics and the E17 KL floor independently, and found concrete errors. The review of Q checked the E10 algebra, and the claim ruling notes that this was an LLM check and not a B.9.2 verification. Q's lack of errors found may reflect less ambitious claims, not higher quality. Similarly, P's lower Principle-integrity score reflects the cost of making stronger claims.
5. **Self-identifying metadata.** Both proposals and the rulings carry author and model-family headers, so anonymization is not clean. I did not use these headers to score, and I make no inference from them. Cross-family adjudication was bound per claim, but the binding differs between the odd and even sets.
6. **Reliance on inherited claims whose verification state is unknown.** C-P1-001, C-P1-002, C-P1-010, C-P1-011 and C-P1-012 are Candidate. Neither the reviews nor I verified them. E03, E07, E13, E15, E17 and E10 depend on them.
7. **Prior ordering context.** The brief itself suggests that Eng-1 is likely to be S2a. That may bias both proposals toward concluding that S2a can proceed. The conclusion is still correct on the evidence: the upstream S2a edges are Grade 3.

DONE
