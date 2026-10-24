# Order-Swapped Adjudication — Packet B01 (Presentation Order 2)

**Adjudicator:** Sonnet 5.5 (order-swapped pass). **Method:** v1.0 §4 Step 4, Appendix B.9. **Tie margin:** 5.0 points.
**Inputs read:** `PROGRAM_CHARTER.md`, `packets/B01/brief.md`, `anonymized/order2_P.md`, `anonymized/order2_Q.md`, `reviews/review-A-on-B.md` (critique of P), `reviews/review-B-on-A.md` (critique of Q). I also read the pinned method's §11.5 and Appendix B (B.2–B.9) from the pinned copy named in P's header, because the gates are defined there. I did **not** read `adjudication-agy-order1.md`. Baseline files 01/03/05 were not read, so baseline claims that neither the charter nor the brief confirms are marked **unverified**.

**Order-2 mapping, taken from the files themselves.**
- P is the candidate whose header says "Primary Author B". Its critique is `review-A-on-B.md`.
- Q is the candidate whose header says "Primary Author A". Its critique is `review-B-on-A.md`.

I weighed both critiques against the candidate text. Where I rely on a reviewer claim, I say whether I re-derived it.

---

## 1. Eligibility Gate Check

Appendix B gates apply before rubric ranking (B.9.5). I checked the charter §2 hard constraints, the brief §2 constraints, and the B.3/B.4/B.9 claim requirements.

| Gate | P | Q |
|---|---|---|
| §2.1 No BC or tracking penalty | PASS. The actor is updated only on −min_k F_kᵀz (§2.2 step 6) and the hybrid objective. No action MSE or phase clock. | PASS. Same. |
| §2.1 "Hybrid actor update" tension. Review of Q raised this as CRITICAL. | Not a violation. Charter Mission item 3, H3, and brief deliverable 2(iii) all authorize a hybrid world-model head with an FB terminal bootstrap. P additionally gates the hybrid behind diagnostics, which makes it safer than Q. | Same finding. I **reject** the review's CRITICAL rating. Q's hybrid is a charter-sanctioned design. The reviewer's point stands only in the sense that Q's own reward head has no diagnostics gate (see Row 2). |
| §2.2 `behavior_z` / `z_update` separation | PASS. Two BN updates, then freeze, then online-B 50/50 relabeling under `no_grad`. `behavior_z` is immutable. The task critic uses `z_actual`. P adds a byte-identical sentinel contract fixture. | PASS in the default design. The optional colouring (site ii) writes the coloured vector as `behavior_z`/`z_actual`, which is consistent but still gated off. |
| §2.3 Single-frame, motion-only B | PASS. | PASS. |
| §2.4 `severe_penetration` vs `invalid` | PASS, with a minor deviation. Nonfinite input "aborts that update and triggers inspection", which is weaker than the charter's halt. | PASS, with a minor deviation. The tracker halts only after 2 consecutive failures. This is an estimator-failure rule, and `invalid` rows are separately excluded. Q does not state the halt-run rule for invalid source data. |
| §2.5 Verified vs unproven | PASS. No results are claimed. | PASS. The NumPy check is explicitly limited to algebra. **But** it reports numbers that I find to be wrong (see Row 1). This is a verification-honesty defect, not a hard-constraint breach. |
| Brief §2: bilinear F·B and sphere √d_z preserved | PASS. W appears only on the reward side. | PASS. |
| Brief §2: causal, bounded Σ̂; target-EMA interaction specified | PASS. Detached FP64 EMA of the target-B Gram, with a frozen tuple per update. | PASS. Tracks the target-B Gram, with W^(t−1) causal. |
| B.3 claim form: premises, shape, implementation independence, falsifier | PASS for CAND-01 and CAND-02. Both are explicit that they do not claim an inverse implementation is necessary. | CAND-01 passes in form only. CAND-02 fails on substance (Section 3). CAND-03 passes in form. |
| B.4 / B.9: claims stay Candidate, no veto, no score-based promotion | PASS. Both claims are Candidate, and P states that independent proof checking and human signature are outstanding. | PASS. Q states the same. |
| §11.1 isolation | **Provisional.** P discloses unrestricted filesystem permissions. Q makes no isolation statement. I have no enforcement evidence for either. | Same. Both are **Provisional** until the orchestrator supplies logs. |
| §11.5 framed agreement | See Section 3. | See Section 3. |

