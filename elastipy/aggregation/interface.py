

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

    def pipeline(self, *aggregation_name_type, **params):
        """
        Alias for aggregation()
        """
        return self.aggregation(*aggregation_name_type, **params)
