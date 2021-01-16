import os
import json
import time
import unittest

from elastipy import Search, query


class TestSearchBody(unittest.TestCase):

    def assertBody(self, search: Search, expected_body: dict):
        for i in range(2):
            body = search.to_body()
            for key, value in expected_body.items():
                if key not in body:
                    raise AssertionError(
                        f"missing field '{key}' in body of {search}"
                    )
                if value != body[key]:
                    raise AssertionError(
                        f"expected value {repr(value)} in body of {search}, got {repr(body[key])}"
                    )
            # test if copy works
            search = search.copy()

    def test_index(self):
        s = Search().index("Bob!")
        self.assertEqual(
            "Bob!",
            s.get_index(),
        )

    def test_size(self):
        s = Search().size(23)
        self.assertBody(s, {
            "size": 23,
        })

    def test_sort(self):
        s = Search().sort("_id")
        self.assertBody(s, {
            "sort": ["_id"],
        })


if __name__ == "__main__":
    unittest.main()
