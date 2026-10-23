# Prin-3 — Proposal A (Author A, Claude Opus)

**Packet:** Prin-3 — spike-informed Principle update after the Eng-1 S2a-XC FAIL
**Author family:** Opus. Per roster, the claim adjudicator for C-P1-012 and C-Eng1-A-01 (both Opus-authored) is Codex gpt-6-astra. Author A proposes changes; it does not change claim state.
**Inputs read:** `brief.md`, `roster.md`, `packets/Prin-3/source/*`, `claims/C-P1-012/*`, `claims/C-Eng1-A-01/*`. I did not read Author B's drafts or proposal.
**Not available in source:** `sensitivity_fixedgain.json`, `contrasts.json`, PLAN v2 text (including the numeric B.9.3 margin). Where an argument depends on these, I mark it **[needs artifact]**.
**Plant framing:** generic home humanoid / target plant only.

---

## 1. Thesis

The S2a-XC FAIL is an **engineering-sufficiency result about one realization** (a motor-side "realized" effort export under XC-0, on a planar fixture, scored against **placeholder** `(q, r)`). It is **not** a Principle result about C-P1-012. The spike changes no grade (B.9.8, B.4).

The spike does yield three things the Principle track should file:

1. **Neither C-P1-012 falsifier fired.** This holds at the DOWN placement (in-scope) and the UP placement (out of scope). It counts as one weak, single-fixture **failed counterexample search**. It is logged but is not grade evidence on its own (B.9.2, B.9.7).
2. **The registered falsifier has a degenerate match rule.** All three DOWN "matches" for Factor E are cells where **both** detectors fail (TPR < 0.05). Under the current wording, two failing detectors "match". The rule should be repaired before it is used again.
3. **The B.9.3 operational test has power, and it shows that motor-side effort does not realize the role when the dominant nuisance sits downstream of the sensor.** UP placement gives a large substitution drop: met, mean 0.56. DOWN placement gives a small one: not met, min 0.06, mean 0.11. H3 in the claim record predicted this. The data show that the operative variable for Factor E is **where the effort is measured relative to the nuisance**, not whether the effort is labelled "realized" or "commanded".

**Engineering stance:** Recommend **B** (S0a finite-horizon envelope, amended before it spikes) as the Eng-2 mainline. Any S2a-XC retry moves to the **Principle track as a C-P1-012 counterexample search (§12.2)**, not an Eng-2 engineering retry. An engineering retry of A is **ineligible** until the human lead ratifies `(q, r)` and the target plant's sensing placement is declared. I reject threshold relaxation and scope widening as ways to turn the FAIL into a PASS.

---

## 2. What the spike does and does not imply for C-P1-012

### 2.1 Data read-back (from `source/Eng-1-S2a-XC-METRICS.md`, r_w = 0.001 per 100 ms = 0.01/s)

**Factor E at DOWN (in scope; joint-side friction downstream of current sensing).** The table compares R1_CMD with R1_REAL_DOWN on d ≥ 10 ms.

| class | CMD | REAL_DOWN | ΔTPR | match (≤ 0.05)? | both < 0.05? |
|---|---|---|---|---|---|
| d10M2 | 0.001 | 0.001 | 0.000 | yes | **yes** |
| d10M5 | 0.014 | 0.033 | 0.019 | yes | **yes** |
| d10M10 | 0.115 | 0.275 | 0.160 | no | no |
| d20M2 | 0.005 | 0.016 | 0.011 | yes | **yes** |
| d20M5 | 0.156 | 0.320 | 0.164 | no | no |
| d20M10 | 0.587 | 0.734 | 0.147 | no | no |
| d50M2 | 0.112 | 0.247 | 0.135 | no | no |
| d50M5 | 0.627 | 0.752 | 0.125 | no | no |
| d50M10 | 0.874 | 0.936 | 0.062 | no | no |

- Every "match" in the 3/9 reported is a both-fail floor cell. On every cell where either detector does anything, realized-DOWN beats CMD by 0.06 to 0.16. Motor-side effort carries **some** information beyond the command reconstruction, but not much.
- Calibrated drift is about the same in both: CMD 0.354, REAL_DOWN 0.328, against REAL_UP 0.018. The large nuisance residual survives in the DOWN "realized" channel. This is what you expect if neither channel observes the joint-side friction.

