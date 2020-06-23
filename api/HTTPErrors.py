""" Classes representing application Errors the client has to handle """

from flask import jsonify, make_response


class APIError(Exception):
    status_code = 500

    def __init__(self, message: str, error: str, status_code: int = 500, payload=None, headers: dict = None):
        """ payload: dict of items in addition to message """
        self.message = message
        self.error = error
        self.status_code = status_code
        self.payload = payload
        self.headers = headers

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

    return resp
