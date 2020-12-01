from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from supports.encoder import MongodbJSONEncoder
from supports.decoder import MongodbJSONDecoder
from supports import jwttoken
from supports import dateutils
import base64
from bson import ObjectId
import os


app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.json_encoder = MongodbJSONEncoder
app.json_decoder = MongodbJSONDecoder
mongo = PyMongo(app)

leo_order_request_url = os.getenv('LEO_ORDER_REQUEST_URL')
order_query_filters = \
    ('customer_name', 'created_at_start', 'created_at_end', 'delivery_date_start', 'delivery_date_end')

default_datetime_fmt = '%d/%m/%Y %H:%M:%S'
default_zone = 'America/Sao_Paulo'
# %Z = UTC; %z = +0000


@app.before_request
def before_request_func():
    return jwttoken.verify_request_token(request)


@app.route('/orders/requests', methods=['GET'])
def generate_order_url():
    payload = {'salesman': 'Caseira Massas', 'doc_id': '99.999.999/9999-99'}
    order_token = jwttoken.generate_default_order_token(payload=payload)
    order_url = '{order_app_url}?token={token}'.format(order_app_url=leo_order_request_url, token=order_token)
    return {'order_url': order_url}, 200


@app.route('/orders', methods=['POST'])
def save_orders():
    new_order = request.json
    new_order['created_at'] = dateutils.current_zoned_datetime('America/Sao_Paulo')
    new_order['status'] = 'Pendente'
    mongo.db.orders.insert_one(new_order)
    response = {'created_id': new_order.get('_id')}
    return response, 201


@app.route('/orders/<order_id>', methods=['GET'])
def get_orders_by_id(order_id):
    response = mongo.db.orders.fin_one({'_id': ObjectId(oid=order_id)})
    return response, 200


@app.route('/orders', methods=['GET'])
def get_orders():
    query_filter = {}
    request_query_params = request.args
    if len(request_query_params):
        rqp_filter = {key: value for (key, value) in request_query_params.items() if key in order_query_filters}
        for key, value in rqp_filter.items():
            if key == 'customer_name':
                query_filter['customer'] = {'name': value}
            elif key == 'created_at_start':
                if 'created_at' not in query_filter.keys():
                    query_filter['created_at'] = {}
                query_filter['created_at']['$gte'] = dateutils.parse(value, default_datetime_fmt)
            elif key == 'created_at_end':
                if 'created_at' not in query_filter.keys():
                    query_filter['created_at'] = {}
                query_filter['created_at']['$lt'] = dateutils.parse(value, default_datetime_fmt)
            elif key == 'delivery_date_start':
                if 'delivery_date' not in query_filter.keys():
                    query_filter['delivery_date'] = {}
                query_filter['delivery_date']['$gte'] = dateutils.parse(value, default_datetime_fmt)
            elif key == 'delivery_date_end':
                if 'delivery_date' not in query_filter.keys():
                    query_filter['delivery_date'] = {}
                query_filter['delivery_date']['$lt'] = dateutils.parse(value, default_datetime_fmt)
    else:
        default_date_filter_start, default_data_filter_end = dateutils.current_zoned_datetime_with_range(default_zone, 14)
        query_filter = {'created_at': {'$gte': default_date_filter_start, '$lt': default_data_filter_end}}

    result = list(mongo.db.orders.find(query_filter))
    response = {"content": result}
    return response, 200


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


@app.route('/salesman/login', methods=['POST'])
def salesman_app_login():
    auth = request.json
    auth_password_b64 = auth['password']
    auth_password_b64 = auth_password_b64.encode('UTF-8')
    auth_password_b64 = base64.b64encode(auth_password_b64)
    auth['password'] = auth_password_b64.decode('UTF-8')
    user_found = mongo.db.users.find_one(auth)

    if user_found is None:
        return {'msg': 'unauthorized'}, 401

    user_details = mongo.db.salesmen.find_one({'user_id': user_found.get('_id')})
    payload = {'salesman': user_details.get('name'), 'doc_id': user_details.get('doc_id')}

    return {'token': jwttoken.generate_salesman_token(payload=payload)}, 200


if __name__ == '__main__':
    app.run(debug=False)
