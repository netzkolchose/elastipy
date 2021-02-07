import datetime
import json
import time
import unittest

import elasticsearch

from elastipy import Search

from tests import data
from tests.live.base import TestCase


class TestOrdersAggregationsTable(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.orders.orders, data.orders.OrderExporter)

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter().delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME)

    def test_named_nested_aggregations_to_rows(self):
        s = self.search()
        agg_sku = s.agg_terms("sku", field="sku")
        agg_channel = agg_sku.aggregation("channel", "terms", field="channel")
        agg_country = agg_channel.aggregation("country", "terms", field="country")
        agg_qty = agg_country.metric("quantity", "sum", field="quantity")

        s.execute()

        #agg_qty.dump.table()
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

        # test the exclude/include params

        self.assertEqual(
            ["sku", "sku.doc_count", "channel", "channel.doc_count", "country", "country.doc_count", "quantity"],
            list(agg_qty.rows())[0],
        )
        self.assertEqual(
            ["sku", "channel", "channel.doc_count", "country", "country.doc_count", "quantity"],
            list(agg_qty.rows(exclude="sku.doc_count"))[0],
        )
        self.assertEqual(
            ["sku", "channel", "country", "quantity"],
            list(agg_qty.rows(exclude="*.doc_count"))[0],
        )
        self.assertEqual(
            ["sku", "sku.doc_count", "quantity"],
            list(agg_qty.rows(include=["sku*", "quantity"]))[0],
        )
        self.assertEqual(
            ["sku.doc_count", "country.doc_count"],
            list(agg_qty.rows(include="*.doc_count", exclude="channel*"))[0],
        )

    def test_named_nested_aggregations_multival_to_rows(self):
        s = self.search()
        agg_sku = s.agg_terms("sku", field="sku")
        agg_channel = agg_sku.aggregation("channel", "terms", field="channel")
        agg_stats = agg_channel.metric("stats", "stats", field="quantity")

        s.execute()

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

    def test_empty_table(self):
        s = self.search().term("sku", "not-existing")
        agg = s.agg_terms("sku", field="sku")

        s.execute()

        self.assertEqual(
            [], list(agg.rows())
        )

        # also make sure that Table(source) is not crashing
        agg.dump.table()


if __name__ == "__main__":
    unittest.main()
