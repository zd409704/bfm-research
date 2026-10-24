#!/usr/bin/env bash
# Order-swapped adjudicator via Claude Sonnet through the authorized gateway.
set -euo pipefail
export TZ=America/Toronto LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
ROUND=/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24
LOG="$ROUND/logs/FR-adj-sonnet-order2.log"
PIDF="$ROUND/logs/FR-adj-sonnet-order2.pid"
PROMPT="$ROUND/prompts/FR-adj-sonnet-order2.txt"
cd /srv/claude
nohup /home/box/.local/bin/claude -p --model sonnet --effort medium \
  --dangerously-skip-permissions --permission-mode bypassPermissions \
  < "$PROMPT" > "$LOG" 2>&1 &
echo $! > "$PIDF"
echo "launched FR adj sonnet pid=$(cat "$PIDF") log=$LOG"
