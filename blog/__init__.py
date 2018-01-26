from flask import Flask, session
from flask_pymongo import PyMongo
from flask_s3 import FlaskS3
from flask_bower import Bower

import os

# typically this web app should be ran like this:

env = os.environ.get("FLASK_ENV", "dev")

if env == "staging" or env == "prod":
    app = Flask(__name__)
    s3 = FlaskS3(app)
else:
    # serve static files during development
    app = Flask(__name__, static_url_path='/static')

if env == "staging" or env == "prod":
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# init MongoDB
mongo = PyMongo(app)

# inject blog title into the context of every template
@app.context_processor
def inject_title():
    try:
        return dict(blog_title=app.config["BLOG_TITLE"])
    except AttributeError:
        return dict(blog_title="My Blog")

# inject session into templates
@app.context_processor
def inject_session():
    return dict(session=session)

from . import forms, views