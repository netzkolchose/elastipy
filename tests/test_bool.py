import os
import json
import time
import unittest

from elastipy import Search, query


class TestBool(unittest.TestCase):

    def q1(self):
        return query.Term("a", "1")

    def q2(self):
        return query.Term("b", "2")

    def q3(self):
        return query.Term("c", "3")

    def q4(self):
        return query.Term("d", "4")

    def test_single_arg(self):
        self.assertEqual(
            query.Bool(must=[self.q1()]),
            query.Bool(must=self.q1())
        )

    def test_transform_dict(self):
        self.assertEqual(
            query.Bool(must=[query.Term("a", 1)]),
            query.Bool(must=[{"term": {"a": {"value": 1}}}])
        )

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            query.Bool(must=23)

        with self.assertRaises(TypeError):
            query.Bool(must=[{"bool": {"must": 23}}])

    def test_copy_bug(self):
        s = Search().copy().bool(must=self.q1())
        self.assertEqual(
            [self.q1()],
            s.get_query().parameters["must"]
        )

        s = s.bool(must_not=self.q2())
        self.assertEqual(
            [self.q1()],
            s.get_query().parameters["must"]
        )
        self.assertEqual(
            [self.q2()],
            s.get_query().parameters["must_not"]
        )

    def test_assignment(self):
        q = query.Bool(must=[self.q1()])
        q.filter = [self.q2()]
        self.assertEqual(
            query.Bool(must=[self.q1()], filter=[self.q2()]),
            q
        )
        self.assertEqual(2, len(q.parameters))

        q.must = [self.q3()]
        self.assertEqual(
            query.Bool(must=[self.q3()], filter=[self.q2()]),
            q
        )

        q.must = None  # default value
        self.assertEqual(
            query.Bool(filter=[self.q2()]),
            q
        )
        self.assertEqual(1, len(q.parameters))

    def test_or_1(self):
        self.assertEqual(
            query.Bool(
                should=[self.q1(), self.q2()],
            ),
            self.q1() | self.q2()
        )

    def test_or_2(self):
        self.assertEqual(
            query.Bool(
                should=[query.Bool(must=self.q1()), query.Bool(must=self.q2())],
            ),
            query.Bool(must=self.q1()) | query.Bool(must=self.q2())
        )

    def test_or_3(self):
        self.assertEqual(
            query.Bool(
                should=[self.q1(), self.q2()],
            ),
            query.Bool(should=[self.q1()]) | self.q2()
        )

    def test_or_4(self):
        self.assertEqual(
            query.Bool(
                should=[query.Bool(must=self.q1()), self.q2()],
            ),
            query.Bool(must=self.q1()) | self.q2()
        )

    def test_or_5(self):
        self.assertEqual(
            query.Bool(
                should=[query.Bool(must=self.q1(), should=self.q3()), self.q2()],
            ),
            query.Bool(must=self.q1(), should=self.q3()) | self.q2()
        )

    def test_or_6(self):
        self.assertEqual(
            query.Bool(
                should=[self.q2(), query.Bool(must=self.q1())],
            ),
            self.q2() | query.Bool(must=self.q1())
        )


if __name__ == "__main__":
    unittest.main()
