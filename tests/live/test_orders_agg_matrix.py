import datetime
import json
import time
import unittest

import pandas as pd

from elastipy import Search
from elastipy.aggregation.helper import create_matrix

from tests import data
from tests.live.base import TestCase


class TestOrdersAggregationsMatrix(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.orders.orders1, data.orders.OrderExporter)

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter().delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME)

    def test_create_matrix(self):
        self.assertEqual(
            None,
            create_matrix()
        )
        self.assertEqual(
            [
                None, None, None,
            ],
            create_matrix(3)
        )
        self.assertEqual(
            [
                [None, None],
                [None, None],
                [None, None],
            ],
            create_matrix(3, 2)
        )
        self.assertEqual(
            [
                [
                    [None, None, None, None]
                ],
                [
                    [None, None, None, None]
                ],
            ],
            create_matrix(2, 1, 4)
        )

    def test_matrix_2d(self):
        s = self.search()
        agg = s\
            .agg_terms("channel", field="channel", order="_key") \
            .agg_terms("sku", field="sku", order="_key", min_doc_count=0) \
        # note, we use min_doc_count=0 to have sku-2 already included
        #   in the first channel bucket, so the keys are sorted properly

        s.execute()
        #print(json.dumps(s.response.aggregations, indent=2))

        keys, matrix = agg.to_matrix()
        self.assertEqual(
            [
                ["the-end", "the-sale", "the-shop"],
                ["sku-1", "sku-2", "sku-3"],
            ],
            keys
        )
        self.assertEqual(
            [
                [1, 0, 1],  # the end
                [1, 1, 0],  # the sale
                [2, 1, 0],  # the shop
            ],
            matrix
        )

    def test_matrix_2d_metric(self):
        s = self.search()
        agg = s \
            .agg_terms("channel", field="channel", order="_key") \
            .agg_terms("sku", field="sku", order="_key", min_doc_count=0) \
            .metric_sum("qty", field="quantity", return_self=True)
        # note, we use min_doc_count=0 to have sku-2 already included
        #   in the first channel bucket, so the keys are sorted properly

        s.execute()
        #print(json.dumps(s.response.aggregations, indent=2))

        keys, matrix = agg.to_matrix()
        self.assertEqual(
            [
                ["the-end", "the-sale", "the-shop"],
                ["sku-1", "sku-2", "sku-3"],
            ],
            keys
        )
        self.assertEqual(
            [
                [1, 0, 5],  # the end
                [3, 1, 0],  # the sale
                [3, 2, 0],  # the shop
            ],
            matrix
        )

    def test_matrix_3d_metric(self):
        s = self.search()
        agg = s \
            .agg_terms("channel", field="channel", order="_key") \
            .agg_terms("sku", field="sku", order="_key", min_doc_count=0) \
            .agg_terms("country", field="country", order="_key", min_doc_count=0) \
            .metric_sum("qty", field="quantity", return_self=True)

        s.execute()
        #print(json.dumps(s.response.aggregations, indent=2))
        agg.print.dict()
        keys, matrix = agg.to_matrix()
        self.assertEqual(
            [
                ["the-end", "the-sale", "the-shop"],
                ["sku-1", "sku-2", "sku-3"],
                ["DE", "GB"],
            ],
            keys
        )
        self.assertEqual(
            [
                [               # the end
                    [1, 0],     # sku-1 / country
                    [0, 0],
                    [0, 5],
                ],
                [               # the sale
                    [3, 0],
                    [1, 0],
                    [0, 0],
                ],
                [               # the shop
                    [1, 2],
                    [2, 0],
                    [0, 0],
                ],
            ],
            matrix
        )


if __name__ == "__main__":
    unittest.main()
