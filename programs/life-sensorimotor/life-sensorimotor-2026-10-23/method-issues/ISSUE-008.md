# ISSUE-008 — Runner reinterpreted “effective latency” between attempts

## Problem
Spike attempt 1 FAIL vs attempt 2 PASS differed by how τ maps to pure delay vs total effective latency. PLAN.md said “effective latency τ” without defining stacking with actuator lag and ZOH. Runner treated attempt 2 as a harness fix (deviations.md); thresholds unchanged. This is a gray zone vs “must not change the mechanism under test.”

## Evidence
spikes/runs.log attempt 1 FAIL / attempt 2 PASS; spikes/deviations.md item 1.

## Proposed amendment
PLAN.md must define latency composition algebraically before attempt 1. Reinterpretation requires Orchestrator PLAN amendment + reseal, not silent runner fix. Optionally cap “interpretation fixes” at 0 without reseal.

## Contest impact
Disclosed. Both attempts logged. decision.md quotes attempt 2 and notes attempt 1. Continue provisional.
