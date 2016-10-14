from urllib.parse import urljoin

from flask import abort, jsonify, redirect, render_template, request

from app import app
from db import get_url, write_url
from utils import get_expiry, get_random_name, return_json
from validation import (
    ValidationError,
    validate_expiry,
    validate_name,
    validate_url,
)


def home_page():
    if return_json():
        return jsonify("Hi, I'm abbr. "
                       "Usage: POST either a url as string or a dict with "
                       "'url' and optionally 'name' and 'expiry' "
                       "('%Y-%m-%d %H:%M:%S').")
    return render_template('index.html')


def create_short_url():
    if len(request.form) == 1 and 'url' not in request.form.keys():
        url = next(request.form.keys())
    else:
        url = request.form.get('url')
    name = request.form.get('name') or get_random_name()
    expiry = request.form.get('expiry') or get_expiry()

    try:
        url = validate_url(url)
        name = validate_name(name)
        expiry = validate_expiry(expiry)
    except ValidationError as err:
        message = err.message
    else:
        write_url(name, url, expiry)
        message = urljoin(app.config.get('DOMAIN'), name)

    if return_json():
        return jsonify(message)
    return render_template('index.html', message=message)


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
