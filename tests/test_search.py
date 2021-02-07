import os
import json
import time
import unittest
from io import StringIO

from elastipy import Search, query, connections
from .mock_client import MockElasticsearch


class TestSearch(unittest.TestCase):

    def test_index(self):
        self.assertEqual(
            "Bob!",
            Search(index="Bob!").get_index()
        )

    def test_client(self):
        client = MockElasticsearch()
        self.assertEqual(
            client,
            Search(client=client).get_client()
        )

        self.assertEqual(
            connections.get("default"),
            Search(client=None).get_client()
        )

        connections.set("mock", client)
        self.assertEqual(
            client,
            Search(client="mock").get_client()
        )

    def test_execute_client(self):
        client = MockElasticsearch()
        Search(client=client).execute()
        self.assertEqual(1, len(client.search_calls))

    def test_change_client(self):
        client = MockElasticsearch()
        s = Search(client=client)
        self.assertEqual(client, s.get_client())

        s2 = s.client("default")
        self.assertEqual(connections.get(), s2.get_client())
        self.assertNotEqual(s, s2)

    def test_execute_callable(self):
        called = False

        def search(**kwargs):
            nonlocal called
            called = True
            return {}

        Search(client=search).execute()
        self.assertTrue(called)

    def test_execute_wrong_type(self):

        class NoClient:
            pass

        s = Search(client=NoClient())
        with self.assertRaises(TypeError):
            s.execute()

    def test_no_response(self):
        with self.assertRaises(ValueError):
            _ = Search().response

    def test_response(self):
        s = Search()
        s.set_response({"hits": {"total": 23}})
        self.assertEqual(
            23,
            s.response.total_hits
        )

    def test_add_body(self):
        s = Search()
        s._add_body("here.there", 23)
        self.assertEqual(
            {
                "query": {"match_all": {}},
                "here": {"there": 23},
            },
            s.to_body(),
        )

        s = Search()
        s._add_body(["here", "there"], 23)
        self.assertEqual(
            {
                "query": {"match_all": {}},
                "here": {"there": 23},
            },
            s.to_body(),
        )

        s = Search()
        s._add_body("here.there", [])
        with self.assertRaises(ValueError):
            s._add_body("here.there.sub", 1)



if __name__ == "__main__":
    unittest.main()
