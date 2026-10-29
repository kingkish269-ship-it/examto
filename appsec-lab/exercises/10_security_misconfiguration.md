# 10 — Security Misconfiguration

**OWASP A05:2021 — Security Misconfiguration.**

## Where

- Response headers in the `harden` function.
- The 500 error handler.
- The debug flag in `run_server.py`.

## Flaws

1. **Missing security headers.** Vulnerable mode sends no
   `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, or
   `Referrer-Policy`.
2. **Verbose errors.** The vulnerable error handler returns the raw exception,
   leaking stack and internal detail.
3. **Debug mode.** Running Flask with `debug=True` exposes the Werkzeug
   debugger, which allows code execution. The lab always runs `debug=False`;
   understand why enabling it on a reachable server is dangerous.

## Check it

```bash
curl -s -D - "http://127.0.0.1:5000/health" -o /dev/null          # vulnerable: no CSP
LAB_SECURE=1 python run_server.py   # then re-run the curl: headers appear
```

## The fixes

```python
resp.headers["X-Content-Type-Options"] = "nosniff"
resp.headers["X-Frame-Options"] = "DENY"
resp.headers["Content-Security-Policy"] = "default-src 'none'"
resp.headers["Referrer-Policy"] = "no-referrer"
# generic error, no internals:
return jsonify(error="internal server error"), 500
```

Set security headers centrally for every response. Return generic errors to
clients and log the detail server-side. Never run production with debug enabled.

## Detect with free tools

- OWASP ZAP baseline scan reports missing headers (`tools/run_zap_baseline.sh`).
- Nikto flags missing headers and common misconfigurations.

## Verify

```bash
pytest tests/test_exploits.py::test_missing_security_headers -v
pytest tests/test_fixes.py::test_security_headers_present -v
```