**Gate outcome: both P and Q are eligible for rubric ranking.** No hard-constraint violation was found in either. Both outcomes are Provisional under §11.1.

---

## 2. Scores (brief.md rubric: Math 30 / Stability 25 / UFO 25 / Spike 20)

### Candidate P

| Row | Max | Score | Justification |
|---|---:|---:|---|
| Exact Mathematical Derivation | 30 | **27** | I re-checked these items and found them correct. (i) A density-readout / raw-kernel / extra-inverse table whose terms are exact (§1.1). (ii) A correct statement that z_g = B(g) gives zero Gram bias in the density readout. (iii) Eqs. (1)–(4) in eigen-coordinates. (iv) The Kantorovich bound (5). (v) The envelopes a_κ = d/(1+(d−1)κ) and b_κ = dκ/(κ+d−1). (vi) The Rényi-2 lower bound (7). (vii) The resolvent bound (10). (viii) The damping formulas (9). (ix) The exact spherical-projection counterexample for hard whitening, diag(4/3, 2/3). Review A found no algebraic error, and I did not either. Deductions: the "joint" (κ,R) bound (6) and bound (13) are vacuous at d=256, since δ ≤ d√(D/2) < 1 only for D ≈ 10⁻⁵ (Review A, confirmed by my arithmetic). The hybrid reward multiplies the target-B Gram by an online-B z, and this coordinate mismatch is logged but not bounded. P does not tie h = q − ΣF to the least-squares FB minimizer. |
| Stability Under Non-Stationary ρ | 25 | **19** | Strengths: the damping rule (12) provably gives ‖W‖ ≤ 20 and κ ≤ 100. The support projector P = ΣΣ⁺ is used for rank deficiency. Cholesky retry rules, FP64, checkpointed covariance, and a drift-lag bound are all given. A 131072-frame calibration is used to diagnose rare directions. The hybrid is gated and the gate-open fraction is logged. Deductions (Review A, which I find well-founded): (a) the split-half gate uses unwhitened relative operator norm, which is dominated by λ_max and cannot detect disagreement in the λ_min directions that W amplifies by up to 20×; (b) the representation-residual gate ‖q−ΣF‖/‖q‖ ≤ 0.10 is not scaled by W, yet the error is hᵀΣ⁻¹z; (c) there is no per-command safeguard for out-of-support demo prompts; (d) there is no hysteresis when the gate flips the actor objective between online-F and damped-prefix/target-tail; (e) the production gate (‖C−I‖ ≤ 0.5, implying κ(C) up to 3) contradicts the spike gate κ(C) ≤ 2. |
| Compatibility with UFO Update Contract | 25 | **23** | The placement table is complete and well argued: no whitening at z_update, expert/near prompts, or the standard actor; the solve only at the hybrid reward. The update order, stop-gradient list, and frozen tuple are explicit. A contract fixture checks BN counters, byte-identical `behavior_z`, resume at update 2173, and the retained-severe-penetration / rejected-nonfinite rows. Deductions: target modules copying online BN buffers (step 2) is attributed to the baseline, but it is **unverified** against baseline files and not in the charter (Review A). The BN jumps this induces in target coordinates are conceded but not modelled. The nonfinite-input rule is "abort update" rather than "halt". |
| Spike Falsifiability | 20 | **14** | Strengths: this is an excellent pre-registration. It fixes seeds, an attempt cap, a budget, INCOMPLETE semantics, and per-cell (q,d) 4-of-5 pass rules. It specifies six arms, including ORACLE-DAMP, DIAG-DAMP and STALE-DAMP, which separate damping error from estimation error and from lag. Gates are numeric. Deductions (Review A, which I accept): (a) B is analytic in every fixture, so the H1 premise (L_orth leaves anisotropy) is never tested; (b) 229/277 enter only as nuisance dimensions; (c) every fixture has h ≡ 0, so the residual gate and the h-amplification are never exercised; (d) fixture C uses exactly d states with an invertible B, so ORACLE reachability is perfect by construction, and the n ≫ d regime behind H1's goal-reaching claim is untested; (e) drift is a spectrum-preserving rotation, which makes the moderate-stage gates easy; (f) no streaming value-error gate, and no effective-rank gate on a learned Σ_B (the brief names both); (g) the rejected alternatives are not arms; (h) the candidate-action distribution is unspecified and the seed bootstrap is not meaningful (126 multisets). |
| **Total** | **100** | **83** | 27 + 19 + 23 + 14 |

