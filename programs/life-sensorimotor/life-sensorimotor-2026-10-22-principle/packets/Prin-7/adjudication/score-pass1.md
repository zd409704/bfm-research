# Prin-7 — PASS1 adjudication score

**Adjudicator:** Packet Adjudicator, PASS1 (Claude Opus). I authored neither proposal and neither review.
**Pass mapping:** P = `proposals/A.md` (Opus; `K` schema, admissibility gate AD-1..AD-9, two-sided T-E plus secondary T-R, refuter battery RF-1..RF-8, routing O-1..O-7). Q = `proposals/B.md` (Astra; exact two-joint bounded-disturbance fixture, event/no-event collision certificates, exact dual separation refuter). Review of P = `reviews/B-on-A.md`. Review of Q = `reviews/A-on-B.md`.
**Inputs read:** packet `brief.md`, `roster.md`, every file in `source/` (packet brief, Appendix B, C-P1-012 claim, Prin-6 claim ruling, Prin-4 and Prin-6 decisions, current ledger), both proposals, both draft summaries, both reviews, the run-level rubric, and the Prin-6 score-pass1 for format parity.
**Effect:** planning only. **C-P1-012 stays Grade 2, Candidate.** The accepted B.9.6 narrowing count stays **1**. This adjudication makes no Locked Grade-1 and no grade or state change. It does not touch the Eng-2 gate (D-Prin-3-001) or D-Eng-2-001. It runs no search, proof attempt, solver, simulation or spike, and it registers and seals no PLAN. It edits no claim file. Nothing below is a necessity order (B.8.3), and nothing mandates an export field, sensor, numeric rate or research order.

---

## 1. Gates (B.9.5, before ranking)

| Gate | P | Q |
|---|---|---|
| No grade/state change; no Locked Grade-1 | Pass. §7 "never available" list and §11 non-claims. | Pass. Header and §6. A lock requires an accepted B.9.2 check plus the human signature. |
| PLAN before search; no execution (B.9.8) | Pass. Nothing was executed. §5 defers the seal to a future packet. | Pass. "PLAN only". §4 requires separate execution authorization and sealing. |
| Claim adjudicator ≠ author (B.9.1) | Pass in intent. Bindings are incomplete (D7 below), but that is an amendment issue, not a gate failure. | Pass. "The primary author cannot adjudicate this B-authored extension." |
| Sufficiency ≠ necessity (B.3.5, B.5) | Pass. No spike or score is offered as Grade-1 evidence. T-E.ii is required to be constructive, not a spike. | Pass. The refuter detector is "an existence result". A collision "does not single out measured effort". |
| Grade-3 / planning order as necessity (B.8) | Pass. No ladder argument. AD-8 forbids rate/order mandates. | Pass. |
| Formal-evidence routing (Prin-6 corrected A P-1 row) | Pass. O-1 → B.9.2 check route → separate grade packet → signature. | Pass. The §6 table matches. |
| Inherited falsifier preserved (Prin-6 P-1(i), P-4, P-5, P-7, R-3) | **Pass, conditional.** §10 keeps the factorial and P-1(i). But as written, O-6 ("Unresolved → AN only") and O-5 (variant void) lack the P-5/P-7 override for a concrete in-premise witness (B-on-A D6). Amendment P-d clears it. | Pass. "A concrete in-premise witness may reach claim review even if this plan's checklist is incomplete." d50_M10 and the filed thresholds are untouched. |
| Eng-2 non-interference | Pass. `Spec` is symbolic or model-level (P-8); no human `(q,r)` is needed. | Pass. The model-level contract is explicitly not target `(q,r)`. |
| No named products/companies | Pass. | Pass. |
| Retire-nominate not requested | Pass. | Pass. |

**Both are eligible for ranking, and neither is a Hard Reject.** P has one conditional gate finding, which P-d must clear before any P routing text is merged.

### Independent checks of the reviews' central objections

These are adjudicator readings of the proposals' own text and declared models. They are **not** filed evidence, not certificates, not a search and not a B.9.2 check.

