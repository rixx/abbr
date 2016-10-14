import sqlite3
from contextlib import closing

from flask import g

from app import app


def connect_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def get_db_connection():
    if not hasattr(g, 'db_connection'):
        g.db_connection = connect_db()
    return g.db_connection


