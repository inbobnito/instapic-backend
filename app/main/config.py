import os

"""
Server config settings. Three environments are defined - development, testing, and production. 

For simplicity, all three of them use Python's SQLLite package for the DB connection. 
Ideally, we'd want to connect to a remote SQL DB. 
"""

# base directory for path resolutions. 
basedir = os.path.abspath(os.path.dirname(__file__))

# Global app settings.
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'keyboard_cat')
    DEBUG = False

# Development environment settings.
class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instapic_dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Test environment / automated testing. 
class TestConfig(Config):
    DEBUG = True
    TEST = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instapic_dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

# Production environment.
class ProdConfig(Config):
    DEBUG = False


configByName = dict(
    dev = DevConfig,
    development = DevConfig,
    test = TestConfig,
    prod = ProdConfig,
    production = ProdConfig
)

# export the unique key.
key = Config.SECRET_KEY
