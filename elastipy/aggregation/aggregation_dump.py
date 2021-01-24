import json
from typing import Optional, List, Iterable, Union, Tuple, TextIO, Sequence, Mapping, Any

from .aggregation import Aggregation
from .visitor import Visitor


class PrintWrapper:

    def __init__(self, agg: Aggregation):
        self._agg = agg

    def dict(
            self,
            key_separator: str = "|",
            default: Any = None,
            indent: int = 2,
            file: Optional[TextIO] = None
    ):
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
            file: Optional[TextIO] = None
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

    def matrix(self, indent: int = 2, file: TextIO = None, **kwargs):
        indent = " " * indent
        names, keys, matrix = self._agg.to_matrix(**kwargs)
        print("names =", names, file=file)

        print("keys = [", file=file)
        for k in keys:
            print(indent, k, file=file)
        print("]", file=file)

        print("matrix = [", file=file)
        for m in matrix:
            print(indent, m, file=file)

        print("]", file=file)

    def heatmap(
            self,
            colors: bool = True,
            ascii: bool = False,
            sort: Optional[Union[bool, str, int, Sequence[Union[str, int]]]] = None,
            default: Optional[Any] = None,
            drop: Optional[Union[str, Sequence[str]]] = None,
            **kwargs
    ):
        from ..plot.text import Heatmap
        names, keys, matrix = self._agg.to_matrix(sort=sort, default=default, drop=drop)
        if len(keys) != 2:
            raise ValueError(
                f"Can not display matrix of dimension {len(keys)} to heatmap, need 2 dimensions"
            )

        hm = Heatmap(
            keys=keys,
            values=matrix,
            colors=colors,
            ascii=ascii
        )
        hm.print(**kwargs)
