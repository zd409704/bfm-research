# Eng-2 — Adjudication score, PASS2 (order-swapped)

**Adjudicator:** Packet Adjudicator (Claude Sonnet) for Eng-2. I authored neither proposal.
**Read:** `proposal-P-PASS2.md`, `proposal-Q-PASS2.md`, `review-of-P-PASS2.md`, `review-of-Q-PASS2.md`, `source/packet-brief.md`, `source/Prin-3-decision.md`, root `brief.md` rubric. I also checked the `drafts/*/PLAN.md` headers, `claims/C-Eng2-A-01/`, and `spikes/` (empty).
**Inherited decisions applied:** D-P1-001 Provisional (acceptance-gate recommendation, not a necessity order). D-Prin-2-001: no ladder-edge gates. D-Prin-3-001: the common execution gate binds both branches.
**Scope:** I issue no claim-state change, no Grade-1 lock, and no spike authorization.

**Mapping (PASS2: P = B, Q = A).**
- **P:** exact-reference Gaussian surrogate, with an amended-B envelope alternative.
- **Q:** the Eng-1 fixture plus genie ceiling tiers, with an XC-1 contract and an amended-B skeleton.

---

## 1. Appendix B gates (before ranking)

| Gate | P | Q |
|---|---|---|
| Hard Reject: Locked Grade-1 asserted without the human lead | Clear. New hypotheses are "grade N/A". No lock asserted. | Clear. C-Eng2-A-01 is "Candidate; Grade 1 narrow lemma; no gate". No lock, and no recommended-for-lock nomination. |
| Hard Reject: Grade-3 used as necessity | Clear. C-P1-003 is quarantined. E05/E06/E08/E09/E14 are recorded as bypassed, not refuted. | Clear. The same edges are bypassed. E17 is explicitly not invoked. |
| Hard Reject: spike executed despite the Prin-3 `(q,r)` / measurement-point gate | Clear. PLAN §1 marks approval, measurement point and branch choice PENDING. No spike directory exists. | Clear. The PLAN header says "DEFERRED-RUNNABLE… sealing does not authorize running". `spikes/` is empty. |
| Incomplete: deferred-spike marking missing while the PLAN claims runnable now | Clear. The header reads "DEFERRED; NOT EXECUTION-AUTHORIZED". | Clear. Stage 2 is marked deferred-runnable. Stage 1, the XC-1 contract, is document-only and may be produced now. |
| D-Eng-1-001 Alternate-B override labeled as a planning choice pending the human lead | Pass. | Pass. Delay cost is stated. |
| Symmetric eligibility, with no Candidate veto | Pass. | Pass. |
| Channel-level upper reference that can fail informatively | **Partial.** The verdicts are largely computable from the chosen σ before any data (review O1). The class-oracle reference makes the "gap" near-guaranteed (O2). | **Present, conditionally.** The NP ceiling is run on the unchanged Eng-1 fixture, so it addresses the actual miss. Specification gaps remain (review items 1–4). |
| Amended-B contract specified | Form passes. The numbers probably certify at every delay (O3), which tilts the branch choice. | Skeleton only, with no numbers. It is symmetric but thin. |
| Claim artifacts complete | Pass. No new claim directory is needed because the claims are N/A. | **Incomplete (non-fatal).** `claims/C-Eng2-A-01/` has `claim.md` only. `upgrade-log.md` and `violations.md` are absent. This is not one of the listed gate failures, so it is a mandatory amendment. |
| Named products or companies | None. | None. |

**Gate result:** neither proposal is Hard Rejected or Incomplete. Both are eligible to rank. Q carries one open artifact deficiency, and P's unmet gate items are scientific rather than procedural.

---

## 2. Rubric (1–5; low scores carry an objection)