- **A-on-B D1 (budget allocation contradiction): confirmed.** Q §2 says both "For each channel separately, `|n_i[k]|≤b`" and "Total nuisance bound `b=1`, allocated to one channel as specified below". Nothing below specifies an allocation.
- **A-on-B D2 (analytic collapse): confirmed, with one addition.** Under Q's declarations (inputs piecewise-constant on 5 ms intervals, exact integration, boundary samples, known initial state, known `u`, diagonal `M`), the velocity increments reveal the per-interval total `n+g` on each joint. So a collision exists iff admissible `n0, n1` exist with `n0 − n1 = g`. Under the per-channel reading, that holds iff `a ≤ 2b` for some admitted `a ∈ [1,2]`, i.e. `b ≥ 1/2`. **Addition:** the slew bound `|Δn| ≤ 1` never binds, because the symmetric witness needs jumps of only `a/2 ≤ 1`. The one constraint that could have made the question non-trivial is set slack. That is exactly the escape route P's RF-3 (onset rate vs nuisance rate) is designed to test. So every preregistered verdict is fixed by the parameter choice: a built-in conclusion of the H3 kind.
- **A-on-B D3 (placement definitional): confirmed.** The dynamics see only `n_up + n_down`, so U and D are the same computation on the baseline transcript. Under augmentation, `a_motor` reveals `n` in U and equals `u` in D. Q §5's "testable rather than definitional" is false for this model.
- **A-on-B D4 (theorem not the claim sentence): confirmed.** The claim's target is non-identifiability of `J_cᵀF` "without a measurement of `τ_cmd + τ_act_unmodeled`". Q targets an event-detection obstruction with joint-aligned generalized torques. Q never states its exact theorem sentence or how it relates to the claim's.
- **A-on-B D5 (zero command), D6 (latency at the boundary), D7 (indexing/units): confirmed** from the text. The refuter decides at the 200 ms deadline, i.e. 100 ms latency against "p95 ≤ 100 ms".
- **B-on-A D1 (schema, not a ready PLAN): confirmed.** P §2 says the families are "examples for the future packet to choose among", and §5 says "the future packet fixes the numbers". No variant has generator equations, parameter boxes, a contact onset family or a budget.
- **B-on-A D2 (L0 overreach): confirmed.** The continuous-time factorization through `r` holds for the nonlinear plant with matched initial conditions. The two displayed per-interval moments are exact only for the double-integrator simplification.
- **B-on-A D3 (history window): confirmed.** AD-3 matches trajectories "over the decision window". Detectors in AD-5 may use earlier declared history, so a witness must match the entire permitted history.
- **B-on-A D4 (`Conf(U↓)` shortcut): confirmed, moderate.** It is correct only when the `U↑` and `U↓` generators are independent. P's own schema lets families share `θ`, hidden state and command dependence, and the paired worlds must also match the `m` history.
- **B-on-A D5 (necessity vs sufficiency): confirmed.** P's O-2 says "Factor E's Grade-1 form fails for that placement" when T-E.ii fails. The inherited target is a necessity statement, and the measurement failing to suffice does not refute it. The error points *against* the claim (an over-reported adverse result), so it is not a rescue. It is still a principle-integrity error.
- **B-on-A D6, D7: confirmed.** O-6 omits the P-5 override. §9 fixes the refuter to Astra and requires the prover to differ, which forces the prover into the claim author's family. The refuter's family also equals the claim adjudicator's family, and no separate-agent binding is made.
- **Cross-observation (not in either review).** Q's fixture fails P's admissibility gate as written. AD-1 fails because the nuisance is a free bounded sequence with no named mechanism, which Q concedes ("not automatically Coulomb friction…"). AD-3 fails because any in-envelope sequence counts as a witness. AD-6 fails because the fixture classes `{10,20,50,100}` ms are not mapped to the registered classes. In the other direction, P has no concrete instance for its gate to admit. The two proposals are complementary: Q supplies the certificate discipline and a worked instance, and P supplies the test that instance must pass to bear on Factor E.

