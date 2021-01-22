# auto-generated file - do not edit
from datetime import date, datetime
from typing import Mapping, Sequence, Any, Union, Optional

from .search_param import SearchParametersBase
from .search import Search


class Unset:
    pass


class SearchParameters(SearchParametersBase):

    # make sure sphinx get's the documentation string
    __doc__ = SearchParametersBase.__doc__

    DEFINITION = {'_source': {'default': True, 'group': 'body'}, '_source_excludes': {'group': 'query'}, '_source_includes': {'group': 'query'}, 'allow_no_indices': {'default': True, 'group': 'query'}, 'allow_partial_search_results': {'default': True, 'group': 'query'}, 'batched_reduce_size': {'default': 512, 'group': 'query'}, 'ccs_minimize_roundtrips': {'default': True, 'group': 'query'}, 'docvalue_fields': {'group': 'body'}, 'expand_wildcards': {'default': 'open', 'group': 'query'}, 'explain': {'default': False, 'group': 'body'}, 'fields': {'group': 'body'}, 'from': {'default': 0, 'group': 'body'}, 'ignore_throttled': {'default': True, 'group': 'query'}, 'ignore_unavailable': {'default': False, 'group': 'query'}, 'indices_boost': {'group': 'body'}, 'max_concurrent_shard_requests': {'default': 5, 'group': 'query'}, 'min_score': {'group': 'body'}, 'pre_filter_shard_size': {'group': 'query'}, 'preference': {'group': 'query'}, 'q': {'group': 'query'}, 'request_cache': {'group': 'query'}, 'rest_total_hits_as_int': {'default': False, 'group': 'query'}, 'routing': {'group': 'query'}, 'scroll': {'group': 'query'}, 'search_type': {'default': 'query_then_fetch', 'group': 'query'}, 'seq_no_primary_term': {'default': False, 'group': 'body'}, 'size': {'default': 10, 'group': 'body'}, 'sort': {'group': 'body'}, 'stats': {'group': 'body'}, 'stored_fields': {'group': 'query'}, 'suggest_field': {'group': 'query'}, 'suggest_text': {'group': 'query'}, 'terminate_after': {'default': 0, 'timeout': {'type': 'str', 'doc': 'Specifies the period of time to wait for a response in\n[time units](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#time-units).\nIf no response is received before the timeout expires,\nthe request fails and returns an error. Defaults to no timeout.\n'}, 'group': 'body'}, 'timeout': {'group': 'query'}, 'track_scores': {'default': False, 'group': 'query'}, 'track_total_hits': {'default': 10000, 'group': 'query'}, 'typed_keys': {'default': True, 'group': 'query'}, 'version': {'default': False, 'group': 'query'}}

    def __call__(
            self,
            source: Union[bool, str, Sequence] = Unset,
            source_excludes: Optional[str] = Unset,
            source_includes: Optional[str] = Unset,
            allow_no_indices: bool = Unset,
            allow_partial_search_results: bool = Unset,
            batched_reduce_size: int = Unset,
            ccs_minimize_roundtrips: bool = Unset,
            docvalue_fields: Optional[Sequence[Union[str, Mapping[str, str]]]] = Unset,
            expand_wildcards: str = Unset,
            explain: bool = Unset,
            fields: Optional[Sequence[Union[str, Mapping[str, str]]]] = Unset,
            from_: int = Unset,
            ignore_throttled: bool = Unset,
            ignore_unavailable: bool = Unset,
            indices_boost: Optional[Sequence[Mapping[str, float]]] = Unset,
            max_concurrent_shard_requests: int = Unset,
            min_score: Optional[float] = Unset,
            pre_filter_shard_size: Optional[int] = Unset,
            preference: Optional[str] = Unset,
            q: Optional[str] = Unset,
            request_cache: Optional[bool] = Unset,
            rest_total_hits_as_int: bool = Unset,
            routing: Optional[str] = Unset,
            scroll: Optional[str] = Unset,
            search_type: str = Unset,
            seq_no_primary_term: bool = Unset,
            size: int = Unset,
            sort: Optional[Union[str, Sequence[Union[str, Mapping[str, str]]], Mapping[str, str]]] = Unset,
            stats: Optional[Sequence[str]] = Unset,
            stored_fields: Optional[str] = Unset,
            suggest_field: Optional[str] = Unset,
            suggest_text: Optional[str] = Unset,
            terminate_after: int = Unset,
            timeout: Optional[str] = Unset,
            track_scores: bool = Unset,
            track_total_hits: Union[int, bool] = Unset,
            typed_keys: bool = Unset,
            version: bool = Unset,
    ) -> Search:
        """
        Can set all search parameters at once.

        Each parameter that is different than it's default value is put into the
        search request.

        The parameters are automatically split into query and body representation.

        :param source: ``Union[bool, str, Sequence]``
            Indicates which `source fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html>`__
            are returned for matching documents. These fields are returned in the
            ``hits._source`` property of the search response. Defaults to ``true``.

            Valid values:

                - ``true`` (Boolean) The entire document source is returned.
                - ``false`` (Boolean) The document source is not returned.
                - ``<wildcard_pattern>`` (string or array of strings) Wildcard
                  (``*``) pattern or array of patterns containing source fields to
                  return.
                - ``<object>`` Object containing a list of source fields to include
                  or exclude. Properties for <object>:

                    - ``excludes`` (string or array of strings) Wildcard (``*``)
                      pattern or array of patterns containing source fields to
                      exclude from the response. You can also use this property to
                      exclude fields from the subset specified in includes property.
                    - ``includes`` (string or array of strings) Wildcard (``*``)
                      pattern or array of patterns containing source fields to
                      return. If this property is specified, only these source
                      fields are returned. You can exclude fields from this subset
                      using the ``excludes`` property.

        :param source_excludes: ``Optional[str]``
            A comma-separated list of `source fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html>`__
            to exclude from the response.

            You can also use this parameter to exclude fields from the subset
            specified in ``_source_includes`` query parameter.

            If the ``_source`` parameter is ``false``, this parameter is ignored.

        :param source_includes: ``Optional[str]``
            A comma-separated list of `source fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html>`__
            to include in the response.

            If this parameter is specified, only these source fields are returned.
            You can exclude fields from this subset using the ``_source_excludes``
            query parameter.

            If the ``_source`` parameter is ``false``, this parameter is ignored.

        :param allow_no_indices: ``bool``
            If false, the request returns an error if any wildcard expression,
            `index alias
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html>`__,
            or _all value targets only missing or closed indices. This behavior
            applies even if the request targets other open indices. For example, a
            request targeting ``foo*,bar*`` returns an error if an index starts with
            ``foo`` but no index starts with ``bar``.

        :param allow_partial_search_results: ``bool``
            If ``true``, returns partial results if there are request timeouts or
            `shard failures
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-replication.html#shard-failures>`__.
            If ``false``, returns an error with no partial results. Defaults to
            ``true``.

            To override the default for this field, set the
            ``search.default_allow_partial_results`` cluster setting to false.

        :param batched_reduce_size: ``int``
            The number of shard results that should be reduced at once on the
            coordinating node. This value should be used as a protection mechanism
            to reduce the memory overhead per search request if the potential number
            of shards in the request can be large. Defaults to ``512``.

        :param ccs_minimize_roundtrips: ``bool``
            If ``true``, network round-trips between the coordinating node and the
            remote clusters are minimized when executing cross-cluster search (CCS)
            requests. See `How cross-cluster search handles network delays
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html#ccs-network-delays>`__.
            Defaults to ``true``.

        :param docvalue_fields: ``Optional[Sequence[Union[str, Mapping[str, str]]]]``
            Array of wildcard (``*``) patterns. The request returns doc values for
            field names matching these patterns in the ``hits.fields`` property of
            the response.

            You can specify items in the array as a string or object. See `Doc value
            fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html#docvalue-fields>`__.

            Properties of ``docvalue_fields`` objects:

                - ``field`` (Required, string) Wildcard pattern. The request returns
                  doc values for field names matching this pattern.
                - ``format`` (Optional, string) Format in which the doc values are
                  returned.

                For `date fields
                <https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html>`__,
                you can specify a [date
                format](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html9.
                For `numeric fields
                <https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html>`__,
                you can specify a `DecimalFormat pattern
                <https://docs.oracle.com/javase/8/docs/api/java/text/DecimalFormat.html>`__.

            For other field data types, this parameter is not supported.

        :param expand_wildcards: ``str``
            Controls what kind of indices that wildcard expressions can expand to.
            Multiple values are accepted when separated by a comma, as in
            ``open,hidden``. Valid values are:

                - ``all`` Expand to open and closed indices, including hidden
                  indices.
                - ``open`` Expand only to open indices.
                - ``closed`` Expand only to closed indices.
                - ``hidden`` Expansion of wildcards will include hidden indices.
                  Must be combined with open, closed, or both.
                - ``none`` Wildcard expressions are not accepted.

            Defaults to ``open``

        :param explain: ``bool``
            If ``true``, returns detailed information about score computation as
            part of a hit. Defaults to ``false``.

        :param fields: ``Optional[Sequence[Union[str, Mapping[str, str]]]]``
            Array of wildcard (``*``) patterns. The request returns values for field
            names matching these patterns in the ``hits.fields`` property of the
            response.

            You can specify items in the array as a string or object. See `Fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html#search-fields-param>`__
            for more details.

            Properties of ``fields`` objects:

                - ``field`` (Required, string) Wildcard pattern. The request returns
                  values for field names matching this pattern.
                - ``format``

                (Optional, string) Format in which the values are returned.

                The date fields date and date_nanos accept a date format. Spatial
                fields accept either geojson for GeoJSON (the default) or wkt for
                Well Known Text.

                For other field data types, this parameter is not supported.

        :param from_: ``int``
            Starting document offset. Defaults to ``0``.

            By default, you cannot page through more than ``10,000`` hits using the
            from and size parameters. To page through more hits, use the
            ``search_after`` parameter.

        :param ignore_throttled: ``bool``
            If ``true``, concrete, expanded or aliased indices will be ignored when
            frozen. Defaults to ``true``.

        :param ignore_unavailable: ``bool``
            If ``true``, missing or closed indices are not included in the response.
            Defaults to ``false``.

        :param indices_boost: ``Optional[Sequence[Mapping[str, float]]]``
            Boosts the ``_score`` of documents from specified indices.

            Properties of ``indices_boost`` objects:

                ``<index>: <boost-value>``

                    - ``<index>`` is the name of the index or index alias. Wildcard
                      (``*``) expressions are supported.
                    - ``<boost-value>`` is the ``float`` factor by which scores are
                      multiplied.

                A boost value greater than ``1.0`` increases the score. A boost
                value between ``0`` and ``1.0`` decreases the score.

        :param max_concurrent_shard_requests: ``int``
            Defines the number of concurrent shard requests per node this search
            executes concurrently. This value should be used to limit the impact of
            the search on the cluster in order to limit the number of concurrent
            shard requests. Defaults to ``5``.

        :param min_score: ``Optional[float]``
            Minimum ``_score`` for matching documents. Documents with a lower
            ``_score`` are not included in the search results.

        :param pre_filter_shard_size: ``Optional[int]``
            Defines a threshold that enforces a pre-filter roundtrip to prefilter
            search shards based on query rewriting if the number of shards the
            search request expands to exceeds the threshold. This filter roundtrip
            can limit the number of shards significantly if for instance a shard can
            not match any documents based on its rewrite method ie. if date filters
            are mandatory to match but the shard bounds and the query are disjoint.
            When unspecified, the pre-filter phase is executed if any of these
            conditions is met:

                - The request targets more than 128 shards.
                - The request targets one or more read-only index.
                - The primary sort of the query targets an indexed field.

        :param preference: ``Optional[str]``
            Nodes and shards used for the search. By default, Elasticsearch selects
            from eligible nodes and shards using `adaptive replica selection
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-shard-routing.html#search-adaptive-replica>`__,
            accounting for `allocation awareness
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html#shard-allocation-awareness>`__.

            Valid values:

                - ``_only_local`` Run the search only on shards on the local node.
                - ``_local`` If possible, run the search on shards on the local
                  node. If not, select shards using the default method.
                - ``_only_nodes:<node-id>,<node-id>`` Run the search on only the
                  specified nodes IDs. If suitable shards exist on more than one
                  selected nodes, use shards on those nodes using the default
                  method. If none of the specified nodes are available, select
                  shards from any available node using the default method.
                - ``_prefer_nodes:<node-id>,<node-id>`` If possible, run the search
                  on the specified nodes IDs. If not, select shards using the
                  default method.
                - ``_shards:<shard>,<shard>`` Run the search only on the specified
                  shards. This value can be combined with other preference values,
                  but this value must come first. For example:
                  ``_shards:2,3|_local``
                - ``<custom-string>`` Any string that does not start with _. If the
                  cluster state and selected shards do not change, searches using
                  the same ``<custom-string>`` value are routed to the same shards
                  in the same order.

        :param q: ``Optional[str]``
            Query in the Lucene query string syntax.

            You can use the ``q`` parameter to run a query parameter search. Query
            parameter searches do not support the full Elasticsearch `Query DSL
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`__
            but are handy for testing.

            .. IMPORTANT::

                The ``q`` parameter overrides the query parameter in the request
                body. If both parameters are specified, documents matching the query
                request body parameter are not returned.

        :param request_cache: ``Optional[bool]``
            If ``true``, the caching of search results is enabled for requests where
            ``size`` is ``0``. See `Shard request cache settings
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-request-cache.html>`__.
            Defaults to index level settings.

        :param rest_total_hits_as_int: ``bool``
            Indicates whether ``hits.total`` should be rendered as an integer or an
            object in the rest search response. Defaults to ``false``.

        :param routing: ``Optional[str]``
            Target the specified primary shard.

        :param scroll: ``Optional[str]``
            Period to retain the `search context
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#scroll-search-context>`__
            for scrolling. Format is `Time units
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#time-units>`__.
            See `Scroll search results
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#scroll-search-results>`__.

            By default, this value cannot exceed ``1d`` (24 hours). You can change
            this limit using the ``search.max_keep_alive`` cluster-level setting.

        :param search_type: ``str``
            How `distributed term frequencies
            <https://en.wikipedia.org/wiki/Tf%E2%80%93idf>`__ are calculated for
            `relevance scoring
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html#relevance-scores>`__.

            Valid values:

                - ``query_then_fetch`` (Default) Distributed term frequencies are
                  calculated locally for each shard running the search. We recommend
                  this option for faster searches with potentially less accurate
                  scoring.
                - ``dfs_query_then_fetch`` Distributed term frequencies are
                  calculated globally, using information gathered from all shards
                  running the search. While this option increases the accuracy of
                  scoring, it adds a round-trip to each shard, which can result in
                  slower searches.

        :param seq_no_primary_term: ``bool``
            If ``true``, returns sequence number and primary term of the last
            modification of each hit. See `Optimistic concurrency control
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/optimistic-concurrency-control.html>`__.

        :param size: ``int``
            Defines the number of hits to return. Defaults to ``10``.

            By default, you cannot page through more than ``10,000`` hits using the
            from and size parameters. To page through more hits, use the
            `search_after
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#search-after>`__
            parameter.

        :param sort: ``Optional[Union[str, Sequence[Union[str, Mapping[str, str]]], Mapping[str, str]]]``
            Change the order of the returned documents. See `sort search results
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/sort-search-results.html>`__.

            The parameter can be:

                - ``"field"`` or ``"-field"`` to sort a field ascending or
                  descending
                - ``{"field": "asc"}`` or ``{"field": "desc"}`` to sort a field
                  ascending or descending
                - a ``list`` of strings or objects as above to sort by a couple of
                  fields
                - ``None`` to turn off sorting

        :param stats: ``Optional[Sequence[str]]``
            Stats groups to associate with the search. Each group maintains a
            statistics aggregation for its associated searches. You can retrieve
            these stats using the `indices stats API
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-stats.html>`__.

        :param stored_fields: ``Optional[str]``
            A comma-separated list of stored fields to return as part of a hit. If
            no fields are specified, no stored fields are included in the response.

            If this field is specified, the ``_source`` parameter defaults to
            ``false``. You can pass ``_source: true`` to return both source fields
            and stored fields in the search response.

        :param suggest_field: ``Optional[str]``
            Specifies which field to use for suggestions.

        :param suggest_text: ``Optional[str]``
            The source text for which the suggestions should be returned.

        :param terminate_after: ``int``
            The maximum number of documents to collect for each shard, upon reaching
            which the query execution will terminate early.

            Defaults to ``0``, which does not terminate query execution early.

        :param timeout: ``Optional[str]``
            Specifies the period of time to wait for a response in `time units
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#time-units>`__.
            If no response is received before the timeout expires, the request fails
            and returns an error. Defaults to no timeout.

        :param track_scores: ``bool``
            If ``true``, calculate and return document scores, even if the scores
            are not used for sorting. Defaults to ``false``.

        :param track_total_hits: ``Union[int, bool]``
            Number of hits matching the query to count accurately. Defaults to
            ``10000``.

            If ``true``, the exact number of hits is returned at the cost of some
            performance.

            If ``false``, the response does not include the total number of hits
            matching the query.

        :param typed_keys: ``bool``
            If ``true``, aggregation and suggester names are being prefixed by their
            respective types in the response. Defaults to ``true``.

        :param version: ``bool``
            If ``true``, returns document version as part of a hit. Defaults to
            ``false``.

        :returns: ``Search``
            A new Search instance is created
        """
        s = self._search.copy()
        if source is not Unset:
            s._parameters._params["_source"] = source
        if source_excludes is not Unset:
            s._parameters._params["_source_excludes"] = source_excludes
        if source_includes is not Unset:
            s._parameters._params["_source_includes"] = source_includes
        if allow_no_indices is not Unset:
            s._parameters._params["allow_no_indices"] = allow_no_indices
        if allow_partial_search_results is not Unset:
            s._parameters._params["allow_partial_search_results"] = allow_partial_search_results
        if batched_reduce_size is not Unset:
            s._parameters._params["batched_reduce_size"] = batched_reduce_size
        if ccs_minimize_roundtrips is not Unset:
            s._parameters._params["ccs_minimize_roundtrips"] = ccs_minimize_roundtrips
        if docvalue_fields is not Unset:
            s._parameters._params["docvalue_fields"] = docvalue_fields
        if expand_wildcards is not Unset:
            s._parameters._params["expand_wildcards"] = expand_wildcards
        if explain is not Unset:
            s._parameters._params["explain"] = explain
        if fields is not Unset:
            s._parameters._params["fields"] = fields
        if from_ is not Unset:
            s._parameters._params["from"] = from_
        if ignore_throttled is not Unset:
            s._parameters._params["ignore_throttled"] = ignore_throttled
        if ignore_unavailable is not Unset:
            s._parameters._params["ignore_unavailable"] = ignore_unavailable
        if indices_boost is not Unset:
            s._parameters._params["indices_boost"] = indices_boost
        if max_concurrent_shard_requests is not Unset:
            s._parameters._params["max_concurrent_shard_requests"] = max_concurrent_shard_requests
        if min_score is not Unset:
            s._parameters._params["min_score"] = min_score
        if pre_filter_shard_size is not Unset:
            s._parameters._params["pre_filter_shard_size"] = pre_filter_shard_size
        if preference is not Unset:
            s._parameters._params["preference"] = preference
        if q is not Unset:
            s._parameters._params["q"] = q
        if request_cache is not Unset:
            s._parameters._params["request_cache"] = request_cache
        if rest_total_hits_as_int is not Unset:
            s._parameters._params["rest_total_hits_as_int"] = rest_total_hits_as_int
        if routing is not Unset:
            s._parameters._params["routing"] = routing
        if scroll is not Unset:
            s._parameters._params["scroll"] = scroll
        if search_type is not Unset:
            s._parameters._params["search_type"] = search_type
        if seq_no_primary_term is not Unset:
            s._parameters._params["seq_no_primary_term"] = seq_no_primary_term
        if size is not Unset:
            s._parameters._params["size"] = size
        if sort is not Unset:
            s._parameters._params["sort"] = sort
        if stats is not Unset:
            s._parameters._params["stats"] = stats
        if stored_fields is not Unset:
            s._parameters._params["stored_fields"] = stored_fields
        if suggest_field is not Unset:
            s._parameters._params["suggest_field"] = suggest_field
        if suggest_text is not Unset:
            s._parameters._params["suggest_text"] = suggest_text
        if terminate_after is not Unset:
            s._parameters._params["terminate_after"] = terminate_after
        if timeout is not Unset:
            s._parameters._params["timeout"] = timeout
        if track_scores is not Unset:
            s._parameters._params["track_scores"] = track_scores
        if track_total_hits is not Unset:
            s._parameters._params["track_total_hits"] = track_total_hits
        if typed_keys is not Unset:
            s._parameters._params["typed_keys"] = typed_keys
        if version is not Unset:
            s._parameters._params["version"] = version
        return s

    def source(
            self,
            value: Union[bool, str, Sequence] = True,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``Union[bool, str, Sequence]``
            Indicates which `source fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html>`__
            are returned for matching documents. These fields are returned in the
            ``hits._source`` property of the search response. Defaults to ``true``.

            Valid values:

                - ``true`` (Boolean) The entire document source is returned.
                - ``false`` (Boolean) The document source is not returned.
                - ``<wildcard_pattern>`` (string or array of strings) Wildcard
                  (``*``) pattern or array of patterns containing source fields to
                  return.
                - ``<object>`` Object containing a list of source fields to include
                  or exclude. Properties for <object>:

                    - ``excludes`` (string or array of strings) Wildcard (``*``)
                      pattern or array of patterns containing source fields to
                      exclude from the response. You can also use this property to
                      exclude fields from the subset specified in includes property.
                    - ``includes`` (string or array of strings) Wildcard (``*``)
                      pattern or array of patterns containing source fields to
                      return. If this property is specified, only these source
                      fields are returned. You can exclude fields from this subset
                      using the ``excludes`` property.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("_source", value)

    def source_excludes(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            A comma-separated list of `source fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html>`__
            to exclude from the response.

            You can also use this parameter to exclude fields from the subset
            specified in ``_source_includes`` query parameter.

            If the ``_source`` parameter is ``false``, this parameter is ignored.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("_source_excludes", value)

    def source_includes(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            A comma-separated list of `source fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html>`__
            to include in the response.

            If this parameter is specified, only these source fields are returned.
            You can exclude fields from this subset using the ``_source_excludes``
            query parameter.

            If the ``_source`` parameter is ``false``, this parameter is ignored.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("_source_includes", value)

    def allow_no_indices(
            self,
            value: bool = True,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``bool``
            If false, the request returns an error if any wildcard expression,
            `index alias
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html>`__,
            or _all value targets only missing or closed indices. This behavior
            applies even if the request targets other open indices. For example, a
            request targeting ``foo*,bar*`` returns an error if an index starts with
            ``foo`` but no index starts with ``bar``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("allow_no_indices", value)

    def allow_partial_search_results(
            self,
            value: bool = True,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``bool``
            If ``true``, returns partial results if there are request timeouts or
            `shard failures
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-replication.html#shard-failures>`__.
            If ``false``, returns an error with no partial results. Defaults to
            ``true``.

            To override the default for this field, set the
            ``search.default_allow_partial_results`` cluster setting to false.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("allow_partial_search_results", value)

    def batched_reduce_size(
            self,
            value: int = 512,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``int``
            The number of shard results that should be reduced at once on the
            coordinating node. This value should be used as a protection mechanism
            to reduce the memory overhead per search request if the potential number
            of shards in the request can be large. Defaults to ``512``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("batched_reduce_size", value)

    def ccs_minimize_roundtrips(
            self,
            value: bool = True,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``bool``
            If ``true``, network round-trips between the coordinating node and the
            remote clusters are minimized when executing cross-cluster search (CCS)
            requests. See `How cross-cluster search handles network delays
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html#ccs-network-delays>`__.
            Defaults to ``true``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("ccs_minimize_roundtrips", value)

    def docvalue_fields(
            self,
            value: Optional[Sequence[Union[str, Mapping[str, str]]]] = None,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``Optional[Sequence[Union[str, Mapping[str, str]]]]``
            Array of wildcard (``*``) patterns. The request returns doc values for
            field names matching these patterns in the ``hits.fields`` property of
            the response.

            You can specify items in the array as a string or object. See `Doc value
            fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html#docvalue-fields>`__.

            Properties of ``docvalue_fields`` objects:

                - ``field`` (Required, string) Wildcard pattern. The request returns
                  doc values for field names matching this pattern.
                - ``format`` (Optional, string) Format in which the doc values are
                  returned.

                For `date fields
                <https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html>`__,
                you can specify a [date
                format](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html9.
                For `numeric fields
                <https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html>`__,
                you can specify a `DecimalFormat pattern
                <https://docs.oracle.com/javase/8/docs/api/java/text/DecimalFormat.html>`__.

            For other field data types, this parameter is not supported.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("docvalue_fields", value)

    def expand_wildcards(
            self,
            value: str = 'open',
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``str``
            Controls what kind of indices that wildcard expressions can expand to.
            Multiple values are accepted when separated by a comma, as in
            ``open,hidden``. Valid values are:

                - ``all`` Expand to open and closed indices, including hidden
                  indices.
                - ``open`` Expand only to open indices.
                - ``closed`` Expand only to closed indices.
                - ``hidden`` Expansion of wildcards will include hidden indices.
                  Must be combined with open, closed, or both.
                - ``none`` Wildcard expressions are not accepted.

            Defaults to ``open``

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("expand_wildcards", value)

    def explain(
            self,
            value: bool = False,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``bool``
            If ``true``, returns detailed information about score computation as
            part of a hit. Defaults to ``false``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("explain", value)

    def fields(
            self,
            value: Optional[Sequence[Union[str, Mapping[str, str]]]] = None,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``Optional[Sequence[Union[str, Mapping[str, str]]]]``
            Array of wildcard (``*``) patterns. The request returns values for field
            names matching these patterns in the ``hits.fields`` property of the
            response.

            You can specify items in the array as a string or object. See `Fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html#search-fields-param>`__
            for more details.

            Properties of ``fields`` objects:

                - ``field`` (Required, string) Wildcard pattern. The request returns
                  values for field names matching this pattern.
                - ``format``

                (Optional, string) Format in which the values are returned.

                The date fields date and date_nanos accept a date format. Spatial
                fields accept either geojson for GeoJSON (the default) or wkt for
                Well Known Text.

                For other field data types, this parameter is not supported.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("fields", value)

    def from_(
            self,
            value: int = 0,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``int``
            Starting document offset. Defaults to ``0``.

            By default, you cannot page through more than ``10,000`` hits using the
            from and size parameters. To page through more hits, use the
            ``search_after`` parameter.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("from", value)

    def ignore_throttled(
            self,
            value: bool = True,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``bool``
            If ``true``, concrete, expanded or aliased indices will be ignored when
            frozen. Defaults to ``true``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("ignore_throttled", value)

    def ignore_unavailable(
            self,
            value: bool = False,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``bool``
            If ``true``, missing or closed indices are not included in the response.
            Defaults to ``false``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("ignore_unavailable", value)

    def indices_boost(
            self,
            value: Optional[Sequence[Mapping[str, float]]] = None,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``Optional[Sequence[Mapping[str, float]]]``
            Boosts the ``_score`` of documents from specified indices.

            Properties of ``indices_boost`` objects:

                ``<index>: <boost-value>``

                    - ``<index>`` is the name of the index or index alias. Wildcard
                      (``*``) expressions are supported.
                    - ``<boost-value>`` is the ``float`` factor by which scores are
                      multiplied.

                A boost value greater than ``1.0`` increases the score. A boost
                value between ``0`` and ``1.0`` decreases the score.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("indices_boost", value)

    def max_concurrent_shard_requests(
            self,
            value: int = 5,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``int``
            Defines the number of concurrent shard requests per node this search
            executes concurrently. This value should be used to limit the impact of
            the search on the cluster in order to limit the number of concurrent
            shard requests. Defaults to ``5``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("max_concurrent_shard_requests", value)

    def min_score(
            self,
            value: Optional[float] = None,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``Optional[float]``
            Minimum ``_score`` for matching documents. Documents with a lower
            ``_score`` are not included in the search results.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("min_score", value)

    def pre_filter_shard_size(
            self,
            value: Optional[int] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[int]``
            Defines a threshold that enforces a pre-filter roundtrip to prefilter
            search shards based on query rewriting if the number of shards the
            search request expands to exceeds the threshold. This filter roundtrip
            can limit the number of shards significantly if for instance a shard can
            not match any documents based on its rewrite method ie. if date filters
            are mandatory to match but the shard bounds and the query are disjoint.
            When unspecified, the pre-filter phase is executed if any of these
            conditions is met:

                - The request targets more than 128 shards.
                - The request targets one or more read-only index.
                - The primary sort of the query targets an indexed field.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("pre_filter_shard_size", value)

    def preference(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            Nodes and shards used for the search. By default, Elasticsearch selects
            from eligible nodes and shards using `adaptive replica selection
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-shard-routing.html#search-adaptive-replica>`__,
            accounting for `allocation awareness
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html#shard-allocation-awareness>`__.

            Valid values:

                - ``_only_local`` Run the search only on shards on the local node.
                - ``_local`` If possible, run the search on shards on the local
                  node. If not, select shards using the default method.
                - ``_only_nodes:<node-id>,<node-id>`` Run the search on only the
                  specified nodes IDs. If suitable shards exist on more than one
                  selected nodes, use shards on those nodes using the default
                  method. If none of the specified nodes are available, select
                  shards from any available node using the default method.
                - ``_prefer_nodes:<node-id>,<node-id>`` If possible, run the search
                  on the specified nodes IDs. If not, select shards using the
                  default method.
                - ``_shards:<shard>,<shard>`` Run the search only on the specified
                  shards. This value can be combined with other preference values,
                  but this value must come first. For example:
                  ``_shards:2,3|_local``
                - ``<custom-string>`` Any string that does not start with _. If the
                  cluster state and selected shards do not change, searches using
                  the same ``<custom-string>`` value are routed to the same shards
                  in the same order.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("preference", value)

    def q(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            Query in the Lucene query string syntax.

            You can use the ``q`` parameter to run a query parameter search. Query
            parameter searches do not support the full Elasticsearch `Query DSL
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`__
            but are handy for testing.

            .. IMPORTANT::

                The ``q`` parameter overrides the query parameter in the request
                body. If both parameters are specified, documents matching the query
                request body parameter are not returned.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("q", value)

    def request_cache(
            self,
            value: Optional[bool] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[bool]``
            If ``true``, the caching of search results is enabled for requests where
            ``size`` is ``0``. See `Shard request cache settings
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-request-cache.html>`__.
            Defaults to index level settings.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("request_cache", value)

    def rest_total_hits_as_int(
            self,
            value: bool = False,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``bool``
            Indicates whether ``hits.total`` should be rendered as an integer or an
            object in the rest search response. Defaults to ``false``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("rest_total_hits_as_int", value)

    def routing(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            Target the specified primary shard.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("routing", value)

    def scroll(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            Period to retain the `search context
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#scroll-search-context>`__
            for scrolling. Format is `Time units
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#time-units>`__.
            See `Scroll search results
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#scroll-search-results>`__.

            By default, this value cannot exceed ``1d`` (24 hours). You can change
            this limit using the ``search.max_keep_alive`` cluster-level setting.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("scroll", value)

    def search_type(
            self,
            value: str = 'query_then_fetch',
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``str``
            How `distributed term frequencies
            <https://en.wikipedia.org/wiki/Tf%E2%80%93idf>`__ are calculated for
            `relevance scoring
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html#relevance-scores>`__.

            Valid values:

                - ``query_then_fetch`` (Default) Distributed term frequencies are
                  calculated locally for each shard running the search. We recommend
                  this option for faster searches with potentially less accurate
                  scoring.
                - ``dfs_query_then_fetch`` Distributed term frequencies are
                  calculated globally, using information gathered from all shards
                  running the search. While this option increases the accuracy of
                  scoring, it adds a round-trip to each shard, which can result in
                  slower searches.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("search_type", value)

    def seq_no_primary_term(
            self,
            value: bool = False,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``bool``
            If ``true``, returns sequence number and primary term of the last
            modification of each hit. See `Optimistic concurrency control
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/optimistic-concurrency-control.html>`__.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("seq_no_primary_term", value)

    def size(
            self,
            value: int = 10,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``int``
            Defines the number of hits to return. Defaults to ``10``.

            By default, you cannot page through more than ``10,000`` hits using the
            from and size parameters. To page through more hits, use the
            `search_after
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#search-after>`__
            parameter.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("size", value)

    def sort(
            self,
            value: Optional[Union[str, Sequence[Union[str, Mapping[str, str]]], Mapping[str, str]]] = None,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``Optional[Union[str, Sequence[Union[str, Mapping[str, str]]], Mapping[str, str]]]``
            Change the order of the returned documents. See `sort search results
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/sort-search-results.html>`__.

            The parameter can be:

                - ``"field"`` or ``"-field"`` to sort a field ascending or
                  descending
                - ``{"field": "asc"}`` or ``{"field": "desc"}`` to sort a field
                  ascending or descending
                - a ``list`` of strings or objects as above to sort by a couple of
                  fields
                - ``None`` to turn off sorting

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("sort", value)

    def stats(
            self,
            value: Optional[Sequence[str]] = None,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``Optional[Sequence[str]]``
            Stats groups to associate with the search. Each group maintains a
            statistics aggregation for its associated searches. You can retrieve
            these stats using the `indices stats API
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-stats.html>`__.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("stats", value)

    def stored_fields(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            A comma-separated list of stored fields to return as part of a hit. If
            no fields are specified, no stored fields are included in the response.

            If this field is specified, the ``_source`` parameter defaults to
            ``false``. You can pass ``_source: true`` to return both source fields
            and stored fields in the search response.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("stored_fields", value)

    def suggest_field(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            Specifies which field to use for suggestions.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("suggest_field", value)

    def suggest_text(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            The source text for which the suggestions should be returned.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("suggest_text", value)

    def terminate_after(
            self,
            value: int = 0,
    ) -> Search:
        """
        A search **body** parameter.

        :param value: ``int``
            The maximum number of documents to collect for each shard, upon reaching
            which the query execution will terminate early.

            Defaults to ``0``, which does not terminate query execution early.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("terminate_after", value)

    def timeout(
            self,
            value: Optional[str] = None,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Optional[str]``
            Specifies the period of time to wait for a response in `time units
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#time-units>`__.
            If no response is received before the timeout expires, the request fails
            and returns an error. Defaults to no timeout.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("timeout", value)

    def track_scores(
            self,
            value: bool = False,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``bool``
            If ``true``, calculate and return document scores, even if the scores
            are not used for sorting. Defaults to ``false``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("track_scores", value)

    def track_total_hits(
            self,
            value: Union[int, bool] = 10000,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``Union[int, bool]``
            Number of hits matching the query to count accurately. Defaults to
            ``10000``.

            If ``true``, the exact number of hits is returned at the cost of some
            performance.

            If ``false``, the response does not include the total number of hits
            matching the query.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("track_total_hits", value)

    def typed_keys(
            self,
            value: bool = True,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``bool``
            If ``true``, aggregation and suggester names are being prefixed by their
            respective types in the response. Defaults to ``true``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("typed_keys", value)

    def version(
            self,
            value: bool = False,
    ) -> Search:
        """
        A search **query** parameter.

        :param value: ``bool``
            If ``true``, returns document version as part of a hit. Defaults to
            ``false``.

        :returns: ``Search``
            A new Search instance is created
        """
        return self._set_parameter("version", value)
