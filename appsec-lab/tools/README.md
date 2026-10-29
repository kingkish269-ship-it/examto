# Free security tools

Every tool here is free and open source. Install instructions are in
[`../SETUP.md`](../SETUP.md). Run them only against this lab locally or systems
you are authorised to test.

| Tool | Type | Finds | Script |
|---|---|---|---|
| Semgrep | SAST | injection, SSRF, weak crypto, dangerous sinks | `run_semgrep.sh` |
| Gitleaks | Secret scan | committed credentials and keys | `run_gitleaks.sh` |
| OWASP ZAP | DAST | XSS, missing headers, traversal on the running app | `run_zap_baseline.sh` |
| sqlmap | DAST | SQL injection (optional) | see `../exercises/02_sql_injection.md` |
| Nikto | DAST | server misconfiguration (optional) | see `../exercises/10_security_misconfiguration.md` |

## Static vs dynamic

- **SAST** reads source code without running it. Fast, runs in CI, finds the bug
  at the line. Produces false positives.
- **DAST** attacks the running app. Confirms real exploitability, finds runtime
  and config issues, but needs the app deployed and misses code it never reaches.

Use both. In this lab, Semgrep finds the injection in `app.py`; ZAP confirms the
XSS and missing headers against the live server.

## Suggested order

1. `run_gitleaks.sh` — catch secrets first; it is the cheapest, highest-signal check.
2. `run_semgrep.sh` — map findings to the exercises.
3. Start the app, then `run_zap_baseline.sh` — confirm the dynamic findings.
