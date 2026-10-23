# Prin-7 — PASS2 adjudication score (order-swapped)

**Adjudicator:** Packet Adjudicator, PASS2 (Claude Opus). I authored neither proposal and neither review.
**Pass mapping (swapped):** P = `proposals/B.md` (Astra; exact two-joint bounded-disturbance fixture, event/no-event collision certificates, exact dual separation refuter). Q = `proposals/A.md` (Opus; `K` schema, admissibility gate AD-1..AD-9, two-sided T-E plus secondary T-R, refuter battery RF-1..RF-8, routing O-1..O-7). Review of P = `reviews/A-on-B.md`. Review of Q = `reviews/B-on-A.md`.
**Inputs read:** packet `brief.md`, `roster.md`, `source/packet-brief.md`, `source/method-Appendix-B.md`, `source/C-P1-012-claim.md`, `source/Prin-6-decision.md`, run-level `brief.md` rubric, both proposals, both reviews. For checking only: `source/C-P1-012-prin6-ruling.md` (P-1, P-5, P-7, P-8, A P-1 rows). `score-pass1.md` was read **only after** §2's independent scores were drafted and frozen (§3 reconciles).
**Effect:** planning only. **C-P1-012 stays Grade 2, Candidate.** Accepted B.9.6 narrowing count stays **1**. No Locked Grade-1, no grade or state change, no Eng-2 gate change (D-Prin-3-001, D-Eng-2-001 untouched). No search, proof attempt, solver, simulation or spike run. No PLAN sealed. No claim file edited. Nothing here is a necessity order (B.8.3) or mandates an export field, sensor, numeric rate or research order.

---

## 1. Gates (B.9.5, before ranking)

| Gate | P (B) | Q (A) |
|---|---|---|
| No grade/state change; no Locked Grade-1 | Pass. Header and §6; lock needs accepted B.9.2 check plus human signature on the exact statement. | Pass. §7 "never available" list; §11. |
| PLAN before search; no execution (B.9.8) | Pass. "PLAN only"; §4 requires separate execution authorization and sealing. | Pass. Seal deferred to a future packet (§5 step 1). |
| Claim adjudicator ≠ author (B.9.1) | Pass. §6 binds an independent reviewer and requires family disclosure. | Pass in intent. Bindings incomplete (refuter and adjudicator both review-side family, prover forced to claim-author family). Amendment, not gate. |
| Sufficiency ≠ necessity (B.3.5, B.5) | Pass. Refuter detector is "an existence result"; a collision "does not single out measured effort". | Pass. T-E.ii must be constructive, not a spike. |
| Grade-3 / planning order as necessity (B.8) | Pass. | Pass. AD-8 forbids rate/order mandates. |
| Formal-evidence routing (Prin-6 corrected A P-1 row) | Pass. §6 table matches. | Pass. O-1 → B.9.2 route → separate grade packet → signature. |
| Inherited falsifier preserved (Prin-6 P-1(i), P-5, P-7, R-3) | Pass. "A concrete in-premise witness may reach claim review even if this plan's checklist is incomplete"; d50_M10 and filed thresholds untouched. | **Pass, conditional.** O-6 "Unresolved → AN only" and O-5 "variant void" omit the P-5/P-7 override (B-on-A D6). Any merged Q routing text must carry amendment Q-d. |
| Eng-2 non-interference | Pass. Model-level contract explicitly not target `(q,r)`. | Pass. `Spec` symbolic/model-level (P-8). |
| No named products/companies | Pass. | Pass. |
| Retire-nominate not requested | Pass. | Pass. |

**Both eligible for ranking. Neither is a Hard Reject.** Q carries one conditional gate finding, cleared by Q-d before any Q routing text is merged.

### Independent checks (adjudicator reading of the proposals' own text; not filed evidence, not a certificate, not a search, not a B.9.2 check)

