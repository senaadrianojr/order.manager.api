from flask import request
from order_manager.supports import jwttoken


def init_app(app):

    @app.before_request
    def before_request_func():
        return jwttoken.verify_request_token(request)
