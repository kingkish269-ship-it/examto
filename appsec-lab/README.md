# Application Security Lab

A hands-on application security lab built around one deliberately vulnerable
Flask app and a test suite that proves each attack works and each fix stops it.
It uses only free, open-source tools. It is designed for an engineer who already
knows endpoint, network, cloud, and data security and now wants practical
application security and secure-code-review skill.

> **Safety:** the app in `vulnerable_app/` is intentionally insecure. Run it only
> on your own machine, bound to `127.0.0.1`. Never deploy it or point it at real
> data. This is the same category of tool as OWASP Juice Shop or DVWA.

## Why this format

You learn application security fastest by doing three things to one codebase:

1. **Attack it** — run the exploit and see the impact.
2. **Read both versions** — the vulnerable branch and the fixed branch sit side
   by side in the same function, controlled by one `SECURE` flag.
3. **Prove the fix** — a test shows the attack now fails.

This mirrors a real security engineer's job: find it, explain it, fix it, verify it.

## What it covers

Ten vulnerabilities, each mapped to the OWASP Top 10 and to a free tool that
detects it:

| # | Vulnerability | OWASP 2021 | Detecting tool |
|---|---|---|---|
| 01 | Broken access control (IDOR) | A01 | Manual / ZAP |
| 02 | SQL injection | A03 | Semgrep, sqlmap |
| 03 | Reflected XSS | A03 | Semgrep, ZAP |
| 04 | SSRF | A10 | Manual / Semgrep |
| 05 | Path traversal | A01/A05 | Semgrep, ZAP |
| 06 | OS command injection | A03 | Semgrep |
| 07 | Insecure deserialization | A08 | Semgrep (Bandit) |
| 08 | Authentication & session flaws | A07 | Manual / ZAP |
| 09 | Cryptographic failures & secrets | A02 | Semgrep, Gitleaks |
| 10 | Security misconfiguration | A05 | ZAP, Nikto |

## Setup

```bash
cd appsec-lab
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the vulnerable app

```bash
python run_server.py               # http://127.0.0.1:5000  (vulnerable)
LAB_SECURE=1 python run_server.py  # the fixed version
```

## Run the tests

```bash
pytest tests/ -v
```

- `tests/test_exploits.py` — every attack **succeeds** against the vulnerable app.
- `tests/test_fixes.py` — every attack is **blocked** by the secure version.

## How to work through it

Follow [`PLAN.md`](PLAN.md). For each vulnerability:

1. Read the exercise in [`exercises/`](exercises/).
2. Reproduce the attack with the provided `curl` command.
3. Open `vulnerable_app/app.py` and read the `if SECURE` branch for that route.
4. Run the matching test and confirm the behaviour.
5. Run the free tool in [`tools/`](tools/) that detects the class of bug.

## Contents

- `vulnerable_app/` — the app (vulnerable + fixed in one place)
- `exercises/` — one walkthrough per vulnerability
- `tests/` — exploit proofs and fix proofs
- `tools/` — free SAST/DAST/secret-scanning guides and runner scripts
- `threat-modeling/` — a reusable template and a worked example
- `PLAN.md` — an eight-week schedule
- `SETUP.md` — installing the free tools
