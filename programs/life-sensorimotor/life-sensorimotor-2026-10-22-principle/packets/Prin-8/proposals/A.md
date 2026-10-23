# Proposal A — Packet Prin-8: target premise-match templates for C-P1-002 and C-P1-010

**Author:** Competing Author A (Claude Opus, medium). Isolated draft tree `drafts/A/`. B's draft was not seen.
**Claims covered (inherited by ID):**
- **C-P1-002** (timely body-response role). Author family Astra. Grade 2, Candidate, tighten-premises.
- **C-P1-010** (sampled-data passivity bound and fast-tier corollary). Author family Opus. Part A Grade 1 narrow, Part B Grade 1 conditional. Candidate, tighten-premises.

**Routing basis:** D-Prin-4-001 priority 5 ("C-P1-002 / C-P1-010 target premise-match templates until measurement point declared"). D-Prin-3-001 and D-Eng-2-001 are unchanged.
**Packet scope:** this packet delivers **templates only**. It runs no measurement, spike or counterexample search, fills no template with target-plant values, and moves no grade or state. It adds no Eng-2 gate or precondition and proposes no Locked Grade-1. It names no products or companies, and it mandates no sensor type, numeric rate, controller family or research order.

**Family note (disclosed).** C-P1-010 is Opus-authored, the same family as this author. This proposal therefore does not interpret C-P1-010's premises beyond the claim text. Every interpretive choice is marked **[A-choice]** so the Astra claim adjudicator can accept or strike it.

---

## 1. Thesis

The two claims share a gap. Each has a well-formed conditional argument, and neither has a **target premise match**: a record showing that the target plant satisfies the claim's stated premises. (Sources: C-P1-002 Scope, "not the missing target-plant premise match"; C-P1-010 H3, "Part B has no force on any route".) A match needs values that can only come from a declared measurement point. That point does not exist yet, so the work that can be done now is structural:

1. **Fix what must be matched** before any number is seen. That means every premise, every field, its source class and its pass/fail/out-of-scope rule.
2. **Fix how a template may be filled before the measurement point** (Phase 0) and how it is frozen and filled after (Phase 1). Then pre-point specification work cannot pass for measurement, and post-point results cannot quietly rewrite the premises.
3. **Route every outcome** to the claim adjudicator under B.9.4 / B.9.6. A filled template is evidence about premises. It never states a transition by itself.

The main risk is not missing data. It is **template-shaped circularity**: filling `K_req,j` from controller gains, inferring C-P1-002's incompatible-history condition from a controller failing, treating instrumentation gaps as role absence, or reading an out-of-scope result (extra delay, nonlinear friction, multi-DoF coupling) as a counterexample. Each template has explicit circularity guards for these.

## 2. Shared template machinery

### 2.1 Field status vocabulary (both claims)

Every field carries exactly one status. Statuses only move forward, except that a later version may supersede an earlier one by append; nothing is overwritten.

| Status | Meaning | Allowed in Phase 0? |
|---|---|---|
| `UNDECLARED` | No value; owner not assigned. | Yes (default) |
| `OWNED` | An owner role and source class are assigned; no value. | Yes |
| `SPECIFIED` | A value or bound is declared from an independent source (task requirement, design document, analysis), with provenance. **Not measured.** | Yes |
| `DERIVED` | Computed from other fields by a stated, checkable procedure. Inherits the weakest status among its inputs. | Yes (inherits) |
| `MEASURED` | Obtained at the declared measurement point under a sealed procedure, with an uncertainty bound and resolution. | **No** |
| `NOT-APPLICABLE` | The field does not apply because a scope exclusion has fired (§2.4). Must cite which exclusion fired. | Yes |
| `CONTESTED` | Two sources disagree or circularity has been flagged; adjudicator must rule. | Yes |

A premise-match row may say **MATCH** only if every field it depends on is `MEASURED`, or `SPECIFIED` where the claim premise itself is a declaration (for example a task requirement, an envelope or a disturbance set). The claim text decides which premises are declarations and which are physical facts (§3.2, §4.2).

### 2.2 Phases

