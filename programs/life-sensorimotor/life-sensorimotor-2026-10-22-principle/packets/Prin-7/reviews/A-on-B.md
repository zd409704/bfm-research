# Prin-7 — Blind Review A on Proposal B

**Reviewer:** Blind Reviewer A (Claude Opus). **Target:** `proposals/B.md` and `drafts/B/summary.md` only. I did not read proposal A or `drafts/A/`.
**Inputs read:** packet `brief.md`, `roster.md`, `source/packet-brief.md`, `source/C-P1-012-claim.md`, `source/C-P1-012-prin6-ruling.md`, `source/Prin-4-decision.md`, `source/Prin-6-decision.md`, `source/method-Appendix-B.md`, `source/program-ledger-current.md`, and the run-level `brief.md` rubric.
**Status:** Review only. I edited no claim record, grade, state, PLAN, Eng-2 gate or decision file. I ran no search, solver, simulation or spike. The hand derivations in D1–D3 below are reviewer reading of B's own declared model. They are not filed evidence, not a certificate, and not a B.9.2 check. C-P1-012 stays **Grade 2, Candidate**.
**Family disclosure:** the reviewer is Opus, B's author is Astra (cross-family), and C-P1-012's claim author is Opus (same family as the reviewer). A same-family reviewer may lean toward keeping the claim alive. I flag every point where that bias could matter.

---

## 1. Gates (Appendix B, B.9.5), checked before scoring

| Gate | Result | Evidence in B |
|---|---|---|
| No grade/state change; no Locked Grade-1 | **PASS** | Header and §6 say "remains Grade 2, Candidate". Any lock requires "an accepted B.9.2 check and human signature on the exact statement". |
| PLAN before search; no execution | **PASS** | "PLAN only; no search, proof check, simulation, or spike executed". §4 says execution needs "a separate execution authorization and sealing step". |
| Author ≠ adjudicator (B.9.1) | **PASS** | §6: "The primary author cannot adjudicate this B-authored extension. Bind an independent reviewer and disclose family relationships". |
| Phenomenology ≠ necessity (B.3.5, B.5) | **PASS** | The refuter detector is called "an existence result". Nothing promotes a score to necessity. |
| Runner files only (B.9.8) | **PASS** | The future artifacts listed are "not a claim-state edit by the runner". |
| B.9.6 counter | **PASS** | Count stays 1. If the submodel is later substituted for the claim, each restriction must be ruled individually. Factor-drop and plant carve-out count as separate events. A zero count needs a written reason. |
| Inherited falsifier intact (Prin-6 P-1(i), P-4, P-7, R-3) | **PASS** | "These contact classes … do not replace or filter the inherited factorial classes, remove d50_M10, or change any filed thresholds". "Formal nonidentifiability cannot retrospectively rescore the factorial". |
| Eng-2 / planning order (D-Prin-3-001, B.8.3) | **PASS** | D-Prin-3-001 and D-Eng-2-001 are unchanged. No rate, field or ladder order is mandated. The model-level `(q,r)` is explicitly not target `(q,r)`. |
| Formal-evidence routing (Prin-6 ruling, "A P-1") | **PASS** | The §6 table matches the corrected rows. A checked certificate leads to a B.9.2 dossier and a separate grade packet. |
| No named products/companies | **PASS** | None found. |
| Retire-nominate not requested | **PASS** | "No retirement is justified by the supplied materials." |

All gates pass. The defects below are about quality and executability, not gates.

---

## 2. Strengths

