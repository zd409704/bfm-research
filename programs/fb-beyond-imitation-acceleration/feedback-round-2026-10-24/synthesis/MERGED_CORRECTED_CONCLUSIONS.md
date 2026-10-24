# Merged Corrected Conclusions — B01–B05 Re-Scoping Ledger (post-adjudication)

This overlay sits on the sealed B01–B05 record. It does **not** edit historical artifacts. A later append-only reconciliation of `../../program-ledger.md` should cite it and preserve the original artifact identities.

**Base:** draft A `CORRECTED_CONCLUSIONS.md` (per-number ledger; both adjudications prefer it).
**Merged in:** draft B's premise wording and the B03 `p^2 + 0.5625` derivation.
**Additions:** items required by MX-8 in `DISPOSITION.md`, which combines agy MF-6, Sonnet fix 9, review A-on-B M5/m1 and review B-on-A F10.

**Rule: a script or accelerator PASS ≠ framework validated.** A PASS covers only the assertions that script executed on its inputs.

**Slots:**
- **THEORY**: a derivation, valid under stated premises.
- **LOCAL CHECK**: a script on artificial data or a toy plant; it verifies algebra, contract or arithmetic only.
- **DESIGN NORM**: a retained engineering rule.
- **PENDING REAL EXPERIMENT**: requires production home-humanoid training (planned external).
- **WITHDRAWN**: the claim is removed.

---

## 0. Source verification performed this round (resolves residual disagreement R5)

Sonnet marked the script-level claims as asserted but unverified. The orchestrator checked them by reading the source directly. No code was run.

| Claim | Source pointer | Verified content |
|---|---|---|
| B03 `> 0.40` check is unfalsifiable | `gpu_experiments/run_b03_contact_aliasing_spike.py:84–95` | Targets are `+0.75` and `-0.75` (`ones * ±0.75`). The metric is `0.5*(mean((p-0.75)^2) + mean((p+0.75)^2)) = mean(p^2) + 0.5625 ≥ 0.5625`, which always exceeds the pass threshold `0.40`. **The subtest cannot fail.** The minimum is 0.5625, at p = 0, under this per-coordinate mean-square convention and equal target weighting. It does not transfer to summed vector losses or to other target distributions. |
| B03 aliasing `0.0` is tautological | same file, lines 41–50 | `b_net(m_same)` is evaluated three times on the identical tensor. A zero difference holds by construction. |
| B04 toy dimensions and reference | `gpu_experiments/run_b04_four_arm_ablation.py:63–66, 106, 125` | `state_dim = 32`, `act_dim = 12`, `d_z = 64`. F is fitted for 100 steps. The "ground-truth" gradient uses `H_true = 24` with a whitened intrinsic reward. |
| B01 spectrum imposed | `gpu_experiments/run_b01_gram_spike.py:33` | `decay = exp(-linspace(0.0, 2.8, d_z))` on Gaussian coordinates |

---

## 1. Charter hypotheses — status

| Hyp. | Status | Note |
|---|---|---|
| H1 Gram conditioning / whitening | **UNTESTED and DEPRIORITIZED** | The algebra is sound (THEORY). Production κ(Σ_B) has never been measured. A log is planned for information only (Gap G11). **No whitening warrant.** |
| H2 Off-policy decoupling | **OPEN** | Fresh encoding and immutable labels fix distinct bugs (LOCAL CHECK contracts). A short replay window gives no unconditional staleness bound. Macro-Q stability under actor drift is untested. The drift metric must suit deterministic execution (Gap G22). |
| H3 World-model horizon | **OPEN, separate track** | The toy ablation is not evidence (B04 below) |
| H4 Three-source schedule → beyond-demo | **OPEN / INCOMPLETE pending real training** | Not closed by the end of the B01–B05 process. Under the corrected mainline:<br>• near = one exploration ablation (deferred E2/Z1);<br>• beyond-demo success = an outcome metric (A secondary);<br>• the schedule is a candidate, and its time-based ramp is a cold-start risk (Gap G17). |

---

## 2. Per-number re-scoping ledger (every headline figure the program ledger advertises)

