"""
Currently collection of all queries that have some peculiarity
"""
from typing import Mapping

from .generated_classes import _Terms, _MatchAll, _MatchNone


__all__ = (
    "Terms",
    "MatchAll",
    "MatchNone",
)


class Terms(_Terms):

    def to_dict(self):
        # the 'field' parameter is not mentioned by key but by actual value
        dic = {
            self.parameters["field"]: self.parameters["value"]
        }
        if self.parameters.get("boost"):
            dic["boost"] = self.parameters["boost"]

        return {self.name: dic}

    @classmethod
    def from_dict(cls, params: Mapping):
        dic = dict()
        for name, value in params.items():
            if name in cls._parameters:
                dic[name] = params.get(name)
            else:
                dic["field"] = name
                dic["value"] = value

        return cls(**dic)


class MatchAll(_MatchAll):

    def __invert__(self):
        return self.query_factory("match_none")


class MatchNone(_MatchNone):

    def __invert__(self):
        return self.query_factory("match_all")
