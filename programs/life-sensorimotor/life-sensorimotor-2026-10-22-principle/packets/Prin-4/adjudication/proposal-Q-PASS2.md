# Prin-4 — Proposal A (Author A, Claude Opus)

**Packet:** Prin-4. Lock-path and next Principle priorities.
**Author:** Competing Author A (Opus family). This document proposes only. It changes no claim state or grade.
**Inputs read:** `brief.md`, `roster.md`, `packets/Prin-4/source/{packet-brief,Eng-2-decision,Prin-3-decision,method-Appendix-B,program-ledger-current}.md`, `claims/C-P1-001/claim.md`, `claims/C-P1-012/claim.md` (status and grade lines only).
**Not read:** `claims/C-P1-001/{upgrade-log,violations}.md`, the Prin-1 ruling text, and the other claim records. When an item below depends on them, it is marked *confirm*.
**Inherited by ID:** D-P1-001 (Provisional, acceptance gate, not a necessity order), D-Prin-2-001 (no ladder-edge gates), D-Prin-3-001 (common human `(q,r)` and measurement-point gate), D-Eng-2-001 (Recommend A, deferred), X-Eng-1-001 (FAIL filed).

---

## 1. Thesis

While Eng-2 is gated, Principle work should go to items that **need no Eng-2 data and either (a) de-risk the gated spike or (b) can be closed by verification and signature alone**. No Principle item should become a new precondition for Eng-2. C-P1-001 is ready for a lock decision once one independent proof check is done and the record is reconciled. The remaining work is administrative and verification work, not research. Even once locked, its veto covers only the **scalar fixture**. It prunes no target-plant route until a separate premise match exists, so its program value is limited and it should not be described as more than that. No Candidate has met a retire trigger. All of them should be left as they are until Eng-2 data or a B.9.6 event arrives.

---

## 2. C-P1-001 lock-path checklist (B.9.2 Grade-1 route; proposal only)

The lock route is B.9.2 Grade 1: (i) a proof checked independently of its author through one of three allowed routes, and (ii) the human lead's signature. Re-derivation by model families, including the Opus claim adjudicator's re-derivation of L* recorded in the ledger, counts as **persuasiveness evidence only** (B.9.7). It is not one of the three allowed routes unless a qualified human reviews it.

Author A independently checked the arithmetic: `L* = ln(1.1)/10 = 0.009531017980…` s, and `Δ(0.02)/2 = 0.1·(e^{0.2}−1) = 0.022140275816…`. Both match the claim. This check is also model agreement, and it does not satisfy item C2.

