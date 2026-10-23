# Prin-5 — Blind Review A on Proposal B

**Reviewer:** Blind Reviewer A (Claude Opus). **Target:** `proposals/B.md` only. I did not read proposal A.
**Inputs read:** `source/packet-brief.md`, `source/method-Appendix-B.md`, root `brief.md` (rubric), and for checking: `source/C-P1-011-claim.md`, `source/Prin-4-decision.md`, `source/program-ledger-current.md`. The source claim copy is byte-identical to canonical `claims/C-P1-011/claim.md` (verified with `diff`).
**Status:** Review only. No claim state, grade, or text changed. C-P1-011 stays **Candidate** (Grade 1, narrow form; tighten-premises).

---

## 1. Gates (Appendix B, B.9.5): checked before ranking

| Gate | Result | Evidence in B |
|---|---|---|
| No Locked Grade-1 / no claim-state change | **PASS** | Header and §4 Governance: "C-P1-011 remains Candidate… no claim-state ruling, lock"; any lock needs the human lead's signature and a non-author transition. |
| Claim adjudicator ≠ author (B.9.1) | **PASS** (one flag, see §5.4) | "The author of these amendments must not adjudicate their own amendments; bind a separate reviewer." |
| Planning order ≠ necessity (B.8.3) | **PASS** | Inherits D-Prin-4-001 "as planning authority only". The Scope checklist row excludes ladder edges and research order. |
| Phenomenology does not promote necessity (B.4/B.5) | **PASS** | §4 Evidence: traces can expose omitted paths but can't prove absence; MI estimates and successful prediction can't certify conditional independence. |
| No spike / counterexample-search discipline (B.9.8) | **PASS** | No spike is proposed. Any later empirical search must seal a PLAN under B.9.8 first. |
| Grade-3 not used as law; citation ablation | **PASS** (vacuous) | No evolutionary or anatomical citation appears. |
| Eng-2 non-interference (D-Prin-3-001, D-Eng-2-001) | **PASS** | Adds no Eng-2 precondition. The "Unresolved" outcome "does not block Eng-2". The C-Eng1-A-01 and C-Eng2-A-01 link is deferred to a later cross-reference, and the human `(q,r)`, measurement-point and branch requirements are inherited unchanged. |
| Hard constraints (no named product/company, writes, no paid compute) | **PASS** | Generic roles only (architecture owner, reviewer, adjudicator). No compute required. |

**All gates pass. B is eligible for ranking.**

---

## 2. Principle integrity

**Strengths (checked against the math):**
- **Joint-form core is correct.** If `Y_t ⊥ Z | (X_t,W_t)`, then `I(Z;Y_t) ≤ I(Z;X_t,W_t)`. The incremental form `I(Z;Y_t|W_t) ≤ I(Z;X_t|W_t)` also follows correctly: `(Y_t,W_t)` is processing of `(X_t,W_t)`; apply the chain rule to both sides and cancel `I(Z;W_t)`. I re-derived both.
- **It correctly finds three wording defects in the canonical claim**, which are real tighten-premises items:
  1. The conclusion says "unless a channel **independent of X** is added". Statistical independence from `X` is neither required nor typical. What matters is conditional information `I(Z;W|X)`. The XOR case makes this concrete: `W` can be independent of both `Z` and `X` and still be decisive.
  2. Premise 5 says processing "can only **lower**" information. It should say "cannot increase", because equality is possible.
  3. Premise 2 has the noise `U` "independent of `Z` given `X`". B notes that exogenous seeds stop satisfying this after feedback (the toy with probe seed `R`). This sharpens H2 / premise 3 beyond "commands correlated with Z".
- **Premise 4 ("does not change between deployment and evaluation") is reframed correctly** as one law per assertion, with a re-audit when the law changes. That avoids overstating DPI's requirements.
- **It separates the target interval from the information cutoff** (online vs retrospective, history inside `X_t` or `W_t`). This is a real gap in premise 1, which fixes only "a time window".
- **The anti-vacuity guard** ("avoid `W_t = Y_t`", inventory primitive inputs independently of the output) speaks directly to H5.
- **Honest about verification.** It says outright that its identities are not a B.9.2 check, and that the record's recommended-for-lock wording conflicts with the ledger's "tighten-premises" disposition and must be reconciled by the adjudicator, not by the author.

**Weaknesses:**
- **(minor) Grade not restated.** B writes "recorded grade unchanged" but never says "Grade 1, narrow form" in its own text. The rubric asks proposals to state grades. Harmless here, but the adjudicator should not need a second file to learn the grade.
- **(minor) The sufficient condition for export-only is stated loosely.** In the "Export-only justified" row, "jointly conditionally independent of `Z` given `X_t`" needs to be read as `(W_t,U) ⊥ Z | X_t` together with the joint construction `Y_t = f(X_t,W_t,U)`. If `U` is left out, the chain does not follow. The text implies this but does not say it.
- **(minor) Checklist labels are ambiguous.** "P2" appears twice and "P2/P3" once. It is unclear whether the labels index canonical premises or are priority tags. Use one scheme.

---

## 3. Inventory completeness vs laundry-list risk

**Completeness: high.** The eight access classes (B01 to B08) are organized by *how* information crosses the boundary, not by device. That makes the inventory close to exhaustive by construction. I stress-tested it with paths a device list usually misses:

