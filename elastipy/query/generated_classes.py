# auto-generated file - do not edit
from typing import Mapping, Sequence, Any, Union, Optional


from .query import Query, QueryInterface


class _Bool(Query, factory=False):

    """
    A query that matches documents matching boolean combinations of other
    queries. The bool query maps to Lucene BooleanQuery. It is built using one
    or more boolean clauses, each clause with a typed occurrence.

    The bool query takes a more-matches-is-better approach, so the score from
    each matching must or should clause will be added together to provide the
    final _score for each document.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html
    """

    name = 'bool'
    _optional_parameters = {'must': None, 'must_not': None, 'should': None, 'filter': None}


    def __init__(
            self,
            must: Optional[Sequence['QueryInterface']] = None,
            must_not: Optional[Sequence['QueryInterface']] = None,
            should: Optional[Sequence['QueryInterface']] = None,
            filter: Optional[Sequence['QueryInterface']] = None,
    ):
        """
        A query that matches documents matching boolean combinations of other
        queries. The bool query maps to Lucene BooleanQuery. It is built using one
        or more boolean clauses, each clause with a typed occurrence.

        The bool query takes a more-matches-is-better approach, so the score from
        each matching must or should clause will be added together to provide the
        final _score for each document.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html

        :param must: Optional[Sequence['QueryInterface']]
            The clause (query) must appear in matching documents and will contribute
            to the score.

        :param must_not: Optional[Sequence['QueryInterface']]
            The clause (query) must not appear in the matching documents. Clauses
            are executed in filter context meaning that scoring is ignored and
            clauses are considered for caching. Because scoring is ignored, a score
            of 0 for all documents is returned.

        :param should: Optional[Sequence['QueryInterface']]
            The clause (query) should appear in the matching document.

        :param filter: Optional[Sequence['QueryInterface']]
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

    https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html
    """

    name = 'match'
    _optional_parameters = {'auto_generate_synonyms_phrase_query': True, 'fuzziness': None, 'max_expansions': 50, 'prefix_length': 0, 'fuzzy_transpositions': True, 'fuzzy_rewrite': None, 'lenient': False, 'operator': None, 'minimum_should_match': None, 'zero_terms_query': 'none'}
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

        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html

        :param field: str
            Field you wish to search.

        :param query: Union[str, int, float, bool]
            Text, number, boolean value or date you wish to find in the provided
            <field>.

            The match query analyzes any provided text before performing a search.
            This means the match query can search text fields for analyzed tokens
            rather than an exact term.

        :param auto_generate_synonyms_phrase_query: bool
            If true, match phrase queries are automatically created for multi-term
            synonyms. Defaults to true.

        :param fuzziness: Optional[str]
            Maximum edit distance allowed for matching. See Fuzziness for valid
            values and more information. See Fuzziness in the match query for an
            example.

        :param max_expansions: int
            Maximum number of terms to which the query will expand. Defaults to 50. 

        :param prefix_length: int
            Number of beginning characters left unchanged for fuzzy matching.
            Defaults to 0. 

        :param fuzzy_transpositions: bool
            If true, edits for fuzzy matching include transpositions of two adjacent
            characters (ab → ba). Defaults to true.

        :param fuzzy_rewrite: Optional[str]
            Method used to rewrite the query. See the rewrite parameter for valid
            values and more information.

            If the fuzziness parameter is not 0, the match query uses a
            fuzzy_rewrite method of top_terms_blended_freqs_${max_expansions} by
            default.

        :param lenient: bool
            If true, format-based errors, such as providing a text query value for a
            numeric field, are ignored. Defaults to false. 

        :param operator: Optional[str]
            Boolean logic used to interpret text in the query value. Valid values
            are:
                OR (Default)
                    For example, a query value of capital of Hungary is interpreted
                    as capital OR of OR Hungary. 
                AND
                    For example, a query value of capital of Hungary is interpreted
                    as capital AND of AND Hungary. 

        :param minimum_should_match: Optional[str]
            Minimum number of clauses that must match for a document to be returned.
            See the minimum_should_match parameter for valid values and more
            information.

        :param zero_terms_query: str
            Indicates whether no documents are returned if the analyzer removes all
            tokens, such as when using a stop filter. Valid values are:
                none (Default)
                    No documents are returned if the analyzer removes all tokens.
                all
                    Returns all documents, similar to a match_all query. 
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


class MatchAll(Query):

    """
    The most simple query, which matches all documents, giving them all a _score
    of 1.0.

    The _score can be changed with the boost parameter

    https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html
    """

    name = 'match_all'
    _optional_parameters = {'boost': None}


    def __init__(
            self,
            boost: Optional[float] = None,
    ):
        """
        The most simple query, which matches all documents, giving them all a _score
        of 1.0.

        The _score can be changed with the boost parameter

        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html

        :param boost: Optional[float]
            The _score can be changed with the boost parameter
        """
        super().__init__(
            boost=boost,
        )


class MatchNone(Query):

    """
    This is the inverse of the match_all query, which matches no documents.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html
    """

    name = 'match_none'
    _optional_parameters = {}


    def __init__(
            self,
    ):
        """
        This is the inverse of the match_all query, which matches no documents.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html
        """
        super().__init__(
        )


class Term(Query):

    """
    Returns documents that contain an exact term in a provided field.

    You can use the term query to find documents based on a precise value such
    as a price, a product ID, or a username.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html
    """

    name = 'term'
    _optional_parameters = {'boost': None, 'case_insensitive': None}
    _top_level_parameter = 'field'


    def __init__(
            self,
            field: str,
            value: str,
            boost: Optional[float] = None,
            case_insensitive: Optional[bool] = None,
    ):
        """
        Returns documents that contain an exact term in a provided field.

        You can use the term query to find documents based on a precise value such
        as a price, a product ID, or a username.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html

        :param field: str
            Field you wish to search.

        :param value: str
            Term you wish to find in the provided <field>. To return a document, the
            term must exactly match the field value, including whitespace and
            capitalization.

        :param boost: Optional[float]
            Floating point number used to decrease or increase the relevance scores
            of a query. Defaults to 1.0.

            You can use the boost parameter to adjust relevance scores for searches
            containing two or more queries.

            Boost values are relative to the default value of 1.0. A boost value
            between 0 and 1.0 decreases the relevance score. A value greater than
            1.0 increases the relevance score.

        :param case_insensitive: Optional[bool]
            allows ASCII case insensitive matching of the value with the indexed
            field values when set to true. Default is false which means the case
            sensitivity of matching depends on the underlying field’s mapping.
        """
        super().__init__(
            field=field,
            value=value,
            boost=boost,
            case_insensitive=case_insensitive,
        )


class Terms(Query):

    """
    Returns documents that contain one or more exact terms in a provided field.

    The terms query is the same as the term query, except you can search for
    multiple values.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-terms-query.html
    """

    name = 'terms'
    _optional_parameters = {'boost': None}
    _top_level_parameter = 'field'


    def __init__(
            self,
            field: str,
            value: Sequence[str],
            boost: Optional[float] = None,
    ):
        """
        Returns documents that contain one or more exact terms in a provided field.

        The terms query is the same as the term query, except you can search for
        multiple values.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-terms-query.html

        :param field: str
            Field you wish to search.

        :param value: Sequence[str]
            The value of this parameter is an array of terms you wish to find in the
            provided field. To return a document, one or more terms must exactly
            match a field value, including whitespace and capitalization.

            By default, Elasticsearch limits the terms query to a maximum of 65,536
            terms. You can change this limit using the index.max_terms_count
            setting.

        :param boost: Optional[float]
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