### Candidate Q

| Row | Max | Score | Justification |
|---|---:|---:|---|
| Exact Mathematical Derivation | 30 | **22** | Strengths: the closed forms are correct and instructive. I checked (1.1) F·z = Ψᵀ Σ⁻¹ z, (1.6) E‖r̃−r‖² = tr Σ⁻¹ − d, (1.7) relMSE = 1 − λ_H and cos_pop = √λ_H, Lemma 1 (Kantorovich), and the H-step bias (1.11). The mechanism that L_orth charges at most ½ for a collapsed direction, while reward error scales as 1/λ, is a good insight that ties directly to H1. The density kernel vs embedding kernel table is correct. Deductions, each re-derived by me: (a) the "numerical checks" are wrong. At κ=28.3 the bound 2√κ/(1+κ) is 0.363, not 0.188, and the overshoot (1+κ)/(2√κ) is 2.75, not 5.32 (5.32 is √κ). At κ=96 the overshoot is 4.95, not 9.80. Q presents these as verification, so its stated standard of checking is not met (Review B, confirmed). (b) C-B01-A-01(c) gives bias Ψ_Hᵀ(ΣM−I)Σ⁻¹z. The correct expression is Ψ_Hᵀ(M−Σ⁻¹)z, and the two differ unless M commutes with Σ. P4 does not impose that (Review B, confirmed). (c) θ_mis is bounded over the whole sphere, but attainable embeddings need not contain the extremizer. The B(i)=√d eᵢ, unequal-ρ example gives zero rotation with κ>1 (Review B, confirmed), so "self-identifying only under isotropic Gram" is not true as stated. (d) G1 applies the E[zzᵀ]=I identity to a 50/50 sphere/goal mixture (Review B, confirmed). (e) The claim that near-null directions carry zero in-support energy holds only for exactly null directions. |
| Stability Under Non-Stationary ρ | 25 | **18** | Strengths: μ_t = max(μ₀, λ̂₁/κ_cap) caps ‖W‖ with a simple relative floor. `clamp_min(0)` plus μ means no singular inverse is ever formed. Trace-invariant integrity checks, an off-support leverage guard with a masked-fraction gate, a Woodbury rejection, and an eigh/Cholesky cost plan are all given. Deductions: (a) the leverage guard drops a branch and its tail, which is a policy-dependent truncation bias outside (1.11)/(1.13), and a ≤1% step count does not bound lost value (Review B, accepted). (b) Singular regimes are called a target regime, but S1/S3 use Σ⁻¹ᐟ² and Σ⁻¹ exactly with no support-restricted diagnostics. (c) The functional drift of target-F is not bounded (a half-life is not a lag bound). (d) Q has no residual-h gate at all. (e) At κ=1000 the default μ = λ_max/1000 gives ≈0.25 damping relMSE even with a perfect estimator, so G2's 0.15 fails for non-estimator reasons (Review B, confirmed by formula). Q is less elaborate than P but has no worse gate-calibration defect than P's operator-norm gate. |
| Compatibility with UFO Update Contract | 25 | **20** | The default is fully compliant: no whitening at z_update, expert/near, or the standard actor, and mandatory only at the hybrid head. The table with code-level assertions is good. The stop-gradient table is explicit, and Q correctly shows that W at the actor would optimize Σ⁻²z. Deductions: (a) the optional Σ-colouring of expert/near prompts uses a target-B Σ̂ on an online-B vector, so the claimed k_I effective reward does not follow (Review B, accepted). Zero-norm handling after projection is unspecified. (b) The halt rule for `invalid` source data is not stated (it covers only the two-failure tracker rule). (c) The BN-freeze / normalizer timing for colouring is unspecified. Colouring is gated and off by default, so these are contained. |
| Spike Falsifiability | 20 | **14** | Strengths: it includes S2, a miniature joint FB training run with the 50/50 z_update sampler that directly tests the H1 premise, with explicit CONFIRMED and REFUTED bands and a legitimate negative outcome. It has a value-bias gate (G3), a gradient-cosine gate (G4), a null control at κ=1, a controlled-κ sweep, an R2 (dual-ascent) arm, an n ≫ d regime, and an off-support demo cluster. Deductions: (a) erank is logged but never gated, although §1.3 says it is. (b) G1's population identity is wrong for the mixture. (c) G4's +0.05 improvement is unattainable when RAW already exceeds 0.95. (d) The Wilson-bound difference is not a CI for the paired difference. (e) R2 retrains B, so it cannot share B checkpoints with the other arms, and R2+W is promised but not registered. (f) The diagonal-scale-then-project procedure does not give a prescribed κ. (g) Several gates are not tied to an exact oracle for the damped target. |
| **Total** | **100** | **74** | 22 + 18 + 20 + 14 |

