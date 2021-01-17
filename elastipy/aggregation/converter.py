from copy import copy, deepcopy
from itertools import chain
from typing import Sequence, Union, Optional, Iterable, Tuple, TextIO, Any, Mapping, List

from .helper import dict_rows_to_list_rows, wildcard_match, create_matrix


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

        :param key_separator: str
            Optional separator to concat multiple keys into one string
        :param tuple_key: bool
            If True, the key is always a tuple
            If False, the key is a string if there is only one key

        :return: generator
        """
        for key, value in self.items(key_separator=key_separator, tuple_key=tuple_key):
            yield key

    def values(self, default=None):
        """
        Iterates through all values of this aggregation.
        :param default: if not None any None-value will be replaced by this
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
        :param key_separator: str, optional separator to concat multiple keys into one string
        :param tuple_key: bool
            If True, the key is always a tuple
            If False, the key is a string if there is only one key
        :param default: if not None any None-value will be replaced by this
        :return: generator
        """
        from .visitor import Visitor
        v = Visitor(self, default_value=default, key_separator=key_separator, tuple_key=tuple_key)
        yield from v.items()

    def rows(
            self,
            header=True,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
    ) -> Iterable[list]:
        """
        Iterates through all result values from this aggregation branch.

        Each row is a list. The first row contains the names if 'header' == True.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics).

        :param header: bool
            If True, the first row contains the names of the columns
        :param include: str or list of str
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that does not fit a pattern is removed
        :param exclude: str or list of str
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that fits a pattern is removed

        :return: generator of list
        """
        yield from dict_rows_to_list_rows(self.dict_rows(include=include, exclude=exclude), header=header)

    def dict_rows(
            self,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
    ) -> Iterable[dict]:
        """
        Iterates through all result values from this aggregation branch.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics).

        :param include: str or list of str
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that does not fit a pattern is removed
        :param exclude: str or list of str
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that fits a pattern is removed

        :return: generator of dict
        """
        from .visitor import Visitor
        return Visitor(self).dict_rows(include=include, exclude=exclude)

    def to_dict(self, key_separator=None, default=None) -> dict:
        """
        Create a dictionary from all key/value pairs.
        :param key_separator: str, optional separator to concat multiple keys into one string
        :param default: if not None any None-value will be replaced by this
        :return: dict
        """
        return {
            key: value
            for key, value in self.items(key_separator=key_separator, default=default)
        }

    def to_pandas(
            self,
            index: str = None,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
    ):
        """
        Converts the results of 'dict_rows()' to a pandas DataFrame.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics).

        Any columns containing dates will be automatically converted to pandas.Timestamp.

        This method has a synonym: 'df'

        :param index: str
            Can explicitly set a certain column as the DataFrame index.
            If omitted, the root aggregation's keys will be set to the index.
        :param include: str or list of str
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that does not fit a pattern is removed
        :param exclude: str or list of str
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that fits a pattern is removed

        :return: DataFrame instance
        """
        import pandas as pd
        from pandas._libs.tslibs import OutOfBoundsDatetime
        import numpy as np
        from dateutil.parser import ParserError

        df = pd.DataFrame(self.dict_rows(include=include, exclude=exclude))
        for key in df:
            if df[key].dtype == np.dtype("O"):
                try:
                    df[key] = pd.to_datetime(df[key])
                except (TypeError, ParserError, OutOfBoundsDatetime):
                    pass
        if index is None:
            index = self.root.name
        df.index = df.pop(index)
        return df

    # synonym
    df = to_pandas

    def to_matrix(
            self,
            sort: Optional[Union[bool, str, int, Sequence[Union[str, int]]]] = None,
            default: Optional[Any] = None,
    ) -> Tuple[List[str], List, List]:
        """
        Generate a N-dimensional matrix from the values of this aggregation.

        Each dimension corresponds to one of the parent bucket keys that lead
        to this aggregation.

        ```
        a = Search().agg_terms("color", field="color").agg_terms("shape", field="shape")
        ...
        names, keys, matrix = a.to_matrix()
        names == ["color", "shape"]
        keys == [["red", "green", "blue"], ["circle", "triangle"]]
        matrix = [[23, 42], [84, 69], [4, 10]]
        ```

        :param sort:
            Can sort one or several keys/axises.
                - `True` sorts all keys ascending
                - `"-"` sorts all keys descending
                - the name of an aggregation sorts it's keys ascending
                    - a "-" prefix sorts descending
                - an integer defines the aggregation by index
                    - negative integers sort descending
                - a sequence of strings or integers can sort multiple keys

            For example, `agg.to_matrix(sort=("color", "-shape", -4))` would
            sort the color keys ascending, the shape keys descending and the
            4th aggregation -whatever that is- descending.

        :param default:
            If not None any None-value will be replaced by this value

        :return:
            A tuple of names, keys and matrix data, each as list.

            The `names` are the names of each aggregation that generates keys.

            The `keys` are a list of lists, each corresponding to all the keys
            of each parent aggregation.

            `Data` is a list, with other nested lists for each further dimension,
            containing the values of this aggregation.

            Returns three empty lists if no data is available.
        """
        from .visitor import Visitor
        names = Visitor(self).key_names()

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

        return names, keys, matrix

    def df_matrix(
            self,
            sort: Optional[Union[bool, str, int, Sequence[Union[str, int]]]] = None,
            default: Optional[Any] = None,
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

        names, keys, matrix = self.to_matrix(sort=sort, default=default)
        if len(keys) == 1:
            df = pd.DataFrame(matrix, index=keys[0])
        elif len(keys) == 2:
            df = pd.DataFrame(matrix, index=keys[0], columns=keys[1])
        else:
            raise ValueError(
                f"Can not convert matrix of dimension {len(keys)} to pandas DataFrame"
            )

        return df
