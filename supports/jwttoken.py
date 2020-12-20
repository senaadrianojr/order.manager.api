import jwt
import pytz
from datetime import datetime, timedelta

sa_timezone = pytz.timezone('America/Sao_Paulo')
secret_key = 'mysecret'

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
        if request.method not in excluded_methods and request.path not in public_routes:
            token = request.headers.get('token')
            if not token or token.isspace():
                return {'msg': 'missing token'}, 401

            jwt.decode(token, secret_key, algorithms='HS256')

    except jwt.ExpiredSignatureError:
        return {'msg': 'order token expired'}, 403

    except jwt.InvalidTokenError:
        return {'msg': 'invalid token'}, 401

#TODO: usar regex para validar rotas publicas
public_routes = ['/salesman/login', '/orders/<order_id>']