**Margin: P − Q = 9.0 > 5.0 tie margin.**

---

## 3. Principle Claim Adjudication (Appendix B.9)

All claims are Candidate. None is eligible to lock now. Locking needs independent proof check plus human signature (B.9.2), and no benchmark can supply that (B.3.5, B.4).

### 3.1 Framing and agreement (§11.5)
Both candidates place the explicit dual conversion Σ⁻¹ **only** at the hybrid reward, and neither places it at z_update, expert/near prompts, or the standard actor. The brief frames this decision directly (deliverable 2 asks "whether and where" it enters (i)/(ii)/(iii)). Both also reject the same two alternatives: hard batch whitening inside B, and adaptive orthogonality dual ascent. This is **framed agreement** that adds no weight, and I record it as **possible framing-driven convergence**. P says as much itself. Neither candidate's necessity claims gain anything from the other's agreement (B.9.7).

### 3.2 Claims by P

**C-B01-CAND-01 (unique dual reward for a fixed full-rank command), Grade 1.** *Mathematically correct.* E_ρ[B Bᵀ a] = Σa, and Σ is SPD, so a_z = Σ⁻¹z is unique, and the value-equivalence half follows under a spanning family of F. Premise sets are explicit and the claim separates the encoding invariant from approximate-density cases. The falsifier is honest that only premise violations can arise. *Weight:* Review A is right that the necessity is definitional. It restates brief §1(1) and cannot exclude any route that does not use an explicit linear-span reward. It is an invariant (a lemma), not a veto-grade necessity claim. The "fixed finite outcome space" premise should be given in measurable form. **Adjudication: accept as a Candidate Grade-1 lemma. Not a veto source.** Keep the premise split (encoding invariant vs value equivalence).

**C-B01-CAND-02 (unobservable latent directions are not recoverable), Grade 1.** *Correct and tight.* If n ∈ ker Σ then nᵀB = 0 a.s., so F and F+tn agree on all replay products but differ in readout by t·nᵀz. This is a valid impossibility under its stated premises, and it correctly rules out "damping recovers missing skills". It is mathematically light but properly scoped. **Adjudication: accept as Candidate Grade 1.** It is of real use as a guard against overclaiming on rank-deficient early replay.

### 3.3 Claims by Q

**C-B01-A-01 (no scalar-calibrated raw intrinsic reward is FB-consistent when κ>1), Grade 1.**
- *(a)* M = Σ⁻¹ is necessary and sufficient for a common M across all z. This is correct and is the same fact as P's CAND-01.
- *(b)* The bound |Fᵀ(cΣ−I)z| ≥ ((κ−1)/(κ+1))‖F‖‖z‖ holds for the operator norm. P3 (F spans) does not give an attainable F aligned with the residual direction, so the pointwise form is unsupported (Review B, accepted).
- *(c)* The stated hybrid-bias formula is wrong (the correct form is Ψ_Hᵀ(M−Σ⁻¹)z).

**Adjudication: Candidate, and narrowed.** Only (a) survives as a Grade-1 lemma. (b) and (c) need repair and a fresh proof check before they can be considered. The falsifier should list separate counterexample criteria for each part. The scope-narrowing counter (B.9.6) should log this as event 1.

