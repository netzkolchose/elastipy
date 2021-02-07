

class SearchParametersBase:

    """
    Access to this class is through `Search.param`.

    Each method returns a new Search instance.

    ... CODE::

        s = Search()
        s = s.param.explain(True).param.size(100)

    """

    # will be replaced by the yaml-generated class
    DEFINITION = {}

    def __init__(self, search):
        from .search import Search
        self._search: Search = search
        self._params = dict()

    def _set_parameter(self, name: str, value):
        s = self._search.copy()
        s._parameters._params[name] = value
        return s

    def to_body(self) -> dict:
        """
        Convert all parameters to the representation in the search request body
        :return: dict
        """
        return self._to_dict("body")

    def to_query_params(self) -> dict:
        """
        Convert all parameters to the representation as search request query parameters
        :return: dict
        """
        params = self._to_dict("query")
        for key, value in params.items():

            if isinstance(value, bool):
                value = repr(value).lower()

            params[key] = value
        return params

    def _to_dict(self, group) -> dict:
        body = dict()
        for name, value in self._params.items():
            defi = self.DEFINITION.get(name) or {}
            if defi.get("group") != group:
                continue

            if value == defi.get("default"):
                continue

            if name == "sort":
                value = self._adjust_sort_param(value)

            body[name] = value
        return body

    def _adjust_sort_param(self, sort) -> list:
        if not isinstance(sort, (list, tuple)):
            sort = [sort]

        args = []
        for s in sort:
            if isinstance(s, (list, tuple)):
                args += list(s)
            else:
                args.append(s)

        for i, arg in enumerate(args):
            if isinstance(arg, str):
                if arg.startswith("-"):
                    args[i] = {arg.lstrip("-"): "desc"}

        return args
