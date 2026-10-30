# 01 — Dockerfile hardening

## See it

```bash
cd container-k8s-lab
python3 -c "from validator.dockerfile_lint import lint; \
[print(f['severity'], f['rule'], 'line', f['line']) for f in \
lint(open('manifests/insecure/Dockerfile').read())]"
```

The insecure Dockerfile is flagged for an untagged `latest` base image, a
pipe-to-shell install, and running as root.

## Read the pair

Compare `manifests/insecure/Dockerfile` and `manifests/secure/Dockerfile`. The
secure one pins the base image by digest, avoids piping downloads into a shell,
adds `--no-install-recommends`, sets a non-root `USER`, and adds a healthcheck.

## Why each matters

- **Pinned base image** — reproducible builds; a moving `latest` can change
  under you and pull in new vulnerabilities.
- **No pipe-to-shell** — a compromised or MITM'd script would run arbitrary
  code at build time (a supply-chain risk).
- **Non-root USER** — limits blast radius if the app is compromised.

## In the real toolchain

Scan the built image with Trivy or Grype (see `tools/README.md`). Combine with
the Kubernetes controls in exercise 02 — a non-root image plus a non-root pod
security context is defence in depth.

## Extend it

Add a rule to `dockerfile_lint.py` that flags `COPY . .` before dependency
installation (which breaks layer caching and can leak secrets), and add a test.
