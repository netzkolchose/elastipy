import json
import datetime


class BodyJsonEncoder(json.JSONEncoder):

    def default(self, o):
        from .query import Query
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        if isinstance(o, Query):
            return o.to_dict()
        return o


def make_json_compatible(o):
    return json.loads(json.dumps(o, cls=BodyJsonEncoder))
