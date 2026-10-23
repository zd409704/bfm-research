# Prin-8 — PASS1 adjudication score

**Adjudicator:** Packet Adjudicator, PASS1 (Claude Opus). I authored neither proposal and neither review.
**Pass mapping:** P = `proposals/A.md` (Opus; field-status vocabulary, Phase 0 / declaration / Phase 1 freeze, T-002 and T-010 premise-match tables, guards G-1..G-10, stop rules). Q = `proposals/B.md` (Astra; separate applicability and realization records, four-valued evidence status, R3 paired-world certificate, V0 formal-statement row, conservative interval worksheet). Review of P = `reviews/B-on-A.md`. Review of Q = `reviews/A-on-B.md`.
**Inputs read:** packet `brief.md` and `roster.md`; every file in `source/` (packet brief, `method-Appendix-B.md`, C-P1-002 and C-P1-010 claim records, Prin-4 and Prin-7 decisions, current program ledger); both proposals; both draft summaries; both reviews; the run-level rubric in run-root `brief.md`; and Prin-7 `score-pass1.md`, read for format parity only.
**Effect:** planning only. **C-P1-002 stays Grade 2, Candidate. C-P1-010 Part A stays Grade 1, Candidate. C-P1-010 Part B stays Grade 1 conditional, Candidate.** This adjudication:
- makes no Locked Grade-1 and changes no grade or state;
- does not touch the Eng-2 gate (D-Prin-3-001), D-Eng-2-001 or D-P1-001;
- runs no measurement, spike, counterexample search, theorem check, solver or simulation, and seals no PLAN;
- edits no claim file and fills no template with target values;
- asserts no B.9.6 count for either claim, because the supplied sources do not establish one.

Nothing below is a necessity order (B.8.3). Nothing below mandates a sensor, numeric rate, controller family, processor location or research order.

---

## 1. Gates (B.9.5, before ranking)

| Gate | P | Q |
|---|---|---|
| Templates only; no execution, spike or search | Pass. Packet scope paragraph; Phase 1 "needs its own packet, which this proposal does not open". | Pass. "Design only." Every target row starts UNSET. Future experiments need "a separate sealed PLAN and authorization". |
| No grade/state change; no Locked Grade-1 | Pass. §3.5 and §4.5 list "Claim effect claimed: None"; closing grade line. | Pass. Header and §4: Grade-1 lock needs independent verification and the human signature. |
| Candidate cannot veto (B.4) | Pass. §4.5: "Candidate cannot veto (B.4). It mandates no rate, tier or ordering." | Pass. §4: "Candidate claims cannot veto a route." |
| Claim adjudicator ≠ author (B.9.1) | Pass. Header field `filler_role` must not be the claim adjudicator; bindings pre-filled to match the roster (Opus for C-P1-002, Astra for C-P1-010). | Pass in intent. The author does not adjudicate its own amendments. The binding is left UNSET (A-on-B W6), which is an amendment issue, not a gate failure. |
| Sufficiency ≠ necessity (B.3.5, B.5) | Pass. G-3: success never fills a realization field. G-9: the sanity spike fills no T-010 field. | Pass. "A successful behavior trace cannot fill an applicability row." Finite probes support "registered probes only". |
| Planning order / Grade 3 as necessity (B.8) | Pass. G-4 (evolution) and G-10 (no ordering or Eng-2 use). | Pass. D-Prin-4-001 is cited as a planning reference only. |
| Exact premise match (claim premises not silently widened) | **Pass, conditional.** T-010 rows A1a, A2b, A2c and A3 allow MATCH under tolerances declared at freeze. C-P1-010's premises and Scope exclude these effects outright, so this widens the premises (B-on-A R1, confirmed below). A labels three of the four rows [A-choice] and routes them to the adjudicator, so nothing is silently locked or vetoed. Amendment P-a must clear the finding before any T-010 row text is merged. | Pass. V1–V3 non-match routes keep the stated class ("Do not replace `T` with total latency"; "Nonlinear friction … cannot simply be called physical `b`"). |
| Eng-2 non-interference (D-Prin-3-001) | Pass. §5 "Not usable for: any Eng-2 gate, precondition or ranking input". | Pass. "These forms add no Eng-2 preconditions and clear none." The measurement point "supplies context, not automatic authorization". |
| B.9.6 count not guessed | **Pass, minor.** The header field `b96_counter_at_open` presupposes a known count. Amendment P-h allows UNKNOWN. | Pass. "Do not reset or guess its cumulative count." |
| No named products/companies | Pass. | Pass. |

