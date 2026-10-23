# Prin-6 — Blind Review A on Proposal B

**Reviewer:** Blind Reviewer A (Claude Opus). **Target:** `proposals/B.md` and `drafts/B/summary.md` only. I did not read proposal A or `drafts/A/`.
**Inputs read:** packet `brief.md`, `roster.md`, `source/packet-brief.md`, `source/method-Appendix-B.md`, `source/C-P1-012-claim.md`, `source/C-P1-012-prin3-ruling.md`, `source/Prin-4-decision.md`, `source/Prin-5-decision.md`, `source/Eng-1-S2a-XC-VERDICT.json`, `source/program-ledger-current.md`, and the run-level `brief.md` rubric.
**Status:** Review only. I changed no claim record, grade, state, PLAN, Eng-2 gate or decision file. C-P1-012 stays **Grade 2, Candidate**.

---

## 1. Gates (Appendix B, B.9.5), checked before scoring

| Gate | Result | Evidence in B |
|---|---|---|
| No grade/state change by packet; no Locked Grade-1 | **PASS** | Header: "C-P1-012 remains Grade 2, Candidate… changes no claim record". The last row withholds any Grade-1 inference and requires a human signature for any eventual lock. |
| Claim adjudicator ≠ author (B.9.1) | **PASS** | "Amend via B.9.6" is defined as a submission for independent adjudication, "not authorize the author or runner to edit the claim". "Claim-adjudicator review requests a ruling; it does not enact one." |
| Phenomenology ≠ necessity (B.3.5, B.4, B.5) | **PASS** | The sufficiency row ("Any structural necessity conclusion from acceptance alone" unavailable). The substitution row withholds "implementation-independent necessity… lock eligibility". |
| Runner files data only (B.9.8) | **PASS** | "The runner files results under B.9.8; the bound non-author claim adjudicator decides." |
| Scope-narrowing counter (B.9.6) | **PASS** (one gap, D2) | Count stated as 1, with 0 new in Prin-3. Bundling to evade counting is forbidden. Previously rejected repairs (A-1, A-2, A-4a) are listed as not adoptable. |
| Planning order ≠ necessity (B.8.3); Grade-3 quarantine | **PASS** (vacuous) | No biological citation. "No export field, numeric sampling rate or ladder order becomes mandatory." |
| Eng-2 non-interference (D-Prin-3-001, D-Prin-5-001) | **PASS** | "They do not create Eng-2 execution preconditions." D-Prin-3-001 gate is unchanged, and "neither table completion nor an audit outcome clears or adds to it". |
| No spike / no PLAN sealed | **PASS** | Stated in the header and in Packet boundary. |
| No named products/companies | **PASS** | I found none. |
| Fidelity to filed record | **PASS** | Verdict facts match the JSON exactly: `harness_pass=true`, `A02=false`, `placeholder_qr=true`, four FE/FR flags false, DOWN mean 0.1115, min 0.0625 at d50_M10, UP passed, and the PLAN hash. B does not reconstruct the missing substitution cutoff or the A02 thresholds. |

**All gates pass. B is eligible for ranking.**

---

## 2. Strengths

1. **It encodes the Prin-3 rulings faithfully.** Each accepted, rejected and deferred amendment shows up in the right place:
   - A-1 (keep every `d ≥ 10 ms` class) and A-2 (keep p95) are preserved.
   - The A-3 deferral appears as "cannot become a two-design admission condition".
   - The A-4b search cell is scored against DOWN; a UP match is diagnostic only. A premise-eliminating model is "a different scope", not a refutation.
   - A-5 / UP exclusion is kept, with the correct note that a Candidate "has no lock veto to pause".
   - B-1 absolute competence comes before realization credit.
   - B-2 three-valued comparison semantics, and infinity minus infinity is never a finite match.
   - B-3 annotation is preserved.
   I found no place where B reopens a rejected repair.
2. **It catches a composition error.** Commanded-at-R1 falsifying E and realized-at-R2 falsifying R do not show that a commanded-at-R2 system works. B keeps the claim's existing "both falsified → retire-nominate" rule, but it forbids describing two witnesses as one role-free system and it preserves the identity of each witness. This is the most original contribution, and it closes a real misreading the claim text invites.
3. **The four evidence components are separated cleanly:** premise status, absolute competence, factor comparison and intervention. Each has three values: met/failed/unresolved, or match/established-failure/unresolved. This keeps a weak reference from silently turning into "no counterexample". It also keeps a failed substitution from turning into "information absent".
4. **The policy is asymmetric, and B.9.4(a) supports it.** One competent, premise-matched witness earns review even when the reference is weak. Negative searches only "delimit what was tried". This matches the Prin-3 statement that the filed negative flags "do not establish necessity".
5. **The "Applying overlapping rows" rule is useful.** Do not pick the most favorable row. Realization in one detector and non-obligation across detectors can hold at the same time. An acceptance failure in system 1 does not cancel a counterexample from system 2. This guards against the most likely adjudication error.
6. **Each row has an "inference that remains unavailable" column.** That makes over-reading detectable mechanically.
7. **Low cost and reversible.** It is a governance table with no compute, no spike and no new claim.

