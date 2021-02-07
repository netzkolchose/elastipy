import re
from copy import copy, deepcopy
from typing import Mapping, Any

from .generated_interface import QueryInterface


class Query(QueryInterface):
    """
    Abstract base class for actual queries.
    """
    _factory_class_map = dict()

    _top_level_parameter = None
    _parameters = {}
    name = None

    def __init_subclass__(cls, **kwargs):
        if "factory" not in kwargs or kwargs["factory"]:
            Query._factory_class_map[cls.name] = cls

    def __init__(self, **params):
        """
        The constructor stores all parameters which are required or are different
        than the default values into the 'parameters' attribute.
        :param params: any
        """
        self.parameters = self._map_parameters(params)
        if not self.name:
            raise TypeError(
                f"Can not create Query instances directly, use one of the derived classes"
            )

    def __repr__(self):
        params = self.parameters
        params = ", ".join(f"{key}={repr(value)}" for key, value in params.items())
        return f"{self.__class__.__name__}({params})"

    def __copy__(self):
        params = deepcopy(self.parameters)
        return self.__class__(**params)

    def __eq__(self, other):
        if isinstance(other, Mapping):
            dic = other
        elif isinstance(other, Query):
            dic = other.to_dict()
        else:
            return False
        return self.to_dict() == dic

    def copy(self):
        return self.__copy__()

    @classmethod
    def from_dict(cls, params: Mapping) -> 'Query':
        """
        Create a new instance from the elastic-search compatible dictionary.

        .. CODE::

            q = Query.from_dict({
                "terms": {
                    "my_field": ["a", "b"],
                    "boost": 2.
                }
            })

        :param params: Mapping
        :return: new Query instance
        """
        if cls._top_level_parameter:
            if len(params) != 1:
                raise TypeError(
                    f"Can not create query {cls.__name__}, "
                    f"expecting one '{cls._top_level_parameter}' parameter, got {params}"
                )
            top_level_param = next(iter(params.keys()))
            params = {
                cls._top_level_parameter: top_level_param,
                **params[top_level_param]
            }

        return cls(**params)

    def to_dict(self):
        dic = dict()
        write_dic = dic
        if self._top_level_parameter:
            value = self.parameters[self._top_level_parameter]
            write_dic = dic[value] = dict()

        for key, value in self.parameters.items():
            if key != self._top_level_parameter:
                write_dic[key] = value_to_dict(value)
        return {self.name: dic}

    def add_query(self, name, **params) -> 'Query':
        query = factory(name, **params)
        return factory("bool", must=[self, query])

    def query_factory(self, name, **params) -> 'Query':
        return factory(name, **params)

    def _map_parameters(self, params: Mapping) -> dict:
        return {
            key: self._map_parameter(key, value)
            for key, value in params.items()
            if self._parameters.get(key, {}).get("required") or value != self._parameters.get(key, {}).get("default")
        }

    def _map_parameter(self, name: str, value: Any) -> Any:
        return value


def value_to_dict(value):
    if hasattr(value, "to_dict"):
        return value.to_dict()
    elif isinstance(value, (list, tuple)):
        return [value_to_dict(v) for v in value]
    return value


def factory(name, **params) -> Query:
    """
    Creates an instance of the matching Query sub-class
    :param name: str
    :param params: any
    :return: instance of derived Query class
    """
    if name in Query._factory_class_map:
        klass = Query._factory_class_map[name]
        return klass(**params)

    raise NotImplementedError(f"Query '{name}' not implemented")


def factory_from_dict(params: Mapping) -> Query:
    """
    Creates an instance of the matching Query sub-class
    :param params: Mapping
        A query object like ``{"term": {"field": "value"}}``
    :return: instance of derived Query class
    """
    if len(params) != 1:
        raise TypeError(
            f"Can not create query, expecting mapping with one base key, got {params}"
        )

    name = next(iter(params.keys()))

    if name in Query._factory_class_map:
        klass = Query._factory_class_map[name]
        return klass.from_dict(params[name])

    raise NotImplementedError(f"Query '{name}' not implemented")