**Both proposals are eligible for ranking, and neither is a Hard Reject.** P has one conditional gate finding, which amendment P-a must clear.

### Independent checks of the reviews' central objections

These are my readings of the proposals' own text and of the claim records. They are **not** filed evidence, not a B.9.2 verification, and not a theorem check.

**B-on-A (review of P)**

- **R1 (tolerance is not a premise match): confirmed.** C-P1-010 premise 1 is single-DoF. Premise 2 says "no extra computational or transport delay beyond the ZOH sample". Premise 3 says `b` is "linear viscous". The Scope excludes multi-DoF coupling, nonlinear friction and extra delay, and says "any delay-extended bound is a separate claim that needs its own source". A tolerance declared at freeze prevents result-dependent tuning, but it does not show the bound survives the deviation. A3's "residual after linear-viscous fit within declared tolerance" has the same defect and is **not** labeled [A-choice]. A's own §7 concedes that the strict reading "is probably fatal to Part B's applicability on a real humanoid joint". That is a real finding about the claim's target reach (see claim follow-up C010-4). It is not a reason to loosen the template.
- **R1, second part (§4.1 override): confirmed.** "…or when the adjudicator accepts a documented reason to proceed" lets a Part-B application verdict stand without its Part-A dependencies. Provisional arithmetic is harmless. An application verdict without those dependencies is not.
- **R2 (hiddenness and feasibility quantifiers): confirmed.**
  - P2-3's fields (pair, matched initial condition, `T`, `S₁`, `S₂`, disjointness argument) omit C-P1-002 premise 3's "initially hidden" condition. That condition is what makes the force history world-dependent *in response*, not world-dependent by construction. Q's R3 includes "who cannot distinguish them and until when".
  - P2-2 accepts "a demonstrated realization; either counts" against premise 2's "all declared disturbances". A finite demonstration does not discharge a universal quantifier.
- **R3 (status machinery contradictions): confirmed.** §2.1 permits MATCH only from MEASURED fields or declarations. Yet P2-2 and P2-3 require analytic arguments, which are DERIVED, and P10-B-cmp is DERIVED. P10-A1b (control-law form) is naturally established by an implementation audit, not by measurement. As written, the analytic rows can never MATCH.
- **R4 (pre-freeze narrowing exemption): partly confirmed, moderate.** Most Phase-0 edits select an instance within unchanged claim scope, and those are not B.9.6 events. But Phase 0 allows pre-marking SCOPE-EXIT "from design information" (§5). Mis-marking an in-scope joint as excluded is exactly the kind of scope change B.9.6 logs. The blanket exemption should become a classification (instance selection / plan revision / mapping correction / claim-scope change), with only the last routed for B.9.6 assessment.
- **R5 (Part-B comparison): confirmed, with one correction to the review.** The three-valued comparison needs registered uncertainty sets and a positive lower bound on `T`. However, the review says the equality case "belongs with the claim's non-strict retirement trigger". That would carry forward a boundary inconsistency in the claim record (adjudicator addition below). The equality case should stay with Q's V0 reconciliation and should not be fixed by either template.
- **R6 (one instance per loop): confirmed, moderate.** Cascaded or parallel loops at one joint share one port and one physical `b`. Part A's class is a single rendered impedance. Separate per-loop records cannot each claim the full `b` or compose a passivity statement.

**A-on-B (review of Q)**

