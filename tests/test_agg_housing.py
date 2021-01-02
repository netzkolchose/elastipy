import os
import json
import time
import unittest

from elastipy import Search, aggregation


class TestAggregationHousing(unittest.TestCase):

    def test_factory(self):
        self.assertEqual(
            aggregation.special.Filter,
            type(Search().agg_filter(filter={"term": {"a": {"value": "b"}}}))
        )

    def test_is_metric(self):
        self.assertTrue(
            Search().metric_sum(field="a").is_metric()
        )


if __name__ == "__main__":
    unittest.main()
