import json
import tempfile
import unittest
from pathlib import Path

from tests._loader import load_drill

MODULE = load_drill("drill_07_cli")


class CliTests(unittest.TestCase):
    def test_parser_defaults_to_high(self):
        args = MODULE.build_parser().parse_args(["findings.json"])
        self.assertEqual(args.minimum_severity, "HIGH")

    def test_run_returns_selected_json(self):
        findings = [
            {"id": "1", "severity": "CRITICAL", "status": "OPEN"},
            {"id": "2", "severity": "MEDIUM", "status": "OPEN"},
            {"id": "3", "severity": "HIGH", "status": "RESOLVED"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "findings.json"
            path.write_text(json.dumps(findings), encoding="utf-8")
            output = MODULE.run([str(path), "--minimum-severity", "MEDIUM"])

        selected = json.loads(output)
        self.assertEqual([item["id"] for item in selected], ["1", "2"])

    def test_parser_rejects_unknown_severity(self):
        with self.assertRaises(SystemExit):
            MODULE.build_parser().parse_args(["findings.json", "--minimum-severity", "URGENT"])


if __name__ == "__main__":
    unittest.main()
