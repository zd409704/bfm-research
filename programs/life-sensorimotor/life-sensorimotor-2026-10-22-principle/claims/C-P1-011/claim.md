<!-- PENDING: full replacement for claims/C-P1-011/claim.md (sealed, mode 444). Not yet applied. Diff: pending-claim.diff. -->
# C-P1-011 — Information ceiling on contact knowledge above the body-loop export (DPI)

| Field | Value |
|---|---|
| **ID** | C-P1-011 (inherited by ID from `inherited-ledger-P1.md`; origin A-C2) |
| **Short title** | Information ceiling / data-processing inequality on contact export |
| **Author family** | Opus (P1 Proposal A). Record compiled in Prin-1 by Author A (Opus). |
| **Claim adjudicator (per roster)** | Codex gpt-6-astra high (cross-family). Not this author. Prin-5 amendments were ruled by an **alternate** (Claude Opus) because the Recommend proposal shared the usual adjudicator's family. See `adjudication-prin5/ruling.md`. |
| **Grade** | **Grade 1** (information-theoretic invariant). This applies only to the narrow statement below. The P1 "gate/ordering" corollary is excluded (H3). |
| **State** | **Candidate**. Not Locked. P1 Proposal A proposed "Locked"; P1 decision kept all A claims Candidate. Prin-1 ruling: tighten-premises-then-Candidate-stay. Prin-5 ruling: premises tightened, Candidate stay. |

## Statement (narrow form)

Let `Z` be a specified contact variable, such as onset time, contact wrench, or contact link. Let `t` be a declared information cutoff for a named recipient. Let `X_t` be the body-loop export transcript actually available to that recipient by `t`, and `Y_t` the upper-layer state or output being bounded at `t`. Let `W_t` be all other information accessible to the recipient by `t`, with its initial state. `W_t` need not be statistically independent of `X_t`.

If `Y_t` is conditionally independent of `Z` given `(X_t, W_t)`, that is `Z → (X_t, W_t) → Y_t`, then

`I(Z; Y_t) ≤ I(Z; X_t, W_t)`,

and no processing of the declared inputs, however deep, learned or slow, can exceed that bound.

The **export-only** form `I(Z; Y_t) ≤ I(Z; X_t)` additionally requires `Z → X_t → Y_t`. That must be justified separately; naming `W_t` does not establish it. Both forms concern one fixed joint law and the declared cutoff.

## Premises (numbered, explicit)

1. `Z` is a well-defined random variable. The declaration states the contact quantity, target interval, resolution, treatment of no-contact cases, and label source. It also states the recipient, the information cutoff `t`, and the mode (online or retrospective), separately from the target interval. Past history is declared as part of either `X_t` or `W_t`. If `Z` is a function of `X_t` or `W_t`, the application is *definitional* and is not read as a physical ceiling.
2. Markov premise, as stated above. A sufficient construction for the joint form is `Y_t = f(X_t, W_t, U)` with `U ⊥ Z | (X_t, W_t)`. For the export-only form, it is the same construction with `(W_t, U) ⊥ Z | X_t`. `X_t` is the *realized* transcript available to the recipient: field values plus any observable delivery metadata (arrival times, ordering, drops, mode/fault/saturation flags, schema presence). Any stream reaching the recipient outside the declared `X_t` either enlarges `X_t` or belongs in `W_t`.
3. Commands, efference copies, action and exploration random state, retained history and memory, and run-varying learned or adapted state belong in `W_t` whenever they can carry information about `Z` beyond `X_t`, unless they are shown to be derived from the declared tuple. This includes information carried through feedback: a seed that shapes the later contact is not independent processing noise. Exclusion requires a joint conditional-independence or derivation argument; zero marginal correlation with `Z` is not sufficient.
4. Each assertion uses one joint law over `(Z, X_t, W_t, Y_t)`, including policy, environment distribution, selection and reset rules, and fixed configuration. Both sides of any comparison use that law. A relevant change requires a new application audit.
5. Subsampling, filtering, quantization, compression and derived fields **cannot increase** information about `Z` when they are processing of the declared inputs; equality is possible. Any inputs that control the processing (adaptive parameters, timestamps, retained samples, auxiliary inputs) must be declared before this premise or H4 is invoked. An event-triggered sampling pattern is information inside the realized `X_t`.

## Conclusion shape

**Invariant / impossibility.** Information about `Z` available above the export cannot increase through processing of the declared inputs. Under the stated premises, the recipient cannot hold more information about `Z` than its declared joint input `(X_t, W_t)` carries. Under the export-only premise, it cannot hold more than `X_t` carries. Exceeding the export-only bound requires additional accessible information about `Z` beyond `X_t`; that information need not be statistically independent of `X_t`.

## Scope

**Covers:** any upper layer of a home-humanoid / target-plant stack (prediction, probing, relational scene modules, decision core, pretrained behavior-model latents) whose contact knowledge flows through the body-loop export. It applies to every implementation family (B.3.3 holds).