- **A-on-B D1 (allocation contradiction): confirmed.** P §2 says "For each channel separately, `|n_i[k]|≤b`" and then "Total nuisance bound `b=1`, allocated to one channel as specified below". No allocation follows.
- **A-on-B D2 (analytic collapse): confirmed and generalized.** With piecewise-constant inputs, exact integration, boundary samples of `q̇`, known initial state, known `u ≡ 0` and diagonal `M`, the transcript reveals the per-interval total `n+g` on each joint. A collision needs admissible `n0, n1` with `n0 − n1 = g`. Before onset `n0 = n1 = c`; after onset the difference must step by `a` in one interval. Writing the slew bound per step as `s` (P declares `s = 1`), the condition is
  **collision iff `a_min ≤ 2·min(b, s)`** (witness `c = 0`, `n0 = +a/2`, `n1 = −a/2`).
  Consequences beyond the reviews:
  - `M` cancels; duration `d` (any `d ≥ 5 ms`), sign `s`, and joint `j` (per-channel reading) never enter. All 16 `(d, s, j)` cells in a budget get the **same** verdict. P's "each cell receives its own verdict" and "one cell's collision must not erase another's separation" are vacuous for this fixture: there is no cell diversity to protect.
  - Across 5 budgets × 2 placements × 16 cells (160 feasibility problems), there are exactly two distinct outcomes: collide for `b ∈ {1/2, 1, 2}`, separate for `b ∈ {0, 1/4}`. The primary `b = 1` verdict ("collision") is readable from the declared parameters.
  - The slew bound is the only parameter that could have made `b` non-decisive, and at `s = 1 ≥ a_max/2` it is slack. This is the RF-3 (onset rate) escape route in Q, set slack in P.
- **A-on-B D3 (placement definitional): confirmed.** The dynamics see only `n_up + n_down`, so U ≡ D on the baseline. Under augmentation, `a_motor` reveals `n` in U and equals `u` in D; `a_joint` reveals `n` in both. P §5's "testable rather than definitional" is false for this model.
- **A-on-B D4–D8: confirmed** from text. The refuter detector decides at the 200 ms deadline, latency exactly 100 ms vs "p95 ≤ 100 ms".
- **B-on-A D1 (schema, not a ready PLAN): confirmed.** Q §2 families are "examples for the future packet to choose among"; §5 "the future packet fixes the numbers". No variant has generator equations, parameter boxes, onset family or budget.
- **B-on-A D2 (L0 overreach): confirmed.** Continuous-time factorization through `r` holds for the nonlinear plant with matched initial conditions and well-posedness (ODE uniqueness). The two displayed per-interval moments are exact only for the double integrator.
- **B-on-A D3 (history window), D4 (`Conf(U↓)` Minkowski shortcut), D5 (O-2 necessity/sufficiency), D6 (routing gaps), D7 (bindings/seal order): confirmed.** D5 errs *against* the claim (over-reports an adverse result); still a principle-integrity error.
- **New on Q (not in either review): AD-7 pre-ruling budget risk.** With the counter at 1 and Q's default "count", two pre-proof regularity premises would reach 3 and force mandatory retirement review before any evidence exists. That would let planning choices, not evidence, drive the claim toward retirement review, contrary to the packet brief ("should not"). The Prin-6 ruling's own standard (a premise is a B.9.6 event only if it narrows claim scope or is added to survive a counterexample) argues against pre-counting exploratory-model premises. Ruled by the claim adjudicator (follow-up 2), not here.
- **Cross-check:** P's fixture fails Q's gate as written (AD-1: unnamed free disturbance, which P concedes; AD-3: any in-envelope sequence counts; AD-6: fixture classes not mapped to registered classes). Q has no instance for its gate to admit. Complementary.

---

## 2. Rubric — independent PASS2 scores (drafted before reading PASS1)

