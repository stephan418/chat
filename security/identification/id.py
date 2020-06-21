from database.db import MDB
import secrets


def _exists_in_tables(tables, value: int, _db: MDB):
    for table in tables:
        if _db.entry_exists_eq(table, 'id', value):
            return True

    return False


# Create a unique id consisting of a timestamp, a number timestamp revision number and a random number
def create_unique_id(_db) -> int:
    """
    Creates a unique ID to be used in databases
    :param _db:
    :return: Integer ID
    """
    tables = ['users', 'messages', 'message_history', 'blobs', 'sessions']

    gen_id = secrets.randbelow(9223372036854775808)  # 2**63 (SQLite max int

    while _exists_in_tables(tables, gen_id, _db):
        gen_id = secrets.randbelow(9223372036854775808)

    return gen_id
