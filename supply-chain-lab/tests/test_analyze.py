import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sbom.analyze import analyze, summary  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SBOM = json.loads((ROOT / "data" / "sample_sbom.json").read_text(encoding="utf-8"))
ADVISORIES = json.loads((ROOT / "data" / "advisories.json").read_text(encoding="utf-8"))


class SbomAnalysisTests(unittest.TestCase):
    def test_flags_vulnerable_and_unpinned(self):
        findings = analyze(SBOM, ADVISORIES)
        kinds = summary(findings)
        self.assertEqual(kinds["vulnerable"], 3)
        self.assertEqual(kinds["unpinned"], 1)

    def test_sorted_critical_first(self):
        findings = analyze(SBOM, ADVISORIES)
        self.assertEqual(findings[0]["severity"], "CRITICAL")
        self.assertIn("pyyaml@5.3", findings[0]["component"])

    def test_clean_sbom(self):
        clean = {"components": [{"name": "flask", "version": "3.0.0"}]}
        self.assertEqual(analyze(clean, ADVISORIES), [])

    def test_unpinned_component(self):
        findings = analyze({"components": [{"name": "x"}]}, [])
        self.assertEqual(findings[0]["kind"], "unpinned")


if __name__ == "__main__":
    unittest.main()
