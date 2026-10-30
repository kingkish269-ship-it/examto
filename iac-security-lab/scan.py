"""CLI for the Terraform plan scanner.

    python3 scan.py terraform/sample_plan_insecure.json
    python3 scan.py terraform/sample_plan_insecure.json --fail-on HIGH

Exits non-zero when findings at or above --fail-on exist, so it can gate a
pipeline.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scanner.tf_scan import scan_plan

SEV = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Scan a Terraform plan for insecure resources.")
    p.add_argument("plan", type=Path, help="terraform show -json output")
    p.add_argument("--fail-on", choices=list(SEV), default="HIGH")
    args = p.parse_args(argv)

    findings = scan_plan(json.loads(args.plan.read_text(encoding="utf-8")))
    if not findings:
        print("No findings. Plan passes all checks.")
        return 0

    for f in findings:
        print(f"{f['severity']:9}{f['rule']:22}{f['resource']:30}{f['message']}")

    threshold = SEV[args.fail_on]
    blocking = [f for f in findings if SEV.get(f["severity"], 9) <= threshold]
    if blocking:
        print(f"\n{len(blocking)} finding(s) at or above {args.fail_on}.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
