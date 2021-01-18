import json
from typing import Optional, List, Iterable, Union, Tuple, TextIO, Sequence, Mapping

from .search import Search


class SearchPrintWrapper:

    def __init__(self, search: Search):
        self.search = search

    def body(self, indent=2, file=None):
        print(json.dumps(self.search.to_body(), indent=indent), file=file)
        return self

    def response(self, indent=2, file=None):
        print(json.dumps(self.search.response, indent=indent), file=file)
        return self
