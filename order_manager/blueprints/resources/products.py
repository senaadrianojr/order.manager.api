from bson import ObjectId
from flask import request, abort
from order_manager.supports import dateutils
from order_manager.extensions.database import db

default_zone = 'America/Sao_Paulo'


def init_app(app):
    mongo = db

    @app.route('/products', methods=['GET'])
    def get_products():
        result = list(mongo.db.products.find({}))
        response = {"content": result}
        return response, 200

    @app.route('/products', methods=['POST'])
    def create_products():
        new_product = request.json
        mongo.db.products.insert_one(new_product)
        response = {'created_id': new_product.get('_id')}
        return response, 201

    @app.route('/products/<product_id>', methods=['PUT'])
    def update_products(product_id):
        product_founded = mongo.db.products.find_one({'_id': ObjectId(oid=product_id)}) or abort(404)
        new_product = request.json
        updated_product = {**product_founded,
                           **new_product,
                           'created_at': product_founded.get('created_at'),
                           'last_update': dateutils.current_zoned_datetime(default_zone)}

        mongo.db.products.replace_one({'_id': ObjectId(oid=product_id)}, updated_product)
        return {}, 203