- **Phase 0 (now, until the human lead declares a measurement point).** Templates may be instantiated per joint and per support mode. Fields may reach `OWNED`, `SPECIFIED`, `DERIVED`, `NOT-APPLICABLE` or `CONTESTED`. A row's match verdict may only be `PENDING`, `SCOPE-EXIT` (an exclusion fired, so the claim does not apply to this row) or `CIRCULARITY-FLAG`. **No row may say MATCH or FAIL in Phase 0.** A Phase-0 instance is a planning artifact. It is not evidence for or against either claim, and it is not an Eng-2 input.
- **Measurement-point declaration (human lead).** This is an external event, not part of this packet. It names the plant build or configuration, the support modes in scope, the joint list and the clock or timestamp authority. When it is recorded, each Phase-0 instance is **version-frozen** (content hash plus timestamp, appended to the template log). The frozen version becomes the premise-match **PLAN**. Changes after freezing are new versions and count under §2.5.
- **Phase 1 (after declaration).** `MEASURED` fields are filled under the frozen PLAN by the experiment runner. Row verdicts become `MATCH`, `FAIL`, `SCOPE-EXIT`, `UNESTABLISHED` (instrument resolution is insufficient) or `CONTESTED`. The runner files results and does not change claim state (B.9.8). Execution needs its own packet, which this proposal does not open.

### 2.3 Instance header (both claims)

```
claim_id:            C-P1-002 | C-P1-010
claim_record_hash:   <sha256 of claim.md version matched against>
template_version:    A-v1 (this proposal) + amendments
instance_id:         <claim>/<plant-config>/<support-mode>/<joint-or-mode>
phase:               0 | 1
measurement_point:   UNDECLARED | <declaration record ref>
envelope_owner:      UNDECLARED | <role, not person-name inference>
approval_path:       UNDECLARED | <version path>
filler_role:         <role>; must not be the claim adjudicator for this claim
adjudicator_binding: <per roster: Opus for C-P1-002; Astra for C-P1-010>
b96_counter_at_open: <current accepted B.9.6 count for this claim>
```

The `envelope_owner` and `approval_path` fields come from C-P1-002's P1 hygiene ("envelope owner, approval/version path and support-mode scope remain required"). They are carried in both templates because C-P1-010 Part B's `K_req,j` also needs an owner who is independent of the controller.

### 2.4 Scope-exit discipline

