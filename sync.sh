#!/bin/bash
# sync.sh — Push all changes to GitHub
# Run this after any work session to keep the repo up to date

cd "$(dirname "$0")"

git add -A
git status

read -p "Commit message: " msg
if [ -z "$msg" ]; then
  msg="Work in progress update"
fi

git commit -m "$msg"
git push origin main

echo ""
echo "✅ Synced to https://github.com/slaguru666/ChaosiumCon26"
