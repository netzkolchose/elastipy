import datetime
import os
import json
from typing import Iterable, Any, Mapping

from elasticsearch import ElasticsearchException, NotFoundError
from elasticsearch.helpers import streaming_bulk, bulk

from .client import get_elastic_client
from .search import Search


class Exporter:
    """
    Base class helper to export stuff to elasticsearch.

    Derive from class and define class attributes:
        INDEX_NAME: str, name of index
        MAPPINGS: dict, the mapping definition for the index

    And override:
        get_object_id()
        and optionally transform_object_data()

    """

    INDEX_NAME = None
    MAPPINGS = None

    def __init__(self, client=None, index_suffix=None):
        for required_attribute in ("INDEX_NAME", "MAPPINGS"):
            if not getattr(self, required_attribute, None):
                raise ValueError(f"Need to define class attribute {self.__class__.__name__}.{required_attribute}")
        self._client = client
        self.index_suffix = index_suffix

    @property
    def client(self):
        if self._client is None:
            self._client = get_elastic_client()
        return self._client

    def index_name(self):
        name = self.INDEX_NAME
        if self.index_suffix:
            name = f"{name}-{self.index_suffix}"
        return name

    def search(self, **kwargs) -> Search:
        """
        return a new Search object for this index and client
        :return: Search instance
        """
        from .search import Search
        return Search(index=self.index_name(), client=self._client, **kwargs)

    def get_document_id(self, es_data):
        """
        Override this to return a single elasticsearch object's id
        :param es_data: dict, single object as returned by transform_object_data()
        :return: str, int etc..
        """
        return None

    def transform_document(self, data):
        """
        Override this to transform each object's data for elasticsearch
        Return a list of you want to split data into multiple elasticsearch documents
        
        :param data: dict 
        :return: dict or list of dict
        """
        return data

    def update_index(self):
        """
        Create the index or update changes to the mapping
        :return:
        """
        try:
            self.client.indices.get_mapping(index=self.index_name())
            self.client.indices.put_mapping(index=self.index_name(), body=self.MAPPINGS)
            return
        except NotFoundError:
            pass

        self.client.indices.create(index=self.index_name(), body=self.get_index_params())

    def delete_index(self):
        try:
            self.client.indices.delete(index=self.index_name())
            return True
        except NotFoundError:
            return False

    def export_list(self, object_list: Iterable[Any], chunk_size=500, refresh=False, verbose=False, **kwargs):
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

                    action = {
                        "_index": self.index_name(),
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

    def get_index_params(self):
        return {
            "mappings": self.MAPPINGS
        }
