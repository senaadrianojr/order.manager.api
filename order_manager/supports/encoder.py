from flask import json
from bson import ObjectId
from datetime import datetime
from order_manager.supports import dateutils


class MongodbJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(dateutils.fix_timezone(o))
        return json.JSONEncoder.default(self, o)
