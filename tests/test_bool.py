import os
import json
import time
import unittest

from elastipy import Search, query


class TestBool(unittest.TestCase):

    maxDiff = 10_000

    def q1(self):
        return query.Term("a", "1")

    def q2(self):
        return query.Term("b", "2")

    def q3(self):
        return query.Term("c", "3")

    def q4(self):
        return query.Term("d", "4")
    
    def assertEqualQuery(self, expected, real):
        if expected != real:
            raise AssertionError(
                f"Expected:\n{expected}\nGot:\n{real}"
            )
    
    def test_single_arg(self):
        self.assertEqualQuery(
            query.Bool(must=[self.q1()]),
            query.Bool(must=self.q1())
        )

    def test_transform_dict(self):
        self.assertEqualQuery(
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
        self.assertEqualQuery(
            [self.q1()],
            s.get_query().parameters["must"]
        )

        s = s.bool(must_not=self.q2())
        self.assertEqualQuery(
            [self.q1()],
            s.get_query().parameters["must"]
        )
        self.assertEqualQuery(
            [self.q2()],
            s.get_query().parameters["must_not"]
        )

    def test_assignment(self):
        q = query.Bool(must=[self.q1()])
        q.filter = [self.q2()]
        self.assertEqualQuery(
            query.Bool(must=[self.q1()], filter=[self.q2()]),
            q
        )
        self.assertEqualQuery(2, len(q.parameters))

        q.must = [self.q3()]
        self.assertEqualQuery(
            query.Bool(must=[self.q3()], filter=[self.q2()]),
            q
        )

        q.must = None  # default value
        self.assertEqualQuery(
            query.Bool(filter=[self.q2()]),
            q
        )
        self.assertEqualQuery(1, len(q.parameters))

    def test_or_1(self):
        self.assertEqualQuery(
            query.Bool(
                should=[self.q1(), self.q2()],
            ),
            self.q1() | self.q2()
        )

    def test_or_2(self):
        self.assertEqualQuery(
            query.Bool(
                should=[query.Bool(must=self.q1()), query.Bool(must=self.q2())],
            ),
            query.Bool(must=self.q1()) | query.Bool(must=self.q2())
        )

    def test_or_3(self):
        self.assertEqualQuery(
            query.Bool(
                should=[self.q1(), self.q2()],
            ),
            query.Bool(should=[self.q1()]) | self.q2()
        )

    def test_or_4(self):
        self.assertEqualQuery(
            query.Bool(
                should=[query.Bool(must=self.q1()), self.q2()],
            ),
            query.Bool(must=self.q1()) | self.q2()
        )

    def test_or_5(self):
        self.assertEqualQuery(
            query.Bool(
                should=[query.Bool(must=self.q1(), should=self.q3()), self.q2()],
            ),
            query.Bool(must=self.q1(), should=self.q3()) | self.q2()
        )

    def test_or_6(self):
        self.assertEqualQuery(
            query.Bool(
                should=[self.q2(), query.Bool(must=self.q1())],
            ),
            self.q2() | query.Bool(must=self.q1())
        )

    def test_or_regression_16(self):
        """
        https://github.com/netzkolchose/elastipy/issues/16
        """
        s = (
            (self.q1() | self.q2())
            & (
                (self.q2() & self.q3())
                | (self.q2() & self.q4())
            )
        )
        self.assertEqualQuery(
            query.Bool(
                must=[
                    query.Bool(should=[self.q1(), self.q2()]),
                    query.Bool(should=[
                        query.Bool(must=[self.q2(), self.q3()]),
                        query.Bool(must=[self.q2(), self.q4()]),
                    ]),
                ],
            ),
            s
        )
        self.assertEqual(
            {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {"term": {"a": {"value": "1"}}},
                                    {"term": {"b": {"value": "2"}}},
                                ]
                            }
                        },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "bool": {
                                            "must": [
                                                {"term": {"b": {"value": "2"}}},
                                                {"term": {"c": {"value": "3"}}},
                                            ]
                                        }
                                    },
                                    {
                                        "bool": {
                                            "must": [
                                                {"term": {"b": {"value": "2"}}},
                                                {"term": {"d": {"value": "4"}}},
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            s.to_dict(),
        )

    def test_or_regression_16_with_other(self):
        self.assertEqualQuery(
            query.Bool(
                should=[self.q1(), self.q2()],
                must=[self.q3()],
            ),
            (self.q1() | self.q2()) & self.q3()
        )

    def test_and_with_other(self):
        self.assertEqualQuery(
            query.Bool(must=[self.q1(), self.q2()]),
            query.Bool(must=[self.q1()]) & self.q2()
        )

    def test_and_avoid_multiples_with_other(self):
        self.assertEqualQuery(
            query.Bool(must=[self.q1(), self.q2()]),
            query.Bool(must=[self.q1()]) & self.q2() & self.q2()
        )

    def test_and_avoid_multiples(self):
        self.assertEqualQuery(
            query.Bool(must=[self.q1(), self.q2()]),
            query.Bool(must=[self.q1()]) & query.Bool(must=[self.q2()]) & query.Bool(must=[self.q2()])
        )

    def test_and_all(self):
        self.assertEqualQuery(
            query.Bool(
                must=[self.q1(), self.q2()],
                must_not=[self.q2(), self.q3()],
                filter=[self.q3(), self.q4()],
            ),
            query.Bool(
                must=[self.q1()],
                must_not=[self.q2()],
                filter=[self.q3()],
            ) & query.Bool(
                must=[self.q2()],
                must_not=[self.q3()],
                filter=[self.q4()],
            ),
        )


if __name__ == "__main__":
    unittest.main()
