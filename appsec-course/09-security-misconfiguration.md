# 09 — Security Misconfiguration & Headers — OWASP A05

## Theory

The cheapest, highest-value hardening — and the most often skipped. Three parts:

**Security headers** on every response:
- `X-Content-Type-Options: nosniff` — stop the browser guessing content types.
- `X-Frame-Options: DENY` — stop clickjacking (your page in a hidden iframe).
- `Content-Security-Policy` — limit what scripts/resources can load or run.
- `Referrer-Policy` — control what URL leaks in the Referer header.

**Generic errors** — never return stack traces or internal detail to users.

**No debug mode** on anything reachable — debug consoles can allow code
execution.

## Lab

App running (appsec-lab, module 00). Second terminal:

```bash
# Insecure mode — look at the headers (no CSP, no nosniff):
curl -s -D - "http://127.0.0.1:5000/health" -o /dev/null
```

Now restart in secure mode (`Ctrl+C`, then):
```bash
LAB_SECURE=1 python3 run_server.py
```
Re-run the curl:
```bash
curl -s -D - "http://127.0.0.1:5000/health" -o /dev/null | grep -iE "content-security|x-content-type|x-frame|referrer"
```
The security headers now appear.

## Verify

- Insecure: response has no security headers.
- Secure: `Content-Security-Policy`, `X-Content-Type-Options`, etc. are present.

Real tools that flag missing headers automatically: OWASP ZAP baseline
(`appsec-lab/tools/run_zap_baseline.sh`) and Nikto.

## Key takeaways

- Set security headers centrally for every response.
- Return generic errors to users; log the detail server-side.
- Never run production with debug enabled.
