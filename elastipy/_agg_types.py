# TODO: add aggregations and pipelines
AGGREGATIONS = {
    "metric": {
        "avg": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-avg-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "missing": {"type": "any"},
                "script": {"type": dict},
            },
            "returns": {"value"},
        },
        "boxplot": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-boxplot-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "compression": {"type": int, "default": 100},
                "missing": {"type": "any"},
            },
            "returns": ["min", "max", "q1", "q2", "q3"],
        },
        "cardinality": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-cardinality-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "precision_threshold": {"type": int, "default": 3000},
                "missing": {"type": "any"},
                "script": {"type": dict},
            },
            "returns": ["value"],
        },
        "extended_stats": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-extendedstats-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "sigma": {"type": float, "default": 3.},
                "missing": {"type": "any"},
                "script": {"type": dict},
            },
            "returns": [
                "count", "min", "max", "avg", "sum", "sum_of_squares",
                "variance", "variance_population", "variance_sampling",
                "std_deviation", "std_deviation_population", "std_deviation_sampling", "std_deviation_bounds"
            ],
        },
        "geo_bounds": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geobounds-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "wrap_longitude": {"type": bool, "default": True},
            },
            "returns": ["top_left", "bottom_right"],
        },
        "geo_centroid": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geocentroid-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
            },
            "returns": ["location"],
        },
        "matrix_stats": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-matrix-stats-aggregation.html",
            "parameters": {
                "fields": {"type": list, "required": True},
                "mode": {"type": str, "default": "avg"},
                "missing": {"type": "any"},
            },
            "returns": ["fields"],
        },
        "max": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-max-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "missing": {"type": "any"},
                "script": {"type": dict},
            },
            "returns": {"value"},
        },
        "median_absolute_deviation": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-median-absolute-deviation-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "compression": {"type": int, "default": 1000},
                "missing": {"type": "any"},
                "script": {"type": dict},
            },
            "returns": {"value"},
        },
        "min": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-min-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "missing": {"type": "any"},
                "script": {"type": dict},
            },
            "returns": {"value"},
        },
        "percentile_ranks": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-rank-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "values": {"type": list, "required": True},
                "keyed": {"type": bool, "default": True},
                "hdr.number_of_significant_value_digits": {"type": int},
                "missing": {"type": "any"},
                "script": {"type": dict},
            },
            "returns": {"values"},
        },
        "percentiles": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "percents": {"type": list, "default": [1, 5, 25, 50, 75, 95, 99]},
                "keyed": {"type": bool, "default": True},
                "tdigest.compression": {"type": int, "default": 100},
                "hdr.number_of_significant_value_digits": {"type": int},
                "missing": {"type": "any"},
                "script": {"type": dict},
            },
            "returns": {"values"},
        },
        "rate": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-rate-aggregation.html",
            "parameters": {
                "unit": {"type": str, "required": True},
                "field": {"type": str},
                "script": {"type": dict},
            },
            "returns": {"value"},
        },
        "scripted_metric": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-scripted-metric-aggregation.html",
            "parameters": {
                "init_script": {"type": str},
                "map_script": {"type": str, "required": True},
                "combine_script": {"type": str, "required": True},
                "reduce_script": {"type": str, "required": True},
                "params": {"type": dict},
            },
            "returns": {"value"},
        },
        "stats": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-stats-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "missing": {"type": "any"},
            },
            "returns": ["count", "min", "max", "sum", "count", "average"],
        },
        "string_stats": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-string-stats-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "show_distribution": {"type": bool, "default": False},
                "missing": {"type": "any"},
            },
            "returns": ["count", "min_length", "max_length", "avg_length", "entropy", "distribution"],
        },
        "sum": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-sum-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "missing": {"type": "any"},
                "script": {"type": dict},
            },
            "returns": {"value"},
        },
        "t_test": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-ttest-aggregation.html",
            "parameters": {
                "a.field": {"type": str, "required": True},
                "b.field": {"type": str, "required": True},
                "a.filter": {"type": dict},
                "b.filter": {"type": dict},
                "type": {"type": str, "required": True},
                "script": {"type": dict},
            },
            "returns": {"value"},
        },
        "top_hits": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-top-hits-aggregation.html",
            "parameters": {
                # TODO: quite incomplete
                "size": {"type": int, "required": True},
                "sort": {"type": dict},
                "_source": {"type": dict},
            },
            "returns": {"hits"},
        },
        "top_metrics": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-top-metrics.html",
            "parameters": {
                "metrics": {"type": dict, "required": True},
                "sort": {"type": dict},
            },
            "returns": {"top"},
        },
        "value_count": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-valuecount-aggregation.html",
            "parameters": {
                "field": {"type": str, "required": True},
                "script": {"type": dict},
            },
            "returns": {"value"},
        },
        "weighted_avg": {
            "doc": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-weight-avg-aggregation.html",
            "parameters": {
                "value.field": {"type": str, "required": True},
                "value.missing": {"type": "any"},
                "weight.field": {"type": str, "required": True},
                "weight.missing": {"type": "any"},
                "format": {"type": str},
                "value_type": {"type": str},
                "script": {"type": dict},
            },
            "returns": {"value"},
        },
    }
}
