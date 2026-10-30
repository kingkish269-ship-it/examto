# 19 — Container Security

## Theory

Containers package your app for deployment — and package its weaknesses too.
Harden the image:
- **Pin the base image** by digest, not `latest` (reproducible, no surprise
  updates).
- Run as a **non-root** user (limits damage if compromised).
- Use a **minimal / distroless** base (smaller attack surface).
- **Read-only root filesystem**, **drop Linux capabilities**.
- Don't pipe downloads into a shell at build time.
- **Scan the image** for CVEs (Trivy/Grype).

A container running as **root** is a classic finding.

## Lab

```bash
cd /workspaces/examto/container-k8s-lab

# Compare the insecure vs hardened Dockerfile:
cat manifests/insecure/Dockerfile
cat manifests/secure/Dockerfile

# Run the Dockerfile linter on the insecure one:
python3 - <<'PY'
from validator.dockerfile_lint import lint
for f in lint(open("manifests/insecure/Dockerfile").read()):
    print(f["severity"], f["rule"], "- line", f["line"])
PY
```

The linter flags the `latest` base image, pipe-to-shell, and running as root.
Real tool: `trivy image python:3.11-slim` scans an image for CVEs.

## Verify

The linter reports `base-image-untagged`, `pipe-to-shell`, and `runs-as-root`
on the insecure Dockerfile; the secure one is clean.

## Key takeaways

- Pin by digest, run non-root, minimal base, read-only fs, drop capabilities.
- Scan images with Trivy/Grype.
- "Runs as root" and "image: latest" are instant findings.
