# ISSUE-007 — Review publish-after-all not enforced

## Problem
v1 §11.2 asks to write reviews to logs first and move both into reviews/ only after both complete. Opus wrote directly to reviews/A-on-B.md while Astra review was still running, so a file-tool reviewer could have seen a sibling review.

## Evidence
A-on-B.md mtime during B-on-A run; Astra deposited after.

## Proposed amendment
Orchestrator-enforced publish-after-all; reviewers write only under private dirs.

## Contest impact
Disclose. Astra (read-only) could not see A-on-B via filesystem write path in its sandbox; residual risk is low but unaudited for Opus side during overlap. Contest continues.
