# Setup: free tools only

Nothing here needs a paid licence or cloud account. Install what each week
requires; you do not need everything on day one.

## 1. The lab itself (required)

```bash
cd appsec-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

## 2. Semgrep — static analysis (SAST)

Finds injection, SSRF, weak crypto, and dangerous functions in source code.

```bash
pip install semgrep
semgrep --config auto vulnerable_app/
semgrep --config tools/semgrep-rules.yml vulnerable_app/
```

Docs: https://semgrep.dev/docs/

## 3. Gitleaks — secret scanning

Finds committed credentials and keys.

```bash
# Linux/macOS: download the binary from the releases page, or:
# brew install gitleaks     (macOS)
gitleaks detect --source . --no-git -v
```

Docs: https://github.com/gitleaks/gitleaks

## 4. OWASP ZAP — dynamic analysis (DAST)

Scans the running app for XSS, missing headers, traversal, and more.
Download the free cross-platform build from the OWASP ZAP site, or use the
Docker image described in `tools/run_zap_baseline.sh`.

Docs: https://www.zaproxy.org/docs/

## 5. sqlmap — SQL injection (optional)

```bash
pip install sqlmap        # or clone the GitHub repo
```

Use only against this lab, running locally. See `exercises/02_sql_injection.md`.

Docs: https://github.com/sqlmapproject/sqlmap

## 6. Nikto — web server misconfiguration (optional)

A Perl tool that flags misconfigurations and missing headers. Install from your
package manager or the GitHub repo.

Docs: https://github.com/sullo/nikto

## Legal and ethical note

Run these tools only against this lab on your own machine, or against systems
you are explicitly authorised to test in writing. Scanning or attacking systems
without authorisation is illegal in most countries.
