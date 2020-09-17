from flask import Blueprint, request, make_response, session, jsonify
from api.HTTPErrors import APIError
from database.db import MDB
from database.actions.session import create_session, get_session
from database.actions.user import check_user_password, get_user
from security.encode.number_encode import b64decode
from api import common
from api.cors import CORS
from database.actions import session

import time
import secrets

session_endpoint = Blueprint('Session endpoint', __name__, url_prefix='/session')
cors = CORS(session_endpoint)


@session_endpoint.route('/', methods=['GET'])
@cors.append('/', ['GET'])
def get_session_root():
    raise APIError('You are not allowed to access this route', 'ACCESS_NOT_GRANTED', 403)


@session_endpoint.route('/', methods=['POST'])
@cors.append('/', ['POST'])
def post_session_route():
    db = MDB('test.db')

    json = request.get_json(force=True)
    f_cors = {'methods': ['POST']}

    for r in ['id', 'password']:
        if r not in json:
            raise APIError("'id' and 'password' fields must be set", 'NOT_ENOUGH_INFORMATION', 400, cors=f_cors)

    uid = b64decode(json['id'])

    if uid is not None:
        user = get_user(uid, db)
    else:
        raise APIError('The ID is malformed and the server was not able to interpret it', 'MALFORMED_ID', 400,
                       cors=f_cors)

    if user is None:
        time.sleep(secrets.randbelow(100) / 100)

        raise APIError('Invalid credentials', 'ACCESS_NOT_GRANTED', 403, cors=f_cors)

    s = None

    if check_user_password(user.id, json['password'], db):
        s = create_session(user.id, request.remote_addr, db)

    time.sleep(secrets.randbelow(100) / 100)

    if s:
        keys = list(s.__dict__.keys())
        keys.remove('request_ip')

        return jsonify({k: common.encode_if_id(k, s.get_item(k), encode=['id', 'for_user']) for k in keys})

    raise APIError('Invalid credentials', 'ACCESS_NOT_GRANTED', 403, cors=f_cors)


@session_endpoint.route('/<string:session_id>', methods=['DELETE'])
def delete_session_id(session_id):
    db = MDB('test.db')

    session_id = b64decode(session_id)

    try:
        s = get_session(session_id, db)
    except session.ExpirationError:
        raise APIError('This session has already expired!', 'RESOURCE_EXPIRED', 410)

    if not s:
        raise APIError('The requested resource could not be found', 'NOT_FOUND', 404)

    db.remove_single_item('sessions', s.id)

    return "", 204
