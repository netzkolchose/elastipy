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

        #agg_qty.dump_table()
        self.assertEqual(
            [
                ["sku", "sku.doc_count", "channel", "channel.doc_count", "country", "country.doc_count", "quantity"],
                ["sku-1", 4, "the-shop", 2, "DE", 1, 1],
                ["sku-1", 4, "the-shop", 2, "GB", 1, 2],
                ["sku-1", 4, "the-end",  1, "GB", 1, 1],
                ["sku-1", 4, "the-sale", 1, "DE", 1, 3],
                ["sku-2", 2, "the-sale", 1, "DE", 1, 1],
                ["sku-2", 2, "the-shop", 1, "DE", 1, 2],
                ["sku-3", 1, "the-end",  1, "GB", 1, 5],
            ],
            list(agg_qty.rows())
        )

    def test_named_nested_aggregations_multival_to_rows(self):
        query = self.query()
        agg_sku = query.agg_terms("sku", field="sku")
        agg_channel = agg_sku.aggregation("channel", "terms", field="channel")
        agg_stats = agg_channel.metric("stats", "stats", field="quantity")

        query.execute()

        #agg_stats.dump_table()
        self.assertEqual(
            [
                ["sku", "sku.doc_count", "channel", "channel.doc_count", "stats.count", "stats.min", "stats.max", "stats.sum", "stats.avg"],
                ["sku-1", 4, "the-shop", 2, 2, 1, 2, 3, 1.5],
                ["sku-1", 4, "the-end",  1, 1, 1, 1, 1, 1],
                ["sku-1", 4, "the-sale", 1, 1, 3, 3, 3, 3],
                ["sku-2", 2, "the-sale", 1, 1, 1, 1, 1, 1],
                ["sku-2", 2, "the-shop", 1, 1, 2, 2, 2, 2],
                ["sku-3", 1, "the-end",  1, 1, 5, 5, 5, 5],
            ],
            list(agg_stats.rows())
        )


if __name__ == "__main__":
    unittest.main()
