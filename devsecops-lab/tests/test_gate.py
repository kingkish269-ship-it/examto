import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gate.gate import (evaluate, normalize_gitleaks, normalize_semgrep,  # noqa: E402
                       normalize_trivy)
from gate.run_gate import run as run_gate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    return json.loads((ROOT / "samples" / name).read_text(encoding="utf-8"))


class NormalizeTests(unittest.TestCase):
    def test_semgrep_severity_mapping(self):
        f = normalize_semgrep(_load("semgrep_sample.json"))
        sev = {x["severity"] for x in f}
        self.assertEqual(sev, {"HIGH", "MEDIUM"})

    def test_trivy_and_gitleaks(self):
        self.assertEqual(len(normalize_trivy(_load("trivy_sample.json"))), 2)
        g = normalize_gitleaks(_load("gitleaks_sample.json"))
        self.assertEqual(g[0]["severity"], "CRITICAL")


class GateTests(unittest.TestCase):
    def _all(self):
        return (normalize_semgrep(_load("semgrep_sample.json"))
                + normalize_trivy(_load("trivy_sample.json"))
                + normalize_gitleaks(_load("gitleaks_sample.json")))

    def test_fails_on_high_by_default(self):
        decision = evaluate(self._all(), fail_on="HIGH")
        self.assertFalse(decision["passed"])
        self.assertEqual(decision["exit_code"], 1)

    def test_allowlist_removes_blocking_finding(self):
        findings = [{"tool": "trivy", "id": "CVE-2023-0001", "severity": "CRITICAL", "location": "x"}]
        blocked = evaluate(findings, fail_on="HIGH")
        allowed = evaluate(findings, fail_on="HIGH", allowlist={"CVE-2023-0001"})
        self.assertFalse(blocked["passed"])
        self.assertTrue(allowed["passed"])

    def test_medium_only_passes_when_fail_on_high(self):
        findings = [{"tool": "t", "id": "x", "severity": "MEDIUM", "location": "l"}]
        self.assertTrue(evaluate(findings, fail_on="HIGH")["passed"])

    def test_max_allowed_tolerance(self):
        findings = [{"tool": "t", "id": f"h{i}", "severity": "HIGH", "location": "l"} for i in range(2)]
        self.assertFalse(evaluate(findings, fail_on="HIGH", max_allowed=1)["passed"])
        self.assertTrue(evaluate(findings, fail_on="HIGH", max_allowed=2)["passed"])

    def test_cli_returns_nonzero(self):
        code = run_gate([
            "--semgrep", str(ROOT / "samples" / "semgrep_sample.json"),
            "--trivy", str(ROOT / "samples" / "trivy_sample.json"),
            "--gitleaks", str(ROOT / "samples" / "gitleaks_sample.json"),
            "--fail-on", "HIGH",
        ])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
