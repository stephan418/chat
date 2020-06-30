from database.objects.session import Session
from security.identification.id import create_unique_id
from database.db import MDB
from security.encode.number_encode import b64decode
import uuid
import time
import base64


class ExpirationError(Exception):
    pass


def create_session(for_user: int, request_ip: str = None, _db: MDB = None):
    """ Create a new session for a specified user """
    session_id = create_unique_id(_db)
    secret = str(uuid.uuid4())

    session = Session(session_id, secret, for_user, request_ip=request_ip)

    _db.insert_all_values(session, 'sessions')

    return session


def get_session(sid: int, _db: MDB):
    """ Get a session based on the session id """
    s = Session.empty()

    if not _db.read_all_values(s, 'sessions', sid):
        return None

    if s.expires < int(time.time() * 1000):
        raise ExpirationError

    return s


def get_by_bearer(token: str, _db: MDB):
    """ Get a session from a base64 encoded bearer token """
    t = base64.b64decode(token).decode()
    t = t.split('.')

    if len(t) < 2:
        raise ValueError('Not able to interpret token, missing session_secret')

    print(t)

    sid, secret = t

    sid = b64decode(sid)

    if sid is None:
        raise ValueError('Invalid session_id')

    # Pass potential ExpirationError to caller
    s = get_session(sid, _db)

    if s is None:
        raise ValueError('Invalid session_id')

    if s.secret != secret:
        raise ValueError('Session secret invalid')

    return s
