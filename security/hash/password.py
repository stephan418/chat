import hashlib
import random
import string


def hash_password(password: str, s: str):
    """
    Hash a password using scrypt
    :param password: Password
    :param s: Salt to be appended to the password
    :return: Hashed password
    """
    h = hashlib.scrypt(password.encode(), salt=s.encode(), n=16384, r=8, p=1)

    return h.hex() + s


def generate_salt(s_len=8):  # Default salt length = 8
    """
    Generates a salt values
    :param s_len: Length of the salt
    :return: Salt
    """
    s = "".join(list(random.choice(string.digits + string.ascii_letters) for _ in range(s_len)))

    return s
