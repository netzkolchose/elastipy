import time

from elastipy import Exporter

from ._helpers import json_data, ExportScope


class TextExporter(Exporter):

    INDEX_NAME = "elastipy---unittest-text"

    MAPPINGS = {
        "properties": {
            "timestamp": {"type": "date"},
            "category": {"type": "keyword"},
            "text": {
                "type": "text",
            },
        }
    }

    def get_document_id(self, data):
        return str(data["timestamp"])


texts = json_data("texts.json")


def export(client):
    return ExportScope(texts, TextExporter, client)
