from flask_cors import CORS
from order_manager.supports.encoder import MongodbJSONEncoder
from order_manager.supports.decoder import MongodbJSONDecoder


def init_app(app):
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.json_encoder = MongodbJSONEncoder
    app.json_decoder = MongodbJSONDecoder