**C-B01-A-02 (single-frame prompts are self-identifying only under isotropic Gram; Σ-colouring is the consistent correction), Grade 1.**
- *Defective as stated.* The unequal-ρ identity-transition example (B(i)=√d eᵢ, Σ = d·diag(ρ), κ>1) gives θ_mis = 0 on every attainable goal, so isotropy is **not necessary** for self-identification. The Kantorovich bound is a supremum over the whole sphere, not over the image of B.
- The "invariant" half (the effective reward is proportional to k_I iff A = cΣ) is a correct identity.
- The statement that inverse whitening is "exactly the wrong correction" is conditional on the whole-sphere extremal case.

**Adjudication: Candidate, not acceptable as stated.** Downgrade to a conditional statement over a specified embedding set, or retire. This is scope-narrowing event 2. Do not promote.

**C-B01-A-03 (a Gram-tracking role R-Σ is obligatory for hybrid FB + world-model heads), Grade 2.**
- *Strengths:* the functional-role form fits B.2 Grade 2. Implementation independence is stated (explicit EMA, exact orthonormality, or a learned dual head are all admissible). A concrete operational realization test (splice residual, ≥2× improvement at κ≥10) satisfies B.9.3 in form. The R2 arm functions as a logged serious attempt.
- *Weaknesses:* the competence class is defined by the proposal's own architecture (a head spliced to a tail), so the necessity follows from design choice more than from the task. Its support rests on CAND-01(c), whose formula is wrong, although the qualitative result (nonzero bias when M ≠ Σ⁻¹) survives. B.9.2 requires a logged failed attempt to build a system without the role, and the human lead's signature, neither of which exists yet. The mere existence of an R2 arm in a spike is not that attempt.

**Adjudication: Candidate Grade 2, retained but not weighted.** It stays as a design obligation to state how the role is realized. It cannot veto and should not appear in the mainline rationale until (c) is corrected and the upgrade-log attempt is run.

**Net on claims:** P's two claims are smaller but correct. Q's three claims are more ambitious, with two carrying proof errors. Under B.9 the more modest, correct set is the better-governed one.

---

## 4. Disposition

**Recommend: P**

P scores 83.0 against Q's 74.0. The margin of 9.0 exceeds the 5.0 tie margin. The decision rests on three points, in order of weight.
1. P's derivations contain no error that I or the reviewer could find. Q has a verifiable numerical misreport, a wrong hybrid-bias formula, and an over-general necessity claim with a counterexample.
2. P's contract compliance and stability engineering are the more thorough, including a hard-gated hybrid with logged gate-open fraction.
3. P's necessity claims are correctly scoped. Q's are not.

**Alternate: Q.** Q holds the stronger empirical design for the **H1 premise** (S2, a learned-B run under drift, an n ≫ d regime, value-bias gate) and the simpler damping rule. If the orchestrator wants the H1 premise tested within B01 itself rather than deferred, Q's spike structure is the better skeleton. Q becomes the lead only if its Row-1 errors are corrected, in which case the gap would narrow, though I would not expect it to close below the margin.

### Mandatory Merge Items

