import os
from flask import Flask


app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.Config')
if os.environ.get('ABBR_CONFIG'):
    app.config.from_envvar('ABBR_CONFIG')
