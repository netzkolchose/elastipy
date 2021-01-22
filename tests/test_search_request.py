import os
import json
import time
import unittest
from io import StringIO

from elastipy import Search, query


class TestSearchRequest(unittest.TestCase):

    def assertRequest(self, search: Search, expected_request: dict, and_not_more: bool = False):
        for i in range(2):
            request = search.to_request()
            self._assert_obj_rec(search, expected_request, request, and_not_more=and_not_more)

            # test if copy works
            if search._aggregations:
                break
            search = search.copy()

        # also check the dump interface

        file = StringIO()
        search.dump.request(file=file)
        file.seek(0)
        request = json.loads(file.read())
        self._assert_obj_rec(search, expected_request, request, and_not_more=and_not_more)

    def _assert_obj_rec(
            self, search: Search,
            expected_data: dict, real_data: dict, and_not_more: bool = False, path=()
    ):
        for key, expected_value in expected_data.items():
            long_key = ".".join(path + (key, ))

            if key not in real_data:
                raise AssertionError(
                    f"missing field '{long_key}' in request of {search}"
                )
            if isinstance(expected_value, dict):
                self._assert_obj_rec(
                    search, expected_value, real_data[key],
                    path=path + (key, ), and_not_more=and_not_more,
                )
            else:
                if expected_value != real_data[key]:
                    raise AssertionError(
                        f"expected {long_key} == {repr(expected_value)} in "
                        f"request of {search}, got {repr(real_data[key])}"
                    )

        if and_not_more:
            for key, real_value in real_data.items():
                long_key = ".".join(path + (key, ))

                if key not in expected_data:
                    raise AssertionError(
                        f"Unexpected {long_key} == {repr(real_value)} in request of {search}"
                    )

    def test_default_request(self):
        s = Search()
        self.assertRequest(
            s,
            {
                "index": None,
                "params": {
                    #"rest_total_hits_as_int": "true",
                },
                "body": {
                    "query": {
                        "match_all": {}
                    },
                },
            },
            and_not_more=True
        )

    def test_query(self):
        s = Search()
        self.assertRequest(s, {
            "body": {
                "query": {
                    "match_all": {}
                },
            }
        })

        s = Search().bool(must=[query.MatchAll()])
        self.assertRequest(s, {
            "body": {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_all": {}
                            }
                        ]
                    }
                },
            }
        })

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

        s = Search().sort(("field", "-another"))
        self.assertRequest(s, {
            "body": {
                "sort": [
                    "field",
                    {"another": "desc"},
                ],
            }
        })

    def test_sort_multi_param(self):
        s = Search().sort("field", "-another", ["third"], ("-4th", ))
        self.assertRequest(s, {
            "body": {
                "sort": [
                    "field",
                    {"another": "desc"},
                    "third",
                    {"4th": "desc"},
                ],
            }
        })

    def test_replace_query(self):
        s = Search().query(query.MatchNone())
        self.assertRequest(s, {
            "body": {
                "query": {
                    "match_none": {}
                },
            }
        })

    def test_invert_query(self):
        s = Search().query(query.MatchAll())
        s = ~s
        self.assertRequest(s, {
            "body": {
                "query": {
                    "match_none": {}
                },
            }
        })

    def test_aggregation(self):
        s = Search()
        s.aggregation("terms", field="field")
        self.assertRequest(s, {
            "body": {
                "query": {
                    "match_all": {}
                },
                "aggregations": {
                    "a0": {
                        "terms": {
                            "field": "field"
                        }
                    }
                }
            }
        })
        s = Search()
        s.aggregation("my-agg", "terms", field="field")
        self.assertRequest(s, {
            "body": {
                "query": {
                    "match_all": {}
                },
                "aggregations": {
                    "my-agg": {
                        "terms": {
                            "field": "field"
                        }
                    }
                }
            }
        })
        with self.assertRaises(ValueError):
            s = Search()
            s.aggregation(field="field")

    def test_search_params_all(self):
        s = Search()
        for name, param in s.param.DEFINITION.items():
            value = "23"

            expected_value = value
            if name == "sort":
                expected_value = [value]

            expected_request = {
                "index": None,
                "params": {},
                "body": {
                    "query": {
                        "match_all": {}
                    },
                },
            }
            path = "params" if param["group"] == "query" else "body"
            expected_request[path][name] = expected_value

            func_name = name.lstrip("_")
            if func_name == "from":
                func_name = "from_"

            # change by s.param.func_name(value)
            s2 = getattr(s.param, func_name)(value)
            self.assertRequest(s2, expected_request)

            # change by s.param(func_name=value)
            s2 = s.param(**{func_name: value})
            self.assertRequest(s2, expected_request)

    def test_params_multi(self):
        s = Search().param(
            size=23,
            from_=42,
        )
        self.assertRequest(s, {
            "index": None,
            "params": {},
            "body": {
                "from": 42,
                "size": 23,
                "query": {"match_all": {}}
            },
        }, and_not_more=True)

        self.assertEqual(
            s.to_request(),
            s.param().to_request(),
        )

    def test_params_replace_to_default(self):
        s = Search().size(23)
        self.assertRequest(s, {
            "index": None,
            "params": {},
            "body": {
                "size": 23,
                "query": {"match_all": {}}
            },
        }, and_not_more=True)

        s = s.param(size=10)
        self.assertRequest(s, {
            "index": None,
            "params": {},
            "body": {
                "query": {"match_all": {}}
            },
        }, and_not_more=True)


if __name__ == "__main__":
    unittest.main()
