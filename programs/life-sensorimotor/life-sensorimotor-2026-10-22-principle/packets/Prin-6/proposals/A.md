# Proposal A — Packet Prin-6: C-P1-012 prospective evidence-to-action table

**Author:** Competing Author A (Claude Opus, medium). Isolated draft tree `drafts/A/`. B's draft was not seen.
**Claim under review:** C-P1-012 (inherited by ID). Current record: **Grade 2, Candidate, stay** (Prin-3 claim adjudication). Cumulative accepted B.9.6 narrowings = **1**.
**Packet scope (packet-brief):** a planning table that maps possible future evidence to the *allowed* claim actions. This packet changes no grade or state, registers or seals no PLAN, runs no spike, and changes no Eng-2 gate.

---

## 1. Thesis

Future evidence about C-P1-012 should reach the record through a **fixed, ceiling-based table** that is agreed before the evidence exists. Each row pairs an evidence class with an evidence-quality tier and gives the **strongest action allowed**. The claim adjudicator may always choose a weaker action; nobody may go above the ceiling without a new packet.

Four design commitments make the table hard to game:

1. **The admissibility tier comes before the result.** Whether a result is favourable or adverse never sets its tier. A result from an unsealed PLAN, a failed harness, or a reference cell that misses the absolute competence contract (A02-class) has **annotate** as its ceiling, whichever direction it points.
2. **The table is asymmetric, as B.3.5, B.4 and B.5 require.** A favourable result (realized-at-R1 wins, substitution drop met) can at most be **annotated** as sufficiency or realization evidence. It never promotes. An adverse, competent, in-premise result can reach **claim-adj review**, which includes challenge or falsification handling and, where the claim says so, retire-nominate consideration.
3. **Rescues are counted at the moment they are proposed.** Any response that keeps the claim alive by narrowing scope or adding a premise is an **amend via B.9.6** action and is logged individually. The count stands at 1 now, so a third accepted event (two more) triggers mandatory retirement review. No row lets a narrowing in as an "annotation" or a "clarification".
4. **Unresolved stays unresolved.** Every comparison row has three outcomes: *competent match*, *established failure of the matching rule*, and *unresolved* (Prin-3 B-2). An unresolved result can only be annotated. It counts neither for nor against the claim, and ∞ − ∞ is never a finite latency match.

## 2. Action vocabulary (ordered weakest → strongest)

| Code | Action | Who | Effect on record | Counter effect |
|---|---|---|---|---|
| **N** | None | — | Filed under the packet/spike only. No entry in claim files. | 0 |
| **AN** | Annotate | Claim adjudicator, or the orchestrator with the adjudicator's countersign | Append-only evidence-status note in `upgrade-log.md` (Prin-3 B-3 style). Must say what does *not* follow. | 0 |
| **AM** | Amend via B.9.6 | Claim adjudicator only | Premise, scope or falsifier text change. Each accepted change is logged with its event number. | +1 per accepted narrowing or rescue premise. 0 only if the adjudicator rules it a non-narrowing clarification under the Prin-3 B-1/B-2 precedent. |
| **CR** | Claim-adj review | Claim adjudicator (cross-family; Astra for this Opus-authored claim) | Formal ruling. Possible outcomes: stay; tighten (then also AM); falsified-factor finding for a plant model; retire-nominate; challenge admission under B.9.4 (only relevant if the claim were ever Locked). | Per any AM it produces |

**Never available from this table:** grade change (in either direction), Candidate→Locked, recommended-for-lock, adding or removing an export field, setting a numeric sampling rate, research-order inference, target-plant acceptance, or any change to the Eng-2 gate (D-Prin-3-001).

## 3. Admissibility tiers (assigned before reading the result)

