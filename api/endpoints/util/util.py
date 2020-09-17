""" Endpoint for utility functionality such as online """

from flask import Blueprint, jsonify
from api.cors import CORS


util_endpoint = Blueprint('Utility Endpoint', __name__, url_prefix='/util')
cors = CORS(util_endpoint)


@util_endpoint.route('/status')
@cors.append('/status', ['GET'])
def get_status_online():
    return jsonify({'online': True})


@util_endpoint.route('/')
def get():
    return "Hi"

