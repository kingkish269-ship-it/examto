# 14 — SAST (Static Application Security Testing)

## Theory

SAST reads **source code without running it** and flags risky patterns — the
automated version of the code review you did in module 13. It finds a **source**
(untrusted input) reaching a **sink** (dangerous call). Free tools: **Bandit**
(Python) and **Semgrep** (many languages, rules written in YAML).

Strengths: fast, runs in CI, points at the exact line. Weakness: false
positives — SAST sees code paths, not real exploitability (that's DAST's job).

## Lab

```bash
cd /workspaces/examto/rooms/sast
python3 scan.py vulnerable_example.py
```
This tiny scanner finds the `shell=True` command-injection line — the same idea
as a real tool. Now run a real one on the lab app:

```bash
pip install bandit
bandit -r /workspaces/examto/appsec-lab/vulnerable_app
```
Bandit reports issues like `subprocess` with `shell=True`, weak MD5, and
`pickle`. Optional: `pip install semgrep && semgrep --config auto /workspaces/examto/appsec-lab`.

Also run **Semgrep** (the headline multi-language SAST tool) with our ruleset:
```bash
cd /workspaces/examto
semgrep scan --config appsec-lab/tools/semgrep-rules.yml appsec-lab/vulnerable_app
```
It reports **5 findings** (MD5 password, unvalidated urlopen/SSRF, subprocess
`shell=True`, pickle). `tools-lab/` installs and runs these for you.

## Verify

- The mini scanner reports `COMMAND INJECTION`.
- Bandit lists findings (MD5 High, SQLi, pickle, subprocess, hardcoded secrets).
- Semgrep reports 5 findings with the lab ruleset.

## Key takeaways

- SAST = automated source-code scanning for insecure patterns.
- Bandit (Python), Semgrep (multi-language, YAML rules).
- Expect false positives; confirm real exploitability with DAST.
