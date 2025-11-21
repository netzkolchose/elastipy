# auto-generated file - do not edit
from datetime import date, datetime
from typing import Mapping, Sequence, Any, Union, Optional

from .query import Query, QueryInterface


__all__ = (
    "_Bool", "GeoBoundingBox", "GeoDistance", "GeoGrid", "GeoShape", "Knn",
    "Match", "_MatchAll", "_MatchNone", "QueryString", "Range", "Term", "_Terms"
)


class _Bool(Query, factory=False):

    """
    A query that matches documents matching boolean combinations of other
    queries. The bool query maps to Lucene BooleanQuery. It is built using one
    or more boolean clauses, each clause with a typed occurrence.

    The bool query takes a more-matches-is-better approach, so the score from
    each matching must or should clause will be added together to provide the
    final _score for each document.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html>`__
    """

    name = 'bool'
    _parameters = {'must': {}, 'must_not': {}, 'should': {}, 'filter': {}}


    def __init__(
            self,
            must: Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]] = None,
            must_not: Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]] = None,
            should: Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]] = None,
            filter: Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]] = None,
    ):
        """
        A query that matches documents matching boolean combinations of other
        queries. The bool query maps to Lucene BooleanQuery. It is built using one
        or more boolean clauses, each clause with a typed occurrence.

        The bool query takes a more-matches-is-better approach, so the score from
        each matching must or should clause will be added together to provide the
        final _score for each document.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html>`__

        :param must: ``Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]]``
            The clause (query) must appear in matching documents and will contribute
            to the score.

        :param must_not: ``Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]]``
            The clause (query) must not appear in the matching documents. Clauses
            are executed in filter context meaning that scoring is ignored and
            clauses are considered for caching. Because scoring is ignored, a score
            of 0 for all documents is returned.

        :param should: ``Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]]``
            The clause (query) should appear in the matching document.

        :param filter: ``Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]]``
            The clause (query) must appear in matching documents. However unlike
            must the score of the query will be ignored. Filter clauses are executed
            in filter context, meaning that scoring is ignored and clauses are
            considered for caching.
        """
        super().__init__(
            must=must,
            must_not=must_not,
            should=should,
            filter=filter,
        )


class GeoBoundingBox(Query):

    """
    Matches geo_point and geo_shape values that intersect a bounding box.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-bounding-box-query.html>`__
    """

    name = 'geo_bounding_box'
    _parameters = {'field': {'required': True}, 'box': {'required': True, 'top_level_field_value': 'field'}, 'validation_method': {'default': 'STRICT'}, 'ignore_unmapped': {'default': False}}
    _top_level_field_parameter = ('box', 'field')


    def __init__(
            self,
            field: str,
            box: Mapping[str, Union[str, float, Mapping[str, float], Sequence[float]]],
            validation_method: str = 'STRICT',
            ignore_unmapped: bool = False,
    ):
        """
        Matches geo_point and geo_shape values that intersect a bounding box.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-bounding-box-query.html>`__

        :param field: ``str``
            The geo_point or geo_shape field you wish to search.

        :param box: ``Mapping[str, Union[str, float, Mapping[str, float], Sequence[float]]]``
            To define the box, provide geopoint values for two opposite corners:

            .. CODE::

                {"top_left": [-74.1, 40.73], "bottom_right": [-71.12, 40.01]}

            or provide values for each of the four corners:

            .. CODE::

                {"top": 40.73, "left": -74.1, "bottom": 40.01, "right": -71.12}

            The points can accept all formats supported by the `geo_point type
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html>`__:

                - Object format: ``{ "lat" : 52.3760, "lon" : 4.894 }`` - this is
                  the safest format as it is the most explicit about the lat & lon
                  values
                - String format: ``"52.3760, 4.894"`` - where the first number is
                  the lat and the second is the lon
                - Array format: ``[4.894, 52.3760]`` - which is based on the GeoJson
                  standard and where the first number is the lon and the second one
                  is the lat

            Additionally, geohashes can be used. When geohashes are used to specify
            the bounding the edges of the bounding box, the geohashes are treated as
            rectangles. The bounding box is defined in such a way that its top left
            corresponds to the top left corner of the geohash specified in the
            top_left parameter and its bottom right is defined as the bottom right
            of the geohash specified in the bottom_right parameter.

            In order to specify a bounding box that would match entire area of a
            geohash the geohash can be specified in both top_left and bottom_right
            parameters:

            .. CODE::

                {"top_left": "dr", "bottom_right": "dr"}

            .. NOTE::

                Notes on precision:

                Geopoints have limited precision and are always rounded down during
                index time. During the query time, upper boundaries of the bounding
                boxes are rounded down, while lower boundaries are rounded up. As a
                result, the points along on the lower bounds (bottom and left edges
                of the bounding box) might not make it into the bounding box due to
                the rounding error. At the same time points alongside the upper
                bounds (top and right edges) might be selected by the query even if
                they are located slightly outside the edge. The rounding error
                should be less than 4.20e-8 degrees on the latitude and less than
                8.39e-8 degrees on the longitude, which translates to less than 1cm
                error even at the equator.

                Geoshapes also have limited precision due to rounding. Geoshape
                edges along the bounding box’s bottom and left edges may not match a
                geo_bounding_box query. Geoshape edges slightly outside the box’s
                top and right edges may still match the query.

        :param validation_method: ``str``
            Set to ``IGNORE_MALFORMED`` to accept geo points with invalid latitude
            or longitude, set to ``COERCE`` to additionally try and infer correct
            coordinates (default is ``STRICT``)

        :param ignore_unmapped: ``bool``
            When set to true the ``ignore_unmapped`` option will ignore an unmapped
            field and will not match any documents for this query. This can be
            useful when querying multiple indexes which might have different
            mappings. When set to false (the default value) the query will throw an
            exception if the field is not mapped.
        """
        super().__init__(
            field=field,
            box=box,
            validation_method=validation_method,
            ignore_unmapped=ignore_unmapped,
        )


