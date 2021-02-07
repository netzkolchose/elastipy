import json
from copy import copy, deepcopy
from typing import Optional, Union, Mapping, Callable, Sequence, List, Any

from elasticsearch import Elasticsearch

from . import connections
from .aggregation import Aggregation, AggregationInterface, factory as agg_factory
from .query import QueryInterface, EmptyQuery
from ._json import make_json_compatible


class Search(QueryInterface, AggregationInterface):
    """
    Interface to elasticsearch ``/search``.

    All changes to a search object create and return a copy.
    Except for aggregations, which are attached to the search instance.

    """
    def __init__(
            self,
            index: str = None,
            client: Union[str, Callable, Elasticsearch, Any, None] = None,
            timestamp_field: str = "timestamp",
    ):
        """
        Create a new Search instance.

        :param index: str, optional index name/pattern, can also be set later via index()
        :param client:
            Can be an ``elasticsearch.Elasticsearch`` instance.

            If None, then ``elastipy.connections.get("default")`` is used.

            Can also be a string to change the connection alias
            from "default" to something else.

            Can also be a callable, which get's the whole ``to_request``__
            as parameters.

        :param timestamp_field: str
            The default timestamp field used for fields that require dates.
        """
        from .query import Query
        from .generated_search_param import SearchParameters

        AggregationInterface.__init__(self, timestamp_field=timestamp_field)
        self._index = index
        self._client = client
        self._parameters = SearchParameters(self)
        self._query: Query = EmptyQuery()
        self._aggregations = []
        self._body = dict()
        self._response: Optional[Response] = None

    @property
    def param(self):
        """Access to the search parameters"""
        return self._parameters

    @property
    def dump(self):
        """Access the print interface"""
        from .search_dump import SearchDump
        return SearchDump(self)

    def get_index(self) -> str:
        """Return current index"""
        return self._index

    def get_query(self):
        """Return current query"""
        return self._query

    def get_client(self):
        """Return current client"""
        client = self._client
        if client is None:
            client = connections.get()
        elif isinstance(client, str):
            client = connections.get(client)

        return client

    def copy(self):
        """
        Make a copy of this instance and it's queries.

        .. WARNING::
            Copying of Aggregations is currently not supported so
            aggregations must be added at the last step, after all queries are applied.

        :return: a new Search instance
        """
        if self._aggregations:
            raise NotImplementedError(
                "Sorry, but copying of aggregations is currently not supported. "
                "Please make all the queries before adding aggregations"
            )

        es = self.__class__(index=self._index, client=self._client, timestamp_field=self.timestamp_field)
        es._body = deepcopy(self._body)
        es._query = self._query.copy()
        es._parameters._params = deepcopy(self._parameters._params)
        return es

    def to_body(self) -> dict:
        """
        Returns the complete body of the search request

        :return: dict
        """
        body = copy(self._body)

        query_dict = self._query.to_dict()
        body.update({"query": query_dict})

        param_dict = self._parameters.to_body()
        if param_dict:
            body.update(param_dict)

        return make_json_compatible(body)

    def to_request(self) -> dict:
        """
        Returns the complete request parameters as would be accepted
        by ``elasticsearch.Elasticsearch.search()``.

        :return: dict
        """
        return {
            "index": self._index,
            "params": self._parameters.to_query_params(),
            "body": self.to_body()
        }

    def execute(self) -> 'Response':
        """
        Sends the search against the current client and returns the response.
        If no client is specified, elastipy.connections.get("default") will be used.

        :return: Response, a dict wrapper with some convenience methods
        """
        client = self.get_client()

        if callable(client):
            response = client(**self.to_request())
        elif hasattr(client, "search") and callable(client.search):
            response = client.search(**self.to_request())
        else:
            raise TypeError(
                f"The client must have a search() method or must itself be callable, "
                f"got {type(client).__name__}"
            )

        self.set_response(response)
        return self._response

    @property
    def response(self) -> 'Response':
        """
        Access to the response of the search.
        Raises exception if accessed before search

        :return: Response, a dict wrapper with some convenience methods
        """
        if self._response is None:
            raise ValueError(
                f"Can not access Search.response, search has not been executed."
            )
        return self._response

    def index(self, index: str):
        """
        Replace the index.

        :param index: str
        :return: new Search instance
        """
        es = self.copy()
        es._index = index
        return es

    def client(self, client):
        """
        Replace the client that will be used for request.

        :param client: an elasticsearch.Elasticsearch client or compatible
        :return: new Search instance
        """
        es = self.copy()
        es._client = client
        return es

    def sort(self, *sort) -> 'Search':
        """
        Change the order of the returned documents. See `sort search results
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/sort-search-results.html>`__.

        The parameter can be:

            - ``"field"`` or ``"-field"`` to sort a field ascending or
              descending
            - ``{"field": "asc"}`` or ``{"field": "desc"}`` to sort a field
              ascending or descending
            - a ``list`` of strings or objects as above to sort by a couple of
              fields
            - ``None`` to turn off sorting

        :returns: ``Search``
            A new Search instance is created
        """
        return self._parameters.sort(sort)

    def size(self, size):
        """
        Replace the maximum document count.

        :param size: int. number of document hits to return
        :return: new Search instance
        """
        return self._parameters.size(size)

    def query(self, query: QueryInterface):
        """
        Replace the query.

        :param query: a QueryInterface sub-class
        :return: new Search instance
        """
        es = self.copy()
        es._query = query
        return es

    # -- attach QueryInterface --

    def add_query(self, name, **params):
        es = self.copy()
        es._query = es._query.add_query(name, **params)
        return es

    def __and__(self, other):
        es = self.copy()
        es._query &= _to_query(other)
        return es

    def __or__(self, other):
        es = self.copy()
        es._query |= _to_query(other)
        return es

    def __invert__(self):
        es = self.copy()
        es._query = ~es._query
        return es

    # -- attach the AggregationInterface --

    def aggregation(self, *aggregation_name_type, **params) -> Aggregation:
        if len(aggregation_name_type) == 1:
            name = f"a{len(self._aggregations)}"
            aggregation_type = aggregation_name_type[0]
        elif len(aggregation_name_type) == 2:
            name, aggregation_type = aggregation_name_type
        else:
            raise ValueError(f"Need to provide (aggregation_type) or (name, aggregation_type), got {aggregation_name_type}")

        agg = agg_factory(
            search=self, name=name, type=aggregation_type, params=params
        )
        self._aggregations.append(agg)
        self._add_body(f"aggregations.{name}.{aggregation_type}", agg.to_body())
        return agg

    agg = aggregation

    # -- debugging stuff --

    def set_response(self, response: Mapping):
        """
        Sets the elasticsearch API response.

        Use this if you need other means of passing the API response to the Search instance.

        :param response: Mapping, the complete response from /search/ endpoint
        :return: self
        """
        self._response = Response(**response)
        for agg in self._aggregations:
            agg._response = self.response
        return self

    # -- private impl --

    def _add_body(self, path: Union[str, list], value, override=True):
        if isinstance(path, str):
            ppath = path.split(".")
        else:
            ppath = copy(path)

        body = self._body
        while ppath:
            key = ppath.pop(0)
            if not isinstance(body, dict):
                raise ValueError(f"Can not assign body:{path} = {value}, {key} is of type {type(body).__name__}")
            if len(ppath):
                if key not in body:
                    body[key] = dict()
                body = body[key]
            else:
                if override or key not in body:
                    body[key] = value


class Response(dict):
    """
    Simple wrapper around a dict with some elasticsearch response helper functions
    """

    @property
    def total_hits(self) -> int:
        total = self["hits"]["total"]
        if isinstance(total, dict):
            return total["value"]
        return total

    @property
    def aggregations(self) -> List[dict]:
        return self["aggregations"]

    @property
    def hits(self) -> List[dict]:
        """Returns the hits list"""
        return self["hits"]

    @property
    def documents(self) -> List[dict]:
        """Returns a list of all documents inside each hit"""
        return [
            doc["_source"]
            for doc in self["hits"]["hits"]
        ]

    @property
    def scores(self) -> List[float]:
        """Returns the list of scores of each hit"""
        return [
            hit["_score"]
            for hit in self["hits"]["hits"]
        ]

    @property
    def dump(self):
        from .response_dump import ResponseDump
        return ResponseDump(self)


def _to_query(query):
    if isinstance(getattr(query, "_query", None), QueryInterface):
        return query._query
    if isinstance(query, QueryInterface):
        return query
    raise ValueError(
        f"Expected Query, got {repr(query)}"
    )
