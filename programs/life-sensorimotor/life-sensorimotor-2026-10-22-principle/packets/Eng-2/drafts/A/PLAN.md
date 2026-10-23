# Eng-2 / Author A — Deferred-runnable spike PLAN: S2a-CEIL (channel-ceiling discriminator)

**Status:** DEFERRED-RUNNABLE. Execution is blocked by the D-Prin-3-001 common hard gate until the human lead (i) ratifies `(q, r)` or an explicit exploratory placeholder policy, and (ii) declares the target plant's effort measurement point. Sealing this PLAN does not authorize running it.
**Seal:** sha256 of this file goes in `PLAN.sha256` next to it. Any edit after sealing is a deviation and must be logged in `deviations.md` with the reason.
**Scope:** harness validity plus fixture-scoped data only. PASS = harness only. It never shows hardware transfer and never changes a claim grade (B.9.8).
**Compute:** CPU, numpy (plus scipy.stats for Clopper–Pearson if available; otherwise a numpy beta-quantile bisection). Budget 30 min wall-clock, 2 GiB. No GPU.

## 0. Question

Eng-1 S2a-XC FAIL (X-Eng-1-001): on the DOWN placement, `d10_M10` and `d20_M10` miss q0.90 at r = 0.001 (tpr_L ≈ 0.26 / 0.72). A02 unmet. The question this PLAN asks:

> For each primary DOWN cell, is the miss a **detector gap** (some detector on the same exported channel could meet `(q, r)`), a **nuisance limit** (the miss is due to unknown actuator-side effects that the channel cannot separate from contact), or a **channel limit** (no detector on that channel, even one given the nuisances, can meet `(q, r)`)?

This adds a **channel-level upper reference that can fail informatively**, as D-Prin-3-001 requires of amended A. It does not loosen thresholds, select classes, or change placement scope.

## 1. Fixture binding (no new physics)

- Reuse the Eng-1 S2a-XC fixture **as bound by PLAN v2 sha256 `3d7b9af6b08d8f1fe36e25c06780bcfca571969656669d9c6fbdd1c902e9ac41`**: the plant, friction placements (DOWN and UP), noise model, contact class generator, window definition, export fields and side channels W.
- The runner records the sha256 of every fixture source file reused. A fixture change of any kind is a deviation. The fixture is not "repaired" here.
- **Primary cells (fixed, not selectable):** `R1_REAL_DOWN` × `{d10_M10, d20_M10, d50_M10}` at `r = 0.001` per window, `q = 0.90`. These are the Eng-1 values and remain PLACEHOLDER until ratified. If the human lead ratifies different `(q, r)`, the run uses the ratified values for **all** cells, and the Eng-1 values are reported alongside as a secondary column. No other change is permitted.
- **Secondary cells (informational, never verdict-bearing):** the same classes on `R1_REAL_UP`, and on the commanded-reconstructed channel `R1_CMD_DOWN` (Factor E contrast). These are reported as data for the C-P1-012 claim adjudicator. UP stays outside C-P1-012 premise-5 scope unless a separate B.9.6 amendment is accepted; this PLAN does not propose one.

## 2. Detectors (three tiers per cell)

All tiers see the same simulated windows. Labels and evaluation truth go only to the scorer.

