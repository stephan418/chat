# Wrapper for a SQLite database

import sqlite3
from database.objects.user import User


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
    def insert_all_values(self, obj, table, _cursor: sqlite3.Cursor, keys=None, values=None):
        if keys is None:
            keys = obj.__dict__.keys()

        if values is None:
            values = []

            for value in obj.__dict__.values():
                if isinstance(value, str):  # Add quotes if the element is a string
                    values.append(f"'{value}'")
                else:
                    values.append(str(value))

        _cursor.execute(f'INSERT INTO {table} ({", ".join(keys)}) '
                        f'VALUES ({", ".join(values)});')  # INSERT INTO table_name (all_keys) VALUES (all_values)


a = User("babo", "babo", 1234, 123, 123, 123)

b = MDB("a.db")
b.insert_all_values(a, "babo")
