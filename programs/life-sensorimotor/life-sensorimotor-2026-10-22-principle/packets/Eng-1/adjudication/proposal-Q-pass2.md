# Eng-1 — Proposal A (Author A, Claude Opus)

**Recommend (primary scope):** **S2a-XC — the contact-observability floor, delivered as a certified body-loop export contract (`XC-0`) with a one-sided divergence certificate.** It runs decoupled from the S0a acceptance gate and does not use any ladder edge as a gate.

**Alternate:** merged contract (S0a envelope + S2a export on one fixture), deferred until XC-0 has a filed certificate.
**Reject as primary:** S0a envelope certification on a richer plant. Reasons are in §1.3.

Inherited by ID: D-P1-001 (Provisional), D-Prin-1-001, D-Prin-2-001, C-P1-001/002/003/010/011/012, C-Prin2-E01..E19, X-P1-001..004. No claim cited here is Locked. All are Candidate.

---

## 1. Thesis

### 1.1 What the packet builds

The packet builds one interface and one acceptance test.

- **Interface `XC-0`.** This is a versioned schema for what the body loop (fast tier) exports to everything above it (policy tier, scene publication, decision core). Each field carries its rate, its effort-source tag (commanded-reconstructed or realized-measured) and its sensor-placement declaration. A separate **side-channel register `W`** lists every contact-correlated signal that reaches upper layers by a route other than `XC-0`, such as command history and efference copies.
- **Acceptance test: the floor certificate.** For a task-stated contact class `c` and task-stated detection requirement `(q_c, r_c)`, an export *meets the S2a floor* when a held-out detector run gives a one-sided confidence bound `TPR_L ≥ q_c` and `FPR_U ≤ r_c`. By C-Eng1-A-01, which is a corollary of the C-Prin2-E17 step-1 data-processing inequality, this certifies `D(P₁ ‖ P₀) ≥ d(q_c ‖ r_c)` on the declared channel at the stated confidence. That is a certificate that information is **present**. It is never a certificate that information is absent.

### 1.2 Why this scope first (planning reasons, not necessity)

1. **It turns Candidate Principle claims into measurable contracts without leaning on them as locks.** C-P1-011 (Grade 1, Candidate) says upper layers cannot exceed what `(X, W)` carries. C-Prin2-E17 Reading A (Grade 1 conditional, Candidate) gives the floor's form, `d(q‖r)`. C-P1-012 (Grade 2, Candidate, downgraded) names the open factorial over rate and effort source. XC-0 is the smallest artifact that makes all three testable on a fixture. None of them is used here as a veto.
2. **It repairs the confound that downgraded C-P1-012.** The factorial in the spike PLAN separates Factor R (rate) from Factor E (effort source), re-tunes the detector per rate (fixing H2) and declares friction placement (fixing H3). This is the registered counterexample search for C-P1-012, so the packet produces claim evidence as well as an engineering baseline.
3. **It is cheap and reversible.** The export is read-only with respect to the control law. Widening it later is a schema version bump (C-P1-011 H3). The spike is CPU/numpy only.
4. **It does not compete with D-P1-001.** The S0a acceptance gate keeps running as P1 left it. XC-0 adds only a non-interference check: the control trajectory is identical with the export on or off.

### 1.3 Why not S0a richer-plant certification as primary

- C-P1-001 is a scalar fixture result, and C-P1-002's target-plant premises 1 and 3 (the plant model and a *verified incompatible disturbance pair*) are not available. A richer plant would need a target dynamics and disturbance envelope that nobody has supplied. Without them the work is a phenomenology bake-off, and it cannot move C-P1-002.
- D-P1-001 is already the acceptance gate. Making its certification the mainline would let planning order pose as necessity (B.8.3). C-Prin2-E02/E04/E06 are quarantined.
- It carries more evidence demand (a richer plant, a disturbance set) and less claim leverage than XC-0.

### 1.4 Why the merged contract is only the Alternate

Merging S0a and S2a was P1's move, and it rested on the confounded C-P1-012 (H6). A merged packet before XC-0 is certified would put the two-factor confound back in. Once XC-0 has a filed certificate, a merged fixture becomes a cheap integration step.

---

## 2. Necessity vs sufficiency

