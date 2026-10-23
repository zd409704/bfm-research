# Eng-1 — Adjudication score, pass 1 (P first, Q second)

Adjudicator: Packet Adjudicator (Claude Sonnet). I authored neither proposal. Inputs read: `proposal-P-pass1.md`, `proposal-Q-pass1.md`, `review-of-P-pass1.md`, `review-of-Q-pass1.md`, `gate-C-Eng1-A-01.md`, `brief.md`, `source/Prin-2-decision.md`, `source/method-Appendix-B.md`. Pass 2 was not read. This file changes no claim state.

Proposals are labelled only P and Q. P = XC-0 contact-observability export with a one-sided divergence certificate. Q = richer-plant S0a envelope certificates.

## 1. Gate results (before ranking, B.9.5 / §4 Step 4)

| Gate | P | Q |
|---|---|---|
| Grade-3 claim used as Locked necessity, gate or ordering | PASS. Edges E05/E06, E08/E09, E10/E11, E14 and C-P1-003 are listed as bypassed or unused. Reading P of E17 is not invoked. | PASS. All 17 edges are inventoried as waived or deferred. None is a gate. |
| Locked Grade-1 claimed without human signature | PASS. Nothing is Locked and nothing is recommended-for-lock. | PASS. Same. |
| C-Eng1-A-01 or any Candidate used as a veto gate | PASS, with a note. C-Eng1-A-01 underwrites the interpretation of `d_cert_bits`, but no decision hangs on it. `gate-C-Eng1-A-01.md` says it may guide exploration and may not gate. C-P1-012 is an experimental target, not a gate. The amendment below keeps this true. | PASS. The Candidate is not used. C-P1-012 appears only as a warning. |
| Prin-2: no Eng-1 ladder-edge gates | PASS. D-P1-001 is treated as an acceptance gate that coexists with the packet, not a necessity order. | PASS. Same treatment of D-P1-001. |
| Locked Grade-2 role as Incomplete-gate without an operational test | Not applicable. No Locked Grade-2 role exists. Roles enter only as Candidate design inputs. | Same. |
| Platform framing (generic home humanoid / target plant; no named robot or company) | PASS. | PASS. |
| Readiness (brief: PLAN only means provisional) | Sealed PLAN, no harness run. Decision would be **provisional**. | Sealed PLAN, no harness run. Decision would be **provisional**. |

**Neither proposal is rejected or ruled incomplete. Both are eligible to be ranked.**

Governance notes that gate nothing:
- Q's `C-Eng1-B-*` IDs sit in the `C-` namespace but have no claim records.
- P adds one new necessity-shaped claim, C-Eng1-A-01. Its state is Candidate, Grade 1 narrow, with no lock recommendation.

## 2. Rubric (1–5, higher is better)

| Dimension | P | Q | Objection behind any score ≤3 |
|---|---:|---:|---|
| Constraint fit | 4 | 4 | P: the false-event unit (per 100 ms window vs the registered 0.01/s) breaks the "registered counterexample search" claim. Q: the spike path differs from `spikes/<packet-id>/`. |
| Principle integrity | 4 | 5 | P: the packet leans on one new Candidate lemma for its acceptance semantics. P's §1.3/§1.4 rationale also makes methodological claims the reviewer found unsupported. Q: the ID-namespace issue is hygiene only. |
| Falsifiability | 3 | 2 | P: H2 (all NULL certificates must equal 0) and H3 (ORACLE upper bound ≤ 0.01 at a calibrated 0.99 quantile) can reject a correct harness. Latency and censoring rules are incomplete. Even so, the claim-relevant outcomes (the rate × source contrasts and the substitution test) can come out either way. Q: the fixture sits about 4× (state) and 14× (command) inside its envelope in every cell. The expected outcome is "all 16 cells certified", and saturation-driven violations cannot be witnessed. |
| Evidence demand | 4 | 5 | P: n = 2000 per cell/class and rare-event conservatism may force larger samples. Q is lighter. Both are CPU-only. |
| Failure modes | 3 | 4 | P: multiplicity across 96 cell/class combinations, the calibration boundary and latency censoring are unresolved. Q: the authority-failure row is undercut by the missing saturation witness. |
| Integrability | 4 | 4 | Both give clear generic owners. P's W-register timing and history are open. Q's certificate expiry and handoff are untested. |
| Latency / criticality | 3 | 3 | P: observer bandwidth changes with rate (20 ms vs 80 ms time constants), so the rate effect and the tuning effect are mixed. Q: 0.2 s certificates have no recertification or invariance story. |
| Complexity cost | 3 | 3 | P: duplicated cells and the statistical protocol. Q: exact arithmetic and a mutation suite buy little at 4×–14× margins. |
| Reversibility | 5 | 5 | Both are read-only or synthetic and cheap to abandon. |
| Stackability | 4 | 3 | Q: no next packet is defined after SUPPORTED, and the scope stays at S0a. P: needs a human-ratified (q, r) table before any task-acceptance use. |
| **Total** | **38** | **38** | Unweighted. Tied. |

My scores differ from the reviewers' (P 37, Q 38) on P's Latency, and on P's Principle integrity relative to Q. They are my own reading of the files above.

