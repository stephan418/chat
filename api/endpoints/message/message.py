from flask import Blueprint


message_endpoint = Blueprint('User endpoint', __name__)

# Gets all messages the user is authorized to see
# @message_endpoint.route('/', methods=['GET'])
