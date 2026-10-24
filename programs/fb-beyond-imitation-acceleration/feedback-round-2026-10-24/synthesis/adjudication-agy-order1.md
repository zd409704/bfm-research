# Independent Cross-Family Adjudication — Order 1 (`feedback-round-2026-10-24`)

**Program**: `fb-beyond-imitation-acceleration`
**Presentation Order**: Order 1 (`Candidate P` = `drafts/A`; `Candidate Q` = `drafts/B`)
**Reviewed Artifacts**:
- Charter & Briefs: `PROGRAM_CHARTER.md`, `briefs/BRIEF.md`, `briefs/OWNER_FEEDBACK_EN.md`
- Candidate Packages: `anonymized/order1_P.md` (`drafts/A/*` 5-file inventory), `anonymized/order1_Q.md` (`drafts/B/*` 5-file inventory)
- Blind Reviews: `reviews/review-B-on-A.md` (critique on Candidate P), `reviews/review-A-on-B.md` (critique on Candidate Q)
**Evidentiary Rule**: Prior `B01`–`B05` script and accelerator `PASS` records are strictly local algebraic, numerical, or state-machine contract checks on synthetic distributions or simplified toy plants; none constitutes validation of the training framework.

---

## 1. Eligibility and Hard-Constraint Gate

| Gate Criterion | Candidate P (`drafts/A`) | Candidate Q (`drafts/B`) |
| :--- | :--- | :--- |
| **5-file deliverable inventory (`FRAMEWORK_REVIEW`, `GAP_TABLE`, `CORRECTED_CONCLUSIONS`, `MINIMAL_EXPERIMENTS`, `STATUS`)** | **PASS** — All five files present, substantive, and internally linked. | **PASS** — All five files present, substantive, and internally linked. |
| **Confinement to `/srv/claude` & no invented production code paths** | **PASS** — Cites local files only; marks production training/tests as planned external steps. | **PASS** — Cites local files only; marks production entrypoints as external items to resolve. |
| **English only; generic home-humanoid / plant-class terminology (zero brand names)** | **PASS** — Uses generic 29-DoF home-humanoid / plant-class terminology throughout. | **PASS** — Uses generic home-humanoid / plant-class terminology throughout. |
| **`B01`–`B05` script/accelerator `PASS` not claimed as framework validation** | **PASS** — Explicitly marks all empirical `(E)` cells empty (`None`) and `H1`–`H4` open. | **PASS** — Explicitly scopes prior `PASS` results to local script assertions only. |
| **Preserved body semantics (standard `B(m)` cues, 50/50 `z_update`, `F·z` readout; no bundled whitening/height-in-`B`/world-model)** | **PASS** — Preserves sealed `B01` sites (i)–(iii) and motion-only `B`; rejects bundled add-ons. | **PASS** — Preserves standard `B(m)` cues, 50/50 sampler, and `F·z`; rejects bundled add-ons. |
| **Charter §2.1 (no behavioral cloning or tracking fallback in framework)** | **PASS** — Tracking reward (`TR`) is isolated as an external comparator arm; `FW` stays pure. | **PASS** — Imitation prior (`A-I`) is isolated as an external comparator arm; `A-F` stays pure. |
| **Charter §2.4 (`severe_penetration` vs `invalid` numerical corruption)** | **CONDITIONAL PASS (Fix Required)** — Distinguishes concepts, but `MINIMAL_EXPERIMENTS` §0 auto-restarts `invalid` halts and excludes arms with `>2` halts instead of halting for fault inspection. | **PASS** — Requires pre-commit quarantine, state rollback verification, and retention of failed runs in cost/reliability accounting. |
| **Owner Deliverable 5 (external production plan: configs, identities, curves, costs)** | **PASS (Scale Fix Required)** — Includes relative cost units (`R`), manifests, and curves, but total step cap (`3.0B`–`8.22B` steps) exceeds small-scale bounds. | **CONDITIONAL PASS (Fix Required)** — Complete manifest/curve schema and transition caps, but omits order-of-magnitude accelerator-hour / wall-clock cost ranges. |