- **S1. Event labels, not force identifiability.** B separates "cannot identify `J_cᵀF`" from "cannot detect an event" (§1). It requires the certified pair to have different event labels and rejects contact/contact ambiguity (§3). This closes a real gap in the claim's Grade-1 target sentence, which is written about identifiability of the force. A force-nonidentifiability result alone would not obstruct detection.
- **S2. The quantifier is right for an impossibility.** The obstruction is stated as "every detector using the permitted transcript, including randomized detectors", with the seed independent of the world. The result is explicitly a worst-case uniform-detection obstruction, with no average-case content (§3). The noncausal full-deadline transcript gives the impossibility side the strongest observer, which is the correct direction.
- **S3. The refuter has equal standing and is certificate-based.** A feasible solve needs an exact rational witness. An infeasible solve needs an exact dual certificate plus a separating functional with a strict gap. A solver status alone is "inconclusive" (§4.3–4.4). There are four distinct refuter types (cell, all-class, premise, proof-error), each with its own route.
- **S4. Union, not hull.** "Do not replace the union by a convex hull: hull overlap can manufacture ambiguity absent from the declared family" (§4.5). This anticipates a real way to manufacture a false positive.
- **S5. No outcome-selection.** The primary budget `b=1` is fixed in advance. The boundary cells `{0,1/4,1/2,2}` are separate model classes "not permission to revise the primary cell". The rules are no adaptive expansion, no deletion of durations, and a per-cell verdict in which one cell's collision cannot erase another cell's separation (§2, §4.6).
- **S6. Honest about what a collision does not show.** A collision does **not** single out measured effort, because a valid actuator law, a different history, an independent channel or another measurement could break the pair (§5). No rate floor is claimed (§5). Free disturbance sequences "cannot masquerade as a friction model" (§2). Together these avoid repeating the H3/H4 errors and do not mint a channel-necessity theorem the model cannot carry.
- **S7. Addresses the Prin-6 P-1(iv) vacuity flag.** It tests the distinguishability of explicitly listed histories instead of using an information criterion that any high-rate export would satisfy (§5).
- **S8. Placement is kept explicit.** U/D variants with `a_motor = u + n_up` versus `a_joint = u + n_up + n_down` follow premise 2 and H3. B adds that no physical device is assumed and that a provenance audit is required.
- **S9. Bounded cost.** One working day plus one review session. At the cap, missing certificates are "unresolved, never a failed counterexample search or proof" (§4), consistent with Prin-6 P-5.

---

## 3. Defects

**D1 — The nuisance-budget allocation is contradictory, and the contradiction decides the primary verdict. (Major.)**
The table says "For each channel separately, `|n_i[k]|≤b`". The next row says "Total nuisance bound `b=1`, allocated to one channel as specified below". Nothing below specifies an allocation; the next paragraph covers only U/D placement. The two readings give opposite primary results:
- *Per-channel `b`:* nuisance exists on both joints. Under the reading in D2, every cell collides.
- *Total `b` on one channel:* the other joint has zero nuisance. Its baseline observation then shows any contact on it exactly, so every `j` = nuisance-free cell separates trivially. The primary conjecture ("a collision in each declared contact cell") then fails in half the cells by construction.

Before sealing, the PLAN must state which reading holds. Under the single-channel reading it must also state which channel and why. Otherwise the runner has to choose, and that choice decides the outcome.

**D2 — The primary and boundary outcomes can be computed from the PLAN text. The search is not a search. (Major, with a confound.)**
Under B's own declarations, the observation map collapses to something trivial:
- Inputs are piecewise constant on 5 ms intervals, integration is exact, samples are taken at interval boundaries, and initial conditions are known.
- So `q̇[k+1] − q̇[k] = T M⁻¹(u + n + g)[k]` per channel. With `u` known, the transcript reveals the per-interval total disturbance `d[k] = n[k] + g[k]` exactly, on each joint separately (`M` is diagonal).
- Hence `L` is injective on `n+g`, and a collision exists iff there are admissible `n0, n1` with `n0 − n1 = g`.