- **W1 ("differentiation resolved" too low): partly confirmed; I downgrade it from major to moderate.**
  - The review is right that a positive lower bound on history distance is close to automatic. The two worlds have different exogenous disturbances, so the states diverge and state-dependent forces differ. Positive distance alone says nothing about the role.
  - Two qualifications. First, under C-P1-002 premise 4 and the tightened equivalence text, passive state-dependent differentiation that keeps the envelope *is* an admissible realization. So "no world-dependent active correction" is not by itself role absence. Second, Q's first disposition row already conjoins "tested envelope maintained".
  - The defect is the standalone sentence "differentiation is resolved". Amend that sentence (Q-1). The disposition logic is sound.
- **W2 (enclosure direction): confirmed as a required clarification.** "Enclosure" ordinarily means an outer bound, and Q's "overlapping enclosures mean unresolved" is consistent only with outer bounds. But "conservative" is ambiguous in safety work, where it often means an inner safe set. An inner approximation that is disjoint certifies nothing. The fix costs one sentence (Q-2).
- **W3 (model-bounded passive forces): confirmed, moderate.** Q's resolution contract carries "per-world reconstruction errors", but it does not flag counterexample or passive-realization candidates that rest on a model-bounded term.
- **W4 (no pre-data seal): confirmed.** Q says "predeclared" and defers execution to a sealed PLAN, but its form records no freeze event, no hash of the filled rows, and no rule for edits made between filling and data. P's §2.2 freeze and §6 stop rules supply exactly this, and are the main merge from P.
- **W5 (`T` as a design variable; inverse period): confirmed as optional.** An inverse-period row is prospective arithmetic. It risks being read as a rate mandate, which B.4 and C-P1-010 H5 forbid. The reviewer discloses same-family affinity with C-P1-010, and so do I. Admit it only as an optional, labeled row (Q-9).
- **W6–W8: confirmed, minor.** W6: bindings unset. W7: V0 is the natural Part-A object for the optional C-P1-001 dossier batch (D-Prin-4-001). W8: no fill order.
- **W9 (per-source observation timing): confirmed, moderate.** This is the same gap B-on-A R2 found in P, seen from the other side. Hiddenness has to be tied to what each response source in R5 can observe, and by when, relative to `D`.
- **S7 (strictness defect in the C-P1-010 wording): confirmed**, and extended in the addition below.

### Adjudicator additions (not in either review)

1. **C-P1-010 boundary inconsistency between Part A and Part B.**
   - Part A says the system is passive iff `b > K·T/2 + |B|`, i.e. iff `K < 2(b−|B|)/T`, a strict inequality. So at `|B| = 0`, `K = 2b/T` is **not** passively renderable, and "largest" `K_max` is a supremum that is never attained.
   - Part B's antecedent is `K_req,j > 2b_j/T_R2`, and its retire trigger is `2b_j/T_R2 ≥ K_req,j`.
   - At equality, Part B therefore says "retire for joint `j`", while Part A says the stated class cannot render `K_req,j` passively.
   - The boundary sits on the wrong side for Part A's own strictness. Neither template should resolve this. Q's V0 is the correct holding place, and P's comparison band must not absorb it. Routed as claim follow-up C010-1.
2. **Where C-P1-002's content lives.** Given premise 3 (disjoint safe-history sets), any trace pair that keeps the envelope in both worlds necessarily has differing histories by deadline `D`. The conclusion follows from premise 3 by set membership. So the empirical and target content of C-P1-002 sits almost entirely in the **R3 / P2-3 premise match**: hiddenness, disjointness and feasibility. The realization rows mainly check consistency.
   - The claim's "counterexample target" (envelope success with the role demonstrably absent) is, under matched premises, the same event as a falsified R3 certificate.
   - Q's §2B already reads it this way ("certificate inconsistency"). P's §3.3 routes it as a B.9.4(a) counterexample, which is less precise.
   - This supports Q's emphasis on the certificate. It also means the R3 row deserves the strongest independence requirement. Routed as claim follow-up C002-2.
