# 05 — Path Traversal

**OWASP A01/A05:2021.**

## Where

`GET /download?file=...` joins the user-supplied name onto a base directory.

## Exploit

```bash
curl -s "http://127.0.0.1:5000/download?file=../lab_secret_outside.txt"
# returns a file from OUTSIDE the intended directory
```

`../` walks up out of the web root. On a real server this reads `/etc/passwd`,
application config, or secrets.

## Source → Sink → Impact → Control

- **Source:** the `file` parameter.
- **Sink:** a file-system read.
- **Impact:** read arbitrary files the server process can access.
- **Control:** resolve the final path and confirm it stays inside the intended
  base directory; reject anything else.

## The fix

```python
target = (base / name).resolve()
if not str(target).startswith(str(base.resolve()) + os.sep):
    return jsonify(error="forbidden"), 403
```

Canonicalise with `resolve()` first, then compare, so `../` and symlink tricks
are neutralised. Prefer mapping an id to a known filename over accepting raw
paths at all.

## Detect with free tools

- Semgrep flags user input flowing into file opens.
- OWASP ZAP has a path-traversal active scan rule.

## Verify

```bash
pytest tests/test_exploits.py::test_path_traversal -v
pytest tests/test_fixes.py::test_path_traversal_blocked -v
```