**Gate Verdict**: Both **Candidate P** and **Candidate Q** are **ELIGIBLE** for adjudication; neither commits a disqualifying violation, though both require mandatory pre-launch protocol repairs (§3).

---

## 2. Comparative Scoring (0–100)

| Dimension | Candidate P | Candidate Q | Brief Justification |
| :--- | :---: | :---: | :--- |
| **1. Framework-theory soundness** | **88** | **89** | **P** cleanly separates `(T)/(I)/(E)` across all five causal links, analyzes dynamic transit-frame occupancy (`m` containing velocity), identifies the time-based `100k`-step planner ramp as a cold-start deadlock hazard, and separates temporal coherence/macro-horizon from FB-specific mechanisms. However, **P** overstates finite 50/50 relabeling as training "every `z`" and drops equal-occupancy/indistinguishable-input (`U_t`) premises when stating `B03` contact impossibility in prose. **Q** states FB measure-density vs moment-consistency premises rigorously and contributes the convex-analysis insight that linear preference optimization (`F·z`) favors exposed extreme points of the achievable occupancy set rather than guaranteeing interior contact skills, though **Q** under-develops the temporal-correlation confounder and deterministic-planner exploration shrinkage. |
| **2. Implementation-gap honesty** | **85** | **91** | **Q** uses a rigorous four-tier epistemic taxonomy (`Observed` in local source / `Reported` by owner audit / `Specified` in contract / `Pending` external verification), explicitly audits the three data paths (forbidding offline motion cues from entering transition replay), and requires snapshot-diff immutability checks. **P** provides a detailed 21-row prioritized table (`P0`–`P2`) including run-identity and tuning-fairness gaps, but conflates owner-reported facts with unverified baseline contracts under a single `"Exists"` label and mis-prioritizes production batch-norm ordering as `P1`. |
| **3. B01-B05 claim re-scoping** | **94** | **86** | **P** conducts a comprehensive forensic re-slotting of every `B01`–`B05` artifact and every headline number in the ledger: exposing `B01`'s script-imposed spectrum (`17.23x`), `B03`'s tautological identical-tensor test (`0.0`) and `0.9105 > 0.5625` predictor error, and `B04`'s toy dimensions (`action=12, d_z=64`), 24-step whitened ground truth (which `H=32` overshoots), and `rel_l2 ≈ 0.95–1.23` across all arms. **Q** accurately derives `B03`'s `p^2 + 0.5625` bound and covers all owner table rows, but leaves `B01/B02/B04/B05` ledger numbers generic rather than individually re-scoped. |
| **4. Minimal-experiment design quality** | **78** | **83** | **Q** contributes a mandatory pre-efficacy Entry Integrity Gate (`≤10k` transitions + fixtures), a censor-proof primary endpoint (normalized success AUC in `[0,1]` with `T70` secondary), Charter-compliant fault accounting, and a clean causal design for `C` (offline body updates on a frozen common donor pool `C-use` vs `C-omit` transferred to disturbance recovery `V`). However, **Q**'s `1M` aggregate transition cap for `A` (~244 steps/env at 4,096 envs, alongside `24M` eval steps) is too small to clear its `79/100` competence gate (`A2`), and **Q** omits a correlated-noise baseline (`DA-C`). **P** includes `DA-C` and a cleaner `E2` exploration ablation, but suffers from a censoring flaw (`T70` median ratio collapses to `1.0` when seeds fail), biased `invalid`-arm exclusion, an unvalidated `E0` pose-distance kill gate, and a multi-billion-step budget. |
| **5. Investment judgment clarity** | **90** | **82** | **P** selects a single unambiguous owner category upfront (`revise-then-continue`), pairs it with an explicit table of decisive assumptions (`D1`–`D3`) and kill/fallback actions, and tabulates six simpler alternatives with fairness rules (marred only by treating a `0.67` step ratio as mechanism falsification). **Q**'s substantive reasoning is sound, but its headline string conflates three owner categories and scatters decisive assumptions in prose. |
| **Mean Score** | **87.0** | **86.2** | Virtual tie with strong complementarity: **P** leads on forensic `B01`–`B05` re-scoping, confounder controls (`DA-C`, `E2`), and decision clarity; **Q** leads on provenance hygiene, entry-gate verification, censor-proof statistics, and causal `C` isolation. |

