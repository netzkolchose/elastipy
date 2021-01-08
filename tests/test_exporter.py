import os
import json
import time
import unittest

from elastipy import Search, query, Exporter


class TestExporter(Exporter):
    INDEX_NAME = "elastipy---unittest-exporter-no-id"
    MAPPINGS = {
        "properties": {
            "id": {"type": "long"},
            "string": {"type": "text"},
            "number": {"type": "float"},
            "tag": {"type": "keyword"},
        }
    }


class TestExporterWithId(TestExporter):
    INDEX_NAME = "elastipy---unittest-exporter-id"

    def get_object_id(self, es_data):
        return es_data["id"]


class TestTheExporter(unittest.TestCase):

    def test_create_update_no_id(self):
        exporter = TestExporter()
        exporter.update_index()
        try:
            exporter.export_list([{"id": 0}, {"id": 1}], refresh=True)
            self.assertEqual(2, exporter.search().execute().total_hits)

            exporter.export_list([{"id": 2}], refresh=True)
            self.assertEqual(3, exporter.search().execute().total_hits)

            exporter.export_list([{"id": 0, "string": "hello"}, {"id": 1, "tag": "python"}], refresh=True)
            response = exporter.search().sort("id").execute()
            self.assertEqual(5, response.total_hits)

            exporter.export_list([{"id": 0}, {"id": 1}], refresh=True)
            response = exporter.search().sort("id").execute()
            self.assertEqual(7, response.total_hits)

        finally:
            exporter.delete_index()

    def test_create_update_id(self):
        exporter = TestExporterWithId()
        exporter.update_index()
        try:
            exporter.export_list([{"id": 0}, {"id": 1}], refresh=True)
            self.assertEqual(2, exporter.search().execute().total_hits)

            exporter.export_list([{"id": 2}], refresh=True)
            self.assertEqual(3, exporter.search().execute().total_hits)

            exporter.export_list([{"id": 0, "string": "hello"}, {"id": 1, "tag": "python"}], refresh=True)
            response = exporter.search().sort("id").execute()
            self.assertEqual(3, response.total_hits)
            self.assertEqual("hello", response.documents[0]["string"])
            self.assertEqual("python", response.documents[1]["tag"])

            exporter.export_list([{"id": 0}, {"id": 1}], refresh=True)
            response = exporter.search().sort("id").execute()
            self.assertEqual(3, response.total_hits)
            self.assertNotIn("string", response.documents[0])
            self.assertNotIn("tag", response.documents[1])

        finally:
            exporter.delete_index()


if __name__ == "__main__":
    unittest.main()
