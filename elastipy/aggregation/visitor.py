import fnmatch
from copy import copy, deepcopy
from itertools import chain
from typing import Sequence, Union, Optional, Iterable, Tuple, TextIO, Any, Mapping

from elastipy.aggregation import Aggregation
from .helper import wildcard_match


class Visitor:
    """
    Helper to access the results of aggregations.

    This is not a public API! Use the methods exposed on the Aggregation class.
    """

    def __init__(self, agg: Aggregation, key_separator=None, default_value=None):
        self.agg = agg
        self.default_value = default_value
        self.key_separator = key_separator

    def aggregations(self, filter: Optional[Union[str, Sequence[str]]] = None, depth_first: bool = True):
        if filter is None or self.agg.group in filter:
            yield self.agg
        yield from self._child_aggregations(self.agg, filter=filter, depth_first=depth_first)

    def children(self, depth_first: bool = True):
        yield from self._child_aggregations(self.agg, depth_first=depth_first)

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

    def items(self) -> Iterable[Tuple]:
        """
        Iterates through all keys and values of this aggregation.
        :return: generator
        """
        for key, value in self._items():
            if not key:
                key = self.agg.name
            yield self.concat_key(key), self.make_default(value)

    def _items(self):
        if not self.agg.parent:
            yield from self._iter_items_from_bucket(self.agg, self.agg.response, tuple())
            return

        aggs = self.root_branch()
        for b_key, b in self._iter_bucket_items(aggs[0]):
            yield from self._iter_sub_items_rec(b, aggs[1:], (b_key, ))

    def dict_rows(
            self,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
    ) -> Iterable[dict]:
        """
        Iterates through all result values from this aggregation branch.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics).

        :param include: str or list of str
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that does not fit a pattern is removed
        :param exclude: str or list of str
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that fits a pattern is removed

        :return: generator of dict
        """
        root = self.agg.root
        for row in self._dict_rows(root, root.search.response.aggregations[root.name]):
            if include:
                row = {
                    key: value
                    for key, value in row.items()
                    if wildcard_match(key, include)
                }
            if exclude:
                row = {
                    key: value
                    for key, value in row.items()
                    if not wildcard_match(key, exclude)
                }
            yield row

    def root_branch(self):
        aggs = []
        a = self.agg
        while a:
            aggs.insert(0, a)
            a = a.parent
        return aggs

    def concat_key(self, key: Union[Any, Sequence]):
        if isinstance(key, str):
            return key
        if isinstance(key, Sequence):
            if self.key_separator:
                return self.key_separator.join(str(i) for i in key)
            return key if len(key) > 1 else key[0]
        return key

    def make_default(self, value):
        if self.default_value is not None and value is None:
            value = self.default_value
        return value

    def _dict_rows(self, agg: Aggregation, response: dict):
        if not agg.is_bucket():
            raise ValueError(f"Can not call dict_rows() on non-bucket aggregation {agg}")

        for b_key, bucket in self._iter_bucket_items(agg, response):
            row = {
                agg.name: bucket[b_key] if b_key in bucket else b_key,
                f"{agg.name}.doc_count": bucket["doc_count"],
            }
            for metric in chain(agg.metrics(), agg.pipelines()):
                return_keys = metric.definition.get("returns", "value")
                if isinstance(return_keys, str):
                    return_keys = [return_keys]

                if len(return_keys) == 1:
                    values = {metric.name: bucket[metric.name].get(return_keys[0])}
                else:
                    values = dict()
                    for key in return_keys:
                        if key in bucket[metric.name]:
                            values[f"{metric.name}.{key}"] = bucket[metric.name][key]

                row.update(self._expand_value(values))

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

    def _expand_value(self, value, prefix=None):
        if isinstance(value, dict):
            def _iter_items(dic, prefix):
                for key, value in dic.items():
                    deep_key = f"{prefix}.{key}" if prefix else key
                    if isinstance(value, dict):
                        yield from _iter_items(value, deep_key)
                    else:
                        yield deep_key, value
            return {k: v for k, v in _iter_items(value, prefix)}
        else:
            return value

    def _iter_bucket_items(self, agg: Aggregation, response=None):
        # this could be a place to specialize by class
        #if hasattr(agg, "_iter_bucket_items"):
        #    yield from agg._iter_bucket_items(response)
        #else:
        if response is None:
            assert agg.is_bucket()
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

    def _iter_sub_items_rec(self, bucket: dict, aggs: Sequence[Aggregation], parent_key: tuple):
        sub_bucket = bucket[aggs[0].name]

        if len(aggs) == 1:
            yield from self._iter_items_from_bucket(aggs[0], sub_bucket, parent_key)
        else:
            for b_key, b in self._iter_bucket_items(aggs[0], sub_bucket):
                yield from self._iter_sub_items_rec(b, aggs[1:], parent_key + (b_key, ))

    def _iter_items_from_bucket(self, agg: Aggregation, bucket: dict, parent_key: tuple):
        if agg.is_metric():
            return_keys = agg.definition.get("returns", "value")
            values = dict()
            for key in return_keys:
                if key in bucket:
                    value = bucket[key]
                    values[key] = self.make_default(value)

            if len(values) > 1:
                yield parent_key, values
            elif len(values) == 1:
                yield parent_key, values.popitem()[1]
            else:
                yield parent_key, self.make_default(None)
        else:
            if "buckets" in bucket:
                for b_key, b in self._iter_bucket_items(agg, bucket):
                    value = b["doc_count"]
                    yield parent_key + (b_key, ), self.make_default(value)
            else:
                value = bucket["doc_count"]
                yield parent_key + (agg.name, ), self.make_default(value)
