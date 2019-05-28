import datetime
from app.main import db
from app.main.model.user import User


def create(data):
    """ Create a new User """
    user = User.query.filter_by(user_name = data['user_name']).first()

    if not user:
        newUser = User(
            user_name =         data['user_name'],
            password =          data['password']
        )
        save(newUser)
        response = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response, 201
    else:
        response = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response, 409


def findAll():
    """ Get all users in table """
    return User.query.all()


def findByUserName(userName):
    """ Get a user by user name """
    return User.query.filter_by(user_name=userName).first()


def save(data):
    """ Save to DB """
    db.session.add(data)
    db.session.commit()