Under the per-channel reading:
- **Primary cell `b=1`.** Before onset set `n0 = n1 = 0`. During the event set `n0 = +a/2`, `n1 = −a/2` with `a = 1`. The per-step jumps are 0.5 ≤ 1 and the amplitudes are 0.5 ≤ 1. This gives a collision in **every** duration/direction/joint cell, under both placements.
- **Boundary cells.** Collisions exist iff `2b ≥ a_min = 1`. So `b ∈ {1/2, 1, 2}` collide (`b = 1/2` only at the boundary, `a = 1`). `b ∈ {0, 1/4}` separate everywhere, with the detector "alarm iff `max|d[k]| > b`".

So the planned LP/dual-certificate machinery would recompute a two-line inequality. The "theorem" content is: *an unknown additive torque whose amplitude bound is at least half the contact amplitude, on the same channel and with the same timing freedom, masks the contact*. That is a correct Grade-1 statement, but close to a definition. Two consequences:
- (a) **Preregistration is weaker than claimed.** "selected now, independently of any result" is formally true, but the result can be read off the parameters `b = 1`, `a ∈ [1,2]`. The choice of `b` relative to `a` is the whole finding. That is the same built-in-conclusion pattern H3 identified for the P1 sim.
- (b) **Too much apparatus.** A closed-form lemma plus independent proof check would fully replace §4 steps 2–5. That would be cheaper, easier to verify under B.9.2 (a qualified human can check it), and more transparent.

B should disclose this collapse and either (i) adopt the closed-form route, or (ii) change the model so the question is non-trivial. For (ii), the nuisance would need structure that contact lacks, for example a declared friction law depending on `q̇` or `u`, a nonzero or probing command, or coupled `M` with a non-joint-aligned `J_cᵀF`. Then ambiguity is not decided by amplitude comparison alone.

**D3 — The placement variants are identical in the baseline and definitional under augmentation. (Moderate.)**
The dynamics see only `n_up + n_down`, so U and D produce the same `L`, `Y0` and `Y1` for the baseline transcript. §4.2's "for each … placement" therefore duplicates every cell. That should be stated, so the duplicates are not read as replication or robustness.

Under the §5 augmentation:
- adding `a_motor` in U reveals `n` exactly and separates trivially;
- in D it equals `u` and adds nothing.

B says the variants make the sensor claim "testable rather than definitional". In this model the result *is* definitional: an effort channel helps exactly when it contains the nuisance. That repeats the H3 concern one level up. It is not wrong, but it adds no evidence about Factor E beyond its definition.

**D4 — The target falls short of C-P1-012's Grade-1 form, and the bridge is left unstated. (Moderate.)**
The claim's Grade-1 target says `J_cᵀF` is not identifiable "**without a measurement of** `τ_cmd + τ_act_unmodeled`", which asserts that a specific channel is needed. B correctly declines to show that (§5, S6). But then a successful certificate does not prove the Grade-1 form as written. At most it proves a restricted reformulation. B's §6 routes that as a separate amendment with B.9.6 accounting, which is good.

What B leaves out: the PLAN never states the exact theorem sentence it expects the dossier to carry, or how that sentence relates to the claim's target sentence. Is it the same statement, a narrower instance, or a different statement? A reader could take a "checked ambiguity certificate" as progress on the Grade-1 form, when it is really progress on a neighbouring statement. Before sealing, B should write out the target theorem and classify it against the claim text.

**D5 — The zero command removes the Factor-E comparison the claim is about. (Moderate.)**
Factor E contrasts "commanded setpoints plus the nominal control law" with realized effort. With `u ≡ 0`, the commanded baseline carries no information, and the nuisance cannot depend on the command or state. B scopes this honestly ("passive finite-horizon"). Even so, command-dependent and state-dependent actuator effects (saturation, velocity-dependent friction) are exactly the ones a nominal-law reconstruction might partly capture. The model class rules them out by construction, so it cannot show whether they are separable. Together with D2, the primary model is closer to "unknown input observer with an arbitrary bounded input" than to Factor E.

