# Prin-8 — Blind Review A on Proposal B

**Reviewer:** Blind Reviewer A (Claude Opus). **Target:** `proposals/B.md` and `drafts/B/summary.md` only. I did not read `proposals/A.md` or `drafts/A/`.
**Inputs read:** run-root `brief.md` (rubric) and `roster.md`; packet `brief.md`, `roster.md`; `source/packet-brief.md`, `source/C-P1-002-claim.md`, `source/C-P1-010-claim.md`, `source/Prin-4-decision.md`, `source/Prin-7-decision.md`, `source/program-ledger-current.md`, `source/method-Appendix-B.md` (section headings and B.9.6 text).
**Status:** Review only. I edited no claim record, grade, state, decision file, or Eng-2 gate. I ran no measurement, search, solver, or spike. The interval and set-direction checks below are my reading of B's own symbolic worksheet. They are not filed evidence and not a B.9.2 verification. C-P1-002 stays **Grade 2 Candidate**. C-P1-010 Part A stays **Grade 1 Candidate**, and Part B stays **Grade 1 conditional Candidate**.
**Family disclosure:** the reviewer is Opus and B's author is Astra (cross-family). C-P1-002 is Astra-authored (cross-family to me). C-P1-010 is Opus-authored, the same family as me, so I may lean toward protecting its Part A wording. I flag that below where it matters (W5).

---

## 1. Gates (Appendix B / packet brief), checked before scoring

| Gate | Result | Evidence in B |
|---|---|---|
| Templates only; no measurement, spike, or search | **PASS** | "Design only. … No measurements, searches, spikes, theorem verification … are reported." Every target row starts UNSET. |
| Grades stay Candidate; no Locked Grade-1 | **PASS** | The header restates all three grades as Candidate. §4: Grade-1 lock needs "independent verification and human signature". |
| No Eng-2 gate change (D-Prin-3-001) | **PASS** | "These forms add no Eng-2 preconditions and clear none." It says a declared measurement point "supplies context, not automatic authorization". |
| Author ≠ adjudicator (B.9.1) | **PASS** | §4: "This template's author does not adjudicate its own amendments." A non-author bound adjudicator handles any state change. |
| Candidate cannot veto (B.4) | **PASS** | "Candidate claims cannot veto a route. No architecture, controller rate, ladder order, or processor location becomes mandatory." |
| Planning order ≠ necessity (B.8.3, H5) | **PASS** | It cites D-Prin-4-001 priority 5 as "a planning reference only". No ladder edge is asserted. |
| B.9.6 counter not guessed | **PASS** | "Route for B.9.6 assessment; do not reset or guess its cumulative count." |
| Phenomenology ≠ necessity (B.5) | **PASS** | "A successful behavior trace cannot fill an applicability row." Finite success is "registered probes only". |
| No named products/companies | **PASS** | None found. The claim record cites a published theorem by its authors' names; B avoids even that. |

All gates pass. The defects below concern technical correctness and usability.

---

## 2. Strengths

- **S1. Splitting applicability from realization is the right core design.** Both claims fail in the same way: success evidence gets used to fill in premises, or premise evidence gets used to infer realization. B forbids both crossings in its opening paragraph and repeats this in §4 ("a damping estimate does not prove incompatible safe histories"). This directly enforces C-P1-002's "successful behavior alone does not identify a hidden role" and C-P1-010 H3.
- **S2. Four-valued evidence status, kept separate from claim state.** UNSET / SUPPORTED-IN-SCOPE / CONTRADICTED / UNRESOLVED, with "They describe evidence, not claim state." CONTRADICTED stops only the target application and "does not retire the general claim automatically". This matches B.4/B.9 and prevents a template from becoming a back door for state changes.
- **S3. The R3 certificate is quantified correctly.** "The certificate must concern all allowed histories, not sampled controller outputs." Overlapping enclosures give "unresolved, not a demonstrated common safe history." This preserves C-P1-002 premise 3's demand for independent dynamics or reachability evidence.
- **S4. Separation δ handled honestly.** B notes that disjointness does not imply positive distance, requires a *certified* `delta > 0` before any finite-resolution absence test, and refuses to "invent a numerical separation or an earlier response deadline from the symbolic condition." It also keeps "measured total delay" separate from "interval of common corrective history", as Prin-4 required for C-P1-001.
- **S5. Correct direction of the error-budget logic.** If the observed distance plus the budget is below δ, B reads that as a *certificate inconsistency to investigate*, not as proof that the role is absent. This is the right epistemic reading: two safe traces closer than δ contradict the certificate before they contradict the claim.
- **S6. Passive and embedded realizations treated symmetrically.** "No default preference for a new controller"; "Passive realization candidate; not evidence that active feedback is mandatory." This matches C-P1-002's tightened equivalence definition.
- **S7. V0 catches real defects in the C-P1-010 wording.** The Part A statement says "iff `b > KT/2 + |B|`", which is strict, and then calls `K_max = 2(b−|B|)/T` the "largest" renderable stiffness. Under a strict inequality that is a supremum that is never attained. The Part A falsifier uses `K ≥ 2(b−|B|)/T` as a violation, so it puts equality in the non-passive set. B demands that these be reconciled before equality can serve as a verdict. B also separates device-port passivity from stability in one coupled environment, which H2 left only half-closed.
- **S8. The interval worksheet is correct in its stated directions.** I checked each row by hand.
  - `K_L > 2b_U/T_L` is the worst case for the trigger. With nonzero |B| the true ceiling is lower, so "even under the optimistic zero-virtual-damping ceiling" is correct.
  - `K_U ≤ 2b_L/T_U` is the best case for non-trigger. B correctly adds that this "does not certify passivity" when virtual damping is nonzero.
  - The ceiling enclosure `[2(b_L−β_U)/T_U, 2(b_U−β_L)/T_L]` is monotone-correct.
  - The `b − β ≤ 0` split is necessary because the Part A formula then gives no positive stiffness.
  - The rule "a T interval bounds an unknown fixed period; it does not authorize within-run variable sampling" correctly keeps jitter out of a fixed-period theorem.
