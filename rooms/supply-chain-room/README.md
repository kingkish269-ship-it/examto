# Room: Software Supply Chain Security

**Topic:** DevSecOps · **Difficulty:** advanced · **high demand**

## Story
Attackers target what you build *with*, not just what you build.

## Theory (2 min)
Know and trust your build:
- **SBOM** (Software Bill of Materials) — a machine-readable inventory of every
  component; generate with Syft. SCA scans it.
- **Signing** — sign artifacts with Cosign so consumers verify they are yours.
- **Provenance / SLSA** — signed metadata about how an artifact was built;
  verify it before deploy.
Pin dependencies, restrict CI permissions, protect branches.

## What you'll do
Run `supply-chain-lab/scan.py` (analyses an SBOM); read the Syft/Cosign/SLSA
exercises in that lab.

## Going further
`supply-chain-lab/` and the `sca` room.
