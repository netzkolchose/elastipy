from .query import Query


class EmptyQuery(Query):

    name = "_empty_query"

    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {
            "match_all": {}
        }

    def add_query(self, name, **params) -> 'Query':
        return self.query_factory(name, **params)
