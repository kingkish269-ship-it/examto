# 04 — Cross-Site Scripting (XSS) — OWASP A03

## Theory

The app takes your input and puts it into the HTML page **without encoding it**.
If your input is `<script>...</script>`, the victim's browser runs it as code.

Impact: steal the victim's session cookie, act as them, deface the page, or
redirect them. **Reflected XSS** is when your input is echoed straight back in
the response (e.g. a search term shown on the results page).

Analogy: you slip a note into someone else's letter, and they read it aloud as
if it were their own.

**The fix: contextual output encoding** — convert `<` to `&lt;` etc. before it
reaches the page, so the browser shows it as text instead of running it. A
strong **Content-Security-Policy** header is a valuable second layer.

## Lab

App running. Second terminal:

```bash
curl -s "http://127.0.0.1:5000/greet?name=<script>alert(1)</script>"
```

You'll see your `<script>` tag reflected back **unescaped** inside the page —
in a browser it would execute.

Fix — restart secure:
```bash
# Ctrl+C, then:
LAB_SECURE=1 python3 run_server.py
```
Re-run it: the response now shows `&lt;script&gt;` — encoded, harmless.

## Verify

- Insecure: `<script>` appears raw in the HTML.
- Secure: it appears as `&lt;script&gt;` (encoded).

## Key takeaways

- XSS = untrusted input rendered into HTML without encoding.
- Fix = encode output for its context (HTML/attribute/JS/URL) + CSP.
- Treat every piece of data going into a page as untrusted.
