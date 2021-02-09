import time
import unittest
from io import BytesIO

import numpy as np
from matplotlib.axes import Axes
from plotly.graph_objects import Figure

from elastipy import Search, plot
from elastipy.aggregation import Aggregation

from tests import data
from tests.live.base import TestCase


class TestPlot(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.orders.orders, data.orders.OrderExporter)

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter().delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME)

    def get_fig_data(self, plt, format: str = "png"):
        if isinstance(plt, Axes):
            file = BytesIO()
            plt.figure.savefig(file, format=format)
            file.seek(0)
            return file.read()
        elif isinstance(plt, Figure):
            # TODO: what could we test here?
            return plt
        else:
            raise AssertionError(f"Invalid plt type '{type(plt)}'")

    def test_backend(self):
        # just check that default is actually what the docs say
        self.assertEqual(
            "matplotlib", plot.get_backend()
        )

    def test_heatmap_matplotlib(self):
        plot.set_backend("matplotlib")

        agg = self.search() \
            .agg_date_histogram(calendar_interval="day") \
            .agg_terms(field="sku").execute()
        ax = agg.plot.heatmap()
        data = self.get_fig_data(ax)

        ax = agg.plot.heatmap(figsize=(20, 20))
        data2 = self.get_fig_data(ax)
        self.assertGreater(len(data2), len(data))

    def test_heatmap_plotly(self):
        plot.set_backend("plotly")

        agg = self.search() \
            .agg_date_histogram("date", calendar_interval="day") \
            .agg_terms("sku", field="sku").execute()

        fig = agg.plot.heatmap(replace={np.nan: 0})
        self.assertEqual("sku", fig.layout.xaxis.title.text)
        self.assertEqual("date", fig.layout.yaxis.title.text)
        self.assertEqual("sku.doc_count", fig.layout.coloraxis.colorbar.title.text)

        fig = agg.plot.heatmap(labels={"x": "override"}, transpose=True)
        self.assertEqual("override", fig.layout.xaxis.title.text)
        self.assertEqual("sku", fig.layout.yaxis.title.text)
        self.assertEqual("sku.doc_count", fig.layout.coloraxis.colorbar.title.text)

        agg = self.search() \
            .agg_date_histogram("date", calendar_interval="day") \
            .agg_terms("sku", field="sku") \
            .metric_sum("qty", field="quantity", return_self=True).execute()

        fig = agg.plot.heatmap()
        self.assertEqual("sku", fig.layout.xaxis.title.text)
        self.assertEqual("date", fig.layout.yaxis.title.text)
        self.assertEqual("qty", fig.layout.coloraxis.colorbar.title.text)

    def assert_line_bar_etc(self, mpl: bool):
        agg: Aggregation = self.search() \
            .agg_date_histogram("date", calendar_interval="day") \
            .metric_sum("qty", field="quantity").execute() \
            .metric_sum("idx", field="item_line_index").execute()

        self.assertTrue(self.get_fig_data(agg.plot(to_index=True)))
        self.assertTrue(self.get_fig_data(agg.plot.bar(to_index=True)))
        self.assertTrue(self.get_fig_data(agg.plot.barh(to_index=True)))
        self.assertTrue(self.get_fig_data(agg.plot.box(to_index=True)))
        self.assertTrue(self.get_fig_data(agg.plot.line(to_index=True)))
        self.assertTrue(self.get_fig_data(agg.plot.hist(to_index=True)))
        if mpl:
            self.assertTrue(self.get_fig_data(agg.plot.kde(to_index=True, y="qty")))
        self.assertTrue(self.get_fig_data(agg.plot.area(to_index=True, y="qty")))
        if mpl:
            self.assertTrue(self.get_fig_data(agg.plot.pie(to_index=True, y="qty")))
        self.assertTrue(self.get_fig_data(agg.plot.scatter("idx", "qty", to_index=True)))
        if mpl:
            self.assertTrue(self.get_fig_data(agg.plot.hexbin("idx", "qty", to_index=True)))

    def test_line_bar_etc_matplotlib(self):
        plot.set_backend("matplotlib")
        self.assert_line_bar_etc(True)

    def test_line_bar_etc_plotly(self):
        plot.set_backend("plotly")
        self.assert_line_bar_etc(False)


if __name__ == "__main__":
    unittest.main()
