import os
import json
import time
import unittest

from elastipy import Search, query
from elastipy.query import factory, factory_from_dict


class TestQueryHousing(unittest.TestCase):

    def test_no_query_instance(self):
        with self.assertRaises(TypeError):
            query.Query()

    def test_factory_special_type(self):
        self.assertEqual(
            query.Bool,
            type(query.factory("bool"))
        )

    def test_factory_from_dict(self):
        self.assertEqual(
            query.Term(field="field1", value="value1", boost=23.),
            factory_from_dict({"term": {"field1": {"value": "value1", "boost": 23.}}})
        )

        self.assertEqual(
            query.Terms(field="field1", value=[1, 2, 3], boost=23.),
            factory_from_dict({"terms": {"field1": [1, 2, 3], "boost": 23.}})
        )

        with self.assertRaises(TypeError):
            factory_from_dict({"some": {}, "other": {}})

        with self.assertRaises(TypeError):
            query.Term.from_dict({"some": {}, "other": {}})

    def test_to_dict(self):
        self.assertEqual(
            {"term": {"field1": {"value": "value1", "boost": 23.}}},
            query.Term(field="field1", value="value1", boost=23.).to_dict()
        )
        self.assertEqual(
            {"terms": {"field1": [1, 2, 3]}},
            query.Terms(field="field1", value=[1, 2, 3]).to_dict()
        )
        self.assertEqual(
            {"terms": {"field1": [1, 2, 3], "boost": 23.}},
            query.Terms(field="field1", value=[1, 2, 3], boost=23.).to_dict()
        )

    def test_compare(self):
        self.assertEqual(
            query.Term("a", "b"),
            query.Term("a", "b"),
        )
        self.assertEqual(
            query.Term("a", "b"),
            {"term": {"a": {"value": "b"}}},
        )
        self.assertIn(
            query.Term("a", "b"),
            [query.Term("c", "d"), query.Term("a", "b")],
        )
        self.assertNotEqual(
            query.Term("a", "b"),
            query.Term("a", "c"),
        )
        self.assertNotEqual(
            query.Term("a", "b"),
            query.Match("a", "c"),
        )
        for not_a_query in (None, [], 23):
            self.assertNotEqual(query.Term("a", "b"), not_a_query)

    def test_copy_compare(self):
        q1 = query.Term("a", "b")
        q2 = q1.copy()
        self.assertEqual(q1, q2)
        self.assertNotEqual(id(q1), id(q2))

        q1.parameters["value"] = "c"
        self.assertNotEqual(q1, q2)

    def test_copy_deep(self):
        q1 = query.Bool(must=[query.Bool(must=[query.Term("a", "b")])])
        q2 = q1.copy()
        self.assertEqual(q1, q2)
        self.assertNotEqual(id(q1), id(q2))
        self.assertNotEqual(id(q1.must[0]), id(q2.must[0]))
        self.assertNotEqual(id(q1.must[0].must[0]), id(q2.must[0].must[0]))

        q1.must[0].must[0].parameters["field"] = "x"
        self.assertNotEqual(q1, q2)

    def test_copy(self):
        s = Search().copy().bool(must=query.MatchAll())
        self.assertEqual(
            [query.MatchAll()],
            s.get_query().parameters["must"]
        )
        s = s.copy().bool(must_not=query.MatchNone())
        self.assertEqual(
            [query.MatchNone()],
            s.get_query().parameters["must_not"]
        )

    def test_repr(self):
        q = query.Term("field", "value")
        self.assertEqual(
            "Term(field='field', value='value')",
            repr(q)
        )


if __name__ == "__main__":
    unittest.main()
