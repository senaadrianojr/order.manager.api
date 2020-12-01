from flask import json
from bson import ObjectId
import re

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)


class MongodbJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.object_id_hook, **kwargs)

    def object_id_hook(self, dct):
        if "_id" in dct:
            dct['_id'] = ObjectId(oid=dct['_id'])
        return dct
