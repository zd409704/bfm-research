# ISSUE-001 — Draft isolation is directory-policy only; CLI prompt delivery brittle

## Problem
Appendix A.3 requires "physical draft isolation — separate directories or branches; no shared scratch chat for Step 2." This run places both proposals under one shared tree (`proposals/`, shared `brief.md`). Authors with Read/Glob/Write can discover the sibling draft mid-contest if they search. Isolation currently depends on prompt discipline, not filesystem separation.

Separately: `claude -p` with a shell-expanded `$(cat prompt)` argument failed immediately with `Input must be provided either through stdin or as a prompt argument when using --print` (exit 1). Competing-author Codex `exec` path works with argv prompt but also prints `Reading additional input from stdin...`, suggesting ambiguous stdin handling under orchestrated redirects.

## Evidence from this run
- `logs/proposal-A-opus.stderr.txt`: prompt-delivery failure; `proposals/A.md` missing; opus_exit=1 at ~03:08 CST.
- `logs/proposal-B-astra.stderr.txt`: Codex running successfully on argv prompt while sharing the same run root.
- Methodology `orchestrating-ai-research-teams.md` A.3 item 2 vs brief roster that co-locates A/B under one canonical root.

## Proposed method amendment
1. Require per-author sandboxes for Step 2: e.g. `drafts/A/` and `drafts/B/` with no cross-read permissions / separate worktrees; Orchestrator merges only after both drafts are marked complete.
2. Document canonical CLI invocation patterns: prefer `claude -p ... < promptfile` (stdin) or explicit argv with verified non-empty prompt; forbid relying on nested `$(cat ...)` inside orchestrator wrappers without a length check.
3. Add a preflight checklist item: `test -s proposals/A.md` / length gate before opening Step 3.

## Contest impact
Does **not** invalidate the contest if Orchestrator re-runs Author A with stdin prompt and keeps Author B blind until both files exist. Continue under current brief.
