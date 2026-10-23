# Blind review B on A — Prin-6

**Disposition: revise before adoption as a binding routing table.** Proposal A is useful as a planning draft, but its present ceilings and tier definitions are not reliably actionable. The repairs below concern evidence handling; they require no grade change. C-P1-012 remains **Grade 2, Candidate**, with **one accepted narrowing**. This review makes no claim ruling, registers no PLAN, runs no spike, and changes no Eng-2 gate.

**Review boundary.** Read the run and packet brief/roster, every supplied file in `source/`, `proposals/A.md`, and `drafts/A/summary.md`. Did not read proposal B or its draft tree. Historical rulings supplied in `source/` were treated as evidence; their linked underlying proposals and experimental artifacts were not opened. This is a review of A alone, not a comparative ranking.

## Strengths

- **Correct separation of evidence and authority.** The proposal consistently forbids score-driven promotion, export mandates, numeric rate mandates, target acceptance, and planning-order inference. It routes substantive rulings to the independent claim adjudicator and leaves Eng-2 authorization unchanged.
- **Good preservation of the inherited falsifier.** E/R rows retain the full registered `d ≥ 10 ms` set, the existing TPR and p95 thresholds, prospective comparison semantics, and an unresolved outcome. They do not revive reference-selected classes or replace tail latency with a more convenient statistic.
- **Useful asymmetry.** A successful realization or performance advantage is local sufficiency/realization evidence; a competent, premise-matched alternative can challenge necessity. UP fixture results remain external diagnostics. The friction-model rows distinguish a residual-nuisance counterexample from a model that removes the nuisance premise.
- **Traceable governance.** Row IDs, forbidden inferences, record destinations, and explicit B.9.6 accounting would make future submissions easier to audit. The count of one agrees with the supplied Prin-3 ruling; bundled substantive rescues are not supposed to hide separate events.
- **Faithful historical disposition.** The supplied verdict supports the proposal's treatment of Eng-1 as a valid harness with A02 unmet, placeholder parameters, no registered Factor-E/R counterexample, failed DOWN substitution, and out-of-scope UP substitution. None of that establishes necessity.

## Defects and required repairs

1. **The tier algorithm cannot be executed as written (§3; §5 step 1).** T2 requires “T1 conditions” while also requiring the reference to meet the absolute contract. T1 includes a competence failure or placeholder parameters. Read literally, T2 either contradicts itself or inherits placeholders; T3 then cannot consistently remove them. Moreover, harness validity and reference competence are observed results, so a final tier cannot be assigned before opening results. Predeclare eligibility rules and analysis rules before execution; separately verify provenance, observed validity, competence, and premise fit afterward. Write each tier's conditions explicitly and distinguish model-task parameters from target-ratified parameters. This repair must not impose target authorization requirements on every model-level counterexample.

2. **Reference competence does not establish alternative competence (§3; E-1, R-1, F-1).** A reference just above an absolute TPR threshold and an alternative just below it can satisfy the allowed relative difference. The claim explicitly requires the falsifying alternative itself to meet the same absolute detection and latency contract. “Competent match” needs that executable definition for each alternative, in addition to the unchanged relative matching rule and full registered class set. It cannot be inferred merely from T2 eligibility.

3. **The fixed ceilings can shelter the claim from valid adverse evidence (§1; R-3; ER-1; §5 step 6).** Unlisted evidence defaults to annotation until another packet; a bandwidth confound can demote an otherwise competent rate counterexample; and ER-1 requires both factor matches in the same sealed run. The supplied Prin-3 A-3 ruling explicitly refuses to require extra controls to admit an independently competent, premise-matched counterexample. The claim does not require both falsifications to occur in one run. Compatible evidence across runs needs a comparability audit, not automatic exclusion. Add an explicit route to adjudicator review for any concrete in-premise counterexample, evidence of target-premise failure, or conflict between table and claim. The adjudicator can reject the submission on evidence, without an automatic grade/state change. Diagnostic controls may strengthen attribution but must not silently become new falsifier restrictions. Any substantive exclusion proposed to preserve the claim needs separate B.9.6 review.

