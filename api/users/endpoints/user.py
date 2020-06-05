""" Endpoints for general User actions """

# Implement the user_endpoint with url_prefix = 'user'

from api.paginate import paginate
from flask import Blueprint, request

user_endpoint = Blueprint("User endpoint", __name__)


# URL-scheme: /user?per_page=a&page=b&order_by=c&descending=d with a < 50 and b + 1 in pages
# and c is one of 'name', 'id', 'creation' and d is True or False
@user_endpoint.route('/', methods=['GET'])
def get_user_root():
    per_page, page, order_by, desc = paginate(request, per_page=10, page=0, order_by='name', descending=False)
    if per_page > 50:
        return ValueError('per_page must not be greater than 50')

    if order_by not in ['name', 'id', 'creation']:
        raise ValueError('order_by must be either name, id or creation')

    if desc.casefold() == 'true':
        desc = True
    elif desc.casefold() == 'false':
        desc = False
    else:
        raise ValueError('descending must be either true or false')