| # | Item | Status (from files read) | What closes it |
|---|---|---|---|
| C1 | **Record reconciliation.** `claim.md` says "Recommended adjudicator action: Candidate-stay; obtain independent proof verification before considering recommended-for-lock". The ledger says "Candidate; recommended-for-lock (conditional)". | **Open (inconsistent)** | The claim adjudicator (Opus family, per roster) appends a note naming the governing state and **enumerating the conditions** behind "conditional". The note is append-only and does not rewrite history. |
| C2 | **Independent proof check, one allowed route** | **Open** | Pick one route: **(a) Formal checker.** Mechanize the scalar statement, for example in Lean/Mathlib: Carathéodory solution of `ẋ = ax + u + d` with `u ∈ L¹_loc`, common `u` on `[0,L)`, the closed-form difference `Δ(t) = (2D/a)(e^{at} − 1)`, the triangle bound `max|x±| ≥ Δ/2`, and the contrapositive for `L > L*`. This route is the cheapest and fully independent. **(b) Published-result match.** Map each premise to the variation-of-constants formula for linear ODEs with locally integrable forcing, citing a standard ODE text, and append the item-by-item premise table. **(c) Qualified human review** of the five-line proof. Record the route, the checker or reviewer identity, and the artifact hash. |
| C3 | **Premise audit before signing** (precision only, no change in force) | Open | The adjudicator confirms in writing: (1) the envelope holds for **all t** in a horizon containing `[0, L]`, so violation at any `t ∈ (L*, L]` suffices, because Δ is monotone increasing; (2) solutions are Carathéodory solutions and continuous, with no impulses, as premise 5 states; (3) randomized controllers are coupled on the same realization, so the claim is a robust guarantee and not an expectation, as premise 4 states; (4) "channel capable of changing applied control" is read as *every* input path to `u`, including passive and mechanical ones, so that passive stabilization counts as changed dynamics (`a`) and not as a counterexample; (5) the bound is stated as `≤`, and equality makes no claim about viability. |
| C4 | **Actuator bound excluded from the theorem** | Done in record (premise 6) | The signing text carries premise 6 verbatim. The `|u| ≤ 3` bound is a fixture constraint, and the latency inequality is not sufficient for invariance. |
| C5 | **Scope and veto statement for the signer** | Partially done | Add an explicit **veto-scope paragraph** to the signing package. The lock vetoes only routes that claim a robust envelope guarantee on *this scalar fixture* (`a = 10`, `b = 0.01`, `D = 1`) with a common-input interval greater than L*. It vetoes **nothing** on the target plant until a separate premise-match record exists, covering `a`, `b`, `D`, support mode, and common-input interval. The humanoid-plausible `a ≈ 3.3` mode needs its own instantiation. |
| C6 | **Measured delay ≠ common-input interval** | Done in record | The signing package repeats this: a measured total response delay is not premise 4's interval, and Eng-1/Eng-2 artifacts may not cite the lock against a measured delay without logging the interval separately. |
| C7 | **Citation ablation (B.8.7)** | Done in record | No biological premise is used. Nothing further is needed. |
| C8 | **Falsifier and challenge mode** | Done in record | Nothing further is needed. Optional: register the counterexample-search PLAN described in the record. **This is not required** for a Grade-1 lock under B.9.2 (the failed-search requirement is Grade-2), so it should not block signing. |
| C9 | **B.9.6 narrowing count** | *Confirm* (`upgrade-log.md` not read) | The adjudicator states the count. The Prin-1 expansion of the stub should be classified explicitly as either a clarification or a narrowing event. |
| C10 | **Adjudicator binding** | Per roster: Astra-authored claim → Opus-family adjudicator | Record the binding in `claims/C-P1-001/` if it is absent. Author A is a packet author and is not the claim adjudicator. |
| C11 | **Signature package and irreversibility notice (§6 rule 4)** | Open | Assemble one file containing the claim text, the C2 artifact, the C3 confirmations, the C5 veto scope, the C9 count, and a "this prunes routes without contest" notice. The human lead signs or declines. **Until signed, the state stays Candidate. No artifact may say "Locked".** |

**Minimal closing sequence:** C1 → C2 (route a or c) → C3 + C9 → C11 → human signature. C5 and C6 are text added to the package. Nothing on this path depends on Eng-2 data or the `(q,r)` gate.

---

## 3. Principle priority list while Eng-2 is gated

**This is a planning order and is not evidence (B.8.3).** No item becomes an Eng-2 precondition beyond D-Prin-3-001's existing common gate. No Candidate is used as a veto.

