import os
import json
import time
import unittest

import elasticsearch

from elastipy import Search, query

from tests import data
from tests.live.base import TestCase


class TestTextHighlight(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = int(1e5)
        data.export_data(data.texts.texts, data.texts.TextExporter)

    @classmethod
    def tearDownClass(cls):
        data.texts.TextExporter().delete_index()

    def search(self):
        return Search(index=data.texts.TextExporter.INDEX_NAME)

    def test_highlight(self):
        result = (
            self.search()
            .param.rest_total_hits_as_int(True)
            .match("text", "much")
            .sort("timestamp")
            .highlight("text")
            .execute()
        )
        self.assertEqual(
            [
                ["A text with <em>much</em> more meaning"],
                ["A text with <em>much</em> less meaning"],
            ],
            [d["highlight"]["text"] for d in result["hits"]["hits"]]
        )

    def test_highlight_global_and_field(self):
        result = (
            self.search()
            .param.rest_total_hits_as_int(True)
            .match("text", "much")
            .term("category", "cat1")
            .sort("timestamp")
            # set global highlight params
            .highlight(pre_tags="<EM>", post_tags="</EM>")
            # set field params
            .highlight("text", pre_tags="<b>", post_tags="</b>")
            # category keeps global params
            .highlight("category")
            .execute()
        )
        self.assertEqual(
            [
                {
                    "text": ["A text with <b>much</b> more meaning"],
                    "category": ["<EM>cat1</EM>"],
                },
                {
                    "text": ["A text with <b>much</b> less meaning"],
                    "category": ["<EM>cat1</EM>"],
                }

            ],
            [d["highlight"] for d in result["hits"]["hits"]]
        )

    def test_highlight_extra_query(self):
        result = (
            self.search()
            .param.rest_total_hits_as_int(True)
            .match("text", "much")
            .sort("timestamp")
            .highlight(
                "text",
                highlight_query=query.Match("text", "more") | query.Match("text", "meaning")
            )
            .execute()
        )
        self.assertEqual(
            [
                ["A text with much <em>more</em> <em>meaning</em>"],
                ["A text with much less <em>meaning</em>"],
            ],
            [d["highlight"]["text"] for d in result["hits"]["hits"]]
        )


if __name__ == "__main__":
    unittest.main()