---

## 2. Rubric (fixed brief, 1–5, higher is better)

I used both reviews as inputs; where my reading differs, the note says why. For parity, I scored identical behaviours identically.

| Dimension | P | Q | Note |
|---|---:|---:|---|
| Constraint fit | 4 | 5 | P: the deliverable is a schema rather than the PLAN the brief asks for. Q: fully inside the remit. |
| Principle integrity | 3 | 3 | P: L0 overreach (D2), the `Conf(U↓)` shortcut and the §8 "iff" (D4), and the O-2 necessity/sufficiency conflation (D5). Its anti-vacuity thesis is strong. Q: a built-in conclusion via an unsourced nuisance envelope, the false "testable rather than definitional", and no theorem sentence or bridge to the claim (D2–D4). Its event-label and quantifier discipline is strong. |
| Falsifiability | 2 | 2 | P: no frozen instance or budget, so nothing can fail yet. Q: it can run within a day, but every preregistered verdict can already be read off `2b ≥ a_min` with the slack slew bound. It is falsifiable in form but predetermined in substance. I score it below A-on-B's 3 because my own re-derivation confirms the collapse. |
| Evidence demand | 3 | 5 | P: five variants including K-nD, envelope sourcing from cited ranges, and multiple prover/refuter rounds. Q: one day plus one review. |
| Failure modes | 4 | 3 | P: RF-1..RF-8 name the real escape routes (cross-joint pattern, state repeat, onset rate, adaptation, placement, vacuity). It misses the history boundary and theorem-failure outcomes. Q: it names hull overlap, solver-status, outcome-selection and constitutive mismatch, but misses its own collapse, the U/D identity and the latency boundary. |
| Integrability | 4 | 4 | Both have clear handoffs (runner files, bound adjudicator, B.9.2 dossier, separate grade packet) and generic channel names. |
| Latency / criticality | 3 | 3 | P attempts the rate floor (T-R), but with undefined latency semantics. Q defers Factor R and puts its refuter latency exactly on the bound. |
| Complexity cost | 3 | 3 | P: two theorem tracks and five variants, beyond what it specifies. Q: exact LP and dual certificates over polytopes with 80+ dimensions, for a question with a closed-form answer. |
| Reversibility | 5 | 5 | Paper artifacts only. |
| Stackability | 4 | 3 | P: the `K` schema and AD gate are reusable scaffolding. Q: the certificate formats extend, but the primary model is too definitional to anchor later work without a counted reformulation. |
| **Total** | **35** | **36** | |

The reviewers' totals were P = 35 (B-on-A) and Q = 38 (A-on-B), so the ordering is the same. **The PASS1 margin is 1 point, which is inside adjudicator and reviewer noise.** Only the within-pass ordering is used (§6).

---

## 3. Decision (PASS1)

| Role | Proposal | Reason |
|---|---|---|
| **Recommend** | **Q** (narrow; provisional on PASS2) | It is a concrete, governance-clean PLAN that closely follows the Prin-6 corrected rows. Strengths: event labels instead of force identifiability; an all-detector quantifier that covers randomized detectors; certificate-only verdicts (exact rational witness, or exact dual plus a strict-gap separating functional); union not hull; per-cell verdicts; and a primary cell fixed before results. Its primary model is near-definitional and must be amended (Q-2, Q-3) before sealing. |
| **Alternate (mandatory merge source)** | **P** | It supplies what Q lacks to make the attempt bear on Factor E: physically sourced admissibility (AD-1..AD-9), realizable hidden-state witnesses, mandatory downstream placement with distinct laws, full registered-class coverage, and a refuter battery aimed at the structural escape routes (RF-1..RF-8). |
| **Merge** | **Required.** Q's protocol and certificate rules form the base. Q's current fixture is kept only as a disclosed closed-form sanity cell. At least one structured variant pair built under P's repaired gate is added. See merge notes and §4. | |
| **Reject** | (i) Treating Q's free-disturbance cell, or its U/D augmentation, as Factor-E evidence, or as progress on the claim's Grade-1 sentence without a stated bridge. (ii) P's O-2 wording "Factor E's Grade-1 form fails" when only the possibility half fails. (iii) P §8's "iff `Conf` shrinks" as a realization criterion, and any import of it into the Grade-2 role text (P already declines this; keep it declined). (iv) P's O-6 "AN only" without the P-5/P-7 override. (v) A refuter whose family equals the claim adjudicator's, with no separate-agent or alternate binding. (vi) Revising `b`, durations, slew or placement after any result, or substituting a convex hull for the union. (vii) Any use of a formal result to rescore the registered factorial, Eng-1 or the substitution result. | |