| Rank | Item | Why now | Needs Eng-2 data? | Output |
|---|---|---|---|---|
| 1 | **C-Eng2-A-01 cross-family claim adjudication (Astra)** | The Recommend-A ceiling construction rests on this lemma. Auditing it before the gate clears avoids sealing a PLAN on an unchecked premise. It is listed as outstanding in D-Eng-2-001. | No | Ruling: Candidate stay / tighten / premise defect. It is still not a gate. |
| 2 | **C-P1-001 signing package (§2)** | It is closest to completion and costs only verification and signature work. It also exercises the B.9.2 Grade-1 path once on a small claim. | No | Signed or declined lock. Fixture-scoped either way. |
| 3 | **C-P1-012 Grade-1 identifiability upgrade attempt** | The upgrade target is a mathematical statement: `J_cᵀF` is not identifiable from `(q, q̇, τ_cmd)` when `τ_act_unmodeled` overlaps it in time and frequency. It can be argued or refuted now, and Eng-2 cell labels (`CH_LIMIT` vs `DET_GAP_*`) will be read against it later. | No | `upgrade-log.md` entry: proof sketch, counterexample, or stated obstruction. The grade stays 2 until B.9.2 is met. |
| 4 | **C-Eng1-A-01 pooled-window independence audit** | Prin-3 listed it. It affects how X-Eng-1-001 statistics are read and is cheap. | No | Audit note. No state change requested. |
| 5 | **C-P1-011 side-channel audit (DPI ceiling)** | It shares the information-ceiling logic with C-P1-012 and Eng-2's channel-level reference. A side channel found here would change how CEIL results are read. | No | Tightened premise list, or a filed violation. |
| 6 | **C-P1-002 / C-P1-010 target premise match** | Both need target-plant facts, and the effort measurement point is still undeclared by the human lead. | Partially (needs the human declaration) | Deferred. Draft the premise-match templates now and fill them in after the declaration. |
| 7 | **Prin-2 edge claims (C-Prin2-E*)** | D-Prin-2-001 set no edge gates, and nothing in Eng-2 depends on them. | No | Dormant. Revisit only if a proposal cites an edge. |

Ranks 1, 2 and 3 can run in parallel because they use different adjudicators and different routes.

---

## 4. Retire / leave nominations

**Retire-nominations: none.** Reasons for each claim:

| Claim | Nomination | Reason |
|---|---|---|
| C-P1-001 | **Leave → lock path (§2)** | Not challenged and not narrowed (C9 *confirm*). |
| C-P1-012 | **Leave until Eng-2 data** | Eng-1 FAIL is sufficiency-level only (D-Prin-3-001). The Prin-1 retire trigger ("both factors falsified") has not fired: X-Eng-1-001 records no FE/FR counterexample, and SUB_DOWN_NOT_MET does not show the information is absent. The narrowing count is 1 (Prin-3 claim adjudication). Watch B.9.6: if an Eng-2 interpretation needs another premise added to survive, log it as an event. |
| C-P1-002 | **Leave (tighten-premises pending)** | The open target premise match is blocked by the human measurement-point declaration. Retiring it now would read a missing declaration as evidence. Watch: if no tightened text exists by the next Prin packet, flag it for adjudicator review. This is not a retire nomination. |
| C-P1-003 | **Leave (Grade 3 quarantined)** | Quarantine already forbids theorem-style use. Retirement would wrongly suggest the path contingency was refuted, when it was neither refuted nor upgraded. X-P1-004 already covers how it is used. |
| C-P1-010, C-P1-011 | **Leave (tighten-premises)** | No counterexample has been filed (*confirm* `violations.md`). They are on the priority list at ranks 5 and 6. |
| C-Eng1-A-01, C-Eng2-A-01 | **Leave** | Design lemmas, not gates. Adjudication or audit is pending. |
| C-Prin2-E* | **Leave** | Quarantine costs nothing. Retiring edges in bulk would be governance churn with no information gain. |

---

## 5. Non-claims

- This proposal does **not** assert that any claim is Locked. C-P1-001 stays Candidate until the human lead signs.
- It does **not** change any grade. All grade movements are left to the bound claim adjudicators.
- Model re-derivations, including this author's arithmetic check and the Opus adjudicator's L* re-derivation, are **not** B.9.2 independent verification (B.9.7).
- A C-P1-001 lock would **not** certify any target-plant latency, controller rate (the nominal 250 Hz / 1 kHz values remain placeholders), architecture, or B-N2 role.
- The priority list is **not** a necessity ladder and **not** an Eng-2 gate. D-P1-001 stays Provisional, and D-Prin-2-001 still sets no edge gates.
- Leaving C-P1-012 alone does **not** endorse it as a veto. Eng-1 FAIL is **not** downgrade evidence, and a future Eng-2 PASS will **not** be promotion evidence.
- This proposal makes **no** claim about the content of the human `(q,r)` table or the measurement point, and no claim about choosing between Eng-2 branches A and B.
- No hardware transfer, named platform, or evolutionary necessity is asserted anywhere in it.
