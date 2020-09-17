""" Classes representing application Errors the client has to handle """

from flask import jsonify, make_response
from api.cors import CORS


class APIError(Exception):
    status_code = 500

    def __init__(self, message: str, error: str, status_code: int = 500, payload=None, headers: dict = None,
                 cors: dict or bool = True):
        """ payload: dict of items in addition to message """
        self.message = message
        self.error = error
        self.status_code = status_code
        self.payload = payload
        self.headers = headers
        self.cors = cors

    def to_repr(self):
        d = {'message': self.message, 'error': self.error}
        d.update(self.payload or {})
        return d, self.headers


def handle_api_error(e: APIError):
    """ Handler for api errors """
    d, headers = e.to_repr()
    resp = jsonify(d)
    resp.status_code = e.status_code
    if headers:
        for key, value in headers.items():
            resp.headers[key] = value

    if e.cors is True:
        CORS.apply_to_response(resp, ['GET', 'POST', 'DELETE'], False)
    elif e.cors:
        CORS.apply_to_response(resp, [e.cors.get('methods')], e.cors.get('authentication', False))

    return resp
