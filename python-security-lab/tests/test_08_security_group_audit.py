import json
import unittest
from pathlib import Path

from tests._loader import load_drill

MODULE = load_drill("drill_08_security_group_audit")
ROOT = Path(__file__).resolve().parents[1]


class SecurityGroupAuditTests(unittest.TestCase):
    def test_flags_dangerous_public_rules(self):
        groups = json.loads((ROOT / "data" / "security_groups.json").read_text(encoding="utf-8"))
        findings = MODULE.audit_security_groups(groups)

        actual = {(item["group_id"], item["port"], item["severity"]) for item in findings}
        self.assertEqual(
            actual,
            {
                ("sg-admin", 22, "HIGH"),
                ("sg-admin", 3389, "HIGH"),
                ("sg-all", "ALL", "CRITICAL"),
            },
        )

    def test_flags_public_database_port_inside_range(self):
        groups = [{
            "group_id": "sg-db",
            "name": "database",
            "rules": [{"protocol": "tcp", "from_port": 5000, "to_port": 6000, "cidr": "::/0"}],
        }]
        findings = MODULE.audit_security_groups(groups)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["port"], 5432)
        self.assertEqual(findings[0]["severity"], "CRITICAL")

    def test_ignores_private_and_https_rules(self):
        groups = [{
            "group_id": "sg-safe",
            "name": "safe",
            "rules": [
                {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr": "10.0.0.0/8"},
                {"protocol": "tcp", "from_port": 443, "to_port": 443, "cidr": "0.0.0.0/0"},
            ],
        }]
        self.assertEqual(MODULE.audit_security_groups(groups), [])


if __name__ == "__main__":
    unittest.main()
