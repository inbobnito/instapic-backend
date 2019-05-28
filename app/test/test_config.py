import os
import unittest
from flask import current_app
from flask_testing import TestCase
from manage import app
from app.main.config import basedir

"""
Unit tests to verify the integrity of our env configs.
"""

class TestDevConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.DevConfig')
        return app

    def testAppIsDev(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'keyboard_cat')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'instapic_dev.db'))


class TestUnitTestConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.TestConfig')
        return app

    def testAppIsTest(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'keyboard_cat')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'instapic_dev.db'))


class TestProdConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.ProdConfig')
        return app

    def testAppIsProd(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()