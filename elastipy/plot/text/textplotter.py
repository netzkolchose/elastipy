import os

from .characters import UnicodeCharacters


class TextPlotter:

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
            width, _ = os.get_terminal_size()

        left_width = key_len + value_len + 6
        bar_width = max(1, width - left_width)

        axis_ticks, axis_values = self._render_x_axis(
            0. if zero_based else values_min,
            values_max,
            bar_width,
            digits=digits,
        )
        print((" " * left_width) + axis_values)
        print((" " * left_width) + axis_ticks)
        for key, value, value_str in zip(keys, values, values_str):
            if zero_based:
                bar_value = value * value_fac
            else:
                bar_value = (value - values_min) * value_fac
            bar = UnicodeCharacters.hbar(bar_value, bar_width)
            print(f"{key:{key_len}} | {value_str} | {bar}", file=file)

    def get_terminal_size(self):
        size = os.get_terminal_size()
        return size.columns, size.lines

    def _render_x_axis(self, min_value, max_value, width, digits=3):
        distance = max_value - min_value
        if not distance:
            return (
                UnicodeCharacters.line_cross + UnicodeCharacters.line_hori * (width - 1),
                str(round(min_value, digits)),
            )

        factor = digits + 3
        while factor < width:
            ticks = UnicodeCharacters.line_hori * width
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
                    ticks = ticks[:i] + UnicodeCharacters.line_cross + ticks[i+1:]

            if values:
                return ticks, values


