"""
This file is used for handling CORS (Cross-Site Request Sharing) requests
"""

from flask import Flask, Blueprint, Response, request
from functools import wraps


class CORS:
    def __init__(self, flask_app: Flask or Blueprint):
        """
        Handles Cross-Site Request Sharing
        :param flask_app: The Flask app or blueprint to provide functionality to
        """
        self._app = flask_app
        self._dict = {}
        self._options = []

    def add_to_dict(self, route, methods, authentication):
        for method in methods:
            self._dict[route] = self._dict.get(route, {})
            self._dict[route][method] = authentication

    @staticmethod
    def apply_to_response(resp: Response, methods: list, authentication: bool = False):
        if not isinstance(resp, Response):
            resp = Response(resp)

        resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', 'http://localhost')
        resp.headers['Vary'] = 'Origin'
        resp.headers['Access-Control-Max-Age'] = 200

        resp.headers['Access-Control-Allow-Methods'] = ''.join([f'{method}, ' for method in methods])[:-2]

        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'

        if authentication:
            resp.headers['Access-Control-Allow-Credentials'] = 'true'
            resp.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'

        return resp

    def append(self, route: str, methods: list, add_options=True, authentication=False):
        """
        Automatically appends CORS-Headers to the response of and view-function
        :param route: route of the view function
        :param methods: A list of all the methods the decorator applies to
        :param add_options: Add a handler for OPTIONS preflight request (Only added once for a route)
        :param authentication: Use authentication at the specified route
        """
        def decorator(func):
            if add_options:
                self.add_to_dict(route, methods, authentication)

                # Only set up handler if there isn't already one at the route (One handler handles all HTTP-Methods)
                if route not in self._options:
                    def handle_options(*args, **kwargs):  # view-function for the options request
                        print('HASLLo')
                        resp = Response()
                        resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', 'http://localhost')
                        resp.headers['Vary'] = 'Origin'
                        resp.headers['Access-Control-Max-Age'] = 5  # TODO: Change if not debugging

                        # Test if the Requested method is in any of the decorated methods
                        if request.headers['Access-Control-Request-Method'] in self._dict[route].keys():
                            resp.headers['Access-Control-Allow-Methods'] = request.headers[
                                'Access-Control-Request-Method']
                        else:
                            resp.headers['Access-Control-Allow-Methods'] = ''.join(
                                [m + ', ' for m in self._dict[route].keys()])[:-2]

                        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'

                        if self._dict.get(route, {}).get(request.headers['Access-Control-Request-Method']) is True:
                            resp.headers['Access-Control-Allow-Credentials'] = 'true'
                            resp.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'

                        return resp

                    self._app.add_url_rule(route, 'handle_options_' + route.replace('/', ''),
                                           handle_options, methods=['OPTIONS'])

                    self._options.append(route)

            @wraps(func)
            def wrapper(*args, **kwargs):
                resp = func(*args, **kwargs)
                return self.apply_to_response(resp, methods, authentication)

            wrapper.provide_automatic_options = False

            return wrapper

        return decorator
