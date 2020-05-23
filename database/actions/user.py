from database.objects.user import User
from database.main_db import db
from security.identification.id import create_unique_id
from security.hash import password
import time


def create_user(name: str, pwd: str) -> User:
    """
    Create a new user and insert into the Database
    :return: Newly created user
    """
    salt = password.generate_salt()
    password_hash = password.hash_password(pwd, salt)
    user_id = create_unique_id()
    cts = int(time.time() * 1000)

    user = User(name, password_hash, user_id, cts, -1, cts)

    db.insert_all_values(user, "users")

    return user


def change_user_password(user: User, new_pwd: str):
    """
    Change the password of a given users
    """
    salt = password.generate_salt()
    password_hash = password.hash_password(new_pwd, salt)
    user_id = user.id

    db.set_single_value("users", user_id, "password_hash", password_hash)


def change_user_name(user: User, new_name: str):
    """ Change the username of a user """
    db.set_single_value("users", user.id, "name", new_name)
