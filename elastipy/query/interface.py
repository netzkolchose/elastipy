

class QueryInterfaceBase:

    def add_query(self, name, **params) -> 'QueryInterface':
        raise NotImplementedError(
            f"{self.__class__.__name__}.add_query() not implemented"
        )

    def new_query(self, name, **params) -> 'QueryInterface':
        raise NotImplementedError(
            f"{self.__class__.__name__}.new_query() not implemented"
        )

    def __and__(self, other):
        return self.new_query("bool", must=[self, other])

    def __or__(self, other):
        return self.new_query("bool", should=[self, other])

    def __invert__(self):
        return self.new_query("bool", must_not=[self])
