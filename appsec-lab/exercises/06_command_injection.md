# 06 — OS Command Injection

**OWASP A03:2021 — Injection.** Often leads directly to remote code execution.

## Where

`GET /diag?host=...` builds a shell command by concatenation and runs it with
`shell=True`.

## Exploit

```bash
curl -s "http://127.0.0.1:5000/diag?host=localhost;%20echo%20INJECTED"
# output contains INJECTED -> a second command ran
```

The `;` ends the first command and starts the attacker's. Real payloads read
files, open reverse shells, or exfiltrate data.

> The lab uses a harmless `echo` as the "diagnostic" command so the injection is
> visible and safe offline. Real tools call `ping`/`nslookup`; the vulnerability
> class is identical.

## Source → Sink → Impact → Control

- **Source:** the `host` parameter.
- **Sink:** `subprocess.run(string, shell=True)`.
- **Impact:** run arbitrary OS commands as the app's user.
- **Control:** avoid the shell; pass an argument list with `shell=False`, and
  validate the input against a strict allowlist.

## The fix

```python
if not all(c.isalnum() or c in ".-" for c in host):
    return jsonify(error="invalid host"), 400
subprocess.run(["echo", "diagnostic for", host], capture_output=True, text=True)
```

No shell means no shell metacharacters to abuse. The allowlist is defence in depth.

## Detect with free tools

Semgrep and Bandit both flag `subprocess` with `shell=True` and a non-literal
command.

## Verify

```bash
pytest tests/test_exploits.py::test_command_injection -v
pytest tests/test_fixes.py::test_command_injection_blocked -v
```
