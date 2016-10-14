import os
import string
from datetime import timedelta


class Config:
    """ The default config class for abbr. """

    # The fqdn where your abbr is hosted
    SITENAME = 'abbr.example.com'
    DOMAIN = 'https://{}'.format(SITENAME)

    # Defautl expiry offset
    EXPIRY = timedelta(days=365)

    # Default short_url length
    NAME_LENGTH = 8

    # Default short_name alphabet
    ALPHABET = string.ascii_lowercase + string.digits

    # Default database settings for sqlite
    DATABASE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'abbr.db',
    )

    SECRET_KEY = 'very secret key'
    USERNAME = 'abbr-admin'
    PASSWORD = 'abbr-password'
