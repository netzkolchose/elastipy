import os
import time
import json
import pathlib

from elastipy import get_elastic_client


PATH = pathlib.Path(__file__).parent.resolve()


def json_data(filename):
    with open(os.path.join(PATH, filename)) as fp:
        return json.load(fp)


def export_data(json_filename_or_data, ExporterClass, client):
    if isinstance(json_filename_or_data, str):
        json_filename_or_data = json_data(json_filename_or_data)

    exporter = ExporterClass(client=client)
    exporter.update_index()
    exporter.export_list(json_filename_or_data)


class ExportScope:

    def __init__(self, json_filename_or_data, ExporterClass, client):
        self.json_filename_or_data = json_filename_or_data
        self.ExporterClass = ExporterClass
        self.client = client

    def __enter__(self):
        export_data(self.json_filename_or_data, self.ExporterClass, self.client)
        time.sleep(1.1)  # wait for index refresh
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ExporterClass(client=self.client).delete_index()
        self.client.close()
