from copy import copy, deepcopy
from typing import Sequence, Union, Optional, Iterable, Tuple, TextIO, Any

from elastipy.aggregation import Aggregation
from elastipy._print import print_dict_rows, dict_rows_to_list_rows


class Visitor:
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

    def dump_table(self, header: bool = True, digits: Optional[int] = None, file: TextIO = None):
        """
        Print the result of the dict_rows() function as table to console.
        :param header: bool, if True, include the names in the first row
        :param digits: int, optional number of digits for rounding
        :param file: optional text stream to print to
        """
        print_dict_rows(self.dict_rows(), header=header, digits=digits, file=file)

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
            if "buckets" in self.agg.response:
                for b_key, b in self._iter_bucket_items(self.agg):
                    if b_key not in b:
                        key = b_key
                    else:
                        key = b[b_key]
                    # wrap into concat in case it does something more at some point
                    yield self._concat_key(key, key_separator=key_separator)
            else:
                # wrap into concat in case it does something more at some point
                yield self._concat_key(self.agg.name, key_separator=key_separator)
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

    def _concat_key(self, key: Union[Any, Sequence], key_separator: Optional[str] = None):
        if isinstance(key, str):
            return key
        if isinstance(key, Sequence):
            if key_separator:
                return key_separator.join(str(i) for i in key)
            return key if len(key) > 1 else key[0]
        return key

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

    def _iter_sub_keys_rec(self, bucket: dict, aggs: Sequence[Aggregation], keys: Tuple[Any, ...]):
        if not aggs[0].name in bucket:
            raise ValueError(f"Expected agg '{aggs[0].name}' in bucket {bucket}")

        sub_bucket = bucket[aggs[0].name]
        key_name = aggs[0].key_name()

        if len(aggs) == 1:
            if aggs[0].is_metric():
                yield keys
            else:
                for b_key, b in self._iter_bucket_items(aggs[0], sub_bucket):
                    if key_name in b:
                        next_key = b[key_name]
                    else:
                        next_key = b_key
                    yield keys + (next_key, )
        else:
            for b_key, b in self._iter_bucket_items(aggs[0], sub_bucket):
                if key_name in b:
                    next_key = b[key_name]
                else:
                    next_key = b_key
                yield from self._iter_sub_keys_rec(b, aggs[1:], keys + (next_key, ))

    def _iter_sub_values(self, aggs: Sequence[Aggregation], default=None):
        for _, b in self._iter_bucket_items(aggs[0]):
            yield from self._iter_sub_values_rec(b, aggs[1:], default=default)

    def _iter_sub_values_rec(self, bucket: dict, aggs: Sequence[Aggregation], default=None):
        sub_bucket = bucket[aggs[0].name]
        if len(aggs) == 1:
            yield from self._iter_values_from_bucket(aggs[0], sub_bucket, default=default)
        else:
            for b_key, b in self._iter_bucket_items(aggs[0], sub_bucket):
                yield from self._iter_sub_values_rec(b, aggs[1:], default=default)

    def _iter_values_from_bucket(self, agg: Aggregation, bucket: dict, default=None):
        def _make_default(value):
            if default is not None and value is None:
                value = default
            return value

        if agg.is_metric():
            return_keys = agg.definition.get("returns", "value")
            values = dict()
            for key in return_keys:
                if key in bucket:
                    value = bucket[key]
                    values[key] = _make_default(value)

            # TODO: it might be empty for some aggregations..
            #if not values:
            #    raise ValueError(f"{self} should have returned fields {return_keys}, got {bucket}")
            if len(values) > 1:
                yield values
            elif len(values) == 1:
                yield values.popitem()[1]
            else:
                yield _make_default(None)
        else:
            if "buckets" in bucket:
                for b_key, b in self._iter_bucket_items(agg, bucket):
                    value = b["doc_count"]
                    yield _make_default(value)
            else:
                value = bucket["doc_count"]
                yield _make_default(value)