**Factor R** (R2_REAL vs R1_REAL). R2 is far worse everywhere: at d50M10, DOWN is 0.375 vs 0.936 and UP is 0.700 vs 1.000. The falsifier did not fire. However, METRICS itself states that "rate contrast is confounded with observer bandwidth (gain·T fixed)". Fixing gain·T makes the R2 observer's continuous bandwidth about 4× lower. The H2 repair therefore swapped the P1 confound (a near-unstable discretization at R2) for another one (a bandwidth handicap at R2). **[needs artifact: sensitivity_fixedgain.json]** is needed before reading anything about Factor R from this run.

**Harness / power.** ORACLE_R1 meets q0.90 on 9 of 12 classes (all except d5), and H1 to H4 pass. The fixture can therefore identify d ≥ 10 contacts. Even the privileged UP channel meets **0 of 12** classes under Bonferroni q0.90 (5 of 12 pointwise). The placeholder `(q, r)` plus the multiplicity correction is demanding enough that A02 could fail for reasons other than the effort channel. p95 latency is `inf` in almost every non-oracle cell, so the latency term of the falsifier (Δp95 ≤ 10 ms) is undefined there.

### 2.2 What the spike does imply

| # | Implication | Force |
|---|---|---|
| I-1 | No in-premise counterexample to Factor E or Factor R was found on this fixture, at either placement, including under the identifiable-only rule. | Log as a failed counterexample search (`upgrade-log.md`). Partial input to the B.9.2 Grade-2 route. **Not** grade evidence alone: one plant, one detector family, one nuisance model. |
| I-2 | The B.9.3 substitution test has demonstrated power. It detects a realizing channel (UP: met) and flags a non-realizing one (DOWN: not met). | Validates the **test**, which supports keeping it as the claim's operational realization test. |
| I-3 | On this fixture, a current-derived (motor-side) effort export does **not** realize the C-P1-012 role when the dominant unmodeled effect is downstream of sensing. | This is a statement about a realization, which is exactly what B.9.3 is for. It is **not** a statement that the role is absent or unneeded. |
| I-4 | The Factor E / Factor R falsifiers as registered are not well-posed in floor cells: both-fail matches count, and p95 = inf. | Falsifier repair needed (A-1, A-2 below). |
| I-5 | The rate contrast is not yet clean. | Factor R stays unadjudicated in either direction until bandwidth is decoupled (A-3). |

### 2.3 What the spike does **not** imply

- It does not imply a grade change for C-P1-012, up or down (B.9.8; B.4: "phenomenology scores never promote … ").
- It does not imply that Factor E is supported. Not falsified is not established, and the failed search is single-fixture.
- It does not imply that Factor E is refuted. A small substitution drop is "NOT proof that effort information is absent" (VERDICT `message_if_not_met`). C-Eng1-A-01 gives no certificate of absence.
- It does not imply that S2a is unneeded, mis-ordered, or blocked. No ladder edge is a gate (D-Prin-2-001), and the claim never constrained order (claim H6).
- It does not imply anything about hardware transfer.
- It does not imply that UP placement supports the claim. UP corresponds to dedicated effort sensing downstream of the nuisance, which premise 5 excludes; claim scope says such plants "satisfy the role trivially". UP is a **positive control** for the test, not evidence for necessity.

---

## 3. Proposed B.9.6 amendments to C-P1-012 (for the Astra claim adjudicator)

**Counter status.** Prin-1 Astra summary accepted the Prin-1 premise tightening as **event #1**. `claims/C-P1-012/upgrade-log.md` still shows "Accepted narrowings: 0 (1 proposed, pending)". The record maintainer should reconcile this (see §7). Every amendment below is labelled by whether it **counts** toward B.9.6. My design goal is to repair the falsifier and test **without** spending a narrowing. Event #2 would leave the claim one step from mandatory retirement review.

### A-1 — Identifiability-restricted match rule (falsifier repair; **does not count**, since it narrows no scope and adds no premise)

Replace "matches on every class with d ≥ 10 ms" with the following. A **counterexample cell** matches the reference realized-at-R1 cell on every class in the **identifiable set** `𝓘`. A class is in `𝓘` iff (i) ORACLE meets `TPR_L ≥ q_id` at the registered r_w, **and** (ii) the reference cell has `TPR_hat ≥ 0.5` (or another value pre-registered in the PLAN). If `|𝓘| < 3`, the search is **inconclusive**, not a non-counterexample.