**Does not cover:**
- Upper layers with additional accessible contact information: vision, tactile skin, audio, separate force/torque sensors, or the layer's own command history when that history is correlated with `Z` (premise 3). These add premises; they are not counterexamples.
- **Estimation quality.** DPI bounds mutual information. It does not say any given estimator reaches the bound, and it gives no error rate or latency.
- **Sufficiency of any particular export.** The claim does not say the proposed I1/I2 fields carry enough information for any task.
- **Which signals to export.** The claim does not by itself show that `τ_realized` must be in `X`. That is C-P1-012 and needs its own argument.
- **Research or ladder ordering.** See H3.

## Falsifier / challenge mode

- No counterexample is possible within premises 1–5. DPI is a standard theorem (Cover & Thomas, Elements of Information Theory, data-processing inequality).
- A challenge is admissible only under B.9.4(b), as a premise failure in the target setting. Examples: an upper layer is shown to receive contact-correlated information that bypasses `X`, or its command history is contact-informative and was omitted from `W`. When that happens the claim stays true, but its application to the target stack must name the joint channel `(X, W)`.
- Any empirical result where an upper layer "beats" the export on contact inference is a signal to audit for a side channel `W`. It is not evidence against the theorem.
- **Application failure criterion (Prin-5).** An application is evaluated against a frozen, versioned interface and configuration manifest. It fails in either of two cases: (a) an input or retained state accessible to the upper layer is missing from the audited boundary record; or (b) a claimed conditional independence is contradicted by an explicit model that satisfies the recorded assumptions. A bypass found later is a B.9.4(b) premise failure in the target setting. Traces can expose a bypass but cannot prove that none exists. Mutual-information estimates and prediction success cannot certify conditional independence. An application with unresolved items remains *unsupported*. That does not block Eng-2.

## Hygiene notes (from P1 decision and this review)

- **H1 — Contact variable undefined in P1.** P1 wrote `I(contact; upper) ≤ I(contact; I1∪I2)` without defining "contact" (onset? wrench? location?), the window, or the time alignment. Premise 1 fixes that.
- **H2 — Omitted side channel: the upper layer's own commands.** P1 framed the ceiling as belonging to the export alone. An upper layer that issued the motion causing the contact has command or efference information correlated with `Z`. P1 also listed only vision and tactile as independent channels. Premise 3 closes the gap.
- **H3 — Stretch: from DPI to "the export contract is a gate for S2–S5 and must be fixed before they stack."** DPI is a statement about information. It implies no research order and no requirement to *fix* the export first. Proposal A itself describes the export as a reversible schema, so it can be widened later and the information recovered at that point. The ordering inference is excluded from this claim. Any edge claim of the form "S2a must precede S3–S5" belongs to Prin-2, and it is Grade 3 by default (B.8.2). **D-P1-001 is a Provisional S0a acceptance-gate recommendation, not a necessity ordering. This claim does not upgrade it, and it does not upgrade the P1 Alternate (S2a next) into one either.**
- **H4 — Redundant term.** In P1, I2 (the contact residual) is computed from I1, so `I(Z; I1 ∪ I2) = I(Z; I1)`. The residual adds usability, not information. The ceiling is set by the raw fields and their rates. Derived fields cannot raise it. *(Prin-5 correction: this holds only if I2 is a function of the published I1 transcript and fixed configuration. If I2 uses body-loop-internal signals, unpublished rates, history or calibration, those inputs must be declared, and I2 can add information.)*
- **H5 — Near-vacuity risk.** The theorem is trivially true. Its programmatic force depends entirely on premise 2 (the export is the *only* path) being true of the target stack. Without an architecture audit showing that, the claim constrains nothing. This is why the record recommends a narrow lock and does not credit P1 with "trivially Locked" status.
- **H6 — Citation ablation (B.8.7).** No evolutionary, developmental or anatomical citation is involved, so ablation leaves the argument intact.

## Recommended adjudicator action

**recommended-for-lock (narrow form only), conditional on tighten-premises.** The claim should be adopted with premises 1–5 and with the P1 ordering corollary removed (H3). The verification route under B.9.2 is an item-by-item match to the published DPI statement, checked independently, followed by the human lead's signature. The claim stays **Candidate** until both are done.

*Reconciliation (Prin-5 alternate adjudicator):* the paragraph above is the author's recommendation. The adjudicated disposition is **Candidate stay**: premises tightened in Prin-5; not recommended-for-lock until the independent B.9.2 match of the *amended* statement and the human signature are done. When `W_t` is non-empty, do not cite `I(Z; X_t)` as the upper layer's ceiling unless an export-only outcome is justified.

Even after a lock, applying the claim to a specific target-plant stack requires a premise-2/3 audit, so that the side channels `W` are known.

## Counterexample-search spike registered?

**No.** No in-premise counterexample to a proven theorem exists. A numerical check would only test the harness, and under B.5 it would prove sufficiency at most. The work that is actually needed is a **side-channel audit** of the target stack architecture (premises 2–3). That is a document review, not a spike.
