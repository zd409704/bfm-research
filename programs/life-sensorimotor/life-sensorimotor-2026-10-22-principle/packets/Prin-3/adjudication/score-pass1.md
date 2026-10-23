# Prin-3 — Score file, PASS1 (order P then Q)

Scorer: Packet Adjudicator (Sonnet). I authored neither proposal. I did not deanonymize.
This is a proposal score. It changes no claim state, grade, or ledger entry. D-P1-001 is read as Provisional acceptance-gate. D-Prin-2-001 is read as: no ladder edge gates Eng-1 or Eng-2.

Read: the four PASS1 adjudication files, `source/packet-brief.md`, `source/method-Appendix-B.md`, `source/Eng-1-S2a-XC-VERDICT.json`, and the run `brief.md` rubric.
Numbers I checked against VERDICT: DOWN substitution drops 0.1467 / 0.1253 / 0.0625 with mean 0.1115 (met = false); UP mean drop 0.565 (met = true); A02 false; H1–H4 true; Factor E/R counterexample flags false at both placements.
Not checked: METRICS.md, the PLAN, `sensitivity_fixedgain.json`, the claim records. Statements that depend on them are marked unverified.

## 1. Gate results (Appendix B, before ranking)

| Gate | P | Q |
|---|---|---|
| Hard Reject: Locked Grade-1 without human signature | Pass. No lock or signature is asserted or recommended. | Pass. Same. |
| Hard Reject: Grade-3 used as necessity | Pass. It cites D-P1-001 and D-Prin-2-001 as non-necessity. It lists bypassed edges as a requirement for B. | Pass. It cites the same decisions and requires a bypassed-edge list with grades. |
| Incomplete: Eng-2 recommendation needs a missing Locked Grade-2 role as veto, with no operational test | Pass. No Locked claims exist, and the recommendation depends on no Locked role. | Pass. Same. Q also names the substitution test as the realization test. |
| Candidate claim used as veto (B.4) | **Flag, not Reject.** G-4 and G-5 declare an S2a engineering retry INELIGIBLE. G-4 rests partly on C-P1-012 H5 and the C-Eng1-A-01 non-claims. Both are Candidate claims. Both rival reviews say the same: a Candidate claim cannot veto, and a stricter scheduling preference must be labeled a planning choice. The ratification requirement is asymmetric: it applies to the A retry, while B may run on declared placeholders. | Pass. All four Candidate claims are explicitly kept non-veto. |
| Spike result used as necessity, transfer, or grade change (B.8.4, B.9.8) | Pass. | Pass. |
| Filed routing rule D-Eng-1-001 (Alternate B only if A fails) | Consistent. It follows the rule. | **Process flag, not an Appendix B gate.** Q ranks amended-A first after the FAIL without labeling this as an override of the pre-committed Alternate rule. |

**P: ELIGIBLE** (flag G-C: Candidate-as-veto framing).
**Q: ELIGIBLE** (process flag G-R: unlabeled override).
Neither is Hard Rejected or Incomplete. Both go to rubric ranking.

## 2. Rubric scores (1–5)

