"""Drill 3: filter actionable security findings."""

SEVERITY_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


def filter_actionable(findings: list[dict], minimum_severity: str = "HIGH") -> list[dict]:
    """Return open findings at or above *minimum_severity*."""
    if minimum_severity not in SEVERITY_RANK:
        raise ValueError(f"Invalid severity: {minimum_severity}")

    minimum_rank = SEVERITY_RANK[minimum_severity]
    selected = []
    for finding in findings:
        severity_rank = SEVERITY_RANK.get(finding.get("severity"), 0)
        if finding.get("status") == "OPEN" and severity_rank >= minimum_rank:
            selected.append(finding)

    return sorted(
        selected,
        key=lambda finding: SEVERITY_RANK.get(finding.get("severity"), 0),
        reverse=True,
    )
