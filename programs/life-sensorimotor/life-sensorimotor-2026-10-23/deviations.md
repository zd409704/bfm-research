# Deviations (S0a runner)

Metrics, thresholds, seeds, attempt cap, and mechanism are unchanged from PLAN.md.
PLAN.md sha256 matched logs/seal.txt (d76cf314...) before running.

1. **Interpretation of "effective latency τ" (attempt 1 -> 2).** Attempt 1 applied τ as a pure sensor delay on top of the 2 ms actuator lag and a 1 ms ZOH sample period. Total latency then exceeded τ, and the τ=5 ms peak was 0.01023 > b, so the verdict was FAIL. Attempt 2 treats τ as the total effective latency: pure delay = max(τ − 2 ms lag − 0.5 ms mean ZOH hold, 0). Controller gain (200, Proposal B's candidate), clip (±3), noise, lag, seeds, and threshold are unchanged. This is a harness interpretation fix, not a threshold change. Attempt 1's FAIL is in runs.log.
2. **Disturbance class** taken from Proposal B's spike section: constant ±1, onset uniform in [0,4) ms (continuous, off-grid), 250 ms episode. Each seed is evaluated with both signs, and the peak is the mean over signs. The PASS rule is applied per seed.
3. **Fixture B:** L*_LIP = ln(1+a·b/D)/a with b=0.01 and D=1, the same as fixture A. This is a placeholder, since the real LIP envelope is undefined.
4. **Caveat:** with the attempt-2 convention, the closed-loop peak first exceeds b at τ=8 ms, below the analytic L*=9.53 ms. The sweep therefore discriminates, but the controller and lag are not tight to L*. The analytic L* is a necessary-condition bound.
