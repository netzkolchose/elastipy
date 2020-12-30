import datetime
import json
import time
import unittest

import elasticsearch

from elastipy import get_elastic_client, Search

from . import data


class TestOrdersAggregationsTable(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        cls.client = get_elastic_client()
        data.export_data(data.orders.orders1, data.orders.OrderExporter, cls.client)
        time.sleep(1.1)  # give time to update index

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter(client=cls.client).delete_index()

    def query(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME, client=self.client)

    def test_named_nested_aggregations_to_rows(self):
        query = self.query()
        agg_sku = query.agg_terms("sku", field="sku")
        agg_channel = agg_sku.aggregation("channel", "terms", field="channel")
        agg_country = agg_channel.aggregation("country", "terms", field="country")
        agg_qty = agg_country.metric("quantity", "sum", field="quantity")

        query.execute()

        # agg_qty.dump_table()
        self.assertEqual(
            [
                ["sku", "channel", "country", "quantity"],
                ["sku-1", "the-shop", "DE", 1],
                ["sku-1", "the-shop", "GB", 2],
                ["sku-1", "the-end",  "GB", 1],
                ["sku-1", "the-sale", "DE", 3],
                ["sku-2", "the-sale", "DE", 1],
                ["sku-2", "the-shop", "DE", 2],
                ["sku-3", "the-end",  "GB", 5],
            ],
            agg_qty.to_rows()
        )

    def test_named_nested_aggregations_multival_to_rows(self):
        query = self.query()
        agg_sku = query.agg_terms("sku", field="sku")
        agg_channel = agg_sku.aggregation("channel", "terms", field="channel")
        agg_stats = agg_channel.metric("stats", "stats", field="quantity")

        query.execute()

        # agg_stats.dump_table()
        self.assertEqual(
            [
                ["sku", "channel", "stats_count", "stats_min", "stats_max", "stats_sum", "stats_avg"],
                ["sku-1", "the-shop", 2, 1, 2, 3, 1.5],
                ["sku-1", "the-end",  1, 1, 1, 1, 1],
                ["sku-1", "the-sale", 1, 3, 3, 3, 3],
                ["sku-2", "the-sale", 1, 1, 1, 1, 1],
                ["sku-2", "the-shop", 1, 2, 2, 2, 2],
                ["sku-3", "the-end",  1, 5, 5, 5, 5],
            ],
            agg_stats.to_rows()
        )


if __name__ == "__main__":
    unittest.main()
