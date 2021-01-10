import os
from itertools import chain
from typing import Mapping, Sequence
from io import StringIO
from decimal import Decimal, InvalidOperation

from .characters import Characters, Colors


class Table:

    def __init__(self, source):
        self.source = source
        self.rows = []
        self.headers = []
        self._extract_source()

    def to_str(self, digits=None, header=True, bars=True, colors=True, ascii=False, max_width=None):
        file = StringIO()
        self.print(digits=digits, header=header, bars=bars, colors=colors, ascii=ascii, max_width=max_width, file=file)
        file.seek(0)
        return file.read()

    def print(self, digits=None, header=True, bars=True, colors=True, ascii=False, max_width=None, file=None):
        def _to_str(v):
            if v is None:
                return "-"
            if digits is not None:
                try:
                    v = round(v, digits)
                except (TypeError, ValueError):
                    pass
            return str(v)

        co = Colors(enable=colors)
        ch = Characters(ascii=ascii)

        # width of header per column
        header_width = {key: len(key) if header else 0 for key in self.headers}
        # width of longest value per column
        value_width = dict()
        # min and max value per column (includes only columns which have non-zero bounds)
        value_bounds = dict()
        # width of each value-column's bar
        bar_width = dict()

        table_rows = []
        for row in self.rows:
            table_row = dict()
            for key in self.headers:
                value = row.get(key)
                value_str = _to_str(value)
                table_row[key] = {
                    "value": value,
                    "str": value_str,
                }
                value_width[key] = max(value_width.get(key, 0), len(value_str))

                number = get_number(value)
                if number:
                    table_row[key]["value"] = number
                    if key not in value_bounds:
                        value_bounds[key] = {"min": number, "max": number}
                    else:
                        value_bounds[key]["min"] = min(value_bounds[key]["min"], number)
                        value_bounds[key]["max"] = max(value_bounds[key]["max"], number)

            table_rows.append(table_row)

        for key, bound in list(value_bounds.items()):
            if bound["min"] != bound["max"]:
                pass
            else:
                value_bounds.pop(key)

        # width of whole column
        column_width = {
            key: max(header_width[key], value_width[key])
            for key in self.headers
        }

        # -- determine additional space for bars --

        bar_offset = 0.
        if bars and value_bounds:
            if max_width is None:
                max_width, _ = os.get_terminal_size()

            needed_width = sum(column_width.values()) + (len(column_width) - 1) * 3
            free_width = max_width - needed_width

            # initial width for bars (because there might be a long header)
            bar_width = {
                key: column_width[key] - value_width[key]
                for key in value_bounds
            }
            max_bar_width = max(bar_width.values())

            while free_width:
                for key in bar_width:
                    if not free_width:
                        break
                    if bar_width[key] < max_width:
                        bar_width[key] += 1
                        max_bar_width = max(max_bar_width, bar_width[key])
                        free_width -= 1

            # final column width
            for key in bar_width:
                column_width[key] = max(
                    column_width[key],
                    value_width[key] + bar_width[key]
                )

            bar_offset = max(0.01, min(.25, 1. / max_bar_width))

        # -- print the thing --

        table_header_row = {key: {"str": key} for key in self.headers}
        for y, row in enumerate(chain([table_header_row], table_rows)):
            if y == 0 and not header:
                continue

            cells = []
            for key in self.headers:
                value = row[key]["str"]

                if y != 0 and key in value_bounds:
                    cell = " " * (value_width[key] - len(value)) + value
                else:
                    cell = f"{value:{value_width[key]}}"

                if y != 0 and bar_width.get(key, 0) > 1:
                    try:
                        value = row[key]["value"]
                        mi, ma = value_bounds[key]["min"], value_bounds[key]["max"]
                        t = bar_offset + (1. - bar_offset) * (value - mi) / (ma - mi)
                        cell += " " + co.LIGHT_BLUE + ch.hbar(t, bar_width[key] - 1) + co.END
                    except TypeError:
                        pass

                cell += " " * (column_width[key] - len(cell))
                cells.append(cell)

            line = f" {ch.line_vert} ".join(cells)
            print(line, file=file)

            if y == 0:
                line = (ch.line_hori + ch.line_cross + ch.line_hori).join(
                    ch.line_hori * column_width[key]
                    for key in self.headers
                )
                print(line, file=file)

    def _extract_source(self):
        self.headers = None
        try:
            row = self.source[0]
            if isinstance(row, Sequence):
                self.headers = row
                self.rows = [
                    {
                        key: value
                        for key, value in zip(self.headers, row)
                    }
                    for row in self.source[1:]
                ]
            elif isinstance(row, Mapping):
                self.rows = self.source
                self.headers = all_dict_row_keys(self.rows)
            return
        except (TypeError, KeyError):
            pass

        if hasattr(self.source, "dict_rows"):
            self.rows = list(self.source.dict_rows())
            self.headers = all_dict_row_keys(self.rows)
            return

        raise TypeError(f"Invalid source {type(self.source).__name__}")


def all_dict_row_keys(rows):
    keys = []
    for row in rows:
        for key in row.keys():
            if key not in keys:
                keys.append(key)
    return keys


def get_number(value):
    try:
        v = int(value)
        if v == float(value):
            return v
    except (TypeError, ValueError):
        pass

    try:
        return float(value)
    except (TypeError, ValueError):
        pass