| Tier | Conditions (all must hold) | Default ceiling |
|---|---|---|
| **T0 — Inadmissible** | No sealed PLAN; or PLAN hash mismatch; or `harness_pass=false`; or smoke-only run; or post-hoc class selection (Prin-3 A-1 rejected) | **N** (AN only to record that the run exists and was not credited) |
| **T1 — Harness-valid, competence-unmet** | Sealed PLAN; harness valid; but the in-scope reference cell misses the declared absolute detection/latency contract (A02-class), *or* placeholder task parameters `(q,r)` are in use | **AN** |
| **T2 — Competent, prospective** | T1 conditions, and: absolute contract met by the reference; every Prin-3 B-2 element predeclared (miss handling, event accounting, confidence family, comparison direction, explicit substitution margin); all registered classes with `d ≥ 10 ms` kept; friction placement declared relative to sensing (premise 2/H3); detector tuned fairly per rate (H2) | Row-specific (§4) |
| **T3 — Competent, target-grounded** | T2 conditions, plus task parameters ratified by the human lead (not placeholders) and a declared target-plant measurement point | Row-specific. Needed for premise-failure rows. |

The Eng-1 S2a-XC result (`harness_pass=true`, `A02=false`, `placeholder_qr=true`) is **T1**. Its existing B-3 annotation is the correct ceiling outcome and is not reopened.

## 4. Evidence-to-action table

"Ceiling" is the strongest action allowed; the adjudicator may pick a weaker one. "Forbidden inference" is binding on all downstream text.

### 4a. Factorial counterexample search (Factor E / Factor R)

| Row | Evidence | Tier | Outcome | Ceiling | Forbidden inference |
|---|---|---|---|---|---|
| E-1 | Commanded-at-R1 vs realized-at-R1, in-scope (DOWN-class placement) | T2+ | **Competent match** on every class with `d ≥ 10 ms` (ΔTPR ≤ 0.05, Δp95 ≤ 10 ms, predeclared CI direction) | **CR**: Factor E falsified *for that plant model*; the adjudicator decides between narrowing (→AM, counted) and retire-nominate if Factor R also falls | "Effort information is never needed"; the result does not carry over to other plant models |
| E-2 | Same | T2+ | **Established failure** of the matching rule (realized clearly better, competent) | **AN** — sufficiency of realized export for this detector/plant | Necessity of Factor E; any grade movement; any export-field mandate |
| E-3 | Same | T2+ | **Unresolved** (CI straddles the threshold, latency undefined in one cell, misses unreconciled) | **AN** | Treating it as a match or as a failure |
| E-4 | Same | T1 | Any | **AN** | Anything beyond "search ran; not credited" |
| R-1 | Realized-at-R2 vs realized-at-R1 (rate re-tuned per H2) | T2+ | **Competent match** | **CR**: Factor R falsified for that plant model | A numeric rate floor or ceiling for the target plant |
| R-2 | Same | T2+ | **Established failure** | **AN** — sufficiency of R1 for this class | A rate floor as necessity; "200 Hz required" |
| R-3 | Same | T2+ | Unresolved, or the rate effect is confounded with observer bandwidth (Prin-3 A-3 issue) | **AN**; a bandwidth-matched control may be recommended for a *future* PLAN | Attributing the difference to rate |
| ER-1 | E-1 **and** R-1 both competent matches in the same sealed run | T2+ | — | **CR** with explicit retire-nominate consideration (claim falsifier text) | Retirement decided by anyone other than the claim adjudicator |

### 4b. A-4b search cell (command + identified friction model)

| Row | Evidence | Tier | Outcome | Ceiling | Forbidden inference |
|---|---|---|---|---|---|
| F-1 | Command + friction model fitted on disjoint data, using permitted information only, scored against the in-scope DOWN reference | T2+ | Competent match, **and** the adjudicator finds residual unmodeled effects still present (premise 2 holds) | **CR**: in-premise command-reconstructible alternative; challenges Factor E | Automatic retirement (A-4a reasoning was rejected) |
| F-2 | Same | T2+ | Competent match, but the fit removed the nuisance premise (no unmodeled effects left) | **AN**: out-of-premise. Optional **CR** only to consider whether premise 2 should be stated more precisely; any resulting change goes through **AM** and is counted | Counting it as an in-premise refutation; quietly adding "friction unidentifiable" as a premise without counting it |
| F-3 | Same | T2+ | Matches UP only | **AN** (external diagnostic) | Any challenge to Factor E |
| F-4 | Same | T2+ | Fails or unresolved | **AN** | Strengthened necessity |

