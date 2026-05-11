#!/bin/bash
# session-start.sh — Run at the start of every Claude session
# Clones or pulls the latest from GitHub so work is always current

REPO_URL="https://github.com/slaguru666/ChaosiumCon26.git"
TARGET_DIR="/home/claude/ChaosiumCon26"

if [ -d "$TARGET_DIR/.git" ]; then
  echo "Repo exists — pulling latest..."
  cd "$TARGET_DIR"
  git pull origin main
else
  echo "Cloning repo..."
  git clone "$REPO_URL" "$TARGET_DIR"
fi

echo ""
echo "✅ Ready. Working directory: $TARGET_DIR"
echo ""
echo "Scenarios:"
ls "$TARGET_DIR/scenarios/"