- *Why:* the current rule lets two failing detectors count as a match. That biases the search toward false counterexamples in weak fixtures, and toward meaningless non-counterexamples when floor cells are excluded ad hoc.
- *Falsifier of the amendment itself:* if, on a re-run, `𝓘` agrees with the post-hoc "identifiable" sets now in VERDICT (DOWN: d20M10, d50M5, d50M10), the rule adds nothing new and is purely a clarification. If it disagrees, the adjudicator should prefer the pre-registered rule.

### A-2 — Latency term defined on censored data (falsifier repair; **does not count**)

Replace `Δp95 ≤ 10 ms` with Δ of the **restricted-mean detection latency up to d** (or Kaplan–Meier p50), computed only on `𝓘`. Undetected events are censored at `d`.

- *Why:* p95 = inf whenever TPR < 0.95, so the current term is undefined in most cells.
- *Falsifier:* if the restricted-mean statistic and p95 disagree in sign on any class where both are finite, report both and adjudicate on TPR only.

### A-3 — Factor R contrast must decouple rate from observer bandwidth (falsifier repair; **does not count**)

A Factor R counterexample/non-counterexample is admissible only from a design with **both** (a) fixed gain·T (current) **and** (b) per-cell optimizing tuning, applied identically, or matched continuous bandwidth where the discretization is stable. Factor R is "not falsified" only if (b) also fails to match. If (a) and (b) disagree, Factor R is **unadjudicated** on that fixture.

- *Basis:* METRICS caveat, claim H2. **[needs artifact: sensitivity_fixedgain.json]**. If that file already contains a decoupled variant, the adjudicator can rule on it now.
- *Falsifier:* R2 with optimized tuning matches R1 on all of `𝓘`. This **is** the Factor R falsifier, now well-posed.

### A-4 — Restate Factor E by measurement point, and add a model-compensation cell to the search (clarification + search strengthening; **counts as event #2 only if the adjudicator judges the restatement narrower**; my argument is that it is not)

Current: "an effort signal measured downstream of the command (realized actuator effort)".
Proposed: "an effort signal whose measurement point lies **downstream of the dominant unmodeled effect** in the contact class (equivalently, a channel in which that effect is observable). 'Realized' vs 'commanded' is replaced by the declared measurement point relative to each declared nuisance (premise 2)."

