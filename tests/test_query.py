import os
import json
import time
import unittest

from elastipy import Search
from elastipy.query import Query, MatchAll


class TestQuery(unittest.TestCase):

    def query_test(self, name, func):
        """
        Test that a Query construct creates the desired body
        :param name: str, name of function to test
        :param func: function receiving a QueryInterface compatible instance
            and returning tuple of query and expected body dict
        """
        for i in range(2):
            if i == 0:
                q = MatchAll()
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

    def test_compare(self):
        self.assertEqual(
            Query.query_factory("term", field="a"),
            Query.query_factory("term", field="a"),
        )
        self.assertIn(
            Query.query_factory("term", field="a"),
            [Query.query_factory("term", field="a")],
        )
        self.assertNotEqual(
            Query.query_factory("term", field="a"),
            Query.query_factory("term", field="b"),
        )

    def test_AND(self):
        def test2(q: Query):
            q = q.term("a", "b").term("c", "d")
            return q, {
                'bool': {'must': [
                    {'term': {'a': {'value': 'b'}}},
                    {'term': {'c': {'value': 'd'}}},
                ]}
            }

        def test3(q: Query):
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
        def test2(q: Query):
            q = q.term("a", "b") | q.term("c", "d")
            return q, {
                'bool': {'should': [
                    {'term': {'a': {'value': 'b'}}},
                    {'term': {'c': {'value': 'd'}}},
                ]}
            }

        def test3(q: Query):
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
        def test3(q: Query):
            q = q.term("a", "b")
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


if __name__ == "__main__":
    unittest.main()