### 4c. Operational realization (substitution) test (B.9.3)

| Row | Evidence | Tier | Outcome | Ceiling | Forbidden inference |
|---|---|---|---|---|---|
| S-1 | Replace the exported effort channel with the command-reconstructed value; in-scope placement; margin predeclared and not lowered from the filed criterion; d50_M10 kept | T2+ | Drop ≥ margin on all identifiable classes, absolute contract met | **AN**: role *realized* by this channel/fixture/detector/calibration. May be cited as the B.9.2 "operational test" item in a *future* lock dossier | Promotion; necessity; implementation independence |
| S-2 | Same | T2+ | Drop < margin on any identifiable class | **AN**: role not realized by that channel on this fixture (filed message text). Optional **CR** if repeated across ≥ 2 independent fixtures/detectors, to ask whether the role is realizable at all in-premise | "Effort information is absent"; lowering the margin afterwards (would be AM, counted, and is discouraged) |
| S-3 | Same | T1 (as Eng-1 DOWN) | Any | **AN**; already done (Prin-3 B-3) | Re-scoring the filed result |
| S-4 | Same, UP placement (friction upstream of sensing) | Any | Any | **AN**: external comparator only (Prin-3 A-5) | In-scope realization or necessity support |

### 4d. A02-class (absolute competence) results

| Row | Evidence | Tier | Outcome | Ceiling | Forbidden inference |
|---|---|---|---|---|---|
| A-1 | Reference cell meets the absolute contract under ratified `(q,r)` | T3 | — | **AN**: raises later comparisons in the same PLAN family to T2/T3 eligibility | That the contract met is a necessity premise; target-plant acceptance |
| A-2 | Reference cell fails the absolute contract again | T1 | — | **AN** | Treating the failure as evidence *for* the role ("nothing works, so the role is needed") or *against* it |
| A-3 | No detector in a serious, logged search meets the contract in any cell | T2 attempted | — | **AN**, plus a recommended **CR** on whether the competence class in premise 3 is achievable on this fixture at all | Converting infeasibility into necessity |

### 4e. UP diagnostics and premise-match evidence

| Row | Evidence | Tier | Outcome | Ceiling | Forbidden inference |
|---|---|---|---|---|---|
| U-1 | Any UP-placement result (substitution, factorial, A-4b) | Any | Any | **AN** (external) | In-scope support or refutation |
| U-2 | A declared target-plant measurement shows its effort sensing sits upstream of the dominant nuisance (UP-like) | T3 | — | **CR** on a B.9.4(b)-style premise-failure submission (scope or premise fit for the target). Any resulting scope change → **AM**, counted | Assuming target placement from a fixture; admitting premise failure without the measurement declaration |
| U-3 | Target plant has a dedicated torque or tactile channel | T3 | — | **AN**: outside scope (premise 5); the role is trivially met | Using it as confirmation |

### 4f. Formal and argument-level evidence (not spikes)

| Row | Evidence | Outcome | Ceiling | Forbidden inference |
|---|---|---|---|---|
| P-1 | Identifiability argument (Grade-1 upgrade target) submitted with a premise list and admissible model class, checked independently (B.9.2 G1 route) | Check passes | **CR**, to record that an upgrade argument exists. *Grade change requires a separate upgrade packet and human signature* | Grade change by this table; Locked |
| P-2 | Same | Check finds a gap or counter-model | **AN** in `upgrade-log.md`. **CR** if the counter-model satisfies the claim premises (it is then a counterexample under §4a semantics) | Retirement without CR |
| P-3 | Argument across implementation classes (Grade-2 route item 1) | Drafted | **AN** | Treating it as B.9.2-complete without the operational test and failed-search log |
| P-4 | C-P1-011 side-channel audit (Prin-5 inventory) finds an upper-layer access path to command history or effort | — | **CR**: H8 dependence; the motivation narrows to the Factor-E nuisance argument. Any wording change → **AM**, with counting decided by the adjudicator | Automatic change to C-P1-012 because C-P1-011 changed |

