import datetime
import jwt
from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.orm import relationship
from .. import db, flaskBrcypt
from ..config import key

class User(db.Model):
    """ User model """
    __tablename__ = "user"

    user_id =       Column(Integer, primary_key=True, autoincrement=True) # would normally declare this int as unsigned to be pedantic but I don't believe SQLite3 supports this. 
    user_name =     Column(Text(convert_unicode=True), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False) # just my convention, TEXT is a pointer under the hood, like to allocate the entire field for senesitive data. 
    
    # for most tables, I always add created_on / updated_on timestamps.
    created_on =    Column(DateTime, default=datetime.datetime.utcnow)
    updated_on =    Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow)

    pics = relationship("Pic", backref="user")

    # get User ID

    @property
    def ID(self):
        return self.user_id

    # password encryption logic.

    @property
    def password(self):
        raise AttributeError('password is write-only.')

    @password.setter
    def password(self, password):
        self.password_hash = flaskBrcypt.generate_password_hash(password).decode('utf-8')

    def checkPassword(self, password):
        return flaskBrcypt.check_password_hash(self.password_hash, password)

    # JWT generation

    def encodeAuthToken(self, userId):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': userId
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod  
    def decodeAuthToken(authToken):
        try:
            payload = jwt.decode(authToken, key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "User: {} | ID {}".format(self.user_name, self.user_id)

    