3. **Q's status set lacks a scope-exit value.** Q's four statuses (UNSET / SUPPORTED-IN-SCOPE / CONTRADICTED / UNRESOLVED) have no value for "outside the claim's stated class". On V1–V3 a known excluded effect would be recorded as CONTRADICTED. Q's routing does say CONTRADICTED "does not retire the general claim automatically". But P's §2.4 distinction is sharper and should be imported (Q-10): a scope exit is neither a counterexample nor a B.9.6 narrowing, yet a pattern of scope exits is decision-relevant.

---

## 2. Rubric (fixed brief, 1–5, higher is better)

I used both reviews as inputs. Where my score differs from a review, the note says why. For parity, I scored identical behaviours identically.

| Dimension | P | Q | Note |
|---|---:|---:|---|
| Constraint fit | 5 | 5 | Both stay strictly template-only, with Candidate grades and no Eng-2 interaction. |
| Principle integrity | 3 | 4 | P: tolerance-MATCH beyond the premises (R1); Part-B override; no hiddenness check; equality pushed into a comparison band. Its guards G-1..G-10 are strong. Q: clean separation of applicability from realization; V0 catches the strictness defect; theorem transfer refused. Q gets 4 rather than A-on-B's 5 because of W1's loose sentence, W2's ambiguity and the missing scope-exit value. |
| Falsifiability | 3 | 4 | P: the absence and counterexample criteria are predeclared, but feasibility coverage and hiddenness are incomplete, and analytic rows cannot reach MATCH (R3). Q: certificate quantified over all histories, error-budget direction correct, and dispositions route adverse outcomes explicitly. |
| Evidence demand | 3 | 3 | Both demand certified safe-history analysis and total generalized-force accounting. That cost is inherent to C-P1-002. Neither lowers it. |
| Failure modes | 4 | 4 | P: named circularity guards, stop rules and a residual-risk section. Misses loop aggregation (R6). Q: four dominant failures named, each with a row. Misses enclosure direction (W2) and model dependence (W3). |
| Integrability | 4 | 3 | P: roster bindings pre-filled, claim hash, freeze and phase discipline, owner and filler separation. Q: owner and custody fields exist, but there is no freeze or seal event, the binding is unset, and there is no fill order. I score Q one below A-on-B for the missing seal, which W4 also flags. |
| Latency / criticality | 4 | 4 | Both keep the deadline `D` separate from measured delay and refuse to mandate a rate. |
| Complexity cost | 3 | 3 | P: seven statuses × three phases × instance multiplication. Q: two records per claim per case. Both acknowledge the cost. |
| Reversibility | 5 | 5 | Forms only. |
| Stackability | 4 | 4 | P: §5 "useful now" list. Q: V0 can feed the dossier, and the cross-claim coherence outcome is handled. |
| **Total** | **38** | **39** | |

Comparison with the reviews: B-on-A scored P at 37 and A-on-B scored Q at 41. My spread (1 point) is narrower than theirs, because I credit P's freeze machinery under Integrability and dock Q for its absence.

---

## 3. Decision (PASS1)

| Role | Proposal | Reason |
|---|---|---|
| **Recommend** | **Q** (narrow; provisional on PASS2) | Its core design is the more correct one. It separates applicability from realization, so success cannot fill premises and premise matches cannot fill realization. Its R3 certificate is quantified over all admissible histories. It handles `delta` honestly and refuses to invent separation or deadlines. Its V0 row catches the strict/equality defect in C-P1-010. Its interval worksheet has the right directions. It treats passive and embedded realizations symmetrically. Its defects (W1, W2, W3, W4, the missing scope-exit value) are local and cheap to repair. |
| **Alternate (mandatory merge source)** | **P** | It supplies the procedural machinery Q lacks: Phase 0 / declaration / Phase 1 with version-freeze and `claim_record_hash`; stop rules §6.1–6.5; named circularity guards G-1..G-10; the scope-exit discipline of §2.4; pre-filled roster bindings; the §5 "useful now / not usable for" list; and per-claim outcome routing tables. |
| **Merge** | **Required.** Q's records, statuses (plus SCOPE-EXIT) and certificate rules form the base. P's freeze/phase/stop-rule machinery and its guards are attached as the procedural layer. See merge notes and §4. | |
| **Reject** | (i) MATCH on any C-P1-010 Part-A row under a negligibility tolerance (P A1a/A2b/A2c/A3 as written). (ii) Part-B application verdicts without their Part-A dependencies (P §4.1 override). (iii) Reading positive history distance alone as role realization (Q §2B standalone sentence). (iv) Disjointness certified from inner or unspecified-direction enclosures. (v) Settling the C-P1-010 equality boundary inside a template, by either the review's "non-strict trigger" reading or a comparison band. (vi) A blanket "pre-freeze edits are never narrowing" rule. (vii) Any use of a filled template, a Phase-0 instance or the scalar-fixture PASS as grade, lock, veto, ordering or Eng-2 evidence. (viii) An inverse-period output framed as a required rate. | |

