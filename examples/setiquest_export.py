from copy import copy

from helper import Exporter
from setiquest_irc_parser import iter_messages


class IrcExporter(Exporter):
    INDEX_NAME = "elastipy-example-setiquest-irc"

    MAPPINGS = {
        "properties": {
            "timestamp": {"type": "date"},
            "timestamp_weekday": {"type": "keyword"},
            "timestamp_hour": {"type": "integer"},
            "raw_line": {"type": "text"},

            "user": {"type": "keyword"},
            "event": {"type": "keyword"},
            "user_event": {"type": "text"},
            "rename_to": {"type": "keyword"},
            "mode": {"type": "keyword"},
            "topic": {"type": "keyword"},

            "text": {
                "type": "text",
                "analyzer": "stop",
                "term_vector": "with_positions_offsets_payloads",
                "store": True,
                "fielddata": True,
                # "analyzer" : "fulltext_analyzer"
            },
        }
    }

    def get_document_id(self, data: dict):
        return data['timestamp'].strftime("%Y%m%d") + f"-{data['index']}"

    def transform_document(self, data: dict):
        data = copy(data)
        data["timestamp_hour"] = data["timestamp"].hour
        data["timestamp_weekday"] = data["timestamp"].strftime("%w %A")
        return data


if __name__ == "__main__":

    exporter = IrcExporter()
    exporter.delete_index()
    exporter.export_list(iter_messages(), verbose=True, refresh=True)
