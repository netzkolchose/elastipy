import unittest
import datetime
from decimal import Decimal

from elastipy.dump import Table


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

    def test_digits(self):
        table = [
            ["a", "b"],
            [0.12345678, 0.12],
            [0.98765432, "a"],
            [None, 9.87654]
        ]
        self.assertTableStr(
            table,
            """
            a          | b
            -----------+--------
            0.12345678 |    0.12
            0.98765432 |       a
                     - | 9.87654
            """,
            bars=False,
        )
        self.assertTableStr(
            table,
            """
            a     | b
            ------+------
            0.123 |  0.12
            0.988 |     a
                - | 9.877
            """,
            bars=False,
            digits=3
        )

    def test_auto_max_width(self):
        self.assertTableStr(
            [["a", "b"], [1, 2]],
            """
            a | b
            --+--
            1 | 2
            """,
            max_width=None
        )

    def test_sort(self):
        table = [
            ["string", "number", "date"],
            ["a", 3, datetime.date(2000, 1, 2)],
            ["c", 1, None],
            ["b", None, datetime.date(2000, 1, 3)],
            [None, 2, datetime.date(2000, 1, 1)],
        ]
        self.assertTableStr(
            table,
            """
            string | number | date
            -------+--------+-----------
            -      | 2      | 2000-01-01
            a      | 3      | 2000-01-02 
            b      | -      | 2000-01-03
            c      | 1      | -
            """,
            bars=False,
            sort="string",
        )
        self.assertTableStr(
            table,
            """
            string | number | date
            -------+--------+-----------
            b      | -      | 2000-01-03
            c      | 1      | -
            -      | 2      | 2000-01-01
            a      | 3      | 2000-01-02 
            """,
            bars=False,
            sort="number",
        )
        self.assertTableStr(
            table,
            """
            string | number | date
            -------+--------+-----------
            c      | 1      | -
            -      | 2      | 2000-01-01
            a      | 3      | 2000-01-02 
            b      | -      | 2000-01-03
            """,
            bars=False,
            sort="date",
        )
        self.assertTableStr(
            table,
            """
            string | number | date
            -------+--------+-----------
            b      | -      | 2000-01-03
            a      | 3      | 2000-01-02 
            -      | 2      | 2000-01-01
            c      | 1      | -
            """,
            bars=False,
            sort="-date",
        )

    def test_bars(self):
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
            max_width=30,
            zero=False,
        )

    def test_bars_maxwidth(self):
        # cccc... has a long header so it get's extra space for bars
        self.assertTableStr(
            [
                ["a", "b", "ccccccccccccc"],
                ["x", 1, Decimal(10)],
                ["yyy", 9, 4],
                ["z", 30, 8.],
            ],
            """
            a   | b    | ccccccccccccc
            ----+------+--------------
            x   |  1   |  10 #########
            yyy |  9 . |   4 :
            z   | 30 # | 8.0 ######
            """,
            bars=True,
            max_width=26,
            zero=False,
        )

        # 'b' would only have space for the 'space' character not for a bar itself
        # so the bar is removed and extra space given to cccc..
        self.assertTableStr(
            [
                ["a", "b", "ccccccccccccc"],
                ["x", 1, Decimal(10)],
                ["yyy", 9, 4],
                ["z", 30, 8.],
            ],
            """
            a   | b  | ccccccccccccc
            ----+----+---------------
            x   |  1 |  10 ##########
            yyy |  9 |   4 :
            z   | 30 | 8.0 ######:
            """,
            bars=True,
            max_width=25,
            zero=False,
        )

    def test_bars_no_space(self):
        self.assertTableStr(
            [
                ["a", "b"],
                [0, 0],
                [10, 10],
            ],
            """
            a  | b   
            ---+---
             0 |  0
            10 | 10
            """,
            bars=True,
            max_width=7,
        )

    def test_no_data(self):
        self.assertTableStr(
            [
                ["a", "b"],
            ],
            """
            a | b   
            --+--
            """,
            bars=True,
        )

    def test_bars_zero_param(self):
        for zero in (True, False):
            self.assertTableStr(
                [
                    ["number"],
                    [0],
                    [5],
                ],
                """
                number
                --------------------
                0 :
                5 ##################
                """,
                max_width=20,
                zero=True,
            )
        self.assertTableStr(
            [
                ["number"],
                [3],
                [5],
            ],
            """
            number
            --------------------
            3 ###########
            5 ##################
            """,
            max_width=20,
            zero=True,
        )
        self.assertTableStr(
            [
                ["number"],
                [3],
                [5],
            ],
            """
            number
            --------------------
            3 :
            5 ##################
            """,
            max_width=20,
            zero=False,
        )

    def test_bars_zero_param_neg(self):
        for zero in (True, False):
            self.assertTableStr(
                [
                    ["number"],
                    [-5],
                    [0],
                    [5],
                ],
                """
                number
                --------------------
                -5 :
                 0 ########:
                 5 #################
                """,
                max_width=20,
                zero=zero,
            )
        self.assertTableStr(
            [
                ["number"],
                [-5],
                [0],
                [5],
            ],
            """
            number
            --------------------
            -5 
             0 :
             5 #################
            """,
            max_width=20,
            zero=0,
        )
        self.assertTableStr(
            [
                ["number"],
                [-5],
                [0],
                [5],
            ],
            """
            number
            --------------------
            -5 ######
             0 ###########:
             5 #################
            """,
            max_width=20,
            zero=-10,
        )

    def test_incomplete_rows(self):
        self.assertTableStr(
            [
                ["a", "b"],
                [1, 2],
                [3]
            ],
            """
            a | b
            --+--
            1 | 2
            3 | -
            """,
            bars=False,
        )
        self.assertTableStr(
            [
                {"a": 1, "b": 2},
                {"a": 3},
                {"b": 4},
                {},
            ],
            """
            a | b
            --+--
            1 | 2
            3 | -
            - | 4
            - | -
            """,
            bars=False,
        )


if __name__ == "__main__":
    unittest.main()
