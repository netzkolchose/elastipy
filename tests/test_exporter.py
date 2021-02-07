import unittest
import datetime
from copy import copy

from elastipy import Exporter

from .mock_client import MockElasticsearch


class TestExporter(Exporter):
    INDEX_NAME = "mock"
    MAPPINGS = {
        "properties": {
            "id": {"type": "long"},
            "string": {"type": "text"},
            "number": {"type": "float"},
            "tag": {"type": "keyword"},
            "timestamp": {"type": "date"},
        }
    }

    timestamp = datetime.datetime(2000, 1, 1)

    def transform_document(self, data):
        data = copy(data)
        data["timestamp"] = self.timestamp
        self.timestamp += datetime.timedelta(seconds=1)
        return data


class TestExporterMock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e9)

    def assertBulkCalls(self, client: MockElasticsearch, *expected_calls: list):
        try:
            self.assertEqual(len(expected_calls), len(client.bulk_calls), "Number of chunks does not match")

            for expected_call, real_call in zip(expected_calls, client.bulk_calls):
                self.assertEqual(
                    expected_call, real_call
                )

        except AssertionError:
            print(f"\nExpected:\n{expected_calls}\n\nGot:\n{client.bulk_calls}")
            raise

    def test_export(self):
        exporter = TestExporter(client=MockElasticsearch())

        exporter.export_list([{"id": 0, "string": "hello"}, {"id": 1, "tag": "python"}])

        self.assertBulkCalls(
            exporter.client,
            [
                {'index': {'_index': 'mock'}},
                {'id': 0, 'string': 'hello', 'timestamp': '2000-01-01T00:00:00'},
                {'index': {'_index': 'mock'}},
                {'id': 1, 'tag': 'python', 'timestamp': '2000-01-01T00:00:01'},
            ]
        )

    def test_export_chunk_size(self):
        exporter = TestExporter(client=MockElasticsearch())

        exporter.export_list([{"id": 0, "string": "hello"}, {"id": 1, "tag": "python"}], chunk_size=1)

        self.assertBulkCalls(
            exporter.client,
            [
                {'index': {'_index': 'mock'}},
                {'id': 0, 'string': 'hello', 'timestamp': '2000-01-01T00:00:00'},
            ],
            [
                {'index': {'_index': 'mock'}},
                {'id': 1, 'tag': 'python', 'timestamp': '2000-01-01T00:00:01'},
            ]
        )


if __name__ == "__main__":
    unittest.main()
