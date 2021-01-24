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

    def test_matrix_1d(self):
        s = self.search()
        agg = s\
            .agg_terms("channel", field="channel", order="_key")

        s.execute()

        names, keys, matrix = agg.to_matrix()
        self.assertEqual(
            ["channel"],
            names
        )
        self.assertEqual(
            [
                ["the-end", "the-sale", "the-shop"],
            ],
            keys
        )
        self.assertEqual(
            [
                2, 2, 3
            ],
            matrix
        )

    def test_matrix_1d_metric(self):
        s = self.search()
        agg = s \
            .agg_terms("channel", field="channel", order="_key") \
            .metric_sum("qty", field="quantity", return_self=True)
        s.execute()

        names, keys, matrix = agg.to_matrix()
        self.assertEqual(
            ["channel"],
            names
        )
        self.assertEqual(
            [
                ["the-end", "the-sale", "the-shop"],
            ],
            keys
        )
        self.assertEqual(
            [
                6, 4, 5
            ],
            matrix
        )

    def test_matrix_1d_metric_only(self):
        s = self.search()
        agg = s \
            .metric_sum("qty", field="quantity", return_self=True)
        s.execute()

        names, keys, matrix = agg.to_matrix()
        self.assertEqual(
            ["qty"],
            names
        )
        self.assertEqual(
            [
                ["qty"],
            ],
            keys
        )
        self.assertEqual(
            [
                15
            ],
            matrix
        )

    def test_matrix_2d(self):
        s = self.search()
        agg = s \
            .agg_terms("channel", field="channel", order="_key") \
            .agg_terms("sku", field="sku", order="_key", min_doc_count=0) \
            # note, we use min_doc_count=0 to have sku-2 already included
        #   in the first channel bucket, so the keys are sorted properly

        s.execute()
        #print(json.dumps(s.response.aggregations, indent=2))

        names, keys, matrix = agg.to_matrix()
        self.assertEqual(
            ["channel", "sku"],
            names
        )
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

    def test_matrix_2d_drop(self):
        s = self.search()
        agg = s \
            .agg_terms("channel", field="channel", order="_key") \
            .agg_terms("sku", field="sku", order="_key", min_doc_count=0) \
            # note, we use min_doc_count=0 to have sku-2 already included
        #   in the first channel bucket, so the keys are sorted properly

        s.execute()

        names, keys, matrix = agg.to_matrix(exclude="sku-1")
        self.assertEqual(
            ["channel", "sku"],
            names
        )
        self.assertEqual(
            [
                ["the-end", "the-sale", "the-shop"],
                ["sku-2", "sku-3"],
            ],
            keys
        )
        self.assertEqual(
            [
                [0, 1],  # the end
                [1, 0],  # the sale
                [1, 0],  # the shop
            ],
            matrix
        )

        names, keys, matrix = agg.to_matrix(exclude=("sku-2", "the-shop",))
        self.assertEqual(
            ["channel", "sku"],
            names
        )
        self.assertEqual(
            [
                ["the-end", "the-sale"],
                ["sku-1", "sku-3"],
            ],
            keys
        )
        self.assertEqual(
            [
                [1, 1],  # the end
                [1, 0],  # the sale
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

        names, keys, matrix = agg.to_matrix()
        self.assertEqual(
            ["channel", "sku"],
            names
        )
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
            .agg_terms("channel", field="channel") \
            .agg_terms("sku", field="sku") \
            .agg_terms("country", field="country") \
            .metric_sum("qty", field="quantity", return_self=True)

        s.execute()

        for default in (None, 0, 23):
            names, keys, matrix = agg.to_matrix(sort=True, default=default)
            self.assertEqual(
                ["channel", "sku", "country"],
                names
            )
            self.assertEqual(
                [
                    ["the-end", "the-sale", "the-shop"],
                    ["sku-1", "sku-2", "sku-3"],
                    ["DE", "GB"],
                ],
                keys
            )
            N = default
            self.assertEqual(
                [
                    [               # the end
                        [N, 1],     # sku-1 / country
                        [N, N],
                        [N, 5],
                    ],
                    [               # the sale
                        [3, N],
                        [1, N],
                        [N, N],
                    ],
                    [               # the shop
                        [1, 2],
                        [2, N],
                        [N, N],
                    ],
                ],
                matrix
            )

    def test_matrix_key_sort(self):
        s = self.search()
        agg = s \
            .agg_terms("channel", field="channel") \
            .agg_terms("sku", field="sku") \
            .agg_terms("country", field="country")

        s.execute()

        def _assert(sort, expected_keys):
            names, keys, matrix = agg.to_matrix(sort=sort)
            self.assertEqual(
                expected_keys,
                keys
            )

        _assert(None, [
            ['the-shop', 'the-end', 'the-sale'],
            ['sku-1', 'sku-2', 'sku-3'],
            ['DE', 'GB']
        ])

        _assert(True, [
            ["the-end", "the-sale", "the-shop"],
            ["sku-1", "sku-2", "sku-3"],
            ["DE", "GB"],
        ])

        _assert("-sku", [
            ['the-shop', 'the-end', 'the-sale'],
            ["sku-3", "sku-2", "sku-1"],
            ["DE", "GB"],
        ])

        _assert(("-channel", "-sku", "country"), [
            ["the-shop", "the-sale", "the-end"],
            ["sku-3", "sku-2", "sku-1"],
            ["DE", "GB"],
        ])


if __name__ == "__main__":
    unittest.main()
