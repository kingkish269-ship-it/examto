import unittest

from tests._loader import load_drill

MODULE = load_drill("drill_02_nested_data")


class NestedDataTests(unittest.TestCase):
    def test_reads_nested_value(self):
        data = {"resource": {"details": {"region": "eu-west-1"}}}
        self.assertEqual(MODULE.get_nested(data, ["resource", "details", "region"]), "eu-west-1")

    def test_returns_default_for_missing_path(self):
        self.assertEqual(MODULE.get_nested({"resource": {}}, ["resource", "name"], "unknown"), "unknown")

    def test_returns_default_when_intermediate_value_is_not_dict(self):
        self.assertIsNone(MODULE.get_nested({"resource": None}, ["resource", "name"]))

    def test_builds_resource_label(self):
        self.assertEqual(MODULE.resource_label({"resource": {"type": "database", "name": "orders"}}), "database:orders")
        self.assertEqual(MODULE.resource_label({}), "unknown:unknown")


if __name__ == "__main__":
    unittest.main()
