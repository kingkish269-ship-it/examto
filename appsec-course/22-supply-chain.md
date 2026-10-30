# 22 — Software Supply Chain Security

## Theory

Attackers increasingly target what you build *with* — dependencies, build tools,
and artifacts — not just your own code (SolarWinds, dependency confusion). You
defend by **knowing and trusting your build**:

- **SBOM** (Software Bill of Materials) — a machine-readable inventory of every
  component in your software. Generate with **Syft**. SCA (module 16) scans it.
- **Signing** — sign artifacts with **Cosign** so consumers can verify they're
  genuinely yours and weren't swapped.
- **Provenance / SLSA** — signed metadata about *how* an artifact was built;
  verify it before deploy.
- Pin dependencies, restrict CI permissions, protect branches.

## Lab

```bash
cd /workspaces/examto/supply-chain-lab

# Analyse a CycloneDX SBOM for risky components:
python3 scan.py

# Read the real-tool exercises (Syft, Grype, Cosign, SLSA):
cat exercises/01_generate_sbom.md
cat exercises/02_scan_and_sign.md
cat exercises/03_provenance_slsa.md
```

Real tools (optional): `syft dir:. -o cyclonedx-json > sbom.json` generates an
SBOM; `cosign` signs and verifies artifacts.

## Verify

`scan.py` prints vulnerable + unpinned components from the SBOM, and you've read
how SBOM → scan → sign → provenance fit together.

## Key takeaways

- SBOM = inventory ("what's in it?"); SCA scans it for CVEs.
- Cosign signing + SLSA provenance = "is this really ours, built how we expect?"
- This is a high-demand, senior DevSecOps topic.

---

## You finished the course

You have now attacked and fixed every major web vulnerability, and worked through
the DevSecOps pipeline and cloud-native security around it. Next:
- Rebuild one exploit+fix from memory and explain it out loud.
- Do the guided web lab (`python3 webapp/app.py`) end to end.
- Follow `FINISH_ON_YOUR_OWN.md` and position yourself as **cloud + product
  security** for the senior roles.
