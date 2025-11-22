import os
import json
import unittest
from typing import Union, Tuple

from elasticsearch import VERSION


def requires_elasticsearch(version: Union[int, Tuple[int, int, int]]):
    """Decorator to skip tests for specific elasticsearch versions"""
    return unittest.skipIf(
        (isinstance(version, int) and VERSION[0] < version)
        or (isinstance(version, tuple) and VERSION < version),
        f"Test requires elasticsearch v{version}"
    )


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if os.environ.get("ELASTIPY_UNITTEST_SERVER"):
            params = json.loads(os.environ["ELASTIPY_UNITTEST_SERVER"])

            from elastipy import connections
            connections.set("default", params)

