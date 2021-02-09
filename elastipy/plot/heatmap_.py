from typing import Tuple, Union

from .backend import get_backend


def heatmap(
        data,
        figsize: Tuple[Union[int, float], Union[int, float]] = None,
        **kwargs,
):
    """
    Generic heatmap wrapper around **matplotlib** or **plotly**.

    Pandas' default plotting backend is matplotlib. In this case the
    `seaborn.heatmap <http://seaborn.pydata.org/generated/seaborn.heatmap.html>`__.
    is used and the ``seaborn`` package must be installed along with
    ``pandas`` and ``matplotlib``.

    The `ploty backend <>`__
    is also supported in which case the
    `plotly.express.imshow <https://plotly.com/python/imshow/>`
    function is used.

    In matplotlib-mode, the ``figsize`` parameter will
    create a new Axes before calling
    `seaborn.heatmap <http://seaborn.pydata.org/generated/seaborn.heatmap.html>`__.
    For plotly it's ignored.

    :param data: :link:`pandas.DataFrame`

    :param figsize: ``tuple of ints or floats``
        Optional tuple to change the size of the plot when the plotting
        backend is ``matplotlib``.
        ``int`` values will be passed to :link:`matplotlib.axes.Axes` unchanged.
        A ``float`` value defines the size in terms of the number of
        keys per axis and is converted to int with ``int(len(keys) * value)``

    :param kwargs: Passed to :meth:`seaborn.heatmap`
    :return:
        :link:`matplotlib.axes.Axes` Axis object with the heatmap.
    """
    if get_backend() == "matplotlib":
        import matplotlib.pyplot
        import seaborn

        if figsize is not None:
            figsize = tuple(
                v if isinstance(v, int) else int(data.shape[i] * v)
                for i, v in enumerate(figsize)
            )
            matplotlib.pyplot.subplots(figsize=figsize)

        kwargs.setdefault("cmap", "cividis")
        return seaborn.heatmap(data, **kwargs)

    elif get_backend() == "plotly":
        import plotly.express

        return plotly.express.imshow(data, **kwargs)

    else:
        raise NotImplementedError(
            f"Plotting backend '{get_backend()}' not supported"
        )
