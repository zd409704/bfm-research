# Eng-2 — Proposal A: contract first, then a ceiling-referenced discriminator ("detector or channel?")

Author A (Claude Opus). Proposed/provisional. The spike is **deferred-runnable** under the D-Prin-3-001 common hard gate. No experiment results are asserted.

Inherit by ID, without paraphrasing their conclusions: D-P1-001 (Provisional acceptance-gate, not necessity order); D-Prin-1-001; D-Prin-2-001 (no ladder edge gates); D-Eng-1-001 (Closed — Recommend A spike FAIL; harness valid; A02 unmet); X-Eng-1-001; D-Prin-3-001 (Recommend B conditional sequence, with mandatory amendments); X-P1-001…004.

## Thesis

Eng-1's FAIL tells us that **this detector** (GMO + CUSUM, as frozen) on **this channel** (DOWN realized effort at R1) misses `(q, r)` on d10/d20. It does not tell us **which of the two is responsible**. Every next step depends on that answer:
- a detector retry is wasted if the channel cannot carry the information;
- an envelope packet (amended B) does not address the miss at all;
- a contract revision (measurement point, contact classes) is the right lever exactly when the channel is the limit.

Proposal A therefore makes the Eng-2 mainline a two-stage sequence. Stage 2 is gated on Stage 1.

1. **Stage 1: Contract XC-1 (executable now, document-only).** A task/channel contract that carries the open human-lead items as typed, versioned fields: `(q, r)` status, effort measurement point, contact classes, window definition, side channels, nuisance prior and placement declaration. It also carries a **symmetric eligibility table** for amended-A and amended-B.
2. **Stage 2: S2a-CEIL spike (deferred-runnable).** On the *unchanged* Eng-1 fixture, it adds two genie references, a full-genie Neyman–Pearson ceiling and a nuisance-marginal reference, plus a preregistered best-in-family detector. Each primary DOWN cell is classified as `CH_LIMIT` / `NUISANCE_LIMIT` / `DET_GAP_*` / `UNRESOLVED`. This is the **channel-level upper reference that can fail informatively** that D-Prin-3-001 requires of amended A. A `CH_LIMIT` result is a fixture-scoped certificate that *no* detector on that channel meets `(q, r)` (C-Eng2-A-01). A detector failure alone could never show that (C-Eng1-A-01 "no certificate of absence").

**Labeling (mandatory amendment).** Running an amended-A discriminator before amended B is a **proposed override** of D-Eng-1-001's automatic Alternate-B routing after A FAIL. It is a planning choice pending the human lead, not a necessity order.

**Cost of delaying B, stated.** Delaying amended B postpones evidence on actuator authority, transition semantics and envelope ownership/versioning by one packet. Those questions are orthogonal to the contact-detection miss. The delay is small for three reasons: S2a-CEIL is CPU-minutes on an existing fixture; D-Eng-1-001 judged the B spike low-information as frozen, and Prin-3 requires the amended-B contract to be specified before B is executable, so B cannot run immediately anyway; and Stage 1 specifies the B contract skeleton in parallel (below). If the human lead has an independently specified envelope question now, B may run in parallel. Nothing in A blocks it.

**Distinctness.** This is neither "retry A with a better detector" (rejected by Prin-3 as threshold-loosening or class-selecting) nor "move to S0a envelope". The S2a-CEIL output decides *which of those, if either*, is next, and it does so with a sealed routing table.

## Necessity vs sufficiency

B.9.5 is applied before ranking. No claim in scope is Locked. **No Prin-2 ladder edge is an Eng-2 gate (D-Prin-2-001).** No Candidate is used as a veto. Eng-1 FAIL is sufficiency-level data only. It is not a downgrade of any claim, not a hardware-transfer result, and not evidence about S0a necessity.

