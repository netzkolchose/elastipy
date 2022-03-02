import json
from copy import copy, deepcopy
from typing import Optional, Union, Mapping, Callable, Sequence, List, Any

from elasticsearch import Elasticsearch, VERSION as ES_VERSION


from . import connections
from .aggregation import Aggregation, AggregationInterface, factory as agg_factory
from .query import QueryInterface, EmptyQuery, Query
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
            version: Optional[int] = None
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

        :param version: int,
            optionally sets the elasticsearch server major version for which
            the request is constructed. Default is the major version of
            the installed ``elasticsearch-py`` package.
        """
        from .query import Query
        from .generated_search_param import SearchParameters

        AggregationInterface.__init__(self, timestamp_field=timestamp_field)
        self._version = version
        self._index = index
        self._client = client
        self._parameters = SearchParameters(self)
        self._query: Query = EmptyQuery()
        self._aggregations = []
        self._body = dict()
        self._highlighters = dict()
        self._response: Optional[Response] = None

        if not self.version >= 7:
            raise ValueError(
                f"Unsupported elasticsearch major version {self.version}"
                f", elastipy only supports 7 and upwards"
            )

    def __repr__(self):  # pragma: no cover
        params = dict()
        if self._index:
            params["index"] = self._index
        if self._client:
            params["client"] = self._client
        if self.timestamp_field != "timestamp":
            params["timestamp"] = self.timestamp_field
        if self._version:
            params["version"] = self._version

        params = ", ".join(
            f"{key}={repr(value)}"
            for key, value in params.items()
        )
        return f"{self.__class__.__name__}({params})"

    @property
    def version(self) -> int:
        return self._version or ES_VERSION[0]

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

    def copy(self) -> "Search":
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

        es = self.__class__(
            index=self._index,
            client=self._client,
            timestamp_field=self.timestamp_field,
            version=self.version,
        )
        es._body = deepcopy(self._body)
        es._query = self._query.copy()
        es._parameters._params = deepcopy(self._parameters._params)
        es._highlighters = deepcopy(self._highlighters)
        return es

    def to_body(self) -> dict:
        """
        Returns the complete body of the search request

        :return: dict
        """
        body = copy(self._body)

        body["query"] = self._query.to_dict()

        param_dict = self._parameters.to_body()
        if param_dict:
            body.update(param_dict)

        if self._highlighters:
            hl = dict()
            for key, value in self._highlighters.items():
                if key == "*global*":
                    hl.update(value)
                else:
                    if "fields" not in hl:
                        hl["fields"] = dict()
                    hl["fields"][key] = value
            body["highlight"] = hl

        return make_json_compatible(body)

    def to_request(self) -> dict:
        """
        Returns the complete request parameters as would be accepted
        by ``elasticsearch.Elasticsearch.search()``.

        :return: dict
        """
        if self.version > 7:
            return {
                "index": self._index,
                **self._parameters.to_query_params(),
                **self.to_body()
            }
        else:
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

    def highlight(
            self,
            *fields: str,
            boundary_chars: Optional[str] = None,
            boundary_max_scan: Optional[int] = None,
            boundary_scanner: Optional[str] = None,
            boundary_scanner_locale: Optional[str] = None,
            encoder: Optional[str] = None,
            force_source: Optional[bool] = None,
            fragmenter: Optional[str] = None,
            fragment_offset: Optional[int] = None,
            fragment_size: Optional[int] = None,
            highlight_query: Optional[Query] = None,
            matched_fields: Optional[List[str]] = None,
            no_match_size: Optional[int] = None,
            number_of_fragments: Optional[int] = None,
            order: Optional[str] = None,
            phrase_limit: Optional[int] = None,
            pre_tags: Optional[str] = None,
            post_tags: Optional[str] = None,
            require_field_match: Optional[bool] = None,
            max_analyzed_offset: Optional[int] = None,
            tags_schema: Optional[str] = None,
            type: Optional[str] = None,
    ) -> "Search":
        kwargs = {
            "boundary_chars": boundary_chars,
            "boundary_max_scan": boundary_max_scan,
            "boundary_scanner": boundary_scanner,
            "boundary_scanner_locale": boundary_scanner_locale,
            "encoder": encoder,
            "force_source": force_source,
            "fragmenter": fragmenter,
            "fragment_offset": fragment_offset,
            "fragment_size": fragment_size,
            "highlight_query": highlight_query,
            "matched_fields": matched_fields,
            "no_match_size": no_match_size,
            "number_of_fragments": number_of_fragments,
            "order": order,
            "phrase_limit": phrase_limit,
            "pre_tags": pre_tags,
            "post_tags": post_tags,
            "require_field_match": require_field_match,
            "max_analyzed_offset": max_analyzed_offset,
            "tags_schema": tags_schema,
            "type": type,
        }

        es = self.copy()

        if not fields:
            fields = ["*global*"]

        for field in fields:
            if field not in es._highlighters:  # pragma: no cover
                es._highlighters[field] = dict()
            hl = es._highlighters[field]

            for key, value in kwargs.items():
                if value is not None:
                    hl[key] = value

        return es

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
