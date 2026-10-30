"""CLI for the SBOM analyzer.

    python3 scan.py
    python3 scan.py --sbom data/sample_sbom.json --advisories data/advisories.json

Exits non-zero when vulnerable components are found.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sbom.analyze import analyze, summary

ROOT = Path(__file__).resolve().parent


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Analyze a CycloneDX SBOM for risky components.")
    p.add_argument("--sbom", type=Path, default=ROOT / "data" / "sample_sbom.json")
    p.add_argument("--advisories", type=Path, default=ROOT / "data" / "advisories.json")
    args = p.parse_args(argv)

    sbom = json.loads(args.sbom.read_text(encoding="utf-8"))
    advisories = json.loads(args.advisories.read_text(encoding="utf-8"))
    findings = analyze(sbom, advisories)

    for f in findings:
        print(f"{f['severity']:9}{f['kind']:12}{f['component']:28}{f['message']}")
    s = summary(findings)
    print(f"\nTotal: {s['total']}  vulnerable: {s['vulnerable']}  unpinned: {s['unpinned']}")
    return 1 if s["vulnerable"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
