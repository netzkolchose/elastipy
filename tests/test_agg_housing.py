import os
import json
import time
import unittest

from elastipy import Search, aggregation
from elastipy.aggregation.visitor import Visitor


class TestAggregationHousing(unittest.TestCase):

    def test_name_type(self):
        agg = Search().aggregation("terms")
        self.assertEqual("terms", agg.type)
        self.assertEqual("a0", agg.name)

        agg = Search().aggregation("boris", "terms")
        self.assertEqual("terms", agg.type)
        self.assertEqual("boris", agg.name)

    def test_factory(self):
        self.assertEqual(
            aggregation.special.Filter,
            type(Search().agg_filter(filter={"term": {"a": {"value": "b"}}}))
        )

    def test_is_metric(self):
        self.assertTrue(
            Search().metric_sum(field="a", return_self=True).is_metric()
        )

    def test_default_timestamp(self):
        self.assertEqual(
            "blabla",
            Search(timestamp_field="blabla").agg_date_histogram(calendar_interval="1d") \
                .search.to_body()["aggregations"]["a0"]["date_histogram"]["field"],
        )
        self.assertEqual(
            "blabla",
            Search(timestamp_field="blabla").agg_auto_date_histogram() \
                .search.to_body()["aggregations"]["a0"]["auto_date_histogram"]["field"],
        )

    def test_ranges_auto_conversion(self):
        self.assertEqual(
            [
                {"to": "2000"},
                {"from": "2000", "to": "2001"},
                {"from": "2001"},
            ],
            Search().agg_date_range(ranges=["2000", "2001"]).to_body()["ranges"]
        )

    def test_order_convenience(self):
        self.assertEqual(
            Search().agg_terms(field="a", order={"metric": "asc"}).to_body(),
            Search().agg_terms(field="a", order="metric").to_body(),
        )
        self.assertEqual(
            Search().agg_terms(field="a", order={"metric": "desc"}).to_body(),
            Search().agg_terms(field="a", order="-metric").to_body(),
        )
        self.assertEqual(
            Search().agg_terms(field="a", order={"_count": "desc"}).to_body(),
            Search().agg_terms(field="a", order="-_count").to_body(),
        )

    def test_visitor_iter_tree(self):
        agg = Search() \
            .agg_terms("1", field="") \
            .agg_terms("2", field="") \
            .metric_sum("2.1", field="") \
            .agg_terms("3", field="") \
            .metric_sum("3.1", field="") \
            .metric_sum("3.2", field="")

        agg2 = agg.search._aggregations[1]
        self.assertEqual("2", agg2.name)
        agg2.agg_terms("2.2", field="").agg_terms("2.2.1", field="")

        self.assertEqual(
            ["3", "3.1", "3.2"],
            [a.name for a in Visitor(agg).iter_tree(depth_first=True)]
        )

        self.assertEqual(
            ["1", "2", "2.1", "3", "3.1", "3.2", "2.2", "2.2.1"],
            [a.name for a in Visitor(agg).iter_tree(root=agg.root, depth_first=True)]
        )

        self.assertEqual(
            ["1", "2", "2.1", "3", "2.2", "3.1", "3.2", "2.2.1"],
            [a.name for a in Visitor(agg).iter_tree(root=agg.root, depth_first=False)]
        )


if __name__ == "__main__":
    unittest.main()
