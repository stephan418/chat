# Wrapper for a SQLite database

import sqlite3
from database.objects.user import User
from database.objects.default import DBObject


# Decorator which handles creating and closing a cursor
def handle_cursor(func):
    def wrapper(self, *args, **kwargs):
        cur = self._conn.cursor()

        func(self, *args, _cursor=cur, **kwargs)

        cur.close()
        self._conn.commit()

    return wrapper


class MDB:  # Main DataBase
    def __init__(self, filename):
        # Establish database connection
        self._conn = sqlite3.connect(filename)

        self._objects = []

    # Generic object stuff
    @handle_cursor  # Handles cursor stuff
    def insert_all_values(self, obj: DBObject, table, _cursor: sqlite3.Cursor, keys=None, values=None):
        keys = keys or obj.__dict__.keys()

        if values is None:
            values = []

            for value in obj.__dict__.values():
                if isinstance(value, str):  # Add quotes if the element is a string
                    values.append(f"'{value}'")
                else:
                    values.append(str(value))

        _cursor.execute(f'INSERT INTO {table} ({", ".join(keys)}) '
                        f'VALUES ({", ".join(values)});')  # INSERT INTO table_name (all_keys) VALUES (all_values)

    @handle_cursor
    def read_all_values(self, obj: DBObject, table, identifier, _cursor: sqlite3.Cursor, keys=None):
        keys = keys or obj.__dict__.keys()

        _cursor.execute(f'SELECT {", ".join(keys)} FROM {table} WHERE id = {identifier}')

        values = _cursor.fetchone()

        if values is not None:
            for key, value in zip(keys, values):
                obj.set_item(key, value)

            return True

        else:
            return False
