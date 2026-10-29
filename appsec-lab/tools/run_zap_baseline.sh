#!/usr/bin/env bash
# Dynamic baseline scan with OWASP ZAP (free) via Docker.
# Start the lab app first, in another terminal:  python run_server.py
set -euo pipefail

TARGET="${1:-http://127.0.0.1:5000}"

echo "== OWASP ZAP baseline scan against ${TARGET} =="
echo "Requires Docker. The app must already be running locally."

# The baseline scan is passive + a few safe active checks. Safe for the lab.
docker run --rm --network host \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t "${TARGET}" -I || true

echo
echo "Expect alerts for reflected XSS (/greet) and missing security headers."
echo "Map them to exercises 03 and 10."
