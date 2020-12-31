
DEFINITIONS = {
    "bool": {
        "auto_generate": False,
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html",
        "doc": """
            A query that matches documents matching boolean combinations of other queries. The bool query maps to Lucene BooleanQuery. It is built using one or more boolean clauses, each clause with a typed occurrence.

            The bool query takes a more-matches-is-better approach, so the score from each matching must or should clause will be added together to provide the final _score for each document.
        """,
        "parameters": {
            "must": {
                "type": "List[QueryInterface]",
                "doc": """
                    The clause (query) must appear in matching documents and will contribute to the score.
                """,
            },
            "must_not": {
                "type": "List[QueryInterface]",
                "doc": """
                    The clause (query) must not appear in the matching documents. Clauses are executed in filter context meaning that scoring is ignored and clauses are considered for caching. Because scoring is ignored, a score of 0 for all documents is returned.
                """,
            },
            "should": {
                "type": "List[QueryInterface]",
                "doc": """
                    The clause (query) should appear in the matching document.
                """,
            },
            "filter": {
                "type": "List[QueryInterface]",
                "doc": """
                    The clause (query) must appear in matching documents. However unlike must the score of the query will be ignored. Filter clauses are executed in filter context, meaning that scoring is ignored and clauses are considered for caching.
                """,
            },

        }
    },

    "term": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html",
        "doc": """
            Returns documents that contain an exact term in a provided field.

            You can use the term query to find documents based on a precise value such as a price, a product ID, or a username.
        """,
        "parameters": {
            "field": {
                "type": str, "required": True, "top_level": True,
                "doc": "Field you wish to search."
            },
            "value": {
                "type": str, "required": True,
                "doc": """
                    Term you wish to find in the provided <field>. To return a document, the term must exactly match the field value, including whitespace and capitalization.
                """,
            },
            "boost": {
                "type": float,
                "doc": """
                    Floating point number used to decrease or increase the relevance scores of a query. Defaults to 1.0.
    
                    You can use the boost parameter to adjust relevance scores for searches containing two or more queries.
    
                    Boost values are relative to the default value of 1.0. A boost value between 0 and 1.0 decreases the relevance score. A value greater than 1.0 increases the relevance score.
                """
            },
            "case_insensitive": {
                "type": bool,
                "doc": "allows ASCII case insensitive matching of the value with the indexed field values when set to true. Default is false which means the case sensitivity of matching depends on the underlying field’s mapping."
            }
        }
    },

    "terms": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-terms-query.html",
        "doc": """
            Returns documents that contain one or more exact terms in a provided field.

            The terms query is the same as the term query, except you can search for multiple values.
        """,
        "parameters": {
            "field": {
                "type": str, "required": True, "top_level": True,
                "doc": """
                    Field you wish to search.
                """,
            },
            "value": {
                "type": str, "required": True,
                "doc": """
                    The value of this parameter is an array of terms you wish to find in the provided field. To return a document, one or more terms must exactly match a field value, including whitespace and capitalization.

                    By default, Elasticsearch limits the terms query to a maximum of 65,536 terms. You can change this limit using the index.max_terms_count setting.
                """
            },
            "boost": {
                "type": float,
                "doc": """
                    Floating point number used to decrease or increase the relevance scores of a query. Defaults to 1.0.
    
                    You can use the boost parameter to adjust relevance scores for searches containing two or more queries.
    
                    Boost values are relative to the default value of 1.0. A boost value between 0 and 1.0 decreases the relevance score. A value greater than 1.0 increases the relevance score.
                """
            },
        }
    },

    "match_all": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html",
        "doc": """
            The most simple query, which matches all documents, giving them all a _score of 1.0.
            
            The _score can be changed with the boost parameter
        """,
        "parameters": {
            "boost": {
                "type": float,
                "doc": "The _score can be changed with the boost parameter"
            }
        }
    },

    "match_none": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html",
        "doc": """
            This is the inverse of the match_all query, which matches no documents.
        """,
        "parameters": {}
    },

    "match": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html",
        "doc": """
            Returns documents that match a provided text, number, date or boolean value. The provided text is analyzed before matching.

            The match query is the standard query for performing a full-text search, including options for fuzzy matching.
        """,
        "parameters": {
            "field": {
                "type": str, "required": True, "top_level": True,
                "doc": """
                    Field you wish to search.
                """,
            },
            "query": {
                "type": str, "required": True,
                "doc": """
                    Text, number, boolean value or date you wish to find in the provided <field>.

                    The match query analyzes any provided text before performing a search. This means the match query can search text fields for analyzed tokens rather than an exact term.
                """
            },
            "auto_generate_synonyms_phrase_query": {
                "type": bool, "default": True,
                "doc": """
                     If true, match phrase queries are automatically created for multi-term synonyms. Defaults to true.
                """
            },
            "fuzziness": {
                "type": str,
                "doc": """
                    Maximum edit distance allowed for matching. See Fuzziness for valid values and more information. See Fuzziness in the match query for an example.
                """
            },
            "max_expansions": {
                "type": int, "default": 50,
                "doc": """
                    Maximum number of terms to which the query will expand. Defaults to 50. 
                """
            },
            "prefix_length": {
                "type": int, "default": 0,
                "doc": """
                    Number of beginning characters left unchanged for fuzzy matching. Defaults to 0. 
                """
            },
            "fuzzy_transpositions": {
                "type": bool, "default": True,
                "doc": """
                    If true, edits for fuzzy matching include transpositions of two adjacent characters (ab → ba). Defaults to true.
                """
            },
            "fuzzy_rewrite": {
                "type": str,
                "doc": """
                    Method used to rewrite the query. See the rewrite parameter for valid values and more information.

                    If the fuzziness parameter is not 0, the match query uses a fuzzy_rewrite method of top_terms_blended_freqs_${max_expansions} by default.
                """
            },
            "lenient": {
                "type": bool, "default": False,
                "doc": """
                     If true, format-based errors, such as providing a text query value for a numeric field, are ignored. Defaults to false. 
                """
            },
            "operator": {
                "type": str,
                "doc": """
                    Boolean logic used to interpret text in the query value. Valid values are:
                        OR (Default)
                            For example, a query value of capital of Hungary is interpreted as capital OR of OR Hungary. 
                        AND
                            For example, a query value of capital of Hungary is interpreted as capital AND of AND Hungary. 
                """
            },
            "minimum_should_match": {
                "type": str,
                "doc": """
                    Minimum number of clauses that must match for a document to be returned. See the minimum_should_match parameter for valid values and more information.
                """
            },
            "zero_terms_query": {
                "type": str, "default": "none",
                "doc": """
                    Indicates whether no documents are returned if the analyzer removes all tokens, such as when using a stop filter. Valid values are:
                        none (Default)
                            No documents are returned if the analyzer removes all tokens.
                        all
                            Returns all documents, similar to a match_all query. 
                """
            },
        }
    },

}