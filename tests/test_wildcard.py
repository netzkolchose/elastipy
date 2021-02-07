import datetime
import unittest
from decimal import Decimal

from elastipy.aggregation.helper import wildcard_match, wildcard_filter


class TestWildcard(unittest.TestCase):

    def test_wildcard_match(self):
        with self.assertRaises(TypeError):
            wildcard_match("text", None)

        self.assertTrue(wildcard_match("text", "text"))
        self.assertTrue(wildcard_match("tex", "t*"))
        self.assertFalse(wildcard_match("tex", "*t"))

    def test_wildcard_filter(self):
        self.assertEqual(
            ["a1", "a2", "a3", "b1", "b2", "b3"],
            list(filter(
                lambda s: wildcard_filter(s, include=None, exclude=None),
                ["a1", "a2", "a3", "b1", "b2", "b3"]
            ))
        )

        self.assertEqual(
            ["a1", "a2", "a3"],
            list(filter(
                lambda s: wildcard_filter(s, include="a*", exclude=None),
                ["a1", "a2", "a3", "b1", "b2", "b3"]
            ))
        )

        self.assertEqual(
            ["b1", "b2", "b3"],
            list(filter(
                lambda s: wildcard_filter(s, include=None, exclude="a*"),
                ["a1", "a2", "a3", "b1", "b2", "b3"]
            ))
        )

        self.assertEqual(
            ["b3"],
            list(filter(
                lambda s: wildcard_filter(s, include="b*", exclude=["*1", "*2"]),
                ["a1", "a2", "a3", "b1", "b2", "b3"]
            ))
        )


if __name__ == "__main__":
    unittest.main()
