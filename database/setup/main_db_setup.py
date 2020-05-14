from database.main_db import db
import os

os.remove("setup.sql")

with open("setup.sql") as sql_file:
    sql_script = sql_file.read()
    db.executescript(sql_script)
