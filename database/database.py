# Wrapper for a SQLite database

import sqlite3


class Db:
    def __init__(self, filename):
        # Establish database connection
        self._conn = sqlite3.connect(filename)

        self._objects = []

    def register_object(self, obj):
        self._objects.append(obj)