from flask import jsonify
from api import common
from api.paginate import paginate
from api.HTTPErrors import APIError
from database.actions.message import get_user_messages
from database.actions.user import get_user
from security.encode import number_encode


def api_get_messages(request, with_user: str = None, _db=None):
    s = common.handle_bearer_token(request, _db)

    per_page, page, order_by, desc = paginate(request.args, per_page=10, page=0, order_by='date_sent',
                                              descending="False")
    if per_page > 50:
        raise APIError('per_page must not be greater than 50', 'INVALID_PAGINATION', 400)

    if order_by not in ['date_sent', 'date_delivered', 'date_read', 'id', 'receiver', 'sender']:
        raise APIError('order_by must be either date_sent, date_delivered, date_read, id, receiver or sender',
                       'INVALID_VALUE', 400)

    if desc.casefold() == 'true':
        desc = True
    elif desc.casefold() == 'false':
        desc = False
    else:
        raise APIError('descending must be either true or false', 'INVALID_VALUE', 400)

    if page < 0 or per_page <= 0:
        raise APIError('page must be larger than per_page larger or equal to 1', 'INVALID_PAGINATION', 400)

    uid = None
    if with_user:
        uid = number_encode.b64decode(with_user)
        if uid is None:
            raise APIError('Unable to interpret an ID', 'INVALID_ID_FORMAT', 400)

        if not get_user(uid, _db):
            raise APIError('The requested resource could not be found or you do not have sufficient '
                           'permissions to access it', 'NOT_FOUND', 404)

    messages = get_user_messages(s.for_user, per_page * page, (page + 1) * per_page, order_by, desc, uid, _db=_db)

    if len(messages) <= 0:
        raise APIError('page out of range', 'PAGE_OUT_OF_RANGE', 404, payload={
            "items": _db.get_number_of_items_in_table('messages')
        })

    keys = list(messages[0].__dict__.keys())

    result = list()
    for msg in messages:
        result.append({k: common.encode_if_id(k, msg.get_item(k), ['id', 'sender', 'receiver']) for k in keys})

    return jsonify(result)
