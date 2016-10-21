from datetime import datetime, timedelta
from urllib.parse import urljoin

from flask import abort, jsonify, redirect, render_template, request
from ago import human

from app import app
from db import get_url, write_url
from utils import from_datetime, get_expiry, get_random_name, return_json
from validation import (
    ValidationError,
    validate_expiry,
    validate_name,
    validate_url,
)


def get_expiries():
    now = datetime.now()
    default = app.config.get('EXPIRY')
    default_hours = default.days * 24 + default.hours
    default_times = [
        1,                   # an hour
        24,                  # a day
        24 * 7,              # a week
        24 * 7 * 30,         # a month
        27 * 7 * 365,        # a year
        27 * 7 * 365 * 100,  # when the server dies (100 years)
    ]

    try:
        default_times.delete(default_hours)
    except ValueError:
        pass

    default_times.append(default_hours)
    expiries = [
        {
            'name': human(now + timedelta(hours=span, seconds=1), precision=1),
            'value': from_datetime(now + timedelta(hours=span)),
        }
        for span in default_hours
    ]
    expiries[-1]['name'] += ' (default)'
    return expiries


def home_page():
    if return_json():
        return jsonify("Hi, I'm abbr. "
                       "Usage: POST either a url as string or a dict with "
                       "'url' and optionally 'name' and 'expiry' "
                       "('%Y-%m-%d %H:%M:%S', Default: " + from_datetime(get_expiry()) + ").")
    return render_template('index.html', expiries=get_expiries())


def create_short_url():
    data = request.get_json(silent=True, force=True) or request.form
    error = None
    short_url = None

    if isinstance(data, str):
        url = data
        name = get_random_name()
        expiry = get_expiry()
    else:
        url = data.get('url')
        name = data.get('name') or get_random_name()
        expiry = data.get('expiry') or get_expiry()

    try:
        url = validate_url(url)
        name = validate_name(name)
        expiry = validate_expiry(expiry)
    except ValidationError as err:
        error = err.message
    else:
        write_url(name, url, expiry)
        short_url = urljoin(app.config.get('DOMAIN'), name)

    if return_json():
        return jsonify(short_url)
    return render_template('index.html', expiries=get_expiries(), short_url=short_url, error=error)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return home_page()
    elif request.method == 'POST':
        return create_short_url()


def get_redirect_or_404(short_url):
    url = get_url(short_url)
    if not url:
        return abort(404)
    if not url.startswith('http'):
        url = 'http://' + url
    return redirect(url, code=301)


def get_info_or_404(short_url):
    url = get_url(short_url)
    if not url:
        return abort(404)
    detail = {'name': short_url, 'url': url}
    if return_json():
        return jsonify(detail)
    return render_template('detail.html', **detail)


@app.route('/<short_url>', methods=['GET'])
def get_redirect(short_url):
    if 'info' in request.args:
        return get_info_or_404(short_url)
    else:
        return get_redirect_or_404(short_url)
