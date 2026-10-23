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
