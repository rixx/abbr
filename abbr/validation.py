import re
from datetime import datetime
from urllib.parse import urlparse

from app import app


class ValidationError(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)


def validate_expiry(expiry):
    try:
        return datetime.strptime(expiry, '%Y-%m-%d %H:%M:%S')
    except:
        raise ValidationError(
            {'expiry': 'Expiry needs to be in format %Y-%m-%d %H:%M:%S.'}
        )


def validate_name(name):
    if len(name) < 2:
        raise ValidationError(
            {'name': 'Name needs to be at least 2 characters long.'}
        )
    if len(name) > 30:
        raise ValidationError(
            {'name': 'This is supposed to be a *shortening* service. '
                     'Names need to be at most 30 characters long.'}
        )
    if not re.match('^[{}]*$'.format(app.config.get('ALPHABET')), name):
        raise ValidationError(
            {'name': 'A name may only contain the following characters: {}'
                     .format(app.config.ALPHABET)}
        )
    return name


def validate_url(url):
    if url[0] == '"' or url[0] == "'":
        url = url[1:-1]

    _url = urlparse(url, scheme='http')
    # this is horrid validation. should really use Django
    if not (_url.netloc or _url.path):
        raise ValidationError({'url': 'This is not a valid URL.'})
    return url
