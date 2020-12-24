import os
import json
import time
import unittest

import elasticsearch

from elastipy import get_elastic_client, Query

from . import data


class TestOrdersQuery(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        cls.client = get_elastic_client()
        data.export_data(data.orders.orders1, data.orders.OrderExporter, cls.client)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter(client=cls.client).delete_index()

    def query(self):
        return Query(index=data.orders.OrderExporter.INDEX_NAME, client=self.client)

    def test_total_hits(self):
        query = self.query()
        response = query.execute()

        num_items = sum(len(o["items"]) for o in data.orders.orders1)
        self.assertEqual(num_items, response.total_hits)

    def test_match(self):
        query = self.query()

        self.assertEqual(3, query.match("channel", "the-shop").execute().total_hits)
        self.assertEqual(2, query.match("channel", "the-sale").execute().total_hits)
        self.assertEqual(2, query.match("channel", "the-end").execute().total_hits)


if __name__ == "__main__":
    unittest.main()
