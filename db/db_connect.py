from flask import g

import sqlite3

HOSTING_DATABASE = '/home/Innosan/mysite/db/portfolio.db'
DATABASE = 'db/portfolio.db'


def get_db():
    db = getattr(g, '_database', None)

    # Change to DATABASE while local development
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db.row_factory = make_dicts

    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()

    cur.connection.commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv
