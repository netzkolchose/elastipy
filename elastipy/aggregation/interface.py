

class AggregationInterfaceBase:
    """
    Interface to create aggregations.
    Used either on Search or Aggregations themselves.
    """
    def __init__(self, timestamp_field="timestamp"):
        self.timestamp_field = timestamp_field

    def aggregation(self, *aggregation_name_type, **params):
        """
        Creates an aggregation.

        Either call
            aggregation("sum", field=...) to create an automatic name
        or call
            aggregation("my_name", "sum", field=...) to set aggregation name explicitly

        :param aggregation_name_type: one or two strings, meaning either "type" or "name", "type"
        :param params: all parameters of the aggregation function
        :return: Aggregation instance
        """
        raise NotImplementedError

    def agg(self, *aggregation_name_type, **params):
        """
        Alias for aggregation()
        """
        from .aggregation import Aggregation
        a: Aggregation = self.aggregation(*aggregation_name_type, **params)
        return a

    def metric(self, *aggregation_name_type, **params):
        """
        Alias for aggregation()
        """
        from .aggregation import Aggregation
        return_self = params.pop("return_self", None)
        a: Aggregation = self.aggregation(*aggregation_name_type, **params)
        if not return_self:
            return self
        return a

    def pipeline(self, *aggregation_name_type, **params):
        """
        Alias for aggregation()
        """
        from .aggregation import Aggregation
        return_self = params.pop("return_self", None)
        a: Aggregation = self.aggregation(*aggregation_name_type, **params)
        if not return_self:
            return self
        return a