**D6 — The latency contract sits on its own boundary. (Minor.)**
The refuter detector decides at the deadline, which gives latency = 100 ms against a contract of "p95 ≤ 100 ms" (§4). Separation in the `b < 1/2` cells could in fact alarm at the first post-onset sample (5 ms). But the PLAN as written credits the all-class refuter only at equality. If the contract were read as strict, or the deadline sample were excluded, the refuter would fail on a technicality. Prefer "decision at the first sample after onset where the certified test fires" or a deadline strictly inside the bound.

**D7 — Indexing and unit ambiguities. (Minor.)**
- `G_j` uses `j` both as the contact-joint index and as the cell index. "Each duration/direction contact cell" leaves unclear whether a cell is (duration, `s`, `j`) or (duration, `s`) with `j` pooled. This matters for per-cell verdicts and for D1.
- The slew bound "≤ 1" has no stated unit. Per 5 ms step, it is 200 units/s. That ties the nuisance class to the sampling grid, and §5 needs that fact before any later rate comparison.
- "Consistent units" for `M = diag(1,2)` is acceptable, but should state that `M` cancels out of the collision condition (D2).

**D8 — Worst-case versus the inherited average-case contract. (Minor; disclosed.)**
The inherited falsifier measures TPR at a fixed false-event rate as an empirical frequency over sampled worlds. B's obstruction is worst-case over nuisance. B says so (S2), but should also state the consequence: a worst-case obstruction cannot conflict with, or pre-empt, a Factor-E witness in the registered factorial. In the factorial, nuisance follows a sampled distribution and adversarial alignment of the kind in D2 has measure zero. §6 already protects the factorial procedurally. This adds the mathematical reason.

---

## 4. Is the PLAN executable without search?

**Mostly yes, after three pre-seal fixes. In fact it is more executable than B claims, because it needs no search at all.**

- **No literature search needed.** The model, horizon, sampling, contact classes, task contract, certificate types and routes are all stated in the packet. They depend on no external result or named tool. Exact rational LP with dual certificates can be done with any exact-arithmetic method. B names no tool, which is consistent with the no-products constraint.
- **No computational search needed (see D2).** Under the per-channel reading, collision versus separation in every cell follows from `2b ≥ 1`, and the witness and separating detector have closed forms. A runner could carry out §4 mechanically, but the whole outcome reduces to a pen-and-paper lemma that a qualified human can check under B.9.2.
- **Blocking before sealing:**
  - (1) resolve the budget allocation (D1);
  - (2) fix the cell indexing and the slew units (D7);
  - (3) write out the exact target theorem sentence and how it relates to C-P1-012's Grade-1 text (D4).
- **Non-blocking but recommended:**
  - disclose the analytic collapse and the U/D baseline identity (D2, D3);
  - move the refuter's decision time strictly inside the latency bound (D6).
- **Still required by governance:** a separate execution authorization and sealing step, an independent bound reviewer (B.9.1), and later a B.9.2 check and grade packet. B states all of these.

---

## 5. Rubric scores (run brief; 1–5; gates already passed)