| Claim | Grade / state (authoritative) | Use here | Limitation |
|---|---|---|---|
| C-P1-001 | G1 narrow scalar; Candidate, conditional recommended-for-lock | Not used by S2a-CEIL. Cited only in the amended-B skeleton as the latency–feasibility separation. | Scalar fixture only; no coupled transfer. |
| C-P1-002 | G2 Candidate, tighten-premises | Amended-B skeleton: total-corrective-force inventory. | No incompatible-history proof for any richer fixture. |
| C-P1-003 | G3, quarantined | None. | No gate or order. |
| C-P1-010 | G1 formal (A) / conditional (B); Candidate | Not used. | Single-joint only. |
| C-P1-011 | G1 narrow DPI; Candidate | Justifies including side channels W in every detector tier, and treating genie info as *extra* information. | Side-channel audit still open. |
| C-P1-012 | **G2 Candidate** (downgraded from G1 label) | Secondary cells (R1_CMD_DOWN, R1_REAL_UP) produce **data** on Factor E / placement for its adjudicator. | UP stays outside premise-5 scope. No B.9.6 event is self-assigned. FAIL ≠ effort info absent. |
| C-Eng1-A-01 | G1 narrow lemma; Candidate, no gate | Floor test (lower side), unchanged. | Pooled-window independence premise under audit (Prin-3 follow-up). S2a-CEIL uses one fresh episode per window. |
| **C-Eng2-A-01 (new)** | **G1 narrow lemma; Candidate**, no gate | Ceiling test (upper side). Basis of the `CH_LIMIT` class. | Probability model of the fixture only. The G-marg reading is valid only under the declared nuisance prior. |

Sufficiency read: a `DET_GAP_FAMILY` result shows that a specific detector configuration suffices *on the fixture*. A `CH_LIMIT` result is an impossibility *for the fixture model*. Neither says anything about the target plant until the measurement point and nuisance model are matched to it.

## Interface contracts

**XC-1 (Stage 1; versioned; sha256 per version).** Fields marked † are owned by the human lead. Every other field is owned as listed.

| Field | Owner | Content / rule |
|---|---|---|
| `qr_status` † | Human lead | `RATIFIED(q_c, r_c per class)` or `PLACEHOLDER_POLICY(text)`. Eng-1 values are carried as `PLACEHOLDER`. Fixture work is allowed on placeholders. **Task acceptance or transfer readings require RATIFIED.** |
| `measurement_point` † | Human lead / target-plant owner | Where effort is sensed relative to each declared actuator nuisance (upstream / downstream per effect), per C-P1-012 premise 2. Blocks spike execution while unset. |
| `contact_classes` | Task owner (human-ratified) | Duration × magnitude × location grid. Primary classes are fixed per version. Changing them is a version bump, never an in-run choice. |
| `window_def`, `false_event_unit` | Body-loop owner | Per-window FPR with i.i.d. windows (one episode per window). Aligned with C-P1-012 registered units per Eng-1 amendment 1. |
| `side_channels W` | Body-loop owner | Enumerated, including command/efference history (C-P1-011 premise 3). |
| `nuisance_prior` | Fixture owner | Declared distribution of actuator nuisance parameters. Required for G-marg. Version-hashed. |
| `export_fields` | Body-loop owner | Realized effort, commanded effort, (q, q̇), timestamps, observation age. Logging must not perturb control (non-interference). |
| `scene_publisher view` | Scene publisher | Read-only: contact event + certificate ID + cell class + scope + expiry. Stale or missing becomes `UNKNOWN`, never "no contact". |
| `decision_core view` | Decision core | Consumes scoped detection validity only. A request outside the certified classes returns `OUT_OF_SCOPE`. |

**Symmetric eligibility table (Prin-3 amendment).**

| Branch | Fixture work on placeholders | Task-acceptance reading | Executable when |
|---|---|---|---|
| Amended A (S2a-CEIL) | Allowed | Needs `qr_status = RATIFIED` and `measurement_point` set | The common hard gate is cleared, *and* the PLAN is resealed with gate values |
| Amended B (S0a envelope) | Allowed | Needs a ratified envelope (state set, disturbance set, horizon, authority) | The common hard gate is cleared, *and* the B contract skeleton below is filled by the envelope owner with an **independently specified** question |
| Neither | — | — | Gate not cleared, or both branches fail eligibility. Contract-only stance holds. |

No Candidate claim vetoes either branch.

