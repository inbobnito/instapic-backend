from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user import create, findAll, findByUserName 
from ..service.pic import viewPostsByUser
from ..util.decorator import token_required

api = UserDto.api
_user = UserDto.user

"""
User controller
"""

@api.route('/')
class UserList(Resource):
    @api.doc('Get all users')
    @token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """ Get all registered users """
        return findAll()

    @api.response(201, 'User successfully created.')
    @api.doc('Create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """ Create a new User """
        data = request.json
        return create(data=data)