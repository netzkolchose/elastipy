import unittest
import datetime
from decimal import Decimal
from io import StringIO

from elastipy.plot.text import Heatmap
from definition.renderer import change_text_indent

class TestHeatmap(unittest.TestCase):

    def assertHeatmapStr(self, keys, values, expected_str, colors=False, ascii=True, **kwargs):
        heatmap = Heatmap(keys, values, colors=colors, ascii=ascii)
        expected_str = "\n".join(
            line.rstrip()
            for line in change_text_indent(expected_str).splitlines()
        )

        file = StringIO()
        heatmap.print(**kwargs, file=file)
        file.seek(0)
        real_str = "\n".join(line.rstrip() for line in file.read().splitlines())

        if real_str != expected_str:
            expected_str = "\n".join(f"[{line}]" for line in expected_str.splitlines())
            real_str = "\n".join(f"[{line}]" for line in real_str.splitlines())
            raise AssertionError(
                f"Heatmap did not match.\n\n# Expected:\n{expected_str}\n\n# Got:\n{real_str}"
            )

    def test_heatmap(self):
        self.assertHeatmapStr(
            keys = [
                ["a", "b", "c"],
                ["x", "y", "z"]
            ],
            values = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
            expected_str="""
            string  | number | another
            --------+--------+--------
            a       | 1      | 10
            baccus  | 2      |  9
            cedelio | 3      |  8
            """,
            colors=True,
            ascii=False,
        )


if __name__ == "__main__":
    unittest.main()