## 3. Disposition

The rubric is unweighted and the totals tie, so I break the tie on one criterion fixed in advance by the brief. The program is meant to be iteratively falsifiable, so I prefer the packet whose spike can still move a claim or an engineering decision. That is Falsifiability, and it carries the largest information-value gap between the two proposals.

| Proposal | Disposition |
|---|---|
| **P** | **Recommend (provisional).** This is conditional on mandatory amendments 1–6 below, and the PLAN must be resealed as a new version before any run. |
| **Q** | **Alternate.** It becomes Recommend-eligible after amendments Q1–Q3 below. It is not Reject, because every gate passes and it is cheap and reversible. |
| Reject | None at the proposal level. Reject any text that promotes a Grade-3 edge or a Candidate to a gate. |

The tie means the ranking is fragile. If order-swap pass 2 reverses it, that is a confound to disclose, not an adjudication finding.

## 4. Spike decision

- **Run P's spike, but only after the PLAN is amended and resealed (v2).** The v1 PLAN should not run, because H2/H3 could fail a correct harness and the false-event units do not match the registered criteria. PASS validates the harness only. It is never hardware transfer, and it never moves a grade. Runner outputs are data; the claim adjudicator rules on them.
- **Do not run Q's spike now.** Under the frozen fixture the outcome is near-certain and low-information. Run it only after Q1–Q3 are in a resealed PLAN, and only if P's spike fails or the human lead asks for S0a depth. If run unamended, the outcome has to be pre-recorded as "all 16 cells certified; authority stress UNRESOLVED_SATURATION", and treated as low-information.
- If no spike runs before the deadline, the Eng-1 decision stays **provisional** (PLAN only).

## 5. Mandatory amendments

**P (resealed PLAN v2 and proposal text):**
1. Replace the universal-zero NULL rule (H2) with a predeclared statistical coverage check. Keep deterministic invariants, such as the re-run and non-interference checks, as separate harness tests.
2. Calibrate the thresholds conservatively below r, using an order-statistic procedure or a stated tolerance, on data separate from the certification split. Revise H3 to match.
3. Restate FPR in the registered units (0.01/s), or file an explicit registered amendment with a mapping to window decisions and event-merging/reset rules. Do not call the contrasts "the registered counterexample search" until the two agree. Recompute the sample sizes.
4. Give each r-specific detector its own ID and certificate. State whether coverage is pointwise or simultaneous, and predefine multiplicity control for any selected cell or packet-wide claim. State `0 < r < q ≤ 1`, with consistent KL log units.
5. Seal rules for contact timing. Cover pulses that are censored by the window, alarms before onset, missed detections, and the latency policy for misses. State whether the contrast margins are one-sided noninferiority or absolute differences. Predefine the subset used by the substitution test, and state whether the detector is frozen or recalibrated.
6. Handle the confounds in the factorial. Declare the complete input history for `W`, with rates and no future samples. Address observer-bandwidth mismatch across rates by matched tuning on independent data, or narrow the inference to "these two rate-specific implementations". Treat the duplicated CMD_RECON cells as shared baselines, and scope the output-torque-sensor cells separately from current-derived effort.

Also edit the proposal text. Remove or soften the §1.3/§1.4 claims that richer S0a certification would let planning order pose as necessity, and that merging fixtures recreates the confound. State that C-Eng1-A-01 is Candidate and exploratory, and that the certificate is not valid evidence if the lemma fails. Keep the "never certifies absence" rule.

**Q (needed before Recommend):**
- **Q1.** Move or extend the fixture so that cells straddle the certification boundary, and preregister the expected boundary so the prediction can fail.
- **Q2.** Add a saturation-aware witness search, using verified clipped replays only.
- **Q3.** Add a terminal-set/handoff invariance check. Also state the post-SUPPORTED next packet.
- Rename or file records for the `C-Eng1-B-*` hypotheses. Merge B-02/B-03 into the harness PASS criteria. Record the spike location as an amendment. State m[100] and the noise indexing explicitly.

**Both:** keep the bypassed Grade-3 edge lists. No Grade-1 lock without a B.9.2 check and the human signature. Any later gate on a Candidate needs a sealed counterexample PLAN first (Prin-2 amendment 2).

## 6. Confounds (no deanonymizing)

- The totals tie at 38, so the ranking depends on the tie-break. A different tie-break could reverse it. The pass-2 order-swap should be compared against this file.
- Different blind reviewers scored P and Q, and their strictness may differ. Their totals (37 and 38) sit within one point.
- The Q reviewer ran their own float estimates, which were disclosed as non-rigorous. That gave Q's weaknesses a quantified basis and left P's less quantified, so Q's Falsifiability score rests on evidence of a different kind than P's.
- P carries a claim record and a registered-experiment link. Q carries none. This may lift P's apparent engineering relevance for reasons unrelated to quality.
- Both PLANs are unrun and their seal hashes were only partly reviewer-verified. Every score is a pre-result judgment.
- Position (P first) may anchor. Differences in length and detail between the two proposals may anchor too.
- Neither proposal has a human-ratified task requirement. P's (q, r) is a placeholder, and Q's envelope is synthetic.
- I am one adjudicator and have not applied a second cross-family check.
