import json
from typing import Optional, List, Iterable, Union, Tuple, TextIO, Sequence, Mapping

from .search import Search


class SearchPrintWrapper:

    def __init__(self, search: Search):
        self.search = search

    def __call__(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the complete request parameters as would be accepted
        by ``elasticsearch.Elasticsearch.search()``.
        :param indent: the json indentation, defaults to 2
        :param file: optional output stream
        """
        self.request(indent=indent, file=file)

    def query(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the query json.
        :param indent: the json indentation, defaults to 2
        :param file: optional output stream
        """
        print(json.dumps(self.search.get_query().to_dict(), indent=indent), file=file)

    def body(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the complete request body.
        :param indent: the json indentation, defaults to 2
        :param file: optional output stream
        """
        print(json.dumps(self.search.to_body(), indent=indent), file=file)

    def request(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the complete request parameters as would be accepted
        by ``elasticsearch.Elasticsearch.search()``.
        :param indent: the json indentation, defaults to 2
        :param file: optional output stream
        """
        print(json.dumps(self.search.to_request(), indent=indent), file=file)

    def response(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the response of the search.
        .. WARNING::

            Search must be executed, otherwise ``ValueError`` is thrown.

        :param indent: the json indentation, defaults to 2
        :param file: optional output stream
        """
        print(json.dumps(self.search.response, indent=indent), file=file)