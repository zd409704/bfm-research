# C-Eng2-A-01: One-sided channel-ceiling certificate from a genie Neyman–Pearson reference

| Field | Value |
|---|---|
| **ID** | C-Eng2-A-01 |
| **Packet** | Eng-2, Proposal A |
| **Author family** | Opus (Eng-2 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family; not this author) |
| **Grade** | **1, narrow formal lemma.** Author derivation: the Neyman–Pearson lemma, plus monotonicity of optimal power in side information, plus exact binomial bounds. Not independently verified. |
| **State** | **Candidate — tighten-premises.** Not Locked and not recommended-for-lock. No veto authority. May not gate any packet. See `adjudication/ruling.md`. |
| **B.9.6 narrowing counter** | 1 (evaluation-test restriction; see `upgrade-log.md`) |
| **Role** | Upper-side companion to C-Eng1-A-01 (lower side). Justifies the `CH_LIMIT` class in `packets/Eng-2/drafts/A/PLAN.md`. It is not a ladder edge and not an ordering claim. |

## Premises

1. `Z ∈ {0,1}` is a declared contact variable per window. `(X, W)` is the declared detector channel: the export plus the registered side channels. There is one fixed probability model (C-P1-011 premise 4).
2. `G` is additional information (the "genie": contact template, nuisance realization). For each `z`, the joint law of `(X, W, G)` given `Z = z` is defined on the same probability model. `G` is used only by the reference test, never by the detectors whose ceiling is claimed.
3. `β*_{V}(r)` is the Neyman–Pearson power at size `r` for testing `Z=0` vs `Z=1` from observation `V`, with randomization allowed.
4. Evaluation windows are i.i.d. given `Z`, with positive sample sizes fixed before evaluation. The actual reference test (true joint likelihood ratio, threshold `t*`, and any boundary-randomization rule), not just its threshold family, is fixed independently of evaluation data; independent calibration is allowed. Any randomization uses fresh independent draws per window. Coverage in (b) is per declared cell; evaluation-based threshold search requires a separate selection-valid proof or simultaneous bounds.

## Conclusion shape (impossibility / one-sided upper bound)

**(a) Exact form.** For every detector `g` on `(X, W)`, possibly randomized, with `FPR(g) ≤ r`: `TPR(g) ≤ β*_{(X,W)}(r) ≤ β*_{(X,W,G)}(r)`.

**(b) Statistical form.** Let `t*` be a threshold of the likelihood-ratio test on `(X,W,G)` such that the one-sided Clopper–Pearson lower bound (level α/2) on its FPR satisfies `FPR_L(t*) ≥ r`. Let `TPR_U(t*)` be the one-sided upper bound (level α/2) on its TPR. Then, with probability ≥ 1 − α, every detector on `(X, W)` with FPR ≤ r has `TPR ≤ TPR_U(t*)`. In particular, if `TPR_U(t*) < q`, no detector on `(X, W)` meets `(q, r)` on this probability model.

### Derivation (author; requires independent check)

1. Any detector on `(X, W)` is a detector on `(X, W, G)` that ignores `G`. So the set of size-≤r tests on `(X,W)` is contained in the set on `(X,W,G)`, which gives the second inequality of (a). The first inequality is the NP lemma: the LR test is most powerful at its size.
2. LR tests with thresholds `t` have power non-increasing as size decreases. On the event `FPR(t*) ≥ FPR_L(t*) ≥ r`, `β*(r) ≤ β*(FPR(t*)) = TPR(t*)`. A true LR test is optimal at its attained size, including at atoms with a fixed boundary rule. Randomization permits intermediate target sizes; the reference need not attain size exactly `r`.
3. On the event `TPR(t*) ≤ TPR_U(t*)`, the chain gives `β*(r) ≤ TPR_U(t*)`.
4. The two one-sided events each fail with probability ≤ α/2. Union bound: joint coverage ≥ 1 − α.
5. If the LR test's power is computed analytically from the exact model (e.g. a Gaussian matched filter with deflection `d'`), (b) reduces to (a) with no sampling term. The MC estimate is then only a harness check.

## What it does NOT say

- **No statement about the target plant.** It covers only the declared probability model, i.e. the simulated fixture. A fixture `CH_LIMIT` does not show that effort information is absent on hardware.
- **Not a statement about which fields are necessary.** Export-field necessity stays with C-P1-012 (Grade 2 Candidate). A ceiling on one channel says nothing about channels not modeled.
- **No grade change to any claim** follows from applying it (B.9.8). Fixture data relevant to C-P1-012 Factor E are routed to that claim's adjudicator for B.9.6 accounting. This lemma does not self-assign whether they count.
- It does not make `(q, r)` task requirements (C-P1-012 H5).
- If the reference uses only partial genie knowledge with a **marginalized** nuisance (G-marg in the PLAN), its optimality holds only under the declared nuisance prior. G-full also requires the correct joint model: conditioning on a nuisance realization does not by itself establish the joint LR or prior-independent aggregate coverage. See `adjudication/ruling.md` for the conditional/joint distinction.
- Nothing about ladder order or hardware transfer.

## Scope

Any detector, any implementation family, on a fixed probability model with i.i.d. evaluation windows. In Eng-2 it applies to the Eng-1 S2a-XC fixture (PLAN v2 sha256 `3d7b9af6…`), re-used by `packets/Eng-2/drafts/A/PLAN.md`.

## Falsifier / challenge mode

- **Formal:** an error in steps 1–4, for example a wrong direction of the size/power monotonicity, misuse of the lower FPR bound, or LR atoms mishandled.
- **B.9.4(b) premise failure (voids, does not refute):** the genie test is computed with a likelihood that differs from the simulator's (a model mismatch, so it is not the true LR), evaluation windows that are not i.i.d., or a threshold fitted on evaluation data.
- **Empirical sanity (harness, not proof):** in a NULL control (`P₁ = P₀` on the full reference observation), `β*(r) = r`. Finite-sample firing frequency requires a separate power analysis. Apparent empirical tier-order violations can arise from sampling or harness errors and require investigation; they do not alone establish likelihood misspecification (PLAN H3/H4).

## Citation-ablation (B.8.7)

No evolutionary, developmental or anatomical premise is used. **Survives.**

## Lock path

This is not nominated. If it is ever nominated, it needs a B.9.2 item-match of step 1 to the NP lemma and of step 2 to monotonicity of the NP power function, a check of Clopper–Pearson coverage by a non-author, and the human lead's signature.
