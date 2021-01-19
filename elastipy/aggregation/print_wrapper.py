import json
from typing import Optional, List, Iterable, Union, Tuple, TextIO, Sequence, Mapping

from .aggregation import Aggregation
from .visitor import Visitor


class PrintWrapper:

    def __init__(self, agg: Aggregation):
        self._agg = agg

    def dict(self, key_separator="|", default=None, indent=2, file=None):
        print(json.dumps(self._agg.to_dict(key_separator=key_separator, default=default), indent=indent), file=file)

    def table(
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
            file=None
    ):
        """
        Print the result of the dict_rows() function as table to console.
        :param sort: str
            optional sort column name which must match a 'header' key.
            can be prefixed with '-' to reverse order
        :param digits: int, optional number of digits for rounding
        :param header: bool, if True, include the names in the first row
        :param bars: bool
            Enable display of horizontal bars in each number column.
            The table width will stretch out in size while limited
            to 'max_width' and 'max_bar_width'
        :param zero:
                If True: the bar axis starts at zero (or at a negative value if appropriate)
                If False: the bar starts at the minimum of all values in the column
                If a number is provides, the bar starts there, regardless of the minimum of all values
        :param colors: bool, enable console colors
        :param ascii: bool, if True fall back to ascii characters
        :param max_width: int
            Will limit the expansion of the table when bars are enabled.
            If left None, the terminal width is used.
        :param max_bar_width: int
            The maximum size a bar should have
        :param file: optional text stream to print to
        """
        from ..plot.text import Table
        Table(self._agg).print(
            sort=sort,
            digits=digits,
            header=header,
            bars=bars,
            zero=zero,
            colors=colors,
            ascii=ascii,
            max_width=max_width,
            max_bar_width=max_bar_width,
            file=file,
        )