| Dimension | P (B) | Q (A) | Objection behind any score ≤ 3 |
|---|---:|---:|---|
| Constraint fit | 5 | 4 | Q: brief asks for a PLAN with an admissible model class; Q delivers an admissibility gate and candidate families, not a class. |
| Principle integrity | 4 | 3 | P: no theorem sentence or bridge to the claim's Grade-1 sentence (D4). Q: L0 overreach; `Conf(U↓)` and §8 "iff"; O-2 treats failure of a sufficiency half as refutation of a necessity statement. |
| Falsifiability | 3 | 2 | P: runs in a day and can fail, but every verdict is fixed by `a_min ≤ 2·min(b,s)`; primary verdict also hinges on the D1 ambiguity. Q: no frozen instance and no numeric budget, so nothing can fail yet. |
| Evidence demand | 5 | 3 | Q: five variants incl. K-nD, envelope sourcing "from cited ranges" (future literature work), multiple prover/refuter rounds. |
| Failure modes | 3 | 4 | P: names hull overlap, solver status, outcome selection, constitutive mismatch; misses its own collapse, U/D identity, cell-verdict identity, latency boundary. Q: RF-1..RF-8 cover the real escape routes; misses history boundary and theorem-failure outcomes. |
| Integrability | 4 | 4 | |
| Latency / criticality | 3 | 3 | P: defers Factor R entirely; refuter latency on the bound. Q: attempts a two-sided T-R but with undefined latency semantics. |
| Complexity cost | 3 | 2 | P: exact LP/dual machinery for a closed-form question. Q: 7 families, 9 AD items, 8 RF lines, 7 outcomes, 2 theorem tracks, 5 variants, all unspecified. |
| Reversibility | 5 | 5 | |
| Stackability | 3 | 4 | P: primary model too definitional to anchor later work without a counted reformulation. |
| **Total /50** | **38** | **34** | |

Reviewer totals (P 38 from A-on-B, Q 35 from B-on-A) came from different reviewers with uncalibrated leniency; they were inputs, not used directly.

---

## 3. Reconciliation with PASS1

PASS1 (P=A, Q=B): A 35, B 36. PASS2 independent: B 38, A 34. **Same ordering in both passes; no position flip.**

| Dimension | Divergence | Resolution |
|---|---|---|
| B Principle integrity | PASS1 3, PASS2 4 | **Adopt 3.** PASS1's point holds: B asserts about its own model that placement is "testable rather than definitional", which is false (§1), and B would deliver a free-disturbance obstruction under the Grade-1 upgrade heading with no bridge. That is necessity-discipline, not only failure-modes. |
| B Falsifiability | PASS1 2, PASS2 3 | **Keep 3.** B has a frozen, runnable instance that could in principle fail; the predetermination is already charged under Principle integrity and Failure modes. Scoring B equal to A, which has no instance at all, would under-reward concreteness (PASS1 itself flagged this as a cost-of-concreteness confound). |
| A Complexity cost | PASS1 3, PASS2 2 | **Keep 2.** A's apparatus is larger than B's and is entirely unspecified; B's excess is a small, cheap machine. |
| B Constraint fit, Evidence demand, Stackability; A Evidence demand, Failure modes, Latency | Agree or within the same reasoning | No change. |

**Reconciled totals: P (B) 37, Q (A) 34.** Margin 3 (PASS1 margin 1). Still small; the ordering rests on concreteness and cheapness (B) against a stronger but unbuilt design (A).

**PASS1 Recommend survives: yes.** Recommend B with mandatory merge from A. PASS1's merge architecture (K-0 sanity cell + structured pair K-S/K-S↓ under A's repaired gate, RF-3 mandatory) survives unchanged. PASS1 Q-1..Q-9 = PASS2 P-1..P-9; PASS1 P-a..P-g = PASS2 Q-a..Q-g; additions are marked **(new)**.

---

## 4. Decision (PASS2)

| Role | Proposal | Reason |
|---|---|---|
| **Recommend** | **P = B** (base text) | Concrete, governance-clean, cheap. Event labels instead of force identifiability; all-detector (incl. randomized) quantifier; certificate-only verdicts; union not hull; preregistered primary cell; correct Prin-6 routing including the P-5/P-7 override. |
| **Alternate (mandatory merge source)** | **Q = A** | Supplies what makes the attempt bear on Factor E: physical sourcing, realizable hidden-state witnesses, distinct downstream laws, full registered-class coverage, refuter lines aimed at structural escape routes. |
| **Merge** | **Required.** As PASS1 §3 merge notes 1–5. | |
| **Reject** | (i) Treating B's free-disturbance K-0 cell, its U/D augmentation, or its per-cell verdict list as Factor-E evidence or Grade-1 progress. (ii) A's O-2 "Factor E's Grade-1 form fails" when only the possibility half fails. (iii) A §8 "iff `Conf` shrinks" as a realization criterion, or importing it into the Grade-2 role text. (iv) A's O-6 "AN only" without the P-5/P-7 override. (v) A refuter sharing the claim adjudicator's family without separate-agent or alternate binding. (vi) Revising `b`, `s`, durations or placement after any result; hull for union. (vii) Using any formal result to rescore the factorial, Eng-1 or the substitution result. (viii) **(new)** Counting exploratory-model regularity premises as B.9.6 events by default before the claim adjudicator rules (follow-up 2). | |

