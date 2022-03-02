import os
import json
import time
import inspect
import unittest
from io import StringIO
from typing import Optional, Union

from elastipy import Search, query


class TestSearchRequest(unittest.TestCase):

    def assertRequest(self, search: Search, expected_request: dict, and_not_more: bool = False):
        for version in (7, 8):
            search._version = version

            if version == 8:
                expected_request = {
                    **{key: value for key, value in expected_request.items() if key not in ("params", "body")},
                    **(expected_request.get("params") or {}),
                    **(expected_request.get("body") or {}),
                }

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

    def test_invalid_version(self):
        with self.assertRaises(ValueError):
            Search(version=6)

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
        s = Search().query(query.MatchNone())
        s = ~s
        self.assertRequest(s, {
            "body": {
                "query": {
                    "match_all": {}
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

    def test_highlight_global_and_field(self):
        self.assertRequest(
            Search().highlight(boundary_chars="abc"),
            {
                "index": None,
                "params": {},
                "body": {
                    "query": {"match_all": {}},
                    "highlight": {
                        "boundary_chars": "abc",
                    }
                },
            },
            and_not_more=True
        )
        self.assertRequest(
            Search()
                .highlight(boundary_chars="abc")
                .highlight("field1", boundary_chars="def")
                .highlight("field2"),
            {
                "index": None,
                "params": {},
                "body": {
                    "query": {"match_all": {}},
                    "highlight": {
                        "boundary_chars": "abc",
                        "fields": {
                            "field1": {"boundary_chars": "def"},
                            "field2": {},
                        }
                    }
                },
            },
            and_not_more=True
        )

    def test_highlight_all_params(self):
        args = inspect.getfullargspec(Search.highlight)
        param_types = {}
        for key, value in args.annotations.items():
            if key not in ("fields", "return"):
                if type(value) is type(Union):
                    self.assertIsNotNone(value.__args__[0])
                    param_type = value.__args__[0]
                else:
                    raise AssertionError(f"parameter '{key}' type {value} not handled")

                param_types[key] = param_type

        self.assertGreaterEqual(len(param_types), 20)

        for param_name, param_type in param_types.items():
            expected_value1, expected_value2 = None, None
            if param_type is str:
                value1 = param_name
                value2 = "".join(reversed(param_name))
            elif param_type is int:
                value1 = sum(ord(c) for c in param_name)
                value2 = value1 + 23
            elif param_type is bool:
                value1 = sum(ord(c) for c in param_name) & 1 == 0
                value2 = not value1
            elif param_type is query.Query:
                value1 = query.Match("some_field", param_name)
                expected_value1 = {"match": {"some_field": param_name}}
                value2 = query.Range("some_field", lte=param_name)
                expected_value2 = {"range": {"some_field": {"lte": param_name}}}
            elif param_name == "matched_fields":
                value1 = [param_name, "bla"]
                value2 = ["bla", param_name]
            else:
                raise AssertionError(f"parameter '{param_name}' type {param_type} not handled")

            if expected_value1 is None:
                expected_value1 = value1
            if expected_value2 is None:
                expected_value2 = value2

            s = (
                Search()
                .highlight(**{param_name: expected_value1})
                .highlight("field2", **{param_name: expected_value2})
            )
            self.assertRequest(
                s,
                {
                    "index": None,
                    "params": {},
                    "body": {
                        "query": {"match_all": {}},
                        "highlight": {
                            param_name: expected_value1,
                            "fields": {
                                "field2": {param_name: expected_value2},
                            }
                        }
                    },
                },
                and_not_more=True
            )


if __name__ == "__main__":
    unittest.main()