class GeoDistance(Query):

    """
    Matches geo_point and geo_shape values within a given distance of a
    geopoint.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-distance-query.html>`__
    """

    name = 'geo_distance'
    _parameters = {'field': {'required': True}, 'origin': {'required': True, 'top_level_field_value': 'field'}, 'distance': {'required': True}, 'distance_type': {'default': 'arc'}, 'validation_method': {'default': 'STRICT'}, 'ignore_unmapped': {'default': False}}
    _top_level_field_parameter = ('origin', 'field')


    def __init__(
            self,
            field: str,
            origin: Union[str, Mapping[str, float], Sequence[float]],
            distance: str,
            distance_type: str = 'arc',
            validation_method: str = 'STRICT',
            ignore_unmapped: bool = False,
    ):
        """
        Matches geo_point and geo_shape values within a given distance of a
        geopoint.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-distance-query.html>`__

        :param field: ``str``
            The geo_point or geo_shape field you wish to search.

        :param origin: ``Union[str, Mapping[str, float], Sequence[float]]``
            The origin point can accept all formats supported by the `geo_point type
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html>`__:

                - Object format: ``{ "lat" : 52.3760, "lon" : 4.894 }`` - this is
                  the safest format as it is the most explicit about the lat & lon
                  values
                - String format: ``"52.3760, 4.894"`` - where the first number is
                  the lat and the second is the lon
                - Array format: ``[4.894, 52.3760]`` - which is based on the GeoJson
                  standard and where the first number is the lon and the second one
                  is the lat

        :param distance: ``str``
            The radius of the circle centred on the specified location. Points which
            fall into this circle are considered to be matches. The distance can be
            specified in various units. See `Distance Units
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/api-conventions.html#distance-units>`__.

        :param distance_type: ``str``
            How to compute the distance. Can either be ``arc`` (default), or
            ``plane`` (faster, but inaccurate on long distances and close to the
            poles).

        :param validation_method: ``str``
            Set to ``IGNORE_MALFORMED`` to accept geo points with invalid latitude
            or longitude, set to ``COERCE`` to additionally try and infer correct
            coordinates (default is ``STRICT``)

        :param ignore_unmapped: ``bool``
            When set to true the ``ignore_unmapped`` option will ignore an unmapped
            field and will not match any documents for this query. This can be
            useful when querying multiple indexes which might have different
            mappings. When set to false (the default value) the query will throw an
            exception if the field is not mapped.
        """
        super().__init__(
            field=field,
            origin=origin,
            distance=distance,
            distance_type=distance_type,
            validation_method=validation_method,
            ignore_unmapped=ignore_unmapped,
        )


class GeoGrid(Query):

    """
    Matches geo_point and geo_shape values that intersect a grid cell from a
    GeoGrid aggregation.

    The query is designed to match the documents that fall inside a bucket of a
    geogrid aggregation by providing the key of the bucket. For geohash and
    geotile grids, the query can be used for geo_point and geo_shape fields. For
    geo_hex grid, it can only be used for geo_point fields.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-grid-query.html>`__
    """

    name = 'geo_grid'
    _parameters = {'field': {'required': True, 'top_level': True}, 'geohash': {}, 'geotile': {}, 'geohex': {}}
    _top_level_parameter = 'field'


    def __init__(
            self,
            field: str,
            geohash: Optional[str] = None,
            geotile: Optional[str] = None,
            geohex: Optional[str] = None,
    ):
        """
        Matches geo_point and geo_shape values that intersect a grid cell from a
        GeoGrid aggregation.

        The query is designed to match the documents that fall inside a bucket of a
        geogrid aggregation by providing the key of the bucket. For geohash and
        geotile grids, the query can be used for geo_point and geo_shape fields. For
        geo_hex grid, it can only be used for geo_point fields.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-grid-query.html>`__

        :param field: ``str``
            The geo_point or geo_shape field you wish to search.

        :param geohash: ``Optional[str]``
            Extract the documents using the geohash bucket key, e.g. ``"u0"``
            "6/32/22"

        :param geotile: ``Optional[str]``
            Extract the documents using the geotile bucket key, e.g. ``"6/32/22"``

        :param geohex: ``Optional[str]``
            Extract the documents using the geohex bucket key, e.g.
            ``"811fbffffffffff"``
        """
        super().__init__(
            field=field,
            geohash=geohash,
            geotile=geotile,
            geohex=geohex,
        )