| Input | Grade / state | How this proposal uses it | What it is NOT used for |
|---|---|---|---|
| C-P1-011 DPI ceiling | G1 narrow, Candidate (tighten) | **Design input:** motivates the side-channel register `W` and the rule that upper-layer performance never exceeds the `(X, W)` channel | Not a gate. Not an ordering. Not an export-sufficiency claim |
| C-Prin2-E17 Reading A | G1 conditional, Candidate (tighten; not recommended-for-lock; zero-FPR caveat open) | **Design input:** the form of the floor `d(q‖r)` and the KL-DPI step that C-Eng1-A-01 rests on. The `r = 0` case is excluded (premise `r_c > 0`) | Reading P (S2a before S2) is Grade 3 and quarantined. Not used |
| C-P1-012 | **G2 Candidate (downgraded)** | **Experimental target:** the spike *is* its registered factorial counterexample search plus the B.9.3 substitution test | **Not** Grade-1 necessity for the export. XC-0 does *not* mandate realized effort or R1. Both are fields whose necessity the spike tests |
| C-Prin2-E10 TV kernel | G3 edge; kernel author-checked, not B.9.2 | Diagnostic idea only (an optimal-classifier error bound) | Not an S2a→S1 gate |
| C-P1-010 Part A/B | G1 / G1 conditional, Candidate | Out of scope. XC-0 renders no impedance | — |
| C-P1-001 / C-P1-002 | G1 narrow / G2, Candidate | S0a acceptance gate stays as is (D-P1-001) | Not a precondition for XC-0 |
| C-P1-003 | G3 quarantined | Not used | — |
| D-P1-001 | Provisional acceptance gate | Coexists. Non-interference check only | **Not** a necessity order |

**Sufficiency outputs of this packet:** certificates on a named fixture with named classes. Every positive result is sufficiency evidence for *that export, detector, fixture and class* (B.5, B.8.4). No result changes any grade. Under B.9.8 the runner files data. The claim adjudicator rules.

---

## 3. Interface contracts (generic names only)

### 3.1 Ownership

| Owner | Owns | Must not |
|---|---|---|
| **Body loop (fast tier)** | Control law, sampling, the `XC-0` publisher, sensor-placement declarations | Change the control law depending on whether the export is on (non-interference) |
| **Export bus** | `XC-0` schema versioning, timestamps, rate decimation | Silently filter or resample without a declared processing step (C-P1-011 premise 5) |
| **Policy tier / scene publication / decision core** | Consuming `XC-0` and declaring every `W` input | Use a contact-correlated input that is not in `W` (audit failure) |
| **Human lead** | The `(q_c, r_c)` table per contact class (task-stated) | — |
| **Experiment runner** | Running the sealed PLAN and filing `verdict.json` | Change thresholds, classes or claim state |

### 3.2 `XC-0` schema (v0)

```
XC-0 frame (one per export tick)
  t_body          : body-clock timestamp [s]
  rate_tag        : {R2≈50Hz, R1≈200Hz, R0≈1kHz}
  q, qdot         : joint position / velocity (declared filter, if any)
  effort          : per-joint effort [N·m]
  effort_src      : {CMD_RECON (command + nominal law), REALIZED_CURRENT, REALIZED_OUTPUT_TORQUE}
  friction_place  : {DOWNSTREAM_OF_SENSOR, UPSTREAM_OF_SENSOR}   (C-P1-012 premise 2 / H3)
  residual?       : optional fast-tier observer residual + observer gain·T
  schema_version  : "XC-0"
Side-channel register W (per consumer)
  list of {signal, rate, Z-correlated? (Y/N/unknown), derived-from-XC-0? (Y/N)}
```

### 3.3 Contact-class table (task-stated; placeholder until the human lead ratifies)

| Field | Meaning |
|---|---|
| `c` | class id |
| `d` | contact duration [ms] |
| `‖J_cᵀF‖` or `‖F‖` | magnitude band |
| location | link / segment band; **non-support** contacts only |
| window `W_Z` | decision window for `Z` |
| `(q_c, r_c)` | TPR floor, per-window FPR ceiling; requires `r_c > 0` |
| latency p95 ceiling | optional |

