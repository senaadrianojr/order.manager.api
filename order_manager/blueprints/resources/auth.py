import base64
from flask import request, abort
from order_manager.supports import jwttoken
from order_manager.extensions.database import db


def init_app(app):
    mongo = db

    @app.route('/salesman/login', methods=['POST'])
    def salesman_app_login():
        auth = request.json
        auth_password_b64 = auth['password']
        auth_password_b64 = auth_password_b64.encode('UTF-8')
        auth_password_b64 = base64.b64encode(auth_password_b64)
        auth['password'] = auth_password_b64.decode('UTF-8')
        user_found = mongo.db.users.find_one(auth) or abort(401)
        user_details = mongo.db.salesmen.find_one({'user_id': user_found.get('_id')})
        payload = {'salesman': user_details.get('name'), 'doc_id': user_details.get('doc_id')}

        return {'token': jwttoken.generate_salesman_token(payload=payload)}, 200
