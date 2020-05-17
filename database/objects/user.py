from security.hash import password
from security.identification.id import create_unique_id
import time


class User:
    def __init__(self, name: str, password_hash: str, user_id: int, cts: int, llts: int):
        self.name = name
        self.password_hash = password_hash
        self.user_id = user_id
        self.creation = cts
        self.last_login = llts


def create_user(name: str, pwd: str) -> User:
    salt = password.generate_salt()
    password_hash = password.hash_password(pwd, salt)
    user_id = create_unique_id()
    cts = int(time.time() * 1000)

    user = User(name, password_hash, user_id, cts, -1)

    return user
