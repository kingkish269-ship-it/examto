#!/usr/bin/env bash
# Secret scanning with Gitleaks (free).
# Install: see ../SETUP.md
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== Gitleaks: scanning working tree for secrets =="
# --no-git scans files on disk; drop it to scan full commit history instead.
gitleaks detect --source . --no-git -v || true

echo
echo "Expected: the hardcoded secret in vulnerable_app/app.py (exercise 09)."
