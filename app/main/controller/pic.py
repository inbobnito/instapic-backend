from flask import request
from flask_restplus import Resource

from ..util.dto import PicDto
from ..service.pic import createPic, viewAllPosts, viewPostsByUser, viewImage
from ..service.user import findByUserName
from ..service.auth import Auth
from ..util.decorator import token_required

api = PicDto.api
_pic = PicDto.pic

"""
Pic (Image Posts) controller
"""

@api.route('/')
class ImagePostUpload(Resource):
    @api.doc('Get all image posts')
    @api.marshal_list_with(_pic, envelope='data')
    def get(self):
        """ View all images """
        return viewAllPosts()

    @api.response(200, 'Image successfully posted.')
    @api.doc('Create a new pic')
    @token_required
    @api.expect(_pic, validate=True)
    def post(self):
        """ Upload a new Pic (Image Post) """
        data = request.json
        userData, status = Auth.getLoggedInUser(request)
        data['user'] = userData.get('data')
        return createPic(data=data)

@api.route('/<username>')
@api.param('username', 'Fetch all images by user name')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('Get image post by user name')
    @api.marshal_list_with(_pic, envelope='data')
    def get(self, username):
        """ Get an image post by a user """
        user = findByUserName(username)
        if not user:
            api.abort(404)
        return viewPostsByUser(user)