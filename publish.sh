#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

mkdir -p archive data/archive weekly

echo "[1/4] Rendering daily site..."
python3 render.py

DATE="$(python3 - <<'PY'
import json
with open("data/latest.json", encoding="utf-8") as f:
    print(json.load(f)["date"])
PY
)"

echo "[2/4] Staging changes..."
git add -A

if git diff --cached --quiet; then
    echo "[3/4] No changes to commit."
else
    echo "[3/4] Committing daily issue: ${DATE}"
    git commit -m "daily: ${DATE}"
fi

echo "[4/4] Pushing to GitHub..."
git push origin main

echo "Published ${DATE}"
