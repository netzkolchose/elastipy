from typing import Sequence, Optional, TextIO

from .console import ColorScale, Characters, get_terminal_size, clip_line
from .helper import get_number, get_min_max


class Heatmap:

    def __init__(
            self,
            keys: Sequence[str],
            values: Sequence[Sequence[float]],
            colors: bool = True,
            ascii: bool = False,
            value_characters: Sequence[str] = None,
    ):
        self.keys = keys
        self.values = values
        self.width = len(self.keys[0])
        self.height = len(self.keys[1])
        self.scale = ColorScale(colors=colors, ascii=ascii, characters=value_characters)
        self.chars = Characters(ascii=ascii)

        self.keys_str = [
            [
                str(k) for k in row
            ]
            for row in keys
        ]

        min_v, max_v = get_min_max(self.values)
        if min_v is None:
            min_v, max_v = 0., 0.

        fac = 0.
        if min_v != max_v:
            fac = 1. / (max_v - min_v)

        self.values_str = [
            [
                self.scale((get_number(x) - min_v) * fac) if get_number(x) is not None else " "
                for x in row
            ]
            for row in self.values
        ]
        self.min_v = min_v
        self.max_v = max_v

    def print(
            self,
            cell_width: int = None,
            cell_height: int = None,
            max_width: int = None,
            max_cell_width: int = 10,
            max_axis_lines: int = 3,
            file: TextIO = None,
            digits: int = 3,
            annotate: bool = True,
    ):
        if max_width is None:
            max_width, _ = get_terminal_size()

        if not self.keys_str or not self.values_str:
            return

        if annotate:
            annot_lines = self._annotation_lines(digits=digits)
        else:
            annot_lines = None

        # -- space we need --

        left_key_width = max(len(key) for key in self.keys_str[1])
        bottom_key_width = max(len(key) for key in self.keys_str[0])
        left_width = left_key_width + 3

        if annot_lines:
            annot_width = max(len(line) for line in annot_lines)
        else:
            annot_width = 0

        # actual width without cells
        needed_width = left_width + 2 + annot_width + 1

        if cell_width is None:
            cell_width = (max_width - needed_width) // self.width
            cell_width = min(cell_width, max_cell_width)

        if cell_height is None:
            cell_height = max(1, int(cell_width / 2 + .5))

        right_end = left_width + 2 + cell_width * self.width

        xbar_segment = self.chars.line_hori * (cell_width // 2 - 1)
        xbar_segment += self.chars.line_cross
        xbar_segment += self.chars.line_hori * (cell_width - len(xbar_segment))

        def _xbar(corner1, corner2):
            line = " " * (left_key_width + 1) + corner1 + self.chars.line_hori
            line += xbar_segment * self.width
            line += self.chars.line_hori + corner2
            if annot_lines:
                line += " " + annot_lines.pop(-1)
            print(clip_line(line, max_width), file=file)

        _xbar(self.chars.line_corners[1], self.chars.line_corners[2])

        for y in range(self.height, 0, -1):
            y -= 1
            for i in range(cell_height):
                if i != cell_height // 2:
                    line = " " * (left_key_width + 1) + self.chars.line_vert + " "
                else:
                    line = f"{self.keys_str[1][y]:{left_key_width}} {self.chars.line_cross} "
                for row in self.values_str:
                    line += row[y] * cell_width
                if i != cell_height // 2:
                    line += " " + self.chars.line_vert
                else:
                    line += " " + self.chars.line_cross

                if annot_lines:
                    line += " " + annot_lines.pop(-1)

                print(clip_line(line, max_width), file=file)

        _xbar(self.chars.line_corners[0], self.chars.line_corners[3])

        x_labels = self._xlabels(left_width, cell_width, bottom_key_width, max_axis_lines)
        if x_labels:
            for row in x_labels:
                line = "".join(row)
                if annot_lines and len(line) <= right_end:
                    line += " " * (right_end - len(line))
                    line += " " + annot_lines.pop(-1)
                print(clip_line(line, max_width), file=file)
        else:
            # print x-labels vertically
            for y in range(bottom_key_width):
                line = " " * left_width
                for x in range(self.width):
                    seg = " " * (cell_width // 2 - 1)
                    seg += self.keys_str[0][x][y] if y < len(self.keys_str[0][x]) else " "
                    seg += " " * (cell_width - len(seg))
                    line += seg

                print(clip_line(line, max_width), file=file)

    def _xlabels(self, left_width: int, cell_width: int, max_key_width: int, max_axis_lines: int):
        for num_rows in range(1, max_axis_lines + 1):
            rows = self._xlabels_rows(num_rows, left_width, cell_width, max_key_width)
            if rows:
                return rows

    def _xlabels_rows(self, num_rows: int, left_width: int, cell_width: int, max_key_width: int):
        rows = [
            [" "] * (left_width + cell_width + max_key_width)
            for i in range(num_rows)
        ]
        for i, key in enumerate(self.keys_str[0]):
            tick_x = left_width + i * cell_width + max(0, cell_width // 2 - 1)
            start_x = tick_x - max(0, int(len(key) / 2 - .5))
            row = rows[i % len(rows)]
            for x, c in enumerate(key):
                x += start_x
                if x > 0:
                    if x >= len(row):
                        row.extend([" "] * (x + 1 - len(row)))
                    if row[x] != " " or (x == start_x and x > 0 and row[x-1] != " "):
                        return None
                    row[x] = c

        return rows

    def _annotation_lines(self, digits: int = None):
        lines = []
        for i, ch in enumerate(self.scale.characters):
            if self.min_v == self.max_v:
                value = self.min_v
            else:
                t = i / max(1, len(self.scale.characters) - 1)
                value = t * (self.max_v - self.min_v) + self.min_v

            if digits is not None:
                value = round(value, digits)

            line = f"{ch}{ch} {value}"
            lines.append(line)
        return lines

"""
     x1 x2
   /-+--+-
   |
y2 + ▒▒▒▒
y1 + ▒▒▒▒
   \-+-+-
     k k
     e e
     y y
     1 2
"""