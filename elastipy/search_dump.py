import json
from typing import Optional, List, Iterable, Union, Tuple, TextIO, Sequence, Mapping

from .search import Search


class SearchDump:

    def __init__(self, search: Search):
        self._search = search

    def __call__(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the complete request parameters as would be accepted
        by ``elasticsearch.Elasticsearch.search()``.

        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        """
        self.request(indent=indent, file=file)

    def query(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the query json.

        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        """
        print(json.dumps(self._search.get_query().to_dict(), indent=indent), file=file)

    def body(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the complete request body.

        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        """
        print(json.dumps(self._search.to_body(), indent=indent), file=file)

    def request(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the complete request parameters as would be accepted
        by ``elasticsearch.Elasticsearch.search()``.

        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        """
        print(json.dumps(self._search.to_request(), indent=indent), file=file)

    def response(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the response of the search.

        .. WARNING::

            Search must be executed, otherwise ``ValueError`` is thrown.

        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        """
        print(json.dumps(self._search.response, indent=indent), file=file)
