# auto-generated file - do not edit
from datetime import date, datetime
from typing import Mapping, Sequence, Any, Union, Optional

from .interface import AggregationInterfaceBase


class AggregationInterface(AggregationInterfaceBase):

    AGGREGATION_DEFINITION = {'adjacency_matrix': {'group': 'bucket', 'parameters': {'filters': {'type': "Mapping[str, Union[Mapping, 'QueryInterface']]", 'required': True}, 'separator': {'type': 'str'}}}, 'auto_date_histogram': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'timestamp': True}, 'buckets': {'type': 'int', 'default': 10}, 'minimum_interval': {'type': 'str'}, 'time_zone': {'type': 'str'}, 'format': {'type': 'str'}, 'keyed': {'type': 'bool', 'default': False}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}}, 'avg': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'avg_bucket': {'group': 'pipeline', 'parameters': {'buckets_path': {'type': 'str', 'required': True}, 'gap_policy': {'type': 'str', 'default': 'skip'}, 'format': {'type': 'str'}}, 'returns': ['value']}, 'boxplot': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'compression': {'type': 'int', 'default': 100}, 'missing': {'type': 'Any'}}, 'returns': ['min', 'max', 'q1', 'q2', 'q3']}, 'bucket_script': {'group': 'pipeline', 'parameters': {'script': {'type': 'str', 'required': True}, 'buckets_path': {'type': 'Mapping[str, str]', 'required': True}, 'gap_policy': {'type': 'str', 'default': 'skip'}, 'format': {'type': 'str'}}, 'returns': ['value']}, 'cardinality': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'precision_threshold': {'type': 'int', 'default': 3000}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'children': {'group': 'bucket', 'parameters': {'type': {'type': 'str', 'required': True}}}, 'composite': {'group': 'bucket', 'parameters': {'sources': {'type': 'Sequence[Mapping]', 'required': True}, 'size': {'type': 'int', 'default': 10}, 'after': {'type': 'Union[str, int, float, datetime]'}}}, 'date_histogram': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'timestamp': True}, 'calendar_interval': {'type': 'str'}, 'fixed_interval': {'type': 'str'}, 'min_doc_count': {'type': 'int', 'default': 1}, 'offset': {'type': 'str'}, 'time_zone': {'type': 'str'}, 'format': {'type': 'str'}, 'keyed': {'type': 'bool', 'default': False}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}}, 'date_range': {'group': 'bucket', 'parameters': {'ranges': {'type': 'Sequence[Union[Mapping[str, str], str]]', 'required': True, 'ranges': True}, 'field': {'type': 'str', 'timestamp': True}, 'format': {'type': 'str'}, 'time_zone': {'type': 'str'}, 'keyed': {'type': 'bool', 'default': False}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}}, 'derivative': {'group': 'pipeline', 'parameters': {'buckets_path': {'type': 'str', 'required': True}, 'gap_policy': {'type': 'str', 'default': 'skip'}, 'format': {'type': 'str'}, 'units': {'type': 'str'}}, 'returns': ['value']}, 'diversified_sampler': {'group': 'bucket', 'parameters': {'field': {'type': 'str'}, 'script': {'type': 'Mapping'}, 'shard_size': {'type': 'int', 'default': 100}, 'max_docs_per_value': {'type': 'int', 'default': 1}}}, 'extended_stats': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'sigma': {'type': 'float', 'default': 3.0}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['count', 'min', 'max', 'avg', 'sum', 'sum_of_squares', 'variance', 'variance_population', 'variance_sampling', 'std_deviation', 'std_deviation_population', 'std_deviation_sampling', 'std_deviation_bounds']}, 'filter': {'group': 'bucket', 'parameters': {'filter': {'type': "Union[Mapping, 'QueryInterface']", 'required': True}}}, 'filters': {'group': 'bucket', 'parameters': {'filters': {'type': "Mapping[str, Union[Mapping, 'QueryInterface']]", 'required': True}}}, 'geo_bounds': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'wrap_longitude': {'type': 'bool', 'default': True}}, 'returns': ['bounds']}, 'geo_centroid': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}}, 'returns': ['location']}, 'geo_distance': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}, 'ranges': {'type': 'Sequence[Union[Mapping[str, float], float]]', 'required': True, 'ranges': True}, 'origin': {'type': 'Union[str, Mapping[str, float], Sequence[float]]', 'required': True}, 'unit': {'type': 'str', 'default': 'm'}, 'distance_type': {'type': 'str', 'default': 'arc'}, 'keyed': {'type': 'bool', 'default': False}}}, 'geohash_grid': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}, 'precision': {'type': 'Union[int, str]', 'default': 5}, 'bounds': {'type': 'Mapping'}, 'size': {'type': 'int', 'default': 10000}, 'shard_size': {'type': 'int'}}}, 'geotile_grid': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}, 'precision': {'type': 'Union[int, str]', 'default': 7}, 'bounds': {'type': 'Mapping'}, 'size': {'type': 'int', 'default': 10000}, 'shard_size': {'type': 'int'}}}, 'global': {'group': 'bucket', 'parameters': {}}, 'histogram': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}, 'interval': {'type': 'int', 'required': True}, 'min_doc_count': {'type': 'int', 'default': 0}, 'offset': {'type': 'int'}, 'extended_bounds': {'type': 'Mapping[str, int]'}, 'hard_bounds': {'type': 'Mapping[str, int]'}, 'format': {'type': 'str'}, 'order': {'type': 'Union[Mapping, str]', 'order': True}, 'keyed': {'type': 'bool', 'default': False}, 'missing': {'type': 'Any'}}}, 'ip_range': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}, 'ranges': {'type': 'Sequence[Union[Mapping[str, str], str]]', 'required': True, 'ranges': True}, 'keyed': {'type': 'bool', 'default': False}}}, 'matrix_stats': {'group': 'metric', 'parameters': {'fields': {'type': 'list', 'required': True}, 'mode': {'type': 'str', 'default': 'avg'}, 'missing': {'type': 'Any'}}, 'returns': ['fields']}, 'max': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'median_absolute_deviation': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'compression': {'type': 'int', 'default': 1000}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'min': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'missing': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}}}, 'nested': {'group': 'bucket', 'parameters': {'path': {'type': 'str', 'required': True}}}, 'percentile_ranks': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'values': {'type': 'list', 'required': True}, 'keyed': {'type': 'bool', 'default': True}, 'hdr.number_of_significant_value_digits': {'type': 'int'}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['values']}, 'percentiles': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'percents': {'type': 'list', 'default': '(1, 5, 25, 50, 75, 95, 99)'}, 'keyed': {'type': 'bool', 'default': True}, 'tdigest.compression': {'type': 'int', 'default': 100}, 'hdr.number_of_significant_value_digits': {'type': 'int'}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['values']}, 'range': {'group': 'bucket', 'parameters': {'ranges': {'type': 'Sequence[Union[Mapping[str, Any], Any]]', 'required': True, 'ranges': True}, 'field': {'type': 'str'}, 'keyed': {'type': 'bool', 'default': False}, 'script': {'type': 'dict'}}}, 'rare_terms': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}, 'max_doc_count': {'type': 'int', 'default': 1}, 'include': {'type': 'Union[str, Sequence[str], Mapping[str, int]]'}, 'exclude': {'type': 'Union[str, Sequence[str]]'}, 'missing': {'type': 'Any'}}}, 'rate': {'group': 'metric', 'parameters': {'unit': {'type': 'str', 'required': True}, 'field': {'type': 'str'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'sampler': {'group': 'bucket', 'parameters': {'shard_size': {'type': 'int', 'default': 100}}}, 'scripted_metric': {'group': 'metric', 'parameters': {'map_script': {'type': 'str', 'required': True}, 'combine_script': {'type': 'str', 'required': True}, 'reduce_script': {'type': 'str', 'required': True}, 'init_script': {'type': 'str'}, 'params': {'type': 'dict'}}, 'returns': ['value']}, 'significant_terms': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}, 'size': {'type': 'int', 'default': 10}, 'shard_size': {'type': 'int'}, 'min_doc_count': {'type': 'int', 'default': 1}, 'shard_min_doc_count': {'type': 'int'}, 'execution_hint': {'type': 'str', 'default': 'global_ordinals'}, 'include': {'type': 'Union[str, Sequence[str], Mapping[str, int]]'}, 'exclude': {'type': 'Union[str, Sequence[str]]'}, 'script': {'type': 'dict'}}}, 'stats': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}}, 'returns': ['count', 'min', 'max', 'sum', 'count', 'avg']}, 'string_stats': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'show_distribution': {'type': 'bool', 'default': False}, 'missing': {'type': 'Any'}}, 'returns': ['count', 'min_length', 'max_length', 'avg_length', 'entropy', 'distribution']}, 'sum': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 't_test': {'group': 'metric', 'parameters': {'a.field': {'type': 'str', 'required': True}, 'b.field': {'type': 'str', 'required': True}, 'type': {'type': 'str', 'required': True}, 'a.filter': {'type': 'dict'}, 'b.filter': {'type': 'dict'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'terms': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}, 'size': {'type': 'int', 'default': 10}, 'shard_size': {'type': 'int'}, 'show_term_doc_count_error': {'type': 'bool'}, 'order': {'type': 'Union[Mapping, str]', 'order': True}, 'min_doc_count': {'type': 'int', 'default': 1}, 'shard_min_doc_count': {'type': 'int'}, 'include': {'type': 'Union[str, Sequence[str], Mapping[str, int]]'}, 'exclude': {'type': 'Union[str, Sequence[str]]'}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}}, 'top_hits': {'group': 'metric', 'parameters': {'size': {'type': 'int', 'required': True}, 'sort': {'type': 'dict'}, '_source': {'type': 'dict'}}, 'returns': ['hits']}, 'top_metrics': {'group': 'metric', 'parameters': {'metrics': {'type': 'dict', 'required': True}, 'sort': {'type': 'dict'}}, 'returns': ['top']}, 'value_count': {'group': 'metric', 'parameters': {'field': {'type': 'str'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'weighted_avg': {'group': 'metric', 'parameters': {'value.field': {'type': 'str', 'required': True}, 'weight.field': {'type': 'str', 'required': True}, 'value.missing': {'type': 'Any'}, 'weight.missing': {'type': 'Any'}, 'format': {'type': 'str'}, 'value_type': {'type': 'str'}, 'script': {'type': 'dict'}}, 'returns': ['value']}}

    def agg_adjacency_matrix(
            self,
            *aggregation_name: Optional[str],
            filters: Mapping[str, Union[Mapping, 'QueryInterface']],
            separator: Optional[str] = None,
    ):
        """
        A bucket aggregation returning a form of adjacency matrix. The request
        provides a collection of named filter expressions, similar to the filters
        aggregation request. Each bucket in the response represents a non-empty cell
        in the matrix of intersecting filters.

        The matrix is said to be symmetric so we only return half of it. To do this
        we sort the filter name strings and always use the lowest of a pair as the
        value to the left of the ``"&"`` separator.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-adjacency-matrix-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param filters: ``Mapping[str, Union[Mapping, 'QueryInterface']]``

        :param separator: ``Optional[str]``
            An alternative separator parameter can be passed in the request if
            clients wish to use a separator string other than the default of the
            ampersand.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("adjacency_matrix", )),
            filters=filters,
            separator=separator,
        )
        return a

    def agg_auto_date_histogram(
            self,
            *aggregation_name: Optional[str],
            field: Optional[str] = None,
            buckets: int = 10,
            minimum_interval: Optional[str] = None,
            time_zone: Optional[str] = None,
            format: Optional[str] = None,
            keyed: bool = False,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        A multi-bucket aggregation similar to the Date histogram except instead of
        providing an interval to use as the width of each bucket, a target number of
        buckets is provided indicating the number of buckets needed and the interval
        of the buckets is automatically chosen to best achieve that target. The
        number of buckets returned will always be less than or equal to this target
        number.

        The buckets field is optional, and will default to 10 buckets if not
        specified.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-autodatehistogram-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``Optional[str]``
            If no field is specified it will default to the 'timestamp_field' of the
            Search class.

        :param buckets: ``int``
            The number of buckets that are to be returned.

        :param minimum_interval: ``Optional[str]``
            The minimum_interval allows the caller to specify the minimum rounding
            interval that should be used. This can make the collection process more
            efficient, as the aggregation will not attempt to round at any interval
            lower than minimum_interval.

            The accepted units for minimum_interval are: year, month, day, hour,
            minute, second

        :param time_zone: ``Optional[str]``
            Date-times are stored in Elasticsearch in UTC. By default, all bucketing
            and rounding is also done in UTC. The ``time_zone`` parameter can be
            used to indicate that bucketing should use a different time zone.

            Time zones may either be specified as an ISO 8601 UTC offset (e.g.
            ``+01:00`` or ``-08:00``) or as a timezone id, an identifier used in the
            TZ database like America/Los_Angeles.

            .. WARNING::

                When using time zones that follow DST (daylight savings time)
                changes, buckets close to the moment when those changes happen can
                have slightly different sizes than neighbouring buckets. For
                example, consider a DST start in the CET time zone: on 27 March 2016
                at 2am, clocks were turned forward 1 hour to 3am local time. If the
                result of the aggregation was daily buckets, the bucket covering
                that day will only hold data for 23 hours instead of the usual 24
                hours for other buckets. The same is true for shorter intervals like
                e.g. 12h. Here, we will have only a 11h bucket on the morning of 27
                March when the DST shift happens.

        :param format: ``Optional[str]``
            Specifies the format of the 'key_as_string' response. See: `mapping date
            format
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html>`__

        :param keyed: ``bool``
            Setting the keyed flag to true associates a unique string key with each
            bucket and returns the ranges as a hash rather than an array.

        :param missing: ``Optional[Any]``
            The missing parameter defines how documents that are missing a value
            should be treated. By default they will be ignored but it is also
            possible to treat them as if they had a value.

        :param script: ``Optional[dict]``
            Generating the terms using a script

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("auto_date_histogram", )),
            field=field,
            buckets=buckets,
            minimum_interval=minimum_interval,
            time_zone=time_zone,
            format=format,
            keyed=keyed,
            missing=missing,
            script=script,
        )
        return a

    def metric_avg(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        A single-value metrics aggregation that computes the average of numeric
        values that are extracted from the aggregated documents. These values can be
        extracted either from specific numeric fields in the documents, or be
        generated by a provided script.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-avg-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param missing: ``Optional[Any]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("avg", )),
            field=field,
            missing=missing,
            script=script,
            return_self=return_self,
        )
        return a

    def pipeline_avg_bucket(
            self,
            *aggregation_name: Optional[str],
            buckets_path: str,
            gap_policy: str = 'skip',
            format: Optional[str] = None,
            return_self: bool = False,
    ):
        """
        A sibling pipeline aggregation which calculates the (mean) average value of
        a specified metric in a sibling aggregation. The specified metric must be
        numeric and the sibling aggregation must be a multi-bucket aggregation.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-avg-bucket-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param buckets_path: ``str``
            The path to the buckets we wish to find the average for.

            See: `bucket path syntax
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#buckets-path-syntax>`__

        :param gap_policy: ``str``
            The policy to apply when gaps are found in the data.

            See: `gap policy
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#gap-policy>`__

        :param format: ``Optional[str]``
            Format to apply to the output value of this aggregation

        :param return_self: ``bool``
            If True, this call returns the created pipeline, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.pipeline(
            *(aggregation_name + ("avg_bucket", )),
            buckets_path=buckets_path,
            gap_policy=gap_policy,
            format=format,
            return_self=return_self,
        )
        return a

    def metric_boxplot(
            self,
            *aggregation_name: Optional[str],
            field: str,
            compression: int = 100,
            missing: Optional[Any] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-boxplot-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param compression: ``int``

        :param missing: ``Optional[Any]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("boxplot", )),
            field=field,
            compression=compression,
            missing=missing,
            return_self=return_self,
        )
        return a

    def pipeline_bucket_script(
            self,
            *aggregation_name: Optional[str],
            script: str,
            buckets_path: Mapping[str, str],
            gap_policy: str = 'skip',
            format: Optional[str] = None,
            return_self: bool = False,
    ):
        """
        A parent pipeline aggregation which executes a script which can perform per
        bucket computations on specified metrics in the parent multi-bucket
        aggregation. The specified metric must be numeric and the script must return
        a numeric value.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-bucket-script-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param script: ``str``
            The script to run for this aggregation. The script can be inline, file
            or indexed. (see `Scripting
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting.html>`__
            for more details)

        :param buckets_path: ``Mapping[str, str]``
            A map of script variables and their associated path to the buckets we
            wish to use for the variable (see `buckets_path Syntax
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#buckets-path-syntax>`__
            for more details)

        :param gap_policy: ``str``
            The policy to apply when gaps are found in the data (see `Dealing with
            gaps
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#gap-policy>`__
            in the data for more details)

        :param format: ``Optional[str]``
            Format to apply to the output value of this aggregation

        :param return_self: ``bool``
            If True, this call returns the created pipeline, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.pipeline(
            *(aggregation_name + ("bucket_script", )),
            script=script,
            buckets_path=buckets_path,
            gap_policy=gap_policy,
            format=format,
            return_self=return_self,
        )
        return a

    def metric_cardinality(
            self,
            *aggregation_name: Optional[str],
            field: str,
            precision_threshold: int = 3000,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-cardinality-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param precision_threshold: ``int``

        :param missing: ``Optional[Any]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("cardinality", )),
            field=field,
            precision_threshold=precision_threshold,
            missing=missing,
            script=script,
            return_self=return_self,
        )
        return a

    def agg_children(
            self,
            *aggregation_name: Optional[str],
            type: str,
    ):
        """
        A special single bucket aggregation that selects child documents that have
        the specified type, as defined in a `join field
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/parent-join.html>`__.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-children-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param type: ``str``
            The child type that should be selected.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("children", )),
            type=type,
        )
        return a

    def agg_composite(
            self,
            *aggregation_name: Optional[str],
            sources: Sequence[Mapping],
            size: int = 10,
            after: Optional[Union[str, int, float, datetime]] = None,
    ):
        """
        A multi-bucket aggregation that creates composite buckets from different
        sources.

        Unlike the other multi-bucket aggregations, you can use the composite
        aggregation to paginate all buckets from a multi-level aggregation
        efficiently. This aggregation provides a way to stream all buckets of a
        specific aggregation, similar to what `scroll
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#scroll-search-results>`__
        does for documents.

        The composite buckets are built from the combinations of the values
        extracted/created for each document and each combination is considered as a
        composite bucket.

        For optimal performance the `index sort
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-index-sorting.html>`__
        should be set on the index so that it matches parts or fully the source
        order in the composite aggregation.

        **Sub-buckets**: Like any multi-bucket aggregations the composite
        aggregation can hold sub-aggregations. These sub-aggregations can be used to
        compute other buckets or statistics on each composite bucket created by this
        parent aggregation.

        **Pipeline aggregations**: The composite agg is not currently compatible
        with pipeline aggregations, nor does it make sense in most cases. E.g. due
        to the paging nature of composite aggs, a single logical partition (one day
        for example) might be spread over multiple pages. Since pipeline
        aggregations are purely post-processing on the final list of buckets,
        running something like a derivative on a composite page could lead to
        inaccurate results as it is only taking into account a "partial" result on
        that page.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-composite-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param sources: ``Sequence[Mapping]``
            The sources parameter defines the source fields to use when building
            composite buckets. The order that the sources are defined controls the
            order that the keys are returned.

            The sources parameter can be any of the following types:

                - Terms
                - Histogram
                - Date histogram
                - GeoTile grid

            .. NOTE::

                You must use a unique name when defining sources.

        :param size: ``int``
            The size parameter can be set to define how many composite buckets
            should be returned. Each composite bucket is considered as a single
            bucket, so setting a size of 10 will return the first 10 composite
            buckets created from the value sources. The response contains the values
            for each composite bucket in an array containing the values extracted
            from each value source.

            **Pagination**: If the number of composite buckets is too high (or
            unknown) to be returned in a single response it is possible to split the
            retrieval in multiple requests. Since the composite buckets are flat by
            nature, the requested size is exactly the number of composite buckets
            that will be returned in the response (assuming that they are at least
            size composite buckets to return). If all composite buckets should be
            retrieved it is preferable to use a small size (100 or 1000 for
            instance) and then use the after parameter to retrieve the next results.

        :param after: ``Optional[Union[str, int, float, datetime]]``
            To get the next set of buckets, resend the same aggregation with the
            after parameter set to the ``after_key`` value returned in the response.

            .. NOTE::

                The after_key is usually the key to the last bucket returned in the
                response, but that isn’t guaranteed. Always use the returned
                after_key instead of derriving it from the buckets.

            In order to optimize the early termination it is advised to set
            ``track_total_hits`` in the request to false. The number of total hits
            that match the request can be retrieved on the first request and it
            would be costly to compute this number on every page.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("composite", )),
            sources=sources,
            size=size,
            after=after,
        )
        return a

    def agg_date_histogram(
            self,
            *aggregation_name: Optional[str],
            field: Optional[str] = None,
            calendar_interval: Optional[str] = None,
            fixed_interval: Optional[str] = None,
            min_doc_count: int = 1,
            offset: Optional[str] = None,
            time_zone: Optional[str] = None,
            format: Optional[str] = None,
            keyed: bool = False,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        This multi-bucket aggregation is similar to the normal histogram, but it can
        only be used with date or date range values. Because dates are represented
        internally in Elasticsearch as long values, it is possible, but not as
        accurate, to use the normal histogram on dates as well. The main difference
        in the two APIs is that here the interval can be specified using date/time
        expressions. Time-based data requires special support because time-based
        intervals are not always a fixed length.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``Optional[str]``
            If no field is specified it will default to the 'timestamp_field' of the
            Search class.

        :param calendar_interval: ``Optional[str]``
            Calendar-aware intervals are configured with the calendar_interval
            parameter. You can specify calendar intervals using the unit name, such
            as ``month``, or as a single unit quantity, such as ``1M``. For example,
            ``day`` and ``1d`` are equivalent. Multiple quantities, such as ``2d``,
            are not supported.

        :param fixed_interval: ``Optional[str]``
            In contrast to calendar-aware intervals, fixed intervals are a fixed
            number of SI units and never deviate, regardless of where they fall on
            the calendar. One second is always composed of 1000ms. This allows fixed
            intervals to be specified in any multiple of the supported units.

            However, it means fixed intervals cannot express other units such as
            months, since the duration of a month is not a fixed quantity.
            Attempting to specify a calendar interval like month or quarter will
            throw an exception.

            The accepted units for fixed intervals are:

                - milliseconds (``ms``): A single millisecond. This is a very, very
                  small interval.
                - seconds (``s``): Defined as 1000 milliseconds each.
                - minutes (``m``): Defined as 60 seconds each (60,000 milliseconds).
                  All minutes begin at 00 seconds.
                - hours (``h``): Defined as 60 minutes each (3,600,000
                  milliseconds). All hours begin at 00 minutes and 00 seconds.
                - days (``d``): Defined as 24 hours (86,400,000 milliseconds). All
                  days begin at the earliest possible time, which is usually
                  00:00:00 (midnight).

        :param min_doc_count: ``int``
            Minimum documents required for a bucket. Set to 0 to allow creating
            empty buckets.

        :param offset: ``Optional[str]``
            Use the offset parameter to change the start value of each bucket by the
            specified positive (+) or negative offset (-) duration, such as ``1h``
            for an hour, or ``1d`` for a day. See `Time units
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#time-units>`__
            for more possible time duration options.

            For example, when using an interval of day, each bucket runs from
            midnight to midnight. Setting the offset parameter to ``+6h`` changes
            each bucket to run from 6am to 6am

        :param time_zone: ``Optional[str]``
            Elasticsearch stores date-times in Coordinated Universal Time (UTC). By
            default, all bucketing and rounding is also done in UTC. Use the
            time_zone parameter to indicate that bucketing should use a different
            time zone.

            For example, if the interval is a calendar day and the time zone is
            ``America/New_York`` then ``2020-01-03T01:00:01Z`` is

                - converted to ``2020-01-02T18:00:01``
                - rounded down to ``2020-01-02T00:00:00``
                - then converted back to UTC to produce ``2020-01-02T05:00:00:00Z``
                - finally, when the bucket is turned into a string key it is printed
                  in ``America/New_York`` so it’ll display as
                  ``"2020-01-02T00:00:00"``

            It looks like:

                ``bucket_key = localToUtc(Math.floor(utcToLocal(value) / interval) *
                interval))``

            You can specify time zones as an ISO 8601 UTC offset (e.g. ``+01:00`` or
            ``-08:00``) or as an IANA time zone ID, such as America/Los_Angeles.

        :param format: ``Optional[str]``
            Specifies the format of the 'key_as_string' response. See: `mapping date
            format
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html>`__

        :param keyed: ``bool``
            Setting the keyed flag to true associates a unique string key with each
            bucket and returns the ranges as a hash rather than an array.

        :param missing: ``Optional[Any]``
            The missing parameter defines how documents that are missing a value
            should be treated. By default they will be ignored but it is also
            possible to treat them as if they had a value.

        :param script: ``Optional[dict]``
            Generating the terms using a script

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("date_histogram", )),
            field=field,
            calendar_interval=calendar_interval,
            fixed_interval=fixed_interval,
            min_doc_count=min_doc_count,
            offset=offset,
            time_zone=time_zone,
            format=format,
            keyed=keyed,
            missing=missing,
            script=script,
        )
        return a

    def agg_date_range(
            self,
            *aggregation_name: Optional[str],
            ranges: Sequence[Union[Mapping[str, str], str]],
            field: Optional[str] = None,
            format: Optional[str] = None,
            time_zone: Optional[str] = None,
            keyed: bool = False,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        A range aggregation that is dedicated for date values. The main difference
        between this aggregation and the normal `range
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-range-aggregation.html>`__
        aggregation is that the from and to values can be expressed in `Date Math
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math>`__
        expressions, and it is also possible to specify a date format by which the
        from and to response fields will be returned.

        .. NOTE::

            Note that this aggregation includes the from value and excludes the to
            value for each range.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-daterange-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param ranges: ``Sequence[Union[Mapping[str, str], str]]``
            List of ranges to define the buckets

            Example:

            .. CODE::

                [
                    {"to": "1970-01-01"},
                    {"from": "1970-01-01", "to": "1980-01-01"},
                    {"from": "1980-01-01"},
                ]

            Instead of date values any `Date Math
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math>`__
            expression can be used as well.

            Alternatively this parameter can be a list of strings. The above example
            can be rewritten as: ``["1970-01-01", "1980-01-01"]``

            .. NOTE::

                This aggregation includes the from value and excludes the to value
                for each range.

        :param field: ``Optional[str]``
            The date field

            If no field is specified it will default to the 'timestamp_field' of the
            Search class.

        :param format: ``Optional[str]``
            The format of the response bucket keys as available for the
            `DateTimeFormatter
            <https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html>`__

        :param time_zone: ``Optional[str]``
            Dates can be converted from another time zone to UTC by specifying the
            time_zone parameter.

            Time zones may either be specified as an ISO 8601 UTC offset (e.g.
            ``+01:00`` or ``-08:00``) or as one of the time zone ids from the TZ
            database.

            The time_zone parameter is also applied to rounding in date math
            expressions.

        :param keyed: ``bool``
            Setting the keyed flag to true associates a unique string key with each
            bucket and returns the ranges as a hash rather than an array.

        :param missing: ``Optional[Any]``
            The missing parameter defines how documents that are missing a value
            should be treated. By default they will be ignored but it is also
            possible to treat them as if they had a value.

        :param script: ``Optional[dict]``
            Generating the terms using a script

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("date_range", )),
            ranges=ranges,
            field=field,
            format=format,
            time_zone=time_zone,
            keyed=keyed,
            missing=missing,
            script=script,
        )
        return a

    def pipeline_derivative(
            self,
            *aggregation_name: Optional[str],
            buckets_path: str,
            gap_policy: str = 'skip',
            format: Optional[str] = None,
            units: Optional[str] = None,
            return_self: bool = False,
    ):
        """
        A parent pipeline aggregation which calculates the derivative of a specified
        metric in a parent histogram (or date_histogram) aggregation. The specified
        metric must be numeric and the enclosing histogram must have min_doc_count
        set to 0 (default for histogram aggregations).

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-derivative-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param buckets_path: ``str``
            The path to the buckets we wish to find the average for.

            See: `bucket path syntax
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#buckets-path-syntax>`__

        :param gap_policy: ``str``
            The policy to apply when gaps are found in the data.

            See: `gap policy
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#gap-policy>`__

        :param format: ``Optional[str]``
            Format to apply to the output value of this aggregation

        :param units: ``Optional[str]``
            The derivative aggregation allows the units of the derivative values to
            be specified. This returns an extra field in the response
            normalized_value which reports the derivative value in the desired
            x-axis units.

        :param return_self: ``bool``
            If True, this call returns the created pipeline, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.pipeline(
            *(aggregation_name + ("derivative", )),
            buckets_path=buckets_path,
            gap_policy=gap_policy,
            format=format,
            units=units,
            return_self=return_self,
        )
        return a

    def agg_diversified_sampler(
            self,
            *aggregation_name: Optional[str],
            field: Optional[str] = None,
            script: Optional[Mapping] = None,
            shard_size: int = 100,
            max_docs_per_value: int = 1,
    ):
        """
        Like the ``sampler`` aggregation this is a filtering aggregation used to
        limit any sub aggregations' processing to a sample of the top-scoring
        documents. The ``diversified_sampler`` aggregation adds the ability to limit
        the number of matches that share a common value such as an "author".

        .. NOTE::

            Any good market researcher will tell you that when working with samples
            of data it is important that the sample represents a healthy variety of
            opinions rather than being skewed by any single voice. The same is true
            with aggregations and sampling with these diversify settings can offer a
            way to remove the bias in your content (an over-populated geography, a
            large spike in a timeline or an over-active forum spammer).

        Example use cases:

            - Tightening the focus of analytics to high-relevance matches rather
              than the potentially very long tail of low-quality matches
            - Removing bias from analytics by ensuring fair representation of
              content from different sources
            - Reducing the running cost of aggregations that can produce useful
              results using only samples e.g. significant_terms

        A choice of field or script setting is used to provide values used for
        de-duplication and the ``max_docs_per_value`` setting controls the maximum
        number of documents collected on any one shard which share a common value.
        The default setting for ``max_docs_per_value`` is 1.

        .. NOTE::

            The aggregation will throw an error if the choice of field or script
            produces multiple values for a single document (de-duplication using
            multi-valued fields is not supported due to efficiency concerns).

        `Limitations:
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-diversified-sampler-aggregation.html#_limitations_5>`__

            Cannot be nested under breadth_first aggregations Being a quality-based
            filter the diversified_sampler aggregation needs access to the relevance
            score produced for each document. It therefore cannot be nested under a
            terms aggregation which has the collect_mode switched from the default
            depth_first mode to breadth_first as this discards scores. In this
            situation an error will be thrown.

            Limited de-dup logic. The de-duplication logic applies only at a shard
            level so will not apply across shards.

            No specialized syntax for geo/date fields Currently the syntax for
            defining the diversifying values is defined by a choice of field or
            script - there is no added syntactical sugar for expressing geo or date
            units such as ``"7d"`` (7 days). This support may be added in a later
            release and users will currently have to create these sorts of values
            using a script.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-diversified-sampler-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``Optional[str]``
            The field to search on. Can alternatively be a script

        :param script: ``Optional[Mapping]``
            The script that specifies the aggregation. Can alternatively be a
            'field'

        :param shard_size: ``int``
            The shard_size parameter limits how many top-scoring documents are
            collected in the sample processed on each shard. The default value is
            100.

        :param max_docs_per_value: ``int``
            The max_docs_per_value is an optional parameter and limits how many
            documents are permitted per choice of de-duplicating value. The default
            setting is 1.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("diversified_sampler", )),
            field=field,
            script=script,
            shard_size=shard_size,
            max_docs_per_value=max_docs_per_value,
        )
        return a

    def metric_extended_stats(
            self,
            *aggregation_name: Optional[str],
            field: str,
            sigma: float = 3.0,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-extendedstats-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param sigma: ``float``

        :param missing: ``Optional[Any]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("extended_stats", )),
            field=field,
            sigma=sigma,
            missing=missing,
            script=script,
            return_self=return_self,
        )
        return a

    def agg_filter(
            self,
            *aggregation_name: Optional[str],
            filter: Union[Mapping, 'QueryInterface'],
    ):
        """
        Defines a single bucket of all the documents in the current document set
        context that match a specified filter. Often this will be used to narrow
        down the current aggregation context to a specific set of documents.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filter-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param filter: ``Union[Mapping, 'QueryInterface']``

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("filter", )),
            filter=filter,
        )
        return a

    def agg_filters(
            self,
            *aggregation_name: Optional[str],
            filters: Mapping[str, Union[Mapping, 'QueryInterface']],
    ):
        """
        Defines a multi bucket aggregation where each bucket is associated with a
        filter. Each bucket will collect all documents that match its associated
        filter.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filters-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param filters: ``Mapping[str, Union[Mapping, 'QueryInterface']]``

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("filters", )),
            filters=filters,
        )
        return a

    def metric_geo_bounds(
            self,
            *aggregation_name: Optional[str],
            field: str,
            wrap_longitude: bool = True,
            return_self: bool = False,
    ):
        """
        A metric aggregation that computes the bounding box containing all geo
        values for a field.

        The Geo Bounds Aggregation is also supported on geo_shape fields.

        If wrap_longitude is set to true (the default), the bounding box can overlap
        the international date line and return a bounds where the top_left longitude
        is larger than the top_right longitude.

        For example, the upper right longitude will typically be greater than the
        lower left longitude of a geographic bounding box. However, when the area
        crosses the 180° meridian, the value of the lower left longitude will be
        greater than the value of the upper right longitude. See `Geographic
        bounding box
        <http://docs.opengeospatial.org/is/12-063r5/12-063r5.html#30>`__ on the Open
        Geospatial Consortium website for more information.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geobounds-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``
            The field defining the geo_point or geo_shape

        :param wrap_longitude: ``bool``
            An optional parameter which specifies whether the bounding box should be
            allowed to overlap the international date line. The default value is
            true.

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("geo_bounds", )),
            field=field,
            wrap_longitude=wrap_longitude,
            return_self=return_self,
        )
        return a

    def metric_geo_centroid(
            self,
            *aggregation_name: Optional[str],
            field: str,
            return_self: bool = False,
    ):
        """
        A metric aggregation that computes the weighted `centroid
        <https://en.wikipedia.org/wiki/Centroid>`__ from all coordinate values for
        geo fields.

        The centroid metric for geo-shapes is more nuanced than for points. The
        centroid of a specific aggregation bucket containing shapes is the centroid
        of the highest-dimensionality shape type in the bucket. For example, if a
        bucket contains shapes comprising of polygons and lines, then the lines do
        not contribute to the centroid metric. Each type of shape’s centroid is
        calculated differently. Envelopes and circles ingested via the `Circle
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-circle-processor.html>`__
        are treated as polygons.

        .. WARNING::

            Using geo_centroid as a sub-aggregation of ``geohash_grid``:

            The geohash_grid aggregation places documents, not individual
            geo-points, into buckets. If a document’s geo_point field contains
            multiple values, the document could be assigned to multiple buckets,
            even if one or more of its geo-points are outside the bucket boundaries.

            If a geocentroid sub-aggregation is also used, each centroid is
            calculated using all geo-points in a bucket, including those outside the
            bucket boundaries. This can result in centroids outside of bucket
            boundaries.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geocentroid-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``
            The field defining the geo_point or geo_shape

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("geo_centroid", )),
            field=field,
            return_self=return_self,
        )
        return a

    def agg_geo_distance(
            self,
            *aggregation_name: Optional[str],
            field: str,
            ranges: Sequence[Union[Mapping[str, float], float]],
            origin: Union[str, Mapping[str, float], Sequence[float]],
            unit: str = 'm',
            distance_type: str = 'arc',
            keyed: bool = False,
    ):
        """
        A multi-bucket aggregation that works on geo_point fields and conceptually
        works very similar to the `range
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-range-aggregation.html>`__
        aggregation. The user can define a point of origin and a set of distance
        range buckets. The aggregation evaluate the distance of each document value
        from the origin point and determines the buckets it belongs to based on the
        ranges (a document belongs to a bucket if the distance between the document
        and the origin falls within the distance range of the bucket).

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geodistance-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``
            The specified field must be of type geo_point (which can only be set
            explicitly in the mappings). And it can also hold an array of geo_point
            fields, in which case all will be taken into account during aggregation.

        :param ranges: ``Sequence[Union[Mapping[str, float], float]]``
            A list of ranges that define the separate buckets, e.g:

            .. CODE::

                [ { "to": 100000 }, { "from": 100000, "to": 300000 }, { "from":
                300000 } ]

            Alternatively this parameter can be a list of numbers. The above example
            can be rewritten as ``[100000, 300000]``

        :param origin: ``Union[str, Mapping[str, float], Sequence[float]]``
            The origin point can accept all formats supported by the `geo_point type
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html>`__:

                - Object format: ``{ "lat" : 52.3760, "lon" : 4.894 }`` - this is
                  the safest format as it is the most explicit about the lat & lon
                  values
                - String format: ``"52.3760, 4.894"`` - where the first number is
                  the lat and the second is the lon
                - Array format: ``[4.894, 52.3760]`` - which is based on the GeoJson
                  standard and where the first number is the lon and the second one
                  is the lat

        :param unit: ``str``
            By default, the distance unit is ``m`` (meters) but it can also accept:
            ``mi`` (miles), ``in`` (inches), ``yd`` (yards), ``km`` (kilometers),
            ``cm`` (centimeters), ``mm`` (millimeters).

        :param distance_type: ``str``
            There are two distance calculation modes: ``arc`` (the default), and
            ``plane``. The arc calculation is the most accurate. The plane is the
            fastest but least accurate. Consider using plane when your search
            context is "narrow", and spans smaller geographical areas (~5km).
            ``plane`` will return higher error margins for searches across very
            large areas (e.g. cross continent search).

        :param keyed: ``bool``
            Setting the keyed flag to true will associate a unique string key with
            each bucket and return the ranges as a hash rather than an array.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("geo_distance", )),
            field=field,
            ranges=ranges,
            origin=origin,
            unit=unit,
            distance_type=distance_type,
            keyed=keyed,
        )
        return a

    def agg_geohash_grid(
            self,
            *aggregation_name: Optional[str],
            field: str,
            precision: Union[int, str] = 5,
            bounds: Optional[Mapping] = None,
            size: int = 10000,
            shard_size: Optional[int] = None,
    ):
        """
        A multi-bucket aggregation that works on geo_point fields and groups points
        into buckets that represent cells in a grid. The resulting grid can be
        sparse and only contains cells that have matching data. Each cell is labeled
        using a `geohash <https://en.wikipedia.org/wiki/Geohash>`__ which is of
        user-definable precision.

            - High precision geohashes have a long string length and represent cells
              that cover only a small area.

            - Low precision geohashes have a short string length and represent cells
              that each cover a large area.

        Geohashes used in this aggregation can have a choice of precision between 1
        and 12.

        The highest-precision geohash of length 12 produces cells that cover less
        than a square metre of land and so high-precision requests can be very
        costly in terms of RAM and result sizes.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geohashgrid-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``
            The specified field must be of type ``geo_point`` or ``geo_shape``
            (which can only be set explicitly in the mappings). And it can also hold
            an array of geo_point fields, in which case all will be taken into
            account during aggregation.

            Aggregating on Geo-shape fields works just as it does for points, except
            that a single shape can be counted for in multiple tiles. A shape will
            contribute to the count of matching values if any part of its shape
            intersects with that tile.

        :param precision: ``Union[int, str]``
            The required precision of the grid in the range [1, 12]. Higher means
            more precise.

            Alternatively, the precision level can be approximated from a distance
            measure like ``"1km"``, ``"10m"``. The precision level is calculate such
            that cells will not exceed the specified size (diagonal) of the required
            precision. When this would lead to precision levels higher than the
            supported 12 levels, (e.g. for distances <5.6cm) the value is rejected.

            .. NOTE::

                When requesting detailed buckets (typically for displaying a "zoomed
                in" map) a filter like `geo_bounding_box
                <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-bounding-box-query.html>`__
                should be applied to narrow the subject area otherwise potentially
                millions of buckets will be created and returned.

        :param bounds: ``Optional[Mapping]``
            The geohash_grid aggregation supports an optional bounds parameter that
            restricts the points considered to those that fall within the bounds
            provided. The bounds parameter accepts the bounding box in all the same
            `accepted formats
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-bounding-box-query.html#query-dsl-geo-bounding-box-query-accepted-formats>`__
            of the bounds specified in the Geo Bounding Box Query. This bounding box
            can be used with or without an additional geo_bounding_box query
            filtering the points prior to aggregating. It is an independent bounding
            box that can intersect with, be equal to, or be disjoint to any
            additional geo_bounding_box queries defined in the context of the
            aggregation.

        :param size: ``int``
            The maximum number of geohash buckets to return (defaults to 10,000).
            When results are trimmed, buckets are prioritised based on the volumes
            of documents they contain.

        :param shard_size: ``Optional[int]``
            To allow for more accurate counting of the top cells returned in the
            final result the aggregation defaults to returning ``max(10, (size x
            number-of-shards))`` buckets from each shard. If this heuristic is
            undesirable, the number considered from each shard can be over-ridden
            using this parameter.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("geohash_grid", )),
            field=field,
            precision=precision,
            bounds=bounds,
            size=size,
            shard_size=shard_size,
        )
        return a

    def agg_geotile_grid(
            self,
            *aggregation_name: Optional[str],
            field: str,
            precision: Union[int, str] = 7,
            bounds: Optional[Mapping] = None,
            size: int = 10000,
            shard_size: Optional[int] = None,
    ):
        """
        A multi-bucket aggregation that works on geo_point fields and groups points
        into buckets that represent cells in a grid. The resulting grid can be
        sparse and only contains cells that have matching data. Each cell
        corresponds to a `map tile <https://en.wikipedia.org/wiki/Tiled_web_map>`__
        as used by many online map sites. Each cell is labeled using a
        "{zoom}/{x}/{y}" format, where zoom is equal to the user-specified
        precision.

            - High precision keys have a larger range for x and y, and represent
              tiles that cover only a small area.

            - Low precision keys have a smaller range for x and y, and represent
              tiles that each cover a large area.

        .. WARNING::

            The highest-precision geotile of length 29 produces cells that cover
            less than a 10cm by 10cm of land and so high-precision requests can be
            very costly in terms of RAM and result sizes. Please first filter the
            aggregation to a smaller geographic area before requesting high-levels
            of detail.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geotilegrid-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``
            The specified field must be of type geo_point (which can only be set
            explicitly in the mappings). And it can also hold an array of geo_point
            fields, in which case all will be taken into account during aggregation.

        :param precision: ``Union[int, str]``
            The required precision of the grid in the range [1, 29]. Higher means
            more precise.

            .. NOTE::

                When requesting detailed buckets (typically for displaying a "zoomed
                in" map) a filter like `geo_bounding_box
                <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-bounding-box-query.html>`__
                should be applied to narrow the subject area otherwise potentially
                millions of buckets will be created and returned.

        :param bounds: ``Optional[Mapping]``
            The geotile_grid aggregation supports an optional bounds parameter that
            restricts the points considered to those that fall within the bounds
            provided. The bounds parameter accepts the bounding box in all the same
            `accepted formats
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-bounding-box-query.html#query-dsl-geo-bounding-box-query-accepted-formats>`__
            of the bounds specified in the Geo Bounding Box Query. This bounding box
            can be used with or without an additional ``geo_bounding_box`` query
            filtering the points prior to aggregating. It is an independent bounding
            box that can intersect with, be equal to, or be disjoint to any
            additional geo_bounding_box queries defined in the context of the
            aggregation.

        :param size: ``int``
            The maximum number of geohash buckets to return (defaults to 10,000).
            When results are trimmed, buckets are prioritised based on the volumes
            of documents they contain.

        :param shard_size: ``Optional[int]``
            To allow for more accurate counting of the top cells returned in the
            final result the aggregation defaults to returning ``max(10, (size x
            number-of-shards))`` buckets from each shard. If this heuristic is
            undesirable, the number considered from each shard can be over-ridden
            using this parameter.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("geotile_grid", )),
            field=field,
            precision=precision,
            bounds=bounds,
            size=size,
            shard_size=shard_size,
        )
        return a

    def agg_global(
            self,
            *aggregation_name: Optional[str],
    ):
        """
        Defines a single bucket of all the documents within the search execution
        context. This context is defined by the indices and the document types
        you’re searching on, but is not influenced by the search query itself.

        .. NOTE::

            Global aggregators can only be placed as top level aggregators because
            it doesn’t make sense to embed a global aggregator within another bucket
            aggregator.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-global-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("global", )),
        )
        return a

    def agg_histogram(
            self,
            *aggregation_name: Optional[str],
            field: str,
            interval: int,
            min_doc_count: int = 0,
            offset: Optional[int] = None,
            extended_bounds: Optional[Mapping[str, int]] = None,
            hard_bounds: Optional[Mapping[str, int]] = None,
            format: Optional[str] = None,
            order: Optional[Union[Mapping, str]] = None,
            keyed: bool = False,
            missing: Optional[Any] = None,
    ):
        """
        A multi-bucket values source based aggregation that can be applied on
        numeric values or numeric range values extracted from the documents. It
        dynamically builds fixed size (a.k.a. interval) buckets over the values. For
        example, if the documents have a field that holds a price (numeric), we can
        configure this aggregation to dynamically build buckets with interval 5 (in
        case of price it may represent $5). When the aggregation executes, the price
        field of every document will be evaluated and will be rounded down to its
        closest bucket - for example, if the price is 32 and the bucket size is 5
        then the rounding will yield 30 and thus the document will "fall" into the
        bucket that is associated with the key 30. To make this more formal, here is
        the rounding function that is used:

            ``bucket_key = Math.floor((value - offset) / interval) * interval +
            offset``

        For range values, a document can fall into multiple buckets. The first
        bucket is computed from the lower bound of the range in the same way as a
        bucket for a single value is computed. The final bucket is computed in the
        same way from the upper bound of the range, and the range is counted in all
        buckets in between and including those two.

        The interval must be a positive decimal, while the offset must be a decimal
        in [0, interval) (a decimal greater than or equal to 0 and less than
        interval)

        Histogram fields: Running a histogram aggregation over histogram fields
        computes the total number of counts for each interval. See `example
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-histogram-aggregation.html#search-aggregations-bucket-histogram-aggregation-histogram-fields>`__

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-histogram-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``
            A numeric field to be indexed by the histogram.

        :param interval: ``int``
            A positive decimal defining the interval between buckets.

        :param min_doc_count: ``int``
            By default the response will fill gaps in the histogram with empty
            buckets. It is possible change that and request buckets with a higher
            minimum count thanks to the min_doc_count setting

            By default the histogram returns all the buckets within the range of the
            data itself, that is, the documents with the smallest values (on which
            with histogram) will determine the min bucket (the bucket with the
            smallest key) and the documents with the highest values will determine
            the max bucket (the bucket with the highest key). Often, when requesting
            empty buckets, this causes a confusion, specifically, when the data is
            also filtered.

            To understand why, let’s look at an example:

                Lets say the you’re filtering your request to get all docs with
                values between 0 and 500, in addition you’d like to slice the data
                per price using a histogram with an interval of 50. You also specify
                "min_doc_count" : 0 as you’d like to get all buckets even the empty
                ones. If it happens that all products (documents) have prices higher
                than 100, the first bucket you’ll get will be the one with 100 as
                its key. This is confusing, as many times, you’d also like to get
                those buckets between 0 - 100.

        :param offset: ``Optional[int]``
            By default the bucket keys start with 0 and then continue in even spaced
            steps of interval, e.g. if the interval is 10, the first three buckets
            (assuming there is data inside them) will be [0, 10), [10, 20), [20,
            30). The bucket boundaries can be shifted by using the offset option.

            This can be best illustrated with an example. If there are 10 documents
            with values ranging from 5 to 14, using interval 10 will result in two
            buckets with 5 documents each. If an additional offset 5 is used, there
            will be only one single bucket [5, 15) containing all the 10 documents.

        :param extended_bounds: ``Optional[Mapping[str, int]]``
            With extended_bounds setting, you now can "force" the histogram
            aggregation to start building buckets on a specific min value and also
            keep on building buckets up to a max value (even if there are no
            documents anymore). Using extended_bounds only makes sense when
            ``min_doc_count`` is 0 (the empty buckets will never be returned if
            min_doc_count is greater than 0).

            Note that (as the name suggest) extended_bounds is not filtering
            buckets. Meaning, if the extended_bounds.min is higher than the values
            extracted from the documents, the documents will still dictate what the
            first bucket will be (and the same goes for the extended_bounds.max and
            the last bucket). For filtering buckets, one should nest the histogram
            aggregation under a range filter aggregation with the appropriate
            from/to settings.

            When aggregating ranges, buckets are based on the values of the returned
            documents. This means the response may include buckets outside of a
            query’s range. For example, if your query looks for values greater than
            100, and you have a range covering 50 to 150, and an interval of 50,
            that document will land in 3 buckets - 50, 100, and 150. In general,
            it’s best to think of the query and aggregation steps as independent -
            the query selects a set of documents, and then the aggregation buckets
            those documents without regard to how they were selected. See note on
            bucketing range fields for more information and an example.

        :param hard_bounds: ``Optional[Mapping[str, int]]``
            The hard_bounds is a counterpart of extended_bounds and can limit the
            range of buckets in the histogram. It is particularly useful in the case
            of open `data ranges
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/range.html>`__
            that can result in a very large number of buckets.

        :param format: ``Optional[str]``
            Specifies the format of the 'key_as_string' response. See: `mapping date
            format
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html>`__

        :param order: ``Optional[Union[Mapping, str]]``
            By default the returned buckets are sorted by their key ascending,
            though the order behaviour can be controlled using the order setting.
            Supports the same order functionality as the `Terms Aggregation
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#search-aggregations-bucket-terms-aggregation-order>`__.

        :param keyed: ``bool``
            Setting the keyed flag to true associates a unique string key with each
            bucket and returns the ranges as a hash rather than an array.

        :param missing: ``Optional[Any]``
            The missing parameter defines how documents that are missing a value
            should be treated. By default they will be ignored but it is also
            possible to treat them as if they had a value.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("histogram", )),
            field=field,
            interval=interval,
            min_doc_count=min_doc_count,
            offset=offset,
            extended_bounds=extended_bounds,
            hard_bounds=hard_bounds,
            format=format,
            order=order,
            keyed=keyed,
            missing=missing,
        )
        return a

    def agg_ip_range(
            self,
            *aggregation_name: Optional[str],
            field: str,
            ranges: Sequence[Union[Mapping[str, str], str]],
            keyed: bool = False,
    ):
        """
        Just like the dedicated `date range
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-daterange-aggregation.html>`__
        aggregation, there is also a dedicated range aggregation for IP typed
        fields:

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-iprange-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``
            The IPv4 field

        :param ranges: ``Sequence[Union[Mapping[str, str], str]]``
            List of ranges to define the buckets, either as straight IPv4 or as CIDR
            masks.

            Example:

            .. CODE::

                [
                    {"to": "10.0.0.5"},
                    {"from": "10.0.0.5", "to": "10.0.0.127"},
                    {"from": "10.0.0.127"},
                ]

            Alternatively this parameter can be a list of strings. The above example
            can be rewritten as: ``["10.0.0.5", "10.0.0.127"]``

        :param keyed: ``bool``
            Setting the keyed flag to true associates a unique string key with each
            bucket and returns the ranges as a hash rather than an array.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("ip_range", )),
            field=field,
            ranges=ranges,
            keyed=keyed,
        )
        return a

    def metric_matrix_stats(
            self,
            *aggregation_name: Optional[str],
            fields: list,
            mode: str = 'avg',
            missing: Optional[Any] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-matrix-stats-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param fields: ``list``

        :param mode: ``str``

        :param missing: ``Optional[Any]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("matrix_stats", )),
            fields=fields,
            mode=mode,
            missing=missing,
            return_self=return_self,
        )
        return a

    def metric_max(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-max-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param missing: ``Optional[Any]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("max", )),
            field=field,
            missing=missing,
            script=script,
            return_self=return_self,
        )
        return a

    def metric_median_absolute_deviation(
            self,
            *aggregation_name: Optional[str],
            field: str,
            compression: int = 1000,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-median-absolute-deviation-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param compression: ``int``

        :param missing: ``Optional[Any]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("median_absolute_deviation", )),
            field=field,
            compression=compression,
            missing=missing,
            script=script,
            return_self=return_self,
        )
        return a

    def metric_min(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-min-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param missing: ``Optional[Any]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("min", )),
            field=field,
            missing=missing,
            script=script,
            return_self=return_self,
        )
        return a

    def agg_missing(
            self,
            *aggregation_name: Optional[str],
            field: str,
    ):
        """
        A field data based single bucket aggregation, that creates a bucket of all
        documents in the current document set context that are missing a field value
        (effectively, missing a field or having the configured NULL value set). This
        aggregator will often be used in conjunction with other field data bucket
        aggregators (such as ranges) to return information for all the documents
        that could not be placed in any of the other buckets due to missing field
        data values.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-missing-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``
            The field we wish to investigate for missing values

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("missing", )),
            field=field,
        )
        return a

    def agg_nested(
            self,
            *aggregation_name: Optional[str],
            path: str,
    ):
        """
        A special single bucket aggregation that enables aggregating nested
        documents.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/7.10/search-aggregations-bucket-nested-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param path: ``str``
            The field of the nested document(s)

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("nested", )),
            path=path,
        )
        return a

    def metric_percentile_ranks(
            self,
            *aggregation_name: Optional[str],
            field: str,
            values: list,
            keyed: bool = True,
            hdr__number_of_significant_value_digits: Optional[int] = None,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-rank-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param values: ``list``

        :param keyed: ``bool``

        :param hdr__number_of_significant_value_digits: ``Optional[int]``

        :param missing: ``Optional[Any]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("percentile_ranks", )),
            field=field,
            values=values,
            keyed=keyed,
            hdr__number_of_significant_value_digits=hdr__number_of_significant_value_digits,
            missing=missing,
            script=script,
            return_self=return_self,
        )
        return a

    def metric_percentiles(
            self,
            *aggregation_name: Optional[str],
            field: str,
            percents: list = '(1, 5, 25, 50, 75, 95, 99)',
            keyed: bool = True,
            tdigest__compression: int = 100,
            hdr__number_of_significant_value_digits: Optional[int] = None,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param percents: ``list``

        :param keyed: ``bool``

        :param tdigest__compression: ``int``

        :param hdr__number_of_significant_value_digits: ``Optional[int]``

        :param missing: ``Optional[Any]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("percentiles", )),
            field=field,
            percents=percents,
            keyed=keyed,
            tdigest__compression=tdigest__compression,
            hdr__number_of_significant_value_digits=hdr__number_of_significant_value_digits,
            missing=missing,
            script=script,
            return_self=return_self,
        )
        return a

    def agg_range(
            self,
            *aggregation_name: Optional[str],
            ranges: Sequence[Union[Mapping[str, Any], Any]],
            field: Optional[str] = None,
            keyed: bool = False,
            script: Optional[dict] = None,
    ):
        """
        A multi-bucket value source based aggregation that enables the user to
        define a set of ranges - each representing a bucket. During the aggregation
        process, the values extracted from each document will be checked against
        each bucket range and "bucket" the relevant/matching document.

        .. NOTE::

            Note that this aggregation includes the from value and excludes the to
            value for each range.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-range-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param ranges: ``Sequence[Union[Mapping[str, Any], Any]]``
            List of ranges to define the buckets

            Example:

            .. CODE::

                [
                    {"to": 10},
                    {"from": 10, "to": 20},
                    {"from": 20},
                ]

            Alternatively this parameter can be a list of strings. The above example
            can be rewritten as: ``[10, 20]``

            .. NOTE::

                This aggregation includes the from value and excludes the to value
                for each range.

        :param field: ``Optional[str]``
            The field to index by the aggregation

        :param keyed: ``bool``
            Setting the keyed flag to true associates a unique string key with each
            bucket and returns the ranges as a hash rather than an array.

        :param script: ``Optional[dict]``
            Generating the terms using a script

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("range", )),
            ranges=ranges,
            field=field,
            keyed=keyed,
            script=script,
        )
        return a

    def agg_rare_terms(
            self,
            *aggregation_name: Optional[str],
            field: str,
            max_doc_count: int = 1,
            include: Optional[Union[str, Sequence[str], Mapping[str, int]]] = None,
            exclude: Optional[Union[str, Sequence[str]]] = None,
            missing: Optional[Any] = None,
    ):
        """
        A multi-bucket value source based aggregation which finds "rare"
        terms — terms that are at the long-tail of the distribution and are not
        frequent. Conceptually, this is like a terms aggregation that is sorted by
        ``_count`` ascending. As noted in the `terms aggregation docs
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#search-aggregations-bucket-terms-aggregation-order>`__,
        actually ordering a terms agg by count ascending has unbounded error.
        Instead, you should use the rare_terms aggregation.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-rare-terms-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``
            The field we wish to find rare terms in

        :param max_doc_count: ``int``
            The maximum number of documents a term should appear in.

            The max_doc_count parameter is used to control the upper bound of
            document counts that a term can have. There is not a size limitation on
            the rare_terms agg like terms agg has. This means that terms which match
            the max_doc_count criteria will be returned. The aggregation functions
            in this manner to avoid the order-by-ascending issues that afflict the
            terms aggregation.

            This does, however, mean that a large number of results can be returned
            if chosen incorrectly. To limit the danger of this setting, the maximum
            max_doc_count is 100.

        :param include: ``Optional[Union[str, Sequence[str], Mapping[str, int]]]``
            A `regexp
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/regexp-syntax.html>`__
            pattern that filters the documents which will be aggregated.

            Alternatively can be a list of strings.

            `Parition expressions
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#_filtering_values_with_partitions>`__
            are also possible.

        :param exclude: ``Optional[Union[str, Sequence[str]]]``
            A `regexp
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/regexp-syntax.html>`__
            pattern that filters the documents which will be aggregated.

            Alternatively can be a list of strings.

        :param missing: ``Optional[Any]``
            The missing parameter defines how documents that are missing a value
            should be treated. By default they will be ignored but it is also
            possible to treat them as if they had a value.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("rare_terms", )),
            field=field,
            max_doc_count=max_doc_count,
            include=include,
            exclude=exclude,
            missing=missing,
        )
        return a

    def metric_rate(
            self,
            *aggregation_name: Optional[str],
            unit: str,
            field: Optional[str] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-rate-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param unit: ``str``

        :param field: ``Optional[str]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("rate", )),
            unit=unit,
            field=field,
            script=script,
            return_self=return_self,
        )
        return a

    def agg_sampler(
            self,
            *aggregation_name: Optional[str],
            shard_size: int = 100,
    ):
        """
        A filtering aggregation used to limit any sub aggregations' processing to a
        sample of the top-scoring documents.

        Example use cases:

            - Tightening the focus of analytics to high-relevance matches rather
              than the potentially very long tail of low-quality matches

            - Reducing the running cost of aggregations that can produce useful
              results using only samples e.g. significant_terms

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-sampler-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param shard_size: ``int``
            The shard_size parameter limits how many top-scoring documents are
            collected in the sample processed on each shard. The default value is
            100.

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("sampler", )),
            shard_size=shard_size,
        )
        return a

    def metric_scripted_metric(
            self,
            *aggregation_name: Optional[str],
            map_script: str,
            combine_script: str,
            reduce_script: str,
            init_script: Optional[str] = None,
            params: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-scripted-metric-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param map_script: ``str``

        :param combine_script: ``str``

        :param reduce_script: ``str``

        :param init_script: ``Optional[str]``

        :param params: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("scripted_metric", )),
            map_script=map_script,
            combine_script=combine_script,
            reduce_script=reduce_script,
            init_script=init_script,
            params=params,
            return_self=return_self,
        )
        return a

    def agg_significant_terms(
            self,
            *aggregation_name: Optional[str],
            field: str,
            size: int = 10,
            shard_size: Optional[int] = None,
            min_doc_count: int = 1,
            shard_min_doc_count: Optional[int] = None,
            execution_hint: str = 'global_ordinals',
            include: Optional[Union[str, Sequence[str], Mapping[str, int]]] = None,
            exclude: Optional[Union[str, Sequence[str]]] = None,
            script: Optional[dict] = None,
    ):
        """
        An aggregation that returns interesting or unusual occurrences of terms in a
        set.

        Example use cases:

            - Suggesting "H5N1" when users search for "bird flu" in text
            - Identifying the merchant that is the "common point of compromise" from
              the transaction history of credit card owners reporting loss
            - Suggesting keywords relating to stock symbol $ATI for an automated
              news classifier
            - Spotting the fraudulent doctor who is diagnosing more than their fair
              share of whiplash injuries
            - Spotting the tire manufacturer who has a disproportionate number of
              blow-outs

        In all these cases the terms being selected are not simply the most popular
        terms in a set. They are the terms that have undergone a significant change
        in popularity measured between a foreground and background set. If the term
        "H5N1" only exists in 5 documents in a 10 million document index and yet is
        found in 4 of the 100 documents that make up a user’s search results that is
        significant and probably very relevant to their search. ``5/10,000,000`` vs
        ``4/100`` is a big swing in frequency.

        .. WARNING::

            Picking a free-text field as the subject of a significant terms analysis
            can be expensive! It will attempt to load every unique word into RAM. It
            is recommended to only use this on smaller indices.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/master/search-aggregations-bucket-significantterms-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param size: ``int``
            The size parameter can be set to define how many term buckets should be
            returned out of the overall terms list. By default, the node
            coordinating the search process will request each shard to provide its
            own top size term buckets and once all shards respond, it will reduce
            the results to the final list that will then be returned to the client.
            This means that if the number of unique terms is greater than size, the
            returned list is slightly off and not accurate (it could be that the
            term counts are slightly off and it could even be that a term that
            should have been in the top size buckets was not returned).

        :param shard_size: ``Optional[int]``
            The higher the requested size is, the more accurate the results will be,
            but also, the more expensive it will be to compute the final results
            (both due to bigger priority queues that are managed on a shard level
            and due to bigger data transfers between the nodes and the client).

            The shard_size parameter can be used to minimize the extra work that
            comes with bigger requested size. When defined, it will determine how
            many terms the coordinating node will request from each shard. Once all
            the shards responded, the coordinating node will then reduce them to a
            final result which will be based on the size parameter - this way, one
            can increase the accuracy of the returned terms and avoid the overhead
            of streaming a big list of buckets back to the client.

        :param min_doc_count: ``int``
            It is possible to only return terms that match more than a configured
            number of hits using the min_doc_count option. Default value is 1.

            Terms are collected and ordered on a shard level and merged with the
            terms collected from other shards in a second step. However, the shard
            does not have the information about the global document count available.
            The decision if a term is added to a candidate list depends only on the
            order computed on the shard using local shard frequencies. The
            min_doc_count criterion is only applied after merging local terms
            statistics of all shards. In a way the decision to add the term as a
            candidate is made without being very certain about if the term will
            actually reach the required min_doc_count. This might cause many
            (globally) high frequent terms to be missing in the final result if low
            frequent terms populated the candidate lists. To avoid this, the
            shard_size parameter can be increased to allow more candidate terms on
            the shards. However, this increases memory consumption and network
            traffic.

        :param shard_min_doc_count: ``Optional[int]``
            The parameter shard_min_doc_count regulates the certainty a shard has if
            the term should actually be added to the candidate list or not with
            respect to the min_doc_count. Terms will only be considered if their
            local shard frequency within the set is higher than the
            shard_min_doc_count. If your dictionary contains many low frequent terms
            and you are not interested in those (for example misspellings), then you
            can set the shard_min_doc_count parameter to filter out candidate terms
            on a shard level that will with a reasonable certainty not reach the
            required min_doc_count even after merging the local counts.
            shard_min_doc_count is set to 0 per default and has no effect unless you
            explicitly set it.

            .. NOTE::

                Setting min_doc_count=0 will also return buckets for terms that
                didn’t match any hit. However, some of the returned terms which have
                a document count of zero might only belong to deleted documents or
                documents from other types, so there is no warranty that a match_all
                query would find a positive document count for those terms.

            .. WARNING::

                When NOT sorting on doc_count descending, high values of
                min_doc_count may return a number of buckets which is less than size
                because not enough data was gathered from the shards. Missing
                buckets can be back by increasing shard_size. Setting
                shard_min_doc_count too high will cause terms to be filtered out on
                a shard level. This value should be set much lower than
                min_doc_count/#shards.

        :param execution_hint: ``str``
            There are different mechanisms by which terms aggregations can be
            executed:

                - by using field values directly in order to aggregate data
                  per-bucket (``map``)
                - by using global ordinals of the field and allocating one bucket
                  per global ordinal (``global_ordinals``)

            Elasticsearch tries to have sensible defaults so this is something that
            generally doesn’t need to be configured.

            ``global_ordinals`` is the default option for keyword field, it uses
            global ordinals to allocates buckets dynamically so memory usage is
            linear to the number of values of the documents that are part of the
            aggregation scope.

            ``map`` should only be considered when very few documents match a query.
            Otherwise the ordinals-based execution mode is significantly faster. By
            default, ``map`` is only used when running an aggregation on scripts,
            since they don’t have ordinals.

        :param include: ``Optional[Union[str, Sequence[str], Mapping[str, int]]]``
            A `regexp
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/regexp-syntax.html>`__
            pattern that filters the documents which will be aggregated.

            Alternatively can be a list of strings.

            `Parition expressions
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#_filtering_values_with_partitions>`__
            are also possible.

        :param exclude: ``Optional[Union[str, Sequence[str]]]``
            A `regexp
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/regexp-syntax.html>`__
            pattern that filters the documents which will be aggregated.

            Alternatively can be a list of strings.

        :param script: ``Optional[dict]``
            Generating the terms using a script

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("significant_terms", )),
            field=field,
            size=size,
            shard_size=shard_size,
            min_doc_count=min_doc_count,
            shard_min_doc_count=shard_min_doc_count,
            execution_hint=execution_hint,
            include=include,
            exclude=exclude,
            script=script,
        )
        return a

    def metric_stats(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-stats-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param missing: ``Optional[Any]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("stats", )),
            field=field,
            missing=missing,
            return_self=return_self,
        )
        return a

    def metric_string_stats(
            self,
            *aggregation_name: Optional[str],
            field: str,
            show_distribution: bool = False,
            missing: Optional[Any] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-string-stats-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param show_distribution: ``bool``

        :param missing: ``Optional[Any]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("string_stats", )),
            field=field,
            show_distribution=show_distribution,
            missing=missing,
            return_self=return_self,
        )
        return a

    def metric_sum(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-sum-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param missing: ``Optional[Any]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("sum", )),
            field=field,
            missing=missing,
            script=script,
            return_self=return_self,
        )
        return a

    def metric_t_test(
            self,
            *aggregation_name: Optional[str],
            a__field: str,
            b__field: str,
            type: str,
            a__filter: Optional[dict] = None,
            b__filter: Optional[dict] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-ttest-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param a__field: ``str``

        :param b__field: ``str``

        :param type: ``str``

        :param a__filter: ``Optional[dict]``

        :param b__filter: ``Optional[dict]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("t_test", )),
            a__field=a__field,
            b__field=b__field,
            type=type,
            a__filter=a__filter,
            b__filter=b__filter,
            script=script,
            return_self=return_self,
        )
        return a

    def agg_terms(
            self,
            *aggregation_name: Optional[str],
            field: str,
            size: int = 10,
            shard_size: Optional[int] = None,
            show_term_doc_count_error: Optional[bool] = None,
            order: Optional[Union[Mapping, str]] = None,
            min_doc_count: int = 1,
            shard_min_doc_count: Optional[int] = None,
            include: Optional[Union[str, Sequence[str], Mapping[str, int]]] = None,
            exclude: Optional[Union[str, Sequence[str]]] = None,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        A multi-bucket value source based aggregation where buckets are dynamically
        built - one per unique value.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``str``

        :param size: ``int``
            The size parameter can be set to define how many term buckets should be
            returned out of the overall terms list. By default, the node
            coordinating the search process will request each shard to provide its
            own top size term buckets and once all shards respond, it will reduce
            the results to the final list that will then be returned to the client.
            This means that if the number of unique terms is greater than size, the
            returned list is slightly off and not accurate (it could be that the
            term counts are slightly off and it could even be that a term that
            should have been in the top size buckets was not returned).

        :param shard_size: ``Optional[int]``
            The higher the requested size is, the more accurate the results will be,
            but also, the more expensive it will be to compute the final results
            (both due to bigger priority queues that are managed on a shard level
            and due to bigger data transfers between the nodes and the client).

            The shard_size parameter can be used to minimize the extra work that
            comes with bigger requested size. When defined, it will determine how
            many terms the coordinating node will request from each shard. Once all
            the shards responded, the coordinating node will then reduce them to a
            final result which will be based on the size parameter - this way, one
            can increase the accuracy of the returned terms and avoid the overhead
            of streaming a big list of buckets back to the client.

        :param show_term_doc_count_error: ``Optional[bool]``
            This shows an error value for each term returned by the aggregation
            which represents the worst case error in the document count and can be
            useful when deciding on a value for the shard_size parameter. This is
            calculated by summing the document counts for the last term returned by
            all shards which did not return the term.

            These errors can only be calculated in this way when the terms are
            ordered by descending document count. When the aggregation is ordered by
            the terms values themselves (either ascending or descending) there is no
            error in the document count since if a shard does not return a
            particular term which appears in the results from another shard, it must
            not have that term in its index. When the aggregation is either sorted
            by a sub aggregation or in order of ascending document count, the error
            in the document counts cannot be determined and is given a value of -1
            to indicate this.

        :param order: ``Optional[Union[Mapping, str]]``
            The order of the buckets can be customized by setting the order
            parameter. By default, the buckets are ordered by their doc_count
            descending.

            .. WARNING::

                Sorting by ascending _count or by sub aggregation is discouraged as
                it increases the error on document counts. It is fine when a single
                shard is queried, or when the field that is being aggregated was
                used as a routing key at index time: in these cases results will be
                accurate since shards have disjoint values. However otherwise,
                errors are unbounded. One particular case that could still be useful
                is sorting by min or max aggregation: counts will not be accurate
                but at least the top buckets will be correctly picked.

        :param min_doc_count: ``int``
            It is possible to only return terms that match more than a configured
            number of hits using the min_doc_count option. Default value is 1.

            Terms are collected and ordered on a shard level and merged with the
            terms collected from other shards in a second step. However, the shard
            does not have the information about the global document count available.
            The decision if a term is added to a candidate list depends only on the
            order computed on the shard using local shard frequencies. The
            min_doc_count criterion is only applied after merging local terms
            statistics of all shards. In a way the decision to add the term as a
            candidate is made without being very certain about if the term will
            actually reach the required min_doc_count. This might cause many
            (globally) high frequent terms to be missing in the final result if low
            frequent terms populated the candidate lists. To avoid this, the
            shard_size parameter can be increased to allow more candidate terms on
            the shards. However, this increases memory consumption and network
            traffic.

        :param shard_min_doc_count: ``Optional[int]``
            The parameter shard_min_doc_count regulates the certainty a shard has if
            the term should actually be added to the candidate list or not with
            respect to the min_doc_count. Terms will only be considered if their
            local shard frequency within the set is higher than the
            shard_min_doc_count. If your dictionary contains many low frequent terms
            and you are not interested in those (for example misspellings), then you
            can set the shard_min_doc_count parameter to filter out candidate terms
            on a shard level that will with a reasonable certainty not reach the
            required min_doc_count even after merging the local counts.
            shard_min_doc_count is set to 0 per default and has no effect unless you
            explicitly set it.

            .. NOTE::

                Setting min_doc_count=0 will also return buckets for terms that
                didn’t match any hit. However, some of the returned terms which have
                a document count of zero might only belong to deleted documents or
                documents from other types, so there is no warranty that a match_all
                query would find a positive document count for those terms.

            .. WARNING::

                When NOT sorting on doc_count descending, high values of
                min_doc_count may return a number of buckets which is less than size
                because not enough data was gathered from the shards. Missing
                buckets can be back by increasing shard_size. Setting
                shard_min_doc_count too high will cause terms to be filtered out on
                a shard level. This value should be set much lower than
                min_doc_count/#shards.

        :param include: ``Optional[Union[str, Sequence[str], Mapping[str, int]]]``
            A `regexp
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/regexp-syntax.html>`__
            pattern that filters the documents which will be aggregated.

            Alternatively can be a list of strings.

            `Parition expressions
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#_filtering_values_with_partitions>`__
            are also possible.

        :param exclude: ``Optional[Union[str, Sequence[str]]]``
            A `regexp
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/regexp-syntax.html>`__
            pattern that filters the documents which will be aggregated.

            Alternatively can be a list of strings.

        :param missing: ``Optional[Any]``
            The missing parameter defines how documents that are missing a value
            should be treated. By default they will be ignored but it is also
            possible to treat them as if they had a value.

        :param script: ``Optional[dict]``
            Generating the terms using a script

        :returns: ``'AggregationInterface'``
            A new instance is created and returned
        """
        a = self.agg(
            *(aggregation_name + ("terms", )),
            field=field,
            size=size,
            shard_size=shard_size,
            show_term_doc_count_error=show_term_doc_count_error,
            order=order,
            min_doc_count=min_doc_count,
            shard_min_doc_count=shard_min_doc_count,
            include=include,
            exclude=exclude,
            missing=missing,
            script=script,
        )
        return a

    def metric_top_hits(
            self,
            *aggregation_name: Optional[str],
            size: int,
            sort: Optional[dict] = None,
            _source: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-top-hits-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param size: ``int``

        :param sort: ``Optional[dict]``

        :param _source: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("top_hits", )),
            size=size,
            sort=sort,
            _source=_source,
            return_self=return_self,
        )
        return a

    def metric_top_metrics(
            self,
            *aggregation_name: Optional[str],
            metrics: dict,
            sort: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-top-metrics.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param metrics: ``dict``

        :param sort: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("top_metrics", )),
            metrics=metrics,
            sort=sort,
            return_self=return_self,
        )
        return a

    def metric_value_count(
            self,
            *aggregation_name: Optional[str],
            field: Optional[str] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        A single-value metrics aggregation that counts the number of values that are
        extracted from the aggregated documents. These values can be extracted
        either from specific fields in the documents, or be generated by a provided
        script. Typically, this aggregator will be used in conjunction with other
        single-value aggregations. For example, when computing the avg one might be
        interested in the number of values the average is computed over.

        value_count does not de-duplicate values, so even if a field has duplicates
        (or a script generates multiple identical values for a single document),
        each value will be counted individually.

        .. NOTE::

            Because value_count is designed to work with any field it internally
            treats all values as simple bytes. Due to this implementation, if _value
            script variable is used to fetch a value instead of accessing the field
            directly (e.g. a "value script"), the field value will be returned as a
            string instead of it’s native format.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-valuecount-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: ``Optional[str]``
            The field who's values should be counted

        :param script: ``Optional[dict]``
            Alternatively counting the values generated by a script

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("value_count", )),
            field=field,
            script=script,
            return_self=return_self,
        )
        return a

    def metric_weighted_avg(
            self,
            *aggregation_name: Optional[str],
            value__field: str,
            weight__field: str,
            value__missing: Optional[Any] = None,
            weight__missing: Optional[Any] = None,
            format: Optional[str] = None,
            value_type: Optional[str] = None,
            script: Optional[dict] = None,
            return_self: bool = False,
    ):
        """
        A single-value metrics aggregation that computes the weighted average of
        numeric values that are extracted from the aggregated documents. These
        values can be extracted either from specific numeric fields in the
        documents.

        When calculating a regular average, each datapoint has an equal "weight" …​
        it contributes equally to the final value. Weighted averages, on the other
        hand, weight each datapoint differently. The amount that each datapoint
        contributes to the final value is extracted from the document, or provided
        by a script.

        As a formula, a weighted average is the ``∑(value * weight) / ∑(weight)``

        A regular average can be thought of as a weighted average where every value
        has an implicit weight of 1

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-weight-avg-aggregation.html>`__

        :param aggregation_name: ``Optional[str]``
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param value__field: ``str``
            The field that values should be extracted from

        :param weight__field: ``str``
            The field that weights should be extracted from

        :param value__missing: ``Optional[Any]``
            A value to use if the field is missing entirely

        :param weight__missing: ``Optional[Any]``
            A weight to use if the field is missing entirely

        :param format: ``Optional[str]``

        :param value_type: ``Optional[str]``

        :param script: ``Optional[dict]``

        :param return_self: ``bool``
            If True, this call returns the created metric, otherwise the parent is
            returned.

        :returns: ``'AggregationInterface'``
            A new instance is created and attached to the parent and the parent is
            returned, unless 'return_self' is True, in which case the new instance
            is returned.
        """
        a = self.metric(
            *(aggregation_name + ("weighted_avg", )),
            value__field=value__field,
            weight__field=weight__field,
            value__missing=value__missing,
            weight__missing=weight__missing,
            format=format,
            value_type=value_type,
            script=script,
            return_self=return_self,
        )
        return a
