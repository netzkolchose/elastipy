import unittest
import datetime
from decimal import Decimal

from definition.generator import change_text_indent
from definition.renderer import doc_to_rst


class TestGenerator(unittest.TestCase):

    def test_doc_to_rst(self):
        self.assertEqual(
            """Here is a `link <https://example.com>`__!""",
            doc_to_rst("""Here is a [link](https://example.com)!"""),
        )
        self.assertEqual(
            """
            Here are two links, `a <https://example.com>`__ and `b <https://example.gov>`__!
            And one on the next line `c <https://example.org>`__!
            """,
            doc_to_rst("""
            Here are two links, [a](https://example.com) and [b](https://example.gov)!
            And one on the next line [c](https://example.org)!
            """),
        )


if __name__ == "__main__":
    unittest.main()
