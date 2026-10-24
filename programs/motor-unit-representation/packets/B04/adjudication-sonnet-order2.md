# Adjudication Report: Packet B04 (order2: Candidate P vs Candidate Q)

Adjudicator: independent cross-family adjudicator (Sonnet 5.5). Methodology v1.0 §4 Step 4 and Appendix B.9. Tie margin: 5.0 points.

Sources: `PROGRAM_CHARTER.md`, `brief.md`, `anonymized/order2_P.md`, `anonymized/order2_Q.md`, `reviews/review-A-on-B.md` (the critique of Candidate P), `reviews/review-B-on-A.md` (the critique of Candidate Q).

I did not try to identify authors. I did not open baseline or decision files, so statements that rest only on them are treated as unverified.

I ran two independent numerical checks, described below as V1 and V2. Neither goes beyond the equations and constants printed in the candidates.

- **V1.** I recomputed Candidate P's static stance demand from its own M, G, Jf, IK and nominal parameters.
  - With Ft = 0 and Fn = m_t g, the knee demand |u2| is 0.966 at H = 0.60, 1.061 at H = 0.55 and 1.208 at H = 0.45. This confirms the critique's table.
  - The critique ignores the horizontal force allocation, which is not forced to zero: the rail reacts horizontal force, so Ft is a free variable in static equilibrium. Choosing Ft within the friction cone (|Ft| ≤ 0.8 Fn) lowers the best achievable worst-joint demand to about 0.56 at H = 0.60, 0.62 at 0.55 and 0.70 at 0.45.
  - Candidate P's contact law is Ft = −0.8 Fn tanh(vx/0.01). A sustained non-zero Ft therefore needs a creeping foot, which conflicts with the |x_foot| ≤ 0.05 m hold criterion over multi-second windows.
  - So the infeasibility is real for a non-drifting hold at Ft ≈ 0. It is not a proven impossibility. It is a serious design defect that the candidate's own pre-training feasibility audit would catch.
- **V2.** I recomputed Candidate Q's `D-ASSIGN-1` hip reference inertia from the printed parameters.
  - The thigh-only inertia is I1 + m1·lc1² + n²·Jr = 0.0207.
  - M11(q2 = 1) is about 0.0500. The two differ by about 2.4×, as the critique states. Q's claim that thigh-only descriptor assignment makes J_tr,1 ≡ M11(q2_nom) is therefore internally inconsistent.

---

## 1. Eligibility Gate Check

Gate source: Charter §2 (Hard Technical Boundaries) and the brief's §2 constraints. The brief defines no further numeric gate.

| Gate | Candidate P | Candidate Q |
|---|---|---|
| Charter §2.1 deployment purity (only x137 / g13 reach π and B) | **PASS.** Local modules see only their own x137, z16 and g13. The upper policy gets common proprioception plus rail encoders and a task descriptor. No contact or payload field is included, and inaccessible fields are randomized to test output invariance. | **PASS.** Same. The observation is 282-D from the two x137 plus an 8-D command. Evaluator-only logs are quarantined. |
| Charter §2.2 causal privileged inputs | **PASS** (not applicable downstream). A latch-timing audit is included. | **PASS** (not applicable). Privileged logging is eval-only. |
| Charter §2.3 zero fabricated coverage | **PASS.** Stage 0 demands a real 144×5 qualification artifact, and a surrogate or boolean is rejected. | **PASS.** The unit prerequisite gate is B02 `coverage_ready` plus the RMSE gate, and surrogate runs must be labelled. Author-side numbers are labelled as calculation artefacts, not rollouts. |
| Charter §2.4 smoke run ≠ converged control | **PASS.** Stated and enforced (`BLOCKED_LOCAL_QUALIFICATION`). | **PASS.** Stated and enforced (`BLOCKED_UNCONVERGED_UNIT`). |
| Brief: local weights frozen | **PASS.** Hash checks; only upper parameters are in the optimizers. | **PASS.** Hash checks (`FROZEN_HASH_MISMATCH`); few-shot trains only the upper layer for A/B. For C, the whole raw policy is trainable, which is allowed. |
| Brief: fair raw-torque baseline with the same proprioception | **PASS.** Same 292-D O, 50 Hz, equal transitions and update steps, and an equal-parameter C plus a total-budget C. | **PASS, with caveats.** Same 282-D O, 50 Hz and equal steps. The parameter-matching rule is circular, because P_A is never fixed, and C-big conflicts with the S-G5 within-1% check. |
| Brief D1/D2/D3 present | **PASS.** All three deliverables are present. | **PASS.** All three are present. |
| No fabricated or unqualified results | **PASS.** It is a pure preregistration. | **PASS.** The author-side calculations are disclosed as such. The "closes Issue #9" wording is premature, but §3.6 and §3.1 separate specification closure from scientific evidence. |

