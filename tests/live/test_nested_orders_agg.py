import datetime
import json
import time
import unittest

from elastipy import Search, query

from tests import data
from tests.live.base import TestCase


class TestNestedOrdersAggregations(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.orders.orders, data.nested_orders.NestedOrderExporter)

    @classmethod
    def tearDownClass(cls):
        data.nested_orders.NestedOrderExporter().delete_index()

    def search(self):
        return Search(index=data.nested_orders.NestedOrderExporter.INDEX_NAME)

    def test_orders_terms_sku(self):
        q = self.search()
        # must put terms agg into nested agg
        agg_count = q.agg_nested("items", path="items").agg_terms(field="items.sku")
        agg_quantity = agg_count.metric_sum(field="items.quantity", return_self=True)

        q.execute()#.dump()

        self.assertEqual(
            {
                ("items", "sku-1"): 4,
                ("items", "sku-2"): 2,
                ("items", "sku-3"): 1,
            },
            agg_count.to_dict()
        )
        self.assertEqual(
            {
                ("items", "sku-1"): 7,
                ("items", "sku-2"): 3,
                ("items", "sku-3"): 5,
            },
            agg_quantity.to_dict()
        )


if __name__ == "__main__":
    unittest.main()
