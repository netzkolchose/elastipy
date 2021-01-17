import unittest
import datetime
from decimal import Decimal

from definition.generator import change_text_indent
from definition.renderer import doc_to_rst, markdown_links_to_rst


class TestGenerator(unittest.TestCase):

    def assertEqualText(self, expected: str, real: str):
        self.assertEqual(
            expected, real,
            "\n\nExpected:\n%s\n\nGot:\n%s" % (
                "\n".join(f"[{line}]" for line in expected.splitlines()),
                "\n".join(f"[{line}]" for line in real.splitlines()),
            )
        )

    def test_markdown_links(self):
        self.assertEqualText(
            """Here is a `link <https://example.com>`__!""",
            markdown_links_to_rst("""Here is a [link](https://example.com)!"""),
        )
        self.assertEqualText(
            """
            Here are two links, `a <https://example.com>`__ and `b <https://example.gov>`__!
            And one on the next line `c <https://example.org>`__!
            """,
            markdown_links_to_rst("""
            Here are two links, [a](https://example.com) and [b](https://example.gov)!
            And one on the next line [c](https://example.org)!
            """),
        )

    def test_sections(self):
        self.assertEqualText(change_text_indent(
            """
            .. NOTE::
            
                Important!
            """),
            doc_to_rst(change_text_indent(
            """
            Note: Important!
            """))
        )
        self.assertEqualText(change_text_indent(
            """
            .. WARNING::
            
                Stuff!
            """),
            doc_to_rst(change_text_indent(
                """
                Warning:
                    Stuff!
                """))
        )


if __name__ == "__main__":
    unittest.main()