4. **Premise-failure evidence is given irrelevant competence prerequisites (U-2; T3).** A declared target measurement can establish sensor/nuisance placement without a competent detector, a substitution margin, or a factorial comparison. Requiring all T2 conditions before reviewing that measurement obstructs the premise-failure route recognized in the supplied Prin-3 A-5 ruling and B.9.4(b). Give premise evidence its own provenance, measurement, and applicability checks. Distinguish review of a Candidate's applicability from admission of a challenge to a future lock. Neither route authorizes an Eng-2 run.

5. **Substitution semantics are incomplete and potentially altered (S-1–S-3).** The current claim says “more than” a stated margin; S-1 uses `≥` and S-2 uses `<`. Equality is consequently credited despite the claim wording. The proposal also asserts an all-identifiable-class aggregation rule, while the supplied adjudication expressly says the filed numerical cutoff is unavailable in the reviewed summaries. Preserve the exact filed criterion by reference; do not infer its cutoff or aggregation from the verdict. Future PLANs must state the inequality, aggregation, fixed false-event rate, calibration policy, and uncertainty handling explicitly. Add a separate unresolved-substitution outcome: an uncertain estimate below a margin is not automatically established non-realization. Conversely, a valid failed intervention can defeat the local realization assertion even with A02 unmet, as Prin-3 B-1 states. T1 annotation must preserve that distinction, rather than imply that all results are merely uncredited searches. No retroactive rescoring is warranted.

6. **Several local rules overreach or contradict the advertised ceilings.** A-1 should not make other runs eligible merely because they share a PLAN family; competence and applicability must be checked for each comparison's relevant evidence. A-3 offers review after no competent detector is found despite the global competence-unmet annotation ceiling. S-2's two-fixture trigger has no supplied methodological basis and should remain an optional prioritization heuristic, never a review prerequisite. F-2 and P-4 overstate accounting when they suggest every wording change is counted: log and adjudicate each proposed change, but count scope narrowings and rescue premises, not every neutral clarification. These examples need explicit precedence rules between routing, annotation, review, and amendment; those actions are not simply interchangeable points on one strength scale.

7. **Formal-evidence routing needs a distinct verification path (P-1/P-2).** “Checked independently” should reference the permitted B.9.2 verification routes rather than imply any independent model review suffices for a Grade-1 lock dossier. A formal counter-model requires its own premise/artifact audit, not spike-tier semantics. P-1 also conflates grade reassessment with lock signature: B.9.2 requires the human signature for locking. This packet should authorize neither, while accurately describing a later upgrade review and the separate requirements for locking.

## Appendix B gates and criterion scores

Scores are **1–5, higher is better**, assessing this planning artifact rather than the truth or grade of C-P1-012. Appendix B does not prescribe numerical weights; these are reviewer assessments tied to its criteria. Gates are considered before scores.

**Gate finding:** no supplied source establishes a Locked principle conflict or a missing Locked Grade-2 role in this planning artifact. A claims no promotion, lock, spike authorization, or new engineering gate. Nevertheless, its proposed binding admissibility restrictions are not ready for adoption under B.3.4/B.9.6: they could change which counterexamples reach review without accounting for that change. A high aggregate score cannot cure this defect.

