from typing import Sequence, Iterable, Mapping, TextIO


def print_dict_rows(dict_rows, header=True, digits=None, file=None):
    print_rows(dict_rows_to_list_rows(dict_rows, header=header), digits=digits, file=file)


def print_rows(rows: Iterable[Sequence], digits: int = None, file: TextIO = None):
    """
    Print a somewhat formatted table from rows of lists
    :param rows: list[list]
    :param digits: int, optional number of digits for rounding
    :param file: optional io stream to write to
    """
    if not isinstance(rows, Sequence):
        rows = list(rows)

    if not rows:
        return

    def _to_str(v):
        if digits is not None:
            try:
                v = round(v, digits)
            except (TypeError, ValueError):
                pass
        return str(v)

    column_width = [0] * len(rows[0])
    for i, row in enumerate(rows):
        rows[i] = [_to_str(v) for v in row]
        for x, v in enumerate(rows[i]):
            column_width[x] = max(column_width[x], len(v))

    format_str = " | ".join(
        "{:%s}" % v
        for v in column_width
    )

    for row in rows:
        print(format_str.format(*row), file=file)


def dict_rows_to_list_rows(dict_rows: Iterable[Mapping], default=None, header: bool = False) -> Iterable[Sequence]:
    if not isinstance(dict_rows, Sequence):
        dict_rows = list(dict_rows)

    rows = []

    if not dict_rows:
        return rows

    # gather all keys but keep order
    column_keys = list(dict_rows[0].keys())
    for row in dict_rows:
        for key in row:
            if key not in column_keys:
                column_keys.append(key)

    if header:
        rows.append(column_keys)

    for row in dict_rows:
        rows.append([row.get(key, default) for key in column_keys])

    return rows
