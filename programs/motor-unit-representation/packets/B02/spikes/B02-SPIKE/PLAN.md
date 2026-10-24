# Spike Plan B02-SPIKE — E0–E4 Sync, Rule Calibration, Coverage Gates

**Experiment ID**: `B02_SCENE_SYNC_RULE_CALIBRATION_COVERAGE`
**Device Preference**: CPU deterministic simulator / synthetic episode scheduler.

## Pass Gates
- G1: Every synthetic E3 episode contains \(\ge 25\) consecutive sustained-load steps.
- G2: Every synthetic E4 episode contains a load-release edge and \(\ge 20\) recovery steps.
- G3: Cross-coverage matrix \(144\times 5\) cells each meet a declared minimum quota under the proposed sampler (or a scaled \(N_{\mathrm{cfg}}\times 5\) proxy with identical logic).
- G4: Static-hold evaluation uses \(g_{13}^{\mathrm{hold}}\) with \(\dot q^\star=\widehat{\ddot q}^\star=0\); no moving-target injection in that panel.
