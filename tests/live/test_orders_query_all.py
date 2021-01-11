import os
import json
import time
import unittest

import elasticsearch

from elastipy import Search, query
from elastipy.query import factory
from definition.data import QUERY_DEFINITION

from tests import data


class TestOrdersQueryAuto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.orders.orders1, data.orders.OrderExporter)

    @classmethod
    def tearDownClass(cls):
        data.orders.OrderExporter().delete_index()

    def search(self):
        return Search(index=data.orders.OrderExporter.INDEX_NAME)

    def iter_searches(self):
        for s in self.iter_queries():
            yield s
            for s2 in self.iter_queries(s):
                yield s2

    def iter_queries(self, q=None, ):
        if q is None:
            q = self.search()

        yield q.copy().match_all()
        yield q.copy().match_none()
        yield q.copy().match("sku", query="sku-1")
        yield q.copy().query_string("sku: sku-*")
        yield q.copy().range(field="timestamp", gte="2000-01-02", lt="2000-01-04")
        yield q.copy().term(field="country", value="DE")
        yield q.copy().terms(field="country", value=["DE", "GB"])
        yield q.copy().bool(must=query.Term(field="sku", value="sku-2"))
        yield q.copy().bool(must_not=query.Term(field="sku", value="sku-2"))
        yield q.copy().bool(should=query.Term(field="sku", value="sku-2"))
        yield q.copy().bool(filter=query.Term(field="sku", value="sku-2"))

    def test_all(self):
        for search in self.iter_searches():
            try:
                count = search.execute().total_hits
            except BaseException:
                search.dump_body()
                print(search.get_query())
                raise

            # print(count, search.get_query())


if __name__ == "__main__":
    unittest.main()
