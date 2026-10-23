# ISSUE-004 — Brief/timebase amended mid-contest without version log

## Problem
Timebase labeling changed mid-run (CST/Shanghai narrative → America/Toronto EDT) while deadline epoch stayed fixed. Progress and brief labels contradicted without a versioned Class-0 amendment log.

## Evidence
Steering messages; conflicting progress.md labels; epoch `1792706829` unchanged.

## Proposed amendment
Canonical time = unix epoch / UTC; local TZ labels display-only; brief amendments carry vN.M, date, class, reason.

## Contest impact
Class 0 (epoch unchanged). Continue with box-local America/Toronto labels; epoch sole deadline authority.
