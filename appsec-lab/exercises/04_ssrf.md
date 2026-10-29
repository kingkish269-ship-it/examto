# 04 — Server-Side Request Forgery (SSRF)

**OWASP A10:2021 — SSRF.** Especially dangerous in cloud environments.

## Where

`GET /fetch?url=...` fetches any URL the client supplies.

## Exploit

The vulnerable handler accepts any scheme, including `file://`, so it reads
local files:

```bash
echo "INTERNAL-ONLY" > /tmp/lab_secret.txt
curl -s "http://127.0.0.1:5000/fetch?url=file:///tmp/lab_secret.txt"
# returns INTERNAL-ONLY
```

## Why this matters to you specifically

In the cloud, the highest-value SSRF target is the instance metadata endpoint
`http://169.254.169.254/...`, which can expose temporary credentials. You know
that link-local range from networking. SSRF turns a naive "fetch this URL"
feature into a path to those internal endpoints.

## Source → Sink → Impact → Control

- **Source:** the `url` parameter.
- **Sink:** the server's outbound HTTP/URL client.
- **Impact:** read internal services, cloud metadata, and local files; pivot
  inside the network.
- **Control:** allowlist schemes (`http`/`https` only), resolve the hostname,
  and reject private, loopback, link-local, and reserved IP ranges.

## The fix

```python
def _ssrf_reason(url):
    parts = urllib.parse.urlparse(url)
    if parts.scheme not in {"http", "https"}:
        return "only http/https allowed"
    for info in socket.getaddrinfo(parts.hostname, None):
        addr = ipaddress.ip_address(info[4][0])
        if addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved:
            return "target resolves to an internal address"
    return None
```

Resolve then validate the actual IP, because a public hostname can resolve to an
internal address (DNS rebinding). Prefer an allowlist of destinations when the
feature permits it.

## Verify

```bash
pytest tests/test_exploits.py::test_ssrf_file_scheme -v
pytest tests/test_fixes.py::test_ssrf_file_scheme_blocked -v
pytest tests/test_fixes.py::test_ssrf_internal_ip_blocked -v
```
