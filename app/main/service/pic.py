import datetime
from sqlalchemy import desc
from app.main import db
from app.main.model.user import User
from app.main.model.pic import Pic

def createPic(data):
    """ Create new post """
    user = data['user']

    if user:
        newPic = Pic(
            title = data['title'],
            description = data['description'],
            image_ext = data['image_ext'],
            image = data['image'],
            user_id = data['user']['user_id']
        )
        db.session.add(newPic)
        db.session.commit()
        response = {
            'status': 'success',
            'message': 'Successfully uploaded'
        }
        return response, 200
    else:
        response = {
            'status': 'fail',
            'message': 'Could not upload pic'
        }
        return response, 400


def viewImage(data):
    """ View image by an ID """
    # ideally we'd generate a GUID for this. 
    return Pic.query.filter_by(pic_id=data['pic_id']).first()

def viewPostsByUser(user):
    """ View posts of a single user sorted by most recent. """
    if user:
        return Pic.query.filter_by(user_id=user.ID).order_by(desc(Pic.created_on)).all()
    else:
        response = {
            'status': 'fail',
            'message': 'User not found.'
        }
        return response, 404

def viewAllPosts():
    """ View all posts sorted by most recent upload datetime stamp. """
    return Pic.query.order_by(desc(Pic.created_on)).all()
