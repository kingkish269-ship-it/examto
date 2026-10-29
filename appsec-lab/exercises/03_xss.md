# 03 — Reflected Cross-Site Scripting (XSS)

**OWASP A03:2021 — Injection.**

## Where

`GET /greet?name=...` reflects the name into HTML without encoding.

## Exploit

```bash
curl -s "http://127.0.0.1:5000/greet?name=<script>alert(1)</script>"
# the script tag is returned verbatim inside the page
```

In a browser, that script runs in the victim's session. Real impact: stealing
session tokens, performing actions as the victim, or defacing the page.

## Source → Sink → Impact → Control

- **Source:** the `name` parameter.
- **Sink:** the HTML response body.
- **Impact:** attacker JavaScript runs in the victim's browser with their
  privileges.
- **Control:** contextual output encoding. Encode data for the context it lands
  in (HTML body, attribute, JS, URL). A strong Content-Security-Policy is a
  valuable second layer (see exercise 10).

## The fix

```python
from markupsafe import escape
body = f"<h1>Hello {escape(name)}</h1>"
```

`escape` turns `<script>` into `&lt;script&gt;`, so the browser displays it as
text instead of executing it.

## Detect with free tools

- Semgrep flags unescaped reflection of request data into responses.
- OWASP ZAP's active scan reports the reflected XSS on `/greet`.

## Verify

```bash
pytest tests/test_exploits.py::test_reflected_xss -v
pytest tests/test_fixes.py::test_xss_encoded -v
```
