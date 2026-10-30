#!/usr/bin/env bash
# Install the pip-based real security tools into a local venv.
set -e
cd "$(dirname "$0")"

python3 -m venv .venv
. .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet bandit semgrep pip-audit checkov sqlmap

echo
echo "Installed (activate with: source tools-lab/.venv/bin/activate):"
echo "  bandit    - SAST (Python)"
echo "  semgrep   - SAST (multi-language)"
echo "  pip-audit - SCA (Python dependencies)"
echo "  checkov   - IaC (Terraform/K8s/etc.)"
echo "  sqlmap    - DAST (SQL injection)"
echo
echo "Binary tools (optional, download from each project's releases):"
echo "  trivy, grype, gitleaks, hadolint, syft, cosign, nuclei, OWASP ZAP"
echo
echo "Next:  source tools-lab/.venv/bin/activate && bash tools-lab/run_real_tools.sh"