The **placeholder grid** used by the spike is `q ∈ {0.90, 0.95}`, `r ∈ {0.01, 0.05}` per 100 ms window. It is marked PLACEHOLDER. Certificates computed against it are provisional and must not be cited as task requirements (C-P1-012 H5).

### 3.4 Certificate format (`floor-cert.json`)

```
{ "schema":"XC-0", "cell":{rate, effort_src, friction_place}, "class":c,
  "detector":{family, gain_T, threshold_calibration_split},
  "n_pos":…, "n_neg":…, "TPR_hat":…, "FPR_hat":…,
  "TPR_L":…, "FPR_U":…, "alpha_joint":0.05,
  "d_cert_bits": d(TPR_L‖FPR_U) if TPR_L>FPR_U else 0,
  "meets":{ "(q,r)":bool, … }, "W_declared":[…], "placeholder_qr":true }
```

`meets = true` certifies information present on the declared `(X, W)`. `meets = false` certifies nothing about absence (C-P1-011 scope: "estimation quality").

---

## 4. Claims table

| ID | Type | Grade | State | Statement (short) | Record |
|---|---|---|---|---|---|
| **C-Eng1-A-01** | Formal lemma (invariant; acceptance-test soundness) | G1 narrow, author derivation | Candidate | Any detector with held-out one-sided bounds `TPR_L > FPR_U` at joint confidence `1−α`, on i.i.d. windows, certifies `D(P₁^{X,W} ‖ P₀^{X,W}) ≥ d(TPR_L ‖ FPR_U)` with confidence ≥ `1−α`. One-sided: it never certifies absence | `claims/C-Eng1-A-01/` |
| C-Eng1-A-02 | Engineering sufficiency hypothesis | — (not a necessity claim) | Hypothesis | On the planar 2-link fixture, `XC-0` at R1 with realized effort meets the placeholder floor for classes `d ≥ 10 ms` | No claim dir (sufficiency only; filed via the spike) |
| C-Eng1-A-03 | Engineering contract property | — | Hypothesis | The `XC-0` publisher is non-interfering: the body-loop trajectory is bitwise identical with the export on or off | No claim dir (harness check) |
| (C-P1-012) | Existing | G2 Candidate | — | The spike is its registered factorial plus the B.9.3 substitution test | Existing record; runner files data only |

New necessity-shaped claims: **one** (C-Eng1-A-01). I give it a record because the acceptance test's soundness depends on it. It adds nothing to the ladder.

---

## 5. Minimal spike PLAN (CPU-only; sealed)

Full text: `drafts/A/spike-PLAN.md`, sealed by sha256 in `drafts/A/spike-PLAN.sha256`. The Orchestrator copies it to `packets/Eng-1/spikes/<id>/PLAN.md` if the proposal is Recommended. It is deferred-runnable by the Sonnet experiment runner.

Summary:

- **Fixture.** Planar 2-link arm, horizontal plane, ground-truth simulation at 1 kHz. A PD controller tracks a band-limited self-motion reference. Non-support external force pulses act on link 2. Unmodeled actuator ripple and bias are added. Coulomb and viscous friction are placed at the joint output.
- **Factorial (8 cells).** Rate {R2 = 50 Hz, R1 = 200 Hz} × effort {CMD_RECON, REALIZED} × placement {DOWNSTREAM (current-derived), UPSTREAM (output-torque sensor)}. Plus a positive control (ORACLE: true external joint torque) and a negative control (zero contact force).
- **Detector.** A generalized-momentum observer at export rate with **gain·T fixed at 0.25** (H2 repair), followed by CUSUM. The threshold is calibrated on a contact-free calibration split to the target `r`, then frozen. Evaluation uses a disjoint held-out split.
- **Classes.** `d ∈ {5, 10, 20, 50} ms` × magnitude {2, 5, 10 N} × location band on link 2. One 100 ms decision window per episode, independent episodes. `n = 2000` positive and `2000` negative episodes per cell and class, 3 seeds.
- **Outputs.** `floor-cert.json` per cell and class. The C-P1-012 contrasts (ΔTPR, Δp95) use the registered criteria verbatim. The B.9.3 substitution test (REALIZED → CMD_RECON at fixed FPR; TPR drop margin 0.10). The non-interference check. `verdict.json`.
- **Harness PASS (all required).** H1: deterministic re-run gives identical verdicts. H2: the negative control never certifies (`d_cert = 0` for all cells). H3: the ORACLE positive control meets the strictest placeholder `(0.95, 0.01)` for `d ≥ 10 ms`, 10 N. H4: non-interference holds. **PASS validates the harness only. It is never evidence of hardware transfer and never moves a grade.**
- **Data, filed without state change.** Whether any non-realized or R2 cell matches realized-at-R1 under C-P1-012's registered counterexample criterion, and the per-cell certificates.
- **Budget.** Vectorized numpy, about 10⁸ step-evaluations, under 30 min on one CPU. No GPU, no network, no hardware.

