# B03 Order-Swapped Adjudication (Order 2: P = Author B text, Q = Author A text)

Adjudicator: Sonnet 5.5, Methodology v1.0 §4 Step 4 and Appendix B.9.
Inputs read: Charter, brief, `order2_P.md`, `order2_Q.md`, review-A-on-B (critique of P), review-B-on-A (critique of Q), and `B03-SPIKE/VERDICT.json`.
Not read: `adjudication-agy-order1.md`, the baselines, and the text of Appendix B. B.5 and B.9 are applied below from the Charter and the brief only. Where the Appendix text would matter, I say so.
No scripts were run. The scores rest on reading and on the two blind critiques, which I spot-checked against the candidate text.

## 1. Eligibility Gate Check

| Gate | P | Q |
|---|---|---|
| §2.1 No BC / tracking fallback | PASS. Actor loss is `-E min_i F_i^T z_update`. Spike actors are fixed `nn.Linear` maps and are not trained. | PASS. The β-term is the Charter's optional single-step action-Q gradient. Probes are detached, but a "detached" probe regressing action labels needs an explicit firewall (Q §5). |
| §2.2 Behavior z vs update z | PASS. "Never substitute z_update" (P l.87). Immutable labels and the 50/50 mixture are kept. The two-pass BN order is only implied (MINOR). | PASS. Q trains on `z_actual`, and AAMC adds an immutable `a_applied` field. The BN order is not stated for the toy FB updates (MINOR). |
| §2.3 Motion-only single-frame B | PASS. | PASS. `c_geom` goes only to Q. |
| §2.4 Penetration vs invalid | PASS. P restates the full rule, including halting and the denominator (P l.122, l.215). | PASS with gap. Q mentions the split but omits the normalizer-rejection and halt predicates. |
| §2.5 Evidence vs claims | PASS. P labels the thresholds as prospective and quotes the VERDICT with caveats. | PASS. Q labels itself deductive or pre-registered. It says the VERDICT is "not independent evidence". |
| Brief §2 NPZ and no R1.3 / `infer_source_support_intent` | PASS. | PASS. Q rejects contact flags in `m` explicitly. |
| Hard-constraint violation found | None. | None. |
| B.5-style necessity-claim form (premises, conclusion, grade, test, falsifier) | Present for both claims. CAND-01 is a true Grade 1 theorem. | Present for all three claims. CAND-01 is graded 1 but not established (see §3). |
| Open blocker | The 278 vs 277 and 107 vs 93 baseline-04 schema mismatch is flagged by P. It remains unreconciled and gates ball-striking integration. | Q does not mention it. |

Both candidates are eligible. Neither is disqualified. Q's CAND-01 fails the grade it claims, and that is dealt with in §3, not as a gate failure.

## 2. Scores (brief.md rubric)

### Candidate P (Order 2)

| Dimension (wt) | Score | Justification |
|---|---:|---|
| Compatibility with kinematic-only NPZ (30) | 24 | `B` stays motion-only. Alternative A is rejected on the grounds that no deterministic `λ̂(m)` can equal two worlds. Synthetic metadata sits in separate tensors, and there is no static filtering. The review's MINOR point holds: the NPZ-derivable `q̈̂` enrichment named in brief deliverable 2(c) is never assessed. The "causal `q̈̂` in history" idea is only gestured at. |
| Rigor of aliasing analysis (25) | 20 | Prop. 1 is exact but conditional. It correctly refuses to claim a global `I(C;E)=0` and refuses to claim injectivity. Prop. 2 is the exact fiber condition plus the Bayes decomposition. It keeps `z=P(H)` inside the information set, so a planner that reveals the load escapes the bound, which is the correct treatment. It separates planner expressivity from actor reachability via `R_θ(o)` and the local rank test. It also separates objective-identifiability from information loss. Deductions: no `F`-observability statement (MAJOR). It misses that a 277→S⁹⁹ map must have learned collisions. Single-frame aliasing is not carried through to successor-occupancy aliasing. The rank test leaves `T` undefined and ignores saturation. |
| Diagnostic precision (25) | 14 | It gives a 128-latent bank, `F^T z` calibration, Q rank correlation, scan/ball mask in F and π separately, and a causal-history vs oracle-load comparison. All are sensible and pair-matched. But none has a threshold. The bank has no source distribution and no decision power. Cause (c) is inferred by elimination with no direct probe. Eval-time masking is confounded by covariate shift. |
| Spike falsifiability (20) | 12 | The specification is exact and reproducible: seeds, float64, `N=4096`, tolerances, and escape controls that restore zero risk. It is honest that it tests representability and the theorem, not emergence. But (a)–(c) are algebraic identities that can fail only through bugs. There is no learned 2×2 isolating F/π conditioning from B features. The VERDICT 0.895 is quarantined, not reconciled. The simulator extension is descriptive only, with no pass/fail line. |
| **Total** | **70** | |