### 4g. Process-level evidence

| Row | Evidence | Ceiling |
|---|---|---|
| G-1 | Researcher-family agreement or disagreement (including A vs B on this packet) | **N** (B.9.7) |
| G-2 | Rubric scores, benchmark wins, convergence across methods | **N** for grade; at most **AN** as sufficiency |
| G-3 | Ladder order, D-P1-001 or P1 Alternate cited for or against | **N** (B.8.3; H6) |
| G-4 | Any proposed rescue arriving with any row above | **AM** only, logged individually even when bundled (Prin-3 instruction) |

## 5. Decision procedure (for whoever files future evidence)

1. Identify the PLAN hash and assign the tier from §3 **before** opening results. Record the tier in the filing.
2. Classify each comparison as competent match / established failure / unresolved, using only predeclared rules.
3. Look up the row. Write the ceiling action and its forbidden inferences into the filing.
4. If the ceiling is CR, route to the bound claim adjudicator (Astra for C-P1-012). The orchestrator does not rule.
5. If any party proposes a narrowing or rescue premise, log it as a separate AM candidate with a provisional counter value (current 1 → would be 2, then 3 = mandatory retirement review).
6. A result that fits no row gets **AN** until a later packet adds a row. The table may be extended only by a packet decision, never at filing time.

## 6. Interfaces with other gates

- **Eng-2 (D-Prin-3-001):** unchanged. No row authorizes, blocks or conditions any Eng-2 spike. T3 requires ratified `(q,r)` and a measurement point; this describes evidence *quality* and is not a gate. If a T3 run ever occurs, it occurs under the human lead's existing gate.
- **C-P1-001 dossier (D-Prin-4-001):** no interaction.
- **Prin-4 priority 4 (identifiability attempt):** feeds rows P-1/P-2 only. It needs its own PLAN before any search.

## 7. Non-claims

This proposal does **not** claim or imply:

1. That C-P1-012 is true, false, necessary, or closer to lock. Grade stays **2, Candidate**.
2. That any row raises or lowers the grade. Grade changes need a separate packet and, for lock, human signature.
3. That the Eng-1 FAIL is evidence for or against necessity (B.9.8). It is T1, already annotated.
4. That a realized-effort export field, a specific sensor type, or a numeric rate (50 Hz, 200 Hz, or other) is required on the target plant.
5. Any ordering of S0a/S2a/S1 or any upgrade of D-P1-001 / the P1 Alternate.
6. Any new Eng-2 precondition, or relaxation of the existing one.
7. That a PLAN is registered or sealed. The thresholds quoted are the claim's existing ones; no new numeric threshold or substitution margin is set here.
8. That UP results or dedicated-sensor plants bear on in-scope necessity.
9. That the table is complete. Unlisted evidence defaults to AN.
10. That this author's agreement with prior rulings is evidence (B.9.7).

## 8. Known weaknesses / objections invited

- **Tier gaming:** a future PLAN author could predeclare loose CI families to reach T2 cheaply. Mitigation: the adjudicator may demote the tier at CR time, and a demotion is not an AM.
- **Repeated-S-2 trigger (≥ 2 fixtures)** is a planning heuristic, not a principled count. B may propose a better trigger.
- **F-2 boundary:** deciding whether a fitted friction model "removed the nuisance premise" is itself a judgment call. The row routes it to the adjudicator rather than encoding it.
- The table assumes the claim stays Candidate. If it is ever Locked, rows E-1/R-1/F-1/U-2 become B.9.4 challenge-admission inputs, and the table would need re-adjudication.

## 9. Requested disposition

Adopt the table as a **planning artifact** attached to the C-P1-012 record by reference (packet decision only). The claim adjudicator is invited, but not required, to note in `upgrade-log.md` that future filings should cite a row ID. No claim-file edits by this packet.
