from typing import Optional, Union, Mapping

from elasticsearch import VERSION, Elasticsearch
import decouple


__all__ = ("get", "set")


class Connections:
    """
    A mapping between keys (aliases) and elasticsearch connections
    """
    def __init__(self):
        self._parameters = dict()
        self._connections = dict()

    def get_connection(self, alias: str = "default") -> Elasticsearch:
        if alias in self._connections:
            return self._connections[alias]

        if alias in self._parameters:
            self._connections[alias] = self._create_client(self._parameters[alias])
            return self._connections[alias]

        if alias == "default":
            self._parameters[alias] = self._default_parameters()
            return self.get_connection(alias)

        raise KeyError(f"No definition for connection alias '{alias}'")

    def set_connection(self, alias: str, con: Union[Elasticsearch, Mapping]):
        if isinstance(con, Mapping):
            if alias in self._parameters:
                if self._parameters[alias] == con:
                    return
            self._parameters[alias] = con
            self._connections.pop(alias, None)
        else:
            self._connections[alias] = con
            self._parameters.pop(alias, None)

    def _create_client(self, params: Mapping):
        from elasticsearch import Elasticsearch
        return Elasticsearch(**params)

    def _default_parameters(self) -> dict:
        protocol = decouple.config("ELASTIPY_PROTOCOL", default="http")
        host = decouple.config("ELASTIPY_HOST", default="localhost")
        port = decouple.config("ELASTIPY_PORT", default=9200, cast=int)
        user = decouple.config("ELASTIPY_USER", default=None)
        password = decouple.config("ELASTIPY_PASSWORD", default=None)
        timeout = decouple.config("ELASTIPY_TIMEOUT", default=30, cast=int)

        if VERSION[0] < 8:
            params = {
                "hosts": [{"host": host, "port": port}],
                "timeout": timeout,
            }
            if user and password:
                params["http_auth"] = (user, password)

        else:
            params = {
                "hosts": f"{protocol}://{host}:{port}",
                "request_timeout": timeout,
                "verify_certs": decouple.config("ELASTIPY_VERIFY_CERTS", default=True, cast=bool),
                "ssl_show_warn": decouple.config("ELASTIPY_SSL_SHOW_WARN", default=True, cast=bool),
            }
            if user and password:
                params["basic_auth"] = (user, password)


        return params


singleton = Connections()
get = singleton.get_connection
set = singleton.set_connection
