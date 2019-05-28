import datetime
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from .. import db

class Pic(db.Model):
    """ Image Post (Picture/Pic) model """
    __tablename__ = "image_pic"

    pic_id =        Column(Integer, primary_key=True, autoincrement=True) # would normally declare this int as unsigned to be pedantic but I don't believe SQLite3 supports this. 
    user_id =       Column(Integer, ForeignKey("user.user_id"))
    
    title =         Column(Text(convert_unicode=True), nullable=False)
    description =   Column(Text(convert_unicode=True), nullable=False)

    image =         Column(Text(convert_unicode=True), nullable=False) # ideally we'd just store a URL here, and use a service like S3 to store the image data.
    image_ext =     Column(String(15), nullable=False)
   
    # for most tables, I always add created_on / updated_on timestamps.
    created_on =    Column(DateTime, default=datetime.datetime.utcnow)
    updated_on =    Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow)


    # This field is populated on user joins
    @property 
    def user_name(self):
        return self.user.user_name

    def __repr__(self):
        return "Image Pic: {} {}".format(self.pic_id, self.user.user_name)

    