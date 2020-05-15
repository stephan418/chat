from database.main_db import db
import os


def setup():
    with open("scheme.sql") as sql_file:
        sql_script = sql_file.read()
        db.executescript(sql_script)
