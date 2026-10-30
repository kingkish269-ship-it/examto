# 01 — Broken Access Control (IDOR) — OWASP A01

## Theory

The #1 web risk. The app lets you reach data or actions that should not be
yours.

The classic form is **IDOR** (Insecure Direct Object Reference): the app returns
an object by its id without checking you're allowed to see it. You're user 1,
you request `/account/2`, and you get user 2's data. In APIs this is called
**BOLA** (Broken Object Level Authorization) and it's API risk #1.

Analogy: a cloakroom that hands over any coat if you just say a ticket number,
without checking the ticket is yours.

The fix is a **server-side ownership check**: the logged-in user must own the
object (or be an admin). Hiding the id in the webpage is *not* a fix — the
attacker types the request by hand.

## Lab

Make sure the app is running (module 00). In a second terminal:

```bash
cd /workspaces/examto/appsec-lab
# Log in as a normal user "alice" and grab her session token:
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/login -d username=alice -d password=password123 \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['session'])")

# Now read the ADMIN's account (id 3) even though you are alice:
curl -s http://127.0.0.1:5000/api/account/3 -H "X-Session: $TOKEN"
```

You get the admin's record back — access control is broken.

Now see the fix. Restart the app in **secure mode** (Ctrl+C the server, then):

```bash
LAB_SECURE=1 python3 run_server.py
```

Repeat the two commands above. The second one now returns `403 forbidden` —
the server checks ownership.

## Verify

- Insecure mode: you read account 3 as alice (should not be allowed).
- Secure mode: the same request is blocked with 403.

Read the fix in `appsec-lab/vulnerable_app/app.py` (search for `A01`).

## Key takeaways

- IDOR/BOLA = returning an object by id with no ownership check.
- Fix = authorize **every object access** on the server.
- Interview line: "I enforce object-level authorization server-side; the id in
  the request is attacker-controlled, so UI hiding is not a control."
