"""Drill 5: write security findings to a CSV report."""

import csv
from pathlib import Path

REPORT_COLUMNS = ["id", "title", "severity", "resource_name"]


def write_csv_report(findings: list[dict], output_path: str | Path) -> int:
    """Write selected finding fields to CSV and return rows written."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=REPORT_COLUMNS)
        writer.writeheader()
        for finding in findings:
            writer.writerow(
                {
                    "id": finding.get("id", ""),
                    "title": finding.get("title", ""),
                    "severity": finding.get("severity", ""),
                    "resource_name": finding.get("resource", {}).get("name", ""),
                }
            )
    return len(findings)
