# B04 Adjudication, Order 2 (P and Q swapped), Sonnet 5.5

Adjudicator: Order-Swapped Adjudicator, Methodology v1.0 §4 Step 4 and App. B.9.
Inputs read: Charter, brief, `order2_P.md`, `order2_Q.md`, `review-A-on-B.md` (critique of P), `review-B-on-A.md` (critique of Q), `VERDICT.json`.
I did not read `adjudication-agy-order1.md`. I ran no code.
Limitation: the Methodology and Appendix B.5 text and the baseline files were not in my reading list. B.5 gates are therefore judged only through the Charter and brief gates and the reviewers' statements. Format-level B.5 compliance is **unverified** for both candidates.
Identity mapping, from the content: P is the candidate that uses the "user's four-arm definitions" with the ensemble residual-MLP model and the 1-D vertical-contact toy. Q is the candidate that inherits D-B01-001 and uses the hopper-torso toy.

## 1. Eligibility Gate Check

| Gate | P | Q |
|---|---|---|
| Charter HC1 (no BC or tracking) | PASS with note. No action-MSE or pose reward. Arm D maximizes a model head plus an FB tail, which the brief's deliverable 1 requires. P never says the brief overrides the literal "exclusively F^T z" wording. | PASS with note. Same tension. The kinematic loss `λκ‖κ(ŝ)−m‖²` trains the model only, not the actor. |
| HC2 (z separation) | PASS. States the 50/50 frozen-BN relabel, `behavior_z` never overwritten, and task Q on executed commands (§2). | PARTIAL. The sampler and BN are stated. `behavior_z` preservation and executed-action task Q are not restated. The spike's half-`B(m_demo)` commands differ from the mandated relabel. Omission, not violation. |
| HC3 (single-frame B) | PASS. Terrain enters W only. | PASS in intent. The toy uses 24 dims and a random frozen B, so contract coverage is limited. |
| HC4 (penetration vs invalid) | PASS. Real replay is handled correctly, and the smooth hazard is explicitly kept separate from the hard label. | PARTIAL. The sigmoid hazard is used without a clean separation panel. Normalizer-level NaN rejection and run halt are not stated. |
| HC5 (evidence vs claims) | PASS. Claims no measured result. | PASS. §5.0 treats the CPU spike as smoke only (I verified its reading below). |
| Brief: no future frames in W_ψ | PASS. Causal state or belief with detached burn-in. | PASS. Future `m` supervises only. A shuffle-leakage test is not specified. |
| Brief: four arms and shared substrate | **FAIL (contract), curable.** Replaces the `baseline/03` §6 arms with its own. Brief §3.3 wants A/B/C at H=1 vs 32 and D at {1,4,8,16}. Shared accounting is satisfied. | **FAIL (contract), curable.** Explicitly supersedes the §6 arms. Gives a §2.4 mapping and a D-V control, but single-task WM is dropped. |

Verdict: both are **eligible with mandatory repair**. Neither breaches a Charter hard constraint. Both deviate from the brief's arm matrix. Both deviations are documented, which is why I do not disqualify either.

## 2. Scores (rubric weights from `brief.md`)

### Candidate P (Order 2): 73 / 100
| Row (weight) | Score | Justification |
|---|---:|---|
| Math rigor of gradient decomposition (30) | 26 | Strongest part. Sensitivity recurrences `S, C`, the adjoint form `g∞=ΣγᵗcₜPₜᵀQₐ`, the `H+1` policy-call count, the oracle-tail identity `g∞−g_H=R_{>H}`, and the explicit `E_{t+1}` recurrence with its `L=1` closed form are all correct (Review A concurs). Survival derivative is the full causal form. Deductions: errors are measured against the fixed-start `g∞`, which favors large H by construction; the bound is vacuous when `L≫1`; and ε_W blows up as `s_min→0`. A variance bound `G_H²/N_H` is given, which Q lacks. |
| Zero future leakage (25) | 22 | Inputs are `(s,a)` only. 16-step detached burn-in, no-`no_grad` rule for frozen weights, and the terminal action kept connected. Deductions: online-B z vs target-B head mismatch is not measured for the actor pass; burn-in start-state shift is unreported; `d_s`, `d_z` are never given numerically. |
| Contact stiffness and rollout stability (25) | 14 | Honest analysis of exponential `A_t(L)`, but no mechanism. Line 154 defers to "event/saltation treatment or a surrogate-bias panel". The only controls are grad clip at 10 (reported) and post-hoc horizon selection. No Jacobian-norm truncation or disagreement penalty, and the model is trained on 8 steps but rolled to 32 with no Sobolev term. Partial credit for the soft-survival derivation and the gate that routes to A when closed. |
| 4-arm ablation completeness (20) | 11 | Reuses A in B/C/D and keeps representation nets in all arms. Reports pairwise isolation (A–B, B–C, A–D) and a matched-segment diagnostic with n_eff histograms. Gaps: throughput is not separated from differentiation depth (no detached-rollout MVE control at equal imagined transitions); the multi-task-z factor is made optional; tail-free H=32 is only a gradient diagnostic. |