| Probe path | Covered? |
|---|---|
| Packet timing, drops or latency carrying contact information with identical payloads | B01 ✓ |
| Debug, fallback or safety-controller routes | B02 ✓ |
| Efference copy, exploration seed, policy mode | B03 ✓ (plus the feedback stress case) |
| Reset failure, cross-episode cache, delayed messages | B04 ✓ |
| Run-specific adaptation and calibration | B05 ✓ |
| Task ID, fixture label, dataset selection / inclusion filters | B06 ✓ |
| Simulator internals, labels, smoothing, evaluator→recipient leak via adaptation | B07 ✓ |
| "Derived" residuals that silently use extra calibration or history (H4 validity) | B08 ✓ |
| Upper layer setting export parameters (filter gains, probe requests), so `X` depends on prior `Y` | Partially (B03/B05). It should be named, because it makes "processing of declared inputs" (P5) conditional on the recipient's own past outputs. |
| Inter-module sharing *inside* the "upper layer" (scene module → decision core carrying vision-derived contact) | Partially (B02 / record "named recipient"). Recommend one sentence on choosing the recipient boundary when the upper layer is composite. |

**Laundry-list risk: well mitigated, with residual cost risk.**
- **Mitigations present:** every row starts **unresolved** (no default "absent"). Exclusion needs evidence. Information is deduplicated by provenance. The whole tuple is audited *jointly*, and the XOR case makes the reason concrete. Inventory completion is explicitly *not* proof of necessity, sufficiency or order.
- **Residual risks:**
  1. **No completion criterion.** "Every relevant access path accounted for" is unprovable in an open world. Export-only may therefore never be reachable, and C-P1-011 would stay vacuous in practice (H5). Recommend certifying relative to a **frozen, versioned interface manifest** (closed-world assumption declared as a premise), with a bypass found later counting as a B.9.4(b) premise failure.
  2. **No triage order.** Eight classes × nine per-row attributes × the seven-field record is a lot for a "minimum deliverable". Recommend a first pass on B03 (commands/feedback) and B04 (retained history), since H2 already identifies these as the most likely leaks. Expand to the other classes only on demand.

---

## 4. Eng-2 non-interference

**Clean.** B states three times that it adds no Eng-2 preconditions. It makes the "Unresolved" outcome explicitly non-blocking for engineering work. It confines C-Eng1-A-01 and C-Eng2-A-01 to an optional later mapping onto B01/B04/B05/B07/B08, and it leaves D-Prin-3-001's human gates unchanged.

One observation: D-Prin-4-001 priority 2 said to *include* C-Eng2-A-01 and C-Eng1-A-01 as sub-items (not gates). B defers them, citing missing premises in the source bundle, although both claim records exist under `claims/`. This is a defensible minimum-scope choice, not a gate issue, but it is under-delivery against the Prin-4 split. The adjudicator may want a one-line placeholder sub-item for each.

---

## 5. Other objections and amendments

1. **Add the closed-world manifest premise** (§3 risk 1) as an explicit premise in the application certificate.
2. **Add a triage order** (B03 and B04 first) to keep the minimum deliverable small.
3. **Tighten the export-only sufficient condition** to `(W_t,U) ⊥ Z | X_t` under the joint construction.
4. **Role separation on amendments.** If B's checklist edits are adopted as amendments to C-P1-011, the roster's bound claim adjudicator for C-P1-011 (Astra) may share a model family with whoever drafted the adopted amendment text. B flags the principle but does not name this collision risk. The adjudicator should check author family vs bound adjudicator before ruling, and bind an alternate if needed.
5. **Name the recipient-controls-export path** and **composite-recipient boundary** (§3 table).

None of these is gate-level.

---

## 6. Rubric scores (1–5)

| Dimension | Score | Rationale |
|---|---|---|
| Constraint fit | **5** | All hard constraints and non-goals respected. No lock, no spike, no named entities, no Eng-2 change. |
| Principle integrity | **5** | Correct math. Finds three real wording defects in the claim (independence, "lowers", noise after feedback). Separates necessity, sufficiency and inference, and governance is honest. Minor: grade not restated in its own text. |
| Falsifiability | **3** | By design no spike. Falsification is "reviewer finds a bypass", which can happen within days, but there is no time-box and no closed-world criterion, so "unresolved" can persist indefinitely. |
| Evidence demand | **5** | Document review only. No compute or hardware. |
| Failure modes | **4** | Names vacuity (`W=Y`), marginal screening, feedback seeds, invalidation on change, and late packets. Missing: open-world non-termination risk. |
| Integrability | **4** | Clear generic ownership (architecture owner populates, independent reviewer attacks, claim adjudicator rules). Composite-recipient boundary under-specified. |
| Latency / criticality | **4** | Sharp treatment of decision cutoff, online vs retrospective, and availability time. Tier placement is not otherwise in scope. |
| Complexity cost | **3** | Machinery is justified but heavy for a minimum deliverable (7-field record, 8 classes × 9 attributes, 11 checklist items). No triage. |
| Reversibility | **5** | Paper artifact, versioned, cheap to revise or abandon. |
| Stackability | **4** | The certificate template carries over to later audits (C-Eng1/C-Eng2 cross-ref) without requiring them now. |
| **Total** | **42 / 50** | |

**Overall:** A strong, technically correct proposal that passes all gates. Its main contribution is replacing a device list with an access-class boundary certificate that has an explicit **unresolved** outcome, plus three concrete tighten-premises corrections to C-P1-011's wording. The main residual risks are open-world non-termination and the cost of a minimum deliverable. Both can be fixed with the amendments in §5. Reviewer A sees no reason to reject B.
