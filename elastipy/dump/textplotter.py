import os

from .console import Characters, Colors, get_terminal_size


class TextPlotter:

    def __init__(self, ascii=False, colors=True):
        self.ch = Characters(ascii=ascii)
        self.co = Colors(enable=colors)

    def hbar(self, keys, values, width=None, zero_based=True, digits=3, file=None):
        values_str = [str(round(v, digits)) for v in values]

        key_len = max(len(key) for key in keys)
        value_len = max(len(v) for v in values_str)

        values_min, values_max = min(*values), max(*values)
        if values_min == values_max:
            value_fac = 0.
        else:
            if zero_based:
                value_fac = 1. / values_max
            else:
                value_fac = 1. / (values_max - values_min)

        if width is None:
            width, _ = get_terminal_size()

        left_width = key_len + value_len + 6
        bar_width = max(1, width - left_width)

        axis_ticks, axis_values = self._render_x_axis(
            0. if zero_based else values_min,
            values_max,
            bar_width,
            digits=digits,
        )

        print((" " * left_width) + axis_values, file=file)
        print((" " * (left_width - 2)) + self.ch.line_corners[1] + self.ch.line_hori + axis_ticks, file=file)

        for key, value, value_str in zip(keys, values, values_str):
            if zero_based:
                bar_value = value * value_fac
            else:
                bar_value = (value - values_min) * value_fac
            bar = self.co.LIGHT_BLUE + self.ch.hbar(bar_value, bar_width) + self.co.END
            print(f"{key:{key_len}} | {value_str:{value_len}} {self.ch.line_cross} {bar}", file=file)

        print((" " * (left_width - 2)) + self.ch.line_corners[0] + self.ch.line_hori + axis_ticks, file=file)
        print((" " * left_width) + axis_values, file=file)

    def _render_x_axis(self, min_value, max_value, width, digits=3):
        distance = max_value - min_value
        if not distance:
            return (
                self.ch.line_cross + self.ch.line_hori * (width - 1),
                str(round(min_value, digits)),
            )

        factor = digits + 3
        while factor < width:
            ticks = self.ch.line_hori * width
            values = " " * width

            for i in range(0, width, factor):
                x = (i / width - min_value) * (max_value - min_value)
                x_str = str(round(x, digits))
                if len(x_str) >= factor:
                    factor += 1
                    values = None
                    break
                if i + len(x_str) < width:
                    values = values[:i] + x_str + values[i+len(x_str):]
                    ticks = ticks[:i] + self.ch.line_cross + ticks[i + 1:]

            if values:
                return ticks, values


