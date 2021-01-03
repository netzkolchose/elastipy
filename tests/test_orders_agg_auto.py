import datetime
import json
import time
import unittest

import elasticsearch

from elastipy import get_elastic_client, Search, query
from definition.data import AGGREGATION_DEFINITION

from . import data


class TestOrdersAggregationsAuto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        cls.client = get_elastic_client()
        data.export_data(data.orders.orders1, data.orders.OrderExporter, cls.client)
        time.sleep(1.1)  # give time to update index

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter(client=cls.client).delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME, client=self.client)

    def iter_aggs(self, group):
        for agg_type, definition in AGGREGATION_DEFINITION.items():
            if definition["group"] == group:
                yield agg_type, definition

    def create_agg(self, parent, agg_type):
        definition = AGGREGATION_DEFINITION[agg_type]

        params = dict()

        if agg_type == "date_histogram":
            params["calendar_interval"] = "1d"
        if agg_type == "filter":
            params["filter"] = query.Term(field="sku", value="sku-1")
        if agg_type == "filters":
            params["filters"] = {"a": query.Term(field="sku", value="sku-1"), "b": query.Term(field="sku", value="sku-2")}

        for name, param in definition["parameters"].items():
            if param.get("required") and name not in params:
                if name == "field":
                    value = "sku"
                else:
                    raise NotImplementedError(f"No value for {agg_type}.{name}")

                params[name] = value

        return parent.aggregation(agg_type, **params)

    def test_all(self):
        for agg_type, definition in self.iter_aggs("bucket"):
            search = self.search()

            agg = self.create_agg(search, agg_type)

            try:
                search.execute()

                list(agg.items())
                list(agg.dict_rows())

            except BaseException as e:
                search.dump_body()
                print("AGG TYPE", agg_type)
                raise
                #raise AssertionError(
                #    f"{type(e).__name__}: {e} / aggregation type {agg_type}"
                #)


if __name__ == "__main__":
    unittest.main()
