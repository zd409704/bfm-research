#!/usr/bin/env bash
set -euo pipefail
export TZ=America/Toronto
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
ROUND=/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24
LOG="$ROUND/logs/FR-disposition-claude.log"
PIDF="$ROUND/logs/FR-disposition-claude.pid"
PROMPT="$ROUND/prompts/FR-disposition-merge.txt"
cd /srv/claude
nohup /home/box/.local/bin/claude -p --model opus --effort medium \
  --dangerously-skip-permissions --permission-mode bypassPermissions \
  < "$PROMPT" > "$LOG" 2>&1 &
echo $! > "$PIDF"
echo "launched FR disposition pid=$(cat "$PIDF") log=$LOG"
