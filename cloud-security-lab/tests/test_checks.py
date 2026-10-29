import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from auditor import checks  # noqa: E402
from auditor.audit import run as run_cli  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = json.loads((ROOT / "data" / "sample_account.json").read_text(encoding="utf-8"))


class CloudCheckTests(unittest.TestCase):
    def test_public_bucket_is_critical(self):
        found = checks.public_s3_buckets(INVENTORY)
        ids = {(f["check"], f["resource"]) for f in found}
        self.assertIn(("s3-public-access", "s3://public-marketing-assets"), ids)
        self.assertIn(("s3-unencrypted", "s3://customer-exports"), ids)

    def test_open_security_groups(self):
        found = checks.open_security_groups(INVENTORY)
        checks_hit = {(f["check"], f["resource"]) for f in found}
        self.assertIn(("sg-sensitive-port", "sg-admin"), checks_hit)
        self.assertIn(("sg-all-open", "sg-legacy"), checks_hit)
        # Public HTTPS on sg-web must NOT be flagged.
        self.assertNotIn("sg-web", {f["resource"] for f in found})

    def test_wildcard_iam(self):
        found = checks.wildcard_iam(INVENTORY)
        by_resource = {f["resource"]: f["check"] for f in found}
        self.assertEqual(by_resource["break-glass-admin"], "iam-admin-wildcard")
        self.assertEqual(by_resource["ci-deployer"], "iam-action-wildcard")
        self.assertNotIn("read-only-metrics", by_resource)

    def test_storage_and_rds(self):
        self.assertTrue(checks.unencrypted_storage(INVENTORY))
        rds = {f["check"] for f in checks.public_and_unencrypted_rds(INVENTORY)}
        self.assertEqual(rds, {"rds-public", "rds-unencrypted"})

    def test_cloudtrail(self):
        self.assertTrue(checks.missing_cloudtrail(INVENTORY))

    def test_run_all_sorted_by_severity(self):
        findings = checks.run_all(INVENTORY)
        severities = [f["severity"] for f in findings]
        self.assertEqual(severities, sorted(severities, key={"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get))
        self.assertEqual(severities[0], "CRITICAL")

    def test_cli_fails_on_high(self):
        code = run_cli([str(ROOT / "data" / "sample_account.json"), "--fail-on", "HIGH", "--format", "json"])
        self.assertEqual(code, 1)  # findings exist -> non-zero gate

    def test_clean_inventory_passes(self):
        clean = {"s3_buckets": [], "security_groups": [], "iam_policies": [],
                 "ebs_volumes": [], "rds_instances": [], "cloudtrail": {"enabled": True}}
        self.assertEqual(checks.run_all(clean), [])


if __name__ == "__main__":
    unittest.main()
