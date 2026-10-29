import json
import tempfile
import unittest
from pathlib import Path

from tests._loader import load_drill

MODULE = load_drill("drill_01_parse_findings")
ROOT = Path(__file__).resolve().parents[1]


class ParseFindingsTests(unittest.TestCase):
    def test_loads_json_list(self):
        findings = MODULE.load_findings(ROOT / "data" / "findings.json")
        self.assertEqual(len(findings), 5)
        self.assertEqual(findings[0]["id"], "F-001")

    def test_rejects_non_list_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps({"findings": []}), encoding="utf-8")
            with self.assertRaises(ValueError):
                MODULE.load_findings(path)

    def test_summarizes_findings(self):
        findings = MODULE.load_findings(ROOT / "data" / "findings.json")
        summary = MODULE.summarize_findings(findings)
        self.assertEqual(summary["total"], 5)
        self.assertEqual(summary["by_severity"], {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 1, "LOW": 1})
        self.assertEqual(summary["open_high_or_critical"], 3)

    def test_counts_missing_severity_as_unknown(self):
        summary = MODULE.summarize_findings([{"status": "OPEN"}])
        self.assertEqual(summary["by_severity"], {"UNKNOWN": 1})


if __name__ == "__main__":
    unittest.main()
