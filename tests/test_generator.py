import unittest
import datetime
from decimal import Decimal

from definition.generator import change_text_indent
from definition.renderer import (
    doc_to_rst, remove_single_newlines,
    markdown_links_to_rst, markdown_literals_to_rst,
)


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

    def test_markdown_literals(self):
        self.assertEqualText(
            """This is ``code``, and this ``also``""",
            markdown_literals_to_rst(
                """This is `code`, and this `also`"""
            ),
        )

    def test_markdown_literals_exceptions(self):
        self.assertEqualText(
            """Someone already did it ``doubly``, and even ``trice``, and ``correctly``""",
            markdown_literals_to_rst(
                """Someone already did it ``doubly``, and even ```trice```, and `correctly`"""
            ),
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

    def test_remove_single_newlines(self):
        self.assertEqualText(change_text_indent(
                """
                A text that has been wrapped around by the author.
                
                This is a new paragraph.
                """
            ),
            remove_single_newlines(change_text_indent(
                """
                A text that has been 
                wrapped around by the
                author.
                
                This is a new paragraph.
                """
            ))
        )

    def test_remove_single_newlines_indent(self):
        self.assertEqualText(change_text_indent(
            """
            A text that has been wrapped around by the author.
            
                This is a new indented paragraph. I keep writing on...
            """
        ),
            remove_single_newlines(change_text_indent(
                """
                A text that has been 
                wrapped around by the
                author.
                
                    This is a new indented paragraph.
                    I keep writing on...
                """
            ))
        )


if __name__ == "__main__":
    unittest.main()
