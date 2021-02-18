import os
from flask_pymongo import PyMongo

db = PyMongo()


def init_app(app):
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    db.init_app(app)
