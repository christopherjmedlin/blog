from flask import Flask, session
from flask_pymongo import PyMongo
from flask_s3 import FlaskS3
from flask_bower import Bower
from flask_sslify import SSLify

import os

# typically this web app should be run like this:

env = os.environ.get("FLASK_ENV", "dev")

s3 = None
if env == "staging" or env == "prod":
    app = Flask(__name__)
else:
    # serve static files during development
    app = Flask(__name__, static_url_path='/static')

if env == "staging" or env == "prod":
    app.config.from_object('config.ProductionConfig')
    s3 = FlaskS3(app)
    if os.environ.get("PROTOCOL") == 'https':
        SSLify(app)
    
else:
    app.config.from_object('config.DevelopmentConfig')

if app.config["MONGO_URI"]:
    pass
else:
    # had some trouble properly escaping the mongo URI on
    # AWS elastic beanstalk, so i added the option of building
    # a mongo URI from several other variables
    try:
        app.config["MONGO_URI"] = ("mongodb://" 
            + app.config["MONGO_DB_USER"] + ":" 
            + app.config["MONGO_DB_PASSWORD"] + "@" 
            + app.config["MONGO_DB_HOST"] + ":"
            + app.config["MONGO_DB_PORT"] + "/"
            + app.config["MONGO_DB_NAME"])
    except Exception:
        raise Exception("Error building database URI. Are your DB settings properly configured?")
    

# init MongoDB
mongo = PyMongo(app)

# inject blog title into the context of every template
@app.context_processor
def inject_title():
    return dict(blog_title=app.config["BLOG_TITLE"],
                blog_description=app.config["BLOG_DESCRIPTION"],
                blog_url=app.config["BLOG_URL"])

from . import forms, views