# Prin-8 — PASS2 adjudication score (order-swap)

**Adjudicator:** Packet Adjudicator, PASS2 (Claude Opus). I authored neither proposal, neither review, and not PASS1.
**Pass mapping (swapped):** P = `proposals/B.md` (Astra; separate applicability and realization records, four-valued evidence status, R3 paired-world certificate, V0 formal-statement row, conservative interval worksheet). Q = `proposals/A.md` (Opus; field-status vocabulary, Phase 0 / declaration / Phase 1 freeze, T-002 and T-010 tables, guards G-1..G-10, stop rules). Review of P = `reviews/A-on-B.md`. Review of Q = `reviews/B-on-A.md`.
**Procedure:** I read packet `brief.md` and `roster.md`, run-root `brief.md` (rubric), all seven files in `source/`, both proposals, and both reviews. I then drafted independent gates and scores (§2, column "Draft") **before** reading `score-pass1.md` in full. Reconciliation with PASS1 is in §3.
**Effect:** planning only. **C-P1-002 stays Grade 2, Candidate. C-P1-010 Part A stays Grade 1, Candidate. C-P1-010 Part B stays Grade 1 conditional, Candidate.** This adjudication:
- makes no Locked Grade-1 and changes no grade or state;
- does not touch the Eng-2 gate (D-Prin-3-001), D-Eng-2-001 or D-P1-001, and adds no Eng-2 precondition;
- runs no measurement, spike, counterexample search, theorem check, solver or simulation, and seals no PLAN;
- edits no claim file and fills no template with target values;
- asserts no B.9.6 count for either claim.

Nothing below is a necessity order (B.8.3). Nothing below mandates a sensor, numeric rate, controller family, processor location or research order.

---

## 1. Gates (B.9.5, before ranking)

| Gate | P (= B) | Q (= A) |
|---|---|---|
| Templates only; no execution, spike or search | Pass. "Design only"; every target row UNSET; future experiments need "a separate sealed PLAN and authorization". | Pass. Phase 1 "needs its own packet, which this proposal does not open". |
| No grade/state change; no Locked Grade-1 | Pass. Header and §4. | Pass. §3.5 / §4.5 "Claim effect claimed: None". |
| Candidate cannot veto (B.4) | Pass. | Pass. |
| Claim adjudicator ≠ author (B.9.1) | Pass in intent; binding left UNSET (amendment, not gate failure). | Pass; `filler_role` ≠ adjudicator; bindings pre-filled per roster. |
| Sufficiency ≠ necessity (B.3.5, B.5) | Pass. "A successful behavior trace cannot fill an applicability row." | Pass. G-3, G-9. |
| Planning order / Grade 3 as necessity (B.8) | Pass. | Pass. G-4, G-10. |
| Exact premise match (no silent widening) | Pass. V1–V3 non-match routes keep the stated class ("Do not replace `T` with total latency"). | **Pass, conditional.** Tolerance-MATCH on P10-A1a/A2b/A2c/A3 widens C-P1-010 premises 1–3 beyond the Scope exclusions; three of four rows are disclosed [A-choice], A3 is not. Nothing is locked or vetoed by it, so this is not a Hard Reject, but no T-010 row text may be merged until amendment Q-a clears it. |
| Eng-2 non-interference (D-Prin-3-001) | Pass. "These forms add no Eng-2 preconditions and clear none." | Pass. §5 "Not usable for … any Eng-2 gate". |
| B.9.6 count not guessed | Pass. | Pass, minor (`b96_counter_at_open` presupposes a known count; Q-h). |
| No named products/companies | Pass. | Pass. |

**Both eligible for ranking; neither is a Hard Reject.** The gate outcome is identical to PASS1 with the labels swapped.

### Independent verification of review objections (readings of text, not filed evidence)

