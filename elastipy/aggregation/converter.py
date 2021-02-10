from copy import copy, deepcopy
from itertools import chain
import fnmatch
from typing import Sequence, Union, Optional, Iterable, Tuple, TextIO, Any, Mapping, List

from .helper import dict_rows_to_list_rows, create_matrix, remove_matrix_axis


class ConverterMixin:
    """
    Interface that uses Visitor(self) to
    convert the aggregation keys and values into various objects.

    Must be bound into an Aggregation or compatible class
    to work properly. Especially:

        - must be compatible for Visitor(self)
        - needs access to self.root.name
    """

    def keys(
            self,
            key_separator: Optional[str] = None,
            tuple_key: bool = False,
    ):
        """
        Iterates through all keys of this aggregation.

        For example, a top-level terms aggregation would return all bucketed field values.

        For a nested bucket aggregation each key is a tuple of all parent keys as well.

        :param key_separator: ``str``
            Optional separator to concat multiple keys into one string

        :param tuple_key: ``bool``
            If True, the key is always a tuple
            If False, the key is a string if there is only one key

        :return: generator
        """
        for key, value in self.items(key_separator=key_separator, tuple_key=tuple_key):
            yield key

    def values(self, default=None):
        """
        Iterates through all values of this aggregation.

        :param default: If not None any None-value will be replaced by this.
        :return: generator
        """
        for key, value in self.items(default=default):
            yield value

    def items(
            self,
            key_separator: str = None,
            tuple_key: bool = False,
            default=None,
    ) -> Iterable[Tuple]:
        """
        Iterates through all key, value tuples.

        :param key_separator: ``str``
            Optional separator to concat multiple keys into one string.

        :param tuple_key: ``bool``
            If True, the key is always a tuple.

            If False, the key is a string if there is only one key.

        :param default:
            If not None any None-value will be replaced by this.

        :return: generator
        """
        from .visitor import Visitor
        v = Visitor(self, default_value=default, key_separator=key_separator, tuple_key=tuple_key)
        yield from v.items()

    def rows(
            self,
            header: bool = True,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
            flat: Union[bool, str, Sequence[str]] = False,
            default = None,
    ) -> Iterable[list]:
        """
        Iterates through all result values from this aggregation branch.

        Each row is a list. The first row contains the names if 'header' == True.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics).

        :param header: ``bool``
            If True, the first row contains the names of the columns

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

        :param default:
            This value will be used wherever a value is undefined.

        :return: generator of list
        """
        yield from dict_rows_to_list_rows(
            self.dict_rows(include=include, exclude=exclude, flat=flat),
            header=header,
            default=default,
        )

    def dict_rows(
            self,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
            flat: Union[bool, str, Sequence[str]] = False,
    ) -> Iterable[dict]:
        """
        Iterates through all result values from this aggregation branch.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics and pipelines).

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

        :return: generator of dict
        """
        from .visitor import Visitor
        return Visitor(self).dict_rows(include=include, exclude=exclude, flat=flat)

    def to_dict(self, key_separator=None, default=None) -> dict:
        """
        Create a dictionary from all key/value pairs.

        :param key_separator: str, optional separator to concat multiple keys into one string
        :param default: If not None any None-value will be replaced by this.
        :return: dict
        """
        return {
            key: value
            for key, value in self.items(key_separator=key_separator, default=default)
        }

    def to_pandas(
            self,
            index: Union[bool, str] = False,
            to_index: Union[bool, str] = False,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
            flat: Union[bool, str, Sequence[str]] = False,
            dtype=None,
            default=None,
    ):
        """
        Converts the results of ``dict_rows()`` to a pandas DataFrame.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics).

        Any columns containing dates will be automatically converted to pandas.Timestamp.

        This method has a synonym: ``df``

        :param index: ``bool`` or ``str``
            Sets a specific column as the index of the DataFrame.

                - If ``False`` no explicit index is set.
                - If ``True`` the root aggregation's keys will be the index.
                - if ``str`` explicitly set a certain column as the DataFrame index.

            .. NOTE::

                The column is kept in the DataFrame. If you wan't to set a
                column as index and remove it from the columns, use ``to_index``.

        :param to_index: ``bool`` or ``str``
            Same as ``index`` but the column is removed from DataFrame.

                - If ``False`` no explicit index is set.
                - If ``True`` the root aggregation's keys will be the index.
                - if ``str`` explicitly set a certain column as the DataFrame index.

        :param include: ``str or list of str``
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that does not fit a pattern is removed

        :param exclude: ``str or list of str``
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that fits a pattern is removed

        :param flat: ``bool``, ``str`` or ``sequence of str``
            Can be one or more aggregation names that should be *flattened out*,
            meaning that each key of the aggregation creates a new column
            instead of a new row. If ``True``, all bucket aggregations are
            *flattened*.

            Only supported for bucket aggregations!

            .. NOTE::
                Currently not supported for the root aggregation!

        :param dtype:
            Numpy data type to force. Only a single dtype is allowed. If None, infer.

        :param default:
            This value will be used wherever a value is undefined.

        :return: pandas ``DataFrame`` instance
        """
        import pandas as pd
        from pandas._libs.tslibs import OutOfBoundsDatetime
        import numpy as np
        from dateutil.parser import ParserError

        if index and to_index:
            raise ValueError(
                "Can not use 'index' and 'to_index' together, settle for one please."
            )

        rows = list(dict_rows_to_list_rows(
            self.dict_rows(include=include, exclude=exclude, flat=flat),
            default=default,
            header=True,
        ))

        if rows:
            df = pd.DataFrame(rows[1:], columns=rows[0], dtype=dtype)
        else:
            df = pd.DataFrame(dtype=dtype)

        for key in df:
            if df[key].dtype == np.dtype("O"):
                try:
                    df[key] = pd.to_datetime(df[key], format="%Y-%m-%dT%H:%M:%S.%fZ")
                except (ValueError, TypeError, ParserError, OutOfBoundsDatetime):
                    pass

        index = index or to_index

        if index and len(df):
            if index is True:
                index = self.root.name

            df.index = df[index]

            if to_index:
                df.pop(index)

        return df

    # synonym
    df = to_pandas

    def to_matrix(
            self,
            sort: Optional[Union[bool, str, int, Sequence[Union[str, int]]]] = None,
            default: Optional[Any] = None,
            include: Optional[Union[str, Sequence[str]]] = None,
            exclude: Optional[Union[str, Sequence[str]]] = None,
    ) -> Tuple[List[str], List, List]:
        """
        Generate an N-dimensional matrix from the values of this aggregation.

        Each dimension corresponds to one of the parent bucket keys that lead
        to this aggregation.

        The values are gathered through the :link:`Aggregation.items` method.
        So the matrix values are either the ``doc_count`` of the bucket
        aggregation or the result of a ``metric`` or ``pipeline`` aggregation
        that is inside one of the bucket aggregations.

        .. CODE::

            a = Search().agg_terms("color", field="color")
            a = a.agg_terms("shape", field="shape")
            ...
            names, keys, matrix = a.to_matrix()
            names == ["color", "shape"]
            keys == [["red", "green", "blue"], ["circle", "triangle"]]
            matrix == [[23, 42], [84, 69], [4, 10]]

        :param sort:
            Can sort one or several keys/axises.

                - ``True`` sorts all keys ascending
                - ``"-"`` sorts all keys descending
                - The **name of an aggregation** sorts it's keys ascending.
                  A "-" prefix sorts descending.
                - An **integer** defines the aggregation by index.
                  Negative integers sort descending.
                - A **sequence** of strings or integers can sort multiple keys

            For example, `agg.to_matrix(sort=("color", "-shape", -4))` would
            sort the ``color`` keys ascending, the ``shape`` keys descending and the
            4th aggregation *-whatever that is-* descending.

        :param default:
            If not None any None-value will be replaced by this value

        :param include: ``str | seq[str]``
            One or more wildcard patterns that include matching keys.
            All other keys are removed from the output.

        :param exclude: ``str | seq[str]``
            One or more wildcard patterns that exclude matching keys.

        :return:
            A tuple of **names**, **keys** and **matrix data**, each as list.

            The **names** are the names of each aggregation that generates keys.

            The **keys** are a list of lists, each corresponding to all the keys
            of each parent aggregation.

            **Data** is a list, with other nested lists for each further dimension,
            containing the values of this aggregation.

            Returns three empty lists if no data is available.
        """
        from .visitor import Visitor
        names = Visitor(self).key_names()

        if isinstance(include, str):
            include = [include]
        if isinstance(exclude, str):
            exclude = [exclude]

        data_items = list(self.items(tuple_key=True, default=default))
        if not data_items:
            return [], [], []

        data_keys, data_values = zip(*data_items)

        num_dim = len(data_keys[0])

        # collect keys for each dimension in the order of appearance
        keys = [[] for _ in range(num_dim)]
        for key in data_keys:
            for i, k in enumerate(key):
                if k not in keys[i]:
                    keys[i].append(k)

        if sort:
            if sort is True:
                names_to_sort = names
            elif isinstance(sort, str):
                if sort == "-":
                    names_to_sort = [f"-{n}" for n in names]
                else:
                    names_to_sort = [sort]
            elif isinstance(sort, Iterable):
                names_to_sort = sort
            else:
                raise TypeError(f"Invalid type {type(sort).__name__} for sort")

            for n in reversed(names_to_sort):
                if isinstance(n, str):
                    n, reverse = n.lstrip("-"), n.startswith("-")
                    try:
                        idx = names.index(n)
                    except IndexError:
                        raise IndexError(
                            f"Column '{n}' not found, available: {', '.join(names)}"
                        )
                else:
                    idx, reverse = abs(n), n < 0
                keys[idx].sort(reverse=reverse)

        matrix = create_matrix(*(len(k) for k in keys), scalar=default)

        for key, value in zip(data_keys, data_values):
            m = matrix
            for i in range(num_dim):
                idx = keys[i].index(key[i])
                if i == num_dim - 1:
                    m[idx] = value
                else:
                    m = m[idx]

        if include or exclude:
            repeat = True
            while repeat:
                repeat = False
                for dim, dim_keys in enumerate(keys):
                    for i, key in enumerate(dim_keys):
                        if not is_key_match(key, include, exclude):
                            dim_keys.pop(i)
                            remove_matrix_axis(matrix, dim, i)
                            repeat = True
                            break
                    if repeat:
                        break

        return names, keys, matrix

    def df_matrix(
            self,
            sort: Optional[Union[bool, str, int, Sequence[Union[str, int]]]] = None,
            default: Optional[Any] = None,
            include: Optional[Union[str, Sequence[str]]] = None,
            exclude: Optional[Union[str, Sequence[str]]] = None,
    ):
        """
        Returns a pandas DataFrame containing the matrix.

        See `to_matrix` for details.

        Only one- and two-dimensional matrices are supported.

        :return:
            pandas.DataFrame instance
        :raises ValueError: If dimensions is 0 or above 2
        """
        import pandas as pd

        names, keys, matrix = self.to_matrix(
            sort=sort,
            default=default,
            include=include,
            exclude=exclude,
        )
        if len(keys) == 1:
            df = pd.DataFrame(matrix, index=keys[0])
        elif len(keys) == 2:
            df = pd.DataFrame(matrix, index=keys[0], columns=keys[1])
        else:
            raise ValueError(
                f"Can not convert matrix of dimension {len(keys)} to pandas DataFrame"
            )

        return df


def is_key_match(key: str, include: Optional[Sequence], exclude: Optional[Sequence]):
    if not include and not exclude:
        return True

    key = str(key)

    if exclude:
        for pattern in exclude:
            if fnmatch.fnmatch(key, pattern):
                return False

    if include:
        for pattern in include:
            if fnmatch.fnmatch(key, pattern):
                return True
        return False

    return True