| Appendix B criterion | Score | Evidence / objection |
|---|---:|---|
| Explicit premises and honest scope — B.3.1, B.6 | 3 | Placement and scope are explicit, but tier contradictions and competence requirements for premise-failure evidence confuse applicability. |
| Permitted conclusion shape and grade discipline — B.2, B.3.2 | 5 | Retains the Candidate functional-role claim; makes no new necessity or grade finding. |
| Implementation independence — B.3.3 | 4 | Preserves alternative effort implementations and friction-model search; fixed routing restrictions could still exclude valid alternatives. |
| Violation/falsification mode — B.3.4 | 2 | Alternative competence is not explicit enough; same-run restriction, bandwidth demotion, and unlisted-evidence ceiling can obstruct counterexamples. |
| Sufficiency versus necessity — B.3.5, B.5 | 5 | Performance and realization successes never promote the claim. |
| Candidate authority and lifecycle — B.4 | 4 | No Candidate veto or lock; future challenge routing needs clearer separation from present Candidate review. |
| Artifact traceability — B.7 | 4 | Row IDs and log destinations help; filings still need exact claim/PLAN/result versions, premise audit, class-wise absolute and relative outcomes, and unresolved fields. |
| Ladder discipline / citation ablation — B.8 | 5 | No biological argument bears necessity weight; planning order is explicitly denied evidentiary force. |
| Role separation and lock verification — B.9.1–2 | 4 | Independent adjudicator retained; formal verification/signature wording needs correction. |
| Operational realization test — B.9.3 | 3 | Intervention is concrete, but equality, aggregation, uncertainty, and competence-failed negative outcomes need repair. |
| Challenge routing and gates before ranking — B.9.4–5 | 2 | Target-premise failure inherits irrelevant experiment conditions; blanket ceilings constrain review. |
| Narrowing counter — B.9.6 | 4 | Correct inherited count and retirement-review trigger; new admissibility restrictions must themselves be audited and neutral edits distinguished. |
| Agreement is not evidence — B.9.7 | 5 | Explicitly excludes researcher agreement from grade evidence. |
| Counterexample-search governance — B.9.8 | 4 | Sealed PLAN and runner/claim-authority separation retained; final tiers cannot precede observed results. |

The fixed brief rubric yields the following additional scores; these do not replace the gates above.

| Brief dimension | Score | Reason |
|---|---:|---|
| Constraint fit | 4 | Scope and engineering gates preserved; binding review restrictions need repair. |
| Principle integrity | 3 | Strong non-promotion discipline, weakened by counterexample restrictions. |
| Falsifiability | 2 | Concrete matching rules exist, but the routing defects can suppress their consequences. |
| Evidence demand | 3 | No new experiment here; T3 and repeat-fixture conditions can impose unnecessary future demands. |
| Failure modes | 4 | Several confounds anticipated; tier and competence logic remain unresolved. |
| Integrability | 4 | Filing roles and record destinations are clear; action precedence is not. |
| Latency / criticality | 4 | Retains p95 and duration classes without inventing a rate mandate; rate/bandwidth attribution remains limited. |
| Complexity cost | 3 | Extensive coverage is useful, but overlapping tiers and exceptions complicate routine filing. |
| Reversibility | 5 | Planning-only artifact, with no claim or engineering execution change. |
| Stackability | 4 | Supports later evidence dossiers without demanding later capabilities; family-level eligibility must not transfer automatically. |

## Actionability without changing claim grade

**Not actionable as a binding table in its current form; actionable after the routing repairs above.** Annotation of the existing Eng-1 evidence and retention of all non-promotion boundaries are already usable. The prospective tier assignments, substitution decisions, and adverse-evidence ceilings need correction before routine use.

A minimally usable filing should identify the row, exact claim and evidence versions, predeclared analysis rules, harness status, applicable premises and permitted channels, absolute competence of the relevant cells, unchanged class-wise matching outcomes, unresolved quantities, requested review/annotation, and any separately proposed amendment. Unexpected adverse evidence must remain reviewable. Logging or routing evidence changes neither grade nor state; any later amendment or disposition belongs to the bound adjudicator. This review does not authorize edits to claim records or `decision.md`.

## Confounds and limits

- Source/rate separation, rate-dependent detector tuning, and observer bandwidth remain distinct issues. Fair tuning is required; extra controls cannot be an uncounted escape condition.
- Sensor placement, residual nuisance after friction fitting, permitted side channels, and parameter provenance determine premise fit. Fitting on disjoint data helps but does not itself establish all premises.
- A weak reference, undefined p95 from misses, class selection, loose confidence rules, and placeholder task parameters can make a comparison uninterpretable. Neither an undefined comparison nor a failed competence search establishes necessity.
- Substitution measures the channel's role for a fixture, detector, calibration, and intervention policy. It does not establish information absence or implementation-independent obligation.
- The supplied materials contain no original sealed PLAN, raw results, sensitivity artifact, or verified target measurement. Numerical cutoffs, additional independence across fixtures, and transfer are not inferred.
- The roster binds this reviewer across family from A, while the planned packet adjudicator shares A's family. Order swapping can address presentation order, not family dependence. The common source packet also limits independence of agreement. No agreement or score here is grade evidence.
