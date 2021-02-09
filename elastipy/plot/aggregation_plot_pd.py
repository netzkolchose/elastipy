from typing import Union, Sequence, Tuple, Optional, Any

from ..aggregation import Aggregation
from .backend import get_backend


class PandasPlotWrapper:
    """
    This is a short-hand accessor to the
    `pandas.DataFrame.plot <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html>`__
    interface.

    The documented parameters below will be passed to
    :link:`Aggregation.to_pandas`. All other parameters
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
            replace=None,
            include: Optional[Union[str, Sequence[str]]] = None,
            exclude: Optional[Union[str, Sequence[str]]] = None,
            transpose: bool = False,
            figsize: Tuple[Union[int, float], Union[int, float]] = None,
            **kwargs,
    ):
        """
        Plots a heatmap using the data from :link:`Aggregation.df_matrix`.

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

        The documented parameters below are passed to
        :link:`Aggregation.df_matrix`, generating a
        `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`__.
        All other parameters are passed to the heatmap function.

        In matplotlib-mode, the ``figsize`` parameter will
        create a new Axes before calling
        `seaborn.heatmap <http://seaborn.pydata.org/generated/seaborn.heatmap.html>`__.
        For plotly it's ignored.

        **Labels** can be defined in **plotly** with the ``labels`` parameter,
        e.g. ``labels={"x": "date", "y": "temperature", "color": "date.doc_count"}``.
        If ``labels`` or any of the keys are not defined they will be set to the
        name of each aggregation. ``color`` will either be ``<bucket-agg-name>.doc_count``
        or ``<metric-name>`` (or pipeline).

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

        :param replace:
            ``str, regex, list, dict, Series, int, float, or None``

            If not None, the :link:`pandas.DataFrame.replace` function will be
            called with this parameter as the ``to_replace`` parameter.

        :param transpose ``bool``
            Transposes the matrix, e.g. exchanges X and Y axis.

        :param figsize: ``tuple of ints or floats``
            Optional tuple to change the size of the plot when the plotting
            backend is ``matplotlib``.
            ``int`` values will be passed to :link:`matplotlib.axes.Axes` unchanged.
            A ``float`` value defines the size in terms of the number of
            keys per axis and is converted to int with ``int(len(keys) * value)``

        :param kwargs: Passed to :meth:`seaborn.heatmap`
        :return: :class:`matplotlib.axes.Axes` Axis object with the heatmap.
        """
        from .heatmap_ import heatmap
        from ..aggregation.visitor import Visitor

        df = self._agg.df_matrix(
            sort=sort,
            default=default,
            include=include,
            exclude=exclude,
        )
        if replace is not None:
            df.replace(to_replace=replace, inplace=True)
        if transpose:
            df = df.transpose()

        # set plotly labels
        if get_backend() == "plotly":

            labels = kwargs.get("labels") or dict()

            names = Visitor(self._agg).key_names()
            if transpose:
                names[0], names[1] = names[1], names[0]

            if self._agg.is_bucket():
                names.append(f"{self._agg.name}.doc_count")
            else:
                names.append(self._agg.name)

            labels.setdefault("x", names[1])
            labels.setdefault("y", names[0])
            labels.setdefault("color", names[2])

            #labels["x"], labels["y"] = labels["y"], labels["x"]

            kwargs["labels"] = labels

        return heatmap(df, figsize=figsize, **kwargs)