### Candidate Q (Order 2): 72 / 100
| Row (weight) | Score | Justification |
|---|---:|---|
| Math rigor of gradient decomposition (30) | 21 | The head and tail split, and the observation that the Arm A truncation is a rescaling under occupancy sampling, are insightful. The `γ^H` and `S_1(H)` table is useful. But Review B's CRITICAL points stand: `ε_f` is introduced and then dropped from `E_J`; the terminal Jacobian term is "absorbed" without a `Q'_s` domination assumption; and the `K_a` factors are missing. The survival chain rule omits `∂_aℓ·∂_sπ`. There is no variance term, though the brief asks for bias-variance. |
| Zero future leakage (25) | 20 | `m_{k+1}` supervises only, real booleans mask only data, and the §2.3 stop-gradient table is explicit and clear. Deductions: the state `s` and observation contract are under-specified (12-dim toy layout, `κ` only partly defined), and no perturbation leakage test. |
| Contact stiffness and rollout stability (25) | 19 | The only candidate with a concrete mechanism: log-space survival with the bounded `(1−p̂)` factor, and a backward-only stop-gradient when the JVP product exceeds `Λ_max=10`, with `H_grad` logged. It also has a clear argument against hard masks (zero a.e. gradient plus a missed boundary term). Deductions: a single warm-started JVP is a heuristic, not an upper bound; backward truncation biases the estimator and is unquantified; smoothing-temperature dependence is untested. |
| 4-arm ablation completeness (20) | 12 | Trains the world model in all arms to equalize overhead. Includes D-no-tail, D-hard-mask, D-V, and oracle substitutions that separate `E_J, E_c, E_F, E_W`. Arm B's `δ_a=0.05` trace cut gives the same near-collapse to `n_eff=1`, which Q predicts and logs per z-source. Gaps: the B/C targets zero the tail after a mismatch instead of bootstrapping at the last valid state (Review B CRITICAL); C vs D still changes two factors; the arms are superseded. |

## 3. Principle Claim Adjudication (Appendix B.9)

Format conformance to the Appendix B template is not checked (template not supplied). The judgments below are on premises, conclusion, test and falsifier.

**P / C-B04-CAND-01 (parameter-path coverage; claimed Grade 1).** Premises are explicit. Conclusion: the frozen-tail hybrid cannot equal `∇J∞` unless `R_{>H}` is represented. **Verdict: Reject as a necessity claim; keep as a diagnostic identity (downgrade).** The "additional premise" `R_{>H}≠0` is the conclusion, because the proof is the definition `g∞−g_H=R_{>H}`. The scope excludes the occupancy-weighted actor, which is the true comparator, and every arm violates the "exact critic and dynamics" premise. The 1e-6 falsifier tests autodiff correctness, not the world, and is tighter than the 1e-4 reference-convergence tolerance. It is acceptable as a verification gate before interpreting results.

**P / C-B04-CAND-02 (head/tail coordinate compatibility; claimed Grade 1).** **Verdict: Accept as Grade 1 conditional.** The one-step Bellman subtraction `E[B̄(s')]ᵀ(M−Σ⁻¹)z=0` with spanning premises forces `M=Σ⁻¹`. This is sound, testable, and falsifiable (a distinct M satisfying all identities). Damping is correctly labeled an approximation. Condition: the spanning premise must be checked empirically on replay, and the claim says nothing about learning speed (P says so).

**Q / C-B04-CAND-01 (terminal-critic state-gradient amplification; claimed Grade 2, bound Grade 1).** **Verdict: Reject as stated.** The derivative condition `ε_F^s K_a(1−H|lnγ|) ≥ |lnγ| ε_F^a` is arithmetically right at `L=1`. But the conclusion "any H3 gain must come from the head, not reduced critic reliance" does not follow. P2 gives no lower bound on `ε_F^s`; P3 is an unmeasured coherence assumption; and a difference of relL2 norms is not an additive critic component (interaction terms). The `Δ_F(32)<0.8Δ_F(4)` falsifier is multiplicative and breaks when `Δ_F≈0` or is negative. Re-register as a measured envelope with an absolute effect size.

**Q / C-B04-CAND-02 (soft survival necessary for pathwise hazard avoidance; claimed Grade 1).** **Verdict: Accept as Grade 1, narrowly.** A hard multiplied mask has zero a.e. pathwise gradient while the true boundary term is nonzero. This is deductive and testable near crossings. Scope: it shows necessity within pathwise estimation, not against score-function or event-based estimators. The hard-mask ablation is a good implementation-leak falsifier. The log-survival formula must first be corrected to include `∂_aℓ·∂_sπ`.

**Q / C-B04-CAND-03 (whitening necessity is κ-conditional; inherited from B01).** **Verdict: Accept conditionally.** The population statement is plausible and the falsifier is concrete. Fix: condition number 1 means `Σ=cI`, not `I`, so scale must be normalized. The spike's 0.415 vs 0.050 at H=8 is point-estimate smoke only.

**Spike check.** `VERDICT.json` gives H=0 cosine −0.0019 (relL2 1.010). H=16 has relL2 0.855, so MSE is about 28% below H=0 and about 30% below H=32 (1.024). H=8 is about 16% below H=0. `best_short_horizon_hybrid_cosine` reports H=8 (0.415) although H=16 (0.520) and H=32 (0.556) are higher. Q's §5.0 readings are accurate. P's review's MSE arithmetic is also accurate. The scalar PASS is not traceable to either candidate's gate, and no H may be locked from it.

## 4. Disposition

**Recommend: Tie.** The scores are P 73 and Q 72. That is a 1-point difference, well inside the uncertainty of my unseen-Appendix limitation. P has the stronger, cleaner mathematics and a variance bound but a thin contact-stability answer, which is the brief's central difficulty. Q has the better contact and ablation controls but a flawed error bound and a weaker claim set. Neither alone satisfies the brief.

**Alternate:** If a single base is required, use P as the base for the derivation and Q's contact and control machinery, because mathematical errors are harder to patch in a locked spike than a missing mechanism. This is an editorial preference, not a score-driven call.

**Mandatory Merge items (apply whichever base is chosen):**
1. Restore the brief's arm matrix: A/B/C at H=1 vs 32 and D at {1,4,8,16}, with the new target variants as additional controls. Put the single-task/no-F baseline (or D-V) back as a required arm.
2. Add a detached-rollout (MVE-style) control matched on imagined transitions and GPU-seconds to separate throughput from pathwise depth. Report a native FB baseline without the dummy model.
3. Report every gradient metric against both `g∞` and the occupancy or ρ-weighted reference. Name one primary metric and correct for multiple comparisons. Add an explicit "inconclusive" category.
4. Contact: adopt Q's log-space survival (with the `∂_aℓ·∂_sπ` fix) and the Jacobian-growth stop-gradient. Replace the single JVP with a conservative bound, or report its false-negative rate. Quantify the truncation bias. Add ensemble-disagreement pessimism on the head, and Sobolev or Jacobian loss and a 32-step training horizon for the model.
5. Repair bounds: P's contact-local refinement; Q's retention of `ε_f` and `K_a` and a domination assumption for `Q'_s`; include P's variance term in both.
6. B/C targets: bootstrap at the last valid prefix state with `γ^{n_eff}` and a target-policy action. A policy mismatch is not a termination. Publish `n_eff` histograms.
7. Claims: drop or downgrade P-01 to a verification identity; keep P-02 and Q-02; re-register Q-01 with an absolute effect size; fix Q-03's `κ=1` wording.
8. State explicitly that the brief's hybrid objective overrides the literal Charter HC1 "exclusively F^T z" wording. Restate `behavior_z` preservation and executed-action Q. Add a drifting-B panel and a well-conditioned isotropic null (P's `A=I` toy is nearly collinear for `q∈[−0.02,0.20]`).
9. Do not cite the `VERDICT.json` PASS as evidence for any H. Rerun under the merged protocol.

**Confounds.** Order effect: P occupies the first slot in this order, and the length and polish of P's derivation may anchor the reading toward P. Q's strengths are mostly design choices that are easy to under-credit when read second. The Order 1 result should be compared before the Tie is finalized. Reviewer asymmetry: the P critique used a different review style from the Q critique (A is more severe on ablation, B is more severe on math), so row scores are partly reviewer-dependent. Neither reviewer saw Appendix B or the baselines. I did not independently re-derive either bound; scores rest on spot-checking against the reviewers' claims and my own read. The two candidates also use different toy plants (1-D contact vs hopper-torso), so their spike designs are not directly comparable. The 1-point margin is not a meaningful separation.
