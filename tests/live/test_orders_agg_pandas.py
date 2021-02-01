import datetime
import json
import time
import unittest

import pandas as pd

from elastipy import Search

from tests import data
from tests.live.base import TestCase


class TestOrdersAggregationsPandas(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.orders.orders1, data.orders.OrderExporter)

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter().delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME)

    def test_df_date_conversion(self):
        s = self.search()
        agg = s \
            .agg_date_histogram("date", calendar_interval="1d") \
            .agg_terms("sku", field="sku") \
            .metric_sum("quantity", field="quantity")

        s.execute()

        df = agg.to_pandas()
        self.assertEqual(pd.Timestamp, type(df["date"][0]))

    def test_df_index(self):
        s = self.search()
        agg = s\
            .agg_date_histogram("date", calendar_interval="1d") \
            .agg_terms("sku", field="sku") \
            .agg_terms("channel", field="channel") \
            .agg_terms("country", field="country") \
            .metric_sum("quantity", field="quantity")

        s.execute()

        df = agg.to_pandas(index=True)
        self.assertEqual(pd.Timestamp, type(df.index[0]))
        self.assertIn("date", df)

        df = agg.to_pandas(to_index=True)
        self.assertEqual(pd.Timestamp, type(df.index[0]))
        self.assertNotIn("date", df)

        with self.assertRaises(ValueError):
            agg.to_pandas(index=True, to_index=True)

    def test_df_exclude(self):
        s = self.search()
        agg = s \
            .agg_date_histogram("date", calendar_interval="1d") \
            .agg_terms("sku", field="sku") \
            .agg_terms("country", field="country") \
            .metric_sum("quantity", field="quantity")

        s.execute()

        df = agg.to_pandas(exclude="*y")
        self.assertEqual(
            ["date", "date.doc_count", "sku", "sku.doc_count", "country.doc_count"],
            list(df.keys())
        )


if __name__ == "__main__":
    unittest.main()
