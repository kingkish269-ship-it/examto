# Room: Security Misconfiguration & Headers (OWASP A05)

**Topic:** OWASP Top 10 · **Difficulty:** core

## Story
The cheap, high-value hardening most apps skip.

## Theory (2 min)
Send security headers on every response:
- `X-Content-Type-Options: nosniff` (stop MIME sniffing),
- `X-Frame-Options: DENY` (stop clickjacking),
- `Content-Security-Policy` (limit what can load/run),
- `Referrer-Policy`.
Return **generic errors** to clients (no stack traces), and never run with debug
mode enabled on a reachable server.

## What you'll do
Read `appsec-lab/exercises/10_security_misconfiguration.md`; compare the response
headers in vulnerable vs secure mode.

## Going further
`appsec-lab/` misconfig lab; OWASP ZAP/Nikto flag missing headers automatically.