| Dimension | P | Q | Objection or note |
|---|---:|---:|---|
| Constraint fit | 4 | 4 | P pre-fills the measurement point as motor-side and placeholder `(q,r)`, which anchors the human lead's declaration (review P3). Q carries Eng-1 `PLACEHOLDER` values and its branch-choice linkage is incomplete. |
| Principle integrity | 4 | 3 | P cites inherited grades by paraphrase, not by ID (P1), and files a unit test as a hypothesis (P2). Q lacks claim companion records. Q's `DET_GAP_OPEN` and `NUISANCE_LIMIT` labels over-read genie outcomes. Q's threshold selection is not assigned to a split. |
| Falsifiability | 2 | 3 | P: the channel verdicts are decided by arithmetic before data. The gap is close to guaranteed by the oracle asymmetry, and the FPR test is underpowered (about 15–74% pass odds depending on calibration, by hand estimate). Q: it can fail (E-INFO), but its routing has uncovered cases and its `t*` choice is ambiguous. |
| Evidence demand | 5 | 4 | P: 15 CPU-minutes, 1 GiB. Q: 30 minutes, 2 GiB. Quadrature cost per nuisance dimension is undemonstrated. |
| Failure modes | 3 | 3 | P misses the oracle asymmetry and the sample-size-driven UNRESOLVED outcomes. Q misses genie-success inference and rare-tail numerical error. |
| Integrability | 4 | 4 | Both have clear owner boundaries. Q's placeholder-rejection mutation test is claimed but not specified. |
| Latency / criticality | 3 | 4 | P's known-onset protocol sidesteps the policy-tier latency question (O5). Q keeps the genie offline and the body loop non-interfering, but deployment latency is unmeasured. |
| Complexity cost | 3 | 3 | P's machinery largely confirms what is known in advance. Q has two genie tiers plus quadrature, which is justified only if the specifications are tightened. |
| Reversibility | 5 | 5 | Both are bounded and deferred, with no claim change. |
| Stackability | 3 | 4 | P cuts its own tie to S2a / Eng-1. Q reuses the Eng-1 fixture and gives a routing table, though some cells have no route. |
| **Total** | **36** | **37** | Gates are passed by both. The totals do not waive any amendment. |

My totals match the two reviewers' totals (P 36 from the Opus reviewer, Q 37 from the Astra reviewer). The per-dimension differences are small.

---

## 3. Ranking

| Role | Proposal | Stance |
|---|---|---|
| **Recommend** | **Q** | Contract-first (XC-1, document-only, can proceed now), then the S2a-CEIL ceiling discriminator as a deferred-runnable PLAN. Execution is held until the human lead records the gate and the branch choice. Recommendation is conditional on the amendments in §4. |
| **Alternate** | **P** | Contract-first, then the surrogate exact-reference discriminator, with the amended-B envelope option. Cheaper, and it has cleaner procedure. It cannot address the actual Eng-1 miss, and it needs the re-scoping in §4 to be more than a harness exercise. |
| **Reject** | — | Neither proposal is rejected as a whole. The following are rejected readings: genie-only success as detector headroom (Q), a surrogate result as an Eng-1 diagnosis (P), and any retry with loosened thresholds. |

**Rationale.** The margin is one point and is inside the confound band (§5), so the ranking leans on substance. P's own text says the surrogate "cannot retrospectively attribute Eng-1 FAIL". The Prin-3 amendment asks for a channel-level reference that can fail informatively. Q puts that reference on the fixture that produced the miss. P puts it on a model whose ceiling and gap are mostly fixed by the chosen parameters. Q's defects are specification and interpretation, which amendments can fix before sealing. P's are structural. Q's recommendation is explicitly conditional.

This is a planning choice only, pending the human lead. It does not choose a branch, authorize execution, or imply S2a-before-S0a necessity.

---

## 4. Mandatory amendments (before any seal or execution)

