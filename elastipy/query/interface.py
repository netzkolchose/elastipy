

class QueryInterfaceBase:

    def add_query(self, name, **params) -> 'QueryInterface':
        raise NotImplementedError(
            f"{self.__class__.__name__}.add_query() not implemented"
        )

    def query_factory(self, name, **params) -> 'QueryInterface':
        raise NotImplementedError(
            f"{self.__class__.__name__}.query_factory() not implemented"
        )

    def __and__(self, other):
        return self.query_factory("bool", must=[self, other])

    def __or__(self, other):
        return self.query_factory("bool", should=[self, other])

    def __invert__(self):
        return self.query_factory("bool", must_not=[self])
