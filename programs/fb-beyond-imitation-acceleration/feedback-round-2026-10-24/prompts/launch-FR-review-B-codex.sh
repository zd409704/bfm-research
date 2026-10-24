#!/usr/bin/env bash
# Blind Reviewer B — Codex gpt-6-astra
set -euo pipefail
export TZ=America/Toronto
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
ROUND=/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24
LOG="$ROUND/logs/FR-review-B-codex.log"
PIDF="$ROUND/logs/FR-review-B-codex.pid"
PROMPT="$ROUND/prompts/FR-review-B-on-A.txt"
cd /srv/claude
nohup /home/box/.local/bin/codex exec -C /srv/claude \
  -m gpt-6-astra \
  -c model_reasoning_effort=high \
  -s workspace-write \
  --skip-git-repo-check \
  --dangerously-bypass-approvals-and-sandbox \
  --add-dir /srv/claude \
  < "$PROMPT" > "$LOG" 2>&1 &
echo $! > "$PIDF"
echo "launched FR review B pid=$(cat "$PIDF") log=$LOG"
