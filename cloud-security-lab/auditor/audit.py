"""CLI for the cloud exposure auditor.

Usage:
    python -m auditor.audit data/sample_account.json
    python -m auditor.audit data/sample_account.json --format csv --out report.csv
    python -m auditor.audit data/sample_account.json --fail-on HIGH

Exit code is non-zero when findings at or above --fail-on exist, so this can
gate a CI/CD pipeline.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from .checks import run_all

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit a cloud inventory snapshot.")
    parser.add_argument("inventory", type=Path, help="path to inventory JSON")
    parser.add_argument("--format", choices=["table", "json", "csv"], default="table")
    parser.add_argument("--out", type=Path, help="write report to this file")
    parser.add_argument("--fail-on", choices=list(SEVERITY_ORDER), default="HIGH")
    return parser


def _render_table(findings: list[dict]) -> str:
    if not findings:
        return "No findings. Inventory passes all checks."
    lines = [f"{'SEVERITY':9} {'CHECK':22} {'RESOURCE':24} MESSAGE"]
    for f in findings:
        lines.append(f"{f['severity']:9} {f['check']:22} {f['resource']:24} {f['message']}")
    return "\n".join(lines)


def _render_csv(findings: list[dict], path: Path) -> None:
    cols = ["severity", "check", "resource", "message", "remediation"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols)
        writer.writeheader()
        writer.writerows(findings)


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    findings = run_all(inventory)

    if args.format == "json":
        output = json.dumps(findings, indent=2)
        (args.out.write_text(output, encoding="utf-8") if args.out else print(output))
    elif args.format == "csv":
        target = args.out or Path("report.csv")
        _render_csv(findings, target)
        print(f"Wrote {len(findings)} findings to {target}")
    else:
        print(_render_table(findings))

    threshold = SEVERITY_ORDER[args.fail_on]
    blocking = [f for f in findings if SEVERITY_ORDER.get(f["severity"], 9) <= threshold]
    if blocking:
        print(f"\n{len(blocking)} finding(s) at or above {args.fail_on}.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
