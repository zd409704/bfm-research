# Prin-2 — Blind Reviewer B on Proposal A

Reviewer: Blind Reviewer B, Codex gpt-6-astra. This is a review recommendation, not a claim-state transition or a B.9.2 lock verification.

Reviewed: `proposals/A.md`, `drafts/A/edge-index.md`, canonical `claims/C-Prin2-E{01,03,05,07,09,11,13,15,17,19}/claim.md`, the ten rubric dimensions in `brief.md`, and `source/method-Appendix-B.md`. No Proposal B, draft-B content, or even-numbered edge claim was read. Referenced P1 records and companion upgrade/violation logs were outside this review; their contents and completion are not independently certified here. No claim file was changed.

## 1. Summary

1. A correctly separates runtime availability from acquisition order and leaves every claim Candidate.
2. Agree with quarantining E01, E05, E09, E11, E19 and every acquisition-order reading.
3. E03/E07 contain a sound scalar separation bound; support Candidate-stay with explicit specification and transfer limits.
4. Dispute E13/E15's established Grade-1 characterization: the reviewed material does not establish the required passivity converse or an exhaustive necessity disjunction.
5. E17's interior binary-KL lower bound is sound, but its zero-FPR statement is false and its general theorem is not automatically an S2a-specific edge.
6. Withhold E17's current recommended-for-lock endorsement pending corrections and the specified independent check; no lock is authorized here.
7. No reviewed edge can veto Eng-1; an S2a packet can proceed with declared bypasses and task-level measurement contracts.
8. Recommend retaining A as a provisional research input with the objections below resolved before any promotion; no comparative ranking is made.

## 2. Constraint fit / Principle integrity / Falsifiability notes

**Constraint fit.** A uses generic plant language, preserves D-P1-001 as a provisional acceptance-gate recommendation, distinguishes Candidate from Locked, and requests rather than assumes a human signature. It does not infer hardware transfer from a spike or require late-ladder capabilities. Its working stage definitions are appropriately flagged as unratified. Proposed scientific revisions below are recommendations only; this review changes no claims.

**Principle integrity.** The availability/acquisition split, individual edge IDs, and refusal to promote shared resources into dependencies are strong. However, surviving citation-ablation is only a filter: it does not establish a proof or B.8.2's requirement that the source stage supply the necessary property. E03/E07 assume envelope maintenance in the destination competence specification. Their nontrivial result is a latency impossibility inside that specification, not an independently discovered obligation to implement all of S0a. E13/E15 yield, at best, a restricted rendering constraint, while E17 initially constrains the complete observation channel. Each must keep the mathematical constraint distinct from the named-stage interpretation.

**Gates before scores.** A passes the prohibition on asserting a current lock or Candidate veto. Its proposed upgrade grades require the qualifications below. Scores cannot repair those proof and scope issues. B.9.2 verification and the human signature remain necessary for Grade 1; Grade 2 additionally requires the operational test and logged serious failed counterexample search. This review is neither a formal-checker result nor a published-result item match.

**Falsifiability.** E03's paired-world optimization has a clear potential failure, and E05/E09 suggest useful fixed-base probes. These are one-line proposals, not sealed experiment PLANs with error controls or completed evidence. E13/E15 need a falsifier that tests the claimed port-passivity guarantee, not merely one favorable coupled system. E17 must allow an apparent in-premise violation to trigger an investigation of the derivation, scope, statistical estimates, and channel audit; it cannot automatically be dismissed as a missing side channel. Absence of such experiments is compatible with Candidate status but does not support promotion.

## 3. Per-edge dispositions

All acquisition-order readings remain Grade 3 and quarantined. “Agree” below endorses a review disposition, not a state change.

