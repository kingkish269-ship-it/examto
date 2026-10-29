"""Policy gate for a DevSecOps pipeline.

Security tools (Semgrep, Trivy, Gitleaks, ...) each emit findings in their own
JSON shape. This module normalises them to a common finding, applies a policy,
and returns a pass/fail decision plus an exit code so a pipeline can block a
release. Pure standard library.

Normalised finding:
    {"tool": str, "id": str, "severity": "CRITICAL|HIGH|MEDIUM|LOW", "location": str}
"""

from __future__ import annotations

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def normalize_semgrep(report: dict) -> list[dict]:
    out = []
    for r in report.get("results", []):
        sev = r.get("extra", {}).get("severity", "WARNING").upper()
        mapped = {"ERROR": "HIGH", "WARNING": "MEDIUM", "INFO": "LOW"}.get(sev, "MEDIUM")
        out.append({
            "tool": "semgrep",
            "id": r.get("check_id", "semgrep-finding"),
            "severity": mapped,
            "location": f"{r.get('path', '?')}:{r.get('start', {}).get('line', '?')}",
        })
    return out


def normalize_trivy(report: dict) -> list[dict]:
    out = []
    for res in report.get("Results", []):
        target = res.get("Target", "?")
        for v in res.get("Vulnerabilities", []) or []:
            out.append({
                "tool": "trivy",
                "id": v.get("VulnerabilityID", "CVE-?"),
                "severity": v.get("Severity", "UNKNOWN").upper(),
                "location": f"{target}:{v.get('PkgName', '?')}",
            })
    return out


def normalize_gitleaks(report: list) -> list[dict]:
    # Gitleaks emits a JSON array of leaks. Any leaked secret is critical.
    out = []
    for leak in report or []:
        out.append({
            "tool": "gitleaks",
            "id": leak.get("RuleID", "secret"),
            "severity": "CRITICAL",
            "location": f"{leak.get('File', '?')}:{leak.get('StartLine', '?')}",
        })
    return out


def evaluate(findings: list[dict], fail_on: str = "HIGH",
             max_allowed: int = 0, allowlist: set[str] | None = None) -> dict:
    """Apply the gate policy.

    fail_on     : lowest severity that counts as blocking.
    max_allowed : number of blocking findings tolerated before failing.
    allowlist   : finding ids to ignore (accepted risk / false positives).
    """
    allowlist = allowlist or set()
    threshold = SEVERITY_ORDER[fail_on]

    considered = [f for f in findings if f["id"] not in allowlist]
    blocking = [f for f in considered if SEVERITY_ORDER.get(f["severity"], 9) <= threshold]

    counts: dict[str, int] = {}
    for f in considered:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1

    passed = len(blocking) <= max_allowed
    return {
        "passed": passed,
        "exit_code": 0 if passed else 1,
        "counts": counts,
        "blocking": blocking,
        "fail_on": fail_on,
        "max_allowed": max_allowed,
    }


def render(decision: dict) -> str:
    lines = ["DevSecOps gate: " + ("PASS" if decision["passed"] else "FAIL")]
    lines.append(f"  policy: fail_on={decision['fail_on']} max_allowed={decision['max_allowed']}")
    lines.append(f"  counts: {decision['counts'] or 'none'}")
    for f in decision["blocking"]:
        lines.append(f"  BLOCK [{f['severity']}] {f['tool']} {f['id']} @ {f['location']}")
    return "\n".join(lines)
