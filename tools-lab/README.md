# Tools Lab — use the REAL free security tools on our labs

The other labs teach the *logic* with small Python stand-ins. This lab runs the
**actual industry tools** against the same targets, so you get hands-on with what
employers use. Every command below was run against this repo and the expected
result is shown.

## Install (once)

```bash
cd /workspaces/examto/tools-lab
bash install.sh
source .venv/bin/activate
```

That installs the pip-based tools: **bandit, semgrep, pip-audit, checkov,
sqlmap**. Binary tools (Trivy, Grype, gitleaks, hadolint, Syft, Cosign, OWASP
ZAP) are single downloads — see the end of this file.

## Run them all

```bash
# from the repo root, with the venv active:
bash tools-lab/run_real_tools.sh
```

## What each tool finds in our labs (verified)

### Bandit — SAST (Python)
```bash
bandit -r appsec-lab/vulnerable_app
```
Finds our intentional bugs: `pickle` (B403), `subprocess` (B404), hardcoded
secrets (B105), **weak MD5** (B324, High), **SQL injection** (B608), and unsafe
`urlopen` (B310). Maps to course modules 02, 03, 07, 08.

### Semgrep — SAST (multi-language)
```bash
semgrep scan --config appsec-lab/tools/semgrep-rules.yml appsec-lab/vulnerable_app
```
Reports **5 findings** with our ruleset: md5 password, unvalidated `urlopen`
(SSRF), `subprocess` shell=True, and `pickle.loads`. Try the community rules too:
`semgrep scan --config auto appsec-lab/vulnerable_app` (needs internet for the
registry). Maps to modules 13, 14.
> If semgrep errors with a read-only `~/.semgrep`, your HOME isn't writable; in a
> Codespace it is. Workaround: `export SEMGREP_SETTINGS_FILE=$PWD/.semgrep.yml`.

### Checkov — IaC
```bash
checkov -d iac-security-lab/terraform/insecure --compact
```
**31 failed checks** on our insecure Terraform — SSH (22) and RDP (3389) open to
the internet, RDS unencrypted, public S3, and more. The secure folder passes.
Maps to module 21.

### pip-audit — SCA (dependencies)
```bash
printf 'requests==2.19.0\n' > /tmp/vreq.txt
pip-audit -r /tmp/vreq.txt
```
Reports **known CVEs** (e.g. `requests 2.19.0` → fix 2.20.0 / 2.31.0 / 2.32.x).
Run against the whole environment with just `pip-audit`. Maps to module 16.

### sqlmap — DAST (SQL injection)
Start the app first (`cd appsec-lab && python3 run_server.py`), then:
```bash
sqlmap -u "http://127.0.0.1:5000/api/search?username=alice" -p username --batch
```
sqlmap confirms the `username` parameter is injectable. Maps to module 02.

## Binary tools (download when you want them)

```bash
# Trivy (SCA + container + IaC):
curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
trivy fs appsec-lab            # scan dependencies
trivy config iac-security-lab  # scan IaC/manifests

# gitleaks (secret scanning):  download from github.com/gitleaks/gitleaks/releases
gitleaks detect --source . --no-git -v     # finds the hardcoded secret in appsec-lab

# hadolint (Dockerfile):  github.com/hadolint/hadolint/releases
hadolint container-k8s-lab/manifests/insecure/Dockerfile

# OWASP ZAP (DAST), via Docker:
#   bash appsec-lab/tools/run_zap_baseline.sh
```

Always inspect an install script before piping it to a shell — that is module 22
(supply chain) in action.

## Safety

Run offensive tools (sqlmap, ZAP, nuclei) only against this repo's labs on
`127.0.0.1`, or systems you are authorised to test.
