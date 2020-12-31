import re
from copy import copy, deepcopy

# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case/1176023#1176023
CAMEL_CASE_RE = re.compile(r'(?<!^)(?=[A-Z])')


def _to_query(query):
    if isinstance(getattr(query, "_query", None), QueryInterface):
        return query._query
    if isinstance(query, QueryInterface):
        return query
    raise ValueError(
        f"Expected Query, got {repr(query)}"
    )


class QueryInterface:

    def add_query(self, name, **params) -> 'QueryInterface':
        raise NotImplementedError(
            f"{self.__class__.__name__}.add_query() not implemented"
        )

    def new_query(self, name, **params) -> 'QueryInterface':
        raise NotImplementedError(
            f"{self.__class__.__name__}.create_query() not implemented"
        )

    def exists(self, field):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-exists-query.html
        """
        return self.add_query(
            "exists",
            field=field
        )

    def match(self, field, query, analyzer=None):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html
        """
        return self.add_query(
            "match",
            field=field,
            query=query,
            _optional=dict(
                analyzer=analyzer,
            )
        )

    def term(self, field, value, boost: float=None, case_insensitive: bool=None):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html
        """
        return self.add_query(
            "term",
            field=field,
            value=value,
            _optional=dict(
                boost=boost,
                case_insensitive=case_insensitive,
            )
        )

    def range(self, field, gt=None, gte=None, lt=None, lte=None, format=None, relation=None, time_zone=None, boost=None):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html
        """
        return self.add_query(
            "match",
            field=field,
            _optional=dict(
                gt=gt, gte=gte, lt=lt, lte=lte,
                format=format,
                relation=relation,
                time_zone=time_zone,
                boost=boost,
            )
        )

    def boosting(self, positive: 'Query', negative: 'Query', negative_boost: float):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-boosting-query.html
        """
        return self.add_query(
            "boosting",
            positive=positive,
            negative=negative,
            negative_boost=negative_boost,
        )

    def bool(self, must=None, must_not=None, should=None, filter=None):
        return self.add_query(
            "bool",
            _optional=dict(
                must=must,
                must_not=must_not,
                should=should,
                filter=filter,
            )
        )

    def __and__(self, other):
        return self.new_query("bool", must=[self, other])

    def __or__(self, other):
        return self.new_query("bool", should=[self, other])

    def __invert__(self):
        return self.new_query("bool", must_not=[self])


class Query(QueryInterface):

    _factory_class_map = dict()
    _top_level_parameter = None

    def __init_subclass__(cls, **kwargs):
        if "factory" not in kwargs or kwargs["factory"]:
            name = CAMEL_CASE_RE.sub('_', cls.__name__).lower()
            Query._factory_class_map[name] = cls

    def __init__(self, name, _optional=None, **params):
        self.name = name
        self.parameters = params
        self.optional_parameters = _optional or dict()

    def __repr__(self):
        params = self.parameters
        if self.optional_parameters:
            params = params.copy()
            for key, value in self.optional_parameters.items():
                if value is not None:
                    params[key] = value
        params = ", ".join(f"{key}={repr(value)}" for key, value in params.items())
        return f"{self.__class__.__name__}({repr(self.name)}, {params})"

    def __copy__(self):
        return self.__class__(
            self.name,
            _optional=deepcopy(self.optional_parameters),
            **deepcopy(self.parameters),
        )

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def copy(self):
        return self.__copy__()

    def to_dict(self):
        dic = dict()
        write_dic = dic
        if self._top_level_parameter:
            value = self.parameters[self._top_level_parameter]
            write_dic = dic[value] = dict()

        for key, value in self.parameters.items():
            if key != self._top_level_parameter:
                write_dic[key] = self._value_to_dict(value)
        for key, value in self.optional_parameters.items():
            if value is not None:
                write_dic[key] = self._value_to_dict(value)
        return {self.name: dic}

    @staticmethod
    def _value_to_dict(value):
        #if hasattr(value, "query_to_dict"):
        #    return value.query_to_dict()
        if hasattr(value, "to_dict"):
            return value.to_dict()
        elif isinstance(value, (list, tuple)):
            return [Query._value_to_dict(v) if hasattr(v, "to_dict") else v for v in value]
        return value

    @classmethod
    def query_factory(cls, name, **params) -> 'Query':
        if name in cls._factory_class_map:
            return cls._factory_class_map[name](name, **params)
        return Query(name, **params)

    def add_query(self, name, **params) -> 'Query':
        query = self.query_factory(name, **params)
        return self.query_factory("bool", must=[self, query])

    def new_query(self, name, **params) -> 'Query':
        return self.query_factory(name, **params)


class MatchAll(Query):

    def __init__(self, name="match_all", **params):
        super().__init__(name, **params)

    def add_query(self, name, **params) -> 'Query':
        return self.new_query(name, **params)


class Bool(Query):
    """
    https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html
    """
    @property
    def must(self):
        return self._get_bool_param("must")

    @must.setter
    def must(self, value):
        self._set_bool_param("must", value)

    @property
    def must_not(self):
        return self._get_bool_param("must_not")

    @must_not.setter
    def must_not(self, value):
        self._set_bool_param("must_not", value)

    @property
    def should(self):
        return self._get_bool_param("should")

    @should.setter
    def should(self, value):
        self._set_bool_param("should", value)

    @property
    def filter(self):
        return self._get_bool_param("filter")

    @filter.setter
    def filter(self, value):
        self._set_bool_param("filter", value)

    def _get_bool_param(self, name):
        return self.optional_parameters.get(name) or self.parameters.get(name) or []

    def _set_bool_param(self, name, value):
        if name in self.parameters:
            self.parameters[name] = value
        else:
            self.optional_parameters[name] = value

    def add_query(self, name, **params) -> 'Bool':
        return self & self.query_factory(name, **params)

    def __and__(self, other):
        self_ = self
        if not isinstance(self_, Bool):
            self_, other = other, self_

        if not isinstance(other, Bool):
            q = copy(self_)
            q.must += [other]
            return q

        else:
            q = copy(self_)
            for key in ("must", "must_not", "should", "filter"):
                for o in getattr(other, key):
                    if o not in getattr(self_, key):
                        setattr(q, key, getattr(q, key) + [o])
            return q

    def __or__(self, other):
        self_ = self
        if not isinstance(self_, Bool):
            self_, other = other, self_

        if not isinstance(other, Bool):
            q = copy(self)
            if q.should:
                if not q.must and not q.must_not and not q.filter:
                    q.should += [other]
                    return q

        return super().__or__(other)


class QueryField(Query, factory=False):
    """
    All queries with top-level parameter 'field'
    """
    _top_level_parameter = "field"


class Match(QueryField):
    pass


class Term(QueryField):
    pass


class Range(QueryField):
    pass



if __name__ == "__main__":
    import json

    q = MatchAll()
    q = q.match("name", "Boris").match("last_name", "Müller") | q.match("other_name", "Ivan")
    print(q)
    print(json.dumps(q.to_dict(), indent=2))

    q |= Match("match", field="yet_another", query="Fuchs")
    print(q)
    print(json.dumps(q.to_dict(), indent=2))

    # print(Query._factory_class_map)