# Decision — Packet Eng-1 (Next mainline engineering)

**Packet:** Eng-1  
**Box-local:** 2026-10-22 ~16:31 EDT  
**Adjudication:** Sonnet order-swap. Pass1 (P=A,Q=B) totals 38/38 → Recommend P=A. Pass2 (P=B,Q=A) totals 37/37 → Recommend Q=A. **Consistent: Recommend A.**

## Outcome

| Role | Proposal | Scope |
|------|----------|-------|
| **Recommend** | **A** | **S2a-XC** — contact-observability floor as certified body-loop export contract `XC-0` with one-sided divergence certificate; factorial spike targeting C-P1-012 confound repair |
| **Alternate** | **B** | Richer-plant S0a finite-horizon envelope certification (coupled modes); run only if A spike fails or human lead requests S0a depth |
| **Reject** | Promoting Grade-3 edges or Candidate claims to Eng-1 gates | — |

**Status:** **Closed — Recommend A spike FAIL** (harness valid; A02 unmet). Route toward Alternate B / Eng-2. See Spike outcome below.

## Gates

Both proposals ELIGIBLE. C-Eng1-A-01 remains **Candidate** (Astra ruling: no lock; **may not gate Eng-1**). No ladder-edge gates (D-Prin-2-001). D-P1-001 stays Provisional acceptance-gate.

## Spike

- **Run:** Proposal A spike after PLAN v2 reseal incorporating mandatory amendments (false-event units vs C-P1-012 register; H2/H3 harness criteria; path under `spikes/S2a-XC/`).
- **Do not run** B spike as frozen (low information); amend first if elevated.
- PASS = harness only; never hardware transfer; never changes claim grade.

## Mandatory amendments (A) before lock / before trusting certificates

1. Align false-event / FPR units with C-P1-012 registered criteria (or explicitly amend that claim's falsifier with B.9.6 count).
2. Reseal PLAN v2 under `spikes/S2a-XC/PLAN.md` with sha256; fix H2/H3 so a correct harness cannot fail spuriously.
3. Keep `(q,r)` PLACEHOLDER until human lead ratifies task table.
4. C-Eng1-A-01 stays Candidate; certificates cite it as design lemma only.
5. List bypassed Grade-3 edges in run log (E05/E06, E08/E09, E14; E10/E11 if applicable).
6. Non-interference check required (export on/off identical control trajectory).

## Human-lead outstanding

- Sign any Grade-1 lock (none asserted this packet).
- Ratify `(q_c,r_c)` task table.
- Choose whether Alternate B proceeds in parallel after A results.

## Spike outcome (S2a-XC PLAN v2)

**Box-local:** 2026-10-22 ~16:59 EDT  
**PLAN sha256:** `3d7b9af6b08d8f1fe36e25c06780bcfca571969656669d9c6fbdd1c902e9ac41`  
**VERDICT:** **FAIL** (`harness_pass=true`; H1–H4 all true; A02 unmet).  
**criteria_fired:** `A02`, `SUB_DOWN_NOT_MET` (informational).  
**Artifacts:** `packets/Eng-1/spikes/S2a-XC/{VERDICT.json,METRICS.md,results.json,contrasts.json,sensitivity_fixedgain.json,floor-cert/,run.log,deviations.md}`.

### Science read-back (data only; no claim grade change)

- Primary cell `R1_REAL_DOWN@r0.001` meets q0.90 only for `d50_M10` among `{d10,d20,d50}_M10`; `d10`/`d20` miss (tpr_L ≈ 0.26 / 0.72). UPSTREAM placement is far stronger (outside C-P1-012 premise-5 scope).
- Factor-E / Factor-R counterexamples: **not** fired (DOWN or UP). Substitution drop DOWN: **not** met (min 0.0625); UP met.
- Smoke (`--smoke`) was INVALID on H3 (small-n CP artifact); formal result is the full-grid FAIL above. Smoke not used for verdict.

### Status after spike

**Status:** **Closed — Recommend A spike FAIL.** Adjudicated Recommend remains A; engineering sufficiency A02 not met on this fixture. Per decision Alternate rule and PLAN §12: **route next engineering mainline toward Alternate B** (S0a finite-horizon envelope), subject to Eng-2 competing proposals and Principle gates. No claim grade changes from this spike (B.9.8). `(q,r)` remains PLACEHOLDER; C-Eng1-A-01 remains Candidate.

### Human-lead outstanding (updated)

- Sign any Grade-1 lock (none asserted).
- Ratify `(q_c,r_c)` task table.
- Confirm Eng-2 proceeds on Alternate B vs amended-A retry vs both.
- Optional: whether UPSTREAM torque-sensor placement should enter C-P1-012 scope via B.9.6 amendment (currently outside premise-5).
