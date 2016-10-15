from datetime import datetime
import random

from flask import request

from app import app


def return_json():
    if 'curl' in request.headers.get('User-Agent'):
        return True
    if 'wget' in request.headers.get('User-Agent'):
        return True
    best = request.accept_mimetypes.best_match(
        ['application/json', 'text/html']
    )
    return best == 'application/json' and \
        request.accept_mimetypes[best] > request.accept_mimetypes['text/html']


def get_random_name():
    import db
    conn = db.get_db_connection()
    i = 10

    while i > 0:
        name = ''.join(
            random.choice(app.config.get('ALPHABET'))
            for _ in range(app.config.get('NAME_LENGTH'))
            )
        query = conn.execute('SELECT * FROM urls WHERE name = ?', (name, ))
        if not query.fetchall():
            return name
    raise Exception('Unable to find unique name.')


def get_expiry():
    return datetime.now() + app.config.get('EXPIRY')


def from_datetime(some_datetime):
    return datetime.strftime(some_datetime, '%Y-%m-%d %H:%M:%S')


def to_datetime(some_string):
    return datetime.strptime(some_string, '%Y-%m-%d %H:%M:%S')
