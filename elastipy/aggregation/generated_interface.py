# auto-generated file - do not edit
from datetime import date, datetime
from typing import Mapping, Sequence, Any, Union, Optional

from .interface import AggregationInterfaceBase


class AggregationInterface(AggregationInterfaceBase):

    AGGREGATION_DEFINITION = {'scripted_metric': {'group': 'metric', 'parameters': {'map_script': {'type': 'str', 'required': True}, 'combine_script': {'type': 'str', 'required': True}, 'reduce_script': {'type': 'str', 'required': True}, 'init_script': {'type': 'str'}, 'params': {'type': 'dict'}}, 'returns': ['value']}, 'avg': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'max': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 't_test': {'group': 'metric', 'parameters': {'a.field': {'type': 'str', 'required': True}, 'b.field': {'type': 'str', 'required': True}, 'type': {'type': 'str', 'required': True}, 'a.filter': {'type': 'dict'}, 'b.filter': {'type': 'dict'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'percentiles': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'percents': {'type': 'list', 'default': '(1, 5, 25, 50, 75, 95, 99)'}, 'keyed': {'type': 'bool', 'default': True}, 'tdigest.compression': {'type': 'int', 'default': 100}, 'hdr.number_of_significant_value_digits': {'type': 'int'}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['values']}, 'rate': {'group': 'metric', 'parameters': {'unit': {'type': 'str', 'required': True}, 'field': {'type': 'str'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'weighted_avg': {'group': 'metric', 'parameters': {'value.field': {'type': 'str', 'required': True}, 'weight.field': {'type': 'str', 'required': True}, 'value.missing': {'type': 'Any'}, 'weight.missing': {'type': 'Any'}, 'format': {'type': 'str'}, 'value_type': {'type': 'str'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'top_metrics': {'group': 'metric', 'parameters': {'metrics': {'type': 'dict', 'required': True}, 'sort': {'type': 'dict'}}, 'returns': ['top']}, 'extended_stats': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'sigma': {'type': 'float', 'default': 3.0}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['count', 'min', 'max', 'avg', 'sum', 'sum_of_squares', 'variance', 'variance_population', 'variance_sampling', 'std_deviation', 'std_deviation_population', 'std_deviation_sampling', 'std_deviation_bounds']}, 'string_stats': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'show_distribution': {'type': 'bool', 'default': False}, 'missing': {'type': 'Any'}}, 'returns': ['count', 'min_length', 'max_length', 'avg_length', 'entropy', 'distribution']}, 'top_hits': {'group': 'metric', 'parameters': {'size': {'type': 'int', 'required': True}, 'sort': {'type': 'dict'}, '_source': {'type': 'dict'}}, 'returns': ['hits']}, 'value_count': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'matrix_stats': {'group': 'metric', 'parameters': {'fields': {'type': 'list', 'required': True}, 'mode': {'type': 'str', 'default': 'avg'}, 'missing': {'type': 'Any'}}, 'returns': ['fields']}, 'geo_bounds': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'wrap_longitude': {'type': 'bool', 'default': True}}, 'returns': ['top_left', 'bottom_right']}, 'min': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'median_absolute_deviation': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'compression': {'type': 'int', 'default': 1000}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'cardinality': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'precision_threshold': {'type': 'int', 'default': 3000}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'geo_centroid': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}}, 'returns': ['location']}, 'boxplot': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'compression': {'type': 'int', 'default': 100}, 'missing': {'type': 'Any'}}, 'returns': ['min', 'max', 'q1', 'q2', 'q3']}, 'sum': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'percentile_ranks': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'values': {'type': 'list', 'required': True}, 'keyed': {'type': 'bool', 'default': True}, 'hdr.number_of_significant_value_digits': {'type': 'int'}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['values']}, 'stats': {'group': 'metric', 'parameters': {'field': {'type': 'str', 'required': True}, 'missing': {'type': 'Any'}}, 'returns': ['count', 'min', 'max', 'sum', 'count', 'avg']}, 'auto_date_histogram': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'timestamp': True}, 'buckets': {'type': 'int', 'default': 10}, 'minimum_interval': {'type': 'str'}, 'time_zone': {'type': 'str'}, 'format': {'type': 'str'}, 'keyed': {'type': 'bool', 'default': False}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}}, 'terms': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'required': True}, 'size': {'type': 'int', 'default': 10}, 'shard_size': {'type': 'int'}, 'show_term_doc_count_error': {'type': 'bool'}, 'order': {'type': 'dict'}, 'min_doc_count': {'type': 'int', 'default': 1}, 'shard_min_doc_count': {'type': 'int'}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}, 'returns': ['value']}, 'filter': {'group': 'bucket', 'parameters': {'filter': {'type': 'QueryInterface', 'required': True}}}, 'date_histogram': {'group': 'bucket', 'parameters': {'field': {'type': 'str', 'timestamp': True}, 'calendar_interval': {'type': 'str'}, 'fixed_interval': {'type': 'str'}, 'min_doc_count': {'type': 'int', 'default': 1}, 'offset': {'type': 'str'}, 'time_zone': {'type': 'str'}, 'format': {'type': 'str'}, 'keyed': {'type': 'bool', 'default': False}, 'missing': {'type': 'Any'}, 'script': {'type': 'dict'}}}, 'filters': {'group': 'bucket', 'parameters': {'filters': {'type': "Mapping[str, 'QueryInterface']", 'required': True}}}, 'derivative': {'group': 'pipeline', 'parameters': {'buckets_path': {'type': 'str', 'required': True}, 'gap_policy': {'type': 'str', 'default': 'skip'}, 'format': {'type': 'str'}, 'units': {'type': 'str'}}, 'returns': ['value']}, 'avg_bucket': {'group': 'pipeline', 'parameters': {'buckets_path': {'type': 'str', 'required': True}, 'gap_policy': {'type': 'str', 'default': 'skip'}, 'format': {'type': 'str'}}, 'returns': ['value']}}

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

        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-autodatehistogram-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: Optional[str]
            If no field is specified it will default to the 'timestamp_field' of the
            Search class.

        :param buckets: int
            The number of buckets that are to be returned.

        :param minimum_interval: Optional[str]
            The minimum_interval allows the caller to specify the minimum rounding
            interval that should be used. This can make the collection process more
            efficient, as the aggregation will not attempt to round at any interval
            lower than minimum_interval.

            The accepted units for minimum_interval are:
                year, month, day, hour, minute, second

        :param time_zone: Optional[str]
            Elasticsearch stores date-times in Coordinated Universal Time (UTC). By
            default, all bucketing and rounding is also done in UTC. Use the
            time_zone parameter to indicate that bucketing should use a different
            time zone.

            For example, if the interval is a calendar day and the time zone is
            America/New_York then 2020-01-03T01:00:01Z is : # Converted to
            2020-01-02T18:00:01 # Rounded down to 2020-01-02T00:00:00 # Then
            converted back to UTC to produce 2020-01-02T05:00:00:00Z # Finally, when
            the bucket is turned into a string key it is printed in America/New_York
            so it’ll display as "2020-01-02T00:00:00"

            It looks like: bucket_key = localToUtc(Math.floor(utcToLocal(value) /
            interval) * interval))

            You can specify time zones as an ISO 8601 UTC offset (e.g. +01:00 or
            -08:00) or as an IANA time zone ID, such as America/Los_Angeles.

        :param format: Optional[str]
            Specifies the format of the 'key_as_string' response.
            See:
            https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html

        :param keyed: bool
            Setting the keyed flag to true associates a unique string key with each
            bucket and returns the ranges as a hash rather than an array.

        :param missing: Optional[Any]
            The missing parameter defines how documents that are missing a value
            should be treated. By default they will be ignored but it is also
            possible to treat them as if they had a value.

        :param script: Optional[dict]
            Generating the terms using a script

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.agg(
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
        return agg

    def metric_avg(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        A single-value metrics aggregation that computes the average of numeric
        values that are extracted from the aggregated documents. These values can be
        extracted either from specific numeric fields in the documents, or be
        generated by a provided script.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-avg-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param missing: Optional[Any]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("avg", )),
            field=field,
            missing=missing,
            script=script,
        )
        return agg

    def pipeline_avg_bucket(
            self,
            *aggregation_name: Optional[str],
            buckets_path: str,
            gap_policy: str = 'skip',
            format: Optional[str] = None,
    ):
        """
        A sibling pipeline aggregation which calculates the (mean) average value of
        a specified metric in a sibling aggregation. The specified metric must be
        numeric and the sibling aggregation must be a multi-bucket aggregation.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-avg-bucket-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param buckets_path: str
            The path to the buckets we wish to find the average for.

            https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#buckets-path-syntax

        :param gap_policy: str
            The policy to apply when gaps are found in the data.

            https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#gap-policy

        :param format: Optional[str]
            Format to apply to the output value of this aggregation

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.pipeline(
            *(aggregation_name + ("avg_bucket", )),
            buckets_path=buckets_path,
            gap_policy=gap_policy,
            format=format,
        )
        return agg

    def metric_boxplot(
            self,
            *aggregation_name: Optional[str],
            field: str,
            compression: int = 100,
            missing: Optional[Any] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-boxplot-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param compression: int

        :param missing: Optional[Any]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("boxplot", )),
            field=field,
            compression=compression,
            missing=missing,
        )
        return agg

    def metric_cardinality(
            self,
            *aggregation_name: Optional[str],
            field: str,
            precision_threshold: int = 3000,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-cardinality-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param precision_threshold: int

        :param missing: Optional[Any]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("cardinality", )),
            field=field,
            precision_threshold=precision_threshold,
            missing=missing,
            script=script,
        )
        return agg

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

        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: Optional[str]
            If no field is specified it will default to the 'timestamp_field' of the
            Search class.

        :param calendar_interval: Optional[str]
            Calendar-aware intervals are configured with the calendar_interval
            parameter. You can specify calendar intervals using the unit name, such
            as month, or as a single unit quantity, such as 1M. For example, day and
            1d are equivalent. Multiple quantities, such as 2d, are not supported.

        :param fixed_interval: Optional[str]
            In contrast to calendar-aware intervals, fixed intervals are a fixed
            number of SI units and never deviate, regardless of where they fall on
            the calendar. One second is always composed of 1000ms. This allows fixed
            intervals to be specified in any multiple of the supported units.

            However, it means fixed intervals cannot express other units such as
            months, since the duration of a month is not a fixed quantity.
            Attempting to specify a calendar interval like month or quarter will
            throw an exception.

        :param min_doc_count: int
            Minimum documents to required for a bucket. Set to 0 to allow creating
            empty buckets.

        :param offset: Optional[str]
            Use the offset parameter to change the start value of each bucket by the
            specified positive (+) or negative offset (-) duration, such as 1h for
            an hour, or 1d for a day. See Time units for more possible time duration
            options.

            For example, when using an interval of day, each bucket runs from
            midnight to midnight. Setting the offset parameter to +6h changes each
            bucket to run from 6am to 6am

        :param time_zone: Optional[str]
            Elasticsearch stores date-times in Coordinated Universal Time (UTC). By
            default, all bucketing and rounding is also done in UTC. Use the
            time_zone parameter to indicate that bucketing should use a different
            time zone.

            For example, if the interval is a calendar day and the time zone is
            America/New_York then 2020-01-03T01:00:01Z is : # Converted to
            2020-01-02T18:00:01 # Rounded down to 2020-01-02T00:00:00 # Then
            converted back to UTC to produce 2020-01-02T05:00:00:00Z # Finally, when
            the bucket is turned into a string key it is printed in America/New_York
            so it’ll display as "2020-01-02T00:00:00"

            It looks like: bucket_key = localToUtc(Math.floor(utcToLocal(value) /
            interval) * interval))

            You can specify time zones as an ISO 8601 UTC offset (e.g. +01:00 or
            -08:00) or as an IANA time zone ID, such as America/Los_Angeles.

        :param format: Optional[str]
            Specifies the format of the 'key_as_string' response.
            See:
            https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html

        :param keyed: bool
            Setting the keyed flag to true associates a unique string key with each
            bucket and returns the ranges as a hash rather than an array.

        :param missing: Optional[Any]
            The missing parameter defines how documents that are missing a value
            should be treated. By default they will be ignored but it is also
            possible to treat them as if they had a value.

        :param script: Optional[dict]
            Generating the terms using a script

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.agg(
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
        return agg

    def pipeline_derivative(
            self,
            *aggregation_name: Optional[str],
            buckets_path: str,
            gap_policy: str = 'skip',
            format: Optional[str] = None,
            units: Optional[str] = None,
    ):
        """
        A parent pipeline aggregation which calculates the derivative of a specified
        metric in a parent histogram (or date_histogram) aggregation. The specified
        metric must be numeric and the enclosing histogram must have min_doc_count
        set to 0 (default for histogram aggregations).

        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-derivative-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param buckets_path: str
            The path to the buckets we wish to find the average for.

            https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#buckets-path-syntax

        :param gap_policy: str
            The policy to apply when gaps are found in the data.

            https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html#gap-policy

        :param format: Optional[str]
            Format to apply to the output value of this aggregation

        :param units: Optional[str]
            The derivative aggregation allows the units of the derivative values to
            be specified. This returns an extra field in the response
            normalized_value which reports the derivative value in the desired
            x-axis units.

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.pipeline(
            *(aggregation_name + ("derivative", )),
            buckets_path=buckets_path,
            gap_policy=gap_policy,
            format=format,
            units=units,
        )
        return agg

    def metric_extended_stats(
            self,
            *aggregation_name: Optional[str],
            field: str,
            sigma: float = 3.0,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-extendedstats-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param sigma: float

        :param missing: Optional[Any]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("extended_stats", )),
            field=field,
            sigma=sigma,
            missing=missing,
            script=script,
        )
        return agg

    def agg_filter(
            self,
            *aggregation_name: Optional[str],
            filter: 'QueryInterface',
    ):
        """
        Defines a single bucket of all the documents in the current document set
        context that match a specified filter. Often this will be used to narrow
        down the current aggregation context to a specific set of documents.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filter-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param filter: 'QueryInterface'

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.agg(
            *(aggregation_name + ("filter", )),
            filter=filter,
        )
        return agg

    def agg_filters(
            self,
            *aggregation_name: Optional[str],
            filters: Mapping[str, 'QueryInterface'],
    ):
        """
        Defines a multi bucket aggregation where each bucket is associated with a
        filter. Each bucket will collect all documents that match its associated
        filter.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filters-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param filters: Mapping[str, 'QueryInterface']

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.agg(
            *(aggregation_name + ("filters", )),
            filters=filters,
        )
        return agg

    def metric_geo_bounds(
            self,
            *aggregation_name: Optional[str],
            field: str,
            wrap_longitude: bool = True,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geobounds-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param wrap_longitude: bool

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("geo_bounds", )),
            field=field,
            wrap_longitude=wrap_longitude,
        )
        return agg

    def metric_geo_centroid(
            self,
            *aggregation_name: Optional[str],
            field: str,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geocentroid-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("geo_centroid", )),
            field=field,
        )
        return agg

    def metric_matrix_stats(
            self,
            *aggregation_name: Optional[str],
            fields: list,
            mode: str = 'avg',
            missing: Optional[Any] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-matrix-stats-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param fields: list

        :param mode: str

        :param missing: Optional[Any]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("matrix_stats", )),
            fields=fields,
            mode=mode,
            missing=missing,
        )
        return agg

    def metric_max(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-max-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param missing: Optional[Any]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("max", )),
            field=field,
            missing=missing,
            script=script,
        )
        return agg

    def metric_median_absolute_deviation(
            self,
            *aggregation_name: Optional[str],
            field: str,
            compression: int = 1000,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-median-absolute-deviation-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param compression: int

        :param missing: Optional[Any]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("median_absolute_deviation", )),
            field=field,
            compression=compression,
            missing=missing,
            script=script,
        )
        return agg

    def metric_min(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-min-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param missing: Optional[Any]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("min", )),
            field=field,
            missing=missing,
            script=script,
        )
        return agg

    def metric_percentile_ranks(
            self,
            *aggregation_name: Optional[str],
            field: str,
            values: list,
            keyed: bool = True,
            hdr__number_of_significant_value_digits: Optional[int] = None,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-rank-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param values: list

        :param keyed: bool

        :param hdr__number_of_significant_value_digits: Optional[int]

        :param missing: Optional[Any]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("percentile_ranks", )),
            field=field,
            values=values,
            keyed=keyed,
            hdr__number_of_significant_value_digits=hdr__number_of_significant_value_digits,
            missing=missing,
            script=script,
        )
        return agg

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
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param percents: list

        :param keyed: bool

        :param tdigest__compression: int

        :param hdr__number_of_significant_value_digits: Optional[int]

        :param missing: Optional[Any]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("percentiles", )),
            field=field,
            percents=percents,
            keyed=keyed,
            tdigest__compression=tdigest__compression,
            hdr__number_of_significant_value_digits=hdr__number_of_significant_value_digits,
            missing=missing,
            script=script,
        )
        return agg

    def metric_rate(
            self,
            *aggregation_name: Optional[str],
            unit: str,
            field: Optional[str] = None,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-rate-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param unit: str

        :param field: Optional[str]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("rate", )),
            unit=unit,
            field=field,
            script=script,
        )
        return agg

    def metric_scripted_metric(
            self,
            *aggregation_name: Optional[str],
            map_script: str,
            combine_script: str,
            reduce_script: str,
            init_script: Optional[str] = None,
            params: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-scripted-metric-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param map_script: str

        :param combine_script: str

        :param reduce_script: str

        :param init_script: Optional[str]

        :param params: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("scripted_metric", )),
            map_script=map_script,
            combine_script=combine_script,
            reduce_script=reduce_script,
            init_script=init_script,
            params=params,
        )
        return agg

    def metric_stats(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-stats-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param missing: Optional[Any]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("stats", )),
            field=field,
            missing=missing,
        )
        return agg

    def metric_string_stats(
            self,
            *aggregation_name: Optional[str],
            field: str,
            show_distribution: bool = False,
            missing: Optional[Any] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-string-stats-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param show_distribution: bool

        :param missing: Optional[Any]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("string_stats", )),
            field=field,
            show_distribution=show_distribution,
            missing=missing,
        )
        return agg

    def metric_sum(
            self,
            *aggregation_name: Optional[str],
            field: str,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-sum-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param missing: Optional[Any]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("sum", )),
            field=field,
            missing=missing,
            script=script,
        )
        return agg

    def metric_t_test(
            self,
            *aggregation_name: Optional[str],
            a__field: str,
            b__field: str,
            type: str,
            a__filter: Optional[dict] = None,
            b__filter: Optional[dict] = None,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-ttest-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param a__field: str

        :param b__field: str

        :param type: str

        :param a__filter: Optional[dict]

        :param b__filter: Optional[dict]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("t_test", )),
            a__field=a__field,
            b__field=b__field,
            type=type,
            a__filter=a__filter,
            b__filter=b__filter,
            script=script,
        )
        return agg

    def agg_terms(
            self,
            *aggregation_name: Optional[str],
            field: str,
            size: int = 10,
            shard_size: Optional[int] = None,
            show_term_doc_count_error: Optional[bool] = None,
            order: Optional[dict] = None,
            min_doc_count: int = 1,
            shard_min_doc_count: Optional[int] = None,
            missing: Optional[Any] = None,
            script: Optional[dict] = None,
    ):
        """
        A multi-bucket value source based aggregation where buckets are dynamically
        built - one per unique value.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param size: int
            The size parameter can be set to define how many term buckets should be
            returned out of the overall terms list. By default, the node
            coordinating the search process will request each shard to provide its
            own top size term buckets and once all shards respond, it will reduce
            the results to the final list that will then be returned to the client.
            This means that if the number of unique terms is greater than size, the
            returned list is slightly off and not accurate (it could be that the
            term counts are slightly off and it could even be that a term that
            should have been in the top size buckets was not returned).

        :param shard_size: Optional[int]
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

        :param show_term_doc_count_error: Optional[bool]
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

        :param order: Optional[dict]
            The order of the buckets can be customized by setting the order
            parameter. By default, the buckets are ordered by their doc_count
            descending.

            Warning: Sorting by ascending _count or by sub aggregation is
            discouraged as it increases the error on document counts. It is fine
            when a single shard is queried, or when the field that is being
            aggregated was used as a routing key at index time: in these cases
            results will be accurate since shards have disjoint values. However
            otherwise, errors are unbounded. One particular case that could still be
            useful is sorting by min or max aggregation: counts will not be accurate
            but at least the top buckets will be correctly picked.

        :param min_doc_count: int
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

        :param shard_min_doc_count: Optional[int]
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

            Note: Setting min_doc_count=0 will also return buckets for terms that
            didn’t match any hit. However, some of the returned terms which have a
            document count of zero might only belong to deleted documents or
            documents from other types, so there is no warranty that a match_all
            query would find a positive document count for those terms.

            Warning: When NOT sorting on doc_count descending, high values of
            min_doc_count may return a number of buckets which is less than size
            because not enough data was gathered from the shards. Missing buckets
            can be back by increasing shard_size. Setting shard_min_doc_count too
            high will cause terms to be filtered out on a shard level. This value
            should be set much lower than min_doc_count/#shards.

        :param missing: Optional[Any]
            The missing parameter defines how documents that are missing a value
            should be treated. By default they will be ignored but it is also
            possible to treat them as if they had a value.

        :param script: Optional[dict]
            Generating the terms using a script

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.agg(
            *(aggregation_name + ("terms", )),
            field=field,
            size=size,
            shard_size=shard_size,
            show_term_doc_count_error=show_term_doc_count_error,
            order=order,
            min_doc_count=min_doc_count,
            shard_min_doc_count=shard_min_doc_count,
            missing=missing,
            script=script,
        )
        return agg

    def metric_top_hits(
            self,
            *aggregation_name: Optional[str],
            size: int,
            sort: Optional[dict] = None,
            _source: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-top-hits-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param size: int

        :param sort: Optional[dict]

        :param _source: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("top_hits", )),
            size=size,
            sort=sort,
            _source=_source,
        )
        return agg

    def metric_top_metrics(
            self,
            *aggregation_name: Optional[str],
            metrics: dict,
            sort: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-top-metrics.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param metrics: dict

        :param sort: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("top_metrics", )),
            metrics=metrics,
            sort=sort,
        )
        return agg

    def metric_value_count(
            self,
            *aggregation_name: Optional[str],
            field: str,
            script: Optional[dict] = None,
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-valuecount-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param field: str

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("value_count", )),
            field=field,
            script=script,
        )
        return agg

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
    ):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-weight-avg-aggregation.html

        :param aggregation_name: Optional[str]
            Optional name of the aggregation. Otherwise it will be auto-generated.

        :param value__field: str

        :param weight__field: str

        :param value__missing: Optional[Any]

        :param weight__missing: Optional[Any]

        :param format: Optional[str]

        :param value_type: Optional[str]

        :param script: Optional[dict]

        :returns: 'AggregationInterface'
            A new instance is created and attached to the parent, the new instance
            is returned.
        """
        agg = self.metric(
            *(aggregation_name + ("weighted_avg", )),
            value__field=value__field,
            weight__field=weight__field,
            value__missing=value__missing,
            weight__missing=weight__missing,
            format=format,
            value_type=value_type,
            script=script,
        )
        return agg