**Result:** Candidate P is **eligible**. Candidate Q is **eligible**. Neither is disqualified.

---

## 2. Rubric Scores

### Candidate P

| Row | Weight | Score | Justification |
|---|---:|---:|---|
| Serial-chain coupling reduction | 30 | **21** | **Strengths.** The EL equations are exact and the critique reproduces all figures. The rail augmentation and Schur form are correct, and the warnings about double-counting −τ2 and about relabeling J_eff are valuable. The local mapping is an exact identity with a clear sign convention. The knee parent acceleration is explicit, and the E0–E4 conditions-for-coverage table is careful. **Weaknesses.** The quantitative comparison uses conservative triangle bounds with assumed V = 4 and A = 20 (not derived from task references, and below the candidate's own 1.5 Hz stress tier). It uses a fixed-base, contact-free setting with mp = 0.2, which matches no task. A "30 N" contact is arbitrary. The dominant stance-contact term is never evaluated at the benchmark's own poses, so the numbers do not say what fraction of E3/E4 amplitude coupling occupies. V1 shows body-weight transmission alone sits at 0.97–1.21 knee demand when Ft ≈ 0. The inside/outside determination is deferred to future empirical envelopes. The hip's articulated distal load is not mapped to calibration constants. |
| Fairness of modular vs raw-torque ablation | 25 | **22** | Identical 292-D observation, 50 Hz, history-buffer protocol, rewards, seeds and reset distributions. Policy parameters are exactly 140,000 via published masks (counts verified by the critique). A total-deployment-budget C is included (421,617), plus a raw-pretraining control, amortization reporting, paired seeds and an exploration-sensitivity arm. The critique's valid points: exploration asymmetry of the normalized-sphere adapter, the discontinuous and expensive Pκ solver for B, and an unspecified evaluation action mode. These deduct a little but do not break the fairness structure. |
| Morphology-transfer falsifiability | 25 | **17** | **Strengths.** A full 3×3 L2 × C02 grid including paired changes. m2 is held fixed and c2/I2 recomputed. IK is recomputed. No normalizer refit or local adaptation is allowed. The "unseen by the upper policy ≠ unseen by the local module" distinction is explicit, with a both-unseen panel. Fine-tuning is secondary. Reporting every cell, and keeping individual-task floors, is good. **Weaknesses.** The PASS rule is per-arm absolute (swapped − nominal ≥ −0.10) and not a paired contrast against C. Retention is pooled over cells, contradicting the anti-pooling rule used elsewhere. Many cells are statically hard for a stationary-foot hold. The critique's 9-cell table is allocation-dependent (V1), but low-C02 and long-L2 cells are still plausibly saturated. This would make retention measure saturation, not transfer. The feasibility audit exists but does not gate. |
| Benchmark reproducibility | 20 | **15** | The specification is very complete: parameters, stops, contact law, integrator and timestep-halving check, tasks with success predicates, reward formulas, seed blocks, termination taxonomy, hyperparameters, artifact list and verdict schema. The key defect is that the specified squat/hop/landing poses are at or beyond the actuator ceiling for a non-drifting hold (V1). The foot payload has no static stance effect, because the payload is at the contact point, so the "payload squat" does not exercise a sustained load. The support-qualification thresholds (n ≈ 20 per bin, 0.25 SD) are likely to fail under the null, so the support panel would be empty. This probably yields INCONCLUSIVE by construction. The Issue #9 closure criteria are separated into specification and engineering levels, which is correct. |
| **Total** | 100 | **75** | |

### Candidate Q

| Row | Weight | Score | Justification |
|---|---:|---:|---|
| Serial-chain coupling reduction | 30 | **24** | **Strengths.** Exact EL equations with rotor dynamics (consistent with the J_nom convention) on a rail. The effective-external-torque identity is exact, with a reported residual of 7e-15. The knee housing-transport identity (heave acts as modified gravity; only ω̇_P and g_eff matter) is a genuinely useful structural result. The closed-chain null-mode analysis is a real addition. This candidate is the only one that quantifies coupling against the S_max / 0.92 E3 ceiling across tasks: frequency tables, the payload threshold, landing contact windows of 1.06–1.39 S_max, and stance inertia ratios of 1.6–19×. It also gives a bandwidth analysis and a five-code coverage certificate. **Weaknesses.** The X/S partition treats off-diagonal acceleration terms as exogenous, which is not an action-independent statement in a coupled chain (critique D1, valid). `D-ASSIGN-1` is internally inconsistent (V2). The stance effective inertia is not normalization-defined (D3). The "3 kg is infeasible" conclusion rests on λx = 0, so it is allocation-dependent (D4; consistent with V1's finding that horizontal force is a free variable). The flight claim ÿ ≈ −g is only approximate. The unknown Ω_E3 / Î_E4 are left to the manifest, which is honest but leaves the E4 verdict conditional. |
| Fairness of modular vs raw-torque ablation | 25 | **17** | The identical-observation and 50 Hz contract is good. The same shared frozen unit is used. Seven arms include useful controls (A-rand, C-PD, C-big). The HP grid and update budget are equal. The reachability diagnostic and the off-image fraction are good ideas. **Weaknesses.** The parameter-matching rule is circular (P_A undefined), and C-big contradicts the within-1% audit. SAC with an unspecified density on projected-sphere actions leaves entropy and the critic action undefined (F1, valid). The normalizer-fitting convention is ambiguous. The A-rand and C-PD interpretations are over-read. Few details are given for B (bounds, transforms). "A cannot beat C asymptotically" is stated without a capacity-class argument. |
| Morphology-transfer falsifiability | 25 | **14** | **Strengths.** Cell-by-cell predictions conditioned on a certificate. R-NOM, R-MULTI and few-shot regimes. Extrapolation values for L2. Explicit decision rules (supported / falsified / not-representational). **Weaknesses.** Eligibility depends on outcomes of the arm being tested (slip and force drift define A-NULL, and trajectories are arm-dependent), so a modular arm can exit the comparison (T1, critical). The retention metric R_cell/R_nom is sign-inverted for negative-cost returns (T2, critical). Hip C0 silently changes with the knee swap. The transfer-cell construction is under-specified (mass, COM and inertia mapping per L2). The claim that "units remain in the local seed hull" is asserted and not demonstrated. Censoring at 2M is claimed conservative but is not. Nominal cells are mostly predicted OUT, so the primary "≥2 of 3 tasks on IN cells" decision may have an empty eligible set. |
| Benchmark reproducibility | 20 | **11** | Plant, tasks, cell grid, closure criteria and artifact path are given. The seed-hull gate and the unit gate are good. But contact friction and stick/slip, integration, stop forces, reset velocities, sine phases, squat interpolation, calibration distributions, episode-key construction and the metric normalizations are missing or loose. Joint-derived height is not observable in flight, yet T3 requires apex evaluation (R2, valid). Run counts are mis-stated (420 vs 210 runs). The "CPU, numpy, ≤ 5 min" spike scope is not substantiated for gates that instantiate networks and run contact rollouts. Closure of Issue #9 is asserted prematurely. |
| **Total** | 100 | **66** | |

Score difference: P − Q = **9** points, which exceeds the 5.0-point tie margin.

---

## 3. Principle Claim Adjudication (Appendix B.9)

### C-B04-P-01 — Same-input incompatible-action obstruction

- **Algebra:** correct. Equal J and equal inputs imply equal action, so the acceleration difference is Δℓ/J. The 2ε separation argument, the midpoint bound (ℓa − ℓb)²/(4J²) and the set-intersection form are all valid.
- **Status:** it holds as a true, nearly tautological identifiability lemma. It does not establish necessity of any design choice, because the candidate itself concedes that the premise fails whenever histories or sensing differ.
- **Proposed test:** it is a determinism or leakage audit. The foot-payload hidden variable violates the equal-J premise and has no stance effect. ε is never tied to task success.
- **Ruling:** **ACCEPT AS GRADE-1 LEMMA / DIAGNOSTIC. DO NOT PROMOTE AS A NECESSITY CLAIM.** Pre-register ε and keep the determinism audit.

### C-B04-P-02 — Joint support needed for a distribution-free transfer certificate

- **Content:** equal marginal hip/knee load distributions can arise from different joint laws, so marginal quotas cannot certify a serial-chain transition law. This is logically sound. The claim is explicitly scoped: it does not say support is necessary for success, and the Grade-2 transfer-gain hypothesis is kept separate.
- **Caveat:** the empirical support test attached to the claim is miscalibrated (see §2 and Mandatory Merge).
- **Ruling:** **ACCEPT** as a narrow conditional Grade-1 logical claim. Do not use the attached qualification thresholds as written.

### C-B04-Q-01 — Amplitude inclusion is insufficient to certify the coverage proviso

- **(a) "τ_self is outside the support of any E3/E4 generator":** over-stated. Conditional independence of an open-loop generator under interventions differs from disjoint trajectory support, and a specific realized path can coincide (critique). It also relies on the D1-flawed X/S partition.
- **(b) the counterexample:** a delayed sampled PD loop can lose stability under an inertia change while onset torque is small. This is a valid existence statement for that loop. The discrete plant, delay indexing and saturation are not specified well enough to reproduce the spectral radius, and the example realizes a reduced inertia (ρ = 0.25) while the stance concern is large inertia. It also does not show a chain trajectory that realizes it.
- **(c) "any certificate must contain A-RHO and A-NULL":** does not follow. A direct robust-stability or coupled-response certificate could also account for it.
- **Ruling:** **PARTIAL ACCEPT, DOWNGRADE.** Retain the narrow statement: within a specified sampled-controller/plant family, an amplitude-only bound does not guarantee closed-loop stability, so the effective coupled dynamics must be considered. Treat A-RHO and A-NULL as proposed diagnostics, not necessary certificate components. The Grade-1 request for the bundled claim is not granted.

### C-B04-Q-02 — Housing-transport identity (knee/terminal joint)

- **Content:** with a single rigid distal body, the effective external torque is −m[r_c × (a_J − g)] − (I + nJr)ω̇_P + τ_grav,tr + τ_contact. There is no bilinear (ω_P, q̇_j) term, and base heave enters only as g → g + ÿ. This is consistent with the printed M, C and G, which I checked by inspection (the rotor terms reconcile).
- **Limits:** it is an instantaneous torque identity. It does not by itself prove equivalence of trajectory distributions, and the "sufficient statistics" reading (iii) holds for the instantaneous torque only. The flight statement ÿ ≈ −g is approximate. The identity applies only to terminal joints. The hip carries an articulated distal chain.
- **Ruling:** **ACCEPT as a Grade-1 derivation**, with the restricted scope above.

### C-B04-Q-03 — Closed-chain integral null mode

- **Content:** conditional on units that realize integral action, the combination w = φ2·I1 − φ1·I2 has ẇ independent of motion, is neutral under consistent targets and ramps under inconsistent targets. This is correct as a conditional linearized statement.
- **Caveats:** the force-driving quantity is k_i·w, so the conventions and the fixed-tangent approximation must be stated. Frozen actors need not realize integrators. Anti-windup, leakage and coordination can suppress drift.
- **Ruling:** **ACCEPT as a conditional Grade-1 statement.** It does not apply to V3 until measured. The stated falsifier is acceptable.

---

## 4. Disposition

**Recommend: P**

P leads by 9 points (75 vs 66), outside the 5-point tie margin. The decisive differences are:

- P's fairness controls and its reproducible specification (rows 2 and 4).
- Q's retention-metric sign error and its arm-dependent eligibility rule. These two defects undermine Q's falsifiability row, and neither can be repaired by merging a single patch.

**Alternate: Q.** Q is the stronger candidate on row 1 (quantified coupling) and has several ideas P lacks. If a single candidate must be chosen with a bias toward physics insight over benchmark completeness, Q's reduction and certificate contribute more. Its benchmark is not releasable without major repairs.

### Mandatory Merge Items

**From Q into P:**

1. Quantify coupling against S_max and the 0.92 E3 ceiling at the benchmark's own operating points. This includes the stance contact torque as a function of horizontal force allocation, the frequency scaling of inertial and Coriolis terms, the bandwidth/delay residual, and stance-inertia ratios. Derive bounds from reference trajectories by inverse dynamics, not nominal V and A.
2. Include the housing-transport identity (with the terminal-joint scope) and the flight gravity-modulation result. State that G = g·a gives exactly zero Schur-reduced gravity in flight, and pre-classify flight windows.
3. Add the reachability, off-image and A-rand and C-PD controls as secondary arms or diagnostics, with their interpretation limits.
4. Add the coverage-certificate codes (inertia ratio, bandwidth, impulse, null-mode drift) as diagnostics. The eligibility labels must be fixed before learning from independent probe trajectories. They must not depend on the evaluated arm's own outcomes.
5. Add the `FROZEN_HASH` check and Q's separation of "specification closure" from "scientific H4 evidence".

**Repairs P needs (from the critiques and V1):**

6. Make the feasibility audit a blocking gate. Publish a per-pose, per-cell demand table analysed over all admissible horizontal force allocations. It should state a required torque reserve, for example ≤ 0.75, and the mass and C0 re-parameterization if it fails. Remove or justify poses needing sustained drift.
7. Move the sustained-load payload to the carriage or torso (or mid-shank). A foot-point payload has no static stance effect.
8. Recalibrate the support test against source-vs-source splits, using coarser or adaptive bins and equivalence tests (TOST-style) with power analysis.
9. Make transfer PASS comparative: a paired retention contrast against C with its own interval, plus a per-cell or worst-cell floor.
10. Specify the evaluation action mode. Address the normalized-sphere exploration asymmetry in A, and the discontinuity and cost of Pκ in B (a warm-started or smooth surrogate, with adapter-switch frequency logged).
11. Handle double censoring and the small-n bootstrap (a BCa or permutation test, with a power analysis).

**Repairs Q would need if chosen as primary** (listed for the alternate path):

- Fix `D-ASSIGN-1` and the stance-inertia normalization.
- Replace the X/S exogeneity claim with an intervention-based statement.
- Replace the signed-return retention ratio.
- Separate the hip C0 change from the knee swap.
- Complete the contact, observation-in-flight and reset specifications.
- Fix the parameter-count rule and the SAC density convention.

### Confounds

I scored from the two sealed candidates and the two blind critiques. I did not read baselines or decisions, so claims resting only on those files are unverified. Scores for rows 2–4 partly rely on the critiques' arithmetic, which I spot-checked only where stated (V1, V2).

The V1 check partly weakens one of the critique's central findings for P. It confirmed the knee demand at Ft = 0, but showed the infeasibility is allocation-dependent. The same objection (D4) was raised against Q's 3 kg threshold, so I treated the two symmetrically. I scored P's benchmark defect as serious and fixable by its own audit clause, not as fatal.

The reviewers had different scopes. Both critics worked from a single proposal and did not see the other. The critique of P found two critical benchmark-feasibility issues and the critique of Q found two critical falsifiability issues, so severity labels are not directly comparable across them.

There is a possible length and detail bias in P's favour: P is more fully specified, which helps rows 2 and 4 almost by construction. Q's physical-insight strength was weighted in row 1 to counter this. A different weighting of row 1 against row 4 could narrow the gap, but would need a swing of about 4–5 points to reach the tie margin. Row 1 is already where Q leads by 3 points.

Neither candidate has executed experiments. All scores reflect specification quality, not demonstrated H4 transfer. No claim here establishes the H4 composition gain, and the frozen unit's convergence prerequisite remains unmet in both.
