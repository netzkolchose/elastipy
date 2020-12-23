import time

from elastipy import Exporter

from ._helpers import json_data, ExportScope


class OrderExporter(Exporter):

    INDEX_NAME = "elastipy---unittest-order"

    MAPPINGS = {
        "properties": {
            "timestamp": {"type": "date"},
            "channel": {"type": "keyword"},
            "country": {"type": "keyword"},
            "order_id": {"type": "keyword"},
            "item_line_index": {"type": "integer"},
            "sku": {"type": "keyword"},
            "quantity": {"type": "integer"},
        }
    }

    def get_object_id(self, data):
        return "%s-%s" % (data["order_id"], data["item_line_index"])

    def transform_object_data(self, data):
        basis = data.copy()
        items = basis.pop("items")
        elastic_data = []
        for i, item in enumerate(items):
            item = item.copy()
            item["item_line_index"] = i
            item.update(basis)
            elastic_data.append(item)
        return elastic_data


orders1 = json_data("orders1.json")


def export1(client):
    return ExportScope(orders1, OrderExporter, client)