- **S9. Circularity guard on K_req.** "Copying controller gains into the requirement is circular" (V7). This carries H3 into a mandatory row.
- **S10. Cross-claim coherence outcome.** A passive mechanism can realize C-P1-002 while also placing the target outside C-P1-010's virtual-only premise 8. B calls this "a coherent outcome, not a reason to modify the target after observing results." That is a real interaction, and B pre-empts a post-hoc rescue.

---

## 3. Weaknesses and required amendments

**W1 (major, correctness). "Differentiation resolved" is set too low.** In §2B, a positive lower bound on observed history distance means "differentiation is resolved." But total corrective force includes state-dependent passive terms (premise 4), and the two worlds have different exogenous disturbances. So the states diverge, and the total-force histories will almost always differ by a positive amount, even with no world-dependent active correction at all. Positive differentiation is therefore nearly automatic and says nothing about the role. What matters is whether each trace lies in its own world's safe set S_i(D). Since the sets are separated by δ, that requires distance ≥ δ.
- *Amend:* define "role-relevant differentiation resolved" as (a) the lower bound on distance is ≥ δ (or, under the shared metric, consistent with membership in disjoint S_i), **and** (b) envelope membership is verified in each world. Report positive differentiation below δ as "differentiation present, role relevance unresolved." The first disposition row should cite this stronger condition.

**W2 (major, correctness). The direction of the reachable-set enclosure is unspecified.** "A conservative reachable-set enclosure may support disjointness if the enclosures themselves are disjoint." To certify that S_0(D) and S_1(D) are disjoint, you need **outer** approximations of each safe-history set (supersets) that are disjoint. An inner (under-)approximation of the safe sets proves nothing about disjointness. "Conservative" is ambiguous here, because for safety work it often means *inner* safe sets. A certificate built with the wrong direction would pass this template.
- *Amend:* R3 must state "outer enclosure of each S_i(D) (every admissible safe history lies inside it)." It should also require the certificate to name the enclosure direction for each uncertain parameter.

**W3 (moderate). Model-bounded passive forces can manufacture a counterexample.** The force inventory lets a contribution be "directly measured or bounded by a validated model." Passive restoring and dissipative forces are rarely measured directly. If they are model-inferred, both the "distance < δ" counterexample-candidate row and the "passive realization candidate" row can be artifacts of that model.
- *Amend:* model-bounded terms must enter the error budget E explicitly, with their own validation domain. Any counterexample candidate or passive-realization candidate that depends on a model-bounded term must carry a flag: "model-dependent; direct-measurement replication required before claim routing."

**W4 (moderate, governance). Freezing values before data is implied but not required.** B says "predeclared error budget" and "fields to fill before any future authorized probe." But no field records a seal (hash and timestamp) of the filled metric, δ, D, E, the probe set, and the disposition table *before* any trace exists. Without that, the post-result scope changes B lists as a dominant failure cannot be detected.
- *Amend:* add a "pre-data seal" row to the cover sheet: a hash of the completed applicability rows plus the resolution contract, sealed under the same PLAN mechanism as spikes. Any later edit becomes a revision-history entry routed for B.9.6 assessment.

