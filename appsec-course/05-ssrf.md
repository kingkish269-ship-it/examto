# 05 — Server-Side Request Forgery (SSRF) — OWASP A10

## Theory

A feature lets the app fetch a URL you supply ("import from URL", "webhook",
"preview link"). If it doesn't validate the URL, you can make the **server**
request things you can't reach yourself — internal services, or the cloud
**metadata endpoint** `http://169.254.169.254/...` which can hand out the
instance's credentials.

This is where your network background pays off: `169.254.169.254` is a
**link-local** address. SSRF is a network-segmentation problem expressed in app
code.

**The fix:** allowlist the scheme (http/https only), resolve the hostname, and
**reject private, loopback, and link-local IP ranges**. Prefer an allowlist of
exact destinations when possible.

## Lab

App running. Second terminal:

```bash
# Put a secret file on the box, then make the server read it via file:// (SSRF):
echo "INTERNAL-ONLY-SECRET" > /tmp/lab_secret.txt
curl -s "http://127.0.0.1:5000/fetch?url=file:///tmp/lab_secret.txt"
```

The server fetched a local file for you — proof it will reach things it
shouldn't.

Fix — restart secure:
```bash
# Ctrl+C, then:
LAB_SECURE=1 python3 run_server.py
```
Re-run it: rejected (`only http/https allowed`). Also try an internal address:
```bash
curl -s "http://127.0.0.1:5000/fetch?url=http://127.0.0.1:80/"
```
Secure mode rejects it (`target resolves to an internal address`).

## Verify

- Insecure: `file://` read works; internal fetch allowed.
- Secure: non-http schemes and internal/link-local addresses are blocked.

## Key takeaways

- SSRF = the server fetching attacker-chosen URLs; cloud metadata is the prize.
- Fix = scheme allowlist + resolve + block private/loopback/link-local ranges.
- Watch for DNS rebinding: resolve, then validate the actual IP.
