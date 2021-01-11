import time
import unittest

from elastipy import Search
from elastipy.plot.text.console import Characters

from tests import data
from tests.live.base import TestCase


class TestPlot(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.orders.orders, data.orders.OrderExporter)
        time.sleep(1.1)  # give time to update index

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter().delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME)

    def test_unicode_bar(self):
        ch = Characters()
        self.assertEqual(
            " ",
            ch.hbar(.124, 1),
        )
        self.assertEqual(
            ch.left8th[0],
            ch.hbar(.125, 1),
        )
        self.assertEqual(
            ch.left8th[3],
            ch.hbar(.5, 1),
        )
        self.assertEqual(
            ch.left8th[6],
            ch.hbar(.875, 1),
        )
        self.assertEqual(
            ch.block * 3,
            ch.hbar(1, 3),
        )
        self.assertEqual(
            ch.block + " ",
            ch.hbar(.5, 2),
        )
        self.assertEqual(
            ch.block + ch.left8th[3] + " ",
            ch.hbar(.5, 3),
        )

    def test_orders_terms_sku(self):
        query = self.search()
        agg_sku_count = query.agg_terms(field="sku")
        agg_sku_qty = agg_sku_count.metric("sum", field="quantity")
        query.execute()

        self.assertEqual(
            {
                "sku-1": 7,
                "sku-2": 3,
                "sku-3": 5,
            },
            agg_sku_qty.to_dict()
        )
        agg_sku_qty.plot.text.hbar()


if __name__ == "__main__":
    unittest.main()
