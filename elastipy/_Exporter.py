import datetime
import os
import json

from elasticsearch import ElasticsearchException, NotFoundError
from elasticsearch.helpers import bulk

from ._client import get_elastic_client


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
        self.client = client if client is not None else get_elastic_client()
        self.index_suffix = index_suffix

    def index_name(self):
        name = self.INDEX_NAME
        if self.index_suffix:
            name = f"{name}-{self.index_suffix}"
        return name

    def get_object_id(self, es_data):
        """
        Override this to return a single elasticsearch object's id
        :param es_data: dict, single object as returned by transform_object_data()
        :return: str, int etc..
        """
        raise NotImplementedError

    def transform_object_data(self, data):
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
        except NotFoundError:
            self.client.indices.create(index=self.index_name(), body=self.get_index_params())

    def delete_index(self):
        try:
            self.client.indices.delete(index=self.index_name())
            return True
        except NotFoundError:
            return False

    def export_list(self, object_list, bulk_size=10000):
        """
        Export a list of objects
        :param object_list: list of dict
        :param bulk_size: int, number of objects per bulk request
        :return: dict, response of elasticsearch bulk call
        """
        bulk_actions = []

        for object_data in object_list:

            es_data_array = self.transform_object_data(object_data)
            if not isinstance(es_data_array, (list, tuple)):
                es_data_array = [es_data_array]

            for es_data in es_data_array:
                object_id = self.get_object_id(es_data)

                if not self.client.exists(index=self.index_name(), id=object_id):
                    bulk_actions.append(
                        {
                            "_index": self.index_name(),
                            "_id": object_id,
                            "_source": es_data,
                        }
                    )
                else:
                    # if the order exists already, some updates will be applied
                    bulk_actions.append(
                        {
                            "_op_type": "update",
                            "_index": self.index_name(),
                            "_id": object_id,
                            "doc": es_data
                        }
                    )

                if len(bulk_actions) >= bulk_size:
                    bulk(self.client, bulk_actions)
                    bulk_actions = []

        if bulk_actions:
            # TODO: only returning last bulk call, if any..
            return bulk(self.client, bulk_actions)

    def get_index_params(self):
        return {
            "mappings": self.MAPPINGS
        }
