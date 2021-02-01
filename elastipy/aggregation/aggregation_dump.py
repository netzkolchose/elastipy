import json
from typing import Optional, Union, TextIO, Sequence, Any

from .aggregation import Aggregation


class AggregationDump:

    def __init__(self, agg: Aggregation):
        self._agg = agg

    def dict(
            self,
            key_separator: str = "|",
            default: Any = None,
            indent: int = 2,
            file: Optional[TextIO] = None
    ):
        """
        Print the result of ``Aggregation.to_dict`` to console.

        :param key_separator: ``str``
            Separator to concat multiple keys into one string.
            Defaults to ``|``

        :param default: If not None any None-value will be replaced by this.
        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        """
        print(json.dumps(self._agg.to_dict(key_separator=key_separator, default=default), indent=indent), file=file)

    def table(
            self,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
            flat: Union[bool, str, Sequence[str]] = False,
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
        Print the result of the ``Aggregation.dict_rows()`` function as table to console.

        :param include: ``str`` or ``sequence of str``
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that does not fit a pattern is removed.

        :param exclude: ``str`` or ``sequence of str``
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that fits a pattern is removed.

        :param flat: ``bool``, ``str`` or ``sequence of str``
            Can be one or more aggregation names that should be *flattened out*,
            meaning that each key of the aggregation creates a new column
            instead of a new row. If ``True``, all bucket aggregations are
            *flattened*.

            Only supported for bucket aggregations!

            .. NOTE::
                Currently not supported for the root aggregation!

        :param sort: ``str``
            Optional sort column name which must match a 'header' key.
            Can be prefixed with ``-`` (minus) to reverse order

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
        from elastipy.dump import Table

        rows = self._agg.dict_rows(
            include=include,
            exclude=exclude,
            flat=flat,
        )

        Table(list(rows)).print(
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
        """
        Print a representation of ``Aggregation.to_matrix()`` to console.

        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        :param kwargs: TODO: list additional to_matrix parameters
        """
        indent = " " * indent
        names, keys, matrix = self._agg.to_matrix(**kwargs)
        print("names =", names, file=file)

        print("keys = [", file=file)
        for k in keys:
            print(indent, k, file=file)
        print("]", file=file)

        # TODO: print with recursive indentation
        print("matrix = [", file=file)
        for m in matrix:
            print(indent, m, file=file)

        print("]", file=file)

    def heatmap(
            self,
            sort: Optional[Union[bool, str, int, Sequence[Union[str, int]]]] = None,
            default: Optional[Any] = None,
            include: Optional[Union[str, Sequence[str]]] = None,
            exclude: Optional[Union[str, Sequence[str]]] = None,
            colors: bool = True,
            ascii: bool = False,
            **kwargs
    ):
        """
        Prints a heat-map from a two-dimensional matrix.

        :param sort:
            Can sort one or several keys/axises.

                - ``True`` sorts all keys ascending
                - ``"-"`` sorts all keys descending
                - The **name of an aggregation** sorts it's keys ascending.
                  A "-" prefix sorts descending.
                - An **integer** defines the aggregation by index.
                  Negative integers sort descending.
                - A **sequence** of strings or integers can sort multiple keys

            For example, `agg.heatmap(sort=("color", "-shape", -4))` would
            sort the ``color`` keys ascending, the ``shape`` keys descending and the
            4th aggregation *-whatever that is-* descending.

        :param default:
            If not None any None-value will be replaced by this value

        :param include: ``str | seq[str]``
            One or more wildcard patterns that include matching keys.
            All other keys are removed from the output.

        :param exclude: ``str | seq[str]``
            One or more wildcard patterns that exclude matching keys.

        :param colors: ``bool``
            Enable console colors.

        :param ascii: ``bool``
            If ``True`` fall back to ascii characters.

        :param max_width: ``int``
            Will limit the expansion of the table when bars are enabled.
            If left None, the terminal width is used.

        :param file:
            Optional text stream to print to.

        :param kwargs: TODO list all Heatmap parameters
        """
        from elastipy.dump import Heatmap
        names, keys, matrix = self._agg.to_matrix(
            sort=sort,
            default=default,
            include=include,
            exclude=exclude
        )
        if len(keys) != 2:
            raise ValueError(
                f"Can not display matrix of dimension {len(keys)} with heatmap, 2 dimensions required"
            )

        hm = Heatmap(
            keys=keys,
            values=matrix,
            colors=colors,
            ascii=ascii
        )
        hm.print(**kwargs)

    def hbar(
            self,
            width: int = None,
            zero_based: bool = True,
            digits: int = 3,
            ascii: bool = False,
            colors: bool = True,
            file: TextIO = None
    ):
        """
        Print a horizontal bar graphic based on
        ``Aggregation.keys()`` and ``values()`` to console.

        :param width: ``int``
            Maximum width to use. Will be auto-detected if ``None``.

        :param zero_based: ``bool``
            If ``True`` start at bars at tero, instead of global minimum

        :param digits: ``int``
            Optional number of digits for rounding.

        :param colors: ``bool``
            Enable console colors.

        :param ascii: ``bool``
            If ``True`` fall back to ascii characters.

        :param file:
            Optional text stream to print to.
        """
        from elastipy.dump import TextPlotter
        keys = list(self._agg.keys(key_separator="|"))
        values = list(self._agg.values())
        TextPlotter(ascii=ascii, colors=colors).hbar(
            keys=keys,
            values=values,
            width=width,
            zero_based=zero_based,
            digits=digits,
            file=file,
        )
