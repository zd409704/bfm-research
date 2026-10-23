# C-Eng2-A-01 — Claim adjudication

Date: 2026-10-22. Role: assigned cross-family claim adjudicator, distinct from the claim author.

**Ruling: tighten-premises. State remains Candidate.** Retain the narrow formal Grade-1 candidate label; no grade promotion, lock recommendation, lock, or veto authority is granted. The exact bound survives. The statistical derivation is accepted only with the evaluation-test restriction recorded below. This document is an independent mathematical review, not a completed B.9.2 published-result item-match, formal-checker certificate, or qualified-human verification.

Read: `claims/C-Eng2-A-01/claim.md`; `packets/Eng-2/decision.md`; the claim section and supporting context in `packets/Eng-2/proposals/A.md`; `packets/Prin-3/source/method-Appendix-B.md`. The claim directory contained no existing sidecar files. Also inspected the relevant likelihood, calibration, ceiling, and harness provisions of `packets/Eng-2/drafts/A/PLAN.md`, and the roster. No spike, simulation, or empirical counterexample search was run.

## Mathematical findings

**Exact form (a): sound on the declared model.** Write `P_z` for the law conditional on `Z=z`, and define `β*_V(r) = sup E_1[φ(V)]` over measurable tests `0 ≤ φ ≤ 1` satisfying `E_0[φ(V)] ≤ r`. A detector is bounded by this supremum by definition. Every test of `(X,W)` lifts to a test of `(X,W,G)` by ignoring `G`; hence the second inequality follows by inclusion. Implementation family is irrelevant. This portion does not require evaluation-window independence.

For a true LR threshold test `φ`, with attained size `s` and power `p`, the Neyman–Pearson argument gives `p = β*(s)`. In the dominated representation, `(φ−ψ)(f_1−t f_0) ≥ 0` pointwise for any competing test `ψ`; integration and `E_0[ψ] ≤ s` give `E_1[ψ] ≤ E_1[φ]`. Include any alternative-only support in the rejection region. At LR atoms, a fixed boundary rule remains optimal at its attained size; randomization is needed only to fill unattained sizes. Thus `s ≥ r` implies `β*(r) ≤ p`. The lower FPR bound has the correct direction.

**Statistical form (b): the original proof leaves selection unresolved.** Fixing a threshold family does not generally make pointwise confidence intervals valid at a threshold selected using evaluation outcomes. The existing falsifier excludes evaluation-fitted thresholds, but premise 4 only fixed the family; the PLAN's ceiling instruction also says to choose a threshold by its lower bound. Its separate prohibition on evaluation tuning does not specify how that choice is made. This is a proof/specification gap, not an observed counterexample. A nested LR family can admit a dedicated selection-valid argument; no claim that every adaptive threshold rule is invalid is made here.

The adopted sufficient repair fixes the actual test independently of evaluation, including its threshold and randomization, with fixed sample sizes and independent window-level random draws. Independent calibration may choose that test. Conditional on calibration, null rejections are `Bin(n₀,s)` and alternative rejections are `Bin(n₁,p)`. For `δ = α/2`, the one-sided Clopper–Pearson bounds satisfy `Pr(L₀ > s) ≤ δ` and `Pr(U₁ < p) ≤ δ`, including the endpoint conventions `L₀(0)=0` and `U₁(n₁)=1`. Independence between these two counts is unnecessary for the union bound.

With probability at least `1−α`, both bounds hold. On that event, if `L₀ ≥ r`, then every eligible channel detector has power at most `β*_(X,W,G)(r) ≤ p ≤ U₁`. Therefore the probability of issuing a false ceiling certificate is at most `α`. This is an unconditional repeated-evaluation guarantee, not a claim of `1−α` conditional coverage given that a certificate fired. If `L₀ < r`, the procedure makes no certificate; it must not search the same evaluation data for a replacement under this proof. The guarantee is per cell, not simultaneous across all cells. Analytic exact power can supply the exact bound directly, subject to the same model and optimality checks.

**Full-genie qualification.** The claim needs the LR of the full observation. In density notation,

`Λ(x,w,g) = [p₁(x,w | g) / p₀(x,w | g)] · [p₁(g) / p₀(g)]`.

A conditional LR alone equals this joint LR only when the omitted factor cancels or is otherwise accounted for. The law of genie information must be defined under both hypotheses, including contact-template metadata under the null. Declaring a nuisance realization observed does not establish cancellation. Even when cancellation holds, unconditional power and its binomial sampling law remain tied to the declared distribution of that realization. A bound valid separately at every realization would need a separate conditional argument and does not follow merely from an aggregate FPR constraint. The unsupported assertion that full-genie validity survives any prior error has been removed; this enforces the existing fixed-model premise rather than adding a second narrowing.

## Disposition and required follow-through

1. Premise 4 now freezes the actual evaluated test and specifies the binomial sampling conditions. Record one B.9.6 narrowing event, counter **0 → 1**, for restricting the statistical branch to independently fixed tests. No empirical rescue or cross-claim narrowing is assigned. Event three would require retirement review; this is event one.
2. Before eventual sealing, the PLAN must identify the independent calibration procedure and the frozen test, or supply a separate selection-valid proof. Its conditional full-genie likelihood must be matched to the joint model. The PLAN was not edited or resealed in this adjudication.
3. NULL controls establish `β*(r)=r` only when both laws agree on the full reference observation. Confidence coverage does not guarantee a finite-sample certificate firing rate; an all-accepting unrandomized NULL reference illustrates why threshold design matters. Observed tier-order deviations require statistical and implementation review and are not, by themselves, proofs of likelihood mismatch. These are harness qualifications, not new scope-narrowing events.
4. Citation ablation survives: no biological premise is load-bearing. Nothing here establishes field necessity, hardware transfer, a ladder order, or task ratification. No other claim changes grade or state.
5. Any later lock nomination requires a B.9.2-acceptable independent verification matching the full joint-model NP argument, side-information inclusion, atom treatment, and the chosen statistical procedure item by item, followed by the human lead's signature. Cross-family agreement alone is not grade evidence under B.9.7.

The packet remains deferred under its existing common gate. No execution authorization or run artifacts are created by this ruling.
