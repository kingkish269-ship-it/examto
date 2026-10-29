"""Reference solution for Drill 7."""

import argparse
import json
from pathlib import Path

SEVERITY_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select actionable security findings")
    parser.add_argument("input_file", type=Path)
    parser.add_argument(
        "--minimum-severity",
        choices=SEVERITY_RANK.keys(),
        default="HIGH",
    )
    return parser


def run(argv: list[str] | None = None) -> str:
    args = build_parser().parse_args(argv)

    with args.input_file.open(encoding="utf-8") as file:
        findings = json.load(file)

    minimum_rank = SEVERITY_RANK[args.minimum_severity]
    selected = [
        finding
        for finding in findings
        if finding.get("status") == "OPEN"
        and SEVERITY_RANK.get(finding.get("severity"), 0) >= minimum_rank
    ]
    selected.sort(
        key=lambda finding: SEVERITY_RANK.get(finding.get("severity"), 0),
        reverse=True,
    )
    return json.dumps(selected, indent=2)


if __name__ == "__main__":
    print(run())
