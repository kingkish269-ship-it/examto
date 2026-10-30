# Room: DAST — attack the running app

**Topic:** DAST (dynamic analysis) · **Difficulty:** intro

## The story

SAST reads code; **DAST attacks the running application** to confirm what is
actually exploitable. Tools like OWASP ZAP do this automatically. Here you do it
by hand against the lab's deliberately vulnerable web app.

## Theory (1 minute)

You send input a web app does not expect and watch what happens. A classic:
**reflected cross-site scripting (XSS)** — the app echoes your input straight
into the HTML, so a `<script>` you send runs in the victim's browser.

## What you will actually do (in your terminal)

Start the vulnerable app (leave it running):

```bash
cd appsec-lab
python3 -m venv .venv 2>/dev/null; . .venv/bin/activate 2>/dev/null; pip install -q -r requirements.txt
python3 run_server.py
```

In a second terminal, send a script payload and look at the response:

```bash
curl -s "http://127.0.0.1:5000/greet?name=<script>alert(1)</script>"
```

You will see your `<script>` reflected back unescaped — the attack worked.

## Your task

What is the OWASP name of this vulnerability (the three-letter abbreviation)?

```bash
python3 rooms.py submit dast <abbreviation>
```

## Going further

Automate it: `tools/run_zap_baseline.sh` in `appsec-lab/` runs an OWASP ZAP
baseline scan against the same app.