### Merge notes (P → Q), conditional on PASS2 agreeing

1. **Sanity cell K-0.** Keep Q's current model as K-0. Disclose that its verdicts are closed-form: collision iff `a_min ≤ 2b`, the slew bound inactive, U ≡ D on the baseline transcript, and augmentation definitional. Prove it as a short lemma checked by a qualified human under the B.9.2 route. The LP/certificate machinery is not needed for K-0. K-0 carries no Factor-E weight.
2. **Structured variant pair K-S / K-S↓** (Q-3). Build it under P's AD-1..AD-3 and AD-6, with Q's certificate rules. The minimum content:
   - a nuisance law with a named mechanism and a sourced envelope that does not reference `C`, including at least one state- or command-dependent family and one hidden-state family;
   - a nonzero known command or declared excitation;
   - either coupled `M` or a non-joint-aligned contact torque pattern from a declared 2-link geometry;
   - a binding (not slack) nuisance rate bound, declared before results;
   - a downstream companion whose `U↓` has its own law, with the joint admissible world set defined (B-on-A D4).
3. **Refuter lines.** Import RF-1..RF-8 as predeclared attack lines on K-S/K-S↓ alongside Q's four refuter types. RF-3 is mandatory, because the slack slew bound is the K-0 collapse.
4. **Admissibility record.** Import AD-7 (list added regularity premises) and AD-9 (hash and freeze), with the repairs in P-e and P-g.
5. **Factor R / T-R.** It stays out of scope, as Q §5 already says. P's T-R may be registered only as an optional later target with its own observation maps (P-a). No rate is set.

Do **not** import P's K-nD as a required variant, its §8 "iff", O-2 wording or O-6 default, or its §9 bindings as written.

---

## 4. Mandatory amendments

### To Q (base)

