from database.objects.user import User
from database.main_db import db
from security.identification.id import create_unique_id
from security.hash import password
import time


def create_user(name: str, pwd: str):
    salt = password.generate_salt()
    password_hash = password.hash_password(pwd, salt)
    user_id = create_unique_id()
    cts = int(time.time() * 1000)

    user = User(name, password_hash, user_id, cts, -1, cts)

    db.insert_all_values(user, "users")


def change_user_password(user: User, new_pwd: str):
    salt = password.generate_salt()
    password_hash = password.hash_password(new_pwd, salt)
    user_id = user.id

    db.set_single_value("users", user_id, "password_hash", password_hash)


def change_user_name(user: User, new_name: str):
    db.set_single_value("users", user.id, "name", new_name)
