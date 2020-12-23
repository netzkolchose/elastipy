import json


# TODO: collect all the names and maybe even machine-readable parameter lists
METRICS = {
    "avg",
    "cardinality",
    "min",
    "max",
    "sum",
    "value_count",
    "weighted_avg",
}


class AggregationInterface:
    """
    Interface to create aggregations.
    Used either on Query or on Aggregations themselves.
    """
    def __init__(self, timestamp_field="timestamp"):
        self.timestamp_field = timestamp_field

    def aggregation(self, *aggregation_name_type, **params) -> 'Aggregation':
        """
        Creates an aggregation.

        Either call
            aggregation("sum", field=...) to create an automatic name
        or call
            aggregation("my_name", "sum", field=...) to set aggregation name explicitly

        :param aggregation_name_type: one or two strings
        :param params: all parameters of the aggregation function
        :return: Aggregation instance
        """
        raise NotImplementedError

    def agg(self, *aggregation_name_type, **params):
        """
        Alias for aggregation()
        """
        return self.aggregation(*aggregation_name_type, **params)

    def agg_terms(self, *aggregation_name, field, size=10, shard_size=None, order=None, min_doc_count=0, show_term_doc_count_error=False):
        return self.aggregation(
            *(aggregation_name + ("terms", )),
            field=field, size=size, min_doc_count=min_doc_count,
            show_term_doc_count_error=show_term_doc_count_error,
            _if_not_none=dict(shard_size=shard_size, order=order)
        )

    def agg_date_histogram(self, *aggregation_name, interval="1y", field=None, min_doc_count=0):
        return self.aggregation(
            *(aggregation_name + ("date_histogram", )),
            calendar_interval=interval,
            field=field or self.timestamp_field,
            min_doc_count=min_doc_count,
        )

    def metric(self, *aggregation_name_type, **params):
        """
        Alias for aggregation()
        """
        aggregation_type = aggregation_name_type[0] if len(aggregation_name_type) == 1 else aggregation_name_type[1]
        assert aggregation_type in METRICS, f"Metric '{aggregation_type}' not supported"
        return self.aggregation(*aggregation_name_type, **params)

    def metric_avg(self, *aggregation_name, field, missing=None, script=None):
        return self.metric(
            *(aggregation_name + ("avg", )),
            field=field, _if_not_none=dict(missing=missing, script=script)
        )

    def metric_cardinality(self, *aggregation_name, field, precision_threshold=3000, missing=None):
        return self.metric(
            *(aggregation_name + ("cardinality", )),
            field=field, precision_threshold=precision_threshold,
            _if_not_none=dict(missing=missing),
        )


