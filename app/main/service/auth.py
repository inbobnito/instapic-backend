from app.main.model.user import User

class Auth:
    """
        Helper methods for Authentication
    """

    @staticmethod
    def login(data):
        """ Generate JWT for a user, effectively logging them in. """
        try:
            # query by user name
            user = User.query.filter_by(user_name=data.get('user_name')).first()
            if user and user.checkPassword(data.get('password')):
                # generate JWT
                auth_token = user.encodeAuthToken(user.user_id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'username or password does not match.'
                }
                return response_object, 401
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout(data):
        if data:
            resp = User.decodeAuthToken(data)
            if not isinstance(resp, str):
                return {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def getLoggedInUser(request):
        """ Gets user information from a JWT """
        # get the auth token
        authToken = request.headers.get('Authorization')
        if authToken:
            resp = User.decodeAuthToken(authToken)
            if not isinstance(resp, str):
                # fetch user info from decoded JWT
                user = User.query.filter_by(user_id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.user_id,
                        'user_name': user.user_name,
                        'created_on': str(user.created_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401