1. **Q-1: Allocation (A-on-B D1).** State one reading before sealing. Recommended: a per-channel bound `b` on both joints. If a single-channel allocation is kept, name the channel and give the reason, and disclose that the nuisance-free joint's cells separate trivially.
2. **Q-2: Disclose the collapse (A-on-B D2; adjudicator addition).** State in the PLAN that, under the declared model, the transcript reveals per-interval `n+g` per joint, so that collision iff `a_min ≤ 2b`. State that the slew bound does not bind and that all K-0 verdicts are fixed by the parameters. Reclassify K-0 per merge note 1. Do not call K-0 a search.
3. **Q-3: Structured variant pair (A-on-B D2(ii), D5; P merge).** Add K-S/K-S↓ per merge note 2. Freeze before any work. The same rules apply: exact witness or dual certificate, union not hull, per-cell verdicts, and no post-result revision.
4. **Q-4: Theorem sentence and bridge (A-on-B D4).** Write the exact target sentence for K-0 and for K-S. Classify each against C-P1-012's Grade-1 sentence as the same statement, a narrower instance, or a different statement. Flag the difference between event detection and `J_cᵀF` identifiability. No dossier may present a certificate as Grade-1 progress until the bound claim adjudicator has ruled on this classification (follow-up 1).
5. **Q-5: Placement (A-on-B D3).** State that U and D are identical under the baseline transcript in K-0, and strike "testable rather than definitional" for K-0. A placement test counts only in K-S/K-S↓, where upstream and downstream effects have distinct laws. The paired worlds must match the complete permitted history, including the added measurement.
6. **Q-6: Indexing, units, latency (A-on-B D6, D7).** A cell is `(d, s, j)`. The slew unit is per 5 ms step, and the PLAN must state that this ties the class to the grid. The refuter detector decides at the first post-onset sample at which a certified test fires, or at a deadline strictly inside `L_p`. Restate early-alarm accounting.
7. **Q-7: Worst-case vs sampled contract (A-on-B D8).** Add the mathematical reason the obstruction cannot pre-empt a factorial witness: the factorial samples nuisance from a distribution, and a worst-case adversarial alignment is not a sampled-world statement. Q §6's procedural protection stays.
8. **Q-8: Class coverage (P AD-6).** Fixture classes are fixture-only. Any statement offered as bearing on the claim must either map to every registered class with `d ≥ 10 ms` or be reported as subclass/neighbouring, routed per Prin-6 P-2/P-9. There is no silent narrowing.
9. **Q-9: Bindings (B.9.1; Prin-6 precedent).** Name the certificate builder, the independent checker, the refuter and the claim-adjudicator agent, and disclose each family's relation to the claim author (Opus), to Q's author (Astra) and to merged P text (Opus). Q is Astra-authored and the usual C-P1-012 adjudicator is Astra, so bind an alternate before any ruling on Q-derived text. Disclose that an Opus alternate is same-family to the claim author, and that a cross-family re-ruling is still required before any lock path.

### To P (only for text merged from it)

- **P-a (B-on-A D2):** Split L0 into three statements: (i) exact continuous-time indistinguishability, with matched initial conditions and well-posedness; (ii) the exact sampled map for the restricted linear/double-integrator case; (iii) any local approximate statement, with error bounds. T-R, if ever registered, must use the correct map.
- **P-b (B-on-A D3, D4):** Define confusion over pairs of complete admissible worlds, with equal observation laws over the **entire** permitted history (or a declared common initialization and history boundary), under each signal set. Link it to `Spec` by a declared trial/window, event-counting rule, miss handling and conversion from α per second to per-trial probability, separately for each quantifier mode. Replace §8's "iff shrinkage" with a task-qualified separation criterion.
- **P-c (B-on-A D5):** Reword AD-4 and O-2. The possibility half is a stronger, separate research target. Its failure is a failure of that target and an AN/CR input. It is not a refutation of the inherited necessity statement. A sufficient witness measurement does not make that physical implementation uniquely necessary.
- **P-d (B-on-A D6; gate condition):** Add theorem/derivation-failure outcomes, and distinguish an invalid proof from a false theorem. Make O-5 and O-6 subject to the Prin-6 P-5/P-7 override: a concrete in-premise witness or premise-failure evidence still goes to CR, and voiding a variant never erases an independently admissible witness against the original claim. The claim text and the adjudicator's rulings control over the table.
- **P-e (B-on-A D7):** Bind separate agents for prover, refuter, checker and claim adjudicator. If the refuter shares the claim adjudicator's family, bind an alternate adjudicator for refuter-authored results. Re-seal after any AD-7-driven edit and before any proof or refuter work.
- **P-f:** K-nD is optional only. Low-dimensional results are reported as subclass results (O-3).
- **P-g:** Under AD-7, an added assumption in an exploratory theorem is not automatically a B.9.6 event. The adjudicator rules whether it changes claim scope or adds a survival premise (see follow-up 2).

---

## 5. Claim follow-ups (for the bound C-P1-012 claim adjudicator; none decided here)

