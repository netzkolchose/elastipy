import math
from itertools import chain
from typing import Mapping, Sequence, Union
from io import StringIO
from collections import deque

try:
    import pandas as pd
except ImportError:
    pd = None

from .console import Characters, Colors, get_terminal_size, clip_line
from .helper import get_number


class Table:

    def __init__(self, source):
        self.source = source
        self.rows = []
        self.headers = []
        self._extract_source()

    def print(
            self,
            sort: Union[str, int] = None,
            digits: int = None,
            header: bool = True,
            bars: bool = True,
            zero: Union[bool, float] = True,
            colors: bool = True,
            ascii: bool = False,
            max_width: int = None,
            max_bar_width: int = 40,
            file=None
    ):
        """
        :param sort: ``str`` or ``int``
            Optional sort column name which must match a 'header' key.
            Can be prefixed with ``-`` (minus) to reverse order.

            Numbers are also accepted, which sort the ``x``th header.
            Negative to reverse the order.

        :param digits: ``int``
            Optional number of digits for rounding.

        :param header: ``bool``
            if True, include the names in the first row.

        :param bars: ``bool``
            Enable display of horizontal bars in each number column.
            The table width will stretch out in size while limited
            to 'max_width' and 'max_bar_width'

        :param zero:
            - If ``True``: the bar axis starts at zero
              (or at a negative value if appropriate).
            - If ``False``: the bar starts at the minimum of all values in the column.
            - If a **number** is provided, the bar starts there,
              regardless of the minimum of all values.

        :param colors: ``bool``
            Enable console colors.

        :param ascii: ``bool``
            If ``True`` fall back to ascii characters.

        :param max_width: ``int``
            Will limit the expansion of the table when bars are enabled.
            If left None, the terminal width is used.

        :param max_bar_width: ``int``
            The maximum size a bar should have

        :param file:
            Optional text stream to print to.
        """
        def _to_str(v):
            if v is None:
                return "-"

            try:
                if math.isnan(v):
                    return "-"
            except TypeError:
                pass

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
                if number is not None:
                    table_row[key]["value"] = number
                    if key not in value_bounds:
                        value_bounds[key] = {"min": number, "max": number}
                    else:
                        value_bounds[key]["min"] = min(value_bounds[key]["min"], number)
                        value_bounds[key]["max"] = max(value_bounds[key]["max"], number)

            table_rows.append(table_row)

        if sort is not None:
            if isinstance(sort, int):
                if not 0 <= abs(sort) < len(self.headers):
                    raise ValueError(
                        f"Sort column {abs(sort)} is out of range, use [0-{len(self.headers)-1}]"
                    )
                reverse = sort < 0
                sort_key = self.headers[abs(sort)]
            else:
                reverse = sort.startswith("-")
                sort_key = sort.lstrip("-")

            table_rows = sorted_rows(table_rows, key=sort_key, reverse=reverse)

        for key, bound in list(value_bounds.items()):
            if bound["min"] != bound["max"]:
                pass
            else:
                value_bounds.pop(key)

        if zero is True:
            for bound in value_bounds.values():
                bound["min"] = min(0, bound["min"])
        elif zero is False:
            pass  # keep the calculated lower bound
        else:
            for bound in value_bounds.values():
                bound["min"] = zero

        # width of whole column
        column_width = {
            key: max(header_width[key], value_width.get(key, 0))
            for key in self.headers
        }

        # -- determine additional space for bars --

        bar_offset = 0.
        if bars and value_bounds:
            if max_width is None:
                max_width, _ = get_terminal_size()

            needed_width = sum(column_width.values()) + (len(column_width) - 1) * 3
            free_width = max_width - needed_width

            # initial width for bars (because there might be a long header)
            bar_width = {
                key: column_width[key] - value_width[key]
                for key in value_bounds
            }

            self._spend_extra_width(bar_width, free_width, max_bar_width)

            # final column width
            for key in bar_width:
                column_width[key] = max(
                    column_width[key],
                    value_width[key] + bar_width[key]
                )

            if bar_width:
                bar_width_max = max(bar_width.values())
                bar_offset = max(0.01, min(.25, 1. / bar_width_max))

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
                    cell = f"{value:{value_width.get(key, 1)}}"

                if y != 0 and bar_width.get(key, 0) > 1:
                    try:
                        value = get_number(row[key]["value"])
                        mi, ma = value_bounds[key]["min"], value_bounds[key]["max"]
                        t = bar_offset + (1. - bar_offset) * (value - mi) / (ma - mi)
                        cell += " " + co.LIGHT_BLUE + ch.hbar(t, bar_width[key] - 1) + co.END
                    except TypeError:
                        pass

                cell += " " * (column_width[key] - len(cell))
                cells.append(cell)

            line = f" {ch.line_vert} ".join(cells)
            line = clip_line(line, max_width)

            print(line, file=file)

            if y == 0:
                line = (ch.line_hori + ch.line_cross + ch.line_hori).join(
                    ch.line_hori * column_width[key]
                    for key in self.headers
                )
                line = clip_line(line, max_width)

                print(line, file=file)

    def to_str(
            self,
            sort: str = None,
            digits: int = None,
            header: bool = True,
            bars: bool = True,
            zero: Union[bool, float] = True,
            colors: bool = True,
            ascii: bool = False,
            max_width: int = None,
            max_bar_width: int = 40,
    ):
        file = StringIO()
        self.print(
            sort=sort, digits=digits, header=header, bars=bars, colors=colors, ascii=ascii, max_width=max_width,
            zero=zero, max_bar_width=max_bar_width,
            file=file,
        )
        file.seek(0)
        return file.read()

    def _extract_source(self):
        self.headers = None

        source = self.source

        if pd is not None and isinstance(self.source, pd.DataFrame):
            source = self.source.values.tolist()
            source.insert(0, list(self.source.columns))

        try:
            try:
                first_row = source[0]
            except IndexError:
                self.rows = []
                self.headers = []
                return

            if isinstance(first_row, Sequence):
                self.headers = first_row
                self.rows = [
                    {
                        key: value
                        for key, value in zip(self.headers, row)
                    }
                    for row in source[1:]
                ]
            elif isinstance(first_row, Mapping):
                self.rows = self.source
                self.headers = all_dict_row_keys(self.rows)
            return
        except (TypeError, KeyError):
            pass

        if hasattr(self.source, "dict_rows"):
            self.rows = list(self.source.dict_rows())
            self.headers = all_dict_row_keys(self.rows)
            return

        raise TypeError(f"Invalid source '{type(self.source).__name__}' for Table")

    def _spend_extra_width(self, width: dict, extra_width: int, max_width: int = None, recursive=True):
        if not width:
            return
        cur_max_width = max(width.values())
        keys = deque(width.keys())
        count = extra_width
        while extra_width > 0 and count:
            count -= 1
            added = False

            # add to the ones that are below current max
            for key in width:
                if not extra_width:
                    break
                if width[key] < cur_max_width and (max_width is None or width[key] < max_width):
                    width[key] += 1
                    extra_width -= 1
                    added = True
            if not extra_width:
                break

            # add to columns in round-robin order
            if not added:
                if not keys:
                    keys = deque(width.keys())
                key = keys.pop()
                if max_width is None or width[key] < max_width:
                    width[key] += 1
                    cur_max_width = max(cur_max_width, width[key])
                    extra_width -= 1

        for key in list(width.keys()):
            if width[key] < 2:
                extra_width += width[key]
                width.pop(key)

        if recursive:
            self._spend_extra_width(width, extra_width, max_width, recursive=False)


def all_dict_row_keys(rows):
    keys = []
    for row in rows:
        for key in row.keys():
            if key not in keys:
                keys.append(key)
    return keys


def sorted_rows(rows, key: str, reverse: bool):
    try:
        return sorted(rows, key=lambda row: row[key]["value"], reverse=reverse)
    except TypeError:
        rows = [RowCompare(row, key) for row in rows]
        rows.sort(reverse=reverse)
        return [row.row for row in rows]


class RowCompare:

    def __init__(self, row, key):
        self.row = row
        self.key = key

    def __lt__(self, other):
        v1 = self.row[self.key]["value"]
        v2 = other.row[self.key]["value"]
        if v1 is None:
            return True
        if v2 is None:
            return False
        return v1 < v2
