import os
import json
import time
import unittest

from elastipy import Search, aggregation


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
                .search.body["aggregations"]["a0"]["date_histogram"]["field"],
        )
        self.assertEqual(
            "blabla",
            Search(timestamp_field="blabla").agg_auto_date_histogram() \
                .search.body["aggregations"]["a0"]["auto_date_histogram"]["field"],
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


if __name__ == "__main__":
    unittest.main()
