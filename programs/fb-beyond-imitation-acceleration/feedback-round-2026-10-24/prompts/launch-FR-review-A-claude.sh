#!/usr/bin/env bash
# Blind Reviewer A — Claude Opus. Run only via the authorized Claude gateway agent.
set -euo pipefail
export TZ=America/Toronto
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
ROUND=/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24
LOG="$ROUND/logs/FR-review-A-claude.log"
PIDF="$ROUND/logs/FR-review-A-claude.pid"
PROMPT="$ROUND/prompts/FR-review-A-on-B.txt"
cd /srv/claude
nohup /home/box/.local/bin/claude -p --model opus --effort medium \
  --dangerously-skip-permissions --permission-mode bypassPermissions \
  < "$PROMPT" > "$LOG" 2>&1 &
echo $! > "$PIDF"
echo "launched FR review A pid=$(cat "$PIDF") log=$LOG"