class GeoShape(Query):

    """
    Filter documents indexed using either the geo_shape or the geo_point type.

    The geo_shape query uses the same `index
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html#geoshape-indexing-approach>`__
    as the geo_shape or geo_point mapping to find documents that have a shape
    that is related to the query shape, using a specified `spatial relationship
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-shape-query.html#geo-shape-spatial-relations>`__:
    either intersects, contained, within or disjoint.

    The query supports two ways of defining the query shape, either by providing
    a whole shape definition, or by referencing the name of a shape pre-indexed
    in another index.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-shape-query.html>`__
    """

    name = 'geo_shape'
    _parameters = {'field': {'required': True, 'top_level': True}, 'shape': {}, 'indexed_shape': {}, 'relation': {'default': 'intersects'}, 'ignore_unmapped': {'default': False}}
    _top_level_parameter = 'field'


    def __init__(
            self,
            field: str,
            shape: Optional[Mapping[str, Any]] = None,
            indexed_shape: Optional[Mapping[str, str]] = None,
            relation: str = 'intersects',
            ignore_unmapped: bool = False,
    ):
        """
        Filter documents indexed using either the geo_shape or the geo_point type.

        The geo_shape query uses the same `index
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html#geoshape-indexing-approach>`__
        as the geo_shape or geo_point mapping to find documents that have a shape
        that is related to the query shape, using a specified `spatial relationship
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-shape-query.html#geo-shape-spatial-relations>`__:
        either intersects, contained, within or disjoint.

        The query supports two ways of defining the query shape, either by providing
        a whole shape definition, or by referencing the name of a shape pre-indexed
        in another index.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-shape-query.html>`__

        :param field: ``str``
            The geo_point or geo_shape field you wish to search.

        :param shape: ``Optional[Mapping[str, Any]]``
            The shape to locate points or shapes.

            For example, this shape will find the point using Elasticsearch’s
            ``envelope`` GeoJSON extension:

            .. CODE::

              { "type": "envelope", "coordinates": [ [13, 53], [14, 52] ] }

            .. CODE::

              { "type": "multipoint" "coordinates": [ [46.25, 20.14], [47.49, 19.04]
              ] }

        :param indexed_shape: ``Optional[Mapping[str, str]]``
            The query also supports using a shape which has already been indexed in
            another index. This is particularly useful for when you have a
            pre-defined list of shapes and you want to reference the list using a
            logical name (for example New Zealand) rather than having to provide
            coordinates each time. In this situation, it is only necessary to
            provide:

              - id - The ID of the document that contains the pre-indexed shape.
              - index - Name of the index where the pre-indexed shape is. Defaults
                to ``shapes``.
              - path - The field specified as path containing the pre-indexed shape.
                Defaults to ``shape``.
              - routing - The routing of the shape document if required.

            The following is an example of using the Filter with a pre-indexed
            shape:

            .. CODE::

                indexed_shape={ "index": "shapes", "id": "deu", "path": "location" }

        :param relation: ``str``
            - ``INTERSECTS`` - (default) Return all documents whose geo_shape or
              geo_point field intersects the query geometry.
            - ``DISJOINT`` - Return all documents whose geo_shape or geo_point field
              has nothing in common with the query geometry.
            - ``WITHIN`` - Return all documents whose geo_shape or geo_point field
              is within the query geometry. Line geometries are not supported.
            - ``CONTAINS`` - Return all documents whose geo_shape or geo_point field
              contains the query geometry.

        :param ignore_unmapped: ``bool``
            When set to true the ``ignore_unmapped`` option will ignore an unmapped
            field and will not match any documents for this query. This can be
            useful when querying multiple indexes which might have different
            mappings. When set to false (the default value) the query will throw an
            exception if the field is not mapped.
        """
        super().__init__(
            field=field,
            shape=shape,
            indexed_shape=indexed_shape,
            relation=relation,
            ignore_unmapped=ignore_unmapped,
        )


