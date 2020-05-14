import hashlib
import random
import string


def hash_password(password: str, s: str):
    h = hashlib.scrypt(password.encode(), salt=s.encode(), n=16384, r=8, p=1)

    return h.hex() + s


def generate_salt(s_len=5):
    s = "".join(list(random.choice(string.digits + string.ascii_letters) for _ in range(s_len)))

    return s
