""" Session object model """

from database.objects.default import DBObject
from security.identification.id import create_unique_id
import time
import uuid


class Session(DBObject):
    def __init__(self, session_id: int, secret: str, for_user: int, creation: int = None,
                 expires: int = None, times_renewed: int = None, request_ip: str = None):
        self.id = session_id
        self.secret = secret
        self.request_ip = request_ip
        self.for_user = for_user
        self.creation = creation or int(time.time() * 1000)
        self.expires = expires or self.creation + 7 * 24 * 60 * 60 * 1000
        self.times_renewed = times_renewed or 0

    @staticmethod
    def empty():
        return Session(None, None, None)

