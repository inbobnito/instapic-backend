from flask_restplus import Api
from flask import Blueprint

from .main.controller.user import api as NSUser
from .main.controller.auth import api as NSAuth
from .main.controller.pic import api as NSPic

"""
Main app 
"""

# Flask's version of extensions/modules
blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Instapic Backend',
          version='1.0',
          description='Instapic API'
          )

# Add routes 
api.add_namespace(NSAuth)
api.add_namespace(NSUser, path='/user') 
api.add_namespace(NSPic, path='/pic')