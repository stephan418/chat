from database.objects.session import Session
from security.identification.id import create_unique_id
from database.db import MDB
import uuid
import time


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

