# 15 — DAST (Dynamic Application Security Testing)

## Theory

DAST **attacks the running application** to confirm what's actually exploitable.
Where SAST reads code, DAST sends real requests and reads responses — catching
runtime and configuration issues SAST can't see, and proving a finding is real.
The free standard is **OWASP ZAP**.

Strengths: confirms exploitability, finds config/header issues. Weakness: only
tests what it can reach; needs the app running.

## Lab

Start the app (appsec-lab), then attack it like DAST does — by hand first:

```bash
cd /workspaces/examto/appsec-lab
source .venv/bin/activate 2>/dev/null
python3 run_server.py &
sleep 2
# Probe for reflected XSS (module 04) against the live app:
curl -s "http://127.0.0.1:5000/greet?name=<script>alert(1)</script>"
# Probe response headers (module 09):
curl -s -D - http://127.0.0.1:5000/health -o /dev/null
```

You confirmed a live vulnerability (reflected `<script>`) and missing headers —
that's DAST thinking. Automate it with ZAP (needs Docker):

```bash
bash tools/run_zap_baseline.sh      # OWASP ZAP baseline scan against the app
```

## Verify

- The live app reflects your `<script>` (confirmed XSS).
- The ZAP baseline (if you run it) reports XSS + missing headers.

## Key takeaways

- DAST attacks the running app to prove exploitability.
- OWASP ZAP (free) is the go-to; a baseline scan is safe to run on your lab.
- Use SAST + DAST together — static finds it, dynamic confirms it.