### Merge notes (P → Q), conditional on PASS2 agreeing

1. **Procedural layer.** Attach P §2.2 (phases and freeze at measurement-point declaration), §2.3 header fields (`claim_record_hash`, `template_version`, `filler_role`, `adjudicator_binding`) and §6 stop rules 1–5 to Q's common cover sheet. Q's "exact claim version" becomes the hash field. This answers W4.
2. **Status mapping.** Keep Q's four evidence statuses and add **SCOPE-EXIT**, carrying P §2.4's three properties. Import P's provenance classes (declaration / specification-audit / observation / derivation) as a separate *provenance* field, not as a status (B-on-A R3). Phase-0 verdict restriction: no SUPPORTED-IN-SCOPE or CONTRADICTED on physical-fact rows before the measurement point. Declaration rows may be SUPPORTED-IN-SCOPE in Phase 0 when they have an owner and an approval path.
3. **Guards.** Import G-1..G-10 as named check rows on the relevant Q rows: G-1/G-2 on R2/R3, G-3 on the realization rows, G-5 on R1–R5, G-6 on V7, G-7/G-8 on V1–V5, G-9 on V0, G-10 on the cover sheet.
4. **Routing tables.** Import P §3.5 and §4.5 as instance-level aggregation, corrected per P-c (feasibility), P-d (aggregation) and addition 2 (the counterexample target is a certificate inconsistency first).
5. **Phase-0 scoping list (P §5).** Import it as is, with P-e's classification applied to any pre-marked SCOPE-EXIT.

Do **not** import P's tolerance MATCH rules, its §4.1 override, its single-status-per-field vocabulary, its §2.5 blanket exemption, or its three-band comparison as written.

---

## 4. Mandatory amendments

### To Q (base)

1. **Q-1: Role-relevant differentiation (A-on-B W1, moderated).** Replace "If its lower bound is positive, differentiation is resolved" with two outcomes:
   - "differentiation present", when the lower bound on distance is positive;
   - "role-relevant realization supported for this probe", when envelope membership is verified in **both** matched worlds through `D`, the measured distance is consistent with the certified `delta`, and the force accounting is complete.

   State that positive distance below `delta` is "differentiation present, role relevance unresolved". Passive state-dependent differentiation that meets the envelope remains a passive-realization candidate, per C-P1-002 premise 4.
