# auto-generated file - do not edit
from datetime import date, datetime
from typing import Mapping, Sequence, Any, Union, Optional

from .query import Query, QueryInterface


__all__ = (
    "_Bool", "Match", "_MatchAll", "_MatchNone", "QueryString", "Range", "Term",
    "_Terms"
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