---

## 3. Defects

**D1 (medium): "role-free" is used but never operationalized.** The direct-counterexample row ("A competent in-premise command-reconstructible or other role-free system exists…") and the B.9.2 dossier row both depend on deciding that a system lacks the role. But the claim's own Grade-2 role statement lists "a fast-tier observer that exports its residual" as a permitted *realization*. So a competent commanded-at-R1 system with an above-policy-rate observer residual is ambiguous. It might be a Factor-E counterexample, a different realization of the role, or both. B says "assuming role absence without auditing its joint inputs" is unavailable, but it gives no criterion the audit should apply.
*Fix:* add a column or note that defines role absence for the direct-counterexample row. One option: no exported field whose information about `τ_cmd + τ_act_unmodeled` exceeds what the upper layer can reconstruct from commands and permitted history. Check it with the C-P1-011/Prin-5 access-boundary register. Until then, classify such witnesses as "unresolved: role-absence not established" rather than routing them as role-free.

**D2 (medium): a single-factor falsification has no B.9.6 route.** The E-only and R-only rows go to "claim-adjudicator review". The likeliest outcome of that review is restating the claim on the surviving factor, which drops a factor to survive a counterexample. Under B.9.6, that is a countable narrowing. It would bring the count to 2, one event short of mandatory retirement review. B's narrowing row covers rescues the *proponent* proposes (class removal, statistic swap, sensing restriction, admissibility premise). It does not say that a factor-drop after an established single-factor counterexample also counts.
*Fix:* add to the E-only and R-only rows: "if the adjudicator restates the claim on the surviving factor, record it as a B.9.6 narrowing event with before/after text".

**D3 (low–medium): no row for a premise-6 / side-channel outcome.** H8 says the "upper layers cannot recover it" motivation depends on C-P1-011. Prin-5 has just produced the access-boundary inventory, with outcomes export-only justified, joint-channel justified, or unresolved. B mentions the audit only in passing ("unresolved access audit cannot be silently recorded as absence"). It does not map a *joint-channel* outcome to an action. Example: the upper layer keeps command history or actuator-side diagnostics. H8 says Factor E's nuisance argument survives that, "but nothing beyond". That premise change is not a factorial result, so B's UP and premise-mismatch rows do not obviously capture it.
*Fix:* add one row. "C-P1-011 audit finds a joint channel carrying effort-relevant information to the upper layer" → claim-adjudicator review under B.9.4(b) of premise 6, plus annotation of which parts of the motivation (H8) lapse. Unavailable inference: falsification of Factor E by itself.

**D4 (low): the "common scope" condition on retire-nomination needs one sentence of guard.** The claim says "If both are falsified, retire-nominate", and each falsification is "for that plant model". Requiring a common, premise-matched scope is a defensible reading. But "results from incompatible scopes must be reviewed separately" could become an escape condition that keeps two separate witnesses from ever combining. A-3 warned against that pattern.
*Fix:* say that the common-scope condition is not a new admissibility premise and does not itself count as a B.9.6 event. Also say that separate-scope witnesses still each trigger their single-factor review (and D2 accounting).

**D5 (low): action targets in artifacts are unspecified.** "Annotate" does not say where the note goes: `upgrade-log.md`, `violations.md`, or a ruling file under B.7. The Prin-3 ruling put evidence annotations in the ruling and the upgrade log, and left `violations.md` for admitted counterexamples. One line mapping annotate → upgrade-log, admitted counterexample → violations.md, and amendment → adjudication ruling would make the table directly executable by a runner or clerk.

**D6 (low): no identifiability/proof evidence row.** D-Prin-4-001 priority 4 (optional Grade-1 identifiability attempt) could produce analytic evidence before any spike: a proof under an admissible model class, or an analytic counterexample showing identifiability without the effort measurement. B's table is entirely empirical, apart from the final dossier row, which withholds Grade-1 inference but does not route a proof attempt. The packet brief's four evidence classes do not strictly require such a row, so this is a completeness note rather than a gate issue.

**D7 (cosmetic): statistical decision rules are delegated without a default.** B correctly requires sealed miss handling, confidence family and direction. It gives no default for the case where a future PLAN omits them. Saying "omitted → comparison classified unresolved" would close the gap, and it is consistent with B's own semantics.

None of D1–D7 needs a grade change, a claim edit or a spike to fix. All are wording additions to the table.