2. **Q-2: Enclosure direction (W2).** R3 must say "outer enclosure of each `S_i(D)`: every admissible safe history lies inside it". The certificate must name the enclosure direction for each uncertain parameter and for initial-state matching. Inner approximations cannot support disjointness.
3. **Q-3: Model-dependence flag (W3).** Every model-bounded force term enters the error budget `E` with its validation domain. Any counterexample candidate, certificate-inconsistency finding or passive-realization candidate that depends on such a term is flagged "model-dependent; replication by direct measurement required before claim routing".
4. **Q-4: Pre-data seal (W4; P merge 1).** Add a seal row: a hash of the completed applicability rows, the R3 certificate, the resolution contract (metric, `delta`, `D`, `E`), the probe set and the disposition table, recorded before any trace exists. Later edits become revision-history entries, classified per P-e.
5. **Q-5: Per-source observation timing (W9; B-on-A R2 mirror).** R3 and R5 jointly record, for each permitted response source, the earliest time its channels can separate `w0` from `w1`, with the information argument, compared against `D`. Hiddenness must be shown from channel content, not from disturbance difference alone.
6. **Q-6: Bindings (W6).** Pre-fill per the roster: Opus-family claim adjudicator for C-P1-002, Astra-family for C-P1-010. Rewrite the §4 author-affinity sentence plainly. Because Q is Astra-authored and C-P1-010's bound adjudicator family is Astra, bind an alternate (non-Astra, separate agent) for any ruling on Q-derived template text affecting C-P1-010. Disclose that an Opus alternate is same-family with the C-P1-010 claim author. Before any lock path, a cross-family re-ruling is still required.
7. **Q-7: Fill order (W8).** Cover sheet → V0 (no target data needed) → R3 certificate on the declared model → declaration rows → parameter and physical rows → realization rows. Premise failures should surface before instrumentation spend. The order is a planning convenience, not a gate.
8. **Q-8: Dossier link (W7).** A completed V0 may be offered as the Part-A component of a B.9.2 dossier if the human lead chooses to batch it with C-P1-001 (D-Prin-4-001). It stays Candidate until verification and signature. A target premise match is not a substitute for the proof check.
9. **Q-9: Optional inverse-period row (W5; same-family caution).** If included at all: label it "prospective arithmetic under the candidate bound; not a required or recommended rate (B.4, C-P1-010 H5)". Split "declared candidate period" from "realized period bound". Any inverse boundary inherits the V0 strictness reconciliation. Two Opus participants (the reviewer and this adjudicator) share family affinity with C-P1-010, so PASS2 should weigh whether to include it at all.
10. **Q-10: SCOPE-EXIT status (addition 3; P merge 2).** Add SCOPE-EXIT with P §2.4's properties. On V1–V3, a known excluded effect is SCOPE-EXIT. CONTRADICTED is reserved for evidence against a premise inside the stated class, or for a declaration that fails. Record patterns of scope exits across contact-critical joints for the claim adjudicator.

### To P (only for text merged from it)

- **P-a (B-on-A R1).** Delete tolerance MATCH on A1a, A2b, A2c and A3. Split each into three records: exact class membership; target-to-model adequacy; and any approximation extension, which is a separately governed claim outside this packet. A known excluded effect gives SCOPE-EXIT. Insufficient evidence gives UNRESOLVED.
- **P-b (R1, second part).** Strike the §4.1 "documented reason to proceed" override. Part-B arithmetic may be computed provisionally, but it gets no application verdict without its Part-A dependencies.
- **P-c (R2).** Add hiddenness to P2-3, carried by Q-5. P2-2: a demonstrated realization supports tested-instance feasibility only, unless it comes with an exhaustive or generalizing coverage argument over the declared sets. Disjointness quantifies over the registered plant uncertainty, not a nominal trajectory. An unproved argument is UNRESOLVED, never FAIL.
- **P-d (R3, R6).** Replace the single-status vocabulary with Q's statuses plus a provenance field. Add a complete aggregation table covering FAIL on P2-1a/P2-1d, CONTESTED, and NOT-APPLICABLE on P2-5b/A4/A5. An inapplicable passivity requirement cannot yield a Part-A application match. Make per-loop records subordinate to one aggregate port-law record per joint; an isolated-loop record needs an explicit isolation condition.
- **P-e (R4).** Replace §2.5's blanket exemption with a four-way classification: instance selection; plan revision; mapping correction; claim-scope change. Log all four with reason and evidence. Route only possible claim-scope changes for B.9.6 assessment, regardless of phase.
- **P-f (R5, corrected).** Comparison uses Q's interval worksheet with registered sets and `T_L > 0`. Name the low-side outcome "Part-B antecedent not established for this joint/configuration". The equality case is held open pending claim follow-up C010-1. It is not assigned by either template. P10-B8 must record the allocation of physical versus virtual stiffness. Mere presence of compliance is not premise-8 failure.
- **P-g (G-guards).** Keep G-1..G-10 verbatim, except that G-4 also covers developmental sources (B.8.6).
- **P-h (header).** `b96_counter_at_open` accepts `UNKNOWN (not established by supplied records)`. The template must never infer a count.

