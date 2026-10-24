# Corrected Research Conclusions — B01–B05 Re-Slotting (Author A)

**Rule:** a script or GPU PASS ≠ framework validated. Each item is re-slotted as:
- **THEORY**: a derivation, valid under stated premises
- **LOCAL CHECK**: a script on artificial data or a toy plant; it verifies algebra, code contracts, or arithmetic only
- **PENDING REAL EXPERIMENT**: requires production humanoid training

Sealed packets are not reopened as science. The review limitations from the original adjudications are kept, and the corrections below add to them. Script facts cite `gpu_experiments/run_b0*_*.py`; recorded values cite the GPU result JSON files in `gpu_experiments/`.

---

## Charter hypotheses — status

| Hypothesis | Status after this round |
|---|---|
| H1 (Gram conditioning; whitening improves goal-reaching) | **OPEN.** The algebra is sound (THEORY). Production κ(Σ_B) has never been measured. No whitening warrant. |
| H2 (off-policy decoupling bounds staleness) | **OPEN.** Label-isolation and BN contracts are LOCAL CHECKS. Macro-Q stability under actor drift is untested. |
| H3 (world-model horizon vs FB bootstrap) | **OPEN, separate track.** The toy ablation is not evidence (see B04). |
| H4 (three-source schedule → beyond-demo exploration) | **OPEN / INCOMPLETE pending real training.** Not closed by the end of the B01–B05 process. Under the corrected mainline it is reframed: near = one exploration ablation (E2), and beyond-demo success = an outcome metric (E1 secondary). |

---

## B01 — FB Gram geometry and intrinsic-reward identifiability

| Item | Slot | Keep | Correction / limitation |
|---|---|---|---|
| Readout table (linear reward cancels Σ_B; in-support goal z_g = B(g); explicit per-step reward needs Σ_B^{-1}) | THEORY | Yes | Holds at the exact FB fixed point with residual h; says nothing about the size of h in production. |
| C-B01-B-01 unique dual reward; C-B01-B-02 nullspace non-identifiability | THEORY | Yes | — |
| Harmonic-mean / Kantorovich error bounds | THEORY | Yes | — |
| B01-SPIKE "17.23× / 11.34×" MSE reduction (QUEUE lists 18.56× / 12.26× from the GPU run) | LOCAL CHECK | Only as a tracker/solver correctness check | The spectrum is **imposed by the script** (`decay = exp(-linspace(0, 2.8))` on Gaussian coordinates). The "exact" reward is *defined* with Σ^{-1}, so whitening wins by construction. Condition number is **not measured on production humanoid replay**. Not a production whitening warrant. |
| Four-site contract | DESIGN NORM | Keep "no whitening at sites i–iii" (z_update, expert/near encoding, 1-step actor) | Site iv applies only to the separate world-model track. **Do not** generalize to "all z must be whitened". |

## B02 — Non-stationarity and off-policy credit

| Item | Slot | Keep | Correction / limitation |
|---|---|---|---|
| Propositions: fixed-label B-drift invariance, gauge symmetry, TV bound, normalizer invariance | THEORY | Yes | B drift leaves a stored z vector's meaning unchanged, but **actor drift does change it**. The macro replay is not off-policy-safe by default. |
| BN two-pass freeze, `behavior_z` immutability, RNN zero-hidden full-prefix burn-in | LOCAL CHECK | Yes, as code-contract unit tests | Run on `torch.randn` tensors. They prove the prototype's contract, not production's. A production unit test is a planned external step. |
| Drift numbers (ΔB 0.64–0.67, Δπ 1.70–1.72 at step 20) | LOCAL CHECK | Descriptive only | Random data and random perturbations. Not a drift rate of real training. |
| D4/D5 tangential z perturbation diagnostics | DESIGN | Valuable | **Not landed in any main experiment.** Reused in E0/E2. |
| Implied claims of macro-Q stability or near effectiveness | — | **Withdrawn** | Random-data checks do not test either. |

## B03 — Motion-only B under contact/terrain aliasing

