from typing import Union, Sequence, Tuple, Optional, Any

from elastipy.aggregation import Aggregation


class PandasPlotWrapper:
    """
    This is a short-hand accessor to the
    `pandas.DataFrame.plot <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html>`__
    interface.

    The documented parameters below will be passed to
    :meth:`Aggregation.to_pandas`. All other parameters
    are passed to the respective functions of the pandas
    interface.

    .. CODE::

        s = Search()
        s.agg_terms("idx", field="a").execute().plot(
            to_index="idx",
            kind="bar",
        )

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

    :return: :link:`matplotlib.axes.Axes` or numpy.ndarray of them
        If the backend is not the default matplotlib one, the return value
        will be the object returned by the backend.
    """

    def __init__(self, agg: Aggregation):
        self._agg = agg

    def __call__(
            self,
            *args,
            index: Union[bool, str] = False,
            to_index: Union[bool, str] = False,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
            flat: Union[bool, str, Sequence[str]] = False,
            dtype=None,
            default=None,
            **kwargs,
    ):
        return self._pd_plot(
            None,
            *args,
            index=index,
            to_index=to_index,
            include=include,
            exclude=exclude,
            flat=flat,
            dtype=dtype,
            default=default,
            **kwargs,
        )

    def _pd_plot(
            self,
            _function,
            *args,
            index: Union[bool, str] = False,
            to_index: Union[bool, str] = False,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
            flat: Union[bool, str, Sequence[str]] = False,
            dtype=None,
            default=None,
            **kwargs,
    ):
        df = self._agg.to_pandas(
            index=index,
            to_index=to_index,
            include=include,
            exclude=exclude,
            flat=flat,
            dtype=dtype,
            default=default,
        )
        if not _function:
            return df.plot(*args, **kwargs)
        else:
            return getattr(df.plot, _function)(*args, **kwargs)

    def line(self, x=None, y=None, **kwargs):
        """
        Plot Series or DataFrame as lines.

        See :link:`pandas.DataFrame.plot.line`
        """
        return self._pd_plot(
            "line", x=x, y=y, **kwargs,
        )

    def bar(self, x=None, y=None, **kwargs):
        """
        Vertical bar plot.

        See :link:`pandas.DataFrame.plot.bar`
        """
        return self._pd_plot(
            "bar", x=x, y=y, **kwargs,
        )

    def barh(self, x=None, y=None, **kwargs):
        """
        Horizontal bar plot.

        See :link:`pandas.DataFrame.plot.barh`
        """
        return self._pd_plot(
            "barh", x=x, y=y, **kwargs,
        )

    def box(self, by=None, **kwargs):
        r"""
        Make a box plot of the DataFrame columns.

        See :link:`pandas.DataFrame.plot.box`
        """
        return self._pd_plot(
            "box", by=by, **kwargs,
        )

    def hist(self, by=None, bins=10, **kwargs):
        """
        Draw one histogram of the DataFrame's columns.

        See :link:`pandas.DataFrame.plot.hist`
        """
        return self._pd_plot(
            "hist", by=by, bins=bins, **kwargs,
        )

    def kde(self, bw_method=None, ind=None, **kwargs):
        """
        Generate Kernel Density Estimate plot using Gaussian kernels.

        See :link:`pandas.DataFrame.plot.kde`
        """
        return self._pd_plot(
            "kde", bw_method=bw_method, ind=ind, **kwargs,
        )

    def area(self, x=None, y=None, **kwargs):
        """
        Draw a stacked area plot.

        See :link:`pandas.DataFrame.plot.area`
        """
        return self._pd_plot(
            "area", x=x, y=y, **kwargs,
        )

    def pie(self, **kwargs):
        """
        Generate a pie plot.

        See :link:`pandas.DataFrame.plot.pie`
        """
        return self._pd_plot(
            "pie", **kwargs,
        )

    def scatter(self, x, y, s=None, c=None, **kwargs):
        """
        Create a scatter plot with varying marker point size and color.

        See :link:`pandas.DataFrame.plot.scatter`
        """
        return self._pd_plot(
            "scatter", x=x, y=y, s=s, c=c, **kwargs,
        )

    def hexbin(self, x, y, C=None, reduce_C_function=None, gridsize=None, **kwargs):
        """
        Generate a hexagonal binning plot.

        See :link:`pandas.DataFrame.plot.hexbin`
        """
        return self._pd_plot(
            "hexbin", x=x, y=y, C=C, reduce_C_function=reduce_C_function, gridsize=gridsize, **kwargs,
        )

    def heatmap(
            self,
            sort: Optional[Union[bool, str, int, Sequence[Union[str, int]]]] = None,
            default: Optional[Any] = None,
            include: Optional[Union[str, Sequence[str]]] = None,
            exclude: Optional[Union[str, Sequence[str]]] = None,
            transpose: bool = False,
            figsize: Tuple[int, int] = None,
            **kwargs,
    ):
        """
        Plots a heatmap using
        `seaborn.heatmap <http://seaborn.pydata.org/generated/seaborn.heatmap.html>`__.

        The documented parameters below are passed to
        :meth:`Aggregation.df_matrix`, generating a
        `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`__.
        All other parameters are passed to :meth:`seaborn.heatmap`.

        The ``figsize`` can be specified as an argument to this function and will
        create a new axis before calling :meth:`seaborn.heatmap`.

        :param sort:
        :param default:
        :param include:
        :param exclude:

        :param transpose ``bool``
            Transposes the matrix, e.g. exchanges X and Y axis.

        :param figsize: ``(int, int)``
            Optional tuple of int to change the size of the plot.

        :param kwargs: Passed to :meth:`seaborn.heatmap`
        :return: :class:`matplotlib.axes.Axes` Axis object with the heatmap.
        """
        import matplotlib.pyplot
        import seaborn

        df = self._agg.df_matrix(
            sort=sort,
            default=default,
            include=include,
            exclude=exclude,
        )
        if transpose:
            df = df.transpose()

        if figsize is not None:
            matplotlib.pyplot.subplots(figsize=figsize)

        kwargs.setdefault("cmap", "cividis")
        return seaborn.heatmap(df, **kwargs)