---

## 3. Disposition, Mandatory Merge/Fix Items, and Confounds

- **Recommend**: **Tie/Hybrid (`Candidate P` primary review/ledger/controls base + `Candidate Q` entry-gate, AUC endpoint, and causal-`C` protocol)**. *(If a single unmerged package must be designated primary base prior to editing: **Recommend Candidate P**, **Alternate Candidate Q**).*
- **Alternate**: **Candidate Q** (supplies the mandatory experimental architecture for the Entry Integrity Gate, censor-proof AUC estimation, four-tier gap provenance, and common-donor `C` intervention).

### Mandatory Merge and Fix Items (from both blind reviews)

1. **[CRITICAL] MF-1 (Review on P `[CRITICAL] F1` & Review on Q `[CRITICAL] F1` — Viable Two-Stage Budget, Censor-Proof Endpoint & Power)**:
   - Replace P's right-censored `T70` median ratio (which collapses to `1.0` and triggers false refutation under non-attainment) and Q's under-powered `1M` aggregate transition cap with a **two-tier staged budget** (Stage 1: `15M` aggregate control transitions; Stage 2 extension to `100M` only if Stage 1 shows non-zero learning or controllability).
   - Use **Q's normalized trapezoidal success AUC** in `[0,1]` as the primary efficacy endpoint and censor-aware `T70` survival curves as co-primary/secondary; separate the relative efficiency gate (`A1`) from the `0.70` Wilson absolute competence gate (`A2`), freeze the best-`DA` comparator from pilots, and state minimum detectable AUC effects at 5 paired seeds (`t_{4, 0.975} = 3.495`).
2. **[CRITICAL] MF-2 (Review on P `[CRITICAL] F2` & Q Entry Gate — Production Entry Integrity Gate & Charter-Compliant Fault Protocol)**:
   - Adopt Q's pre-efficacy **Entry Integrity Gate** (`≤10k` transitions + fault fixtures verifying three-path data provenance, snapshot-level `behavior_z` and normalizer immutability, `1e-6` macro-return and `1e-5` RNN prefix parity, and R2.1 terminal priority latch).
   - Delete P's auto-restart and `>2`-halt arm-exclusion rule; halt for inspection on verified `invalid` corruption and retain all scheduled seeds and rollback/attempted steps in cost and reliability tables.