class Aggregation(AggregationInterface):
    """
    Aggregation definition and response parser.

    Do not create instances yourself,
    use the Query.aggregation() and Aggregation.aggregation() variants
    """
    def __init__(self, query, name, type, params):
        AggregationInterface.__init__(self, timestamp_field=query.timestamp_field)
        self.query = query
        self.name = name
        self.type = type
        self.params = params.copy()
        if_not_none = self.params.pop("_if_not_none", None)
        if if_not_none:
            for key, value in if_not_none.items():
                if value is not None:
                    self.params[key] = value
        self._response = None
        self.parent: Aggregation = None
        self.root: Aggregation = None

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.type}')"

    def is_metric(self):
        return self.type in METRICS

    def execute(self):
        """
        Executes the whole query with all aggregations
        :return: self
        """
        self.query.execute()
        return self

    @property
    def response(self):
        if self.parent:
            raise ValueError(f"Can not get response of sub-aggregation '{self.name}' (type {self.type})")

        return self._response.aggregations[self.name]

    @property
    def buckets(self):
        if self.parent:
            raise ValueError(f"Can not get buckets of sub-aggregation '{self.name}' (type {self.type}) "
                             f"directly, use keys() and values()")
        return self.response["buckets"]

    def keys(self, key_separator=None):
        """
        Iterates through all keys of this aggregation.

        For example, a top-level date_histogram would return all timestamps.

        For nested bucket aggregations each key is a tuple of all parent keys as well.

        :param key_separator: str, optional separator to concat multiple keys into one string
        :return: generator
        """
        if not self.parent:
            key_name = self._bucket_key_name()
            for b in self.buckets:
                yield self._key_to_key(b[key_name], key_separator=key_separator)
            return

        for k in self.root._iter_sub_keys(self._aggregations()):
            yield self._key_to_key(k, key_separator=key_separator)

    def values(self, default=None):
        """
        Iterates through all values of this aggregation.
        :param default: if not None any None-value will be replaced by this
        :return: generator
        """
        if not self.parent:
            yield from self._iter_values_from_bucket(self.response, default=default)
            return

        yield from self.root._iter_sub_values(self._aggregations(), default=default)

    def items(self, key_separator=None, default=None):
        """
        Iterates through all key, value tuples.
        :param key_separator: str, optional separator to concat multiple keys into one string
        :param default: if not None any None-value will be replaced by this
        :return: generator
        """
        yield from zip(self.keys(key_separator=key_separator), self.values(default=default))

    def to_dict(self, key_separator=None, default=None):
        """
        Create a dictionary from all key/value pairs.
        :param key_separator: str, optional separator to concat multiple keys into one string
        :param default: if not None any None-value will be replaced by this
        :return: dict
        """
        return {
            key: value
            for key, value in self.items(key_separator=key_separator, default=default)
        }

    def dump_dict(self, key_separator="|", default=None, indent=2, file=None):
        print(json.dumps(self.to_dict(key_separator=key_separator, default=default), indent=indent), file=file)

    def aggregation(self, *aggregation_name_type, **params):
        if len(aggregation_name_type) == 1:
            name = f"a{len(self.query._aggregations)}"
            aggregation_type = aggregation_name_type[0]
        elif len(aggregation_name_type) == 2:
            name, aggregation_type = aggregation_name_type
        else:
            raise ValueError(f"Need to provide (aggregation_type) or (name, aggregation_type), got {aggregation_name_type}")

        agg = Aggregation(
            query=self.query, name=name, type=aggregation_type, params=params
        )
        agg.parent = self
        agg.root = self.root or self
        self.query._aggregations.append(agg)
        self.query._add_body(f"{self._agg_path()}.aggregations.{name}.{aggregation_type}", agg.params)
        return agg

    def _key_to_key(self, key, key_separator=None):
        if isinstance(key, str):
            return key
        if key_separator:
            return key_separator.join(key)
        return key if len(key) > 1 else key[0]

    def _iter_sub_keys(self, aggs):
        assert self.name == aggs[0].name
        key_name = aggs[0]._bucket_key_name()
        for b in self.response["buckets"]:
            keys = (b[key_name], )
            yield from self._iter_sub_keys_rec(b, aggs[1:], keys)

    def _iter_sub_keys_rec(self, bucket, aggs, keys):
        if not aggs[0].name in bucket:
            raise ValueError(f"Expected agg '{aggs[0].name}' in bucket {bucket}")

        sub_bucket = bucket[aggs[0].name]
        key_name = aggs[0]._bucket_key_name()

        if len(aggs) == 1:
            if aggs[0].is_metric():
                yield keys
            else:
                for b in sub_bucket["buckets"]:
                    yield keys + (b[key_name], )
        else:
            aggs = aggs[1:]
            for b in sub_bucket["buckets"]:
                yield from self._iter_sub_keys_rec(b, aggs, keys + (b[key_name], ))

    def _iter_sub_values(self, aggs, default=None):
        assert self.name == aggs[0].name
        for b in self.response["buckets"]:
            yield from self._iter_sub_values_rec(b, aggs[1:], default=default)

    def _iter_sub_values_rec(self, bucket, aggs, default=None):
        sub_bucket = bucket[aggs[0].name]
        if len(aggs) == 1:
            yield from aggs[0]._iter_values_from_bucket(sub_bucket, default=default)
        else:
            aggs = aggs[1:]
            for b in sub_bucket["buckets"]:
                yield from self._iter_sub_values_rec(b, aggs, default=default)

    def _iter_values_from_bucket(self, bucket, default=None):
        if self.is_metric():
            value = bucket["value"]
            if default is not None and value is None:
                value = default
            yield value
        else:
            for b in bucket["buckets"]:
                value = b["doc_count"]
                if default is not None and value is None:
                    value = default
                yield value

    def _bucket_key_name(self):
        if self.is_metric() and self.parent:
            return self.parent._bucket_key_name()
        key_name = "key"
        if self.type == "date_histogram":
            key_name = "key_as_string"
        return key_name

    def _agg_path(self):
        if not self.parent:
            return f"aggregations.{self.name}"
        else:
            return f"{self.parent._agg_path()}.aggregations.{self.name}"

    def _name_path(self):
        return [a.name for a in self._aggregations()]

    def _aggregations(self):
        aggs = []
        a = self
        while a:
            aggs.insert(0, a)
            a = a.parent
        return aggs


