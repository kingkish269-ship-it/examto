"""Run every security Python pattern without external services."""

import json
from pathlib import Path

from drills.drill_01_parse_findings import load_findings, summarize_findings
from drills.drill_02_nested_data import resource_label
from drills.drill_03_filter_findings import filter_actionable
from drills.drill_04_api_pagination import collect_all_items
from drills.drill_05_csv_report import write_csv_report
from drills.drill_06_retry import call_with_retry
from drills.drill_07_cli import run as run_cli
from drills.drill_08_security_group_audit import audit_security_groups

ROOT = Path(__file__).resolve().parent


def heading(number: int, title: str) -> None:
    print(f"\n[{number}] {title}")
    print("-" * (len(title) + 4))


def main() -> None:
    findings_path = ROOT / "data" / "findings.json"
    findings = load_findings(findings_path)

    heading(1, "Parse and summarize JSON findings")
    print(json.dumps(summarize_findings(findings), indent=2))

    heading(2, "Read nested resource data safely")
    print(resource_label(findings[0]))
    print(resource_label({}))

    heading(3, "Filter actionable findings")
    actionable = filter_actionable(findings, "HIGH")
    print([finding["id"] for finding in actionable])

    heading(4, "Collect paginated API results")
    pages = json.loads((ROOT / "data" / "api_pages.json").read_text(encoding="utf-8"))

    def fetch_page(token):
        return pages["first" if token is None else token]

    print(collect_all_items(fetch_page))

    heading(5, "Write a CSV security report")
    report_path = ROOT / "reports" / "actionable_findings.csv"
    rows = write_csv_report(actionable, report_path)
    print(f"Wrote {rows} rows to {report_path.relative_to(ROOT)}")

    heading(6, "Retry a temporary API failure")
    attempt_count = 0

    def temporary_operation():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise TimeoutError("simulated timeout")
        return "API recovered"

    result = call_with_retry(temporary_operation, sleep_fn=lambda seconds: None)
    print(f"{result} after {attempt_count} attempts")

    heading(7, "Run filtering as a command-line tool")
    cli_output = json.loads(run_cli([str(findings_path), "--minimum-severity", "CRITICAL"]))
    print([finding["id"] for finding in cli_output])

    heading(8, "Audit cloud security groups")
    groups = json.loads((ROOT / "data" / "security_groups.json").read_text(encoding="utf-8"))
    group_findings = audit_security_groups(groups)
    for finding in group_findings:
        print(
            f"{finding['severity']:8} {finding['group_id']:12} "
            f"port={finding['port']!s:4} {finding['reason']}"
        )

    print("\nAll eight patterns ran successfully.")


if __name__ == "__main__":
    main()
