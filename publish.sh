
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python3 render.py
DATE="$(python3 - <<'PY'
import json
print(json.load(open("data/latest.json"))["date"])
PY
)"

git add config.json data index.html archive weekly README.md .github hermes render.py publish.sh
git commit -m "daily: ${DATE}" || true
git push origin main