### Candidate Q (Order 2)

| Dimension (wt) | Score | Justification |
|---|---:|---|
| Compatibility with kinematic-only NPZ (30) | 24 | Prop. 3.1 (any imputed `B''(m)=B'(m,c̄(m))` has the fibres of Prop. 1.1) is the cleanest argument in either document. Prop. 3.2 (85.7% wrong-`h` relabels) ties the argument to the 50% relabel rule. It also rejects contact-flag channels in `m`. The NPZ argument is over-stated: imputation does not make the encoder unusable, and the real prohibition is Charter §2.3 (review MAJOR). `q̈̂` is again not assessed. AAMC adds one replay field, which is compatible. |
| Rigor of aliasing analysis (25) | 16 | The strongest idea in either document is the R/K/I taxonomy and the point that FB aliasing lives in future occupancy Ψ, not in `B(m_t)`. It also explicitly gives `F` an observability role (the regime-mixture gradient bias). It models the `G_D` group, with the 229 vs 277 base-height distinction. But the load-bearing claims are unsound as written. Prop. 1.4 conflates measurability with learnability (CRITICAL). Case K treats `Δ_K>0` as sufficient for addressability, ignoring convex-hull occupancies (CRITICAL). Prop. 1.5 is an instantaneous nullspace, not a future-isokinematic boundary (CRITICAL). The Bayes floor conditions on `(o_low)` and omits `z`, so a planner can encode intent (CRITICAL). "Zero mean gradient along `n_a`" ignores parameter coupling through `J_θπ` (CRITICAL). The AAMC "reduces to Design 2" claim and the O(1)-gap divergence in the striking ε-variant are asserted, not shown. |
| Diagnostic precision (25) | 16 | It is the only candidate with numeric diagnostics and a stated attribution order: `D_P` (CEM gap, >0.1), `D_F` (<0.02), `D_B` (>50% null component, ≥0.8 L*). It also gives the 3-arm ablation with Wilson bounds. These are actionable. But `D_P` uses the suspect Q as its own oracle (CRITICAL). `D_F` measures sensitivity and uses impossible shuffled scenes. `D_B` presupposes the answer. The sequential order has no "unresolved" bin. `τ_dec` is not observable from replay. The ball-striking action-Q transfer is incomplete. |
| Spike falsifiability (20) | 12 | The positive controls and the VOID→INCONCLUSIVE rule make the test non-vacuous. The SVD rank gate must equal the predicted `dim N`. The probe-MSE band `[0.95L*, 1.05L*+σ²]` ties to an analytic floor. The privileged-`c` control shows the floor is informational. Deductions: the main positive result is a detached supervised probe, not an FB-trained actor. The linear-FB toy is under-specified. The ablation has no oracle arm. The `a_+ − a_-` factor-of-4 convention is ambiguous. Random postures are not feasible contacts. The thresholds are unjustified. |
| **Total** | **68** | |

Q's four dimension scores are 24+16+16+12=68. P is ahead by 2 points. That is inside scoring noise, and the difference comes from soundness, not ambition.

## 3. Principle Claim Adjudication (Appendix B.9)

Caveat: Appendix B text was not provided to me. I judge each claim by whether it identifies premises, a conclusion, a necessity grade, an operational test and a falsifier, and by whether the argument supports the grade claimed.