---

## 6. Failure modes

| # | Failure | Effect | Mitigation |
|---|---|---|---|
| F1 | `(q, r)` taken from the spike rather than the task | The certificate becomes circular (C-P1-012 H5) | Placeholder flag. Human lead ratifies the table. Results stay provisional until then |
| F2 | Side-channel leak: CMD_RECON cells use the command, which is part of `W` | The "export-only" floor is misattributed | Every cell declares `W`. CMD_RECON is reported as a joint `(X, W)` channel. The C-Prin2-E17 caveat is applied |
| F3 | Friction placement privileges one effort source (C-P1-012 H3) | The conclusion is built in | Both placements are in the factorial |
| F4 | Detector under-tuned at R2 (H2) | A false Factor-R effect | gain·T held fixed. An optional sensitivity sweep is reported separately |
| F5 | Non-i.i.d. windows inflate confidence | The certificate overclaims | One window per independent episode. Clopper–Pearson bounds with Bonferroni correction across the two rates |
| F6 | Reading a failed certificate as absence of information | An illegitimate necessity inference | Hard rule in §3.4. A failure is only "not certified by this detector" |
| F7 | Fixture too simple (planar, rigid, no support contacts) | Transfer is overstated | Non-claims §7. A richer fixture only after the certificate is filed |
| F8 | Rare-event and zero-FPR issues in the floor (E17 caveat) | Infinite or unstable floors | `r_c > 0` is required. Report `n_neg` and the FPR upper bound explicitly |
| F9 | Planning order read as necessity | Breaks B.8.3 | §8 lists the bypassed edges. No edge is cited as a gate |

## 7. Non-claims

- No hardware transfer, no target-plant certification, no claim about any existing pretrained behavior model's latents (X-P1-002 stands).
- No claim that realized effort or R1 is *necessary*. That is C-P1-012's open question, and the spike only files data.
- No claim that S2a must precede S1, S2 or S0b, or follow S0a.
- No change to D-P1-001 (it stays Provisional and is not a necessity order).
- No Locked claim, no recommended-for-lock. C-Eng1-A-01 is Candidate.
- No claim about support/foot contacts, contact semantics, or plants with tactile skin or F/T sensors.
- A failed certificate is not evidence that information is absent.

## 8. Bypassed Grade-3 edges (B.8.5)

This packet works on S2a without first completing S0a, S0b or S1, and it builds no S2. Each bypass is allowed because no edge is Locked (D-Prin-2-001: Eng-1 gates from ladder edges are NONE).

| Edge | Claim(s) | Grade / state | Bypass |
|---|---|---|---|
| S0a → S2a | C-Prin2-E05, C-Prin2-E06 | G3 quarantined, Candidate | S2a proceeds without an S0a-order lock. The S0a gate runs in parallel (D-P1-001) |
| S1 → S2a | C-Prin2-E08, C-Prin2-E09 | G3 quarantined, Candidate | The self-motion reference is a fixed PD trajectory, not S1 competence |
| S0b → S2a | C-Prin2-E14 | G3 quarantined, Candidate | No impedance or reflex package is required. Direct-channel observation only |
| S2a → S1 | C-Prin2-E10, C-Prin2-E11 | G3 quarantined, Candidate | Not bypassed in the forward direction. Listed because XC-0 does *not* claim to gate S1 |
| S2a → S2 (Reading P) | C-Prin2-E17 Reading P | G3 quarantined | Not invoked as a reason for priority |
| S0-first evolutionary path | C-P1-003 | G3 quarantined | Not used |

Not bypassed (no S2 or S1 work is done here): E07, E13, E15, E19, E01/E02, E03/E04, E12.