1. **Target classification.** Rule how a proved restricted-model statement relates to the Grade-1 target sentence: same, narrower instance, different, or AM. This covers both a K-0/K-S event-detection obstruction and a P-type theorem with added regularity premises. Rule before any B.9.2 dossier relies on it.
2. **When exploratory premises count.** Rule whether regularity premises added to a formal attempt count under B.9.6 at the pre-ruling stage (P's default) or only when they are substituted into claim text (Q's position). The counter is at 1. Two counted events would trigger mandatory retirement review, so this needs a ruling before any execution packet.
3. **Identifiability vs detection wording.** The Grade-1 sentence is about `J_cᵀF` identifiability. Premise 3 defines detection by TPR, false-event rate and latency. Rule whether aligning the target sentence to event detection is a 0-count clarification (with a written reason) or an AM.
4. **Two-sidedness.** Rule whether a possibility half is part of the Grade-1 upgrade target or a separate research target. Whichever way it goes, the Grade-2 role text is unaffected unless an AM is accepted.
5. **Premise-2 match.** Q's free bounded disturbance does not match premise 2's mechanism list. If any K-0 result is cited, a premise-match check is needed, and the default is "not premise-matched".
6. **Vacuity input (Prin-6 P-1(iv)).** P's two-sided criterion, repaired per P-b, is offered only as an input to the B.9.2 Grade-2 argument. Importing it into the role text would be an AM, counted per Prin-6 follow-up 2.
7. **Role binding.** Apply the Prin-6 affinity rule to Q-derived text (Q author = Astra = usual adjudicator family). Also check refuter/adjudicator family overlap for any execution packet. A cross-family re-ruling is still needed before any lock path.
8. **Record housekeeping.** The Prin-6 upgrade-log append is staged in `upgrade-log-append.md` and is not applied (the log is read-only). Someone with write authority needs to apply it. Prin-7 adds only an optional annotation, "identifiability PLAN adjudicated; no evidence filed", with count 0.
9. **Counter.** Accepted narrowings stay at **1**. Nothing in Prin-7 is an accepted event, and no proposal item is accepted into claim text here.

---

## 6. Confounds

- **Adjudicator family.** This PASS1 adjudicator is Opus. That is the same family as Author A (P), Reviewer A (who reviewed Q), the orchestrator, the C-P1-012 claim author and the Prin-6 alternate claim adjudicator. The roster binds the packet adjudicator to a different model within that same family, so this binding deviates from the roster at the model level but not at the family level. It is disclosed here. A family-level preference would favour P, and P ranked one point lower. With a margin this small, bias in the margins or in the merge selections cannot be ruled out.
- **Order swap incomplete.** This is PASS1 only. The Recommend is provisional until PASS2 (P = B, Q = A). If PASS2 flips, the 1-point margin means the packet decision should rest on the merge, with the base text chosen by the decision step and the amendments in §4 applying regardless of which text is the base.
- **Reviewer asymmetry.** Reviewer A did hand derivations against Q's model. Reviewer B did a structural review of P, which had no instance to derive against. The finding of Q's collapse depends partly on Q being concrete enough to analyze. The penalty is partly a cost of concreteness, and I discounted it only by not scoring Q below P on falsifiability.
- **My re-derivation.** §1's check of the collapse is a reading of Q's declared model. It is not a filed certificate, a search or a B.9.2 check, and it carries no claim-state weight.
- **Common source set.** Both authors and both reviewers read the same `source/` set. Agreement among them is not independent confirmation (B.9.7).
- **Length.** P is about 27.5 kB and Q about 15 kB. Length was not scored. P's extra material was credited only under Failure modes and Stackability.
- **Isolation.** Isolation is author-declared. The draft summaries are consistent with their proposals. I did not authenticate the logs.
- **Model abstraction (both).** Diagonal or joint-aligned contact, a passive command, and worst-case quantifiers bias a formal result toward ambiguity relative to the claim's real comparison of commanded plus nominal law against realized effort. A target-relevant result needs the structured variants and a premise match.
- **Inherited evidence confounds (unchanged; neither proposal resolves them, nor should it):**
  - rate vs observer bandwidth (H2; A-3 deferred);
  - friction placement relative to sensing (H3);
  - the Eng-1 weak reference and `placeholder_qr`;
  - a single planar 2-link sim fixture;
  - the factorial falsifier remains unrun.

---

DONE
