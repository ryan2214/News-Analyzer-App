import sqlite3
from flask import g

DATABASE = './database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Files
       (file_name              TEXT    ,
       upload_date             TEXT    ,
       text                    TEXT    ,
       title                   TEXT    ,
       author                  TEXT    ,
       sentiment_score         REAL    NOT NULL,
       sentiment_magnitude     REAL    NOT NULL,
       sentiment               TEXT    NOT NULL,
       description             TEXT    ,
       url                     TEXT             );''')
    db.commit()
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
