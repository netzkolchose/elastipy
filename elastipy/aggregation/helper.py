import fnmatch
from typing import Sequence, Iterable, Mapping, List, Union, Optional


def wildcard_match(name: str, pattern: Union[str, Sequence[str]]):
    if isinstance(pattern, str):
        return fnmatch.fnmatchcase(name, pattern)

    for p in pattern:
        if fnmatch.fnmatchcase(name, p):
            return True

    return False


def wildcard_filter(
        name: str,
        include: Optional[Union[str, Sequence[str]]] = None,
        exclude: Optional[Union[str, Sequence[str]]] = None,
):
    """
    Return True if ``name`` matches the filter.

    :return: bool
    """
    if include is not None:
        if not wildcard_match(name, include):
            return False

    if exclude is not None:
        if wildcard_match(name, exclude):
            return False

    return True


def dict_rows_to_list_rows(dict_rows: Iterable[Mapping], default=None, header: bool = False) -> Iterable[Sequence]:
    if not isinstance(dict_rows, Sequence):
        dict_rows = list(dict_rows)

    if not dict_rows:
        return

    # gather all keys but keep order
    column_keys = list(dict_rows[0].keys())
    for row in dict_rows:
        for key in row:
            if key not in column_keys:
                column_keys.append(key)

    if header:
        yield column_keys

    for row in dict_rows:
        yield [row.get(key, default) for key in column_keys]


def create_matrix(*sizes, scalar=None):
    """
    Creates a N-dimensional matrix of lists
    :param sizes: list of int
    :param scalar: the content of each cell
    :return: list
        The innermost values will be None.

        If no sizes are given, scalar is returned.
    """
    num_dim = len(sizes)

    if not num_dim:
        return scalar

    matrix = [
        create_matrix(*sizes[1:], scalar=scalar)
        for _ in range(sizes[0])
    ]
    return matrix


def remove_matrix_axis(matrix: List, dim: int, index: int):
    if dim > 0:
        for vec in matrix:
            remove_matrix_axis(vec, dim - 1, index)
    else:
        matrix.pop(index)

    return matrix
