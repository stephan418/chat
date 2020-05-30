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
        if login_id is None and email is None:
            raise ValueError("Both login_id and email are none, which is not allowed")

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


def create_user(name: str, pwd: str) -> User:
    salt = password.generate_salt()
    password_hash = password.hash_password(pwd, salt)
    user_id = create_unique_id()
    cts = int(time.time() * 1000)

    user = User(name, password_hash, user_id, cts, -1, cts)

    return user
