""" Endpoints for general User actions """

# Implement the user_endpoint with url_prefix = 'user'

from api.paginate import paginate
from flask import Blueprint, request, jsonify
from api.HTTPErrors import APIError
from database.actions.user import get_all_users
from database.db import MDB

user_endpoint = Blueprint("User endpoint", __name__)


# URL-scheme: /user?per_page=a&page=b&order_by=c&descending=d with a < 50 and b + 1 in pages
# and c is one of 'name', 'id', 'creation' and d is True or False
@user_endpoint.route('/', methods=['GET'])
def get_user_root():
    # Create db connection (Thread) TODO: Investigate
    db = MDB('test.db')

    per_page, page, order_by, desc = paginate(request.args, per_page=10, page=0, order_by='name', descending="False")
    if per_page > 50:
        raise APIError('per_page must not be greater than 50', 'INVALID_PAGINATION', 400)

    if order_by not in ['name', 'id', 'creation']:
        raise APIError('order_by must be either name, id or creation', 'INVALID_VALUE', 400)

    if desc.casefold() == 'true':
        desc = True
    elif desc.casefold() == 'false':
        desc = False
    else:
        raise APIError('descending must be either true or false', 'INVALID_VALUE', 400)

    if page < 0 or per_page <= 0:
        raise APIError('page must be larger than per_page larger or equal to 1', 'INVALID_PAGINATION', 400)

    users = get_all_users(per_page * page, (page + 1) * per_page, order_by, desc, _db=db)

    if len(users) <= 0:
        raise APIError('page out of range', 'PAGE_OUT_OF_RANGE', payload={
            "items": db.get_number_of_items_in_table('users')
        })

    if len(users) <= 0:
        result = [{}]
    else:
        keys = list(users[0].__dict__.keys())

        disallowed = ['password_hash', 'last_write', 'email']
        for key in disallowed:
            keys.remove(key)

        result = list()
        for user in users:
            result.append({k: user.get_item(k) for k in keys})

    response = jsonify(result)

    return response
