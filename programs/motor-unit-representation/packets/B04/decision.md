# Packet B04 Decision — Hierarchical Composition of Frozen Local Motor Units Under Coupled Loads

- **Decision ID**: `D-B04-001`
- **Packet ID**: `B04`
- **Method Version**: v1.0 (`1ce8d1b3e42cfbec2122468c595d52d238d6ca1dfd079292b7d61d95fb3d11f7`)
- **Adjudicators**:
  1. `agy` (Order 1: `P=A, Q=B`): `packets/B04/adjudication-agy-order1.md`
  2. `claude` (`sonnet`, Order 2: `P=B, Q=A`): `packets/B04/adjudication-sonnet-order2.md`
- **Pre-Registered Empirical Spike**: `packets/B04/spikes/B04-SPIKE/VERDICT.json` (`PASS`, CPU)

---

## 1. Consolidated Order-Swapped Rubric Scores

| Proposal Track | Author Model | Order 1 (`agy`: P=A, Q=B) | Order 2 (`sonnet`: P=B, Q=A) | Mean Score |
|---|---|---:|---:|---:|
| **Proposal A** (`proposals/A.md`) | `claude` Opus | `71.0 / 100.0` | `66.0 / 100.0` (as Q) | **68.5 / 100.0** |
| **Proposal B** (`proposals/B.md`) | `codex` `gpt-6-astra` | `65.0 / 100.0` | `75.0 / 100.0` (as P) | **70.0 / 100.0** |

- **Winning Track**: **Tie / Hybrid** (mean margin `+1.5` for B, strictly inside tie margin `5.0`).
- **Order notes**: Order 1 recommends P(=A) by `+6.0` (clears win; primary `LIMB2-v1` coupling / certificate base). Order 2 recommends P(=B) by `+9.0` (fairness / reproducibility lead). Cross-order mean does not clear the win threshold.
- **Disposition**: **`Recommend: Tie / Hybrid`** — merge both scaffolds with mandatory fixes listed below. Treat **Proposal A (`LIMB2-v1`)** as the primary generative / coupling-reduction / coverage-certificate base; merge Proposal B's Schur reduction, numerical-plant completeness, masked parameter counts, comparative transfer metrics, and blocking feasibility / support repairs.

---

## 2. Key Adjudication Findings & Mandatory Merges

1. **Plant & coupling reduction (base = Proposal A `LIMB2-v1` / `LIMB2-REF`)**:
   - Keep A's physically verified reference geometry and actuator capacities (`l1=l2=0.25 m`, pelvis-mounted T2 payload, hip `C01=9`, knee `C02=6` N·m, `Sj=1.25 C0,j`). Never mount the sustained-load payload on the grounded foot.
   - Adopt A's housing-transport identity (terminal / knee joint) and closed-chain integral null-mode analysis as scoped Grade-1 lemmas.
   - **Merge from B**: Exact Schur-complement reduction `M_red = M_qq − M_qy M_yy^{-1} M_yq` and full `M(Q)^{-1}` input-output sensitivity; replace any claim that off-diagonal `−M_jk Q̈_k` is purely exogenous ("Class X") with an intervention-based partition. State free-flight Schur identity `G(q) − g a(q) ≡ 0`. Fix isolated-link `J_tr` / stance-manifold tangent normalization (`s=q2`).

2. **Feasibility & coverage certificate**:
   - Adopt A's five-code coverage diagnostics (`A-AMP`, `A-BW`, `A-IMP`, `A-RHO`, `A-NULL`) as a **Grade-2 preregistered diagnostic protocol**, not as necessary components of every H4 certificate.
   - **Blocking Stage-1 Inverse-Dynamics Feasibility Gate** (from both adjudications): for every task/morphology cell, minimize actuator demand over friction-cone-admissible contact forces before training; mark `FEASIBLE` only if static demand ≤ `0.92` (or a published reserve, e.g. ≤ `0.75`); else `INFEASIBLE_CONFIG`.
   - Quantify coupling against `S_max` / `0.92` E3 ceiling at the benchmark's own operating points via inverse-dynamics on reference trajectories (not nominal `V`/`A` triangle bounds alone).
   - Pre-register cell eligibility (`IN` / `EDGE` / `OUT`) from controller-independent probe rollouts **before** downstream learning; never reclassify `OUT` from a learned arm's own slip / internal-force drift.

3. **Fair ablation Modes A / B / C**:
   - Retain A's smooth closed-form kinematic completion `Kc` for Mode B with B's explicit box bounds; reject discontinuous multi-start SLSQP projection `Pκ` as the primary adapter.
   - Adopt B's fixed `140,000` active upper-policy parameters via deterministic SHA256 binary masks; `C-big = 140,000 + 281,617 = 421,617` explicitly exempted in `S-G5`. Fixed observation scaling so frozen `πθ` receives calibrated `x137`.
   - Mode A: pass projected `z ∈ S^{15}(4)` to critic/replay; entropy on projected spherical density (or tangent / vMF); torque-variance-matched exploration calibration on tuning seeds; specify evaluation action mode (deterministic mean vs sampled).
   - Keep A's `A-rand` / `C-PD` / `C-big` control arms; add B's reachability / off-image diagnostics with interpretation limits.
   - Include proprioceptive rail encoder `(y,ẏ)` in shared upper observation; never feed rail states to frozen local modules. Compute height/apex metrics from simulator-truth `y`.

