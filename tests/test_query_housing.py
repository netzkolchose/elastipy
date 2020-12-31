import os
import json
import time
import unittest

from elastipy import Search, query


class TestQueryHousing(unittest.TestCase):

    def test_factory(self):
        self.assertEqual(
            query.Bool,
            type(query.factory("bool"))
        )

    def test_compare(self):
        self.assertEqual(
            query.Term("a", "b"),
            query.Term("a", "b"),
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


if __name__ == "__main__":
    unittest.main()
