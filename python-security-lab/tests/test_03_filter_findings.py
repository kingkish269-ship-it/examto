import unittest

from tests._loader import load_drill

MODULE = load_drill("drill_03_filter_findings")


class FilterFindingsTests(unittest.TestCase):
    def setUp(self):
        self.findings = [
            {"id": "1", "severity": "HIGH", "status": "OPEN"},
            {"id": "2", "severity": "CRITICAL", "status": "OPEN"},
            {"id": "3", "severity": "HIGH", "status": "ACCEPTED"},
            {"id": "4", "severity": "MEDIUM", "status": "OPEN"},
            {"id": "5", "severity": "UNKNOWN", "status": "OPEN"},
            {"id": "6", "severity": "HIGH", "status": "OPEN"},
        ]

    def test_selects_open_findings_at_threshold(self):
        selected = MODULE.filter_actionable(self.findings, "HIGH")
        self.assertEqual([item["id"] for item in selected], ["2", "1", "6"])

    def test_supports_lower_threshold(self):
        selected = MODULE.filter_actionable(self.findings, "MEDIUM")
        self.assertEqual([item["id"] for item in selected], ["2", "1", "6", "4"])

    def test_rejects_invalid_threshold(self):
        with self.assertRaises(ValueError):
            MODULE.filter_actionable(self.findings, "URGENT")


if __name__ == "__main__":
    unittest.main()
