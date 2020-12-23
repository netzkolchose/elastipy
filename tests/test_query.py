import os
import json
import datetime
import copy
import unittest

import elasticsearch

from elastipy import get_elastic_client, Query

from . import data


class TestQuery(unittest.TestCase):

    def setUp(self):
        self.client = get_elastic_client()

    def test_orders(self):
        with data.orders.export1(self.client):
            query = Query(index=data.orders.OrderExporter.INDEX_NAME)
            response = query.execute()

            num_items = sum(len(o["items"]) for o in data.orders.orders1)
            self.assertEqual(num_items, response.total_hits)

        with self.assertRaises(elasticsearch.NotFoundError):
            Query(index=data.orders.OrderExporter.INDEX_NAME).execute()

    def test_orders_match(self):
        with data.orders.export1(self.client):
            query = Query(index=data.orders.OrderExporter.INDEX_NAME, client=self.client)

            self.assertEqual(3, query.match("channel", "the-shop").execute().total_hits)
            self.assertEqual(2, query.match("channel", "the-sale").execute().total_hits)


if __name__ == "__main__":
    unittest.main()
