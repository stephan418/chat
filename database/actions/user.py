from database.objects.user import User
from database.main_db import db
from security.identification.id import create_unique_id
from security.hash import password
import time
import copy


def create_user(name: str, pwd: str, email: str = None, login_id: str = None, _db=db) -> User:
    """
    Create a new user and insert into the Database
    :return: Newly created user
    """
    salt = password.generate_salt()
    password_hash = password.hash_password(pwd, salt)
    user_id = create_unique_id()
    cts = int(time.time() * 1000)

    if not login_id:
        if email:
            login_id = email
        elif not _db.entry_exists_eq('users', 'login_id', name):
            login_id = name
        else:
            login_id = "Hallo"  # randomize

    user = User(name, password_hash, user_id, cts, -1, cts, login_id)

    _db.insert_all_values(user, "users")

    return user


def change_user_password(user: User, new_pwd: str, no_copy=False, _db=db):
    """
    Change the password of a given users
    """
    salt = password.generate_salt()
    password_hash = password.hash_password(new_pwd, salt)
    user_id = user.id

    _db.set_single_value("users", user_id, "password_hash", password_hash)

    if not no_copy:
        new_user = copy.deepcopy(user)
        new_user.password_hash = password_hash

        return new_user


def change_user_name(user: User, new_name: str, no_copy=False, _db=db):
    """ Change the username of a user """
    _db.set_single_value("users", user.id, "name", new_name)

    if not no_copy:
        new_user = copy.deepcopy(user)
        new_user.name = new_name
        return new_user


def get_user(user_id: int, _db=db):
    user = User.empty()

    _db.read_all_values(user, "users", user_id)

    return user


def get_all_users(range_from: int, range_to: int, order_by: str = None, desc: bool = False, _db=db):
    user_dict = User.empty().__dict__
    keys = user_dict.keys()
    columns = ", ".join(keys)

    fetched_users = _db.get_all_elements_from_table('users', range_from, range_to, order_by, desc, columns)

    users = []

    for user_data in fetched_users:
        user = User.empty()
        for k, v in zip(keys, user_data):
            user.set_item(k, v)

        users.append(user)

    return users
