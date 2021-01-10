import json
from typing import Optional, List, Iterable, Union, Tuple, TextIO, Sequence, Mapping

from .aggregation import Aggregation
from .visitor import Visitor


class PrintWrapper:

    def __init__(self, agg: Aggregation):
        self.agg = agg

    def dict(self, key_separator="|", default=None, indent=2, file=None):
        print(json.dumps(self.agg.to_dict(key_separator=key_separator, default=default), indent=indent), file=file)

    def table(self, header: bool = True, digits: Optional[int] = None, file: TextIO = None):
        """
        Print the result of the dict_rows() function as table to console.
        :param header: bool, if True, include the names in the first row
        :param digits: int, optional number of digits for rounding
        :param file: optional text stream to print to
        """
        from ..plot.text import Table
        Table(self.agg).print(
            digits=digits, header=header,
            file=file
        )
