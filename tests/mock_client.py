import json

from elasticsearch.serializer import JSONSerializer
from elasticsearch import VERSION


if VERSION[0] == 7:

    class MockElasticsearch:

        def __init__(self):
            self.transport = Transport(self)
            self.indices = FakeIndices(self)
            self.bulk_calls = []
            self.search_calls = []

        def exists(self, index, id):
            return False

        def bulk(self, *args, **kwargs):
            if args:
                body = args[0]
            else:
                body = kwargs["body"]

            self.bulk_calls.append(list(
                json.loads(s) for s in body.splitlines()
            ))

            return {
                "items": []
            }

        def dump_bulk(self):
            for i, bc in enumerate(self.bulk_calls):
                print(f"--- bulk call #{i+1} ---")
                for d in bc:
                    print(json.dumps(d, indent=2))

        def search(self, **kwargs):
            self.search_calls.append(kwargs)
            return {
                "took": 0,
                "timed_out": False,
                "_shards": {
                    "total": 1,
                    "successful": 1,
                    "skipped": 0,
                    "failed": 0
                },
                "hits": {
                    "total": 0,
                    "max_score": None,
                    "hits": []
                }
            }


    class Transport:
        def __init__(self, parent):
            self.parent = parent
            self.serializer = JSONSerializer()


    class FakeIndices:
        def __init__(self, parent):
            self.parent = parent
            self._mapping = dict()

        def get_mapping(self, *args, **kwargs):
            return self._mapping

        def put_mapping(self, *args, **kwargs):
            self._mapping = kwargs["body"]


elif VERSION[0] == 8:

    class MockElasticsearch:

        def __init__(self):
            self.indices = FakeIndices(self)
            self._client = FakeClient(self)
            self.bulk_calls = []
            self.search_calls = []

        def exists(self, index, id):
            return False

        def bulk(self, *args, **kwargs):
            return self._client.bulk(*args, **kwargs)

        def dump_bulk(self):
            for i, bc in enumerate(self.bulk_calls):
                print(f"--- bulk call #{i+1} ---")
                for d in bc:
                    print(json.dumps(d, indent=2))

        def search(self, **kwargs):
            self.search_calls.append(kwargs)
            return {
                "took": 0,
                "timed_out": False,
                "_shards": {
                    "total": 1,
                    "successful": 1,
                    "skipped": 0,
                    "failed": 0
                },
                "hits": {
                    "total": 0,
                    "max_score": None,
                    "hits": []
                }
            }

        def options(self):
            return self._client


    class FakeClient:

        def __init__(self, parent):
            self.parent = parent
            self.transport = Transport(parent)

        def bulk(self, *args, **kwargs):
            self.parent.bulk_calls.append([
                json.loads(o.decode())
                for o in kwargs["operations"]
            ])

            class Response:
                def __init__(self):
                    self.body = {
                        "items": [],
                    }

            return Response()


    class Transport:

        def __init__(self, parent):
            self.parent = parent
            self.serializer = JSONSerializer()
            self.serializers = Serializers()


    class Serializers:

        def get_serializer(self, format):
            return JSONSerializer()


    class FakeIndices:
        def __init__(self, parent):
            self.parent = parent
            self._mapping = dict()

        def get_mapping(self, *args, **kwargs):
            return self._mapping

        def put_mapping(self, *args, **kwargs):
            self._mapping = kwargs["body"]