**A-on-B (review of P):**
- **W1:** confirmed as **moderate**, not major. Given C-P1-002 premise 3, any pair of traces that keeps the envelope in both worlds is in `S_0(D)` and `S_1(D)` respectively and so necessarily differs; positive distance alone is near-automatic and uninformative. But B's first disposition row already conjoins "tested envelope maintained", and passive state-dependent differentiation that keeps the envelope is an admissible realization under the claim's tightened equivalence text. The defect is the standalone sentence "differentiation is resolved". Independently reached the same moderation as PASS1.
- **W2:** confirmed. Disjointness needs disjoint **outer** enclosures of each `S_i(D)`; "conservative" is ambiguous. One-sentence fix.
- **W3, W4, W9:** confirmed, moderate. W4 (no pre-data seal) is the main reason Q's freeze machinery must be merged.
- **W5:** see §4, P-9 — I decline to admit it in this packet.
- **W6–W8:** confirmed, minor.
- **S7 / S8:** confirmed. I re-derived the interval-row directions from B's own symbols: `K_L > 2b_U/T_L` is the worst case for the trigger; `K_U ≤ 2b_L/T_U` is the best case for non-trigger; the ceiling enclosure is monotone-correct given `b_L > β_U`.

**B-on-A (review of Q):**
- **R1 (tolerance ≠ premise match), both parts:** confirmed. C-P1-010 Scope: "Any delay-extended bound is a separate claim that needs its own source." A's own §7 concedes the strict reading is "probably fatal to Part B's applicability on a real humanoid joint" — a real finding about target reach, not a reason to loosen the template. The §4.1 "documented reason to proceed" override is also confirmed.
- **R2:** confirmed. P2-3 omits "initially hidden"; P2-2 lets a finite demonstration discharge "all declared disturbances".
- **R3:** confirmed. Under §2.1 the analytic rows (P2-2, P2-3, P10-B-cmp) can never reach MATCH, which is an internal contradiction.
- **R4:** partly confirmed. Most Phase-0 edits are instance selection, not narrowing; but pre-marking SCOPE-EXIT "from design information" (§5) can mis-exclude an in-scope joint, which B.9.6 should see.
- **R5:** confirmed except the review's equality recommendation (assigning equality to the "non-strict retirement trigger"), which would carry forward the C-P1-010 boundary inconsistency (§5, C010-1).
- **R6:** confirmed. Multiple loops at one joint share one port and one physical `b`.

### PASS2 adjudicator additions (not in either review or in PASS1)

1. **Symbol collision `T`.** C-P1-002 uses `T` for the incompatible-history deadline; C-P1-010 uses `T` for the sampling period. A uses `T` for the deadline in P2-3 and also proposes a shared clock field across both claims (§2.6). In a merged template this invites substituting one for the other — exactly the "measured delay ≠ common-input interval" confusion Prin-4 warned about. B already uses `D` for the deadline. **Merged text must use `D` for the C-P1-002 deadline and reserve `T` for sampling period**, with a note in the cover sheet.
2. **Phase-0 status of analytic rows.** PASS1 merge note 2 forbids SUPPORTED-IN-SCOPE on physical-fact rows before the measurement point, and PASS1 Q-7 places the R3 certificate early in the fill order. These are consistent only if a Phase-0 R3 certificate computed on an unvalidated model is recorded as **UNRESOLVED (provenance: derivation; dependency: R1 model validation pending)**, not SUPPORTED-IN-SCOPE. State this explicitly.
3. **V0 is not a Phase-gated row.** V0 needs no target data. Completing it is a B.9.2 verification event for the bound C-P1-010 adjudicator and the human lead, not a template fill, and it may proceed independently of the measurement point. A V0 entry in a template instance only references that verification record; it never constitutes it.
4. **A's P2-1d "FAIL if below the authority assumed in P2-3".** Actuator authority is a fixed premise of the certificate, not a test outcome. A mismatch means the R3 certificate was computed on the wrong plant: route as a **new case / certificate recomputation**, not as FAIL or premise-failure evidence against the claim.

---

## 2. Rubric (fixed brief, 1–5, higher is better)

