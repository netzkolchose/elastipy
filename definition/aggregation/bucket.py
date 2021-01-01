# TODO: composite aggregation allows sub-aggregations as 'sources' list, not as nested 'aggs'
#   https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-composite-aggregation.html

# TODO: adjacency_matrix allows sub-aggregations as 'filters'
#   https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-adjacency-matrix-aggregation.html

BUCKET = {
    "date_histogram": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html",
        "doc": """
            This multi-bucket aggregation is similar to the normal histogram, but it can only be used with date or date range values. Because dates are represented internally in Elasticsearch as long values, it is possible, but not as accurate, to use the normal histogram on dates as well. The main difference in the two APIs is that here the interval can be specified using date/time expressions. Time-based data requires special support because time-based intervals are not always a fixed length.
        """,
        "parameters": {
            "field": {"type": str, "required": True},
            "calendar_interval": {
                "type": str,
                "doc": """
                    Calendar-aware intervals are configured with the calendar_interval parameter. You can specify calendar intervals using the unit name, such as month, or as a single unit quantity, such as 1M. For example, day and 1d are equivalent. Multiple quantities, such as 2d, are not supported.
                """
            },
            "fixed_interval": {
                "type": str,
                "doc": """
                    In contrast to calendar-aware intervals, fixed intervals are a fixed number of SI units and never deviate, regardless of where they fall on the calendar. One second is always composed of 1000ms. This allows fixed intervals to be specified in any multiple of the supported units.

                    However, it means fixed intervals cannot express other units such as months, since the duration of a month is not a fixed quantity. Attempting to specify a calendar interval like month or quarter will throw an exception.
                """
            },
            "min_doc_count": {
                "type": int, "default": 1,
                "doc": """
                    Minimum documents to required for a bucket. Set to 0 to allow creating empty buckets.  
                """,
            },
            "offset": {
                "type": str,
                "doc": """
                    Use the offset parameter to change the start value of each bucket by the specified positive (+) or negative offset (-) duration, such as 1h for an hour, or 1d for a day. See Time units for more possible time duration options.

                    For example, when using an interval of day, each bucket runs from midnight to midnight. Setting the offset parameter to +6h changes each bucket to run from 6am to 6am
                """
            },
            "time_zone": {
                "type": str,
                "doc": """
                    Elasticsearch stores date-times in Coordinated Universal Time (UTC). By default, all bucketing and rounding is also done in UTC. Use the time_zone parameter to indicate that bucketing should use a different time zone.

                    For example, if the interval is a calendar day and the time zone is America/New_York then 2020-01-03T01:00:01Z is : # Converted to 2020-01-02T18:00:01 # Rounded down to 2020-01-02T00:00:00 # Then converted back to UTC to produce 2020-01-02T05:00:00:00Z # Finally, when the bucket is turned into a string key it is printed in America/New_York so it’ll display as "2020-01-02T00:00:00"
                    
                    It looks like: bucket_key = localToUtc(Math.floor(utcToLocal(value) / interval) * interval))

                    You can specify time zones as an ISO 8601 UTC offset (e.g. +01:00 or -08:00) or as an IANA time zone ID, such as America/Los_Angeles.
                """
            },
            "format": {
                "type": str,
                "doc": """
                    Specifies the format of the 'key_as_string' response.
                    See: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html
                """
            },
            # TODO: This would break the current Aggregation.keys/values logic
            "keyed": {
                "type": bool, "default": False,
                "doc": """
                    Setting the keyed flag to true associates a unique string key with each bucket and returns the ranges as a hash rather than an array.
                """
            },
            "missing": {"type": "any", "doc": """The missing parameter defines how documents that are missing a value should be treated. By default they will be ignored but it is also possible to treat them as if they had a value."""},
            "script": {"type": dict, "doc": """Generating the terms using a script"""},
        }
    },

    "auto_date_histogram": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-autodatehistogram-aggregation.html",
        "doc": """
            A multi-bucket aggregation similar to the Date histogram except instead of providing an interval to use as the width of each bucket, a target number of buckets is provided indicating the number of buckets needed and the interval of the buckets is automatically chosen to best achieve that target. The number of buckets returned will always be less than or equal to this target number.

            The buckets field is optional, and will default to 10 buckets if not specified.
        """,
        "parameters": {
            "field": {"type": str, "required": True},
            "buckets": {
                "type": int, "default": 10,
                "doc": """
                    The number of buckets that are to be returned.
                """
            },
            "minimum_interval": {
                "type": str,
                "doc": """
                    The minimum_interval allows the caller to specify the minimum rounding interval that should be used. This can make the collection process more efficient, as the aggregation will not attempt to round at any interval lower than minimum_interval.

                    The accepted units for minimum_interval are:
                        year, month, day, hour, minute, second
                """
            },
            "time_zone": {
                "type": str,
                "doc": """
                    Elasticsearch stores date-times in Coordinated Universal Time (UTC). By default, all bucketing and rounding is also done in UTC. Use the time_zone parameter to indicate that bucketing should use a different time zone.

                    For example, if the interval is a calendar day and the time zone is America/New_York then 2020-01-03T01:00:01Z is : # Converted to 2020-01-02T18:00:01 # Rounded down to 2020-01-02T00:00:00 # Then converted back to UTC to produce 2020-01-02T05:00:00:00Z # Finally, when the bucket is turned into a string key it is printed in America/New_York so it’ll display as "2020-01-02T00:00:00"
                    
                    It looks like: bucket_key = localToUtc(Math.floor(utcToLocal(value) / interval) * interval))

                    You can specify time zones as an ISO 8601 UTC offset (e.g. +01:00 or -08:00) or as an IANA time zone ID, such as America/Los_Angeles.
                """
            },
            "format": {
                "type": str,
                "doc": """
                    Specifies the format of the 'key_as_string' response.
                    See: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html
                """
            },
            # TODO: This would break the current Aggregation.keys/values logic
            "keyed": {
                "type": bool, "default": False,
                "doc": """
                    Setting the keyed flag to true associates a unique string key with each bucket and returns the ranges as a hash rather than an array.
                """
            },
            "missing": {"type": "any", "doc": """The missing parameter defines how documents that are missing a value should be treated. By default they will be ignored but it is also possible to treat them as if they had a value."""},
            "script": {"type": dict, "doc": """Generating the terms using a script"""},
        }
    },

    "filter": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filter-aggregation.html",
        "doc": """
            Defines a single bucket of all the documents in the current document set context that match a specified filter. Often this will be used to narrow down the current aggregation context to a specific set of documents.
        """,
        "parameters": {
            "filter": {"type": "'QueryInterface'", "required": True},
        },
    },

    "filters": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filters-aggregation.html",
        "doc": """
            Defines a multi bucket aggregation where each bucket is associated with a filter. Each bucket will collect all documents that match its associated filter.
        """,
        "parameters": {
            "filters": {"type": "Mapping[str, 'QueryInterface']", "required": True},
        },
    },

    "terms": {
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html",
        "doc": """
            A multi-bucket value source based aggregation where buckets are dynamically built - one per unique value.
        """,
        "parameters": {
            "field": {"type": str, "required": True},
            "size": {
                "type": int, "default": 10,
                "doc": """
                    The size parameter can be set to define how many term buckets should be returned out of the overall terms list. By default, the node coordinating the search process will request each shard to provide its own top size term buckets and once all shards respond, it will reduce the results to the final list that will then be returned to the client. This means that if the number of unique terms is greater than size, the returned list is slightly off and not accurate (it could be that the term counts are slightly off and it could even be that a term that should have been in the top size buckets was not returned).
                """,
            },
            "shard_size": {
                "type": int,
                "doc": """
                    The higher the requested size is, the more accurate the results will be, but also, the more expensive it will be to compute the final results (both due to bigger priority queues that are managed on a shard level and due to bigger data transfers between the nodes and the client).

                    The shard_size parameter can be used to minimize the extra work that comes with bigger requested size. When defined, it will determine how many terms the coordinating node will request from each shard. Once all the shards responded, the coordinating node will then reduce them to a final result which will be based on the size parameter - this way, one can increase the accuracy of the returned terms and avoid the overhead of streaming a big list of buckets back to the client.
                """,
            },
            "show_term_doc_count_error": {
                "type": bool,
                "doc": """
                    This shows an error value for each term returned by the aggregation which represents the worst case error in the document count and can be useful when deciding on a value for the shard_size parameter. This is calculated by summing the document counts for the last term returned by all shards which did not return the term.

                    These errors can only be calculated in this way when the terms are ordered by descending document count. When the aggregation is ordered by the terms values themselves (either ascending or descending) there is no error in the document count since if a shard does not return a particular term which appears in the results from another shard, it must not have that term in its index. When the aggregation is either sorted by a sub aggregation or in order of ascending document count, the error in the document counts cannot be determined and is given a value of -1 to indicate this.
                """,
            },
            "order": {
                "type": dict,
                "doc": """
                    The order of the buckets can be customized by setting the order parameter. By default, the buckets are ordered by their doc_count descending.
                    
                    Warning: Sorting by ascending _count or by sub aggregation is discouraged as it increases the error on document counts. It is fine when a single shard is queried, or when the field that is being aggregated was used as a routing key at index time: in these cases results will be accurate since shards have disjoint values. However otherwise, errors are unbounded. One particular case that could still be useful is sorting by min or max aggregation: counts will not be accurate but at least the top buckets will be correctly picked.
                """,
            },
            "min_doc_count": {
                "type": int, "default": 1,
                "doc": """
                    It is possible to only return terms that match more than a configured number of hits using the min_doc_count option. Default value is 1.

                    Terms are collected and ordered on a shard level and merged with the terms collected from other shards in a second step. However, the shard does not have the information about the global document count available. The decision if a term is added to a candidate list depends only on the order computed on the shard using local shard frequencies. The min_doc_count criterion is only applied after merging local terms statistics of all shards. In a way the decision to add the term as a candidate is made without being very certain about if the term will actually reach the required min_doc_count. This might cause many (globally) high frequent terms to be missing in the final result if low frequent terms populated the candidate lists. To avoid this, the shard_size parameter can be increased to allow more candidate terms on the shards. However, this increases memory consumption and network traffic.
                """,
            },
            "shard_min_doc_count": {
                "type": int,
                "doc": """
                    The parameter shard_min_doc_count regulates the certainty a shard has if the term should actually be added to the candidate list or not with respect to the min_doc_count. Terms will only be considered if their local shard frequency within the set is higher than the shard_min_doc_count. If your dictionary contains many low frequent terms and you are not interested in those (for example misspellings), then you can set the shard_min_doc_count parameter to filter out candidate terms on a shard level that will with a reasonable certainty not reach the required min_doc_count even after merging the local counts. shard_min_doc_count is set to 0 per default and has no effect unless you explicitly set it.
                    
                    Note: Setting min_doc_count=0 will also return buckets for terms that didn’t match any hit. However, some of the returned terms which have a document count of zero might only belong to deleted documents or documents from other types, so there is no warranty that a match_all query would find a positive document count for those terms.
                    
                    Warning: When NOT sorting on doc_count descending, high values of min_doc_count may return a number of buckets which is less than size because not enough data was gathered from the shards. Missing buckets can be back by increasing shard_size. Setting shard_min_doc_count too high will cause terms to be filtered out on a shard level. This value should be set much lower than min_doc_count/#shards.
                """,
            },
            "missing": {"type": "any", "doc": """The missing parameter defines how documents that are missing a value should be treated. By default they will be ignored but it is also possible to treat them as if they had a value."""},
            "script": {"type": dict, "doc": """Generating the terms using a script"""},
        },
        "returns": ["value"],
    },
}
