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


@app.before_request
def before_request():
    g.db_connection = get_db_connection()


@app.teardown_appcontext
def close_db_connection(exception):
    if hasattr(g, 'db_connection'):
        g.db_connection.close()


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', 'r') as schema_file:
            db.cursor().executescript(schema_file.read())
        db.commit()


@app.cli.command('initdb')
def command_initdb():
    init_db()
    print('Initialized the database')


def get_url(short_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    print(short_name)
    cursor.execute(
        'SELECT url FROM urls WHERE name = ?',
        (short_name, ),
    )
    result = cursor.fetchall()
    if len(result) != 1:
        return None
    return result[0]['url']


def write_url(short_name, url, expiry):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO urls (name, url, expiry) values (?, ?, ?)',
        (short_name, url, expiry),
    )
    conn.commit()
