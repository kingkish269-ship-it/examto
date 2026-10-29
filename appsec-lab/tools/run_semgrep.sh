#!/usr/bin/env bash
# Static analysis of the lab app with Semgrep (free).
# Install: pip install semgrep
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== Semgrep: community rules (auto) =="
semgrep --config auto --error vulnerable_app/ || true

echo
echo "== Semgrep: lab custom rules =="
semgrep --config tools/semgrep-rules.yml vulnerable_app/ || true

echo
echo "Map each finding to the matching file in exercises/."
