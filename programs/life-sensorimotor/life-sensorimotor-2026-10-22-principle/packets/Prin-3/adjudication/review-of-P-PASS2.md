# Prin-3 — Blind review of Proposal B (reviewer: A, Claude Opus)

**Scope of review.** Read only `proposals/B.md`, `source/packet-brief.md`, `source/method-Appendix-B.md`, the run `brief.md` rubric, and (to verify B's numeric and decision citations) the supplied Eng-1 VERDICT/METRICS/decision excerpts, the Prin-1 decision, the claim summaries and the current ledger. Did not read `proposals/A.md` during this review. This review changes no claim grade or state, and does not adjudicate.

## 1. Gates (B.9.5, applied before scoring)

| Gate | Finding | Risk |
|---|---|---|
| Locked Grade-1 conflict (B.5.1) | None. No Locked claims exist. B explicitly refuses to elevate C-P1-012/002/011 or C-Eng1-A-01 to a veto. | **Reject risk: none** |
| Locked Grade-2 role missing (B.5.2) | No Locked Grade-2 roles exist. B still names an operational realization test for the C-P1-012 role (the substitution intervention plus a new absolute-competence prerequisite). | **Incomplete risk: low** |
| Grade-3 used as law / ladder-edge gate | None. B cites D-Prin-2-001, requires a bypassed-edge list with grades, and does not use planning order as evidence (B.8.3). | none |
| Spike result rewriting a claim (B.4, B.8.4, B.9.8) | B keeps C-P1-012 at Grade-2 Candidate. It treats the FAIL as evidence for annotation, not as a downgrade or upgrade. | none |
| B.9.6 counter discipline | B flags its amendment 1 (and possibly 2) as a likely event #2. It forbids bundling. It concedes that the counter history must be reconciled by the maintainer. This is conservative and correct. | none |
| Out-of-scope items (packet brief) | No hardware-transfer claim, no rerun of S2a-XC, no named products, no Grade-1 lock. | none |
| Departure from a filed routing rule | D-Eng-1-001 says Alternate B runs "only if A spike fails". The spike-outcome note routes Eng-2 "toward Alternate B". B ranks amended-A first. That is admissible, because the human lead has an open question on exactly this point ("B vs amended-A retry vs both"). But B never labels it as a departure from a pre-committed rule that needs human-lead confirmation. | **Eligibility: OK; process flag** (see O1) |

**Gate verdict: ELIGIBLE.** No reject trigger. There is no incompleteness trigger in the B.5 sense. Process flag O1 should be resolved in adjudication.

## 2. Principle integrity

Strong overall.
- The table separating supported from unsupported readings is accurate against the source. I checked these numbers: DOWN d10/d20 TPR_L ≈ 0.26/0.72; drops 0.1467/0.1253/0.0625; UP 5/12 pointwise vs 0/12 Bonferroni; p95 = inf for every R1_REAL_DOWN class; Factor-E/R flags false for both placements.
- B keeps the all-detector quantifier for necessity, keeps UP outside premise-5, and states that the C-Eng1-A-01 certificate has no converse. All three positions are correct.
- B states that the factorial test and the substitution test answer different questions and can both fail without contradiction. This is the key interpretive point, and B gets it right.

Weakness: amendment 1 makes the role "candidate obligatory only within the explicitly audited sensor, nuisance and side-information model". That relativizes the necessity claim to a declared channel model. It sits in tension with B.3.3 implementation independence. It also risks a claim that can be re-scoped to whatever model happens to survive. B does count it as a possible B.9.6 event, which mitigates this. But B does not say what would make the audited model itself wrong, i.e., a falsifier for the scoping clause (O3).

## 3. Over-reading of the Eng-1 FAIL

B does **not** over-read the FAIL. If anything it is slightly under-assertive, in two places the data support a stronger, still sufficiency-level, reading:
- **Signal behavior.** R1_REAL_DOWN's TPR profile tracks R1_CMD closely, with a modest uplift (for example d20M10 0.734 vs 0.587, d50M5 0.752 vs 0.627). Its calibration drift (0.328) is close to CMD (0.354), while UP (0.018) and the oracle (0.024) drift far less. That pattern is what you would see if the DOWN signal is dominated by actuator/command-correlated nuisance. It is fixture-level evidence pointing toward a *channel* limitation rather than a *detector* limitation. B treats the two as equally open. It should at least register this prior, because it bears directly on whether amended-A is the right first bet (O2).
- **Effort information over command reconstruction.** The Factor-E non-counterexample partly reflects REAL@R1 beating CMD_RECON@R1 on DOWN. That is weak positive evidence that DOWN effort carries some information beyond command reconstruction. B correctly declines to call it necessity. It could note it as the one result that cuts in the claim's favor, to balance the annotation.

Neither point is an error. Both are calibration notes.

## 4. Eng-2 gate soundness

The five gates (principle/governance, task contract, channel contract, experiment validity, branch-specific eligibility) are sound and come before ranking. Specific concerns:

- **Gate 2 is soft where it matters.** Gate 2 requires a ratified (q,r) "before claiming task acceptance". But it allows "an explicitly labeled exploratory packet" on placeholders. The recommended amended-A packet could therefore run on placeholder targets again. Its best outcome would then be uninterpretable as task sufficiency, which is the same defect that limited Eng-1. B should state which it is: either ratified (q,r) is a hard eligibility gate for amended-A, or amended-A is explicitly exploratory and cannot trigger the "limited engineering acceptance" row of its outcome table.
- **Gate 5 (amended-A) requires a comparison that "can discriminate detector inadequacy from observed export inadequacy".** This is the right gate. But B's own design does not pass it (see O2).
- **Branch-B trigger is undefined.** Amended B advances when "task review independently identifies" an envelope bottleneck. The review has no named owner, no criterion and no deadline. In practice B could be deferred indefinitely, and the filed Alternate rule could be neutralized without an explicit decision.
- **Latency is not a gate.** Every in-scope DOWN cell has p95 = inf. B notes this, but finite p95 at the ratified deadline is not an explicit pass condition for the amended-A "meets task" row. It is only "subject to latency and coverage".

## 5. Concrete objections

**O1 — Unlabeled reversal of a pre-committed routing rule.** D-Eng-1-001 pre-registered B as the Alternate if A's spike failed. Re-ranking A first *after* seeing the FAIL is the forking-paths pattern that pre-commitment exists to block. This holds even though B's diagnostic rationale is reasonable. *Fix:* label the recommendation as a proposed override of D-Eng-1-001's Alternate rule, route it to the human lead's open question, and state what B (Alternate) loses by the delay.

**O2 — The "discriminator" does not discriminate in its failure direction.** The design compares the existing observer against **one** predeclared alternative detector on the same information. If both miss, B's own table concludes only "insufficiency of tested implementations; no channel-impossibility claim". That is the same epistemic state as today. So the packet can separate detector from channel only if the alternative succeeds. Given the drift/TPR pattern in §3, the alternative most plausibly fails. *Fix:* add a channel-level upper reference that can fail informatively. Options include a nuisance-model-aware likelihood-ratio or Bayes-optimal detector on the permitted DOWN `(X,W)` under the fixture's known generative model, or a d_cert/upper-bound proxy for DOWN against ORACLE_R1. Then a miss by that reference reads as "channel insufficient at this fixture", and a pass by it reads as "detector deficient". Predeclare both readings.

**O3 — Amendment 1's audited-model clause lacks a falsifier.** If the role is obligatory "only within the explicitly audited sensor, nuisance and side-information model", the record must say what evidence invalidates the audit itself. For example, that would be an unmodeled side channel discovered later, or a target plant whose actuator effects differ. Without that, future counterexamples can be absorbed by re-auditing. *Fix:* attach an audit falsifier, and pre-count any re-audit as a B.9.6 event.

**O4 — Placeholder (q,r) ambiguity in the recommended path.** See §4, Gate 2. Make ratification a hard gate, or demote the amended-A outcome row "limited engineering acceptance" to "exploratory only" under placeholders.

**O5 — Integrability and tiering left implicit.** B declines a compulsory export schema, which is defensible. But it never says which component owns the contact-effort detector or which tier (fast reflex vs policy) the finite-latency deadline binds. That ownership is the body loop vs the decision core in the rubric's generic terms. The rubric asks for this explicitly, and the latency deadline in Gate 2 is meaningless without the tier.

**O6 — Branch-B trigger is unowned.** Name who performs the "independent task review", what finding triggers amended B, and a time bound. Otherwise "neither branch is universally first" degenerates in practice into "A first, B never".

**Minor.** B records honestly that the sensitivity artifact and the exact substitution margin were not supplied. Keep that, and require both in the resealed PLAN (B already requires the margin). The bandwidth-matched control for Factor R is a good, concrete repair of the documented gain·T confound.

## 6. Scores (1–5)

| Dimension | Score | Reason |
|---|---|---|
| Constraint fit | 5 | Obeys all hard constraints and non-goals; no lock, no transfer claim, no rerun, no names. |
| Principle integrity | 4 | Grades preserved, the three negatives kept separate, UP kept out of scope; docked for the audited-model relativization without a falsifier (O3). |
| Falsifiability | 3 | A one-packet test that can run within days, but its failure branch is non-discriminating (O2) and it may run on placeholder targets (O4). |
| Evidence demand | 4 | One resealed sim packet with equal calibration budgets; low compute and no hardware. |
| Failure modes | 4 | Names the over-reading, UP-rescue and automatic-fallback risks and mitigates them; misses the post-hoc routing-reversal risk (O1). |
| Integrability | 2 | No ownership assigned for the detector or export (body loop vs decision core); "no compulsory export schema" leaves the interface open (O5). |
| Latency / criticality | 3 | Correctly refuses to treat TPR as a finite-latency certificate; does not bind the deadline to a tier or make finite p95 a pass gate. |
| Complexity cost | 4 | Minimal extra machinery; the bandwidth-matched control is justified. |
| Reversibility | 5 | Bounded to one packet, a "neither" exit, no schema lock-in. |
| Stackability | 3 | Keeps S0a open in principle, but the unowned B trigger (O6) risks stalling the envelope stage. |

**Total: 37/50.**

## 7. Bottom line for the adjudicator

B is **eligible**, careful and largely correct on Principle discipline and on what the FAIL does and does not imply. Its Eng-2 recommendation (amended-A first) rests on a discriminator that cannot discriminate if it fails. It also reverses the filed Alternate rule without labeling the reversal. Before B's ranking is accepted, require O1 (label and route to the human lead), O2 (a channel-level upper reference that can fail informatively) and O4 (a hard (q,r) gate or explicit exploratory status). O3, O5 and O6 are recommended amendments.
