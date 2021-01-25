import math
from typing import Iterable


def get_number(value):
    """Convert any number format-able thing to int or float"""
    try:
        v = int(value)
        if v == float(value):
            return v
    except (TypeError, ValueError):
        pass

    try:
        v = float(value)
        if not math.isnan(value):
            return v
    except (TypeError, ValueError):
        pass


def get_min_max(seq: Iterable):
    mi, ma = None, None
    for x in seq:
        n = get_number(x)
        if n is not None:
            if mi is None:
                mi = n
            else:
                mi = min(mi, n)
            if ma is None:
                ma = n
            else:
                ma = max(ma, n)
        elif isinstance(x, Iterable):
            smi, sma = get_min_max(x)
            if smi is not None:
                if mi is None:
                    mi = smi
                else:
                    mi = min(mi, smi)
            if sma is not None:
                if ma is None:
                    ma = sma
                else:
                    ma = max(ma, sma)

    return mi, ma
