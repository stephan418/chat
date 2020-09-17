from security.encode import number_encode
from api.HTTPErrors import APIError
from flask import Request
from database.actions.session import get_by_bearer, ExpirationError


def encode_if_id(key: str, value, encode: list = None):
    """ Encode and pad the value if it is under the key 'id' """
    if encode is None:
        encode = ['id']

    return value if key not in encode else number_encode.b64encode_pad(value, 11)


def _raise_token_error():
    raise APIError('Invalid or non existent bearer token in \'Authenticate\' header', 'INVALID_TOKEN', 401, {
        'authenticate': {
            'endpoint': 'POST /session',
            'parameters': {
                'id': '[user_id]',
                'password': '[user_password]'
            }
        }
    }, {'WWW-Authenticate': 'Bearer realm="basic user data"'}, cors=True)


def handle_bearer_token(request: Request, db):
    b_token = request.headers.get('Authorization')

    if b_token is None or not b_token.startswith('Bearer '):
        _raise_token_error()

    s = None
    try:
        s = get_by_bearer(b_token.split('Bearer ')[1], db)
    except ValueError:
        _raise_token_error()
    except ExpirationError:
        _raise_token_error()

    return s
