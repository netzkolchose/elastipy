import datetime
import json
import time
import unittest

import pandas as pd

from elastipy import Search

from . import data


class TestOrdersAggregationsPandas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.orders.orders1, data.orders.OrderExporter)

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter().delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME)

    def test_named_nested_aggregations_to_rows(self):
        s = self.search()
        agg = s\
            .agg_date_histogram("date", calendar_interval="1d") \
            .agg_terms("sku", field="sku") \
            .agg_terms("channel", field="channel") \
            .agg_terms("country", field="country") \
            .metric_sum("quantity", field="quantity")

        s.execute()

        df: pd.DataFrame = agg.to_pandas()
        #print(df)
        self.assertEqual(pd.Timestamp, type(df.index[0]))



if __name__ == "__main__":
    unittest.main()
