# Eng-1 Proposal A — one-page summary (Author A, Claude Opus)

**Recommend:** **S2a-XC.** This packet builds the contact-observability floor as a *certified body-loop export contract* (`XC-0`) with a one-sided divergence certificate. It runs alongside the S0a acceptance gate (D-P1-001, Provisional, not a necessity order) and is not gated by it.
**Alternate:** a merged S0a+S2a fixture, deferred until an XC-0 certificate is filed. **Reject as primary:** S0a certification on a richer plant (no target dynamics or disturbance pair is available, and the claim leverage is low).

## Core idea
- **XC-0** is a versioned export schema. Each field declares its rate, its effort source (CMD_RECON / REALIZED_CURRENT / REALIZED_OUTPUT_TORQUE) and its friction placement. A **side-channel register `W`** is required for every consumer: policy tier, scene publication, decision core.
- **Acceptance test.** A held-out detector run must give `TPR_L ≥ q_c` and `FPR_U ≤ r_c`. By **C-Eng1-A-01** (new, G1 narrow lemma, Candidate), this certifies `D(P₁‖P₀) ≥ d(q‖r)` on `(X, W)` at confidence 1−α. The certificate shows information is **present**. A failed certificate shows nothing about absence.
- `(q_c, r_c)` per contact class is **task-stated by the human lead**. The spike uses a PLACEHOLDER grid only.

## Principle inputs (all Candidate; none used as a gate)
- **C-P1-011** (G1 narrow): the DPI ceiling. It motivates the `W` register.
- **C-Prin2-E17 Reading A** (G1 conditional): the form of the floor `d(q‖r)`, with `r > 0` enforced. Reading P is G3 and not used.
- **C-P1-012** (**G2, downgraded**): used as the experimental target, not as necessity. XC-0 does not mandate realized effort or R1.
- **C-P1-001/002/010**: not preconditions. **C-P1-003**: G3, not used.

## Spike (sealed PLAN: `drafts/A/spike-PLAN.md`, sha256 `ffc9b78a…28cc7`; CPU/numpy, < 30 min, deferred-runnable)
- Planar 2-link arm at 1 kHz, with non-support pulses on link 2, unmodeled ripple and bias, and output friction.
- **Factorial:** rate {50, 200 Hz} × effort {CMD_RECON, REALIZED} × placement {downstream, upstream} gives 8 cells, plus ORACLE and NULL controls.
- The observer's gain·T is fixed at 0.25 (fixes C-P1-012 H2). Both friction placements are run (fixes H3).
- **Outputs:** floor certificates, the registered C-P1-012 Factor-E and Factor-R counterexample criteria, the B.9.3 substitution test, and a non-interference check.
- **Harness PASS** requires H1 determinism, H2 NULL never certifies, H3 ORACLE certifies, and H4 non-interference. PASS validates the harness only. It is never evidence of hardware transfer and never changes a grade.

## Key failure modes
- `(q, r)` taken from the spike rather than the task.
- Command side-channel leakage.
- Friction placement or tuning building the conclusion in.
- Non-i.i.d. windows.
- Reading a failed certificate as absence of information.
- An over-simple fixture.

## Bypassed Grade-3 edges (B.8.5)
S0a→S2a (E05/E06), S1→S2a (E08/E09), S0b→S2a (E14). E10/E11 (S2a→S1) are listed because XC-0 does not gate S1. E17 Reading P and C-P1-003 are not invoked. No edge is Locked, so every bypass is allowed.

## Non-claims
No hardware transfer, no necessity of R1 or realized effort, no ladder order, no lock or recommended-for-lock, and no change to D-P1-001.
