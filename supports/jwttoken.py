import jwt
import pytz
from datetime import datetime, timedelta
import re

sa_timezone = pytz.timezone('America/Sao_Paulo')
secret_key = 'mysecret'
public_routes = (r'^(/salesman/login)$', r'^(/orders/\w{1,})$', r'^(/orders/resume/\w{1,})$')
excluded_methods = ("OPTIONS")


def generate_default_order_token(payload={}, exp_time_hours=24):
    current_datetime = datetime.now(sa_timezone)
    exp_time = current_datetime + timedelta(hours=exp_time_hours)
    payload['exp'] = exp_time.timestamp()
    return jwt.encode(payload, secret_key, algorithm='HS256').decode('UTF-8')


def generate_salesman_token(payload={}, exp_time_hours=8):
    current_datetime = datetime.now(sa_timezone)
    exp_time = current_datetime + timedelta(hours=exp_time_hours)
    payload['exp'] = exp_time.timestamp()
    return jwt.encode(payload, secret_key, algorithm='HS256').decode('UTF-8')


def decode_token_get_salesman_details(request):
    token = request.headers.get('token')
    decoded_token = decode(token)
    return decoded_token;


def decode(token):
    return jwt.decode(token, secret_key, algorithms='HS256')


def verify_request_token(request):
    try:
        excluded_route = route_matches_excluded_pattern(request.path)
        if request.method not in excluded_methods and not excluded_route:
            token = request.headers.get('token')
            if not token or token.isspace():
                return {'msg': 'missing token'}, 401

            jwt.decode(token, secret_key, algorithms='HS256')

    except jwt.ExpiredSignatureError:
        return {'msg': 'order token expired'}, 403

    except jwt.InvalidTokenError:
        return {'msg': 'invalid token'}, 401


def route_matches_excluded_pattern(str_value):
    value_matches = False
    for regex_pattern in public_routes:
        p = re.compile(regex_pattern)
        if p.match(str_value):
            value_matches = True
    return value_matches
