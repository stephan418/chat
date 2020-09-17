from flask import Blueprint, request, jsonify
import base64
from database.db import MDB
from database.actions.message import get_user_messages, get_message, create_message
from database.objects.message import Content
from api.HTTPErrors import APIError
from api.paginate import paginate
from api import common
from api.endpoints.message import common as message_common
from security.encode.number_encode import b64decode
import time
from api.cors import CORS

message_endpoint = Blueprint('Message endpoint', __name__, url_prefix='/message')
cors = CORS(message_endpoint)


# Gets all messages the user is authorized to see
# Authorization: Bearer b64_ascii([session_id].[session_secret])
# WWW-Authenticate: Bearer realm='user-related'
# URL-scheme: /message?per_page=a&page=b&order_by=c&descending=d with a < 50 and b + 1 in pages
# and c is one of 'date_sent', 'date_delivered', 'date_read', 'id', 'receiver', 'sender' and d is True or False
@message_endpoint.route('/', methods=['GET'], provide_automatic_options=False)
@cors.append('/', ['GET'], authentication=True)
def get_message_root():
    db = MDB('test.db')

    return message_common.api_get_messages(request, _db=db)


@message_endpoint.route('/<string:message_id>', methods=['GET'])
def get_message_id(message_id):
    db = MDB('test.db')

    s = common.handle_bearer_token(request, db)
    msg_id = b64decode(message_id)

    msg = get_message(msg_id, db)

    if msg is None:
        raise APIError('The requested resource could not be found or you do not have sufficient '
                       'permissions to access it', 'NOT_FOUND', 404)

    if not msg.receiver == s.for_user and not msg.sender == s.for_user:
        raise APIError('The requested resource could not be found or you do not have sufficient '
                       'permissions to access it', 'NOT_FOUND', 404)

    return jsonify({k: common.encode_if_id(k, msg.get_item(k), ['id', 'sender', 'receiver']) for k in msg.__dict__
                   .keys()})


@message_endpoint.route('/', methods=['POST'])
@cors.append('/', ['POST'], authentication=True)
def post_message_root():
    db = MDB('test.db')

    s = common.handle_bearer_token(request, db)

    json_data = request.get_json(force=True)

    required = ['receiver', 'text_content']
    for r in required:
        if r not in json_data:
            raise APIError("'receiver' and 'text_content' fields must be set", 'NOT_ENOUGH_INFORMATION',
                           400)

    receiver = b64decode(json_data['receiver'])
    if receiver is None:
        raise APIError('Unable to interpret an ID', 'INVALID_ID_FORMAT', 400)

    msg = create_message(s.for_user, receiver, Content(json_data['text_content']), int(time.time()) * 1000, db)

    return jsonify({k: common.encode_if_id(k, msg.get_item(k), ['id', 'sender', 'receiver']) for k in msg.__dict__
                   .keys()})
