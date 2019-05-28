from functools import wraps
from flask import request
from app.main.service.auth import Auth


""" Check the validity of a JWT from the client to avoid anyone making requests """
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.getLoggedInUser(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated