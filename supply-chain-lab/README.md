# Software Supply Chain Security Lab

Generate a software bill of materials (SBOM), find vulnerable and unpinned
dependencies, and understand signing and provenance. You get a working Python
SBOM analyzer plus guides for the real free tools (Syft, Grype, Cosign).

Analyzer is pure standard library.

## Run it

```bash
cd supply-chain-lab
python3 -c "import json; from sbom.analyze import analyze, summary; \
f=analyze(json.load(open('data/sample_sbom.json')), json.load(open('data/advisories.json'))); \
print(json.dumps(f, indent=2)); print(summary(f))"
python3 -m unittest discover -v    # 4 tests
```

## What it flags

- **Vulnerable components** — a component version listed in `advisories.json`
  (the sample flags vulnerable `requests`, `pyyaml`, and `urllib3`).
- **Unpinned components** — a component with no version, which cannot be assessed.

The SBOM is CycloneDX JSON, the format Syft produces, so the analyzer works on
real SBOMs too.

## The real toolchain

- `exercises/01_generate_sbom.md` — produce an SBOM with **Syft**.
- `exercises/02_scan_and_sign.md` — scan with **Grype**, sign with **Cosign**.
- `exercises/03_provenance_slsa.md` — build provenance and the SLSA levels.

## Why this matters

Supply-chain attacks (malicious or vulnerable dependencies, tampered build
artifacts) are a top risk. SBOMs give you an inventory to answer "are we
affected by CVE-X?" in minutes. Signing and provenance let you verify an
artifact is the one you built and nothing swapped it.

## Extend it

Add version-range matching (for example "affected below 2.20.0") instead of an
exact list, with tests.
