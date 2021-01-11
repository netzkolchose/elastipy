import os
import json
from unittest import TestCase as TestCaseOrg


class TestCase(TestCaseOrg):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if os.environ.get("ELASTIPY_UNITTEST_SERVER"):
            params = json.loads(os.environ["ELASTIPY_UNITTEST_SERVER"])

            from elastipy import connections
            connections.set("default", params)

