import datetime
import unittest
from decimal import Decimal

from docs.sphinx_ext.link import relative_path_change


class TestDocExtensions(unittest.TestCase):

    def test_relative_path(self):
        self.assertEqual(
            "",
            relative_path_change("", "")
        )
        self.assertEqual(
            "a/b",
            relative_path_change("", "a/b")
        )
        self.assertEqual(
            "../..",
            relative_path_change("a/b", "")
        )
        self.assertEqual(
            "../c",
            relative_path_change("a/b", "a/c")
        )
        self.assertEqual(
            "../../c/d",
            relative_path_change("a/b", "c/d")
        )


if __name__ == "__main__":
    unittest.main()
