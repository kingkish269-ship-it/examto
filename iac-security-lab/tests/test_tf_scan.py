import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scanner.tf_scan import scan_plan  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    return json.loads((ROOT / "terraform" / name).read_text(encoding="utf-8"))


class TerraformScanTests(unittest.TestCase):
    def test_insecure_plan_flags_everything(self):
        findings = scan_plan(_load("sample_plan_insecure.json"))
        rules = {f["rule"] for f in findings}
        self.assertEqual(rules, {
            "s3-public-acl", "sg-sensitive-open", "rds-public",
            "rds-unencrypted", "ebs-unencrypted", "iam-admin-wildcard",
        })
        self.assertEqual(findings[0]["severity"], "CRITICAL")

    def test_secure_plan_is_clean(self):
        findings = scan_plan(_load("sample_plan_secure.json"))
        self.assertEqual(findings, [])

    def test_child_modules_are_scanned(self):
        plan = {"planned_values": {"root_module": {"child_modules": [
            {"resources": [{"address": "module.db.aws_db_instance.x", "type": "aws_db_instance",
                            "name": "x", "values": {"publicly_accessible": True}}]}
        ]}}}
        findings = scan_plan(plan)
        self.assertEqual(findings[0]["rule"], "rds-public")


if __name__ == "__main__":
    unittest.main()
