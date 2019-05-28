from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix

from .config import configByName

"""
The main module, loads global libs and creates the flask instance.
"""

# global DB object, using SQLAlchemy ORM.
db = SQLAlchemy()

# bcrypt library for password security.
flaskBrcypt = Bcrypt()

"""
Insantiates Flask and loads the config. Loads our ORM and bcrypt libs.
@param {config} - the config class to load, depending on env.  
"""
def createApp(config):
    app = Flask(__name__)

    # CORS policies for each of the toplevel routes.
    CORS(app, resources={
        r"/user/*": {"origins": "*"}, 
        r"/auth/*": {"origins": "*"}, 
        r"/pic/*": {"origins": "*"}
    })

    # Load environment specific information
    app.config.from_object(configByName[config])

    # Fix for swagger HTTP/HTTPS cross loading on Heroku.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Load SQLAlchemy and Bcrypt
    db.init_app(app)
    flaskBrcypt.init_app(app)

    return app

