import fnmatch
from copy import copy, deepcopy
from itertools import chain
from typing import Sequence, Union, Optional, Iterable, Tuple, TextIO, Any, Mapping, List

from elastipy.aggregation import Aggregation
from .helper import wildcard_filter


class Visitor:
    """
    Helper to access the results of aggregations.

    This is not a public API! Use the methods exposed on the Aggregation class.
    """

    def __init__(self, agg: Aggregation, key_separator: str = None, default_value=None, tuple_key: bool = None):
        self.agg = agg
        self.default_value = default_value
        self.key_separator = key_separator
        self.tuple_key = tuple_key

    def iter_tree(
            self,
            root: Aggregation = None,
            group: Optional[Union[str, Sequence[str]]] = None,
            depth_first: bool = True
    ):
        """
        Iterate through all aggregations starting at self
        :param root: optional root aggregation to start at
        :param group: filter for specific group or groups
        :param depth_first: True: depth-first, False: breadth-first
        :return: generator
        """
        if isinstance(group, str):
            group = [group]

        agg = self.agg if root is None else root

        if group is None or self.agg.group in group:
            yield agg

        yield from self._iter_tree(agg, group=group, depth_first=depth_first)

    def _iter_tree(self, agg: Aggregation, group=None, depth_first: bool = True):
        if depth_first:
            for c in agg.children:
                if group is None or c.group in group:
                    yield c
                yield from self._iter_tree(c, depth_first=depth_first)
        else:
            for c in agg.children:
                if group is None or c.group in group:
                    yield c
            for c in agg.children:
                yield from self._iter_tree(c, depth_first=depth_first)

    def items(self) -> Iterable[Tuple]:
        """
        Iterates through all keys and values of this aggregation.
        :return: generator
        """
        for key, value in self._items():
            if not key:
                key = self.agg.name
            yield self.concat_key(key), self.make_default(value)

    def dict_rows(
            self,
            include: Union[str, Sequence[str]] = None,
            exclude: Union[str, Sequence[str]] = None,
            flat: Union[bool, str, Sequence[str]] = False,
    ) -> Iterable[dict]:
        """
        Iterates through all result values from this aggregation branch.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics and pipelines).

        :param include: ``str`` or ``sequence of str``
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that does not fit a pattern is removed.

        :param exclude: ``str`` or ``sequence of str``
            Can be one or more (OR-combined) wildcard patterns.
            If used, any column that fits a pattern is removed.

        :param flat: ``bool``, ``str`` or ``sequence of str``
            Can be one or more aggregation names that should be *flattened out*,
            meaning that each key of the aggregation creates a new column
            instead of a new row.

            .. NOTE::
                Currently not supported for the root aggregation!

        :return: generator of dict
        """
        root = self.agg.root

        if flat is True:
            flat = [a.name for a in self.iter_tree(root=root, group="bucket")]
        elif isinstance(flat, str):
            flat = [flat]
        elif not flat:
            flat = []

        for row in self._dict_rows(root, root.search.response.aggregations[root.name], flat):
            if include or exclude:
                row = {
                    key: value
                    for key, value in row.items()
                    if wildcard_filter(key, include, exclude)
                }
            yield row

    def root_branch(self):
        aggs = []
        a = self.agg
        while a:
            aggs.insert(0, a)
            a = a.parent
        return aggs

    def key_names(self, buckets: bool = True) -> List[str]:
        """
        Return all names of aggregation branch, starting at root

        :param buckets: ``bool``
            If True, do not return metric/pipeline names unless
            it's the only aggregation
        :return: list[str]
        """
        aggs = self.root_branch()
        if len(aggs) == 1:
            return [aggs[0].name]
        else:
            return [a.name for a in aggs if not buckets or a.is_bucket()]

    def concat_key(self, key: Union[Any, Sequence]):
        if isinstance(key, str):
            pass
        elif isinstance(key, tuple):
            if self.key_separator:
                key = self.key_separator.join(str(i) for i in key)
            else:
                key = key if len(key) > 1 else key[0]
        else:
            raise NotImplementedError(f"Unhandled key type {type(key).__name__}")

        if self.tuple_key and not isinstance(key, tuple):
            key = (key, )
        return key

    def make_default(self, value):
        if self.default_value is not None and value is None:
            value = self.default_value
        return value

    def _dict_rows(self, agg: Aggregation, response: dict, flat):
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

                    if bucket_agg.name not in flat:
                        for sub_row in self._dict_rows(bucket_agg, bucket[bucket_agg.name], flat):
                            # copy the row until here
                            full_row = copy(row)
                            # and add each sub-aggregation's values
                            full_row.update(sub_row)
                            yield full_row

                    else:
                        # drop the "agg_name" and "agg_name.doc_count" columns
                        # and instead use the value in "agg_name" column as column key
                        # and the "agg_name.doc_count" value as value in that column
                        agg_value_key = f"{bucket_agg.name}.doc_count"
                        for sub_row in self._dict_rows(bucket_agg, bucket[bucket_agg.name], flat):
                            # the value in "agg_name" a.k.a the key
                            sub_agg_key = sub_row[bucket_agg.name]
                            row[sub_agg_key] = sub_row[agg_value_key]
                            for key, value in sub_row.items():
                                if key != bucket_agg.name and key != agg_value_key:
                                    # sub-aggregations get their key attached
                                    row[f"{sub_agg_key}.{key}"] = value
                        yield row

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

    def _items(self):
        if not self.agg.parent:
            yield from self._iter_items_from_bucket(self.agg, self.agg.response, tuple())
            return

        aggs = self.root_branch()
        for b_key, b in self._iter_bucket_items(aggs[0]):
            yield from self._iter_sub_items_rec(b, aggs[1:], (b_key, ))

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