Each claim lists explicit exclusions. When an exclusion fires for a row, the verdict is `SCOPE-EXIT`. A scope exit:
- is **not** a counterexample (B.9.4a requires the claim's stated premises);
- is **not** a B.9.6 narrowing (the scope already excluded it);
- **is** recorded, because a pattern of scope exits on every contact-critical joint is decision-relevant. It shows the claim cannot bear on the target plant as stated. The adjudicator may then consider a separate claim. This template never drafts one.

### 2.5 B.9.6 hooks

Any of the following, proposed in order to keep a row from `FAIL`, is a **candidate narrowing event** and is logged with the row:
- adding a premise not in the claim text;
- shrinking the disturbance set, envelope, joint list or support-mode list after values are seen;
- changing tolerances or resolution after values are seen;
- reclassifying a `FAIL` row as `SCOPE-EXIT` by citing an exclusion that was not marked at freeze.

The template only logs these. Whether one counts toward the B.9.6 total is decided by the claim adjudicator. Pre-freeze edits to Phase-0 content are not narrowing events, because no value has been seen yet.

### 2.6 Shared-clock and cross-claim note [A-choice]

Both claims need time-stamped signals: C-P1-002 needs disturbance, state and total-force histories on a common clock, and C-P1-010 needs the sampling period `T` and any added delay. When the measurement point is declared, **one clock-authority field** should be shared by instances of both claims for the same plant configuration. This is a bookkeeping convenience only. The two claims are **not merged**, neither claim's premises are imported into the other, and a C-P1-010 result never discharges a C-P1-002 premise or the reverse.

---

## 3. Template T-002 — C-P1-002 target premise match

### 3.1 Unit of instantiation

One instance per **(plant configuration, support mode, disturbance pair)**. C-P1-002 premise 1 forbids pooling support modes without justification. A pooling justification, if offered, is a separate `SPECIFIED` field with provenance and is flagged `CONTESTED` by default.

### 3.2 Premise-match table

| Row | Premise (claim text, by number) | Fields | Declaration or physical fact? | MATCH rule (Phase 1) | FAIL / other |
|---|---|---|---|---|---|
| **P2-1a** | P1 plant model | plant model ref; model-validity range; parameter uncertainty | Physical fact (model must be validated) | Model validated against measured responses within the declared uncertainty over the declared envelope | `FAIL` if residual exceeds the declared uncertainty; `UNESTABLISHED` if validation data are absent |
| **P2-1b** | P1 initial-state set, body envelope | set definitions; envelope owner; version | **Declaration** | `SPECIFIED` with owner + approval path is sufficient | `CONTESTED` if the envelope is derived from an existing controller's achieved performance (circularity G-2) |
| **P2-1c** | P1 disturbance set | disturbance classes; magnitude, onset-time and duration bounds; off-grid onset included | **Declaration** | `SPECIFIED` with provenance from task/household requirements | `CONTESTED` if defined as "what the current controller survives" (G-2) |
| **P2-1d** | P1 actuator authority | torque/force limits per joint; rate limits; thermal limits over horizon | Physical fact | `MEASURED` within stated uncertainty | `FAIL` if below the authority assumed in P2-3 |
| **P2-1e** | P1 observation/actuation channels | channel list; per-channel latency, rate, resolution | Physical fact | `MEASURED` | — |
| **P2-1f** | P1 support-mode certification choice | per-mode vs pooled; justification | Declaration | `SPECIFIED` | pooled without justification → `CONTESTED` |
| **P2-2** | P2 feasibility of the envelope | an existence witness: *some* allowed mechanism keeps the envelope under all declared disturbances | Physical fact, by analysis or demonstration | A reachability/feasibility argument over the validated model (P2-1a) **or** a demonstrated realization; either counts | If infeasible, the claim's application to this instance is withdrawn (premise fails). Not a counterexample. Faster response is **not** a remedy (claim P2) |
| **P2-3** | P3 incompatible disturbance pair and deadline `T` | pair `(w₁, w₂)`; matched initial condition; `T`; safe total-force-history sets `S₁`, `S₂`; disjointness argument; computation method | Physical fact, **from dynamics/reachability** | Disjointness of `S₁` and `S₂` on `[0, T]` established by an argument independent of any controller's failure, checked by a non-author | `FAIL` if a common safe history exists (then the claim's target application is withdrawn, per its Falsifier). `CIRCULARITY-FLAG` if the only support is that some controller failed (G-1) |
| **P2-4** | P4 total corrective force accounting | list of every force source: active feedback, embedded feedback, passive restoring/dissipative; exogenous disturbance excluded; measurement or estimation route for each | Physical fact | Every source is enumerated, with an instrument or a validated estimator, and passive contributions are included in `S₁` and `S₂` | `FAIL` if fixed passive mechanics alone admit a common safe history (claim P4 last sentence). `UNESTABLISHED` if a source cannot be measured or bounded |
| **P2-5a** | P5 all timely force-variation sources included | inventory of sources available before the deadline: active, embedded, distributed, passive | Physical fact | Inventory complete; each source has a test route | A missing source is `UNESTABLISHED`, not absence |
| **P2-5b** | P5 upper-layer interruption | Is interruption in the declared disturbance/resource envelope? If yes: interruption profile | Declaration (whether), then physical fact (availability during it) | If declared: availability of the force-variation sources during interruption is `MEASURED` | If not declared: `NOT-APPLICABLE`. **No universal stall premise may be imported** (claim P5) |

### 3.3 Realization / absence fields (carried, not executed)

These follow C-P1-002's "Operational realization and absence test" and are needed so a later Phase-1 PLAN cannot leave them open. All must be `SPECIFIED` at freeze:

| Field | Content | Guard |
|---|---|---|
| `Δ_req` | required force-history separation between worlds within `[0, T]` (from P2-3) | Must come from the disjointness argument, not from observed traces |
| `ε_F`, `δ_t` | force measurement error and temporal resolution | **Resolution rule:** if `ε_F` or `δ_t` cannot resolve `Δ_req` within the response window, the instance verdict is `UNESTABLISHED`. It is never "role absent" (claim: "missing force instrumentation makes realization unestablished, not proven absent") |
| `t_diff` | time by which differentiation must appear | ≤ the deadline from P2-3 |
| intervention list | replay / channel interventions removing the proposed differentiating response; recorded premise changes | An intervention that changes plant/envelope is logged as a **premise change**, not as an absence result |
| realization classes | passive-only; existing embedded-control; active controller | All three **must be listed** and tested with equal seriousness (claim text). Omitting passive-only is `CONTESTED` |
| counterexample criterion | envelope success with total corrective histories indistinguishable within `ε_F`, `δ_t` across the window, under matched premises | Predeclared; any success while the role is demonstrably absent goes to the adjudicator as a candidate B.9.4(a) counterexample |

