import os
import json
import time
import unittest

from elastipy import Search, query


class TestBool(unittest.TestCase):

    def test_copy_bug(self):
        s = Search().copy().bool(must=query.MatchAll())
        self.assertEqual(
            [query.MatchAll()],
            s.get_query().parameters["must"]
        )
        s = s.bool(must_not=query.MatchNone())
        self.assertEqual(
            [query.MatchAll()],
            s.get_query().parameters["must"]
        )
        self.assertEqual(
            [query.MatchNone()],
            s.get_query().parameters["must_not"]
        )


if __name__ == "__main__":
    unittest.main()
