import json
from copy import copy, deepcopy
from typing import Optional, Union, Mapping, Callable, Sequence

from elasticsearch import Elasticsearch

from . import connections
from .aggregation import Aggregation, AggregationInterface, factory as agg_factory
from .query import QueryInterface, EmptyQuery
from ._json import make_json_compatible


class Search(QueryInterface, AggregationInterface):
    """
    Interface to elasticsearch /search.

    All changes to a search object create and return a copy.
    Except for aggregations, which are attached to the search instance.

    """
    def __init__(
            self,
            index: str = None,
            client: Union[Elasticsearch, Callable] = None,
            timestamp_field: str = "timestamp",
    ):
        """
        Create a new Search instance.
        :param index: str, optional index name/pattern, can also be set later via index()
        :param client: elasticsearch.Client instance, if None elastipy.connections.get("default") is used
        :param timestamp_field: str, the default timestamp field used for fields that require dates
        """
        AggregationInterface.__init__(self, timestamp_field=timestamp_field)
        self._index = index
        self._client = client
        self._sort = None
        self._size = None
        self._query = EmptyQuery()
        self._aggregations = []
        self._body = dict()
        self._response: Optional[Response] = None

    @property
    def dump(self):
        """Access the print interface"""
        from .search_print import SearchPrintWrapper
        return SearchPrintWrapper(self)

    def get_index(self) -> str:
        """Return current index"""
        return self._index

    def get_query(self) -> QueryInterface:
        """Return current query"""
        return self._query

    def get_client(self):
        """Return current client"""
        return self._client

    def copy(self):
        """
        Make a copy of this instance and it's queries.

        Warning: Copying of Aggregations is currently not supported so
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
        es._sort = self._sort
        es._size = self._size
        return es

    def to_body(self) -> dict:
        """
        Returns the complete body of the search request
        :return: dict
        """
        body = copy(self._body)

        query_dict = self._query.to_dict()
        if "query" not in query_dict:
            query_dict = {"query": query_dict}
        body.update(query_dict)

        if self._sort is not None:
            body["sort"] = self._sort
        if self._size is not None:
            body["size"] = self._size

        return make_json_compatible(body)

    def execute(self) -> 'Response':
        """
        Sends the search against the current client and returns the response.
        If no client is specified, elastipy.connections.get("default") will be used.
        :return: Response, a dict wrapper with some convenience methods
        """
        client = self._client
        if client is None:
            client = connections.get()

        response = client.search(
            index=self._index,
            params={
                "rest_total_hits_as_int": "true"
            },
            body=self.to_body(),
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

    def sort(self, *sort):
        """
        Replace the sorting

        `sort search results <https://www.elastic.co/guide/en/elasticsearch/reference/current/sort-search-results.html>`__

        :param sort: can be str, dict or list
        :return: new Search instance
        """
        args = []
        for s in sort:
            if isinstance(s, (list, tuple)):
                args += list(s)
            else:
                args.append(s)

        for i, arg in enumerate(args):
            if isinstance(arg, str):
                if arg.startswith("-"):
                    args[i] = {arg.lstrip("-"): "desc"}

        es = self.copy()
        es._sort = args or None
        return es

    def size(self, size):
        """
        Replace the maximum document count
        :param size: int. number of document hits to return
        :return: new Search instance
        """
        es = self.copy()
        es._size = size
        return es

    def query(self, query: QueryInterface):
        """
        Replace the query
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

    def new_query(self, name, **params):
        es = self.copy()
        es._query = es._query.new_query(name, **params)
        return es

    def query_to_dict(self):
        return self._query.to_dict()

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

    def _add_body(self, path: str, value, override=True):
        # print("ADD BODY", path, value)
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

    def _add_bool_filter(self, data):
        self._add_body(f"query.bool.filter", [], override=False)
        self._body["query"]["bool"]["filter"].append(data)


class Response(dict):
    """
    Simple wrapper around a dict with some elasticsearch response helper functions
    """

    @property
    def total_hits(self):
        return self["hits"]["total"]

    @property
    def aggregations(self):
        return self["aggregations"]

    @property
    def documents(self):
        return [
            doc["_source"]
            for doc in self["hits"]["hits"]
        ]

    def dump(self, indent=2, file=None):
        print(json.dumps(self, indent=indent), file=file)


def _to_query(query):
    if isinstance(getattr(query, "_query", None), QueryInterface):
        return query._query
    if isinstance(query, QueryInterface):
        return query
    raise ValueError(
        f"Expected Query, got {repr(query)}"
    )
