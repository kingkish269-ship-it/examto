# 03 — Provenance and SLSA

## What provenance is

Provenance is signed metadata describing how an artifact was built: the source
commit, the builder, and the build parameters. With it, a consumer can verify
an artifact came from the expected pipeline and was not tampered with.

## SLSA levels (summary)

SLSA is a framework for supply-chain integrity. Rising levels add stronger
guarantees:

- **Build L1** — provenance exists and describes the build.
- **Build L2** — provenance is signed by a hosted build service.
- **Build L3** — the build runs in a hardened, isolated service that prevents
  tampering with the provenance.

Content was rephrased for licensing compliance; see https://slsa.dev/ for the
authoritative definitions.

## Practise

- Generate provenance in GitHub Actions with the free SLSA generator workflow.
- Sign it with Cosign (exercise 02).
- Verify provenance before deploy, and reject artifacts whose provenance does
  not match the expected source repository and builder.

## Tie it together

Your release pipeline (see `devsecops-lab/`) should: build, generate an SBOM
(Syft), scan it (Grype), sign the artifact and SBOM (Cosign), produce provenance
(SLSA), and verify signature + provenance at deploy. Each step answers a
different supply-chain question: what is in it, is it vulnerable, is it ours, and
how was it built.
