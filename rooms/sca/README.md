# Room: Dependency Scanning (SCA)

**Topic:** DevSecOps · **Difficulty:** core

## Story
Most of your app is code you didn't write — your dependencies. Vulnerable ones
are a top breach cause.

## Theory (2 min)
**Software Composition Analysis (SCA)** inventories your dependencies and flags
ones with known **CVEs**, plus **unpinned** versions you can't assess. Tools:
Trivy, Grype, OWASP Dependency-Check. You triage by severity, exploitability,
and whether a fixed version exists. An **SBOM** (see the supply-chain room) is
the inventory SCA works from.

## What you'll do
Run `supply-chain-lab/scan.py` — it analyses a sample SBOM and flags vulnerable
and unpinned components.

## Going further
`supply-chain-lab/` (the analyzer) and the `supply-chain` room.
