# ISSUE-001 — Wrong Astra model id on first Prin-1 launch (Class 0 correction)

## Problem
First Astra claim-author invoke used `-m gpt-5.4-astra` instead of roster-pinned `gpt-6-astra`.

## Correction
Killed the mistyped session before claim files were relied upon; relaunched with `gpt-6-astra`. Any partial drafts/B or C-P1-001/002/003 from the mistyped session are discarded and rewritten.

## Class
Class 0 (mechanical correction; contest-neutral).
