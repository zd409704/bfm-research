# ISSUE-003 — Relaunch overwrote failure evidence

## Problem
Per-attempt logs were overwritten: `logs/proposal-A-opus.stderr.txt` cited by ISSUE-001 is now 0 bytes after stdin relaunch reused the filename.

## Evidence
ISSUE-001 cites non-empty stderr; current file is 0 bytes (mtime at relaunch). `progress.md` still records the failure.

## Proposed amendment
Per-attempt append-only names: `logs/<step>-<role>-attempt<N>.{stdout,stderr}` (v1 §12.4).

## Contest impact
None (Class 0). Continue.
