""" User object model """
from security.hash import password
from security.identification.id import create_unique_id
from database.objects.default import DBObject
import time


class User(DBObject):
    """
    Object model of the users table
    """
    def __init__(self, name: str, password_hash: str, user_id: int, cts: int, llts: int, lwts: int,
                 login_id: str = None, email: str = None):

        self.name = name
        self.password_hash = password_hash
        self.login_id = login_id or email
        self.email = email
        self.id = user_id
        self.creation = cts
        self.last_login = llts
        self.last_write = lwts

    # Used to create an empty instance of the class. Not to be written to any database
    @staticmethod
    def empty():
        """
        :return: Empty user
        """
        return User(None, None, None, None, None, None)