class Knn(Query):

    """
    Finds the k nearest vectors to a query vector, as measured by a similarity
    metric. knn query finds nearest vectors through approximate search on
    indexed dense_vectors. The preferred way to do approximate kNN search is
    through the `top level knn section
    <https://www.elastic.co/docs/solutions/search/vector/knn>`__ of a search
    request. knn query is reserved for expert cases, where there is a need to
    combine this query with other queries, or perform a kNN search against a
    `semantic_text
    <https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text>`__
    field.

    `elasticsearch documentation
    <https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-knn-query>`__
    """

    name = 'knn'
    _parameters = {'field': {'required': True}, 'query_vector': {}, 'query_vector_builder': {}, 'k': {}, 'num_candidates': {}, 'visit_percentage': {'version': '9.2'}, 'filter': {}, 'similarity': {}, 'boost': {}}


    def __init__(
            self,
            field: str,
            query_vector: Optional[Union[str, Sequence[int], Sequence[float]]] = None,
            query_vector_builder: Optional[Mapping] = None,
            k: Optional[int] = None,
            num_candidates: Optional[int] = None,
            visit_percentage: Optional[float] = None,
            filter: Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]] = None,
            similarity: Optional[float] = None,
            boost: Optional[float] = None,
    ):
        """
        Finds the k nearest vectors to a query vector, as measured by a similarity
        metric. knn query finds nearest vectors through approximate search on
        indexed dense_vectors. The preferred way to do approximate kNN search is
        through the `top level knn section
        <https://www.elastic.co/docs/solutions/search/vector/knn>`__ of a search
        request. knn query is reserved for expert cases, where there is a need to
        combine this query with other queries, or perform a kNN search against a
        `semantic_text
        <https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text>`__
        field.

        `elasticsearch documentation
        <https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-knn-query>`__

        :param field: ``str``
            The name of the vector field to search against. Must be a
            ```dense_vector`` field with indexing enabled
            <https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector#index-vectors-knn-search>`__,
            or a ```semantic_text`` field
            <https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text>`__
            with a compatible dense vector inference model.

        :param query_vector: ``Optional[Union[str, Sequence[int], Sequence[float]]]``
            Query vector. Must have the same number of dimensions as the vector
            field you are searching against. Must be either an array of floats or a
            hex-encoded byte vector. Either this or ``query_vector_builder`` must be
            provided.

        :param query_vector_builder: ``Optional[Mapping]``
            Query vector builder. A configuration object indicating how to build a
            query_vector before executing the request. You must provide either a
            query_vector_builder or query_vector, but not both. Refer to `Perform
            semantic search
            <https://www.elastic.co/docs/solutions/search/vector/knn#knn-semantic-search>`__
            to learn more.

            If all queried fields are of type ```semantic_text``
            <https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text>`__,
            the inference ID associated with the ``semantic_text`` field may be
            inferred.

        :param k: ``Optional[int]``
            The number of nearest neighbors to return from each shard. Elasticsearch
            collects ``k`` results from each shard, then merges them to find the
            global top results. This value must be less than or equal to
            ``num_candidates``. Defaults to search request size.

        :param num_candidates: ``Optional[int]``
            The number of nearest neighbor candidates to consider per shard while
            doing knn search. Cannot exceed 10,000. Increasing num_candidates tends
            to improve the accuracy of the final results. Defaults to ``1.5 * k`` if
            ``k`` is set, or ``1.5 * size`` if ``k`` is not set.

        :param visit_percentage: ``Optional[float]``
            The percentage of vectors to explore per shard while doing knn search
            with ``bbq_disk``. Must be between 0 and 100.  0 will default to using
            ``num_candidates`` for calculating the percent visited. Increasing
            ``visit_percentage`` tends to improve the accuracy of the final results.
             If ``visit_percentage`` is set for ``bbq_disk``, ``num_candidates`` is
            ignored. Defaults to ~1% per shard for every 1 million vectors.

        :param filter: ``Optional[Union['QueryInterface', Mapping, Sequence[Union['QueryInterface', Mapping]]]]``
            Query to filter the documents that can match. The kNN search will return
            the top documents that also match this filter. The value can be a single
            query or a list of queries. If ``filter`` is not provided, all documents
            are allowed to match.

            The filter is a pre-filter, meaning that it is applied **during** the
            approximate kNN search to ensure that ``num_candidates`` matching
            documents are returned.

        :param similarity: ``Optional[float]``
            The minimum similarity required for a document to be considered a match.
            The similarity value calculated relates to the raw ```similarity``
            <https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector#dense-vector-similarity>`__
            used. Not the document score. The matched documents are then scored
            according to ```similarity``
            <https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector#dense-vector-similarity>`__
            and the provided ``boost`` is applied.

        :param boost: ``Optional[float]``
            Floating point number used to multiply the scores of matched documents.
            This value cannot be negative. Defaults to ``1.0``.
        """
        super().__init__(
            field=field,
            query_vector=query_vector,
            query_vector_builder=query_vector_builder,
            k=k,
            num_candidates=num_candidates,
            visit_percentage=visit_percentage,
            filter=filter,
            similarity=similarity,
            boost=boost,
        )


