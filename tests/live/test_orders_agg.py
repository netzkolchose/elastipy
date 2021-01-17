import datetime
import json
import time
import unittest

import elasticsearch

from elastipy import Search, query

from tests import data
from tests.live.base import TestCase


class TestOrdersAggregations(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.orders.orders1, data.orders.OrderExporter)

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter().delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME)

    def test_orders_terms_sku(self):
        q = self.search()
        agg_sku_count = q.agg_terms(field="sku")
        agg_sku_qty = agg_sku_count.metric_sum(field="quantity", return_self=True)

        #q.dump_body()
        q.execute()#.dump()

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
        q = self.search()
        agg_sku = q.agg_terms(field="sku")
        agg_channel = agg_sku.agg_terms(field="channel")
        agg_qty = agg_channel.metric_sum(field="quantity", return_self=True)

        q.execute()# .dump()

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
        q = self.search()
        agg_sku = q.agg_terms(field="sku")
        agg_channel = agg_sku.aggregation("terms", field="channel")
        agg_country = agg_channel.aggregation("terms", field="country")
        agg_qty = agg_country.metric("sum", field="quantity")

        q.execute()#.dump()

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
        #agg_qty.dump_table()

    def test_orders_filter(self):
        # The filter agg has a special request format and it's response is single-bucket style
        # and we test for support of Queries as parameters
        aggs = [
            self.search().agg_filter(filter={"term": {"sku": "sku-1"}})
                .metric_sum("qty", field="quantity", return_self=True),
            self.search().agg_filter(filter=query.Term(field="sku", value="sku-1"))
                .metric_sum("qty", field="quantity", return_self=True),
        ]
        for agg in aggs:
            #q.dump_body()
            agg.execute()#.dump()

            #agg.dump_table()
            self.assertEqual(
                [
                    ["a0", "a0.doc_count", "qty"],
                    ["a0", 4, 7]
                ],
                list(agg.rows())
            )
            self.assertEqual(
                {
                    "a0": 7,
                },
                agg.to_dict()
            )

    def test_orders_filters(self):
        # filters also support Query parameters
        # and it's bucket response is not list but dict
        aggregations = [
            self.search().agg_filters("group", filters={
                "group1": {"term": {"sku": "sku-1"}},
                "group2": {"term": {"sku": "sku-2"}},
            }),
            self.search().agg_filters("group", filters={
                "group1": query.Term("sku", "sku-1"),
                "group2": query.Bool(must=[query.Term("sku", "sku-2")]),
            }),
        ]
        for agg in aggregations:
            agg.execute()

            self.assertEqual(
                [
                    ["group", "group.doc_count"],
                    ["group1", 4],
                    ["group2", 2],
                ],
                list(agg.rows())
            )
            self.assertEqual(
                {
                    "group1": 4,
                    "group2": 2,
                },
                agg.to_dict()
            )

    def test_orders_filters_metric(self):
        # filters also support Query parameters
        # and it's bucket response is not list but dict
        aggregations = [
            self.search().agg_filters("group", filters={
                "group1": {"term": {"sku": "sku-1"}},
                "group2": {"term": {"sku": "sku-2"}},
            }).metric_sum("qty", field="quantity", return_self=True),
            self.search().agg_filters("group", filters={
                "group1": query.Term("sku", "sku-1"),
                "group2": query.Bool(must=[query.Term("sku", "sku-2")]),
            }).metric_sum("qty", field="quantity", return_self=True),
        ]
        for agg in aggregations:
            agg.execute()

            self.assertEqual(
                [
                    ["group", "group.doc_count", "qty"],
                    ["group1", 4, 7],
                    ["group2", 2, 3],
                ],
                list(agg.rows())
            )
            self.assertEqual(
                {
                    "group1": 7,
                    "group2": 3,
                },
                agg.to_dict()
            )

    def test_orders_filters_sub(self):
        # filters also support Query parameters
        # and it's bucket response is not list but dict
        aggregations = [
            self.search().agg_terms("country", field="country").agg_filters("group", filters={
                "group1": {"term": {"sku": "sku-1"}},
                "group2": {"term": {"sku": "sku-2"}},
            }).metric_sum("qty", field="quantity", return_self=True),
            self.search().agg_terms("country", field="country").agg_filters("group", filters={
                "group1": query.Term("sku", "sku-1"),
                "group2": query.Bool(must=[query.Term("sku", "sku-2")]),
            }).metric_sum("qty", field="quantity", return_self=True),
        ]
        for agg in aggregations:
            agg.execute()#.print.dict()#.search.dump_body()

            self.assertEqual(
                [
                    ["country", "country.doc_count", "group", "group.doc_count", "qty"],
                    ["DE", 4, "group1", 2, 4],
                    ["DE", 4, "group2", 2, 3],
                    ["GB", 3, "group1", 2, 3],
                    ["GB", 3, "group2", 0, 0],
                ],
                list(agg.rows())
            )
            self.assertEqual(
                {
                    ("DE", "group1"): 4,
                    ("DE", "group2"): 3,
                    ("GB", "group1"): 3,
                    ("GB", "group2"): 0,
                },
                agg.to_dict()
            )
            self.assertEqual(
                {
                    "DE|group1": 4,
                    "DE|group2": 3,
                    "GB|group1": 3,
                    "GB|group2": 0,
                },
                agg.to_dict(key_separator="|")
            )

    def test_orders_date_histogram(self):
        q = self.search()
        items_per_day = q.agg_date_histogram(field="timestamp", calendar_interval="1d")
        orders_per_day = items_per_day.metric_cardinality(field="order_id", return_self=True)
        #q.dump_body()
        q.execute()#.dump()

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

    def test_orders_string_stats(self):
        q = self.search()
        agg = q.agg_terms(field="country").metric_string_stats(field="sku", show_distribution=True, return_self=True)
        q.execute()#.dump()
        list(agg.dict_rows())
        list(agg.items())

    def test_orders_date_range(self):
        q = self.search()
        agg = q.agg_date_range(ranges=[{"to": "2000-01-02"}, {"from": "2000-01-02", "to": "2000-01-03"}, {"from": "2000-01-03"}])
        # alternative form
        agg2 = q.agg_date_range(ranges=["2000-01-02", "2000-01-03"])
        q.execute()
        for a in (agg, agg2):
            self.assertEqual(
                [2, 1, 4],
                list(a.values()),
            )

    def test_orders_geo_distance(self):
        q = self.search()
        agg = q.agg_geo_distance(
            field="location",
            origin={"lat": 50.9, "lon": 11.5},
            unit="km",
            ranges=[{"to": 100}, {"from": 100, "to": 500}, {"from": 500}]
        )
        # alternative form
        agg2 = q.agg_geo_distance(
            field="location",
            origin={"lat": 50.9, "lon": 11.5},
            unit="km",
            ranges=[100, 500]
        )
        q.execute()
        for a in (agg, agg2):
            self.assertEqual(
                [2, 2, 3],
                list(a.values()),
            )


if __name__ == "__main__":
    unittest.main()
