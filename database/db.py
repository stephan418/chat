# Wrapper for a SQLite database
# TODO: Test on multiple threats (race conditions?) and reimplement (command queue?)

import sqlite3
from functools import wraps
from database.objects.default import DBObject


# Decorator which handles creating and closing a cursor
def handle_cursor(func):
    """
    Handles the creation, passing and destruction of a cursor
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        cur = self._conn.cursor()

        result = func(self, *args, _cursor=cur, **kwargs)

        cur.close()
        self._conn.commit()

        return result

    return wrapper


class MDB:  # Main DataBase
    """
    Object Mapper for the main database
    """
    def __init__(self, filename):
        # Establish database connection
        self._conn = sqlite3.connect(filename)

        self._objects = []

    # Generic object stuff
    @handle_cursor  # Handles cursor stuff
    def insert_all_values(self, obj: DBObject, table, keys=None, values=None, _cursor: sqlite3.Cursor = None):
        """
        Insert all the values in the object into the specified table
        :param obj: Object to be inserted
        :param table: Table to be inserted into
        :param keys: Keys to be added (If already computed before) Not to be passed without passing according values
        :param values: Values (In the same order as the keys; also like keys)
        :param _cursor: Cursor used to execute queries
        """
        keys = keys or obj.__dict__.keys()

        if values is None:
            values = obj.__dict__.values()

        # INSERT INTO table_name (all_keys) VALUES (all_values)
        _cursor.execute(f'INSERT INTO {table} ({", ".join(keys)}) '
                        f'VALUES ({", ".join("?" for _ in values)});', (*values,))

    @handle_cursor
    def read_all_values(self, obj: DBObject, table: str, identifier: int, keys=None, _cursor: sqlite3.Cursor = None):
        """
        Read all the values from a specified table into an object
        :param obj: Object to be read into
        :param table: Table to be read
        :param identifier: ID of the element to be read
        :param keys: Keys to be read (If already computed)
        :param _cursor: Cursor used to execute queries
        """
        keys = keys or obj.__dict__.keys()

        _cursor.execute(f'SELECT {", ".join(keys)} FROM {table} WHERE id = {identifier}')

        values = _cursor.fetchone()

        if values is not None:
            for key, value in zip(keys, values):
                obj.set_item(key, value)

            return True

        else:
            return False

    @handle_cursor
    def get_single_item(self, table: str, identifier: str, column: str, _cursor: sqlite3.Cursor = None):
        """
        Get a single item from a table
        :param table: Table to be read
        :param identifier: ID of the item to be read
        :param column: Column to be read
        :param _cursor: Cursor used to execute queries
        """
        _cursor.execute(f'SELECT {column} FROM {table} WHERE id = ?', (identifier,))
        values = _cursor.fetchone()
        if len(values) < 1:
            return None

        return values[0]

    @handle_cursor
    def remove_single_item(self, table: str, identifier: str, _cursor: sqlite3.Cursor = None):
        """
        Delete a single item from a table
        :param table: The table where the item is located
        :param identifier: The ID of the item
        :param _cursor: Cursor used to execute queries
        """
        _cursor.execute(f"DELETE FROM {table} WHERE id = ?", identifier)

    @handle_cursor
    def set_single_value(self, table: str, identfier: int, column: str, value, _cursor: sqlite3.Cursor = None):
        """
        Set a single value
        :param table: Table to be set
        :param identfier: ID of the item to be set
        :param column: Column of the item to be set
        :param value: Value to be set to
        :param _cursor: Cursor used to execute queries
        """

        _cursor.execute(f'UPDATE {table} SET {column} = ? WHERE id = ?', (value, identfier,))

    @handle_cursor
    def update_all_values(self, obj: DBObject, table: str, identifier: int, keys=None, values=None,
        _cursor: sqlite3.Cursor = None):

        keys = keys or obj.__dict__.keys()

        if values is None:
            values = obj.__dict__.values()

        _cursor.execute(f'UPDATE {table} SET {", ".join([f"{c} = ?" for c in keys])} WHERE id = ? ;',
                        (*values, identifier))

    @handle_cursor
    def entry_exists_eq(self, table: str, column: str, value, _cursor: sqlite3.Cursor = None):
        """
        Checks for elements satisfying the condition
        Don't use with user input (Vulnerable to SQL injection)
        :param table: Table to check
        :param column: Column where value must be located
        :param value: Value which the column must have
        :param _cursor: Cursor to be used for execution
        :return: ID of the first element or False
        """
        _cursor.execute(f"SELECT * FROM {table} WHERE {column} = ? LIMIT 1;", (value,))

        v = _cursor.fetchone()

        return True if v is not None else False

    @handle_cursor
    def get_all_elements_eq(self, table: str, column: str, value, columns: str = "*", _cursor: sqlite3.Cursor = None):
        """
        Get all the elements where the column specified in column is the value specified
        :param table: Table
        :param column: Column which should be equal
        :param value: Value to be tested for
        :param columns: The columns to be selected
        :param _cursor: Cursor used to execute queries
        :return: None or a list of elements
        """
        _cursor.execute(f"SELECT {columns} FROM {table} WHERE {column} = ?", (value,))
        values = _cursor.fetchall()

        return values if len(values) > 0 else None

    def get_cursor(self):
        """
        Get a Cursor for the connection of the instance
        :return: Cursor
        """
        return self._conn.cursor()

    def get_connection(self):
        """
        Get the connection used by the instance
        :return: Connection
        """
        return self._conn
