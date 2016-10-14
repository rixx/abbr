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
