import datetime
import copy
import time
import unittest

import elasticsearch

from elastipy import get_elastic_client, Query

from . import data


class TestOrdersAggregations(unittest.TestCase):

    def setUp(self):
        self.maxDiff = int(1e5)
        self.client = get_elastic_client()
        data.export_data(data.orders.orders1, data.orders.OrderExporter, self.client)
        time.sleep(1)

    def tearDown(self):
        data.orders.OrderExporter(client=self.client).delete_index()

    def query(self):
        return Query(index=data.orders.OrderExporter.INDEX_NAME, client=self.client)

    def test_orders_terms_sku(self):
        query = self.query()
        agg_sku_count = query.agg_terms(field="sku")
        agg_sku_qty = agg_sku_count.metric("sum", field="quantity")

        #query.dump_body()
        query.execute()#.dump()

        self.assertEqual(
            {
                "sku-1": 4,
                "sku-2": 2,
                "sku-3": 1,
            },
            agg_sku_count.to_dict()
        )
        self.assertEqual(
            {
                "sku-1": 7,
                "sku-2": 3,
                "sku-3": 5,
            },
            agg_sku_qty.to_dict()
        )

    def test_orders_terms_sku_terms_channel(self):
        query = self.query()
        agg_sku = query.agg_terms(field="sku")
        agg_channel = agg_sku.aggregation("terms", field="channel")
        agg_qty = agg_channel.aggregation("sum", field="quantity")

        query.execute()# .dump()

        self.assertEqual(
            {
                ("sku-1", "the-shop"): 2,
                ("sku-1", "the-sale"): 1,
                ("sku-1", "the-end"): 1,
                ("sku-2", "the-shop"): 1,
                ("sku-2", "the-sale"): 1,
                ("sku-3", "the-end"): 1,
            },
            agg_channel.to_dict()
        )

        self.assertEqual(
            {
                ("sku-1", "the-shop"): 3,
                ("sku-1", "the-sale"): 3,
                ("sku-1", "the-end"): 1,
                ("sku-2", "the-shop"): 2,
                ("sku-2", "the-sale"): 1,
                ("sku-3", "the-end"): 5,
            },
            agg_qty.to_dict()
        )

    def test_orders_terms_sku_terms_channel_terms_country(self):
        query = self.query()
        agg_sku = query.agg_terms(field="sku")
        agg_channel = agg_sku.aggregation("terms", field="channel")
        agg_country = agg_channel.aggregation("terms", field="country")
        agg_qty = agg_country.metric("sum", field="quantity")

        query.execute()# .dump()

        self.assertEqual(
            {
                ("sku-1", "the-shop", "DE"): 1,
                ("sku-1", "the-shop", "GB"): 2,
                ("sku-1", "the-sale", "DE"): 3,
                ("sku-1", "the-end",  "GB"): 1,
                ("sku-2", "the-shop", "DE"): 2,
                ("sku-2", "the-sale", "DE"): 1,
                ("sku-3", "the-end",  "GB"): 5,
            },
            agg_qty.to_dict()
        )

    def test_orders_date_histogram(self):
        query = self.query()
        items_per_day = query.agg_date_histogram(interval="1d")
        orders_per_day = items_per_day.metric_cardinality(field="order_id")
        #query.dump_body()
        query.execute()#.dump()

        self.assertEqual(
            {
                "2000-01-01T00:00:00.000Z": 2,
                "2000-01-02T00:00:00.000Z": 1,
                "2000-01-03T00:00:00.000Z": 4,
            },
            items_per_day.to_dict()
        )

        self.assertEqual(
            {
                "2000-01-01T00:00:00.000Z": 2,
                "2000-01-02T00:00:00.000Z": 1,
                "2000-01-03T00:00:00.000Z": 2,
            },
            orders_per_day.to_dict()
        )


if __name__ == "__main__":
    unittest.main()
