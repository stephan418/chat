""" Classes representing application Errors the client has to handle """

from flask import jsonify


class APIError(Exception):
    status_code = 500

    def __init__(self, message: str, error: str, status_code: int = 500, payload=None):
        """ payload: dict of items in addition to message """
        self.message = message
        self.error = error
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        d = {'message': self.message, 'error': self.error}
        d.update(self.payload or {})
        return d


def handle_api_error(e: APIError):
    """ Handler for api errors """
    resp = jsonify(e.to_dict())
    resp.status_code = e.status_code
    return resp