### 3.4 Circularity guards (T-002)

- **G-1 (incompatibility from failure).** P2-3 may not cite a controller's failure as evidence of disjointness. Failure traces may motivate *which* pair to analyze. They are never support for disjointness.
- **G-2 (envelope from capability).** The envelope and disturbance set may not be defined as what an existing implementation achieves. Then any realization would match trivially and no role could be tested as absent.
- **G-3 (success as realization).** Envelope success alone never fills a realization field (claim: "successful behavior alone does not identify a hidden role").
- **G-4 (evolution).** No field may be filled from evolutionary or anatomical sources (claim citation-ablation; B.8.7). Such a citation in a provenance column makes the field `CONTESTED`.
- **G-5 (fixture transfer).** The C-P1-001 scalar fixture and the reported scalar-harness PASS may not fill any P2-* row. They are a one-instance example, not a target match (C-P1-002 Scope; D-P1-001).

### 3.5 Instance-level outcomes and routing

| Outcome | Condition | Route (to Opus claim adjudicator) | Claim effect claimed by this template |
|---|---|---|---|
| All rows MATCH | Phase 1 only | Supports "target premise match established for this instance" | None. Grade-2 lock still needs the cross-implementation argument, a logged failed counterexample search and the human signature (B.9.2) |
| P2-2 or P2-3 or P2-4 FAIL | Premise fails on target | B.9.4(b) premise-failure evidence for this instance; claim Falsifier says withdraw the **target application** | None decided here |
| Any row UNESTABLISHED | Insufficient instrument/validation | Stays open; names missing instrument | None |
| CIRCULARITY-FLAG | G-1..G-5 | Adjudicator rules before any further fill | None |
| Candidate counterexample | §3.3 criterion met under matched premises | B.9.4(a) admission request | None |

---

## 4. Template T-010 — C-P1-010 target premise match

### 4.1 Unit of instantiation

One instance per **(plant configuration, joint `j`, rendering loop)**. "Rendering loop" means the loop that actually renders virtual stiffness at that joint, with its own period. A joint rendered by more than one loop gets one instance per loop. Part A and Part B are separate sub-tables. A Part-B row may only be evaluated when the Part-A rows that apply to the same instance are `MATCH`, or when the adjudicator accepts a documented reason to proceed.

### 4.2 Part A premise-match table (premises 1–5)

Part A is a formal bound. Its target premise match asks one question: **does this joint/loop fall inside the bound's class?** It does not test the theorem. The claim's own Falsifier says an in-premise violation challenges the premise mapping, not the theorem.

| Row | Premise | Fields | MATCH rule | Otherwise |
|---|---|---|---|---|
| **P10-A1a** | P1 single DoF | coupling to other joints at the frequencies of interest: reflected inertia ratio, cross-coupling bound | Cross-coupling below a threshold that is **declared at freeze** with its justification [A-choice: the claim gives no threshold, so the adjudicator must accept the threshold or strike the row] | `SCOPE-EXIT` (multi-DoF exclusion) |
| **P10-A1b** | P1 LTI virtual impedance `F = −Kx − Bẋ_d`, backward-difference velocity | control-law form at this loop; velocity estimator form | Law reduces to the stated class over the operating range | `SCOPE-EXIT` (learned/nonlinear policy outputting torque directly; or a different velocity estimator, which is outside the cited result) |
| **P10-A2a** | P2 ZOH at period `T`, position sampled at same period | `T`; hold type; sampling alignment | `MEASURED` `T`; ZOH confirmed | `SCOPE-EXIT` if hold or sampling differ |
| **P10-A2b** | P2 no delay beyond the ZOH sample | measured compute, transport, filter delay `d_x` | `d_x` ≤ a negligibility bound **declared at freeze** [A-choice] | `SCOPE-EXIT` (delay exclusion). Any delay-extended bound is a **separate claim needing its own source** (claim Scope). This template does not draft it |
| **P10-A2c** | P2 position quantization ignored | encoder resolution; effect on rendered K at the stiffness of interest | Quantization effect below a declared bound [A-choice] | `SCOPE-EXIT` |
| **P10-A3** | P3 linear viscous `b`, continuous-time, in parallel | measured friction curve over the velocity range; Coulomb/Stribeck/backlash magnitude; load and temperature dependence | Residual after linear-viscous fit within declared tolerance over the operating envelope | `SCOPE-EXIT` (nonlinear friction or varying `b`) |
| **P10-A4** | P4 environment passive, otherwise unknown | which environments are in scope (human contact, objects, supports) | **Declaration**: the requirement is stated as passivity against unknown passive environments | If the requirement is stability for a *known* environment, `NOT-APPLICABLE` (claim H2, premise 5) |
| **P10-A5** | P5 passivity of the device port is the property demanded | Requirement source; owner | **Declaration** with an owner independent of the controller | If the requirement is not passivity, `NOT-APPLICABLE`. This is not a failure of the claim |

