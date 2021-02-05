import datetime
import unittest
from decimal import Decimal

from definition.renderer import change_text_indent
from docs.helper import (
    remove_hidden_cells_markdown,
    remove_hidden_cells_rst,
    fix_links_in_rst,
)

class TestDocHelper(unittest.TestCase):

    def assertEqualText(self, expected_text: str, text: str):
        expected_text = "\n".join(
            line.rstrip() for line in change_text_indent(expected_text).splitlines()
        ).strip()
        text = "\n".join(
            line.rstrip() for line in change_text_indent(text).splitlines()
        ).strip()

        if expected_text != text:
            expected_text = "\n".join(f"[{line}]" for line in expected_text.splitlines())
            text = "\n".join(f"[{line}]" for line in text.splitlines())
            raise AssertionError(
                f"Text not equal\n\n# Expected:\n{expected_text}\n\n# Got:\n{text}"
            )

    def test_fix_rst_links(self):
        self.assertEqual(
            "bla bla :link:`goal` bla",
            fix_links_in_rst(
                "bla bla :link:``goal`` bla"
            )
        )
        # multi
        self.assertEqual(
            "bla bla :link:`goal` bla :other:`stuff`",
            fix_links_in_rst(
                "bla bla :link:``goal`` bla :other:``stuff``"
            )
        )

    def test_remove_hidden_cells_markdown(self):
        self.assertEqualText(
            """
            Hello


            ```
            visible-stuff
            ```
            
            World
            """,
            remove_hidden_cells_markdown(change_text_indent(
                """
                Hello 
                
                ```
                # run-but-hide
                hidden-stuff
                ```

                ```
                visible-stuff
                ```
                
                World
                """
            ), ["# run-but-hide"])
        )

    def test_remove_hidden_cells_rst(self):
        self.assertEqualText(
            """
            Hello

            headline
            --------
            
            .. parsed-literal::
            
                stuff
            
            .. parsed-literal::
                
                other-stuff

            World
            """,
            remove_hidden_cells_rst(change_text_indent(
                """
                Hello 
                
                .. code::
                
                    # run-but-hide
                    for i in range(10:
                        secret_stuff()
                    done()

                headline
                --------
                                
                .. parsed-literal::
                
                    stuff

                .. parsed-literal::
                
                    other-stuff
                
                World
                """
            ), ["# run-but-hide", "# secret"])
        )


if __name__ == "__main__":
    unittest.main()
