import re
from copy import copy, deepcopy
from typing import Mapping

from .generated_interface import QueryInterface


class Query(QueryInterface):
    """
    Abstract base class for actual queries.
    """
    _factory_class_map = dict()

    _top_level_parameter = None
    _optional_parameters = {}
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

    def new_query(self, name, **params) -> 'Query':
        return factory(name, **params)

    def _map_parameters(self, params: Mapping) -> dict:
        return {
            key: value
            for key, value in params.items()
            if key not in self._optional_parameters or value != self._optional_parameters[key]
        }

def value_to_dict(value):
    #if hasattr(value, "query_to_dict"):
    #    return value.query_to_dict()
    if hasattr(value, "to_dict"):
        return value.to_dict()
    elif isinstance(value, (list, tuple)):
        return [value_to_dict(v) if hasattr(v, "to_dict") else v for v in value]
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
        try:
            return klass(**params)
        except TypeError as e:
            raise TypeError(f"{e} in class {klass.__name__}")

    raise NotImplementedError(f"Query '{name}' not implemented")
    #return Query(name, **params)
