import unittest

from tests._loader import load_drill

MODULE = load_drill("drill_04_api_pagination")


class PaginationTests(unittest.TestCase):
    def test_collects_every_page(self):
        pages = {
            None: {"items": [{"id": "A-1"}], "next_token": "page-2"},
            "page-2": {"items": [{"id": "A-2"}, {"id": "A-3"}], "next_token": None},
        }
        calls = []

        def fetch_page(token):
            calls.append(token)
            return pages[token]

        result = MODULE.collect_all_items(fetch_page)
        self.assertEqual([item["id"] for item in result], ["A-1", "A-2", "A-3"])
        self.assertEqual(calls, [None, "page-2"])

    def test_handles_empty_result(self):
        self.assertEqual(MODULE.collect_all_items(lambda token: {"items": [], "next_token": None}), [])

    def test_stops_repeated_token(self):
        def broken_api(token):
            return {"items": [], "next_token": "same-token"}

        with self.assertRaises(ValueError):
            MODULE.collect_all_items(broken_api)


if __name__ == "__main__":
    unittest.main()
