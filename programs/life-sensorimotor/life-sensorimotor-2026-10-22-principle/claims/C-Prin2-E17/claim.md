# C-Prin2-E17 — Edge S2a → S2 (contact observability floor available to contact-aware interaction)

| Field | Value |
|---|---|
| **Edge** | S2a → S2 |
| **Author family** | Opus (Prin-2 Author A) |
| **Claim adjudicator (roster)** | Codex gpt-6-astra high (cross-family) |
| **Grade** | **Reading A: Grade 1, formal and conditional.** It composes two standard data-processing inequalities. Its application to the target stack is conditional on a side-channel audit. **Reading P: Grade 3, quarantined.** |
| **State** | Candidate |
| **B.9.6 narrowing counter** | 0 |
| **Recommended adjudicator action** | **recommended-for-lock (narrow formal form only), conditional.** See §Lock path. Candidate-stay until verification and the human signature are in place. This is the only edge Author A nominates. |

Stage meanings: Author-A W-defs (`proposals/A.md` §1).

## Premises

1. **Contact variable.** `Z ∈ {0, 1}` indicates whether a declared non-support contact of a declared class occurs in a declared window. The class is set by duration, magnitude and location (C-P1-012 premise 3); the variable by its window and resolution (C-P1-011 premise 1). A finite-alphabet `Z`, for example contact link identity, is handled in the Fano form below.
2. **S2 task specification (task-stated, not a spike threshold).** S2 competence requires that some decision `Ẑ` reachable by the S2 tier achieves `TPR ≥ q` and `FPR ≤ r` per window, with `0 ≤ r < q ≤ 1`. If `r = 0`, the floor is infinite: the class-conditional laws must be mutually singular. Alternatively, it requires *response actions* `A` whose admissible sets are disjoint between `Z = 0` and `Z = 1`. In that case the required response itself defines a detector `Ẑ = 1[A ∈ S₁]`, with the same `q`, `r`.
3. **Channel structure.** `Z → (X, W) → Y → Ẑ` is a Markov chain. Here:
   - `X` is the body-loop export.
   - `W` is every upper-layer-side source correlated with `Z` that is not derived from `X`: vision, tactile, audio, and the upper layer's own commands and efference copies (C-P1-011 premises 2–3).
   - `Y` is everything the S2 tier holds.
4. One fixed probability model over `(Z, X, W, Y)` (C-P1-011 premise 4).

## Derivation (author; requires independent check)

Let `P_z` be the law of a variable conditioned on `Z = z`, and let `d(x‖y) = x log(x/y) + (1−x) log((1−x)/(1−y))` be binary KL divergence.

1. **Data processing for KL divergence.** `D(P₁^{X,W} ‖ P₀^{X,W}) ≥ D(P₁^{Y} ‖ P₀^{Y}) ≥ D(P₁^{Ẑ} ‖ P₀^{Ẑ}) = d(TPR ‖ FPR)`.
2. **Monotonicity.** `d(x‖y)` increases in `x` on `x ≥ y` and decreases in `y` on `y ≤ x`. Premise 2 gives `TPR ≥ q > r ≥ FPR`, so `d(TPR‖FPR) ≥ d(q‖r)`.
3. **Floor.** Combining 1 and 2: `D(P₁^{X,W} ‖ P₀^{X,W}) ≥ d(q‖r)`. Example: `q = 0.95`, `r = 0.01` gives `d = 6.03` bits.
4. **Mutual-information (Fano) form.** For prior `p = P(Z=1)` and error `Pe < min(p, 1−p)`: `I(Z; X, W) ≥ H(Z) − H_b(Pe)`. For `|Z| = M`: `I(Z; X, W) ≥ H(Z) − H_b(Pe) − Pe·log(M−1)`. This form is weak for rare events, so the divergence form (step 3) is primary.

## Conclusion shape — Reading A (lower bound / invariant)

Under premises 1–4, **any system with S2 competence at `(q, r)` for the class must have a channel `(X, W)` whose class-conditional divergence is at least `d(q‖r)`. Processing in the S2 tier, however deep or learned, cannot create it.**

If the side-channel audit shows that `W` is empty, or that `W` is conditionally independent of `Z` given `X`, then the floor falls **on the body-loop export alone**: `D(P₁^X ‖ P₀^X) ≥ d(q‖r)`. That is exactly the S2a contact observability floor, which must be available to S2. With `W` non-empty, the edge weakens to the disjunction "S2a export **jointly with** side channels" and does not single out S2a.

## What it does NOT say

- It does not say any estimator reaches the floor (C-P1-011 scope).
- It does not say which signals, rates or effort sources achieve the floor. That is C-P1-012's open factorial.
- It does not say S2a must be engineered before S2 (Reading P).
- It does not fix `(q, r)`. Those values are a task-specification input owned by the human lead or the packet. They must not be taken from a spike threshold (C-P1-012 H5).

## Reading P (quarantined)

"S2a must be built before S2." DPI gives no build order. As C-P1-011 H3 records, the export is a reversible schema that can be widened later. → **Grade 3.** It is admissible as an engineering planning *reason* (the floor is cheap to test first and specifies the S2 input budget), but not as necessity.

## Citation-ablation (B.8.7)

No evolutionary, developmental or anatomical premise is used. **Survives.**

## Scope

Any implementation family whose S2 tier sees contact only through `(X, W)`. Generic home humanoid / target plant. Non-support contacts. Programmatic force on the target requires two things: the C-P1-011 premise-2/3 audit, and task-stated `(q, r)` per contact class.

## Falsifier / challenge mode

- **In premises:** none is possible if steps 1–2 are correct, because they are standard results. An error found in the item match or the monotonicity step refutes the claim.
- **B.9.4(b) premise failure:** an S2 tier shown to receive `Z`-correlated information outside `(X, W)`. The claim stays true but must name the extra channel. Or a `(q, r)` taken from an implementation rather than the task.
- An empirical S2 detector that "beats" the export floor is an audit signal for a missed side channel, not a counterexample.

## Lock path (nomination)

**Recommended-for-lock: the narrow formal form (steps 1–3 with premises 1–4) only.**
- **Verification route (B.9.2):** match each step item by item to published statements of the data-processing inequality for relative entropy and the binary-hypothesis-testing converse. These are standard information-theory textbook results, the same family as the C-P1-011 route. A party other than the author must perform the check.
- **Human lead signature** is required.
- **Until both are done: Candidate.** The lock would not apply to the target stack until the side-channel audit is filed. A lock would let a later S2 proposal be marked as violating the claim if it offers no channel able to meet `d(q‖r)`. It would never pick an implementation.

## Counterexample-search spike registered?

**No.** These are standard results, and a numerical check would only test the harness (B.5). The required work is (i) a **side-channel audit** of the target stack, which is a document review, and (ii) a task-stated `(q, r)` table per contact class.
