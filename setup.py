from codecs import open
from os import path
from setuptools import setup

setup(
    name = 'abbr',
    version = '0.0.0',

    description = 'Self-hosted URL shortener',

    url = 'https://github.com/rixx/abbr',

    author = 'Tobias Kunze',
    author_email = 'rixx@cutebit.de',

    license = 'Apache Software License',

    classifiers = [
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    packages = ['abbr'],

    install_requires = [
        'Flask==0.11.1',
    ],
)
