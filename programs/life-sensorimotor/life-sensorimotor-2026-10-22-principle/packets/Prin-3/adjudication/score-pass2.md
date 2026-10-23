# Prin-3 — Adjudication score, PASS2 (order-swapped)

Adjudicator: Packet Adjudicator (Claude Sonnet). I did not author either proposal. Proposals are referred to only as P and Q. No claim grade or state is changed here. Edits to claims: none.
Inputs: `adjudication/proposal-{P,Q}-PASS2.md`, `adjudication/review-of-{P,Q}-PASS2.md`, `source/packet-brief.md`, `source/method-Appendix-B.md`, `source/Eng-1-S2a-XC-VERDICT.json`, `brief.md` (rubric).
Standing decisions applied: D-P1-001 is a Provisional acceptance-gate, not a necessity order. D-Prin-2-001: no ladder edge is a gate. No named products or companies.

## 1. Gate results (Appendix B, before rubric ranking)

No Locked claims exist: every relevant claim is a Candidate. The Locked-based gates therefore cannot fire for either proposal.

| Gate | P | Q |
|---|---|---|
| Locked Grade-1 asserted without human signature (Hard Reject) | Pass. No lock is asserted, and C-P1-012, C-P1-002, C-P1-011 and C-Eng1-A-01 are kept as Candidates. | Pass. It explicitly asserts no lock or signature. |
| Grade-3 used as necessity (Hard Reject) | Pass. It cites D-Prin-2-001, requires a bypassed-edge list with grades, and does not cite planning order as evidence. | Pass. Its G-1 and G-3 are explicit, and it says S0a is recommended by elimination, not necessity. |
| Eng-2 recommendation needs a missing Locked Grade-2 role as veto without an operational test (Incomplete) | Pass. No Locked Grade-2 role exists. It names a substitution intervention plus an absolute-competence prerequisite as the realization test. | Pass on the literal gate, since no Locked Grade-2 role exists. **Flag:** G-4 and G-5 make a Candidate's premise (C-P1-012 H5) an engineering ineligibility rule, and Candidates may not veto (B.4, B.5). This is not an Incomplete trigger, but it is scored under Constraint fit and Principle integrity. The review of Q also found it asymmetric. |
| Spike result rewriting a claim (B.4, B.8.4, B.9.8) | Pass. | Pass. |
| Out-of-scope items (hardware transfer, re-running S2a-XC, names) | Pass. | Pass. Its proposed counterexample search is a new sealed PLAN, not a re-run. |

**Eligibility: P eligible. Q eligible.** Neither is Hard Reject or Incomplete.

## 2. Rubric scores (1–5)

Scores combine my own read with the two reviews. I spot-verified only the VERDICT-level facts: A02 false, `SUB_DOWN_NOT_MET`, DOWN drops 0.1467/0.1253/0.0625, UP substitution met, and the Factor E/R flags false. I did not independently re-derive Q's per-class METRICS table (the Factor E cells). The review of P checked P's numbers, and the review of Q did not check Q's table.

| Dimension | P | Q | Basis |
|---|---:|---:|---|
| Constraint fit | 5 | 3 | P honours all constraints and non-goals. Q turns Candidate-claim premises into an engineering ineligibility rule (G-4, G-5) while exempting its own preferred route. |
| Principle integrity | 4 | 3 | P keeps three negatives separate and keeps UP outside premise 5. It is docked because its audited-model clause has no falsifier. Q's data reading is strong. It overreaches in three places: "the test has power", A-4's spatial equivalence, and the claim that A-1 to A-3 do not count toward B.9.6. |
| Falsifiability | 3 | 4 | P's discriminator cannot discriminate when it fails (both detectors missing is no new information). Q gives concrete falsifiers for each amendment (A-1 to A-4, including a model-compensation cell). They are incompletely specified (q_id, cutoff, latency statistic, tuning budget). |
| Evidence demand | 4 | 4 | Both are cheap, local and simulation-only. |
| Failure modes | 4 | 4 | Both name the over-reading risks. P misses the unlabeled-reversal risk. Q underchecks premise escape in the model-compensation cell. |
| Integrability | 2 | 2 | Neither assigns ownership across body loop, scene publication and decision core. |
| Latency / criticality | 3 | 3 | Both note p95 = inf. Neither binds a deadline to a tier. Q's censored-latency fix is unspecified. |
| Complexity cost | 4 | 3 | P adds minimal machinery. Q's multiple estimands and tuning regimes need one bounded protocol. |
| Reversibility | 5 | 4 | P is a bounded one-packet design with a "neither" exit. Q's categorical retry exclusion narrows options. |
| Stackability | 3 | 3 | P's trigger for the B branch is unowned. Q's B is recommended without a concrete amended contract. |
| **Total /50** | **37** | **33** | |

The 4-point margin is small relative to the confounds in section 5. I treat it as weak evidence, not a decisive ranking.

## 3. Stance (Principle + Eng-2 gate)