---

## 5. Mandatory amendments

### To P (base, B)

1. **P-1 Allocation.** One reading before sealing; recommended per-channel `b` on both joints. A single-channel reading must name the channel, give the reason, and disclose trivial separation on the other joint.
2. **P-2 Disclose the collapse.** State `collision iff a_min ≤ 2·min(b, s)` for K-0, that the slew bound is slack at `s = 1`, and that K-0 verdicts are parameter-fixed. Reclassify K-0 as a closed-form sanity lemma, checkable by a qualified human under B.9.2. Do not call K-0 a search.
3. **P-3 Structured pair K-S / K-S↓.** Per PASS1 merge note 2: named-mechanism nuisance with a sourced envelope independent of `C` (≥1 state/command-dependent family, ≥1 hidden-state family); nonzero known command or declared excitation; coupled `M` or non-joint-aligned contact pattern from a declared 2-link geometry; a binding nuisance-rate bound declared before results; a downstream companion with its own law and a defined joint admissible world set.
4. **P-4 Theorem sentence and bridge.** Exact target sentence for K-0 and K-S, each classified against C-P1-012's Grade-1 sentence (same / narrower instance / different). Flag event detection vs `J_cᵀF` identifiability. No dossier presents a certificate as Grade-1 progress until the bound adjudicator rules (follow-up 1).
5. **P-5 Placement.** State U ≡ D on the K-0 baseline; strike "testable rather than definitional" for K-0. Placement counts only in K-S/K-S↓, with paired worlds matching the complete permitted history including the added measurement.
6. **P-6 Indexing, units, latency.** Cell = `(d, s, j)`; slew per 5 ms step, tied to the grid; refuter decides at the first post-onset sample where a certified test fires, or at a deadline strictly inside `L_p`; restate early-alarm accounting.
7. **P-7 Worst-case vs sampled contract.** State why the obstruction cannot pre-empt a factorial witness (sampled nuisance vs adversarial alignment).
8. **P-8 Class coverage.** Fixture classes are fixture-only; anything offered as bearing on the claim maps to every registered class with `d ≥ 10 ms` or is reported subclass/neighbouring, routed per Prin-6 P-2/P-9.
9. **P-9 Bindings.** Name certificate builder, independent checker, refuter and claim-adjudicator agent with family relations to claim author (Opus), B author (Astra) and merged A text (Opus). B is Astra and the usual C-P1-012 adjudicator is Astra: bind an alternate before ruling on B-derived text; disclose that an Opus alternate is same-family to the claim author and that a cross-family re-ruling is still needed before any lock path.
10. **P-10 (new) Cell-verdict identity.** Disclose that in K-0 all `(d, s, j)` cells within a budget share one verdict and placement duplicates them, so the 160 problems carry two distinct outcomes. Per-cell verdict and no-erasure rules become operative only in K-S/K-S↓; require K-S to contain at least one parameter (e.g. binding rate bound vs onset profile, or geometry vs nuisance coupling) under which duration or contact location can change the verdict, declared before results.
11. **P-11 (new) Fully specified K-S before seal.** K-S/K-S↓ must be written out with equations, parameter boxes, initial hidden-state sets, numeric envelopes with sources, command, contact classes and budget **before** sealing. If the execution packet cannot specify them, it runs K-0 only as a labeled sanity lemma and the upgrade attempt is filed **unresolved** (Prin-6 P-5). The merge must not reintroduce A's schema-not-PLAN defect.

### To Q (only for text merged from A)