class Match(Query):

    """
    Returns documents that match a provided text, number, date or boolean value.
    The provided text is analyzed before matching.

    The match query is the standard query for performing a full-text search,
    including options for fuzzy matching.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html>`__
    """

    name = 'match'
    _parameters = {'field': {'required': True, 'top_level': True}, 'query': {'required': True}, 'auto_generate_synonyms_phrase_query': {'default': True}, 'fuzziness': {}, 'max_expansions': {'default': 50}, 'prefix_length': {'default': 0}, 'fuzzy_transpositions': {'default': True}, 'fuzzy_rewrite': {}, 'lenient': {'default': False}, 'operator': {}, 'minimum_should_match': {}, 'zero_terms_query': {'default': 'none'}}
    _top_level_parameter = 'field'


    def __init__(
            self,
            field: str,
            query: Union[str, int, float, bool],
            auto_generate_synonyms_phrase_query: bool = True,
            fuzziness: Optional[str] = None,
            max_expansions: int = 50,
            prefix_length: int = 0,
            fuzzy_transpositions: bool = True,
            fuzzy_rewrite: Optional[str] = None,
            lenient: bool = False,
            operator: Optional[str] = None,
            minimum_should_match: Optional[str] = None,
            zero_terms_query: str = 'none',
    ):
        """
        Returns documents that match a provided text, number, date or boolean value.
        The provided text is analyzed before matching.

        The match query is the standard query for performing a full-text search,
        including options for fuzzy matching.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html>`__

        :param field: ``str``
            Field you wish to search.

        :param query: ``Union[str, int, float, bool]``
            Text, number, boolean value or date you wish to find in the provided
            <field>.

            The match query analyzes any provided text before performing a search.
            This means the match query can search text fields for analyzed tokens
            rather than an exact term.

        :param auto_generate_synonyms_phrase_query: ``bool``
            If true, match phrase queries are automatically created for multi-term
            synonyms. Defaults to true.

        :param fuzziness: ``Optional[str]``
            Maximum edit distance allowed for matching. See Fuzziness for valid
            values and more information. See Fuzziness in the match query for an
            example.

        :param max_expansions: ``int``
            Maximum number of terms to which the query will expand. Defaults to 50.

        :param prefix_length: ``int``
            Number of beginning characters left unchanged for fuzzy matching.
            Defaults to 0.

        :param fuzzy_transpositions: ``bool``
            If true, edits for fuzzy matching include transpositions of two adjacent
            characters (ab → ba). Defaults to true.

        :param fuzzy_rewrite: ``Optional[str]``
            Method used to rewrite the query. See the rewrite parameter for valid
            values and more information.

            If the fuzziness parameter is not 0, the match query uses a
            fuzzy_rewrite method of ``top_terms_blended_freqs_${max_expansions}`` by
            default.

        :param lenient: ``bool``
            If true, format-based errors, such as providing a text query value for a
            numeric field, are ignored. Defaults to false.

        :param operator: ``Optional[str]``
            Boolean logic used to interpret text in the query value. Valid values
            are:

                - ``OR`` (Default) For example, a query value of capital of Hungary
                  is interpreted as capital OR of OR Hungary.
                - ``AND`` For example, a query value of capital of Hungary is
                  interpreted as capital AND of AND Hungary.

        :param minimum_should_match: ``Optional[str]``
            Minimum number of clauses that must match for a document to be returned.
            See the minimum_should_match parameter for valid values and more
            information.

        :param zero_terms_query: ``str``
            Indicates whether no documents are returned if the analyzer removes all
            tokens, such as when using a stop filter. Valid values are: none
            (Default) No documents are returned if the analyzer removes all tokens.
            all Returns all documents, similar to a match_all query.
        """
        super().__init__(
            field=field,
            query=query,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            fuzziness=fuzziness,
            max_expansions=max_expansions,
            prefix_length=prefix_length,
            fuzzy_transpositions=fuzzy_transpositions,
            fuzzy_rewrite=fuzzy_rewrite,
            lenient=lenient,
            operator=operator,
            minimum_should_match=minimum_should_match,
            zero_terms_query=zero_terms_query,
        )


class _MatchAll(Query, factory=False):

    """
    The most simple query, which matches all documents, giving them all a
    ``_score`` of 1.0.

    The _score can be changed with the boost parameter

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html>`__
    """

    name = 'match_all'
    _parameters = {'boost': {}}


    def __init__(
            self,
            boost: Optional[float] = None,
    ):
        """
        The most simple query, which matches all documents, giving them all a
        ``_score`` of 1.0.

        The _score can be changed with the boost parameter

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html>`__

        :param boost: ``Optional[float]``
            The _score can be changed with the boost parameter
        """
        super().__init__(
            boost=boost,
        )


class _MatchNone(Query, factory=False):

    """
    This is the inverse of the match_all query, which matches no documents.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html>`__
    """

    name = 'match_none'
    _parameters = {}


    def __init__(
            self,
    ):
        """
        This is the inverse of the match_all query, which matches no documents.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html>`__
        """
        super().__init__(
        )


