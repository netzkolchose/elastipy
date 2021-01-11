import time
from copy import deepcopy

from elastipy import Exporter

from ._helpers import json_data, ExportScope


class NestedOrderExporter(Exporter):

    INDEX_NAME = "elastipy---unittest-nested-order"

    MAPPINGS = {
        "properties": {
            "timestamp": {"type": "date"},
            "channel": {"type": "keyword"},
            "country": {"type": "keyword"},
            "location": {"type": "geo_point"},
            "order_id": {"type": "keyword"},
            "items": {
                "type": "nested",
                "properties": {
                    "sku": {"type": "keyword"},
                    "quantity": {"type": "integer"},
                    "item_line_index": {"type": "integer"},
                }
            },
        }
    }

    def get_document_id(self, data):
        return data["order_id"]

    def transform_document(self, data):
        data = deepcopy(data)
        for i, item in enumerate(data["items"]):
            item["item_line_index"] = i
        return data


orders = json_data("orders.json")


def export(client):
    return ExportScope(orders, NestedOrderExporter, client)
