import json
from typing import Optional, List, Iterable, Union, Tuple, TextIO, Sequence, Mapping

from .aggregation import Aggregation
from .visitor import Visitor


class PrintWrapper:

    def __init__(self, agg: Aggregation):
        self.agg = agg

    def dict(self, key_separator="|", default=None, indent=2, file=None):
        print(json.dumps(self.agg.to_dict(key_separator=key_separator, default=default), indent=indent), file=file)

    def table(
            self,
            sort: str = None,
            header: bool = True,
            bars: bool = True,
            digits: int = None,
            zero_based: bool = False,
            file: TextIO = None
    ):
        """
        Print the result of the dict_rows() function as table to console.
        :param digits: int, optional number of digits for rounding
        :param header: bool, if True, include the names in the first row
        :param bars: bool, enable display of horizontal bars in each number column
        :param zero_based: bool, if True, the bar axis starts at zero,
            otherwise it starts at each columns minimum value
        :param file: optional text stream to print to
        """
        from ..plot.text import Table
        Table(self.agg).print(
            sort=sort,
            digits=digits,
            header=header,
            bars=bars,
            zero_based=zero_based,
            file=file,
        )
