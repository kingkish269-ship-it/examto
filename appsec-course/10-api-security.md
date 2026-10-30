# 10 — API Security (OWASP API Top 10)

## Theory

Modern apps are mostly **APIs** returning JSON. They have their own Top 10, and
the headline is **BOLA** (Broken Object Level Authorization) — the API version
of IDOR, and API risk #1. Others you'll meet constantly:

- **Broken authentication** — weak tokens (module 06).
- **Broken function-level authorization** — a normal user calling an admin-only
  endpoint.
- **Excessive data exposure** — the API returns more fields than the client
  needs (e.g. password hashes, internal flags), trusting the UI to hide them.
- **Mass assignment** — the API blindly binds JSON fields to objects, letting a
  user set `"role":"admin"`.
- **No rate limiting** — enabling brute force and scraping.

Fixes: authorize **every object and function** server-side; return only the
fields needed; rate-limit.

## Lab

App running (appsec-lab). Second terminal:

```bash
# BOLA: read another user's object by id (as in module 01):
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/login -d username=alice -d password=password123 \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['session'])")
curl -s http://127.0.0.1:5000/api/account/3 -H "X-Session: $TOKEN"
```

Look at the JSON returned — note it exposes fields a normal client shouldn't get
(that's **excessive data exposure**), and you reached another user's object
(that's **BOLA**).

Go deeper (optional, free): run **OWASP crAPI** (a deliberately vulnerable API)
with Docker for a richer target.

## Verify

You retrieved another user's API object and saw it return more than the client
needs — BOLA + excessive data exposure in one call.

## Key takeaways

- API #1 is BOLA — authorize every object access on the server.
- Return only needed fields; beware mass assignment; rate-limit.
- The OWASP API Top 10 is a must-know for product-security interviews.
