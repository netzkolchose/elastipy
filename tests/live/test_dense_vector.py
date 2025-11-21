import datetime
from copy import copy
from io import StringIO
import unittest

import numpy as np

from elastipy import Search, query, Exporter
from tests.live.base import TestCase, requires_elasticsearch


# see: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector
class DenseVector3Exporter(Exporter):
    INDEX_NAME = "elastipy---unittest-dense-vector"
    MAPPINGS = {
        "properties": {
            "key": {"type": "keyword"},
            "vector": {
                "type": "dense_vector",
                "dims": 3,
                "similarity": "cosine",
            },
        }
    }


@requires_elasticsearch(9)
class TestDenseVector(TestCase):

    def test_dense_vector(self):
        exporter = DenseVector3Exporter()
        try:
            exporter.export_list([
                {"key": "0", "vector": [1, 0, 0]},
                {"key": "1", "vector": [0, 1, 0]},
                {"key": "2", "vector": [0, 0, 1]},
                {"key": "01", "vector": [1, 1, 0]},
                {"key": "12", "vector": [0, 1, 1]},
            ], refresh=True)

            r = (
                exporter.search()
                .knn(field="vector", query_vector=[1, .5, .1])
                .execute()
            )
            self.assertEqual(
                ["01", "0", "1", "12", "2"],
                [d["key"] for d in r.documents]
            )
        finally:
            exporter.delete_index()


    def test_dense_vector_numpy(self):
        exporter = DenseVector3Exporter()
        try:
            exporter.export_list([
                {"key": "0", "vector": np.array([1, 0, 0], dtype=np.float32)},
                {"key": "1", "vector": np.array([0, 1, 0], dtype=np.float64)},
                {"key": "2", "vector": np.array([0, 0, 1], dtype=np.int8)},
                {"key": "01", "vector": np.array([1, 1, 0], dtype=np.int16)},
                {"key": "12", "vector": np.array([0, 1, 1], dtype=np.int32)},
            ], refresh=True)

            r = (
                exporter.search()
                .knn(field="vector", query_vector=np.array([1, .5, .1], dtype=np.float16))
                .execute()
            )
            self.assertEqual(
                ["01", "0", "1", "12", "2"],
                [d["key"] for d in r.documents]
            )
        finally:
            exporter.delete_index()


if __name__ == "__main__":
    unittest.main()
