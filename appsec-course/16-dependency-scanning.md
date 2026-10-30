# 16 — Dependency Scanning (SCA)

## Theory

Most of your app is code you didn't write — your **dependencies**. Vulnerable
ones are a leading breach cause (think Log4Shell). **Software Composition
Analysis (SCA)** inventories your dependencies and flags any with known **CVEs**,
plus **unpinned** versions you can't even assess. Free tools: **Trivy**,
**Grype**, OWASP Dependency-Check.

You triage findings by severity, whether it's actually reachable/exploitable,
and whether a fixed version exists. SCA reads from an **SBOM** (module 22).

## Lab

```bash
cd /workspaces/examto/supply-chain-lab
python3 scan.py
```

This analyses a sample SBOM and flags vulnerable components (e.g. an old
`requests`, `pyyaml`, `urllib3`) and an unpinned one. Read each finding: the
component, the CVE, and the fixed version.

Real tools (verified — install via `tools-lab/`):
```bash
# pip-audit on a deliberately old dependency:
printf 'requests==2.19.0\n' > /tmp/vreq.txt
pip-audit -r /tmp/vreq.txt          # reports known CVEs + fix versions
# Trivy on the whole repo's dependencies:
trivy fs /workspaces/examto
```

## Verify

`scan.py` prints a list of vulnerable + unpinned components and a summary count.

## Key takeaways

- SCA = find known-vulnerable and unpinned dependencies.
- Trivy / Grype / Dependency-Check; fail CI on high severity.
- Pin versions; keep an SBOM so you can answer "are we affected by CVE-X?".
