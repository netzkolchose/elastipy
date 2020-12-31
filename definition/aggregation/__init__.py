from .metric import METRIC
from .bucket import BUCKET

# TODO: add aggregations and pipelines
AGGREGATION_DEFINITION = {
    **{
        key: {**value, "type": "metric"}
        for key, value in METRIC.items()
    },
    **{
        key: {**value, "type": "agg"}
        for key, value in BUCKET.items()
    },
}
