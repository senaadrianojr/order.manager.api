import os
from bson import ObjectId
from flask import request, abort
from flask_pymongo import ASCENDING, DESCENDING
from order_manager.supports import dateutils, jwttoken
from order_manager.extensions.database import db

leo_order_request_url = os.getenv('LEO_ORDER_REQUEST_URL')

order_query_filters = \
    ('customer_name',
     'created_at_start',
     'created_at_end',
     'delivery_date_start',
     'delivery_date_end',
     'page_number',
     'page_size',
     'order_by',
     'sort')

default_datetime_fmt = '%d/%m/%Y %H:%M:%S%z'
default_zone = 'America/Sao_Paulo'
# %Z = UTC; %z = +0000


def init_app(app):
    mongo = db

    @app.route('/orders/requests', methods=['GET'])
    def generate_order_url():
        payload = {'salesman': 'Caseira Massas', 'doc_id': '99.999.999/9999-99'}
        order_token = jwttoken.generate_default_order_token(payload=payload)
        order_url = '{order_app_url}?token={token}'.format(order_app_url=leo_order_request_url, token=order_token)
        return {'order_url': order_url}, 200

    @app.route('/orders', methods=['POST'])
    def save_orders():
        new_order = request.json
        new_order['created_at'] = dateutils.current_zoned_datetime(default_zone)
        new_order['status'] = 'pendente'
        mongo.db.orders.insert_one(new_order)
        response = {'created_id': new_order.get('_id')}
        return response, 201

    @app.route('/orders/<order_id>', methods=['GET'])
    def get_orders_by_id(order_id):
        response = mongo.db.orders.find_one({'_id': ObjectId(oid=order_id)})
        return response, 200

    @app.route('/orders/<order_id>', methods=['PUT'])
    def update_orders(order_id):
        order_founded = mongo.db.orders.find_one({'_id': ObjectId(oid=order_id)}) or abort(404)
        new_order = request.json
        updated_order = {**order_founded,
                         **new_order,
                         'created_at': order_founded.get('created_at'),
                         'last_update': dateutils.current_zoned_datetime(default_zone)}

        mongo.db.orders.replace_one({'_id': ObjectId(oid=order_id)}, updated_order)

        return {}, 203

    @app.route('/orders/resume/<order_id>', methods=['GET'])
    def get_order_resume_by_id(order_id):
        response = mongo.db.orders.find_one({'_id': ObjectId(oid=order_id)}) or abort(404)
        return response, 200

    @app.route('/orders', methods=['GET'])
    def get_orders():
        query_filter = {}
        request_query_params = request.args
        pagination = {'page_number': 1, 'page_size': 25}
        ordination = {'order_by': 'created_at', 'sort': ASCENDING}
        if len(request_query_params):
            rqp_filter = {key: value for (key, value) in request_query_params.items() if key in order_query_filters}
            for key, value in rqp_filter.items():
                if key == 'customer_name':
                    query_filter['customer'] = {'name': value}
                elif key == 'created_at_start':
                    if 'created_at' not in query_filter.keys():
                        query_filter['created_at'] = {}
                    query_filter['created_at']['$gte'] = dateutils.parse_with_fixed_tz(value, default_datetime_fmt)
                elif key == 'created_at_end':
                    if 'created_at' not in query_filter.keys():
                        query_filter['created_at'] = {}
                    query_filter['created_at']['$lt'] = dateutils.parse_with_fixed_tz(value, default_datetime_fmt)
                elif key == 'delivery_date_start':
                    if 'delivery_date' not in query_filter.keys():
                        query_filter['delivery_date'] = {}
                    query_filter['delivery_date']['$gte'] = dateutils.parse_with_fixed_tz(value, default_datetime_fmt)
                elif key == 'delivery_date_end':
                    if 'delivery_date' not in query_filter.keys():
                        query_filter['delivery_date'] = {}
                    query_filter['delivery_date']['$lt'] = dateutils.parse_with_fixed_tz(value, default_datetime_fmt)
                elif key == 'page_number' and int(value) > 0:
                    pagination['page_number'] = int(value)
                elif key == 'page_size' and int(value) > 0:
                    pagination['page_size'] = int(value)
                elif key == 'sort' and value is not None:
                    ordination['sort'] = ASCENDING if value == 'asc' else DESCENDING
                elif key == 'order_by' and value is not None:
                    ordination['order_by'] = value

        else:
            default_date_filter_start, default_data_filter_end = dateutils.current_zoned_datetime_with_range(default_zone, 14)
            query_filter = {'created_at': {'$gte': default_date_filter_start, '$lt': default_data_filter_end}}

        total_records_found = mongo.db.orders.find(query_filter).count()
        max_page_number = round(total_records_found/pagination.get('page_size'))
        pages = list(range(1, max_page_number + 1))
        if pagination.get('page_number') == 1:
            cursor = mongo.db.orders.find(query_filter)\
                .sort(ordination.get('order_by'), ordination.get('sort'))\
                .limit(pagination.get('page_size'))
        else:
            skip = (pagination.get('page_number') - 1) * pagination.get('page_size')
            limit = pagination.get('page_size')
            cursor = mongo.db.orders.find(query_filter).skip(skip).limit(limit)

        result = list(cursor)
        response = {"content": result, "pages": pages}
        return response, 200
