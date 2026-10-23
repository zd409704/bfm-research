# C-Eng1-A-01: One-sided floor certificate from held-out detector performance

| Field | Value |
|---|---|
| **ID** | C-Eng1-A-01 |
| **Packet** | Eng-1, Proposal A |
| **Author family** | Opus (Eng-1 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family; not this author) |
| **Grade** | **1, narrow formal lemma.** This is an author derivation. It is a corollary of the KL data-processing step used in C-Prin2-E17 step 1, combined with exact binomial confidence bounds. Not independently verified. |
| **State** | **Candidate.** Not Locked and not recommended-for-lock. No veto authority. |
| **B.9.6 narrowing counter** | 0 |
| **Role** | This lemma justifies the XC-0 acceptance test. It is **not** a ladder edge and not an ordering claim. |

## Premises

1. `Z ∈ {0,1}` is a declared contact variable per window, as in C-P1-011 premise 1 and C-Prin2-E17 premise 1. `(X, W)` is the declared channel, meaning the export plus the registered side channels. There is one fixed probability model (C-P1-011 premise 4).
2. The detector `g` maps `(X, W)` to `Ẑ ∈ {0,1}`. It may use internal randomness independent of `Z` given `(X, W)`. It is **fixed before** the evaluation data are drawn, so thresholds are calibrated on a disjoint split.
3. The evaluation consists of `n₁` windows with `Z = 1` and `n₀` with `Z = 0`, drawn i.i.d. from the respective conditional laws `P₁`, `P₀`. Detector state is reset per window.
4. `TPR_L` is a one-sided exact (Clopper–Pearson) lower bound at level `α/2` on `TPR = P₁(Ẑ=1)`. `FPR_U` is a one-sided upper bound at level `α/2` on `FPR = P₀(Ẑ=1)`.

## Conclusion shape (invariant / one-sided lower bound)

With probability at least `1 − α` over the evaluation sample, if `TPR_L > FPR_U` then

`D(P₁^{X,W} ‖ P₀^{X,W}) ≥ d(TPR_L ‖ FPR_U)`,

where `d` is binary KL divergence. Consequently, if `TPR_L ≥ q` and `FPR_U ≤ r` with `r < q`, the channel meets the C-Prin2-E17 floor `d(q ‖ r)` at confidence `1 − α`.

### Derivation (author; requires independent check)

1. By data processing for relative entropy through the fixed kernel `g`, `D(P₁^{X,W} ‖ P₀^{X,W}) ≥ D(P₁^{Ẑ} ‖ P₀^{Ẑ}) = d(TPR ‖ FPR)`.
2. By the union bound over the two one-sided intervals, `TPR ≥ TPR_L` and `FPR ≤ FPR_U` hold jointly with probability `≥ 1 − α`.
3. On that event, `TPR ≥ TPR_L > FPR_U ≥ FPR`. Because `d(x‖y)` is increasing in `x` for `x ≥ y` and decreasing in `y` for `y ≤ x`, `d(TPR‖FPR) ≥ d(TPR_L‖FPR_U)`.
4. Steps 1 and 3 give the bound. With `TPR_L ≥ q > r ≥ FPR_U`, monotonicity gives `≥ d(q‖r)`.

## What it does NOT say

- **No certificate of absence.** If the detector fails to meet `(q, r)`, nothing follows about `D`. A better detector may exist (C-P1-011 scope, "estimation quality").
- It says nothing about which export fields are necessary. That question stays with C-P1-012 (Grade 2 Candidate).
- It does not cover the export alone unless `W` is empty or conditionally independent of `Z` given `X` (C-Prin2-E17 caveat).
- It does not make `(q, r)` task requirements. They must be task-stated, and spike placeholders are not task requirements (C-P1-012 H5).
- It does not certify `r = 0` floors.
- It says nothing about hardware, transfer, or ladder order.

## Scope

Any detector, any implementation family, on a fixed probability model with i.i.d. evaluation windows. In Eng-1 it applies to the planar fixture in `packets/Eng-1/drafts/A/spike-PLAN.md`.

## Falsifier / challenge mode

- **Formal:** an error in steps 1–3, for example a misapplied union bound, a wrong monotonicity direction, or a calibration that leaks evaluation data.
- **B.9.4(b) premise failure:** non-i.i.d. windows (shared episodes or detector state carried across windows), thresholds tuned on evaluation data, or an undeclared side channel. In these cases the certificate is void. The lemma is not refuted.
- **Empirical sanity (harness, not proof):** a NULL control (`P₁ = P₀`) should yield `TPR_L > FPR_U` at frequency ≤ α. A higher rate indicates a harness bug.

## Citation-ablation (B.8.7)

No evolutionary, developmental or anatomical premise is used. **Survives.**

## Lock path

This is not nominated. If it is ever nominated: B.9.2 item-match of step 1 to the published KL data-processing inequality and of step 2 to Clopper–Pearson coverage, checked by a non-author, plus the human lead's signature.