| Dimension | P (B) Draft | P (B) Final | Q (A) Draft | Q (A) Final | Note |
|---|---:|---:|---:|---:|---|
| Constraint fit | 5 | 5 | 5 | 5 | Both strictly template-only. |
| Principle integrity | 5 | 4 | 3 | 3 | P: clean applicability/realization split; V0 catches strictness defect. Reconciled down to 4 (see §3). Q: tolerance-MATCH (R1), Part-B override, no hiddenness. |
| Falsifiability | 4 | 4 | 3 | 3 | P: certificate over all histories; W1/W2 weaken the absence test as written. Q: analytic rows cannot MATCH (R3); feasibility coverage incomplete. |
| Evidence demand | 3 | 3 | 3 | 3 | Both inherit C-P1-002's safe-history and total-force cost. |
| Failure modes | 4 | 4 | 4 | 4 | P misses enclosure direction, model dependence. Q misses loop aggregation; strong guards. |
| Integrability | 4 | 4 | 5 | 4 | Reconciled (see §3). |
| Latency / criticality | 4 | 4 | 4 | 4 | Both separate deadline from measured delay; neither mandates a rate. |
| Complexity cost | 3 | 3 | 3 | 3 | P: two records per claim per case. Q: seven statuses × phases × instance multiplication. |
| Reversibility | 5 | 5 | 5 | 5 | Forms only. |
| Stackability | 4 | 4 | 4 | 4 | P: V0 feeds optional dossier; cross-claim coherence. Q: §5 "useful now" list. |
| **Total** | **41** | **40** | **39** | **38** | |

---

## 3. Reconciliation with PASS1

| | PASS1 | PASS2 draft | PASS2 final |
|---|---:|---:|---:|
| B | 39 (as Q) | 41 (as P) | **40** |
| A | 38 (as P) | 39 (as Q) | **38** |
| Margin | B +1 | B +2 | **B +2** |

Dimension-level differences and resolution:
- **B, Principle integrity (draft 5 → final 4; PASS1 4).** I accept PASS1's addition 3: B has no status for "outside the stated class". On V1–V3 a known excluded effect would be recorded as CONTRADICTED, which B defines as an "adverse record". A pattern of scope exits filed as adverse records could later read as counter-evidence. That is a principle-integrity defect (applicability vs. falsification conflated), not only a usability one.
- **A, Integrability (draft 5 → final 4; PASS1 4).** I accept R6 as an integrability defect: one instance per loop assigns ownership at the wrong unit for a shared physical port.
- **B, Integrability (draft 4; PASS1 3; final 4).** I do **not** follow PASS1 here. PASS1 docked B for the missing seal/freeze event; I score that under Failure modes/Falsifiability (where W4 already bears), and B does have owner, custody, review and measurement-context rows. Counting the seal twice would penalise B for one defect. This is the only unresolved dimension disagreement; it moves B by 1 and does not affect the ranking.
- All other dimensions agree exactly across PASS1 and PASS2 after label swap.

**Order effect:** none detected in the ranking. B leads in both orders; the PASS2 margin is 1 point wider, entirely from the Integrability disagreement above.

---

## 4. Decision (PASS2)

| Role | Proposal | Reason |
|---|---|---|
| **Recommend** | **P = B** | Same reasons as PASS1, independently reached: applicability/realization separation; R3 certificate over all admissible histories; honest `delta`; V0 holds the C-P1-010 strictness defect open instead of resolving it; correct interval directions; passive/embedded symmetry. Its defects are local wording fixes. |
| **Alternate (mandatory merge source)** | **Q = A** | Procedural layer B lacks: phases and freeze with `claim_record_hash`; stop rules §6.1–6.5; guards G-1..G-10; §2.4 scope-exit discipline; pre-filled roster bindings; §5 useful-now / not-usable list; routing tables. Its defects (R1–R3) are structural and must not be merged as written. |
| **Reject** | — | PASS1 Reject list (i)–(viii) affirmed, plus (ix) using `T` for the C-P1-002 deadline in merged text; (x) recording a Phase-0 model-only certificate as SUPPORTED-IN-SCOPE. |