---

## 5. Claim follow-ups (for the bound claim adjudicators; none decided here)

**C-P1-010 (Astra-family claim adjudicator; Opus-authored claim)**

1. **C010-1: Strictness and boundary.** Reconcile three things: Part A's strict "iff `b > K·T/2 + |B|`"; the word "largest" for a supremum that is not attained; and Part B's antecedent `K_req,j > 2b_j/T_R2` against its retire trigger `2b_j/T_R2 ≥ K_req,j`. At equality the retire trigger fires although Part A says the stated class cannot render `K_req,j` passively. Rule whether this is a 0-count wording correction (with a written reason) or an amendment. Either way it is part of the B.9.2 item match for Part A.
2. **C010-2: Part B omits `|B|`.** Part B's threshold `2b_j/T_R2` is the zero-virtual-damping (optimistic) ceiling. Rule whether the record should say so explicitly, as Q's worksheet does.
3. **C010-3: Multiple loops per joint.** Rule whether the Scope should name cascaded or parallel rendering loops at one port explicitly as outside the class (B-on-A R6).
4. **C010-4: Target reach.** P §7 notes that strict premise matching may exclude every real contact-critical joint. Patterns of SCOPE-EXIT are not narrowing events. They are relevant to whether Part B can ever bear on the target plant, and a delay- or friction-extended bound would be a separate claim. No action is requested now.

**C-P1-002 (Opus-family claim adjudicator; Astra-authored claim)**

1. **C002-1: Operational hiddenness.** Premise 3's "initially hidden" has no operational definition in the record. Rule whether the per-source observation-timing record (Q-5) is the intended reading.
2. **C002-2: Where the content lies.** Given disjoint safe-history sets, envelope success in both worlds implies differentiation by `D`. The claim's counterexample target is therefore, under matched premises, a falsified premise-3 certificate. Rule whether the realization/absence text should say so, and whether the premise-3 certificate needs a stronger independence requirement than the other rows.
3. **C002-3: Support-mode pooling.** Both templates default to a per-mode instance. Confirm that this default matches premise 1.

**Counters.** No accepted B.9.6 event for either claim arises from Prin-8. Historical counts are not asserted (P-h).

---

## 6. Confounds

- **Adjudicator family.** This PASS1 adjudicator is Opus. That is the same family as Author A (P), Reviewer A (who reviewed Q), the orchestrator and the C-P1-010 claim author. The roster binds the packet adjudicator to an order-swapped Sonnet, which is a different model in the same family. This binding therefore deviates at the model level but not the family level, and the deviation is disclosed. A family-level preference would favour P, and P ranked one point lower. A same-family preference toward C-P1-010 could favour the optional Q-9 and claim follow-ups C010-1/2. Those are flagged for PASS2 to weigh.
- **Order swap incomplete.** This is PASS1 only (P = A, Q = B). The Recommend is provisional until PASS2 (P = B, Q = A) agrees. The margin is 1 point. The decision rests mainly on the qualitative gate and correctness findings (the P-a gate condition; W1/W2 as local fixes against R1–R3 as structural fixes), not on the total.
- **Review asymmetry.** B-on-A comes from an Astra reviewer of an Opus proposal, and A-on-B from an Opus reviewer of an Astra proposal. Each review is cross-family to its target. I checked every central objection against the proposal text (§1). I moderated W1 and corrected R5's equality recommendation.
- **No execution.** Every check above is a reading of text. None is a filed result, a theorem verification or a measurement.

**Status:** PASS1 complete. Recommend Q (B), provisional; Alternate P (A), mandatory merge source. All three claim components remain **Candidate** at their inherited grades. No Locked Grade-1. No Eng-2 gate change.