| Dimension | P | Q | Basis |
|---|---:|---:|---|
| Constraint fit | 4 | 4 | P: respects all hard constraints, but the A-retry exclusion is built on Candidate claims. Q: clean on constraints, but the override of D-Eng-1-001 is unlabeled. |
| Principle integrity | 4 | 4 | P: strong necessity/sufficiency separation, and UP is kept out of scope as a positive control. Overreach: "the test has power" and "measurement point is the operative variable" are stated more broadly than VERDICT's "this fixture, detector and calibration". The "does not count" labels on A-1 to A-3 are self-assigned B.9.6 treatments. Q: it keeps three negatives separate, preserves the original falsifiers, and gives its own scope changes conservative B.9.6 accounting. Weakness: amendment 1 relativizes the role to an "audited model". That sits in tension with B.3.3, and the audit has no falsifier. |
| Falsifiability | 4 | 3 | P: a concrete sim-only v3 search (identifiable-set rule, bandwidth-decoupled R cell, command-plus-identified-model cell) that can fail in days. `q_id`, the reference cutoff and the latency statistic are still open. Q: the single-packet design cannot discriminate detector from channel when both detectors miss. Its own table ends in "insufficiency of tested implementations", which is today's state. It also depends on a task contract not yet ratified. |
| Evidence demand | 4 | 4 | Both are local sim, with no hardware or paid compute. |
| Failure modes | 4 | 4 | P: thorough over-reading table (unverified against METRICS). It does not check whether a model-compensation match is a premise failure. Q: names the three conflated negatives and the UP-rescue risk. It misses the post-hoc routing-reversal risk. |
| Integrability | 2 | 2 | Neither assigns ownership for body loop, scene publication and decision core. P recommends S0a without the amended interface. Q declines an export schema and leaves the detector's owner and tier unnamed. |
| Latency / criticality | 3 | 3 | P notes p95 = inf and proposes a censored statistic, but leaves the statistic and the miss handling unfixed. Q refuses to treat TPR as a latency certificate, but it does not bind a deadline to a tier or make finite p95 a pass condition. |
| Complexity cost | 3 | 4 | P: four interacting estimand changes plus a new cell. Q: one bounded packet, with one added control (a bandwidth-matched cell). |
| Reversibility | 4 | 5 | P: sim work is cheap to drop, but the categorical A-retry exclusion narrows options. Q: one packet, a "neither" exit, no schema lock-in. |
| Stackability | 3 | 3 | P: B is unspecified. Q: the trigger for B has no owner, so B may never run. |
| **Total** | **35** | **36** | The totals are within scorer noise. I do not treat the 1-point gap as decisive. |

## 3. Stance

**Principle stance (C-P1-012):** both proposals keep the claim at Grade-2 Candidate with no veto, and both read the FAIL as sufficiency-only. They differ in the amendments.
- P's falsifier repairs (A-1 to A-3) and its command-plus-model cell are the more concrete Principle-track content. The cell is the most dangerous untried counterexample to Factor E.
- Q's discipline on counting is the safer rule: preserve the original flags, and count any change that excludes a previously admissible counterexample as a B.9.6 event.
- P's A-4 (spatial "downstream of the dominant nuisance" restatement) is a substantive change, not a clarification. Its physical equivalence is argued but not shown.
- Q's amendment 1 ("only within the audited model") is not adoptable without a falsifier for the audit.

**Eng-2 gate (gates before ranking):** neither engineering packet is executable as written.
- B requires its own amendments first, per the Eng-1 decision.
- Amended-A requires a task and channel contract, a ratified `(q, r)` or an explicitly exploratory status, and a comparison that can discriminate detector from channel.
- Both routes need prerequisites. P's asymmetric eligibility between them is not supported by Appendix B.

| | Stance | Reason |
|---|---|---|
| **Q** | **Recommend** for the Eng-2 gate structure | Symmetric eligibility gates. It keeps Candidate claims non-veto. It has an explicit "neither" exit. Recommend only with mandatory amendments Q-1 to Q-4 below. |
| **P** | **Alternate** | Adopt P's Principle-track search (§12.2) content, and P's B-first direction as a candidate. This is conditional on removing the Candidate-as-veto framing and specifying B's amendments. |
| Reject (both) | | Threshold-loosening or class-selecting A retries; importing UP placement as in-scope support; reading the FAIL as a downgrade, as hardware transfer failure, or as evidence that S0a must come first. |

Margin: narrow. A reasonable adjudicator could prefer P's concreteness on the Principle track. The Q-for-Eng-2 and P-for-Principle-search split is deliberate, and I do not claim the choice is robust.

## 4. Mandatory amendments

