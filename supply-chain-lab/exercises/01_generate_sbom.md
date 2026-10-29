# 01 — Generate an SBOM with Syft

An SBOM lists every component in your software so you can answer "what are we
running?" and "are we affected by this CVE?".

## Install Syft (free)

See the Syft releases page, or:

```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
```

(Downloading a script and piping to a shell is itself a supply-chain risk —
inspect it first, or install from your package manager.)

## Generate an SBOM

```bash
# For a directory of source:
syft dir:. -o cyclonedx-json > sbom.json
# For a container image:
syft python:3.11-slim -o cyclonedx-json > image-sbom.json
```

## Analyze it with the lab

```bash
python3 -c "import json; from sbom.analyze import analyze, summary; \
print(summary(analyze(json.load(open('sbom.json')), json.load(open('data/advisories.json')))))"
```

In practice you would feed the SBOM to a scanner (Grype) that carries a full
vulnerability database instead of the small sample advisory list.