- *Why not a narrowing:* premise 2 already requires the placement to be declared, and the Grade-2 role already reads "an effort-information channel that cannot be reconstructed from upper-layer commands". A-4 states what "cannot be reconstructed" requires physically. Spike I-3 shows that the label "realized" does not guarantee it.
- *Search strengthening (not narrowing):* add a cell **CMD + identified nominal friction model** (identified on disjoint data, structure-matched to premise 2's declared effects). If it matches REAL_UP on `𝓘`, Factor E reduces to "the effect was unmodeled". That would be a **retire-nominate signal for Factor E as a role**: the "role" would then be "model your actuators", which any competent design already does. This is the most dangerous counterexample to Factor E, and the current search does not try it.
- *Falsifier of A-4:* any channel whose measurement point is upstream of the dominant nuisance still produces a substitution drop above the registered margin. That would mean the measurement point is not the operative variable, and A-4 is wrong.

### A-5 — Explicit non-amendment: keep UP / dedicated-sensor placement **out** of C-P1-012 scope (no change; **does not count**)

The Eng-1 decision lists "whether UPSTREAM torque-sensor placement should enter C-P1-012 scope" as an option. I recommend **no**. Premise 5 excludes dedicated effort/contact sensing because it satisfies the role trivially. Bringing UP into scope would let a privileged-by-construction channel (the H3 failure mode, reintroduced) count as support. UP results are filed as the B.9.3 test's **positive control** only.

- *Falsifier of this stance:* if the target plant is declared (premise-match evidence) to carry joint-side effort sensing, C-P1-012 is **out of premise for the target plant** and should be scoped as such. That is a B.9.4(b) premise-failure note, not a widening.

### Summary of counter impact

If A-1, A-2, A-3 and A-5 are accepted, the counter stays at 1. If the adjudicator rules A-4 a narrowing, the counter goes to 2. In that case I ask the adjudicator to log explicitly that **one more narrowing triggers mandatory retirement review** (B.9.6), and to treat a CMD + friction-model match (A-4 cell) as the decisive next event.

---

## 4. Related claims: touched only where the spike touches them

| Claim | Spike contact | Proposed action |
|---|---|---|
| **C-Eng1-A-01** (G1 narrow lemma, Candidate) | H2 NULL coverage passed. The NULL-control sanity check behaves as the lemma predicts. FAIL cells produce small `d_cert`, which the lemma correctly does **not** read as absence. | **No state change, no counter event.** One premise-3 audit item for the adjudicator: windows are "pooled 3 seeds". Confirm that windows within a seed do not share episode or detector state (i.i.d. premise). If they do, the certificates are void under the claim's own B.9.4(b) clause, but the lemma is not refuted. |
| **C-P1-011** (DPI ceiling, narrow) | CMD_RECON uses command history as its channel. This is consistent with C-P1-012 H8 (if command history is available, only Factor E's nuisance argument survives). | **No action.** Nothing in the data bears on the DPI invariant. |
| **C-P1-002** (timely body response) | None. The spike measured detection, not response. | **No action.** |

---

## 5. Eng-2 recommendation: gates before ranking (B.9.5)

### 5.1 Gates (applied first; pass/fail per candidate)

| Gate | Statement | B (S0a envelope, amended) | Amended-A as **engineering** retry | Amended-A as **Principle counterexample search** |
|---|---|---|---|---|
| G-1 | No Grade-3 edge or ladder order used as necessity (B.8.3; D-Prin-2-001) | pass, provided it lists bypassed edges | pass | pass |
| G-2 | No Candidate claim used as veto/gate (B.4) | pass, provided it does not cite C-P1-001/002 as gates | pass, provided C-Eng1-A-01 is cited as a design lemma only | pass |
| G-3 | Spike FAIL not cited as necessity or transfer evidence (B.8.4, B.9.8) | pass, provided its motivation does not read "A failed, so S0a must come first" | pass | pass |
| G-4 | Acceptance thresholds are task-stated, not spike placeholders (C-P1-012 H5; C-Eng1-A-01 non-claims) | **conditional**: B's envelope thresholds must be declared as placeholders, or ratified | **FAIL** until the human lead ratifies `(q, r)`. Re-running against placeholders cannot discriminate between "channel insufficient" and "thresholds infeasible" (UP itself gets 0/12 under Bonferroni). | n/a, because the falsifier uses relative match, not absolute `(q, r)` |
| G-5 | Target-plant premise declared where the result depends on it | **conditional**: plant mode set declared | **FAIL** until the target plant's effort measurement point relative to the dominant nuisance is declared. Otherwise the DOWN/UP choice is arbitrary. | pass, since both placements run as declared variants |
| G-6 | No post-hoc threshold or scope change to flip a filed verdict | pass | at risk, so it needs a sealed PLAN v3 with A-1 to A-4 written **before** any run | pass if sealed |
| G-7 | Eng-1 decision instruction: B "do not run as frozen; amend first" | **conditional**: amendments are required before any B spike | n/a | n/a |

**Gate result.** B is **ELIGIBLE (conditional on G-4/G-5/G-7 amendments)**. Amended-A as an engineering retry is **INELIGIBLE now** (G-4, G-5). Amended-A as a Principle counterexample search is **ELIGIBLE**.

### 5.2 Ranking (among eligible only)

| Rank | Candidate | Role | Rationale |
|---|---|---|---|
| **Recommend** | **B: S0a finite-horizon envelope, amended** | Eng-2 mainline | This follows the Eng-1 Alternate rule. The A FAIL does not make B more *necessary*; it makes B the remaining eligible engineering candidate. B's own amendments are required before its spike (G-7). D-P1-001 stays Provisional acceptance-gate, **not** necessity order. |
| **Alternate** (parallel, low cost, Principle track) | **C-P1-012 counterexample search v3** (PLAN with A-1 to A-4: identifiable-set rule, censored latency, bandwidth-decoupled R cell, CMD + friction-model cell, two placements) | Experiment under §12.2 and B.9.8; runner files data only | This is the cheapest high-information next step for the claim. It is sim-only and numpy-only on the existing fixture. It is **not** an Eng-2 deliverable and gates nothing in Eng-2. |
| **Reject** | (a) Amended-A engineering retry with thresholds relaxed or classes dropped post hoc. (b) Bringing UP placement into C-P1-012 scope to read UP results as support. (c) Citing the FAIL as evidence that the S2a contact floor is unnecessary or mis-ordered. (d) "Neither": pausing engineering has no Principle basis, since no Locked claim blocks B. | — | G-3 / G-6 violations, or no basis. |

**Answer to the packet's option list:** **B**, with the amended-A content moved to the Principle track (not "sequenced" engineering). A later engineering S2a-XC retry becomes eligible once G-4 and G-5 clear. At that point it competes as a normal Eng-n candidate.

### 5.3 Mandatory amendments to carry into the Eng-2 decision

1. Eng-2 B proposal lists bypassed edges and grades (B.8.5). It does not cite D-P1-001 as necessity.
2. Eng-2 B PLAN states its envelope thresholds as placeholders unless ratified.
3. C-P1-012 v3 search PLAN is sealed (sha256) before the run and includes A-1 to A-4. The runner changes no claim state.
4. Human lead: ratify the `(q_c, r_c)` task table, and declare the target plant's effort measurement point(s) relative to the dominant actuator nuisances. These two items unblock any future engineering S2a retry.

---

## 6. Non-claims

- I claim no grade change for any claim. No Locked Grade-1 is asserted or recommended. No signature is implied.
- I do not claim that C-P1-012 is supported, refuted, or closer to lock. I-1 is one weak failed search.
- I do not claim that motor-current sensing is useless. It added 0.06 to 0.16 TPR over command reconstruction on DOWN.
- I do not claim that S0a precedes S2a in any necessary sense. D-P1-001 is Provisional acceptance-gate. D-Prin-2-001 says no ladder edge gates Eng-1 or Eng-2.
- I do not claim that any result transfers to hardware or to the target plant.
- I do not claim that the A-4 restatement is correct. It carries its own falsifier.
- Reading of Factor R is withheld pending the sensitivity artifact.

---

## 7. Risk of over-reading the FAIL

| Over-reading | Why it is wrong | Guard |
|---|---|---|
| "FAIL means the contact-observability floor is unachievable from proprioception." | ORACLE meets 9/12. The fixture can identify d ≥ 10 contacts. The FAIL is channel-, detector- and threshold-specific. | Cite ORACLE in every read-back. |
| "FAIL means C-P1-012 should be downgraded or retired." | No falsifier fired. B.9.8 forbids state changes from spikes. Retirement needs falsification or B.9.6 count 3. | Adjudicator rules only on the A-1 to A-5 amendments. |
| "No counterexample means C-P1-012 is now supported." | Single fixture, single detector family. The falsifier was degenerate in floor cells (I-4). The model-compensation counterexample was never tried. | Log as partial failed search only. |
| "UP passed, so add torque sensing and S2a is solved." | UP is privileged by construction and out of premise 5. It is a positive control, not a design result for the target plant. | A-5. |
| "FAIL means do S0a first, by necessity." | Planning order is not evidence (B.8.3). B is recommended by elimination and the Alternate rule, not by necessity. | G-3 in the Eng-2 decision text. |
| "FAIL against `(q, r)` means XC-0 is insufficient for home tasks." | `(q, r)` is PLACEHOLDER. Even the privileged channel fails Bonferroni q0.90. | G-4. No engineering retry until ratified. |
| Retry A with loosened thresholds until it passes. | This is threshold-shopping. A PASS would still be harness-only. | G-6, sealed PLAN v3. |

**Bookkeeping for the record maintainer** (I do not edit claim files): reconcile the `claims/C-P1-012/upgrade-log.md` counter with the Prin-1 Astra ruling (event #1 accepted). Append the Eng-1 S2a-XC run as a failed counterexample search row, with the caveats I-4 and I-5. Add **no** row to `violations.md`, because no in-premise counterexample was found.

## 8. Claim IDs needing adjudicator follow-up

- **C-P1-012** (Astra): rule on A-1 to A-5, decide whether A-4 counts as a B.9.6 event, reconcile the counter, and register the v3 search PLAN.
- **C-Eng1-A-01** (Astra): premise-3 i.i.d. audit of pooled-seed windows. No state change requested.
- C-P1-011, C-P1-002: none.
