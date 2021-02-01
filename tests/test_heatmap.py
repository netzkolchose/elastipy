import unittest
from io import StringIO
from copy import deepcopy

from elastipy.dump import Heatmap
from elastipy.aggregation.helper import remove_matrix_axis
from definition.renderer import change_text_indent


class TestHeatmap(unittest.TestCase):

    def assertHeatmapStr(self, keys, values, expected_str, colors=False, ascii=True, annotate=False, **kwargs):
        heatmap = Heatmap(keys, values, colors=colors, ascii=ascii)
        expected_str = "\n".join(
            line.rstrip()
            for line in change_text_indent(expected_str).splitlines()
        )

        file = StringIO()
        heatmap.print(annotate=annotate, **kwargs, file=file)
        file.seek(0)
        real_str = "\n".join(line.rstrip() for line in file.read().splitlines())

        if real_str != expected_str:
            expected_str = "\n".join(f"[{line}]" for line in expected_str.splitlines())
            real_str = "\n".join(f"[{line}]" for line in real_str.splitlines())
            raise AssertionError(
                f"Heatmap did not match.\n\n# Expected:\n{expected_str}\n\n# Got:\n{real_str}"
            )

    def assertRemoveMatrix(self, matrix, dim, index, expected_result):
        result = deepcopy(matrix)
        remove_matrix_axis(result, dim, index)
        self.assertEqual(expected_result, result)

    def test_remove_matrix(self):
        self.assertRemoveMatrix(
            [
                [1, 2],
                [3, 4],
            ],
            0, 0,
            [
                [3, 4],
            ],
        )
        self.assertRemoveMatrix(
            [
                [1, 2],
                [3, 4],
            ],
            0, 1,
            [
                [1, 2],
            ],
        )
        self.assertRemoveMatrix(
            [
                [1, 2],
                [3, 4],
            ],
            1, 0,
            [
                [2],
                [4],
            ],
        )
        self.assertRemoveMatrix(
            [
                [1, 2],
                [3, 4],
            ],
            1, 1,
            [
                [1],
                [3],
            ],
        )

    def test_heatmap(self):
        self.assertHeatmapStr(
            keys=[
                ["a", "b"],
                ["0", "1", "2"]
            ],
            values=[
                [None, 2, 3],
                [4, None, 6],
            ],
            cell_width=2,
            expected_str=r"""
              /-+-+--\
            2 + ::## +
            1 + ..   +
            0 +   ** +
              \-+-+--/
                a b
            """,
        )

    def test_heatmap_unicode(self):
        self.assertHeatmapStr(
            keys=[
                ["a", "b"],
                ["0", "1", "2"]
            ],
            values=[
                [None, 2, 3],
                [4, None, 6],
            ],
            cell_width=2,
            ascii=False,
            colors=False,
            expected_str=r"""
              ┌─┼─┼──┐
            2 ┼ ▒▒██ ┼
            1 ┼ ░░   ┼
            0 ┼   ▓▓ ┼
              └─┼─┼──┘
                a b
            """,
        )

    def test_heatmap_bottom_keys(self):
        self.assertHeatmapStr(
            keys=[
                ["a", "bb", "ccc", "dddd"],
                ["0", "1", "2"]
            ],
            values=[
                [None, 2, 3],
                [4, None, 6],
                [4, None, 6],
                [4, None, 6],
            ],
            cell_width=2,
            expected_str=r"""
              /-+-+-+-+--\
            2 + ::###### +
            1 + ..       +
            0 +   ****** +
              \-+-+-+-+--/
                a  ccc 
                  bb dddd
            """,
        )

    def x_test_heatmap(self):
        self.assertHeatmapStr(
            keys=[
                ["alpha", "beta"],
                ["0-10", "10-20", "20-30"]
            ],
            values=[
                [1, 2, 3],
                [4, 5, 6],
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

    def x_test_heatmap_accidents(self):
        self.assertHeatmapStr(
            keys=[
                ['01 Sunday', '02 Monday', '03 Tuesday', '04 Wednesday', '05 Thursday', '06 Friday', '07 Saturday'],
                [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0],
            ],
            values=[[636, 576, 476, 449, 405, 385, 311, 266, 372, 653, 1013, 1511, 1667, 1928, 2186, 2085, 2022, 2084, 1752, 1297, 925, 654, 491, 321], [197, 118, 90, 100, 157, 736, 1650, 3610, 2469, 2185, 2169, 2286, 2351, 2779, 2853, 3512, 4005, 3772, 2596, 1614, 987, 693, 608, 312], [252, 148, 143, 119, 169, 720, 1626, 3589, 2525, 2075, 2036, 2156, 2330, 2731, 2883, 3380, 4073, 3818, 2675, 1713, 1086, 786, 626, 352], [209, 132, 121, 105, 157, 669, 1570, 3546, 2332, 2040, 1932, 2225, 2409, 2704, 2845, 3429, 3919, 3805, 2837, 1773, 1184, 851, 690, 397], [244, 173, 143, 130, 176, 665, 1416, 3118, 2259, 1953, 1914, 2157, 2274, 2779, 2915, 3610, 3947, 3910, 2838, 1803, 1200, 842, 736, 445], [266, 213, 146, 127, 195, 678, 1302, 2985, 1889, 1983, 2122, 2566, 3115, 3816, 3859, 3650, 3514, 3337, 2581, 1859, 1312, 1011, 917, 688], [559, 529, 414, 336, 290, 404, 416, 506, 810, 1387, 2073, 2556, 2534, 2624, 2687, 2444, 2181, 2301, 2021, 1578, 1171, 964, 840, 761]],
            expected_str="",
            colors=True,
            ascii=False,
        )


if __name__ == "__main__":
    unittest.main()
