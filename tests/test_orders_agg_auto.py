"""
This tries out all defined aggregations
and runs the .to_dict() and .dict_rows() methods to see if the visitor can walk the tree
"""
import re
import datetime
import json
import time
import unittest
import warnings

from elastipy import get_elastic_client, Search, query
from definition.data import AGGREGATION_DEFINITION

from . import data


class TestOrdersAggregationsAuto(unittest.TestCase):
    """
    Auto-generates all combinations of aggregations (which are defined in the yaml files)
    and tests the Aggregation.to_dict() and dict_rows() methods
    """
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

    def iter_searches(self, search):
        """
        generate all Search instances we want to test

        :param search:
        :return:
        """
        # all metrics at top-level
        for agg_type, definition in self.iter_aggs("metric"):
            s = search.copy()
            self.create_agg(s, agg_type)
            yield s

        # all buckets at top-level
        for agg_type, definition in self.iter_aggs("bucket"):
            s = search.copy()
            self.create_agg(s, agg_type)
            yield s

        # buckets with metrics on top
        for agg_type, definition in self.iter_aggs("bucket"):
            for agg_type2, definition2 in self.iter_aggs("metric"):
                s = search.copy()
                agg = self.create_agg(s, agg_type)
                if not agg:
                    continue
                self.create_agg(agg, agg_type2)
                yield s

        # nested buckets with metrics on top
        for agg_type1, _ in self.iter_aggs("bucket"):
            for agg_type2, _ in self.iter_aggs("bucket"):
                for agg_type3, _ in self.iter_aggs("metric"):
                    s = agg = search.copy()
                    if agg:
                        for agg_type in (agg_type1, agg_type2, agg_type3):
                            if agg:
                                agg = self.create_agg(agg, agg_type)
                        yield s

    def create_agg(self, parent, agg_type):
        definition = AGGREGATION_DEFINITION[agg_type]

        params = dict()

        if agg_type in ("geo_bounds", "geo_centroid", "children"):
            warnings.warn(f"{agg_type} tests currently not supported")
            return

        if agg_type == "date_histogram":
            params["calendar_interval"] = "1d"
        if agg_type == "filter":
            params["filter"] = query.Term(field="sku", value="sku-1")
        if agg_type in ("filters", "adjacency_matrix"):
            params["filters"] = {"a": query.Term(field="sku", value="sku-1"), "b": query.Term(field="sku", value="sku-2")}
        if agg_type == "composite":
            params["sources"] = [
                {"sku": {"terms": {"field": "sku"}}},
                {"country": {"terms": {"field": "country"}}},
            ]
            # TODO: currently breaks the visitor because bucket keys are dictionaries
            warnings.warn(f"{agg_type} tests currently not supported")
            return
        if agg_type == "date_range":
            params["ranges"] = [
                {"from": "now-1M/M"},
                {"to": "now/M"},
            ]

        if agg_type == "matrix_stats":
            params["fields"] = ["quantity", "item_line_index"]
        if agg_type == "percentile_ranks":
            params["values"] = [1, 50, 99]
        if agg_type == "rate":
            params["unit"] = "d"
        if agg_type == "scripted_metric":
            params.update({
                "init_script": "state.something = 0",
                "map_script": "state.something += 1",
                "combine_script": "return state.something",
                "reduce_script": "double something = 0; for (s in states) { something += s} return something",
            })
        if agg_type == "string_stats":
            params["field"] = "sku"
        if agg_type == "t_test":
            params.update({
                "a.field": "quantity",
                "b.field": "item_line_index",
                "type": "paired",
            })
        if agg_type == "top_metrics":
            params["metrics"] = {"field": "quantity"}
        if agg_type == "weighted_avg":
            params.update({
                "value.field": "quantity",
                "weight.field": "item_line_index",
            })

        for name, param in definition["parameters"].items():
            if param.get("required") and name not in params:
                if name == "field":
                    if definition["group"] == "metric":
                        value = "quantity"
                    else:
                        value = "sku"
                elif name == "size":
                    value = 10
                else:
                    raise NotImplementedError(f"No value for {agg_type}.{name}")

                params[name] = value

        return parent.aggregation(agg_type, **params)

    def test_all(self):
        for search in self.iter_searches(self.search()):
            if not search._aggregations:
                continue

            # TODO: actually we need some interface for that
            agg = search._aggregations[-1]
            #print(search._aggregations)
            try:
                search.execute()

                list(agg.items())
                if not agg.is_metric() or agg.parent:
                    list(agg.dict_rows())

            except BaseException as e:
                match = re.match(r".*unable to parse BaseAggregationBuilder with name \[(.*)\].*", str(e))
                if match:
                    warnings.warn(f"aggregation '{match.groups()[0]}' not supported by elasticsearch backend")
                    continue

                do_raise = True
                agg_types = list(map(lambda a: a.type, search._aggregations))
                if "scripted_metric" in agg_types:
                    for agg_type in agg_types:
                        if agg_type in (
                                "date_histogram", "auto_date_histogram", "date_range", "filter", "filters"
                        ):
                            # probably needs a min_doc_count=0
                            warnings.warn(
                                f"TODO: scripted_metric execution fails on top of date and filter aggregations"
                            )
                            do_raise = False
                            break
                if not do_raise:
                    continue

                print("-"*10)
                if search._response:
                    search.dump_response()
                print("-"*10)
                search.dump_body()
                print("AGGREGATIONS", search._aggregations)
                raise
                #raise AssertionError(
                #    f"{type(e).__name__}: {e} / aggregation type {agg_type}"
                #)


if __name__ == "__main__":
    unittest.main()