### PASS1 Recommend survives: **YES.**
PASS1 Recommend B (as Q) / Alternate A (as P); PASS2 Recommend B (as P) / Alternate A (as Q). Consistent across the order swap. Merge direction (B base, A procedural layer) is also consistent.

---

## 5. Mandatory amendments (PASS2 relabelled; deltas from PASS1 marked)

PASS1's Q-1..Q-10 now apply as **P-1..P-10** (to B, base) and PASS1's P-a..P-h now apply as **Q-a..Q-h** (to A text being merged). All are affirmed, with these PASS2 changes:

- **P-9 (inverse-period row, A-on-B W5): NOT ADMITTED in this packet. [PASS2 change]** PASS1 left this to PASS2. Both passes and the proposing reviewer are Opus, the C-P1-010 author family, so the affinity confound is not removed by the swap. On merits: before the measurement point, all inputs are unset, so the row has no planning value now, and its output reads naturally as a required rate, which B.4, C-P1-010 H5 and the packet brief forbid. It may be re-proposed by a non-Opus participant or by the bound Astra C-P1-010 adjudicator after V0 reconciliation. The "declared candidate period vs realized period bound" split from W5 **is** admitted, since it is bookkeeping, not an output.
- **P-11 (new): deadline symbol.** Merged text uses `D` for the C-P1-002 incompatible-history deadline and reserves `T` for sampling period (addition 1). A's shared clock-authority field (§2.6) is retained only as a timestamp authority; it carries no period or deadline value.
- **P-12 (new): Phase-0 analytic rows.** A Phase-0 R3 certificate on an unvalidated model is UNRESOLVED with provenance "derivation" and a listed dependency on R1 validation (addition 2).
- **P-13 (new): V0 status.** V0 references an external B.9.2 verification record; it is never satisfied by template fill and is not phase-gated (addition 3).
- **Q-i (new): authority mismatch.** A's P2-1d mismatch routes to "new case / certificate recomputation", not FAIL (addition 4).
- **P-6 (bindings), clarified.** Same as PASS1 Q-6. Note that both packet adjudications were Opus; this does not change the binding rule for claim rulings.

Merge notes 1–5 from PASS1 stand unchanged.

---

## 6. Claim follow-ups (for bound claim adjudicators; none decided here)

PASS1 §5 items C010-1..C010-4 and C002-1..C002-3 are affirmed. I independently re-derived C010-1: with `|B| = 0`, Part A's strict condition makes `K = 2b/T` non-passive, while Part B's retire trigger `2b_j/T_R2 ≥ K_req,j` fires at equality. The boundary is on the wrong side for Part A's strictness.

Added:
- **C002-4:** Rule whether the claim record should adopt a distinct symbol for the deadline (premise 3's `T`) to avoid collision with C-P1-010's sampling period in shared target evidence. Wording only; no scope effect intended, so not a B.9.6 event unless the adjudicator rules otherwise.

**Counters.** No accepted B.9.6 event for either claim arises from Prin-8. Historical counts not asserted.

---

## 7. Confounds

- **Adjudicator family.** This PASS2 adjudicator is Opus, as was PASS1. The roster specifies an order-swapped Sonnet adjudicator: same family, different model. Both passes deviate at model level, not family level; disclosed. The order swap therefore controls position bias only, not family bias. A family preference would favour A (Opus); A ranked lower in both passes.
- **Same-family affinity with C-P1-010.** Shared by Author A, Reviewer A, PASS1 and PASS2. This is the reason P-9 is not admitted.
- **No cross-family packet adjudication.** If the wall clock allows, a Class-2 cross-family check would remove the remaining confound; not applied here, and its absence is logged.
- **No execution.** Every check is a reading of text; none is a filed result, theorem verification or measurement.

**Status:** PASS2 complete. **Recommend B (P), Alternate A (Q), mandatory merge. PASS1 Recommend survives.** All three claim components remain **Candidate** at their inherited grades. No Locked Grade-1. No Eng-2 gate change.