| Dimension | Score | Reason |
|---|---|---|
| Constraint fit | **5** | PLAN only. No grade, Eng-2, lock or retire change. No named products. Inherited falsifiers untouched. |
| Principle integrity | **4** | Grades, necessity vs sufficiency, worst-case vs average, and model vs target are cleanly separated, and it refuses to claim channel necessity. −1 for D4: the theorem it would deliver is not the claim's Grade-1 sentence, and the PLAN does not say so explicitly. |
| Falsifiability | **3** | Refuters are well defined and can succeed within a day. But the outcome of every preregistered cell is fixed by the declared parameters (D2), and the primary verdict depends on an unresolved allocation (D1). The attempt is falsifiable in form but predetermined in substance. |
| Evidence demand | **5** | One working day plus one review. No hardware, data or training. |
| Failure modes | **3** | Many failures are named: hull overlap, floating-point status, outcome selection, constitutive mismatch, hidden information. It misses the analytic collapse (D2), the U/D identity (D3) and the latency boundary (D6). |
| Integrability | **4** | Clear handoffs: runner files, bound reviewer, B.9.2 dossier, separate grade packet. The body-loop channel definitions (`a_motor`, `a_joint`) are generic and audited. |
| Latency / criticality | **3** | The fixed 5 ms grid and noncausal deadline are fine for an impossibility. They say nothing about the fast-tier or rate question (Factor R), which B correctly defers. The refuter latency sits at the bound. |
| Complexity cost | **3** | Exact LP with dual certificates over 80+-dimensional polytopes, for a problem with a closed-form answer (D2). The machinery would only pay off under a richer, structured nuisance model. |
| Reversibility | **5** | Cheap to abandon. Every output routes as an annotation or a review input. Nothing locks. |
| Stackability | **3** | Certificate formats and routes extend to richer models. But the primary model's results are too close to definitional to anchor later work. Bridging to the target needs a counted reformulation (D4), plus D5's command and state dependence. |
| **Total** | **38 / 50** | |

---

## 6. Confounds

1. **Built-in conclusion via the amplitude ratio (D2).** With `b = 1` and `a_min = 1`, collision is guaranteed. With `b < 1/2`, separation is guaranteed. The preregistered grid fixes every verdict in advance. Whatever the runner files, it records the parameter choice, not a discovery about Factor E.
2. **Placement is definitional (D3).** In the baseline the U/D variants are the same computation. Under augmentation, an effort channel separates exactly when it contains the nuisance. This is H3's concern moved up one level.
3. **Passive, state-independent nuisance (D5).** It excludes the command- and state-dependent effects where a nominal-law reconstruction could plausibly help, so it is biased toward ambiguity relative to Factor E's real comparison.
4. **Decoupled, joint-aligned contact.** `M` is diagonal and contact is applied as `a s e_j` in joint space. That removes the Jacobian and localization structure in the claim's `J_cᵀF` and the inertial coupling that might separate contact from per-joint actuator nuisance.
5. **Worst-case vs. sampled-world contract (D8).** The formal obstruction and the registered factorial measure different things. Neither can pre-empt the other, and B's §6 correctly keeps them apart procedurally.
6. **Allocation ambiguity (D1).** If it is left unresolved, the runner's reading becomes an uncontrolled factor that decides the primary verdict.
7. **Reviewer family.** I am the same family as C-P1-012's claim author. My D4/D5 criticism, that the model is too weak to bear on Factor E, runs *against* an easy upgrade, so it is not the direction a same-family bias would push. But my overall acceptance of B's framing should be weighed with this disclosure. The packet adjudicator (Sonnet, order-swap) is also the same family as this reviewer. Disclose this under the roster note.

---

## 7. Recommendation to the packet adjudicator (on B alone)

B is a disciplined, governance-clean PLAN that is consistent with the record. Its framing has real merit: event labels instead of force identifiability, a randomized-detector quantifier, union not hull, and certificate-only verdicts. Before it is sealed, it should be amended as follows:
- (M1) resolve the budget allocation (D1);
- (M2) disclose that the declared model reduces to the closed-form condition `2b ≥ a_min`, and either adopt a closed-form proof as the primary route or add nuisance structure (state- or command-dependent law, nonzero command, coupled `M` / non-aligned `J_cᵀF`) so that the formal question is non-trivial (D2, D5);
- (M3) state the exact target theorem and classify it against C-P1-012's Grade-1 sentence, as the same statement, a narrower instance, or a different statement (D4);
- (M4) state that U/D are identical under the baseline observation (D3);
- (M5) fix the cell indexing, the slew units and the refuter decision time (D6, D7).

None of these amendments changes C-P1-012's grade, state, B.9.6 count, falsifier or any Eng-2 gate. **C-P1-012: Grade 2, Candidate. No retire-nominate warranted.**
