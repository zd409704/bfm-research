# Deviations from PLAN v2 (sha256 3d7b9af6…ac41)

**No scientific or threshold deviations.** The full grid ran as sealed (no reduction): about 154k episodes per pipeline pass, about 3 min CPU per pass, two passes for H1. The budget was not an issue.

Process notes, none of which changed the spec:
1. PLAN v2 was sealed (`PLAN.sha256`) before `run.py` existed. `run.py` was then written to it and smoke-tested with `--smoke` (reduced n, output in a `smoke_out/` directory that was deleted). The smoke run is not used for any result. It showed H3 failing and k* = -1, as expected, because n is too small at smoke scale. No PLAN text was edited after sealing.
2. The first launch of the full run failed before starting, because the redirect target `/tmp/claude/` did not exist. It was relaunched with output under `$TMPDIR`. The result files come from the single completed relaunch.
3. Implementation choices where PLAN left detail open, with no effect on the spec: Publisher noise is drawn up front from its own RNG stream; `H4` is run once with 50 episodes (every fifth has `M = 0`); calibration `k*` is found by incrementing `k` while the CP upper bound ≤ `0.25·r_w`; the p95 latency uses the `ceil(0.95·(n−1))` order statistic of the sorted latencies (misses = +inf).
4. PLAN §12 says `VERDICT.json` carries `H1..H4`. It does. `results.json` is the byte-identical-compared science file (the v1 "verdict.json" role); `VERDICT.json` is the summary.
5. `scipy` is unavailable, so Clopper–Pearson bounds are computed by exact binomial-sum bisection (`xcstats.py`). They were not validated against scipy.

## Orchestrator process note (post-runner)
The experiment-runner's first full `python3 -I run.py` stalled after H4 (no further log lines; process gone). Orchestrator re-ran smoke (INVALID H3, small-n; not used) then full grid under the sealed PLAN; `VERDICT.json` / `METRICS.md` match the runner's DONE summary. No PLAN text change.
