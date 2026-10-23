# Eng-2 — Blind review of Proposal B, by Reviewer A (Claude Opus)

**Read:** `proposals/B.md`, `drafts/B/PLAN.md` (B's own deferred PLAN, cited by B.md), `source/packet-brief.md`, `source/Prin-3-decision.md`, and the `brief.md` rubric. I did **not** read `proposals/A.md` or `drafts/A/`. I did not change any claims and did not run a spike. The only calculation I ran was a generic binomial bound on PLAN §5's sample sizes, and it uses nothing from the fixture. Every number below about B's channel or envelope is a hand estimate, flagged as such, for the author or owner to confirm before sealing.

---

## 1. Gates (before ranking)

| Gate (Prin-3 / packet brief) | Verdict | Notes |
|---|---|---|
| G1: No spike execution before the human lead ratifies `(q,r)` (or a placeholder policy) and declares the effort measurement point | **PASS** | PLAN §1 lists approval, measurement point, branch choice and hashes as **PENDING**. It says "Missing approval means DEFERRED, not experimental FAIL" and "No approval is inferred from elapsed time." The author created no spike directory. |
| G2: Proposals and sealable deferred PLANs only; the spike is marked deferred-runnable | **PASS** | The header reads "DEFERRED; NOT EXECUTION-AUTHORIZED." Only the approval, identity and hash fields can be filled without an amendment. Any change to the design needs an amendment and a reseal. |
| G3: Stance matches Prin-3 Recommend (contract → bounded amended-A if eligible; B only for an independent envelope question; neither if gates fail) | **PASS (form)** / **CONDITIONAL (substance)** | B states the sequence, the "neither" option and an independently worded envelope question. **But** the "amended-A discriminator" is a new known-onset Gaussian surrogate that B itself says "cannot retrospectively attribute Eng-1 FAIL." Its eligibility *as amended A* rather than as a new fixture is asserted, not argued (see O1, O2). |
| G4: The override of D-Eng-1-001's automatic Alternate-B routing is labeled as a planning choice pending the human lead | **PASS** | This is explicit in B.md line 3 and PLAN header line 3. B states the cost of delaying B, but understates it (O7). |
| Mandatory amendment: symmetric eligibility; no Candidate claim used as a veto | **PASS** | Covered in B.md §"Symmetric eligibility". The same gate is applied to the envelope branch even though `q/r` is not one of its premises, and B says so honestly. |
| Mandatory amendment: a channel-level upper reference that can fail informatively | **PARTIAL** | The exact LR reference *can* return MODEL_CHANNEL_SHORTFALL, so it can fail. Whether that failure is *informative* is the problem: the reference is attached to a model whose parameters the author chose, so the shortfall/clear split is fixed by arithmetic before any data is drawn (O1). It is also an oracle that knows the class, which inflates any "detector gap" (O2). |
| Mandatory amendment: the amended-B contract is specified (modes, pass/fail, ownership) | **PASS (form)** / **FAIL (discriminating power)** | PLAN §9 does specify modes, reset, ownership and CERTIFIED/VIOLATION/UNRESOLVED. But the proposed parameters look degenerate: they probably certify open-loop at every delay (O3). That makes the symmetric branch choice lopsided. |
| Mandatory amendment: B.9.6 accounting deferred to the claim adjudicator | **PASS** | Covered in B.md contracts table and PLAN §8. |
| Mandatory amendment: "this fixture, detector and calibration" qualifiers; placement not called "the operative variable" | **PASS** | Covered in B.md Failure modes and PLAN §7. |
| Brief hard constraints: no named products or companies; home humanoid / target plant only; no Locked Grade-1; no Grade-3 used as law | **PASS** | None found. |

**Gate summary:** B is **eligible to rank**. It clears every procedural and ratification gate cleanly. Two of the substantive amendments are only partly met: the informative channel reference and a discriminating amended-B contract. I recommend those as **conditions on sealing**, not as grounds for rejection.

---

## 2. Principle integrity

Strengths:
- Every inherited claim is listed with its grade and state and given a non-load-bearing role. The new hypotheses are given grade N/A, explicitly not a necessity grade.
- C-P1-003 (Grade 3) is quarantined and does no work.
- Grade-3 edge bypasses (E05/E06/E08/E09/E14) are recorded as *bypassed prerequisites*, not as refuted necessity claims, and the verdict schema lists them.
- B does not treat SUB_DOWN_NOT_MET as evidence that effort information is absent. UP evidence is excluded from C-P1-012. B does not self-assign a B.9.6 count.
- B states plainly that the Gaussian reference is "an engineering calculation … not a new transferable necessity claim."

Minor issues:
- **P1.** The table states inherited grades ("C-P1-001 … conditionally recommended-for-lock per ledger") without citing which decision ID sets each. That breaks the brief's rule "inherit by ID, do not paraphrase." Add a decision or ledger row ID per claim.
- **P2.** C-Eng2-B-01 (two numerical paths agree) is a unit test, not a hypothesis. Calling it a "Candidate hypothesis" inflates the claims table. Move it to harness gates. It already appears there as gate 1.
- **P3.** PLAN §3 fixes the measurement point as "motor-side, `m` upstream of `f`" *before* the human lead declares it. B correctly requires a reseal if the declaration differs. Even so, a PLAN pre-filled this way anchors the very declaration that gate G1 reserves for the human lead. Present motor-side as one option alongside at least one other placement, not as the default.

---

## 3. Falsifiability of the deferred PLAN

The PLAN is carefully built: fixed seeds, disjoint splits, a Clopper–Pearson union bound, a ban on rerolls, and harness status kept separate from engineering status. The weakness is not rigor. It is that **most outcomes can be decided before data is drawn, and the one part that does depend on data is underpowered.**

**O1 — The reference verdicts are pre-computable, so the "channel can fail" branch carries no empirical risk.** `kappa² = μᵀS⁻¹μ` is a closed-form function of parameters the author chose (§3). A hand estimate for CMD (per-sample variance ≈ 9 + 9 + 0.32, with F correlated at ρ = 0.8) suggests:
- d = 10 ms, M = 2 → κ ≈ 1. That is a clear MODEL_CHANNEL_SHORTFALL at `q = 0.9`, `r_w = 6e-4`, which needs κ ≳ 4.5.
- d = 50 ms, M = 10 → κ ≈ 7 or more, which clears.

The split between SHORTFALL and clear across all 36 cells is therefore known on paper today. Sampling only checks that the code matches the algebra. This is not a fatal flaw, but it has three consequences:
- The PLAN should **publish the analytic 36-cell U table as a pre-registered prediction**.
- The PLAN should **admit that only the comparator side is empirical**.
- The proposal should not present a shortfall as a "discriminator" result. It is a property of the chosen σ values, and the human lead could reach it by choosing different σ values.

**O2 — REF_DETECTOR_GAP compares a reference that knows the class with a detector that does not. The gap is largely guaranteed by construction.** The reference for each cell uses that cell's μ, meaning it knows d, M and the onset. The boxcar uses one fixed weight vector spread evenly over 12 samples. For d = 10 ms, only 2 of the 12 samples carry signal, so the boxcar is mismatched by design. A hand estimate for d = 50 ms, M = 10, CMD gives boxcar z ≈ 8.3/2.3 ≈ 3.6 against a threshold of ≈ 3.4, so TPR ≈ 0.6 while U ≈ 1. That alone produces a GAP, so C-Eng2-B-02 is very likely "supported" before anyone runs it. The decomposition B wants (a detector missing an attainable point vs. a channel limit) needs a reference that is **attainable by a single detector without knowing the class**. Two options:
- (a) A composite or mixture-hypothesis reference: the Neyman–Pearson test for the class mixture the deployment would actually face, or a GLRT with its exact null calibrated.
- (b) Report the oracle gap and the class-agnostic gap separately.

Without one of these, a "gap" mostly measures the information asymmetry, not detector inefficiency. This is the core objection to Prin-3's "can fail informatively" amendment.

**O4 — The FPR test is underpowered, so many cells will be UNRESOLVED because of sample size, not because of the channel or detector.** Both SUPPORTED and GAP require `FPR_U ≤ r_w = 6e-4`, using 100,000 null windows and a one-sided α = 0.05/288 ≈ 1.7e-4. I computed this with a generic binomial calculation that uses nothing from the fixture:
- The Clopper–Pearson upper bound stays ≤ 6e-4 only for ≤ 33 observed false positives.
- If the comparator is calibrated exactly at the intended r/2 = 3e-4 (expected 30), P(pass) ≈ 0.74.
- Calibration error from a 30-exceedance quantile can plausibly push the true FPR to about 3.6–4e-4. P(pass) then falls to roughly 0.15–0.35.
- Thresholds apply per channel, so needing all four channels to pass makes things worse.

**Fix before sealing:** raise the null counts (about 10⁶ per split is still cheap under 15 CPU minutes for 12-dimensional linear scores), or calibrate at about r/3. Then state the predicted probability of an FPR-driven UNRESOLVED. As written, a likely outcome is "UNRESOLVED everywhere the comparator is close." That is a weak test that will look like caution.

**O5 — The known-onset reset-window protocol cuts the link to the latency question Eng-1 was asking.** B is open about this ("No continuous-onset p95 latency claim"). But it means a result from the amended-A branch says nothing about whether a contact-observability *floor* is met at the policy tier. Prin-3 asked for a discriminator of *detector vs channel*. B delivers that for a different problem: a simple hypothesis with known onset. The human lead should know that choosing this branch postpones the unknown-onset question rather than narrowing it.

**O3 — The amended-B contract's parameters look non-discriminating (envelope branch).** A hand estimate for open-loop growth over 200 steps:
- ‖A1‖ ≈ 1.003, so 1.003²⁰⁰ ≈ 1.8.
- Starting state: |x| ≤ 0.001·√2 grows to about 0.0026.
- Accumulated disturbance: Σ|w| ≤ about 1.4e-5 · 270 ≈ 0.004.
- Total ≈ 0.0065, inside the 0.01 envelope **with no control at all**.

The loop gain is about 0.001·8·0.2 per step. Even with a delay of l = 10 steps, gain × delay ≪ 1, so delay cannot destabilize the loop. The transition reset `diag(1, 0.9)` only contracts the state. So CERTIFIED is likely at **every** delay and schedule, and C-Eng2-B-04 is near-trivially supported. B's stated purpose, "with sensing delay and actuator memory retained," would never be exercised. Because Prin-3 requires a specified B contract *so the choice of branch is symmetric*, a degenerate B contract tilts that choice. Rescale the dynamics so that at least one delay is predicted, before the run, to come out UNRESOLVED or VIOLATION, for example a longer horizon or larger eigenvalue excess or loop gain. Alternatively, explicitly mark the §9 numbers as illustrative only.

**O6 — Missing pre-registered predictions.** O1 and O3 show that much of the design can be computed analytically. The PLAN should include the author's predicted status for each cell, so the run can falsify the *author's model of the PLAN* and not just check that the code is consistent.

---

## 4. Other concrete objections

- **O7 — The cost of the override is understated.** "One implementation/run cycle … 15 CPU minutes" leaves out the real cost: one more human ratification and seal cycle, plus another adjudication cycle, before the envelope question is reached. Given O2 and O5, that cycle may only confirm that a boxcar is worse than a matched filter. State the cost in program cycles, not CPU time.
- **O8 — The paired comparison is described but not used.** §5 allows shared base trajectories across channels for pairing. But the statuses use unpaired per-cell CP bounds, and no paired test (e.g. McNemar) between REAL and CMD, or between R1 and R2, is registered. Either register one or drop the claim.
- **O9 — "Attainable" is overstated even within the model.** U(r) is attainable only by a detector that knows μ for the cell. Rename it, or condition it as "attainable given class oracle" (this ties to O2).
- **O10 — Non-interference gate 4 is trivially satisfied.** The commanded effort is zero and there is no feedback path in the fixture, so the publication on/off replay cannot differ. The gate is fine to keep, but do not count it as evidence for C-Eng2-B-03.

---

## 5. Scores (rubric dimensions, 1–5)

| Dimension | Score | Rationale / objection |
|---|---|---|
| Constraint fit | **4** | Deferred correctly; no named products or companies; home humanoid / target plant only; no Locked Grade-1. Minus one for anchoring the measurement point and placeholder `(q,r)` that the human lead is supposed to declare (P3). |
| Principle integrity | **4** | Clean separation of necessity and sufficiency; Grade 3 quarantined; bypasses logged; B.9.6 deferred. Minus one for inheriting grades by paraphrase rather than by ID (P1) and for calling a unit test a hypothesis (P2). |
| Falsifiability | **2** | The reference verdicts can be computed in advance (O1). The gap is close to guaranteed by the class-oracle asymmetry (O2). The FPR test is underpowered and likely to give UNRESOLVED (O4). The B contract probably cannot fail (O3). The test can fail within days in form, but it carries little real risk. |
| Evidence demand | **5** | CPU/NumPy only, ≤ 15 min, ≤ 1 GiB, no hardware. Even the O4 fix keeps it cheap. |
| Failure modes | **3** | A good table of risks around leakage, pooling and placement. It misses the dominant ones: the oracle-reference asymmetry, sample-size-driven UNRESOLVED, and the degenerate envelope parameters. |
| Integrability | **4** | Owner boundaries are clear (body loop / fixture / reference / scene publisher / decision core / claim adjudicator), with UNKNOWN on stale scope and read-only publication. |
| Latency / criticality | **3** | The 60 ms deadline is declared, but the known-onset reset protocol avoids the policy-tier latency question (O5). The tier assignment is stated but not tested. |
| Complexity cost | **3** | Exact LR + whitening checker + CP union bound + 4 channels × 36 cells is justified *only if* the reference is informative. Given O1/O2, much of this machinery confirms things known in advance. |
| Reversibility | **5** | A single bounded attempt, no automatic second run, a stop rule, and no claim changes. Very cheap to abandon. |
| Stackability | **3** | The report/certificate contracts with UNKNOWN semantics carry forward well. But the surrogate's tie to S2a or Eng-1 is explicitly cut, so a result does not open the next stage. |
| **Total** | **36 / 50** | |

---

## 6. Bottom line

B is a governance-clean, well-fenced proposal. It passes every ratification and deferral gate, and it is careful about Principle matters. Its weakness is **scientific discriminating power**. As drafted:
- the channel reference's verdicts are fixed by the chosen parameters;
- the "detector gap" is mostly a class-oracle artifact;
- the FPR criterion is underpowered;
- the alternative envelope contract probably certifies trivially.

**Conditions I would attach before any seal (no claim changes):**
1. Add a class-agnostic (mixture or GLRT) reference, or report the oracle and class-agnostic gaps separately (O2, O9).
2. Pre-register the analytic per-cell U table and the author's predicted statuses (O1, O6).
3. Raise the null sample sizes or tighten calibration, and state the predicted FPR-driven UNRESOLVED rate (O4).
4. Rescale the §9 envelope parameters so at least one delay is predicted non-CERTIFIED, or label them illustrative (O3).
5. Restate the override cost in program cycles (O7). Cite inherited grades by decision ID (P1).

If those conditions are met, B stays a credible Recommend-class candidate under D-Prin-3-001. If they are not, the human lead should treat the amended-A branch as a harness-machinery exercise only, not as a channel-vs-detector diagnosis.
