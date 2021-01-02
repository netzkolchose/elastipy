import json

from .generated_interface import AggregationInterface


class Aggregation(AggregationInterface):
    """
    Aggregation definition and response parser.

    Do not create instances yourself,
    use the Query.aggregation() and Aggregation.aggregation() variants
    """

    _factory_class_map = dict()

    def __init_subclass__(cls, **kwargs):
        if "factory" not in kwargs or kwargs["factory"]:
            Aggregation._factory_class_map[cls._agg_type] = cls

    def __init__(self, search, name, type, params):
        AggregationInterface.__init__(self, timestamp_field=search.timestamp_field)
        self.search = search
        self.name = name
        self.type = type
        self.definition = self.AGGREGATION_DEFINITION.get(self.type) or dict()
        self.params = {
            key: value
            for key, value in params.items()
            if not self.definition.get("parameters") \
                or key not in self.definition["parameters"] \
                or self.definition["parameters"][key].get("required") \
                or self.definition["parameters"][key].get("default") != value
        }
        self._response = None
        self.parent: Aggregation = None
        self.root: Aggregation = None

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.type}')"

    def is_metric(self):
        return self.definition.get("group") == "metric"

    def execute(self):
        """
        Executes the whole query with all aggregations
        :return: self
        """
        self.search.execute()
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

    def to_body(self):
        """
        Returns the part of the elasticsearch body
        :return: dict
        """
        return self.params

    def to_dict_rows(self, default=None):
        dic = self.to_dict(default=default)
        aggs = self._aggregations()
        rows = []
        keys_set = set()
        for keys, value in dic.items():
            if not isinstance(keys, tuple):
                keys = (keys, )

            row = dict()
            for agg, key in zip(aggs, keys):
                row[agg.name] = key

            if isinstance(value, dict):
                for key, val in value.items():
                    row[f"{self.name}_{key}"] = val
            else:
                row[self.name] = value
            rows.append(row)
            keys_set |= set(row.keys())

        keys_set = sorted(keys_set)
        for row in rows:
            for key in keys_set:
                if key not in row:
                    row[key] = None

        return rows

    def to_rows(self, header=True, default=None):
        dict_rows = self.to_dict_rows(default=default)
        rows = []
        if not dict_rows:
            return rows
        header_keys = list(dict_rows[0].keys())
        if header and dict_rows:
            rows.append(header_keys)
        for row in dict_rows:
            rows.append([row[key] for key in header_keys])
        return rows

    def dump_dict(self, key_separator="|", default=None, indent=2, file=None):
        print(json.dumps(self.to_dict(key_separator=key_separator, default=default), indent=indent), file=file)

    def dump_table(self, header=True, default=None, file=None):
        rows = self.to_rows(header=header, default=default)
        if not rows:
            return
        column_width = [0] * len(rows[0])
        for i, row in enumerate(rows):
            rows[i] = [str(v) for v in row]
            for x, v in enumerate(rows[i]):
                column_width[x] = max(column_width[x], len(v))

        format_str = " | ".join(
            "{:%s}" % v
            for v in column_width
        )

        for row in rows:
            print(format_str.format(*row), file=file)

    def aggregation(self, *aggregation_name_type, **params) -> 'Aggregation':
        if len(aggregation_name_type) == 1:
            name = f"a{len(self.search._aggregations)}"
            aggregation_type = aggregation_name_type[0]
        elif len(aggregation_name_type) == 2:
            name, aggregation_type = aggregation_name_type
        else:
            raise ValueError(f"Need to provide (aggregation_type) or (name, aggregation_type), got {aggregation_name_type}")

        agg = factory(
            search=self.search, name=name, type=aggregation_type, params=params
        )
        agg.parent = self
        agg.root = self.root or self
        self.search._aggregations.append(agg)
        self.search._add_body(f"{self._agg_path()}.aggregations.{name}.{aggregation_type}", agg.to_body())
        return agg

    def _key_to_key(self, key, key_separator=None):
        if isinstance(key, str):
            return key
        if key_separator:
            return key_separator.join(key)
        return key if len(key) > 1 else key[0]

    def _iter_sub_keys(self, aggs):
        assert self.name == aggs[0].name
        for b_key, b in self._iter_bucket_items():
            keys = (b_key, )
            yield from self._iter_sub_keys_rec(b, aggs[1:], keys)

    def _iter_bucket_items(self, buckets=None):
        if buckets is None:
            buckets = self.response["buckets"]

        if isinstance(buckets, list):
            for b in buckets:
                yield b[self._bucket_key_name()], b
        elif isinstance(buckets, dict):
            yield from buckets.items()
        else:
            raise NotImplementedError(f"Can not work with buckets of type {type(buckets).__name__}")

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
        for _, b in self._iter_bucket_items():
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
            return_keys = self.definition.get("returns", "value")
            values = dict()
            for key in return_keys:
                if key in bucket:
                    value = bucket[key]
                    if default is not None and value is None:
                        value = default
                    values[key] = value
            if not values:
                raise ValueError(f"{self} should have returned fields {return_keys}, got {bucket}")
            yield values if len(values) > 1 else values[list(values.keys())[0]]
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


def factory(search, name, type, params) -> Aggregation:
    """
    Creates an instance of the matching Aggregation sub-class
    :return: instance of (derived) Aggregation class
    """
    if type in Aggregation._factory_class_map:
        klass = Aggregation._factory_class_map[type]
        try:
            return klass(search, name, type, params)
        except TypeError as e:
            raise TypeError(f"{e} in class {klass.__name__}")

    return Aggregation(search, name, type, params)
