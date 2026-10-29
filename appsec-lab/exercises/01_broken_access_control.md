# 01 — Broken Access Control (IDOR)

**OWASP A01:2021 — Broken Access Control.** The most common serious web flaw.

## Where

`GET /api/account/<id>` in `vulnerable_app/app.py`.

## Exploit

Log in as `alice`, then read `admin`'s account (id 3):

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/login \
  -d username=alice -d password=password123 | python3 -c "import sys,json;print(json.load(sys.stdin)['session'])")

curl -s http://127.0.0.1:5000/api/account/3 -H "X-Session: $TOKEN"
# returns admin's record including balance
```

## Source → Sink → Impact → Control

- **Source:** the `account_id` in the URL path.
- **Sink:** a database read keyed only by that id.
- **Impact:** any authenticated user reads (or, in richer apps, modifies) any
  other user's data. This is Insecure Direct Object Reference (IDOR), also called
  BOLA in API terms.
- **Control:** server-side authorization — the record's owner must match the
  caller (or the caller must be an admin).

## The fix (read it in the code)

```python
if row["username"] != user["username"] and user["role"] != "admin":
    return jsonify(error="forbidden"), 403
```

Authorization must be enforced on the server for every object access. Hiding the
id in the UI is not a control; the attacker controls the request.

## Verify

```bash
pytest tests/test_exploits.py::test_idor_reads_other_account -v   # attack works
pytest tests/test_fixes.py::test_idor_blocked -v                  # fix blocks it
```

## Connect to your background

This is the application-layer version of least privilege. You enforce it with
IAM in the cloud; here you enforce it per object in code.
