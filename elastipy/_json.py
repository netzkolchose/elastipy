import json
import datetime

try:
    import numpy as _numpy
except ImportError:
    _numpy = None


class BodyJsonEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            return super().default(o)
        except TypeError:
            if isinstance(o, (datetime.datetime, datetime.date)):
                return o.isoformat()

            elif _numpy is not None and isinstance(o, _numpy.ndarray):
                return o.tolist()

            elif getattr(o, "to_dict", None):  # pragma: no cover (it's actually run but not reported)
                return o.to_dict()

            else:
                raise


def make_json_compatible(o):
    return json.loads(json.dumps(o, cls=BodyJsonEncoder))