- **Q-a** Split L0: exact continuous-time statement (matched initial conditions, well-posedness); exact sampled map for the restricted linear case; any local approximation with error bounds.
- **Q-b** Define confusion over pairs of complete admissible worlds with equal observation laws over the entire permitted history (or declared common initialization), per signal set; link to `Spec` via trial window, event counting, miss handling and α-per-second → per-trial conversion per quantifier mode; replace §8 "iff shrinkage" with a task-qualified separation criterion.
- **Q-c** Reword AD-4 / O-2: the possibility half is a separate, stronger research target; its failure is an AN/CR input, not refutation of the inherited necessity statement; a sufficient witness measurement is not uniquely necessary.
- **Q-d (gate condition)** Add theorem/derivation-failure outcomes (invalid proof vs false theorem); make O-5/O-6 subject to the Prin-6 P-5/P-7 override; claim text and adjudicator rulings control over the table.
- **Q-e** Separate agents for prover, refuter, checker, claim adjudicator; alternate adjudicator if refuter shares its family; re-seal after any AD-7-driven edit, before proof or refuter work.
- **Q-f** K-nD optional only; low-dimensional results reported as subclass (O-3).
- **Q-g** An added exploratory assumption is not automatically a B.9.6 event; the adjudicator rules.
- **Q-h (new)** Strike A's "this PLAN defaults to counting" (O-3) and the AD-7 pre-proof counting default from merged text pending follow-up 2. Until ruled, added premises are listed and flagged, not counted.

---

## 6. Claim follow-ups (bound C-P1-012 adjudicator; none decided here)

PASS1 §5 items 1–9 carry forward unchanged: target classification; when exploratory premises count; identifiability vs detection wording; two-sidedness; premise-2 match of free disturbance (default "not premise-matched"); vacuity input only; role binding / affinity; record housekeeping (`upgrade-log-append.md` still unapplied); counter stays **1**. Additions:

10. **(new)** On follow-up 2, consider that pre-counting exploratory premises at counter 1 can force retirement review from planning choices alone; rule before any execution packet seals.
11. **(new)** Any K-0 lemma, if filed, is an AN on a free-disturbance model only, with the closed form recorded, so that it is not later cited as Factor-E or Grade-1 evidence.
12. Suggested ledger append (append-only, orchestrator): D-Prin-7-001 — Recommend B (base) with mandatory merge from A; Recommend survives order swap; no claim-grade or state change; no B.9.6 event.

---

## 7. Confounds and limits

- **Adjudicator family.** PASS2 adjudicator is Opus: same family as Author A (Q), Reviewer A (who reviewed P), the PASS1 adjudicator, the orchestrator and the C-P1-012 claim author. The roster binds the packet adjudicator to a different model in that family; both passes deviate at model level, not family level. **The two passes are therefore not family-independent**; agreement across them tests position bias only, not family bias (B.9.7). A family preference would favour A; A ranked lower in both passes.
- **Order swap.** Same ordering in both passes, so no position effect is visible. Margins (1 and 3) are small.
- **Reconciliation contamination.** §2 was drafted before reading PASS1, but by the same family with the same inputs; I adopted one PASS1 score (B Principle integrity) after reading it.
- **Reviewer asymmetry.** Reviewer A derived against B's concrete model; Reviewer B could only review A structurally. B's collapse is visible partly because B is concrete.
- **My re-derivation** (`a_min ≤ 2·min(b,s)`, cell-verdict identity) is a hand reading of B's declared model. It is not a filed certificate, a search or a B.9.2 check, and carries no claim-state weight.
- **Common source set.** Authors and reviewers read the same `source/` set; agreement is not independent confirmation.
- **Length.** A ≈ 27.5 kB, B ≈ 15 kB; length not scored.
- **Isolation** is author-declared; logs not authenticated.
- **Model abstraction (both).** Joint-aligned contact, passive command and worst-case quantifiers bias a formal result toward ambiguity relative to the claim's real comparison; a target-relevant result needs K-S and a premise match.
- **Inherited confounds unchanged:** rate vs observer bandwidth (H2), friction placement (H3), Eng-1 weak reference and `placeholder_qr`, single planar 2-link fixture, factorial falsifier unrun.

C-P1-012: **Grade 2, Candidate.** No Locked Grade-1. No Eng-2 gate change. No retire-nominate.

DONE
