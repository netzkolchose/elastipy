from typing import Optional, Union, Mapping

__all__ = ("get", "set")


DEFAULT_PARAMS = {
    "hosts": [{"host": "localhost", 'port': 9200}],
    "timeout": 30,
}


class Connections:

    def __init__(self):
        self._parameters = dict()
        self._connections = dict()

    def get_connection(self, alias : str = "default"):
        if alias in self._connections:
            return self._connections[alias]

        if alias in self._parameters:
            self._connections[alias] = self._create_client(self._parameters[alias])
            return self._connections[alias]

        if alias == "default":
            self._parameters[alias] = DEFAULT_PARAMS
            return self.get_connection(alias)

        raise KeyError(f"No definition for connection alias '{alias}'")

    def set_connection(self, alias: str, con):
        if isinstance(con, Mapping):
            if alias in self._parameters:
                if self._parameters[alias] == con:
                    return
            self._parameters[alias] = con
            self._connections.pop(alias, None)
        else:
            self._connections[alias] = con
            self._parameters.pop(alias, None)

    def _create_client(self, params):
        from elasticsearch import Elasticsearch
        return Elasticsearch(**params)


singleton = Connections()
get = singleton.get_connection
set = singleton.set_connection
