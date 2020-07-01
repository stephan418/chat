from flask import Blueprint, request, jsonify
from api import common
from api.HTTPErrors import APIError
from api.paginate import paginate
from database.db import MDB
from database.actions.conversation import get_user_conversations
from security.encode.number_encode import b64encode_pad

conversation_endpoint = Blueprint('Conversation Blueprint', __name__, url_prefix='/conversation')


@conversation_endpoint.route('/', methods=['GET'])
def get_conversation_root():
    db = MDB('test.db')

    s = common.handle_bearer_token(request, db)

    # TODO: Refactor into function for use in other endpoints
    per_page, page = paginate(request.args, per_page=10, page=0)
    if per_page > 50:
        raise APIError('per_page must not be greater than 50', 'INVALID_PAGINATION', 400)

    if page < 0 or per_page <= 0:
        raise APIError('page must be larger than per_page larger or equal to 1', 'INVALID_PAGINATION', 400)

    conversations = get_user_conversations(s.for_user, per_page * page, (page + 1) * per_page, _db=db)

    if len(conversations) <= 0:
        raise APIError('page out of range', 'PAGE_OUT_OF_RANGE', 404)

    result = list()
    for conversation in conversations:
        result.append({
            'participants': [
                b64encode_pad(conversation.participants[0], 11),
                b64encode_pad(conversation.participants[1], 11)
            ],
            'last_activity': conversation.last_activity
        })

    return jsonify(result)