### 4.3 Part B premise-match table (premises 6–8)

| Row | Premise | Fields | MATCH rule | Otherwise |
|---|---|---|---|---|
| **P10-B6** | P6 measured `b_j` reflected at the joint, including actuator/gear damping | `b_j`; uncertainty; method; velocity range; reflected-through-transmission flag | `MEASURED` with uncertainty; same identification as P10-A3 | `UNESTABLISHED` until measured. If P10-A3 is `SCOPE-EXIT`, P10-B6 is `NOT-APPLICABLE` |
| **P10-B7** | P7 `K_req,j` stated independently of any implementation | `K_req,j`; task derivation (task → required stiffness); owner; version | `SPECIFIED` from a task requirement with a derivation a non-author can check | `CIRCULARITY-FLAG` if it comes from an existing controller's gains, tuning or achieved performance (claim H3; guard G-6) |
| **P10-B8** | P8 stiffness is virtual; physical compliance outside | Physical compliance present at `j` (series elastic, structural); its stiffness `K_phys,j` | Required stiffness at `j` is assigned to the virtual loop | If physical compliance supplies or shares `K_req,j`, the row is B.9.4(b) premise-failure evidence (claim Falsifier, Part B). It is **not** a counterexample |
| **P10-B9** | Policy-rate period `T_R2` | measured `T_R2` at the loop that would otherwise render `K_req,j` | `MEASURED` | — |
| **P10-B-cmp** | Comparison | `2 b_j / T_R2` vs `K_req,j`, with **propagated uncertainty** | `DERIVED` from B6, B7, B9 | Three-valued: `K_req,j` above the interval, so the corollary applies to `j`; below the interval, so the **Part B retire trigger** for `j` (claim Falsifier); overlapping the interval, so `UNRESOLVED`. The comparison band is declared at freeze |

### 4.4 Circularity and transfer guards (T-010)

- **G-6 (gain circularity).** `K_req,j` may not be read from existing gains, autotuning outputs or the stiffness at which a current controller "works". It must be traced to a task quantity (for example, allowed deflection under a stated load) by a derivation recorded in the row.
- **G-7 (generalization stretch, H1).** No row, verdict or summary may restate Part A as "any ~50 Hz-rendered architecture is soft or non-passive". A `SCOPE-EXIT` on A1a, A1b, A2b, A2c or A3 means the claim **says nothing** about that joint/loop.
- **G-8 (false dichotomy, H2).** "Stable but not passive" is an admissible design outcome, recorded as `NOT-APPLICABLE` under A4/A5 when the requirement is restricted-environment stability.
- **G-9 (sanity spike is not a match).** SA-1 or its frequency-domain replacement checks the harness and the premise mapping. Its results fill no T-010 field (claim Falsifier; B.4/B.5).
- **G-10 (ordering, H5).** No T-010 outcome may be cited as S0-before-S1 ordering evidence, as an S0a necessity or as an Eng-2 gate. D-P1-001 stays Provisional.

### 4.5 Outcomes and routing (to Astra claim adjudicator)

| Outcome | Effect requested | Claim effect claimed here |
|---|---|---|
| Part A rows all MATCH for `(j, loop)` | Record "Part A in-class at `(j, loop)`" in a premise-match note | None. Part A lock path stays the B.9.2 published-result item match plus the human signature (C-P1-010 Recommended action), batched with the C-P1-001 dossier if the human lead chooses (D-Prin-4-001). A target match is **not** a substitute for the proof check |
| Any Part A SCOPE-EXIT | Record, with the exclusion fired | None. Not a counterexample, not a narrowing |
| Part B corollary applies to `j` | Candidate evidence that a faster loop or physical compliance must supply the passive guarantee at `j` | None. Candidate cannot veto (B.4). It mandates no rate, tier or ordering |
| Part B retire trigger for `j` | Request per-joint retirement ruling for Part B at `j` | None decided here |
| P10-B8 physical compliance present | B.9.4(b) premise-failure evidence for Part B at `j` | None decided here |
| UNRESOLVED / UNESTABLISHED | Names the measurement that would resolve it | None |

