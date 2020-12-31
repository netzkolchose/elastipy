from copy import copy, deepcopy
from typing import List

from .query import Query, QueryInterface, factory


class Bool(Query):

    name = "bool"
    _optional_parameters = {
        "must": None,
        "must_not": None,
        "should": None,
        "filter": None,
    }

    def __init__(
            self,
            must: List[QueryInterface]=None,
            must_not: List[QueryInterface]=None,
            should: List[QueryInterface]=None,
            filter: List[QueryInterface]=None,
    ):
        """
        A query that matches documents matching boolean combinations of other
        queries. The bool query maps to Lucene BooleanQuery. It is built using
        one or more boolean clauses, each clause with a typed occurrence.

        The bool query takes a more-matches-is-better approach, so the score
        from each matching must or should clause will be added together to
        provide the final _score for each document.

        See: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html
        :param must: QueryInterface
            The clause (query) must appear in matching documents and will
            contribute to the score.

        :param must_not: QueryInterface
            The clause (query) must not appear in the matching documents.
            Clauses are executed in filter context meaning that scoring is
            ignored and clauses are considered for caching. Because scoring is
            ignored, a score of 0 for all documents is returned.

        :param should: QueryInterface
            The clause (query) should appear in the matching document.

        :param filter: QueryInterface
            The clause (query) must appear in matching documents. However unlike
            must the score of the query will be ignored. Filter clauses are
            executed in filter context, meaning that scoring is ignored and
            clauses are considered for caching.
        """
        super().__init__(
            must=must,
            must_not=must_not,
            should=should,
            filter=filter,
        )

    @property
    def must(self):
        return self._get_bool_param("must")

    @must.setter
    def must(self, value):
        self._set_bool_param("must", value)

    @property
    def must_not(self):
        return self._get_bool_param("must_not")

    @must_not.setter
    def must_not(self, value):
        self._set_bool_param("must_not", value)

    @property
    def should(self):
        return self._get_bool_param("should")

    @should.setter
    def should(self, value):
        self._set_bool_param("should", value)

    @property
    def filter(self):
        return self._get_bool_param("filter")

    @filter.setter
    def filter(self, value):
        self._set_bool_param("filter", value)

    def _get_bool_param(self, name):
        return self._optional_parameters.get(name) or self.parameters.get(name) or []

    def _set_bool_param(self, name, value):
        if name in self.parameters:
            self.parameters[name] = value
        else:
            self._optional_parameters[name] = value

    def add_query(self, name, **params) -> 'Bool':
        return self & factory(name, **params)

    def __and__(self, other) -> 'Bool':
        self_ = self
        if not isinstance(self_, Bool):
            self_, other = other, self_

        if not isinstance(other, Bool):
            q = copy(self_)
            q.must += [other]
            return q

        else:
            q = copy(self_)
            for key in ("must", "must_not", "should", "filter"):
                for o in getattr(other, key):
                    if o not in getattr(self_, key):
                        setattr(q, key, getattr(q, key) + [o])
            return q

    def __or__(self, other):
        self_ = self
        if not isinstance(self_, Bool):
            self_, other = other, self_

        if not isinstance(other, Bool):
            q = copy(self)
            if q.should:
                if not q.must and not q.must_not and not q.filter:
                    q.should += [other]
                    return q

        return super().__or__(other)
