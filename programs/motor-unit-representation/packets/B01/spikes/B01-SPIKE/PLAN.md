# Spike Plan B01-SPIKE — Privileged Future-Force Leakage Jacobian Audit

**Experiment ID**: `B01_PRIVILEGED_FUTURE_FORCE_JACOBIAN`
**Preregistered Before Step 2 Seals**
**Device Preference**: CUDA if available; else honest CPU FP32/FP64.

## Hypothesis
Sanitizing Groups 18–21 of \(p_{5065}\) so that only exogenous generator Markov state \(\xi_t\) remains (no endogenous \(t+1..t+K\) reaction forces) restores non-degenerate \(\|\partial F/\partial a\|_2\) relative to \(\|\partial F/\partial p_{\mathrm{future}}\|_2\) and reduces one-step Bellman residual bias under controlled plant rollouts.

## Protocol (Minimum)
1. Construct a minimal differentiable surrogate \(F_\eta(x,p,a,z)\) with a privileged compressor over a synthetic \(p\) that embeds (i) causal \(\xi_t\) and (ii) an optional future-force window correlated with \(a\).
2. Measure Jacobian norms before/after masking the future window.
3. Measure TD/Bellman residual when targets are generated from a known plant with and without leakage.

## Pass Gates (Pre-Registered)
- G1: With leakage ON, \(\|\partial F/\partial p_{\mathrm{future}}\|_2 / (\|\partial F/\partial a\|_2 + 10^{-8}) \ge 5.0\).
- G2: With leakage OFF (causal sanitization), the same ratio \(\le 1.0\).
- G3: Causal sanitization reduces absolute one-step Bellman residual bias by \(\ge 2\times\) vs leaked \(p\).
- G4: Deployed modules \(B,\pi\) never receive \(p\) (structural assert).