---

## 5. What a Phase-0 instance can be useful for, and what it cannot

**Useful now (planning only, B.8.3):**
- Assigning owners for the envelope, disturbance set, `K_req,j` and the passivity requirement. These are the declaration-type premises. They need human or task-owner input and are the longest-lead items.
- Listing joints where the C-P1-010 Part A exclusions are **already known** to fire from design information (for example, a known learned torque policy, or known extra delay). Those can be pre-marked `SCOPE-EXIT` at `SPECIFIED` status. That lets the measurement point be scoped to joints where a match is possible.
- Drafting the P2-3 disjointness analysis on a model, marked `DERIVED` from `SPECIFIED` model inputs. The analysis is useful, but it **cannot reach MATCH** until P2-1a is validated.
- Telling the human lead what the measurement point must cover: support modes, joints, clock authority and force-instrumentation resolution against `Δ_req`.

**Not usable for:**
- any claim-state or grade change;
- any Eng-2 gate, precondition or ranking input (D-Prin-3-001 unchanged);
- any statement that either claim "holds on the target plant";
- any S0a/S0b/S1/S2 ordering argument.

## 6. Stop rules for template use

1. If the human lead has not declared a measurement point, no instance may leave Phase 0.
2. If a template amendment is proposed after freeze and before Phase-1 results, it is a new version and is logged under §2.5. Results are reported against the version frozen at declaration.
3. If any `CIRCULARITY-FLAG` is open on an instance, no further rows on that instance are filled until the adjudicator rules.
4. If C-P1-002's or C-P1-010's `claim.md` is amended by its adjudicator, existing instances keep their `claim_record_hash`. A new instance is opened against the new hash. Old instances are not silently re-pointed.
5. If cumulative accepted B.9.6 events on either claim reach the threshold (default 3), template filling for that claim pauses pending the retirement review B.9.6 requires.

## 7. Residual risks and known weaknesses of this proposal

- **[A-choice] thresholds.** T-010 rows A1a, A2b and A2c need negligibility thresholds that the claim does not supply. I chose to make them declare-at-freeze fields rather than invent numbers. The adjudicator may prefer to strike these rows and treat any non-zero coupling, delay or quantization as `SCOPE-EXIT`. That is stricter, and it is probably fatal to Part B's applicability on a real humanoid joint. I flag it; I do not resolve it.
- **Measurability of total corrective force (T-002 P2-4).** Passive and embedded contributions may not be directly measurable on a home-humanoid plant. Then the realistic Phase-1 outcome for C-P1-002 is `UNESTABLISHED`, not MATCH. The template makes that outcome explicit instead of hiding it.
- **Disjointness computation cost (P2-3).** Computing reachable safe-force-history sets for a full humanoid may be intractable. The template allows a reduced-model argument only if the reduction is validated within P2-1a's uncertainty. Otherwise the row stays `UNESTABLISHED`.
- **Same-family authorship on C-P1-010.** Disclosed above. The Astra adjudicator should treat my Part A row decomposition as a proposal, not a reading.
- **Template proliferation.** Instances multiply as joints × loops × support modes × pairs. Phase-0 pre-scoping (§5) is meant to keep the Phase-1 set small. Its effectiveness is unproven.

## 8. Requested decisions (for packet adjudicator)

1. Adopt the field-status vocabulary and Phase 0 / declaration / Phase 1 split (§2.1–2.2) for both claims.
2. Adopt T-002 (§3) and T-010 (§4) as the premise-match templates pending measurement-point declaration, with guards G-1..G-10.
3. Route [A-choice] items (§2.6, P10-A1a, A2b, A2c) to the respective claim adjudicators: Opus for C-P1-002, Astra for C-P1-010.
4. Confirm that nothing in this packet changes grades, states, D-P1-001, D-Prin-3-001 or D-Eng-2-001.

Grades: C-P1-002 Grade 2 **Candidate**; C-P1-010 Part A Grade 1 **Candidate**, Part B Grade 1 conditional **Candidate**. Unchanged.
