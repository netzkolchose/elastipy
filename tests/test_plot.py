import time
import unittest

from elastipy import get_elastic_client, Search
from elastipy.plot.text.characters import UnicodeCharacters

from . import data


class TestOrdersAggregations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        cls.client = get_elastic_client()
        data.export_data(data.orders.orders1, data.orders.OrderExporter, cls.client)
        time.sleep(1.1)  # give time to update index

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter(client=cls.client).delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME, client=self.client)

    def test_unicode_bar(self):
        #for i in range(9):
        #    t = i / 8
        #    print(f"{round(t, 3):6}: {UnicodeCharacters.hbar(t, 1)}")
        self.assertEqual(
            "",
            UnicodeCharacters.hbar(.124, 1),
        )
        self.assertEqual(
            UnicodeCharacters.left8th[0],
            UnicodeCharacters.hbar(.125, 1),
        )
        self.assertEqual(
            UnicodeCharacters.left8th[3],
            UnicodeCharacters.hbar(.5, 1),
        )
        self.assertEqual(
            UnicodeCharacters.left8th[6],
            UnicodeCharacters.hbar(.875, 1),
        )
        self.assertEqual(
            UnicodeCharacters.block * 3,
            UnicodeCharacters.hbar(1, 3),
        )
        self.assertEqual(
            UnicodeCharacters.block,
            UnicodeCharacters.hbar(.5, 2),
        )
        self.assertEqual(
            UnicodeCharacters.block + UnicodeCharacters.left8th[3],
            UnicodeCharacters.hbar(.5, 3),
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