**Into P from Q (required before spike lock):**
1. Add a learned-B stage modelled on Q's S2. It trains a miniature FB system with the exact UFO z_update sampler under a drifting synthetic ρ, with pre-registered CONFIRMED/REFUTED bands on κ and λ_H, and it gates effective rank on the **learned** Σ_B. P currently has no test of the H1 premise.
2. Add a streaming value-error gate (Q's G3: H-step bias vs RAW), plus the damped-prefix / undamped-tail mismatch that P's own (13) predicts.
3. Add an n ≫ d fixture with a rank-d B, and a non-rotational (affine) drift stream, per Review A.
4. Add Q's R2 (dual ascent) arm, matched on training budget, as P itself promises a comparator. Add R2+W.
5. Add Q's off-support leverage diagnostic ℓ(ŷ) as a **monitor**. Do not adopt its branch-dropping rule, since that rule changes the objective (Review B).
6. Add Q's null control at κ=1 (all arms agree within a stated tolerance).

**Into P from the critique of P (required):**
7. Replace the split-half gate with a whitened discrepancy ‖Σ̂^(−1/2)(Σ₍₁₎−Σ₍₂₎)Σ̂^(−1/2)‖, and scale the residual gate to hᵀWz (or ‖Σ^(−1/2)h‖/‖Σ^(−1/2)q‖).
8. Add hysteresis or a minimum dwell time for the hybrid gate, and simulate toggling in the spike.
9. Add a per-command safeguard for out-of-support prompts (for example z^T W z/‖z‖² or per-command split-half agreement of Wz).
10. Make the production gate (‖C−I‖) consistent with the spike gate on κ(C).
11. Pre-register the candidate-action distribution and the expected RAW agreement for fixture C. Replace the seed bootstrap with exact paired ranges.
12. Confirm against baseline 05 that the target-BN buffer copy is baseline behaviour and not new mechanism. Add a BN-jump (affine) drift term to the streaming fixture.
13. Align the nonfinite-input rule with the charter §2.4 halt-run requirement.

**Corrections required of Q if it is carried forward:**
14. Correct the Section 1.2 numerical checks (bound 0.363 and overshoot 2.75 at κ=28.3; 4.95 at κ=96) and re-run the verification before it is cited.
15. Correct CAND-01(c) to Ψ_Hᵀ(M−Σ⁻¹)z; restate (b) so it asserts only the operator-norm bound unless a coverage premise is added; restrict CAND-02 to a specified embedding set or retire it.
16. Replace G1's identity with tr[(Σ−2I+Σ⁻¹)C]/tr(Σ⁻¹C) for the mixture, and add an erank gate.

**Claim handling.** Carry P's CAND-01 and CAND-02 forward as Candidate Grade-1 lemmas. Carry Q's A-01(a) as the same lemma, merged with P's CAND-01. Hold Q's A-02 and A-03 as Candidate, flagged as narrowed (scope-narrowing counter at 2). None may veto anything.

### Confounds

- **Isolation (§11.1) is unproven for both candidates.** P discloses unrestricted filesystem permissions, and Q is silent. Both claim no sibling-draft reading, but that rests on self-report, not a tool-log breach audit. Every result here is **Provisional** until the orchestrator supplies that audit.
- **Framing-driven convergence (§11.5).** Both candidates make the same placement decision and reject the same two alternatives. The brief frames that decision, so its agreement is not independent evidence. It does not help P over Q or vice versa.
- **Order and presentation.** This is the order-swapped pass. P and Q are the reverse of Order 1, so any position bias should be visible as a score discrepancy between the two passes. I did not read the Order-1 report. Reconciling the passes belongs to the orchestrator.
- **Review asymmetry.** The reviewers differ in depth. Review A (on P) re-derived every equation and ran numerical re-implementations, and it found only scope and calibration issues. Review B (on Q) found concrete counterexamples and arithmetic errors. Part of P's margin therefore reflects how little a hostile reviewer found. I discounted for this by re-deriving the contested items myself: Q's numerical misreport, the CAND-01(c) formula, the CAND-02 counterexample, and P's bound (6) vacuity. I did not independently run any code. I did not verify P's simulated claims (the §1.5 gradient counterexample and the §3.1 diag(4/3, 2/3) example) beyond checking the algebra by hand.
- **Unverified baseline attributions.** Several mechanics that both candidates attribute to baselines 01/03/05 (BN-buffer copy to target, 10–20° near-prompt rotation, twin-min tail) were not confirmed. I did not read the baselines. If one of them is new mechanism, P's UFO score is affected more than Q's.
- **Different rubric surface.** P is longer and more exhaustively pre-registered, while Q has the more informative experiment design. The rubric rewards both, and my 14/14 spike scores are a judgement that P's rigor and Q's coverage offset each other. A reasonable adjudicator could shift ±2 on that row, and that would not change the recommendation.
- **Hybrid-authorization disagreement.** I overrode Review B's CRITICAL finding on charter §2.1, because Mission item 3, H3, and brief deliverable 2(iii) authorize the hybrid. If the orchestrator reads §2.1 more narrowly, that applies to both candidates, since both use a hybrid head.
- **No empirical evidence.** All scores reflect proposals and pre-registrations. Neither candidate has results, and none should be inferred. The charter §2.5 boundary holds.
