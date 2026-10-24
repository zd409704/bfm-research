#!/usr/bin/env bash
set -euo pipefail
export TZ=America/Toronto LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
ROUND=/srv/claude/research/fb-beyond-imitation-acceleration/feedback-round-2026-10-24
LOG="$ROUND/logs/FR-adj-agy-order1.log"
PIDF="$ROUND/logs/FR-adj-agy-order1.pid"
PROMPT="$ROUND/prompts/FR-adj-agy-order1.txt"
cd /srv/claude
nohup /home/box/.local/bin/agy --effort high --dangerously-skip-permissions --add-dir /srv/claude \
  -p "$(cat "$PROMPT")" > "$LOG" 2>&1 &
echo $! > "$PIDF"
echo "launched FR adj agy pid=$(cat "$PIDF") log=$LOG"
