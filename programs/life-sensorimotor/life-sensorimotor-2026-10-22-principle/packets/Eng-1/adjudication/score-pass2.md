# Eng-1 — Adjudication score, pass 2 (P / Q)

Adjudicator: Packet Adjudicator (Claude Sonnet). I authored neither proposal. I make no claim-state changes.
Inputs read: proposal-P-pass2, proposal-Q-pass2, review-of-P-pass2, review-of-Q-pass2, gate-C-Eng1-A-01, brief.md, Prin-2-decision.md, method-Appendix-B (gate lines 29, 42, 98-99, 133, 136, 147).
Not read: the sealed PLAN files. I did not re-verify their hashes and relied on the proposals' summaries and the reviewers' statements about them.

Labels here are P and Q only, as in the pass-2 filenames.

## 1. Gate results (applied before ranking, B.9.5 / §4 Step 4)

| Gate | P | Q |
|---|---|---|
| Grade-3 treated as Locked necessity | PASS. Every Grade-3 reading is quarantined and no edge gates. | PASS. Same. §8 lists the bypassed edges. |
| Locked Grade-1 claimed without human signature | PASS. No Locked claim is asserted, and C-P1-001 is only "conditional recommendation-for-lock". | PASS. States "No Locked claim, no recommended-for-lock". |
| C-Eng1-A-01 or any Candidate used as veto gate | PASS. P does not use C-Eng1-A-01. Its inputs are explicitly "no gate, no veto". | PASS with a required amendment (M1). Q uses C-Eng1-A-01 as the soundness basis of its acceptance test, which is a design input and not a veto. Wording such as "meets the S2a floor" must not read as a gate (see M1). |
| Eng-1 ladder-edge gates (Prin-2: none) | PASS. None imposed. | PASS. None imposed. |
| B.8.5 bypassed-edge list (at least E05/E06, E08/E09, E14; E10/E11 if S1 without S2a) | PASS. Complete, and it separates "waived prerequisite" from "experimentally bypassed". | PASS. E05/E06, E08/E09, E14 and E10/E11 are all listed. |
| Incomplete (missing Locked Grade-2 role without an operational test) | Not applicable. No Locked Grade-2 role exists. | Not applicable. |
| Plant scope (home humanoid / target plant only, generic names) | PASS. | PASS. |
| D-P1-001 treated as acceptance-gate, not necessity order | PASS. | PASS in text, but see M2 on two unsupported planning arguments. |

Both proposals are eligible. Neither is rejected at the gates. Reviewer lean: both reviewers leaned Alternate, so nothing in the gate stage separates P from Q.

## 2. Rubric (1-5, fixed brief rubric). Low scores carry an objection.

| Dimension | P | Q | Basis |
|---|---:|---:|---|
| Constraint fit | 4 | 4 | Both obey hard constraints. P: spike artifacts are placed under `drafts/` instead of `spikes/<packet-id>/`. Q: the claimed match to the C-P1-012 registered search changes the false-event units (0.01 per 100 ms window against a registered 0.01/s). |
| Principle integrity | 5 | 4 | P has exact grades, a clean necessity/sufficiency split and a complete bypass list. Q is sound but leans on a Candidate lemma for its acceptance test. It also makes two unsupported methodological claims in §1.3/§1.4 (planning order posing as necessity; merging recreating the confound). |
| Falsifiability | 2 | 3 | P: the reviewer's float estimate shows state margin about 4x and command margin about 14x in every cell, so "supported" is near-certain. The witness search cannot see saturation failures, and B-02/B-03 are close to tautological. Q: it has real controls and contrasts that can fail, but H2 (universal-zero null) and H3 (oracle FPR bound at the calibration boundary) can reject a correct harness. |
| Evidence demand | 5 | 4 | P is CPU-only at 15 min / 1 GiB. Q is CPU-only at about 30 min, but conservative rare-event bounds may need larger samples. |
| Failure modes | 3 | 3 | P names its risks, but the saturation-witness gap undercuts the authority row. Q names many, but calibration boundary, multiplicity and latency censoring are unresolved. |
| Integrability | 4 | 4 | Both give clear generic ownership. P leaves expiry/handoff for the decision core untested. Q leaves W input history, rates and publication age/jitter open. |
| Latency / criticality | 3 | 3 | P: the certificate is offline, which is the right tier, but the 0.2 s validity has no recertification or invariance story. Q: body-loop ownership is right, but the observer bandwidth differs across rate cells and the latency statistic has no censoring rule. |
| Complexity cost | 3 | 3 | P: exact arithmetic, producer/checker split and mutation suite buy little at 4x-14x margins. Q: the duplicated 8-cell factorial and statistics need a tighter protocol. |
| Reversibility | 5 | 5 | Both are synthetic, CPU-only and cheap to abandon. |
| Stackability | 3 | 4 | P: no next step after a SUPPORTED result, and it stays at S0a. Q: the export interface and W register feed later stages without forcing an order. |
| **Total** | **37** | **37** | Tied. Totals are for reference only. Gates govern, and a rubric row never substitutes for a gate. |

