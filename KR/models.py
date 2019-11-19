# sql database sigma   
from . import db
from flask_login import UserMixin
from datetime import datetime

#user sigma
class User(db.Model, UserMixin):
    __tablename__='user' # good practice to specify table name
    id = db.Column(db.Integer, index=True, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String, index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(255), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    def __repr__(self): #string print method
        return "<id:{},name: {}, emailid: {},>".format(self.id,self.name, self.emailid)



#Restaurant sigma
class Restaurant(db.Model, UserMixin):
    __tablename__ = 'restaurant'
    id = db.Column(db.String, primary_key=True)
    image = db.Column(db.String(255))
    title = db.Column(db.String(255))
    mobile = db.Column(db.String(255))
    description = db.Column(db.String(512))
    address = db.Column(db.String(255))
    admin_id = db.Column(db.String, db.ForeignKey('user.name'))

    def __repr__(self): #string print method
        return "<id: {}, image: {}, title: {}, description: {}, address: {}>".format(self.id, self.image, self.title, self.description,self.address)

#comment sigma
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    restaurant_id = db.Column(db.String, db.ForeignKey('restaurant.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.name'))
    comment = db.Column(db.String(512))
    rate = db.Column(db.Integer)
    image = db.Column(db.String(255))
    def __repr__(self): #string print method

         return "<id: {}, date: {},user_id:{},restaurant_id: {},rate{},image:{},comment:{}>".format(self.id, self.date, self.user_id, self.restaurant_id,self.rate,self.image,self.comment)