| Claim | Proposed grade | Adjudicated | Reason |
|---|---|---|---|
| P: C-B03-CAND-01 (information separation necessary for incompatible contact commands) | 1 | **Grade 1 accepted, but retitle.** | The premises are explicit and verifiable. The result follows from functional equality plus the conditional-variance decomposition. The escape (a planner that sees distinguishing history) is stated as scope, not a falsifier. The review's MAJOR point is right: the title says "routing into F/π/P/Q" is necessary, but the proof shows only that *some* distinguishing information is necessary, and that is nearly trivial. It also does not cover the headline 0.40 vs 0.60 m case, which `scan` distinguishes. The falsifier is algebraically impossible, so the claim is a theorem and its test is a bug-detector. Retitle it to "distinguishing information is necessary" and move the empirical content to whether simulator snapshots satisfy the premises. |
| P: C-B03-CAND-02 (context sufficiency requires action availability) | 1 | **Grade 1 accepted as an existence statement.** | Both feasibility conditions (observable context makes the action deterministic; the latent image contains it) are necessary and sufficient for representability. The claim explicitly excludes learning. It is modest and correct. |
| Q: C-B03-CAND-01 (isokinematic blindness of FB-only channels) | 1 | **Downgrade to Grade 3 (conjecture with a falsifier). Not accepted as necessity.** | P3 gives only instantaneous nullspace redundancy. P4 does not require intent to be independent of `z` or planner history, and the Bayes floor omits `z`. So the conclusion that "planner choice of z alone is insufficient" is contradicted by FB-tied branches that a planner can select. The gradient claim ignores parameter coupling. It conflates missing information with missing learning signal. Falsifier 2 tests critic fidelity, not the exact represented return. The repair review B gives is the right one: condition on all actor inputs, prove feasible equal-occupancy branches, and state only that equal occupancies give equal ideal linear FB returns. |
| Q: C-B03-CAND-02 (perceptive sufficiency, Case R) | 2 | **Grade 2 accepted, conditional.** | It is honestly empirical, and its premises and falsifier are concrete. It is not yet runnable, because the oracle arm and the trial unit are missing. The "e is necessary in both π and F" wording must be softened. It holds only when `e` is not redundant and the optimal action depends on it. |
| Q: C-B03-CAND-03 (prompt-side impossibility) | 1 | **Grade 1 accepted, narrowly.** | The claim is that a demo-NPZ-compatible encoder is `m`-measurable on demo prompts. That is valid, since the premise "the NPZ contains only m" fixes it. It is closer to a corollary of the contract than a research finding. The falsifier (an NPZ-only encoder that separates a `G_D`-orbit) correctly flags temporal features such as `q̈̂` as the one escape that Charter §2.3 would have to rule on. |

## 4. Disposition

**Recommend: P.** The margin is narrow (70 vs 68).
P wins on soundness. Its necessity claims are correct as stated, it keeps the planner's information set explicit, and its spike is reproducible. Q has better ideas and better diagnostics, but its headline claim (CAND-01) and its three-case theorem do not hold as written. A downgraded principal claim should not become the program's lead.

**Alternate: Q**, as the source of merge material and as the lead if the blocking repairs below are completed before spike lock.

**Mandatory Merge items (from Q into P)**
1. The R/K/I taxonomy, rewritten with the exposed-optimum condition for Case K and with "Case I" defined by *feasible, equal-occupancy trajectories*, not by an instantaneous null-space rank.
2. An `F`-observability proposition: if `o_F` omits `e`, the actor gradient is biased toward the averaged response, using the action-conditional posterior `p(c | ξ_p, a, z)` as review B requires.
3. Q's positive controls and the VOID→INCONCLUSIVE rule, plus the learned-collision measurement on real extracted frames. Negative controls need numeric thresholds.
4. `D_F`, `D_P` and `D_B`, repaired: use paired feasible scene interventions for `D_F`, simulator-return validation of the candidate latents for `D_P`, and a direct regime probe for `D_B`. Add an "unresolved/mixed" outcome and retrain-masked arms.
5. The 2×2 learned factorial {motion-only B, B+`q̈̂`} × {context in F/π, context masked at training} under the unchanged FB objective. Both reviews ask for it and neither candidate has it.
6. The `q̈̂` compatibility question under Charter §2.3 (single-frame or not, NPZ-derivable or not), resolved explicitly in one place.
7. Reconcile the VERDICT `0.895` against a stated convention (sum vs per-channel; `Δ`; paired or not) as a *pre-lock gate*. Fix the `a_+ − a_-` factor-of-4 convention.
8. Keep P's baseline-04 schema (278/277, 107/93) reconciliation as an explicit open blocker.
9. Add the compute-matched nulls (context-blind hierarchy, monolithic recurrent policy) and Q's 3-arm ablation, plus the oracle arm and the trial-unit definition.
10. P's CAND-01 retitle, and P's tied-branch point (a planner can select among FB-tied branches). The merged text must not carry Q's claim that planner choice is insufficient.

**Confounds.** The two candidates were generated under one packet from the same VERDICT. Both quote its numbers, and both reviews noted that the VERDICT carries no seeds, uncertainty or floor, so none of it counts as independent support. Order effects are possible. Under Order 2 the more conservative document (P) is read first, and Q's wider claim surface then draws more critical findings (6 CRITICAL against 0). Review B on Q is also visibly more adversarial than review A on P, so part of the score gap may come from reviewer severity, not from candidate quality. Neither reviewer had the baselines or Appendix B, and neither could check the schema claims. I did not read them either. The scores weigh claim-correctness above ambition. If Order 1 weights the richer diagnostics more heavily, Q could win, which is why Tie is not excluded. P and Q also differ in length and format, so a style bias toward the more formal P is possible. No simulator evidence exists for either candidate, and nothing here supports a claim that traversal or striking has been learned.