class QueryString(Query):

    """
    Returns documents based on a provided query string, using a parser with a
    strict syntax.

    This query uses a `syntax
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax>`__
    to parse and split the provided query string based on operators, such as
    ``AND`` or ``NOT``. The query then `analyzes
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html>`__
    each split text independently before returning matching documents.

    You can use the query_string query to create a complex search that includes
    wildcard characters, searches across multiple fields, and more. While
    versatile, the query is strict and returns an error if the query string
    includes any invalid syntax.

    .. WARNING::

        Because it returns an error for any invalid syntax, we don’t recommend
        using the query_string query for search boxes.

        If you don’t need to support a query syntax, consider using the `match
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html>`__
        query. If you need the features of a query syntax, use the
        `simple_query_string
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-simple-query-string-query.html>`__
        query, which is less strict.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html>`__
    """

    name = 'query_string'
    _parameters = {'query': {'required': True}, 'default_field': {}, 'allow_leading_wildcard': {'default': True}, 'analyze_wildcard': {'default': False}, 'analyzer': {}, 'auto_generate_synonyms_phrase_query': {}, 'boost': {'default': 1.0}, 'default_operator': {}, 'enable_position_increments': {'default': True}, 'fields': {}, 'fuzziness': {}, 'fuzzy_max_expansions': {'default': 50}, 'fuzzy_prefix_length': {'default': 0}, 'fuzzy_transpositions': {'default': True}, 'lenient': {'default': False}, 'max_determinized_states': {'default': 10000}, 'minimum_should_match': {}, 'quote_analyzer': {}, 'phrase_slop': {'default': 0}, 'quote_field_suffix': {}, 'rewrite': {}, 'time_zone': {}}


    def __init__(
            self,
            query: str,
            default_field: Optional[str] = None,
            allow_leading_wildcard: bool = True,
            analyze_wildcard: bool = False,
            analyzer: Optional[str] = None,
            auto_generate_synonyms_phrase_query: Optional[bool] = None,
            boost: float = 1.0,
            default_operator: Optional[str] = None,
            enable_position_increments: bool = True,
            fields: Optional[Sequence[str]] = None,
            fuzziness: Optional[str] = None,
            fuzzy_max_expansions: int = 50,
            fuzzy_prefix_length: int = 0,
            fuzzy_transpositions: bool = True,
            lenient: bool = False,
            max_determinized_states: int = 10000,
            minimum_should_match: Optional[str] = None,
            quote_analyzer: Optional[str] = None,
            phrase_slop: int = 0,
            quote_field_suffix: Optional[str] = None,
            rewrite: Optional[str] = None,
            time_zone: Optional[str] = None,
    ):
        """
        Returns documents based on a provided query string, using a parser with a
        strict syntax.

        This query uses a `syntax
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax>`__
        to parse and split the provided query string based on operators, such as
        ``AND`` or ``NOT``. The query then `analyzes
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html>`__
        each split text independently before returning matching documents.

        You can use the query_string query to create a complex search that includes
        wildcard characters, searches across multiple fields, and more. While
        versatile, the query is strict and returns an error if the query string
        includes any invalid syntax.

        .. WARNING::

            Because it returns an error for any invalid syntax, we don’t recommend
            using the query_string query for search boxes.

            If you don’t need to support a query syntax, consider using the `match
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html>`__
            query. If you need the features of a query syntax, use the
            `simple_query_string
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-simple-query-string-query.html>`__
            query, which is less strict.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html>`__

        :param query: ``str``
            Query string you wish to parse and use for search. See `Query string
            syntax
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax>`__.

        :param default_field: ``Optional[str]``
            Default field you wish to search if no field is provided in the query
            string.

            Defaults to the ``index.query.default_field`` index setting, which has a
            default value of ``*``. The ``*`` value extracts all fields that are
            eligible for term queries and filters the metadata fields. All extracted
            fields are then combined to build a query if no prefix is specified.

            Searching across all eligible fields does not include nested documents.
            Use a nested query to search those documents.

            For mappings with a large number of fields, searching across all
            eligible fields could be expensive.

            There is a limit on the number of fields that can be queried at once. It
            is defined by the indices.query.bool.max_clause_count search setting,
            which defaults to 1024.

        :param allow_leading_wildcard: ``bool``
            If true, the wildcard characters * and ? are allowed as the first
            character of the query string. Defaults to true.

        :param analyze_wildcard: ``bool``
            If true, the query attempts to analyze wildcard terms in the query
            string. Defaults to false.

        :param analyzer: ``Optional[str]``
            `Analyzer
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html>`__
            used to convert text in the query string into tokens. Defaults to the
            `index-time analyzer
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/specify-analyzer.html#specify-index-time-analyzer>`__
            mapped for the default_field. If no analyzer is mapped, the index’s
            default analyzer is used.

        :param auto_generate_synonyms_phrase_query: ``Optional[bool]``
            If true, `match phrase
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query-phrase.html>`__
            queries are automatically created for multi-term synonyms. Defaults to
            true. See `Synonyms and the query_string query
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-synonyms>`__
            for an example.

        :param boost: ``float``
            Floating point number used to decrease or increase the `relevance scores
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html#relevance-scores>`__
            of the query. Defaults to 1.0.

            Boost values are relative to the default value of 1.0. A boost value
            between 0 and 1.0 decreases the relevance score. A value greater than
            1.0 increases the relevance score.

        :param default_operator: ``Optional[str]``
            Default boolean logic used to interpret text in the query string if no
            operators are specified. Valid values are:

                - ``OR`` (Default) For example, a query string of capital of Hungary
                  is interpreted as capital OR of OR Hungary.
                - ``AND`` For example, a query string of capital of Hungary is
                  interpreted as capital AND of AND Hungary.

        :param enable_position_increments: ``bool``
            If true, enable position increments in queries constructed from a
            query_string search. Defaults to true.

        :param fields: ``Optional[Sequence[str]]``
            Array of fields you wish to search.

            You can use this parameter query to search across multiple fields. See
            `Search multiple fields
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-multi-field>`__.

        :param fuzziness: ``Optional[str]``
            Maximum edit distance allowed for matching. See `Fuzziness
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#fuzziness>`__
            for valid values and more information.

        :param fuzzy_max_expansions: ``int``
            Maximum number of terms to which the query will expand. Defaults to 50.

        :param fuzzy_prefix_length: ``int``
            Number of beginning characters left unchanged for fuzzy matching.
            Defaults to 0.

        :param fuzzy_transpositions: ``bool``
            If true, edits for fuzzy matching include transpositions of two adjacent
            characters (ab → ba). Defaults to true.

        :param lenient: ``bool``
            If true, format-based errors, such as providing a text query value for a
            numeric field, are ignored. Defaults to false.

        :param max_determinized_states: ``int``
            Maximum number of `automaton states
            <https://en.wikipedia.org/wiki/Deterministic_finite_automaton>`__
            required for the query. Default is 10000.

            Elasticsearch uses Apache Lucene internally to parse regular
            expressions. Lucene converts each regular expression to a finite
            automaton containing a number of determinized states.

            You can use this parameter to prevent that conversion from
            unintentionally consuming too many resources. You may need to increase
            this limit to run complex regular expressions.

        :param minimum_should_match: ``Optional[str]``
            Minimum number of clauses that must match for a document to be returned.
            See the `minimum_should_match parameter
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-minimum-should-match.html>`__
            for valid values and more information.

            See `How minimum_should_match works
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-min-should-match>`__
            for an example.

        :param quote_analyzer: ``Optional[str]``
            `Analyzer
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html>`__
            used to convert quoted text in the query string into tokens. Defaults to
            the `search_quote_analyzer
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html#search-quote-analyzer>`__
            mapped for the default_field.

            For quoted text, this parameter overrides the analyzer specified in the
            analyzer parameter.

        :param phrase_slop: ``int``
            Maximum number of positions allowed between matching tokens for phrases.
            Defaults to 0. If 0, exact phrase matches are required. Transposed terms
            have a slop of 2.

        :param quote_field_suffix: ``Optional[str]``
            Suffix appended to quoted text in the query string.

            You can use this suffix to use a different analysis method for exact
            matches. See `Mixing exact search with stemming
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mixing-exact-search-with-stemming.html>`__.

        :param rewrite: ``Optional[str]``
            Method used to rewrite the query. For valid values and more information,
            see the `rewrite parameter
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-term-rewrite.html>`__.

        :param time_zone: ``Optional[str]``
            `Coordinated Universal Time (UTC) offset
            <https://en.wikipedia.org/wiki/List_of_UTC_time_offsets>`__ or `IANA
            time zone
            <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`__ used
            to convert date values in the query string to UTC.

            Valid values are ISO 8601 UTC offsets, such as ``+01:00`` or ``-08:00``,
            and IANA time zone IDs, such as ``America/Los_Angeles``.

            .. NOTE::

                The time_zone parameter does not affect the `date math
                <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math>`__
                value of now. now is always the current system time in UTC. However,
                the time_zone parameter does convert dates calculated using ``now``
                and `date math rounding
                <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math>`__.
                For example, the ``time_zone`` parameter will convert a value of
                ``now/d``.
        """
        super().__init__(
            query=query,
            default_field=default_field,
            allow_leading_wildcard=allow_leading_wildcard,
            analyze_wildcard=analyze_wildcard,
            analyzer=analyzer,
            auto_generate_synonyms_phrase_query=auto_generate_synonyms_phrase_query,
            boost=boost,
            default_operator=default_operator,
            enable_position_increments=enable_position_increments,
            fields=fields,
            fuzziness=fuzziness,
            fuzzy_max_expansions=fuzzy_max_expansions,
            fuzzy_prefix_length=fuzzy_prefix_length,
            fuzzy_transpositions=fuzzy_transpositions,
            lenient=lenient,
            max_determinized_states=max_determinized_states,
            minimum_should_match=minimum_should_match,
            quote_analyzer=quote_analyzer,
            phrase_slop=phrase_slop,
            quote_field_suffix=quote_field_suffix,
            rewrite=rewrite,
            time_zone=time_zone,
        )


