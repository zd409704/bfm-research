# C-P1-011 — Information ceiling on contact knowledge above the body-loop export (DPI)

| Field | Value |
|---|---|
| **ID** | C-P1-011 (inherited by ID from `inherited-ledger-P1.md`; origin A-C2) |
| **Short title** | Information ceiling / data-processing inequality on contact export |
| **Author family** | Opus (P1 Proposal A). Record compiled in Prin-1 by Author A (Opus). |
| **Claim adjudicator (per roster)** | Codex gpt-6-astra high (cross-family). Not this author. |
| **Grade** | **Grade 1** (information-theoretic invariant). This applies only to the narrow statement below. The P1 "gate/ordering" corollary is excluded (H3). |
| **State** | **Candidate**. Not Locked. P1 Proposal A proposed "Locked"; P1 decision kept all A claims Candidate. |

## Statement (narrow form)

Let `Z` be a specified contact variable over a specified time window, such as onset time, contact wrench, or contact link. Let `X` be the body-loop export over that window, `Y` be everything an upper layer receives or holds over that window, and `W` be any upper-layer-side information not derived from `X` (its own commands and efference copies, priors and memory, other sensors).

If `Z → X → Y` is a Markov chain, meaning `Y` is conditionally independent of `Z` given `X`, then

`I(Z; Y) ≤ I(Z; X)`,

and no processing of `Y`, however deep, learned or slow, can exceed that bound.

When `W` exists, the valid form is `I(Z; Y) ≤ I(Z; X, W)`. The ceiling then belongs to the *joint* channel `(X, W)`, not to the body-loop export alone.

## Premises (numbered, explicit)

1. `Z` is a well-defined random variable, with the contact quantity, time window and resolution all stated. "Contact" left undefined is not admissible.
2. All upper-layer access to information about `Z` passes through `X`, so `Y = f(X, U)` with noise `U` independent of `Z` given `X`. Otherwise all side channels `W` are enumerated and included as above.
3. Upper-layer commands and efference copies count as side information whenever they are correlated with `Z` (contact depends on the motion commanded). They must be included in `W` or shown to be already contained in `X`.
4. The probability model over `(Z, X, Y)` is fixed. In particular the bound is over one shared distribution, and it does not change between deployment and evaluation.
5. Subsampling, filtering, quantization and compression of `X` are all processing steps, so each of them can only lower the information.

## Conclusion shape

**Invariant / impossibility.** Information about `Z` available above the export is monotonically non-increasing through processing. Recovering information that the export dropped is impossible unless a channel independent of `X` is added.

## Scope

**Covers:** any upper layer of a home-humanoid / target-plant stack (prediction, probing, relational scene modules, decision core, pretrained behavior-model latents) whose contact knowledge flows through the body-loop export. It applies to every implementation family (B.3.3 holds).

**Does not cover:**
- Upper layers with independent contact channels: vision, tactile skin, audio, separate force/torque sensors, or the layer's own command history when that history is correlated with `Z` (premise 3). These add premises; they are not counterexamples.
- **Estimation quality.** DPI bounds mutual information. It does not say any given estimator reaches the bound, and it gives no error rate or latency.
- **Sufficiency of any particular export.** The claim does not say the proposed I1/I2 fields carry enough information for any task.
- **Which signals to export.** The claim does not by itself show that `τ_realized` must be in `X`. That is C-P1-012 and needs its own argument.
- **Research or ladder ordering.** See H3.

## Falsifier / challenge mode

- No counterexample is possible within premises 1–5. DPI is a standard theorem (Cover & Thomas, Elements of Information Theory, data-processing inequality).
- A challenge is admissible only under B.9.4(b), as a premise failure in the target setting. Examples: an upper layer is shown to receive contact-correlated information that bypasses `X`, or its command history is contact-informative and was omitted from `W`. When that happens the claim stays true, but its application to the target stack must name the joint channel `(X, W)`.
- Any empirical result where an upper layer "beats" the export on contact inference is a signal to audit for a side channel `W`. It is not evidence against the theorem.

## Hygiene notes (from P1 decision and this review)

- **H1 — Contact variable undefined in P1.** P1 wrote `I(contact; upper) ≤ I(contact; I1∪I2)` without defining "contact" (onset? wrench? location?), the window, or the time alignment. Premise 1 fixes that.
- **H2 — Omitted side channel: the upper layer's own commands.** P1 framed the ceiling as belonging to the export alone. An upper layer that issued the motion causing the contact has command or efference information correlated with `Z`. P1 also listed only vision and tactile as independent channels. Premise 3 closes the gap.
- **H3 — Stretch: from DPI to "the export contract is a gate for S2–S5 and must be fixed before they stack."** DPI is a statement about information. It implies no research order and no requirement to *fix* the export first. Proposal A itself describes the export as a reversible schema, so it can be widened later and the information recovered at that point. The ordering inference is excluded from this claim. Any edge claim of the form "S2a must precede S3–S5" belongs to Prin-2, and it is Grade 3 by default (B.8.2). **D-P1-001 is a Provisional S0a acceptance-gate recommendation, not a necessity ordering. This claim does not upgrade it, and it does not upgrade the P1 Alternate (S2a next) into one either.**
- **H4 — Redundant term.** In P1, I2 (the contact residual) is computed from I1, so `I(Z; I1 ∪ I2) = I(Z; I1)`. The residual adds usability, not information. The ceiling is set by the raw fields and their rates. Derived fields cannot raise it.
- **H5 — Near-vacuity risk.** The theorem is trivially true. Its programmatic force depends entirely on premise 2 (the export is the *only* path) being true of the target stack. Without an architecture audit showing that, the claim constrains nothing. This is why the record recommends a narrow lock and does not credit P1 with "trivially Locked" status.
- **H6 — Citation ablation (B.8.7).** No evolutionary, developmental or anatomical citation is involved, so ablation leaves the argument intact.

## Recommended adjudicator action

**recommended-for-lock (narrow form only), conditional on tighten-premises.** The claim should be adopted with premises 1–5 and with the P1 ordering corollary removed (H3). The verification route under B.9.2 is an item-by-item match to the published DPI statement, checked independently, followed by the human lead's signature. The claim stays **Candidate** until both are done.

Even after a lock, applying the claim to a specific target-plant stack requires a premise-2/3 audit, so that the side channels `W` are known.

## Counterexample-search spike registered?

**No.** No in-premise counterexample to a proven theorem exists. A numerical check would only test the harness, and under B.5 it would prove sufficiency at most. The work that is actually needed is a **side-channel audit** of the target stack architecture (premises 2–3). That is a document review, not a spike.