| Edge | Review disposition | Reason and required qualification |
|---|---|---|
| **E01: S0a → S0b** | **Agree: quarantine.** | A common fast tier is not a necessity edge. A joint-local impedance specification does not entail whole-body viability. A fixed-base example should explicitly show absence of the defined S0a competence rather than merely absence of an envelope controller. |
| **E03: S0a → S1** | **Agree: Candidate-stay for the conditional fixture bound; no lock.** | Subtracting the two scalar equations yields the stated separation and delay ceiling. The result rules out a policy-only implementation under the disturbance-inclusive S1 specification. It neither proves build order nor makes a timely response sufficient for S0a competence. The Grade-2 companion remains unverified in this review. |
| **E05: S0a → S2a** | **Agree: quarantine; correct the information-floor wording.** | Observability need not require a closed viability loop. “Mutual-information floor” and “detection divergence floor” are not generally equivalent, as premise 1 claims. A supported plant might itself satisfy viability through mechanics; lacking a controller alone does not establish the counterexample. |
| **E07: S0a → S2** | **Agree: Candidate-stay for the hidden-contact fixture bound; no lock.** | The same separation proof applies when the two contact worlds have identical available histories before the response. External initiation alone does not establish hiddenness, and self-initiation alone does not establish predictability of the distinguishing wrench. Keep the explicit history condition as the operative premise. |
| **E09: S1 → S2a** | **Agree: quarantine.** | Static sensing or prescribed probing can supply information without full goal-directed whole-body competence. This rejects a universal edge, not possible task-specific benefits of motion. Validate the declared contact class rather than extrapolating one static detector to localization in all configurations. |
| **E11: S2a → S1** | **Agree: quarantine under A's definitions.** | A support-contact information requirement is not the stated non-support S2a edge. Even if support contact is later included in S2a, necessity attaches first to the total available information, not automatically to its body-loop export. Disjoint action sets also need explicit probabilistic success requirements to instantiate q and r. |
| **E13: S0b → S1** | **Dispute the established Grade-1 upgrade; retain as an unverified conditional Candidate argument.** | A sufficient passivity inequality cannot be contraposed into an impossibility result. An exact necessity/converse result for the stated sampled port, impedance class, and B convention must be supplied. Relaxing the passivity specification is leaving the premises, not satisfying an in-premise disjunction. |
| **E15: S0b → S2** | **Same dispute as E13; no lock or gate.** | An unknown environment does not by itself mandate passivity. Under an explicitly chosen passivity specification, verify the converse and the mapping from a joint port to the declared interaction. Treat passive environments as a scoped assumption; interactions with people do not automatically satisfy it. |
| **E17: S2a → S2** | **Dispute recommended-for-lock as written; Candidate-stay pending correction and verification.** | Steps 1–3 establish a necessary joint-channel KL floor. The r = 0 mutual-singularity assertion is false for q < 1. The X-only edge additionally needs W empty or Z conditionally independent of W given X. A large KL value is not an acceptance certificate for the requested detector performance. |
| **E19: S1 → S2** | **Agree: quarantine for the broad edge.** | Supported interaction need not contain whole-body competence. However, definitional inclusion is not categorically prohibited by B.3: a valid functional-completeness claim can concern required subcompetence. It simply supplies no nontrivial universal ladder edge or build order here. |

**E03/E07 mathematical check.** For D > 0 and b > 0, a common applied input cancels, giving Δ′ = aΔ + 2D. Thus Δ(L) = 2D(exp(aL) − 1)/a, or 2DL at a = 0. Both states in [−b,b] require Δ ≤ 2b, yielding the stated L*. The branch L* = infinity for a < 0 and D/|a| ≤ b is correct. Independent arithmetic reproduces 9.531 ms at a = 10, 9.839 ms at a = 3.3, and 10 ms at a = 0 for b/D = 0.01 s. The approximation emphasizes b/D only when |a|b/D is small. A faster channel meeting this necessary deadline may still fail through insufficient authority, saturation, or coupling; this is not a feasibility proof. For arbitrary onset, the paired states must coincide at onset; they need not both be zero for the separation calculation.

**E13/E15 proof debt.** E01 presents b > KT/2 + |B| as a passivity condition. E13/E15 need the stronger statement that above their chosen K threshold no admissible rendering can meet the specified guarantee. The inherited eight premises and exact converse are not reproduced in the reviewed records. A converse might hold for a narrower pure-stiffness class, but measurements of b and K alone cannot establish it. State whether B = 0, how damping is implemented, whether physical damping is fixed, and what is held fixed when faster rendering is claimed necessary. If B is free, changing damping may alter the threshold. Physical compliance is an alternative realization requiring a new plant match; dropping passivity is a specification change. Neither makes the general S0b edge necessary.

**E17 mathematical check and scope.** For a common class-independent channel kernel, KL data processing followed by a binary decision gives D(P1^(X,W) || P0^(X,W)) ≥ d(TPR || FPR). Monotonicity on TPR ≥ q > r ≥ FPR yields the claimed floor. With base-2 logarithms, d(0.95 || 0.01) = 6.02599 bits, consistent with the record. Specify the log base explicitly. Conditional independence Z ⟂ W | X gives a common conditional law of W given X and hence equality between joint-channel and X-only divergence. Without that condition, X can contain no information while W supplies all detection capability. The joint-channel theorem then remains valid but does not upgrade the named S2a edge. Future verification must match the actual observation histories and any adaptive probing to the Markov premise.

## 4. Eng-1 gating implications

**No reviewed edge supplies a current veto.** Candidate claims may shape proposals under B.4. Eng-1 can pursue S2a before completing S0a or S1 and should list E05 and E09 as bypassed Grade-3 edges; any further bypasses depend on its actual scope. This conclusion neither removes D-P1-001's provisional acceptance-gate recommendation nor adjudicates other inherited claims outside this review.

Eng-1 should make the following contract concrete before its spike:

