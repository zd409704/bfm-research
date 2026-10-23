# Decision — Packet Eng-2 (Next mainline after Eng-1 FAIL)

**Packet:** Eng-2  
**Box-local:** 2026-10-22 ~17:19 EDT  
**Adjudication:** Sonnet order-swap. Pass1 (P=A,Q=B): Recommend P=A (38) / Alternate Q=B (36). Pass2 (P=B,Q=A): Recommend Q=A (37) / Alternate P=B (36). **Consistent: Recommend A.**

## Outcome

| Role | Proposal | Scope |
|------|----------|-------|
| **Recommend** | **A** | Contract-first (XC-1 docs) then **S2a-CEIL** deferred-runnable discriminator on the *unchanged* Eng-1 fixture: genie ceiling + nuisance-marginal + best-in-family → cell labels `CH_LIMIT` / `NUISANCE_LIMIT` / `DET_GAP_*` / `UNRESOLVED`. PLAN: `drafts/A/PLAN.md` (sha256 in `drafts/A/PLAN.sha256`). |
| **Alternate** | **B** | Contract-first then surrogate exact-reference channel discriminator; amended-B envelope only if independently justified. PLAN: `drafts/B/PLAN.md` (deferred). |
| **Reject** | Genie-only success as detector headroom; surrogate result as Eng-1 diagnosis; threshold-loosening retries; any spike execution before Prin-3 common gate | — |

**Status:** **Closed — Recommend A (deferred).** No spike executed. Execution blocked by D-Prin-3-001 until human lead ratifies `(q,r)` / placeholder policy, declares effort measurement point, and chooses branch.

## Gates

- Both proposals **eligible**; neither Hard Reject / Incomplete.
- D-Prin-3-001 common gate binds both.
- Recommend A is a **labeled proposed override** of D-Eng-1-001 auto-route to Alternate B — consistent with D-Prin-3-001 Recommend B (conditional amended-A sequence).
- D-P1-001 Provisional; D-Prin-2-001 no ladder edge gates.
- New claim **C-Eng2-A-01** remains Candidate (narrow lemma; not a gate). Cross-family claim adj outstanding if elevated.

## Mandatory amendments (before sealing for eventual run)

From order-swap (condensed):
- Rename/qualify `DET_GAP_OPEN`: genie-only success ≠ exported-channel detector headroom without a channel-only witness.
- Carry Prin-3 amendments: informative channel-level upper reference; fixture/detector/calibration qualifiers; no Candidate-as-veto.
- Seal only after human gate clearance + approval manifest; PASS = harness only.
- Alternate B: re-scope discriminating power if elevated; do not treat as Eng-1 miss diagnosis.

## Spike

**Not run.** Deferred-runnable PLANs filed under `drafts/{A,B}/PLAN.md`. Do not create `spikes/` run artifacts until gate clearance.

## Human-lead outstanding

- Ratify `(q_c,r_c)` or exploratory placeholder policy; declare effort measurement point; choose A vs B vs neither.
- Sign any Grade-1 lock (none asserted).
- Optional: claim-adj C-Eng2-A-01 (Astra; Opus-authored).