| Item | Slot | Keep | Correction / limitation |
|---|---|---|---|
| Case R / K / I trichotomy; Bayes action-MSE floor under indistinguishable U_t; prompt-side impossibility of contact imputation (C-B03-A-03) | THEORY | Yes | Premises (equal future occupancy, indistinguishable U_t) have not been shown to occur on the production plant. |
| `b_space_kinematic_aliasing_max_diff = 0.0` | LOCAL CHECK (tautological) | Only as a statement that B ignores context | The script feeds **the identical tensor** `m_same` three times into the same deterministic network (`run_b03_contact_aliasing_spike.py`). Zero difference is guaranteed by construction. |
| Perceptive disambiguation MSE 3.31e-4 / 6.80e-4 | LOCAL CHECK | No physics content | 120 Adam steps of **supervised regression** onto synthetic `tanh` targets with constant context vectors. Not an FB-trained actor and not a contact skill. |
| "Irreducible floor" 0.8953 / 0.9105 | LOCAL CHECK | **Corrected** | This is the MSE of an actor trained on *other* targets, evaluated against constant targets ±0.75. The actual Bayes lower bound for that setup is 0.75² = **0.5625**. So 0.91 is **predictor error above the bound**, not a verified physics floor. The synthesis statement "matching the theoretical conditional-variance lower bound" is incorrect. |
| 6/7 ≈ 85.7% cross-height relabel waste | THEORY (inapplicable) | Keep only as conditional math | Assumes height in B. **Current B has no height.** Do not claim 85.7% waste. Do not install 70% same-height sampling. |
| Recommendation: perceptive F/π, motion-only B | DESIGN NORM | Yes | Unchanged; consistent with the charter. |

## B04 — Pathwise world-model gradients vs FB first-action derivatives

| Item | Slot | Keep | Correction / limitation |
|---|---|---|---|
| Tube / compounding bound; splice compatibility M = Σ^{-1} (C-B04-A-03/B-02); survival-gradient necessity (C-B04-A-02) | THEORY | Yes, for the separate world-model track | — |
| Cosines (H=0 −0.0338; H=8 0.319; H=16 0.387), "optimal H=16", "7.38× whitening gain" | LOCAL CHECK | **Not usable as conclusions** | Toy differentiable plant (state 32, **action 12**, **d_z 64**, not 29 / 256). F fitted for 100 steps to a 16-step whitened feature sum. "True" gradient uses a 24-step horizon with a whitened reward, so the whitened arm is favored by construction, and H=32 exceeds the reference horizon. rel-L2 errors ≈ 0.95–1.23 for every arm, i.e., no arm is accurate. **Do not declare acceleration or an optimal H.** Arm definitions are misaligned (owner, agreed). |
| "H=0 FB gradient is nearly orthogonal to the true return gradient" | — | **Withdrawn as a general statement** | An accurate F's first-action derivative includes long-horizon consequences. The toy result reflects an under-trained F. |
| 414,771 steps/s | LOCAL CHECK | Throughput of a toy batched MLP plant only | Not a simulator or production throughput figure. |

## B05 — Terminal boundary and curriculum

| Item | Slot | Keep | Correction / limitation |
|---|---|---|---|
| Priority latch invalid ≻ severe_penetration ≻ success ≻ timeout; deferred commit; survivor-only non-identifiability (C-B05-B-02) | THEORY / DESIGN NORM | Yes | — |
| Tests 1/2a/2b on a toy multi-link simulator env with injected NaN/overflow | LOCAL CHECK | Yes, as FSM unit tests | **Does not replace** real production terminate / replay / eval / recovery verification (planned external step). |
| Wilson LB (79/100 → 0.7002) and 4096-env quota conservation | LOCAL CHECK (arithmetic) | Yes | Arithmetic only. Unlock behavior in real training is unobserved. |

---

## Cross-cutting corrections

1. No B01–B05 artifact is evidence for any empirical cell of the causal chain (see `FRAMEWORK_REVIEW.md` §1).
2. Prior narrowing to "near" and "success beyond demonstration" as the research question is withdrawn. Near is an ablation; beyond-demo success is an outcome metric.
3. Do not batch-add whitening, same-height relabel, world-model losses, or B-input expansion from these toy tests.
4. Keep sealed B01 tip/update semantics: standard expert/near encoding, UFO z_update, standard `F·z` actor readout.
