# 08 — Authentication and Session Flaws

**OWASP A07:2021 — Identification and Authentication Failures.**

## Where

`POST /login` issues a session token and (in secure mode) throttles attempts.

## Flaw 1: forgeable session token

The vulnerable token is just `base64("username:role")`, so anyone can mint an
admin token without logging in:

```bash
FORGED=$(python3 -c "import base64;print(base64.b64encode(b'admin:admin').decode())")
curl -s http://127.0.0.1:5000/api/account/1 -H "X-Session: $FORGED"
# accepted as admin
```

## Flaw 2: no brute-force protection

The vulnerable login accepts unlimited password guesses.

## Source → Sink → Impact → Control

- **Impact:** full account takeover by forging identity or guessing credentials.
- **Controls:**
  - Session tokens must be random and server-side, carrying no forgeable meaning.
  - Lock or throttle after repeated failures.
  - (Real systems add MFA, secure cookie flags, and session expiry.)

## The fixes

```python
# Unforgeable, random, server-side session id:
token = secrets.token_urlsafe(32)
sessions[token] = {"username": username, "role": role}

# Throttle brute force:
if attempts.get(username, 0) >= 5:
    return jsonify(error="account temporarily locked"), 429
```

A random token carries no attacker-controllable meaning, so it cannot be forged;
the server decides what it maps to.

## Verify

```bash
pytest tests/test_exploits.py::test_forgeable_session_token -v
pytest tests/test_fixes.py::test_rate_limited -v
```