---

## 4. Is the evidence-to-action table actionable without changing claim grade?

**Yes, with the D1–D2 additions recommended before adoption.**

- Every action in the table is one of none, annotate, amend via B.9.6 (submission only), or claim-adjudicator review (request only). No row enacts a grade or state change. Even the strongest rows (both factors falsified; full B.9.2 dossier) route to the non-author adjudicator, and the lock row also requires the human signature. The table runs entirely below the grade.
- Rows are keyed to observable outcomes that a sealed PLAN can declare ahead of time: competence met/failed/unresolved, match/failure/unresolved, substitution met/unmet/unresolved. The filed Eng-1 result maps unambiguously to rows 2, 3, 9 and 12, plus the UP row. That matches the existing B-3 annotation, which is a good consistency check.
- **Limits on actionability.** Rows 2–4 and 10–11 need an absolute task contract, and the substitution rows need a margin. B correctly declines to invent either. So those rows can only be applied once a future PLAN (and, for target scope, the human `(q,r)`) supplies them. That is a dependency, not a defect. Without D1, the direct-counterexample row cannot be applied reliably. Without D2, single-factor outcomes are actionable but can leave narrowing accounting off the books.

---

## 5. Rubric scores (run brief; 1–5; gates already passed)

| Dimension | Score | Reason |
|---|---|---|
| Constraint fit | 5 | All hard constraints and packet limits are respected. No spike, lock, Eng-2 change or named entity. |
| Principle integrity | 4 | Necessity and sufficiency are separated throughout, and the Prin-3 rulings are honored. Docked for D1 (role absence undefined) and D2 (missing B.9.6 route for factor-drop). |
| Falsifiability | 4 | Every row is keyed to outcomes of the registered sim factorial or substitution test, which can run and fail within days once a PLAN is sealed. The table itself has no completeness check (D3, D6). |
| Evidence demand | 5 | Zero for this packet. It invents no new experiments. |
| Failure modes | 4 | It names the dominant misreadings: weak-reference suppression, ∞−∞ match, composition error, rescue bundling, UP leakage. Docked for the "common scope" escape (D4). |
| Integrability | 3 | Clear roles between runner, author, adjudicator and human. Little on body-loop vs upper-layer ownership beyond premise status. D3 is the integrability gap with C-P1-011. |
| Latency / criticality | 3 | It correctly declines to mandate a rate or tier, and it keeps fair per-rate tuning and p95. It adds nothing beyond preserving the record. That is appropriate for this packet, but it is neutral. |
| Complexity cost | 4 | 16 rows plus four component definitions. Somewhat dense, but each row has a distinct inference boundary. Rows 2–4 could be merged. |
| Reversibility | 5 | It is a governance note. Abandoning it costs nothing. |
| Stackability | 4 | It lets future factorial, identified-model and dossier work proceed without requiring any of it, and it adds no Eng-2 precondition. |
| **Total** | **41 / 50** | |

---

## 6. Confounds noted

1. **Reviewer family.** I am Claude Opus. That is the same family as Author A, the Orchestrator, and the original C-P1-012 claim author, and close to the Sonnet packet adjudicator. I have not read A, but any shared-family preference for A-style framing cannot be ruled out. My review of B is cross-family.
2. **Author B's family matches the claim adjudicator's.** B is authored by Codex Astra, and C-P1-012's bound claim adjudicator is also Astra. If B's table is adopted, a same-family adjudicator will apply rules drafted by its own family. B's wording also closely tracks the Astra Prin-3 ruling. That is good for fidelity, but it makes "consistent with the ruling" weaker evidence of independent judgment (compare B.9.7).
3. **The underlying evidence is confounded, and B inherits those limits correctly.**
   - Rate and observer bandwidth are still confounded (H2; A-3 deferred).
   - Friction placement relative to sensing (H3) is the variable that separates DOWN from UP.
   - The reference is weak (A02 unmet), so a "match" to it is uninformative.
   - `placeholder_qr=true` means no target task contract exists.
   - The data come from one planar 2-link sim fixture with 3 seeds.
   - Substitution recalibrates the threshold on the substituted channel (`same r_w`), so the drop sizes depend on that policy.
   - The filed substitution cutoff is not in the reviewed sources.
   B does not resolve any of these, and it should not. Adjudicators should not read B's rows as reducing them.
4. **Proposal-length / parity.** B is compact (61 lines). I have not compared it with A, so I make no parity judgment.

---

## 7. Recommendation to the packet adjudicator (on B alone)

B is suitable as the D-Prin-4-001 priority-3 deliverable, **after adding D1 and D2** as table amendments. D3–D7 are optional improvements. No adoption step changes C-P1-012's grade (2), state (Candidate) or narrowing count (1).
