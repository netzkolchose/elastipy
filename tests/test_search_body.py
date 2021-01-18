import os
import json
import time
import unittest

from elastipy import Search, query


class TestSearchRequest(unittest.TestCase):

    def assertRequest(self, search: Search, expected_request: dict):
        for i in range(2):
            request = search.to_request()
            self._assert_obj_rec(search, expected_request, request)
            # test if copy works
            search = search.copy()
    
    def _assert_obj_rec(self, search: Search, expected_data: dict, real_data: dict):
        for key, value in expected_data.items():
            if key not in real_data:
                raise AssertionError(
                    f"missing field '{key}' in request of {search}"
                )
            if isinstance(value, dict):
                self._assert_obj_rec(search, value, real_data[key])
            else:
                if value != real_data[key]:
                    raise AssertionError(
                        f"expected value {repr(value)} in request of {search}, got {repr(real_data[key])}"
                    )

    def test_index(self):
        s = Search().index("Bob!")
        self.assertRequest(s, {
            "index": "Bob!"
        })

    def test_size(self):
        s = Search().size(23)
        self.assertRequest(s, {
            "body": {
                "size": 23,
            },
        })

    def test_sort(self):
        s = Search().sort("-field")
        self.assertRequest(s, {
            "body": {
                "sort": [
                    {"field": "desc"},
                ],
            }
        })


if __name__ == "__main__":
    unittest.main()
