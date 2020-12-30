import json
from copy import deepcopy

from ._client import get_elastic_client
from ._Aggregation import Aggregation, AggregationInterface


class Search(AggregationInterface):
    """
    Interface to elasticsearch /search.

    All changes to a search object create and return a copy.
    Except for aggregations, which are attached to the search instance.

    """
    def __init__(
            self,
            index=None,
            client=None,
            timestamp_field="timestamp",
    ):
        """
        Create a new Search instance.
        :param index: str, optional index name/pattern, can also be set later via index()
        :param client: elasticsearch.Client instance, if None elastipy.get_elastic_client() is used
        :param timestamp_field: str, the default timestamp field used for date-ranges and date_histogram
        """
        AggregationInterface.__init__(self, timestamp_field=timestamp_field)
        self._index = index
        self._client = client
        self.body = dict()
        self._aggregations = []
        self.response = None

    def get_index(self):
        return self._index

    def copy(self):
        es = self.__class__(index=self._index, client=self._client, timestamp_field=self.timestamp_field)
        es.body = deepcopy(self.body)
        es._aggregations = self._aggregations.copy()
        return es

    def execute(self):
        body = deepcopy(self.body)
        if "query" not in body:
            body["query"] = {"match_all": {}}

        client = self._client
        close_client = False
        if client is None:
            client = get_elastic_client()
            close_client = True

        response = client.search(
            index=self._index,
            params={
                "rest_total_hits_as_int": "true"
            },
            body=body,
        )

        if close_client:
            client.close()

        self.response = Response(**response)
        for agg in self._aggregations:
            agg._response = self.response
        return self.response

    def index(self, index):
        es = self.copy()
        es._index = index
        return es

    def match(self, field, value):
        es = self.copy()
        es._add_bool_filter({"match_phrase": {field: value}})
        return es

    def query_string(self, query):
        es = self.copy()
        es._add_bool_filter({"query_string": {"query": query}})
        return es

    def date_from(self, date):
        es = self.copy()
        es._add_bool_filter({"range": {self.timestamp_field: {"gte": date}}})
        return es

    def date_to(self, date):
        es = self.copy()
        es._add_bool_filter({"range": {self.timestamp_field: {"lte": date}}})
        return es

    def date_before(self, date):
        es = self.copy()
        es._add_bool_filter({"range": {self.timestamp_field: {"lt": date}}})
        return es

    def year(self, year):
        return self.date_from(f"{year}-01-01T00:00:00Z").date_to(f"{year}-12-31T23:59:59Z")

    def year_month(self, year, month):
        if month < 12:
            year2, month2 = year, month + 1
        else:
            year2, month2 = year + 1, 1
        return self.date_from(f"{year:04}-{month:02}-01T00:00:00Z").date_before(f"{year2}-{month2:02}-01T00:00:00Z")

    def aggregation(self, *aggregation_name_type, **params) -> Aggregation:
        from ._Aggregation import Aggregation

        if len(aggregation_name_type) == 1:
            name = f"a{len(self._aggregations)}"
            aggregation_type = aggregation_name_type[0]
        elif len(aggregation_name_type) == 2:
            name, aggregation_type = aggregation_name_type
        else:
            raise ValueError(f"Need to provide (aggregation_type) or (name, aggregation_type), got {aggregation_name_type}")

        agg = Aggregation(
            query=self, name=name, type=aggregation_type, params=params
        )
        self._aggregations.append(agg)
        self._add_body(f"aggregations.{name}.{aggregation_type}", agg.params)
        return agg

    def dump_body(self, indent=2, file=None):
        print(json.dumps(self.body, indent=indent), file=file)

    def dump_response(self, indent=2, file=None):
        print(json.dumps(self.response, indent=indent), file=file)

    def _add_body(self, path: str, value, override=True):
        # print("ADD BODY", path, value)
        if isinstance(path, str):
            ppath = path.split(".")
        else:
            ppath = path.copy()

        body = self.body
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
        self.body["query"]["bool"]["filter"].append(data)


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