**Q (before its Eng-2 ranking is accepted)**
- Q-1: Label the A-first ranking as a proposed override of D-Eng-1-001's Alternate rule. Route it to the human lead's open question. State what delaying B costs.
- Q-2: Add a channel-level upper reference that can fail informatively, for example a nuisance-aware likelihood-ratio detector on the permitted DOWN channel. Predeclare both readings (miss: channel insufficient on this fixture; pass: detector deficient). Without this, the packet cannot discriminate in its failure direction.
- Q-3: Either make a ratified `(q, r)` a hard gate for amended-A, or demote the "limited engineering acceptance" row to exploratory only.
- Q-4: Attach a falsifier to the "audited model" clause. Pre-count any re-audit as a B.9.6 event. Name an owner, criterion and time bound for the branch-B trigger.

**P (before any of its content is adopted)**
- P-1: Remove or relabel the G-4/G-5 INELIGIBLE verdict as a proposed planning preference, not a Principle veto. Apply the same placeholder and declared-assumption rule to both routes.
- P-2: Carry the VERDICT qualifier "this fixture, detector and calibration" into the thesis and I-2/I-3. Do not call placement "the operative variable".
- P-3: Specify `q_id`, the reference cutoff, one latency statistic and its tolerance, tuning budgets, and miss handling before any PLAN is sealed. Preserve the original result alongside the revised protocol.
- P-4: Specify B's amended interface and ownership (richer mode set, discriminating failure case, pass/fail rule, output contract). Until then B is a direction, not the "remaining eligible" candidate.
- P-5: Do not self-assign "does not count" for A-1 to A-4. Defer B.9.6 accounting to the adjudicator for each. Correct "retirement needs falsification or count 3": the third event mandates review, not automatic retirement.
- P-6: Add a premise audit for the command-plus-model cell. A match that removes the claim's required unmodeled nuisance is a premise-failure result, not an in-premise refutation.

## 5. Claim IDs needing adjudicator follow-up (listed only; not performed here)

- **C-P1-012**: rule on each amendment separately (P: A-1 to A-5; Q: amendments 1 to 3). That includes whether any is a B.9.6 event, the audited-model clause, and the model-compensation premise match. Reconcile the narrowing counter. Both proposals say it is unreconciled against the Prin-1 ruling (event #1). Rule on the evidence-status annotation (Q). Register a sealed search PLAN (B.9.8).
- **C-Eng1-A-01**: audit the pooled-window independence and calibration premises (P and the rival reviews agree). No state change requested.
- **C-P1-002 / C-P1-011**: no spike-driven action from either proposal.
- Open for the human lead, not a claim: ratify the `(q, r)` task table and declare the target plant's effort measurement point.

## 6. Confounds (disclosed)

- **Order swap.** This is PASS1 (P then Q). PASS2 files exist and I did not read them. Position effects are not controlled in this score. The P/Q gap is 1 point, so an order effect could flip it.
- **Review provenance.** Each proposal's only review was written by its rival. Both reviews are adversarial by construction. Their rubric scores are not used here, except to find objections I then checked against the proposals and VERDICT. The reviews agree on some issues (for example, reading the FAIL as sufficiency-only). They disagree on others: the review of P scored its Integrability 2 and Principle integrity 3, while the review of Q scored Constraint fit 5 and a total of 37/50. My scores differ from both.
- **Thin verification.** METRICS, the PLAN, the sensitivity file and the claim records were not in my read set. P's floor-cell table, the ORACLE 9/12 count and Q's TPR lower bounds are unverified here beyond what the rival review cross-checked. Neither proposal had `sensitivity_fixedgain.json` or the numeric substitution margin either.
- **Anonymization.** The proposal bodies carry self-labels and roster-style references that could support inference about authorship. I did not use them, and nothing in this file depends on them.
- **Single scorer.** No second adjudicator ran. Researcher agreement is not grade evidence (B.9.7), and this file moves no grade.

DONE
