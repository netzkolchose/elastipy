import os
import json
import time
import unittest

import elasticsearch

from elastipy import get_elastic_client, Search

from . import data


class TestOrdersQuery(unittest.TestCase):

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

    def test_total_hits_all(self):
        search = self.search()
        response = search.execute()

        num_items = sum(len(o["items"]) for o in data.orders.orders1)
        self.assertEqual(num_items, response.total_hits)

    def test_total_hits_term(self):
        search = self.search()

        for country in ("DE", "GB"):
            self.assertEqual(
                sum(
                    len(o["items"])
                    for o in data.orders.orders1
                    if o["country"] == country
                ),
                search.term("country", country).execute().total_hits
            )

            self.assertEqual(
                sum(
                    len(o["items"])
                    for o in data.orders.orders1
                    if o["country"] != country
                ),
                (~search.term("country", country)).execute().total_hits
            )

        self.assertEqual(3, search.term("channel", "the-shop").execute().total_hits)
        self.assertEqual(2, search.term("channel", "the-sale").execute().total_hits)
        self.assertEqual(2, search.term("channel", "the-end").execute().total_hits)

    def test_total_hits_terms(self):
        search = self.search()
        search = search.terms(field="country", value=["DE", "GB"])
        self.assertEqual(
            sum(
                len(o["items"])
                for o in data.orders.orders1
            ),
            search.execute().total_hits
        )

    def test_total_hits_match(self):
        query = self.search()

        self.assertEqual(3, query.match("channel", "the-shop").execute().total_hits)
        self.assertEqual(2, query.match("channel", "the-sale").execute().total_hits)
        self.assertEqual(2, query.match("channel", "the-end").execute().total_hits)

    def test_total_hits_match_and(self):
        query = self.search()

        self.assertEqual(2, query.match("channel", "the-shop").match("country", "DE").execute().total_hits)

    def test_total_hits_match_or(self):
        query = self.search()
        self.assertEqual(5, (query.match("channel", "the-shop") | query.match("country", "GB")).execute().total_hits)


if __name__ == "__main__":
    unittest.main()