| Tier | What it sees | Role |
|---|---|---|
| **D0 — deployed** | Exported channel `(X, W)` only. The Eng-1 GMO + CUSUM detector, frozen as in PLAN v2. | Reproduces the Eng-1 result. |
| **D1 — best-in-family** | `(X, W)` only. Preregistered grid: observer gain·T ∈ {0.05, 0.1, 0.25, 0.5}, CUSUM drift ∈ {0.25, 0.5, 1.0}·σ̂, and window-max vs CUSUM statistic (24 configurations). Configuration and threshold are chosen on a **selection split** and scored on a disjoint **evaluation split**. | Measures detector headroom inside a realistic family. |
| **G-marg — nuisance-marginal reference** | `(X, W)` plus genie knowledge of contact onset, duration and location. Actuator nuisance parameters are **not** given; they are marginalized over the fixture's declared nuisance prior by a fixed quadrature grid (≥ 64 nodes per nuisance dimension, convergence check below). The statistic is the marginal likelihood ratio. | Estimates the most any detector can get when the contact template is known but the nuisance is not. |
| **G-full — full-genie ceiling** | `(X, W)` plus genie knowledge of contact onset, duration, location **and** the realized nuisance trajectory (friction state, actuator-side unmodeled torque). Statistic: exact log-likelihood ratio of contact vs no contact given everything else. Under the fixture's Gaussian measurement noise this is a matched filter on the innovations. Its power curve is computed **analytically** (deflection `d'`) and verified by Monte Carlo. | An upper reference on the power any detector of `(X, W)` can reach at FPR ≤ r. |

Ordering expected by construction (within CI): `G-full ≥ G-marg ≥ D1 ≥ D0` in TPR at matched FPR. A violation beyond CI is a harness bug (H4).

## 3. Statistics

- Windows are i.i.d.: a fresh episode per window, detector state reset per window (C-Eng1-A-01 premise 3). Seeds for the selection, calibration and evaluation splits are disjoint and hashed.
- Per cell: `n₁ = 600` contact windows in evaluation (+ 600 selection), and `n₀ = 30 000` null windows in evaluation (+ 30 000 calibration/selection). With zero false events, the Clopper–Pearson upper bound at α/2 = 0.025 is ≈ 1.2·10⁻⁴ < r.
- **Floor test (from C-Eng1-A-01, unchanged):** a detector meets `(q, r)` iff `TPR_L ≥ q` and `FPR_U ≤ r` at α = 0.05.
- **Ceiling test (C-Eng2-A-01):** for G-full, choose the threshold `t*` whose **lower** CP bound satisfies `FPR_L(t*) ≥ r`, so the true FPR at `t*` is ≥ r with probability ≥ 1 − α/2. Then `β*(r) ≤ TPR(t*) ≤ TPR_U(t*)` with joint probability ≥ 1 − α. Where the analytic power curve is available it is used as primary and MC as a check (H2). The channel is **ceiling-limited** at the cell iff `TPR_U(t*) < q`.
- The same ceiling test is applied to G-marg. Read it as "below q for any detector that does not know the nuisance realization but does know the contact template", **not** as a universal ceiling, because G-marg optimality holds only under the declared nuisance prior.
- No pooling across classes or placements. No multiplicity correction beyond the per-cell α. Three primary cells are reported individually.

## 4. Outcome classes per primary cell (sealed mapping)

| Class | Condition | Meaning (this fixture, detector set and calibration only) |
|---|---|---|
| `CH_LIMIT` | G-full ceiling test: `TPR_U(t*) < q` | No detector on `(X, W)` meets `(q, r)` on this fixture model, even with the nuisance and contact template known. |
| `NUISANCE_LIMIT` | G-full not ceiling-limited **and** G-marg ceiling-limited | The miss traces to unseparated actuator-side nuisance under the declared prior. Data for C-P1-012 Factor E / premise 2, routed to the claim adjudicator. |
| `DET_GAP_FAMILY` | G-marg meets the floor **and** D1 meets the floor **and** D0 does not | Detector tuning gap inside the existing family. |
| `DET_GAP_OPEN` | G-marg meets the floor **and** D1 does not | Headroom exists, but not inside the preregistered family. |
| `MET` | D0 meets the floor | Only possible if the ratified `(q, r)` differs from Eng-1 or the reproduction drifted (see H1). |
| `UNRESOLVED` | Anything else (CIs straddle q) | No conclusion. Not a failure of the channel, not a pass. |

## 5. Harness criteria (verdict = PASS iff all hold)

- **H1 — reproduction.** D0 on the three primary cells reproduces the Eng-1 `tpr_L` values within the 95% CI of the Eng-1 estimate. If it does not, the fixture binding has drifted: verdict INVALID, nothing else is read.
- **H2 — analytic/MC agreement.** For G-full, the analytic power at three thresholds lies inside the MC 99% CI on every primary cell.
- **H3 — null control.** With contact magnitude set to zero (`P₁ = P₀`), across 200 replicate small cells (n₁ = 200, n₀ = 2000), the floor test passes at frequency ≤ α + 0.02, and the G-full ceiling test fires at frequency ≥ 1 − α − 0.02 for any `q > r + 0.05`. Sized so that a correct harness cannot fail spuriously.
- **H4 — ordering.** `TPR(G-full) ≥ TPR(G-marg) − ε` and `TPR(G-marg) ≥ TPR(D1) − ε` at matched FPR on every cell, with ε = the half-width of the larger 95% CI.
- **H5 — quadrature convergence.** G-marg statistics computed with 64 and 128 nodes agree in AUC to ≤ 0.005 on every primary cell. If they do not, those cells' G-marg-dependent classes become `UNRESOLVED`; this is not a harness failure.
- **H6 — no leakage.** Split seed sets are pairwise disjoint (hash check). D0/D1 input provenance contains no evaluator truth. Genie inputs are confined to G-tiers and logged.
- **H7 — non-interference.** Turning export logging on or off leaves the control trajectory bitwise identical (as in Eng-1 amendment 6).

## 6. Engineering read-back criterion (does not decide the verdict)

`E-INFO`: at least two of the three primary DOWN cells are not `UNRESOLVED`. A harness PASS with `E-INFO` false means the discriminator was uninformative at this sample size. It is reported as such, and no branch decision follows from it.

## 7. Routing (sealed now, chosen by the human lead after the run)

| Primary-cell pattern | Recommended next engineering step (planning choice, not necessity) |
|---|---|
| any of d10/d20 is `CH_LIMIT` or `NUISANCE_LIMIT` | **No amended-A detector retry at these `(q, r)` on DOWN.** Route to (a) a contract revision by the human lead (measurement point, or the task contact classes), or (b) amended B (S0a envelope) if an independently specified envelope question exists. Never loosen `(q, r)` to rescue A. |
| d10 and d20 both `DET_GAP_FAMILY` | Amended-A detector packet eligible (Eng-3), using the D1 configuration resealed as a new frozen detector against a fresh evaluation seed set. |
| any `DET_GAP_OPEN`, none limit-class | Amended-A eligible only with a new preregistered detector family. Headroom is quantified by G-marg − D1. |
| `E-INFO` false | Neither branch is supported by this spike. Contract-only stance holds. |

## 8. Outputs

`packets/Eng-2/spikes/S2a-CEIL/{VERDICT.json, METRICS.md, results.json, ceilings.json, run.log, deviations.md, fixture-hashes.txt}`.

VERDICT.json fields: `verdict ∈ {PASS, FAIL, INVALID}` (FAIL = some H criterion false with H1 true), `H1..H7`, `cell_classes`, `E_INFO`, `qr_source ∈ {RATIFIED, PLACEHOLDER_POLICY}`, `measurement_point_declared`, `plan_sha256`, `bypassed_edges` (E05, E06, E08, E09, E14; listed not bypassed: E10, E11), `claim_grade_changes: "none"`, `scope: "harness validity + fixture-scoped data; no hardware transfer"`.

## 9. Forbidden moves (any one voids the run)

Changing `(q, r)` after seeing data. Dropping or adding primary classes. Tuning thresholds on evaluation windows. Treating UP results as in-scope C-P1-012 support. Treating `CH_LIMIT` as proof that effort information is absent on the target plant (it is a statement about this fixture model only). Treating any outcome as a C-P1-012 grade change or a ladder-edge result.
