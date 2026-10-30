import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import detections as d  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EVENTS = json.loads((ROOT / "data" / "events.json").read_text(encoding="utf-8"))


class DetectionTests(unittest.TestCase):
    def test_brute_force_fires_on_attacker_ip(self):
        alerts = d.detect_brute_force(EVENTS)
        entities = {a["entity"] for a in alerts}
        self.assertIn("203.0.113.9", entities)

    def test_brute_force_quiet_on_benign(self):
        benign = [e for e in EVENTS if e.get("src_ip") == "10.0.0.5"]
        self.assertEqual(d.detect_brute_force(benign), [])

    def test_sqli_detected(self):
        alerts = d.detect_sqli(EVENTS)
        self.assertTrue(any(a["rule"] == "web-sqli-attempt" for a in alerts))

    def test_path_traversal_detected(self):
        alerts = d.detect_path_traversal(EVENTS)
        self.assertTrue(any("passwd" in a["evidence"] for a in alerts))

    def test_unauthorized_admin_grant_is_critical(self):
        alerts = d.detect_unauthorized_admin_grant(EVENTS)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["entity"], "mallory")
        self.assertEqual(alerts[0]["severity"], "CRITICAL")

    def test_authorized_admin_grant_not_flagged(self):
        # secops is a known admin; granting to newhire must not alert.
        self.assertNotIn("secops", {a["entity"] for a in d.detect_unauthorized_admin_grant(EVENTS)})

    def test_impossible_travel(self):
        alerts = d.detect_impossible_travel(EVENTS)
        self.assertEqual(alerts[0]["entity"], "bob")

    def test_run_all_sorted_critical_first(self):
        alerts = d.run_all(EVENTS)
        self.assertEqual(alerts[0]["severity"], "CRITICAL")
        self.assertGreaterEqual(len(alerts), 5)


if __name__ == "__main__":
    unittest.main()
