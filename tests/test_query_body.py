import os
import json
import time
import unittest

from elastipy import Search, query


class TestQueryBody(unittest.TestCase):

    def query_test(self, name, func):
        """
        Test that a Query construct creates the desired body
        :param name: str, name of function to test
        :param func: function receiving a QueryInterface compatible instance
            and returning tuple of query and expected body dict
        """
        for i in range(2):
            if i == 0:
                q = query.MatchAll()
            else:
                q = Search()

            q, expected_body = func(q)
            if i == 0:
                real_body = q.to_dict()
            else:
                real_body = q.body["query"]
            self.assertEqual(
                expected_body,
                real_body,
                f"\nExpected: {json.dumps(expected_body, indent=2)}\n"
                f"\nGot: {json.dumps(real_body, indent=2)}"
                f"\nIn function {repr(name)}"
            )

    def test_AND(self):
        def test2(q: query.QueryInterface):
            q = q.term("a", "b").term("c", "d")
            return q, {
                'bool': {'must': [
                    {'term': {'a': {'value': 'b'}}},
                    {'term': {'c': {'value': 'd'}}},
                ]}
            }

        def test3(q: query.QueryInterface):
            q = q.term("a", "b").term("c", "d").term("e", "f")
            return q, {
                'bool': {'must': [
                    {'term': {'a': {'value': 'b'}}},
                    {'term': {'c': {'value': 'd'}}},
                    {'term': {'e': {'value': 'f'}}},
                ]}
            }

        for name, func in locals().items():
            if callable(func) and name != "self":
                self.query_test(name, func)

    def test_OR(self):
        def test2(q: query.QueryInterface):
            q = q.term("a", "b") | q.term("c", "d")
            return q, {
                'bool': {'should': [
                    {'term': {'a': {'value': 'b'}}},
                    {'term': {'c': {'value': 'd'}}},
                ]}
            }

        def test3(q: query.QueryInterface):
            q = q.term("a", "b") | q.term("c", "d") | q.term("e", "f")
            return q, {
                'bool': {'should': [
                    {'term': {'a': {'value': 'b'}}},
                    {'term': {'c': {'value': 'd'}}},
                    {'term': {'e': {'value': 'f'}}},
                ]}
            }

        for name, func in locals().items():
            if callable(func) and name != "self":
                self.query_test(name, func)

    def test_AND_avoid_duplicates(self):
        def test3(q: query.QueryInterface):
            q = q.term("a", "b")
            # both ANDed queries contain the a-b part from above
            q = q.term("c", "d") & q.term("e", "f")
            return q, {
                'bool': {'must': [
                    {'term': {'a': {'value': 'b'}}},
                    {'term': {'c': {'value': 'd'}}},
                    {'term': {'e': {'value': 'f'}}},
                ]}
            }

        for name, func in locals().items():
            if callable(func) and name != "self":
                self.query_test(name, func)

    def test_bool_filter(self):
        def test1(q: query.QueryInterface):
            q = q.bool(filter=[query.Term("a", "b")])
            return q, {
                'bool': {'filter': [
                    {'term': {'a': {'value': 'b'}}},
                ]}
            }
    
        for name, func in locals().items():
            if callable(func) and name != "self":
                self.query_test(name, func)


if __name__ == "__main__":
    unittest.main()