| Packet | Headline figure (ledger / result JSON) | Slot | Correct scope | Remaining real experiment |
|---|---|---|---|---|
| B01 | `17.23x` (d_z = 256) / `11.34x` (d_z = 100) MSE reduction; the accelerator run lists `18.56x` / `12.26x` | LOCAL CHECK | Tracker/solver correctness on an **imposed** spectrum (§0). The "exact" reward is defined with Σ⁻¹, so whitening wins by construction. **Not a production whitening warrant**; production condition number never measured. | Information-only κ log (G11) |
| B01 | Readout table; unique dual reward; nullspace non-identifiability; harmonic-mean/Kantorovich bounds | THEORY | Holds at the FB fixed point with residual h, under the fixed-representation / full-rank (or identified-subspace) premises. Says nothing about h in production. | — |
| B01 | Four-site contract | DESIGN NORM | Keep "no whitening at sites i–iii" (`z_update`, expert/near encoding, 1-step actor). Site iv applies only to the world-model track. **Never generalize this to "all z must be whitened".** | — |
| B02 | `0.0` frozen-query drift vs `10.43` double-update bias; 2 clean BN updates | LOCAL CHECK | A prototype normalizer contract on artificial inputs | Production snapshot-hash test (G07) |
| B02 | `0.0` `behavior_z` mutation diff | LOCAL CHECK | Prototype storage isolation | Production hash test (G08) |
| B02 | Recurrent burn-in error `0.0` (accelerator) / `4.77e-7` (CPU) vs stale-hidden `0.383` / `0.277` | LOCAL CHECK | Recomputation parity on random tensors only | 1e-5 parity on production fixtures (G21) |
| B02 | Drift numbers ΔB 0.64–0.67, Δπ 1.70–1.72 at step 20 | LOCAL CHECK (descriptive) | Random data and random perturbations. Not a real-training drift rate. | Replay-age histograms; action-RMS drift (G22) |
| B02 | Gaussian-KL drift gate | THEORY (conditional) | **Assumes a stochastic policy. With deterministic `.loc` execution the KL is undefined or uninformative**, so the gate cannot be applied as written. | Deterministic drift metric (G22) |
| B02 | Implied macro-Q stability or near effectiveness | **WITHDRAWN** | Random-data checks test neither | A (Q calibration, non-gating); deferred Z1 |
| B02 | D4/D5 tangential z-perturbation diagnostics | DESIGN | Valuable but **not landed** in any main experiment | Branch panels (descriptive); deferred E2 |
| B03 | `b_space_kinematic_aliasing_max_diff = 0.0` | LOCAL CHECK (tautological) | Identical tensor fed three times (§0). It shows only that B ignores context it never receives. | — |
| B03 | Perceptive disambiguation MSE `6.80e-4` (accelerator) / `3.31e-4` (CPU) | LOCAL CHECK | 120 Adam steps of **supervised** regression onto synthetic `tanh` targets with constant context. Not an FB-trained actor and not a contact skill. | — |
| B03 | "Irreducible floor" `0.9105` (accelerator) / `0.8953` (CPU) | LOCAL CHECK, **corrected** | This is **predictor error above the 0.5625 optimum** for that constructed distribution. It is not a verified physics floor. The synthesis phrase "matching the theoretical conditional-variance lower bound" is incorrect. **The `> 0.40` pass condition was mathematically unfalsifiable (§0).** | Real contact-skill branching (G09, P2) |
| B03 | Case R / K / I trichotomy; Bayes action-MSE floor; prompt-side impossibility of contact imputation | THEORY | **Premises must be stated wherever the result is cited:**<br>• equal *future* represented occupancy;<br>• an indistinguishable *full* actor input U_t;<br>• the stated target distribution and feasible torque ambiguity.<br>Equal single-frame B encodings alone are insufficient: perceptive actor/F inputs and later occupancy can distinguish behaviors. The premises are not shown on the plant. | G09 |
| B03 | 6/7 ≈ 85.7% cross-height relabel waste | THEORY (inapplicable) | Assumes height in B. **Current B has no height.** Do not claim 85.7% waste. Do not install 70% same-height sampling. | — |
| B03 | Perceptive F/π with motion-only B | DESIGN NORM | Unchanged; consistent with Charter §2.3 | — |
| B04 | `414,771.3` steps/s | LOCAL CHECK | Throughput of a toy batched MLP plant. **Not a simulator or production figure.** It must not seed the Stage-0 throughput assumption. | Stage-0 throughput benchmark |
| B04 | Cosines: H = 0 FB `-0.0338`; whitened hybrid `0.3191` (H = 8), `0.3871` (H = 16) | LOCAL CHECK, **not usable as conclusions** | Toy plant (state 32, **action 12**, **d_z 64**, not 29 / 256). F under-fitted (100 steps). The reference uses H_true = 24 with a whitened reward, so the whitened arm is favored by construction and H = 32 overshoots the reference. Arm definitions are misaligned (owner, agreed). | Separate world-model track, with aligned objectives |
| B04 | "Optimal `rel_l2 = 0.949` at H = 16" vs `1.230` at H = 32 | LOCAL CHECK | rel-L2 ≈ 0.95–1.23 for **every** arm, so no arm is accurate. **No optimal H and no acceleration can be declared.** | — |
| B04 | "7.38× whitening gain" | LOCAL CHECK | Favored by construction (whitened reference) | — |
| B04 | "H = 0 FB gradient nearly orthogonal to the true return gradient" | **WITHDRAWN as a general statement** | The first-action derivative of an *accurate* F can include long-horizon consequences. The near-zero cosine is the expected symptom of an under-trained F and misaligned arms. It is not evidence that first-action FB gradients are uninformative. | — |
| B04 | Tube/compounding bound; splice compatibility M = Σ⁻¹; survival-gradient necessity | THEORY | World-model track only | — |
| B05 | `test1` credible penetration committed with Φ_next = 0 | LOCAL CHECK | A toy multi-link simulator environment and a returned flag. **Not an atomic production transaction.** | Production fixture (G25) |
| B05 | `test2` NaN (substep 3) + overflow (substep 4) → `invalid`, with zero replay/normalizer/counter mutation | LOCAL CHECK | Injected faults in a toy wrapper. A full contact buffer alone is not evidence of lost contacts without backend verification. | Production fixture (G25) |
| B05 | `test3` Wilson LB95 `79/100 → 0.7002 ≥ 0.70` | LOCAL CHECK (**formula only**) | Arithmetic checked (re-verified this round: 79/100 → 0.7002; 78/100 → 0.689). Real unlock behavior is unobserved. | G28 audit |
| B05 | Exact 4096-env quota conservation across 2, 5 and 7 heights | LOCAL CHECK (arithmetic) | Integer formula only | G28 audit |
| B05 | Priority latch invalid ≻ severe_penetration ≻ success ≻ timeout; deferred commit; survivor-only non-identifiability | THEORY / DESIGN NORM | Retained | Production terminate/replay/evaluation/recovery verification (planned external) |