**Principle stance (C-P1-012 and related Candidates): the two proposals are substantively equivalent.** Both keep C-P1-012 as a Grade-2 Candidate and treat the FAIL as sufficiency-level data. Both keep UP out of scope and use B.9.6 counter discipline. Neither proposes any change to C-P1-002, C-P1-011 or C-Eng1-A-01.
- P: **Recommend**, subject to the amendments below.
- Q: **Recommend** on the Principle content (its A-1 to A-3 and A-5 falsifier repairs). Its A-4 and its counter accounting go to the claim adjudicator.

**Eng-2 gate: the proposals conflict.**
- P: **Recommend, conditional.** First a task and channel contract, then one bounded amended-A discriminator. Amended B is the Alternate when an envelope bottleneck is independently identified. "Neither" is the answer if no branch passes the gates.
- Q: **Alternate.** Amended B as the mainline, with the A content moved to a Principle-track counterexample search. This tracks the filed D-Eng-1-001 routing. It is held back by the asymmetric G-4/G-5 gate and by recommending B before its own amendments are concrete.

**Adjudicator's disposition for this pass.** P ranks first on the rubric by a thin margin. Both proposals agree that **no Eng-2 execution should start until the human lead ratifies `(q, r)` and declares the effort measurement point.** That common gate should be adopted as the Eng-2 gate. Which branch runs afterwards is a human-lead decision, because it departs from the D-Eng-1-001 Alternate rule (see O1 below). **Neither proposal is rejected.**

## 4. Mandatory amendments and claim follow-ups

**Mandatory amendments for P:**
- **M-P1 (review of P, O1).** Label the amended-A-first ranking as a proposed override of D-Eng-1-001's Alternate rule. Route it to the human lead's open question, and state what the Alternate (B) loses by delay.
- **M-P2 (O2).** Add a channel-level upper reference that can fail informatively, so the packet can separate detector from channel. Predeclare both readings.
- **M-P3 (O4).** Make a ratified `(q, r)` a hard gate for amended A. Otherwise mark amended A explicitly exploratory, and remove the "limited engineering acceptance" outcome row.
- **M-P4 (O3).** Attach a falsifier to the "audited model" clause, and count any re-audit as a B.9.6 event.
- **M-P5 (O5, O6).** Name the owner and tier of the detector. Name who runs the independent task review that triggers B, with a time bound.

**Mandatory amendments for Q:**
- **M-Q1.** Apply one eligibility rule to both routes. Fixture work may proceed on declared placeholders. Task-acceptance and transfer claims require ratification. Any stricter ordering is a planning preference, not a Principle veto.
- **M-Q2.** Specify the concrete amended contract for B (modes, pass/fail rule, observable output, ownership) before B is called the executable mainline.
- **M-Q3.** Carry the "this fixture, detector and calibration" qualifiers into the thesis, I-2 and I-3. State that UP meeting the substitution test is a positive control for the test, not a calibrated power claim.
- **M-Q4.** Supply the premise and scope redline for A-4. Leave its B.9.6 treatment to the adjudicator, and drop the claim that A-1 to A-3 do not count. Correct the statement that retirement "needs" falsification or count 3.
- **M-Q5.** Specify `q_id`, the reference cutoff, the single latency statistic and the tuning budget. Add a premise audit for the model-compensation cell.

**Claim IDs needing adjudicator follow-up (list only; not performed here):**
- **C-P1-012:** Rule on each proposed amendment separately: P's amendments 1 to 3 and Q's A-1 to A-5. Decide event accounting under B.9.6. The log (`upgrade-log.md`) shows 0 accepted narrowings while the Prin-1 ruling records event #1; the maintainer should reconcile the two. Consider the model-compensation cell and the audited-model clause.
- **C-Eng1-A-01:** Audit the independence and calibration premises behind the pooled-window certificates (the pooled-seed i.i.d. premise). A failed premise limits applicability and does not refute the lemma. No state change.
- **C-P1-011, C-P1-002:** No action from this pass.

## 5. Confounds

- **Order-swap.** This is PASS2: the files were presented in swapped order relative to PASS1. I did not read the PASS1 score in this pass, so I cannot report the net effect of the swap. Position or primacy effects on the 4-point margin are possible.
- **Review provenance.** Each review comes from the rival's family (blind). Each reviewer saw only one proposal and scored it alone, so the two scores are not calibrated against each other. Q's per-class table was not independently checked by its reviewer or by me.
- **Length and structure.** Q is longer and more table-heavy. This may inflate Falsifiability and Failure modes for Q and has not been controlled.
- **Shared-family risk.** I am a model from the same family as one of the rubric-scoring reviewer pairs. I do not know which proposal's author shares my family (the labels are anonymized), so I cannot rule out a family-affinity effect.
- **Missing artifacts.** `sensitivity_fixedgain.json`, the numeric B.9.3 margin and the PLAN v2 text were not available to either author or to me. Factor R conclusions are withheld by both proposals and by me.
- **Single adjudicator.** One adjudicator, one pass. This is not a dual cross-family adjudication, and the margin should not be read as stronger than that.
