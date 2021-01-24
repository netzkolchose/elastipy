from typing import Sequence, TextIO

from .console import ColorScale, Characters, get_terminal_size


class Heatmap:

    def __init__(
            self,
            keys: Sequence[str],
            values: Sequence[Sequence[float]],
            colors: bool = True,
            ascii: bool = False,
    ):
        self.keys = keys
        self.values = values
        self.width = len(self.keys[0])
        self.height = len(self.keys[1])
        self.scale = ColorScale(colors=colors, ascii=ascii)
        self.chars = Characters(ascii=ascii)

        if self.values:
            min_v = min(min(row) for row in self.values)
            max_v = max(max(row) for row in self.values)
            fac = 0.
            if min_v != max_v:
                fac = 1. / (max_v - min_v)

            self.value_chars = [
                [
                    self.scale((x - min_v) * fac)
                    for x in row
                ]
                for row in self.values
            ]

    def print(
            self,
            cell_width: int = None,
            cell_height: int = None,
            max_width: int = None,
            max_cell_width: int = 10,
            file: TextIO = None,
    ):
        if max_width is None:
            max_width, _ = get_terminal_size()

        if not self.keys or not self.values:
            return

        # -- space we need --

        left_key_width = max(len(key) for key in self.keys[1])
        left_width = left_key_width + 3

        if cell_width is None:
            cell_width = (max_width - left_width) // self.width
            cell_width = min(cell_width, max_cell_width)
        if cell_height is None:
            cell_height = max(1, cell_width // 2)

        xbar = " " * (left_key_width + 1) + self.chars.line_corners[1] + self.chars.line_hori
        xbar += (self.chars.line_cross + self.chars.line_hori * (cell_width - 1)) * self.width
        print(xbar, file=file)

        for y in range(self.height, 0, -1):
            y -= 1
            for i in range(cell_height):
                if i < cell_height - 1:
                    line = " " * (left_key_width + 1) + self.chars.line_vert + " "
                else:
                    line = f"{self.keys[1][y]:{left_key_width}} {self.chars.line_cross} "
                for x in self.value_chars[y]:
                    line += x * cell_width
                print(line, file=file)

        xbar = xbar[:left_key_width+1] + self.chars.line_corners[0] + xbar[left_key_width+2:]
        print(xbar, file=file)




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