from copy import copy, deepcopy
from itertools import chain
from typing import Sequence, Union, Optional, Iterable, Tuple, TextIO, Any, Mapping, List

from .helper import dict_rows_to_list_rows, wildcard_match, create_matrix


class ConverterMixin:
    """
    Interface that uses keys(), values() and dict_rows() iterators to
    convert into various objects.
    """

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

    def to_matrix(self) -> Tuple[List, List]:
        """
        Generate a N-dimensional matrix from the values of this aggregation.

        Each dimension corresponds to one of the parent bucket keys that lead
        to this aggregation.

        :return:
            A tuple of keys and matrix data, both as list.

            The keys are a list of lists, each corresponding to all the keys
            of each parent aggregation.

            Data is a list, with other nested lists for each further dimension,
            containing the values of this aggregation.

            Returns two empty lists if no data is available.
        """
        data_keys = list(self.keys())
        data_values = list(self.values())
        if not data_keys:
            return [], []

        if not isinstance(data_keys[0], tuple):
            data_keys = [(k, ) for k in data_keys]

        num_dim = len(data_keys[0])

        keys = [[] for _ in range(num_dim)]
        for key in data_keys:
            for i, k in enumerate(key):
                if k not in keys[i]:
                    keys[i].append(k)

        matrix = create_matrix(*(len(k) for k in keys))

        for key, value in zip(data_keys, data_values):
            m = matrix
            for i in range(num_dim):
                idx = keys[i].index(key[i])
                if i == num_dim - 1:
                    m[idx] = value
                else:
                    m = m[idx]

        return keys, matrix

    def df_matrix(self):
        """
        Returns a pandas DataFrame containing the matrix.

        See `to_matrix` for details.

        Only one- and two-dimensional matrices are supported.

        :return:
            pandas.DataFrame instance
        """
        import pandas as pd

        keys, matrix = self.to_matrix()
        if len(keys) == 1:
            df = pd.DataFrame(matrix, index=keys[0])
        elif len(keys) == 2:
            df = pd.DataFrame(matrix, index=keys[0], columns=keys[1])
        else:
            raise ValueError(
                f"Can not convert matrix of dimension {len(keys)} to pandas DataFrame"
            )

        return df
