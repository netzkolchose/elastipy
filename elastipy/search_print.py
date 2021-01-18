import json
from typing import Optional, List, Iterable, Union, Tuple, TextIO, Sequence, Mapping

from .search import Search


class SearchPrintWrapper:

    def __init__(self, search: Search):
        self.search = search

    def query(self, indent=2, file=None):
        print(json.dumps(self.search.get_query().to_dict(), indent=indent), file=file)

    def body(self, indent=2, file=None):
        print(json.dumps(self.search.to_body(), indent=indent), file=file)

    def request(self, indent=2, file=None):
        print(json.dumps(self.search.to_request(), indent=indent), file=file)

    def response(self, indent=2, file=None):
        print(json.dumps(self.search.response, indent=indent), file=file)