class Range(Query):

    """
    Returns documents that contain terms within a provided range.

    When the <field> parameter is a date field data type, you can use date math
    with the ``gt``, ``gte``, ``lt`` and ``lte`` parameters. See `date math
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math>`__

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html>`__
    """

    name = 'range'
    _parameters = {'field': {'required': True, 'top_level': True}, 'gt': {}, 'gte': {}, 'lt': {}, 'lte': {}, 'format': {}, 'relation': {'default': 'INTERSECTS'}, 'time_zone': {}, 'boost': {}}
    _top_level_parameter = 'field'


    def __init__(
            self,
            field: str,
            gt: Optional[Union[str, int, float, date, datetime]] = None,
            gte: Optional[Union[str, int, float, date, datetime]] = None,
            lt: Optional[Union[str, int, float, date, datetime]] = None,
            lte: Optional[Union[str, int, float, date, datetime]] = None,
            format: Optional[str] = None,
            relation: str = 'INTERSECTS',
            time_zone: Optional[str] = None,
            boost: Optional[float] = None,
    ):
        """
        Returns documents that contain terms within a provided range.

        When the <field> parameter is a date field data type, you can use date math
        with the ``gt``, ``gte``, ``lt`` and ``lte`` parameters. See `date math
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math>`__

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html>`__

        :param field: ``str``
            Field you wish to search.

        :param gt: ``Optional[Union[str, int, float, date, datetime]]``
            Greater than.

        :param gte: ``Optional[Union[str, int, float, date, datetime]]``
            Greater than or equal to.

        :param lt: ``Optional[Union[str, int, float, date, datetime]]``
            Less than.

        :param lte: ``Optional[Union[str, int, float, date, datetime]]``
            Less than or equal to.

        :param format: ``Optional[str]``
            Date format used to convert date values in the query.

            By default, Elasticsearch uses the date format provided in the <field>`s
            mapping. This value overrides that mapping format.

            For valid syntax see `mapping data format
            <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html>`__

        :param relation: ``str``
            Indicates how the range query matches values for range fields. Valid
            values are:

                - ``INTERSECTS`` (Default) Matches documents with a range field
                  value that intersects the query’s range.
                - ``CONTAINS`` Matches documents with a range field value that
                  entirely contains the query’s range.
                - ``WITHIN`` Matches documents with a range field value entirely
                  within the query’s range.

        :param time_zone: ``Optional[str]``
            Coordinated Universal Time (UTC) offset or IANA time zone used to
            convert date values in the query to UTC.

            Valid values are ISO 8601 UTC offsets, such as ``+01:00`` or ``-08:00``,
            and IANA time zone IDs, such as ``America/Los_Angeles``.

        :param boost: ``Optional[float]``
            Floating point number used to decrease or increase the relevance scores
            of a query. Defaults to 1.0.

            You can use the boost parameter to adjust relevance scores for searches
            containing two or more queries.

            Boost values are relative to the default value of 1.0. A boost value
            between 0 and 1.0 decreases the relevance score. A value greater than
            1.0 increases the relevance score.
        """
        super().__init__(
            field=field,
            gt=gt,
            gte=gte,
            lt=lt,
            lte=lte,
            format=format,
            relation=relation,
            time_zone=time_zone,
            boost=boost,
        )