**W5 (moderate; same-family caution applies). Part B's T is a design variable, not just a measured uncertain quantity.** The worksheet treats `T ∈ [T_L,T_U]` as uncertain. In C-P1-010 Part B, `T_R2` is the *candidate policy-rate period being assessed*. It is a declared architectural hypothesis per case, and only its realized jitter is uncertain. The template also gives no inverse output, even though the decision-relevant quantity is the largest period that clears the trigger: `T* < 2(b_L − β_U)/K_U`, with all the same caveats. Without it, users will run the comparison at 20 ms, fail, and then guess a rate.
- *Amend:* split "declared candidate period" from "realized period bound". Add an optional conservative row for the inverse period `T*`, labeled prospective and not a mandated rate (B.4 and H5 still apply).
- *Bias note:* this amendment makes Part B more usable. As an Opus reviewer of an Opus-authored claim, I may favor that. The packet adjudicator should weigh it accordingly.

**W6 (minor). Adjudicator binding could be pre-filled.** The cover sheet's Review row leaves the "bound claim adjudicator" UNSET. The roster already fixes it: an Opus-family adjudicator for C-P1-002 (Astra-authored) and an Astra-family adjudicator for C-P1-010 (Opus-authored). Pre-filling these removes one avenue of drift. B's §4 sentence about "amendments affecting a claim for which the roster otherwise assigns that author's family" is hard to parse. It should say plainly that B (Astra) must not adjudicate template amendments on C-P1-010 even though the roster assigns Astra to that claim.

**W7 (minor). No link to the C-P1-001 dossier route.** Prin-4 lists "optionally batch C-P1-010 Part A narrow core into same dossier." B's V0 row is exactly the object that such a dossier needs: exact statement, independent check, scope match. B does not say so. *Amend:* add one line saying a completed V0 can be submitted as the Part A component of a B.9.2 seven-row dossier, while staying Candidate until the human signs.

**W8 (minor, usability). Paperwork load.** For each claim and target case, B requires a cover sheet, five or nine premise rows, a certificate attachment, five realization attachments, and a worksheet. B acknowledges the cost and suggests starting with "one declared mode/joint." It gives no fill order, though. *Amend:* state a minimal fill order: cover sheet → V0 (needs no target data) → R1/R3 certificate (needs no instrumentation) → parameter rows → realization rows. That lets premise failures surface before any instrumentation spend.

**W9 (minor). The R3 information structure lacks a causal-observation row.** R3 records "who cannot distinguish them and until when." The incompatibility argument also depends on *what each permitted response source could observe, and by when*, which links R3 to R5. The template should require this per response source: the earliest time at which its observation channel can separate w0 from w1, compared against D. Otherwise the timing role cannot be tied to the inventory of response sources.

---

## 4. Rubric scores (1–5)

| Dimension | Score | Note |
|---|---|---|
| Constraint fit | 5 | All gates pass. It is strictly template-only. |
| Principle integrity | 5 | Evidence status is separate from claim state. Part A and Part B are separate. Theorem direction and strictness are flagged. |
| Falsifiability | 4 | Counterexample-candidate routes are explicit. W1 and W2 weaken the discriminating power of the C-P1-002 absence test as written. |
| Evidence demand | 3 | It is heavy: total generalized-force accounting and certified δ are expensive. This is inherent to C-P1-002, but there is no fill-order economy (W8). |
| Failure modes | 4 | It names four dominant failures with rows for each. It misses the outer/inner enclosure error (W2) and model-dependence (W3). |
| Integrability | 4 | Owners, custody, and reviewer fields exist. Adjudicator binding is not pre-filled (W6). |
| Latency / criticality | 4 | It keeps the deadline D separate from measured delay and refuses to mandate a rate. There is no inverse-period output (W5). |
| Complexity cost | 3 | Two records per claim per case is justified, but it is costly. |
| Reversibility | 5 | These are forms only. Abandoning them costs nothing, and CONTRADICTED does not retire claims. |
| Stackability | 4 | It is reusable across modes and joints and coherent across the two claims. It could feed the C-P1-001-style dossier (W7). |
| **Total** | **41 / 50** | |

---

## 5. Recommendation to the packet adjudicator

**B is suitable as a Recommend base**, subject to the mandatory amendments **W1** (role-relevant differentiation requires δ plus envelope membership) and **W2** (outer enclosures for the disjointness certificate). Both are correctness defects in the C-P1-002 absence logic. Without them, the template could report a role as realized, or certify incompatibility, on invalid grounds.
- W3 and W4 are strongly recommended.
- W5–W9 are optional merges. Apply W5 with the same-family caution noted.
- None of these amendments changes any grade, state, or Eng-2 gate, and none requires execution.

No claim follow-up is decided here. All three claim components remain Candidate at their inherited grades.
