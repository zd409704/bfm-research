# ISSUE-002 — Wall-clock / timezone and pause-resume underspecified

## Problem
The methodology states wall-clock deadlines and pause-at-deadline behavior but does not pin which machine clock is authoritative when the orchestrator box, user laptop, and agent narrative use different timezones. This run saw labels flip CST→EDT while the deadline *epoch* stayed fixed. Without an explicit rule, progress.md timestamps become ambiguous and human/agent schedules diverge.

Also missing: a standard pause/resume packet (what to freeze, how to resume Step N without reopening Step 2 drafts).

## Evidence from this run
- `deadline_epoch.txt` held constant (`1792706829`) while human-facing timezone labels changed from Asia/Shanghai framing to America/Toronto EDT mid-run.
- Progress notes required an external steering message to correct timezone labels; methodology did not specify "box-local epoch is sole authority; label with box TZ name."

## Proposed method amendment
1. Require `deadline_epoch.txt` (unix seconds) as sole deadline authority; progress timestamps must include box `date +%Z` / IANA TZ.
2. Add pause/resume artifact: `pause.md` with completed step, open files, next action, and "do not mutate proposals/ after Step 2 close."
3. Optional: copy `timedatectl` / `date` snapshot into `logs/run-start.md`.

## Contest impact
Does not invalidate contest; epoch deadline honored. Continue.
