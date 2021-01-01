

class AggregationInterfaceBase:
    """
    Interface to create aggregations.
    Used either on Search or Aggregations themselves.
    """
    def __init__(self, timestamp_field="timestamp"):
        self.timestamp_field = timestamp_field

    def aggregation(self, *aggregation_name_type, **params) -> 'AggregationInterfaceBase':
        """
        Creates an aggregation.

        Either call
            aggregation("sum", field=...) to create an automatic name
        or call
            aggregation("my_name", "sum", field=...) to set aggregation name explicitly

        :param aggregation_name_type: one or two strings
        :param params: all parameters of the aggregation function
        :return: Aggregation instance
        """
        raise NotImplementedError

    def agg(self, *aggregation_name_type, **params):
        """
        Alias for aggregation()
        """
        return self.aggregation(*aggregation_name_type, **params)

    def metric(self, *aggregation_name_type, **params):
        """
        Alias for aggregation()
        """
        # aggregation_type = aggregation_name_type[0] if len(aggregation_name_type) == 1 else aggregation_name_type[1]
        # assert aggregation_type in DEFINITION["metric"], f"'{aggregation_type}' is not a supported metric"
        return self.aggregation(*aggregation_name_type, **params)

    """
    def agg_terms(self, *aggregation_name, field, size=10, shard_size=None, order=None, min_doc_count=1, show_term_doc_count_error=False):
        return self.aggregation(
            *(aggregation_name + ("terms", )),
            field=field, size=size, min_doc_count=min_doc_count,
            show_term_doc_count_error=show_term_doc_count_error,
            _if_not_none=dict(shard_size=shard_size, order=order)
        )

    def agg_date_histogram(self, *aggregation_name, interval="1y", field=None, min_doc_count=0):
        return self.aggregation(
            *(aggregation_name + ("date_histogram", )),
            calendar_interval=interval,
            field=field or self.timestamp_field,
            min_doc_count=min_doc_count,
        )

    def metric_avg(self, *aggregation_name, field, missing=None, script=None):
        return self.metric(
            *(aggregation_name + ("avg", )),
            field=field, _if_not_none=dict(missing=missing, script=script)
        )

    def metric_cardinality(self, *aggregation_name, field, precision_threshold=3000, missing=None, script=None):
        return self.metric(
            *(aggregation_name + ("cardinality", )),
            field=field, precision_threshold=precision_threshold,
            _if_not_none=dict(missing=missing, script=script),
        )
    """