- Define contact classes, onset/window convention, duration, location resolution, task-stated q and r, and the allowed decision/response deadline. Distinguish per-window FPR from false events per unit time.
- Enumerate X, all side channels W, history/memory, commands, and sensor timing. Give ownership for the body-loop export and the consuming decision tier. Test both the complete channel and an X-only ablation where meaningful.
- Evaluate achievable detection operating points with uncertainty and held-out trials. Treat E17's KL floor as a necessary screening bound, not an acceptance criterion sufficient for S2 competence. A low empirical KL estimate is not a certified upper bound on true KL.
- Separate observability from envelope protection and passivity. A supported fixture can permit the experiment; it does not establish target-plant transfer or prove a missing viability capability.
- Seal a runnable PLAN with counterexample and premise-failure criteria before experiments. No reviewed counterexample search has been completed. PASS remains harness evidence only.

After a valid future E17 lock, an in-scope S2 proposal with a verified upper bound on its complete channel below d(q || r) could be rejected. Passing the bound would still not demonstrate achievable detection, localization, timely response, or whole-body safety. E03/E07 would likewise require their disturbance and timing premise matches; E13/E15 cannot become gates merely by filling measurement fields.

## 5. Concrete objections and required resolutions

1. **False zero-FPR claim — E17, premise 2.** Let X be binary with P0(X = 1) = 0 and P1(X = 1) = 1/2. The detector 1[X = 1] has TPR = 1/2 and FPR = 0. The laws overlap at X = 0, so they are not mutually singular, although D(P1 || P0) is infinite. Zero FPR with positive TPR requires a P0-null detection event carrying sufficient P1 mass; mutual singularity follows for perfect detection q = 1. Correct this before endorsing the current nomination.

2. **Necessary floor presented too close to an acceptance floor — proposal §6 and E05 premise 1.** Let P1(X = 1) = 0.01 and P0(X = 1) = 10^−200. This channel has KL approximately 6.56306 bits, exceeding the 6.02599-bit floor for (q,r) = (0.95,0.01). Yet even the optimal randomized detector at FPR ≤ 0.01 achieves TPR at most 0.0199. The large divergence comes from an event rare even under contact. Require an achievable operating-point test as well as any necessary information bound. Mutual information additionally depends on the contact prior and is not interchangeable with this directional KL floor. These examples are algebraic checks, not registered experimental results.

3. **Unverified passivity converse — E13/E15.** Supply the exact necessary condition with item-matched assumptions, distinguish port passivity from stability of one interconnection, and correct the falsifier. A stable or passive coupled example with one favorable environment does not by itself refute failure of a guarantee against every admissible passive environment. Do not label the current gap as measurement debt alone.

4. **Stage identity versus property necessity — E03/E07/E17.** Preserve the narrower theorem even when its stage interpretation fails. A timely channel is not sufficient for the full viability competence; a joint information floor need not be an X-export floor. Explicitly state the additional source-stage mapping before any B.8.2 edge promotion.

5. **Prediction and counterexample classification — E07.** Predictable onset alone does not reveal the sign or magnitude distinguishing the paired worlds. Register the predictable-onset arm's actual observable histories and what they reveal. Classify an outcome as premise failure only after demonstrating that a stated premise fails, rather than preclassifying every success in that arm.

6. **Counterexample fixtures and governance traceability.** Absence of a controller does not prove absence of a property that A expressly allows passive mechanics to realize. E01/E05/E09 experiments must operationalize the missing source competence, destination performance, and unchanged task scope. Record any later repair that adds a premise or narrows scope under B.9.6. The initial zero counters are not disproved by this review, but repairs must not silently retain them when the rule applies.

## 6. Rubric scores

Scores apply to Proposal A alone, after the gate assessment above. Higher is better; evidence demand rewards lower burden for comparable evidential force.

| Brief rubric dimension | Score (1–5) | Rationale / concrete objection |
|---|---:|---|
| Constraint fit | **5** | Respects Candidate status, human signature, generic plant scope, and the provisional acceptance-gate distinction. |
| Principle integrity | **3** | Strong quarantine discipline, but the E17 boundary error, unverified E13/E15 converse, and stage/property conflations block endorsement of all proposed upgrades. |
| Falsifiability | **3** | Useful paired-world failure conditions; no sealed new PLANs, and passivity/side-channel failure classifications need repair. |
| Evidence demand | **4** | Algebraic checks and document audits are inexpensive; target latency, damping, stiffness, and channel-distribution evidence remain substantial and openly deferred. |
| Failure modes | **3** | Names side channels and transfer limits, but misses the rare-event KL failure and overgeneralizes predictability and passivity falsifiers. |
| Integrability | **4** | X/W and runtime/build-order distinctions support an interface contract; stage ownership and complete observation histories remain unsettled. |
| Latency / criticality | **4** | Correct conditional fast-response ceiling; no target premise match or sufficiently explicit end-to-end detection deadline yet. |
| Complexity cost | **4** | No unnecessary architecture is mandated; disjunctive edge labels and overlapping information-floor forms need simplification. |
| Reversibility | **5** | All claims remain Candidate; quarantined edges and proposed observations are cheap to revise before any lock. |
| Stackability | **4** | Frees S2a work from unsupported predecessor requirements while retaining future conditional constraints; stage definitions still need ratification. |

