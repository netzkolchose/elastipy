from copy import copy, deepcopy
from typing import Sequence, Union, Optional, Iterable, Tuple, TextIO

from elastipy.aggregation import Aggregation
from elastipy._print import print_dict_rows, dict_rows_to_list_rows


class AggregationVisitor:
    """
    Helper to access the results of aggregations
    """

    def __init__(self, agg: Aggregation):
        self.agg = agg

    def aggregations(self, filter: Optional[Union[str, Sequence[str]]] = None, depth_first: bool = True):
        if filter is None or self.agg.group in filter:
            yield self.agg
        yield from self._child_aggregations(self.agg, filter=filter, depth_first=depth_first)

    def children(self, depth_first: bool = True):
        yield from self._child_aggregations(self.agg, depth_first=depth_first)

    def dump_table(self, header: bool = True, file: TextIO = None):
        """
        Print the result of the dict_rows() function as table to console.
        :param header: bool, if True, include the names in the first row
        :param file: optional text stream to print to
        """
        print_dict_rows(self.dict_rows(), header=header, file=file)

    def _child_aggregations(self, agg: Aggregation, filter=None, depth_first: bool = True):
        if depth_first:
            for c in agg.children:
                if filter is None or c.group in filter:
                    yield c
                    yield from self._child_aggregations(c, depth_first=depth_first)
        else:
            for c in agg.children:
                if filter is None or c.group in filter:
                    yield c
            for c in agg.children:
                if filter is None or c.group in filter:
                    yield from self._child_aggregations(c, depth_first=depth_first)

    def dict_rows(self) -> Iterable[dict]:
        """
        Iterates through all result values from this aggregation branch.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics).

        :return: generator of dict
        """
        root = self.agg.root
        yield from self._dict_rows(root, root.search.response.aggregations[root.name])

    def rows(self, header=True) -> Iterable[Sequence]:
        return dict_rows_to_list_rows(self.dict_rows(), header=header)

    def keys(self, key_separator=None) -> Iterable[Union[str, int, float]]:
        """
        Iterates through all keys of this aggregation.

        For example, a top-level date_histogram would return all timestamps.

        For a nested bucket aggregation each key is a tuple of all parent keys as well.

        :param key_separator: str, optional separator to concat multiple keys into one string
        :return: generator of str, int or float
        """
        if not self.agg.parent:
            for b in self.agg.buckets:
                yield self._concat_key(b[self.agg.key_name()], key_separator=key_separator)
            return

        for k in self._iter_sub_keys(self.root_branch()):
            yield self._concat_key(k, key_separator=key_separator)

    def values(self, default=None) -> Iterable:
        """
        Iterates through all values of this aggregation.
        :param default: if not None any None-value will be replaced by this
        :return: generator
        """
        if not self.agg.parent:
            yield from self._iter_values_from_bucket(self.agg, self.agg.response, default=default)
            return

        yield from self._iter_sub_values(self.root_branch(), default=default)

    def root_branch(self):
        aggs = []
        a = self.agg
        while a:
            aggs.insert(0, a)
            a = a.parent
        return aggs

    def _dict_rows(self, agg: Aggregation, response: dict):
        if not agg.is_bucket():
            raise ValueError(f"Can not call dict_rows() on non-bucket aggregation {agg}")

        for b_key, bucket in self._iter_bucket_items(agg, response):
            row = {
                agg.name: bucket[b_key] if b_key in bucket else b_key,
                f"{agg.name}.doc_count": bucket["doc_count"],
            }
            for metric in agg.metrics():
                return_keys = metric.definition.get("returns", "value")
                if isinstance(return_keys, str):
                    return_keys = [return_keys]

                if len(return_keys) == 1:
                    row[metric.name] = bucket[metric.name][return_keys[0]]
                else:
                    for key in return_keys:
                        row[f"{metric.name}.{key}"] = bucket[metric.name][key]

            has_sub_bucket = False
            for bucket_agg in agg.children:
                if bucket_agg.is_bucket():
                    has_sub_bucket = True
                    for sub_rows in self._dict_rows(bucket_agg, bucket[bucket_agg.name]):
                        sub_row = copy(row)
                        sub_row.update(sub_rows)
                        yield sub_row

            if not has_sub_bucket:
                yield row

    def _concat_key(self, key: Union[str, Sequence], key_separator: Optional[str] = None):
        if isinstance(key, str):
            return key
        if key_separator:
            return key_separator.join(key)
        return key if len(key) > 1 else key[0]

    def _iter_bucket_items(self, agg: Aggregation, response=None):
        assert agg.is_bucket()
        # this could be a place to specialize by class
        #if hasattr(agg, "_iter_bucket_items"):
        #    yield from agg._iter_bucket_items(response)
        #else:
        if response is None:
            response = agg.response
        if "buckets" in response:
            buckets = response["buckets"]
            if isinstance(buckets, list):
                for b in buckets:
                    yield b[agg.key_name()], b
            elif isinstance(buckets, dict):
                yield from buckets.items()
            else:
                raise NotImplementedError(f"Can not work with buckets of type {type(buckets).__name__}")
        else:
            # single bucket aggregations
            yield agg.name, response

    def _iter_sub_keys(self, aggs: Sequence[Aggregation]):
        for b_key, b in self._iter_bucket_items(aggs[0]):
            keys = (b_key, )
            yield from self._iter_sub_keys_rec(b, aggs[1:], keys)

    def _iter_sub_keys_rec(self, bucket: dict, aggs: Sequence[Aggregation], keys: Tuple[str]):
        if not aggs[0].name in bucket:
            raise ValueError(f"Expected agg '{aggs[0].name}' in bucket {bucket}")

        sub_bucket = bucket[aggs[0].name]
        key_name = aggs[0].key_name()

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

    def _iter_sub_values(self, aggs: Sequence[Aggregation], default=None):
        for _, b in self._iter_bucket_items(aggs[0]):
            yield from self._iter_sub_values_rec(b, aggs[1:], default=default)

    def _iter_sub_values_rec(self, bucket: dict, aggs: Sequence[Aggregation], default=None):
        sub_bucket = bucket[aggs[0].name]
        if len(aggs) == 1:
            yield from self._iter_values_from_bucket(aggs[0], sub_bucket, default=default)
        else:
            aggs = aggs[1:]
            for b in sub_bucket["buckets"]:
                yield from self._iter_sub_values_rec(b, aggs, default=default)

    def _iter_values_from_bucket(self, agg: Aggregation, bucket: dict, default=None):
        if agg.is_metric():
            return_keys = agg.definition.get("returns", "value")
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
