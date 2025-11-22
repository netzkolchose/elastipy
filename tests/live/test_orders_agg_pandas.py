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
        data.export_data(data.orders.orders, data.orders.OrderExporter)

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

        df = agg.to_pandas(convert_datetime=False)
        self.assertEqual(str, type(df["date"][0]))

    def test_df_include(self):
        s = self.search()
        agg = s \
            .agg_date_histogram("date", calendar_interval="1d") \
            .agg_terms("sku", field="sku") \
            .agg_terms("country", field="country") \
            .metric_sum("quantity", field="quantity")

        s.execute()

        self.assertEqual(
            ["date", "date.doc_count", "quantity"],
            list(agg.to_pandas(include="*a*").keys())
        )

        self.assertEqual(
            ["date.doc_count", "sku", "sku.doc_count", "country", "country.doc_count"],
            list(agg.to_pandas(include=["sku", "*o*"]).keys())
        )

    def test_df_exclude(self):
        s = self.search()
        agg = s \
            .agg_date_histogram("date", calendar_interval="1d") \
            .agg_terms("sku", field="sku") \
            .agg_terms("country", field="country") \
            .metric_sum("quantity", field="quantity")

        s.execute()

        self.assertEqual(
            ["date", "date.doc_count", "sku", "sku.doc_count", "country.doc_count"],
            list(agg.to_pandas(exclude="*y").keys())
        )
        self.assertEqual(
            ["date", "date.doc_count", "sku.doc_count", "country.doc_count"],
            list(agg.to_pandas(exclude=["*y", "sku"]).keys())
        )

    def test_df_include_exclude(self):
        s = self.search()
        agg = s \
            .agg_date_histogram("date", calendar_interval="1d") \
            .agg_terms("sku", field="sku") \
            .agg_terms("country", field="country") \
            .metric_sum("quantity", field="quantity")

        s.execute()

        self.assertEqual(
            ["date.doc_count", "sku", "sku.doc_count"],
            list(agg.to_pandas(include="*u*", exclude="*y*").keys())
        )


if __name__ == "__main__":
    unittest.main()