---

## 3. Corrections to the review drafts' own claims (premise repairs, MX-7)

These apply to statements in the round's drafts, not to the sealed packets:
1. "One transition trains every z / all z" (draft A) is restated as follows. **Each transition is eligible for updates under the finitely many sampled conditions.** Shared parameters may generalize, but neither coverage nor beneficial transfer follows. Update eligibility ≠ executable capability.
2. "Holding z runs a policy optimal for some reward and therefore yields stabilized exploration" splits into three separate claims: reward indexing (ideal FB), learned optimality, and physical stabilization. Finite coverage, approximation error, actor optimization and the replay distribution all intervene.
3. "Planner confinement to a thin demo tube" is a **measurable coverage risk** (G13, G18), not a proven fact.
4. Linear preference optimization over motion occupancy can favor exposed extreme points of the achievable occupancy set (draft B). It does not guarantee access to every task-useful behavior.
5. A 0.67 time-to-threshold ratio (draft A) is an **investment hurdle**, reported separately. It is not the scientific boundary of framework value.

---

## 4. Cross-cutting conclusions

1. No B01–B05 artifact is evidence for any empirical cell of the causal chain. Historical packet scores measure review judgments, not efficacy.
2. The prior narrowing to "near" and "success beyond demonstration" as the research question is withdrawn. Near is an ablation; beyond-demo success is an outcome metric.
3. Do not batch-add whitening, same-height relabel, world-model losses or B-input expansion on the basis of these toy tests.
4. Sealed B01 tip/update semantics are retained: standard expert/near encoding, UFO `z_update`, standard `F·z` actor readout.
5. **Re-verify, not reopen:** the source checks in §0 confirm scope corrections only. They do not create new science and do not change any sealed decision.
