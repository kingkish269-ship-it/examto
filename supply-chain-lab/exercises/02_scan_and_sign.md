# 02 — Scan with Grype and sign with Cosign

## Grype — vulnerability scanning (free)

```bash
grype sbom:sbom.json          # scan an SBOM you generated
grype python:3.11-slim        # or scan an image directly
```

Grype maps components to known CVEs. The lab analyzer does the same against a
small sample list so you understand the mechanism.

## Cosign — sign and verify artifacts (free)

Signing proves an artifact is the one you built and was not swapped.

```bash
# Keyless signing (uses an OIDC identity, no long-lived key):
cosign sign <registry>/<image>@sha256:<digest>

# Verify before deploy:
cosign verify <registry>/<image>@sha256:<digest> \
  --certificate-identity <ci-identity> \
  --certificate-oidc-issuer <issuer>
```

Enforce verification at admission with the Kyverno `verifyImages` rule or a
Cosign policy controller, so unsigned images are rejected — the supply-chain
equivalent of the container lab's admission policies.

Docs: Grype https://github.com/anchore/grype · Cosign https://docs.sigstore.dev/
