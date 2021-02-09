from typing import Optional


def get_backend() -> Optional[str]:
    """
    Returns the current pandas plotting backend,
    or ``None`` if pandas is not available.

    Typically the result will be ``"matplotlib"``.

    :return: str or None
    """
    try:
        import pandas
    except ImportError:
        return None

    return pandas.options.plotting.backend


def set_backend(backend: str):
    """
    Sets the pandas plotting backend.

    If pandas is not install nothing happens.

    :param backend: str
        A string like ``"matplotlib"`` or ``"plotly"``.

    """
    try:
        import pandas
    except ImportError:
        return

    pandas.options.plotting.backend = backend
