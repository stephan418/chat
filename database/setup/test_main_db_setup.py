# Test cases fot the database setup

import unittest
import sqlite3
import os
from builtins import classmethod


class TestDatabaseSetup(unittest.TestCase):
    def test_1setup(self):
        conn = sqlite3.connect("test.db")
        self.db = conn.cursor()

        with open("scheme.sql") as sql_file:
            self.db.executescript(sql_file.read())

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.db")


class TestDatabaseFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        with open("scheme.sql") as sql_file:
            cursor.executescript(sql_file.read())

        cursor.close()
        conn.commit()
        conn.close()

    def setUp(self):
        self.conn = sqlite3.connect("test.db")
        self.cursor = self.conn.cursor()

    def test_1_insert(self):
        self.cursor.execute("INSERT INTO users (id, name, password_hash, email, creation, last_write) VALUES "
                            "(123, 'babo', 123, 'babo', 123, 123)")

    def test_2_read(self):
        self.cursor.execute("SELECT * FROM users")
        entry = self.cursor.fetchone()

        self.assertEqual(entry, (123, 'babo', '123', None, 'babo', 123, None, 123))

    def test_3_invalid_input_data_type(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("INSERT INTO users (id, name, password_hash, creation, last_write) VALUES "
                                "(123, 'babo', 'hallo', 123, 123)")

    def test_3_invalid_input_not_given(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("INSERT INTO users (id, name, password_hash, last_write) VALUES "
                            "(123, 'babo', 123, 123)")

    def test_4_message_insert(self):
        self.cursor.execute("INSERT INTO messages (id, sender, receiver, text_content, creation, date_sent, "
                            "date_delivered, last_write) VALUES (123, 123, 123, 'babo', 123, 123, 123, 123)")

    def test_5_messsage_read(self):
        self.cursor.execute("SELECT text_content FROM messages WHERE sender = 123")
        content = self.cursor.fetchone()

        self.assertEqual('babo', content[0])

    def tearDown(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.db")

unittest.main()