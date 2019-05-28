from flask import request
from flask_restplus import Resource
from flask import request

from app.main.service.auth import Auth
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.auth

"""
Authentication controller
"""

@api.route('/login')
class UserLogin(Resource):
    @api.doc('User Login')
    @api.expect(user_auth, validate=True)
    def post(self):
        """
            Logs a user in, generatnig a JWT to send back to the client.
        """
        post_data = request.json
        return Auth.login(data=post_data)


@api.route('/status')
class UserStatus(Resource):
    @api.doc('Check status of a logged in user')
    def get(self):
        """
            Used by a client to check if they are logged in via JWT and provides user information.
        """
        return Auth.getLoggedInUser(request)


@api.route('/logout')
class LogoutAPI(Resource):
    @api.doc('logout a user')
    def post(self):
        """
            Removes a JWT and logs a user out.
        """
        auth_header = request.headers.get('Authorization')
        return Auth.logout(data=auth_header)