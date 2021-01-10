import time
import unittest
from decimal import Decimal

from elastipy import Search
from elastipy.plot.text.console import Characters
from elastipy.plot.text import Table


class TestTable(unittest.TestCase):

    def assertTableStr(self, rows, expected_str, colors=False, ascii=True, **kwargs):
        table = Table(rows)
        expected_str = "\n".join(line.strip() for line in expected_str.splitlines()).strip()

        table_str = table.to_str(colors=colors, ascii=ascii, **kwargs)
        table_str = "\n".join(line.strip() for line in table_str.splitlines()).strip()

        if table_str != expected_str:
            expected_str = "\n".join(f"[{line}]" for line in expected_str.splitlines())
            table_str = "\n".join(f"[{line}]" for line in table_str.splitlines())
            raise AssertionError(
                f"Table did not match.\n\n# Expected:\n{expected_str}\n\n# Got:\n{table_str}"
            )

    def test_table(self):
        self.assertTableStr(
            [
                ["string", "number", "another"],
                ["a", 1, Decimal(10)],
                ["baccus", 2, Decimal(9)],
                ["cedelio", 3, Decimal(8)],
            ],
            """
            string  | number | another
            --------+--------+--------
            a       | 1      | 10
            baccus  | 2      |  9
            cedelio | 3      |  8
            """,
            bars=False,
        )
        self.assertTableStr(
            [
                ["string", "number", "another"],
                ["a", 1, Decimal(10)],
                ["baccus", 2, Decimal(9)],
                ["cedelio", 3, Decimal(8)],
            ],
            """
            a       | 1 | 10
            baccus  | 2 |  9
            cedelio | 3 |  8
            """,
            bars=False,
            header=False,
        )

    def test_table_bars(self):
        self.assertTableStr(
            [
                ["a", "b", "cccc"],
                ["x", 1, Decimal(10)],
                ["yyy", 9, None],
                ["z", 30, 8.],
            ],
            """
            a   | b          | cccc
            ----+------------+------------
            x   |  1 :       |  10 #######
            yyy |  9 ##:     |   -
            z   | 30 ####### | 8.0 :
            """,
            bars=True,
            ascii=True,
            max_width=30,
        )


if __name__ == "__main__":
    unittest.main()