## 3. Disposition

| Packet | Disposition | Reason |
|---|---|---|
| **Q** | **Recommend (provisional)**, conditional on M1-M6 and a resealed PLAN | The tie on totals is broken by information value, not by principle quality (P is stronger there). Q's spike can give filed data bearing on the open Candidate C-P1-012 and yields a reusable export contract. It also follows the S2a direction that the inherited Alternate and Prin-2 point to. That direction is a planning preference only. Q's defects are protocol-level and fixable by reseal. |
| **P** | **Alternate** | Its principle hygiene is the best of the two. As frozen, its spike mostly validates certificate bookkeeping on a fixture where a float calculation already predicts the outcome. Moving the fixture to the certification boundary (P-M1) would make P a competitive primary. |
| Reject | none | No gate failure in either. |

The Recommend rests on Q being repaired. If Q's PLAN cannot be resealed in time, Q stays Recommend-provisional with a PLAN-only decision, and P is not promoted by default.

## 4. Spike decision

- **Q spike: run only after a resealed, newly versioned PLAN (v2) that applies M3-M5.** Running the current sealed PLAN would risk H2/H3 failing a correct harness and a false match to the C-P1-012 registered search. If v2 is not sealed before the wall clock (deadline epoch 1792708988, 18:43:08 EDT), file the PLAN only and keep the decision provisional.
- **P spike: do not run as frozen.** Run it only if P is later elevated and the fixture is amended per P-M1 to P-M3 and resealed. Its expected outcome as frozen is "all 16 cells certified; authority stress UNRESOLVED_SATURATION", which is low information. Record that expectation before any run.
- For either spike, PASS validates the harness only. It never validates hardware transfer and never moves a grade.
- Both spikes are CPU-only, so they raise no cloud-GPU approval question.

## 5. Mandatory amendments

Q (conditions on Recommend):

