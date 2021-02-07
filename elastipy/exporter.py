import time
import sys
from typing import Iterable, Any, Mapping, Union, Iterator, Sequence

from elasticsearch import ElasticsearchException, NotFoundError
from elasticsearch.helpers import streaming_bulk, bulk

from . import connections
from .search import Search


class Exporter:
    """
    Base class helper to export stuff to elasticsearch.

    Derive from class and define class attributes:

        - ``INDEX_NAME``: ``str``
          Name of index, might contain a wildcard `*`

        - ``MAPPINGS``: ``dict``
          The `mapping <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html>`__
          definition for the index.

    And optionally override methods:

        - :meth:`.transform_document`
          Convert a document to elasticsearch.

        - :meth:`.get_document_id`
          Return a unique id for the elasticsearch document.

        - :meth:`.get_document_index`
          Return an alternative index name for the document.
    """

    # Name of the elasticsearch index where things are exported
    INDEX_NAME: str = None

    # dict with mapping parameters
    MAPPINGS: dict = None

    def __init__(
            self,
            client=None,
            index_prefix: str = None,
            index_postfix: str = None,
            update_index: bool = True,
    ):
        """
        Create a new instance of the exporter.

        :param client:
            An optional instance of an elasticsearch.Elasticsearch compatible object
            If omitted elastipy.connections.get("default") will be used

        :param index_prefix: ``str``
            Optional string that is put before the class-attribute ``INDEX_NAME``

        :param index_postfix: ``str``
            Optional string that is put after the class-attribute ``INDEX_NAME``

        :param update_index: ``bool``
            If ``True``, the elasticsearch index will be created or updated with
            the current ``MAPPINGS`` before the first export of a document.
        """
        for required_attribute in ("INDEX_NAME", "MAPPINGS"):
            if not getattr(self, required_attribute, None):
                raise ValueError(f"Need to define class attribute {self.__class__.__name__}.{required_attribute}")
        self._client = client
        self.index_prefix = index_prefix
        self.index_postfix = index_postfix
        self._do_update_index = update_index
        self._index_updated = dict()

    @property
    def client(self):
        """
        Access to the elasticsearch client.
        If none was defined in constructor
        then ``elastipy.connections.get("default")`` is returned.
        """
        if self._client is None:
            self._client = connections.get()
        return self._client

    def index_name(self) -> str:
        """
        Returns the configured ``index_prefix - INDEX_NAME - index_suffix``

        :return: str
        """
        name = self.INDEX_NAME
        if self.index_prefix:
            name = f"{self.index_prefix}-{name}"
        if self.index_postfix:
            name = f"{name}-{self.index_postfix}"
        return name

    def search(self, **kwargs) -> Search:
        """
        Return a new ``Search`` object for this index and client.

        :return: Search instance
        """
        from .search import Search
        return Search(index=self.index_name(), client=self._client, **kwargs)

    def get_document_id(self, es_data: Mapping):
        """
        Override this to return a single elasticsearch object's id.

        :param es_data: ``dict``
            Single object as returned by transform_document()

        :return: str, int etc..
        """
        return None

    def get_document_index(self, es_data: Mapping) -> str:
        """
        Override to define an index per document.

        The default function returns the result from ``index_name()``
        but it's possible to put objects into separate indices.

        For example you might define ``INDEX_NAME = "documents-*"``

        and ``get_document_index`` might return

        .. CODE::

            self.index_name().replace("*", es_data["type"]

        :param es_data: ``dict``
            Single document as returned by transform_document()

        :return: str
        """
        return self.index_name()

    def transform_document(self, data: Mapping) -> Union[Mapping, Iterator[Mapping]]:
        """
        Override this to transform each documents's data into
        an elasticsearch document.

        It's possible to return a **list** or **yield** multiple
        elasticsearch documents.
        
        :param data: dict 
        :return: dict or iterable of dict
        """
        return data

    def update_index(self) -> None:
        """
        Create the index or update changes to the mapping.

        Can only be called if ``INDEX_NAME`` does not contain a ``'*'``
        :return: None
        """
        if "*" in self.index_name():
            raise ValueError(f"update_index() can not be called for wildcard indices like '{self.index_name()}'")
        self._update_index(self.index_name())

    def delete_index(self) -> bool:
        """
        Try to delete the index. Ignore if not found.

        :return: ``bool``
            True if deleted, False otherwise.

            If the index name contains a wildcard ``*``,
            True is always returned.
        """
        from .aggregation.helper import wildcard_match

        name = self.index_name()
        try:
            self.client.indices.delete(index=name)
            self._index_updated.pop(self.index_name(), None)
            if "*" in name:
                for key in list(self._index_updated):
                    if wildcard_match(key, name):
                        self._index_updated.pop(key)
            return True
        except NotFoundError:
            return False

    def export_list(
            self,
            object_list: Iterable[Any],
            chunk_size: int = 500,
            refresh: bool = False,
            verbose: bool = False,
            count: int = None,
            file=None,
            **kwargs
    ):
        """
        Export a list of objects.

        :param object_list: ``sequence of dict``
            This can be a list or generator of dictionaries, containing the
            objects that should be exported.

        :param chunk_size: ``int``
            Number of objects per bulk request.

        :param refresh: ``bool``
            if ``True`` require the immediate refresh of the index
            when finished exporting.

        :param verbose: ``bool``
            If True print some progress to stderr
            (using `tqdm <https://pypi.org/project/tqdm/>`__ if present)

        :param count: ``int``
            Provide the number of objects for the **verbosity** if
            ``object_list`` is a generator.

        :param file:
            Optional string stream to output verbose info, default is ``stderr``.

        All other parameters are passed to
        `elasticsearch.helpers.bulk <https://elasticsearch-py.readthedocs.io/en/v7.10.1/helpers.html#elasticsearch.helpers.bulk>`__

        :return: ``dict``
            Response of elasticsearch bulk call.
        """
        def bulk_actions():
            for object_data in self._verbose_iter(object_list, verbose, count, file):

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

        response = bulk(
            client=self.client,
            actions=bulk_actions(),
            chunk_size=chunk_size,
            refresh=refresh,
            **kwargs,
        )
        if verbose:
            # TODO: print error status
            print(f"{self.__class__.__name__}: exported {response[0]} objects", file=file)

        return response

    def get_index_params(self) -> dict:
        """
        Returns the complete index parameters.

        Override if you need to specialize things.

        :return: dict
        """
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

    @classmethod
    def _verbose_iter(cls, iter, verbose: bool, count=None, file=None):
        if not verbose:
            yield from iter
            return

        if file is None:
            file = sys.stderr

        # this is just a unittest switch
        if verbose != "simple":
            try:
                import tqdm
                yield from tqdm.tqdm(iter, total=count, file=file)
                return
            except ImportError:
                pass

        if count is None:
            try:
                count = len(iter)
            except (TypeError, ):
                pass

        last_time = None
        for i, item in enumerate(iter):
            ti = time.time()
            if last_time is None or ti - last_time >= 1.:
                last_time = ti
                if count:
                    print(f"{cls.__name__} {i}/{count}", file=file)
                else:
                    print(f"{cls.__name__} {i}", file=file)
            yield item