3. **[CRITICAL] MF-3 (Review on P `[CRITICAL] F3` — Scope `E0` Controllability Probe to Validated Constructs)**:
   - Freeze the `E0` kinematic distance metric (including velocity and upright survival alongside pose, reporting both demo and replay goals at `k=10` and `k=50`, and retaining terminated branches in denominators).
   - Use `E0` (`CR ≤ 0.80` or repeatable non-fall branching in Q's branch panels) as a diagnostic and Stage-2 launch gate rather than claiming short-horizon pose proximity alone falsifies the entire framework.
4. **[MAJOR] MF-4 (Review on P `[MAJOR] F5, F6` & Review on Q `[MAJOR] M2` — Matched Temporal-Abstraction Baselines & Exploration Fidelity in `A`)**:
   - Include P's temporally correlated action-noise / action-repeat baseline (`DA-C`, held/OU over `K=10` at matched marginal action variance) inside `A`, plus a correlated-noise direct-action probe in the branch panels; define explicit reference-phase and recovery rules for `TR`/`A-I`.
   - Because audited `FW`/`A-F` executes deterministic `.loc` actor means (shrinking executed exploration as the schedule ramps to `70%` planner), either include a pre-declared minimal-exploration variant (`A-F'` with held planner-`z` tangent noise enabled) or explicitly route an `A-F` failure with poor executed `z` coverage to a capped `E2` (`Z2`) diagnostic rather than declaring architectural refutation.
5. **[MAJOR] MF-5 (Review on Q `[MAJOR] M3` & Review on P `[MAJOR] F9` — Causal Common-Donor `C` Protocol with `C-rand` and `C-pos` Controls)**:
   - Adopt Q's offline common-donor intervention for `C` (`C-use` vs `C-omit` on a frozen donor pool, followed by fresh-planner training on disturbance recovery `V` and three-sense retention checks: readable, executable, planner-findable), avoiding P's online return-filtering collection confound.
   - Decouple `C`'s launch gate from `A` baseline superiority (gate `C` on Entry Integrity + demonstrated `A-F` controllability + minimal `0.30` Wilson competence at `0.10` m), add a size-matched random non-`L` omission control (`C-rand`) and a `V`-relevant positive enrichment control (`C-pos`), and specify full-return bootstrapped targets for `Q_task` calibration diagnostics.
6. **[MAJOR] MF-6 (Review on P `[MAJOR] F4, F8` & Review on Q `[MAJOR] M1, M5, M6` — Unify Verdict Table, Provenance, Premises & Numeric Re-Scoping)**:
   - Merge P's single-category verdict + decisive-assumption table (`D1`–`D3`) and per-number `B01`–`B05` re-scoping ledger with Q's `Observed / Reported / Specified / Pending` gap provenance, explicit 3-data-path audit, and a dedicated row on executed stochasticity by source (`expert`/`near`/`planner` vs `.loc`).
   - Record in `CORRECTED_CONCLUSIONS` that `B03`'s `> 0.40` pass check was mathematically unfalsifiable (`mean(p^2) + 0.5625 ≥ 0.5625 > 0.40`). In `FRAMEWORK_REVIEW`, qualify `L3` as sampled-condition update eligibility, retain equal-occupancy and full-input (`U_t`) premises for `B03` Case I, note off-sphere planner `z` extrapolation risk, and connect `B02`'s Gaussian KL drift gate to deterministic `.loc` execution.
7. **[MAJOR] MF-7 (Review on P `[MAJOR] F7` & Review on Q `[MAJOR] M4` — Explicit Compute, Wall-Clock & Evaluation Cost Ceilings)**:
   - Convert transition caps into explicit order-of-magnitude accelerator-hour, wall-clock, and memory ceilings conditional on measured entry-gate throughput before launch, define vector-step vs aggregate-transition units consistently, and cap intermediate evaluation panels so evaluation transitions do not dwarf training transitions.

### Key Confounds to Control Across Adjudicated Experiments

- **Information & demonstration asymmetry**: `FW`/`A-F` and `TR`/`A-I` access the 859-frame `0.704` m demonstration (as `B(m)` cues or tracking reference), whereas `DA` and `DA-C` learn from task reward alone. Gains over `DA`/`DA-C` measure the joint effect of demo cues + hierarchy + relabeling; comparison against `TR`/`A-I` isolates cue-based hierarchy against tracking priors under identical demo access.
- **Temporal correlation vs learned behavioral manifold**: Holding `z` for `K=10` steps confounds closed-loop behavioral stabilization with simple 0.2 s action persistence; `DA-C` and `Z4` are mandatory to separate them.
- **Compute vs sample efficiency**: Updating six networks (`B`, twin `F`, actor, twin `Q_task`, recurrent planner with prefix burn-in) costs more compute per environment step than two-network `DA`; both environment-step and accelerator-hour ratios must be co-reported.
- **Matched failure-to-recovery alignment in `C`**: Low-return obstacle episodes (`L`) are predominantly falls/stumbles, making post-disturbance recovery (`V`) a favorable transfer target; conclusions must be scoped to failure-to-recovery reuse unless replicated on a second target task.

---

## 4. Final Investment Call

**Final Investment Call**: **`revise-then-continue`**

**Justification**:
1. **Mandatory revisions before efficacy spend**: (a) Reconcile the research ledger to re-scope all `B01`–`B05` script/accelerator `PASS` results as local contract/algebra checks only; (b) pass the `≤10k`-step production Entry Integrity Gate and add source-tagged executed-`z` telemetry; and (c) lock the merged two-stage experiment manifest (`MF-1`–`MF-7`) with zero bundled whitening, height-in-`B`, or world-model additions.
2. **Bounded continuation warranted**: The reward-free off-policy body relabeling + macro-`z` task split is theoretically coherent and addresses a real experience-utilization bottleneck, making a bounded, kill-gated production validation (`E0/A` then `C`/`E2`) a high-information investment.
