"""
Currently collection of all aggregations that have some peculiarity
"""

from .aggregation import Aggregation


class Filter(Aggregation):
    _agg_type = "filter"

    def to_body(self):
        return self.params["filter"]