**Amended-B contract skeleton (specified, not run).** It is specified here so that B can be called executable when it is elevated.
- *Modes:* ≥ 2 declared support/contact modes plus a reset map, carrying actuator and delayed-state memory across resets.
- *Pass:* a checked finite-horizon reachable tube inside the envelope for one fixed-mode cell and one transition cell at the same delay.
- *Fail:* a verified in-set trajectory outside a certified tube (it falsifies that certificate implementation).
- *Unresolved:* explicit, never reported as unsafe.
- *Ownership:* the envelope owner (sets, horizon), the body-loop owner (controller, timing), and certificate producer/checker paths kept separate.
- *Forbidden rescues:* shrinking disturbance, removing transitions, raising effort.

**Spike ownership.** Experiment runner (Sonnet) executes the sealed PLAN only. The genie tiers (G-full, G-marg) are evaluator-side objects, never deployable exports. Their inputs are logged and confined (PLAN H6).

## Claims table

| ID | Statement / scope | Evidence / falsifier | State, grade |
|---|---|---|---|
| **C-Eng2-A-01** | One-sided channel ceiling: if the genie NP test on `(X,W,G)` has `TPR_U(t*) < q` at a threshold with `FPR_L(t*) ≥ r`, then no detector on `(X,W)` meets `(q,r)` on that probability model (conf. 1 − α). File: `claims/C-Eng2-A-01/claim.md`. | Formal error in the NP/monotonicity/CP steps. Voided (not refuted) by a likelihood mismatch to the simulator or non-i.i.d. windows. | **Candidate; Grade 1 narrow lemma**; adjudicator Astra; no gate |
| C-Eng2-A-02 | Engineering: S2a-CEIL classifies ≥ 2 of 3 primary DOWN cells as non-`UNRESOLVED` at the PLAN sample sizes (`E-INFO`). | `E-INFO` false falsifies the design's informativeness at this n. | Candidate, untested; sufficiency, grade N/A |
| C-Eng2-A-03 | Contract: XC-1's typed `qr_status` / `measurement_point` fields, plus the scope/expiry semantics in the scene-publisher view, prevent a placeholder-based result from being consumed as task acceptance. | A mutation test in which a PLACEHOLDER-tagged certificate is accepted by the decision-core view fails the contract. | Candidate, untested; contract, grade N/A |

C-Eng2-A-02 and C-Eng2-A-03 are engineering hypotheses and have no separate claim directories. Any future necessity claim needs its own claim.md, upgrade-log.md and violations.md, plus cross-family adjudication.

## Minimal spike PLAN (sealable; deferred-runnable)

Full preregistration: **`packets/Eng-2/drafts/A/PLAN.md`**, sealed by `PLAN.sha256`. Summary:
- **Fixture:** the Eng-1 S2a-XC fixture, bound by PLAN v2 sha256 `3d7b9af6…`, without modification. Primary cells are `R1_REAL_DOWN × {d10, d20, d50}_M10`. Secondary cells (informational only) are `R1_REAL_UP` and `R1_CMD_DOWN`.
- **Tiers:** D0 (Eng-1 detector, frozen); D1 (24-configuration GMO/CUSUM family, selected on a disjoint split); G-marg (template genie, nuisance marginalized by quadrature); G-full (full-genie LR, analytic `d'` plus MC check).
- **Statistics:** one episode per window; disjoint hashed seed sets; n₁ = 600 and n₀ = 30 000 per evaluation cell; CP α = 0.05. The floor test comes from C-Eng1-A-01 and the ceiling test from C-Eng2-A-01.
- **Harness criteria H1–H7:** reproduction of Eng-1 tpr_L (else INVALID), analytic/MC agreement, NULL control, tier ordering, quadrature convergence, no leakage, non-interference.
- **Sealed routing table:** a limit class on d10/d20 means no amended-A detector retry at these `(q,r)`, and routes to a contract revision or to amended B. `DET_GAP_FAMILY` means an amended-A detector packet is eligible. `E-INFO` false means neither.
- **Budget:** CPU/numpy, ≤ 30 min, ≤ 2 GiB. **PASS = harness only.** No hardware transfer. No claim grade change.
- **Gate:** do not execute until the human lead ratifies `(q,r)` (or a placeholder policy) and declares the measurement point. If ratified values differ from the Eng-1 values, they apply to all cells, and the Eng-1 values are reported as a secondary column.