**Q (Recommend):**
- **Q-1.** Rename `DET_GAP_OPEN`. G-marg success with D1 failure is not exported-channel headroom. Require a witness using only `(X,W)` before any "detector opportunity" routing.
- **Q-2.** `NUISANCE_LIMIT` requires G-full to meet a valid floor and G-marg to fall below a valid ceiling. Otherwise report the marginal ceiling with attribution unresolved.
- **Q-3.** Write out the genie likelihood: null-template generation, joint laws under both hypotheses, nuisance dimensions, the marginalization rule, and why the conditional statistic equals the joint LR. If that is unavailable, the ceiling is UNRESOLVED.
- **Q-4.** Assign `t*` to a calibration split. Check convergence of the actual tail probabilities, threshold and decision at `r`, not only AUC. Specify the D1 selection objective and tie-break.
- **Q-5.** Make the verdict and routing exhaustive: precedence, defaults, and the conflict between "PASS iff all H" and "H5 failure is not a harness failure". Do not give the aggregate E-INFO/routing decision a per-cell 95% guarantee.
- **Q-6.** Separate historical Eng-1 reproduction from the new independent-window estimator, and define a drift test that is not an interval-versus-bound comparison. Freeze a per-cell `(q,r)` table.
- **Q-7.** Specify the placeholder / stale / out-of-scope mutation test for C-Eng2-A-03, or downgrade the claim to a design proposal.
- **Q-8.** Supply `upgrade-log.md` and `violations.md` for C-Eng2-A-01 through the authorized claim workflow. State the quadrature dimension and the timeout outcome.
- **Q-9.** Record the human's branch choice with the ratification, and use the human's explicit exploratory policy rather than a carried `PLACEHOLDER`.

**P (Alternate), if elevated:**
- **P-1.** Add a class-agnostic (mixture or GLRT) reference, or report the oracle gap and the class-agnostic gap separately. Rename "attainable" to "attainable given class oracle".
- **P-2.** Pre-register the analytic 36-cell U table and the predicted statuses. Say that only the comparator side is empirical.
- **P-3.** Raise the null counts or calibrate at about r/3. State the predicted FPR-driven UNRESOLVED rate.
- **P-4.** Rescale the §9 envelope numbers so at least one delay is predicted non-CERTIFIED, or label them illustrative.
- **P-5.** Present the measurement point as one option among several. Cite inherited grades by decision ID. Move C-Eng2-B-01 to the harness gates. State the override cost in program cycles. Register the paired test, or drop it. Do not count non-interference gate 4 as evidence for C-Eng2-B-03.

**Both:** carry the "this fixture, detector set and calibration" qualifier. PASS is harness-only. Neither is a hardware-transfer result. Neither lets Eng-1 FAIL read as a downgrade.

---

## 5. Confounds (order-swap and other)

1. **Pass1 and PASS2 are one adjudicator family.** I am Sonnet. Class-1 order-swap controls position bias only. It does not provide cross-family adjudication.
2. **Blinding leak.** Each proposal names its author family in its own text (P: "Author B (Astra)", Q: "Author A (Claude Opus)"). Anonymization does not hide author identity, and I cannot rule out a family-preference effect in my scores.
3. **Reviewer-family asymmetry.** Opus reviewed P's family and Astra reviewed Q's family. Each reviewer scored its rival's output, and neither had the other proposal. Review severity may differ by family, so the 36/37 totals are not on a shared scale. The one-point gap is within noise.
4. **Review depth differs.** The P review ran hand estimates (κ, FPR power, envelope growth) that I did not independently verify. The Q review checked the claim directory and PLAN seal and found concrete defects. P's score depends on estimates the reviewer flags as unconfirmed.
5. **Length and position.** Q's text is longer (about 15.8 KB vs 12.9 KB), and which was labeled P or Q was swapped relative to Pass1. I have not re-read Pass1 here, so cross-pass consistency is not verified in this file. The final Eng-2 decision must reconcile the two passes. Class-2 dual cross-family adjudication was not applied here.
6. **Unverified assumptions.** I did not run any code. Numerical claims in the PLANs and reviews are unchecked.

---

**Status.** Provisional. Decision is Recommend Q and Alternate P, conditional on §4. Execution of either spike is deferred until the human lead clears the Prin-3 common gate. No claim-state, grade or lock change is made.
