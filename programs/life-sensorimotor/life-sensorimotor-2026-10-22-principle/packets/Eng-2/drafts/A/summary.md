# Eng-2 / Author A — One-page summary

**Thesis.** Eng-1 S2a-XC FAIL (A02 unmet on DOWN d10/d20; harness valid) does not tell us whether the **detector** or the **channel** is responsible, and every next step depends on that. Proposal A makes the Eng-2 mainline a two-stage sequence:
- **Stage 1:** contract XC-1. It types the open human-lead items (`(q,r)` status, effort measurement point), fixes the contact classes, windows, side channels and nuisance prior, and adds a symmetric A/B eligibility table plus an amended-B contract skeleton.
- **Stage 2:** S2a-CEIL, a deferred-runnable discriminator on the *unchanged* Eng-1 fixture. It adds a full-genie Neyman–Pearson **ceiling**, a nuisance-marginal reference and a preregistered best-in-family detector. These classify each primary cell as `CH_LIMIT` / `NUISANCE_LIMIT` / `DET_GAP_*` / `UNRESOLVED`.

**Why this ordering.** It provides the "channel-level upper reference that can fail informatively" that D-Prin-3-001 requires of amended A. A `CH_LIMIT` result rules out futile detector retries. `DET_GAP` justifies one. Neither result changes a claim grade. Running it before B is a **proposed override** of D-Eng-1-001's automatic Alternate-B routing, pending the human lead. Cost: B's envelope evidence is delayed by one packet. B may run in parallel if an independently specified envelope question exists.

**Grades.** C-P1-012 stays G2 Candidate; secondary-cell data go to its adjudicator, and no B.9.6 event is self-assigned. C-Eng1-A-01 (floor) and the new **C-Eng2-A-01** (ceiling; G1 narrow lemma; Candidate; adjudicator Astra) are design lemmas only, with no gate. No ladder-edge gates (D-Prin-2-001). D-P1-001 stays a Provisional acceptance-gate.

**Spike.** `drafts/A/PLAN.md`: CPU/numpy, ≤ 30 min.
- Sizes: n₁ = 600, n₀ = 30 000 per cell; one episode per window; disjoint seeds.
- Harness criteria H1–H7: reproduce Eng-1 (else INVALID), analytic/MC agreement, NULL control, tier ordering, quadrature convergence, no leakage, non-interference.
- Sealed routing table.
- **Execution is blocked** until the human lead ratifies `(q,r)` and declares the measurement point.
- PASS = harness only.

**Key risks.** A genie likelihood mismatch (caught by H2/H3/H4). An uninformative ceiling (the `E-INFO` test, reported). Reading `CH_LIMIT` as a hardware statement (explicitly excluded in scope).

**Non-claims.** No locks, no necessity order, no threshold loosening or class selection, no UP import into C-P1-012 scope, no hardware transfer.

Files:
- `packets/Eng-2/proposals/A.md`
- `packets/Eng-2/drafts/A/PLAN.md` (+ `PLAN.sha256`)
- `claims/C-Eng2-A-01/claim.md`
