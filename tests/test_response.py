import os
import json
import time
import unittest
from io import StringIO

from elastipy import Search, Response


RESPONSE1 = {
    "took": 0,
    "timed_out": False,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": 2,
        "max_score": 1.5,
        "hits": [
            {
                "_index": "index-1",
                "_type": "_doc",
                "_id": "LX9-GncBeebHNMb694fe",
                "_score": 1.5,
                "_source": {
                    "name": "Bob!",
                    "slack": 1000.,
                }
            },
            {
                "_index": "index-2",
                "_type": "_doc",
                "_id": "bX9-GncBeebHNMb694fe",
                "_score": 1.,
                "_source": {
                    "name": "Stang!",
                    "slack": 100.,
                }
            }
        ]
    },
    "aggregations": {
        "names": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
                {
                    "key": "Bob!",
                    "doc_count": 1
                },
                {
                    "key": "Stang!",
                    "doc_count": 1
                }
            ]
        }
    }
}


class TestResponse(unittest.TestCase):

    def test_response_properties(self):
        r = Response(**RESPONSE1)
        self.assertEqual(RESPONSE1["hits"]["total"], r.total_hits)
        self.assertEqual(RESPONSE1["aggregations"], r.aggregations)
        self.assertEqual(RESPONSE1["hits"], r.hits)
        self.assertEqual(
            [
                {
                    "name": "Bob!",
                    "slack": 1000.,
                },
                {
                    "name": "Stang!",
                    "slack": 100.,
                }
            ],
            r.documents,
        )

    def test_dump_response(self):
        file = StringIO()
        Response(**RESPONSE1).dump(file=file)
        file.seek(0)
        self.assertEqual(
            json.dumps(RESPONSE1, indent=2),
            file.read().rstrip(),
        )

    def test_dump_aggregations(self):
        file = StringIO()
        Response(**RESPONSE1).dump.aggregations(file=file)
        file.seek(0)
        self.assertEqual(
            json.dumps(RESPONSE1["aggregations"], indent=2),
            file.read().rstrip(),
        )

    def test_dump_documents(self):
        file = StringIO()
        Response(**RESPONSE1).dump.documents(file=file)
        file.seek(0)
        self.assertEqual(
            json.dumps([
                {
                    "name": "Bob!",
                    "slack": 1000.,
                },
                {
                    "name": "Stang!",
                    "slack": 100.,
                }
            ], indent=2),
            file.read().rstrip(),
        )

    def test_dump_table(self):
        file = StringIO()
        Response(**RESPONSE1).dump.table(file=file, bars=False, ascii=True, score=False)
        file.seek(0)
        self.assertEqual(strip_each_line(
            """
            name   | slack
            -------+-------
            Bob!   | 1000.0
            Stang! |  100.0
            """),
            strip_each_line(file.read().rstrip()),
        )

        file = StringIO()
        Response(**RESPONSE1).dump.table(file=file, bars=False, ascii=True)
        file.seek(0)
        self.assertEqual(strip_each_line(
            """
            _score | name   | slack
            -------+--------+-------
            1.5    | Bob!   | 1000.0
            1.0    | Stang! |  100.0
            """),
            strip_each_line(file.read().rstrip()),
        )


def strip_each_line(text: str):
    return "\n".join(line.strip() for line in text.splitlines()).strip()


if __name__ == "__main__":
    unittest.main()
