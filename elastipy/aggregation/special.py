"""
Currently collection of all aggregations that have some pecularity
"""

from .aggregation import Aggregation


class Filter(Aggregation):
    _agg_type = "filter"

    def to_body(self):
        return self.params["filter"]

    # TODO: filter-aggregation has some 'bucket' format that is not compatible with current approach
    def _iter_bucket_items(self, buckets=None):
        for key, value in self.response.items():
            if isinstance(value, dict):
                yield key, value
