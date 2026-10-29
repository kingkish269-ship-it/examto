"""Reference solution for Drill 1."""

import json
from pathlib import Path


def load_findings(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as file:
        findings = json.load(file)

    if not isinstance(findings, list):
        raise ValueError("Expected the JSON document to contain a list")
    return findings


def summarize_findings(findings: list[dict]) -> dict:
    by_severity: dict[str, int] = {}
    open_high_or_critical = 0

    for finding in findings:
        severity = finding.get("severity", "UNKNOWN")
        by_severity[severity] = by_severity.get(severity, 0) + 1

        if finding.get("status") == "OPEN" and severity in {"HIGH", "CRITICAL"}:
            open_high_or_critical += 1

    return {
        "total": len(findings),
        "by_severity": by_severity,
        "open_high_or_critical": open_high_or_critical,
    }
