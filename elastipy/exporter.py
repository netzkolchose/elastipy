import datetime
import os
import json
from typing import Iterable, Any, Mapping, Union, Iterator, Sequence

from elasticsearch import ElasticsearchException, NotFoundError
from elasticsearch.helpers import streaming_bulk, bulk

from . import connections
from .search import Search


class Exporter:
    """
    Base class helper to export stuff to elasticsearch.

    Derive from class and define class attributes:

        INDEX_NAME: str, name of index
            It can contain a wildcard *
        MAPPINGS: dict, the mapping definition for the index

    And optionally override:
        transform_document()
        get_document_id()
        get_document_index()
    """

    INDEX_NAME: str = None
    MAPPINGS: Mapping = None

    def __init__(self, client=None, index_prefix: str = None, index_postfix: str = None):
        for required_attribute in ("INDEX_NAME", "MAPPINGS"):
            if not getattr(self, required_attribute, None):
                raise ValueError(f"Need to define class attribute {self.__class__.__name__}.{required_attribute}")
        self._client = client
        self.index_prefix = index_prefix
        self.index_postfix = index_postfix
        self._index_updated = dict()

    @property
    def client(self):
        if self._client is None:
            self._client = connections.get()
        return self._client

    def index_name(self) -> str:
        name = self.INDEX_NAME
        if self.index_prefix:
            name = f"{self.index_prefix}-{name}"
        if self.index_postfix:
            name = f"{name}-{self.index_postfix}"
        return name

    def search(self, **kwargs) -> Search:
        """
        return a new Search object for this index and client
        :return: Search instance
        """
        from .search import Search
        return Search(index=self.index_name(), client=self._client, **kwargs)

    def get_document_id(self, es_data: Mapping):
        """
        Override this to return a single elasticsearch object's id
        :param es_data: dict, single object as returned by transform_document()
        :return: str, int etc..
        """
        return None

    def get_document_index(self, es_data: Mapping) -> str:
        """
        Override to define an index per document.

        The default function returns the result from index_name() but it's possible
        to put objects into separate indices.

        For example you might define
            INDEX_NAME = "documents-*"
        and get_document_index() might return
            self.index_name() + es_data["type"]

        :param es_data: dict, single document as returned by transform_document()
        :return: str
        """
        return self.index_name()

    def transform_document(self, data: Mapping) -> Union[Mapping, Iterator[Mapping]]:
        """
        Override this to transform each documents's data into an elasticsearch document

        It's possible to return a list or yield multiple elasticsearch documents.
        
        :param data: dict 
        :return: dict or iterable of dict
        """
        return data

    def update_index(self) -> None:
        """
        Create the index or update changes to the mapping.

        Can only be called if INDEX_NAME does not contain a '*'
        :return: None
        """
        if "*" in self.index_name():
            raise ValueError(f"update_index() can not be called for wildcard indices like '{self.index_name()}'")
        self._update_index(self.index_name())

    def delete_index(self) -> bool:
        """
        Try to delete the index. Ignore if not found.

        :return: bool, True if delete, False otherwise
        """
        try:
            self.client.indices.delete(index=self.index_name())
            self._index_updated.pop(self.index_name(), None)
            return True
        except NotFoundError:
            return False

    def export_list(
            self,
            object_list: Iterable[Any],
            chunk_size: int = 500,
            refresh: bool = False,
            verbose: bool = False,
            **kwargs
    ):
        """
        Export a list of objects
        :param object_list: list of dict
        :param chunk_size: int, number of objects per bulk request
        :return: dict, response of elasticsearch bulk call
        """
        verbose_iter = lambda x: x
        if verbose:
            try:
                import tqdm
                verbose_iter = tqdm.tqdm
            except ImportError:
                pass

        def bulk_actions():
            for object_data in verbose_iter(object_list):

                es_data_iter = self.transform_document(object_data)
                if isinstance(es_data_iter, Mapping):
                    es_data_iter = [es_data_iter]

                for es_data in es_data_iter:
                    object_id = self.get_document_id(es_data)
                    index_name = self.get_document_index(es_data)

                    if index_name not in self._index_updated:
                        self._update_index(index_name)

                    action = {
                        "_index": self.get_document_index(es_data),
                        "_source": es_data,
                    }
                    if object_id is not None:
                        action["_id"] = object_id

                    yield action

        bulk(
            client=self.client,
            actions=bulk_actions(),
            chunk_size=chunk_size,
            refresh=refresh,
            **kwargs,
        )

    def get_index_params(self) -> dict:
        return {
            "mappings": self.MAPPINGS
        }

    def _update_index(self, name):
        try:
            self.client.indices.get_mapping(index=name)
            self.client.indices.put_mapping(index=name, body=self.MAPPINGS)
            self._index_updated[name] = True
            return
        except NotFoundError:
            pass

        self.client.indices.create(index=name, body=self.get_index_params())