4. **Numerical plant completeness (merge from B)**:
   - float64 semi-implicit Euler at `Δt = 0.25 ms` with `0.125 ms` timestep-halving gate (`<5%` impulse/success drift).
   - Explicit joint-stop spring-damper; stateful bristle/stiction-clamped Coulomb tangential contact (not memoryless slip-at-rest); quintic smoothstep squat/hop references.
   - `FROZEN_HASH` check; separate "specification closure" from "scientific H4 evidence".

5. **Transfer metrics & morphology grid**:
   - Replace signed-return ratio `η_ZS = R_cell / R_nom` with bounded success difference `ΔS_ZS = S_cell − S_nom` and positive skill `R̃ = exp(−RMSE/σ_task) ∈ (0,1]`.
   - Evaluate **comparatively** vs Baseline C (`ΔS^{A|B} − ΔS^C`) with mean retention contrast **and** worst-cell floor.
   - Clean `3×3` grid: `L2 ∈ {0.18, 0.25, 0.32} m × C02 ∈ {4.5, 6.0, 9.0} N·m` with `C01=9.0` held fixed; uniform-rod scaling (`m2` fixed, `c2=L2/2`, `I2=m2 L2²/12`); separately labeled stress panel `L2=0.40 m` / `C02=3.0`.
   - Recalibrate joint-support bins (coarser / adaptive + TOST equivalence on source-vs-source splits); do not ship the miscalibrated 6,250-bin / `n=20` / `0.25 SD` gate as written.

6. **Hard constraints preserved**: each local `(Bω, πθ)` frozen (`281,617` deployed each); upper policy compared fairly against raw-torque Baseline C on identical proprioceptive history / rate / update budget; no new deployed local parameters from composition adapters.

---

## 3. Principle Claim Rulings (Appendix B.9)

Mapped from order-swapped labels (`Order1 P/Q = A/B`; `Order2 P/Q = B/A`) to stable `C-B04-A-*` / `C-B04-B-*` IDs:

- **`C-B04-A-01`** (amplitude-envelope inclusion insufficient for H4 coverage proviso; Order1 `C-B04-P-01` / Order2 `C-B04-Q-01`): `Candidate` — **PARTIAL ACCEPT**. Narrow Grade-1 conditional lemma (counterfactual law distinction + constructive onset-amplitude insufficiency in a specified delayed sampled servo family). Reclassify bundled `A-RHO`/`A-NULL`-must-appear certificate claim as Grade-2 diagnostic protocol.
- **`C-B04-A-02`** (housing-transport identity, terminal joint; Order1 `C-B04-P-02` / Order2 `C-B04-Q-02`): `Candidate` Grade 1 — **ACCEPT** (analytical identity; scope = single rigid distal body / knee; proximal articulated subchains retain bilinear terms).
- **`C-B04-A-03`** (closed-chain integral null mode; Order1 `C-B04-P-03` / Order2 `C-B04-Q-03`): `Candidate` Grade 1 — **ACCEPT WITH QUALIFICATION** (conditional on pinned sticking contact + local integral action; does not assert frozen V3 actors realize ideal integrators).
- **`C-B04-B-01`** (same-input incompatible-action obstruction; Order1 `C-B04-Q-01` / Order2 `C-B04-P-01`): **DOWNGRADE TO OPERATIONAL AUDIT GATE** — retain as Stage-1 determinism / leakage unit test; do not promote as a ledger necessity / design-forcing principle claim.
- **`C-B04-B-02`** (joint support needed for distribution-free transfer certificate; Order1 `C-B04-Q-02` / Order2 `C-B04-P-02`): `Candidate` Grade 1 — **ACCEPT** as narrow methodological principle (marginals ≠ joint/conditional serial-chain law). Do **not** lock the attached miscalibrated support thresholds.

---

## 4. Empirical Verification Summary (`B04-SPIKE`)

Reused `packets/B04/spikes/B04-SPIKE/VERDICT.json` (`PASS`, device `cpu`, `elapsed_sec≈0.0054`):

- G1 coupling vs E3/E4 envelope: `PASS` (`fraction_inside_envelope=1.0`, `couple_p50≈0.461`, `couple_p95≈0.737`, `E3_amp=6.0`, `E4_amp=9.0`)
- G2 fair ablation scaffold: `PASS` (obs-history match, `50 Hz`, equal update budget, frozen local modules; modes `A_direct_latent`, `B_target_outcome_via_B`, `C_raw_torque_baseline`)
- G3 morphology-swap protocol: `PASS` (`L2_swap ∈ {0.12,0.25,0.4}`, `C0_swap ∈ {3.0,6.0,9.0}`; metrics sample-efficiency-to-hold-RMSE-0.35 and zero-shot transfer return)

Status: Candidate-level analytic / scaffold evidence that 2-DoF RR coupling magnitudes sit inside the single-unit E3/E4 torque envelope under the spike's assumptions, and that the Mode A/B/C + morphology-swap protocol is specified. **Does not lock Charter H4** composition / transfer gains; full Stage-2 learning curves remain deferred to integrated simulation after the mandatory merges above.
