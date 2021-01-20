import unittest
import datetime
from decimal import Decimal

from definition.generator import change_text_indent
from definition.renderer import (
    doc_to_rst
)


class TestGenerator(unittest.TestCase):

    def assertEqualText(self, expected: str, real: str):
        expected = "\n".join(line.rstrip() for line in expected.splitlines()).rstrip()
        real = "\n".join(line.rstrip() for line in real.splitlines()).rstrip()

        self.assertEqual(
            expected, real,
            "\n\nExpected:\n%s\n\nGot:\n%s" % (
                "\n".join(f"[{line}]" for line in expected.splitlines()),
                "\n".join(f"[{line}]" for line in real.splitlines()),
            )
        )

    def test_change_indent(self):
        self.assertEqualText(
"""
level 1
    level 2
        level 3
""".strip(),
            change_text_indent("""
    level 1
        level 2
            level 3
""")
        )

    def test_change_indent_bullets(self):
        self.assertEqualText(
"""
- a short bullet point
- a long bullet point where
  the new line's indentation
  should be after the bullet
    - a sub bullet point that
      should also break
      correctly
""".strip(),
            change_text_indent("""
    - a short bullet point
    - a long bullet point where the new line's indentation should be after the bullet 
        - a sub bullet point that should also break correctly
""", max_length=30)
        )

    def test_change_indent_bullets_authors_newline(self):
        self.assertEqualText(
            """
- a short bullet point
- a long bullet point where 
  the new line's indentation 
  should be after the bullet
""".strip(),
            change_text_indent(doc_to_rst("""
    - a short bullet point
    - a long bullet point where the new line's 
    indentation should be after the bullet 
"""), max_length=30)
        )

    def test_doc_to_rst_bullets_authors_newline(self):
        self.assertEqualText(
            """
Example:

    - a long bullet point where the new line's indentation should be after the 
      bullet, even so, the author decided to break the line for better reading
    - another short point 
""".strip(),
            change_text_indent(doc_to_rst("""
    Example:
    
        - a long bullet point where the new line's indentation should be after the bullet, even so,
        the author decided to break the line for better reading
        - another short point 
"""), max_length=80),
        )

    def test_markdown_links(self):
        self.assertEqualText(
            """Here is a `link <https://example.com>`__!""",
            doc_to_rst("""Here is a [link](https://example.com)!"""),
        )
        self.assertEqualText(
            """
Here are two links, `a <https://example.com>`__ and `b <https://example.gov>`__!

And one on the next line `c <https://example.org>`__!
            """.strip(),
            doc_to_rst("""
            Here are two links, [a](https://example.com) and [b](https://example.gov)!
            
            And one on the next line [c](https://example.org)!
            """),
        )

    def test_markdown_literals(self):
        self.assertEqualText(
            """This is ``code``, and this ``also``""",
            doc_to_rst(
                """This is `code`, and this `also`"""
            ),
        )

    def test_markdown_literals_exceptions(self):
        self.assertEqualText(
            """Someone already did it ``doubly``, and even ``trice``, and ``correctly``""",
            doc_to_rst(
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
            doc_to_rst(change_text_indent(
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
            doc_to_rst(change_text_indent(
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
