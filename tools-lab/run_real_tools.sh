#!/usr/bin/env bash
# Run the real free tools against this repo's labs.
# First: bash tools-lab/install.sh && source tools-lab/.venv/bin/activate
set +e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
# semgrep needs a writable settings dir; harmless if HOME is already writable.
export SEMGREP_SETTINGS_FILE="${SEMGREP_SETTINGS_FILE:-$REPO/tools-lab/.semgrep_settings.yml}"

echo "=================================================================="
echo " Bandit (SAST) on appsec-lab/vulnerable_app"
echo "=================================================================="
bandit -r appsec-lab/vulnerable_app 2>/dev/null | grep -E ">> Issue|Severity:" | head -20

echo; echo "=================================================================="
echo " Semgrep (SAST) with the lab ruleset"
echo "=================================================================="
semgrep scan --config appsec-lab/tools/semgrep-rules.yml --metrics=off appsec-lab/vulnerable_app 2>/dev/null \
  | grep -E "Findings|lab-" | head -20

echo; echo "=================================================================="
echo " Checkov (IaC) on iac-security-lab/terraform/insecure"
echo "=================================================================="
checkov -d iac-security-lab/terraform/insecure --compact 2>/dev/null | grep -E "Passed checks|Failed checks"

echo; echo "=================================================================="
echo " pip-audit (SCA) on a deliberately vulnerable requirement"
echo "=================================================================="
printf 'requests==2.19.0\n' > /tmp/vreq.txt
pip-audit -r /tmp/vreq.txt 2>/dev/null | head -6

echo; echo "=================================================================="
echo " sqlmap (DAST) — start the app first, then run:"
echo "   cd appsec-lab && python3 run_server.py   # terminal 1"
echo "   sqlmap -u 'http://127.0.0.1:5000/api/search?username=alice' -p username --batch"
echo "=================================================================="
