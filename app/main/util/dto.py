from flask_restplus import Namespace, fields

"""
    Object mappings for each data model.
"""

class UserDto:
    api = Namespace('user', description='User related operations.')
    user = api.model('User', {
        'user_name': fields.String(required=True, description='The user name'),
        'password': fields.String(required=True, description='The user password'),
    })

class AuthDto:
    api = Namespace('auth', description='User authentication.')
    auth = api.model('Auth', {
        'user_name': fields.String(required=True, description='The user name')
    })

class PicDto:
    api = Namespace('pic', description='Image posts with a title and description.')
    pic = api.model('Image Pic', {
        'image': fields.String(required=True, description='Raw image data, encoded as a string.'), 
        'image_ext': fields.String(required=True, description='Image file extension.'),
        'title': fields.String(required=True, description='Title of the pic.'),
        'description': fields.String(required=True, description='Description of the pic.'),
        'user_name': fields.String(description='User name of the submitter'),
        'created_on': fields.DateTime(description='When the image was posted')
    })