class Term(Query):

    """
    Returns documents that contain an exact term in a provided field.

    You can use the term query to find documents based on a precise value such
    as a price, a product ID, or a username.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html>`__
    """

    name = 'term'
    _parameters = {'field': {'required': True, 'top_level': True}, 'value': {'required': True}, 'boost': {}, 'case_insensitive': {}}
    _top_level_parameter = 'field'


    def __init__(
            self,
            field: str,
            value: Union[str, int, float, bool, datetime],
            boost: Optional[float] = None,
            case_insensitive: Optional[bool] = None,
    ):
        """
        Returns documents that contain an exact term in a provided field.

        You can use the term query to find documents based on a precise value such
        as a price, a product ID, or a username.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html>`__

        :param field: ``str``
            Field you wish to search.

        :param value: ``Union[str, int, float, bool, datetime]``
            Term you wish to find in the provided <field>. To return a document, the
            term must exactly match the field value, including whitespace and
            capitalization.

        :param boost: ``Optional[float]``
            Floating point number used to decrease or increase the relevance scores
            of a query. Defaults to 1.0.

            You can use the boost parameter to adjust relevance scores for searches
            containing two or more queries.

            Boost values are relative to the default value of 1.0. A boost value
            between 0 and 1.0 decreases the relevance score. A value greater than
            1.0 increases the relevance score.

        :param case_insensitive: ``Optional[bool]``
            Allows ASCII case insensitive matching of the value with the indexed
            field values when set to true. Default is false which means the case
            sensitivity of matching depends on the underlying field’s mapping.
        """
        super().__init__(
            field=field,
            value=value,
            boost=boost,
            case_insensitive=case_insensitive,
        )


class _Terms(Query, factory=False):

    """
    Returns documents that contain one or more exact terms in a provided field.

    The terms query is the same as the term query, except you can search for
    multiple values.

    `elasticsearch documentation
    <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-terms-query.html>`__
    """

    name = 'terms'
    _parameters = {'field': {'required': True, 'top_level': True}, 'value': {'required': True}, 'boost': {}}
    _top_level_parameter = 'field'


    def __init__(
            self,
            field: str,
            value: Sequence[Union[str, int, float, bool, datetime]],
            boost: Optional[float] = None,
    ):
        """
        Returns documents that contain one or more exact terms in a provided field.

        The terms query is the same as the term query, except you can search for
        multiple values.

        `elasticsearch documentation
        <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-terms-query.html>`__

        :param field: ``str``
            Field you wish to search.

        :param value: ``Sequence[Union[str, int, float, bool, datetime]]``
            The value of this parameter is an array of terms you wish to find in the
            provided field. To return a document, one or more terms must exactly
            match a field value, including whitespace and capitalization.

            By default, Elasticsearch limits the terms query to a maximum of 65,536
            terms. You can change this limit using the index.max_terms_count
            setting.

        :param boost: ``Optional[float]``
            Floating point number used to decrease or increase the relevance scores
            of a query. Defaults to 1.0.

            You can use the boost parameter to adjust relevance scores for searches
            containing two or more queries.

            Boost values are relative to the default value of 1.0. A boost value
            between 0 and 1.0 decreases the relevance score. A value greater than
            1.0 increases the relevance score.
        """
        super().__init__(
            field=field,
            value=value,
            boost=boost,
        )