- **M1. Candidate is not a gate.** Reword Q's acceptance test so that "meets the S2a floor" is a chosen engineering specification. Its soundness cites C-Eng1-A-01 as a Candidate with Grade 1 scoped, B.9.2 unmet and no signature, per gate-C-Eng1-A-01. State explicitly that the lemma may guide XC-0 exploration but may not veto or impose a necessity gate. State `0 < r < q <= 1` and consistent log units for the channel KL and `d_cert_bits`.
- **M2. Remove two unsupported planning arguments.** Drop the §1.3 claim that richer S0a certification would let planning order pose as necessity. Drop the §1.4 claim that merging fixtures itself recreates the rate/source confound. Keep the evidence-demand argument. Either S0a or merged work is a legitimate engineering choice under D-P1-001.
- **M3. Statistics.** Give each r-specific detector its own ID and certificate, and say whether coverage is pointwise or simultaneous. Predefine multiplicity control or independent confirmation for any selected cell or packet-wide claim. Replace H2 "all NULL certificates are zero" with a predeclared coverage check plus deterministic invariants. Fix H3 by calibrating conservatively below r, with a predeclared tolerance and enough data, and keep certification data independent of calibration data.
- **M4. Registered-search match.** Either file a registered amendment to C-P1-012's search or keep the registered false-event rate (0.01/s) with a stated mapping to window decisions. Do not describe the results as the original counterexample search until units and event semantics agree. Also resolve the observer-bandwidth confound (matched bandwidth or tuning budgets, or narrow the inference to these two rate-specific implementations). Treat commanded-effort duplicates across placements as shared baselines. Scope the output-torque-sensor cells, since C-P1-012 excludes plants with dedicated torque sensing.
- **M5. Event and latency semantics.** Seal rules for censored pulses (an onset at 60 ms with a 50 ms duration), pre-onset alarms, missed detections in latency statistics, detector warm-up and reset, and the margin type (one-sided noninferiority or absolute difference). Predefine the substitution-test class subset on separate data. State the retrain/recalibrate policy. Scope the "role not realized" message so that a small drop is not read as proof that effort information is absent.
- **M6. W and publication.** Declare W input rates, history lengths and availability times, with no future samples. Add publication age, jitter and queue policy before any hardware integration. Mark the placeholder q/r as provisional until the human lead ratifies the contact-class table, and use a fresh confirmation set afterwards.

P (conditions on any elevation):

- **P-M1. Move the fixture to the certification boundary.** Extend the delay sweep until certification is lost, or calibrate j and K so cells straddle it. Preregister the expected boundary so the prediction can fail.
- **P-M2. Add a saturation-aware witness generator.** Use extreme or bang-bang replays in the clipped recurrence, and keep the rule that only verified replays count.
- **P-M3. Add a handoff/invariance check.** Test whether the terminal augmented-state enclosure lies inside the declared initial set.
- **P-M4. ID hygiene.** Use a distinct prefix for engineering hypotheses (for example `H-Eng1-B-*`) or file minimal records marked "engineering sufficiency, no grade". Merge B-02/B-03 into harness criteria. Record the spike path deviation. Clarify m[100] and the noise indexing in the PLAN. State the post-SUPPORTED next packet.

Both:

- **A-1.** Reseal as a new versioned PLAN. The runner makes no silent discretion.
- **A-2.** Carry the Prin-2 amendments forward: no Grade-1 nomination without B.9.2 checks and a human signature, and no Candidate becomes an Incomplete-gate until sealed counterexample PLANs are registered.

## 6. Confounds (no deanonymizing)

- **Tied totals.** Both proposals total 37 on my scoring. The Recommend/Alternate order rests on a judgement about information value, not on the rubric margin. A different weighting could reverse it. The reviewers also split near the same line (38 and 37 in their absolute scores).
- **Reviewers saw one proposal each.** Their scores are absolute, not comparative, and the two reviewers may calibrate differently. I took the objections as evidence but scored independently.
- **Order swap.** This is pass 2 of an order-swap design. I did not read pass 1 and cannot say whether the ordering is consistent across passes. Cross-pass consistency should be checked before the decision is finalized.
- **Presentation effects.** One proposal is far more polished on principle hygiene. The other adds a claim record and so exposes more governance surface. I tried to score substance, but I cannot rule out residual bias toward either.
- **Unverified artifacts.** I did not read or hash-check the sealed PLANs. The reviewers' numbers for P (margins, saturation witness, terminal-set bound) are non-rigorous float estimates, not spike results. Q's statistical objections come from one reviewer's reading of the PLAN, and I have not independently re-derived them.
- **Dependence on one lemma.** The Q Recommend relies on a Candidate lemma that is sound pointwise but not locked (B.9.2 unmet). If the lemma were later retired or narrowed, Q's acceptance-test framing would need rework, though the export interface would survive.
- **Wall clock.** Whether M3-M5 can be resealed before the deadline is outside this review. A late reseal turns the Recommend into a PLAN-only provisional decision.
- **Reuse of claim-namespace IDs.** `C-Eng1-A-*` and `C-Eng1-B-*` are engineering hypotheses mixed with a necessity-shaped claim record. This can confuse the ledger regardless of which proposal is chosen.