## Failure modes

| Risk | Mitigation |
|---|---|
| The genie likelihood does not match the simulator, so the "ceiling" is not an upper bound | H2 (analytic vs MC), H4 (no practical detector beats G-full beyond CI), and the H3 NULL control. A mismatch voids `CH_LIMIT`; it does not refute the lemma. |
| G-full is too optimistic, so it never fires and the result is uninformative | G-marg provides the intermediate tier. `E-INFO` is an explicit, preregistered informativeness test. Its failure is reported, not hidden. |
| The nuisance prior is mis-declared, so G-marg is misleading | G-marg is read only under that prior and versioned in XC-1. Limit claims rely on G-full. |
| D1 selection turns into class or threshold shopping | Selection is done on a disjoint split. Primary classes are fixed. `(q,r)` is fixed before data. PLAN §9 lists forbidden moves. |
| Fixture drift since Eng-1 | H1 reproduction is a hard gate (INVALID). Fixture file hashes are recorded. |
| `CH_LIMIT` is read as "effort information is absent on the robot" | Scope text in the claim and the VERDICT. Hardware needs a matched measurement point and nuisance model. |
| UP results are imported as C-P1-012 support | Secondary, informational only. A B.9.6 amendment is the adjudicator's call and is not proposed here. |
| Delaying B loses envelope evidence | Cost is stated above. The B skeleton is specified now. A parallel B run is allowed if the human lead specifies an envelope question. |
| The gate never clears | Stage 1 still delivers XC-1 and the eligibility table. The spike stays sealed and deferred, and the decision stays provisional. |

## Non-claims

- No Locked claim and no recommended-for-lock nomination.
- No necessity order: neither S2a before S0a nor the reverse.
- No reading of Eng-1 FAIL as a claim downgrade, a hardware-transfer failure, or S0a necessity.
- No claim that realized-effort export is necessary, or that DOWN placement is "the operative variable". Every result carries the qualifier "this fixture, detector set and calibration".
- No threshold loosening or class selection.
- No hardware or comparative-performance claim.
- No assertion about the other author's proposal (not read).

## Bypassed Grade-3 edges

B.8.5 inventory. Bypass dispositions follow the Eng-1 VERDICT and the Prin-2 edge set. None of these edges gates research, and harness PASS refutes none of them.

| Edge IDs | Grade-3 reading | Disposition in S2a-CEIL |
|---|---|---|
| C-Prin2-E05 / E06 (S0a → S2a) | Ordering prerequisite | **Bypassed.** S2a work proceeds without an S0a certificate on the fixture. |
| C-Prin2-E08 / E09 (S1 → S2a) | Ordering prerequisite | **Bypassed.** No S1 policy. |
| C-Prin2-E14 (S0b → S2a) | Reflex/impedance prerequisite | **Bypassed.** No S0b tier. |
| C-Prin2-E10 / E11 (S2a → S1) | Forward edge | Listed, not bypassed. S1 not pursued. |
| C-Prin2-E17 (S2a → S2) | Acquisition reading Grade 3 | Not invoked. C-Eng2-A-01 uses NP/side-information monotonicity, not E17 as a gate. |
| C-Prin2-E01–E04, E07, E12, E13, E15, E19 | Various G3 readings | Destinations not exercised. No prerequisite imposed. |
| (Amended-B branch, if elevated) | — | Would traverse no S1/S2a/S2 destination. Its bypass set is empty, per the Eng-1 B inventory. |

Citation ablation: no biological citation is load-bearing anywhere in this proposal.

**Provenance:** brief.md; roster.md; packets/Eng-2/source/*; packets/Prin-3/decision.md (identical to source copy); claims/C-P1-*/claim.md; claims/C-Eng1-A-01/claim.md. Disclosure: a directory listing exposed the first lines of `packets/Eng-2/logs/*`, which contain Author B's *task prompt* only. No Author B draft or proposal content was read.
