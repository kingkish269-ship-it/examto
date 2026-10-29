import csv
import tempfile
import unittest
from pathlib import Path

from tests._loader import load_drill

MODULE = load_drill("drill_05_csv_report")


class CsvReportTests(unittest.TestCase):
    def test_writes_expected_columns_and_rows(self):
        findings = [
            {"id": "F-1", "title": "Public database", "severity": "CRITICAL", "resource": {"name": "orders-db"}},
            {"id": "F-2", "title": "Missing tag", "severity": "LOW"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "report.csv"
            count = MODULE.write_csv_report(findings, output)
            self.assertEqual(count, 2)
            self.assertTrue(output.exists())
            with output.open(newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))

        self.assertEqual(rows[0], {"id": "F-1", "title": "Public database", "severity": "CRITICAL", "resource_name": "orders-db"})
        self.assertEqual(rows[1]["resource_name"], "")

    def test_writes_header_for_empty_report(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.csv"
            self.assertEqual(MODULE.write_csv_report([], output), 0)
            self.assertEqual(output.read_text(encoding="utf-8").strip(), "id,title,severity,resource_name")


if __name__ == "__main__":
    unittest.main()
